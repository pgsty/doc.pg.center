---
title: "OPTIONAL CALL"
linkTitle: "OPTIONAL CALL"
description: "调用未返回任何行时保留相应的输入行，并将所有输出变量绑定为空值。"
type: docs
weight: 250
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/optional-call.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**  **自 2.18 起提供**

若调用没有返回任何行，仍保留输入行，并将原本应返回的所有变量绑定为 null。它对 `CALL` 的作用相当于 `OPTIONAL MATCH` 对模式匹配的作用。

## 语法 {#synopsis}

```text
OPTIONAL CALL [ variable_scope ] { subquery }
OPTIONAL CALL function( [ argument [, argument ] ... ] ) YIELD yield_list
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`OPTIONAL` 可用于 [`CALL`](/zh/agensgraph/reference/clauses/call/) 的两种形式，即内联子查询和具名函数。普通 `CALL` 将调用结果与输入行连接，调用没有返回行时，对应输入行就被丢弃。`OPTIONAL CALL` 会转换为**左连接**，保留该输入行。

- 系统**逐条输入行**判断。相关调用对某一行没有找到结果时，仅在该行上填入 null，其他行不受影响。
- 在这样的行中，调用原本应绑定的所有变量都变为 null，无论其类型是顶点、边、路径、列表、映射还是标量。
- 这是 SQL 空值，有别于 jsonb 的 `null`。请使用 `IS NULL` 检测。
- `OPTIONAL` 只保留已有输入行。如果输入为空，输出也为空。
- 保留下来的行仍是普通行，后续子句仍可把它展开为多行。

## 参数 {#parameters}

variable_scope
: 子查询可以访问的外层变量。与 [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) 一样，可写成 `(v, w)`、`(*)`、`()`，也可在花括号内用 `WITH` 导入。导入规则完全相同，裸 `OPTIONAL CALL { … }` 不导入变量。

subquery
: 以 `RETURN` 结尾的只读查询。

function, argument, yield_list
: 含义同 [`CALL … YIELD`](/zh/agensgraph/reference/clauses/call-yield/)。仍然必须指定 `YIELD`。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

示例中的三个人，Keanu Reeves 参演了四部影片，Ryan Gosling 一部，Christopher Nolan 没有参演。`OPTIONAL CALL` 会保留这位导演。

```cypher
MATCH (p:person) WHERE p.name IN ['Keanu Reeves', 'Ryan Gosling', 'Christopher Nolan']
OPTIONAL CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film }
RETURN p.name AS person, film ORDER BY person, film;
```

```
       person        |            film
---------------------+----------------------------
 "Christopher Nolan" |
 "Keanu Reeves"      | "The Matrix"
 "Keanu Reeves"      | "The Matrix Reloaded"
 "Keanu Reeves"      | "The Matrix Resurrections"
 "Keanu Reeves"      | "The Matrix Revolutions"
 "Ryan Gosling"      | "Blade Runner 2049"
(6 rows)
```

去掉 `OPTIONAL`，同一个查询体会丢弃导演所在的行，另两人不受影响。

```cypher
MATCH (p:person) WHERE p.name IN ['Keanu Reeves', 'Ryan Gosling', 'Christopher Nolan']
CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film }
RETURN p.name AS person, film ORDER BY person, film;
```

```
     person     |            film
----------------+----------------------------
 "Keanu Reeves" | "The Matrix"
 "Keanu Reeves" | "The Matrix Reloaded"
 "Keanu Reeves" | "The Matrix Resurrections"
 "Keanu Reeves" | "The Matrix Revolutions"
 "Ryan Gosling" | "Blade Runner 2049"
(5 rows)
```

三人分别产生四行、一行和一条保留行。一个调用产生几行，取决于各条输入行。

### 函数没有返回行时保留输入行 {#preserve-a-row-a-function-yielded-nothing-for}

对于具名调用，`OPTIONAL` 的位置相同，适用于函数对某些输入返回空集的情况。

```cypher
MATCH (m:movie) WHERE m.title IN ['The Matrix', 'Avatar']
OPTIONAL CALL generate_series(1, CASE WHEN m.title = 'Avatar' THEN 0 ELSE 2 END)
         YIELD generate_series AS n
