from datetime import datetime
import os

# serializer
from .serializers import CategorySerializer, RestaurantCategorySerializer

# model
from ..models import Category, RestaurantCategory
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


class CategoryView(ModelViewSet):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # permission_classes = (AdminPermission,)
    pagination_class = None

    def create(self, request, *args, **kwargs):
        split_name = self.request.FILES['image'].name.split('.')
        split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        joint_name = ".".join(split_name)
        self.request.FILES['image'].name = joint_name
        print(self.request.FILES['image'].file)
        # self.request.data['created_by'] = request.user.id
        serialized_data = self.serializer_class(data=request.data)
        if serialized_data.is_valid():
            print(serialized_data)
            image = serialized_data.save()
            if image:
                return Response(
                    {constant.SUCCESS: True, constant.DATA: serialized_data.data},
                    status=status.HTTP_201_CREATED,)
        return Response({constant.SUCCESS: False, constant.MESSAGE: serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST,)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if 'image' in request.data:
            os.remove(instance.image.path)
            split_name = self.request.FILES['image'].name.split('.')
            split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            joint_name = ".".join(split_name)
            self.request.FILES['image'].name = joint_name
            self.request.data['created_by'] = request.user.id
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


class RestaurantCategoryView(ListCreateAPIView):
    serializer_class = RestaurantCategorySerializer
    queryset = RestaurantCategory.objects.all()
    pagination_class = None
    permission_classes = (AdminPermission| RestaurantPermission, )

    def get_queryset(self):
        rest_cat_obj = self.queryset.filter(created_by=self.request.user)
        return rest_cat_obj
    
    def post(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        print(self.request.user)
        user_obj = User.objects.filter(username=self.request.user, role='restaurant').first()
        if user_obj:
            rest_cat_obj = RestaurantCategory.objects.filter(restaurant=user_obj.restaurant, created_by=self.request.user).first()
            request.data['restaurant'] = user_obj.restaurant.id
            request.data['created_by'] = self.request.user.id
            if rest_cat_obj:
                serialized_data = self.get_serializer(rest_cat_obj, data=request.data, partial=partial)
                if serialized_data.is_valid(raise_exception=True):
                    serialized_data.save()
                    return Response({constant.SUCCESS: True, constant.DATA: serialized_data.data}, status=status.HTTP_201_CREATED,)
                
                return Response({constant.SUCCESS: False, constant.MESSAGE: serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST,)
            
            serialized_data = self.serializer_class(data=request.data, context=request)
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return Response({constant.SUCCESS: True, constant.DATA: serialized_data.data}, status=status.HTTP_201_CREATED,)
                
        return Response({constant.SUCCESS: False, constant.MESSAGE: "only restaurant user can choose category"}, status=status.HTTP_201_CREATED,)
