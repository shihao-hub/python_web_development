"""
试图直接操作 sqlite，即我想入门 sqlite

SQLite As An Application File Format: https://www.sqlite.org/appfileformat.html

"""

import sqlite3
import os
import functools
from datetime import datetime

import pytz

# 【知识点】明确指定时区为中国标准时间
tz_shanghai = pytz.timezone("Asia/Shanghai")
now = functools.partial(datetime.now, tz=tz_shanghai)


# 注册适配器和转换器，原因：
# DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12;
# see the sqlite3 documentation for suggested replacement recipes
sqlite3.register_adapter(datetime, lambda dt: dt.isoformat())
sqlite3.register_converter("datetime", lambda ts: datetime.fromisoformat(ts.decode()))

# DDL: 数据定义语言
DDL = """

"""


# DML: 数据操纵语言


# POP：面向过程
# 1. 创建数据库表
# 2. 初始化数据（如插入默认数据）
# 至此，数据库创建完毕，后续最主要的就是 DML SQL 语句了吧？但是有必要进一步了解 sqlite 官方提供的能力

# 题外话：
# 1. 如非必要，勿增实体，那么关于 RabbitMQ，也有什么开箱即用的工具吗？
# 2. 关于 django 提供的很多能力，在不允许 django 的情况下能否使用呢？比如：ORM 就可以单独使用！


class AppDatabase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.conn = None

    def initialize(self):
        """初始化数据库文件"""
        is_new_db = not os.path.exists(self.file_path)

        self.conn = sqlite3.connect(self.file_path)

        if is_new_db:
            self._create_schema()
            self._set_user_version(1)  # 设置用户版本
        else:
            self._migrate_schema()

    def _create_schema(self):
        """创建初始表结构"""
        self.conn.execute("""
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TRIGGER update_timestamp 
        AFTER UPDATE ON documents 
        BEGIN
            UPDATE documents SET modified_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
        END;
        """)
        self.conn.commit()

    def _set_user_version(self, version):
        """使用 PRAGMA user_version 管理架构版本"""
        self.conn.execute(f"PRAGMA user_version = {version}")
        self.conn.commit()

    def _get_user_version(self):
        """获取当前架构版本"""
        cursor = self.conn.execute("PRAGMA user_version")
        return cursor.fetchone()[0]

    def _migrate_schema(self):
        """执行架构迁移"""
        current_version = self._get_user_version()

        if current_version < 2:
            # 示例：从版本1迁移到版本2
            self.conn.execute("ALTER TABLE documents ADD COLUMN author TEXT DEFAULT 'Unknown'")
            self._set_user_version(2)

        # 添加更多迁移步骤...

    def save_document(self, title, content, author=None):
        """保存文档到数据库"""
        self.conn.execute("""
        INSERT INTO documents (title, content, author)
        VALUES (?, ?, ?)
        """, (title, content, author))
        self.conn.commit()

    def search_documents(self, keyword):
        """搜索文档"""
        cursor = self.conn.execute("""
        SELECT id, title, snippet(documents, 2, '<b>', '</b>', '...', 20) AS snippet
        FROM documents
        WHERE content MATCH ?
        ORDER BY rank
        """, (keyword,))

        return cursor.fetchall()

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()


def test():
    conn = sqlite3.connect("./just_sqlite_db.sqlite")
    # 【知识点】sqlite 类型 INTEGER 才能自增 AUTOINCREMENT，INT 居然不行！
    # todo: 每次执行都要创建一下吗？还是说其实 DDL 语句并不是在程序中执行的，而是程序启动前。
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS COMPANY(
        ID INTEGER PRIMARY KEY,
        NAME           TEXT    NOT NULL, -- 设定为主键后，数据库自动建立索引？
        AGE            INT     NOT NULL,
        ADDRESS        CHAR(50),
        SALARY         REAL,
        is_deleted INTEGER DEFAULT false,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS AUDIT(
        EMP_ID INT NOT NULL,
        ENTRY_DATE TEXT NOT NULL
    );
    
    CREATE TRIGGER IF NOT EXISTS audit_log AFTER INSERT ON COMPANY
    BEGIN
        INSERT INTO AUDIT(EMP_ID, ENTRY_DATE) VALUES (NEW.ID, NEW.updated_at);
    END;
    """)
    conn.commit()

    conn.execute("INSERT INTO COMPANY (NAME, AGE, created_at, updated_at) VALUES (?, ?, ?, ?)", (
        "Google",
        20,
        now(),
        now()
    ))
    conn.commit()

    cursor = conn.execute("SELECT * FROM COMPANY")
    for row in cursor:
        print(f"{row}")

    conn.commit()


if __name__ == '__main__':
    test()
