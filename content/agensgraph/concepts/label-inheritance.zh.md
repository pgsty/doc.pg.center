---
title: 标签继承
linkTitle: 标签继承
description: 一个标签可以继承另一个标签。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/label-inheritance.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


一个标签可以继承另一个标签。子标签仍是独立标签，有自己的 id 序列和自己的行；但命名父标签的模式也会匹配子标签的行。这样既得到类型层级，又不必放弃用一个模式查询整个家族的能力。

继承就是 PostgreSQL 表继承——[标签是表](/zh/agensgraph/concepts/graph-on-postgresql/)，标签上的 `INHERITS` 会变成那张表上的 `INHERITS`。

## 声明层级 {#declaring-a-hierarchy}

本页示例会创建自己的小图，而不使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)，因为在层级上观察继承比在电影和人物上更容易。用完后运行 `DROP GRAPH inh CASCADE;`。

```cypher
CREATE GRAPH inh;
SET graph_path = inh;

CREATE VLABEL work;
CREATE VLABEL film INHERITS (work);
CREATE VLABEL series INHERITS (work);

CREATE (:film {title: 'A'}), (:series {title: 'B'}), (:work {title: 'C'});
```

命名父标签会匹配家族中的所有行：

```cypher
MATCH (n:work) RETURN label(n) AS label, n.title AS t ORDER BY t;
```

```
  label   |  t
----------+-----
 "film"   | "A"
 "series" | "B"
 "work"   | "C"
```

命名子标签只匹配该子标签：

```cypher
MATCH (n:film) RETURN label(n) AS label, n.title AS t;
```

```
 label  |  t
--------+-----
 "film" | "A"
```

注意 `label(n)` 返回的是创建顶点时使用的标签，永远不会返回父标签。顶点恰好属于一个标签。“匹配父标签”说的是模式扫描哪些表，不是说顶点拥有两个标签。

## ONLY：排除子标签 {#only-excluding-the-children}

`ONLY` 把模式限制为命名的标签本身：

```cypher
MATCH (n:work ONLY) RETURN label(n) AS label, n.title AS t;
```

```
 label  |  t
--------+-----
 "work" | "C"
```

它也适用于边，并且写在括号内：

```cypher
MATCH ()-[e:rel ONLY]->() RETURN count(e) AS n;
```

```
 n
---
 0
```

这个零正是有用的情况：`rel` 有一个子标签 `sequel`，而所有边都创建为 `sequel`。因此 `rel ONLY` 一条也不匹配，普通 `rel` 全部匹配。

## 边以相同方式继承 {#edges-inherit-the-same-way}

```cypher
CREATE ELABEL rel;
CREATE ELABEL sequel INHERITS (rel);

MATCH (a:film {title: 'A'}), (b:series {title: 'B'}) CREATE (a)-[:sequel]->(b);
MATCH ()-[e:rel]->() RETURN label(e) AS label;
```

```
  label
----------
 "sequel"
```

## 多个父标签 {#more-than-one-parent}

一个标签可以同时继承多个标签：

```cypher
CREATE VLABEL hybrid INHERITS (work, film);
```

此后，`MATCH (n:work)` 和 `MATCH (n:film)` 都会匹配 `hybrid` 的行。

## 每个图已经继承的内容 {#what-every-graph-already-inherits}

即使不写 `INHERITS` 子句，你创建的每个标签也继承自 `ag_vertex` 或 `ag_edge`。这就是无标签的 `MATCH (n)` 能匹配所有内容的原因。参见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#every-graph-has-two-labels-you-did-not-create)。

## 代价 {#what-it-costs}

匹配父标签的模式会扫描父标签的表及其下的每一张表，因此执行计划会在整个家族上增加一个 `Append`：

```cypher
EXPLAIN (COSTS OFF) MATCH (n:work) RETURN n;
```

```
             QUERY PLAN
------------------------------------
 Result
   ->  Append
         ->  Seq Scan on work n_1
         ->  Seq Scan on film n_2
         ->  Seq Scan on series n_3
         ->  Seq Scan on hybrid n_4
```

`ONLY` 会去掉 `Append`：

```cypher
EXPLAIN (COSTS OFF) MATCH (n:work ONLY) RETURN n;
```

```
     QUERY PLAN
--------------------
 Seq Scan on work n
```

由此得到两点。第一，深层级会让最简单的查询——“给我一个标签的行”——在比所需更多的关系上制定计划。因此，只要想要一个标签的行且不想要其他行，就命名子标签或添加 `ONLY`。第二，每个将被扫描的表上都必须有索引：`work` 上的索引不会索引 `film` 的行。[索引与约束](/zh/agensgraph/querying/indexes-and-constraints/)介绍了如何跨层级建立索引。

> [!NOTE]
> 当查询确实需要整个家族——一个有时是 `film`、有时是 `series` 的 `work`——时再使用继承。如果每个查询反正都会命名子标签，独立标签更简单，执行计划也更好。
