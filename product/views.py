from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import F, Sum
from rest_framework import viewsets, permissions, pagination, response
from rest_framework.decorators import action
from .serializers import ProductSerializer
from .models import Product
from sales.models import OrderItem


class ProductPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class ProductViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(published=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ProductPagination
    filterset_fields = ('depots', 'name', 'pack_size')
    ordering_fields = ('name', 'created-at',)

    @action(detail=False, methods=['get'])
    def statement(self, request):
        to_date = request.query_params.get(
            'to', timezone.now().strftime('%Y-%m-%d'))
        from_date = request.query_params.get(
            'from', (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'))

        query = OrderItem.objects\
            .filter(
                order__approved=True,
                order__created_at__date__gte=timezone.make_aware(
                    datetime.strptime(from_date, '%Y-%m-%d')),
                order__created_at__date__lte=timezone.make_aware(
                    datetime.strptime(to_date, '%Y-%m-%d'))
            )\
            .values('product',).annotate(total=Sum('quantity'))

        return response.Response(query)
