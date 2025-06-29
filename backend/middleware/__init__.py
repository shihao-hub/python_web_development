import requests
from loguru import logger

from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse


class LoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 如果响应是 401 Unauthorized/403 Forbidden，则重定向到登录页
        if response.status_code in [401, 403]:
            login_url = reverse('rest_framework:login')
            redirect_url = f"{login_url}?next={request.path}"
            return HttpResponseRedirect(redirect_url)

        return response


# fixme: 待删除
class ReverseProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # todo: 这只是让响应结果在此处显示而已，但是目标又不是静态页面啊。这不对！
        # 只处理根路径请求
        if request.path == '/':
            # 目标服务地址（端口12000）
            target_url = f'http://127.0.0.1:12000{request.path}'

            logger.debug("{}", request.headers)
            logger.debug("{}", {
                    key: value
                    for (key, value) in request.headers.items()
                    if key.lower() not in ['host', 'content-length']
                })

            # 转发请求并获取响应
            resp = requests.get(
                target_url,
                headers={
                    key: value
                    for (key, value) in request.headers.items()
                    if key.lower() not in ['host', 'content-length']
                },
                cookies=request.COOKIES,
                allow_redirects=False
            )

            logger.debug("{}", resp.headers)

            # 构建 Django 响应对象
            response = HttpResponse(
                content=resp.content,
                status=resp.status_code,
                reason=resp.reason
            )

            # 复制响应头
            for key, value in resp.headers.items():
                if key.lower() != 'content-encoding':  # 避免编码冲突
                    response[key] = value
            return response

        return self.get_response(request)