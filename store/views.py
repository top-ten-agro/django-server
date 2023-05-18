from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Store, StoreRole, Balance, Stock
from .serializers import StoreSerializer, StoreRoleSerializer, StoreProductSerializer, BalanceSerializer


class StoreViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Store.objects.filter(employees=self.request.user)

    @action(detail=True)
    def roles(self, request, *args, **kwargs):
        roles = StoreRole.objects.filter(store=self.kwargs.get("pk"))
        serializer = StoreRoleSerializer(roles, many=True)
        return Response(serializer.data)


class StoreRoleViewset(viewsets.ReadOnlyModelViewSet):
    queryset = StoreRole.objects.all()
    serializer_class = StoreRoleSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("store",)

    def get_queryset(self):
        return StoreRole.objects.filter(user=self.request.user)


class BalancePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class BalanceViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = BalanceSerializer
    pagination_class = BalancePagination
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('customer', 'store', 'id')
    ordering_fields = ('customer', 'cash_in', 'sales', 'created_at')

    def get_queryset(self):
        employee = Balance.objects.filter(store__employees=self.request.user)
        return employee

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        customer_id = self.request.query_params.get("customer.id", None)
        name = self.request.query_params.get("customer.name", None)
        phone = self.request.query_params.get("customer.phone", None)

        if customer_id is not None:
            queryset = queryset.filter(customer=customer_id)

        if name is not None:
            queryset = queryset.filter(customer__name__istartswith=name)

        if phone is not None:
            queryset = queryset.filter(customer__phone__istartswith=phone)

        return queryset


class StockPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class StockViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.filter(product__published=True)
    serializer_class = StoreProductSerializer
    pagination_class = StockPagination
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('store', 'id')
    ordering_fields = ('product__price', 'product__name',
                       'product__pack_size', 'quantity',)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        product_id = self.request.query_params.get("product.id", None)
        name = self.request.query_params.get("product.name", None)
        size = self.request.query_params.get("product.pack_size", None)

        if product_id is not None:
            queryset = queryset.filter(product=product_id)

        if name is not None:
            queryset = queryset.filter(product__name__istartswith=name)

        if size is not None:
            queryset = queryset.filter(product__pack_size__istartswith=size)

        return queryset

    def get_queryset(self):
        return self.queryset.filter(store__employees=self.request.user)
