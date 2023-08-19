from cart.models import Cart
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        # read_only_fields = ("restaurant", "image", "price", "restaurant", "food_name")