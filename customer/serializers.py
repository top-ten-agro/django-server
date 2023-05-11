from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Customer
from store.serializers import BalanceSerializer


class CustomerSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        expandable_fields = {
            "balances": (BalanceSerializer, {"many": True})
        }
