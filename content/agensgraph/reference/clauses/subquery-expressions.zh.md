---
title: "子查询值表达式"
linkTitle: "子查询值表达式"
description: "六种通过子查询计算值的表达式，可用于 RETURN、WHERE、FILTER、WITH 及 SQL 中。"
type: docs
weight: 260
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/subquery-expressions.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**  **自 2.18 起提供**

这六种表达式通过子查询计算一个值，可用在任何接受值的位置，包括 `RETURN`、`WHERE`、`FILTER`、`WITH` 及 SQL 中。

## 语法 {#synopsis}

```text
EXISTS { body }
COUNT { body }
COLLECT { body }
ARRAY { body }
VALUE { body }
expression [ NOT ] IN { body }
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

每种表达式都执行查询体，并将结果归约为一个值。与 [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) 不同，查询体直接关联表达式所在作用域的变量，无须声明导入列表。这些变量在整个查询体中都可见，不能用 `LET`、`UNWIND` 或 `FOR` 重新绑定，不能用 `WITH` 将其他值改为同名，也不能由 `CALL { }` 返回同名变量。`MATCH (n)` 引用外层节点，`WITH n` 则原样传递它。

下表列出六种表达式的返回值及查询体没有结果行时的行为。其中五种在结果为空时仍能返回自身类型的值，如假、零或空列表。只有 `VALUE { }` 没有这样的值，因而返回 null。

| 表达式 | 返回值 | 查询体返回零行时 |
| --- | --- | --- |
| `EXISTS { }` | 布尔值 | `false` |
| `COUNT { }` | 行数，类型为 `bigint` | `0` |
| `COLLECT { }` | 由查询体的唯一一列组成的列表 | `[]` |
| `ARRAY { }` | 与 `COLLECT` 相同 | `[]` |
| `VALUE { }` | 查询体的单个值，保留其类型 | `null` |
| `x IN { }` | 布尔值 | `false` |

### 可用的查询体 {#what-a-body-may-be}

查询体有四种形式，各表达式支持的形式如下。

| 查询体 | `EXISTS` / `COUNT` | `COLLECT` / `ARRAY` / `VALUE` / `IN` |
| --- | --- | --- |
| 直接书写的模式，可带 `WHERE` | 是 | 否 |
| `MATCH` 语句，包括 `OPTIONAL MATCH` | 是 | 否 |
| 以 `RETURN` 结尾的 GQL 读语句 | 是 | 是 |
| A SQL `SELECT` | 是 | 是 |

- **不允许写入子句。** `CREATE`、`INSERT`、`MERGE`、`SET`、`REMOVE`、`DELETE`、`DETACH DELETE` 均会在对应关键字处报语法错误。
- 读语句可包含 `DISTINCT`、`ORDER BY`、`SKIP`、`LIMIT`、集合运算符及嵌套的 `CALL { }`，但不能使用 [`NEXT`](/zh/agensgraph/reference/clauses/next/)。
- 直接书写的模式不能为路径命名（`EXISTS { p = (a)-[]->(b) }` 会报语法错误），可使用 `shortestpath()` 或变长边。
- **SQL `SELECT` 查询体与外层不相关**，无法访问外层变量。引用外层变量会报 `missing FROM-clause entry for table "<name>"`。

## 参数 {#parameters}

body
: 上述四种形式之一。`COLLECT`、`ARRAY`、`VALUE` 和 `IN` 要求子查询恰好返回一列。

expression
: 在 `x IN { }` 中，这是要查找的值。对于节点、关系或 graphid，与 `x IN [list]` 一样按标识匹配。若左侧为图元素，查询体却返回普通值，会报类型错误。其他类型的左值与 Cypher 查询体的输出列按 `jsonb` 比较。SQL 查询体保留其列类型，因此应先提取属性值，例如 `m.title #>> '{}'` 得到 `text`。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 检测模式是否存在 {#test-whether-a-pattern-exists}

`EXISTS { }` 可以短路求值。规划器会生成半连接或 `EXISTS` 子计划，无须统计全部匹配。最简短的查询体是直接写模式，它也接受 `WHERE`。

```cypher
MATCH (p:person)
WHERE EXISTS { (p)-[:directed]->(m:movie) WHERE m.year > 2015 }
RETURN p.name AS director ORDER BY director;
```

```
      director
--------------------
 "Denis Villeneuve"
 "Lana Wachowski"
(2 rows)
```

用在 `RETURN` 中时，它返回一个布尔列。没有匹配时，值为 `false`。

