from rest_framework.routers import DefaultRouter
from django.urls import path

# view
from .views import(
    FoodView
)

router = DefaultRouter()
router.register(r"food", FoodView, basename="food")


urlpatterns = router.urls