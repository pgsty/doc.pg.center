---
title: "ORDER BY"
linkTitle: "ORDER BY"
description: "对工作表中的行排序。"
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/order-by.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

对工作表中的行排序。这是独立子句，可以在流水线的任意适当位置排序，包括中间步骤。

## 语法 {#synopsis}

```text
ORDER BY sort_key [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...]
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`ORDER BY` 对流水线中当前的行排序。它写在产生这些行的子句之后，作用于该子句的输出。前面的子句可以是 [`RETURN`](/zh/agensgraph/reference/clauses/return/)、[`WITH`](/zh/agensgraph/reference/clauses/with/) 或 [`MATCH`](/zh/agensgraph/reference/clauses/match/)。

- 先比较第一个排序键，相等时再比较下一个，依此类推。
- 各键默认升序排列，可显式写 `ASC`，或写 `DESC` 改为降序。
- 除非指定 `NULLS FIRST` 或 `NULLS LAST`，否则空值在 `ASC` 时排在**最后**，在 `DESC` 时排在**最前**。
- 排序键是表达式。`ORDER BY 2` 中的 2 是常量，所有行都相等，无法据此排序。详见[兼容性](#compatibility)。
- `ORDER BY` 既不能**开始**查询，也不能**结束**查询。
- 在 `RETURN DISTINCT` 之后，每个排序键都必须出现在投影列表中。

排序是独立子句，可在流水线中途使用。通常会紧跟 [`LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)，减少后续子句需要处理的行数。

## 参数 {#parameters}

sort_key
: 使用当前作用域内变量的表达式。在 `RETURN` 或 `WITH` 后，可以使用该子句定义的别名，也可以使用未列入投影的表达式。

ASC, DESC
: 升序或降序。默认 `ASC`。

NULLS FIRST, NULLS LAST
: 空值的位置。升序默认 `NULLS LAST`，降序默认 `NULLS FIRST`。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 按输出列排序 {#sort-by-a-projected-column}

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY year;
```

```
            film            | year
----------------------------+------
 "Blade Runner 2049"        | 2017
 "The Matrix Resurrections" | 2021
(2 rows)
```

### 按未输出的表达式排序 {#sort-by-something-you-did-not-project}

排序键是普通表达式，无须出现在结果列中。

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY m.year
LIMIT 3;
```

```
       film
------------------
 "Blade Runner"
 "The Terminator"
 "Total Recall"
(3 rows)
```

```cypher
MATCH (p:person)
RETURN p.name AS person
ORDER BY length(p.name) DESC
LIMIT 3;
```

```
         person
-------------------------
 "Arnold Schwarzenegger"
 "Matthew McConaughey"
 "Laurence Fishburne"
(3 rows)
```

### 按多个键分别升降序排列 {#sort-by-several-keys-in-different-directions}

```cypher
MATCH (m:movie)
RETURN m.genre AS genre, m.year AS year, m.title AS film
ORDER BY genre, year DESC
LIMIT 5;
```

```
  genre   | year |            film
----------+------+----------------------------
 "Action" | 2021 | "The Matrix Resurrections"
 "Action" | 2012 | "The Avengers"
 "Action" | 2003 | "The Matrix Reloaded"
 "Action" | 2003 | "The Matrix Revolutions"
 "Action" | 1999 | "The Matrix"
(5 rows)
```

先按 `genre` 升序，同一类型内再按 `year` 降序。

### 指定空值的位置 {#place-the-nulls}

`OPTIONAL MATCH` 可能留下空值，用它可以看出默认顺序。升序时空值排在最后。

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY directed;
```

```
      person       | directed
-------------------+-----------
 "Neill Blomkamp"  | "Elysium"
 "Ryan Gosling"    |
 "Sam Worthington" |
(3 rows)
```

降序时空值排在最前。

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY directed DESC;
```

```
      person       | directed
-------------------+-----------
 "Ryan Gosling"    |
 "Sam Worthington" |
 "Neill Blomkamp"  | "Elysium"
(3 rows)
```

`NULLS FIRST` 可以把空值放到最前，同时维持其余值原来的排序方向。

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY directed NULLS FIRST;
```

```
      person       | directed
-------------------+-----------
 "Ryan Gosling"    |
 "Sam Worthington" |
 "Neill Blomkamp"  | "Elysium"
(3 rows)
```

### 在流水线中途排序 {#sort-in-the-middle-of-a-pipeline}

在 `MATCH` 后使用 `ORDER BY` 并接上 `LIMIT`，可缩小后续子句处理的数据范围。

```cypher
MATCH (m:movie)
ORDER BY m.year DESC LIMIT 2
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

第二个 `MATCH` 只处理两行，原本有十八行。

### ORDER BY 的位置限制 {#where-order-by-cannot-go}

它不能放在查询开头。

```cypher
ORDER BY 1;
```

```
ERROR:  syntax error at or near "ORDER"
LINE 1: ORDER BY 1;
        ^
```

排序本身不输出查询结果，也不能放在查询结尾。

```cypher
MATCH (m:movie) ORDER BY m.title;
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

## 注意事项 {#notes}

按属性排序，实际比较的是 jsonb 值。jsonb 先按类型、再按值排序：数值大于所有字符串，两者又都大于 jsonb 空值。若排序键混合多种类型，而你希望统一比较，应先做类型转换。

## 兼容性 {#compatibility}

### 数字用作排序键时的含义 {#a-number-is-a-sort-key-not-a-column-reference}

SQL 中的 `ORDER BY 2` 按第二个输出列排序。这里的排序键是值表达式，整数只是常量，各行相等，既不会改变顺序，也不会报错。

```cypher
MATCH (m:movie) WHERE m.year > 2015
RETURN m.title AS film, m.year AS year
ORDER BY 2;
```

```
            film            | year
----------------------------+------
 "The Matrix Resurrections" | 2021
 "Blade Runner 2049"        | 2017
(2 rows)
```

行按扫描顺序返回。若要按年份排序，应像本页第一个示例一样写明键名。这符合 ISO/IEC 39075 §16.17：`<sort key>` 是 `<aggregating value expression>`，没有按列序号指定的形式。它与 SQL 的行为不同，应始终明确写出排序键。

### ASCENDING 和 DESCENDING（ISO/IEC 39075 §16.17） {#ascending-and-descending-isoiec-39075-1617}

标准允许使用 `ASCENDING`、`DESCENDING`，也允许 `ASC`、`DESC`。AgensGraph 只接受缩写。`ORDER BY film ASCENDING` 会报语法错误。

## 另请参阅 {#see-also}

- [`SKIP` 和 `LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)：通常用于排序之后的分页子句
- [`RETURN`](/zh/agensgraph/reference/clauses/return/)、[`WITH`](/zh/agensgraph/reference/clauses/with/)：排序所作用的投影
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：在流水线中途排序以减少后续工作量
