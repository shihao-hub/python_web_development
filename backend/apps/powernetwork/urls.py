from django.urls import path, include
from rest_framework import routers

from .views import BusModelViewSet

router = routers.DefaultRouter()
router.register(r'bus', BusModelViewSet, basename='bus')

urlpatterns = [
    path("", include(router.urls))
]
