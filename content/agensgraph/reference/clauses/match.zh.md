---
title: MATCH 子句
linkTitle: MATCH 子句
description: 查找图中模式匹配的每个位置，并为每个匹配绑定一行变量。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/match.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**

查找图中模式匹配的每个位置，并为每个匹配绑定一行变量。

## 语法概要 {#synopsis}

```text
[ OPTIONAL ] MATCH pattern [, pattern ] ... [ WHERE condition ]
```

其中 *pattern* 是节点和边模式的链，可以命名：

```text
[ path_variable = ] node [ edge node ] ...
```

*node* 写在圆括号中：

```text
( [ variable ] [ : label [ ONLY ] ] [ { property_map } ] )
```

*edge* 写在两个短横线之间的方括号中，并带有 *edge_body*：

```text
[ variable ] [ : label [ ONLY ] ] [ * [ min ] [ .. [ max ] ] ] [ { property_map } ]
```

周围的短横线和箭头指定方向。共有三种：

```text
-[ edge_body ]->      left to right<-[ edge_body ]-      right to left-[ edge_body ]-       either direction
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`MATCH` 读取图。每当它的模式可以覆盖到已存储的顶点和边上，它就产生一行。模式中每个已命名元素都会绑定到它匹配的顶点、边或路径。管道中后面的子句可以看到这些绑定。位于管道中间的
`MATCH` 对每个传入行运行一次，并把其匹配结果连接到该行，就像连接为关系查询增加行一样。

- **没有变量**的模式元素仍会被匹配，只是后续不能引用它。当你只需要该元素约束形状时，可以省略变量。
- **标签**把元素限制到该标签及其子标签；`ONLY`
  把它限制到标签本身。没有标签时，元素会匹配图中的每个顶点或每条边。
- 模式中的**属性映射**是对其中列出的每个键做相等测试。它是简写：`(m:movie {year: 1999})` 与
  `(m:movie) WHERE m.year = 1999` 匹配相同顶点。
- **逗号**在一个 `MATCH` 中分隔独立模式。共享变量的模式会按该变量连接；完全不共享内容的模式会产生笛卡尔积。
- 在一个模式匹配内，**任何边都不会使用两次**。节点绑定可以重复，因此模式可以闭合三角形；但两跳模式绝不会沿它到达所用的边折返。
- 一个**边变量**在每个模式中最多使用一次；重复使用会引发
  `duplicate variable`。**节点变量**可以重复，这会约束两个位置必须是同一顶点。
- `MATCH` 可以开启查询，也可以位于第一个子句之后的任何位置。它永远不会结束查询：查询必须以
  `RETURN`、`FINISH` 或写子句结束。

`OPTIONAL MATCH` 会保留模式未找到结果的输入行，把模式变量绑定为
null，而不是丢弃该行。它有单独一页：[`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/)。

## 参数 {#parameters}

pattern
: 一个路径模式，前面可加 `path_variable =`。可以列出多个模式，用逗号分隔。

path_variable
: 绑定到整条匹配路径的名称；该值按顺序携带路径中的顶点和边。可用路径函数
  `length()`、`nodes()` 和 `edges()` 读取。该名称必须是标识符：`path`
  这类未保留关键字在这里会被拒绝，除非加引号（`` "path" ``）。

variable
: 绑定到匹配顶点或边的名称。可选。对该子句之后的每个子句可见。

label
: 节点模式上的顶点标签，或边模式上的边标签。每个元素一个标签。

ONLY
: 排除子标签，因此元素只匹配该标签自身表中的行，而不匹配继承它的任何内容。需要标签。

property_map
: 映射字面量，或持有映射的查询参数。每个键都会与元素同名属性做相等比较。

min, max
: 变长边模式遍历边数的边界。`*n` 恰好 *n* 跳；`*m..n` 在 *m* 到 *n* 之间；`*m..`
  为 *m* 或更多；`*..n` 为至多 *n*；裸 `*` 为一跳或更多。

condition
: 过滤匹配结果的布尔表达式，在模式中的所有变量都已绑定时求值。参见
  [`WHERE`](/zh/agensgraph/reference/clauses/where/)。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

### 按属性查找一个顶点 {#find-one-vertex-by-a-property}

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p;
```

```
                         p
---------------------------------------------------
 person[4.1]{"born": 1964, "name": "Keanu Reeves"}
