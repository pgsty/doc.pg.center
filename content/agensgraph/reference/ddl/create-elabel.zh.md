---
title: CREATE ELABEL
linkTitle: CREATE ELABEL
description: 创建边标签，即一张继承图基础边标签的 (id, start, end, properties) 表；可选地把属性提升为类型列。
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-elabel.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


创建边标签，即一张继承图基础边标签的 `(id, start, end, properties)` 表；可选地把属性提升为类型列。

## Synopsis {#synopsis}

```text
CREATE [ UNLOGGED ] ELABEL [ IF NOT EXISTS ] label_name [ ( promoted_property [, ... ] ) ]    [ DISABLE INDEX ]    [ INHERITS ( parent_label [, ... ] ) ]    [ WITH ( storage_parameter [= value] [, ... ] ) ]    [ TABLESPACE tablespace_name ]CREATE [ UNLOGGED ] ELABEL ONLY label_name ( label_id ) [ option ... ]where promoted_property is one of:    column_name data_type GENERATED    column_name data_type GENERATED ( property_key )    column_name data_type GENERATED ALWAYS AS ( expression ) [ STORED ]
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

边标签是一张有四列的表：`graphid` 类型的 `id`、边 `start` 与 `end` 顶点的 `graphid`，以及 `jsonb` 类型的 `properties` 列。除非指定父标签，它继承图的 `ag_edge`。

创建边标签还会创建为其编号的序列和三个索引。其中两个是 B-tree 索引，分别在 `(start, "end")` 与 `("end", start)` 上，让两个方向的遍历都更快。第三个是 `id` 上的 BRIN 索引。边标签的 `id` 没有主键，因为边通过端点访问。[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)完整介绍该布局。

标签创建在 `graph_path` 指定的图中。

- **选项位置敏感。** 必须按所示顺序出现：先 `DISABLE INDEX`，再 `INHERITS`，再 `WITH`，最后 `TABLESPACE`。其他顺序都是语法错误。
- `INHERITS` 中指定的父标签必须在同一个图中，并且必须是边标签。指定顶点标签会被拒绝。
- `IF NOT EXISTS` 与 `ONLY` 属于不同形式，不能组合。
- 边标签不限制端点可以有哪些标签。`start` 与 `end` 是普通 `graphid` 列，不是外键。
- Cypher 会按需创建标签：在没有 `directed` 标签的图上执行 `CREATE (a)-[:directed]->(b)` 会创建它。需要选项、提升列或父标签时使用 `CREATE ELABEL`。

### Promoted properties {#promoted-properties}

提升属性是位于 `properties` 包旁边的类型列，由该包计算并存储。读取这个属性时会访问列，而不是进入 JSON 文档。三种形式和限制与顶点标签相同，[`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/#promoted-properties) 已完整列出。边标签的保留列名是 `id`、`properties`、`start` 和 `end`。

## Parameters {#parameters}

UNLOGGED
: 将标签表创建为 unlogged 表：其内容不写入预写日志，崩溃后会丢失。

IF NOT EXISTS
: 同名标签已存在时发出通知而不是错误。不会创建任何内容；既有标签的选项也不会改变。

label_name
: 要创建的标签名，位于 `graph_path` 指定的图中。

promoted_property
: 要镜像到类型列的属性。列按书写顺序添加在 `properties` 之后。

DISABLE INDEX
: 创建标签的三个索引但保持无效，使加载行时不必维护它们。读写仍然可用；规划器会忽略无效索引。用 [`REINDEX ELABEL`](/zh/agensgraph/reference/ddl/reindex/) 重建。没有 `ENABLE INDEX`。

INHERITS ( parent_label [, ...] )
: 父标签，替换默认父标签 `ag_edge`。每个父标签都必须是同一个图中的边标签。参见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。

WITH ( storage_parameter [= value] [, ...] )
: 标签表的存储参数，与 `CREATE TABLE` 相同。

TABLESPACE tablespace_name
: 标签表的表空间。省略时由 `default_tablespace` 决定。

ONLY label_name ( label_id )
: 以给定标签 ID 创建标签，不创建默认父标签、ID 默认值或端点索引。`pg_dump` 输出的就是这个形式，以便恢复时保留转储图中的 ID。仅在复现转储时使用。

## Examples {#examples}

这些示例创建自己的图 `castlists`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

### 创建边标签 {#create-an-edge-label}

```cypher
CREATE GRAPH castlists;
SET graph_path = castlists;
CREATE VLABEL person;
CREATE VLABEL film;
CREATE ELABEL worked_on;
```

```
CREATE ELABEL
```

```psql
\d castlists.worked_on
```

```
                                                             Table "castlists.worked_on"
   Column   |  Type   | Collation | Nullable |                                                Default                                                
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('castlists.worked_on'::cstring), nextval('castlists.worked_on_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "worked_on_end_idx" btree ("end", start)
    "worked_on_id_idx" brin (id)
    "worked_on_start_idx" btree (start, "end")
Inherits: castlists.ag_edge
```

创建标签还把 `start` 和 `end` 的统计目标设为 1000，因为遍历的行估计取决于这两列的分布：

```sql
SELECT attname, attstattarget FROM pg_attribute
 WHERE attrelid = 'castlists.worked_on'::regclass AND attnum > 0;
```

```
  attname   | attstattarget 
------------+---------------
 id         |              
 start      |          1000
 end        |          1000
 properties |              
(4 rows)
```

### 将多种边类型归入一个父标签 {#group-several-edge-types-under-one-parent}

```cypher
CREATE ELABEL acted_in INHERITS (worked_on);
CREATE ELABEL directed INHERITS (worked_on);
```

