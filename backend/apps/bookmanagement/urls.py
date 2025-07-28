from django.urls import path
from rest_framework import routers

from . import views

app_name = "bookmanagement"

router = routers.DefaultRouter()
router.register("", views.BookViewSet)

urlpatterns = [
    path("advanced/", views.BookAdvancedAPIView.as_view())
]

urlpatterns += router.urls
