---
title: SQL 支持与变通方法
description: 介绍在 Citus 分布式表上使用 PostgreSQL 功能时，常见限制和边界情况的变通方法。
weight: 110
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/reference-workarounds?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

Citus 通过扩展 PostgreSQL 提供分布式功能，因此兼容 PostgreSQL 的语法结构。这意味着，对于通过 Citus 创建的分布式表，用户也可以使用 PostgreSQL 丰富且可扩展的生态系统中的工具和功能。

对于能够在单个工作节点上执行的查询，Citus 支持全部 SQL 功能。在 `mt_use_case` 中访问单个租户的信息时，这类查询很常见。

即使是用于并行计算的跨节点查询，也支持大多数 SQL 功能。不过，对于需要合并多个节点信息的查询，仍有一些 SQL 功能不受支持。

## 限制 {#limitations}

以下各节介绍在 Citus 分布式表上使用 PostgreSQL 功能时的常见限制。

### 一般限制 {#general}

以下限制适用于所有运行模式。

- 不支持[规则系统](https://www.postgresql.org/docs/current/rules.html)。
- 不支持在 INSERT 查询中放置子查询的变通方法。
- 不支持将多级分区表转换为分布式表。
- 分布式表的 UPDATE 查询中使用的函数不得为 VOLATILE。
- UPDATE 查询中使用的 STABLE 函数不能以列引用作为参数调用。
- 查询包含 Citus 表时，不支持修改视图。

Citus 在每个节点生成的序列值中编码节点标识符，使各节点都能直接接受插入，而不会产生重复的序列值。不过，这种方式不适用于小于 BIGINT 的序列类型，可能导致工作节点上的插入失败。此时需要删除原列并添加一个基于 BIGINT 的列，或通过协调节点路由插入操作。

### 跨节点 SQL 查询 {#cross-node-sql-queries}

- [SELECT ... FOR UPDATE](https://www.postgresql.org/docs/current/static/sql-select.html#SQL-FOR-UPDATE-SHARE) 仅适用于单分片查询。
- [TABLESAMPLE](https://www.postgresql.org/docs/current/static/sql-select.html#SQL-FROM) 仅适用于单分片查询。
- 仅当关联条件基于 `dist_column` 时，才支持关联子查询。
- 分布式表之间的外连接仅支持基于 `dist_column` 的连接。
- [递归公共表表达式（CTE）](https://www.postgresql.org/docs/current/static/queries-with.html#idm46428713247840) 仅适用于单分片查询。
- [分组集](https://www.postgresql.org/docs/current/static/queries-table-expressions.html#QUERIES-GROUPING-SETS)仅适用于单分片查询。
- 只有普通表、外表或分区表可以转换为分布式表。
- SQL [MERGE 命令](https://www.postgresql.org/docs/current/sql-merge.html)对各种 [表类型](/citus/overview/what-is-citus/#table-types) 组合的支持情况如下：

  | 目标 | 来源 | 是否支持 | 说明 |
  | --- | --- | --- | --- |
  | 本地表 | 本地表 | 是 |  |
  | 本地表 | 参考表 | 是 |  |
  | 本地表 | 分布式表 | 否 | 功能开发中。 |
  | 分布式表 | 本地表 | 是 |  |
  | 分布式表 | 分布式表 | 是 | 包括非共置表。 |
  | 分布式表 | 参考表 | 是 |  |
  | 参考表 | 不适用 | 否 | 不允许将参考表作为目标。 |

有关 PostgreSQL 及其功能的更多信息，请参阅 [PostgreSQL 文档](http://www.postgresql.org/docs/current/static/index.html)。有关 PostgreSQL SQL 命令方言的详细参考，请参阅 [SQL 命令参考](http://www.postgresql.org/docs/current/static/sql-commands.html)，Citus 用户可以直接使用这些命令。

### 基于模式的分片的 SQL 兼容性 {#schema-based-sharding-sql-compatibility}

使用 `schema_based_sharding` 时，以下功能不可用：

- 不支持跨分布式模式的外键。
- 跨分布式模式的连接受 `cross_node_sql_limits` 限制。
- 不支持在一条 SQL 语句中创建分布式模式及其表。

## 变通方法 {#workarounds}

尝试变通方法之前，请先考虑 Citus 是否适合你的场景。当前版本的 Citus 适合实时分析和多租户场景（[实时分析和多租户使用场景](/citus/overview/use-cases/)）。

Citus 在多租户场景中支持所有 SQL 语句。即使在查询跨越多个节点的实时分析场景中，Citus 也支持大多数语句。少数不受支持的查询类型列于 `unsupported`。其中许多功能都有变通方法，以下介绍一些最实用的方法。

### 使用 CTE 绕过限制 {#work-around-limitations-using-ctes}

如果某条 SQL 查询不受支持，可以尝试使用 CTE，通过所谓的“拉取—推送执行”来绕过限制。

```sql
SELECT * FROM dist WHERE EXISTS (SELECT 1 FROM local WHERE local.a = dist.a);
/*
ERROR:  direct joins between distributed and local tables are not supported
HINT:  Use CTE's or subqueries to select from local tables and use them in joins
*/
```

可以将查询中的分布式部分包装在 CTE 中，将其转为路由查询，从而绕过此限制：

```sql
WITH cte AS (SELECT * FROM dist)
SELECT * FROM cte WHERE EXISTS (SELECT 1 FROM local WHERE local.a = cte.a);
```

请记住，协调节点会将 CTE 的结果发送给所有需要这些结果来执行查询的工作节点。因此，最好尽可能在内部查询中添加精确的过滤条件和行数限制，或者先对表进行聚合，以减少这类查询带来的网络开销。

### 临时表：最后的变通手段 {#temp-tables-the-workaround-of-last-resort}

即使通过子查询使用推送—拉取执行，仍有少数查询不受支持，例如在分布式表上使用[分组集](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUPING-SETS)。

在实时分析教程中，我们创建了一个名为 `github_events` 的表，并按 `user_id` 列分布数据。现在要查询预先选定的一组仓库中最早的事件，按事件类型和事件是否公开的组合分组。使用分组集可以方便地完成这项查询，但如前所述，分布式查询尚不支持这一功能：

```sql
-- this won't work

  SELECT repo_id, event_type, event_public,
         grouping(event_type, event_public),
         min(created_at)
    FROM github_events
   WHERE repo_id IN (8514, 15435, 19438, 21692)
GROUP BY repo_id, ROLLUP(event_type, event_public);
```

```text
    ERROR: could not run distributed query with GROUPING
    HINT: Consider using an equality filter on the distributed table's partition column.
```

不过，可以用一个技巧：将相关信息拉取到协调节点上的临时表中。

```sql
-- grab the data, minus the aggregate, into a local table

CREATE TEMP TABLE results AS (
  SELECT repo_id, event_type, event_public, created_at
    FROM github_events
       WHERE repo_id IN (8514, 15435, 19438, 21692)
    );

-- now run the aggregate locally

  SELECT repo_id, event_type, event_public,
         grouping(event_type, event_public),
         min(created_at)
    FROM results
GROUP BY repo_id, ROLLUP(event_type, event_public);
```

```text
repo_id |    event_type     | event_public | grouping |         min
--------+-------------------+--------------+----------+---------------------
   8514 | PullRequestEvent  | t            |        0 | 2016-12-01 05:32:54
   8514 | IssueCommentEvent | t            |        0 | 2016-12-01 05:32:57
  19438 | IssueCommentEvent | t            |        0 | 2016-12-01 05:48:56
  21692 | WatchEvent        | t            |        0 | 2016-12-01 06:01:23
  15435 | WatchEvent        | t            |        0 | 2016-12-01 05:40:24
  21692 | WatchEvent        |              |        1 | 2016-12-01 06:01:23
  15435 | WatchEvent        |              |        1 | 2016-12-01 05:40:24
   8514 | PullRequestEvent  |              |        1 | 2016-12-01 05:32:54
   8514 | IssueCommentEvent |              |        1 | 2016-12-01 05:32:57
  19438 | IssueCommentEvent |              |        1 | 2016-12-01 05:48:56
  15435 |                   |              |        3 | 2016-12-01 05:40:24
  21692 |                   |              |        3 | 2016-12-01 06:01:23
  19438 |                   |              |        3 | 2016-12-01 05:48:56
   8514 |                   |              |        3 | 2016-12-01 05:32:54
```

在协调节点上创建临时表是最后的手段，受该节点磁盘容量和 CPU 的限制。

### INSERT 查询中的子查询 {#subqueries-within-insert-queries}

尝试使用“INSERT INTO ... SELECT”语法重写查询。

以下 SQL：

```sql
INSERT INTO a.widgets (map_id, widget_name)
VALUES (
    (SELECT mt.map_id FROM a.map_tags mt WHERE mt.map_license = '12345'),
    'Test'
);
```

可以改写为：

```sql
INSERT INTO a.widgets (map_id, widget_name)
SELECT mt.map_id, 'Test'
  FROM a.map_tags mt
 WHERE mt.map_license = '12345';
```

## 相关内容 {#related-content}

- [Citus SQL 参考概述](/citus/reference/)
- [什么是 Azure Cosmos DB for PostgreSQL？](/citus/overview/what-is-citus/)
