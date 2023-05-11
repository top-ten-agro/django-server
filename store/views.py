from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Store, StoreRole, Balance
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

    @action(detail=True)
    def stock(self, request, *args, **kwargs):
        store = Store.objects.get(pk=self.kwargs.get("pk"))
        products = store.stock_set.all()
        serializer = StoreProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def customers(self, request, *args, **kwargs):
        store = Store.objects.get(pk=self.kwargs.get("pk"))
        products = store.stock_set.all()
        serializer = StoreProductSerializer(products, many=True)
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
    ordering_fields = ('customer', 'cash_in', 'revenue', 'created_at')

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
            queryset = queryset.filter(customer__name__startswith=name)

        if phone is not None:
            queryset = queryset.filter(customer__phone__startswith=phone)

        return queryset
