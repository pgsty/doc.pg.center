---
title: "RETURN"
linkTitle: "RETURN"
description: "结束查询并指定结果列。"
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/return.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

结束查询并指定结果列。

## 语法 {#synopsis}

```text
RETURN [ DISTINCT | ALL ] { * | expression [ AS alias ] } [, ...]
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`RETURN` 是最终投影，对每条工作行计算表达式，并将结果作为输出列。读查询必须以 `RETURN` 或 [`FINISH`](/zh/agensgraph/reference/clauses/finish/) 结尾。写查询还可以直接以写入子句结尾。

- **由属性得到的列以 jsonb 返回。** `RETURN m.title` 显示带引号的 `"The Matrix"`，`RETURN m.title::text` 也是如此。若需要原生标量，请在 SQL 中包裹这条查询。详见[注意事项](#notes)。
- `*` 输出当前作用域中所有**具名**绑定。模式中未命名的元素不会输出。
- 列表中的**聚合**会隐式分组，其他非聚合表达式成为分组键，相当于 SQL 中的 `GROUP BY`。
- `DISTINCT` 消除重复行。`ALL` 显式指定默认行为，保留重复行。
- `ORDER BY`、`SKIP`/`OFFSET` 和 `LIMIT` 都是跟在 `RETURN` 之后的**独立子句**。详见 [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/) 和 [`SKIP` 与 `LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)。
- 与 [`WITH`](/zh/agensgraph/reference/clauses/with/) 不同，`RETURN` 允许两个输出列重名，因为后续没有子句需要解析列名。

## 参数 {#parameters}

DISTINCT
: 消除结果中的重复行。

ALL
: 保留重复行，默认如此。

\*
: 输出当前作用域内所有具名绑定。

expression
: 使用作用域内变量的任意 Cypher 表达式，包括顶点或边变量、属性引用、路径变量、函数调用、聚合、算术表达式、`CASE` 表达式、列表或映射构造器，以及常量。

alias
: 结果列名。不加双引号会折叠为小写，加双引号则保留大小写。未指定别名时，属性引用取属性名，其他表达式的列名为 `?column?`。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 返回整个顶点 {#return-a-whole-vertex}

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p;
```

```
                         p
---------------------------------------------------
 person[4.1]{"born": 1964, "name": "Keanu Reeves"}
(1 row)
```

顶点显示为 `label[id]{properties}`，边还会显示两个端点。

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'})
RETURN r;
```

```
                   r
---------------------------------------
 acted_in[5.1][4.1,3.1]{"role": "Neo"}
(1 row)
```

### 返回属性并指定或省略别名 {#return-properties-with-and-without-an-alias}

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born;
```

```
 born
------
 1964
(1 row)
```

不带别名的属性引用使用属性名，计算表达式没有可沿用的名称。

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born + 1;
```

```
 ?column?
----------
 1965
(1 row)
```

不带引号的别名会被折叠为小写，加引号则保留原样。

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born AS BornIn;
```

```
 bornin
--------
 1964
(1 row)
```

```cypher
MATCH (p:person {name: 'Keanu Reeves'})
RETURN p.born AS "BornIn";
```

```
 BornIn
--------
 1964
(1 row)
```

### 返回所有具名元素 {#return-everything-that-has-a-name}

```cypher
MATCH (p:person {name: 'Ryan Gosling'})-[r:acted_in]->(m:movie)
RETURN *;
```

```
                         p                          |                   r                   |                                                                                                                                     m
----------------------------------------------------+---------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 person[4.10]{"born": 1980, "name": "Ryan Gosling"} | acted_in[5.13][4.10,3.9]{"role": "K"} | movie[3.9]{"plot": "A new blade runner unearths a long-buried secret that has the potential to plunge what's left of society into chaos.", "year": 2017, "genre": "Sci-Fi", "title": "Blade Runner 2049", "embedding": [0.21560573, -0.07505179, -0.01331814, 0.13403069]}
(1 row)
```

结果有三列，每个具名元素一列。如果模式写作 `(p:person {name: 'Ryan Gosling'})-[:acted_in]->(m:movie)`，`RETURN *` 只返回两列。

### 消除重复行 {#remove-duplicate-rows}

25 条 `acted_in` 边指向三种类型的影片。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
RETURN DISTINCT m.genre AS genre
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

去掉 `DISTINCT`，同一查询会返回 25 行。`ALL` 是这种默认行为的显式写法。

### 聚合 {#aggregate}

若仅输出聚合表达式，整个输入会汇总成一行。

```cypher
MATCH (m:movie)
RETURN count(*) AS films, min(m.year) AS earliest, max(m.year) AS latest;
```

```
 films | earliest | latest
-------+----------+--------
 18    | 1982     | 2021
(1 row)
```

若同时列出其他非聚合表达式，就会按该表达式分组。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
RETURN m.genre AS genre, count(*) AS roles
ORDER BY genre;
```

```
    genre    | roles
-------------+-------
 "Action"    | 13
 "Adventure" | 1
 "Sci-Fi"    | 11
(3 rows)
```

`collect()` 将一组值收集为列表。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie {title: 'The Matrix'})
RETURN collect(p.name) AS cast;
```

```
                            cast
