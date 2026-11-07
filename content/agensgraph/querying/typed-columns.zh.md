---
title: 把属性提升为列
linkTitle: 把属性提升为列
description: 标签无模式，因为属性保存在每个元素自己的 jsonb 文档中。
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/typed-columns.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


标签之所以无模式，是因为属性保存在每个元素自己的 `jsonb` 文档中。这带来两项成本。

读取 `m.year` 表示在查询触碰的每一行中，于 JSON 文档里查找 `year` 键。而且读取产生的值是 jsonb 值，其上的索引也是 jsonb 索引，永远不是 `integer` 或 `vector` 上的索引。

提升会为选中的一个键消除这两项成本。`ALTER VLABEL film ADD COLUMN year int GENERATED` 为 `year` 属性创建真实的 `integer` 列，存储在属性包旁边并由服务器维护。它同时让 Cypher 编译器知道 `f.year` 应从该列回答。

查询不变，属性也没有任何改变：它仍是属性；对所有其他键，标签仍无模式；提升可以撤销。

本页讨论这笔交易何时值得，以及随之承担什么。DDL 语法见 [`ALTER VLABEL`](/zh/agensgraph/reference/ddl/alter-label/) 和 [`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)。

## 用于提升的自建标签 {#a-label-of-your-own-to-promote-on}

提升会改变标签形状，所以在副本上实验，而不是修改手册的共享图。对标签表使用 `LOAD FROM` 会直接复制属性包：

```cypher
CREATE GRAPH promolab;
SET graph_path = promolab;
CREATE VLABEL film;
LOAD FROM moviekb.movie AS r CREATE (:film = r.properties);
```

这样你就在一个可以自由重塑的图中得到[示例数据集](/zh/agensgraph/get-started/example-dataset/)的 18 部电影。整页都在这个图中运行，并在末尾删除它。

## 提升做什么 {#what-promotion-does}

提升前，`year` 上的过滤要进入属性包。`EXPLAIN (VERBOSE)` 把属性读取显示为 `properties.'key'`：

```cypher
EXPLAIN (VERBOSE, COSTS OFF) MATCH (f:film) WHERE f.year > 2010 RETURN f.title;
```

```
                   QUERY PLAN                    
-------------------------------------------------
 Seq Scan on promolab.film f
   Output: f.properties.'title'
   Filter: (f.properties.'year' > '2010'::jsonb)
```

提升它：

```cypher
ALTER VLABEL film ADD COLUMN year int GENERATED;
```

```psql
\d promolab.film
```

```
                                                            Table "promolab.film"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('promolab.film'::cstring), nextval('promolab.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
Inherits: promolab.ag_vertex
```

该列是 `GENERATED ALWAYS AS ... STORED`：一个普通的 PostgreSQL 生成列，其表达式从属性包中取出一个键。`ag_property_text(properties, 'year', 'n')` 只有在值属于该列可保存的类型时才返回键的文本：`'n'` 表示数字，`'s'` 表示字符串，`'b'` 表示布尔值。

其余由转换为 `integer` 完成。没有人写入该列；服务器在每次插入和更新时计算它。

同一查询现在过滤列：

```cypher
EXPLAIN (VERBOSE, COSTS OFF) MATCH (f:film) WHERE f.year > 2010 RETURN f.title;
```

```
           QUERY PLAN           
--------------------------------
 Seq Scan on promolab.film f
   Output: f.properties.'title'
   Filter: (f.year > 2010)
```

`f.title` 仍是属性包读取，因为只提升了 `year`。答案不变：

```cypher
MATCH (f:film) WHERE f.year > 2010 RETURN f.title AS title, f.year AS year ORDER BY year;
```

```
           title            | year 
----------------------------+------
 "The Avengers"             | 2012
 "Elysium"                  | 2013
 "Interstellar"             | 2014
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
```

既有行会作为 `ALTER` 的一部分填充，因此列存在的瞬间就是完整的。而且值同时在**两个**位置。属性包仍保存它：

```sql
SELECT properties->>'title' AS title, year, properties->>'year' AS in_the_bag
FROM promolab.film ORDER BY year LIMIT 3;
```

```
     title      | year | in_the_bag 
----------------+------+------------
 Blade Runner   | 1982 | 1982
 The Terminator | 1984 | 1984
 Total Recall   | 1990 | 1990
```

这种重复是刻意的。属性仍是属性，因此读取 `properties` 的客户端看到的内容与以前相同。转储在属性包中保存一次数据，并重新生成列。删除列不会丢失任何内容。代价是存储：你要为该值付两次空间。

属性键到列的映射记录在 `ag_label_property`：

```sql
SELECT l.labname, p.propname, a.attname, format_type(a.atttypid, a.atttypmod) AS type
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_label_property p ON p.laboid = l.oid
  JOIN pg_attribute a ON a.attrelid = l.relid AND a.attnum = p.attnum
WHERE l.relid = 'promolab.film'::regclass;
```

```
 labname | propname | attname |  type   
---------+----------+---------+---------
 film    | year     | year    | integer
```

正是这一行让读取解析到列。没有它，列虽然存在，Cypher 却不知道它。参见[长格式不会注册映射](#the-long-form-registers-nothing-unless-it-is-a-single-key)。

### 提升后的读取具有列类型 {#a-promoted-read-has-the-columns-type}

Cypher 的 `RETURN` 把属性读取作为 jsonb 交回，所以 `RETURN f.title` 会连同引号输出 `"The Matrix"`。读取提升键是例外：它以列声明类型返回。这里 `year` 已提升，`title` 未提升。

```cypher
SELECT pg_typeof(t) AS title_type, pg_typeof(y) AS year_type
FROM (MATCH (f:film) RETURN f.title AS t, f.year AS y LIMIT 1) q;
```

```
 title_type | year_type 
------------+-----------
 jsonb      | integer
```

值和排序无论哪种方式都相同；客户端收到的*类型*不同。期望每个 Cypher 列都以 JSON 到达的驱动会在这里看到 `integer`。

这通常是简化，因为它是得到[普通值](/zh/agensgraph/querying/combining-sql-and-cypher/#getting-a-plain-value-out)的最短路径。但它确实改变结果形状，值得对照消费者检查。

## 为提升列建索引 {#indexing-a-promoted-column}

对提升键执行 `CREATE PROPERTY INDEX` 会在列上创建普通 btree，而不是属性包上的表达式索引。规划器像使用任何列索引一样使用它。[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/#what-promotion-changes)度量它能服务哪些谓词，以及提升后变*差*的两个谓词。简短版本：

* 相等、范围和 `ORDER BY` 可被服务，且 `ORDER BY` 提升为 index-only 扫描。
* `IS NULL` 变得可索引；属性包上不是。
* `IN` 和 `STARTS WITH` 停止使用索引，因为列被重新装箱为 jsonb，以匹配 jsonb 操作数。

有一条容易忽略的规则：**提升键的那一刻，属性包上的索引就死了。** 没有任何查询再编译为 `properties.'year'`，因此该表达式上的索引永远不会被匹配，却仍在每次写入时维护。提升永远是两步：先提升，再基于列重建索引。

## 在标签定义中声明提升列 {#declaring-promoted-columns-with-the-label}

创建时，列写在标签定义中：

```cypher
CREATE VLABEL doc (words int GENERATED, tag text GENERATED (category));
```

`words int GENERATED` 把属性 `words` 提升为同名列。括号形式提升*不同*的键：`tag text GENERATED (category)` 表示“列 `tag`，由属性 `category` 填充”。当想要的键不是合法或合适的列名时使用它。

目录记录的是键，不是列名：

```sql
SELECT l.labname, p.propname, a.attname, format_type(a.atttypid, a.atttypmod) AS type
FROM pg_catalog.ag_label l
  JOIN pg_catalog.ag_label_property p ON p.laboid = l.oid
  JOIN pg_attribute a ON a.attrelid = l.relid AND a.attnum = p.attnum
WHERE l.relid = 'promolab.doc'::regclass ORDER BY p.propname;
```

```
 labname | propname | attname |  type   
---------+----------+---------+---------
 doc     | category | tag     | text
 doc     | words    | words   | integer
```

所以解析到列的 Cypher 读取是键 `d.category`。`d.tag` 是从未有人设置过的属性：

```cypher
CREATE (:doc {title: 'a note', words: 12, category: 'news'});
MATCH (d:doc) RETURN d.words AS words, d.category AS category, d.tag AS tag;
```

```
 words | category | tag 
-------+----------+-----
    12 | news     | 
```

`ALTER ELABEL` 以同样方式提升边属性。对遍历所依据的权重，这样做很值得。

## 扩展类型 {#extension-types}

列类型可以来自扩展。正是这种情况让提升不止是微优化。作为属性存储的嵌入是 JSON 数组，因此每次相似度查询都必须逐行转换：`p.emb::vector(4)`。提升后，转换在写入时发生一次：

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

```cypher
CREATE VLABEL page (emb vector(4) GENERATED);
```

```psql
\d promolab.page
```

```
                                                           Table "promolab.page"
   Column   |   Type    | Collation | Nullable |                                          Default                                          
------------+-----------+-----------+----------+-------------------------------------------------------------------------------------------
 id         | graphid   |           | not null | graphid(graph_labid('promolab.page'::cstring), nextval('promolab.page_id_seq'::regclass))
 properties | jsonb     |           | not null | jsonb_build_object()
 emb        | vector(4) |           |          | generated always as (((properties ->> 'emb'::text))::vector(4)) stored
Indexes:
    "page_pkey" PRIMARY KEY, btree (id)
Inherits: promolab.ag_vertex
```

注意生成表达式。对没有 JSON 对应物的类型，服务器使用普通 `->>` 而不是 `ag_property_text`，并让类型自己的输入函数接受或拒绝文本。`vector(4)` 拒绝一切不是括号中四个数字的内容。

该列随后可以承载真实向量索引。索引定义不再需要转换表达式，因为已经没有转换要做。先加载足够多的行，让索引值得被首先选择：

```sql
CREATE TABLE seed_page AS
SELECT 'page ' || g AS title, jsonb_build_array(random(), random(), random(), random()) AS emb
FROM generate_series(1, 5000) g;
```

```cypher
LOAD FROM seed_page AS r CREATE (:page {title: r.title, emb: r.emb});
CREATE PROPERTY INDEX ON page USING hnsw (emb vector_cosine_ops);
```

```sql
ANALYZE promolab.page;
```

然后 Cypher 相似度搜索会使用它：

```cypher
EXPLAIN (COSTS OFF)
MATCH (p:page) RETURN p.title AS title
ORDER BY p.emb <=> '[0.1,0.2,0.3,0.4]'::vector(4) LIMIT 3;
```

```
                         QUERY PLAN                         
------------------------------------------------------------
 Limit
   ->  Index Scan using page_emb_idx on page p
         Order By: (emb <=> '[0.1,0.2,0.3,0.4]'::vector(4))
```

同一查询的未提升版本必须为每行计算距离并排序：

```cypher
SET enable_property_promotion = off;
EXPLAIN (COSTS OFF)
MATCH (p:page) RETURN p.title AS title
ORDER BY p.emb::vector(4) <=> '[0.1,0.2,0.3,0.4]'::vector(4) LIMIT 3;
RESET enable_property_promotion;
```

```
                                        QUERY PLAN                                        
------------------------------------------------------------------------------------------
 Limit
   ->  Sort
         Sort Key: (((p.properties.'emb')::vector(4) <=> '[0.1,0.2,0.3,0.4]'::vector(4)))
         ->  Seq Scan on page p
```

在提升列上保留的 `::vector(4)` 会被折叠而不是拒绝，因此既有查询继续工作并继续使用索引。

对提升列，优先选择提升，而不是在*转换表达式*上建属性索引，例如 `((emb::vector(4)) vector_cosine_ops)`。提升列上的索引是普通列索引，在转储和恢复后更持久。参见[向量搜索](/zh/agensgraph/guides/search/vector/)。

## 提升的代价 {#what-promotion-costs-you}

### 提升后的键不再无模式 {#a-promoted-key-is-no-longer-schemaless}

这才是真正的取舍。标签上的其他键仍接受任何 JSON 值。被提升的键只接受列能保存的内容；不合适的写入会中止：

```cypher
CREATE (:film {title: 'Bad Year', year: 'nineteen ninety nine'});
```

```
ERROR:  property "year" holds a string
DETAIL:  A column promoting this property holds numbers.
CONTEXT:  while computing the promoted typed columns of graph label "film"
```

```cypher
CREATE (:film {title: 'Fractional', year: 1999.5});
```

```
ERROR:  invalid input syntax for type integer: "1999.5"
CONTEXT:  while computing the promoted typed columns of graph label "film"
```

这里能看到两种不同的检查。第一种是类型种类检查：字符串不是数字，不管它写着什么。第二种来自列类型本身。对扩展类型，只有第二种适用：

```cypher
CREATE (:page {title: 'wrong dims', emb: [1, 2, 3]});
```

```
ERROR:  expected 4 dimensions, not 3
CONTEXT:  while computing the promoted typed columns of graph label "page"
```

完全省略键始终可以。缺失属性生成 null 列，正如缺失属性读取为 null：

```cypher
CREATE (:film {title: 'Undated'});
MATCH (f:film {title: 'Undated'}) RETURN f.year AS year;
```

```
 year 
------
     
```

因此提升既是速度决策，也是数据质量决策。在生产标签上提升键之前，先查明每个既有值是否合适。`ALTER` 会对既有行应用同样检查，并在第一个不合适的值上失败：

```cypher
CREATE VLABEL city;
CREATE (:city {name: 'Seoul', pop: 9700000}), (:city {name: 'Nowhere', pop: 'many'});
```

```cypher
ALTER VLABEL city ADD COLUMN pop bigint GENERATED;
```

```
ERROR:  property "pop" holds a string
DETAIL:  A column promoting this property holds numbers.
```

这种失败很有用：它会在提交任何内容之前告诉你，标签数据不是你以为的样子。

### ALTER 会重写表 {#the-alter-rewrites-the-table}

添加存储生成列会重写标签堆，并在重写期间持有 `ACCESS EXCLUSIVE` 锁。在这个 18 行标签上是一瞬间。在大标签上，要像规划任何 `ALTER TABLE` 重写一样规划它。如果想观察，可以检查关系的文件编号：

```sql
SELECT relfilenode FROM pg_class WHERE oid = 'promolab.film'::regclass;
```

`ALTER` 前后的编号不同。

### 提升列不能有自己的排序规则 {#a-promoted-column-cannot-have-a-collation-of-its-own}

属性映射使用数据库默认排序规则比较字符串。以其他方式排序的列会对相同值给出不同的顺序和比较结果。这会把“这次读取取哪个答案”从速度问题变成结果问题。

所以它会被拒绝；即使排序规则通过域传入而不是显式写出，也同样拒绝：

```sql
CREATE DOMAIN sortkey AS text COLLATE "C";
```

```cypher
CREATE VLABEL note;
ALTER VLABEL note ADD COLUMN k sortkey GENERATED;
```

```
ERROR:  a promoted property cannot have a collation of its own
DETAIL:  Column "k" is collated "C", while a property map compares strings with the database default.
HINT:  Leave the collation unspecified, or use a type that does not carry one.
```

### Cypher 查询上的视图会固定列 {#a-view-over-a-cypher-query-pins-the-column}

视图编译一次；如果 Cypher 查询把属性解析到列，其上的视图会依赖该列：

```cypher
CREATE VIEW recent_films AS
SELECT title #>> '{}' AS title, year
FROM (MATCH (f:film) WHERE f.year > 2010 RETURN f.title AS title, f.year AS year) q;
```

```cypher
ALTER VLABEL film DROP COLUMN year;
```

```
ERROR:  cannot drop column year of table promolab.film because other objects depend on it
DETAIL:  view recent_films depends on column year of table promolab.film
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

这是正确的：否则视图会静默改读属性包。但这意味着视图是一项承诺。删除视图、删除列、重建视图。依赖在 `pg_get_viewdef` 中可见，它显示 lowered SQL 引用 `f.year`：[Cypher 查询上的视图长什么样](/zh/agensgraph/querying/combining-sql-and-cypher/#a-view-over-a-cypher-query)。

```sql
DROP VIEW recent_films;
```

### 表达式属性索引建立在属性包上 {#an-expression-property-index-is-built-over-the-bag}

`CREATE PROPERTY INDEX` 对裸键和同一键在表达式中的解析不同。裸键变成提升列；基于该键的表达式变成基于 jsonb 属性包的表达式：

```cypher
ALTER VLABEL film ADD COLUMN title text GENERATED;
CREATE PROPERTY INDEX film_title_idx ON film (title);
CREATE PROPERTY INDEX film_lower_idx ON film ((lower(title)));
```

```sql
SELECT c.relname, pg_get_indexdef(c.oid) AS real_definition
FROM pg_class c JOIN pg_index i ON i.indexrelid = c.oid
WHERE i.indrelid = 'promolab.film'::regclass AND c.relname LIKE 'film_%idx'
ORDER BY 1;
```

```
    relname     |                                   real_definition
----------------+--------------------------------------------------------------------------------------
 film_lower_idx | CREATE INDEX film_lower_idx ON promolab.film USING btree (lower(properties.'title'))
 film_title_idx | CREATE INDEX film_title_idx ON promolab.film USING btree (title)
```

两种情况下查询都读取列，所以只有裸形式能给出查询可用的索引。

`\dGi` 用 Cypher 形式报告二者，并把每个都写为 `title`：

```psql
\dGi promolab.*
```

```
                                                       List of property indexes
  Graph   | LabelName |   IndexName    | Unique | Owner |                                  Indexdef
----------+-----------+----------------+--------+-------+-----------------------------------------------------------------------------
 promolab | film      | film_lower_idx | f      | agens | CREATE PROPERTY INDEX film_lower_idx ON film USING btree ((lower((title))))
 promolab | film      | film_title_idx | f      | agens | CREATE PROPERTY INDEX film_title_idx ON film USING btree (title)
```

所以想知道标签索引基于哪一个时，请读取 `pg_get_indexdef`。

提升键有两种索引方式。裸索引让查询直接使用列。或者，当需要索引的是表达式本身时，用 SQL 基于列书写，匹配查询读取的内容：

```sql
CREATE INDEX film_lower_col_idx ON promolab.film (lower(title));
```

无论哪种方式，都先删除读取该键的表达式索引再提升键，然后按这两种形式之一重建。

### 长格式除非是单个键，否则不注册映射 {#the-long-form-registers-nothing-unless-it-is-a-single-key}

用长格式写的生成列就是普通生成列。只有当表达式恰好是从属性包取出一个键时，它才被识别为提升：`(properties ->> 'key')::type`，或转储输出的 `ag_property_text` 形式。来自多个键或经过计算的任何内容都不会注册映射：

```cypher
CREATE VLABEL post;
ALTER VLABEL post ADD COLUMN body_len int GENERATED ALWAYS AS (length(properties->>'body')) STORED;
CREATE (:post {body: 'hello there'});
```

列存在，SQL 可以读取：

```sql
SELECT id, body_len, properties FROM promolab.post;
```

```
 id  | body_len |       properties        
-----+----------+-------------------------
 8.1 |       11 | {"body": "hello there"}
```

Cypher 不能：

```cypher
MATCH (p:post) RETURN p.body_len AS body_len;
```

```
 body_len 
----------
 
```

`p.body_len` 读取名为 `body_len` 的属性，而没有任何 post 设置过它；也没有一个键能让这个列作为其值。于是这个列看起来像提升，实际不是。提升用 `GENERATED` 简写；只打算让 SQL 读取的派生列用长格式。

## 关闭解析 {#turning-resolution-off}

`enable_property_promotion` 控制 Cypher 属性读取是否解析到列，默认开启。关闭后，同一查询回到属性包：

```cypher
SET enable_property_promotion = off;
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year > 2010 RETURN f.title;
RESET enable_property_promotion;
```

```
                  QUERY PLAN                   
-----------------------------------------------
 Seq Scan on film f
   Filter: (properties.'year' > '2010'::jsonb)
```

并给出相同答案，因为属性包仍保存该值。这个设置的目的，是在不删除列的情况下判断提升是否导致意外计划。它不会停止维护列。

## 撤销提升 {#undoing-a-promotion}

```cypher
ALTER VLABEL film DROP COLUMN year;
```

列及其目录行消失，其上的任何索引也随之消失，读取回到属性包并得到相同结果：

```cypher
MATCH (f:film) WHERE f.year > 2010 RETURN count(f) AS films;
```

```
 films 
-------
 5
```

没有内容丢失，因为从来没有任何内容只存储在列中。唯一需要先清理的是固定它的视图。

## 何时提升 {#when-to-promote}

当以下四点全部成立时提升键：

* **查询按它过滤、连接或排序**，而不只是投影。只返回的键得不到收益；属性包读取已经是获取它的最便宜方式。
* **值均匀。** 如果一些行是数字、一些是字符串，`ALTER` 会拒绝；把它们强制成一种类型是数据修改，不是调优。
* **你想要值自身类型上的索引**——真实 `integer` 上的范围、index-only `ORDER BY`、`vector` 上的 HNSW。
* **标签足够大，读取成本值得关心。** 在 18 行上，这里的任何差异都测不到。

不要因为键出现在每个顶点中就提升它。均匀是前提，不是理由。还要对照应用实际发送的查询，检查提升后变差的两个谓词：`IN` 和 `STARTS WITH`。

## 清理 {#clean-up}

```cypher
DROP GRAPH promolab CASCADE;
```

```sql
DROP TABLE seed_page;
DROP DOMAIN sortkey;
```

## 接下来去哪里 {#where-to-go-next}

* [索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)——提升前后的可索引性表。
* [调优查询](/zh/agensgraph/querying/performance/)——提升在其他计划形状选择中的位置。
* [向量搜索](/zh/agensgraph/guides/search/vector/)——有无提升列的嵌入。
