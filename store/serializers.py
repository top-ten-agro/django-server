from rest_framework import serializers
from .models import Store, StoreRole, Stock
from product.serializers import ProductSerializer


class StoreRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRole
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name", "address", "created_at", "updated_at",)


class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'
