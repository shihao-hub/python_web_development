import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = Path(__file__).resolve().parent.parent.parent  # 项目根目录

# sys.path.insert(0, os.path.join(BASE_DIR, ".."))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "lyv+won7%7!=ra!nc160o-x1yz+m%n1jxm)wtw_y1r3%shh@-%X"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    "djangoorm.app",  # noqa: Unresolved reference 'djangoorm'
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "test_db.sqlite3") if DEBUG else os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True  # 启用国际化

USE_TZ = False  # 禁用 UTC 时区（建议国内项目关闭，直接使用本地时间）


# -------------------------------------------------------------------------------------------------------------------- #

# todo: 确定一下，本属于 django settings 的配置，如果此处覆盖了，对于使用 django orm 使用有影响，我认为没有隔离的必要性！
#       突然发现，class xxx 在 settings.py 中 django.conf 不会解析，所以我认为可以分离一下 nicegui 与 django orm ！
class nicegui_settings:  # noqa: Class names should use CapWords convention
    """临时充当 settings.py 使用的类"""

    DEBUG = DEBUG
    ROOT_DIR = ROOT_DIR

    UPGRADING = False

    STATIC_DIR = ROOT_DIR / "static"

    UPLOADED_DIR = ROOT_DIR / "storage" / "uploads"

    CACHE_TTL = 60 * 60 * 12 if not DEBUG else 2  # 缓存的时间

    TITLE = "心悦卿兮的饥荒模组合集"
    FAVICON = "🌿"
    HOST = "localhost"
    PORT = 15001
    RECONNECT_TIMEOUT = 10
    NATIVE = False
