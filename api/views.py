from functools import reduce
from datetime import timedelta
from django.utils import timezone
from django.core import serializers
from django.db.models import Sum, Q
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from rest_framework import serializers, viewsets, views, permissions, response
from rest_framework.decorators import action
from product.models import Product
from customer.models import Customer
from depot.models import Depot, DepotRole, Stock
from sales.models import Transaction, Order


class HomepageView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        duration = request.query_params.get('days', "30")
        today = timezone.now()
        from_date = today - timedelta(days=int(duration))

        products = Product.objects.filter(published=True)
        customers = Customer.objects.all()
        depots = Depot.objects.all()
        stock = Stock.objects.aggregate(total=Sum('quantity'))['total']
        my_roles = DepotRole.objects.filter(user=self.request.user)

        officers = [
            role.user for role in my_roles if role.role == DepotRole.Role.OFFICER]
        other_roles = [
            role.depot for role in my_roles if role.role != DepotRole.Role.OFFICER]

        trx_query = Transaction.objects.filter(approved=True).filter(
            created_at__gte=from_date, created_at__lte=today)
        order_query = Order.objects.filter(approved=True).filter(
            created_at__gte=from_date, created_at__lte=today)

        transactions = trx_query.filter(
            created_by__in=officers) | trx_query.filter(depot__in=other_roles)
        orders = order_query.filter(
            created_by__in=officers) | order_query.filter(balance__depot__in=other_roles)

        transactions = transactions.values("created_at__date").annotate(
            total_cash_in=Sum('cash_in'), total_cash_out=Sum('cash_out'))
        orders = orders.values("created_at__date").annotate(sales=Sum('total'))

        return response.Response({
            "products": products.count(),
            "customers": customers.count(),
            "depots": depots.count(),
            "stock": stock,
            "orders": orders,
            "transactions": transactions,

        })


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class BackupRestoreViewset(viewsets.ViewSet):
    serializer_class = FileUploadSerializer

    def get_queryset(self, request):
        if not request.pk:
            raise PermissionDenied("List methods not allowed.")

        if request.pk == 'products':
            return Product.objects.all()

        if request.pk == 'customers':
            return Customer.objects.all()

        raise PermissionDenied("provided model is unavailable.")

    def retrive(self, request, pk=None):
        queryset = self.get_queryset()
        serialized_data = serializers.serialize('json', queryset)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        filename = f"{pk}_backup_{timestamp}.json"
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(serialized_data)
        return response

    @action(detail=True, methods=['post'])
    def restore_products(self, request):
        pass

    @action(detail=True, methods=['get'])
    def backup_customers(self, request):
        queryset = Customer.objects.all()
        serialized_data = serializers.serialize('json', queryset)
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        filename = f"customers_backup_{timestamp}.json"
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(serialized_data)
        return response
