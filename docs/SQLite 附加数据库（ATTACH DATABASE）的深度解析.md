# SQLite 附加数据库（ATTACH DATABASE）的深度解析

SQLite 的 **ATTACH DATABASE** 命令允许在同一个数据库连接中访问多个数据库文件，这是 SQLite 提供的一个强大而独特的功能。其主要目的是**在单个数据库连接中创建逻辑统一的数据视图**，使开发者能够像操作单个数据库一样操作多个物理分离的数据库文件。

## 核心目的与价值

### 1. 多数据库联合操作
```sql
-- 附加第二个数据库
ATTACH DATABASE 'customer_data.db' AS cust;

-- 跨数据库JOIN查询
SELECT orders.*, cust.customers.name 
FROM main.orders
JOIN cust.customers ON orders.customer_id = cust.customers.id;
```

### 2. 数据模块化与隔离
```sql
-- 附加配置数据库
ATTACH DATABASE 'config.db' AS cfg;

-- 附加用户数据库
ATTACH DATABASE 'users.db' AS usr;

-- 跨数据库查询
SELECT usr.users.username, cfg.settings.theme
FROM usr.users
JOIN cfg.settings ON usr.users.setting_id = cfg.settings.id;
```

### 3. 简化数据迁移
```sql
-- 附加旧版本数据库
ATTACH DATABASE 'old_data_v1.db' AS old;

-- 迁移数据到新结构
INSERT INTO main.customers(name, email)
SELECT old_name, old_email FROM old.legacy_customers;

-- 验证数据完整性
SELECT COUNT(*) FROM main.customers
UNION ALL
SELECT COUNT(*) FROM old.legacy_customers;
```

### 4. 临时数据处理
```sql
-- 创建内存数据库
ATTACH DATABASE ':memory:' AS temp;

-- 在内存中创建临时表
CREATE TABLE temp.intermediate_results AS
SELECT ... FROM main.data WHERE ...;

-- 使用临时数据
UPDATE main.records
SET status = 'processed'
WHERE id IN (SELECT id FROM temp.intermediate_results);
```

### 5. 分片与分区
```sql
-- 附加分片数据库
ATTACH DATABASE 'shard_2023.db' AS shard1;
ATTACH DATABASE 'shard_2024.db' AS shard2;

-- 跨分片联合查询
SELECT * FROM shard1.sales
UNION ALL
SELECT * FROM shard2.sales
WHERE sale_date > '2024-01-01';
```

## 技术实现细节

### 语法结构
```sql
ATTACH [DATABASE] 'filename' AS schema-name;
```

### 关键特性：
1. **统一命名空间**：使用 `schema.object` 格式访问不同数据库的对象
   ```sql
   SELECT * FROM main.employees;    -- 主数据库
   SELECT * FROM archive.employees; -- 附加的存档数据库
   ```

2. **跨数据库事务**：
   ```sql
   BEGIN;
   UPDATE main.accounts SET balance = balance - 100;
   UPDATE external.transfers SET status = 'completed';
   COMMIT; -- 原子提交到多个数据库文件
   ```

3. **临时附加**：附加的数据库仅在当前连接有效
4. **无限附加**：SQLite 没有硬性限制附加数据库数量（受系统资源限制）

### 附加顺序与优先级
```sql
-- 附加优先级示例
ATTACH 'db1.db' AS db1;
ATTACH 'db2.db' AS db2;

-- 对象查找顺序：
-- 1. temp (临时数据库)
-- 2. main (主数据库)
-- 3. 按附加顺序：db1 → db2
```

## 实际应用场景

### 场景1：多租户架构
```sql
-- 附加租户特定数据库
ATTACH DATABASE 'tenant_123_data.db' AS tenant;

-- 统一查询接口
SELECT * FROM tenant.orders 
WHERE user_id = @user_id;
```

