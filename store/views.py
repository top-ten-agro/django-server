from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Store, StoreRole
from .serializers import StoreSerializer, StoreRoleSerializer


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
