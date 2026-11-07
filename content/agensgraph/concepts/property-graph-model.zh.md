---
title: 属性图模型
linkTitle: 属性图模型
description: AgensGraph 同时以关系表和属性图两种形态保存数据。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/property-graph-model.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 同时以两种形态保存数据：关系表和*属性图*。本页定义其中的图这一半，也就是图由哪五类事物组成，以及每类事物在 AgensGraph 中分别遵循哪些规则。

![带标签的属性图](/agensgraph/assets/images/upstream/property_model.png)

## 顶点 {#vertices}

顶点是一个实体：一个人、一部电影、一个账户、一个传感器。它有身份、标签和任意数量的属性。

一个顶点**恰好属于一个标签**。这条规则最可能不同于你用过的其他图数据库——顶点没有一组标签。如果想在同一个顶点上使用多个标签，应改用[标签继承](/zh/agensgraph/concepts/label-inheritance/)；它允许一个模式匹配一个标签家族。

## 边 {#edges}

边连接两个顶点。它有身份、标签、任意数量的属性，以及方向：边始终有起点和终点。

AgensGraph 遵循三条规则：

* **边始终有标签。** 不存在无标签的边。
* **边始终有两个端点。** 悬空边不可能存在，因此删除仍带有边的顶点会被拒绝：

      ERROR:  Vertex with connected edges cannot be removed
      HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
* **方向会被记录，匹配方向是可选的。** 你按一个方向存储边，并在每个查询中决定方向是否重要：`-[:acted_in]->` 沿方向遍历，`-[:acted_in]-` 忽略方向。没有理由再存储一条边的镜像边。

## 属性 {#properties}

属性是顶点或边上的数据。属性由字符串名称和值组成。

每个元素的属性存储为一个 `jsonb` 文档，因此值可以是任何 JSON 类型：字符串、数字、布尔值、数组或嵌套对象。这带来两个后果：

* **标签不强加列清单。** 同一标签下的两个顶点可以携带完全不同的属性名。任何属性都不必预先声明。
* **`null` 不是属性值。** 给属性赋 `null` 会删除它：

      MATCH (n:person {name: 'Tmp'}) SET n.born = NULL RETURN n;
      person[4.40]{"name": "Tmp"}

  因此设置为 null 的属性和从未存在过的属性是同一回事。打开 `allow_null_properties` 会改变这一点，null 会被存储：

      person[4.40]{"born": null, "name": "Tmp"}

因为读取属性必须进入 JSON 文档，如果每个查询都按同一属性过滤，把它[提升为类型列](/zh/agensgraph/querying/typed-columns/)可能值得。那是性能选择，不是建模选择——它仍然是属性。

> [!NOTE]
> `n.id` 不是顶点的身份。它读取名为 `id` 的属性，而这个属性通常不存在。身份是 `id(n)`。

## 标签 {#labels}

标签把同类元素分组。`movie`、`person`、`acted_in` 都是标签。

标签是附加索引的对象，是授予权限的对象，也是模式命名以缩小搜索范围的对象。顶点标签和边标签是不同类别，分别用 `CREATE VLABEL` 和 `CREATE ELABEL` 创建；每个名称在同一个图中只能使用一次。

每个图创建时都会带两个你未声明的标签：`ag_vertex` 和 `ag_edge`。你创建的每个标签都继承其中之一。正是这层继承，让 `MATCH (n)` 这样的无标签模式表示“任意顶点”。完全未指定标签创建的顶点会落入 `ag_vertex`：

```cypher
CREATE ({tmp: 1});
MATCH (n:ag_vertex ONLY) RETURN label(n) AS label, id(n) AS id, n.tmp;
```

```
    label    | id  | tmp
-------------+-----+------
 "ag_vertex" | 1.3 | 1
```

你不能自行命名默认标签：

```cypher
CREATE (:ag_vertex {tmp: 1});
```

```
ERROR:  specifying default label is not allowed
```

除非加双引号，标签名会折叠为小写，这与 PostgreSQL 折叠未加引号标识符的方式相同。这里的反引号不是引用字符——参见[语法](/zh/agensgraph/reference/syntax/)。

## 路径 {#paths}

路径是由边连接的顶点序列。它本身就是一个值：可以绑定到变量、返回，并询问长度或成员。

```cypher
MATCH p = (a:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
RETURN length(p) AS hops, a.name AS actor, m.title AS film
ORDER BY film LIMIT 2;
```

```
 hops |     actor      |         film
------+----------------+-----------------------
 1    | "Keanu Reeves" | "The Matrix"
 1    | "Keanu Reeves" | "The Matrix Reloaded"
```

路径的长度是边的数量，因此单个顶点是长度为 0 的路径，一条指向自身的边是长度为 1 的路径。路径用来表达“任意跳数”；变长模式、最短路径和加权搜索见[路径](/zh/agensgraph/querying/paths/)。

## 图 {#graphs}

图是标签的容器，一个数据库可以保存多个图。图同时也是 PostgreSQL 模式，因此图名和模式名不能冲突——参见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

会话一次只工作在**一个**图中，该图由 `graph_path` 指定：

```cypher
SET graph_path = moviekb;
```

没有它，任何名称都无法解析：

```
ERROR:  graph_path is NULL
HINT:  Use SET graph_path
```

`graph_path` 只接受一个图名，模式也不能用图名限定标签——`MATCH (n:other.work)` 是语法错误。要在一条语句中读取两个图，应使用 SQL；SQL 把它们视为两个模式：

```cypher
CREATE GRAPH other;
SET graph_path = other;
CREATE VLABEL work;
CREATE (:work {title: 'A'}), (:work {title: 'B'});
SET graph_path = moviekb;
```

```sql
SELECT (SELECT count(*) FROM moviekb.movie) AS movies,
       (SELECT count(*) FROM other.work)    AS works;
```

```
 movies | works
--------+-------
     18 |     2
```

```cypher
DROP GRAPH other CASCADE;
```

因为 `graph_path` 是会话级设置，如果每个会话都要使用同一个图，请在数据库级别设置：

```sql
ALTER DATABASE mydb SET graph_path = moviekb;
```
