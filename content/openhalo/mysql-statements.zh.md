---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16；2026-11-07 文档快照"
upstream_notice: /zh/attribution/#halodb
title: 兼容的 MySQL 语句
linkTitle: MySQL 语句
description: Halo 文档列出的插入、分页、预处理语句和用户变量等 MySQL 语法。
weight: 40
---

Halo 1.0.16 官方 SQL 语法页面列出了以下 MySQL 特有形式。示例反映文档描述的兼容面；应用中的实际语句仍应在确切的服务端版本上验证。

## `REPLACE` 与冲突处理 {#replace-and-conflict-handling}

`REPLACE INTO` 遇到相同主键或唯一键时，会先删除原行再插入新行。`INSERT IGNORE` 跳过主键或唯一键冲突的行。`ON DUPLICATE KEY UPDATE` 在键冲突时更新已有行。

```sql
CREATE TABLE test (
  id INT PRIMARY KEY,
  name VARCHAR(50),
  UNIQUE (name)
);

INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob');
REPLACE INTO test VALUES (1, 'Charlie');
INSERT IGNORE INTO test VALUES (1, 'Duplicate'), (3, 'David');
INSERT INTO test VALUES (1, 'Alice')
  ON DUPLICATE KEY UPDATE name = 'Alice updated';
```

`REPLACE` 的语义是先删除再插入。用它实现 upsert 前，请检查触发器、生成值、外键和审计逻辑的行为。

## `INSERT ... SET` {#insert-set}

文档列出的 MySQL 写法使用 `SET` 列表代替 `VALUES`：

```sql
CREATE TABLE tab1 (
  id INT,
  name1 VARCHAR(128),
  name2 VARCHAR(128),
  UNIQUE (name1)
);

INSERT INTO tab1 SET name1 = 'n1', id = 1, name2 = 'n2';
```

## `LIMIT` 分页 {#limit}

Halo 文档说明支持 `LIMIT N`、`LIMIT N,M` 和 `LIMIT N OFFSET M`：

```sql
SELECT * FROM events ORDER BY created_at DESC LIMIT 10;
SELECT * FROM events ORDER BY created_at DESC LIMIT 20, 10;
SELECT * FROM events ORDER BY created_at DESC LIMIT 10 OFFSET 20;
```

需要稳定分页时，请显式指定 `ORDER BY`。

## 预处理语句 {#prepared-statements}

SQL 级 MySQL 写法是 `PREPARE`、`EXECUTE` 和 `DEALLOCATE PREPARE`：

```sql
PREPARE stmt1 FROM 'SELECT ? + ?';
SET @a = 1, @b = 2;
EXECUTE stmt1 USING @a, @b;
DEALLOCATE PREPARE stmt1;
```

应用驱动也可能使用 MySQL 二进制协议。请通过应用实际使用的驱动测试参数类型、生成计划和连接池行为。

## 用户变量 {#user-variables}

MySQL 风格的用户变量使用 `@name` 形式，并在同一会话中保留：

```sql
SET @myvar = 100;
SELECT @myvar;

SET @name = 'John';
SELECT * FROM users WHERE username = @name;
```

处理不可信输入时，不要用会话变量代替绑定参数。

## 历史冒烟测试结果 {#historical-tests}

一份独立报告使用 MySQL 5.7.32 客户端测试了 OpenHalo `1.0.14.18`，记录了基础 CRUD、连接、视图、事务、普通索引、常见字符串函数、约束、派生表、相关子查询和 `EXISTS` 等成功案例。这些结果是历史冒烟测试，不能保证 Halo Database 1.0.16 或所有 OpenHalo 构建都支持相同功能。报告来源和限制见[已知兼容边界](/openhalo/mysql-compatibility-gaps/)。

## 资料来源 {#sources}

本页为 [Halo Database MySQL 兼容参考](https://doc.halodbtech.com/multi-mode-compatibility/mysql/sql-syntax)的原创摘要。上游未明确公开文档许可证；版本、版权与引用方式见[来源说明](/attribution/#halodb)。
