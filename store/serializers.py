from rest_framework import serializers
from .models import Store, StoreRole, Stock, Balance
from product.serializers import ProductSerializer
from customer.serializers import CustomerSerializer


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name", "address", "created_at", "updated_at",)


class StoreRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRole
        fields = "__all__"


class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Balance
        fields = '__all__'