```cypher
MATCH (p:person {name: 'Keanu Reeves'}) RETURN EXISTS { (p)-[:directed]->(:movie) } AS directs;
```

```
 directs
---------
 f
(1 row)
```

### 统计匹配数 {#count-matches}

对模式使用 `COUNT { }` 会得到匹配总数。

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN COUNT { (:person)-[:acted_in]->(m) } AS cast_size;
```

```
 cast_size
-----------
 3
(1 row)
```

读语句查询体有自己的 `DISTINCT`、`LIMIT` 和分组规则，因而可以统计单个模式无法表达的结果。

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COUNT { MATCH (p:person)-[:acted_in]->(m) RETURN DISTINCT p } AS distinct_cast;
```

```
 distinct_cast
---------------
 3
(1 row)
```

### 将一列收集为列表 {#gather-a-column-into-a-list}

`COLLECT { }` 返回列表，保留查询体的顺序和空值。`ARRAY { }` 是同一表达式的另一种写法，采用 ARRAY 名称。

{{< tabs >}}
{{< tab label="GQL — ARRAY" >}}
```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN ARRAY { MATCH (p:person)-[:acted_in]->(m) RETURN p.name ORDER BY p.name } AS cast;
```
{{< /tab >}}
{{< tab label="Cypher — COLLECT" >}}
```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COLLECT { MATCH (p:person)-[:acted_in]->(m) RETURN p.name ORDER BY p.name } AS cast;
```
{{< /tab >}}
{{< /tabs >}}
```
                            cast
------------------------------------------------------------
 ["Carrie-Anne Moss", "Keanu Reeves", "Laurence Fishburne"]
(1 row)
```

查询体没有返回行时，结果是空列表。

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN COLLECT { MATCH (p:person)-[:acted_in]->(m) WHERE p.born > 2000 RETURN p.name } AS nobody;
```

```
 nobody
--------
 []
(1 row)
```

### 取得单个值 {#take-a-single-value}

`VALUE { }` 是标量子查询。它与本页其他形式不同，会保留输出列本身的类型，因此图元素能以原生形式返回。

```cypher
MATCH (m:movie {title: 'Inception'})
RETURN VALUE { MATCH (p:person)-[:directed]->(m) RETURN p.name } AS director;
```

```
      director
---------------------
 "Christopher Nolan"
(1 row)
```

```cypher
MATCH (m:movie {title: 'Inception'})
RETURN label(VALUE { MATCH (p:person)-[:directed]->(m) RETURN p }) AS yielded_type;
```

```
 yielded_type
--------------
 "person"
(1 row)
```

查询体至多可返回一行。返回多行会在运行时报错。若无法保证只有一个值，可加上 `ORDER BY … LIMIT 1` 或聚合。

```cypher
MATCH (m:movie {title: 'The Matrix'})
RETURN VALUE { MATCH (p:person)-[:acted_in]->(m) RETURN p.name } AS one_of_three;
```

```
ERROR:  more than one row returned by a subquery used as an expression
```

### 检测值是否出现在子查询结果中 {#test-membership-against-a-subquery}

`x IN { }` 使用半连接，无须物化整个列表，所以查询体很大时开销也较低。普通值与 Cypher 查询体的列按 `jsonb` 比较。

```cypher
MATCH (m:movie)
WHERE m.year IN { MATCH (x:movie) WHERE x.genre = 'Adventure' RETURN x.year }
RETURN m.title AS film ORDER BY film;
```

```
      film
-----------------
 "Jurassic Park"
(1 row)
```

节点按标识匹配，即使两个节点的属性完全相同，也仍是不同节点。此时半连接按节点 ID 执行。

```cypher
MATCH (p:person)
WHERE p IN { MATCH (d:person)-[:directed]->(:movie {title: 'Inception'}) RETURN d }
RETURN p.name AS director;
```

```
      director
--------------------
 "Christopher Nolan"
(1 row)
```

SQL 查询体保留输出列的类型。`rating.title` 的类型是 `text`，所以应先用 `#>> '{}'` 提取属性值，避免直接拿 `jsonb` 比较。

```cypher
MATCH (m:movie)
WHERE m.title #>> '{}' IN { SELECT title FROM rating WHERE source = 'audience' }
RETURN m.title AS film ORDER BY film;
```

```
      film
----------------
 "Inception"
 "Interstellar"
 "The Matrix"
(3 rows)
```

省略提取步骤将找不到比较运算符，并报 `operator does not exist: jsonb = text`。

