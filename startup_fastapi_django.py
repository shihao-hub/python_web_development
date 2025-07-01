import os
from importlib.util import find_spec

import uvicorn
from loguru import logger

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  # 配置 Django 环境
os.environ.setdefault("DJANGO_CONFIGURATIN", "Localdev")
django_app = get_wsgi_application()  # 获取 Django WSGI/ASGI 应用

# todo: 了解 runserver，因为我发现 settings.DEBUG 居然可以使用欸
# todo: 了解一下为什么正式环境需要收集所有静态资源？

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

# logger.debug("{}", os.path.normpath(
#                           os.path.join(find_spec("django.contrib.admin").origin, "..", "static")
#                       ))
# fastapi_app.mount("/django/static",
#                   StaticFiles(
#                       directory=os.path.normpath(
#                           os.path.join(find_spec("django.contrib.admin").origin, "..", "static")
#                       )
#                   ),
#                   name="django_static")

# todo: 探索为什么挂载后，django 静态文件无法访问
# 继续探索了一段时间，解决不了。ai 不能及时解决的内容，只能去找博客了！外网最佳。
# 但是我发现了 如何在 django 中使用 fastapi：https://www.5axxw.com/questions/simple/irlqub，我来看看
# 呃，好像不行。

# 警告：
# fastapi 挂载 django
# django 中使用 fastapi
# 8888 redirect 12000，等等
# 上述内容我找不到什么资料，结果花费我很多时间，啥都没捣鼓出来，是否应该放弃呢？（得追求利益、效率...）
# 举个例子，我是为了复用 django 的 admin 登陆功能，所以想 django 负责部分前端，
# 但是这花费了时间，收益却很小，而且还不如手动实现个登录系统，还能练习一下！
# 而且也不至于搞得不伦不类，特殊用法可以后续研究，但是最好还是规范点。
# 所以，定下规范：
# 在使用 nicegui 的时候，nicegui 就完全负责前端，django 只负责后端（admin/ 应该也属于后端）
# 花里胡哨可以有空的时候研究！高效一点！

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="localhost", port=8887)
