---
title: DROP CONSTRAINT
linkTitle: DROP CONSTRAINT
description: 从标签删除约束。
type: docs
weight: 110
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/drop-constraint.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


从标签删除约束。

## Synopsis {#synopsis}

```text
DROP CONSTRAINT constraint_name ON label_name
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

`DROP CONSTRAINT` 从一个标签删除一个约束。它接受 [`CREATE CONSTRAINT`](/zh/agensgraph/reference/ddl/create-constraint/) 创建的两种形式：`IS UNIQUE` 背后的排除约束，以及条件背后的检查约束。它还会删除唯一约束拥有的索引。

这条语句刻意保持很小。以下是它没有的能力：

- **必须给出名称。** 无法表示“删除该属性上的任何约束”。
- **没有 `IF EXISTS`。** `DROP CONSTRAINT IF EXISTS ...` 是语法错误，因此不存在的约束总是报错。
- **没有 `CASCADE` 或 `RESTRICT`，也没有名称列表。**
- 约束名不能带限定名，标签名也不能。标签在 `graph_path` 指定的图中查找。
- 它能作用于标签表上的任何具名约束，而不仅是 Cypher 创建的约束。标签的主键就是其中之一。运行前先核对名称。
- 属性索引不是约束。删除属性索引用 [`DROP PROPERTY INDEX`](/zh/agensgraph/reference/ddl/drop-property-index/)。

## Parameters {#parameters}

constraint_name
: 要删除的约束名。必须是非限定名。`\dGv`、`\dGe` 和 `\d` 都会报告它；`pg_constraint` 也会。

label_name
: 约束所在的标签，位于 `graph_path` 指定的图中。

## Examples {#examples}

这些示例创建自己的图 `rulebooks`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH rulebooks;
SET graph_path = rulebooks;
CREATE VLABEL film;
CREATE CONSTRAINT film_title_uniq ON film ASSERT title IS UNIQUE;
CREATE CONSTRAINT ON film ASSERT year IS UNIQUE;
CREATE VLABEL teen;
CREATE CONSTRAINT teen_age ON teen ASSERT (10 <= age::int AND age::int <= 19);
CREATE CONSTRAINT ON teen ASSERT age > 9;
```

### 删除唯一约束 {#drop-a-unique-constraint}

```cypher
DROP CONSTRAINT film_title_uniq ON film;
```

```
DROP CONSTRAINT
```

约束及其索引都不见了；随后创建的未命名约束仍在：

```psql
\d rulebooks.film
```

```
                                                          Table "rulebooks.film"
   Column   |  Type   | Collation | Nullable |                                           Default                                           
------------+---------+-----------+----------+---------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('rulebooks.film'::cstring), nextval('rulebooks.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
    "film_unique_constraint" EXCLUDE USING btree ((properties.'year') WITH =)
Inherits: rulebooks.ag_vertex
```

第二次运行会报错，因为没有 `IF EXISTS` 可以缓和：

```cypher
DROP CONSTRAINT film_title_uniq ON film;
```

```
ERROR:  constraint "film_title_uniq" of relation "film" does not exist
```

```cypher
DROP CONSTRAINT IF EXISTS film_title_uniq ON film;
```

```
ERROR:  syntax error at or near "EXISTS"
LINE 1: DROP CONSTRAINT IF EXISTS film_title_uniq ON film;
                           ^
```

### 查找未命名约束的名称 {#find-the-name-of-a-constraint-you-did-not-name}

未命名约束会有派生名称。`pg_constraint` 列出标签表上的所有约束：

```sql
SELECT conname FROM pg_constraint WHERE conrelid = 'rulebooks.teen'::regclass ORDER BY conname;
```

```
         conname          
--------------------------
 teen_age
 teen_id_not_null
 teen_pkey
 teen_properties_check
 teen_properties_not_null
(5 rows)
```

`teen_age` 是具名检查约束，`teen_properties_check` 是派生名称。其余三个属于标签自身结构。

### 删除检查约束 {#drop-a-check-constraint}

```cypher
DROP CONSTRAINT teen_properties_check ON teen;
DROP CONSTRAINT teen_age ON teen;
```

二者都已删除；`\dGv` 没有约束可报告：

```psql
\dGv rulebooks.teen
```

```
          List of labels
   Graph   | Name |  Type  | Owner
-----------+------+--------+-------
 rulebooks | teen | vertex | agens
(1 row)

Vertex label "rulebooks.teen"
--
Inherits: rulebooks.ag_vertex
```

### 值得识别的拒绝情况 {#refusals-worth-recognizing}

属性索引不是约束，无论它叫什么名字：

```cypher
CREATE PROPERTY INDEX film_year_idx ON film (year);
DROP CONSTRAINT film_year_idx ON film;
```

```
ERROR:  constraint "film_year_idx" of relation "film" does not exist
```

名称不能携带图名：

```cypher
DROP CONSTRAINT rulebooks.film_unique_constraint ON film;
```

```
ERROR:  syntax error at or near "."
LINE 1: DROP CONSTRAINT rulebooks.film_unique_constraint ON film;
                                 ^
```

最后删除示例创建的图：

```cypher
DROP GRAPH rulebooks CASCADE;
```

## Notes {#notes}

> [!WARNING]
> `DROP CONSTRAINT` 能作用于标签表上的任何具名约束，标签的主键就是其中之一。`DROP CONSTRAINT film_pkey ON film` 会成功，并使标签的 `id` 主键消失；没有任何语句能把它恢复。先用 `\dGv` 或 `pg_constraint` 核对名称，并只使用 [`CREATE CONSTRAINT`](/zh/agensgraph/reference/ddl/create-constraint/) 生成的名称。

要修改约束，先删除再重新创建；`CREATE OR REPLACE CONSTRAINT` 会被拒绝。

子标签继承的检查约束只能从声明它的标签删除：

```cypher
CREATE GRAPH hierarchy;
SET graph_path = hierarchy;
CREATE VLABEL work;
CREATE CONSTRAINT work_y ON work ASSERT (year::int > 1900);
CREATE VLABEL feature INHERITS (work);
```

指定子标签会被拒绝：

```cypher
DROP CONSTRAINT work_y ON feature;
```

```
ERROR:  cannot drop inherited constraint "work_y" of relation "feature"
```

从父标签删除会把它从整个标签家族移除：

```cypher
DROP CONSTRAINT work_y ON work;
DROP GRAPH hierarchy CASCADE;
```

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有约束 DDL，因此没有语句与本页对应。它约束图的方式是图类型，由 `<drop graph type statement>`（§12.7）整体删除。图类型在 [GQL 一致性矩阵](/zh/agensgraph/appendix/gql-conformance/)中记录为规划项。

### PostgreSQL {#postgresql}

`DROP CONSTRAINT ... ON <label>` 对应 `ALTER TABLE <table> DROP CONSTRAINT <name>`，只是标签名放在约束名之后。它提供的能力更少：没有 `IF EXISTS`，没有 `CASCADE`/`RESTRICT`，也无法在一条语句中删除多个约束。但作用范围一样大：标签表上的任何具名约束，与 `ALTER TABLE` 能到达的集合相同。

## See also {#see-also}

- [`CREATE CONSTRAINT`](/zh/agensgraph/reference/ddl/create-constraint/)
- [`DROP PROPERTY INDEX`](/zh/agensgraph/reference/ddl/drop-property-index/)
- [`ALTER VLABEL` 与 `ALTER ELABEL`](/zh/agensgraph/reference/ddl/alter-label/)
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
