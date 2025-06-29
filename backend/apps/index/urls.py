from django.urls import path, include
from rest_framework import routers

from .views import IndexViewSet0, IndexViewSet

router = routers.DefaultRouter()
# fixme: 这个不对，不能这样用，router 的原理还是要去了解一下的
# router.register("", IndexViewSet0, basename="index")

urlpatterns = [
    # path("", include(router.urls)),
    # todo: 弄清楚传入的字典是什么目的，有什么用，难道只支持 get put post delete 吗？
    path("", IndexViewSet.as_view({"get": "index"})),
]
