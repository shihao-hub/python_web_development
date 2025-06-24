__all__ = ["api"]

import traceback

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest
from ninja_extra import NinjaExtraAPI

from apps.ninjaapi.utils import ORJSONParser

# staff_member_required -> 访问 API 文档需要登录
api = NinjaExtraAPI(parser=ORJSONParser(), docs_decorator=None)

api.add_router("/chatgpt", "apps.ninjaapi.routersets.chatgpt.router")
