from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from .models import Customer


class CustomerSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
