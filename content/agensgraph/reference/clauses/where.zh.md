---
title: "WHERE"
linkTitle: "WHERE"
description: "约束模式或过滤投影结果。普通过滤会丢弃条件不为真的行。"
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/where.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

约束模式或过滤投影结果。普通过滤会丢弃条件不为真的行。

## 语法 {#synopsis}

```text
WHERE condition
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`WHERE` 依附于其他子句，其含义取决于它跟随以下哪一种子句。

- 跟在 [`MATCH`](/zh/agensgraph/reference/clauses/match/) 后时，条件属于匹配过程。判断条件时模式中的变量均已绑定，只有条件成立才会产生匹配。
- 跟在 [`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/) 后时，条件属于可选匹配。若条件不成立，系统仍**保留**对应输入行，模式引入的变量为空。
- 跟在 [`WITH`](/zh/agensgraph/reference/clauses/with/) 后时，条件在聚合完成后过滤投影结果。要根据聚合结果过滤，应将条件写在此处。

条件必须是布尔表达式，不能自动将其他类型当作真假值。使用 jsonb 字符串或数值作为条件会报错。`WHERE` 不接受聚合，请在 `WITH` 中先聚合再过滤。

单独写 `WHERE` 是语法错误，查询也不能以它结束。可独立串联的过滤子句是 [`FILTER`](/zh/agensgraph/reference/clauses/filter/)，接受 `FILTER condition` 和 `FILTER WHERE condition` 两种形式。

## 参数 {#parameters}

condition
: 布尔表达式，可用 `AND`、`OR`、`XOR` 和 `NOT` 组合判断条件。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 比较属性 {#compare-a-property}

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

### 组合条件 {#combine-conditions}

```cypher
MATCH (m:movie) WHERE m.genre = 'Action' AND m.year < 1995
RETURN m.title AS film
ORDER BY film;
```

```
             film
------------------------------
 "Terminator 2: Judgment Day"
 "The Terminator"
(2 rows)
```

除 `AND`、`OR` 和 `NOT` 外，也可使用 `XOR`。

```cypher
MATCH (m:movie) WHERE m.genre = 'Action' XOR m.year < 1995
RETURN count(*) AS n;
```

```
 n
---
 8
(1 row)
```

### 检测标签 {#test-a-label}

`label()` 以字符串形式返回元素标签，适用于顶点和边。

```cypher
MATCH (n) WHERE label(n) = 'person'
RETURN count(*) AS n;
```

```
 n
----
 28
(1 row)
```

要在一个模式中匹配多种边标签，可对名称列表使用 `IN`。边模式本身无法表达这项条件。

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

### 匹配子串或模式 {#match-on-a-substring-or-a-pattern}

`STARTS WITH`、`ENDS WITH` 和 `CONTAINS` 用于检测字符串属性。

```cypher
MATCH (m:movie) WHERE m.title STARTS WITH 'The Matrix'
RETURN count(*) AS n;
```

```
 n
---
 4
(1 row)
```

```cypher
MATCH (m:movie) WHERE m.title ENDS WITH 'Runner'
RETURN m.title AS film;
```

```
      film
----------------
 "Blade Runner"
(1 row)
```

`=~` 用于匹配 POSIX 正则表达式。

```cypher
MATCH (m:movie) WHERE m.title =~ '^Blade.*'
RETURN m.title AS film
ORDER BY film;
```

```
        film
---------------------
 "Blade Runner"
 "Blade Runner 2049"
(2 rows)
```

使用 `NOT` 对结果取反。属性没有 `!~` 运算符，这里也不能写 `NOT LIKE`。

```cypher
MATCH (m:movie) WHERE NOT m.title STARTS WITH 'The'
RETURN count(*) AS n;
```

```
 n
----
 11
(1 row)
```

### 检测缺失的属性 {#test-for-a-missing-property}

从未设置的属性读作空值，可以用 `IS NULL` 检测。

```cypher
MATCH (m:movie) WHERE m.runtime IS NULL
RETURN count(*) AS n;
```

```
 n
----
 18
(1 row)
```

### 检测模式是否存在 {#test-for-a-pattern}

子查询表达式可以判断是否存在匹配，同时不绑定模式中的变量。

```cypher
MATCH (p:person) WHERE EXISTS { MATCH (p)-[:directed]->() }
RETURN p.name AS director
ORDER BY director
LIMIT 4;
```

```
      director
---------------------
 "Andrew Niccol"
 "Christopher Nolan"
 "Denis Villeneuve"
 "James Cameron"
(4 rows)
```

### 在 WITH 后过滤聚合结果 {#filter-an-aggregate-with-with}

在 `WHERE` 中直接写聚合会被拒绝。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie) WHERE count(m) > 1
RETURN p.name;
```

```
ERROR:  aggregate functions are not allowed in WHERE
```

在 `WITH` 中先执行聚合，再过滤结果。`WITH` 自带的 `WHERE` 会在分组后执行。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p, count(m) AS films WHERE films >= 3
RETURN p.name AS actor, films
ORDER BY actor;
```

