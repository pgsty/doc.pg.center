---
title: "UNION"
linkTitle: "UNION"
description: "将两条或多条查询的结果合为一个结果集。"
type: docs
weight: 210
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/union.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

将两条或多条查询的结果合为一个结果集。`INTERSECT` 和 `EXCEPT` 使用相同的结构，分别求交集和差集。

## 语法 {#synopsis}

```text
query { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] query [ ... ]
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

集合运算符连接两条分别以 `RETURN` 结尾的完整查询，生成一个结果集。

| 运算符 | 结果 |
| --- | --- |
| `UNION` | 至少出现在一条查询中的行。 |
| `INTERSECT` | 同时出现在两条查询中的行。 |
| `EXCEPT` | 出现在第一条查询而未出现在第二条查询中的行。 |

三种运算共同遵循以下规则。

- 各查询必须返回**相同数量的列**，对应位置的列必须可以比较。列名无须一致，结果采用第一条查询的列名。
- 默认 `DISTINCT`，即删除重复行。`ALL` 保留重复行。`UNION` 与 `UNION DISTINCT` 含义相同。
- 多个运算可以**串联**，按从左到右的顺序求值。
- 结果行的顺序没有保证。在集合运算后直接写 `ORDER BY` **不能**对合并结果排序。可行的写法见[注意事项](#notes)。
- 每个分支都必须是以 `RETURN` 结尾的完整查询，不能以写入子句或单独的 `MATCH` 结尾。

## 参数 {#parameters}

query
: 以 `RETURN` 结尾的完整查询。它返回的列数必须与链中其他查询相同。

ALL
: 保留重复行。

DISTINCT
: 删除重复行，默认如此。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 合并两个结果集 {#combine-two-result-sets}

查找与 `Inception` 有关的所有人，无论他们与影片的关系是什么。

```cypher
MATCH (p:person)-[:directed]->(:movie {title: 'Inception'}) RETURN p.name AS name
UNION
MATCH (p:person)-[:acted_in]->(:movie {title: 'Inception'}) RETURN p.name AS name;
```

```
        name
---------------------
 "Christopher Nolan"
 "Leonardo DiCaprio"
(2 rows)
```

### 保留或删除重复行 {#keep-or-drop-the-duplicates}

这里两个分支各返回 18 个类型值，每部影片一个。`UNION` 将它们去重后只剩三个。

```cypher
MATCH (m:movie) RETURN m.genre AS genre
UNION
MATCH (m:movie) RETURN m.genre AS genre;
```

```
    genre
-------------
 "Action"
 "Sci-Fi"
 "Adventure"
(3 rows)
```

`UNION DISTINCT` 是同一语句的完整写法。`UNION ALL` 保留两个分支输出的所有行。

```cypher
MATCH (m:movie {genre: 'Adventure'}) RETURN m.title AS film
UNION ALL
MATCH (m:movie) WHERE m.year = 2021 RETURN m.title AS film;
```

```
            film
----------------------------
 "Jurassic Park"
 "The Matrix Resurrections"
(2 rows)
```

这个例子中的两行本来就不同，因此 `ALL` 只影响开销，省去了去重操作。

### 取得两个查询共同返回的行 {#take-the-rows-in-both-queries}

```cypher
MATCH (m:movie {genre: 'Action'}) RETURN m.title AS film
INTERSECT
MATCH (m:movie) WHERE m.year < 1995 RETURN m.title AS film;
```

```
             film
------------------------------
 "The Terminator"
 "Terminator 2: Judgment Day"
(2 rows)
```

### 从一条查询的结果中减去另一条的结果 {#subtract-one-query-from-another}

查找执导过影片却从未参演的人。

```cypher
MATCH (p:person)-[:directed]->(m:movie) RETURN p.name AS name
EXCEPT
MATCH (p:person)-[:acted_in]->(m:movie) RETURN p.name AS name;
```

```
        name
---------------------
 "Andrew Niccol"
 "Neill Blomkamp"
 "Lana Wachowski"
 "Lilly Wachowski"
 "Joss Whedon"
 "James Cameron"
 "Luc Besson"
 "Denis Villeneuve"
 "Christopher Nolan"
 "Paul Verhoeven"
 "Ridley Scott"
 "Steven Spielberg"
