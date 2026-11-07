---
title: 组合 SQL 与 Cypher
linkTitle: 组合 SQL 与 Cypher
description: AgensGraph 中 SQL 与 Cypher 之间没有桥接层，因为没有需要桥接的东西。
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/combining-sql-and-cypher.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 中 SQL 与 Cypher 之间没有桥接层，因为没有需要桥接的东西。图是与普通表位于同一数据库中的一组 PostgreSQL 表，两种语言都编译到同一棵计划树。

因此二者通过嵌套混合：Cypher 查询放在 SQL 期望表的位置，SQL 查询放在 Cypher 期望值的位置。

本页按你可能的使用顺序走一遍交叉点，然后讲那条让所有人意外的规则：Cypher `RETURN` 交回什么。

本文所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行；该数据集包含不属于图的普通表 `rating`。

## 用普通 SQL 读取标签 {#reading-a-label-with-plain-sql}

标签是表，所以读取它不需要 Cypher：

```sql
SELECT id, properties->>'title' AS title, properties->>'year' AS year
FROM moviekb.movie ORDER BY (properties->>'year')::int LIMIT 3;
```

```
  id  |     title      | year 
------+----------------+------
 3.8  | Blade Runner   | 1982
 3.15 | The Terminator | 1984
 3.11 | Total Recall   | 1990
```

