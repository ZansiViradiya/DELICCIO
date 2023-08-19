from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from django.views.decorators.http import require_POST, require_GET


# view
from .views import(
    OrderView,
)

router = DefaultRouter()
router.register(r"order", OrderView, basename="cart_create")


urlpatterns = [
    # path(r"order/", OrderView.as_view(), name="cart_create"),
    # path(r"cart/<int:id>", UDGCartView.as_view(), name="cart_UDG"),
] + router.urls