### 场景2：版本化数据管理
```sql
-- 附加历史版本数据库
ATTACH 'v1_backup.db' AS v1;
ATTACH 'v2_backup.db' AS v2;

-- 数据差异比较
SELECT * FROM v1.products
EXCEPT
SELECT * FROM main.products;
```

### 场景3：模块化应用设计
```sql
-- 核心模块
ATTACH 'core.db' AS core;

-- 插件模块
ATTACH 'plugin_analytics.db' AS analytics;
ATTACH 'plugin_reporting.db' AS reports;

-- 跨模块查询
SELECT core.users.name, analytics.metrics.value
FROM core.users
JOIN analytics.metrics ON core.users.id = analytics.metrics.user_id;
```

### 场景4：数据沙盒测试
```sql
-- 附加生产数据库（只读）
ATTACH 'production.db' AS prod;

-- 创建测试沙盒
ATTACH ':memory:' AS sandbox;

-- 克隆生产结构
CREATE TABLE sandbox.orders AS SELECT * FROM prod.orders LIMIT 0;

-- 安全测试
INSERT INTO sandbox.orders (...) VALUES (...);
```

## 性能与限制

### 性能考虑：
1. **跨数据库JOIN**：可能比单库JOIN稍慢，但比应用层合并高效
2. **索引利用**：每个数据库的索引独立使用
3. **事务开销**：多数据库事务需要协调多个文件写入

### 主要限制：
1. **并发写入**：多个连接同时写入不同数据库时需谨慎处理
   ```python
   # Python中安全处理多数据库事务
   with db_connection:
       # 自动开始事务
       db_connection.execute("UPDATE main.table...")
       db_connection.execute("UPDATE aux.table...")
   # 事务自动提交
   ```

2. **跨数据库约束**：
   - 外键约束不能跨数据库
   - UNIQUE约束仅限当前数据库

3. **ATTACH权限**：需要文件系统读写权限

## 最佳实践

### 1. 命名约定
```sql
-- 使用有意义的schema名称
ATTACH 'customer_data.db' AS cust;  -- 良好
ATTACH 'data.db' AS db2;            -- 避免
```

### 2. 资源管理
```sql
-- 使用后及时分离
DETACH DATABASE temp_data;

-- 或让连接关闭时自动分离
```

### 3. 路径处理
```sql
-- 使用绝对路径避免歧义
ATTACH DATABASE '/var/db/aux_data.db' AS aux;

-- 特殊名称：
ATTACH ':memory:' AS mem;  -- 内存数据库
ATTACH '' AS temp;         -- 临时磁盘数据库
```

### 4. 错误处理
```python
# Python 示例
try:
    cursor.execute("ATTACH DATABASE 'data.db' AS aux")
except sqlite3.OperationalError as e:
    if "database is already attached" in str(e):
        print("数据库已附加")
    elif "unable to open database file" in str(e):
        print("文件不存在或权限不足")
```

## 与替代方案的比较

| 特性 | 附加数据库 | 多个连接 | 数据合并 |
|------|------------|----------|----------|
| **事务一致性** | 支持原子操作 | 不支持 | 不支持 |
| **查询复杂度** | 单SQL跨库 | 需多查询 | 单查询 |
| **性能** | 中等 | 高（并行） | 低 |
| **内存占用** | 低 | 高 | 高 |
| **开发复杂度** | 低 | 高 | 中等 |

## 总结：何时使用附加数据库？

在以下场景优先考虑 ATTACH DATABASE：
1. 需要跨多个数据库执行复杂SQL查询
2. 逻辑相关但物理分离的数据需要统一视图
3. 临时数据处理需要与持久数据交互
4. 分阶段数据迁移或版本比较
5. 模块化应用架构中各组件有独立数据库

> **关键洞察**：SQLite 的附加数据库功能不是简单的文件链接，而是创建了一个虚拟的统一数据空间，使开发者能够以关系型思维操作分布式数据存储，同时保持SQLite的轻量级特性。