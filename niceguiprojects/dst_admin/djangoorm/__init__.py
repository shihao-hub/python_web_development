__all__ = [
    "load_djangoorm"
]

import os

# 必须在导入 django 内容前设置 DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoorm.djangoorm.settings")

from django.apps import apps  # noqa
from django.conf import settings  # noqa

# 把所有的 app 加载到 Django 里
apps.populate(settings.INSTALLED_APPS)


def load_djangoorm(migrate=True):
    """使用 djangoorm 的项目入口必须调用的方法"""
    from django.core.management import call_command

    if migrate:
        call_command("makemigrations", "app")
        call_command("migrate", "app")
