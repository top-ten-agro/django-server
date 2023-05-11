from rest_framework import viewsets, pagination
from rest_flex_fields import FlexFieldsModelViewSet
from .models import Customer
from .serializers import CustomerSerializer


class CustomersPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class CustomerViewset(FlexFieldsModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = CustomersPagination
    ordering_fields = ('created_at', )
    filterset_fields = ('name', 'phone', 'stores',)
