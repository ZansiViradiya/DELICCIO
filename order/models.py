from django.db import models
from core.models import User
from restaurant.models import Restaurant
from core.models import Contact, Address
from delivery_boy.models import Delivery
from food.models import Food
from core.models import TimeStamp
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator

# Create your models here.
class Status(TimeStamp):
    status_name = models.CharField(unique=True, max_length=50)
    description = models.CharField(max_length=100)


class Order(TimeStamp):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    total_item = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=10, default="cash")
    delivery_boy = models.ForeignKey(Delivery, null=True, blank=True, on_delete=models.CASCADE)
    delivery_on = models.DateTimeField(auto_now=True)
    mobile_no = models.ForeignKey(Contact, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)


class OrderItem(TimeStamp):
    food_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/items/', default=None)
    price = models.IntegerField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, models.SET_NULL,null=True, blank=True)
    food = models.ForeignKey(Food, models.SET_NULL,null=True, blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

