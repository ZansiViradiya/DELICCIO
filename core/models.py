from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from foodordering import constant
from restaurant.models import Restaurant
from delivery_boy.models import Delivery 

# Create your models here.
class TimeStamp(models.Model):
    """
    An abstract models which will be used in all models to save created and updated
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """
    A custom manager for User model
    """
    def save(self):
        user = super(CustomUserManager, self)
        user.set_password(self.password)
        user.save()
        return user

    def _create_user(self, password, is_staff, is_superuser, **extra_fields):
        user = self.model(is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password=None, **extra_fields):
        return self._create_user(password, False, False, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        user = self._create_user(password, True, True, **extra_fields)
        admin_group, created = Group.objects.get_or_create(name=constant.ADMIN_GROUP)
        admin_group.user_set.add(user)
        user.role = constant.ADMIN
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStamp):
    """
    Custom user model
    """

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(
        max_length=10, choices=constant.USER_ROLE_CHOICES, default="user"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=True, blank=True
    )
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, null=True, blank=True
    )
    unique_code = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=True)
    objects = CustomUserManager()
    objects_all = models.Manager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username    
    
class Address(TimeStamp):
    title = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(
        max_length=10, choices=constant.TYPE_CHOICES, default="order"
    )
    zipcode = models.CharField(max_length=6, default="395006")
    is_selected = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Contact(TimeStamp):
    mobile_no = models.CharField(max_length=10)
    type = models.CharField(
        max_length=10, choices=constant.TYPE_CHOICES, default="order"
    )
    is_selected = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)