这不需要启用任何设置。用 SQL 向标签写行则需要；参见[哪些操作被刻意关闭](/zh/agensgraph/concepts/graph-on-postgresql/#what-is-deliberately-closed-off)。读取就是读取。

当问题本身是关系型时，直接 SQL 是正确工具：按标签计数、把属性值连接到引用表、对属性执行窗口函数。对任何涉及可变跳数的问题，它都是错误工具。本页其余部分讨论那些情况。

## SQL FROM 中的 Cypher 查询 {#a-cypher-query-in-a-sql-from}

在 SQL `FROM` 期望表的位置放入括号中的 Cypher 查询，并给它别名。它的 `RETURN` 列表变成列：

```psql
SELECT * FROM (MATCH (m:movie) WHERE m.year > 2015 RETURN m.title AS title, m.year AS year) q
ORDER BY year;
```

```
           title            | year 
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
```

别名必选：

```psql
SELECT count(*) FROM (MATCH (m:movie) RETURN m.title AS title);
```

```
ERROR:  Cypher in FROM must have an alias
HINT:  For example, FROM (...) [AS] foo.
```

还有两条规则。每列都需要名称，因为外层查询必须能够引用它；所以不带 `AS` 的 `RETURN m.title` 会拒绝。嵌套查询必须是读取；`FROM` 内的写入子句是语法错误。

可以嵌套多个，并像任意两个子查询一样连接：

```psql
SELECT d.name #>> '{}' AS director, a.name #>> '{}' AS actor
FROM (MATCH (p:person)-[:directed]->(:movie {title: 'The Matrix'}) RETURN p.name AS name) d
CROSS JOIN (MATCH (p:person)-[:acted_in]->(:movie {title: 'The Matrix'}) RETURN p.name AS name) a
ORDER BY director, actor LIMIT 4;
```

```
    director     |       actor        
-----------------+--------------------
 Lana Wachowski  | Carrie-Anne Moss
 Lana Wachowski  | Keanu Reeves
 Lana Wachowski  | Laurence Fishburne
 Lilly Wachowski | Carrie-Anne Moss
```

## 把图连接到普通表 {#joining-a-graph-to-an-ordinary-table}

这是多数人来到本页的原因。先向图提出图问题，再把答案连接到关系数据：

```psql
SELECT q.title #>> '{}' AS film, r.score
FROM (MATCH (:person {name: 'Christopher Nolan'})-[:directed]->(m:movie) RETURN m.title AS title) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score 
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

两侧的 `#>> '{}'` 就是全部诀窍，[下一节](#getting-a-plain-value-out)会解释它。没有它，你在比较 `jsonb` 字符串和 `text` 列，类型检查不会通过。

图和表之间没有外键，所以连接键是值：标题、代码、外部 id。如果你能控制模型，就把该 id 存为属性并建索引。

如果连接很热，把它提升为列：`text` 列连接 `text` 列完全不需要转换。参见[把属性提升为列](/zh/agensgraph/querying/typed-columns/)。

## CTE 中的 Cypher 查询 {#a-cypher-query-in-a-cte}

`WITH` 子句接收 Cypher 查询与接收 `SELECT` 一样容易。这给你一个可以多次引用的名称：

```psql
WITH films AS (MATCH (m:movie) WHERE m.year > 2010 RETURN m.title AS title, m.year AS year)
SELECT f.title #>> '{}' AS title, r.score
FROM films f JOIN rating r ON r.title = f.title #>> '{}'
WHERE r.source = 'critics' ORDER BY r.score DESC;
```

```
          title           | score 
--------------------------+-------
 Interstellar             |   8.7
 Blade Runner 2049        |   8.0
 The Avengers             |   8.0
 Elysium                  |   6.6
 The Matrix Resurrections |   5.7
```

注意*语句*是哪种语言。以 `WITH cte AS (...)` 开头的语句是 SQL，其主体必须是 SQL。这不是 Cypher 的 `WITH`；Cypher 的 `WITH` 是流水线分隔符，不能命名子查询。参见[二者如何不同](/zh/agensgraph/querying/composing/#how-it-differs-from-a-cte)。

这个模式可以推广为用关系方式聚合遍历结果。这里 Cypher 统计每部电影的演员数，SQL 计算评分均值：

```psql
WITH cast_size AS (
  MATCH (p:person)-[:acted_in]->(m:movie) RETURN m.title AS title, count(p) AS players
)
SELECT c.title #>> '{}' AS film, c.players #>> '{}' AS players, round(avg(r.score), 2) AS mean_score
FROM cast_size c JOIN rating r ON r.title = c.title #>> '{}'
GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 4;
```

```
            film            | players | mean_score 
----------------------------+---------+------------
 The Matrix                 | 3       |       8.90
 Inception                  | 1       |       8.90
 Interstellar               | 1       |       8.65
 Terminator 2: Judgment Day | 2       |       8.60
```

## Cypher 查询中的 SQL {#sql-inside-a-cypher-query}

嵌套也可以反向工作。SQL 标量子查询是表达式，所以可以放在 Cypher 需要表达式的任何地方：`WHERE`、`RETURN`、正在写入的属性值：

```cypher
MATCH (m:movie)
WHERE m.title = (SELECT title FROM rating WHERE source = 'critics' ORDER BY score DESC LIMIT 1)
RETURN m.title AS title, m.year AS year;
```

```
    title    | year 
-------------+------
 "Inception" | 2010
```

与 SQL 一样，子查询必须返回一行一列。这里不需要转换：子查询的 `text` 与 `jsonb` 属性比较，比较可以解析。需要 `#>> '{}'` 的是另一个方向：把 `jsonb` 属性放入 `text` 列。

用户定义函数也是表达式，所以 Cypher 的 `RETURN` 可以调用 SQL 函数：

```sql
CREATE FUNCTION decade(y int) RETURNS int AS 'SELECT (y / 10) * 10' LANGUAGE sql IMMUTABLE;
```

```cypher
MATCH (m:movie) RETURN decade(m.year::int) AS decade, count(*) AS films ORDER BY decade;
```

```
 decade | films 
--------+-------
 1980   | 2
 1990   | 6
 2000   | 4
 2010   | 5
 2020   | 1
```

`m.year` 上的 `::int` 把 jsonb 属性转换成函数签名接受的参数。任何语言都可以：PL/pgSQL、PL/Python、C。任何聚合或窗口函数也可以，因为 Cypher 的聚合*就是* PostgreSQL 的聚合。

## 得到普通值 {#getting-a-plain-value-out}

Cypher `RETURN` 中任何从属性派生的内容都以 `jsonb` 返回。这不是显示习惯，而是列类型。在查询*内部*转换或解包不会改变它，因为投影会把结果重新装箱。

这是这个边界上最常见的混淆来源，所以下面从每个角度说明。

并非每列都装箱，只有属性派生列装箱。检查 Cypher 子查询列的外层类型可以准确看到规则：

```psql
SELECT pg_typeof(raw) AS raw, pg_typeof(cast_text) AS cast_text,
       pg_typeof(unwrapped) AS unwrapped, pg_typeof(is_modern) AS boolean_expr,
       pg_typeof(gid) AS gid, pg_typeof(v) AS vertex
FROM (MATCH (m:movie {title: 'The Matrix'})
      RETURN m.title AS raw, m.title::text AS cast_text, m.title #>> '{}' AS unwrapped,
             m.year > 1990 AS is_modern, id(m) AS gid, m AS v) q;
```

```
  raw  | cast_text | unwrapped | boolean_expr |   gid   | vertex
-------+-----------+-----------+--------------+---------+--------
 jsonb | jsonb     | jsonb     | boolean      | graphid | vertex
```

布尔表达式保持 `boolean`，`id(m)` 保持 `graphid`，图元素保持 `vertex`、`edge` 或 `graphpath`。三个属性派生列都以 `jsonb` 到达，包括已转换为 `text` 的列和已经解包的列。

字符串属性返回时带 JSON 引号：

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS t;
```

```
      t       
--------------
 "The Matrix"
```

在 Cypher 查询内转换没有帮助，因为外层投影会重新装箱结果：

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title::text AS t;
```

```
      t       
--------------
 "The Matrix"
```

```psql
SELECT pg_typeof(t) AS type FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title::text AS t) q;
```

```
 type  
-------
 jsonb
```

出于同样原因，在 Cypher 内用 `#>> '{}'` 提取文本也没有帮助：

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title #>> '{}' AS t;
```

```
      t       
--------------
 "The Matrix"
```

**出路是在上一层 SQL 中解包。** 包住 Cypher 查询，并在其外应用 `#>> '{}'`。该运算符的含义是 jsonb 的“把空路径上的值提取为 text”：

```psql
SELECT t #>> '{}' AS t FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS t) q;
```

```
     t      
------------
 The Matrix
```

```psql
SELECT pg_typeof(t #>> '{}') AS type FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS t) q;
```

```
 type 
------
 text
```

此后该值像任何 `text` 一样工作：与列比较、传给函数，数字再用 `(q.year #>> '{}')::int` 继续转换。

关于这条规则有三点说明。

它只适用于最外层投影。Cypher 表达式*内部*的属性读取全程保持自身类型，所以上面的 `decade(m.year::int)` 有效。

**已提升**属性是例外。背后有类型列的属性以该列类型返回，而不是 jsonb。因此提升后的 `RETURN m.year` 已经是 `integer`，不需要解包。参见[提升后的读取具有列类型](/zh/agensgraph/querying/typed-columns/#a-promoted-read-has-the-columns-type)。

顶点或边以自己的复合类型返回，而不是 jsonb；SQL 可以用字段表示法拆开：

```psql
SELECT pg_typeof(m) AS type, (m).id AS id, (m).properties->>'title' AS title
FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m) q;
```

```
  type  | id  |   title    
--------+-----+------------
 vertex | 3.1 | The Matrix
```

`m` 两侧的括号属于 SQL；读取复合列字段时始终必需。

## Cypher 查询上的视图 {#a-view-over-a-cypher-query}

视图不能以 Cypher 子句开头：

```psql
CREATE VIEW film_rating AS MATCH (m:movie) RETURN m.title AS title;
```

```
ERROR:  syntax error at or near "MATCH"
```

包进 `SELECT` 就可以。于是图遍历可以作为关系视图发布给任何说 SQL 的东西：BI 工具、ORM、外部数据封装器：

```psql
CREATE VIEW film_rating AS
SELECT q.title #>> '{}' AS title, (q.year #>> '{}')::int AS year, r.score
FROM (MATCH (m:movie) RETURN m.title AS title, m.year AS year) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics';
```

```sql
SELECT * FROM film_rating ORDER BY score DESC LIMIT 4;
```

```
           title            | year | score 
----------------------------+------+-------
 Inception                  | 2010 |   8.8
 Interstellar               | 2014 |   8.7
 The Matrix                 | 1999 |   8.7
 Terminator 2: Judgment Day | 1991 |   8.6
```

视图是普通视图，所以落在 SQL 搜索路径中，而不是图中。`graph_path` 决定标签名属于哪个图；它不决定视图放在哪里：

```sql
SELECT schemaname, viewname FROM pg_views WHERE viewname = 'film_rating';
```

```
 schemaname |  viewname   
------------+-------------
 public     | film_rating
```

### 服务器保存了什么 {#what-the-server-stored}

视图保存解析后的查询树，而不是你的文本。请求定义时，得到的是 Cypher 编译后的 *lowered SQL*，不是你写的 Cypher：

```sql
SELECT pg_get_viewdef('public.film_rating'::regclass, true);
```

```
                            pg_get_viewdef                             
-----------------------------------------------------------------------
  SELECT q.title #>> '{}'::text[] AS title,                           +
     (q.year #>> '{}'::text[])::integer AS year,                      +
     r.score                                                          +
    FROM ( SELECT (_agens_default_s.m).properties.'title' AS title,   +
             (_agens_default_s.m).properties.'year' AS year           +
            FROM ( SELECT ROW(m.id, m.properties, m.ctid)::vertex AS m+
                    FROM moviekb.movie m) _agens_default_s) q         +
      JOIN rating r ON r.title = (q.title #>> '{}'::text[])           +
   WHERE r.source = 'critics'::text;
```

这值得读一次，因为它最清楚地说明 Cypher 查询在这个引擎中*是什么*。`MATCH (m:movie)` 变成对 `moviekb.movie` 的扫描，其行被组装成 `vertex` 值。`m.title` 变成 `(m).properties.'title'`。以 `_agens_default_s` 开头的名称是流水线阶段生成的别名。

由此得到两个后果。

**你的 Cypher 无法从目录恢复。** 像其他 schema 对象一样，把视图源码放进版本控制。这不是视图特有的：任何基于存储查询树构建的对象都记录 lowered 形式，例如规则和物化视图。

**它可以往返。** `pg_dump` 输出同样的 lowered SQL，恢复后会重建可用视图。转储并恢复到新数据库后，定义逐字符相同，视图返回相同行。

因此 Cypher 查询上的视图在运维上可以依赖，即使读回来的内容不是你书写的形式。

有一点要注意：如果 Cypher 把属性解析到[提升列](/zh/agensgraph/querying/typed-columns/)，视图会依赖该列。视图删除前，删除列会被拒绝。这是刻意的；否则视图会静默改变含义。

## 清理 {#clean-up}

```sql
DROP VIEW film_rating;
DROP FUNCTION decade(int);
```

## 接下来去哪里 {#where-to-go-next}

* [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)——这一切为什么可行，以及用 SQL 写标签的两道关卡。
* [组合查询](/zh/agensgraph/querying/composing/)——Cypher 自己的流水线，以及它的 `WITH` 与 CTE 的区别。
* [加载数据](/zh/agensgraph/guides/loading-data/)——把普通表读入图的 `LOAD FROM`。
* [把属性提升为列](/zh/agensgraph/querying/typed-columns/)——用于你持续使用的连接键。
