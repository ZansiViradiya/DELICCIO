from rest_framework import serializers
from ..models import Order, OrderItem

    


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    class Meta:
        model = Order
        fields = "__all__"

    def save(self, **kwargs):
        items_data = self.validated_data.pop('items', [])
        order = super().save(**kwargs)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status_name'] = instance.status.status_name
        representation['item'] = []
        for order_item in instance.orderitem_set.all():
            waste_representation = {
                'id': order_item.id,
                'food': order_item.food.id,
                'price': order_item.price,
                'order': order_item.order.id,
                'quantity': order_item.quantity,
                'restaurant': order_item.restaurant.id,
                'food_name': order_item.food_name,
                'image': order_item.image.name
            }
            representation['item'].append(waste_representation)
        return representation