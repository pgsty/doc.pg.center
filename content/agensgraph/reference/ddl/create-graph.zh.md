---
title: CREATE GRAPH
linkTitle: CREATE GRAPH
description: 创建图，即一个模式、所有标签共同继承的两个基础标签，以及分配标签 ID 的序列。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-graph.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


创建图，即一个模式、所有标签共同继承的两个基础标签，以及分配标签 ID 的序列。

## Synopsis {#synopsis}

```text
CREATE GRAPH [ IF NOT EXISTS ] graph_name [ AUTHORIZATION role_specification ]CREATE GRAPH ONLY graph_name
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

图就是模式。`CREATE GRAPH` 创建该模式，并在其中放入三个对象：

- `ag_vertex`，基础顶点标签；
- `ag_edge`，基础边标签；
- `ag_label_seq`，分配标签 ID 的序列。

之后创建的每个标签都继承自 `ag_vertex` 或 `ag_edge`。这个继承关系让 `MATCH (n)` 这类无标签模式有了明确含义。[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)完整说明了这些对象和标识符方案。

- 该名称必须同时未作为图名和模式名占用，因为图拥有同名模式。
- 如果会话的 `graph_path` 为空，`CREATE GRAPH` 会把它设为新图。已经设置的 `graph_path` 保持不变。
- `CREATE GRAPH ONLY` 只创建模式和目录行，不创建其他对象。`pg_dump` 输出的就是这个形式，以便恢复时能用原始标签 ID 自行重建基础标签。在基础标签存在之前，这样创建的图不能持有标签。

## Parameters {#parameters}

IF NOT EXISTS
: 同名图已存在时发出通知而不是错误。不会创建任何内容，也不会改变既有对象。

graph_name
: 要创建的图名。

AUTHORIZATION role_specification
: 拥有图及随图创建对象的角色。可以写角色名、`CURRENT_ROLE`、`CURRENT_USER` 或 `SESSION_USER`。省略该子句时，图属于执行语句的角色。

ONLY
: 创建模式和目录行，但不创建 `ag_vertex`、`ag_edge` 或 `ag_label_seq`。与普通形式不同，它不会改动 `graph_path`。

## Examples {#examples}

这些示例创建自己的图 `boxoffice`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

### 创建图 {#create-a-graph}

```cypher
CREATE GRAPH boxoffice;
```

```
CREATE GRAPH
```

该语句占用了原本为空的 `graph_path`：

```sql
SHOW graph_path;
```

```
 graph_path
------------
 boxoffice
(1 row)
```

`\dG` 会列出这个图：

```psql
\dG boxoffice
```

```
  List of graphs
   Name    | Owner
-----------+-------
 boxoffice | agens
(1 row)
```

它已经持有两个基础标签：

```psql
\dGl boxoffice.*
```

```
             List of labels
   Graph   |   Name    |  Type  | Owner
-----------+-----------+--------+-------
 boxoffice | ag_edge   | edge   | agens
 boxoffice | ag_vertex | vertex | agens
(2 rows)
```

### 仅在图不存在时创建 {#create-a-graph-only-if-it-is-not-there}

```cypher
CREATE GRAPH IF NOT EXISTS boxoffice;
```

```
NOTICE:  graph "boxoffice" already exists, skipping
CREATE GRAPH
```

既有图不会被改动。这不是“创建或替换”。

### 创建由其他角色拥有的图 {#create-a-graph-owned-by-another-role}

```sql
CREATE ROLE curator;
```

```cypher
CREATE GRAPH festival AUTHORIZATION curator;
```

```
CREATE GRAPH
```

```psql
\dG festival
```

```
   List of graphs
   Name   |  Owner
----------+---------
 festival | curator
(1 row)
```

### 创建不含基础标签的模式 {#create-the-schema-without-the-base-labels}

```cypher
CREATE GRAPH ONLY skeleton;
```

```
CREATE GRAPH
```

图存在，但其中没有任何对象：

```psql
\dGl skeleton.*
```

```
No matching labels found.
```

由于缺少 `ag_vertex`，不能在其中创建标签：

```cypher
SET graph_path = skeleton;
CREATE VLABEL film;
```

```
ERROR:  relation "skeleton.ag_vertex" does not exist
```

清理这三个图和角色：

```cypher
DROP GRAPH boxoffice CASCADE;
DROP GRAPH festival CASCADE;
DROP GRAPH skeleton;
```

```sql
DROP ROLE curator;
```

`skeleton` 不需要 `CASCADE`，因为其中没有创建任何对象。普通形式创建的图始终需要。参见[`DROP GRAPH`](/zh/agensgraph/reference/ddl/drop-graph/)。

## Notes {#notes}

`graph_path` 指定未限定标签名所属的图。它是逐会话设置；每个新会话都要设置，也可以把它附加到数据库或角色上：

```sql
ALTER DATABASE <database> SET graph_path = boxoffice;
```

还有两条语句作用于整图。二者都没有 `IF EXISTS` 形式：

```cypher
CREATE GRAPH receipts;
ALTER GRAPH receipts RENAME TO takings;
ALTER GRAPH takings OWNER TO CURRENT_USER;
SHOW graph_path;
```

```
 graph_path
------------
 takings
(1 row)
```

重命名会随图一起移动底层模式，会话的 `graph_path` 也会跟随它。因此上面的结果是 `takings`，而不是 `receipts`。

```cypher
DROP GRAPH takings CASCADE;
```

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 将 `<create graph statement>`（§12.4）定义为
`CREATE [PROPERTY] GRAPH <name> {<open graph type> | <of graph type>}`。图可以创建为接受任意内容的 `ANY`，也可以按约束其节点类型、边类型和属性的*图类型*创建。AgensGraph 的图始终是开放图，因此不写图类型，也不可能写。不接受 `PROPERTY` 拼法：`CREATE PROPERTY GRAPH boxoffice` 是语法错误。图类型在 [GQL 一致性矩阵](/zh/agensgraph/appendix/gql-conformance/)中记录为规划项。

`AUTHORIZATION` 和 `ONLY` 是 AgensGraph 自有扩展；GQL 没有二者。GQL 的 `OR REPLACE` 形式也不被接受。

### PostgreSQL {#postgresql}

`CREATE GRAPH` 对应 `CREATE SCHEMA`，`IF NOT EXISTS` 和 `AUTHORIZATION` 的含义也与 PostgreSQL 相同。差别在内容。`CREATE SCHEMA` 创建空模式；`CREATE GRAPH` 还会创建基础标签和标签 ID 序列，并在 `ag_graph` 中注册模式，使 Cypher 能找到它。单独的 `CREATE SCHEMA` 不会产生图。

## See also {#see-also}

- [`DROP GRAPH`](/zh/agensgraph/reference/ddl/drop-graph/)
- [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)
- [`CREATE ELABEL`](/zh/agensgraph/reference/ddl/create-elabel/)
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)