(1 row)
```

顶点打印为 `label[id]{properties}`。`4.1` 是它的图 id，可用 `id(p)`
读取。`p.id` 读取的是名为 `id` 的属性，而该属性不存在。

### 沿一个方向跟踪边 {#follow-an-edge-in-one-direction}

```cypher
MATCH (p:person)-[r:acted_in]->(m:movie {title: 'The Matrix'})
RETURN p.name AS actor, r.role AS role
ORDER BY actor;
```

```
        actor         |    role
----------------------+------------
 "Carrie-Anne Moss"   | "Trinity"
 "Keanu Reeves"       | "Neo"
 "Laurence Fishburne" | "Morpheus"
(3 rows)
```

两个端点和边都带有标签，边绑定到 `r`，因此可以投影其 `role`
属性。字符串值带引号返回，因为 Cypher `RETURN` 产生 jsonb。

### 省略不需要的元素 {#leave-out-the-elements-you-do-not-need}

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m)
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

边没有变量，远端点没有标签。二者仍会约束匹配；但都不会占用绑定。

### 匹配任一方向的边 {#match-an-edge-in-either-direction}

不带箭头的边模式无论边指向哪一方都会匹配：

```cypher
MATCH (m:movie {title: 'Total Recall'})-[:related_to]-(n:movie)
RETURN n.title AS neighbour
ORDER BY neighbour;
```

```
  neighbour
--------------
 "Inception"
 "The Matrix"
(2 rows)
```

`Total Recall` 有一条出站 `related_to` 边和一条入站边。两端都写箭头
`<-[:related_to]->` 的含义相同。

### 在共享变量上连接两个模式 {#join-two-patterns-on-a-shared-variable}

```cypher
MATCH (a:person)-[:acted_in]->(m:movie), (d:person)-[:directed]->(m)
WHERE m.title = 'The Matrix'
RETURN a.name AS actor, d.name AS director
ORDER BY actor, director;
```

```
        actor         |     director
----------------------+-------------------
 "Carrie-Anne Moss"   | "Lana Wachowski"
 "Carrie-Anne Moss"   | "Lilly Wachowski"
 "Keanu Reeves"       | "Lana Wachowski"
 "Keanu Reeves"       | "Lilly Wachowski"
 "Laurence Fishburne" | "Lana Wachowski"
 "Laurence Fishburne" | "Lilly Wachowski"
(6 rows)
```

两个模式都提到 `m`，因此会按它连接。两个连续 `MATCH`
子句会得到相同结果；在中间相遇的一个模式
`(a:person)-[:acted_in]->(m:movie)<-[:directed]-(d:person)` 也一样。

### 命名整条路径 {#name-the-whole-path}

在模式前写 `variable =` 即可绑定路径本身：

```cypher
MATCH p = (a:movie {title: 'The Matrix'})-[:related_to*1..3]->(b:movie)
RETURN length(p) AS hops, [x IN nodes(p) | x.title] AS route
ORDER BY hops, route;
```

```
 hops |                                            route
------+---------------------------------------------------------------------------------------------
 1    | ["The Matrix", "The Matrix Reloaded"]
 1    | ["The Matrix", "The Terminator"]
 1    | ["The Matrix", "Total Recall"]
 2    | ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"]
 2    | ["The Matrix", "The Terminator", "Terminator 2: Judgment Day"]
 2    | ["The Matrix", "Total Recall", "Inception"]
 3    | ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions", "The Matrix Resurrections"]
(7 rows)
```

### 遍历可变数量的边 {#walk-a-variable-number-of-edges}

边模式上的 `*` 会重复该边。每个边界都是可选的：

```cypher
MATCH (m:movie {title: 'The Matrix'})-[:related_to*2]->(n:movie)
RETURN n.title AS reached
ORDER BY reached;
```

```
           reached
------------------------------
 "Inception"
 "Terminator 2: Judgment Day"
 "The Matrix Revolutions"
(3 rows)
```

下界 `0` 包含零长度路径，因此起始顶点是答案之一：

```cypher
MATCH (m:movie {title: 'The Matrix'})-[:related_to*0..1]->(n:movie)
RETURN n.title AS reached
ORDER BY reached;
```

```
        reached
-----------------------
 "The Matrix"
 "The Matrix Reloaded"
 "The Terminator"
 "Total Recall"
(4 rows)
```

### 用 ONLY 排除子标签 {#exclude-child-labels-with-only}

标签也会匹配其子标签，因为标签是表，而子标签继承它。`ONLY`
把匹配收窄到一个标签。给 `person` 添加子标签即可看出差异：

```cypher
CREATE VLABEL crew INHERITS (person);
CREATE (:crew {name: 'Bill Pope', born: 1952});
```

```
CREATE VLABEL
UPDATE 1
```

```cypher
MATCH (p:person) RETURN count(*) AS people;
```

```
 people
