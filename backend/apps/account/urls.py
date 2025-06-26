from django.urls import path, include
from rest_framework import routers

from .views import LoginLogoutViewSet, UserDetailModelViewSet

router = routers.DefaultRouter()
# todo: 为什么此处和另一个 app 中都定义了 ModelViewSet queryset = User.objects.all() 会导致 url 冲突
# router.register(r"userdetail", UserDetailModelViewSet)

# todo: [to be understood] why the router is not working(api doc is not showing)
router.register(r"loginlogout", LoginLogoutViewSet, basename="login-logout")

urlpatterns = [
    path("", include(router.urls)),
    # todo: use as_views
    # path("login/",LoginLogoutViewSet),
]
