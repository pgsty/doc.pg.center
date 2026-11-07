---
title: 组合查询
linkTitle: 组合查询
description: Cypher 或 GQL 语句是一条流水线。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/composing.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


Cypher 或 GQL 语句是一条流水线。每个子句接收行流，对它做一件事，并把结果交给下一个子句。`MATCH` 产生行，`WHERE` 删除一些行，`WITH` 重塑它们，`RETURN` 结束语句。

这与 SQL 的思维模型不同：SQL 的 `SELECT` 是单个块，命名部分按固定顺序求值；这里顺序就是你书写的顺序。一个查询可以匹配、聚合、过滤聚合结果、从幸存行再次匹配、再次聚合，而不需要子查询、CTE 或 `HAVING`。

本文所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## WITH 是分隔符 {#with-is-the-divider}

`WITH` 结束流水线的一部分并开始下一部分。它的投影列表与 `RETURN` 完全一样；只有它列出的名称会留在作用域中：

```cypher
MATCH (d:person)-[:directed]->(m:movie)
WITH d, count(m) AS films
WHERE films > 2
RETURN d.name AS director, films ORDER BY films DESC, director;
```

```
     director      | films 
-------------------+-------
 "Lana Wachowski"  | 4
 "James Cameron"   | 3
 "Lilly Wachowski" | 3
```

`m` 在 `WITH` 后消失；剩下的是 `d` 和 `films`。其后的 `WHERE` 过滤聚合值，也就是 SQL 中需要 `HAVING` 的工作。

`WITH` 内部顺序固定，值得记住：先 `WHERE`，再 `ORDER BY`，最后 `SKIP` 和 `LIMIT`。因此下面先过滤出五部电影，再取其中两部，而不是先取两部再过滤：

```cypher
MATCH (m:movie) WITH m.year AS y WHERE y > 2010 ORDER BY y LIMIT 2 RETURN y;
```

```
  y   
------
 2012
 2013
```

一个名称只能向下传递一次：

```cypher
MATCH (m:movie) WITH m.year AS y, m.genre AS y RETURN y;
```

```
ERROR:  WITH passes on "y" more than once
```

### 它与 CTE 的区别 {#how-it-differs-from-a-cte}

两种语言都有 `WITH` 关键字，而且它们会划分查询，但不是同一个关键字。

SQL CTE *有名字并被引用*：声明 `WITH films AS (...)` 后，可以在任何位置按任意次数提到 `films`。

Cypher 的 `WITH` 是*位置性的*：没有名字，通过“在下一步”被引用，而且恰好消费一次。无法把 Cypher 流水线分成两个分支再合并。

二者不能混用。Cypher 的 `WITH` 不能引入命名子查询：`WITH d AS (MATCH ...)` 是语法错误。但 SQL CTE 可以保存 Cypher 查询；需要 CTE 行为时，这就是使用方式：

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

外层语句是 SQL，因为以 SQL CTE 开头的语句就是 SQL 语句。[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)专讲这条边界。

这也是 Cypher 流水线不能以 `WITH` *开始*的原因。开头的 `WITH` 会被读作 CTE，所以解析器期待名称和括号中的查询：

```cypher
WITH 1 AS x RETURN x;
```

```
ERROR:  syntax error at or near "1"
LINE 1: WITH 1 AS x RETURN x;
             ^
```

[`LET`](#the-gql-clauses)没有这种冲突，因此它是用计算值开启语句的子句：

```cypher
LET x = 1 RETURN x;
```

```
 x
---
 1
```

## 聚合 {#aggregation}

聚合就是 PostgreSQL 的聚合，分组是隐式的：投影列表中不在聚合内部的每一项都成为分组键。

```cypher
MATCH (m:movie) RETURN m.genre AS genre, count(*) AS films, min(m.year) AS earliest ORDER BY genre;
```

```
    genre    | films | earliest 
-------------+-------+----------
 "Action"    | 7     | 1984
 "Adventure" | 1     | 1993
 "Sci-Fi"    | 10    | 1982
```

`count(*)` 统计行；`count(x)` 统计 `x` 非 null 的行。这让 `count(x)` 在 `OPTIONAL MATCH` 后有用。`count(DISTINCT x)` 统计去重值；两者差距通常就是模式的扇出：

```cypher
MATCH (:person)-[:acted_in]->(m:movie) RETURN count(m) AS rows, count(DISTINCT m) AS films;
```

```
 rows | films 
------+-------
 25   | 18
```

`collect()` 是你最常用的聚合，因为它把扇出重新变成一行。对顶点、边或路径聚合时，它构造这些元素的原生数组，收集到的元素仍可使用：

```cypher
MATCH (p:person)-[:acted_in]->(m:movie {title: 'The Matrix'})
WITH collect(p) AS players
RETURN pg_typeof(players) AS type, cardinality(players) AS n, players[1].name AS first;
```

```
    type    | n |        first         
------------+---+----------------------
 "vertex[]" | 3 | "Laurence Fishburne"
```

对*属性*使用 `collect()` 仍返回 jsonb 列表，因此存储数据保持自身形状。

整个投影上的 `DISTINCT` 对行去重；当模式经多条路线到达同一事物时，需要的正是它：

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie)<-[:acted_in]-(co:person)
RETURN DISTINCT co.name AS co_actor ORDER BY co_actor;
```

```
       co_actor
