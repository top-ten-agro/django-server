from rest_framework import viewsets
from .models import Store
from .serializers import StoreSerializer


class StoreViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
