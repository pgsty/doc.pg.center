---
title: ALTER VLABEL 与 ALTER ELABEL
linkTitle: ALTER VLABEL 与 ALTER ELABEL
description: 重命名标签，更改其存储，附加或分离父标签，禁用其索引，或添加和删除提升的类型列。
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/alter-label.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


重命名标签，更改其存储，附加或分离父标签，禁用其索引，或添加和删除提升的类型列。

## Synopsis {#synopsis}

```text
ALTER VLABEL [ IF EXISTS ] label_name action [, ... ]ALTER VLABEL [ IF EXISTS ] label_name RENAME TO new_label_nameALTER ELABEL [ IF EXISTS ] label_name action [, ... ]ALTER ELABEL [ IF EXISTS ] label_name RENAME TO new_label_namewhere action is one of:    ADD [ COLUMN ] promoted_property    DROP [ COLUMN ] column_name [ CASCADE | RESTRICT ]    DISABLE INDEX    SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }    SET TABLESPACE tablespace_name    SET { LOGGED | UNLOGGED }    CLUSTER ON index_name    SET WITHOUT CLUSTER    INHERIT parent_label    NO INHERIT parent_label    REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }    OWNER TO role_specification
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

`ALTER VLABEL` 作用于顶点标签，`ALTER ELABEL` 作用于边标签。除关键字外，两条语句相同：**上面列出的每个动作都可用于两种标签。**差别在于每种标签为动作提供的作用对象不同。

- 标签创建时得到的索引不同：顶点标签在 `id` 上得到主键；边标签在 `(start, "end")` 和 `("end", start)` 上得到 B-tree 索引，并在 `id` 上得到 BRIN 索引。无论哪种情况，`DISABLE INDEX` 都会使该标签的全部索引失效；因此新的顶点标签有一个可失效的索引，新的边标签有三个。`CLUSTER ON` 可选的索引名也不同。
- `DROP COLUMN` 拒绝的结构列，在顶点标签上是 `id` 和 `properties`，在边标签上还包括 `start` 和 `end`。
- `INHERIT` 与 `NO INHERIT` 要求父标签与该标签同属一种类型，并且位于同一个图中。

标签在 `graph_path` 指定的图中查找；名称不能带限定名。

- `RENAME TO` 是独立形式。它不能与任何其他动作组合；包含多个动作的列表也不能包含它。
- 一条语句中的多个动作用逗号分隔，并按顺序应用。
- 基础标签 `ag_vertex` 和 `ag_edge` 完全不能修改。
- `ALTER VLABEL` 拒绝边标签，`ALTER ELABEL` 拒绝顶点标签。

除非开启 `enable_graph_ddl`，用 `ALTER TABLE` 重塑标签会被拒绝。图目录描述标签的列，而 `ALTER TABLE` 不会更新它。[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-is-deliberately-closed-off)介绍了这道门禁。

## Parameters {#parameters}

IF EXISTS
: 标签不存在时发出通知而不是错误。

label_name
: 要修改的标签，位于 `graph_path` 指定的图中。

RENAME TO new_label_name
: 给标签一个新名称。顶点和边保留自己的 ID，因此对重命名前创建的行，`label()` 会报告新名称。表的序列和索引保留创建时的名称，所以写 `CLUSTER ON` 前要先检查它们。

ADD [ COLUMN ] promoted_property
: 添加一个提升的类型列，并从既有行回填它。`promoted_property` 采用与
  [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/#promoted-properties) 相同的三种形式，限制也相同。标签上已提升的属性会被拒绝；在同一条语句中把同一个键提升两次也会被拒绝。

DROP [ COLUMN ] column_name [ CASCADE | RESTRICT ]
: 删除一个列；若是提升属性，则同时忘记其映射。标签的结构列会被拒绝。建立在被删列上的索引会随之删除。

DISABLE INDEX
: 将标签上的每个索引标记为无效，使批量加载不必维护它们。读写仍可继续，规划器会忽略无效索引。没有
  `ENABLE INDEX`；恢复方式是 [`REINDEX VLABEL`](/zh/agensgraph/reference/ddl/reindex/)。

SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN }
: 设置标签 `properties` 列的存储模式。该模式决定大型属性映射是保存在行内、表的 TOAST 关系中，以及是否压缩。标签初始为 `EXTENDED`，即行外存储并压缩。这条语句只改变后续写入的策略，不会重写已存储的内容。

SET TABLESPACE tablespace_name
: 把标签的表移动到另一个表空间。其索引保持原位。

SET { LOGGED | UNLOGGED }
: 打开或关闭标签表的预写日志。标签的 ID 序列会随之改变持久性。

CLUSTER ON index_name
: 把一个索引记录为后续 `CLUSTER` 应使用的索引。它现在不会重排任何数据。

SET WITHOUT CLUSTER
: 忘记该记录。

INHERIT parent_label
: 把标签添加为同图中同类型另一个标签的子标签，因此匹配父标签的模式会开始匹配这个标签的行。

NO INHERIT parent_label
: 移除该关系。

REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }
: 为逻辑复制选择写入操作写入 WAL 的旧值，用这些值标识一行。

OWNER TO role_specification
: 把标签交给另一个角色。写角色名、`CURRENT_ROLE`、`CURRENT_USER` 或
  `SESSION_USER`。

## Examples {#examples}

这些示例自建 `catalogue` 图，而不是使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH catalogue;
SET graph_path = catalogue;
CREATE VLABEL film;
CREATE (:film {title: 'Arrival', year: 2016}), (:film {title: 'Dune', year: 2021});
```

