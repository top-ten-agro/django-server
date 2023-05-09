from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Order, OrderItem, Transaction, Restock, RestockItem


User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'rate',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class RestockItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestockItem
        fields = ('product', 'quantity', )


class StockCreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id',)


class RestockSerializer(FlexFieldsModelSerializer):
    items = RestockItemSerializer(many=True)

    class Meta:
        model = Restock
        fields = '__all__'
        expandable_fields = {
            'created_by': (StockCreatedBySerializer, {'many': False})
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        restock = Restock.objects.create(**validated_data)
        for item_data in items_data:
            RestockItem.objects.create(restock=restock, **item_data)
        return restock
