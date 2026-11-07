---
title: CREATE 子句
linkTitle: CREATE 子句
description: 向图中添加顶点和边；模式中的每个元素各创建一个。
type: docs
weight: 100
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/create.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


向图中添加顶点和边；模式中的每个元素各创建一个。

## 语法概要 {#synopsis}

```text
CREATE pattern [, pattern ] ...
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`CREATE` 会把你给出的模式写入图。它使用与 [`MATCH`](/zh/agensgraph/reference/clauses/match/)
读取时相同的模式语法，但每个元素都是被构建出来，而不是被查找出来。

- `CREATE` **总是创建**。它不检查相同的顶点或边是否已经存在。若只想创建缺失的内容，请使用
  [`MERGE`](/zh/agensgraph/reference/clauses/merge/)。
- 命名了一个**已在作用域内的变量**的元素会被复用，而不是重建。这就是边如何连接到 `MATCH`
  找到的顶点：端点是已绑定的变量，因此只有边是新的。
- 命名了一个**新变量或未命名**的元素会被创建。因此，一个模式可以在一步中同时创建顶点及其边。
- 每个元素都需要足够的信息才能构建。边需要标签和方向；没有标签的顶点会成为裸
  `ag_vertex`。
- 属性映射可以是**映射字面量**、查询参数，或 `= expression`，其中表达式产生
  jsonb 对象。最后一种形式用于把整张表的一行变成属性包。参见
  [`LOAD FROM`](/zh/agensgraph/reference/clauses/load-from/)。
- `CREATE` 对每个传入行运行一次。如果前面没有子句，它运行一次。
- `CREATE` 可以开启查询，也可以跟在其他子句之后，并且可以结束查询。添加
  [`RETURN`](/zh/agensgraph/reference/clauses/return/) 可以查看它构建的内容。

[`INSERT`](/zh/agensgraph/reference/clauses/insert/) 是完全同义的写法，也是 ISO/IEC 39075 使用的拼写。

## 参数 {#parameters}

pattern
: [`MATCH`](/zh/agensgraph/reference/clauses/match/) 语法中的路径模式。可以列出多个模式，用逗号分隔；它们按顺序创建，并可以共享变量。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。最后一个示例会撤销前面的写入。

### 创建一个顶点 {#create-one-vertex}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```

```
UPDATE 1
```

图写入会把它触及的图元素数量报告在 `UPDATE` 标签下，无论使用的是哪个子句。

### 创建顶点并查看创建结果 {#create-a-vertex-and-see-what-you-made}

```cypher
CREATE (p:person {name: 'John David Washington', born: 1984})
RETURN p.name AS person, p.born AS born;
```

```
         person          | born
-------------------------+------
 "John David Washington" | 1984
(1 row)
```

### 在两个现有顶点之间创建边 {#create-an-edge-between-two-existing-vertices}

先找到两个端点，然后只创建边：

```cypher
MATCH (d:person {name: 'Christopher Nolan'}), (m:movie {title: 'Tenet'})
CREATE (d)-[r:directed]->(m)
RETURN d.name AS director, label(r) AS edge, m.title AS film;
```

```
      director       |    edge    |  film
---------------------+------------+---------
 "Christopher Nolan" | "directed" | "Tenet"
(1 row)
```

`d` 和 `m` 已经绑定，因此会被复用。如果该模式在 `CREATE`
内部再次写成 `(d:person {name: 'Christopher Nolan'})`，就会创建第二个
Christopher Nolan。

### 同时创建顶点及其边 {#create-a-vertex-and-its-edge-together}

模式中所有尚未绑定的内容都会被构建：

```cypher
MATCH (m:movie {title: 'Tenet'})
CREATE (a:person {name: 'Elizabeth Debicki', born: 1990})-[r:acted_in {role: 'Kat'}]->(m)
RETURN a.name AS actor, r.role AS role, m.title AS film;
```

