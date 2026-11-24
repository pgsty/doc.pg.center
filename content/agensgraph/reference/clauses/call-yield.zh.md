---
title: "CALL … YIELD"
linkTitle: "CALL … YIELD"
description: "调用具名函数，将返回的行与当前工作行连接，并把所选输出列加入工作行。"
type: docs
weight: 230
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/call-yield.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**  **自 2.18 起提供**

调用具名函数，将返回的行与当前工作行连接，并把所选输出列加入工作行。

## 语法 {#synopsis}

```text
[ OPTIONAL ] CALL function( [ argument [, argument ] ... ] ) YIELD *
[ OPTIONAL ] CALL function( [ argument [, argument ] ... ] ) YIELD column [ AS alias ] [, column ] ...
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

该子句会生成函数扫描，与前一子句的结果行连接，类似于横向执行 `SELECT * FROM function(arguments)`。`YIELD` 从函数结果中选择列，只能引用函数的输出。即使查询已绑定同名变量，引用函数未返回的列也会报错。

- **必须**写 `YIELD`。只写 `CALL f(x)` 而省略 `YIELD` 会报语法错误。
- 该子句不能放在查询的开头或结尾。语句开头的 `CALL` 会被解析为 PostgreSQL 的 SQL `CALL`，因此以 `CALL f() YIELD …` 开头会报语法错误。
- 若参数引用前面绑定的变量，这就是**相关**调用，对每条输入行执行一次。若参数均为常量，则函数只执行一次，其返回行与流水线中的行做交叉连接。
- 返回的列按普通变量处理，可以过滤、聚合、排序，也可传给后续的 `MATCH`。
- 若函数未返回任何行，对应的输入行会像内连接一样被**丢弃**。用 [`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/) 可以保留它。

## 参数 {#parameters}

function
: 待调用函数的名称。若 `search_path` 找不到该函数，须写上模式名。即使没有参数也要写括号。若指定过程，将报 `<name>() is a procedure`。

argument
: 按输入行求值的表达式。访问属性得到的是 `jsonb`，若函数参数要求其他类型，需要显式转换。

column
: 函数的输出列。标量函数或返回单列集合的函数只有一列，与函数同名。返回复合类型或声明为 `RETURNS TABLE` 的函数按字段名输出各列。`YIELD *` 选取所有列。如果没有与函数同名的列，函数名代表整行。这样，声明为 `RETURNS SETOF vertex` 或 `RETURNS SETOF edge` 的函数就能直接返回顶点或边。其他未知名称会报 `function f has no output column "x"`。

alias
: 输出列的新名称。原列名已在查询中绑定时，必须指定别名。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

将一部影片的属性展开为多行。`jsonb_each_text` 返回两列，`YIELD` 列出了这两列。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_each_text(jsonb_build_object('title', m.title, 'year', m.year, 'genre', m.genre))
     YIELD key, value
RETURN key AS property, value ORDER BY property;
```

```
 property |    value
----------+--------------
 "genre"  | "Action"
 "title"  | "The Matrix"
 "year"   | "1999"
(3 rows)
```

### 为输出列改名 {#rename-a-yielded-column}

`AS` 指定的新名称供所有后续子句使用。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_each_text(properties(m)) YIELD key AS property
RETURN property ORDER BY property;
```

```
  property
-------------
 "embedding"
 "genre"
 "plot"
 "title"
 "year"
(5 rows)
```

可以只选择部分列。这里没有绑定 `value`。

### 用 YIELD * 选取所有列 {#take-every-column-with-yield}

返回单列集合的函数以函数名作为列名。

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure'
CALL generate_series(1, 2) YIELD *
RETURN m.title AS film, generate_series AS n ORDER BY n;
```

```
      film       | n
-----------------+---
 "Jurassic Park" | 1
 "Jurassic Park" | 2
(2 rows)
```

参数均为常量，因此 `generate_series` 只执行一次，返回的两行与影片行做交叉连接。

### 在调用中引用匹配行 {#correlate-the-call-with-the-matched-row}

传入当前行的值，函数便会逐行执行。`m.year` 的类型是 `jsonb`，所以需要类型转换。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, (m.year)::int) YIELD generate_series AS n
RETURN count(n) AS years;
```

```
 years
-------
 1999
(1 row)
```

