---
title: 第一个查询
linkTitle: 第一个查询
description: 使用电影示例数据学习设置图路径、匹配顶点、沿边遍历、聚合和写入。
type: docs
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/get_started/first-query.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
weight: 40
translation_status: complete
---


本页带你查询[示例数据集](/zh/agensgraph/get-started/example-dataset/)：18 部电影、28 个人物，以及连接它们的边。请先加载数据，再按顺序执行下面的查询，后面的查询会以前面的内容为基础。

这里全部使用 Cypher。[参考手册](/zh/agensgraph/reference/clauses/)会注明等价的 GQL 写法；[组合 SQL 和 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)则重新引入 SQL。

## 指定要使用的图 {#say-which-graph-you-mean}

```cypher
SET graph_path = moviekb;
```

这是 Cypher 所需的一项会话状态。没有它，所有标签名都无法解析。现在统计图中的全部顶点：

```cypher
MATCH (n) RETURN count(n) AS elements;
```

```
 elements
----------
       46
```

`MATCH (n)` 是最简单的模式：一个顶点，没有标签，也没有属性，因此会匹配所有顶点。46 来自 18 部电影与 28 个人物之和。

## 查找一个对象 {#find-one-thing}

模式可以通过两种方式缩小范围：标签与属性。

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.year AS year, m.genre AS genre;
```

```
 year |  genre
------+----------
 1999 | "Action"
```

`(m:movie {title: 'The Matrix'})` 表示：一个标签为 `movie`、`title` 属性为 `'The Matrix'` 的顶点，并将它绑定到变量 `m`。随后 `RETURN` 从 `m` 中投影所需的值。

注意 `"Action"` 带有引号，而 `1999` 没有。`RETURN` 以 `jsonb` 返回属性，因此字符串带有 JSON 引号。将结果与客户端字符串比较之前，需要了解这一点。如何取得普通值，参见[组合 SQL 和 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/#getting-a-plain-value-out)。

每个顶点还有一个独立于属性的标识：

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS title, id(m) AS id;
```

```
    title     | id
--------------+-----
 "The Matrix" | 3.1
```

`3.1` 是 `graphid`，表示标签 3 的第 1 行。它是顶点的标识，通过 `id(m)` 获取。`m.id` 则会寻找名为 `id` 的*属性*，而这些电影都没有该属性。

## 沿一条边查询 {#follow-an-edge}

接下来的关系才是图的重点。在模式中加入一条边：

```cypher
MATCH (p:person)-[r:acted_in]->(:movie {title: 'The Matrix'})
RETURN p.name AS actor, r.role AS role
ORDER BY actor;
```

```
        actor         |    role
----------------------+------------
 "Carrie-Anne Moss"   | "Trinity"
 "Keanu Reeves"       | "Neo"
 "Laurence Fishburne" | "Morpheus"
```

这里有三个新点。`-[r:acted_in]->` 是标签为 `acted_in`、从人物指向电影的边。它绑定到 `r`，因此可以读取其属性：`r.role` 是*关系*的属性，不属于任一端点。`(:movie {title: 'The Matrix'})` 没有变量，因为模式需要到达该电影，但投影不引用它。

## 沿两条边查询 {#follow-two}

将模式向另一个方向扩展，就能提出一个需要 SQL 自连接才能回答的问题：

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie)<-[:acted_in]-(co:person)
RETURN DISTINCT co.name AS co_actor
ORDER BY co_actor;
```

```
       co_actor
----------------------
 "Carrie-Anne Moss"
 "Laurence Fishburne"
```

从左向右读取模式：从 Keanu Reeves 出发，沿一条 `acted_in` 边到达电影，再*反向*沿另一条 `acted_in` 边到达第二个人。这里需要 `DISTINCT`，因为两个人共同出演三部电影时，会产生三行结果。

## 聚合 {#aggregate}

聚合函数来自 PostgreSQL，行为与你预期的一样：

```cypher
MATCH (d:person)-[:directed]->(m:movie)
RETURN d.name AS director, count(m) AS films
ORDER BY films DESC, director
LIMIT 5;
```

```
      director       | films
---------------------+-------
 "Lana Wachowski"    | 4
 "James Cameron"     | 3
 "Lilly Wachowski"   | 3
 "Christopher Nolan" | 2
 "Steven Spielberg"  | 2
```

`RETURN` 中没有放在聚合函数内部的表达式都会成为分组键，这一点也与 SQL 相同。

## 查询可能不存在的对象 {#ask-for-something-that-might-not-be-there}

模式匹配失败时，`MATCH` 会丢弃该行。`OPTIONAL MATCH` 则保留该行，并将缺失的变量填为 null，相当于左连接：

```cypher
MATCH (d:person)-[:directed]->(:movie)
WITH DISTINCT d
OPTIONAL MATCH (d)-[:acted_in]->(m:movie)
RETURN d.name AS director, m.title AS also_acted_in
ORDER BY director
LIMIT 6;
```

```
      director       | also_acted_in