------------------------------------------------------------
 ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"]
(1 row)
```

### 返回常量 {#return-a-constant}

`RETURN` 前面不一定要有模式。

```cypher
RETURN 1 + 2 AS sum, 'Hello' AS greeting;
```

```
 sum | greeting
-----+----------
 3   | "Hello"
(1 row)
```

## 注意事项 {#notes}

属性列以 jsonb 返回。若应用程序需要原生类型，可以把 Cypher 放入 SQL 的 `SELECT` 子查询，在外层提取原生值。jsonb 运算符 `->>` 将键对应的值读为文本，`#>> '{}'` 将 jsonb 标量列提取为文本。直接使用 `RETURN` 获取原生类型并不方便。

```psql
SELECT d.props ->> 'title' AS film, r.score
FROM (MATCH (p:person)-[:directed]->(m:movie)
      WHERE p.name = 'Christopher Nolan'
      RETURN properties(m) AS props) d
JOIN rating r ON r.title = d.props ->> 'title'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
(2 rows)
```

这里的片名是不带引号的文本，`score` 保留原表的数值类型。完整用法见 [SQL 与 Cypher 混合查询](/zh/agensgraph/querying/combining-sql-and-cypher/)。

## 兼容性 {#compatibility}

### 列类型 {#column-types}

ISO/IEC 39075 §14.11 的 `<return statement>` 规定结果列采用表达式的声明类型。AgensGraph 的 Cypher 输出列使用 jsonb，即使表达式中显式转换类型也是如此。可按上例在 SQL 中提取所需类型。

### DISTINCT 与 ORDER BY {#distinct-and-order-by}

`RETURN DISTINCT` 后的 `ORDER BY` 只能按投影列表中出现的表达式排序。

```cypher
MATCH (m:movie) RETURN DISTINCT m.genre AS genre ORDER BY m.year;
```

```
ERROR:  for SELECT DISTINCT, ORDER BY expressions must appear in select list
```

这与 SQL 的 `SELECT DISTINCT` 相同。可以把排序键加入投影，或去掉 `DISTINCT`，改用分组聚合去重。

## 另请参阅 {#see-also}

- [`WITH`](/zh/agensgraph/reference/clauses/with/)：在流水线中间进行投影
- [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/)、[`SKIP` 与 `LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)：可跟在 `RETURN` 后的子句
- [`FINISH`](/zh/agensgraph/reference/clauses/finish/)：结束查询且不返回行
- [`UNION`](/zh/agensgraph/reference/clauses/union/)：合并多条查询的结果
- [SQL 与 Cypher 混合查询](/zh/agensgraph/querying/combining-sql-and-cypher/)：提取原生类型
