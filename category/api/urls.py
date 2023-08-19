
from rest_framework.routers import DefaultRouter
from django.urls import path
# view
from .views import(
    CategoryView,
    RestaurantCategoryView
)

router = DefaultRouter()
router.register(r"category", CategoryView, basename="category")


urlpatterns = [ path(r"restaurant_category", RestaurantCategoryView.as_view(),name="restaurant_category")] + router.urls
