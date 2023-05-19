from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from rest_framework import viewsets, pagination
from rest_framework.decorators import action
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
