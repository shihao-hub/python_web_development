from django.urls import path, include
from rest_framework import routers

from .views import UserModelViewSet, GroupModelViewSet, TestViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)
router.register(r'groups', GroupModelViewSet)
router.register(r'test', TestViewSet, basename='test')

urlpatterns = [
    path("", include(router.urls))
]
