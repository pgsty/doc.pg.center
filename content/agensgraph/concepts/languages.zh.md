---
title: Cypher、GQL 与 SQL
linkTitle: Cypher、GQL 与 SQL
description: AgensGraph 用三种语言回答问题。
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/concepts/languages.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 用三种语言回答问题。它们不是三个产品、三种模式或三种连接。这里只有一个解析器、一个规划器、一组表和一个线协议；你可以按语句选择，也可以在一条语句中混合两种语言。

**Cypher** 是图语言，也是覆盖面最完整的接口。图能做的所有事情都可以通过 Cypher 完成。

**GQL** 是 ISO/IEC 39075 标准图查询语言。在 AgensGraph 中，它不是单独的方言。凡是接受 Cypher 语句的地方也接受 GQL 语句：`LET`、`NEXT`、`FILTER`、`FINISH`、`INSERT`、`FOR`、`CALL { }`，以及子查询值表达式 `EXISTS { }` 和 `VALUE { }`。没有需要切换的开关，也没有单独的解析器。[GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)记录标准中哪些部分已经实现。

**SQL** 就是 PostgreSQL 的 SQL，未作改动。你熟悉的 PostgreSQL 表、视图、函数、扩展、角色和事务都在这里；SQL 看到的图就是普通表。

## 选择 {#choosing}

按问题的形状选择，而不是按偏好：

* **沿着关系查找**——一个人如何连接到一部电影、两部电影相距多远、三跳内能到达什么——正是图模式的用途。SQL 中的连接链要长几倍才能表达同样含义，而且完全无法表达“任意跳数”。
* **聚合、窗口、集合操作、与普通表连接，以及任何管理工作**属于 SQL；Cypher 不试图取代它们。
* **GQL** 用于你想要标准拼写，或者要面向多个图数据库编写并希望使用可移植形式的场合。`INSERT` 和 `CREATE` 做同样的工作；`FILTER` 和 `WHERE` 做同样的工作。

你不必只选一次。[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)完整介绍了交叉点；对已经了解 SQL 的读者来说，这是本手册中最有用的一页。

## 如果你了解 SQL {#if-you-know-sql}

这些语言的词汇比语法看起来更接近，因为[图是模式、标签是表](/zh/agensgraph/concepts/graph-on-postgresql/)：

| SQL | Cypher | 说明 |
| --- | --- | --- |
| `CREATE SCHEMA s` | `CREATE GRAPH s` | 图*就是*模式。 |
| `CREATE TABLE t` | `CREATE VLABEL t` | 顶点标签；边用 `CREATE ELABEL`。 |
| `INSERT INTO t VALUES (…)` | `CREATE (:t {…})` | `INSERT (:t {…})` 是 GQL 拼写。 |
| `SELECT … FROM t WHERE …` | `MATCH (n:t) WHERE … RETURN …` | `RETURN` 是投影，放在最后。 |
| `SELECT … FROM a JOIN b ON …` | `MATCH (a)-[:e]->(b)` | 模式是沿边连接。 |
| `LEFT JOIN` | `OPTIONAL MATCH` | 未匹配的行会带 null 返回。 |
| `UPDATE t SET c = …` | `MATCH (n:t) SET n.c = …` | 先查找，再写入。 |
| `DELETE FROM t WHERE …` | `MATCH (n:t) WHERE … DELETE n` | `DETACH DELETE` 会同时删除边。 |
| `WITH cte AS (…)` | `WITH …` / `NEXT` | Cypher 的 `WITH` 划分流水线，不是 CTE。 |
| `ORDER BY` / `LIMIT` / `OFFSET` | `ORDER BY` / `LIMIT` / `SKIP` | `SKIP` 与 `OFFSET` 是同义词。 |
| `CREATE INDEX ON t ((c))` | `CREATE PROPERTY INDEX ON t (c)` | 会变成表达式索引。 |
| `count(*)`、`sum`、`avg` | 相同 | 聚合来自 PostgreSQL。 |
| `information_schema`、`pg_catalog` | `ag_graph`、`ag_label` | 见[系统目录](/zh/agensgraph/system-catalogs/)。 |

三个差异会让 SQL 用户早早中招，而且三者都是静默失败而不是报错：

**属性读取返回 `jsonb`，而不是文本。** `RETURN m.title` 会连同引号一起输出 `"The Matrix"`；在查询内部转换类型不会改变这一点。要得到普通标量，请在外面解包：`SELECT t #>> '{}' FROM (MATCH (m:movie) RETURN m.title AS t) q`。

**`ORDER BY 2` 不表示“第二列”。** 在 Cypher 中，`2` 是常量，所以每行比较结果都相等，没有任何排序。请按别名或表达式排序。

**`n.id` 不是 id。** `id(n)` 返回 `graphid`；`n.id` 查找名为 `id` 的属性，如果没有就什么也不返回。

## 一条语句，两种语言 {#one-statement-two-languages}

Cypher 查询可以出现在 SQL 期望表的位置：

```psql
SELECT q.title #>> '{}' AS film, r.score
FROM (MATCH (:person {name: 'Christopher Nolan'})-[:directed]->(m:movie)
      RETURN m.title AS title) q
JOIN rating r ON r.title = q.title #>> '{}'
WHERE r.source = 'critics'
ORDER BY r.score DESC;
```

```
     film     | score
--------------+-------
 Inception    |   8.8
 Interstellar |   8.7
```

SQL 也可以出现在 Cypher 期望值的位置：

```cypher
MATCH (m:movie)
WHERE m.title = (SELECT to_jsonb(title) FROM rating
                 WHERE source = 'critics' ORDER BY score DESC LIMIT 1)
RETURN m.title AS best;
```

```
    best
-------------
 "Inception"
```

这两个示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## 本版本中“GQL 支持”的含义 {#what-gql-support-means-in-this-release}

GQL 进入 AgensGraph 的方式，是在现有语法上增加语句，而不是引入第二种语言。这有两个后果，值得明说。

GQL 语句可以在一个查询中与 Cypher 混用——`MATCH … LET … RETURN` 是有效语句，`MATCH … FILTER … NEXT RETURN …` 也是。没有任何东西把查询标记为“GQL”。

一致性是按特性划分的部分支持，而不是按模式划分。[GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)按 ISO/IEC 39075:2024 的子条款逐项列出；[参考](/zh/agensgraph/reference/clauses/)中的每个子句页面也会在自己的 *Compatibility* 标题下重复该子句的相同说明。
