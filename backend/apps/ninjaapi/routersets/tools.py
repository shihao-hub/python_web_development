import functools
import io
import os
from typing import List, Dict

from django.http.request import HttpRequest
from django.http.response import FileResponse, JsonResponse
from django.conf import settings
from ninja import Router, Query, Body
from ninja.errors import HttpError
from ninja.responses import Response
from ninja.security import APIKeyHeader, HttpBearer

router = Router(tags=["tools"])


# 添加身份验证
class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "YOUR_SECRET_TOKEN":
            return token


# 添加速率限制
# ip = request.META.get('REMOTE_ADDR')
# cache_key = f"download_limit_{ip}"
# count = cache.get(cache_key, 0)
# if count > 10:  # 限制每小时10次下载
#     return JsonResponse({"error": "下载次数过多"}, status=429)
# cache.set(cache_key, count + 1, 3600)  # 1小时过期

def rate_limitation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


# 添加文件访问日志
# download_logger = logging.getLogger('downloads')
# # 在返回响应前添加
# download_logger.info(
#     f"用户 {request.user.username if request.user.is_authenticated else '匿名'} "
#     f"下载了文件: {safe_file_name}"
# )

@router.get("/get_gitignore_file_list", summary="列出可下载的文件")
def get_gitignore_file_list(request: HttpRequest):
    if not settings.RESOURCES_DIR.exists():
        raise HttpError(404, "Resources directory is not existent.")
    top_filenames = []
    for _, _, files in os.walk(settings.RESOURCES_DIR):
        top_filenames = files
    return {"data": top_filenames}


@router.post("/download_specified_gitignore_file", summary="下载指定文件")
def download_specified_gitignore_file(request: HttpRequest, filename: Query[str]):
    old_filename = filename
    filename = filename if filename.endswith(".gitignore") else filename + ".gitignore"
    filepath = settings.RESOURCES_DIR / "gitignore" / filename
    if not filepath.exists():
        raise HttpError(404, f"{old_filename} is not existent.")

    response = FileResponse(
        open(filepath, "rb"),
        as_attachment=True,
        filename=filename
    )

    response["Content-Type"] = "text/plain"

    return response
