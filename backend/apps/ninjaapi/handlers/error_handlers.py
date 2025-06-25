import traceback

from loguru import logger
from pydantic import ValidationError

from django.conf import settings
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from ninja.errors import HttpError
from ninja_extra import NinjaExtraAPI


def register_global_handlers(api: NinjaExtraAPI):
    """
    注册全局异常处理器
    """

    # 1. 处理验证错误（Pydantic 模型验证失败）
    @api.exception_handler(ValidationError)
    def handle_validation_error(request, exc: ValidationError):
        errors = []
        for error in exc.errors():
            field = ".".join(map(str, error["loc"]))
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"]
            })

        return api.create_response(
            request,
            {
                "success": False,
                "code": "VALIDATION_ERROR",
                "message": "输入验证失败",
                "errors": errors
            },
            status=422
        )

    # 2. 处理权限错误
    @api.exception_handler(PermissionDenied)
    def handle_permission_denied(request, exc: PermissionDenied):
        return api.create_response(
            request,
            {
                "success": False,
                "code": "PERMISSION_DENIED",
                "message": "您没有执行此操作的权限"
            },
            status=403
        )

    # 3. 处理可疑操作（如路径遍历攻击）
    @api.exception_handler(SuspiciousOperation)
    def handle_suspicious_operation(request, exc: SuspiciousOperation):
        return api.create_response(
            request,
            {
                "success": False,
                "code": "SUSPICIOUS_OPERATION",
                "message": "检测到可疑操作",
                "details": str(exc)
            },
            status=400
        )

    # 4. 处理 HTTP 错误（自定义 HTTP 异常）
    @api.exception_handler(HttpError)
    def handle_http_error(request, exc: HttpError):
        return api.create_response(
            request,
            {
                "success": False,
                "code": f"HTTP_{exc.status_code}",
                "message": exc.message
            },
            status=exc.status_code
        )

    # 5. 全局捕获所有未处理异常
    @api.exception_handler(Exception)
    def handle_unexpected_exceptions(request, exc: Exception):
        # 记录完整的错误堆栈
        logger.error(f"未处理的异常: {str(exc)}\n{traceback.format_exc()}")

        # 生产环境不返回详细错误
        is_production = not settings.DEBUG
        details = "内部服务器错误" if is_production else str(exc)
        stack_trace = None if is_production else traceback.format_exc()

        return api.create_response(
            request,
            {
                "success": False,
                "code": "SERVER_ERROR",
                "message": "服务器内部错误",
                "details": details,
                "stack_trace": stack_trace
            },
            status=500
        )