RETURN m.title AS film, n ORDER BY film, n;
```

```
     film     | n
--------------+---
 "Avatar"     |
 "The Matrix" | 1
 "The Matrix" | 2
(3 rows)
```

`generate_series(1, 0)` 为空，因此《Avatar》那一行保留下来，其中 `n` 为 null。去掉 `OPTIONAL`，该行便会消失，只剩《The Matrix》的两行。

### 检测保留下来的空值 {#test-a-preserved-binding}

保留行中，查询体原本应返回的每个变量都取 SQL 空值。

```cypher
MATCH (p:person {name: 'Christopher Nolan'})
OPTIONAL CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film, m.year AS year }
RETURN film IS NULL AS film_is_null, year IS NULL AS year_is_null;
```

```
 film_is_null | year_is_null
--------------+--------------
 t            | t
(1 row)
```

### 确认不会凭空增加行 {#confirm-that-no-row-is-invented}

`OPTIONAL` 保留输入行。如果输入中没有行，就没有可以保留的行。

```cypher
MATCH (p:person {name: 'Nobody'})
OPTIONAL CALL (p) { MATCH (p)-[:acted_in]->(m:movie) RETURN m.title AS film }
RETURN p.name AS person, film;
```

```
 person | film
--------+------
(0 rows)
```

## 注意事项 {#notes}

执行计划直接展示了这一机制。`generate_series` 扫描位于 `Nested Loop Left Join` 可填充空值的一侧，正是这个连接保留了《Avatar》所在的行。

```cypher
EXPLAIN (COSTS OFF)
MATCH (m:movie) WHERE m.title IN ['The Matrix', 'Avatar']
OPTIONAL CALL generate_series(1, CASE WHEN m.title = 'Avatar' THEN 0 ELSE 2 END)
         YIELD generate_series AS n
RETURN m.title AS film, n;
```

```
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Nested Loop Left Join
   ->  Seq Scan on movie m
         Filter: (properties.'title' = ANY ('{"\"The Matrix\"","\"Avatar\""}'::jsonb[]))
   ->  Function Scan on generate_series
(4 rows)
```

某些查询体总会返回至少一行，此时 `OPTIONAL` 不改变结果。典型情形是无分组的聚合，它总会产生一行，因此没有演出记录的人会得到 `0`。可对照 [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/#aggregate-per-row-without-collapsing-the-pipeline) 中的 `films` 列。

`OPTIONAL` 不放宽其他限制。查询体出现写入子句仍报语法错误，返回外层已有名称仍会被拒绝，裸 `OPTIONAL CALL { … }` 也仍然不导入变量。

## 兼容性 {#compatibility}

> [!NOTE] GQL 标准符合性
> :class: gql-conformance
>
> 实现 GQL *过程调用语句*（ISO/IEC 39075:2024 §15.1）的 `OPTIONAL` 前缀，适用于 §15.2 的*内联过程调用*和 §15.3 的*具名过程调用*。
>
> - **支持**在两种调用前使用 `OPTIONAL`，逐行保留输入，并将所有输出变量绑定为空值。
> - **不支持**对数据修改调用（§13.6）使用 `OPTIONAL`，因为这里的调用不能写入图。
>
> 各项支持情况见 [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)。

### openCypher {#opencypher}

`OPTIONAL CALL` 源自 GQL，openCypher 只有 `OPTIONAL MATCH`。在两种写法都适用的场景中，结果一致。标准将 `OPTIONAL MATCH p` 定义为 `OPTIONAL CALL (imports) { MATCH p RETURN vars }`，因此 `OPTIONAL CALL` 是同一机制更一般的形式。

## 另请参阅 {#see-also}

- [`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/)：在模式匹配时同样保留输入行
- [`CALL`](/zh/agensgraph/reference/clauses/call/) **GQL**：两种调用形式
- [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) **GQL**：内联形式及其导入列表
- [`CALL … YIELD`](/zh/agensgraph/reference/clauses/call-yield/) **GQL**：具名函数形式
- [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)
