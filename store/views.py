from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Store, StoreRole
from .serializers import StoreSerializer, StoreRoleSerializer


class StoreViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    @action(detail=True)
    def roles(self, request, *args, **kwargs):
        roles = StoreRole.objects.filter(store=self.kwargs.get("pk"))
        serializer = StoreRoleSerializer(roles, many=True)
        return Response(serializer.data)


class StoreRoleViewset(viewsets.ReadOnlyModelViewSet):
    queryset = StoreRole.objects.all()
    serializer_class = StoreRoleSerializer
