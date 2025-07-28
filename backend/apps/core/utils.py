import sqlite3
from typing import Annotated, Type

from loguru import logger

from django.http.request import HttpRequest
from django import forms
from django.db import models

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


class HttpRequestProxy:
    """django request proxy"""

    def __init__(self, request: HttpRequest):
        self._request = request

    def value(self) -> HttpRequest:
        """返回 request """
        return self._request

    def is_form_request(self):
        """用户的请求是通过表单 POST 提交数据的"""
        # 注意，django 对于表单和 json 有不一样的处理。而且，forms.py 主要还是给表单使用的。
        return self._request.content_type in ["application/x-www-form-urlencoded", "multipart/form-data"]

    def is_json_request(self):
        """用户的请求是通过 JSON POST 提交数据的"""
        return self._request.content_type == "application/json"

    def save_by_form(self, model_form: Type[forms.ModelForm]) -> bool:
        """通过 Form 类直接保存数据"""
        if self._request.method != "POST":
            raise exceptions.NotAllowedMethodError(self._request.method)
        # 使用了自定义的 For m类对用户提交的数据(request.POST)进行验证，并将通过验证的数据存入数据库。
        form = model_form(self._request.POST)
        if form.is_valid():
            form.save()
            return True
        return False