省略转换就无法解析函数。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, m.year) YIELD generate_series AS n
RETURN count(n);
```

```
ERROR:  function generate_series(integer, jsonb) does not exist
LINE 2: CALL generate_series(1, m.year) YIELD generate_series AS n
        ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

### 串联两次调用 {#chain-two-calls}

第二次调用可引用第一次调用返回的列。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, 2) YIELD generate_series AS n
CALL generate_series(1, n) YIELD generate_series AS k
RETURN n, k ORDER BY n, k;
```

```
 n | k
---+---
 1 | 1
 2 | 1
 2 | 2
(3 rows)
```

### 返回整行 {#yield-the-whole-row}

如果没有与函数同名的输出列，函数名便代表整行。`jsonb_each_text` 返回由 `(key, value)` 组成的行。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL jsonb_each_text(jsonb_build_object('title', m.title, 'year', m.year))
     YIELD jsonb_each_text AS pair
RETURN pair ORDER BY pair;
```

```
                  pair
-----------------------------------------
 {"key": "title", "value": "The Matrix"}
 {"key": "year", "value": "1999"}
(2 rows)
```

声明为 `RETURNS SETOF vertex` 的函数也以这种方式返回顶点，用函数名即可引用。

## 注意事项 {#notes}

执行计划可以区分两种调用。相关调用采用 `Nested Loop`，函数扫描位于内侧。不相关调用把函数扫描放在外侧，并将图扫描结果物化。

```cypher
EXPLAIN (COSTS OFF)
MATCH (m:movie) CALL generate_series(1, (m.year)::int) YIELD generate_series AS n
RETURN m.title, n;
```

```
               QUERY PLAN
----------------------------------------
 Nested Loop
   ->  Seq Scan on movie m
   ->  Function Scan on generate_series
(3 rows)
```

输出名与当前作用域内某个绑定重名时会报 `variable "m" yielded by CALL is already bound in the outer query`。使用 `AS` 改名即可。

反之也一样。即使前面已绑定同名变量，引用函数未输出的列也会报错。`YIELD` 只能指向函数的输出。

```cypher
MATCH (m:movie {title: 'The Matrix'})
CALL generate_series(1, 2) YIELD m AS n
RETURN n;
```

```
ERROR:  function generate_series has no output column "m"
LINE 2: CALL generate_series(1, 2) YIELD m AS n
                                         ^
```

> [!NOTE]
> 不能调用返回伪类型 `record` 的函数，因为此子句无法指定 PostgreSQL 要求的列定义列表。`CALL jsonb_to_recordset(…) YIELD *` 会报 `a column definition list is required for functions returning "record"`。可改在 SQL 子查询中调用。

## 兼容性 {#compatibility}

> [!NOTE] GQL 标准符合性
> :class: gql-conformance
>
> 实现 GQL 的*具名过程调用*（ISO/IEC 39075:2024 §15.3）和 §16.14 的*结果列子句*，属于 §15.1 的*过程调用语句*。
>
> - **支持**参数列表、相关参数、`YIELD *` 和 `YIELD column [AS alias]`、§16.14 语法规则 7（输出项必须引用过程结果中的列）、语法规则 6（拒绝重复别名）及 `OPTIONAL` 前缀。
> - **不支持**调用 GQL 过程。§15.3 根据 §17.5 的目录解析*过程引用*。AgensGraph 没有这个目录，名称会解析为 PostgreSQL 函数。
> - **差异**：§15.3 规定 `YIELD` 可省略。AgensGraph 要求调用为工作表增加列，因此必须写出该子句。
>
> 各项支持情况见 [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)。

### openCypher {#opencypher}

openCypher 的语法类似，但从过程注册表解析名称（如 `db.labels()` 和 `dbms.components()`），也允许将不含 `YIELD` 的 `CALL proc()` 写为独立语句。AgensGraph 没有该注册表，也不支持独立调用，名称解析为 PostgreSQL 函数，且必须写 `YIELD`。

## 另请参阅 {#see-also}

- [`CALL`](/zh/agensgraph/reference/clauses/call/) **GQL**：两种调用形式，以及例程在这里的含义
- [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) **GQL**：内联调用形式
- [`OPTIONAL CALL`](/zh/agensgraph/reference/clauses/optional-call/) **GQL**：当函数未返回任何行时保留输入行
- [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)
