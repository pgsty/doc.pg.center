---
title: DROP GRAPH
linkTitle: DROP GRAPH
description: 删除图；使用 CASCADE 时连同其中的所有标签、顶点和边一起删除。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-graph.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


删除图；使用 `CASCADE` 时连同其中的所有标签、顶点和边一起删除。

## Synopsis {#synopsis}

```text
DROP GRAPH [ IF EXISTS ] graph_name [, ... ] [ CASCADE | RESTRICT ]
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

`DROP GRAPH` 删除图在系统目录中的行及其模式。图持有的所有内容都依赖该模式：标签、标签背后的表、表中的行、索引、约束和序列。因此默认的 `RESTRICT` 只要发现其中任何对象存在就会拒绝删除。

用普通 [`CREATE GRAPH`](/zh/agensgraph/reference/ddl/create-graph/) 创建的图从来不是空图：创建时会同时创建 `ag_vertex`、`ag_edge` 和 `ag_label_seq`。因此每个这样的图都需要 `CASCADE`。只有用 `CREATE GRAPH ONLY` 创建的图可以不带 `CASCADE` 删除，因为这种形式不会创建上述对象。

- 删除图不要求标签为空。`CASCADE` 会随表一起删除其中的行。
- 如果被删除的图是会话的 `graph_path`，该设置会被清空。
- 图的模式不能单独删除：对它执行 `DROP SCHEMA` 会被拒绝，并指向本页语句。

## Parameters {#parameters}

IF EXISTS
: 对不存在的图发出通知而不是错误。同一语句中的其他名称仍会被删除。

graph_name
: 要删除的图名。可以给出多个名称，并用逗号分隔。

CASCADE
: 删除依赖图的对象：其标签、标签对应的表和行，以及标签 ID 序列。

RESTRICT
: 有任何对象依赖图时拒绝删除。这是默认行为。

## Examples {#examples}

### 删除图及其中所有内容 {#drop-a-graph-and-everything-in-it}

```cypher
CREATE GRAPH clearance;
SET graph_path = clearance;
CREATE VLABEL film;
CREATE (:film {title: 'Arrival'});
```

不带 `CASCADE` 时删除会被拒绝，消息会列出阻碍删除的对象：

```cypher
DROP GRAPH clearance;
```

```
ERROR:  cannot drop graph clearance because other objects depend on it
DETAIL:  sequence clearance.ag_label_seq depends on schema clearance
vlabel ag_vertex depends on schema clearance
elabel ag_edge depends on schema clearance
vlabel film depends on schema clearance
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

`CASCADE` 会删除这四个对象，以及 `film` 中的顶点：

```cypher
DROP GRAPH clearance CASCADE;
```

```
NOTICE:  drop cascades to 4 other objects
DETAIL:  drop cascades to sequence clearance.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
drop cascades to vlabel film
DROP GRAPH
```

`clearance` 是会话的 `graph_path`，因此该设置现在为空：

```sql
SHOW graph_path;
```

```
 graph_path
------------

(1 row)
```

### 删除多个图并跳过已不存在的图 {#drop-several-graphs-skipping-the-ones-that-are-gone}

```cypher
CREATE GRAPH archive_2024;
CREATE GRAPH archive_2025;
DROP GRAPH IF EXISTS archive_2024, archive_2025, archive_2026 CASCADE;
```

```
NOTICE:  graph "archive_2026" does not exist, skipping
NOTICE:  drop cascades to 6 other objects
DETAIL:  drop cascades to sequence archive_2025.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
drop cascades to sequence archive_2024.ag_label_seq
drop cascades to vlabel ag_vertex
drop cascades to elabel ag_edge
DROP GRAPH
```

缺失的名称会被报告，存在的两个图则被删除：

```psql
\dG archive*
```

```
No matching graphs found.
```

## Notes {#notes}

要清空图而不删除它，可运行 `MATCH (n) DETACH DELETE n`，然后删除不再需要的标签。模式和基础标签会保留。[`DROP VLABEL`](/zh/agensgraph/reference/ddl/drop-label/) 只有在标签为空时才能删除它，因此这个删除操作通常是第一步。`DROP GRAPH ... CASCADE` 完全绕过该要求，因为它删除的是表，而不是逐个删除标签。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 的 `<drop graph statement>`（§12.5）是
`DROP [PROPERTY] GRAPH [IF EXISTS] <name>`。AgensGraph 接受其中的 `DROP GRAPH` 和
`IF EXISTS` 部分，并新增了名称列表以及 GQL 没有的 `CASCADE`/`RESTRICT` 选择。不接受
`PROPERTY` 拼法：`DROP PROPERTY GRAPH clearance` 是语法错误。

### PostgreSQL {#postgresql}

`DROP GRAPH` 对应 `DROP SCHEMA`，`IF EXISTS`、名称列表和 `CASCADE`/`RESTRICT` 的行为也与 PostgreSQL 相同。差别在于它拒绝留下半删除的图。对图的模式执行 `DROP SCHEMA` 会失败，错误为
`cannot drop schema clearance because graph clearance requires it`，因此目录行和模式总是同时删除。

## See also {#see-also}

- [`CREATE GRAPH`](/zh/agensgraph/reference/ddl/create-graph/)
- [`DROP VLABEL` 与 `DROP ELABEL`](/zh/agensgraph/reference/ddl/drop-label/)
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)
