---
title: "SKIP 与 LIMIT"
linkTitle: "SKIP 与 LIMIT"
description: "对工作行分页。SKIP 跳过开头的行，LIMIT 限制保留的行数。"
type: docs
weight: 90
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/skip-and-limit.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


**GQL 子句**

对工作行分页。`SKIP` 跳过开头的若干行，`LIMIT` 限制保留的行数。`OFFSET` 是 `SKIP` 的同义词。

## 语法 {#synopsis}

```text
{ SKIP | OFFSET } count
```

```text
LIMIT count
```

**记法**：大写表示关键字，小写表示占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 说明 {#description}

`SKIP` 和 `LIMIT` 是独立子句，可在流水线的中间或末尾分页。可以跟在 [`RETURN`](/zh/agensgraph/reference/clauses/return/) 或 [`WITH`](/zh/agensgraph/reference/clauses/with/) 后，也可紧跟 [`MATCH`](/zh/agensgraph/reference/clauses/match/)。两者都可单独使用。

- `SKIP` 与 `OFFSET` 是同一子句的两种写法，任选其一。ISO/IEC 39075 先列出 `OFFSET`。
- *count* 可以是表达式，也可以是字面量，只求值一次。
- 负数会报错。超过总行数不会报错。`SKIP` 跳过末尾时不返回任何行，`LIMIT` 超出总行数时保留全部行。
- 小数会舍入为最接近的整数。
- 这两个子句都不能**开始**查询，也不能单独结束查询。查询仍须以 `RETURN`、`FINISH` 或写入子句结束。
- 如果没有 [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/)，不能保证某一页会包含哪些行。若需可重现的分页结果，应先排序。
- 写在投影之后时，各修饰子句必须依次为 `ORDER BY`、`SKIP`/`OFFSET`、`LIMIT`。详见[注意事项](#notes)。

## 参数 {#parameters}

count
: 非负整数表达式。`SKIP` 跳过开头指定数量的行，`LIMIT` 至多保留指定数量的行。

## 示例 {#examples}

以下示例均使用[示例数据集](/zh/agensgraph/get-started/example-dataset/)。

### 取前几行 {#take-the-first-few-rows}

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
LIMIT 2;
```

```
      film
----------------
 "Avatar"
 "Blade Runner"
(2 rows)
```

### 取中间一页 {#take-a-page-from-the-middle}

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
SKIP 2
LIMIT 3;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
(3 rows)
```

使用 `OFFSET` 效果相同。

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
OFFSET 2
LIMIT 3;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
(3 rows)
```

### 计算行数 {#compute-the-count}

可以使用表达式。

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
SKIP 1+1
LIMIT 2;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
(2 rows)
```

小数会舍入。`LIMIT 1.5` 保留两行。

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
LIMIT 1.5;
```

```
      film
----------------
 "Avatar"
 "Blade Runner"
(2 rows)
```

### 翻到末页之后 {#page-past-the-end}

```cypher
MATCH (m:movie)
RETURN m.title AS film
ORDER BY film
SKIP 20;
```

```
 film
------
(0 rows)
```

总共只有 18 部影片，因此没有剩余行。在同一查询中指定 `LIMIT 100` 会返回全部 18 行。

### 在查询中途缩减行数 {#cut-the-pipeline-down-mid-query}

在 `MATCH` 后加 `LIMIT`，可减少后续子句需要连接的行数。

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

### 拒绝负数 {#reject-a-negative-count}

```cypher
MATCH (m:movie) RETURN m.title AS film ORDER BY film LIMIT -1;
```

```
ERROR:  LIMIT must not be negative
```

```cypher
MATCH (m:movie) RETURN m.title AS film ORDER BY film SKIP -1;
```

```
ERROR:  OFFSET must not be negative
```

`SKIP` 会在错误中显示为 `OFFSET`，因为两者是同一子句。

### 位置限制 {#where-they-cannot-go}

这两个子句都不能放在查询开头。

```cypher
LIMIT 3;
```

```
ERROR:  syntax error at or near "LIMIT"
LINE 1: LIMIT 3;
        ^
```

也不能单独结束查询。

```cypher
MATCH (m:movie) LIMIT 3;
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

## 注意事项 {#notes}

投影之后应先写 `ORDER BY`，再写 `SKIP`/`OFFSET`，最后写 `LIMIT`。只有这种顺序才能并入投影。若把 `LIMIT` 放在 `SKIP` 前面，末尾的 `SKIP` 会成为独立子句，查询便失去了投影结尾。这就是以下错误的含义。

```cypher
MATCH (m:movie) RETURN m.title AS film ORDER BY film LIMIT 3 SKIP 2;
```

```
ERROR:  Cypher query must end with RETURN, FINISH or update clause
```

在流水线中途，两种顺序都可解析，但含义不同。每个子句都处理前一句的结果。先跳过两行，可以取得第三至第六行。

```cypher
MATCH (m:movie) ORDER BY m.title SKIP 2 LIMIT 4 RETURN m.title AS film;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
 "Gattaca"
 "Inception"
(4 rows)
```

先限制为四行，再跳过两行，最终只剩两行。

```cypher
MATCH (m:movie) ORDER BY m.title LIMIT 4 SKIP 2 RETURN m.title AS film;
```

```
        film
---------------------
 "Blade Runner 2049"
 "Elysium"
(2 rows)
```

## 兼容性 {#compatibility}

### SKIP 与 OFFSET（ISO/IEC 39075 §16.19） {#skip-and-offset-isoiec-39075-1619}

标准的 `<offset synonym>` 定义为 `OFFSET | SKIP`，两种写法均符合标准。openCypher 只有 `SKIP`。

## 另请参阅 {#see-also}

- [`ORDER BY`](/zh/agensgraph/reference/clauses/order-by/)：先排序以取得可重现的分页结果
- [`RETURN`](/zh/agensgraph/reference/clauses/return/)、[`WITH`](/zh/agensgraph/reference/clauses/with/)：分页子句作用的投影
- [`MATCH`](/zh/agensgraph/reference/clauses/match/)：在流水线中途分页以减少后续工作量