```
        actor        | role  |  film
---------------------+-------+---------
 "Elizabeth Debicki" | "Kat" | "Tenet"
(1 row)
```

### 一次创建多个模式 {#create-several-patterns-at-once}

逗号分隔的模式会在一个子句中构建，并可以共享变量：

```cypher
MATCH (p:person {name: 'John David Washington'}), (m:movie {title: 'Tenet'})
CREATE (p)-[:acted_in {role: 'The Protagonist'}]->(m),
       (m)-[:related_to {weight: 2}]->(:movie {title: 'Memento', year: 2000, genre: 'Thriller'});
```

```
UPDATE 3
```

三个元素：一条 `acted_in` 边、一条 `related_to` 边，以及 `Memento`
顶点。`Tenet` 现在有四条边：

```cypher
MATCH (m:movie {title: 'Tenet'})-[r]-(x)
RETURN label(r) AS edge, label(x) AS other, coalesce(x.name, x.title) AS name
ORDER BY edge, name;
```

```
     edge     |  other   |          name
--------------+----------+-------------------------
 "acted_in"   | "person" | "Elizabeth Debicki"
 "acted_in"   | "person" | "John David Washington"
 "directed"   | "person" | "Christopher Nolan"
 "related_to" | "movie"  | "Memento"
(4 rows)
```

### 观察 CREATE 产生重复 {#watch-create-duplicate}

`CREATE` 没有任何幂等性：

```cypher
CREATE (:person {name: 'Duplicate', born: 1}), (:person {name: 'Duplicate', born: 1});
```

```
UPDATE 2
```

```cypher
MATCH (p:person {name: 'Duplicate'}) RETURN count(*) AS rows;
```

```
 rows
------
 2
(1 row)
```

再次运行第一条语句会得到四个顶点。当键必须保持唯一时，请使用
[`MERGE`](/zh/agensgraph/reference/clauses/merge/) 或唯一约束。

### 撤销示例 {#undo-the-examples}

```cypher
MATCH (p:person {name: 'Duplicate'}) DELETE p;
MATCH (m:movie) WHERE m.title IN ['Tenet', 'Memento'] DETACH DELETE m;
MATCH (p:person) WHERE p.name IN ['John David Washington', 'Elizabeth Debicki'] DETACH DELETE p;
```

```
UPDATE 2
UPDATE 6
UPDATE 2
```

## 说明 {#notes}

顶点 id 由标签自身的序列分配，因此新顶点得到的编号取决于该标签此前创建过什么。可用
`id(v)` 读取它；不要依赖特定值。

> [!NOTE]
> 不带标签的 `CREATE`——`CREATE ()`——是合法的，会产生图基础标签
> `ag_vertex` 的顶点。这种顶点对所有 `MATCH (n:label)` 都不可见，也很容易失去跟踪。请始终提供标签。

## 兼容性 {#compatibility}

### 子句名称（ISO/IEC 39075 §13.2） {#the-clause-name-isoiec-39075-132}

标准的插入数据语句是 `INSERT`，不是 `CREATE`。AgensGraph
接受这两种拼写来表示同一个子句；参见 [`INSERT`](/zh/agensgraph/reference/clauses/insert/)。SQL 的
`CREATE` 语句（例如 `CREATE GRAPH` 和 `CREATE VLABEL`）是独立语句，不受影响。

## 另见 {#see-also}

- [`INSERT`](/zh/agensgraph/reference/clauses/insert/) **GQL**——该子句的标准拼写
- [`MERGE`](/zh/agensgraph/reference/clauses/merge/)——只创建尚不存在的内容
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)——模式语法，以及如何先绑定端点
- [`SET`](/zh/agensgraph/reference/clauses/set/)——创建后修改属性
- [`DELETE`](/zh/agensgraph/reference/clauses/delete/)——删除你创建的内容
- [`LOAD FROM`](/zh/agensgraph/reference/clauses/load-from/)——从表中的行创建图元素
