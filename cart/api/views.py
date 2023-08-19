import os
from io import BytesIO
from PIL import Image
from sys import getsizeof
from django.core.files.uploadedfile import InMemoryUploadedFile

from cart.api.serializers import CartSerializer

from cart.models import Cart
from food.models import Food
from core.models import User
# from cart.models import 

# rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated

from foodordering.permission import AdminPermission
from foodordering import constant

from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class CartCreateView(APIView):
    # serializer_class = CartSerializer
    parser_classes = (MultiPartParser, )
    queryset = Cart.objects.all()
    pagination_class = None
    # http_method_names=['post']

    @swagger_auto_schema(manual_parameters=[
    openapi.Parameter('food', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title="Food"), 
    openapi.Parameter('quantity', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title="quantity")])
    def post(self, request, *args, **kwargs):
        if request.user.role == "user":
            cart_obj = Cart.objects.filter(created_by=request.user.id, food=request.data['food']).first()
            if cart_obj:
                serialized_data = CartSerializer(cart_obj)
                if int(request.data['quantity']) == 0:
                    cart_obj.quantity = int(request.data['quantity'])
                    cart_obj.save()
                    return Response(
                            {constant.SUCCESS: True, constant.DATA: serialized_data.data},
                            status=status.HTTP_201_CREATED,)

                cart_obj.quantity += int(request.data['quantity'])
                cart_obj.save()
                # self.request.data["quantity"]
                return Response(
                            {constant.SUCCESS: True, constant.DATA: serialized_data.data},
                            status=status.HTTP_201_CREATED,)
            if not cart_obj:
                food_obj = Food.objects.filter(id=request.data['food']).first()
                split_name = food_obj.image.name.split('.')
                split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                joint_name = ".".join(split_name)

                img = Image.open(food_obj.image)
                output = BytesIO()
                original_width, original_height = img.size
                aspect_ratio = round(original_width / original_height)
                desired_height = 100
                desired_width = desired_height * aspect_ratio

                img = img.resize((desired_width, desired_height))
                img.save(output, quality=90)
                output.seek(0)

                in_memory_image = InMemoryUploadedFile(output, 'ImageField', joint_name, 'image/png', getsizeof(output), None)
                request.data._mutable = True
                self.request.data['image'] = in_memory_image
                self.request.FILES['image'] = in_memory_image
                self.request.FILES['image'].name = joint_name
                self.request.data["food_name"] = food_obj.name
                self.request.data["restaurant"] = food_obj.restaurant.id
                self.request.data["price"] = food_obj.price
                self.request.data['created_by'] = request.user.id
                serialized_data = CartSerializer(data=request.data)
                if serialized_data.is_valid():
                    image = serialized_data.save()
                    if image:
                        return Response(
                            {constant.SUCCESS: True, constant.DATA: serialized_data.data},
                            status=status.HTTP_201_CREATED,)
            return Response({constant.SUCCESS: True, constant.MESSAGE: serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST,)
        
    def get(self, request, *args, **kwargs):
        queryset = Cart.objects.filter(created_by = request.user.id, quantity__gte=1)
        serializer_class = CartSerializer(queryset, many=True)
        return Response({constant.SUCCESS: True, constant.MESSAGE: serializer_class.data}, status=status.HTTP_200_OK,)

class UDGCartView(APIView):
    parser_classes = (MultiPartParser, )
    queryset = Cart.objects.all()
    pagination_class = None

    @swagger_auto_schema(manual_parameters=[ 
    openapi.Parameter('quantity', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title="quantity")])
    def put(self, request, *args, **kwargs):
        cart_obj = Cart.objects.filter(created_by=request.user.id, id=kwargs['id']).first()
        serializer_class = CartSerializer(cart_obj)
        if cart_obj:
            if int(request.data['quantity']) == 0:
                cart_obj.created_by = None
                cart_obj.quantity = int(request.data['quantity'])
                cart_obj.save()
                return Response({constant.SUCCESS: True, constant.MESSAGE: serializer_class.data}, status=status.HTTP_204_NO_CONTENT,)
            cart_obj.created_by = request.user
            cart_obj.quantity += int(request.data['quantity'])
            cart_obj.save()
            return Response({constant.SUCCESS: True, constant.MESSAGE: serializer_class.data}, status=status.HTTP_200_OK,)
        return  Response({constant.SUCCESS: False, constant.MESSAGE: "Item does not exist"}, status=status.HTTP_400_BAD_REQUEST,)
    
    def get(self, request, *args, **kwargs):
        cart_obj = Cart.objects.filter(created_by=request.user.id, id=kwargs['id']).first()
        serializer_class = CartSerializer(cart_obj)
        if cart_obj:
            return Response({constant.SUCCESS: True, constant.MESSAGE: serializer_class.data}, status=status.HTTP_200_OK,)
        return  Response({constant.SUCCESS: False, constant.MESSAGE: "Item does not exist"}, status=status.HTTP_400_BAD_REQUEST,)
    
    def delete(self, request, *args, **kwargs):
        cart_obj = Cart.objects.filter(created_by=request.user.id, id=kwargs['id']).first()
        serializer_class = CartSerializer(cart_obj)
        if cart_obj:
            cart_obj.created_by = None
            cart_obj.quantity = 0
            cart_obj.save()
            return Response({constant.SUCCESS: True, constant.MESSAGE: serializer_class.data}, status=status.HTTP_204_NO_CONTENT,)
        return  Response({constant.SUCCESS: False, constant.MESSAGE: "Item does not exist"}, status=status.HTTP_400_BAD_REQUEST,)