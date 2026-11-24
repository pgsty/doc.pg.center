---
title: "CALL { subquery }"
linkTitle: "CALL { subquery }"
description: "在查询流水线中执行只读子查询。若从外层查询导入变量，则对每条输入行执行一次。"
type: docs
weight: 240
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/call-subquery.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**  **自 2.18 起提供**

在查询流水线中执行只读子查询。若从外层查询导入变量，则对每条输入行执行一次。

> [!IMPORTANT]
> **单写 `CALL { … }` 不会导入任何变量。** 花括号内的模式会*声明*变量。若写入与外层变量相同的名称，绑定的是一个新的同名变量，外层约束对它无效。请显式导入所需变量，写成 `CALL (v) { … }`、`CALL (*) { … }` 或 `CALL { WITH v … }`。

## 语法 {#synopsis}

```text
[ OPTIONAL ] CALL { subquery }
[ OPTIONAL ] CALL ( [ variable [, variable ] ... ] ) { subquery }
[ OPTIONAL ] CALL ( * ) { subquery }
[ OPTIONAL ] CALL { WITH variable [, variable ] ... subquery }
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`CALL { … }` 执行子查询，并将结果连接到工作表。子查询体能访问哪些外层变量，完全取决于导入列表。

- 指定导入变量时，查询体**对每条输入行**执行一次。变量绑定到该行的值，返回的各行再与该行连接。
- 不导入变量时，查询体与外层**不相关**，只执行一次，结果与所有输入行做交叉连接。
- 查询体只读，末尾必须是 `RETURN`。解析器遇到写入子句就会报错，若以 `FINISH` 结尾则报 `CALL subquery must RETURN at least one variable`。
- 查询体返回的名称会绑定到外层查询。若外层已绑定同名变量，查询会报错。导入的变量在查询体内也保留原名，不能用 `LET`、`UNWIND`、`FOR` 或带重命名的 `WITH` 再次绑定。
- 若查询体未返回任何行，对应的输入行会被丢弃。使用 [`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/) 可保留该行。

### 导入变量的写法 {#the-forms-that-import}

共有五种写法，前两种不导入变量。上面的提示针对的就是它们与后三种的区别。

| 写法 | 查询体可见的变量 |
| --- | --- |
| `CALL { … }` | 无 |
| `CALL () { … }` | 无 |
| `CALL (v, w) { … }` | `v` 和 `w` |
| `CALL (*) { … }` | 作用域内的所有变量 |
| `CALL { WITH v, w … }` | `v` 和 `w` |

作用域子句可以与导入用的 `WITH` 一起使用。`CALL (v) { WITH w … }` 会同时导入两个变量。以下三种写法会报语法错误：`CALL (*) { WITH v … }`、`CALL (*, v) { … }`，以及未直接列出变量名的导入 `WITH`（包括 `WITH *` 和 `WITH v AS x`）。

## 参数 {#parameters}

variable
: 外层查询已绑定、需要在花括号内使用的变量。变量不存在时报 `variable "<name>" to import into CALL does not exist`。作用域子句之前没有查询子句时报 `CALL has no preceding clause to import variables from`。

