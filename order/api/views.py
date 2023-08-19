import os
from io import BytesIO
from PIL import Image
from sys import getsizeof
from django.core.files.uploadedfile import InMemoryUploadedFile

from cart.api.serializers import CartSerializer
from order.api.serializers import OrderSerializer, OrderItemSerializer


from order.models import Order, OrderItem
from cart.models import Cart
from food.models import Food
from core.models import User, Contact, Address
# from cart.models import

# rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated

from foodordering.permission import AdminPermission
from foodordering import constant

from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class OrderView(ModelViewSet):
    # serializer_class = OrderItemSerializer
    parser_classes = (MultiPartParser, )
    queryset = Order.objects.all()
    pagination_class = None
    # http_method_names=['post']

    def create(self, request, *args, **kwargs):
        cart_queryset = Cart.objects.filter(
            created_by=self.request.user, quantity__gte=1)
        total = 0
        foods = 0
        items = []
        request.data['items'] = []
        print(request.data)
        for obj in cart_queryset:
            split_name = obj.image.name.split('.')
            split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            joint_name = ".".join(split_name)

            img = Image.open(obj.image)
            output = BytesIO()
            img.save(output, quality=90)
            output.seek(0)

            in_memory_image = InMemoryUploadedFile(output, 'ImageField', joint_name, 'image/png', getsizeof(output), None)
            request.data._mutable = True
            self.request.data['image'] = in_memory_image
            self.request.FILES['image'] = in_memory_image
            self.request.FILES['image'].name = joint_name
            request.data['price'] = obj.price
            request.data['quantity'] = obj.quantity
            request.data['restaurant'] = obj.restaurant
            request.data['food'] = obj.food
            request.data['food_name'] = obj.food_name
            request.data['created_by'] = request.user.id

            total += obj.price * obj.quantity
            foods += obj.quantity

        print(items)
        # request.data.setlist('items', items)
        print(request.data)
        request.data['username'] = request.user.username
        request.data['email'] = request.user.email
        request.data['total_item'] = foods
        request.data['total_price'] = total

        mobile_obj = Contact.objects.filter(created_by=request.user, is_selected=True).first()
        if mobile_obj:
            request.data['mobile_no'] =  mobile_obj.mobile_no

        # 
        # request.data['address'] = 
        print(total)
        return Response(
            {constant.SUCCESS: True, constant.DATA: True},
            status=status.HTTP_200_OK
        )
