from rest_framework import permissions
from .models import StoreRole


class HasRestockPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        storeRole = StoreRole.objects.filter(
            user=request.user, store=obj.store).first()

        if (storeRole == None):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if (storeRole.role == StoreRole.Role.DIRECTOR):
            return request.method in ['PUT', 'PATCH', 'DELETE']

        return storeRole.role == StoreRole.Role.MANAGER and obj.created_by == request.user
