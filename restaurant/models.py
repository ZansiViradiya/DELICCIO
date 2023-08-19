from django.db import models
from foodordering import constant
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField
from django.core.validators import MinLengthValidator, MaxValueValidator
from foodordering import settings


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    owner_email = models.EmailField(max_length=100)
    open_time = models.TimeField()
    closed_time = models.TimeField()
    holidays = ArrayField(models.CharField(choices=constant.HOLIDAY_CHOICES, max_length=10),max_length=3)
    address_id = models.ForeignKey('core.Address', null=True, blank=True, on_delete=models.SET_NULL)
    contact_id = models.ForeignKey('core.Contact', null=True, blank=True, on_delete=models.SET_NULL)
    is_approve = models.BooleanField(default=False)


class RestaurantRate(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MaxValueValidator(6)])
    comment = models.CharField(max_length=1000, validators=[MinLengthValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

class RestaurantImages(models.Model):
    image = ArrayField(models.CharField(default=None, max_length=200), max_length=20, default=None)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE, related_name='multi_image')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)