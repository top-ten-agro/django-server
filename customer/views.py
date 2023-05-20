from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Sum
from django.core import serializers
from django.http import HttpResponse
from rest_framework import viewsets, pagination, response
from rest_framework.decorators import action
from rest_flex_fields import FlexFieldsModelViewSet
from .models import Customer
from sales.models import Transaction, Order
from depot.models import Balance, DepotRole
from depot.serializers import BalanceSerializer
from .serializers import CustomerSerializer


class CustomersPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class CustomerViewset(FlexFieldsModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomersPagination
    ordering_fields = ('created_at', )
    filterset_fields = ('name', 'phone', 'depots',)

    @action(detail=False, methods=['get'])
    def backup(self, request):
        queryset = self.get_queryset()
        serialized_data = serializers.serialize('json', queryset)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"customer_backup_{timestamp}.json"
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(serialized_data)
        return response

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

        trx_query = Transaction.objects.filter(
            approved=True, balance__isnull=False).filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)
        order_query = Order.objects.filter(approved=True).filter(
            created_at__date__gte=from_date, created_at__date__lte=to_date)

        transactions = trx_query.filter(
            created_by__in=officers) | trx_query.filter(depot__in=other_roles)
        orders = order_query.filter(
            created_by__in=officers) | order_query.filter(balance__depot__in=other_roles)
        print(orders, transactions)
        transactions = transactions.values("balance").annotate(
            total_cash_in=Sum('cash_in'), total_cash_out=Sum('cash_out'))
        orders = orders.values("balance").annotate(sales=Sum('total'))

        return response.Response({
            "transactions": transactions,
            "orders": orders,
        })
