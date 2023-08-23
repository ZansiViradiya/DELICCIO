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

    def list(self, request, *args, **kwargs):
        order_queryset = Order.objects.filter(
            created_by=self.request.user)
        serializer_class = OrderSerializer(order_queryset, many=True)
        return Response(
            {constant.SUCCESS: True, constant.DATA: serializer_class.data},
            status=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        cart_queryset = Cart.objects.filter(
            created_by=self.request.user, quantity__gte=1, ordered=False)
        total = 0
        foods = 0
        request.data['items'] = []
        request.FILES['items'] = []
        EXTENSION = {'jpeg': 'JPEG', 'png': 'PNG', 'jpg': 'JPG',}
        
        if cart_queryset:
            for obj in cart_queryset:
                obj.ordered = True
                obj.save()
                split_name = obj.image.name.split('.')
                ext = split_name[-1].lower()
                format = EXTENSION.get(ext, 'jpg')
                split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                joint_name = ".".join(split_name)

                img = Image.open(obj.image)
                output = BytesIO()
                original_width, original_height = img.size
                aspect_ratio = round(original_width / original_height)
                desired_height = 100
                desired_width = desired_height * aspect_ratio

                img = img.resize((desired_width, desired_height))
                img.save(output, format=format, quality=90)
                output.seek(0)

                in_memory_image = InMemoryUploadedFile(output, 'ImageField', joint_name, 'image/png', getsizeof(output), None)

                request.data['items'].append({
                    'image': in_memory_image,
                    'price': obj.price,
                    'quantity': obj.quantity,
                    'restaurant': obj.restaurant.id,
                    'food': obj.food.id,
                    'food_name': obj.food_name,
                    'created_by': request.user.id
                })

                total += obj.price * obj.quantity
                foods += obj.quantity

            request.data['username'] = request.user.username
            request.data['email'] = request.user.email
            request.data['total_item'] = foods
            request.data['total_price'] = total
            request.data['created_by'] = request.user.id
            request.data['status'] = 1

            mobile_obj = Contact.objects.filter(created_by=request.user, is_selected=True).first()
            if mobile_obj:
                request.data['mobile_no'] =  mobile_obj.id

            address_obj = Address.objects.filter(created_by=request.user, is_selected=True).first()
            if address_obj:
                request.data['address'] =  address_obj.id
            
            try:
                serializer = OrderSerializer(
                    data=request.data, context={"request": request}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {constant.SUCCESS: True, constant.DATA: serializer.data},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                print(e)

            return Response(
                {constant.SUCCESS: False, constant.DATA: False},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {constant.SUCCESS: False, constant.MESSAGE: "Items does not found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, *args, **kwargs):
        order_obj = Order.objects.filter(
            created_by=self.request.user, id=self.kwargs['pk']).first()
        serializer_class = OrderSerializer(order_obj)
        if order_obj:
            return Response(
                { constant.SUCCESS: True, constant.DATA: serializer_class.data },
                status=status.HTTP_200_OK
            )
        return Response(
            {constant.SUCCESS: False, constant.DATA: {}},
            status=status.HTTP_400_BAD_REQUEST
        )
