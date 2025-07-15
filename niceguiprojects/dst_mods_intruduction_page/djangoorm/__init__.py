__all__ = [
    "load_djangoorm",
    "settings",  # todo: 确定一下这是 django.conf 的 settings，有很多多余的东西，单纯使用 django orm 是否需要呢？
    "nicegui_settings",
    "models",
    "utils"
]


def _execute_before_anything():
    import os

    # 必须在导入 django 内容前设置 DJANGO_SETTINGS_MODULE
    # 注意，按照我目前的理解，启动整个项目的入口文件与 djangoorm 目录应该是同级的才行
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoorm.djangoorm.settings")

    from django.apps import apps
    from django.conf import settings

    # 把所有的 app 加载到 Django 里
    apps.populate(settings.INSTALLED_APPS)


_execute_before_anything()

from django.conf import settings

from .app import models, utils  # 注意，此处需要用 .app 的方式才能找到对于 Python Package
from .djangoorm.settings import nicegui_settings  # 注意，django.conf 的 settings 无法将 settings.py 中的 class 解析！


def load_djangoorm(migrate=True):
    """使用 djangoorm 的项目入口必须调用的方法"""
    from django.core.management import call_command

    if migrate:
        call_command("makemigrations", "app")
        call_command("migrate", "app")
