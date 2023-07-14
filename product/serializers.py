from rest_flex_fields import FlexFieldsModelSerializer
from .models import Product


class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
