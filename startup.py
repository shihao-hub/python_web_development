import os

import uvicorn
from loguru import logger

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # 配置 Django 环境
django_app = get_wsgi_application()  # 获取 Django WSGI/ASGI 应用

fastapi_app = FastAPI(title="混合应用")

logger.info("startup file path: {}", __file__)


@fastapi_app.get("/fastapi-endpoint")
def read_fastapi():
    return {"message": "来自 FastAPI"}


# 挂载 Django 应用到 /django 路径。注意：Django 的 STATIC_URL 也得改。
# fastapi_app.mount("/django", django_app)
fastapi_app.mount("/django", WSGIMiddleware(django_app))

# 挂载 Django 静态文件
# fastapi_app.mount(
#     "/django/static",
#     StaticFiles(directory=os.path.join(os.path.dirname(__file__), "backend", "staticfiles")),
#     name="django_static"
# )

# todo: 探索为什么挂载后，django 静态文件无法访问

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="localhost", port=8887)