---------------------+---------------
 "Andrew Niccol"     |
 "Christopher Nolan" |
 "Denis Villeneuve"  |
 "James Cameron"     |
 "Joss Whedon"       |
 "Lana Wachowski"    |
```

数据集中没有人既执导又出演电影，因此每个 `also_acted_in` 都是 null。这正是示例要说明的：如果使用普通 `MATCH`，这六行都会消失。

中间的 `WITH` 是查询流水线的分界。它结束前一部分，开始下一部分，因此可以在执行可选匹配之前，对导演应用 `DISTINCT`。

## 遍历未知跳数的路径 {#walk-an-unknown-number-of-hops}

不知道具体路径时，也可以查询两个人如何连接：

```cypher
MATCH p = shortestpath((a:person {name: 'Keanu Reeves'})-[*..6]-(b:person {name: 'Arnold Schwarzenegger'}))
RETURN length(p) AS hops;
```

```
 hops
------
 3
```

`[*..6]` 表示变长边：最多六条，标签不限，方向不限。`p = ...` 将整个路径绑定到变量，`length(p)` 返回其中的边数。这类查询没有合理的直接 SQL 写法。

`shortestpath` 的两个端点都需要变量，即使后续不会使用。将端点写成匿名形式会报错：`ERROR: node must be a reference to a specific node`。

[路径](/zh/agensgraph/querying/paths/)介绍其余内容：有界范围、`allshortestpaths`，以及使用 `dijkstra` 的加权搜索。

## 写入数据 {#write-something}

写入与读取的模式很相似，只是使用不同的动词。`CREATE` 创建顶点：

```cypher
CREATE (p:person {name: 'Hugo Weaving', born: 1960}) RETURN p;
```

```
                         p
----------------------------------------------------
 person[4.63]{"born": 1960, "name": "Hugo Weaving"}
```

要将它连接到其他对象，先找到两个端点，再创建边：

```cypher
MATCH (p:person {name: 'Hugo Weaving'}), (m:movie {title: 'The Matrix'})
CREATE (p)-[r:acted_in {role: 'Agent Smith'}]->(m)
RETURN r;
```

```
                        r
-------------------------------------------------
 acted_in[5.60][4.63,3.1]{"role": "Agent Smith"}
```

边显示为 `label[id][start,end]{properties}`，因此可以在结果中看到两个端点。

`SET` 添加或替换属性：

```cypher
MATCH (p:person {name: 'Hugo Weaving'}) SET p.nationality = 'Australian' RETURN p;
```

```
                                        p
---------------------------------------------------------------------------------
 person[4.63]{"born": 1960, "name": "Hugo Weaving", "nationality": "Australian"}
```

`REMOVE` 删除一个属性：

```cypher
MATCH (p:person {name: 'Hugo Weaving'}) REMOVE p.nationality RETURN p;
```

```
                         p
----------------------------------------------------
 person[4.63]{"born": 1960, "name": "Hugo Weaving"}
```

`DETACH DELETE` 会同时删除顶点及其边。如果顶点仍然有边，普通的 `DELETE` 会被拒绝，因为 AgensGraph 不允许保留端点缺失的边：

```cypher
MATCH (p:person {name: 'Hugo Weaving'}) DETACH DELETE p;
```

数据集由此恢复为 46 个顶点，手册其余示例的结果仍然一致。

## 混合使用 SQL {#mix-in-sql}

随数据集创建的 `rating` 是普通关系表，不属于图。把 Cypher 放到 SQL 期望表的位置，就能将关系表与 Cypher 查询连接：

```psql
SELECT q.film #>> '{}' AS film, r.score
FROM (MATCH (:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
      RETURN m.title AS film) q
JOIN rating r ON r.title = q.film #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

`#>> '{}'` 将 `jsonb` 标题转换为普通 `text`，以便与 `text` 列比较。注意，这里的电影名不带引号，因为执行的是 SQL 投影，而不是 Cypher 投影。

## 接下来阅读什么 {#where-to-go-next}

- [查询](/zh/agensgraph/querying/)深入介绍读取、写入、流水线、路径和索引。
- [参考](/zh/agensgraph/reference/clauses/)为每个子句提供完整语法。
- [图的存储方式](/zh/agensgraph/concepts/graph-on-postgresql/)解释服务端如何保存刚才创建的对象。
- [向量搜索](/zh/agensgraph/guides/search/vector/)、[全文搜索](/zh/agensgraph/guides/search/full-text/)和[混合搜索](/zh/agensgraph/guides/search/hybrid/)使用本页没有涉及的 `plot` 和 `embedding` 属性。
