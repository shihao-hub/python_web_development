from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    """实现全站要求登录，但是登录页面和开放白名单上的urls除外"""

    def __init__(self, get_response):
        self.get_response = get_response
        self._login_url = settings.LOGIN_URL
        # 开放白名单，比如['/login/', '/admin/']
        # todo: OPEN_URLS 需要考虑冲突问题，建议学习 drf，一个字典作为命名空间
        self._open_urls = [self._login_url] + getattr(settings, "OPEN_URLS", [])

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info not in self._open_urls:
            return redirect(self._login_url + '?next=' + request.get_full_path())

        response = self.get_response(request)
        return response
