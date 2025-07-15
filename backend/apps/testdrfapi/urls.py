from django.urls import path, include
from rest_framework import routers

from .views import (
    UserModelViewSet, GroupModelViewSet,
    TestViewSet, CourseViewSet,
    course_list, course_detail,
    CourseList, CourseDetail,
    GCourseDetail,
    jupyternotebooks_test,
)

# 2025-07-15：
# 暂且注释掉 router 相关内容
# 目前对于 router 的理解如下：
# - router 有些特别，对于 path(r"", include(router.urls)) 而言，url 为 {path's route}/{router's url_path}（必有 / 分隔）
# - 【待确认】router 中使用 @decorators.action，其 url_path 参数不允许以 / 开头（似乎也不能以 / 结尾？）

# router = routers.DefaultRouter()
# router.register(r'users', UserModelViewSet)
# router.register(r'groups', GroupModelViewSet)
# # router.register(r'test', TestViewSet, basename='test')
# router.register(r'viewset', CourseViewSet, basename='viewset')

urlpatterns = [
    # path(r"", include(router.urls)),

    path(r"jupyternotebooks/test/", jupyternotebooks_test, name="jupyternotebooks_test"),

    # summary: 本人目前推荐使用的是：ModelViewSet, ViewSet, decorators.action, APIView 等
    # todo: drf 细节继续理解，推荐一定记个笔记，关于 fbv cbv gcbv 等...
    path(r"fbv/list/", course_list, name="fbv-list"),
    path(r"fbv/detail/<int:pk>/", course_detail, name="fbv-detail"),

    path(r"cbv/list/", CourseList.as_view(), name='cbv-list'),
    path(r"cbv/detail/<int:pk>/", CourseDetail.as_view(), name='cbv-detail'),

    # path(r"gcbv/list/", GCourseList.as_view(), name='gcbv-list'),
    path(r"gcbv/detail/<int:pk>/", GCourseDetail.as_view(), name='gcbv-detail'),
]
