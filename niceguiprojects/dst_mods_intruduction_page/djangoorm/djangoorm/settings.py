import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# sys.path.insert(0, os.path.join(BASE_DIR, ".."))

SECRET_KEY = "lyv+won7%7!=ra!nc160o-x1yz+m%n1jxm)wtw_y1r3%shh@-%X"

DEBUG = True

INSTALLED_APPS = [
    "djangoorm.app",  # noqa: Unresolved reference 'djangoorm'
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "test_db.sqlite3") if DEBUG else os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
