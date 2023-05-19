from django.db.models import Q, Prefetch
from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Depot, DepotRole, Balance, Stock
from .serializers import DepotSerializer, DepotRoleSerializer, DepotProductSerializer, BalanceSerializer
from .permissions import HasBalancePermission


class DepotViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = DepotSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Depot.objects.filter(employees=self.request.user)

    @action(detail=True)
    def roles(self, request, *args, **kwargs):
        roles = DepotRole.objects.filter(depot=self.kwargs.get("pk"))
        serializer = DepotRoleSerializer(
            roles, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True)
    def customers(self, request, *args, **kwargs):
        query = Balance.objects.filter(depot=self.kwargs.get("pk"))
        role = DepotRole.objects.filter(
            depot=self.kwargs.get("pk"), user=self.request.user).first()
        if role is None:
            return Response({"message": "Forbidden"}, status=400,)
        if role.role == DepotRole.Role.OFFICER:
            query = query.filter(officer=role)
        serializer = BalanceSerializer(
            query, many=True, context={"request": request})
        return Response(serializer.data)


class DepotRoleViewset(viewsets.ReadOnlyModelViewSet):
    queryset = DepotRole.objects.all()
    serializer_class = DepotRoleSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("depot",)

    def get_queryset(self):
        return DepotRole.objects.filter(user=self.request.user)


class BalancePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"


class BalanceViewset(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    pagination_class = BalancePagination
    permission_classes = (IsAuthenticated, HasBalancePermission,)
    filterset_fields = ('customer', 'depot', 'id', 'officer')
    ordering_fields = ('customer', 'cash_in', 'sales', 'created_at')

    def get_queryset(self):
        employee = Balance.objects.filter(depot__employees=self.request.user)
        return employee

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        customer_id = self.request.query_params.get("customer.id", None)
        name = self.request.query_params.get("customer.name", None)
        phone = self.request.query_params.get("customer.phone", None)
        officer = self.request.query_params.get("officer", None)

        if officer is not None:
            queryset = queryset.filter(officer=officer)

        if customer_id is not None:
            queryset = queryset.filter(customer=customer_id)

        if name is not None:
            queryset = queryset.filter(customer__name__istartswith=name)

        if phone is not None:
            queryset = queryset.filter(customer__phone__istartswith=phone)

        return queryset


class StockPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"


class StockViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.filter(product__published=True)
    serializer_class = DepotProductSerializer
    pagination_class = StockPagination
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('depot', 'id')
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
        return self.queryset.filter(depot__employees=self.request.user)
