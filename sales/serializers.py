from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Order, OrderItem, Transaction, Restock, RestockItem
from customer.serializers import CustomerSerializer

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'rate',)


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id',)


class OrderSerializer(FlexFieldsModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        expandable_fields = {
            'created_by': (CreatedBySerializer),
            'customer': (CustomerSerializer, {'fields': ['id', 'name']})
        }

    def create(self, validated_data):
        amount = 0
        validated_data.pop('amount')
        items_data = validated_data.pop('items')
        for item in items_data:
            amount += item.get('rate') * item.get('quantity')

        order = Order.objects.create(**validated_data, amount=amount)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order

    def update(self, instance, validated_data):
        amount = 0
        items_data = validated_data.pop('items')

        for item in items_data:
            print(item.get('rate') * item.get('quantity'))
            amount += item.get('rate') * item.get('quantity')

        instance.amount = amount
        OrderItem.objects.filter(order=instance).delete()

        for item in items_data:
            OrderItem.objects.create(order=instance, **item)
        return instance


class TransactionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        expandable_fields = {
            'created_by': (CreatedBySerializer),
            'customer': (CustomerSerializer, {'fields': ['id', 'name']})
        }


class RestockItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestockItem
        fields = ('id', 'product', 'quantity',)


class RestockSerializer(FlexFieldsModelSerializer):
    items = RestockItemSerializer(many=True)

    class Meta:
        model = Restock
        fields = '__all__'
        expandable_fields = {
            'created_by': (CreatedBySerializer, {'many': False})
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        restock = Restock.objects.create(**validated_data)
        for item_data in items_data:
            RestockItem.objects.create(restock=restock, **item_data)
        return restock

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.approved = validated_data.get('approved', False)
        RestockItem.objects.filter(restock=instance).delete()
        for item_data in items_data:
            RestockItem.objects.create(restock=instance, **item_data)
        return instance
