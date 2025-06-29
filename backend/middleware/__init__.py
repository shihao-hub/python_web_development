from django.urls import reverse
from django.http import HttpResponseRedirect


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
