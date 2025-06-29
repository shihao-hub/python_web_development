import pprint
from typing import Union
from urllib.parse import urljoin

from loguru import logger

from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponseRedirect
from rest_framework import views, viewsets, decorators
from rest_framework.request import Request
from rest_framework.response import Response

TARGET_SERVICE = "http://127.0.0.1:12000/"


class IndexViewSet0(viewsets.ViewSet):

    @decorators.action(detail=False, methods=['get'], url_path="")
    def index(self, request):
        pass


class IndexViewSet(viewsets.ViewSet):
    def index(self, request: Union[Request, HttpRequest]):
        # 永久重定向用 301，临时用 302
        return redirect("http://127.0.0.1:12000/", permanent=False)
