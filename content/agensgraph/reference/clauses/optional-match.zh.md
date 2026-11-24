---
title: "OPTIONAL MATCH"
linkTitle: "OPTIONAL MATCH"
description: "像 MATCH 一样匹配模式。若未匹配，仍保留输入行，并将模式引入的变量绑定为空值。"
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/optional-match.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

像 `MATCH` 一样匹配模式。若某条输入行找不到匹配，仍保留该行，并将模式引入的变量绑定为空值。

## 语法 {#synopsis}

```text
OPTIONAL MATCH pattern [, pattern ] ... [ WHERE condition ]
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`OPTIONAL MATCH` 接受与 [`MATCH`](/zh/agensgraph/reference/clauses/match/) 相同的模式，也按相同规则匹配。未匹配时，普通 `MATCH` 丢弃该行，而 `OPTIONAL MATCH` 保留该行，并将模式新引入的变量全部绑定为空值。它相当于图查询中的 `LEFT JOIN`。

- 作用域中已有的变量保留原值，只有可选模式新引入的变量可能变为空值。
- 紧跟 `OPTIONAL MATCH` 的 `WHERE` **属于可选匹配本身**。若模式匹配但条件不成立，系统仍会保留输入行，并将新变量置空。若要丢弃这样的行，请在子句之后用 [`WITH`](/zh/agensgraph/reference/clauses/with/) 或 [`FILTER`](/zh/agensgraph/reference/clauses/filter/) 过滤。
- 若查询以 `OPTIONAL MATCH` 开头且模式未匹配，结果中会有一行，所有列均为空值。
- 同一子句中用逗号分隔的多个模式作为整体参与可选匹配。它们必须全部匹配，否则整个子句的新增变量均为空值。

## 参数 {#parameters}

pattern
: 路径模式，语法同 `MATCH`。顶点、边、路径及 `ONLY` 的写法见 [`MATCH`](/zh/agensgraph/reference/clauses/match/)。

condition
: 在匹配过程中求值的布尔表达式。条件不成立时保留输入行，模式引入的变量为空值。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 列出人物，包括从未执导影片的人 {#list-people-whether-or-not-they-directed-anything}

```cypher
MATCH (p:person) WHERE p.born > 1974
OPTIONAL MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY person;
```

```
      person       | directed
-------------------+-----------
 "Neill Blomkamp"  | "Elysium"
 "Ryan Gosling"    |
 "Sam Worthington" |
(3 rows)
```

三人中有两人未执导影片，因此这两行的 `m` 和 `m.title` 都为空。若第二行改用普通 `MATCH`，则只返回一行。

```cypher
MATCH (p:person) WHERE p.born > 1974
MATCH (p)-[:directed]->(m:movie)
RETURN p.name AS person, m.title AS directed
ORDER BY person;
```

```
      person      | directed
------------------+-----------
 "Neill Blomkamp" | "Elysium"
(1 row)
```

### 只保留未匹配的行 {#keep-only-the-rows-that-failed-to-match}

在子句之后检测可选变量是否为空。下面找出没有出向 `related_to` 边的科幻影片。

```cypher
MATCH (m:movie) WHERE m.genre = 'Sci-Fi'
OPTIONAL MATCH (m)-[:related_to]->(n:movie)
WITH m, n WHERE n IS NULL
RETURN m.title AS film
ORDER BY film;
```

```
        film
---------------------
 "Avatar"
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
 "Inception"
 "The Fifth Element"
(6 rows)
```

### WHERE 的位置如何影响结果 {#see-where-the-where-goes}

`Jurassic Park` 有一位演员 Sam Neill，生于 1947 年。若把条件写在可选匹配内部，这部影片会保留，演员为空。

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure'
OPTIONAL MATCH (p:person)-[:acted_in]->(m) WHERE p.born > 1950
RETURN m.title AS film, p.name AS actor
ORDER BY film, actor;
```

```
      film       | actor
-----------------+-------
 "Jurassic Park" |
(1 row)
```

若在该子句之后应用同一条件，该影片就会被过滤掉。

```cypher
MATCH (m:movie) WHERE m.genre = 'Adventure'
OPTIONAL MATCH (p:person)-[:acted_in]->(m)
WITH m, p WHERE p.born > 1950
RETURN m.title AS film, p.name AS actor
ORDER BY film, actor;
```

```
 film | actor
------+-------
(0 rows)
```

### 以可选匹配开始查询 {#lead-a-query-with-an-optional-match}

```cypher
OPTIONAL MATCH (m:movie {title: 'Nope'})
RETURN m;
```

```
 m
---

(1 row)
```

结果只有一行，其中 `m` 为空。这里若使用普通 `MATCH`，则一行也不返回。

## 注意事项 {#notes}

读取空顶点的属性会返回空值，因此在未匹配的行中读取 `m.title` 也是安全的。要可靠地找出未匹配的行，应检测变量本身，如 `WHERE n IS NULL`。已匹配的顶点也可能恰好缺少被检测的属性。

## 兼容性 {#compatibility}

### 可选语句块（ISO/IEC 39075 §14.4） {#optional-blocks-isoiec-39075-144}

标准的 `<optional match statement>` 还允许用花括号或圆括号包围多个匹配语句，如 `OPTIONAL { MATCH ... MATCH ... }`。AgensGraph 只接受直接位于 `MATCH` 前面的 `OPTIONAL`，块形式会报语法错误。`OPTIONAL` 还可以放在 [`CALL`](/zh/agensgraph/reference/clauses/call-subquery/) 前。

## 另请参阅 {#see-also}

- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：模式语法与普通匹配
- [`WHERE`](/zh/agensgraph/reference/clauses/where/)：条件及其生效位置
- [`WITH`](/zh/agensgraph/reference/clauses/with/)：在可选匹配后过滤
- [`CALL { subquery }`](/zh/agensgraph/reference/clauses/call-subquery/)：也可带 `OPTIONAL` 前缀
