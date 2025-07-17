"""
试图直接操作 sqlite，即我想入门 sqlite

SQLite As An Application File Format: https://www.sqlite.org/appfileformat.html

"""

import sqlite3
import os

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
    conn.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    );
    """)
    conn.commit()

    # 插入文档
    conn.execute("INSERT INTO documents (title, content) VALUES (?, ?)",
                 ("First Doc", "This is the content of the first document."))
    # 查询文档
    cursor = conn.execute("SELECT id, title FROM documents")
    for row in cursor:
        print(f"ID: {row[0]}, Title: {row[1]}")

    # 保存更改
    conn.commit()


if __name__ == '__main__':
    test()
