---
title: FILTER 子句
linkTitle: FILTER 子句
description: 只保留满足条件的行。
type: docs
weight: 180
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/filter.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**  **2.18 新增**

只保留满足条件的行。它是独立的过滤子句，不需要投影，这一点不同于 Cypher 的
`WITH … WHERE`。

## 语法概要 {#synopsis}

```text
FILTER [ WHERE ] condition
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`FILTER` 丢弃条件不为真的每一行，并且不改变其他内容：它在执行前的作用域列与执行后完全相同。可选的
`WHERE` 是冗余词。`FILTER x > 1` 与 `FILTER WHERE x > 1`
会解析成同一个子句。

- `FILTER` 是**中间**子句。它不能开启查询，也不能结束查询。
- 它作用于前一个子句产生的任何内容，包括聚合 `WITH` 的输出。因此它是 Cypher
  管道中的 `HAVING`。
- 连续的 `FILTER` 按顺序应用，每一个都会进一步收窄上一个保留下来的行。
- 条件求值为 null 的行会被丢弃，与 SQL 中的行为相同。

## 参数 {#parameters}

condition
: 作用域内变量上的谓词。可以是 `WHERE` 接受的任何布尔表达式，包括
  [子查询值表达式](/zh/agensgraph/reference/clauses/subquery-expressions/)，例如 `EXISTS { }` 或
  `COUNT { }`。条件必须是布尔值：裸数字会被拒绝，错误为
  `argument of FILTER must be type boolean, not type integer`；裸属性会被拒绝，错误为
  `cannot cast 2003 (jsonb type numeric) to boolean`。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

保留 2014 年及以后的电影。模式后面的 `FILTER` 与附加在该模式上的 Cypher
`WHERE` 是同一个测试。切换标签页比较：

{{< tabs >}}
{{< tab label="GQL — FILTER" >}}
```cypher
MATCH (m:movie)
FILTER m.year >= 2014
RETURN m.title AS film, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< tab label="Cypher — WHERE" >}}
```cypher
MATCH (m:movie)
WHERE m.year >= 2014
RETURN m.title AS film, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< /tabs >}}
```
            film            | year
----------------------------+------
 "Interstellar"             | 2014
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(3 rows)
```

两种形式的执行计划完全相同，甚至对 `movie` 扫描都带有同一个
`Filter: (properties.'year' >= '2014'::jsonb)`。

### 过滤聚合结果 {#filter-an-aggregate}

`WHERE` 不能跟在聚合 `RETURN` 之后；把它附加到 `WITH` 上又会迫使你重述投影。
`FILTER` 可以直接测试聚合值：

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p.name AS actor, count(m) AS films
FILTER films >= 3
RETURN actor, films ORDER BY actor;
```

```
          actor          | films
-------------------------+-------
 "Arnold Schwarzenegger" | 3
 "Keanu Reeves"          | 4
(2 rows)
```

### 分两个阶段收窄行 {#narrow-rows-in-two-stages}

每个 `FILTER` 只能看见上一个 `FILTER` 保留的行：

```cypher
MATCH (m:movie)
FILTER m.genre = 'Sci-Fi'
FILTER m.year < 1998
RETURN m.title AS film ORDER BY film;
```

```
        film
---------------------
 "Blade Runner"
 "Gattaca"
 "The Fifth Element"
 "Total Recall"
(4 rows)
```

### 过滤写子句产生的行 {#filter-the-rows-a-write-clause-produced}

写子句之后的 `FILTER` 会先执行写入，再限制继续流动的行。这里 `SET`
会修改电影，而 `FILTER` 决定该行是否被报告：

```cypher
MATCH (m:movie {title: 'The Matrix'})
SET m.reviewed = true
FILTER m.year = 1999
RETURN m.title AS film, m.reviewed AS reviewed;
```

```
     film     | reviewed
--------------+----------
 "The Matrix" | true
(1 row)
```

## 说明 {#notes}

由于 `FILTER` 不能开启查询，以它开头的语句是语法错误，而不是子句位置错误：

```cypher
FILTER true;
```

```
ERROR:  syntax error at or near "FILTER"
LINE 1: FILTER true;
        ^
```

`FILTER` 唯一可以排在首位的位置是在 [`NEXT`](/zh/agensgraph/reference/clauses/next/)
之后；此时它作用于跨越边界传递的表。查询以 `FILTER` 结束会引发
`Cypher query must end with RETURN, FINISH or update clause`。

`filter` 是未保留关键字，因此仍可用作变量名、标签名或属性名。

## 兼容性 {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> 实现 GQL *FILTER statement*（ISO/IEC 39075:2024 §14.6），Feature GQ08
> “FILTER statement”。
>
> - **支持**——标准定义的两种写法，即 `FILTER <search condition>` 和
>   `FILTER WHERE <search condition>`，可用于所有非首、非终止位置。
> - **不支持**——该小节没有缺失内容。`FILTER` 是完整的。
>
> 在 [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)中跟踪状态。

### openCypher {#opencypher}

openCypher 没有 `FILTER` 语句；等价形式是附加在 `MATCH` 或 `WITH`
上的 `WHERE`，AgensGraph 原样接受这两者。无关的 openCypher 列表函数
`filter(x IN list WHERE predicate)` 同样不被接受。括号内的 `WHERE`
是语法错误。请改写列表推导：`[x IN m.embedding WHERE x > 0]`。

## 另见 {#see-also}

- [`WHERE`](/zh/agensgraph/reference/clauses/where/)——附加到子句上的 Cypher 对应形式
- [`WITH`](/zh/agensgraph/reference/clauses/with/)——在一个子句中投影并过滤
- [`LET`](/zh/agensgraph/reference/clauses/let/) **GQL**——添加列而不丢弃任何列
- [`NEXT`](/zh/agensgraph/reference/clauses/next/) **GQL**——`FILTER` 唯一可以排在首位的位置
- [子查询值表达式](/zh/agensgraph/reference/clauses/subquery-expressions/) **GQL**——`FILTER` 可使用的谓词
- [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)
