---
title: 读取图
linkTitle: 读取图
description: 每次读取都从模式开始。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/reading.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


每次读取都从模式开始。模式是你寻找形状的图画，用 ASCII 写成：括号表示顶点，方括号和短线表示边。`MATCH` 把这幅图交给规划器；规划器把它转换成扫描和连接，并在数据每适配这幅图的一种方式上返回一行。

本页讨论这幅图，以及规划器对它做什么。正式语法见 [`MATCH`](/zh/agensgraph/reference/clauses/match/) 和 [`WHERE`](/zh/agensgraph/reference/clauses/where/)；这里的所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## 一个顶点 {#one-vertex}

最小的模式是一对括号。加上标签，可以把它缩小到一张表：

```cypher
MATCH (m:movie) RETURN m.title AS title ORDER BY title LIMIT 3;
```

```
        title        
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
```

`m` 是绑定到每个匹配顶点的变量；`movie` 是标签。两者都可以省略。`(m)` 匹配每个顶点，`(:movie)` 匹配每部电影但不命名，`()` 匹配每个顶点且不命名。

命名标签会包含继承它的标签。`ONLY` 排除它们：

```cypher
MATCH (m:movie ONLY) RETURN count(m) AS films;
```

```
 films 
-------
 18
```

这里没有标签继承自 `movie`，所以两种写法计数相同。在层级上，差异就是整个 `Append`。参见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。

## 两种收窄方式 {#two-ways-to-narrow}

模式内的属性映射按相等性测试属性：

```cypher
MATCH (m:movie {genre: 'Adventure'}) RETURN m.title AS title, m.year AS year;
```

```
      title      | year 
-----------------+------
 "Jurassic Park" | 1993
```

`WHERE` 接受任何谓词，因此所有非相等条件都放到那里：

```cypher
MATCH (m:movie) WHERE m.year >= 2017 RETURN m.title AS title, m.year AS year ORDER BY year;
```

```
           title            | year 
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
```

两者可以组合；对普通 `MATCH` 来说，它们含义完全相同。无论怎么写，规划器都会收到同一个合取：

```cypher
MATCH (m:movie {genre: 'Action'}) WHERE m.year < 2000
RETURN m.title AS title, m.year AS year ORDER BY year;
```

```
            title             | year 
------------------------------+------
 "The Terminator"             | 1984
 "Terminator 2: Judgment Day" | 1991
 "The Matrix"                 | 1999
```

