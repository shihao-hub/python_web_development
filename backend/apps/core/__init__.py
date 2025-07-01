__all__ = ["handle_unexpected_exception", "SuccessResponse", "ErrorResponse"]

import functools
import socket
from typing import Optional, Union, Dict, List

from loguru import logger

from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self,
                 data: Optional[Union[Dict, List]] = None,
                 message="Operation successful",
                 pagination: Optional[Dict] = None,
                 **kwargs):
        """
        初始化成功响应

        :param data: 返回数据
        :param message: 成功消息
        :param pagination: 分页信息
        """

        response_data = {
            "data": data,
            "message": message,
        }
        if pagination is not None:
            response_data["pagination"] = pagination
        super().__init__(data=response_data, status=200, **kwargs)


class ErrorType:
    """ 常用错误类型常量 """
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTH_FAILED = "AUTHENTICATION_FAILED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_FOUND = "RESOURCE_NOT_FOUND"
    CONFLICT = "RESOURCE_CONFLICT"
    THROTTLED = "REQUEST_THROTTLED"
    SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"


class ErrorCode:
    """ 常用错误码常量 """
    # 通用错误 (10xxx)
    VALIDATION_FAILED = 10001
    INVALID_INPUT = 10002

    # 认证错误 (20xxx)
    TOKEN_EXPIRED = 20001
    INVALID_CREDENTIALS = 20002
    ACCOUNT_DISABLED = 20003

    # 资源错误 (30xxx)
    RESOURCE_NOT_FOUND = 30001
    RESOURCE_CONFLICT = 30002

    # 业务错误 (40xxx)
    INSUFFICIENT_BALANCE = 40001
    OPERATION_LIMITED = 40002

    # 服务器错误 (50xxx)
    DATABASE_ERROR = 50001
    INTERNAL_ERROR = 50000


class ErrorResponse(Response):
    def __init__(self,
                 message: str,
                 status: int = 500,
                 details: Optional[Union[List, Dict]] = None,
                 documentation: Optional[str] = None,
                 code: int = 0,
                 error_type: str = "",
                 **kwargs):
        """
        初始化错误响应

        :param message: 错误摘要
        :param details: 错误详情
        :param status: HTTP 状态码
        :param documentation: 文档链接
        :param code: 业务错误码 【未实际使用，暂且默认为 0】
        :param error_type: 错误类型（机器可读）【未实际使用，暂且默认为 ""】
        """
        response_data = {
            "message": message,
            # 暂且如此
            # "details": details,
            # "documentation": "",
            # "code": code,
            # "error_type": error_type,
        }
        super().__init__(data=response_data, status=status, **kwargs)


def handle_unexpected_exception(func):
    """ Decorator to handle unexpected exceptions in API views """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return ErrorResponse("Unexpected error occurred")

    return wrapper


def find_available_port(start_port=8888, max_retry=50):
    port = start_port
    while port <= start_port + max_retry:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
        port += 1
    raise Exception("No available ports")