--------
 29
(1 row)
```

```cypher
MATCH (p:person ONLY) RETURN count(*) AS people;
```

```
 people
--------
 28
(1 row)
```

`ONLY` 位于标签之后、属性映射之前，例如
`(p:person ONLY {name: 'Keanu Reeves'})`。它在边模式上的用法相同：
`-[r:acted_in ONLY]->`。用以下语句撤销设置：

```cypher
MATCH (p:crew) DETACH DELETE p;
DROP VLABEL crew;
```

```
UPDATE 1
DROP VLABEL
```

### 用 WHERE 过滤匹配结果 {#filter-the-matches-with-where}

附加到 `MATCH` 的 `WHERE` 是匹配的一部分，不是后续步骤：

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY year, film;
```

```
            film            | year
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(2 rows)
```

### 匹配多个标签的边 {#match-edges-of-several-labels}

边模式最多带一个标签。列出两个会引发错误：

```cypher
MATCH (p:person)-[r:acted_in|directed]->(m:movie) RETURN count(r);
```

```
ERROR:  multiple types for relationship not supported
```

改为匹配未加标签的边，并在 `WHERE` 中测试其标签：

```cypher
MATCH (p:person)-[r]->(m:movie)
WHERE label(r) IN ['acted_in', 'directed']
RETURN count(r) AS edges;
```

```
 edges
-------
 46
(1 row)
```

`label()` 以字符串返回元素标签。因此，对名称列表使用 `IN`
是通用形式，也是匹配一组边标签的唯一方式。

## 说明 {#notes}

标签测试应写在 `label(n) = '...'` 中，而不是 `WHERE` 的冒号形式。`WHERE n:movie`
是语法错误；裸模式用作谓词也一样：`WHERE (m)-[:related_to]->(:movie)` 无法解析。请使用
`WHERE EXISTS { MATCH (m)-[:related_to]->(:movie) }` 来测试模式是否存在。

属性映射比较 jsonb 值，与属性的比较也一样。当字面量类型与存储类型不一致时，这一点很重要。参见
[`WHERE`](/zh/agensgraph/reference/clauses/where/)。

> [!NOTE]
> 命名路径变量的解析比元素变量更窄。`(path)` 是可接受的节点变量，但
> `MATCH path = ...` 是语法错误，因为 `path` 是关键字；请写 `MATCH p = ...` 或给名称加引号。

## 兼容性 {#compatibility}

### 标签表达式（ISO/IEC 39075 §16.8） {#label-expressions-isoiec-39075-168}

标准的 `<label expression>` 用 `|` 表示析取，`&` 表示合取，`!`
表示否定。AgensGraph 每个模式元素只接受一个标签名，因此三者都不可用。
`-[r:acted_in|directed]->` 会引发
`multiple types for relationship not supported`；`-[r:acted_in|:directed]->`
是语法错误。openCypher 也用竖线表示析取；在这里，它同样会在固定长度边、变长边以及
`shortestpath` 内被拒绝。请如上所示使用 `WHERE label(r) IN [...]`。

### 标签谓词（ISO/IEC 39075 §19.9） {#labeled-predicate-isoiec-39075-199}

标准把标签测试写成 `n IS LABELED movie` 或 `n:movie`。AgensGraph
两种写法都不接受；请使用 `label(n) = 'movie'`。

### ONLY 修饰符（ISO/IEC 39075 §16.7） {#the-only-modifier-isoiec-39075-167}

标准的 `<element pattern filler>` 包含变量声明、标签表达式和谓词，不包含其他内容；没有
`ONLY`。AgensGraph 添加它是因为这里的标签是可被子标签继承的表，标签匹配是对继承树的匹配。参见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。

## 另见 {#see-also}

- [`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/)——保留模式未匹配的行
- [`WHERE`](/zh/agensgraph/reference/clauses/where/)——匹配可携带的条件
- [`CREATE`](/zh/agensgraph/reference/clauses/create/) 与 [`MERGE`](/zh/agensgraph/reference/clauses/merge/)——用于写入的相同模式语法
- [`LOAD FROM`](/zh/agensgraph/reference/clauses/load-from/)——把表读入同一管道
- [函数](/zh/agensgraph/reference/functions/)——`length()`、`nodes()`、`edges()` 及其他路径函数
- [查询](/zh/agensgraph/querying/)——路径查询，包括 `shortestpath`、`allshortestpaths` 和 `dijkstra` 形式
