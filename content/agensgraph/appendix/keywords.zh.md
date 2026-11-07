---
title: 关键字
linkTitle: 关键字
description: AgensGraph 继承 PostgreSQL 的关键字表，并新增图语句所需的词。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/keywords.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 继承 PostgreSQL 的关键字表，并新增图语句所需的词。关键字的类别决定这个词还能在哪里用作名称。**非保留**词可以为任何对象命名。**保留**词不能，必须先加双引号。

PostgreSQL 的 [Key Words](https://www.postgresql.org/docs/18/sql-keywords-appendix.html) 附录列出继承的 SQL 词及其类别。本页只覆盖 AgensGraph 新增和改变的部分。PostgreSQL 使用的另外两个类别——*类型/函数名*和*列名*——没有 AgensGraph 条目。下面的每个词要么非保留，要么完全保留。

标识符按 SQL 方式加双引号。反引号是语法错误，所以 `` `let` `` 不能作为转义写法——应写 `"let"`。

## AgensGraph 新增的词 {#words-agensgraph-adds}

以下二十四个词在 AgensGraph 的关键字表中，且不在 PostgreSQL 18 的表中。注释说明该词所属的子句或语句。

| 词 | 类别 | 注释 |
| --- | --- | --- |
| `allshortestpaths` | 非保留 | 路径函数：两个顶点之间的所有最短路径。 |
| `assert` | 非保留 | `CREATE CONSTRAINT … ASSERT`。 |
| `collect` | 非保留 | `COLLECT { }` 子查询表达式。 |
| `contains` | 非保留 | `CONTAINS` 字符串谓词。 |
| `count` | 非保留 | `COUNT { }` 子查询表达式。 |
| `current_graph` | **保留** | 以裸关键字表示的工作图。 |
| `current_property_graph` | **保留** | `CURRENT_GRAPH` 的同义词。 |
| `dijkstra` | 非保留 | 路径函数：加权最短路径。 |
| `elabel` | 非保留 | `CREATE ELABEL`、`ALTER ELABEL`、`DROP ELABEL`。 |
| `ends` | 非保留 | `ENDS WITH` 字符串谓词。 |
| `finish` | **保留** | `FINISH` 子句，用于结束不投影任何结果的查询。 |
| `graph` | 非保留 | `CREATE GRAPH`、`DROP GRAPH` 以及 `graph_path` 设置的语句。 |
| `let` | **保留** | `LET` 子句。 |
| `optional` | 非保留 | `OPTIONAL MATCH` 和 `OPTIONAL CALL`。 |
| `property` | 非保留 | `CREATE PROPERTY INDEX`、`CURRENT_PROPERTY_GRAPH`。 |
| `remove` | 非保留 | `REMOVE` 子句。 |
| `shortestpath` | 非保留 | 路径函数：一条最短路径。 |
| `single` | 非保留 | `single()` 列表谓词。 |
| `size` | 非保留 | `size()` 函数。 |
| `starts` | 非保留 | `STARTS WITH` 字符串谓词。 |
| `unwind` | **保留** | `UNWIND` 子句。 |
| `vlabel` | 非保留 | `CREATE VLABEL`、`ALTER VLABEL`、`DROP VLABEL`。 |
| `xor` | **保留** | `XOR` 布尔运算符。 |
| `yield` | 非保留 | `CALL … YIELD`。 |

AgensGraph 继承的四个词在这里保留而在 PostgreSQL 中非保留，因为它们各自引导一个 Cypher 子句：`insert`、`match`、`merge` 和 `return`。

`CALL` 被有意保留为非保留词，因此 `call` 仍可以为列、表、别名、标签、属性键或变量命名。只有两种拼法会改变含义，因为当 `CALL` 后面是 `(` 或 `{` 时，词法分析器会特殊处理它：

- `call(...)`——一个字面名为 `call` 的函数，带参数调用。需要加引号：`"call"(1)`。
- `(call { ... })`——变量名为 `call` 且带属性映射但没有标签的点模式。需要加引号：`("call" { ... })`。

## 在 2.18 中变为保留的词 {#words-that-became-reserved-in-218}

六个词在 2.18 中保留，在 2.17 中不是：`insert`、`finish`、`let`、`xor`、`current_graph` 和 `current_property_graph`。保留一个词可能破坏曾把它用作名称的应用，因此每个词的保留范围都收窄到语法允许的程度。结果并不统一：有些位置仍可用，下表是实测结果，不是泛化规则。

每个单元格都是在 2.18 服务端上运行对应位置得到的结果。**可用**表示未加引号的词被接受。

| 词 | 模式中的标签 | `CREATE VLABEL` | 变量 | `RETURN … AS` 别名 | 作为排序键的别名 | 属性键 |
| --- | --- | --- | --- | --- | --- | --- |
| `insert` | 可用 | 失败 | 可用 | 可用 | 可用 | 可用 |
| `finish` | 可用 | 失败 | 失败 | 可用 | 失败 | 可用 |
| `let` | 失败 | 失败 | 失败 | 可用 | 失败 | 可用 |
| `xor` | 失败 | 失败 | 失败 | 可用 | 失败 | 可用 |
| `current_graph` | 失败 | 失败 | 失败 | 可用 | 可用 | 可用 |
| `current_property_graph` | 失败 | 失败 | 失败 | 可用 | 可用 | 可用 |

表中两列看起来反常，需要用文字明确说明。

对 `insert` 和 `finish` 来说，标签在模式中可用，但在标签 DDL 中不可用。`CREATE (:insert)` 和 `MATCH (n:insert)` 会接受；`CREATE VLABEL insert` 不会：

```cypher
CREATE VLABEL insert;
```

```
ERROR:  syntax error at or near "insert"
```

用带引号的名称创建标签：`CREATE VLABEL "insert"`。之后未加引号的模式拼法仍能找到它，因为未加引号的标识符会折叠为小写。

别名总是可用，但按该别名排序不一定可用。`RETURN n.k AS let` 会接受，而其后的 `ORDER BY let` 不会：

```cypher
MATCH (n:t) RETURN n.k AS let ORDER BY let;
```

```
ERROR:  syntax error at or near "let"
```

`current_graph` 和 `current_property_graph` 是例外。这两个名称的别名都可以排序。

在定义处和每个使用处都加双引号，可以修复表中每个失败单元格：

```cypher
MATCH (n:t) RETURN n.k AS "let" ORDER BY "let";
```

属性键从不需要引号。键是 `jsonb` 文档中的字符串，不是标识符，所以 `CREATE (:t {let: 1})` 和 `RETURN n.let` 不受以上任何影响。

在 SQL 一侧，同样六个词作为列名时需要引号。`CREATE TABLE t (xor int)` 是语法错误；`CREATE TABLE t ("xor" int)` 可用。

## 保留集比图语言词更宽 {#the-reserved-set-is-wider-than-the-graph-words}

为图子句保留一个词只是问题的一部分。AgensGraph 也继承 PostgreSQL 的保留字。Cypher 标签或变量是同一语法中的标识符，所以其中任何保留字未加引号都会被拒绝。`both` 是一个好例子：它是 PostgreSQL 保留字，但与图毫无关系：

```cypher
CREATE VLABEL both;
```

```
ERROR:  syntax error at or near "both"
```

`all`、`and`、`any`、`array`、`as`、`case`、`cast`、`end`、`from`、`in`、`not`、`null`、`or`、`select`、`table`、`to`、`union`、`when`、`where` 以及 PostgreSQL 保留表中的其余词也是如此。选择标签、变量或属性索引名之前，请对照 PostgreSQL 的 [Key Words](https://www.postgresql.org/docs/18/sql-keywords-appendix.html) 附录，其中给出 AgensGraph 携带的每个 SQL 词的类别。

> [!NOTE]
> 关键字表在 AgensGraph 源码中是单个文件，每个词一行并带类别。当某个名称被拒绝而本页没有说明原因时，请查阅该文件。

## 另见 {#see-also}

- [语法](/zh/agensgraph/reference/syntax/)——词法规则，包括标识符折叠
- [Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)——移植查询会遇到的其他差异
- [升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/)——完整的升级前检查清单
- [AgensGraph 2.18.6.1 发布说明](/zh/agensgraph/release-notes/2.18/)——这些词所属的子句
