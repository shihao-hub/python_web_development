from django.urls import path, include
from rest_framework import routers

from .views import IndexViewSet, SessionInvitationCodeViewSet, HeartBeatViewSet

router = routers.DefaultRouter()
# {basename}-{func_name} 是对于路由的 name
# 注意，router.register 的 viewset 中的方法，url: temp/{url_path} 且 url_path 不为空，所以不可能有 temp/ 这样的路径
router.register("session_invitation_code", SessionInvitationCodeViewSet, basename="session_invitation_code")
router.register("heart_beat", HeartBeatViewSet, basename="heart_beat")

urlpatterns = [
    path("index/", include(router.urls)),
    # todo: 弄清楚传入的字典是什么目的，有什么用，难道只支持 get put post delete 吗？
    path("", IndexViewSet.as_view({"get": "index"})),
]
