---
title: FOR 子句
linkTitle: FOR 子句
description: 把列表展开为行，每个元素一行，并可选择绑定每个元素的位置。
type: docs
weight: 170
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/for.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**  **2.18 新增**

把列表展开为行，每个元素一行，并可选择绑定每个元素的位置。它是 Cypher
`UNWIND` 的 GQL 对应形式。

## 语法概要 {#synopsis}

```text
FOR variable IN list [ WITH OFFSET [ AS offset_variable ] ]
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`FOR` 会把每个输入行与列表中的元素连接，因此遇到 *n* 个元素列表的输入行会变成
*n* 个输出行。当列表依赖该行时，展开会逐行运行。

- 元素变量必须是**新**名称。复用作用域中的名称会引发
  `duplicate variable "<name>"`。
- `WITH OFFSET` 绑定每个元素的位置。偏移从 **0** 开始。
- 空列表、null 列表和缺失属性都会产生**零行**，因此对空内容执行 `FOR`
  会丢弃其输入行。
- 标量不是列表，会被拒绝，而不会被包装成列表。
- `FOR` 可以开启查询、位于查询中间，或驱动写子句。它不能结束查询。

## 参数 {#parameters}

variable
: 绑定到每个输出行一个元素的名称。不能已存在于作用域中。

list
: 产生列表的任何表达式：字面量、`range()`、列表值属性、由更早的 `collect()`
  构建的列表，或用 `+` 连接的两个列表。

offset_variable
: 绑定到元素从 0 开始的位置的名称。省略 `AS` 子句时，位置会绑定到
  `offset`。这是一个保留字，因此之后处处都必须写成 `"offset"`。优先使用
  `AS` 形式。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

展开标题列表并逐个查找。`FOR` 与 Cypher 的 `UNWIND`
展开同一个列表。切换标签页比较：

{{< tabs >}}
{{< tab label="GQL — FOR" >}}
```cypher
FOR t IN ['The Matrix', 'Inception', 'Gattaca']
MATCH (m:movie {title: t})
RETURN t AS title, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< tab label="Cypher — UNWIND" >}}
```cypher
UNWIND ['The Matrix', 'Inception', 'Gattaca'] AS t
MATCH (m:movie {title: t})
RETURN t AS title, m.year AS year ORDER BY year;
```
{{< /tab >}}
{{< /tabs >}}
```
    title     | year
--------------+------
 "Gattaca"    | 1997
 "The Matrix" | 1999
 "Inception"  | 2010
(3 rows)
```

### 在元素展开时编号 {#number-the-elements-as-they-expand}

`WITH OFFSET AS` 为位置命名。当列表顺序本身就是答案时，例如排名的标题列表，你会需要它：

```cypher
FOR t IN ['The Matrix', 'Inception', 'Gattaca'] WITH OFFSET AS i
MATCH (m:movie {title: t})
RETURN i, t AS title ORDER BY i;
```

```
 i |    title
---+--------------
 0 | "The Matrix"
 1 | "Inception"
 2 | "Gattaca"
(3 rows)
```

第一个元素的位置是 0，不是 1。

### 不命名而使用偏移 {#reach-the-offset-without-naming-it}

省略 `AS` 子句仍会绑定位置，但名称是 `offset`，这是保留关键字。后续每次引用都必须加引号：

```cypher
FOR t IN ['The Matrix', 'Inception'] WITH OFFSET RETURN "offset", t;
```

```
 offset |      t
--------+--------------
 0      | "The Matrix"
 1      | "Inception"
(2 rows)
```

去掉引号后查询无法解析：

```cypher
FOR t IN ['The Matrix'] WITH OFFSET RETURN offset, t;
```

```
ERROR:  syntax error at or near "offset"
LINE 1: FOR t IN ['The Matrix'] WITH OFFSET RETURN offset, t;
                                                   ^
```

### 展开列表值属性 {#expand-a-list-valued-property}

列表可以来自匹配到的行；此时展开会逐行运行：

```cypher
MATCH (m:movie {title: 'The Matrix'})
FOR e IN m.embedding
RETURN e ORDER BY e;
```

```
      e
-------------
 -0.11921061
 -0.07594558
 0.04081754
 0.29592122
(4 rows)
```

### 生成查询所需的行 {#generate-the-rows-a-query-needs}

`range()` 与其他列表一样，因此 `FOR` 可以基于生成的键驱动查找：

```cypher
FOR y IN range(1999, 2001)
MATCH (m:movie {year: y})
RETURN y, m.title AS film ORDER BY y, film;
```

```
  y   |     film
------+--------------
 1999 | "The Matrix"
(1 row)
```

## 说明 {#notes}

`FOR` 编译为 lateral `unnest()`，而 `UNWIND` 编译为 `ProjectSet`。
二者含义可互换，但执行计划不同：

```cypher
EXPLAIN (COSTS OFF) FOR x IN [1, 2, 3] RETURN x;
```

```
                 QUERY PLAN
--------------------------------------------
 Function Scan on unnest _agens_default_for
(1 row)
```

由于展开经过 `unnest()`，标量源是类型错误，而不是单元素列表。整数会引发
`function unnest(integer) does not exist`，标量属性会引发
`cannot extract elements from a scalar`。相反，null 会被视为空列表，不产生任何行。

> [!NOTE]
> `FOR` 在 PostgreSQL 中已是保留关键字，因此该子句没有给标识符名称添加新的限制。`offset`
> 同样是保留字，这就是裸 `WITH OFFSET` 形式在回读时必须加引号的原因。

## 兼容性 {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> 实现 GQL *FOR statement*（ISO/IEC 39075:2024 §14.8）、Feature GQ10 “FOR
> statement: list value support” 以及 Feature GQ24 “FOR statement: WITH OFFSET”。
>
> - **支持**——列表值表达式的展开、按输入行求值、null 源视为空列表，以及带
>   `WITH OFFSET` 的标准所规定的从 0 开始位置（§14.8，General Rule 2 中的 `j−1`）。
> - **不支持**——`WITH ORDINALITY`（Feature GQ11），即从 1 开始的对应形式；请改为给偏移加一。同样不支持的还有
>   `<binding table reference value expression>` 作为源（Feature GQ23），因为 AgensGraph
>   没有命名绑定表。
> - **偏差**——标准写位置变量时不使用 `AS`（`WITH OFFSET i`）。AgensGraph 要求
>   `WITH OFFSET AS i`；裸 `WITH OFFSET` 会把名称默认为 `offset`。
>
> 在 [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)中跟踪状态。

### openCypher {#opencypher}

openCypher 将该子句写作 [`UNWIND … AS x`](/zh/agensgraph/reference/clauses/unwind/)；AgensGraph
原样接受它，并且它没有偏移形式。

## 另见 {#see-also}

- [`UNWIND`](/zh/agensgraph/reference/clauses/unwind/)——没有偏移的 Cypher 对应形式
- [`INSERT`](/zh/agensgraph/reference/clauses/insert/) **GQL**——`FOR` 可以驱动的写入
- [`LET`](/zh/agensgraph/reference/clauses/let/) **GQL**
- [`FILTER`](/zh/agensgraph/reference/clauses/filter/) **GQL**——收窄展开后的行
- [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/)——排序 `FOR` 产生的行
- [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)
