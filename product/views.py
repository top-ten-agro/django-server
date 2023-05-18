
from rest_framework import viewsets, permissions, pagination
from .serializers import ProductSerializer
from .models import Product


class ProductPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class ProductViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(published=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductPagination
    filterset_fields = ('stores', 'name', 'pack_size')
    ordering_fields = ('name', 'created-at',)
