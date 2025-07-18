import sqlite3
from typing import Annotated

from loguru import logger

from . import exceptions


class Cache:
    def __init__(self):
        self._conn = sqlite3.connect(":memory:")
        self._create_schema()
        self._set_user_version(1)

    def _create_schema(self):
        """创建初始表结构"""
        self._conn.executescript("""
        CREATE TABLE IF NOT EXISTS cache_ss_kv (
            key TEXT PRIMARY KEY NOT NULL, -- 键
            value TEXT NOT NULL, -- 值
            expire_on REAL -- 过期时间戳
        );
        """)
        self._conn.commit()

    def _set_user_version(self, version: int):
        """使用 PRAGMA user_version 管理架构版本"""
        self._conn.execute(f"PRAGMA user_version = {version}")
        self._conn.commit()

    def get(self, key: str):
        if not isinstance(key, str):
            raise exceptions.TypeCheckError(key, str)

        cursor = self._conn.execute("SELECT value FROM cache_ss_kv WHERE key = ?", (key,))  # noqa
        row = cursor.fetchone()
        if row is None:
            return None
        logger.info("value type: {}", type(row[0]))
        return row[0]

    def set(self, key: str, value: str, retention_time: Annotated[float, "保留时间"] = None):
        if not isinstance(key, str):
            raise exceptions.TypeCheckError(key, str)
        if not isinstance(value, str):
            raise exceptions.TypeCheckError(value, str)

        # update or insert
        cursor = self._conn.execute("SELECT value FROM cache_ss_kv WHERE key = ?", (key,))  # noqa
        row = cursor.fetchone()
        if row is None:
            self._conn.execute("INSERT INTO cache_ss_kv (key, value) VALUES (?, ?)", (key, value))  # noqa
        else:
            self._conn.execute("UPDATE cache_ss_kv SET value = ? WHERE key = ?", (value, key))  # noqa
        # todo: retention_time -> expired_on = time.time() + retention_time
        self._conn.commit()

    def __repr__(self):
        cursor = self._conn.execute("SELECT * FROM cache_ss_kv")  # noqa
        rows = cursor.fetchall()
        if rows is None:
            return "<Cache: empty>"
        max_len = 10
        formated = ", ".join(map(str, rows[:max_len]))
        if len(rows) > max_len:
            formated += f", ...[{len(rows) - max_len} remaining]"
        return f"<Cache: {formated}>"
