---
title: DROP PROPERTY INDEX
linkTitle: DROP PROPERTY INDEX
description: 删除属性索引。
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-property-index.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


删除属性索引。

## Synopsis {#synopsis}

```text
DROP PROPERTY INDEX [ IF EXISTS ] index_name [, ... ] [ CASCADE | RESTRICT ]
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

`DROP PROPERTY INDEX` 只删除由 [`CREATE PROPERTY INDEX`](/zh/agensgraph/reference/ddl/create-property-index/) 创建的一个或多个索引，不删除其他对象。

- 名称在 `graph_path` 指定的图中解析，并且**不能带限定名**。带模式名的名称会以 `improper property index name` 被拒绝。要删除其他图中的索引，先更改 `graph_path`。
- 只接受属性索引。标签上的其他索引会以 `"<name>" is not property index` 被拒绝，包括主键、边标签的端点索引，以及用 SQL 创建的索引。
- 相比之下，`DROP INDEX` 接受标签上的任何索引，也包括属性索引；因此任一语句创建的索引都可以用任一语句删除。
- 属于约束的索引会随约束一起由 [`DROP CONSTRAINT`](/zh/agensgraph/reference/ddl/drop-constraint/) 删除。

## Parameters {#parameters}

IF EXISTS
: 对不存在的索引发出通知而不是错误。同一语句中的其他名称仍会被删除。

index_name
: 要删除的属性索引的非限定名。可以给出多个名称，并用逗号分隔；它们不必属于同一个标签。

CASCADE
: 删除依赖该索引的对象。

RESTRICT
: 有任何对象依赖该索引时拒绝删除。这是默认行为。索引很少拥有依赖对象，因此二者多数时候表现相同。

## Examples {#examples}

这些示例创建自己的图 `unindexed`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH unindexed;
SET graph_path = unindexed;
CREATE VLABEL movie;
CREATE VLABEL person;
CREATE (:movie {title: 'Arrival', year: 2016}), (:person {name: 'Denis Villeneuve'});
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
CREATE PROPERTY INDEX movie_year_idx ON movie (year);
CREATE PROPERTY INDEX person_name_idx ON person (name);
```

```psql
\dGi unindexed.*
```

```
                                                   List of property indexes
   Graph   | LabelName |    IndexName    | Unique | Owner |                              Indexdef
-----------+-----------+-----------------+--------+-------+--------------------------------------------------------------------
 unindexed | movie     | movie_title_idx | f      | agens | CREATE PROPERTY INDEX movie_title_idx ON movie USING btree (title)
 unindexed | movie     | movie_year_idx  | f      | agens | CREATE PROPERTY INDEX movie_year_idx ON movie USING btree (year)
 unindexed | person    | person_name_idx | f      | agens | CREATE PROPERTY INDEX person_name_idx ON person USING btree (name)
(3 rows)
```

### 删除一个索引 {#drop-one-index}

```cypher
DROP PROPERTY INDEX movie_title_idx;
```

```
DROP PROPERTY INDEX
```

第二次尝试会报错，因为索引已经不存在：

```cypher
DROP PROPERTY INDEX movie_title_idx;
```

```
ERROR:  index "movie_title_idx" does not exist
```

`IF EXISTS` 会把它变成通知：

```cypher
DROP PROPERTY INDEX IF EXISTS movie_title_idx;
```

```
NOTICE:  index "movie_title_idx" does not exist, skipping
DROP PROPERTY INDEX
```

### 一次删除多个索引 {#drop-several-indexes-at-once}

这些名称不必属于同一个标签：

```cypher
DROP PROPERTY INDEX movie_year_idx, person_name_idx;
```

```
DROP PROPERTY INDEX
```

```psql
\dGi unindexed.*
```

```
No matching property indexes found.
```

### 值得识别的拒绝情况 {#refusals-worth-recognizing}

名称不能携带图名：

```cypher
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
DROP PROPERTY INDEX unindexed.movie_title_idx;
```

```
ERROR:  improper property index name
```

不属于本语句管辖的索引会被拒绝。标签的主键就是一种：

```cypher
DROP PROPERTY INDEX movie_pkey;
```

```
ERROR:  "movie_pkey" is not property index
```

`DROP INDEX` 也可以通过模式限定名删除属性索引：

```sql
DROP INDEX unindexed.movie_title_idx;
```

```
DROP INDEX
```

最后删除示例创建的图：

```cypher
DROP GRAPH unindexed CASCADE;
```

## Notes {#notes}

因为名称是在 `graph_path` 中解析的，另一个图中存在的索引会被视为缺失，而不是属于其他人：

```cypher
CREATE GRAPH oneplace;
SET graph_path = oneplace;
CREATE VLABEL movie;
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
CREATE GRAPH otherplace;
SET graph_path = otherplace;
DROP PROPERTY INDEX movie_title_idx;
```

```
ERROR:  index "movie_title_idx" does not exist
```

两个图可以持有同名索引，因此在假定裸名称会命中哪一个之前，先检查 `\dGi`。

```cypher
DROP GRAPH oneplace CASCADE;
DROP GRAPH otherplace CASCADE;
```

要在批量加载等场景中关闭标签索引而不删除它们，可改用 `ALTER VLABEL ... DISABLE INDEX` 和 [`REINDEX VLABEL`](/zh/agensgraph/reference/ddl/reindex/)。这会保留定义，只使其失效。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有索引 DDL。它修改目录的语句仅限于模式、图和图类型（§12），因此 `DROP PROPERTY INDEX` 是 AgensGraph 自有扩展。

### PostgreSQL {#postgresql}

`DROP PROPERTY INDEX` 对应 `DROP INDEX`，`IF EXISTS`、名称列表和 `CASCADE`/`RESTRICT` 的行为也与 PostgreSQL 相同。差别有三点。名称在 `graph_path` 而不是 `search_path` 中解析，且不能带模式限定名。不接受 `CONCURRENTLY`。两条语句严格分区：各自拒绝对方的索引，因此属性索引只能由本语句删除。

## See also {#see-also}

- [`CREATE PROPERTY INDEX`](/zh/agensgraph/reference/ddl/create-property-index/)
- [`REINDEX VLABEL` 与 `REINDEX ELABEL`](/zh/agensgraph/reference/ddl/reindex/)
- [`DROP CONSTRAINT`](/zh/agensgraph/reference/ddl/drop-constraint/)
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
