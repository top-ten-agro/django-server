from rest_framework import viewsets, permissions, pagination
from django_filters import rest_framework as dj_filters
from .serializers import OrderSerializer, TransactionSerializer, RestockSerializer
from .models import Order, Transaction, Restock


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('store', 'customer', 'created_by',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TransactionViewset(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('store', 'customer', 'created_by',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# class RestockFilter(dj_filters.FilterSet):
#     max_creatted = dj_filters.DateTimeFilter(
#         field_name='created_at', label="Date Range")

#     class Meta:
#         model = Restock
#         fields = ['created_by', 'created_at', 'store', 'approved',]


class RestockPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'


class RestockViewset(viewsets.ModelViewSet):
    queryset = Restock.objects.all()
    serializer_class = RestockSerializer
    pagination_class = RestockPagination
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ['created_by', 'store', 'approved', 'id']
    ordering_fields = ('created_at', 'approved', 'created_by',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        email = self.request.query_params.get("created_by.email", None)

        if email is not None:
            print(email)
            queryset = queryset.filter(created_by__email__startswith=email)

        return queryset