```psql
\dGe castlists.acted_in
```

```
           List of labels
   Graph   |   Name   | Type | Owner
-----------+----------+------+-------
 castlists | acted_in | edge | agens
(1 row)

Edge label "castlists.acted_in"
--
Inherits: castlists.worked_on
```

父标签上的模式现在可以匹配两种边，而 `label()` 仍报告创建边时使用的具体标签：

```cypher
CREATE (:person {name: 'Denis Villeneuve'})-[:directed {credited: true}]->(:film {title: 'Arrival'});
MATCH (p)-[e:worked_on]->(f) RETURN label(e) AS type, e.credited AS credited;
```

```
    type    | credited 
------------+----------
 "directed" | true
(1 row)
```

### 仅在标签不存在时创建 {#create-a-label-only-if-it-is-not-there}

```cypher
CREATE ELABEL IF NOT EXISTS acted_in;
```

```
NOTICE:  label "acted_in" already exists, skipping
CREATE ELABEL
```

### 先加载边标签再构建索引 {#load-an-edge-label-before-building-its-indexes}

三个索引都会创建为无效，而表本身是 unlogged 表：

```cypher
CREATE UNLOGGED ELABEL staged DISABLE INDEX WITH (fillfactor = 70) TABLESPACE pg_default;
```

```psql
\d castlists.staged
```

```
                                                       Unlogged table "castlists.staged"
   Column   |  Type   | Collation | Nullable |                                             Default                                             
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('castlists.staged'::cstring), nextval('castlists.staged_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "staged_end_idx" btree ("end", start) INVALID
    "staged_id_idx" brin (id) INVALID
    "staged_start_idx" btree (start, "end") INVALID
Inherits: castlists.ag_edge
```

加载边之后，运行 `REINDEX ELABEL staged` 构建三个索引。

### 将边属性提升为类型列 {#promote-an-edge-property-to-a-typed-column}

```cypher
CREATE ELABEL scored (rating numeric GENERATED, source text GENERATED (site));
```

```psql
\d castlists.scored
```

```
                                                           Table "castlists.scored"
   Column   |  Type   | Collation | Nullable |                                             Default                                             
------------+---------+-----------+----------+-------------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('castlists.scored'::cstring), nextval('castlists.scored_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
 rating     | numeric |           |          | generated always as (ag_property_text(properties, 'rating'::text, 'n'::"char")::numeric) stored
 source     | text    |           |          | generated always as (ag_property_text(properties, 'site'::text, 's'::"char")) stored
Indexes:
    "scored_end_idx" btree ("end", start)
    "scored_id_idx" brin (id)
    "scored_start_idx" btree (start, "end")
Inherits: castlists.ag_edge
```

写入边会填充两列：

```cypher
MATCH (p:person), (f:film) CREATE (p)-[:scored {rating: 8.5, site: 'critics'}]->(f);
```

```
UPDATE 1
```

SQL 用列名读取它们：

```sql
SELECT rating, source FROM castlists.scored;
```

```
 rating | source  
--------+---------
    8.5 | critics
(1 row)
```

Cypher 用属性键读取它们，因此第二个是 `e.site`，不是 `e.source`：

```cypher
MATCH ()-[e:scored]->() RETURN e.rating AS rating, e.site AS site;
```

```
 rating |  site   
--------+---------
    8.5 | critics
(1 row)
```

### 值得识别的拒绝情况 {#refusals-worth-recognizing}

边标签只能继承边标签：

```cypher
CREATE ELABEL wrong INHERITS (person);
```

```
ERROR:  parent graph label "person" is not edge label.
```

最后删除示例创建的图：

```cypher
DROP GRAPH castlists CASCADE;
```

## Notes {#notes}

标签名不能带限定名。`CREATE ELABEL castlists.directed` 是语法错误，图始终来自 `graph_path`。未设置时，语句以 `graph_path is NULL` 停止。

`\dGe` 列出边标签并描述每个匹配项；`\dGl` 列出两种标签但不给详情。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有标签 DDL。边由图类型中的*边类型*描述，图类型来自 `<create graph type statement>`（§12.6）。边类型命名边的端点节点类型和属性，并约束引用它的图。AgensGraph 逐个声明边标签，而边标签既不约束端点，也不约束属性。图类型在 [GQL 一致性矩阵](/zh/agensgraph/appendix/gql-conformance/)中记录为规划项。

### PostgreSQL {#postgresql}

`CREATE ELABEL` 对应 `CREATE TABLE`。`UNLOGGED`、`IF NOT EXISTS`、`INHERITS`、`WITH` 和 `TABLESPACE` 的含义与 PostgreSQL 相同，提升属性形式会变成 `GENERATED ALWAYS AS ... STORED` 生成列。差别是固定的四列形状、自动创建的三个索引、在 `ag_label` 中的注册、自动父标签，以及位置敏感的选项顺序。`start` 与 `end` 不是外键，因此表层不会阻止边指向已删除的顶点。[`DROP VLABEL`](/zh/agensgraph/reference/ddl/drop-label/) 负责处理这种情况。

## See also {#see-also}

- [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)
- [`ALTER VLABEL` 与 `ALTER ELABEL`](/zh/agensgraph/reference/ddl/alter-label/)
- [`DROP VLABEL` 与 `DROP ELABEL`](/zh/agensgraph/reference/ddl/drop-label/)
- [`REINDEX VLABEL` 与 `REINDEX ELABEL`](/zh/agensgraph/reference/ddl/reindex/)
- [标签继承](/zh/agensgraph/concepts/label-inheritance/)
