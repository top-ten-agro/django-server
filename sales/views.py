from rest_framework import viewsets, permissions
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


class RestockViewset(viewsets.ModelViewSet):
    queryset = Restock.objects.all()
    serializer_class = RestockSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('store', 'created_by',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
