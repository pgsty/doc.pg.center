---
title: "UNWIND"
linkTitle: "UNWIND"
description: "将列表展开，每个元素产生一条工作行。"
type: docs
weight: 160
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/unwind.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


将列表展开，每个元素产生一条工作行。

## 语法 {#synopsis}

```text
UNWIND list_expression AS variable
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`UNWIND` 将列表展开到流水线中，为每个元素生成一行，将 *variable* 绑定到该元素，其余已有变量原样传递。其作用与 `collect()` 相反，可将含有一个列表的单行展开为各含一个元素的多行。

- **必须**写 `AS variable`，不能省略变量名。
- 列表可以是**字面量**、**值为列表的属性**、`collect()` 生成的变量，或任何返回 jsonb 数组或 PostgreSQL 数组的表达式。标量会被拒绝。
- **空列表**不产生结果行，对应的整条输入行随之消失。
- 列表**内部的空值**也是元素，每个空值同样产生一行。
- `UNWIND` 对每条输入行分别执行，生成的行数会相乘。例如，三条输入行各展开一个两元素列表，共得到六行。
- `UNWIND` 可以位于查询开头或其他子句之后，但不能结束查询。
- 连续使用两个 `UNWIND`，可将嵌套列表展平。

[`FOR`](/zh/agensgraph/reference/clauses/for/) 是 GQL 中对应的子句，还可选用元素序号。

## 参数 {#parameters}

list_expression
: 返回 jsonb 数组或 PostgreSQL 数组的表达式。

variable
: 绑定到各元素的变量名，所有后续子句均可引用。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 展开列表字面量 {#expand-a-list-literal}

```cypher
UNWIND [1, 91, 203, 1, 7, 91] AS n
RETURN n;
```

```
  n
-----
 1
 91
 203
 1
 7
 91
(6 rows)
```

按列表顺序返回六行，保留重复项。

### 对列表去重并排序 {#deduplicate-and-sort-a-list}

不能就地对列表应用 `DISTINCT`。可以先展开，对结果行去重，再重新收集为列表。

```cypher
UNWIND [1, 91, 203, 1, 7, 91] AS n
WITH DISTINCT n
ORDER BY n
RETURN collect(n) AS uniq;
```

```
      uniq
-----------------
 [1, 7, 91, 203]
(1 row)
```

### 用列表驱动 MATCH {#drive-a-match-from-a-list}

每个元素生成一行，再依次参与匹配。

```cypher
UNWIND ['The Matrix', 'Inception'] AS t
MATCH (m:movie {title: t})
RETURN m.title AS film, m.year AS year;
```

```
     film     | year
--------------+------
 "The Matrix" | 1999
 "Inception"  | 2010
(2 rows)
```

客户端可以将一组键作为单个列表参数传入，这是按这些键执行查询的常见方式。

### 展开值为列表的属性 {#expand-a-list-valued-property}

属性值可以是列表，用 `UNWIND` 即可展开。

```cypher
MATCH (m:movie {title: 'The Matrix'})
UNWIND m.embedding AS component
RETURN component;
```

```
  component
-------------
 -0.07594558
 0.04081754
 0.29592122
 -0.11921061
(4 rows)
```

### 反向展开 collect 的结果 {#undo-a-collect}

`collect()` 将行收集为列表，`UNWIND` 将其展开。两者配合可以先聚合，再回到逐行处理。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH collect(DISTINCT m.genre) AS genres
UNWIND genres AS genre
RETURN genre
ORDER BY genre;
```

```
    genre
-------------
 "Action"
 "Adventure"
 "Sci-Fi"
(3 rows)
```

### 展平嵌套列表 {#flatten-a-list-of-lists}

连续使用两个 `UNWIND`，第二个展开第一个刚绑定的变量。

```cypher
UNWIND [[1, 2], [3]] AS pair
UNWIND pair AS x
RETURN pair, x;
```

```
  pair  | x
--------+---
 [1, 2] | 1
 [1, 2] | 2
 [3]    | 3
(3 rows)
```

### 展开空列表 {#expand-an-empty-list}

不产生结果行，相应的输入行也会消失。

```cypher
UNWIND [] AS x RETURN x;
```

```
 x
---
(0 rows)
```

若列表为空时仍须保留该行，可使用 [`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/) 或 `CASE` 表达式加以保护。

### 保留空值 {#keep-the-nulls}

空值也是列表元素。

```cypher
UNWIND [1, NULL, 3] AS x RETURN x;
```

```
  x
------
 1
 null
 3
(3 rows)
```

结果列的类型是 jsonb，因此显示为 `null`。jsonb 的 null 本身就是一个值。

## 注意事项 {#notes}

`UNWIND` 要求输入为列表。标量不会自动变成单元素列表，单独的 `NULL` 也不会被视为空列表。

```cypher
UNWIND 3 AS x RETURN x;
```

```
ERROR:  expression must be jsonb or array, but integer
LINE 1: UNWIND 3 AS x RETURN x;
               ^
```

```cypher
UNWIND NULL AS x RETURN x;
```

```
ERROR:  expression must be jsonb or array, but unknown
LINE 1: UNWIND NULL AS x RETURN x;
               ^
```

若属性可能缺失，可先用表达式提供列表默认值，例如 `UNWIND coalesce(m.tags, []) AS tag`。

## 兼容性 {#compatibility}

### UNWIND 的标准地位 {#unwind-is-not-a-gql-clause}

ISO/IEC 39075 没有 `UNWIND`。标准用于展开列表的是 `<for statement>`（§14.8），AgensGraph 通过 [`FOR`](/zh/agensgraph/reference/clauses/for/) 实现。`FOR` 还接受 `WITH OFFSET`，为每个元素给出从 0 开始的位置。`UNWIND` 没有这项功能。

## 另请参阅 {#see-also}

- [`FOR`](/zh/agensgraph/reference/clauses/for/) **GQL**：标准写法，可返回序号
- [`WITH`](/zh/agensgraph/reference/clauses/with/)：使用 `collect()` 和对行去重的位置
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：使用展开后的行驱动匹配
- [函数](/zh/agensgraph/reference/functions/)：`collect()` 及其他列表函数
