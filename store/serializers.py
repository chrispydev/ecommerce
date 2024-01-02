from rest_framework.serializers import ModelSerializer
from store.models import Product, ShippingRate


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ShippingRateSerializer(ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = "__all__"
