from django.urls import path, include
from rest_framework import routers

from .views import (
    UserModelViewSet, GroupModelViewSet, TestViewSet,
    CourseList,
    course_list, course_detail,
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)
router.register(r'groups', GroupModelViewSet)
router.register(r'test', TestViewSet, basename='test')

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"fbv/course_list/", course_list, name="fbv-course_list"),
    path(r"fbv/detail/<int:pk>", course_detail, name="fbv-course_detail"),
    path(r"cbv/list/", CourseList.as_view(), name='cbv-list')
]
