from django.db.models import F
from django.db import transaction
from rest_framework import viewsets, permissions, pagination, status
from django_filters import rest_framework as dj_filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import OrderSerializer, TransactionSerializer, RestockSerializer
from .models import Order, OrderItem, Transaction, Restock, RestockItem
from store.permissions import HasRestockPermission, HasOrderPermission
from store.models import Stock, Balance


class Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = Pagination
    permission_classes = (permissions.IsAuthenticated, HasOrderPermission,)
    filterset_fields = ('store', 'customer', 'created_by', 'approved')
    ordering_fields = ('created_at', 'approved', 'created_by',)

    def get_queryset(self):
        return self.queryset.filter(store__employees=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        email = self.request.query_params.get("created_by.email", None)
        if email is not None:
            queryset = queryset.filter(created_by__email__startswith=email)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        order = self.get_object()
        if order.approved == True:
            return Response({"message": "Restock already approved."}, status=status.HTTP_403_FORBIDDEN)
        order.approved = True
        items = OrderItem.objects.filter(order=order)

        with transaction.atomic():
            order.save(update_fields=['approved'])
            Balance.objects.filter(store=order.store, customer=order.customer).update(
                revenue=F('revenue')+order.amount)
            for item in items:
                Stock.objects.filter(product=item.product, store=order.store).update(
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
            Balance.objects.filter(store=order.store, customer=order.customer).update(
                revenue=F('revenue')-order.amount)
            for item in items:
                Stock.objects.filter(product=item.product, store=order.store).update(
                    quantity=F('quantity')+item.quantity)
            order.delete()

        return Response({"success": True})


class TransactionViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('store', 'customer', 'created_by',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RestockViewset(viewsets.ModelViewSet):
    serializer_class = RestockSerializer
    pagination_class = Pagination
    permission_classes = (permissions.IsAuthenticated, HasRestockPermission,)
    filterset_fields = ['created_by', 'store', 'approved', 'id']
    ordering_fields = ('created_at', 'approved', 'created_by',)

    def get_queryset(self):
        return Restock.objects.filter(store__employees=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        approved = serializer.validated_data.get("approved", False)
        if approved == True:
            return Response({"message": "Restock already approved."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        email = self.request.query_params.get("created_by.email", None)
        if email is not None:
            queryset = queryset.filter(created_by__email__startswith=email)
        return queryset

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        restock = self.get_object()
        if restock.approved == True:
            return Response({"message": "Restock already approved."}, status=status.HTTP_403_FORBIDDEN)
        restock.approved = True
        restock_items = RestockItem.objects.filter(restock=restock)

        with transaction.atomic():
            restock.save(update_fields=['approved'])
            for item in restock_items:
                stock, created = Stock.objects.get_or_create(
                    store=restock.store, product=item.product,  defaults={
                        "quantity": item.quantity
                    })
                if not created:
                    stock.quantity += item.quantity
                    stock.save(update_fields=['quantity',])

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
                Stock.objects.filter(store=restock.store, product=item.product).update(
                    quantity=F('quantity')-item.quantity)
            restock.delete()
        return Response({"success": True})
