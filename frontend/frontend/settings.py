import configparser
from pathlib import Path

# todo: 这个打包之后就存在问题了呀！
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

config = configparser.ConfigParser()
# fixme: 这个路径容易找不到！
config.read(ROOT_DIR / "conf" / "config.ini")

TITLE = "柔性配电评估系统"
HOST = "localhost"
PORT = 12000  # config.getint("settings", "frontend_port")

SECRET_KEY = 'django-insecure-ok))2mb#mev0$i$9i9-c9130*r26iveph$$=-927l(uwp9i4(k'
