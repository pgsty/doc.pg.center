---
title: "WITH"
linkTitle: "WITH"
description: "将工作行投影为一组新列，并交给下一子句。"
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/with.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


将工作行投影为一组新列，交给下一子句，相当于流水线中间的 `RETURN`。

## 语法 {#synopsis}

```text
WITH [ DISTINCT | ALL ] { * | expression [ AS alias ] } [, ...] [ WHERE condition ]
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`WITH` 结束当前一段流水线，并开始下一段。它与 [`RETURN`](/zh/agensgraph/reference/clauses/return/) 一样逐行计算表达式，再把生成的列交给下一子句。以下三种操作会用到它。

- **先聚合，再过滤或继续匹配。** `WHERE` 不能包含聚合，应在 `WITH` 中聚合，再过滤其输出。
- **只计算一次**，在多个后续子句中复用结果。
- **缩减中间结果**，用 `DISTINCT`、`ORDER BY` 和 `LIMIT` 减少后续高开销操作需要处理的数据。

作为投影，WITH 遵循以下规则。

- `WITH` **替换**当前作用域。只有投影列会传下去，后面引用被省略的变量会报 `variable does not exist`。若只想新增变量且保留已有变量，可写 `WITH *, expr AS v` 或使用 [`LET`](/zh/agensgraph/reference/clauses/let/)。
- 输出名在**同一子句内必须唯一**。两次投影同名列会报 `WITH passes on "..." more than once`。`RETURN` 没有这项限制。
- 它自带的 `WHERE` 在投影和聚合**之后**执行，因此可以引用聚合结果的别名。
- `ORDER BY`、`SKIP`/`OFFSET` 和 `LIMIT` 是跟在 `WITH` 之后的独立子句，也位于附属的 `WHERE` 之后。先过滤，再对保留的行排序和分页。
- `WITH` 既不能**开始**也不能结束 Cypher 查询。在语句开头，`WITH` 会被解释为 SQL 的公用表表达式，需要指定名称和括号内的查询。[`LET`](/zh/agensgraph/reference/clauses/let/) 没有这一歧义，可以作为首句。

## 参数 {#parameters}

DISTINCT
: 去掉投影中的重复行，再将结果传给下一子句。

ALL
: 保留重复行，默认如此。

\*
: 原样传递作用域内所有具名绑定。可同时列出其他项，例如用 `WITH *, expr AS v` 增加列且保留已有列。

expression
: 作用域内变量构成的任意 Cypher 表达式，可以包含聚合。

alias
: 后续子句使用的名称。除简单变量引用外，表达式都需要别名，以便后续子句可以引用。

condition
: 过滤投影结果的布尔表达式。在投影之后求值，因而可以引用本子句定义的别名。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 按计数过滤 {#filter-on-a-count}

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p.name AS actor, count(m) AS films
WHERE films > 1
RETURN actor, films
ORDER BY films DESC, actor;
```

```
          actor          | films
-------------------------+-------
 "Keanu Reeves"          | 4
 "Arnold Schwarzenegger" | 3
 "Carrie-Anne Moss"      | 2
 "Harrison Ford"         | 2
 "Laurence Fishburne"    | 2
 "Linda Hamilton"        | 2
(6 rows)
```

`count(m)` 按 `p.name` 分组，`WHERE` 检查结果列 `films`。若把同一聚合条件写在 `MATCH ... WHERE` 中，会报 `aggregate functions are not allowed in WHERE`。

### 添加新列并保留原有列 {#add-a-column-without-losing-the-others}

```cypher
MATCH (p:person)-[:directed]->(m:movie)
WITH *, m.year - p.born AS age_at_release
RETURN p.name AS director, m.title AS film, age_at_release
ORDER BY age_at_release
LIMIT 3;
```

```
     director      |       film       | age_at_release
-------------------+------------------+----------------
 "James Cameron"   | "The Terminator" | 30
 "Lilly Wachowski" | "The Matrix"     | 32
 "Andrew Niccol"   | "Gattaca"        | 33
(3 rows)
```

