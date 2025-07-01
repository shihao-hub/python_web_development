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
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # index[special case] 需要特殊对待
    path('', include("apps.index.urls")),

    path('powernetwork/', include("apps.powernetwork.urls")),

    # drf 自带的 token 认证，调用获得 token。前端需要将 token 放在请求头中，key 为 Authorization，value 为 Token <token>
    path('api-token-auth/', views.obtain_auth_token),

    # [note] drf 的这个 session 认证和 django admin 是同一个，假如 admin/ 退出登录，这边的登录也会失效
    # 基于 session 的认证，适用于前后端不分离的项目，目前先用这个实现登录页面，未来这边肯定需要增加逻辑用来支持生成 token
    path('api-session-auth/', include('rest_framework.urls', namespace='rest_framework')),  # DRF 的可浏览 API 认证

    # rest_framework_simplejw
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 获取 Token 对
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新 Access Token

    # drf_spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),  # OpenAPI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),  # 交互式文档
    # 并不如 swagger-ui 友好
    # path('api/redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='redoc'),

    # djang admin
    path('admin/', admin.site.urls),  # django 后台面板，app 下的 admin.py 的目的就是这个，用于管理后台
]

if settings.CUSTOM_DEBUG:
    from apps.ninjaapi.routers import api as ninjaapi_api

    urlpatterns += [
        path('debug/testdjangoapi/', include("apps.testdjangoapi.urls")),

        path('debug/testdrfapi/', include("apps.testdrfapi.urls")),

        path('debug/testaccount/', include("apps.testaccount.urls")),

        # [to be deleted]
        path('debug/ninjaapi/', ninjaapi_api.urls),
    ]
