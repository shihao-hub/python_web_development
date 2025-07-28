from typing import Union

from loguru import logger

from django.http.request import HttpRequest
from django_filters import rest_framework as rest_framework_filters
from rest_framework import views, generics, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from . import models, serializers, filters, schemas


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer

    # 【知识点】django_filters，让过滤如此简单
    filterset_class = filters.BookFilter


class BookAdvancedAPIView(views.APIView):
    def post(self, request: Union[HttpRequest, Request]):
        # 多维度图书检索：支持组合条件搜索 + 全文检索
        models.Book.objects.annotate()

    def get(self, request: Union[HttpRequest, Request]):
        ret5 = models.Book.objects.filter(name="Python").values("author__first_name")
        logger.debug("{}", ret5)
        logger.debug("{}", ret5.query)
        ret6 = models.Book.objects.filter(author__first_name="alex").values("name")
        logger.debug("{}", ret6)
        logger.debug("{}", ret6.query)

        return Response({"message": "advanced!"})
