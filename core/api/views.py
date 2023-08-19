# django contrib
from django.contrib.auth.models import Group


# serializers
from .serializers import UserSerializer, ContactSerializer, AddressSerializer
from restaurant.api.serializers import RestaurantSerializer
from delivery_boy.api.serializers import DeliverySerializer

# models
from ..models import User, Contact, Address
from restaurant.models import Restaurant
from delivery_boy.models import Delivery

# restframwork
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# simplejwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.backends import TokenBackend

# message
from foodordering import message, constant

# drf_yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    queryset = User.objects.all()

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title='User',
        required = ['username', 'email', 'role', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, title="Username", maxLength = 100, minLength = 1),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, title="email", maxLength = 100, minLength = 1),
            'password': openapi.Schema(type=openapi.TYPE_STRING, title="Password", maxLength = 128, minLength= 1),
            'role': openapi.Schema(type=openapi.TYPE_STRING, title="Otp", maxLength = 100, x_nullable=True, enum=['user', 'admin', 'restaurant', 'delivery']),
            'restaurant': openapi.Schema(type=openapi.TYPE_INTEGER, title="Restaurant", x_nullable=True),
            'delivery': openapi.Schema(type=openapi.TYPE_INTEGER, title="Delivery", x_nullable=True),
            'otp': openapi.Schema(type=openapi.TYPE_STRING, title="Otp", maxLength = 100, x_nullable=True),
            'unique_code': openapi.Schema(type=openapi.TYPE_STRING, title="Unique code", maxLength = 100)
        }
    ))
    def post(self, request):
        if self.request.data['role'] == "restaurant":
            if 'delivery' not in request.data:
                if 'restaurant' in request.data:
                    restaurant_serializer = RestaurantSerializer(data=request.data,context=request)
                    if restaurant_serializer.is_valid():
                        user_serializer = self.serializer_class(data=request.data)
                        if user_serializer.is_valid():
                            restaurant = restaurant_serializer.save()
                            user = user_serializer.save()
                            if user:
                                user.restaurant = restaurant
                                user.save()
                                rest, restaurant_group = Group.objects.get_or_create(name=constant.RESTAURANT_GROUP)
                                rest.user_set.add(user)

                                address_serializer = AddressSerializer(data=request.data)
                                if address_serializer.is_valid():
                                    address = address_serializer.save()
                                    if address:
                                        address.created_by = user
                                        address.save()
                                        restaurant.address_id = address.id
                                        restaurant.save()
                                else:
                                    return Response({constant.MESSAGE: address_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)

                                contact_serializer = ContactSerializer(data=request.data)
                                if contact_serializer.is_valid():
                                    contact = contact_serializer.save()
                                    if contact:
                                        contact.created_by = user
                                        contact.save()
                                        restaurant.contact_id = contact.id
                                        restaurant.save()
                                else:
                                    return Response({constant.MESSAGE: contact_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)

                                response = user_serializer.data
                                return Response({constant.DATA: response, constant.SUCCESS: True}, status=status.HTTP_201_CREATED)

                        return Response({constant.MESSAGE: user_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)

                    return Response({constant.MESSAGE: restaurant_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({constant.MESSAGE: message.RESTAURANT_PERMISSION, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({constant.MESSAGE: message.RESTRICT_RESTAURANT, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
        elif self.request.data['role'] == "delivery":
            if 'restaurant' not in request.data:
                if 'delivery' in request.data:
                    delivery_serializer = DeliverySerializer(data=request.data,context=request)
                    if delivery_serializer.is_valid():
                        user_serializer = self.serializer_class(data=request.data)
                        if user_serializer.is_valid():
                            delivery = delivery_serializer.save()
                            user = user_serializer.save()
                            if user:
                                user.delivery = delivery
                                user.save()
                                deli, delivery_group = Group.objects.get_or_create(name=constant.DELIVERY_GROUP)
                                deli.user_set.add(user)

                                address_serializer = AddressSerializer(data=request.data)
                                if address_serializer.is_valid():
                                    address = address_serializer.save()
                                    if address:
                                        address.created_by = user
                                        address.save()
                                else:
                                    return Response({constant.MESSAGE: address_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)

                                contact_serializer = ContactSerializer(data=request.data)
                                if contact_serializer.is_valid():
                                    contact = contact_serializer.save()
                                    if contact:
                                        contact.created_by = user
                                        contact.save()
                                else:
                                    return Response({constant.MESSAGE: contact_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)

                                response = user_serializer.data
                                return Response({constant.DATA: response, constant.SUCCESS: True}, status=status.HTTP_201_CREATED)


                        return Response({constant.MESSAGE: user_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)

                    return Response({constant.MESSAGE: delivery_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({constant.MESSAGE: message.DELIVERY_PERMISSION, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({constant.MESSAGE: message.RESTRICT_DELIVERY, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
        elif self.request.data['role'] == "user":
            if ('delivery' in request.data) or ('restaurant' in request.data):
                return Response({constant.MESSAGE: message.RESTRICT_USER, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user_serializer = self.serializer_class(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    if user:
                        normal, user_group = Group.objects.get_or_create(name=constant.USER_GROUP)
                        normal.user_set.add(user)

                        address_serializer = AddressSerializer(data=request.data)
                        if address_serializer.is_valid():
                            address = address_serializer.save()
                            if address:
                                address.created_by = user
                                address.save()

                        contact_serializer = ContactSerializer(data=request.data)
                        if contact_serializer.is_valid():
                            contact = contact_serializer.save()
                            if contact:
                                contact.created_by = user
                                contact.save()
                        else:
                            return Response({constant.MESSAGE: contact_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
                        
                        response = user_serializer.data
                        return Response({constant.DATA: response, constant.SUCCESS: True}, status=status.HTTP_201_CREATED)

                return Response({constant.MESSAGE: user_serializer.errors, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({constant.MESSAGE: message.ROLE_PERMISSION, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        self.user.last_login = timezone.now()
        self.user.save()
        data.update({'user': self.user.username})
        data.update({'id': self.user.id})
        data.update({'role': self.user.role})
        return data

class LoginView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            serialized_data = serializer.validate(request.data)
            print(serialized_data)
        return Response({constant.DATA: serialized_data, constant.SUCCESS: False}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = None
    queryset = User.objects.all()

class ContactView(ModelViewSet):
    serializer_class = ContactSerializer
    pagination_class = None
    queryset = Contact.objects.all()

class AddressView(ModelViewSet):
    serializer_class = AddressSerializer
    pagination_class = None
    queryset = Address.objects.all()
