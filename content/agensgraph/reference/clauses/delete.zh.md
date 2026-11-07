---
title: DELETE 子句
linkTitle: DELETE 子句
description: 从图中移除顶点和边。
type: docs
weight: 150
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/delete.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**

从图中移除顶点和边。`DETACH DELETE` 会在移除顶点的同时移除其边。

## 语法概要 {#synopsis}

```text
[ DETACH ] DELETE expression [, expression ] ...
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`DELETE` 移除其表达式求值得到的图元素。它需要先绑定这些元素，因此总是跟在查找它们的子句之后。

- **普通 `DELETE` 会拒绝仍带有边的顶点**。删除这种顶点会留下指向空处的边，因此该子句会引发错误并回滚事务。
- **`DETACH DELETE`** 会先删除顶点的边，再删除顶点。只要顶点可能存在连接，就应使用它。
- 删除**边**从不需要 `DETACH`，也绝不会影响其端点。
- 可以列出多个表达式。它们按给定顺序删除，因此把边列在其端点之前时不需要 `DETACH` 也能成功。
- `DELETE` 对每个传入行运行一次。某个元素若已被更早的行删除，不会构成错误。
- 每个表达式都必须是顶点、边或路径。属性引用不被接受：若要移除属性，请使用
  [`REMOVE`](/zh/agensgraph/reference/clauses/remove/)。
- `DELETE` 可以结束查询。添加 [`RETURN`](/zh/agensgraph/reference/clauses/return/) 可以查看被删除的内容。

## 参数 {#parameters}

DETACH
: 在删除每个顶点的同时删除其连接的边。

expression
: 产生顶点、边或路径的表达式，通常是由 [`MATCH`](/zh/agensgraph/reference/clauses/match/) 绑定的变量。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。第一个示例构建供后续示例删除的子图，因此数据集最终会回到初始状态。

### 构建待删除内容 {#build-something-to-delete}

```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
MATCH (d:person {name: 'Christopher Nolan'}), (m:movie {title: 'Tenet'})
CREATE (d)-[:directed]->(m);
MATCH (m:movie {title: 'Tenet'})
CREATE (a:person {name: 'Elizabeth Debicki', born: 1990})-[:acted_in {role: 'Kat'}]->(m);
```

```
UPDATE 1
UPDATE 1
UPDATE 2
```

`Tenet` 现在有两条边：

```cypher
MATCH (m:movie {title: 'Tenet'})-[r]-(x)
RETURN label(r) AS edge, count(*) AS n
ORDER BY edge;
```

```
    edge    | n
------------+---
 "acted_in" | 1
 "directed" | 1
(2 rows)
```

### 查看普通 DELETE 拒绝已连接顶点 {#see-a-plain-delete-refuse-a-connected-vertex}

```cypher
MATCH (m:movie {title: 'Tenet'}) DELETE m;
```

```
ERROR:  Vertex with connected edges cannot be removed
HINT:  Use DETACH DELETE or remove connected edges before deleting the vertex.
```

什么也没有删除。图中永远不会持有端点已经消失的边。

### 删除一条边 {#delete-an-edge}

边不需要 `DETACH`，其端点会保留：

```cypher
MATCH (:person {name: 'Elizabeth Debicki'})-[r:acted_in]->(:movie {title: 'Tenet'})
DELETE r;
```

```
UPDATE 1
```

```cypher
MATCH (p:person {name: 'Elizabeth Debicki'})-[r]-() RETURN count(*) AS edges;
```

```
 edges
-------
 0
(1 row)
```

### 删除未连接的顶点并查看结果 {#delete-an-unconnected-vertex-and-see-what-went}

没有剩余边时，普通 `DELETE` 会成功。其后的 `RETURN` 会报告被移除的元素：

```cypher
MATCH (p:person {name: 'Elizabeth Debicki'})
DELETE p
RETURN properties(p) AS removed;
```

```
                   removed
---------------------------------------------
 {"born": 1990, "name": "Elizabeth Debicki"}
(1 row)
```

### 同时删除顶点及其边 {#delete-a-vertex-and-its-edges-together}

`Tenet` 仍有 `directed` 边。`DETACH DELETE` 会同时删除二者：

```cypher
MATCH (m:movie {title: 'Tenet'}) DETACH DELETE m;
```

```
UPDATE 2
```

两个元素：边和顶点。Christopher Nolan 不受影响，并保留其他边：

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN m.title AS film
ORDER BY film;
```

```
      film
----------------
 "Inception"
 "Interstellar"
(2 rows)
```

### 在一个子句中删除多个元素 {#delete-several-elements-in-one-clause}

把边列在它连接的顶点之前，就不需要 `DETACH`，因为删除顶点时边已经不存在：

```cypher
CREATE (:person {name: 'Extra Two'});
MATCH (a:person {name: 'Extra Two'}) CREATE (a)-[:acted_in]->(:movie {title: 'Scratch'});
```

```
UPDATE 1
UPDATE 2
```

```cypher
MATCH (a:person {name: 'Extra Two'})-[r:acted_in]->(m:movie {title: 'Scratch'})
DELETE r, a, m;
```

```
UPDATE 3
```

数据集回到原始大小：

```cypher
MATCH (n) RETURN label(n) AS label, count(*) AS n ORDER BY label;
```

```
  label   | n
----------+----
 "movie"  | 18
 "person" | 28
(2 rows)
```

## 说明 {#notes}

`DELETE` 接受元素，不接受属性。命名属性会被拒绝，而不是被静默忽略：

```cypher
MATCH (m:movie {title: 'The Matrix'}) DELETE m.title;
```

```
ERROR:  node, relationship, or path is expected
LINE 1: MATCH (m:movie {title: 'The Matrix'}) DELETE m.title;
                                                     ^
```

属性请使用 [`REMOVE`](/zh/agensgraph/reference/clauses/remove/)，或使用 `SET m.title = NULL`。

> [!NOTE]
> 对高连接度顶点执行 `DETACH DELETE` 可能在一条语句中删除大量边，而这一切都发生在同一个事务中。当你不确定影响范围有多大时，请先用
> `MATCH (v)-[r]-() RETURN count(r)` 计数。

## 兼容性 {#compatibility}

### NODETACH（ISO/IEC 39075 §13.5） {#nodetach-isoiec-39075-135}

标准的 `<delete statement>` 是 `[ DETACH | NODETACH ] DELETE`，其中
`NODETACH` 是隐式默认值。AgensGraph 实现了该默认行为，但没有实现该关键字：
`NODETACH DELETE m` 是语法错误。请写普通 `DELETE`，二者含义相同。

## 另见 {#see-also}

- [`REMOVE`](/zh/agensgraph/reference/clauses/remove/)——移除属性而不是元素
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)——绑定待删除的元素
- [`CREATE`](/zh/agensgraph/reference/clauses/create/)、[`MERGE`](/zh/agensgraph/reference/clauses/merge/)——把这些元素放入图的子句
- [数据定义](/zh/agensgraph/reference/ddl/)——删除整个标签或图
