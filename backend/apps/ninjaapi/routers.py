__all__ = ["api"]

from ninja_extra import NinjaExtraAPI

from apps.ninjaapi.utils import ORJSONParser
from apps.ninjaapi.handlers.error_handlers import register_global_handlers

# staff_member_required -> 访问 API 文档需要登录
api = NinjaExtraAPI(parser=ORJSONParser(), docs_decorator=None)

api.add_router("/chatgpt", "apps.ninjaapi.routersets.chatgpt.router")
api.add_router("/tools", "apps.ninjaapi.routersets.tools.router")

register_global_handlers(api)
