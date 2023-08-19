from django.db import models
from core.models import User
from food.models import Food
from django.core.validators import MinValueValidator
from restaurant.models import Restaurant
from core.models import TimeStamp

# Create your models here.
class Cart(TimeStamp):
    food_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/carts/', default=None)
    price = models.IntegerField(default=None)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    food = models.ForeignKey(Food, null=True, blank=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created_by = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)