import os
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from restaurant.api.serializers import RestaurantSerializer, RestaurantImageSerializer, RestaurantWithImageSerializer, RestaurantImage1Serializer

from restaurant.models import Restaurant, RestaurantRate, RestaurantImages
from core.models import User

# restframwork
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated

from foodordering.permission import AdminPermission
from foodordering import constant

from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class RestaurantView(ModelViewSet):
    serializer_class = RestaurantSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, )
    queryset = Restaurant.objects.all()

    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT, title="Restaurant", required=["is_approve"],
                                                     properties={
        "is_approve": openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True, title="Is approve")
    }))
    @action(methods=["PATCH"], detail=True, permission_classes=(AdminPermission,))
    def approve(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(id=self.kwargs.get("pk"))
        except:
            return Response(
                {constant.SUCCESS: False,
                    constant.MESSAGE: "This restaurant does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer_data = serializer.save()
            if serializer_data:
                user_obj = User.objects.filter(restaurant=restaurant).first()
                if user_obj:
                    email = user_obj.email
                    username = user_obj.username
                    subject, from_email, to = 'Congrulations! your restaurant has been approved', settings.EMAIL_HOST_USER, email
                    html_template = get_template('html/rest_approval.html')
                    restaurant_dict = {'username': username, 'owner_email': restaurant.owner_email, 'restaurant': restaurant.name,
                                       'owner_name': restaurant.owner_name, 'open': restaurant.open_time, 'closed': restaurant.closed_time, 'holidays': restaurant.holidays}
                    html_content = html_template.render(restaurant_dict)
                    msg = EmailMultiAlternatives(
                        subject, html_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    return Response({constant.SUCCESS: True, constant.MESSAGE: "restaurant approved"}, status=status.HTTP_200_OK)

        return Response(
            {constant.SUCCESS: False, constant.MESSAGE: "This restaurant does not exist."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    @action(methods=["GET"], detail=False, permission_classes=())
    def latest_restaurant(self, request, *args, **kwargs):
        queryset = self.queryset.order_by('-id')[:3]
        serializer = RestaurantWithImageSerializer(queryset, many=True, context=request)
        return  Response({constant.SUCCESS: True, constant.DATA: serializer.data},status=status.HTTP_200_OK,)

class RestaurantImagesView(ListCreateAPIView):
    parser_classes = (MultiPartParser, )
    serializer_class = RestaurantImageSerializer
    pagination_class = None
    # permission_classes = (IsAuthenticated,)
    queryset = RestaurantImages.objects.all()
    
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_FILE), maxLength = 20),
    openapi.Parameter('restaurant', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title = 'Restaurant', x_nullable = True), 
    openapi.Parameter('created_by', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title = 'Created by', x_nullable = True)])
    def post(self, request, *args, **kwargs):
         
        total_image = 20
        total_uploaded_images = len(self.request.FILES.getlist('image', None))
        restaurant_obj = Restaurant.objects.filter(id=request.data['restaurant']).first()
        if restaurant_obj:
            rest_image_obj = RestaurantImages.objects.filter(restaurant=request.data['restaurant']).first()
            if rest_image_obj:
                remaining_image = total_image - len(rest_image_obj.image)
                if remaining_image == 0:
                    return Response({constant.SUCCESS: False, constant.MESSAGE: "Image upload limit - 20, You have already uploaded 20 images"}, status=status.HTTP_400_BAD_REQUEST,)
                elif total_uploaded_images <= remaining_image:
                    index = 1
                    images = []
                    for i in self.request.FILES.getlist('image', None):
                        split_name = i.name.split('.')
                        split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+str(index)
                        joint_name = ".".join(split_name)
                        i.name = joint_name
                        index += 1
                        with open('media/images/rest_images/'+joint_name, 'wb') as file_upload:
                            file_upload.write(i.read())
                        rest_image_obj.image.append(i.name)
                        rest_image_obj.save()
                    serializer = self.serializer_class(rest_image_obj)
                    return Response({constant.SUCCESS: True, constant.DATA: serializer.data},status=status.HTTP_200_OK,)      
                else:
                    return Response({constant.SUCCESS: False, constant.MESSAGE: "You have uploading total "+ str(total_uploaded_images)+" images but you can upload only "+ str(remaining_image)+" images because uploaded image limit is 20"},status=status.HTTP_400_BAD_REQUEST,)

            index = 1
            images = []
            for i in self.request.FILES.getlist('image', None):
                split_name = i.name.split('.')
                split_name[0] = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+str(index)
                joint_name = ".".join(split_name)
                i.name = joint_name
                index += 1
                with open('media/images/rest_images/'+joint_name, 'wb') as file_upload:
                    file_upload.write(i.read())
                images.append(i.name)
            request.data.setlist('image', images)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  Response({constant.SUCCESS: True, constant.DATA: serializer.data},status=status.HTTP_201_CREATED,)
        return  Response({constant.SUCCESS: False , constant.MESSAGE: "Restaurant does not exist"}, status=status.HTTP_201_CREATED,)
    
class RUDRestaurantImagesView(RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, )
    serializer_class = RestaurantImageSerializer
    pagination_class = None
    http_method_names = ["get", "put", "delete"]
    # permission_classes = (IsAuthenticated,)
    queryset = RestaurantImages.objects.all()

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(openapi.TYPE_FILE), maxLength = 20),
    openapi.Parameter('restaurant', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title = 'Restaurant', x_nullable = True), 
    openapi.Parameter('created_by', openapi.IN_FORM, type=openapi.TYPE_INTEGER, title = 'Created by', x_nullable = True)])
    def put(self, request, *args, **kwargs):
        total_uploaded_images = len(self.request.FILES.getlist('image', None))
        rest_image_obj = RestaurantImages.objects.filter(id=kwargs['pk'], restaurant=request.data['restaurant']).first()
        if rest_image_obj:
            if len(rest_image_obj.image) == 0:
                return Response({constant.SUCCESS: False, constant.MESSAGE: "You have no image"}, status=status.HTTP_400_BAD_REQUEST,)
            elif len(rest_image_obj.image) == total_uploaded_images:
                index = 0
                for i in self.request.FILES.getlist('image', None):
                    with open('media/images/rest_images/'+rest_image_obj.image[index], 'wb') as image_upload:
                       image_upload.write(i.read())
                    index += 1 
                serializer = self.serializer_class(rest_image_obj)
                return Response({constant.SUCCESS: True, constant.DATA: serializer.data},status=status.HTTP_200_OK,)      
            else:
                return Response({constant.SUCCESS: False, constant.MESSAGE: "You have "+str(len(rest_image_obj.image))+" images so you have to upload "+str(len(rest_image_obj.image))+" images"}, status=status.HTTP_400_BAD_REQUEST,)
            
        return Response({constant.SUCCESS: True, constant.MESSAGE: "Restaurant images does not exist" },status=status.HTTP_400_BAD_REQUEST,)
    
        