----------------------
 "Carrie-Anne Moss"
 "Laurence Fishburne"
```

## UNWIND {#unwind}

`UNWIND` 与 `collect()` 相反：接收列表，并为每个元素产生一行。

```cypher
UNWIND [1999, 2010, 2014] AS y MATCH (m:movie {year: y}) RETURN y, m.title AS title ORDER BY y, title;
```

```
  y   |     title      
------+----------------
 1999 | "The Matrix"
 2010 | "Inception"
 2014 | "Interstellar"
```

它也会展开同一条流水线中更早构建的列表；这就是先按聚合过滤、再回到每元素一行的方法：

```cypher
MATCH (m:movie)<-[:acted_in]-(p:person)
WITH m, collect(p) AS players
WHERE cardinality(players) > 2
UNWIND players AS actor
RETURN m.title AS film, actor.name AS actor ORDER BY actor;
```

```
     film     |        actor         
--------------+----------------------
 "The Matrix" | "Carrie-Anne Moss"
 "The Matrix" | "Keanu Reeves"
 "The Matrix" | "Laurence Fishburne"
```

[`FOR`](/zh/agensgraph/reference/clauses/for/)是 GQL 拼写，并额外提供元素从 0 开始索引的 `WITH OFFSET`。参见 [`UNWIND`](/zh/agensgraph/reference/clauses/unwind/)。

## 排序与分页 {#ordering-and-paging}

`ORDER BY`、`SKIP`、`OFFSET` 和 `LIMIT` 本身就是子句。它们可以像 SQL 一样放在 `RETURN` 或 `WITH` 末尾：

```cypher
MATCH (m:movie) RETURN m.title AS title, m.year AS year ORDER BY year SKIP 2 LIMIT 3;
```

```
            title             | year 
------------------------------+------
 "Total Recall"               | 1990
 "Terminator 2: Judgment Day" | 1991
 "Jurassic Park"              | 1993
```

也可以独立放在流水线中间；`RETURN` 形式做不到这一点：

```cypher
MATCH (m:movie) LET y = m.year ORDER BY y LIMIT 3 RETURN m.title AS title, y;
```

```
      title       |  y   
------------------+------
 "Blade Runner"   | 1982
 "The Terminator" | 1984
 "Total Recall"   | 1990
```

它们不能*结束*语句：查询仍必须以 `RETURN`、`FINISH` 或写入子句结束。

排序键按它本身的值排序，而不是按它的 jsonb 表示排序，因此属性上的索引可以服务排序。这正是值得关心它的原因：[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/#ordering)。

## UNION {#union}

`UNION` 堆叠两个列名相同的结果集并去重。`UNION ALL` 保留重复。

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS name
UNION
MATCH (p:person {name: 'Keanu Reeves'}) RETURN p.name AS name;
```

```
      name      
----------------
 "Keanu Reeves"
 "The Matrix"
```

