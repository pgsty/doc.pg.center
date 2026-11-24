---
title: "NEXT"
linkTitle: "NEXT"
description: "串联两条查询，将前一条返回的行作为后一条的输入。"
type: docs
weight: 190
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/next.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**  **自 2.18 起提供**

串联两条查询，将前一条返回的行作为后一条的输入。

## 语法 {#synopsis}

```text
query NEXT query [ NEXT query ] ...
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`NEXT` 将左侧查询的结果表作为右侧查询的输入表。它在两条完整查询之间执行组合，相当于单条查询内部的 `WITH`。

- `NEXT` 左侧的查询必须以 `RETURN` 结尾。
- 经过边界时**重置作用域**。右侧只能访问 `RETURN` 输出的列，其他变量不再可见。
- 列的类型跨越边界后保持不变。顶点、边和路径仍分别是顶点、边和路径。
- `NEXT` 按从左到右的顺序结合，`A NEXT B NEXT C` 相当于 `(A NEXT B) NEXT C`。
- 两侧均可使用由 [`UNION`](/zh/agensgraph/reference/clauses/union/)、`INTERSECT` 或 `EXCEPT` 组成的复合查询。
- 顶层语句以及 `EXPLAIN`、`PREPARE` 中的查询均可使用 `NEXT`。子查询中不能使用，包括 `CALL { }` 的查询体和子查询值表达式。

## 参数 {#parameters}

query
: 一条完整查询。`NEXT` 左侧须以 `RETURN` 结尾，并为所有输出列命名。表达式缺少别名时报 `expression in WITH must be aliased (use AS)`。右侧另起查询，开头可以是 `MATCH`、`OPTIONAL MATCH`、`CREATE`、`INSERT`、`MERGE`、`LOAD FROM`、`UNWIND`、`FOR`、`CALL`、`LET`、`RETURN` 或 `FINISH`。也可以从处理传入表的子句开始，即 `WITH`、`FILTER`、`ORDER BY`、`SKIP`、`OFFSET` 或 `LIMIT`。与普通查询一样，末尾须为 `RETURN`、`FINISH` 或写入子句。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

先找出一位导演执导的影片，再将这些影片传入第二条查询，查找演员。使用 `NEXT` 或中间的 `WITH` 可以组合出同样的两个步骤。切换标签页可比较两种写法。

{{< tabs >}}
{{< tab label="GQL — NEXT" >}}
```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN m
NEXT
MATCH (a:person)-[:acted_in]->(m)
RETURN m.title AS film, a.name AS actor ORDER BY film;
```
{{< /tab >}}
{{< tab label="Cypher — WITH" >}}
```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
WITH m
MATCH (a:person)-[:acted_in]->(m)
RETURN m.title AS film, a.name AS actor ORDER BY film;
```
{{< /tab >}}
{{< /tabs >}}
```
      film      |         actor
----------------+-----------------------
 "Inception"    | "Leonardo DiCaprio"
 "Interstellar" | "Matthew McConaughey"
(2 rows)
```

`m` 以顶点类型传到下一条查询，可以从该顶点继续遍历。

### 过滤第一条查询的聚合结果 {#filter-an-aggregate-computed-by-the-first-query}

`FILTER` 不能作为独立查询的开头，却可以紧跟 `NEXT`。这使得聚合结果可以像使用 `HAVING` 一样过滤，无须另写 `WITH`。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
RETURN p.name AS actor, count(m) AS films
NEXT
FILTER films > 2
RETURN actor, films ORDER BY actor;
```

```
          actor          | films
-------------------------+-------
 "Arnold Schwarzenegger" | 3
 "Keanu Reeves"          | 4
(2 rows)
```

### 串联三条查询 {#chain-three-queries}

每个 `NEXT` 都形成新的边界，从左向右求值。

```cypher
MATCH (m:movie) RETURN m.genre AS genre
NEXT
RETURN DISTINCT genre AS g
NEXT
RETURN count(g) AS genres;
```

```
 genres
--------
 3
(1 row)
```

### 引用第一条查询没有返回的变量 {#reach-a-variable-the-first-query-did-not-return}

只有输出列能传到下一条查询。引用其他变量会在解析阶段报错。

```cypher
MATCH (p:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
RETURN m
NEXT
RETURN p.name;
```

```
ERROR:  variable does not exist
LINE 4: RETURN p.name;
               ^
```

## 注意事项 {#notes}

`NEXT` 不增加运行时开销。系统将左侧查询的 `RETURN` 改写为 `WITH`，这与查询流水线在子句组之间使用的机制相同。因此，上述两个标签页里的查询生成相同的计划。

有两种误用会得到专门的报错。左侧查询没有以 `RETURN` 结尾时报 `a query statement before NEXT must end with RETURN`，以 `FINISH` 结尾时报 `FINISH cannot be followed by NEXT`。

最后一条查询也要有适当的结尾。`ORDER BY`、`SKIP`、`OFFSET` 和 `LIMIT` 都是独立子句，却都不能终结查询。若以其中任何一个结束，将报 `Cypher query must end with RETURN, FINISH or update clause`。可在后面加上 `RETURN` 或 `FINISH`。

`next` 是非保留关键字，可以用作变量名、标签名或属性名。

## 兼容性 {#compatibility}

> [!NOTE] GQL 标准符合性
> :class: gql-conformance
>
> 实现 GQL *过程体*（ISO/IEC 39075:2024 §9.2）中的 `<next statement>`，对应特性 GQ20「使用 NEXT 的高级线性组合」。
>
> - **支持**串联查询语句、按左结合顺序串联多条查询、在边界重置作用域，以及在任一侧使用集合运算。
> - **不支持**标准允许在 `NEXT` 与后续语句之间插入的可选 `YIELD` 子句。`NEXT YIELD a, b …` 会报语法错误。可在前一条查询的 `RETURN` 中投影并改名。
>
> 各项支持情况见 [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)。

### openCypher {#opencypher}

openCypher 没有 `NEXT`，始终用上例的 `WITH` 写法组合查询。AgensGraph 可直接运行这种写法。

## 另请参阅 {#see-also}

- [`WITH`](/zh/agensgraph/reference/clauses/with/)：单条 Cypher 查询中对应的组合方式
- [`LET`](/zh/agensgraph/reference/clauses/let/) **GQL**：不引入新边界即可增加列
- [`FILTER`](/zh/agensgraph/reference/clauses/filter/) **GQL**：可紧接 `NEXT` 使用的过滤子句
- [`FINISH`](/zh/agensgraph/reference/clauses/finish/) **GQL**
- [`RETURN`](/zh/agensgraph/reference/clauses/return/)：左侧查询必须使用的结尾
- [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)
