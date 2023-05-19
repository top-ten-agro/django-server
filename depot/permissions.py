from rest_framework import permissions
from .models import DepotRole


class HasRestockPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        depotRole = DepotRole.objects.filter(
            user=request.user, depot=obj.depot).first()

        if (depotRole == None):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if (depotRole.role == DepotRole.Role.DIRECTOR):
            return request.method in ['PUT', 'PATCH', 'DELETE']

        return depotRole.role == DepotRole.Role.MANAGER and obj.created_by == request.user


class HasOrderPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        depotRole = DepotRole.objects.filter(
            user=request.user, depot=obj.depot).first()

        if (depotRole == None):
            return False

        if request.method in permissions.SAFE_METHODS and depotRole.role != DepotRole.Role.OFFICER:
            return True

        if (depotRole.role == DepotRole.Role.MANAGER):
            return request.method in ['PUT', 'PATCH', 'DELETE']

        return depotRole.role == DepotRole.Role.OFFICER and obj.created_by == request.user


class HasBalancePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        depotRole = DepotRole.objects.filter(
            user=request.user, depot=obj.depot).first()

        if (depotRole == None):
            return False

        if request.method in permissions.SAFE_METHODS and depotRole.role != DepotRole.Role.OFFICER:
            return True

        if request.method == 'PATCH' and depotRole.role == DepotRole.Role.MANAGER:
            return True

        return depotRole.role == DepotRole.Role.OFFICER and obj.officer == depotRole
