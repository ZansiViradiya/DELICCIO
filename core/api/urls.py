
from django.urls import path
from .views import (
    RegisterView, 
    UserListView, 
    ContactView,
    AddressView,
    LoginView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"contact", ContactView, basename="contact")
router.register(r"address", AddressView, basename="address")
router.register(r"user_list", UserListView, basename="user_list")

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login")
]+router.urls
