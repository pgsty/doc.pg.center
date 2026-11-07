---
title: DROP VLABEL 与 DROP ELABEL
linkTitle: DROP VLABEL 与 DROP ELABEL
description: 删除顶点标签或边标签；使用 CASCADE 时连同其中的行一起删除。
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-label.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


删除顶点标签或边标签；使用 `CASCADE` 时连同其中的行一起删除。

## Synopsis {#synopsis}

```text
DROP VLABEL [ IF EXISTS ] label_name [, ... ] [ CASCADE | RESTRICT ]DROP ELABEL [ IF EXISTS ] label_name [, ... ] [ CASCADE | RESTRICT ]
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

`DROP VLABEL` 删除顶点标签，`DROP ELABEL` 删除边标签；二者各自拒绝另一种标签。删除标签会删除其背后的表，以及它的 ID 序列、索引和约束。

默认的 `RESTRICT` 会在两种情况下拒绝：

- **还有行。** 仍持有顶点或边的标签会以 `cannot drop <label> because it is not empty.` 被拒绝。这比 PostgreSQL 对表执行的依赖检查更严格，容易让人意外。
- **还有子标签。** 有子标签的标签会被拒绝，消息会指出该子标签。

`CASCADE` 会越过这两种限制。无论标签持有什么，它都会删除标签，并且：

- 删除**顶点**标签会删除附着在其顶点上的边，无论这些边属于哪个标签。边标签本身保留。
- 删除**边**标签只删除它自己的边。被这些边连接的顶点保留。

标签在 `graph_path` 指定的图中查找；名称不能带限定名。

- 基础标签 `ag_vertex` 和 `ag_edge` 不能删除。
- 标签背后的表不能单独删除：对它执行 `DROP TABLE` 会被拒绝，并指向本页语句。
- 要清空图而不删除标签，可改用 `MATCH (n) DETACH DELETE n`。

## Parameters {#parameters}

IF EXISTS
: 对不存在的标签发出通知而不是错误。同一语句中的其他名称仍会被删除。

label_name
: 要删除的标签名。可以给出多个名称，并用逗号分隔。

CASCADE
: 连同行和子标签一起删除标签。对于顶点标签，还删除附着在其顶点上的边。

RESTRICT
: 标签持有任何行或有子标签时拒绝删除。这是默认行为。

## Examples {#examples}

这些示例创建自己的图 `tidygraph`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH tidygraph;
SET graph_path = tidygraph;
CREATE VLABEL film;
CREATE VLABEL person;
CREATE ELABEL directed;
CREATE (:person {name: 'Denis Villeneuve'})-[:directed]->(:film {title: 'Arrival'});
CREATE VLABEL draft;
```

### 删除空标签 {#drop-an-empty-label}

```cypher
DROP VLABEL draft;
```

```
DROP VLABEL
```

没有其他报告，因为没有其他对象受影响。

### 删除仍持有顶点的标签 {#drop-a-label-that-still-holds-vertices}

`film` 中有一个顶点，因此默认形式会拒绝：

```cypher
DROP VLABEL film;
```

```
ERROR:  cannot drop film because it is not empty.
```

`CASCADE` 会删除标签、其中的顶点，以及指向它的 `directed` 边：

```cypher
DROP VLABEL film CASCADE;
```

```
DROP VLABEL
```

```cypher
MATCH ()-[e:directed]->() RETURN count(e) AS directed_edges;
```

```
 directed_edges 
----------------
 0
(1 row)
```

边没有了，但它的标签还在。`directed` 仍然存在且为空：

```psql
\dGl tidygraph.dir*
```

```
           List of labels
   Graph   |   Name   | Type | Owner
-----------+----------+------+-------
 tidygraph | directed | edge | agens
(1 row)
```

### 删除父标签 {#drop-a-parent-label}

```cypher
CREATE VLABEL work;
CREATE VLABEL documentary INHERITS (work);
DROP VLABEL work;
```

```
ERROR:  cannot drop vlabel work because other objects depend on it
DETAIL:  vlabel documentary depends on vlabel work
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

`CASCADE` 会指出随之删除的子标签：

```cypher
DROP VLABEL work CASCADE;
```

```
NOTICE:  drop cascades to vlabel documentary
DROP VLABEL
```

### 删除多个标签并跳过已不存在的标签 {#drop-several-labels-skipping-the-ones-that-are-gone}

```cypher
CREATE VLABEL a;
CREATE VLABEL b;
DROP VLABEL IF EXISTS a, b, c;
```

```
NOTICE:  vlabel "c" does not exist, skipping
DROP VLABEL
```

### 值得识别的拒绝情况 {#refusals-worth-recognizing}

每条语句只删除一种标签：

```cypher
DROP ELABEL person;
```

```
ERROR:  DROP ELABEL cannot DROP vertex label
```

基础标签保留：

```cypher
DROP VLABEL ag_vertex;
```

```
ERROR:  DROP base vertex label is prohibited
```

也不能绕过标签删除其背后的表：

```sql
DROP TABLE tidygraph.person;
```

```
ERROR:  cannot drop table tidygraph.person because vlabel person requires it
HINT:  You can drop vlabel person instead.
```

最后删除示例创建的图：

```cypher
DROP GRAPH tidygraph CASCADE;
```

## Notes {#notes}

端点顶点被删除时，附着在它上面的边会随之删除；本语句和 `DETACH DELETE` 都是这样。`start` 与 `end` 是普通的 `graphid` 列，不是外键。这个行为来自图写入路径，而不是表上的引用动作。

> [!NOTE]
> `cypher_allow_unsafe_ddl` 会关闭标签类型检查和基础标签检查。开启后，`DROP ELABEL` 可以删除顶点标签，`ag_vertex` 也可以删除。它用于修复目录已经损坏的图。其他情况下保持关闭。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有删除标签的语句。元素类型属于图类型，而图类型由 `<drop graph type statement>`（§12.7）整体删除；删除图类型不会删除任何数据。图类型在 [GQL 一致性矩阵](/zh/agensgraph/appendix/gql-conformance/)中记录为规划项。

### PostgreSQL {#postgresql}

`DROP VLABEL` 和 `DROP ELABEL` 对应 `DROP TABLE`，`IF EXISTS`、名称列表和 `CASCADE`/`RESTRICT` 的行为也与 PostgreSQL 相同。有一处新增行为没有 `DROP TABLE` 对应物。`DROP TABLE` 不关心表中有多少行；这些语句在标签非空时会拒绝，除非写 `CASCADE`。而且对于顶点标签，`CASCADE` 还会删除*其他*标签中的边。这里的 `CASCADE` 应理解为“连同依赖它的图数据”，而不只是“连同依赖它的目录对象”。

## See also {#see-also}

- [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)
- [`CREATE ELABEL`](/zh/agensgraph/reference/ddl/create-elabel/)
- [`ALTER VLABEL` 与 `ALTER ELABEL`](/zh/agensgraph/reference/ddl/alter-label/)
- [`DROP GRAPH`](/zh/agensgraph/reference/ddl/drop-graph/)
- [标签继承](/zh/agensgraph/concepts/label-inheritance/)
