from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Store, StoreRole, Stock, Balance
from user.serializers import UserSerializer
from product.serializers import ProductSerializer
from customer.serializers import CustomerSerializer


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name", "address", "created_at", "updated_at",)


class StoreRoleSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = StoreRole
        fields = "__all__"
        expandable_fields = {
            'user': (UserSerializer, {'fields': ('id', 'first_name', 'last_name', 'email')})
        }


class StoreProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class BalanceSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Balance
        fields = '__all__'
        expandable_fields = {
            'customer': (CustomerSerializer,),
            'officer': (StoreRoleSerializer, {'fields': ('id', 'user.email', 'user.id',)})
        }
