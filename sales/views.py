from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import F, Sum
from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, permissions, pagination, status
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import OrderSerializer, TransactionSerializer, RestockSerializer
from .models import Order, OrderItem, Transaction, Restock, RestockItem
from depot.permissions import HasRestockPermission, HasOrderPermission
from depot.models import Stock, DepotRole


class Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = Pagination
    permission_classes = (permissions.IsAuthenticated, HasOrderPermission,)
    filterset_fields = ('balance', 'balance__depot',
                        'balance__officer',  'created_by', 'approved')
    ordering_fields = ('created_at', 'approved', 'total', 'created_by',)

    def get_queryset(self):
        return self.queryset.filter(balance__depot__employees=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        createdby_name = self.request.query_params.get("created_by.name", None)
        if createdby_name is not None:
            queryset = queryset.filter(
                created_by__name__istartswith=createdby_name)

        name = self.request.query_params.get("balance.customer.name", None)
        if name is not None:
            queryset = queryset.filter(
                balance__customer__name__istartswith=name)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        approved = serializer.validated_data.get("approved", False)
        if approved == True:
            raise ValidationError(
                'This row is immutable and cannot be updated.')
        serializer.save()

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        order = self.get_object()
        if order.approved == True:
            return Response({"message": "Order already approved."}, status=status.HTTP_403_FORBIDDEN)
        order.approved = True
        order.approved_by = request.user
        order.approved_at = timezone.now()
        items = OrderItem.objects.filter(order=order)

        with transaction.atomic():
            order.save(update_fields=['approved',
                       'approved_at', 'approved_by'])
            order.balance.sales = F('sales') + order.total
            order.balance.save()
            for item in items:
                Stock.objects.filter(product=item.product, depot=order.balance.depot).update(
                    quantity=F('quantity')-item.quantity)

        return Response({"success": True})

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        order = self.get_object()

        if order.approved == False:
            order.delete()
            return Response({"success": True})

        items = OrderItem.objects.filter(order=order)

        with transaction.atomic():
            order.balance.sales = F('sales') - order.total
            order.balance.save()
            for item in items:
                Stock.objects.filter(product=item.product, depot=order.balance.depot).update(
                    quantity=F('quantity')+item.quantity)
            order.delete()

        return Response({"success": True})

    @action(detail=False, methods=['get'])
    def statement(self, request):
        to_date = request.query_params.get(
            'to', timezone.now().strftime('%Y-%m-%d'))
        from_date = request.query_params.get(
            'from', (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        my_roles = DepotRole.objects.filter(user=self.request.user)

        officers = [
            role.user for role in my_roles if role.role == DepotRole.Role.OFFICER]
        other_roles = [
            role.depot for role in my_roles if role.role != DepotRole.Role.OFFICER]

        orders = Order.objects.filter(approved=True).filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)
        orders = orders.filter(
            created_by__in=officers) | orders.filter(balance__depot__in=other_roles)

        serializer = OrderSerializer(
            orders, many=True, context={"request": request})
        return Response(serializer.data)


class TransactionViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = Pagination
    filterset_fields = ('depot', 'balance', 'balance__officer', 'created_by',
                        'id', 'approved', 'title', 'category',)
    ordering_fields = ('balance', 'category', 'created_by',
                       'id', 'approved', 'cash_in', 'cash_out')

    def get_queryset(self):
        return self.queryset.filter(depot__employees=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        email = self.request.query_params.get("created_by.email", None)
        if email is not None:
            queryset = queryset.filter(
                created_by__email__istartswith=email)
        name = self.request.query_params.get("balance.customer.name", None)
        if name is not None:
            queryset = queryset.filter(
                balance__customer__name__istartswith=name)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        approved = serializer.validated_data.get("approved", False)
        if approved == True:
            raise ValidationError(
                'This row is immutable and cannot be updated.')
        serializer.save()

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        txn = self.get_object()
        if txn.approved == True:
            return Response({"message": "Transaction already approved."}, status=status.HTTP_403_FORBIDDEN)
        txn.approved = True
        txn.approved_by = request.user
        txn.approved_at = timezone.now()

        if txn.balance is None:
            txn.save(update_fields=['approved', 'approved_at', 'approved_by'])
            return Response({"success": True})

        with transaction.atomic():
            txn.save(update_fields=['approved', 'approved_at', 'approved_by'])
            txn.balance.cash_in = F('cash_in') + txn.cash_in - txn.cash_out
            txn.balance.save()
        return Response({"success": True})

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        txn = self.get_object()

        if txn.approved == False or txn.balance is None:
            txn.delete()
            return Response({"success": True})

        with transaction.atomic():
            txn.balance.cash_in = F('cash_in') - txn.cash_in + txn.cash_out
            txn.balance.save()
            txn.delete()

        return Response({"success": True})

    @action(detail=False, methods=['get'])
    def statement(self, request):
        to_date = request.query_params.get(
            'to', timezone.now().strftime('%Y-%m-%d'))
        from_date = request.query_params.get(
            'from', (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        my_roles = DepotRole.objects.filter(user=self.request.user)

        officers = [
            role.user for role in my_roles if role.role == DepotRole.Role.OFFICER]
        other_roles = [
            role.depot for role in my_roles if role.role != DepotRole.Role.OFFICER]

        trxs = Transaction.objects.filter(approved=True).filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)
        trxs = trxs.filter(
            created_by__in=officers) | trxs.filter(depot__in=other_roles)

        serializer = TransactionSerializer(
            trxs, many=True, context={"request": request})
        return Response(serializer.data)


class RestockViewset(viewsets.ModelViewSet):
    serializer_class = RestockSerializer
    pagination_class = Pagination
    permission_classes = (permissions.IsAuthenticated, HasRestockPermission,)
    filterset_fields = ['created_by', 'depot', 'approved', 'id']
    ordering_fields = ('created_at', 'approved', 'created_by',)

    def get_queryset(self):
        return Restock.objects.filter(depot__employees=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        email = self.request.query_params.get("created_by.email", None)
        if email is not None:
            queryset = queryset.filter(created_by__email__istartswith=email)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        approved = serializer.validated_data.get("approved", False)
        if approved == True:
            raise ValidationError(
                'This row is immutable and cannot be updated.')
        serializer.save()

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        restock = self.get_object()
        if restock.approved == True:
            return Response({"message": "Restock already approved."}, status=status.HTTP_403_FORBIDDEN)
        restock.approved = True
        restock.approved_by = request.user
        restock.approved_at = timezone.now()
        restock_items = RestockItem.objects.filter(restock=restock)

        with transaction.atomic():
            restock.save(update_fields=['approved',
                         'approved_at', 'approved_by'])
            for item in restock_items:
                stock, created = Stock.objects.get_or_create(
                    depot=restock.depot, product=item.product, defaults={
                        "quantity": item.quantity
                    })
                if not created and item.quantity > 0:
                    stock.quantity += item.quantity
                    stock.save(update_fields=['quantity',])
                if item.quantity == 0:
                    item.delete()

        return Response({"success": True})

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        restock = self.get_object()

        if restock.approved == False:
            restock.delete()
            return Response({"success": True})

        restock_items = RestockItem.objects.filter(restock=restock)

        with transaction.atomic():
            for item in restock_items:
                Stock.objects.filter(depot=restock.depot, product=item.product).update(
                    quantity=F('quantity')-item.quantity)
            restock.delete()
        return Response({"success": True})
