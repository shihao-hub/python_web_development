import contextlib
from pathlib import Path

import cachetools
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL, ROOT_DIR, STATIC_DIR

# todo: 确定一下是否需要 __all__ = []，如果不需要，参考第三方库，不对外的如何命名？

# 数据库配置
Base = declarative_base()

# 创建数据库引擎
is_sqlite = DATABASE_URL.startswith("sqlite")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if is_sqlite else {},
    execution_options={"isolation_level": "SERIALIZABLE"} if is_sqlite else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


@contextlib.contextmanager
def get_db() -> sqlalchemy.orm.session.Session:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @cachetools.cached(cachetools.TTLCache(maxsize=20, ttl=60 * 5))
def read_static_file(relative_path: str) -> str:
    """读取 static 文件"""
    filepath = ROOT_DIR / "static"
    for part in Path(relative_path).parts:
        filepath = filepath / part
    if not filepath.exists():
        raise FileNotFoundError(f"文件 `{relative_path}` 不存在")
    return filepath.read_text("utf-8")  # 进行了一层封装


# @cachetools.cached(cachetools.TTLCache(maxsize=20, ttl=60 * 5))
def read_markdown_file(relative_path: str):
    """读取 markdown 文件"""
    markdown_path = STATIC_DIR / "markdown" / Path(relative_path)
    return markdown_path.read_text("utf-8")
