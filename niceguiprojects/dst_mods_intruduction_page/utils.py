import contextlib

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_URL

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
