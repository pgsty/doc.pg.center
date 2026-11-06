---
title: "REFRESH MATERIALIZED VIEW"
description: "替换物化视图的内容。"
weight: 1580
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/refresh-materialized-view.md"
---

## 概要 {#synopsis}

```sql
REFRESH MATERIALIZED VIEW [ CONCURRENTLY ] <name>
    [ WITH [ NO ] DATA ]
```

## 描述 {#description}

`REFRESH MATERIALIZED VIEW` 完全替换物化视图的内容，丢弃旧内容。必须是物化视图所有者才能运行此命令。如果指定 `WITH DATA`（或采用默认值），会执行其底层查询以生成新数据，并使物化视图处于可扫描状态。如果指定 `WITH NO DATA`，则不生成新数据，物化视图处于不可扫描状态。

不能同时指定 `CONCURRENTLY` 和 `WITH NO DATA`。

## 参数 {#parameters}

**`CONCURRENTLY`**

刷新物化视图时，不阻止对它的并发查询。不使用此选项时，影响大量行的刷新通常会消耗更少资源、完成得更快，但可能阻塞尝试读取物化视图的其他连接。如果只影响少量行，使用此选项可能更快。

只有在物化视图上至少存在一个仅使用列名且包含所有行的 `UNIQUE` 索引时，才允许使用此选项；也就是说，该索引不能基于表达式，也不能包含 `WHERE` 子句。

物化视图尚未填充数据时，不能使用此选项。

即使使用此选项，对任一物化视图也只能同时运行一个 `REFRESH`。

**`name`**

要刷新的物化视图名称（可带模式限定）。

**`WITH [ NO ] DATA`**

`WITH DATA` 是默认值，表示执行物化视图查询以生成新数据，并使物化视图处于可扫描状态。如果指定 `WITH NO DATA`，则不生成新数据，物化视图处于不可扫描状态。

## 注意事项 {#notes}

如果物化视图的定义查询中包含 `ORDER BY` 子句，初始内容会按该方式排序；但 `REFRESH MATERIALIZED VIEW` 不保证保留此顺序。

## 示例 {#examples}

此命令使用物化视图定义中的查询替换 `order_summary` 的内容，并使其处于可扫描状态。

```sql
REFRESH MATERIALIZED VIEW order_summary;
```

此命令释放与物化视图 `annual_statistics_basis` 关联的存储空间，并使其处于不可扫描状态。

```sql
REFRESH MATERIALIZED VIEW annual_statistics_basis WITH NO DATA;
```

## 兼容性 {#compatibility}

`REFRESH MATERIALIZED VIEW` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另见 {#see-also}

[ALTER MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/alter-materialized-view/), [CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/), [DROP MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/drop-materialized-view/)
