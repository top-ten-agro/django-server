from rest_framework import serializers
from .models import Store, StoreRole


class StoreRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRole
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"
