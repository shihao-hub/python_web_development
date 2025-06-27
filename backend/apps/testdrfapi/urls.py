from django.urls import path, include
from rest_framework import routers

from .views import (
    UserModelViewSet, GroupModelViewSet, TestViewSet,
    CourseList, CourseDetail,
    GCourseDetail,
    course_list, course_detail,
)

router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)
router.register(r'groups', GroupModelViewSet)
router.register(r'test', TestViewSet, basename='test')

urlpatterns = [
    path(r"", include(router.urls)),

    # summary: 本人目前推荐使用的是：ModelViewSet, ViewSet, decorators.action, APIView 等
    path(r"fbv/list/", course_list, name="fbv-list"),
    path(r"fbv/detail/<int:pk>/", course_detail, name="fbv-detail"),

    path(r"cbv/list/", CourseList.as_view(), name='cbv-list'),
    path(r"cbv/detail/<int:pk>/", CourseDetail.as_view(), name='cbv-detail'),

    # path(r"gcbv/list/", GCourseList.as_view(), name='gcbv-list'),
    path(r"gcbv/detail/<int:pk>/", GCourseDetail.as_view(), name='gcbv-detail'),
]
