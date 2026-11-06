---
title: "CREATE MATERIALIZED VIEW"
description: "定义新的物化视图。"
weight: 670
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-materialized-view.md"
---

## 概要 {#synopsis}

```sql
CREATE MATERIALIZED VIEW [ IF  NOT EXISTS ] <table_name>
    [ (<column_name> [, ...] ) ]
    [ USING <method> ]
    [ WITH ( <storage_parameter> [= <value>] [, ... ] ) ]
    [ TABLESPACE <tablespace_name> ]
    AS <query>
    [ WITH [ NO ] DATA ]
    [DISTRIBUTED { BY ( <column> [<opclass>] [, ... ] ) | RANDOMLY | REPLICATED }]
```

## 描述 {#description}

`CREATE MATERIALIZED VIEW` 定义查询的物化视图。发出命令时会执行查询并用结果填充视图（除非使用 `WITH NO DATA`），之后可以通过 [REFRESH MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/refresh-materialized-view/) 刷新。

`CREATE MATERIALIZED VIEW` 类似于 `CREATE TABLE AS`，但还会记住所用的初始化查询，以便随后按需刷新。使用 `REFRESH MATERIALIZED VIEW` 命令可刷新物化视图数据。物化视图具有许多与表相同的属性，但不支持临时物化视图。

## 参数 {#parameters}

**`IF NOT EXISTS`**

如果同名物化视图已经存在，不报错，而是发出一条提示。注意，无法保证现有物化视图与原本要创建的物化视图有任何相似之处。

**`table_name`**

要创建的物化视图名称（可带模式限定）。

**`column_name`**

新物化视图中的列名称。列名按位置分配：第一个列名分配给查询结果的第一列，依此类推。如果未提供列名，则使用查询的输出列名。

**`USING method`**

此可选子句指定存储新物化视图内容所用的表访问方法；该方法必须是 `TABLE` 类型的访问方法。如果未指定，则为新物化视图选择默认表访问方法。更多信息见 default_table_access_method。

**`WITH ( storage_parameter [= value] [, ... ] )`**

此子句指定物化视图的可选存储参数。`CREATE TABLE` 支持的所有参数也都适用于 `CREATE MATERIALIZED VIEW`。更多信息见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

**`TABLESPACE tablespace_name`**

tablespace_name 是将要在其中创建新物化视图的表空间名称。如果未指定，则使用服务器配置参数 default_tablespace 的设置。

**`query`**

一个 [SELECT](/cloudberry/reference/sql-stmts/select/)、[TABLE](/cloudberry/reference/sql-stmts/select/#the-table-command) 或 [VALUES](/cloudberry/reference/sql-stmts/values/) 命令。该查询在安全受限操作中执行；特别是，调用自身会创建临时表的函数将失败。

**`WITH [ NO ] DATA`**

此子句指定创建物化视图时是否填充数据。默认值 `WITH DATA` 表示填充物化视图。使用 `WITH NO DATA` 时，不填充数据，将物化视图标记为不可扫描；在通过 `REFRESH MATERIALIZED VIEW` 填充之前，不能查询它。

**`[DISTRIBUTED { BY ( <column> [<opclass>] [, ... ] )`**<br />
**`DISTRIBUTED RANDOMLY`**<br />
**`DISTRIBUTED REPLICATED`**

用于声明物化视图数据的 Apache Cloudberry 分布策略。关于表分布策略，见 [CREATE TABLE](/cloudberry/reference/sql-stmts/create-table/)。

## 注意事项 {#notes}

物化视图是只读的。系统不允许对物化视图执行 `INSERT`、`UPDATE` 或 `DELETE`。使用 `REFRESH MATERIALIZED VIEW` 更新物化视图数据。

要在生成数据时排序，必须在物化视图查询中使用 `ORDER BY` 子句。不过，即使物化视图查询包含 `ORDER BY` 或 `SORT` 子句，对物化视图执行 `SELECT` 时也不保证数据有序。

## 示例 {#examples}

创建包含所有喜剧电影的视图：

```sql
CREATE MATERIALIZED VIEW comedies AS SELECT * FROM films 
WHERE kind = 'comedy';
```

这会创建一个视图，包含创建视图时 `film` 表中的所有列。虽然创建物化视图时使用了 `*`，但之后添加到表中的列不会成为视图的一部分。

创建获取排名前十的婴儿姓名的视图：

```sql
CREATE MATERIALIZED VIEW topten AS SELECT name, rank, gender, year FROM 
names, rank WHERE rank < '11' AND names.id=rank.id;
```

## 兼容性 {#compatibility}

`CREATE MATERIALIZED VIEW` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[SELECT](/cloudberry/reference/sql-stmts/select/), [VALUES](/cloudberry/reference/sql-stmts/values/), [CREATE VIEW](/cloudberry/reference/sql-stmts/create-view/), [ALTER MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/alter-materialized-view/), [DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/), [REFRESH MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/refresh-materialized-view/)