(12 rows)
```

结果行没有固定顺序。

### 对合并结果排序和分页 {#sort-and-page-the-combined-result}

将集合运算放入 [`NEXT`](/zh/agensgraph/reference/clauses/next/) 链，再在接收合并结果的下一条查询中排序。

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
UNION
MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film
NEXT ORDER BY film LIMIT 3 RETURN film;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
(3 rows)
```

用 [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/) 包裹也可以得到同样的结果。

```cypher
CALL { MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
       UNION
       MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film }
RETURN film ORDER BY film LIMIT 3;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
(3 rows)
```

### 拒绝列数不匹配的查询 {#reject-a-mismatched-column-count}

```cypher
MATCH (m:movie) RETURN m.title AS t
UNION
MATCH (p:person) RETURN p.name AS n, p.born AS b;
```

```
ERROR:  each UNION query must have the same number of columns
```

这三种运算符在此报错时都显示为 `UNION`。

## 注意事项 {#notes}

集合运算之后的 `ORDER BY`、`SKIP` 或 `LIMIT` 只属于**链中的最后一条查询**。因此它们只会在合并之前对最后一个分支排序或分页。下例中的 `LIMIT 1` 最终返回多于一行。

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
UNION
MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film
LIMIT 1;
```

```
      film
-----------------
 "Inception"
 "Jurassic Park"
(2 rows)
```

科幻分支原有 10 部影片，`LIMIT` 将其减为一行，随后才并入冒险分支中唯一的影片。别名也按相同规则解析，排序键必须能引用最后一个分支的列。

```cypher
MATCH (m:movie) RETURN m.title AS first_col
UNION
MATCH (p:person) RETURN p.name AS second_col
ORDER BY first_col LIMIT 2;
```

```
ERROR:  variable does not exist
LINE 4: ORDER BY first_col LIMIT 2;
                 ^
```

要对合并结果排序或分页，可使用上述 `NEXT` 或 `CALL` 写法。在 SQL 中也可以对整个集合运算执行一层 `SELECT`。

```psql
SELECT * FROM (
  MATCH (m:movie) WHERE m.genre = 'Adventure' RETURN m.title AS film
  UNION
  MATCH (m:movie) WHERE m.genre = 'Sci-Fi' RETURN m.title AS film
) q ORDER BY film LIMIT 3;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner"
 "Blade Runner 2049"
(3 rows)
```

## 兼容性 {#compatibility}

### 集合运算符（ISO/IEC 39075 §14.2） {#set-operators-isoiec-39075-142}

标准将 `<set operator>` 定义为 `UNION [ <set quantifier> ] | EXCEPT [ <set quantifier> ] | INTERSECT [ <set quantifier> ]`，省略量词时默认为 `DISTINCT`。AgensGraph 按此规则实现了三种运算符及两种量词。openCypher 只有 `UNION` 和 `UNION ALL`，AgensGraph 还提供 `INTERSECT` 和 `EXCEPT`。

尚未实现标准的 `OTHERWISE` 连接形式，它仅在第一条查询未返回任何行时采用第二条查询的结果。

### 对合并结果排序（ISO/IEC 39075 §14.9） {#sorting-a-combined-result-isoiec-39075-149}

标准将 `<order by and page statement>` 应用于当前工作表，复合查询之后的工作表就是合并结果。AgensGraph 会把它附在最后一个分支上，见[注意事项](#notes)。请用 `NEXT`、`CALL { }` 或 SQL `SELECT` 包裹集合运算，再对结果排序或分页。

## 另请参阅 {#see-also}

- [`RETURN`](/zh/agensgraph/reference/clauses/return/)：集合运算的每个分支均以此结束
- [`NEXT`](/zh/agensgraph/reference/clauses/next/) **GQL**：将合并结果传给下一条查询
- [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/)：包裹集合运算的另一种方法
- [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/)、[`SKIP` 与 `LIMIT`](/zh/agensgraph/reference/clauses/skip-and-limit/)：这些子句在集合运算中的作用范围
- [SQL 与 Cypher 混合查询](/zh/agensgraph/querying/combining-sql-and-cypher/)：用 SQL 对集合运算结果排序
