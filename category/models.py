from django.db import models

from restaurant.models import Restaurant
from core.models import User
from core.models import TimeStamp



# Create your models here.
class Category(TimeStamp):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/categories/', default=None)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

class RestaurantCategory(TimeStamp):
    category = models.ManyToManyField(Category, blank=True)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
