---
title: 图如何存储
linkTitle: 图如何存储
description: AgensGraph 没有把图引擎外挂在 PostgreSQL 上。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/graph-on-postgresql.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 没有把图引擎外挂在 PostgreSQL 上。它使用 PostgreSQL 已有的模式、表、索引和继承，把图*作为* PostgreSQL 对象存储。理解这层映射后，你掌握的大部分 PostgreSQL 运维知识都可以直接沿用。这也不再令人意外：一条语句可以混用 Cypher 与 SQL，因为始终只有一组表。

这层映射只有三句话。

**图是模式。** `CREATE GRAPH moviekb` 创建名为 `moviekb` 的模式。

**标签是表。** `CREATE VLABEL movie` 创建表 `moviekb.movie`。

**顶点或边是那张表中的一行。**

## 标签表长什么样 {#what-a-label-table-looks-like}

顶点标签有两列：

```psql
\d moviekb.movie
```

```
                                              Table "moviekb.movie"
   Column   |  Type   | Nullable |                                   Default
------------+---------+----------+-------------------------------------------------------------------------
 id         | graphid | not null | graphid(graph_labid('moviekb.movie'::cstring), nextval('moviekb.movie_id_seq'))
 properties | jsonb   | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
Inherits: moviekb.ag_vertex
```

边标签有同样的两列，再加上两个端点的 id：

```psql
\d moviekb.acted_in
```

```
                                              Table "moviekb.acted_in"
   Column   |  Type   | Nullable |                                     Default
------------+---------+----------+---------------------------------------------------------------------------
 id         | graphid | not null | graphid(graph_labid('moviekb.acted_in'::cstring), nextval('moviekb.acted_in_id_seq'))
 start      | graphid | not null |
 end        | graphid | not null |
 properties | jsonb   | not null | jsonb_build_object()
Indexes:
    "acted_in_end_idx" btree ("end", start)
    "acted_in_id_idx" brin (id)
    "acted_in_start_idx" btree (start, "end")
Inherits: moviekb.ag_edge
```

标签可以携带比这些更多的列。[提升属性](/zh/agensgraph/querying/typed-columns/)会在属性包旁边添加真正的类型列，并在写入时填充。此后，热属性会存储两次：一次作为 jsonb 键，一次作为规划器可以原生索引和比较的列。目录 `ag_label_property` 记录哪个属性键由哪一列响应。Cypher 仍按键名访问，因此列名永远不会出现在查询中。

所以，边是一行记录两个顶点的数据，遍历边就是按 `graphid` 连接。`(start, "end")` 与 `("end", start)` 上的两个 btree 索引让这个连接在两个方向都很快；创建标签时，AgensGraph 会自动创建它们。`id` 上的 BRIN 索引很小，有助于按标签 id 做范围扫描。

注意每种标签会得到哪些索引。顶点标签在 `id` 上有主键；边标签没有，因为边通过端点访问，而不是通过 id 访问。

因为 `properties` 是单个 `jsonb` 列，标签不会对行强加列清单。两个 `movie` 顶点可以携带完全不同的键。这就是这里“无模式属性”的含义。这也是读取属性必须读入 JSON 文档的原因。[把属性提升为列](/zh/agensgraph/querying/typed-columns/)介绍了这种成本何时重要以及应对方法。

## 身份：graphid {#identity-the-graphid}

`graphid` 是 64 位标识符，包含两部分。高 16 位是*标签 id*；低 48 位是*本地 id*，即每个标签自己的序列。它输出为 `labid.locid`：

```sql
SELECT id, graphid_labid(id) AS labid, graphid_locid(id) AS locid
FROM moviekb.movie ORDER BY id LIMIT 3;
```

```
 id  | labid | locid
-----+-------+-------
 3.1 |     3 |     1
 3.2 |     3 |     2
 3.3 |     3 |     3
```

这种布局有两个后果，而且都很重要。

第一，id 自带标签。要知道顶点来自哪张表，不需要再查找。

第二，标签 id 位于*高*位，因此一个标签的所有 id 构成一段连续的 `graphid` 值范围。于是，`id` 上的普通 btree 索引可以回答“这个顶点是 `movie` 吗”，完全不必触碰 `movie` 表。

标签 id 本身保存在 `ag_label`：

```sql
SELECT labname, labid, labkind FROM pg_catalog.ag_label
WHERE graphid = (SELECT oid FROM pg_catalog.ag_graph WHERE graphname = 'moviekb')
ORDER BY labid;
```

```
  labname   | labid | labkind
------------+-------+---------
 ag_vertex  |     1 | v
 ag_edge    |     2 | e
 movie      |     3 | v
 person     |     4 | v
 acted_in   |     5 | e
 directed   |     6 | e
 related_to |     7 | e
```

