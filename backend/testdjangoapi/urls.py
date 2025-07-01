from django.urls import path, include

from .views import TestTemplateView

urlpatterns = [
    path("test/", TestTemplateView.as_view(), name="test"),
]
