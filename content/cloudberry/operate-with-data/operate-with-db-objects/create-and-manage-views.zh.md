---
title: "在 Apache Cloudberry 中创建和管理视图"
linkTitle: "创建和管理视图"
description: "在 Apache Cloudberry 中，视图允许保存经常使用或复杂的查询，然后在 `SELECT` 语句中像访问表一样访问这些查询。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-views.md"
---

视图不会在磁盘上物化：访问视图时，查询会作为子查询运行。

有关视图的更多信息，请参见[视图存储概述](/cloudberry/operate-with-data/operate-with-db-objects/view-storage/)和[使用视图依赖](/cloudberry/operate-with-data/operate-with-db-objects/work-with-view-dependencies/)。

## 创建视图 {#create-views}

`CREATE VIEW` 命令定义查询的视图。例如：

```sql
CREATE VIEW comedies AS SELECT * FROM films WHERE kind = 'comedy';
```

<!-- Views ignore `ORDER BY` and `SORT` operations stored in the view. -->

## 删除视图 {#drop-views}

`DROP VIEW` 命令删除视图。例如：

```sql
DROP VIEW topten;
```

`DROP VIEW...CASCADE` 命令还会删除所有依赖对象。例如，如果另一个视图依赖于即将删除的视图，则另一个视图也会被删除。如果没有 `CASCADE` 选项，`DROP VIEW` 命令会失败。

## 创建视图的最佳实践 {#best-practices-when-creating-views}

定义和使用视图时，请记住，视图只是一个 SQL 语句，查询运行时会用视图的定义替换视图。

下面是视图的一些常见用途：

- 可以将反复使用的 SQL 查询或表达式集中在一个位置，方便复用。
- 可以将视图用作抽象实际表定义的接口，从而可以重新组织表，而不必修改接口。

如果某个子查询仅与单个查询关联，可以考虑使用 `SELECT` 命令的 `WITH` 子句，而不是创建很少使用的视图。

一般来说，这些用途不需要嵌套视图，也就是不需要基于其他视图定义视图。

以下两种创建视图的模式往往会带来问题，因为视图的 SQL 会在查询执行期间使用。

- 定义多层视图，使最终查询看似简单。

    当尝试增强或排查使用这些视图的查询时，就会出现问题，例如检查执行计划时。查询的执行计划往往很复杂，难以理解和改进。

- 定义反规范化的“世界”视图。该视图连接大量数据库表，供各种查询使用。

    对于某些使用该视图的查询，其 `WHERE` 条件可能导致性能问题，而其他 `WHERE` 条件则运行良好。
