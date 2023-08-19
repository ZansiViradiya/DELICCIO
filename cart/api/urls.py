from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from django.views.decorators.http import require_POST, require_GET


# view
from .views import(
    CartCreateView,
    UDGCartView
)

router = DefaultRouter()
# router.register(r"cart", CartView, basename="cart")


urlpatterns = [
    path(r"cart/", CartCreateView.as_view(), name="cart_create"),
    path(r"cart/<int:id>", UDGCartView.as_view(), name="cart_UDG"),
] + router.urls







# re_path(r"cart", CartCreateView.as_view(), name="cart_create"),
# path(r"cart", CartListView.as_view(), name="cart_list")
# re_path(r"cart/$", CartListView.as_view(), name="cart_list")
# path+re_path = True
# re_path+re_path = False - method_not_allow
# path+path = False - get - page_not_found error