### 重命名标签 {#rename-a-label}

```cypher
ALTER VLABEL film RENAME TO movie;
```

```psql
\dGl catalogue.mov*
```

```
           List of labels
   Graph   | Name  |  Type  | Owner
-----------+-------+--------+-------
 catalogue | movie | vertex | agens
(1 row)
```

行也随标签一起保留：

```cypher
MATCH (m:movie) RETURN count(m) AS movies;
```

```
 movies 
--------
 2
(1 row)
```

序列和主键仍使用旧名称：

```psql
\d catalogue.movie
```

```
                                                          Table "catalogue.movie"
   Column   |  Type   | Collation | Nullable |                                           Default                                            
------------+---------+-----------+----------+----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('catalogue.movie'::cstring), nextval('catalogue.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
Inherits: catalogue.ag_vertex
```

因此 `ALTER VLABEL movie CLUSTER ON movie_pkey` 会以
`index "movie_pkey" for table "movie" does not exist` 失败；应写的名称是 `film_pkey`。

### 为批量加载关闭标签索引 {#turn-a-labels-indexes-off-for-a-bulk-load}

```cypher
ALTER VLABEL movie DISABLE INDEX;
```

```psql
\d catalogue.movie
```

```
                                                          Table "catalogue.movie"
   Column   |  Type   | Collation | Nullable |                                           Default                                            
------------+---------+-----------+----------+----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('catalogue.movie'::cstring), nextval('catalogue.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id) INVALID
Inherits: catalogue.ag_vertex
```

加载行之后，再重建索引：

```cypher
REINDEX VLABEL movie;
```

```
REINDEX
```

### 在已有行的标签上提升属性 {#promote-a-property-on-a-label-that-already-holds-rows}

```cypher
ALTER VLABEL movie ADD COLUMN year int GENERATED;
```

```psql
\d catalogue.movie
```

```
                                                           Table "catalogue.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('catalogue.movie'::cstring), nextval('catalogue.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
Inherits: catalogue.ag_vertex
```

既有行会被回填，因此语句返回时列已经完整：

```sql
SELECT year FROM catalogue.movie ORDER BY year;
```

```
 year 
------
 2016
 2021
(2 rows)
```

### 查看标签提升了什么 {#look-up-what-a-label-promotes}

`ag_label_property` 把属性键映射到代表它的列：

```cypher
ALTER VLABEL movie ADD COLUMN released text GENERATED (releaseDate);
```

```sql
SELECT p.propname, p.attnum FROM pg_catalog.ag_label_property p
  JOIN pg_catalog.ag_label l ON l.oid = p.laboid
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
 WHERE g.graphname = 'catalogue' AND l.labname = 'movie' ORDER BY p.attnum;
```

```
  propname   | attnum 
-------------+--------
 year        |      3
 releasedate |      4
(2 rows)
```

`attnum` 是列在表中的位置。需要列名时，可以按它再连接 `pg_attribute`。只要使用过显式键形式，二者就可能不同。

### 删除提升列 {#drop-a-promoted-column}

```cypher
ALTER VLABEL movie DROP COLUMN released;
```

映射会随列一起消失：

```sql
SELECT p.propname, p.attnum FROM pg_catalog.ag_label_property p
  JOIN pg_catalog.ag_label l ON l.oid = p.laboid
  JOIN pg_catalog.ag_graph g ON g.oid = l.graphid
 WHERE g.graphname = 'catalogue' AND l.labname = 'movie' ORDER BY p.attnum;
```

```
 propname | attnum 
----------+--------
 year     |      3
(1 row)
```

读取 `releasedate` 会回到属性包；属性包中的内容没有被删除。

### 更改属性映射的存储方式 {#change-how-the-property-map-is-stored}

```cypher
ALTER VLABEL movie SET STORAGE external;
```

无论你原本可能期待哪个列，模式都设置在 `properties` 上：

```sql
SELECT attname, attstorage FROM pg_attribute
 WHERE attrelid = 'catalogue.movie'::regclass AND attnum > 0 AND NOT attisdropped;
```

```
  attname   | attstorage 
------------+------------
 id         | p
 properties | e
 year       | p
(3 rows)
```