subquery
: 以 `RETURN` 结尾的只读查询。可以使用 `MATCH`、`OPTIONAL MATCH`、`WITH`、`LET`、`UNWIND`、`FOR`、`LOAD FROM`、嵌套的 `CALL`、`DISTINCT`、`ORDER BY`、`SKIP`/`LIMIT` 和集合运算符。不能使用 [`NEXT`](/zh/agensgraph/reference/clauses/next/)。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 为什么要写导入列表 {#why-the-import-list-matters}

例如，要分别统计每部有导演的影片有多少位演员，就适合用子查询。省略导入列表，算出来的却是另一个数。

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 4;
```

```
        film         | cast_size
---------------------+-----------
 "Avatar"            | 25
 "Blade Runner"      | 25
 "Blade Runner 2049" | 25
 "Elysium"           | 25
(4 rows)
```

每部影片的演员数都相同。25 实际上是整张图中 `acted_in` 边的总数。

```cypher
MATCH ()-[r:acted_in]->() RETURN count(r) AS acted_in_edges;
```

```
 acted_in_edges
----------------
 25
(1 row)
```

花括号内的 `m` 和外层匹配的 `m` 是两个变量。内层模式重新声明了变量，只受 `acted_in` 边约束。因此，子查询独立执行一次，统计全图的 `acted_in` 边，再将总数与每条输入行做交叉连接。

显式导入变量，才能得到各部影片的演员数。

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL (m) { MATCH (a:person)-[:acted_in]->(m) RETURN count(a) AS cast_size }
RETURN m.title AS film, cast_size ORDER BY film LIMIT 4;
```

```
        film         | cast_size
---------------------+-----------
 "Avatar"            | 1
 "Blade Runner"      | 1
 "Blade Runner 2049" | 2
 "Elysium"           | 1
(4 rows)
```

`CALL (*) { … }` 和 `CALL { WITH m … }` 算出的数值相同。

这里没有报错，因为*表达式*引用已有变量，而*模式*声明变量。若在 `WHERE` 中犯同样的错误，系统就能发现。

```cypher
MATCH (d:person)-[:directed]->(m:movie)
CALL { MATCH (a:person) WHERE a.name = m.title RETURN count(a) AS n }
RETURN n;
```

```
ERROR:  variable does not exist
LINE 2: CALL { MATCH (a:person) WHERE a.name = m.title RETURN count(...
                                               ^
```

只有在模式中重用变量名，才会悄然得到不同结果。这种写法很常见，所以应始终写明导入列表。

### 逐行聚合并保留外层行数 {#aggregate-per-row-without-collapsing-the-pipeline}

聚合查询体对每条输入行恰好返回一行，即使计算结果为零也一样，因此外层行数不变。

```cypher
MATCH (p:person) WHERE p.name IN ['Keanu Reeves', 'Christopher Nolan']
CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN count(m) AS films }
RETURN p.name AS person, films ORDER BY person;
```

```
       person        | films
---------------------+-------
 "Christopher Nolan" | 0
 "Keanu Reeves"      | 4
(2 rows)
```

### 只计算一次 {#compute-one-number-once}

空作用域子句明确表示查询体与外层不相关。当结果对整个查询为常量时，可用这种写法。

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
CALL () { MATCH (m:movie) RETURN count(m) AS movies }
RETURN p.name AS person, movies;
```

```
     person     | movies
----------------+--------
 "Keanu Reeves" | 18
(1 row)
```

### 导入多个变量 {#import-several-variables}

列出的变量在查询体中都可见，可以只使用其中一部分。

```cypher
MATCH (p:person {name: 'Keanu Reeves'}), (q:person {name: 'Carrie-Anne Moss'})
CALL (p, q) { MATCH (p)-[:acted_in]->(m:movie)<-[:acted_in]-(q) RETURN count(m) AS shared }
RETURN shared;
```

```
 shared
--------
 2
(1 row)
```

## 注意事项 {#notes}

相关查询体在执行计划中未必逐行执行。规划器会将它上提，因此上例与直接写成内联模式时生成相同的连接计划：对 `person`、`acted_in` 和 `movie` 执行 `Hash Join`，与 `MATCH (p:person)-[:acted_in]->(m:movie)` 相同。只有无法展平的查询体（如聚合查询）才会保留为逐行执行的横向连接，在 `Nested Loop` 下执行 `Aggregate`。

以下写入关键字中的任意一个出现在查询体内，都会在该处报语法错误：`CREATE`、`INSERT`、`MERGE`、`SET`、`REMOVE` 和 `DELETE`、`DETACH DELETE`。

若返回的名称已在外层绑定，将报 `variable "<name>" returned by the CALL subquery is already bound in the outer query`。否则后续子句将无法访问原外层变量。请在查询体的 `RETURN` 中指定别名。

## 兼容性 {#compatibility}

> [!NOTE] GQL 标准符合性
> :class: gql-conformance
>
> 实现 GQL 的*内联过程调用*（ISO/IEC 39075:2024 §15.2），属于 §15.1 的*过程调用语句*，用于 §14.5 的查询位置。
>
> - **支持**带绑定变量列表的*变量作用域子句*及其空列表形式 `()`、嵌套调用和 `OPTIONAL` 前缀。
> - **不支持**在查询体中修改数据（§13.6，*数据修改过程调用语句*）。
> - **与标准的重要差异**：按 §15.2 语法规则 3，若*省略*变量作用域子句，调用应改写为显式列出输入工作记录的**全部**字段。标准中的 `CALL { … }` 因而与 `CALL (*) { … }` 一样导入所有变量。AgensGraph 的默认行为与 `CALL () { … }` 一样，不导入变量。
> - **扩展**：标准的*绑定变量引用列表*没有 `(*)` 形式，也没有用 `WITH` 导入变量的写法。两者均源自 openCypher。
>
> 各项支持情况见 [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)。

### openCypher {#opencypher}

openCypher 也要求列出导入变量。在 `CALL { }` 中引用未声明的外层变量时，它会报错。移植时，`CALL (v) { }`、`CALL (*) { }`、`CALL { WITH v … }` 的含义相同，可以沿用。原先被 openCypher 拒绝的裸 `CALL { }` 在这里能运行，但可能给出不同结果。

## 另请参阅 {#see-also}

- [`CALL`](/zh/agensgraph/reference/clauses/call/) **GQL**：两种调用形式
- [`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/) **GQL**：在查询体不返回任何行时保留输入行
- [`CALL … YIELD`](/zh/agensgraph/reference/clauses/call-yield/) **GQL**：调用具名函数
- [子查询值表达式](/zh/agensgraph/reference/clauses/subquery-expressions/) **GQL**：在表达式中使用子查询
- [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)
