from datetime import datetime
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from product.models import Product
from customer.models import Customer


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
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
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
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"customers_backup_{timestamp}.json"
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write(serialized_data)
        return response