### 在投影或 SQL 中使用 {#use-one-in-a-projection-or-from-sql}

子查询表达式有一个值，因此可以先用 `WITH` 投影，再判断其结果。

```cypher
MATCH (m:movie)
WITH m.title AS film, COUNT { (:person)-[:acted_in]->(m) } AS cast_size
FILTER cast_size > 2
RETURN film, cast_size;
```

```
     film     | cast_size
--------------+-----------
 "The Matrix" | 3
(1 row)
```

也可以从 SQL 使用它，由内嵌的 Cypher 查询提供所需变量。

```cypher
SELECT (MATCH (m:movie {title: 'The Matrix'}) RETURN COUNT { (:person)-[:acted_in]->(m) }) AS cast_size;
```

```
 cast_size
-----------
 3
(1 row)
```

## 注意事项 {#notes}

无论使用哪种表达式，只要查询体中出现写入子句，就会在该关键字处报错。

```cypher
MATCH (m:movie) RETURN COUNT { CREATE (:tmp) RETURN 1 AS one } AS n;
```

```
ERROR:  syntax error at or near "CREATE"
LINE 1: MATCH (m:movie) RETURN COUNT { CREATE (:tmp) RETURN 1 AS one...
                                       ^
```

如果某个绑定会遮蔽外层变量，也会被拒绝。错误与在顶层使用相应子句时相同。

```cypher
MATCH (m:movie) RETURN COUNT { LET m = 1 RETURN m } AS n;
```

```
ERROR:  variable "m" already exists
LINE 1: MATCH (m:movie) RETURN COUNT { LET m = 1 RETURN m } AS n;
                                           ^
HINT:  LET cannot redefine an existing variable; use a different name.
```

> [!NOTE]
> 与 PostgreSQL 一样，`ARRAY` 和 `IN` 是保留关键字。`COLLECT`、`COUNT`、`EXISTS` 和 `VALUE` 都不是保留字，仍可用作标识符。例如，`RETURN … AS value` 是合法写法。

## 兼容性 {#compatibility}

> [!NOTE] GQL 标准符合性
> :class: gql-conformance
>
> 六种形式中有两种属于标准。
>
> - `EXISTS { }` 实现 GQL 的*存在性谓词*（ISO/IEC 39075:2024 §19.4），包括该条款中的直接 `<graph pattern>`、`<match statement block>` 查询体以及嵌套查询规范。**完整支持**。
> - `VALUE { }` 实现 GQL 的*值查询表达式*（§20.6），对应特性 GQ18「标量子查询」，遵循通则 2 关于无结果时返回 null 的规定。**支持，但有一项差异**：§20.6 语法规则 10 要求查询体包含 `LIMIT 1` 或聚合。AgensGraph 接受任意查询体，返回多行时才在运行时报错。
>
> `COUNT { }`、`COLLECT { }`、`ARRAY { }` 和 `x IN { }` 都是**扩展**。ISO/IEC 39075:2024 没有 `COUNT` 的子查询形式。§20.9 只定义 `COUNT(*)` 和 `COUNT(<value expression>)`。标准的列表聚合 `COLLECT_LIST(…)` 也是对行做聚合。`COUNT { }` 和 `COLLECT { }` 源自 openCypher，`ARRAY { }` 仿照 SQL 的 `ARRAY(<subquery>)`，`x IN { }` 仿照 SQL 的 `IN (<subquery>)`。
>
> 各项支持情况见 [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)。

### openCypher {#opencypher}

openCypher 也支持 `EXISTS { }`、`COUNT { }` 和 `COLLECT { }`，含义相同，但没有 `ARRAY { }`、`VALUE { }` 和使用子查询的 `x IN { }`。它用 `head(COLLECT { … })` 取得标量，用 `x IN COLLECT { … }` 判断成员关系。两种写法在这里也能工作，但会物化整个列表，宜优先使用 `VALUE { }` 和 `x IN { }`。

## 另请参阅 {#see-also}

- [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) **GQL**：将子查询用作子句，显式列出导入变量
- [`FILTER`](/zh/agensgraph/reference/clauses/filter/) **GQL**：可使用这些谓词的过滤子句
- [`WHERE`](/zh/agensgraph/reference/clauses/where/)：另一处可使用谓词的位置
- [SQL 与 Cypher 混合查询](/zh/agensgraph/querying/combining-sql-and-cypher/)：如何使用 SQL 查询体
- [GQL 符合性对照表](/zh/agensgraph/appendix/gql-conformance/)
