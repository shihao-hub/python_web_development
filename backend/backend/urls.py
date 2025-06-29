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
from django.contrib.auth import views as auth_views
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', include("apps.index.urls")),
    path('powernetwork/', include("apps.powernetwork.urls")),

    # rest_framework_simplejw
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取 Token 对
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 Access Token

    # apps.index：生成一个欢迎页面 protocol://domain:port

    # 基于 session 的认证，适用于前后端不分离的项目，目前先用这个实现登录页面
    # 但是目前认为，未来这边肯定需要增加逻辑用来支持生成 token
    path('api-session-auth/', include('rest_framework.urls', namespace='rest_framework')),  # DRF 的可浏览 API 认证

    # path('api-token-auth/', views.obtain_auth_token),  # DRF 自带的 token 认证
    path('api-docs/', include_docs_urls(title='DRF API 文档', description='无')),  # DRF 自带的文档

    path('admin/', admin.site.urls),  # django 后台面板，app 下的 admin.py 的目的就是这个，用于管理后台
]

if settings.CUSTOM_DEBUG:
    from apps.ninjaapi.routers import api as ninjaapi_api

    urlpatterns += [
        path('debug/testdrfapi/', include("apps.testdrfapi.urls")),

        path('debug/testaccount/', include("apps.testaccount.urls")),

        # [to be deleted]
        path('debug/api/', ninjaapi_api.urls),
    ]
