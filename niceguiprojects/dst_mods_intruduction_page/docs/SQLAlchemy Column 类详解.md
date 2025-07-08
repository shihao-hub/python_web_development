# SQLAlchemy `Column` 类详解

SQLAlchemy 是一个强大的 Python SQL 工具包和对象关系映射(ORM)系统。`Column` 类是 SQLAlchemy ORM 的核心组件，用于定义数据库表的列结构。下面我将详细解释 `Column` 类的构造函数参数：

## 基本结构

```python
from sqlalchemy import Column

class MyTable(Base):
    __tablename__ = 'my_table'
    
    # 基本用法
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
```

## 参数详解

### 1. 位置参数
- **`__name_pos` (位置参数1)**
  - 列名（字符串）或列类型（如 `Integer`, `String`）
  - 示例：`Column('user_id', Integer)` 或 `Column(Integer)`

- **`__type_pos` (位置参数2)**
  - 列类型（如果第一个位置参数是列名）
  - 示例：`Column('user_id', Integer)`

- **`*args`**
  - 其他模式相关对象，如外键约束
  - 示例：`Column(Integer, ForeignKey('users.id'))`

### 2. 命名参数

#### 核心属性
- **`name`**
  - 列名（字符串）
  - 示例：`Column(name='email', type_=String(255))`

- **`type_`**
  - 列的数据类型（`TypeEngine` 实例）
  - 常用类型：
  ```python
  Integer()      # 整数
  String(50)     # 字符串，长度为50
  Text()         # 长文本
  DateTime()     # 日期时间
  Boolean()      # 布尔值
  Float()        # 浮点数
  Numeric(10,2)  # 精确数字，10位总长度，2位小数
  JSON()         # JSON 数据
  ```

- **`primary_key`**
  - 是否为主键（布尔值）
  - 示例：`Column(Integer, primary_key=True)`

- **`nullable`**
  - 是否允许 NULL 值
  - 可选值：`True`, `False`, `SchemaConst.NULL_UNSPECIFIED`
  - 示例：`Column(String, nullable=False)`

- **`autoincrement`**
  - 自动递增设置
  - 可选值：
    - `'auto'`：自动判断（默认）
    - `True`：强制自增
    - `False`：非自增
  - 示例：`Column(Integer, autoincrement=True)`

#### 默认值相关
- **`default`**
  - Python 端的默认值（在对象创建时应用）
  - 示例：`Column(DateTime, default=datetime.utcnow)`

- **`insert_default`**
  - 插入时的默认值（已弃用，使用 `default` 代替）

- **`server_default`**
  - 数据库端的默认值（SQL 表达式）
  - 示例：`Column(DateTime, server_default=func.now())`

- **`onupdate`**
  - Python 端的更新时默认值
  - 示例：`Column(DateTime, onupdate=datetime.utcnow)`

- **`server_onupdate`**
  - 数据库端的更新时默认值
  - 示例：`Column(DateTime, server_onupdate=func.now())`

#### 约束与索引
- **`index`**
  - 是否为该列创建索引
  - 示例：`Column(String, index=True)`

- **`unique`**
  - 是否要求唯一值
  - 示例：`Column(String, unique=True)`

#### 元数据与文档
- **`doc`**
  - 列的文档字符串
  - 示例：`Column(String, doc="用户全名")`

- **`key`**
  - ORM 映射的属性名（可与列名不同）
  - 示例：`Column('user_id', Integer, key='id')`

- **`info`**
  - 附加信息字典
  - 示例：`Column(Integer, info={'unit': 'cm'})`

- **`comment`**
  - 列注释（数据库注释）
  - 示例：`Column(Integer, comment="用户身高")`

#### 高级选项
- **`quote`**
  - 是否强制引用列名（处理保留字）
  - 示例：`Column('select', String, quote=True)`

- **`system`**
  - 是否为系统列（通常用于 PostgreSQL 系统列）
  - 示例：`Column('ctid', String, system=True)`

- **`insert_sentinel`**
  - 用于插入操作的哨兵值（高级用法）

#### 内部参数
- **`_omit_from_statements`**
  - 是否从 SQL 语句中省略（内部使用）

- **`_proxies`**
  - 代理对象（内部使用）

- **`dialect_kwargs`**
  - 特定数据库方言的参数
  - 示例：`Column(String, mysql_charset='utf8mb4')`

## 完整示例

