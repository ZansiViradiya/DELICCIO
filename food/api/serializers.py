from rest_framework import serializers
from ..models import Food, FoodRate

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"

class FoodRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodRate
        fields = "__all__"

