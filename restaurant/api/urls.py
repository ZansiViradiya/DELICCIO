from django.urls import path
from .views import (
    RestaurantView,
    RestaurantImagesView,
    RUDRestaurantImagesView,
    UpdateDeleteImageView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"restaurant", RestaurantView, basename="restaurant")
# router.register(r"restaurant/image", RestaurantImagesView, basename="restaurant_images")

urlpatterns = [
    # path('restmultiple', MultipleImagesView.as_view(), name="rest_multiple"),
    # path('restaurant/multi-image/<int:id>', UpdateMultiImageView.as_view(), name="image"),
    path('restaurant/images', RestaurantImagesView.as_view(), name="restaurant_images"),
    path('restaurant/images/<int:pk>', RUDRestaurantImagesView.as_view(), name="restaurant_images"),
    path('restaurant/images/<int:id>/image/<int:index_no>', UpdateDeleteImageView.as_view(), name="single_image_update"),
    # path('restaurant/images/<int:id>/image/<int:index_no>', DeleteImageView.as_view(), name="image_delete")
 ]+ router.urls
