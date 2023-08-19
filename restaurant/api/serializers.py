from rest_framework import serializers
from ..models import Restaurant, RestaurantRate, RestaurantImages
from foodordering import constant
from core.api.serializers import AddressSerializer
from core.models import Address

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantRate
        fields = "__all__"


class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImages
        fields = "__all__"

class RestaurantImage1Serializer(serializers.Serializer):
    pass

class RestaurantWithImageSerializer(serializers.ModelSerializer):
    multi_image = serializers.SerializerMethodField('_get_children')
    address =  serializers.SerializerMethodField('_get_address')

    # images = serializers.ListField(child=serializers.StringRelatedField(many=True))
    # image = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # images = serializers.SlugRelatedField( many=True,
    #     read_only=True,
    #     slug_field='image')
    class Meta:
        model = Restaurant
        fields = ['name', 'owner_name', 'owner_email', 'open_time', 'closed_time','multi_image', 'holidays', 'address']

    def _get_children(self, obj):
        queryset = RestaurantImages.objects.filter(restaurant=obj.id).first()
        serializer = RestaurantImageSerializer(queryset)
        if serializer.data['image']:           
           return serializer.data['image'][0]
        return ''
    
    def _get_address(self, obj):
        if obj.address_id:
            queryset = Address.objects.filter(id=obj.address_id.id).first()
            serializer = AddressSerializer(queryset)
            return queryset.address+queryset.city+queryset.zipcode
        return None