这也是绕开缺失边标签交替的干净方法：两个窄模式取并集时扫描两张边表，而一个无类型模式会扫描全部边表。参见[读取图](/zh/agensgraph/querying/reading/#one-label-per-edge)。

## GQL 子句 {#the-gql-clauses}

四个 ISO/IEC 39075 子句完成 Cypher 需要多个子句才能完成的工作。它们与其他子句接受在同一条语句中，没有单独模式。

`LET` 添加计算值，而不丢弃作用域中的任何内容。`WITH` 要求列出每个仍想要的变量；`LET` 全部保留：

```cypher
MATCH (m:movie) LET decade = (m.year / 10) * 10 FILTER decade = 2010
RETURN m.title AS title, m.year AS year, decade ORDER BY year;
```

```
        title        | year | decade 
---------------------+------+--------
 "Inception"         | 2010 | 2010
 "The Avengers"      | 2012 | 2010
 "Elysium"           | 2013 | 2010
 "Interstellar"      | 2014 | 2010
 "Blade Runner 2049" | 2017 | 2010
```

`FILTER` 只过滤行，不做其他事，因此过滤器不再必须附加到 `WITH`。它接受裸谓词或 `FILTER WHERE` 拼写。

`NEXT` 把一个查询链接到另一个查询的结果上；这就是不用 `WITH` 在投影后过滤的方法：

```cypher
MATCH (m:movie) RETURN m.genre AS genre, count(*) AS films
NEXT FILTER films > 3
RETURN genre, films ORDER BY genre;
```

```
  genre   | films 
----------+-------
 "Action" | 7
 "Sci-Fi" | 10
```

`FINISH` 结束不投影任何内容的查询；对为效果而运行的语句，它是 `RETURN` 的对应形式：

```cypher
MATCH (m:movie {title: 'The Matrix'}) FINISH;
```

```
--
(0 rows)
```

每个子句都有参考页：[`LET`](/zh/agensgraph/reference/clauses/let/)、[`FILTER`](/zh/agensgraph/reference/clauses/filter/)、[`NEXT`](/zh/agensgraph/reference/clauses/next/)、[`FINISH`](/zh/agensgraph/reference/clauses/finish/)。

## 子查询 {#subqueries}

`CALL { }` 对每个输入行运行一次子查询，并把结果连接回来。当每行需要的是整个查询而不是表达式时使用它：按行聚合、按行 Top-N。

它的一切都很普通，除了一点；这一点改变答案，而不是抛出错误。

> [!IMPORTANT]
> 没有 import 清单的 `CALL { }` **不会**导入外层变量。主体内使用且外层也存在的名称会重新绑定为全新的、无约束变量，于是子查询遍历整张图，而不是当前行。始终写 import 清单。

区别如下。`m` 在外部绑定，主体提到 `m`，而每部电影的答案都相同：

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 3;
```

```
        film         | cast_size 
---------------------+-----------
 "Avatar"            | 25
 "Blade Runner"      | 25
 "Blade Runner 2049" | 25
```

25 是图中全部 `acted_in` 边。子查询的 `m` 不是外层的 `m`。

命名 import 后就正确了：

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL (m) { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 3;
```

```
        film         | cast_size 
---------------------+-----------
 "Avatar"            | 1
 "Blade Runner"      | 1
 "Blade Runner 2049" | 2
```

`CALL (*) { ... }` 导入作用域中的全部内容；`CALL { WITH m ... }` 是同一件事的旧拼写。三者一致。

子查询不能交回已经在外部绑定的名称：

```cypher
MATCH (m:movie) CALL (m) { MATCH (p:person)-[:acted_in]->(m) RETURN m AS m } RETURN count(*);
```

```
ERROR:  variable "m" returned by the CALL subquery is already bound in the outer query
```

子查询主体中不允许写入子句。`OPTIONAL CALL` 是左连接形式，即使主体不产生结果也生成一行。参见 [`CALL { }`](/zh/agensgraph/reference/clauses/call-subquery/) 和 [`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/)。

### 作为值的子查询 {#subqueries-as-values}

六种值表达式接收子查询，并把它归约成可以放进 `WHERE` 或 `RETURN` 的值。它们不需要 import 清单，因为外层变量作为表达式在作用域中，而不是作为单独查询。

`EXISTS { }` 在子查询返回任意行时为真：

```cypher
MATCH (p:person) WHERE EXISTS { MATCH (p)-[:directed]->(:movie) } RETURN count(p) AS directors;
```

```
 directors 
-----------
 12
```

`COUNT { }` 是它返回的行数：

```cypher
MATCH (m:movie) WHERE COUNT { MATCH (:person)-[:acted_in]->(m) } > 2
RETURN m.title AS title ORDER BY title;
```

```
    title     
--------------
 "The Matrix"
```

`COLLECT { }` 和 `ARRAY { }` 把单一列收集为列表：

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COLLECT { MATCH (p:person)-[:acted_in]->(m) RETURN p.name ORDER BY p.name } AS players;
```

```
                          players                           
------------------------------------------------------------
 ["Carrie-Anne Moss", "Keanu Reeves", "Laurence Fishburne"]
```

`VALUE { }` 取它的单一值：

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN VALUE { MATCH (p:person)-[:directed]->(m) RETURN p.name ORDER BY p.name LIMIT 1 } AS a_director;
```

```
    a_director    
------------------
 "Lana Wachowski"
```

`x IN { }` 测试成员关系：

```cypher
MATCH (p:person)
WHERE p.name IN { MATCH (d:person)-[:directed]->(:movie {title: 'Inception'}) RETURN d.name }
RETURN p.name AS name;
```

```
        name         
---------------------
 "Christopher Nolan"
```

`EXISTS { }` 是最常用的，因为裸模式不是谓词。参见[读取图](/zh/agensgraph/querying/reading/#asking-whether-a-pattern-exists)。六个表达式都在[子查询表达式](/zh/agensgraph/reference/clauses/subquery-expressions/)中定义。

## 接下来去哪里 {#where-to-go-next}

* [路径](/zh/agensgraph/querying/paths/)——长度未知的模式。
* [组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)——CTE、与普通表连接、视图。
* [调优查询](/zh/agensgraph/querying/performance/)——流水线在执行计划中的样子。