`WITH *` 将 `p` 和 `m` 保留在作用域内，所以 `RETURN` 仍能读取它们的属性。[`LET`](/zh/agensgraph/reference/clauses/let/) 无须写 `*` 也能做到这一点。

### 查看 WITH 丢弃了哪些变量 {#watch-what-a-with-drops}

投影中省略的变量随后就不再可见。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH m
RETURN p.name;
```

```
ERROR:  variable does not exist
LINE 1: ...ATCH (p:person)-[:acted_in]->(m:movie) WITH m RETURN p.name;
                                                                ^
```

### 在流水线中途去重 {#deduplicate-mid-pipeline}

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH DISTINCT m.genre AS genre
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

### 在继续匹配之前缩减输入 {#cut-the-pipeline-down-before-matching-further}

在 `WITH` 后用 `ORDER BY` 和 `LIMIT` 可以减少下一条子句需要处理的行数。

```cypher
MATCH (m:movie)
WITH m ORDER BY m.year DESC LIMIT 2
MATCH (p:person)-[:directed]->(m)
RETURN m.title AS film, p.name AS director
ORDER BY film;
```

```
            film            |      director
----------------------------+--------------------
 "Blade Runner 2049"        | "Denis Villeneuve"
 "The Matrix Resurrections" | "Lana Wachowski"
(2 rows)
```

只有最新的两部影片会进入第二个 `MATCH`。

### 分页在过滤之后执行 {#see-that-paging-follows-the-filter}

`WHERE` 属于 `WITH`，而 `ORDER BY` 和 `LIMIT` 位于其后，所以 `LIMIT` 只在通过过滤的行中计数。

```cypher
MATCH (m:movie)
WITH m.title AS film, m.genre AS genre WHERE genre = 'Action'
ORDER BY film LIMIT 3
RETURN film, genre;
```

```
             film             |  genre
------------------------------+----------
 "Terminator 2: Judgment Day" | "Action"
 "The Avengers"               | "Action"
 "The Matrix"                 | "Action"
(3 rows)
```

去掉过滤条件，同样的分页会选出完全不同的行，此时保留的是按片名排序的前三行。

```cypher
MATCH (m:movie)
WITH m.title AS film, m.genre AS genre
ORDER BY film LIMIT 3
RETURN film, genre;
```

```
        film         |  genre
---------------------+----------
 "Avatar"            | "Sci-Fi"
 "Blade Runner"      | "Sci-Fi"
 "Blade Runner 2049" | "Sci-Fi"
(3 rows)
```

### 拒绝重复的输出名 {#reject-a-repeated-output-name}

```cypher
MATCH (m:movie)
WITH m.title AS film, m.genre AS film
RETURN film;
```

```
ERROR:  WITH passes on "film" more than once
LINE 1: MATCH (m:movie) WITH m.title AS film, m.genre AS film RETURN...
                                              ^
```

若传递一个变量，又把别的表达式改为同名，也会发生冲突。`WITH m, m.title AS m` 会报 `WITH passes on "m" more than once`。

## 注意事项 {#notes}

`WHERE` 必须紧跟投影列表，位于任何 `ORDER BY`、`SKIP` 或 `LIMIT` 之前。若放在后面就会产生语法错误，例如 `WITH ... ORDER BY film WHERE genre = 'Action'` 无法通过解析。

## 另请参阅 {#see-also}

- [`RETURN`](/zh/agensgraph/reference/clauses/return/)：使用相同的投影结束查询
- [`LET`](/zh/agensgraph/reference/clauses/let/) **GQL**：增加绑定并保留已有变量
- [`WHERE`](/zh/agensgraph/reference/clauses/where/)：`WITH` 可包含的过滤条件
- [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/)、[`SKIP` 与 `LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)：跟在 `WITH` 之后的子句
- [`UNWIND`](/zh/agensgraph/reference/clauses/unwind/)：常用来反向展开 `collect()` 的结果
