from django.urls import path, include
from rest_framework import routers

from .views import BusModelViewSet

router = routers.DefaultRouter()
router.register(r'bus', BusModelViewSet, basename='bus')

urlpatterns = [
    # todo: 这个 name 被设置成了 api-root，这没有命名空间的话，不同 app 的 url 是否会混乱呢？
    path("", include(router.urls))
]
