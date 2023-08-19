from django.contrib import admin
from .models import Restaurant, RestaurantImages, RestaurantRate

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(RestaurantImages)
admin.site.register(RestaurantRate)
