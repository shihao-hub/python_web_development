from pathlib import Path


class nicegui_settings:  # noqa: Class names should use CapWords convention
    """临时充当 settings.py 使用的类"""
    UPGRADING = False


DEBUG = True

UPGRADING = nicegui_settings.UPGRADING

# todo: 尽量多使用 Path，少用 os.path
ROOT_DIR = Path(__file__).resolve().parent  # 项目根目录
STATIC_DIR = ROOT_DIR / "static"

UPLOADED_DIR = ROOT_DIR / "storage" / "uploads"

CACHE_TTL = 60 * 60 * 12 if not DEBUG else 2  # 缓存的时间

TITLE = "心悦卿兮的饥荒模组合集"
FAVICON = "🌿"
HOST = "localhost"
PORT = 15001