```
          actor          | films
-------------------------+-------
 "Arnold Schwarzenegger" | 3
 "Keanu Reeves"          | 4
(2 rows)
```

## 注意事项 {#notes}

属性存储 jsonb 值，将它与字面量比较时按 jsonb 的规则判断。数值在排序中大于所有字符串，因此拿带引号的数字与数值属性比较可能得不到预期结果。

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN m.year > '9999' AS num_gt_str, m.year > 1990 AS num_gt_num;
```

```
 num_gt_str | num_gt_num
------------+------------
 t          | t
(1 row)
```

应以与属性相同的类型书写字面量。如果存储类型不符合预期，可先转换属性，如 `m.year::int > 1990`。

> [!NOTE]
> `WHERE` 只接受布尔值。例如，`WHERE m.title` 会报 `cannot cast "The Matrix" (jsonb type string) to boolean`。与将非空字符串视为真的语言不同，这里应显式比较，或使用 `IS NOT NULL`。

## 兼容性 {#compatibility}

### 标签谓词（ISO/IEC 39075 §19.9） {#labeled-predicate-isoiec-39075-199}

标准写作 `n IS LABELED movie`，简写为 `n:movie`。AgensGraph 不接受这两种写法，请使用 `label(n) = 'movie'`。

### 模式谓词 {#pattern-predicates}

裸模式不是表达式，不能作为谓词。`WHERE (m)-[:related_to]->(:movie)` 和不带标签的 `WHERE (m)-[]->()` 都会报语法错误。请使用标准 §19.4 定义且 AgensGraph 支持的 `EXISTS { MATCH ... }` 包裹模式。

### SQL 字符串运算符 {#sql-string-operators}

Cypher 条件不支持 `LIKE` 或 `NOT LIKE`。`WHERE m.title LIKE 'Blade%'` 无论是否使用类型转换都会报语法错误。请使用 `STARTS WITH`、`ENDS WITH`、`CONTAINS` 或 `=~`。若要使用 SQL 运算符，可将 Cypher 包裹在 SQL 中，参见 [SQL 与 Cypher 混合查询](/zh/agensgraph/querying/combining-sql-and-cypher/)。

## 另请参阅 {#see-also}

- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：最常使用 `WHERE` 的子句
- [`OPTIONAL MATCH`](/zh/agensgraph/reference/clauses/optional-match/)：条件不成立时仍保留输入行
- [`WITH`](/zh/agensgraph/reference/clauses/with/)：在投影或聚合后过滤
- [`FILTER`](/zh/agensgraph/reference/clauses/filter/)：独立的过滤子句
- [子查询表达式](/zh/agensgraph/reference/clauses/subquery-expressions/)：`EXISTS`、`COUNT`、`COLLECT` 等
