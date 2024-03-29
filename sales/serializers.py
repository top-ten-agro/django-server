from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Order, OrderItem, Transaction, Restock, RestockItem
from depot.serializers import BalanceSerializer, DepotSerializer

User = get_user_model()


class OrderItemSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'rate',)
        expandable_fields = {
            'product': ('product.serializers.ProductSerializer', {
                'fields': ('id', 'name', 'unit', 'price', 'pack_size',
                           )})
        }


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'name', )


class OrderSerializer(FlexFieldsModelSerializer):
    total = serializers.ReadOnlyField()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        expandable_fields = {
            'created_by': (CreatedBySerializer),
            'balance': (BalanceSerializer, {
                'fields': ['id', 'depot', 'customer.id', 'customer.name', 'customer.address', 'cash_in', 'sales']
            }),
            'items': (OrderItemSerializer, {'many': True}),
        }

    def create(self, validated_data):
        subtotal = 0
        validated_data.pop('subtotal')
        items_data = validated_data.pop('items')
        for item in items_data:
            subtotal += item.get('rate') * item.get('quantity')

        with transaction.atomic():
            order = Order.objects.create(**validated_data, subtotal=subtotal)
            for item in items_data:
                OrderItem.objects.create(order=order, **item)

        return order

    def update(self, instance, validated_data):
        subtotal = 0
        items_data = validated_data.pop('items')
        commission = validated_data.pop('commission')

        for item in items_data:
            subtotal += item.get('rate') * item.get('quantity')

        instance.subtotal = subtotal
        instance.commission = commission

        with transaction.atomic():
            OrderItem.objects.filter(order=instance).delete()
            for item in items_data:
                OrderItem.objects.create(order=instance, **item)
            instance.save()

        return instance


class TransactionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        expandable_fields = {
            'created_by': (CreatedBySerializer,),
            'balance': (BalanceSerializer, {
                'fields': ['id', 'depot', 'customer.id', 'customer.name', 'customer.address']
            }),
            'depot': (DepotSerializer, {'fields': ['id', 'name']})
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
        with transaction.atomic():
            restock = Restock.objects.create(**validated_data)
            for item_data in items_data:
                RestockItem.objects.create(restock=restock, **item_data)
        return restock

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            RestockItem.objects.filter(restock=instance).delete()
            for item_data in items_data:
                RestockItem.objects.create(restock=instance, **item_data)

        return instance
