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


class HasOrderPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        storeRole = StoreRole.objects.filter(
            user=request.user, store=obj.store).first()

        if (storeRole == None):
            return False

        if request.method in permissions.SAFE_METHODS and storeRole.role != StoreRole.Role.OFFICER:
            return True

        if (storeRole.role == StoreRole.Role.MANAGER):
            return request.method in ['PUT', 'PATCH', 'DELETE']

        return storeRole.role == StoreRole.Role.OFFICER and obj.created_by == request.user


class HasBalancePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        storeRole = StoreRole.objects.filter(
            user=request.user, store=obj.store).first()

        if (storeRole == None):
            return False

        if request.method in permissions.SAFE_METHODS and storeRole.role != StoreRole.Role.OFFICER:
            return True

        if request.method == 'PATCH' and storeRole.role == StoreRole.Role.MANAGER:
            return True

        return storeRole.role == StoreRole.Role.OFFICER and obj.officer == storeRole
