---
title: CREATE CONSTRAINT
linkTitle: CREATE CONSTRAINT
description: 要求标签的属性唯一，或要求标签中的每个元素满足一个条件。
type: docs
weight: 100
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-constraint.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


要求标签的属性唯一，或要求标签中的每个元素满足一个条件。

## Synopsis {#synopsis}

```text
CREATE CONSTRAINT [ constraint_name ] ON label_name ASSERT property IS UNIQUECREATE CONSTRAINT [ constraint_name ] ON label_name ASSERT condition
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

有两种形式，它们在磁盘上会变成两种不同的对象。

**`ASSERT property IS UNIQUE`** 会变成基于属性读取的排除约束：`EXCLUDE USING btree ((properties.'title') WITH =)`。值已存在的写入会作为冲突被拒绝。

**`ASSERT condition`** 会变成基于同类读取的检查约束：`CHECK ((properties.'age')::integer > 9)`。行使条件不满足的写入会被拒绝。

**两种形式的名称都可省略。** 省略时会派生名称：唯一形式用 `<label>_unique_constraint`，检查形式用 `<label>_properties_check`。若名称已被占用，会追加数字后缀。手动指定的名称必须在图的模式中未占用，因为唯一形式会创建同名索引。

其他规则：

- 标签在 `graph_path` 指定的图中查找；标签名不能带限定名。
- 两种形式都可用于顶点标签和边标签。
- `CREATE OR REPLACE CONSTRAINT` 能被解析，但会以 `CREATE OR REPLACE CONSTRAINT is not supported` 被拒绝。要修改约束，先删除再重新创建。
- 约束会作用于标签中已有的行，因此已有违反约束的行会让语句失败。
- 检查约束就是 SQL 检查约束，所以**缺失的属性满足约束。** 条件对缺失属性求值为 unknown，而检查约束接受 unknown。用约束限制值，不要用它要求键必须存在。

[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)在一屏内说明了磁盘映射。

## Parameters {#parameters}

constraint_name
: 约束名。可选；省略时按标签和形式派生。唯一形式的名称还命名索引，因此不能与图中已有关系冲突。

label_name
: 约束适用的标签，位于 `graph_path` 指定的图中。

property
: 必须唯一的属性，按 Cypher 的写法书写：`title`，或嵌套映射内键的 `name.first`。

condition
: 基于标签属性的 Cypher 条件。每个写入元素求值一次。

## Examples {#examples}

这些示例创建自己的图 `constrain`，不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH constrain;
SET graph_path = constrain;
CREATE VLABEL film;
CREATE ELABEL rated;
```

### 要求属性唯一 {#require-a-property-to-be-unique}

```cypher
CREATE CONSTRAINT film_title_uniq ON film ASSERT title IS UNIQUE;
```

```
CREATE CONSTRAINT
```

它生成了基于属性读取的排除约束：

```psql
\d constrain.film
```

```
                                                          Table "constrain.film"
   Column   |  Type   | Collation | Nullable |                                           Default                                           
------------+---------+-----------+----------+---------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('constrain.film'::cstring), nextval('constrain.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
    "film_title_uniq" EXCLUDE USING btree ((properties.'title') WITH =)
Inherits: constrain.ag_vertex
```

第一次写入成功：

```cypher
CREATE (:film {title: 'Arrival', year: 2016});
```

```
UPDATE 1
```

第二次写入被拒绝，消息指出约束和值：

```cypher
CREATE (:film {title: 'Arrival', year: 2021});
```

```
ERROR:  conflicting key value violates exclusion constraint "film_title_uniq"
DETAIL:  Key ((properties.'title'))=("Arrival") conflicts with existing key ((properties.'title'))=("Arrival").
```

### 省略约束名 {#leave-the-constraint-unnamed}

```cypher
CREATE CONSTRAINT ON film ASSERT year IS UNIQUE;
```

`\dGv` 用书写约束时的形式显示两个约束，以及第二个约束的派生名：

```psql
\dGv constrain.film
```

```
          List of labels
   Graph   | Name |  Type  | Owner
-----------+------+--------+-------
 constrain | film | vertex | agens
(1 row)

Vertex label "constrain.film"
--
Constraints:
    "film_title_uniq" ASSERT (title) IS UNIQUE
    "film_unique_constraint" ASSERT (year) IS UNIQUE
Inherits: constrain.ag_vertex
```

### 限制属性可以持有的值 {#restrict-what-a-property-may-hold}

```cypher
CREATE VLABEL teen;
CREATE CONSTRAINT teen_age ON teen ASSERT (10 <= age::int AND age::int <= 19);
```

```psql
\d constrain.teen
```

```
                                                          Table "constrain.teen"
   Column   |  Type   | Collation | Nullable |                                           Default                                           
------------+---------+-----------+----------+---------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('constrain.teen'::cstring), nextval('constrain.teen_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "teen_pkey" PRIMARY KEY, btree (id)
Check constraints:
    "teen_age" CHECK (10 <= ((properties.'age')::integer) AND ((properties.'age')::integer) <= 19)
Inherits: constrain.ag_vertex
```

范围内的行会写入：

```cypher
CREATE (:teen {name: 'Kim', age: 15});
```

```
UPDATE 1
```

范围外的行不会写入：

```cypher
CREATE (:teen {name: 'Lee', age: 20});
```

```
ERROR:  new row for relation "teen" violates check constraint "teen_age"
DETAIL:  Failing row contains (5.2, {"age": 20, "name": "Lee"}).
```

完全没有 `age` 的顶点会被接受，因为条件结果是 unknown 而不是 false：

```cypher
CREATE (:teen {name: 'Bo'});
MATCH (t:teen) RETURN t.name AS name, t.age AS age ORDER BY name;
```

```
 name  | age 
-------+-----
 "Bo"  | 
 "Kim" | 15
(2 rows)
```

### 不加转换进行比较 {#compare-without-a-cast}

对原始属性直接写比较时，比较的是 `jsonb` 值而不是整数：

```cypher
CREATE CONSTRAINT ON teen ASSERT age > 9;
```

```psql
\dGv constrain.teen
```

```
          List of labels
   Graph   | Name |  Type  | Owner
-----------+------+--------+-------
 constrain | teen | vertex | agens
(1 row)

Vertex label "constrain.teen"
--
Constraints:
    "teen_age" ASSERT (10 <= ((age)::integer) AND ((age)::integer) <= 19)
    "teen_properties_check" ASSERT ((age) > cypher_to_jsonb(9))
Inherits: constrain.ag_vertex
```

两种形式都会拒绝 `{age: 'twelve'}`，但报告方式不同。转换形式会抛出 `invalid input syntax for type integer: "twelve"`。未转换形式会报告违反检查约束。如果既想强制属性类型又想限制范围，请使用转换。

### 约束边标签 {#constrain-an-edge-label}

```cypher
CREATE CONSTRAINT rated_pair ON rated ASSERT source IS UNIQUE;
```

```psql
\d constrain.rated
```

```
                                                           Table "constrain.rated"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('constrain.rated'::cstring), nextval('constrain.rated_id_seq'::regclass))
 start      | graphid |           | not null | 
 end        | graphid |           | not null | 
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "rated_end_idx" btree ("end", start)
    "rated_id_idx" brin (id)
    "rated_pair" EXCLUDE USING btree ((properties.'source') WITH =)
    "rated_start_idx" btree (start, "end")
Inherits: constrain.ag_edge
```

约束位于标签的三个普通索引旁边。

### 向已有行的标签添加约束 {#add-a-constraint-to-a-label-that-already-has-rows}

约束会检查现有内容，因此不能在违反它的行上创建。两种形式的报告方式不同：

```cypher
CREATE VLABEL rerun;
CREATE (:rerun {title: 'Arrival'}), (:rerun {title: 'Arrival'});
CREATE CONSTRAINT rerun_t ON rerun ASSERT title IS UNIQUE;
```

```
ERROR:  could not create exclusion constraint "rerun_t"
DETAIL:  Key ((properties.'title'))=("Arrival") conflicts with key ((properties.'title'))=("Arrival").
```

```cypher
CREATE VLABEL adult;
CREATE (:adult {age: 40});
CREATE CONSTRAINT adult_a ON adult ASSERT (age::int < 20);
```

```
ERROR:  check constraint "adult_a" of relation "adult" is violated by some row
```

### 值得识别的拒绝情况 {#refusals-worth-recognizing}

没有替换形式：

```cypher
CREATE OR REPLACE CONSTRAINT film_title_uniq ON film ASSERT title IS UNIQUE;
```

```
ERROR:  CREATE OR REPLACE CONSTRAINT is not supported
```

唯一约束的名称就是索引名，因此会与索引冲突：

```cypher
CREATE CONSTRAINT film_title_uniq ON film ASSERT year IS UNIQUE;
```

```
ERROR:  relation "film_title_uniq" already exists
```

标签必须已经存在。Cypher 在这里不会像 `CREATE (:film)` 那样按需创建标签：

```cypher
CREATE CONSTRAINT c ON nosuch ASSERT a IS UNIQUE;
```

```
ERROR:  label "nosuch" does not exist
```

最后删除示例创建的图：

```cypher
DROP GRAPH constrain CASCADE;
```

## Notes {#notes}

唯一约束是排除约束，不是唯一索引，因此不能与 `CREATE UNIQUE PROPERTY INDEX` 互换。二者都会拒绝重复值。错误不同：`conflicting key value violates exclusion constraint` 对 `duplicate key value violates unique constraint`。`\dGv` 的报告不同。删除语句也不同：约束用 [`DROP CONSTRAINT`](/zh/agensgraph/reference/ddl/drop-constraint/) 删除，唯一索引用 [`DROP PROPERTY INDEX`](/zh/agensgraph/reference/ddl/drop-property-index/) 删除。

两种形式在[标签继承](/zh/agensgraph/concepts/label-inheritance/)上的行为不同，这个差别容易让人意外。检查约束会被继承：之后创建的子标签携带该约束并受它检查。唯一约束不会被继承。子标签不会获得排除约束，因此同一个值可以通过父标签写入一次，再通过子标签写入一次。对父标签执行 `MATCH` 会返回两行。

> [!NOTE]
> 要让属性在整个层级中唯一，可为层级中的每个标签分别创建约束。没有任何机制能让一个值跨多个标签唯一；约束与其背后的索引一样，只覆盖一张表。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有约束 DDL。它用图类型（`<create graph type statement>`，§12.6）约束图，声明图元素可以有哪些标签和属性。图类型没有逐属性唯一规则，也没有检查条件。而且只有引用图类型的图才会受到约束。AgensGraph 的图是开放图，因此 `CREATE CONSTRAINT` 是其自有扩展。图类型在 [GQL 一致性矩阵](/zh/agensgraph/appendix/gql-conformance/)中记录为规划项。

### PostgreSQL {#postgresql}

检查形式对应 `ALTER TABLE ... ADD CONSTRAINT ... CHECK`，唯一形式对应 `ALTER TABLE ... ADD CONSTRAINT ... EXCLUDE USING btree (... WITH =)`。它不对应 `UNIQUE`，因为 `UNIQUE` 不能建立在表达式上。条件是 Cypher 表达式而不是 SQL 表达式，因此 `age` 指属性而不是列。`ADD CONSTRAINT` 提供的 `NOT NULL`、`PRIMARY KEY`、`FOREIGN KEY`、`DEFERRABLE` 和 `NOT VALID` 在这里没有对应拼法。

## See also {#see-also}

- [`DROP CONSTRAINT`](/zh/agensgraph/reference/ddl/drop-constraint/)
- [`CREATE PROPERTY INDEX`](/zh/agensgraph/reference/ddl/create-property-index/)
- [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
