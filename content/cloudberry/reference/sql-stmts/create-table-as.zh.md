---
title: "CREATE TABLE AS"
description: "根据查询结果定义新表。"
weight: 820
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-table-as.md"
---

## 概要 {#synopsis}

```sql
CREATE [ [ GLOBAL | LOCAL ] { TEMPORARY | TEMP } | UNLOGGED ] TABLE [ IF NOT EXISTS ] <table_name>
        [ (<column_name> [, ...] ) ]
        [ USING <access_method> ]
        [ WITH ( <storage_parameter> [= <value>] [, ... ] ) | WITHOUT OIDS ]
        [ ON COMMIT { PRESERVE ROWS | DELETE ROWS | DROP } ]
        [ TABLESPACE <tablespace_name> ]
        AS <query>
        [ WITH [ NO ] DATA ]
        [ DISTRIBUTED BY ( <column> [<opclass>] [, ... ] ) 
           | DISTRIBUTED RANDOMLY
           | DISTRIBUTED REPLICATED ]
```

## 描述 {#description}

`CREATE TABLE AS` 创建表，并用 [SELECT](/cloudberry/reference/sql-stmts/select/) 命令计算的数据填充它。表列具有与 `SELECT` 输出列对应的名称和数据类型，但可以显式提供新的列名列表来覆盖列名。

`CREATE TABLE AS` 创建新表，仅执行一次查询来初始填充新表。新表不会跟踪查询源表的后续变化。

## 参数 {#parameters}

**`GLOBAL | LOCAL`**

为兼容性而接受，但会被忽略。这些关键字已弃用；详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`TEMPORARY | TEMP`**

如果指定，将新表创建为临时表。详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`UNLOGGED`**

如果指定，将表创建为不记录 WAL 的表。详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`IF NOT EXISTS`**

如果同名关系已经存在，不报错；只发出一条提示，不修改现有表。

**`table_name`**

要创建的新表名称（可带模式限定）。

**`column_name`**

新表中的列名称。如果未提供列名，则使用查询的输出列名。

**`USING access_method`**

可选的 `USING` 子句指定存储新表内容所用的表访问方法；该方法必须是 [TABLE](/cloudberry/reference/sql-stmts/select/#the-table-command) 类型的访问方法。设为 `heap` 时按堆存储表访问，设为 `ao_row` 时按行存 AO 表访问，设为 `ao_column` 时按列存 AO 表（AO/CO）访问。默认访问方法由服务器配置参数 default_table_access_method 的值决定。

> **注意：**
>
> 虽然可以使用 `WITH (appendoptimized=true|false, orientation=row|column)` 指定表访问方法，但建议改用 `USING <access_method>`。

**`WITH ( storage_parameter=value )`**

`WITH` 子句指定新表的可选存储参数。更多信息见 `CREATE TABLE` 参考页中的[存储参数](/cloudberry/reference/sql-stmts/create-table/#storage-parameters)一节。

**`ON COMMIT`**

可以使用 `ON COMMIT` 控制临时表在事务块结束时的行为。有三个选项：

PRESERVE ROWS —— 事务结束时，Apache Cloudberry 不对临时表执行特殊操作。这是默认行为。

DELETE ROWS —— 每个事务块结束时，Apache Cloudberry 删除临时表中的所有行。实质上，相当于每次提交时自动执行 [TRUNCATE](/cloudberry/reference/sql-stmts/truncate/)。

DROP —— 当前事务块结束时，Apache Cloudberry 删除临时表。

**`TABLESPACE tablespace_name`**

tablespace_name 参数是将要在其中创建新表的表空间名称。如果未指定，则使用数据库的 `default_tablespace`；若为临时表，则使用 `temp_tablespaces`。

**`AS query`**

一个 [SELECT](/cloudberry/reference/sql-stmts/select/)、[TABLE](/cloudberry/reference/sql-stmts/select/#the-table-command) 或 [VALUES](/cloudberry/reference/sql-stmts/values/) 命令，或者执行预备 `SELECT`、`TABLE` 或 `VALUES` 查询的 [EXECUTE](/cloudberry/reference/sql-stmts/execute/) 命令。

**`DISTRIBUTED BY ( column [opclass] [, ... ] )`**<br />
**`DISTRIBUTED RANDOMLY`**<br />
**`DISTRIBUTED REPLICATED`**

用于声明表的 Apache Cloudberry 分布策略。详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

## 注意事项 {#notes}

此命令在功能上类似于 [SELECT INTO](/cloudberry/reference/sql-stmts/select-into/)，但更推荐使用，因为它不易与 `SELECT INTO` 语法的其他用法混淆。此外，`CREATE TABLE AS` 的功能涵盖并超出了 `SELECT INTO`。

`CREATE TABLE AS` 可用于从外部表数据源快速加载数据。见 [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/)。

## 示例 {#examples}

创建新表 `films_recent`，仅包含表 `films` 中的近期记录：

```sql
CREATE TABLE films_recent AS
  SELECT * FROM films WHERE date_prod >= '2020-01-01';
```

要完整复制表，也可以使用指定 `TABLE` 命令的简写形式：

```sql
CREATE TABLE films2 AS
  TABLE films;
```

使用预备语句创建新临时表 `films_recent`，仅包含表 `films` 中的近期记录。新表将在提交时删除：

```sql
PREPARE recentfilms(date) AS
  SELECT * FROM films WHERE date_prod > $1;
CREATE TEMP TABLE films_recent ON COMMIT DROP AS 
  EXECUTE recentfilms('2020-01-01');
```

## 兼容性 {#compatibility}

`CREATE TABLE AS` 符合 SQL 标准，但有以下例外：

- 标准要求子查询子句外带括号；在 Apache Cloudberry 中，这些括号是可选的。
- 标准要求必须写出 `WITH [NO] DATA` 子句；在 Apache Cloudberry 中，它是可选的。
- Apache Cloudberry 对临时表的处理与标准不同；详情见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。
- `WITH` 子句是 Apache Cloudberry 的扩展；存储参数不属于标准。
- Apache Cloudberry 的表空间概念不属于标准。`TABLESPACE` 子句是扩展。

## 另见 {#see-also}

[CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/), [CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/), [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/), [EXECUTE](/cloudberry/reference/sql-stmts/execute/), [SELECT](/cloudberry/reference/sql-stmts/select/), [SELECT INTO](/cloudberry/reference/sql-stmts/select-into/), [VALUES](/cloudberry/reference/sql-stmts/values/)