`labid` 是 16 位，而 0 不是有效标签，因此一个数据库最多有 65,535 个标签。单个标签最多有 2<sup>48</sup> − 1 行。参见[限制](/zh/agensgraph/appendix/limits/)。

## 每个图都有两个你未创建的标签 {#every-graph-has-two-labels-you-did-not-create}

`ag_vertex` 和 `ag_edge` 随图一起创建，你创建的每个标签都继承其中之一：

```sql
SELECT c.relname AS child, p.relname AS parent
FROM pg_inherits i
  JOIN pg_class c ON c.oid = i.inhrelid
  JOIN pg_class p ON p.oid = i.inhparent
  JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'moviekb' ORDER BY 1;
```

```
   child    |  parent
------------+-----------
 acted_in   | ag_edge
 directed   | ag_edge
 movie      | ag_vertex
 person     | ag_vertex
 related_to | ag_edge
```

正是这层继承赋予无标签模式含义。`MATCH (n)` 不扫描某种包含所有内容的特殊索引；它扫描 `ag_vertex`，并通过继承扫描其下的每一张表：

```cypher
EXPLAIN (COSTS OFF) MATCH (n) RETURN n;
```

```
              QUERY PLAN
---------------------------------------
 Result
   ->  Append
         ->  Seq Scan on ag_vertex n_1
         ->  Seq Scan on movie n_2
         ->  Seq Scan on person n_3
```

命名标签会把扫描缩小到那张表及其子表，`ONLY` 修饰符把它进一步缩小为恰好那张表。[标签继承](/zh/agensgraph/concepts/label-inheritance/)介绍了可以用它构建什么。

## 属性索引和约束会变成什么 {#what-a-property-index-and-a-constraint-become}

Cypher 属性索引是 `properties` 列上的 PostgreSQL 表达式索引：

```cypher
CREATE PROPERTY INDEX ON movie (title);
```

```psql
\d moviekb.movie
```

```
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_title_idx" btree ((properties.'title'))
```

唯一约束会变成同一表达式上的排除约束：

```cypher
CREATE CONSTRAINT movie_title_uq ON movie ASSERT title IS UNIQUE;
```

```
Indexes:
    "movie_title_uq" EXCLUDE USING btree ((properties.'title') WITH =)
```

这些定义中的 `properties.'title'` 形式是 Cypher 解析器书写属性读取的方式，不是你在 SQL 中输入的语法。

调优时，普通部分才重要。它们都是基于表达式的 btree 索引。规划器按常规规则选择它们，而且只有当谓词能匹配到该表达式时才有帮助。[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)介绍了哪些谓词符合条件。

## 这带来什么 {#what-this-buys-you}

PostgreSQL 对表做的所有事，也会对标签做。这不是口号；下面就是你不必学两遍的事情清单：

* **事务。** 一个事务中的 Cypher 写入和 SQL 写入会一起提交或回滚，因为它们写的是同一个数据库中的表。
* **访问控制。** `GRANT SELECT ON moviekb.movie TO analyst` 有效，标签上的行级安全也有效。参见[安全](/zh/agensgraph/operations/security/)。
* **备份与复制。** `pg_dump`、`pg_basebackup`、WAL 归档和流复制按图的真实形态处理它——模式和表。
* **扩展。** `pgvector` 可以把向量存放在图旁边，因为属性是扩展可以索引的表中的 `jsonb`。这就是[向量搜索](/zh/agensgraph/guides/search/vector/)指南的全部基础。
* **规划器。** Cypher 查询上的 `EXPLAIN` 会显示顺序扫描、索引扫描和连接；你可以像调优任何 PostgreSQL 查询一样调优它们。

这也是 SQL 与 Cypher 能在一条语句中组合、不需要桥接层的原因：[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。

## 哪些操作被刻意关闭 {#what-is-deliberately-closed-off}

这层映射是真实的，但不是邀请你把图当作普通表直接编辑。两道关卡挡在前面，而且默认都关闭，因为任一操作都可能让图目录描述的内容不再成立。

直接写入行会被拒绝：

```psql
INSERT INTO moviekb.movie (properties) VALUES ('{"title": "x"}');
```

```
ERROR:  DML query to graph objects is not allowed
```

改变标签形状同样会被拒绝：

```sql
ALTER TABLE moviekb.movie ADD COLUMN foo int;
```

```
ERROR:  cannot add a column to graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

`enable_graph_dml` 与 `enable_graph_ddl` 分别打开这两道关卡；[服务器设置](/zh/agensgraph/reference/guc/)说明这样做要承担什么。用 SQL 读取标签不需要任何设置——本页的每个 `SELECT` 都可以直接运行。
