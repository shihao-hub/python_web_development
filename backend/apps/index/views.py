import pprint
from typing import Union
from urllib.parse import urljoin

from loguru import logger

from django.shortcuts import redirect
from django.conf import settings
from django.views import View
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpRequest, HttpResponseRedirect, HttpResponsePermanentRedirect
from rest_framework import views, viewsets, decorators, generics
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core import handle_unexpected_exception, SuccessResponse, ErrorResponse


class IndexViewSet(viewsets.ViewSet):
    def index(self, request: Union[Request, HttpRequest]):
        """ 登录成功后重定向到前端页面 """

        # 永久重定向用 301，临时用 302
        logger.debug("request.COOKIES: {}", request.COOKIES)
        logger.debug("request.session: {}", request.session)

        # 重定向到 /home
        response = redirect("http://127.0.0.1:12000/home", permanent=False)

        # 显式设置跨域 Cookie（关键步骤）
        response.set_cookie(
            key="sessionid",  # Django 默认 Session Cookie 名称
            value=request.session.session_key,
            domain="127.0.0.1",  # 与 SESSION_COOKIE_DOMAIN 一致
            max_age=settings.SESSION_COOKIE_AGE,
            # todo: [to be understood] samesite, secure, httponly?
            samesite="None",  # 必须为 None 才能跨域
            secure=False,  # 开发环境可关闭
            httponly=True,  # 增强安全性
        )

        # 添加 CORS 响应头（确保浏览器接受跨域凭据）
        response["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
        response["Access-Control-Allow-Credentials"] = "true"

        logger.debug("response.headers: {}", response.headers)
        logger.debug("response.COOKIES: {}", response.cookies)

        # todo: 以上代码需要验证，后续如果能签下来，需要在写前端的时候通过 debug 的方式来确认，所以还要学习前端知识

        # todo: 实现 admin 用户和普通用户的区分，比如 admin/ 只能是管理员账号才能登录

        # todo: 确定一下为什么 admin/ 退出登陆，另一半也推出了，如果账号不一样是不是就没问题了

        return response


class SessionInvitationCodeViewSet(viewsets.ViewSet):
    # [note] url_path == "" 似乎视作 None
    # [note] url_path 必须形如 a/b，前后缀不能有 /，/ 会自动被添加
    # [note] 装饰器生成的路由除了 index/，还有 index.(?P<format>[a-z0-9]+)/，似乎设置为 detail = True 就有用了
    @decorators.action(detail=False, methods=['get'])
    def index(self, request: Request):
        pass

    @decorators.action(detail=True, methods=['get'])
    def index2(self, request):
        pass


class HeartBeatViewSet(viewsets.ViewSet):
    @decorators.action(detail=False, methods=["get"])
    def verify_identity(self, request: HttpRequest):
        """ 单纯提供一个端口，用来调用，判断是否被 middleware 拦截，以验证身份 """
        return SuccessResponse()
