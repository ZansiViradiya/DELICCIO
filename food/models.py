from django.db import models
from restaurant.models import Restaurant
from core.models import User
from category.models import Category
from django.core.validators import MinLengthValidator, MaxValueValidator
from core.models import TimeStamp

# Create your models here.
class Food(TimeStamp):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_veg = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, null=True, blank=True,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/foods/', default=None)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True,on_delete=models.CASCADE)


class FoodRate(TimeStamp):
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True,on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MaxValueValidator(6)])
    comment = models.CharField(max_length=1000, validators=[MinLengthValidator(5)])
    image = models.ImageField(upload_to='images/food_rates/', default=None)
    user = models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE)