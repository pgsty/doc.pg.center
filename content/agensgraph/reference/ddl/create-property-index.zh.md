---
title: CREATE PROPERTY INDEX
linkTitle: CREATE PROPERTY INDEX
description: 在标签的一个或多个属性上创建索引。
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/ddl/create-property-index.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


在标签的一个或多个属性上创建索引。

## Synopsis {#synopsis}

```text
CREATE [ UNIQUE ] PROPERTY INDEX [ CONCURRENTLY ] [ [ IF NOT EXISTS ] index_name ]    ON [ ONLY ] label_name [ USING method ]    ( { property | ( expression ) } [ COLLATE collation ] [ opclass ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ... ] )    [ NULLS [ NOT ] DISTINCT ]    [ WITH ( storage_parameter [= value] [, ... ] ) ]    [ TABLESPACE tablespace_name ]    [ WHERE condition ]
```

**记法**：大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## Description {#description}

这条语句背后没有单独一类索引。属性索引是普通的 PostgreSQL 索引，建立在一个从标签的 `jsonb` 属性包中读出属性的表达式上。`CREATE PROPERTY INDEX ON movie (title)` 会创建键为 `(properties.'title')` 的 B-tree。`\d` 也是这样报告它；规划器必须能以该形式看到谓词，才能使用这个索引。

这个表达式决定了语句的全部限制：

- **被索引值的类型是 `jsonb`，**因此访问方法必须有适用于 `jsonb` 的默认操作符类。`btree`（默认）、`hash` 和 `gin` 有；`gist`、`spgist` 和 `brin` 没有。请求后一类访问方法会失败，错误为
  `data type jsonb has no default operator class for access method "gist"`。
- **不能对它应用排序规则。**`jsonb` 不携带排序规则，因此对属性包读取使用 `COLLATE` 会失败，错误为
  `collations are not supported by type jsonb`。
- **这个值永远不能作为 included column。**`INCLUDE` 会以
  `expressions are not supported in included columns` 被拒绝；属性读取总是表达式，所以 `INCLUDE` 不适用于属性。

对**提升后**属性的索引不同，因为被索引的值这时是列而不是表达式。`\d` 报告的是 `btree (year)`，而不是 `btree ((properties.'year'))`。访问方法、操作符类和排序规则只受列自身类型的限制，因此 `int` 列上的 `brin (year)` 和 `text` 列上的 `btree (name COLLATE "C")` 都可用。[把属性提升为列](/zh/agensgraph/querying/typed-columns/)介绍了何时应该提升。

另有三条规则：

