"""foodordering URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from core.api import urls as User
from core import urls as temp_url
from restaurant.api import urls as Restaurant
from category.api import urls as Category
from food.api import urls as Food
from cart.api import urls as Cart
from order.api import urls as Order


urlpattern1 = [
    path("admin/", admin.site.urls),
    path("api/", include(User)),
    path("api/", include(Restaurant)),
    path("api/", include(Category)),
    path("api/", include(Food)),
    path("api/", include(Cart)),
    path("api/", include(Order))
]
schema_view = get_schema_view(
    openapi.Info(
        title="WowFoodFamily API", default_version="v1", description="This is the API documentation of WowFoodFamily"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    validators=[],
    patterns=urlpattern1
)

urlpatterns = urlpattern1 +[
    path("", include(temp_url), name="home"),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
