"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from apps.ninjaapi.routers import api as ninjaapi_api
from apps.powernetwork.views import router as powernetwork_router
from apps.testdrfapi.views import router as drfapi_router
from apps.account import views as account_views

urlpatterns = [
    path('powernetwork/', include(powernetwork_router.urls)),
    path('testdrfapi/', include(drfapi_router.urls)),
    path('login', account_views.LoginAPIView.as_view()),
    path('logout', account_views.LogoutAPIView.as_view()),

    path('api/', ninjaapi_api.urls),
]

if settings.DEBUG:
    urlpatterns += [
        # django 后台面板，app 下的 admin.py 的目的就是这个，用于管理后台
        path('admin/', admin.site.urls),

        # DRF 的可浏览 API 认证
        # 用于测试和开发环境，生产环境应使用更安全的认证方式(Token, JWT等)
        # api-auth/ 可以自由修改。登录视图：api-auth/login/，注销视图：api-auth/logout/
        path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
