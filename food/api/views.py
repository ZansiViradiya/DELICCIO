from datetime import datetime
import os

# serializer
from .serializers import FoodSerializer, FoodRateSerializer

# model
from ..models import Food, FoodRate
from core.models import User

# restframwork
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status

# food ordering
from foodordering.permission import AdminPermission, RestaurantPermission
from foodordering import constant


class FoodView(ModelViewSet):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    # permission_classes = (AdminPermission| RestaurantPermission, )
    pagination_class = None

    def create(self, request, *args, **kwargs):
        split_name = self.request.FILES['image'].name.split('.')
        split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        joint_name = ".".join(split_name)
        self.request.FILES['image'].name = joint_name
        self.request.data['created_by'] = request.user.id
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            image = serialized_data.save()
            if image:
                return Response(
                    {constant.SUCCESS: True, constant.DATA: serialized_data.data},
                    status=status.HTTP_201_CREATED,)
        return Response({constant.SUCCESS: True, constant.MESSAGE: "Image not uploaded"}, status=status.HTTP_400_BAD_REQUEST,)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        print(self.request.user)
        request.data['created_by'] = self.request.user
        instance = self.get_object()
        if 'image' in request.data:
            os.remove(instance.image.path)
            split_name = self.request.FILES['image'].name.split('.')
            split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            joint_name = ".".join(split_name)
            self.request.FILES['image'].name = joint_name
        serialized_data = self.get_serializer(
            instance, data=request.data, partial=partial)
        if serialized_data.is_valid(raise_exception=True):
            self.perform_update(serialized_data)
            return Response(
                {constant.SUCCESS: True, constant.DATA: serialized_data.data},
                status=status.HTTP_201_CREATED,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        os.remove(instance.image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)