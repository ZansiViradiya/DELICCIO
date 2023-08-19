from django.contrib import admin
from .models import Category, RestaurantCategory

# Register your models here.
admin.site.register(Category)
admin.site.register(RestaurantCategory)