---
title: REINDEX VLABEL 与 REINDEX ELABEL
linkTitle: REINDEX VLABEL 与 REINDEX ELABEL
description: 重建标签上的所有索引；被禁用索引的标签也通过它恢复索引。
type: docs
weight: 90
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/reindex.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


重建标签上的所有索引；被禁用索引的标签也通过它恢复索引。

## Synopsis {#synopsis}

```text
REINDEX [ ( option [, ... ] ) ] VLABEL label_nameREINDEX [ ( option [, ... ] ) ] ELABEL label_namewhere option is one of:    CONCURRENTLY [ boolean ]    TABLESPACE new_tablespace    VERBOSE [ boolean ]
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

`REINDEX VLABEL` 重建顶点标签上的所有索引，`REINDEX ELABEL` 重建边标签上的所有索引。这包括标签自身的索引、其上的每个属性索引，以及 TOAST 关系上的索引。重建会把无效索引重新标记为有效，因此本语句是 `DISABLE INDEX` 的对应恢复语句。

没有 `ENABLE INDEX`。“先加载后构建”的顺序是 `ALTER VLABEL <label> DISABLE INDEX`，然后加载，最后 `REINDEX VLABEL <label>`。

- 标签在 `graph_path` 指定的图中查找。名称**不能带限定名**：`REINDEX VLABEL rebuildme.movie` 是语法错误。
- 每条语句只接受一种标签。对边标签执行 `REINDEX VLABEL` 会以 `REINDEX VLABEL cannot REINDEX edge label` 失败；反过来会得到对应消息。
- 选项写在标签关键字之前的圆括号中。这里的 `REINDEX VLABEL CONCURRENTLY movie` 是语法错误，但 `REINDEX TABLE` 接受这种裸关键字拼法。
- 不存在旧拼法 `REINDEX LABEL`。它会在 `LABEL` 处报语法错误。

## Parameters {#parameters}

option
: `CONCURRENTLY`、`TABLESPACE` 或 `VERBOSE`，放在圆括号中并用逗号分隔。含义与 `REINDEX` 相同：构建时不锁住写入、把重建后的索引移动到其他表空间，以及在每个索引完成时报告它。`CONCURRENTLY` 和 `VERBOSE` 还接受显式布尔值，因此 `(VERBOSE false)` 等同于省略 `VERBOSE`。

label_name
: 要重建索引的标签，位于 `graph_path` 指定的图中。

## Examples {#examples}

这些示例创建自己的图 `rebuildme`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH rebuildme;
SET graph_path = rebuildme;
CREATE VLABEL movie;
CREATE ELABEL directed;
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
CREATE (:movie {title: 'Arrival'});
```

### 批量加载后构建标签索引 {#build-a-labels-indexes-after-a-bulk-load}

关闭索引会保留它们但使其无效，因此加载过程不会维护索引：

```cypher
ALTER VLABEL movie DISABLE INDEX;
```

```psql
\d rebuildme.movie
```

```
                                                           Table "rebuildme.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('rebuildme.movie'::cstring), nextval('rebuildme.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id) INVALID
    "movie_title_idx" btree ((properties.'title')) INVALID
Inherits: rebuildme.ag_vertex
```

标签的主键和属性索引都会标记为 `INVALID`。一条语句即可构建二者：

```cypher
REINDEX VLABEL movie;
```

```
REINDEX
```

```psql
\d rebuildme.movie
```

```
                                                           Table "rebuildme.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('rebuildme.movie'::cstring), nextval('rebuildme.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_title_idx" btree ((properties.'title'))
Inherits: rebuildme.ag_vertex
```

### 观察每个索引的重建过程 {#watch-each-index-as-it-is-rebuilt}

```cypher
ALTER ELABEL directed DISABLE INDEX;
REINDEX (VERBOSE) ELABEL directed;
```

```
INFO:  index "pg_toast_60285_index" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
INFO:  index "directed_id_idx" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
INFO:  index "directed_start_idx" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
INFO:  index "directed_end_idx" was reindexed
DETAIL:  CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
REINDEX
```

边标签的三个索引都会被重建，持有超大属性映射的 TOAST 关系上的索引也会被重建。TOAST 索引名包含表的 OID，因此每次运行都会不同。

### 重建时不锁住写入 {#rebuild-without-locking-writes-out}

```cypher
REINDEX (CONCURRENTLY) VLABEL movie;
```

```
REINDEX
```

```cypher
REINDEX (TABLESPACE pg_default) VLABEL movie;
```

```
REINDEX
```

### 值得识别的拒绝情况 {#refusals-worth-recognizing}

每条语句只接受一种标签：

```cypher
REINDEX VLABEL directed;
```

```
ERROR:  REINDEX VLABEL cannot REINDEX edge label
```

```cypher
REINDEX ELABEL movie;
```

```
ERROR:  REINDEX ELABEL cannot REINDEX vertex label
```

没有 `REINDEX LABEL`：

```cypher
REINDEX LABEL movie;
```

```
ERROR:  syntax error at or near "LABEL"
LINE 1: REINDEX LABEL movie;
                ^
```

名称不能携带图名：

```cypher
REINDEX VLABEL rebuildme.movie;
```

```
ERROR:  syntax error at or near "."
LINE 1: REINDEX VLABEL rebuildme.movie;
                                ^
```

`CONCURRENTLY` 必须放在圆括号内：

```cypher
REINDEX VLABEL CONCURRENTLY movie;
```

```
ERROR:  syntax error at or near "CONCURRENTLY"
LINE 1: REINDEX VLABEL CONCURRENTLY movie;
                       ^
```

不存在的标签会以限定名报告，因为 `graph_path` 已经应用在它上面：

```cypher
REINDEX VLABEL nosuch;
```

```
ERROR:  relation "rebuildme.nosuch" does not exist
```

最后删除示例创建的图：

```cypher
DROP GRAPH rebuildme CASCADE;
```

## Notes {#notes}

对标签表执行 `REINDEX TABLE` 能完成同样工作，而且不需要设置，因此 `REINDEX TABLE rebuildme.movie` 也能恢复被禁用标签的索引。尽管如此，仍优先使用标签拼法。它们会检查标签是否属于你指定的类型，并且接受在 `graph_path` 中解析的名称，而不是模式限定名。

对图的模式执行 `REINDEX SCHEMA` 会重建图中所有索引，`REINDEX INDEX` 按名称重建单个索引。二者都是普通 SQL 语句，没有标签感知形式。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有索引 DDL，也没有重建索引的语句。它修改目录的语句仅限于模式、图和图类型（§12），因此这两种拼法是 AgensGraph 自有扩展。

### PostgreSQL {#postgresql}

`REINDEX VLABEL` 和 `REINDEX ELABEL` 是带标签感知目标的 `REINDEX TABLE`。选项就是 `REINDEX` 自身的选项，含义相同。两处拼法差别重要：目标名称在 `graph_path` 中解析，不能带模式限定名；`CONCURRENTLY` 只能作为圆括号中的选项，绝不能作为标签关键字后的裸关键字。

## See also {#see-also}

- [`ALTER VLABEL` 与 `ALTER ELABEL`](/zh/agensgraph/reference/ddl/alter-label/)
- [`CREATE PROPERTY INDEX`](/zh/agensgraph/reference/ddl/create-property-index/)
- [`DROP PROPERTY INDEX`](/zh/agensgraph/reference/ddl/drop-property-index/)
- [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)
