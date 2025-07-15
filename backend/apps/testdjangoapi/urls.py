from django.urls import path, include

from .views import TestTemplateView

urlpatterns = [
    # todo: 熟悉 drf 和 django 的所有视图类
    path("test/", TestTemplateView.as_view(), name="test"),
]
