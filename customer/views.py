from django.db.models import Prefetch
from rest_framework import viewsets, pagination
from rest_flex_fields import FlexFieldsModelViewSet, is_expanded
from .models import Customer
from .serializers import CustomerSerializer
from store.models import Balance


class CustomersPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class CustomerViewset(FlexFieldsModelViewSet):
    permit_list_expands = ['balances']
    serializer_class = CustomerSerializer
    pagination_class = CustomersPagination

    def get_queryset(self):
        queryset = Customer.objects.all()
        store = self.request.query_params.get('store', None)
        print(store)
        if is_expanded(self.request, 'balances') and store is not None:
            queryset = queryset.prefetch_related(
                Prefetch('balances', queryset=Balance.objects.filter(store=store))).filter(stores=store)

        elif store is not None:
            queryset = queryset.filter(stores=store)
        return queryset
