---
title: "在 Apache Cloudberry 中创建和管理物化视图"
linkTitle: "创建和管理物化视图"
description: "在 Apache Cloudberry 中，物化视图与视图相似。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-materialized-views.md"
---

物化视图允许保存经常使用或复杂的查询，然后在 `SELECT` 语句中像访问表一样访问查询结果。物化视图以类似表的形式持久保存查询结果。

虽然访问物化视图中存储的数据可能比直接访问底层表或通过普通视图访问快得多，但这些数据并不总是最新的。物化视图数据不能直接更新。要刷新物化视图数据，请使用 `REFRESH MATERIALIZED VIEW` 命令。

用于创建物化视图的查询，其存储方式与视图查询完全相同。例如，如果可以接受当天的数据不完整，就可以创建一个快速显示历史销售数据汇总的物化视图。

```sql
CREATE MATERIALIZED VIEW sales_summary AS
  SELECT seller_no, invoice_date, sum(invoice_amt)::numeric(13,2) as sales_amt
    FROM invoice
    WHERE invoice_date < CURRENT_DATE
    GROUP BY seller_no, invoice_date

CREATE UNIQUE INDEX sales_summary_seller
  ON sales_summary (seller_no, invoice_date);
```

该物化视图可以用于在为销售人员创建的仪表板中显示图表。可以调度一个作业，每晚使用以下命令更新汇总信息：

```sql
REFRESH MATERIALIZED VIEW sales_summary;
```

Apache Cloudberry 系统目录中的物化视图信息，与表或视图的信息完全相同。物化视图与表或视图一样，都是关系。在查询中引用物化视图时，会像访问表一样直接从物化视图返回数据。物化视图定义中的查询仅用于填充物化视图。

如果可以接受定期更新物化视图数据，就可以从中获得很大的性能收益。

物化视图的一种用途是加快访问通过外部表或外部数据包装器等外部数据源引入的数据。此外，可以在物化视图上定义索引，而外部数据包装器不支持索引；这一优势可能不适用于其他类型的外部数据访问。

如果某个子查询仅与单个查询关联，可以考虑使用 `SELECT` 命令的 `WITH` 子句，而不是创建很少使用的物化视图。

## 创建物化视图 {#create-materialized-views}

`CREATE MATERIALIZED VIEW` 命令根据查询定义物化视图。

```sql
CREATE MATERIALIZED VIEW us_users AS SELECT u.id, u.name, a.zone FROM users u, address a WHERE a.country = 'USA';
```

> [!TIP]
> 使用 `ORDER BY` 或 `SORT` 子句创建物化视图时，只会在初次创建视图时应用排序。后续刷新物化视图时不会维持此顺序，因为物化视图本质上是数据的静态快照，不会在插入新数据时动态更新或保留排序。

## 刷新或停用物化视图 {#refresh-or-deactivate-materialized-views}

`REFRESH MATERIALIZED VIEW` 命令更新物化视图数据。

```sql
REFRESH MATERIALIZED VIEW us_users;
```

使用 `WITH NO DATA` 子句时，会删除当前数据，不生成新数据，并使物化视图处于不可扫描状态。如果查询尝试访问不可扫描的物化视图，就会返回错误。

```sql
REFRESH MATERIALIZED VIEW us_users WITH NO DATA;
```

## 删除物化视图 {#drop-materialized-views}

`DROP MATERIALIZED VIEW` 命令删除物化视图的定义和数据。例如：

```sql
DROP MATERIALIZED VIEW us_users;
```

`DROP MATERIALIZED VIEW ... CASCADE` 命令还会删除所有依赖对象。例如，如果另一个物化视图依赖于即将删除的物化视图，则另一个物化视图也会被删除。如果没有 `CASCADE` 选项，`DROP MATERIALIZED VIEW` 命令会失败。