- 标签在 `graph_path` 指定的图中查找；标签名不能带限定名。
- 父标签上的索引只覆盖该标签自身的行。无论是否使用 `ONLY`，子标签都不会被索引。参见[标签继承](/zh/agensgraph/concepts/label-inheritance/#what-it-costs)。
- `IF NOT EXISTS` 需要一个可检查的名称，因此不能与未命名索引组合。

## Parameters {#parameters}

UNIQUE
: 拒绝被索引值与既有行重复的行，并在创建索引时检查已存在的行。要用 Cypher 自身的概念表达唯一性规则，参见[`CREATE CONSTRAINT`](/zh/agensgraph/reference/ddl/create-constraint/)。

CONCURRENTLY
: 创建索引时不阻止对标签的写入，代价是构建时间更长并需要两次表扫描。

IF NOT EXISTS index_name
: 同名关系已存在时发出通知而不是错误。不会创建任何内容，也不会检查既有索引是否就是你要创建的索引。

index_name
: 索引名。省略时，名称由标签和被索引属性派生：`movie` 和 `year` 得到 `movie_year_idx`。

ONLY
: 被接受，但对普通标签没有效果。它会抑制对分区的递归，而标签是继承父表，不是分区表。

label_name
: 被索引的标签，位于 `graph_path` 指定的图中。

USING method
: 索引访问方法。对从属性包读取的属性，可选 `btree`（默认）、`hash` 或 `gin`。对提升列，可选任何对该列类型有默认操作符类的方法。

property
: 标签的属性，按 Cypher 的写法书写：`title`，或嵌套映射内键的 `name.first`。

( expression )
: 括起来的、基于标签属性的 Cypher 表达式，例如 `(year / 10)`。

COLLATE collation
: 被索引值的排序规则。只有当该值是可排序类型的提升列时才能使用。

opclass
: 被索引值的操作符类，例如 `gin` 索引的 `jsonb_path_ops`。不接受操作符类*参数*。

ASC | DESC | NULLS FIRST | NULLS LAST
: 索引中保存的排序顺序。`ASC` 和 `NULLS LAST` 是默认值；在 `DESC` 下，默认值是 `NULLS FIRST`。

NULLS [ NOT ] DISTINCT
: 对唯一索引，指定两个 null 是否算作不同值。默认的 `NULLS DISTINCT` 允许索引保存多个 null。

WITH ( storage_parameter [= value] [, ...] )
: 索引的存储参数，例如 btree 的 `fillfactor` 或 gin 的 `fastupdate`。

TABLESPACE tablespace_name
: 索引的表空间。未指定时由 `default_tablespace` 决定。

WHERE condition
: 创建部分索引，只覆盖满足条件的行。

## Examples {#examples}

这些示例自建 `indexdemo` 图，而不是使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，并在最后删除它。

```cypher
CREATE GRAPH indexdemo;
SET graph_path = indexdemo;
CREATE VLABEL movie;
CREATE VLABEL person;
CREATE (:movie {title: 'Arrival', year: 2016, genre: 'Sci-Fi'}),
       (:movie {title: 'Dune', year: 2021, genre: 'Sci-Fi'}),
       (:movie {title: 'Gattaca', year: 1997, genre: 'Sci-Fi'}),
       (:movie {title: 'Sicario', year: 2015, genre: 'Thriller'}),
       (:movie {title: 'Prisoners', year: 2013, genre: 'Thriller'}),
       (:movie {title: 'Enemy', year: 2013, genre: 'Thriller'});
CREATE (:person {name: 'Denis Villeneuve'}), (:person {name: 'Roger Deakins'});
```

### 为属性创建索引 {#index-a-property}

```cypher
CREATE PROPERTY INDEX movie_title_idx ON movie (title);
```

```
CREATE PROPERTY INDEX
```

它创建的是表达式上的 B-tree：

```psql
\d indexdemo.movie
```

```
                                                           Table "indexdemo.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.movie'::cstring), nextval('indexdemo.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_title_idx" btree ((properties.'title'))
Inherits: indexdemo.ag_vertex
```

`\dGi` 以能重建该索引的语句形式列出同一个索引：

```psql
\dGi indexdemo.*
```

```
                                                   List of property indexes
   Graph   | LabelName |    IndexName    | Unique | Owner |                              Indexdef
-----------+-----------+-----------------+--------+-------+--------------------------------------------------------------------
 indexdemo | movie     | movie_title_idx | f      | agens | CREATE PROPERTY INDEX movie_title_idx ON movie USING btree (title)
(1 row)
```

规划器会把 `title` 上的相等条件匹配到该表达式。六个顶点太少，规划器不会因此优先选择索引扫描，所以下面的设置让计划可见：

```cypher
SET enable_seqscan = off;
EXPLAIN (COSTS OFF) MATCH (m:movie {title: 'Dune'}) RETURN m.year;
```

```
                      QUERY PLAN                      
------------------------------------------------------
 Index Scan using movie_title_idx on movie m
   Index Cond: (properties.'title' = '"Dune"'::jsonb)
(2 rows)
```

```cypher
RESET enable_seqscan;
```

### 省略索引名 {#let-the-index-name-itself}

```cypher
CREATE PROPERTY INDEX ON movie (year);
```

```psql
\dGi indexdemo.movie_year_idx
```

```
                                                  List of property indexes
   Graph   | LabelName |   IndexName    | Unique | Owner |                             Indexdef
-----------+-----------+----------------+--------+-------+------------------------------------------------------------------
 indexdemo | movie     | movie_year_idx | f      | agens | CREATE PROPERTY INDEX movie_year_idx ON movie USING btree (year)
(1 row)
```

### 选择访问方法 {#choose-an-access-method}

对属性包读取，除 btree 外还可选 `gin` 和 `hash`：

```cypher
CREATE PROPERTY INDEX movie_genre_gin ON movie USING gin (genre);
CREATE PROPERTY INDEX movie_genre_hash ON movie USING hash (genre);
```

```
CREATE PROPERTY INDEX
CREATE PROPERTY INDEX
```

另外三个访问方法与 AgensGraph 无关。它们没有适用于 `jsonb` 的默认操作符类：

```cypher
CREATE PROPERTY INDEX movie_genre_gist ON movie USING gist (genre);
```

```
ERROR:  data type jsonb has no default operator class for access method "gist"
HINT:  You must specify an operator class for the index or define a default operator class for the data type.
```

`spgist` 和 `brin` 以同样方式失败。

### 拒绝重复值 {#reject-duplicate-values}

```cypher
CREATE UNIQUE PROPERTY INDEX movie_title_uniq ON movie (title);
CREATE (:movie {title: 'Dune', year: 1984});
```

```
ERROR:  duplicate key value violates unique constraint "movie_title_uniq"
DETAIL:  Key ((properties.'title'))=("Dune") already exists.
```

消息中的 `Key` 是索引表达式；凭借这一点，可以区分唯一属性索引和列上的唯一约束。

### 索引标签的一部分 {#index-part-of-a-label}

```cypher
CREATE PROPERTY INDEX movie_recent_idx ON movie (title) WHERE (year > 2010);
```

```
CREATE PROPERTY INDEX
```

### 索引多个属性和表达式 {#index-several-properties-and-an-expression}

```cypher
CREATE PROPERTY INDEX movie_genre_year_idx ON movie (genre, year DESC NULLS LAST);
CREATE PROPERTY INDEX movie_decade_idx ON movie ((year / 10));
CREATE PROPERTY INDEX movie_title_ops ON movie USING gin (title jsonb_path_ops);
```

它们全都是表达式索引。`\d` 会准确显示创建了什么，包括算术索引携带的 Cypher 运算符：

```psql
\d indexdemo.movie
```

```
                                                           Table "indexdemo.movie"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.movie'::cstring), nextval('indexdemo.movie_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
Indexes:
    "movie_pkey" PRIMARY KEY, btree (id)
    "movie_decade_idx" btree (((properties.'year') `/` cypher_to_jsonb(10)))
    "movie_genre_gin" gin ((properties.'genre'))
    "movie_genre_hash" hash ((properties.'genre'))
    "movie_genre_year_idx" btree ((properties.'genre'), (properties.'year') DESC NULLS LAST)
    "movie_recent_idx" btree ((properties.'title')) WHERE (properties.'year') > cypher_to_jsonb(2010)
    "movie_title_idx" btree ((properties.'title'))
    "movie_title_ops" gin ((properties.'title') jsonb_path_ops)
    "movie_title_uniq" UNIQUE, btree ((properties.'title'))
    "movie_year_idx" btree ((properties.'year'))
Inherits: indexdemo.ag_vertex
```

### 索引提升属性 {#index-a-promoted-property}

属性已提升为列的标签，索引的是该列：

```cypher
CREATE VLABEL title (year int GENERATED, name text GENERATED);
CREATE (:title {name: 'Arrival', year: 2016}), (:title {name: 'Dune', year: 2021}), (:title {name: 'Gattaca', year: 1997});
CREATE PROPERTY INDEX title_year_idx ON title (year);
```

```psql
\d indexdemo.title
```

```
                                                           Table "indexdemo.title"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.title'::cstring), nextval('indexdemo.title_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
 name       | text    |           |          | generated always as (ag_property_text(properties, 'name'::text, 's'::"char")) stored
Indexes:
    "title_pkey" PRIMARY KEY, btree (id)
    "title_year_idx" btree (year)
Inherits: indexdemo.ag_vertex
```

是 `btree (year)`，不是 `btree ((properties.'year'))`。执行计划的读法也相同，只是比较整数而不是 `jsonb`：

```cypher
SET enable_seqscan = off;
EXPLAIN (COSTS OFF) MATCH (t:title) WHERE t.year > 2010 RETURN t.name;
```

```
                 QUERY PLAN                 
--------------------------------------------
 Index Scan using title_year_idx on title t
   Index Cond: (year > 2010)
(2 rows)
```

```cypher
RESET enable_seqscan;
```

因为被索引值是列，排序规则、操作符类以及该列类型支持的访问方法都变得可用：

```cypher
CREATE PROPERTY INDEX title_name_coll ON title (name COLLATE "C");
CREATE PROPERTY INDEX title_name_pat ON title (name text_pattern_ops);
CREATE PROPERTY INDEX title_year_brin ON title USING brin (year);
```

```psql
\d indexdemo.title
```

```
                                                           Table "indexdemo.title"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('indexdemo.title'::cstring), nextval('indexdemo.title_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
 name       | text    |           |          | generated always as (ag_property_text(properties, 'name'::text, 's'::"char")) stored
Indexes:
    "title_pkey" PRIMARY KEY, btree (id)
    "title_name_coll" btree (name COLLATE "C")
    "title_name_pat" btree (name text_pattern_ops)
    "title_year_brin" brin (year)
    "title_year_idx" btree (year)
Inherits: indexdemo.ag_vertex
```

这三项都不能用于从属性包读取的属性。

### 值得识别的拒绝 {#refusals-worth-recognizing}

`INCLUDE` 完全不能使用，无论是否是提升列，因为属性总是写成表达式：

```cypher
CREATE PROPERTY INDEX title_name_incl ON title (name) INCLUDE (year);
```

```
ERROR:  expressions are not supported in included columns
```

操作符类参数不属于这条语句：

```cypher
CREATE PROPERTY INDEX movie_title_op ON movie USING gin (title jsonb_ops (fastupdate = off));
```

```
ERROR:  syntax error at or near "("
LINE 1: ...ovie_title_op ON movie USING gin (title jsonb_ops (fastupdat...
                                                             ^
```

嵌套路径只在属性持有映射时有效。这里的 `person.name` 是字符串，因此在构建索引时深入其中会失败：

```cypher
CREATE PROPERTY INDEX person_first_idx ON person (name.first);
```

```
ERROR:  map or list is expected but scalar value
```

已占用的名称会被报告，不会被替换：

```cypher
CREATE PROPERTY INDEX IF NOT EXISTS movie_title_idx ON movie (title);
```

```
NOTICE:  relation "movie_title_idx" already exists, skipping
CREATE PROPERTY INDEX
```

最后删除示例创建的图：

```cypher
DROP GRAPH indexdemo CASCADE;
```

## Notes {#notes}

`CONCURRENTLY` 被接受，作用与 `CREATE INDEX` 中相同：创建索引时不阻止写入。`ONLY` 也被接受，但对普通标签没有任何影响。无论是否使用 `ONLY`，父标签上的索引都只覆盖父标签自身的行；因此一个继承层级中，每个会被扫描的标签都需要自己的索引。

### 提升键在这里如何解析 {#how-a-promoted-key-resolves-here}

在带有[提升属性](/zh/agensgraph/querying/typed-columns/)的标签上，`( ... )` 的两种形式解析方式不同：

| 写法 | 被索引的内容 |
| --- | --- |
| `( year )`，裸键 | 提升列 `year` |
| `( (lower(title)) )`，表达式 | `lower(properties.'title')`，基于 jsonb 属性包 |

查询提升键时，两种情况都会读取列，因此裸键形式才能让查询使用索引。要索引基于提升键的表达式，应把它写成基于列的 SQL——`CREATE INDEX ON g.film (lower(title))`——`\dGi` 仍会列出它。

`\dGi` 以 Cypher 形式渲染 `Indexdef` 列，因此两种写法中的键看起来相同。要判断索引基于哪一种，可读取 `pg_get_indexdef`，或对标签的表执行 `\d`：那里裸提升键显示为 `btree (year)`，属性形式显示为
`btree ((properties.'year'))`。

## Compatibility {#compatibility}

### ISO/IEC 39075 (GQL) {#isoiec-39075-gql}

GQL 没有索引 DDL。它修改目录的语句仅限模式、图和图类型（§12）。索引在那里没有标准写法，因此 `CREATE PROPERTY INDEX` 是 AgensGraph 自有语句。

### PostgreSQL {#postgresql}

`CREATE PROPERTY INDEX` 对应表达式上的 `CREATE INDEX`。`UNIQUE`、
`CONCURRENTLY`、`USING`、`COLLATE`、操作符类、排序顺序、`NULLS [NOT]
DISTINCT`、`WITH`、`TABLESPACE` 和 `WHERE` 的含义都与 PostgreSQL 相同。
三处差别重要。索引目标写成 Cypher 属性，而不是列或括起来的 SQL 表达式，因此解析器会替你构造 `properties` 读取。`CREATE INDEX` 接受的 `INCLUDE` 和操作符类参数在这里不能使用。另外，[`DROP PROPERTY INDEX`](/zh/agensgraph/reference/ddl/drop-property-index/) 只接受属性索引，而 `DROP INDEX` 接受标签的任何索引，其中包括属性索引。

## See also {#see-also}

- [`DROP PROPERTY INDEX`](/zh/agensgraph/reference/ddl/drop-property-index/)
- [`REINDEX VLABEL` 与 `REINDEX ELABEL`](/zh/agensgraph/reference/ddl/reindex/)
- [`CREATE CONSTRAINT`](/zh/agensgraph/reference/ddl/create-constraint/)
- [把属性提升为列](/zh/agensgraph/querying/typed-columns/)
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)