```python
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True,
        comment='用户唯一ID'
    )
    
    username = Column(
        String(50), 
        unique=True,
        nullable=False,
        index=True,
        doc='用户名，用于登录'
    )
    
    email = Column(
        String(255),
        name='email_address',  # 实际数据库列名
        key='email',           # ORM属性名
        nullable=False,
        unique=True,
        info={'validation': 'email'},
        comment='用户邮箱地址'
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        comment='创建时间'
    )
    
    updated_at = Column(
        DateTime,
        onupdate=datetime.utcnow,
        server_onupdate=func.now(),
        comment='最后更新时间'
    )
    
    status = Column(
        String(20),
        default='active',
        server_default="'active'",
        comment='用户状态'
    )
    
    # 外键关系
    group_id = Column(
        Integer,
        ForeignKey('groups.id', ondelete='SET NULL'),
        nullable=True
    )
    
    group = relationship('Group', back_populates='users')
```

## 使用技巧

### 1. 自动时间戳

```python
created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())
updated_at = Column(DateTime, onupdate=datetime.utcnow, server_onupdate=func.now())
```

### 2. 枚举类型

```python
from sqlalchemy import Enum

class Status(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

status = Column(Enum(Status), default=Status.ACTIVE, nullable=False)
```

### 3. 自引用外键

```python
manager_id = Column(Integer, ForeignKey('employees.id'))
manager = relationship('Employee', remote_side=[id], backref='subordinates')
```

### 4. 复合主键

```python
__table_args__ = (
    PrimaryKeyConstraint('user_id', 'role_id'),
)

user_id = Column(Integer, ForeignKey('users.id'))
role_id = Column(Integer, ForeignKey('roles.id'))
```

### 5. 数据库特定选项

```python
# PostgreSQL JSONB
data = Column(JSONB)

# MySQL 字符集
name = Column(String(100), info={'mysql_charset': 'utf8mb4'})

# SQLite 自增
id = Column(Integer, primary_key=True, autoincrement=True, sqlite_autoincrement=True)
```

## 最佳实践

1. **明确指定列名**：避免依赖默认行为
   ```python
   # 推荐
   id = Column('id', Integer, primary_key=True)
   
   # 不推荐
   id = Column(Integer, primary_key=True)
   ```

2. **使用注释**：提高可维护性
   ```python
   age = Column(Integer, comment="用户年龄，单位：岁")
   ```

3. **合理使用默认值**
   - 使用 `default` 处理应用层逻辑
   - 使用 `server_default` 处理数据库层逻辑

4. **索引策略**
   - 为主键和外键自动创建索引
   - 为查询频繁的列创建索引
   - 避免为低基数列创建索引

5. **外键约束**
   ```python
   group_id = Column(
       Integer, 
       ForeignKey(
           'groups.id', 
           ondelete='CASCADE', 
           onupdate='CASCADE'
       ),
       nullable=False
   )
   ```

6. **使用 ORM 关系**
   ```python
   posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')
   ```

7. **版本控制**
   ```python
   version_id = Column(Integer, default=0)
   __mapper_args__ = {'version_id_col': version_id}
   ```

## 常见问题

### 1. 自增主键设置

```python
# 正确方式
id = Column(Integer, primary_key=True, autoincrement=True)

# 错误方式（SQLAlchemy 会自动处理）
id = Column(Integer, primary_key=True, autoincrement=True, default=next_id)
```

### 2. 时间戳处理

```python
# 推荐使用 UTC 时间
created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

# 避免使用本地时间（会有时区问题）
created_at = Column(DateTime, default=datetime.now)
```

### 3. 大文本处理

```python
# 小文本
title = Column(String(255))

# 大文本
content = Column(Text)
```

### 4. 布尔值处理

```python
# 标准布尔列
is_active = Column(Boolean, default=True)

# 避免使用整数表示布尔值
# 不推荐：is_active = Column(Integer, default=1)
```

### 5. 关系加载策略

```python
# 延迟加载（默认）
posts = relationship('Post')

# 立即加载
posts = relationship('Post', lazy='joined')

# 动态加载（返回查询对象）
posts = relationship('Post', lazy='dynamic')
```

SQLAlchemy 的 `Column` 类提供了丰富的选项来定义数据库表结构。通过合理使用这些参数，可以创建高效、可维护的数据库模型，同时充分利用 SQLAlchemy ORM 的强大功能。