### 附加和分离父标签 {#attach-and-detach-a-parent}

```cypher
CREATE VLABEL work;
ALTER VLABEL movie INHERIT work;
```

```psql
\dGv catalogue.movie
```

```
           List of labels
   Graph   | Name  |  Type  | Owner
-----------+-------+--------+-------
 catalogue | movie | vertex | agens
(1 row)

Vertex label "catalogue.movie"
--
Inherits: catalogue.ag_vertex,
          catalogue.work
```

`movie` 现在有两个父标签：创建时的基础标签和 `work`。分离不会影响基础标签：

```cypher
ALTER VLABEL movie NO INHERIT work;
```

```
ALTER VLABEL
```

### 值得识别的拒绝 {#refusals-worth-recognizing}

结构列不能删除：

```cypher
ALTER VLABEL movie DROP COLUMN properties;
```

```
ERROR:  cannot drop column "properties" of graph label "movie"
HINT:  It is a structural column of the graph label.
```

新增列必须由属性包生成：

```cypher
ALTER VLABEL movie ADD COLUMN rank int;
```

```
ERROR:  a non-generated promoted column is not supported yet
HINT:  Use GENERATED to mirror the property from the jsonb bag.
```

已提升的属性不能再次提升：

```cypher
ALTER VLABEL movie ADD COLUMN yr2 int GENERATED (year);
```

```
ERROR:  property "year" is already promoted on graph label "movie"
HINT:  Drop the existing promoted column first, or promote the property to a different column name.
```

基础标签不可使用，无论作为父标签还是目标：

```cypher
ALTER VLABEL movie INHERIT ag_vertex;
```

```
ERROR:  cannot ALTER inheritance with base label
```

```cypher
ALTER VLABEL ag_vertex SET STORAGE main;
```

```
ERROR:  ALTER base vertex label is prohibited
```

每条语句只作用于一种标签：

```cypher
CREATE ELABEL directed;
ALTER VLABEL directed RENAME TO helmed;
```

```
ERROR:  RENAME VLABEL cannot RENAME edge label
```

`RENAME TO` 必须单独使用：

```cypher
ALTER VLABEL movie RENAME TO film, SET STORAGE main;
```

```
ERROR:  syntax error at or near ","
LINE 1: ALTER VLABEL movie RENAME TO film, SET STORAGE main;
                                         ^
```

在 `enable_graph_ddl` 关闭时，用 SQL 重塑标签的表会被拒绝：

```sql
ALTER TABLE catalogue.movie ADD COLUMN rank int;
```

```
ERROR:  cannot add a column to graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

最后删除示例创建的图：

```cypher
DROP GRAPH catalogue CASCADE;
```

## Notes {#notes}

`SET STORAGE` 接受四个关键字，而不是五个。`DEFAULT` 是保留字，在这里是语法错误。要回到标签初始的存储模式，写
`SET STORAGE extended`。无法识别的单词会报告为 `invalid storage type "..."`。

两种形式的 `IF EXISTS` 通知不同：`RENAME TO` 给出
`label "nosuch" does not exist, skipping`，动作列表给出
`graph label "nosuch" does not exist, skipping`。随后二者都报告成功，并且不做任何事。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有修改标签的语句，因为它没有可修改的标签。元素类型属于图类型，而图类型作为整体创建和删除
（`<create graph type statement>`，§12.6）。GQL 中没有与重命名标签、提升属性或关闭索引对应的语句。图类型在
[GQL 一致性矩阵](/zh/agensgraph/appendix/gql-conformance/)中列为计划支持。

### PostgreSQL {#postgresql}

这里的每个动作都是 `ALTER TABLE` 动作，含义也与 PostgreSQL 相同，但有两处调整。`SET STORAGE` 不指定列名。唯一值得选择存储模式的列是 `properties`，因此模式只应用于它。`DISABLE INDEX` 完全没有 `ALTER TABLE` 对应动作：它把标签索引标记为无效；除此之外，SQL 只能通过中断 `CREATE INDEX CONCURRENTLY` 达到这一状态。

反过来说，除非开启 `enable_graph_ddl`，对标签表的 `ALTER TABLE` 在会重塑表的动作上会被拒绝。添加、删除或更改列类型都属于这类动作；上面的示例展示了拒绝。本页动作从不需要该设置，因为它们会自行更新图目录。

## See also {#see-also}

- [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)
- [`CREATE ELABEL`](/zh/agensgraph/reference/ddl/create-elabel/)
- [`DROP VLABEL` 与 `DROP ELABEL`](/zh/agensgraph/reference/ddl/drop-label/)
- [`REINDEX VLABEL` 与 `REINDEX ELABEL`](/zh/agensgraph/reference/ddl/reindex/)
- [把属性提升为列](/zh/agensgraph/querying/typed-columns/)
- [标签继承](/zh/agensgraph/concepts/label-inheritance/)