class UpdateDeleteImageView(RetrieveUpdateDestroyAPIView):
    parser_classes = (MultiPartParser, )
    pagination_class = None
    http_method_names = ["delete", "patch"]
    serializer_class = RestaurantImage1Serializer
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE)])
    def patch(self, request, *args, **kwargs):
        rest_image_obj = RestaurantImages.objects.filter(id = kwargs['id']).first()
        if rest_image_obj:
            if int(kwargs['index_no']) == 0:
                return Response({ constant.SUCCESS: False, constant.MESSAGE: "Please choose index_no greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
            elif int(kwargs['index_no']) <= len(rest_image_obj.image):
                image = request.FILES['image']
                with open('media/images/rest_images/'+rest_image_obj.image[int(kwargs['index_no'])-1], 'wb') as fileupload:
                    fileupload.write(image.read())
                serializer = RestaurantImageSerializer(rest_image_obj)
                return  Response({constant.SUCCESS: True, constant.DATA: serializer.data}, status=status.HTTP_200_OK,)
            else:
                return Response({ constant.SUCCESS: False, constant.MESSAGE: "The index_no given by you is not found because it contains Total "+str(len(rest_image_obj.image))+" images"}, status=status.HTTP_400_BAD_REQUEST,)
        
        return Response({ constant.SUCCESS: False, constant.MESSAGE: "Restaurant images does not exist"}, status=status.HTTP_400_BAD_REQUEST,)
    

    def delete(self, request, *args, **kwargs):
        rest_image_obj = RestaurantImages.objects.filter(id = kwargs['id']).first()
        if rest_image_obj:
            if int(kwargs['index_no']) == 0:
                return Response({ constant.SUCCESS: False, constant.MESSAGE: "Please choose index_no greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
            elif int(kwargs['index_no']) <= len(rest_image_obj.image):
                os.remove("media/images/rest_images/"+rest_image_obj.image[int(kwargs['index_no'])-1])
                rest_image_obj.image.remove(rest_image_obj.image[int(kwargs['index_no'])-1])
                rest_image_obj.save()
                return Response({ constant.SUCCESS: True, constant.MESSAGE: "not found"}, status=status.HTTP_204_NO_CONTENT,)
            else:
                return Response({ constant.SUCCESS: False, constant.MESSAGE: "The index_no given by you is not found because it contains Total "+str(len(rest_image_obj.image))+" images"}, status=status.HTTP_400_BAD_REQUEST,)

        return Response({ constant.SUCCESS: False, constant.MESSAGE: "Restaurant images does not exist"}, status=status.HTTP_400_BAD_REQUEST,)
