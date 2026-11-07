---
title: 索引与约束
linkTitle: 索引与约束
description: 属性索引是 PostgreSQL btree，其表达式从标签的 jsonb 属性包中读取一个键。
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/indexes-and-constraints.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


属性索引是 PostgreSQL btree，其表达式从标签的 `jsonb` 属性包中读取一个键。这句话几乎解释了它何时有帮助：恰好当规划器能把谓词匹配到该表达式时有帮助；匹配不到时完全不起作用。

本页通过实验确定哪些谓词符合条件。答案不对称，其中几项令人意外，所以下文的表格是本页重点。[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#what-a-property-index-and-a-constraint-become)展示索引在磁盘上的样子。完整语法见 [`CREATE PROPERTY INDEX`](/zh/agensgraph/reference/ddl/create-property-index/) 和 [`CREATE CONSTRAINT`](/zh/agensgraph/reference/ddl/create-constraint/)。

## 用于测量的图 {#a-graph-to-measure-on}

[示例数据集](/zh/agensgraph/get-started/example-dataset/)只有 18 部电影，行数太少，规划器不会为了读表而偏好索引。创建一个更大的标签来实验，并在页面末尾删除它：

```sql
CREATE TABLE seed_film AS
SELECT 'Film ' || lpad(g::text, 6, '0') AS title,
       1900 + (g % 130) AS year,
       (ARRAY['Action','Sci-Fi','Drama','Comedy'])[1 + (g % 4)] AS genre
FROM generate_series(1, 50000) g;
```

```cypher
CREATE GRAPH idxlab;
SET graph_path = idxlab;
CREATE VLABEL film;
LOAD FROM seed_film AS r CREATE (:film {title: r.title, year: r.year, genre: r.genre});
CREATE PROPERTY INDEX ON film (title);
CREATE PROPERTY INDEX ON film (year);
```

```sql
ANALYZE idxlab.film;
```

`ANALYZE` 与索引同样重要。规划器没有统计信息的索引，就是它会拒绝使用的索引。

下面每个计划都是规划器在 50,000 行上的自主选择，没有为了证明观点关闭任何设置。

## 索引能服务什么 {#what-an-index-can-serve}

相等是衡量其他情况的基准：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title = 'Film 000042' RETURN f.year;
```

```
                         QUERY PLAN                          
-------------------------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (properties.'title' = '"Film 000042"'::jsonb)
```

`Index Cond` 是要找的词。它表示谓词变成了索引搜索。如果谓词出现在 `Filter` 中，则是在扫描已经取回的行上求值；这正是索引本应避免的事情。

模式中的属性映射会编译成同一个相等条件，并得到同一个计划：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film {title: 'Film 000042'}) RETURN f.year;
```

```
                         QUERY PLAN                          
-------------------------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (properties.'title' = '"Film 000042"'::jsonb)
```

范围可以使用索引，因为 btree 有序：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year >= 2025 AND f.year < 2030 RETURN f.title;
```

```
                                             QUERY PLAN                                             
----------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on film f
   Recheck Cond: ((properties.'year' >= '2025'::jsonb) AND (properties.'year' < '2030'::jsonb))
   ->  Bitmap Index Scan on film_year_idx
         Index Cond: ((properties.'year' >= '2025'::jsonb) AND (properties.'year' < '2030'::jsonb))
```

比较发生在 jsonb 自身的排序中；数字按数值排序，所以 `>= 2025` 的含义正是你想要的。但 jsonb 先按*类型*再按值排序：保存字符串 `"2025"` 的属性不会位于两个数字之间。

字面量 `IN` 列表会变成数组搜索：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title IN ['Film 000042', 'Film 000043'] RETURN f.year;
```

```
                                         QUERY PLAN                                          
---------------------------------------------------------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (properties.'title' = ANY ('{"\"Film 000042\"","\"Film 000043\""}'::jsonb[]))
```

## 索引不能服务什么 {#what-an-index-cannot-serve}

`<>` 不能使用索引，原因很普通：“不是这一个值”就是表的大部分：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year <> 2020 RETURN f.title;
```

```
                   QUERY PLAN                   
------------------------------------------------
 Seq Scan on film f
   Filter: (properties.'year' <> '2020'::jsonb)
```

字符串谓词最容易让人中招，因为 `STARTS WITH` 看起来应该能变成前缀范围：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title STARTS WITH 'Film 00004' RETURN f.year;
```

```
                               QUERY PLAN                                
-------------------------------------------------------------------------
 Seq Scan on film f
   Filter: string_starts_with(properties.'title', '"Film 00004"'::jsonb)
```

事实并非如此。`STARTS WITH` 编译为函数调用 `string_starts_with`，而 `properties.'title'` 上的 btree 没有该函数的运算符类条目。因此完全没有索引路径，不只是索引被拒绝。关闭 `enable_seqscan` 也不会产生路径；计划仍是顺序扫描，并标记为 `Disabled: true`。

`CONTAINS`、`ENDS WITH` 和 `=~` 行为相同，各自编译为自己的函数：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title CONTAINS '00042' RETURN f.year;
```

```
                           QUERY PLAN                            
-----------------------------------------------------------------
 Seq Scan on film f
   Filter: string_contains(properties.'title', '"00042"'::jsonb)
```

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title =~ '^Film 00004' RETURN f.year;
```

```
                             QUERY PLAN                             
--------------------------------------------------------------------
 Seq Scan on film f
   Filter: string_regex(properties.'title', '"^Film 00004"'::jsonb)
```

对未提升属性，`IS NULL` 和 `IS NOT NULL` 也会退回扫描：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.director IS NULL RETURN f.title;
```

```
                QUERY PLAN                 
-------------------------------------------
 Seq Scan on film f
   Filter: (properties.'director' IS NULL)
```

这个原因值得理解，因为它也解释了提升后 `IS NULL` 为什么表现*不同*。对于属性包中没有 `director` 键的行，`properties.'director'` 为 null。该键上的表达式索引会为每个这样的行存一个 null，因此索引几乎必须从头读到尾。

在提升列上，同一测试是真实列上的真实 `IS NULL`，btree 可以直接回答。

### 汇总表 {#the-table}

以下结果在 50,000 行上测得，`title` 上有 `film_title_idx`，`year` 上有 `film_year_idx`，并已运行 `ANALYZE`：

| 谓词 | 使用索引 |
| --- | --- |
| `f.title = 'x'` | 是——`Index Cond` |
| 模式中的 `(f:film {title: 'x'})` | 是——`Index Cond` |
| `f.year >= 2025 AND f.year < 2030` | 是——`Bitmap Index Scan` |
| `f.title IN ['x', 'y']` | 是——带 `= ANY` 的 `Index Cond` |
| `f.year <> 2020` | 否——`Seq Scan` |
| `f.title STARTS WITH 'x'` | 否——`string_starts_with` 过滤 |
| `f.title CONTAINS 'x'` | 否——`string_contains` 过滤 |
| `f.title ENDS WITH 'x'` | 否——`string_ends_with` 过滤 |
| `f.title =~ '^x'` | 否——`string_regex` 过滤 |
| `f.director IS NULL` | 否——`Seq Scan` |
| `f.title IS NOT NULL` | 否——`Seq Scan` |
| `ORDER BY f.title LIMIT n` | 是——`Index Scan`，无排序 |

对 Cypher 谓词而言，任何索引类型都救不了这些字符串谓词：它们是函数调用，没有运算符类认领。如果需要前缀或子串搜索，[全文搜索](/zh/agensgraph/guides/search/full-text/)才是工具。也可以从 SQL 访问列；见[下文](#what-promotion-changes)。

## 排序 {#ordering}

索引可以服务同一属性上的 `ORDER BY`。因此“按属性取前 N”的查询完全不需要排序：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) RETURN f.title AS t ORDER BY t LIMIT 5;
```

```
                   QUERY PLAN                    
-------------------------------------------------
 Limit
   ->  Index Scan using film_title_idx on film f
```

有效的原因是排序键按值本身排序，而不是按它的 jsonb 表示排序。如果按索引未保存的表达式排序，仍会执行排序。

## 复合索引与部分索引 {#composite-and-partial-indexes}

属性索引可以接受多个键，最左前缀规则沿用 PostgreSQL：

```cypher
CREATE PROPERTY INDEX ON film (genre, year);
```

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.genre = 'Comedy' AND f.year >= 2025 RETURN f.title;
```

```
                                               QUERY PLAN                                                
---------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on film f
   Recheck Cond: ((properties.'genre' = '"Comedy"'::jsonb) AND (properties.'year' >= '2025'::jsonb))
   ->  Bitmap Index Scan on film_genre_year_idx
         Index Cond: ((properties.'genre' = '"Comedy"'::jsonb) AND (properties.'year' >= '2025'::jsonb))
```

只查 `year` 时无法使用它，会回到 `year` 的单键索引。因此像在 SQL 中一样，把相等条件的键放在前面。

索引上的 `WHERE` 子句会创建部分索引。这就是为大标签中的小型热子集建立索引的方法：

```cypher
CREATE PROPERTY INDEX film_comedy_year_idx ON film (year) WHERE genre = 'Comedy';
```

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.genre = 'Comedy' AND f.year >= 2025 RETURN f.title;
```

```
                                             QUERY PLAN                                              
-----------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on film f
   Recheck Cond: ((properties.'year' >= '2025'::jsonb) AND (properties.'genre' = '"Comedy"'::jsonb))
   ->  Bitmap Index Scan on film_comedy_year_idx
         Index Cond: (properties.'year' >= '2025'::jsonb)
```

`genre` 测试离开了索引条件，因为这个索引中的每个条目已经是喜剧，只保留在 recheck 中。该索引大小是 `year` 全量索引的四分之一：524,288 字节对 2,056,192 字节。规划器在两个备选中选择了它。

`CREATE PROPERTY INDEX` 也接受 `USING btree | hash | gin | brin | gist | spgist`、`CONCURRENTLY`、`IF NOT EXISTS`、`INCLUDE` 和表空间。它们的含义都与 PostgreSQL 中相同。

> [!NOTE]
> `CREATE PROPERTY INDEX (...)` 中的每个裸名称都是*属性键*，包括 `properties` 这个词。`CREATE PROPERTY INDEX ON film USING gin (properties)` 索引名为 `properties` 的属性，而电影没有这个属性。要索引属性包本身，使用普通 SQL——`CREATE INDEX film_bag_idx ON idxlab.film USING gin (properties)`；并注意只有 `properties @> '{"genre": "Comedy"}'` 这类 SQL 谓词能使用它。Cypher 属性读取编译为 `properties.'genre'`，属性包上的 GIN 索引匹配不到它。

## 提升改变了什么 {#what-promotion-changes}

提升属性会为它创建真实类型列，此后每个谓词都编译到该列，而不是属性包。[把属性提升为列](/zh/agensgraph/querying/typed-columns/)专讲原因和方法。这里重要的是，它会双向改变上表答案。

```cypher
ALTER VLABEL film ADD COLUMN year int GENERATED;
ALTER VLABEL film ADD COLUMN title text GENERATED;
```

先看提升对已有索引的影响。`properties.'year'` 上的索引匹配不到任何查询，因为没有查询再编译到该表达式：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.year >= 2025 AND f.year < 2030 RETURN f.title;
```

```
                  QUERY PLAN                  
----------------------------------------------
 Seq Scan on film f
   Filter: ((year >= 2025) AND (year < 2030))
```

索引仍然存在，每次写入仍然维护，而且不再被任何查询使用。因此提升永远是两步：先提升，再基于列重建索引。

对裸键来说，重建为属性索引有效；这是常见情况，也是下面的情况。基于该键的*表达式*需要另一种形式。`CREATE PROPERTY INDEX` 把裸键编译到提升列，但把基于该键的表达式编译到 jsonb 属性包，而查询读取的不是属性包。这个索引用 SQL 写在列上；`\dGi` 仍会列出：

```sql
CREATE INDEX film_lower_idx ON idxlab.film (lower(title));
```

参见[表达式属性索引建立在属性包上](/zh/agensgraph/querying/typed-columns/#an-expression-property-index-is-built-over-the-bag)。

```cypher
DROP PROPERTY INDEX film_year_idx;
DROP PROPERTY INDEX film_title_idx;
DROP PROPERTY INDEX film_genre_year_idx;
DROP PROPERTY INDEX film_comedy_year_idx;
CREATE PROPERTY INDEX ON film (year);
CREATE PROPERTY INDEX ON film (title);
```

标签现在如下所示。新索引是普通列索引，不是表达式索引：

```psql
\d idxlab.film
```

```
                                                             Table "idxlab.film"
   Column   |  Type   | Collation | Nullable |                                            Default                                            
------------+---------+-----------+----------+-----------------------------------------------------------------------------------------------
 id         | graphid |           | not null | graphid(graph_labid('idxlab.film'::cstring), nextval('idxlab.film_id_seq'::regclass))
 properties | jsonb   |           | not null | jsonb_build_object()
 year       | integer |           |          | generated always as (ag_property_text(properties, 'year'::text, 'n'::"char")::integer) stored
 title      | text    |           |          | generated always as (ag_property_text(properties, 'title'::text, 's'::"char")) stored
Indexes:
    "film_pkey" PRIMARY KEY, btree (id)
    "film_bag_idx" gin (properties)
    "film_title_idx" btree (title)
    "film_year_idx" btree (year)
Inherits: idxlab.ag_vertex
```

相等和范围现在比较原生值而不是 jsonb：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title = 'Film 000042' RETURN f.year;
```

```
                 QUERY PLAN                  
---------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (title = 'Film 000042'::text)
```

`IS NULL` 变得可使用索引；提升之前不是：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title IS NULL RETURN f.year;
```

```
                QUERY PLAN                 
-------------------------------------------
 Index Scan using film_title_idx on film f
   Index Cond: (title IS NULL)
```

`ORDER BY` 从索引扫描提升为 index-only 扫描，因为查询需要的值就在索引中：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) RETURN f.title AS t ORDER BY t LIMIT 5;
```

```
                      QUERY PLAN                      
------------------------------------------------------
 Limit
   ->  Index Only Scan using film_title_idx on film f
```

同时两个谓词变*差*。`IN` 不再使用索引，因为列被重新装箱为 jsonb，与 jsonb 列表比较：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title IN ['Film 000042', 'Film 000043'] RETURN f.year;
```

```
                                         QUERY PLAN                                          
---------------------------------------------------------------------------------------------
 Seq Scan on film f
   Filter: (cypher_to_jsonb(title) = ANY ('{"\"Film 000042\"","\"Film 000043\""}'::jsonb[]))
```

`STARTS WITH` 以同样方式装箱，因此提升也救不了它：

```cypher
EXPLAIN (COSTS OFF) MATCH (f:film) WHERE f.title STARTS WITH 'Film 00004' RETURN f.year;
```

```
                                 QUERY PLAN                                  
-----------------------------------------------------------------------------
 Seq Scan on film f
   Filter: string_starts_with(cypher_to_jsonb(title), '"Film 00004"'::jsonb)
```

但该列是真实的 `text` 列，SQL 可以用真实 `text` 运算符访问它；那*确实是*前缀范围：

```sql
EXPLAIN (COSTS OFF) SELECT count(*) FROM idxlab.film WHERE title LIKE 'Film 00004%';
```

```
                                      QUERY PLAN                                      
--------------------------------------------------------------------------------------
 Aggregate
   ->  Index Only Scan using film_title_idx on film
         Index Cond: ((title >= 'Film 00004'::text) AND (title < 'Film 00005'::text))
         Filter: (title ~~ 'Film 00004%'::text)
```

这就是热键前缀搜索的实用答案：提升属性，并用 SQL 写前缀谓词；如果需要，再包一层 Cypher。参见[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。

### 提升后的汇总表 {#the-table-after-promotion}

| 谓词 | 未提升（jsonb） | 已提升（类型列） |
| --- | --- | --- |
| `f.title = 'x'` | 是 | 是 |
| `f.year >= a AND f.year < b` | 是 | 是 |
| `f.title IN ['x', 'y']` | 是 | **否**——装箱为 jsonb |
| `f.year <> 2020` | 否 | 否 |
| `f.title STARTS WITH 'x'` | 否 | 否 |
| `f.title CONTAINS 'x'` | 否 | 否 |
| `f.title =~ '^x'` | 否 | 否 |
| `f.title IS NULL` | 否 | **是** |
| `ORDER BY f.title LIMIT n` | 是——索引扫描 | 是——index-only 扫描 |
| SQL `title LIKE 'x%'` | 不适用 | 是——前缀范围 |

## 跨标签层级 {#across-a-label-hierarchy}

索引属于一张表。匹配父标签的模式会扫描父标签及其下每个标签，而每张表都需要自己的索引。创建一个家族来观察：

```sql
CREATE TABLE seed_work AS SELECT g FROM generate_series(1, 10000) g;
```

```cypher
CREATE VLABEL work;
CREATE VLABEL short INHERITS (work);
CREATE VLABEL feature INHERITS (work);
LOAD FROM seed_work AS r CREATE (:short {code: 'S' || lpad((r.g)::text, 6, '0')});
LOAD FROM seed_work AS r CREATE (:feature {code: 'F' || lpad((r.g)::text, 6, '0')});
CREATE PROPERTY INDEX ON work (code);
```

```sql
ANALYZE idxlab.work; ANALYZE idxlab.short; ANALYZE idxlab.feature;
```

只有 `work` 有索引，每个子标签都会全量读取：

```cypher
EXPLAIN (COSTS OFF) MATCH (w:work) WHERE w.code = 'F000042' RETURN w;
```

```
                           QUERY PLAN                           
----------------------------------------------------------------
 Result
   ->  Append
         ->  Seq Scan on work w_1
               Filter: (properties.'code' = '"F000042"'::jsonb)
         ->  Seq Scan on short w_2
               Filter: (properties.'code' = '"F000042"'::jsonb)
         ->  Seq Scan on feature w_3
               Filter: (properties.'code' = '"F000042"'::jsonb)
```

给每个子标签建索引后，`Append` 的每个分支都有一个：

```cypher
CREATE PROPERTY INDEX ON short (code);
CREATE PROPERTY INDEX ON feature (code);
```

```
                             QUERY PLAN                             
--------------------------------------------------------------------
 Result
   ->  Append
         ->  Seq Scan on work w_1
               Filter: (properties.'code' = '"F000042"'::jsonb)
         ->  Index Scan using short_code_idx on short w_2
               Index Cond: (properties.'code' = '"F000042"'::jsonb)
         ->  Index Scan using feature_code_idx on feature w_3
               Index Cond: (properties.'code' = '"F000042"'::jsonb)
```

`work` 本身仍是顺序扫描，因为它没有自己的行；读空表比打开索引便宜。这是正确决策。这也是要警惕的形状：只要按同一属性搜索一个家族，层级就要求你为每个标签永久维护一个索引。

## 约束 {#constraints}

存在两种形式，底层就是 PostgreSQL 的两种形式。

`ASSERT <key> IS UNIQUE` 在该键表达式上创建排除约束：

```cypher
CREATE VLABEL account;
CREATE CONSTRAINT account_email_uq ON account ASSERT email IS UNIQUE;
```

```cypher
CREATE (:account {email: 'a@example.com', age: 30});
CREATE (:account {email: 'a@example.com', age: 31});
```

```
ERROR:  conflicting key value violates exclusion constraint "account_email_uq"
DETAIL:  Key ((properties.'email'))=("a@example.com") conflicts with existing key ((properties.'email'))=("a@example.com").
```

`ASSERT <predicate>` 创建检查约束：

```cypher
CREATE CONSTRAINT account_age_ck ON account ASSERT age > 0;
CREATE (:account {email: 'b@example.com', age: -1});
```

```
ERROR:  new row for relation "account" violates check constraint "account_age_ck"
DETAIL:  Failing row contains (7.3, {"age": -1, "email": "b@example.com"}).
```

两者都显示为普通约束；唯一约束背后是该表达式上的真实 btree，因此也可用作该键查找的索引：

```sql
SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint
WHERE conrelid = 'idxlab.account'::regclass AND contype IN ('c', 'x') ORDER BY conname;
```

```
     conname      |               pg_get_constraintdef                
------------------+---------------------------------------------------
 account_age_ck   | CHECK ((properties.'age' > cypher_to_jsonb(0)))
 account_email_uq | EXCLUDE USING btree ((properties.'email') WITH =)
```

两个约束都没有说明缺少属性的顶点应该怎样处理。缺失键读取为 null，null 与另一个 null 不相等，未知值上的检查约束通过：

```cypher
CREATE (:account {email: 'c@example.com'});
CREATE (:account {age: 44});
CREATE (:account {age: 45});
MATCH (a:account) RETURN a.email AS email, a.age AS age ORDER BY email NULLS LAST, age;
```

```
      email      | age 
-----------------+-----
 "a@example.com" | 30
 "c@example.com" | 
                 | 44
                 | 45
```

两个完全没有 email 的账户可以共存。如果键必须存在且唯一，请添加第二个约束断言它非 null。属性包不会替你做到这一点。

`CREATE UNIQUE PROPERTY INDEX` 是唯一性的另一种写法，它产生唯一索引而不是排除约束：

```cypher
CREATE VLABEL member;
CREATE UNIQUE PROPERTY INDEX ON member (card);
CREATE (:member {card: '0001'});
CREATE (:member {card: '0001'});
```

```
ERROR:  duplicate key value violates unique constraint "member_card_idx"
DETAIL:  Key ((properties.'card'))=("0001") already exists.
```

需要快速唯一查找时选它。需要一条以自选名称出现在 `pg_constraint` 和转储中的规则时，选命名约束。两者都不会被子标签继承：父标签上的约束只约束父标签自己的行。

## 实际工作顺序 {#practical-order-of-work}

回答大多数“为什么慢”问题的顺序如下：

1. 对涉及的所有标签执行 `ANALYZE`，包括边标签。未分析的边标签比缺失索引更昂贵；参见[调优查询](/zh/agensgraph/querying/performance/#statistics-on-edge-labels)。
2. 给模式*锚定*的属性建索引：那个有选择性的相等条件用于挑选起始顶点。下游全部通过已存在的边索引连接。
3. 用 `EXPLAIN` 检查谓词是否以 `Index Cond` 到达，而不是 `Filter`。
4. 之后才考虑提升属性；当成本来自读取本身而不是搜索时，提升才是答案。

## 清理 {#clean-up}

```cypher
DROP GRAPH idxlab CASCADE;
```

```sql
DROP TABLE seed_film;
DROP TABLE seed_work;
```

## 接下来去哪里 {#where-to-go-next}

* [把属性提升为列](/zh/agensgraph/querying/typed-columns/)——上文故事的另一半。
* [调优查询](/zh/agensgraph/querying/performance/)——计划形状、统计信息以及改变它们的设置。
* [全文搜索](/zh/agensgraph/guides/search/full-text/)——子串和前缀匹配的可索引答案。