用映射写识别目标对象的键，用 `WHERE` 写它身上的条件。唯一一个选择有影响的位置是下文的 [`OPTIONAL MATCH`](#a-pattern-that-may-not-fit)。

条件必须是布尔值。`WHERE m.title` 不表示“有标题”；它会抛出 `ERROR: cannot cast "The Matrix" (jsonb type string) to boolean`。写出你真正要的测试：`WHERE m.title IS NOT NULL`。

## 一条边 {#an-edge}

边是写在两条短线之间的方括号，箭头表示方向：

```cypher
MATCH (p:person)-[]->(m:movie {title: 'Blade Runner 2049'})
RETURN p.name AS person ORDER BY person;
```

```
       person       
--------------------
 "Denis Villeneuve"
 "Harrison Ford"
 "Ryan Gosling"
```

注意空方括号。方括号不能省略：`-->` 和 `--` 不是模式，因为 `--` 开始 SQL 行注释。`MATCH (p:person)-->(m:movie) RETURN count(p)` 会把第一个短线之后的内容全部注释掉，并以 `ERROR: Cypher query
must end with RETURN, FINISH or update clause` 失败。写 `-[]->` 和 `-[]-`。

把边绑定到变量后，它的标签和属性就可以访问：

```cypher
MATCH (p:person)-[r]->(m:movie {title: 'Blade Runner 2049'})
RETURN p.name AS person, label(r) AS via, r.role AS role ORDER BY person;
```

```
       person       |    via     |      role      
--------------------+------------+----------------
 "Denis Villeneuve" | "directed" | 
 "Harrison Ford"    | "acted_in" | "Rick Deckard"
 "Ryan Gosling"     | "acted_in" | "K"
```

`label(r)` 是边的标签，`r.role` 是边自身的属性。`directed` 边没有 `role`，所以该单元格为 null。

### 方向 {#direction}

`-[]->` 按存储方向遍历边，`<-[]-` 反向遍历，`-[]-` 忽略方向。方向属于查询，不属于数据：你按一个方向存储边，并在每个模式中决定它是否重要。

```cypher
MATCH (a:movie {title: 'The Matrix Reloaded'})-[:related_to]->(b:movie)
RETURN b.title AS neighbour ORDER BY neighbour;
```

```
        neighbour         
--------------------------
 "The Matrix Revolutions"
```

```cypher
MATCH (a:movie {title: 'The Matrix Reloaded'})-[:related_to]-(b:movie)
RETURN b.title AS neighbour ORDER BY neighbour;
```

```
        neighbour         
--------------------------
 "The Matrix"
 "The Matrix Revolutions"
```

### 每条边一个标签 {#one-label-per-edge}

边模式最多命名一个标签。没有交替语法：

```cypher
MATCH (p:person)-[r:acted_in|directed]->(m:movie) RETURN count(r);
```

```
ERROR:  multiple types for relationship not supported
```

这个限制适用于所有长度，也适用于 `shortestpath` 内部。保留边不带类型，并用谓词测试标签：

```cypher
MATCH (p:person)-[r]->(m:movie {title: 'Blade Runner'})
WHERE label(r) IN ['acted_in', 'directed']
RETURN p.name AS person, label(r) AS via ORDER BY person;
```

```
     person      |    via     
-----------------+------------
 "Harrison Ford" | "acted_in"
 "Ridley Scott"  | "directed"
```

这种形式有代价：无类型边会扫描图中每个边标签，标签测试在之后应用。当交替只覆盖少数标签而图很大时，用 [`UNION`](/zh/agensgraph/reference/clauses/union/) 连接两个模式可以让每个扫描保持狭窄。

## 一条完整路径 {#a-whole-path}

模式前的 `p = ` 绑定路径本身，而不只是两端：

```cypher
MATCH p = (a:person {name: 'Ryan Gosling'})-[:acted_in]->(m:movie)
RETURN length(p) AS hops,
       [x IN nodes(p) | label(x)] AS labels,
       [r IN relationships(p) | label(r)] AS edges;
```

```
 hops |       labels        |    edges     
------+---------------------+--------------
 1    | ["person", "movie"] | ["acted_in"]
```

`length(p)` 是边数，`nodes(p)` 是按顺序排列的顶点，`relationships(p)` 是边。路径是一个值：可以返回它、按长度排序或收集它。[路径](/zh/agensgraph/querying/paths/)介绍其余内容，包括长度未知的模式。

## 多个模式 {#more-than-one-pattern}

`MATCH` 接受逗号分隔的模式列表。出现在两个模式中的变量会把它们连接起来：

```cypher
MATCH (d:person)-[:directed]->(m:movie), (a:person)-[:acted_in]->(m)
RETURN d.name AS director, a.name AS actor, m.title AS film
ORDER BY film, actor LIMIT 5;
```

```
      director      |       actor       |        film         
--------------------+-------------------+---------------------
 "James Cameron"    | "Sam Worthington" | "Avatar"
 "Ridley Scott"     | "Harrison Ford"   | "Blade Runner"
 "Denis Villeneuve" | "Harrison Ford"   | "Blade Runner 2049"
 "Denis Villeneuve" | "Ryan Gosling"    | "Blade Runner 2049"
 "Neill Blomkamp"   | "Matt Damon"      | "Elysium"
```

`m` 由第一个模式绑定，并被第二个模式复用。因此这是按电影的内连接，而不是笛卡尔积。两个没有公共变量的模式*确实是*笛卡尔积；这合法，而且偶尔正是你想要的：

```cypher
MATCH (p:person {name: 'Keanu Reeves'}), (m:movie {genre: 'Adventure'})
RETURN p.name AS person, m.title AS film;
```

```
     person     |      film       
----------------+-----------------
 "Keanu Reeves" | "Jurassic Park"
```

把两个模式写成两个连续的 `MATCH` 子句含义相同。对于上面的导演与演员查询，逗号形式和双子句形式都产生 31 行，执行计划形状也相同。选择读起来更清楚的形式：逗号表示“这些事物在一起”，第二个 `MATCH` 表示“然后”。

## 可能不适配的模式 {#a-pattern-that-may-not-fit}

如果某行的模式什么也没找到，`MATCH` 会丢弃该行：

```cypher
MATCH (p:person {name: 'Ridley Scott'})-[:acted_in]->(m:movie)
RETURN p.name AS person, m.title AS film;
```

```
 person | film 
--------+------
(0 rows)
```

`OPTIONAL MATCH` 保留该行，并把模式中的变量留为 null。它是左连接，并且在每个方面都像左连接一样工作：

```cypher
MATCH (p:person {name: 'Ridley Scott'})
OPTIONAL MATCH (p)-[:acted_in]->(m:movie)
RETURN p.name AS person, m.title AS film;
```

```
     person     | film 
----------------+------
 "Ridley Scott" | 
```

正是在这里，属性映射和 `WHERE` 不再等价。写在 `OPTIONAL MATCH` *之上*的 `WHERE` 属于连接条件，因此未通过它的行会带 null 存活：

```cypher
MATCH (m:movie {title: 'The Matrix'})
OPTIONAL MATCH (m)<-[r:acted_in]-(p:person) WHERE r.role = 'Agent Smith'
RETURN m.title AS film, p.name AS actor;
```

```
     film     | actor 
--------------+-------
 "The Matrix" | 
```

同一个谓词晚一个子句出现，就是对连接结果过滤，并会丢弃该行：

```cypher
MATCH (m:movie {title: 'The Matrix'})
OPTIONAL MATCH (m)<-[r:acted_in]-(p:person)
WITH m, p, r WHERE r.role = 'Agent Smith'
RETURN m.title AS film, p.name AS actor;
```

```
 film | actor 
------+-------
(0 rows)
```

如果你了解 SQL，就已经见过这一点：这是 `LEFT JOIN` 后条件写在 `ON` 中与写在 `WHERE` 中的区别。参见 [`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/)。

## 询问模式是否存在 {#asking-whether-a-pattern-exists}

模式本身不是谓词。`WHERE (p)-[:acted_in]->(:movie)` 是语法错误。把它放进 `EXISTS { }` 子查询：

```cypher
MATCH (p:person)
WHERE EXISTS { MATCH (p)-[:acted_in]->(:movie {title: 'The Matrix'}) }
RETURN p.name AS actor ORDER BY actor;
```

```
        actor         
----------------------
 "Carrie-Anne Moss"
 "Keanu Reeves"
 "Laurence Fishburne"
```

`EXISTS`、`COUNT`、`COLLECT`、`ARRAY`、`VALUE` 和 `IN` 都接受这样的子查询。[组合查询](/zh/agensgraph/querying/composing/#subqueries-as-values)会一起介绍它们。

## 模式如何变成执行计划 {#how-a-pattern-becomes-a-plan}

模式不会按“走图”执行。它被编译成标签表上的普通关系代数，`EXPLAIN` 显示的正是这一点：

```cypher
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->(m:movie) RETURN p.name, m.title;
```

```
                                                                               QUERY PLAN                                                                                
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r.start = p.id)
   ->  Hash Join
         Hash Cond: (r."end" = m.id)
         ->  Seq Scan on acted_in r
               Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
         ->  Hash
               ->  Seq Scan on movie m
   ->  Hash
         ->  Seq Scan on person p
```

有三点值得读出来。

每个模式元素都是一次扫描。`person`、`acted_in` 和 `movie` 是三张表，模式就是它们之间的两个连接：`r.start = p.id` 和 `r."end" = m.id`。遍历边*就是*按 `graphid` 连接。因此每个边标签自带的 `(start, "end")` 和 `("end", start)` 索引非常重要。

端点上的标签测试在边上回答。`p` 是 `person`，所以 `r.start` 只能是 `person` 的 id。标签 id 位于 `graphid` 高位，因此一个标签的所有 id 构成连续范围。

规划器把“`start` 是 person”转换成 `start >= '4.0' AND start <= '4.281474976710655'`。这个范围测试可以下推到边扫描或其索引，完全不必访问 `person`。参见[身份：graphid](/zh/agensgraph/concepts/graph-on-postgresql/#identity-the-graphid)。

锚定模式会改变连接顺序。把一端固定到单个顶点后，执行计划不再哈希整表：

```cypher
EXPLAIN (COSTS OFF)
MATCH (p:person {name: 'Keanu Reeves'})-[r:acted_in]->(m:movie) RETURN m.title;
```

```
                                                                                              QUERY PLAN                                                                                              
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Nested Loop
   ->  Nested Loop
         ->  Seq Scan on person p
               Filter: (properties.'name' = '"Keanu Reeves"'::jsonb)
         ->  Bitmap Heap Scan on acted_in r
               Recheck Cond: ((p.id = start) AND (start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
               ->  Bitmap Index Scan on acted_in_start_idx
                     Index Cond: ((start = p.id) AND (start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid) AND ("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid))
   ->  Index Scan using movie_pkey on movie m
         Index Cond: (id = r."end")
```

现在，`acted_in` 通过 `acted_in_start_idx` 从这一个人访问，`movie` 通过主键从每条找到的边访问。

这就是从已知起点遍历时想要的形状。这也是有选择性的锚点（带有索引的属性）通常比其他调优更值得的原因。[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)介绍哪些谓词可以充当锚点。

## 不使用的端点有什么代价 {#what-an-endpoint-you-do-not-use-costs}

查询从不读取其值的端点完全不必取回。这里 `m` 被绑定并有标签，但投影中没有任何内容请求它：

```cypher
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->(m:movie) RETURN p.name;
```

```
                                                                            QUERY PLAN                                                                             
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r.start = p.id)
   ->  Seq Scan on acted_in r
         Filter: (("end" >= '3.0'::graphid) AND ("end" <= '3.281474976710655'::graphid) AND (start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
   ->  Hash
         ->  Seq Scan on person p
```

没有 `m` 的扫描。它剩下的唯一贡献是过滤条件的后半部分：`"end"` 必须在 `movie` 范围内。于是整个 `(m:movie)` 折叠成边扫描本来就要读的列上的两个比较。

关闭这项省略后，查询从未请求的顶点会在整个 `ag_vertex` 家族上取回：

```cypher
SET enable_graph_endpoint_elision = off;
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->(m) RETURN p.name;
```

```
                                          QUERY PLAN                                           
-----------------------------------------------------------------------------------------------
 Hash Join
   Hash Cond: (r."end" = m.id)
   ->  Hash Join
         Hash Cond: (r.start = p.id)
         ->  Seq Scan on acted_in r
               Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
         ->  Hash
               ->  Seq Scan on person p
   ->  Hash
         ->  Append
               ->  Seq Scan on ag_vertex m_1
               ->  Seq Scan on movie m_2
               ->  Seq Scan on person m_3
```

该设置默认开启；除了本例这样的实验，没有理由关闭它。

这个对比显示了节省的规模，也显示了它的边界。给那个 `RETURN` 加上 `m.title`，`Append` 就会回来，因为查询确实需要电影。只投影你使用的端点。

> [!NOTE]
> 如果打算保留执行计划，请命名模式中每个元素。未命名元素会得到 `"<0000000002>"` 这样的合成别名；它背后的计数器在每条语句上都会前进，所以同一个查询第二次运行会打印不同的计划。

> [!NOTE]
> 匿名并非处处免费。`shortestpath` 的两个端点必须都是命名变量，即使从不使用——匿名端点会得到 `ERROR: node must be a reference to a specific node`。

## 接下来去哪里 {#where-to-go-next}

* [组合查询](/zh/agensgraph/querying/composing/)——`WITH`、聚合、子查询，以及跟随 `MATCH` 之后的其余流水线。
* [路径](/zh/agensgraph/querying/paths/)——变长边、最短路径和加权搜索。
* [写入图](/zh/agensgraph/querying/writing/)——同一批模式后接写入子句。
* [索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)——索引可以服务哪些谓词。
