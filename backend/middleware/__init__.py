import requests
from loguru import logger

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse


# todo: 为了安全起见，需要在此处做权限认证，因为我发现，哪怕是基于 drf 框架的插件，权限居然用的不是 drf 的
# 不对，我只要保证我的所有接口都是 drf 实现的不就行了？如果用到了第三方插件，则需要验一下。


class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # todo: 确认一下，是不是 cookies/token/jwt 任何一个通过都行，还是说按顺序校验的？那岂不是无法复用 django 的登录页面了？
        # 1. Django 并不支持同一个浏览器中同一个域名下的多个独立会话，因为 HTTP 协议和浏览器的同源策略决定了 cookie 是共享的
        # 2. 对于 Django 管理页面，默认情况下我们通常不需要多个独立会话。
        #    但如果你有特殊需求，比如同时操作多个账户，你可能需要自定义认证中间件，使其能够同时处理多个会话。
        #    这通常比较复杂，因为需要改变 Django 的认证流程。

        # 问题复现流程：
        # tab1 为 admin/ 登录 username=admin 用户，注销后，浏览器保存的 session 失效
        # tab2 为 index/ 登录 username=guest 用户，此时浏览器保存的是 guest 的 session
        # 接着，进入 tab1 登录 admin/，由于此时携带了 guest 的 session，导致权限校验失败，执行此处的重定向逻辑了！
        # 至于为什么权限校验失败，那自然是 admin/login/ 这个接口还会进行角色校验！guest 用户不是 superuser

        # 临时结论：
        # 无法复用 django 自带的登录页面，可能需要自己实现一份了。除非我不需要提供 admin/ 给甲方。

        # 如果响应是 401 Unauthorized/403 Forbidden，则重定向到登录页
        # logger.info("response.status_code: {}", response.status_code)

        # nicegui app amount django_app，为什么 django 的请求日志消失了？
        if response.status_code == 404:
            logger.info("{} {}", request.path, response.status_code)

        # logger.debug("{}", request.path)
        if response.status_code in [401, 403]:
            login_url = reverse('rest_framework:login')
            redirect_url = f"{login_url}?next={request.path}"
            return HttpResponseRedirect(redirect_url)

        return response
