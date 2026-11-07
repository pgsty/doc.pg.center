---
title: LET 子句
linkTitle: LET 子句
description: 向工作记录添加计算值，而不丢弃已在作用域中的列。
type: docs
weight: 70
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/let.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**  **2.18 新增**

向工作记录添加计算值，而不丢弃已在作用域中的列。它是 Cypher
`WITH *, expr AS v` 的 GQL 标准对应形式。

## 语法概要 {#synopsis}

```text
LET variable = expression [, variable = expression ] ...
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`LET` 会基于作用域中已有变量上的表达式，向当前行引入一个或多个新变量。与
`WITH` 不同，它是**可累加的**：作用域中的每个绑定都会自动继续传递，因此
`LET` 永远不会意外从管道中丢弃变量。

- 每个变量都**只能引入**。作用域中已有的名称不能重新绑定；这一点既适用于顶层，也适用于子查询表达式或导入型
  `CALL { }` 的主体。
- 表达式**逐行**求值；不允许聚合。
- `LET` 可以**开启**查询或位于中间，但不能终止查询。它是适合用来开启语句的子句，因为 [`WITH`](/zh/agensgraph/reference/clauses/with/)
  在该位置表示 SQL 的公共表表达式。

## 参数 {#parameters}

variable
: 新绑定的名称。不能已存在于作用域中。对之后的每个子句可见。

expression
: 任何按行求值的值表达式：属性访问、算术、函数调用、`CASE`、列表/映射构造器。对每个输入行求值一次。

## 示例 {#examples}

这些示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

### 添加派生值并保留作用域中的所有内容 {#add-a-derived-value-and-keep-everything-in-scope}

GQL 与 Cypher 形式等价。切换标签页比较：

{{< tabs >}}
{{< tab label="GQL — LET" >}}
```cypher
MATCH (p:person)
LET age_in_2026 = 2026 - p.born
RETURN p.name AS name, age_in_2026
ORDER BY age_in_2026 LIMIT 3;
```
{{< /tab >}}
{{< tab label="Cypher — WITH" >}}
```cypher
MATCH (p:person)
WITH *, 2026 - p.born AS age_in_2026
RETURN p.name AS name, age_in_2026
ORDER BY age_in_2026 LIMIT 3;
```
{{< /tab >}}
{{< /tabs >}}
```
       name        | age_in_2026
-------------------+-------------
 "Ryan Gosling"    | 46
 "Neill Blomkamp"  | 47
 "Sam Worthington" | 50
(3 rows)
```

差异在于 `p` 的处理。`LET` 会自动传递它。`WITH`
形式必须用 `*` 显式请求；忘记 `*` 的 `WITH` 会丢弃 `p`，随后的 `RETURN`
便会失败。

### 用计算值开启查询 {#lead-a-query-with-computed-values}

因为 `LET` 可累加，它可以开启语句，在作用域尚无内容时生成初始值：

```cypher
LET radius = 7, area = 3.14159 * 7 * 7
RETURN radius, area;
```

```
 radius |   area
--------+-----------
 7      | 153.93791
(1 row)
```

### 只能引入 {#introduce-only}

作用域中已有的名称不能重新绑定：

```cypher
MATCH (p:person) LET p = 1 RETURN p;
```

```
ERROR:  variable "p" already exists
HINT:  LET cannot redefine an existing variable; use a different name.
```

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> 实现 GQL *LET statement*（ISO/IEC 39075:2024 §14.7）。
>
> - **支持**——变量定义、多个绑定、开头位置以及按行求值的表达式。
> - **不支持**——在聚合表达式上使用 `LET`。在[兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)中跟踪状态。

> [!NOTE]
> `LET` 在 2.18 中成为**保留关键字**。如果你在早期版本中把 `let`
> 用作标签或变量名，请加引号（`"let"`——双引号，不是反引号）或改名。属性键和
> `RETURN` 别名不受影响。

## 另见 {#see-also}

- [`WITH`](/zh/agensgraph/reference/clauses/with/)——Cypher 对应形式
- [`NEXT`](/zh/agensgraph/reference/clauses/next/) **GQL**
- [`RETURN`](/zh/agensgraph/reference/clauses/return/)
- [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)
