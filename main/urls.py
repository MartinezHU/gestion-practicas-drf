from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.core.views import APIUserViewSet

router = DefaultRouter()

# Viewsets

router.register(r'users', APIUserViewSet, basename='apiuser')

urlpatterns = [
    path('admin/', admin.site.urls),
    path("rest-auth/", include("rest_framework.urls")),
    path('api/', include(router.urls))
]
