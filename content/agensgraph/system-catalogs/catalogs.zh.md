---
title: 图目录
linkTitle: 图目录
description: AgensGraph 在 pg_catalog 中新增七张表。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/system_catalogs/catalogs.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 在 `pg_catalog` 中新增七张表。其中四张描述图结构，也是你通常要查询的表；另外三张是每个标签继承的共享父关系。PostgreSQL 自身目录未改变，见[其目录章节](https://www.postgresql.org/docs/18/catalogs.html)。

| 目录 | 保存内容 |
| --- | --- |
| [`ag_graph`](#ag_graph) | 每个图一行。 |
| [`ag_label`](#ag_label) | 每个标签一行，顶点标签和边标签都在其中。 |
| [`ag_label_property`](#ag_label_property) | 每个提升为类型化列的属性一行。 |
| [`ag_graphmeta`](#ag_graphmeta) | 按（起始标签、边标签、结束标签）三元组统计的边数。 |
| `ag_vertex`、`ag_edge` | 图中每个顶点或边标签的父关系。每一对存在于各自图的模式中，而不在 `pg_catalog` 中。 |
| `ag_graphpath` | 支撑 `graphpath` 类型的组合类型。 |

两个视图以可读形式呈现同样信息：见[图视图](/zh/agensgraph/system-catalogs/views/)。

## ag_graph {#ag_graph}

每个图一行。图是模式，所以 `nspid` 指向承载其标签的模式。

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `oid` | `oid` | 行标识符。 |
| `graphname` | `name` | 图名。在数据库内唯一。 |
| `nspid` | `oid` | 图模式对应的 `pg_namespace` 行。 |
| `graphmeta_valid` | `boolean` | `ag_graphmeta` 对这个图是否为最新。为 false 表示规划器不能将其用于扫描剪枝。 |

```sql
SELECT oid, graphname, nspid, graphmeta_valid FROM pg_catalog.ag_graph;
```

```
  oid  | graphname | nspid | graphmeta_valid
-------+-----------+-------+-----------------
 16386 | g         | 16385 | t
 16434 | moviekb   | 16433 | f
```

当元数据已知过期时，例如二进制升级之后，`graphmeta_valid` 会设为 false。`SELECT regather_graphmeta();` 会重建元数据并设置该标志。见[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)。

## ag_label {#ag_label}

每个标签一行。顶点标签和边标签都在这里，由 `labkind` 区分。

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `oid` | `oid` | 行标识符。 |
| `labname` | `name` | 标签名。在图内唯一。 |
| `graphid` | `oid` | 该标签所属的 `ag_graph` 行。 |
| `labid` | `integer` | 标签在图内的 id，也是其中每个 `graphid` 的高 16 位。 |
| `relid` | `oid` | 标签表对应的 `pg_class` 行。 |
| `labkind` | `"char"` | `v` 表示顶点标签，`e` 表示边标签。 |

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

`labid` 1 和 2 总是图的 `ag_vertex` 和 `ag_edge`，二者随图一起创建。因为 `labid` 是 16 位且 0 无效，一个图最多有 65,535 个标签。见[限制](/zh/agensgraph/appendix/limits/)。

把 `relid` 连接到 `pg_class`，可以从标签找到它的表。正是这个连接让普通的 PostgreSQL 内省能够作用于图：

```sql
SELECT l.labname, pg_size_pretty(pg_total_relation_size(l.relid)) AS size
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
WHERE g.graphname = 'moviekb' AND l.labkind = 'v'
ORDER BY 1;
```

## ag_label_property {#ag_label_property}

每个[提升为类型化列](/zh/agensgraph/querying/typed-columns/)的属性一行。这个目录是 2.18 新增的。

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `laboid` | `oid` | 提升列所属的 `ag_label` 行。 |
| `propname` | `name` | 该列承载的属性键。 |
| `attnum` | `smallint` | 列在标签表中的属性编号。 |
| `semantics` | `"char"` | 列与属性的关系。 |

主键是 `(laboid, propname)`，因此一个标签对给定键最多提升一次。

只有这里存在行时，属性读取才会解析到提升列。这个机制是提升表单令人意外的原因。`GENERATED ALWAYS AS (expr) STORED` 会创建列，但不会在这个目录中登记行。因此该列可以从 SQL 读取，却对 Cypher 属性读取不可见。

## ag_graphmeta {#ag_graphmeta}

图中实际出现的每个（起始标签、边标签、结束标签）三元组一行，并给出组成它的边数。规划器以两种方式使用它：估算遍历，以及剪除不可能参与模式的标签扫描。

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `graph` | `oid` | `ag_graph` 行。 |
| `edge` | `smallint` | 边标签的 `labid`。 |
| `start` | `smallint` | 起始顶点标签的 `labid`。 |
| `end` | `smallint` | 结束顶点标签的 `labid`。 |
| `edgecount` | `bigint` | 这种形态的边有多少条。 |

请通过 [`ag_graphmeta_view`](/zh/agensgraph/system-catalogs/views/#ag_graphmeta_view) 读取它；该视图会把标签 id 解析为名称。只有在 `auto_gather_graphmeta` 开启时才维护这张表，`regather_graphmeta()` 会从头重建它。[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)介绍二者。

## ag_vertex 与 ag_edge {#ag_vertex-and-ag_edge}

它们不在 `pg_catalog` 中。每个图的模式都包含自己的一对关系，你创建的每个标签都继承其中之一。正是这个继承让无标签模式有了含义。见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

`<graph>.ag_vertex` 具有顶点列对 `(id graphid, properties jsonb)`。`<graph>.ag_edge` 增加端点，为 `(id, start, end, properties)`。

## ag_graphpath {#ag_graphpath}

支撑 [`graphpath`](/zh/agensgraph/reference/types/) 的组合类型。它是实现细节。请用模式语法和路径函数创建、读取路径，而不要直接操作它。
