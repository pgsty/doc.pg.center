---
title: GQL 一致性
linkTitle: GQL 一致性
description: AgensGraph 实现了 ISO/IEC 39075:2024, Information technology — Database languages — GQL 的一部分。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/gql-conformance.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 实现了 ISO/IEC 39075:2024 *Information technology — Database languages — GQL* 的一部分。本附录不是完整一致性声明；它以合理且有用的详细程度覆盖主要主题。

下表以标准的子条款为键，因为标准本身就用这个单位把一致性规则附加到一段语法上。每一行都对照运行中的 2.18 服务端检查过。只有当子条款定义的语法被接受并产生子条款要求的结果时，行中才写**是**。子条款的部分语法被接受而其余抛错时写**部分**；完全不能解析时写**否**。标准为同一概念提供多种拼法时，注释说明 AgensGraph 采用哪一种。

三个总体要点适用于每一行，因此不在每条注释中重复。

GQL 不是独立模式。GQL 语句与 Cypher 语句经过同一解析器，并可在同一条流水线中混合，所以 `LET` 可以挨着 `WITH`，`INSERT` 可以挨着 `CREATE`。见[Cypher、GQL 和 SQL](/zh/agensgraph/concepts/languages/)。

图是 PostgreSQL 模式，标签是表。因此，标准中描述目录、模式和图类型目录的部分对应 PostgreSQL 而不是 GQL。工作图来自 `graph_path` 设置而不是 `USE` 子句，权限也是 PostgreSQL 权限。见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

错误携带五个字符的 SQLSTATE，而不是 GQLSTATUS。见[错误码](/zh/agensgraph/appendix/error-codes/)。

## 支持的特性 {#supported-features}

这些子条款全部或部分实现。**部分**注释指出缺失内容，让移植标准 GQL 的读者知道要查找什么。

| 子条款 | 名称 | 支持 | 注释 |
| --- | --- | --- | --- |
| 8.1–8.4 | `<start transaction command>`、`<transaction characteristics>`、`<rollback command>`、`<commit command>` | 是 | 由 PostgreSQL 自身事务语句回答。`START TRANSACTION READ ONLY`、`COMMIT` 和 `ROLLBACK` 都可用。 |
| 9.2 | `<procedure body>` | 部分 | `NEXT` 把一条语句链接到上一条语句的结果。`NEXT` 不能携带 `YIELD` 子句；9.2 还允许的绑定变量定义块不存在——见下方 10.1–10.3。 |
| 11.1 | `<graph expression>` | 部分 | `CURRENT_GRAPH` 和 `CURRENT_PROPERTY_GRAPH` 在 Cypher 和 SQL 中都被接受。它们是裸关键字：`current_graph()` 是语法错误。不存在其他图表达式形式。 |
| 12.4 | `<create graph statement>` | 部分 | `CREATE GRAPH name` 和 `CREATE GRAPH IF NOT EXISTS name` 可用。名称后标准要求的图类型（`ANY`、`LIKE` 或图类型引用）不被接受，`OR REPLACE`、`PROPERTY GRAPH` 和 `AS COPY OF` 也不被接受。 |
| 12.5 | `<drop graph statement>` | 部分 | `DROP GRAPH name` 和 `DROP GRAPH IF EXISTS name` 可用，另有非标准的 `CASCADE`；它是必需的，因为新图已经包含 `ag_vertex` 和 `ag_edge`。`DROP PROPERTY GRAPH` 是语法错误。 |
| 13.1 | `<linear data-modifying statement>` | 是 | 一条语句可在同一条流水线中组合读子句和写子句，写子句的更改对其后的读子句可见。 |
| 13.2 | `<insert statement>` | 是 | `INSERT` 采用与 Cypher `CREATE` 相同的模式，是它的同义词。 |
| 13.3 | `<set statement>` | 部分 | 属性赋值可用，包括非标准的 `+=` 合并形式。子条款还定义的标签集赋值不存在：顶点恰好有一个标签。 |
| 13.4 | `<remove statement>` | 部分 | `REMOVE n.prop` 删除属性。出于同一原因，`REMOVE n:Label` 不存在。 |
| 13.5 | `<delete statement>` | 是 | `DELETE` 和 `DETACH DELETE`。仍带边的顶点除非给出 `DETACH`，否则删除会被拒绝。 |
| 14.2 | `<composite query expression>` | 部分 | `UNION`、`UNION ALL`、`EXCEPT` 和 `INTERSECT` 组合两条查询语句。`OTHERWISE` 是语法错误。 |
| 14.3 | `<linear query statement>` 与 `<simple query statement>` | 是 | 查询是由下列基本查询语句组成的序列，并以一个基本结果语句结束。 |
| 14.4 | `<match statement>` | 部分 | `MATCH` 和 `OPTIONAL MATCH` 可用。花括号形式 `OPTIONAL { MATCH … MATCH … }` 是语法错误。 |
| 14.5 | `<call query statement>` | 部分 | 两种调用形式都可用。各自的要求见 15.2 和 15.3。 |
| 14.6 | `<filter statement>` | 是 | `FILTER expr` 和 `FILTER WHERE expr` 都可用。 |
| 14.7 | `<let statement>` | 是 | 可累加、按行计算，并能引导查询。`LET` 表达式中的聚合会被拒绝。 |
| 14.8 | `<for statement>` | 部分 | 迭代列表可用，`WITH OFFSET AS name` 给出从 0 开始的下标。`WITH ORDINALITY` 是语法错误，`FOR` 不能迭代绑定表。 |
| 14.9 | `<order by and page statement>` | 是 | `ORDER BY`、`SKIP`、`OFFSET` 和 `LIMIT` 是独立语句，可位于流水线任意位置。与标准一样，AgensGraph 不允许它们*结束*查询——14.3 要求最后一个语句是基本结果语句——所以以 `ORDER BY` 结尾的查询抛出 `ERROR: Cypher query must end with RETURN, FINISH or update clause`。 |
| 14.10 | `<primitive result statement>` | 是 | `RETURN`、`RETURN … ORDER BY …` 和 `FINISH`。 |
| 14.11 | `<return statement>` | 部分 | `RETURN`、`RETURN DISTINCT`、`RETURN ALL`、`RETURN *` 和显式别名。`RETURN NO BINDINGS` 是语法错误。分组是隐式的——见 16.15。 |
| 15.1 | `<call procedure statement>` 与 `<procedure call>` | 是 | `CALL` 和 `OPTIONAL CALL`，可用于两种调用形式。 |
| 15.2 | `<inline procedure call>` | 部分 | `CALL (v) { … }`、`CALL () { … }`、`CALL (*) { … }` 和 `CALL { WITH v … }` 都能正确导入。裸 `CALL { … }` 存在偏差：语法规则 3 说明省略变量作用域子句时会改写为命名传入工作记录的*每个*字段，因此按标准它像 `CALL (*) { … }` 一样导入全部。AgensGraph 则什么都不导入，也不抛错，因此查询回答的问题与表面不同——始终写导入列表。子查询体中的写子句会被拒绝，`IN TRANSACTIONS` 不存在。 |
| 15.3 | `<named procedure call>` | 部分 | `CALL routine(args) YIELD item [AS alias]` 和 `YIELD *` 可用；参数引用已在作用域中的变量时可关联。子条款允许省略 `YIELD`，这里它是必需的，且该子句既不能引导也不能结束查询。名称解析为 PostgreSQL 函数，而不是 17.5 描述的目录过程：原版服务端不注册过程，调用会抛出 `<name>() is a procedure`。 |
| 16.3 | `<graph pattern binding table>` | 部分 | 图模式生成绑定表。子条款还允许的模式 `YIELD` 子句是语法错误。 |
| 16.4 | `<graph pattern>` | 部分 | 逗号分隔的路径模式可用。匹配模式（`DIFFERENT EDGES`、`REPEATABLE ELEMENTS`）和 `KEEP` 子句是语法错误。 |
| 16.5 | `<insert graph pattern>` | 是 | `INSERT` 或 `CREATE` 后的模式可以创建顶点、边，或连接已绑定顶点之间的边。 |
| 16.7 | `<path pattern expression>` | 部分 | 串联可用。路径多重集交替和路径模式并集——用 `\|` 分隔两个路径模式——是语法错误。 |
| 16.8 | `<label expression>` | 部分 | 只支持单个标签名。析取（`:a\|b`）、合取（`:a&b`）、否定（`:!a`）和通配符（`:%`）都是语法错误。请在 `WHERE` 中用 `label()` 函数测试标签。 |
| 16.9 | `<path variable reference>` | 是 | `MATCH p = (…)` 绑定整条路径，`nodes()`、`relationships()` 和 `length()` 可读取它。 |
| 16.10 | `<element variable reference>` | 是 | 模式变量在其后的每个子句中都处于作用域内。 |
| 16.11 | `<graph pattern quantifier>` | 部分 | 边量词 `-[r*1..3]->` 遍历可变跳数。标准中放在带括号路径模式上的量词 `(…)->{1,3}` 是语法错误，用 `+` 代替 `*` 同样如此。 |
| 16.13 | `<where clause>` | 部分 | `WHERE` 可用于 `MATCH` 之后，以及 `FILTER`、`WITH` 和列表推导式内部。点模式内部的 `WHERE` 是语法错误。搜索条件必须是布尔值；属性读取不会被强制转换。 |
| 16.16 | `<order by clause>` | 是 | 多排序键、`ASC`/`DESC`、`NULLS FIRST`/`NULLS LAST`、表达式排序键，以及 `RETURN` 别名排序键。 |
| 16.17 | `<sort specification list>` | 是 | 同 16.16。整数排序键是常量，不是输出列号——见[Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)。 |
| 16.18 | `<limit clause>` | 是 | `LIMIT`，包括把表达式用作数量。 |
| 16.19 | `<offset clause>` | 是 | 子条款定义的两种拼法 `OFFSET` 和 `SKIP` 都支持。 |
| 19.1 | `<search condition>` | 是 | 条件只接受布尔值，这正是子条款的要求。 |
| 19.2 | `<predicate>` | 部分 | 下方四个谓词。19.6–19.13 定义的另外九个不支持。 |
| 19.3 | `<comparison predicate>` | 是 | `=`、`<>`、`<`、`<=`、`>`、`>=`，作用于标量、图元素和列表。 |
| 19.4 | `<exists predicate>` | 部分 | 子条款定义五种形式中的四种：`EXISTS { pattern }`（可带 `WHERE`）、`EXISTS ( pattern )`（不能带——括号内 `WHERE` 是语法错误）、`EXISTS { MATCH … }` 和 `EXISTS { <read statement> }`。`EXISTS ( MATCH … )` 是语法错误；包含多个 `MATCH` 的匹配语句块需要 `RETURN` 才能解析，因此不满足 Feature GQ22。 |
| 19.5 | `<null predicate>` | 是 | `IS NULL` 和 `IS NOT NULL`。 |
| 20.1 | `<value expression>` | 是 | 运算符、函数调用、`CASE`、子查询表达式和构造器可自由组合。 |
| 20.2 | `<value expression primary>` | 是 | 字面量、变量、属性引用、带括号表达式。 |
| 20.3 | `<value specification>` | 部分 | `SESSION_USER` 和 `CURRENT_USER`。参数是 PostgreSQL 参数 `$1`，由驱动提供，而不是由 GQL general-parameter 声明提供。 |
| 20.6 | `<value query expression>` | 是 | `VALUE { … }`，这正是该子条款定义的全部内容：返回体的单个值及其自身类型，体为空时为 null。语法规则 10 要求体带 `LIMIT 1` 或聚合；AgensGraph 接受任意体，并在运行时抛出 `more than one row returned by a subquery used as an expression`。`EXISTS { }` 属于 19.4；`COUNT { }`、`COLLECT { }`、`ARRAY { }` 和 `x IN { }` 是扩展——见下方。 |
| 20.7 | `<case expression>` | 是 | 搜索形式和简单形式都支持，另有 `NULLIF` 和 `COALESCE`。 |
| 20.8 | `<cast specification>` | 部分 | `::` 运算符执行转换，并接受关键字类型名（`::int`、`::numeric`、`::interval`）。`CAST(x AS t)` 在 Cypher 中是语法错误；在 SQL 中可用。 |
| 20.9 | `<aggregate function>` | 部分 | `COUNT(*)`，以及通用集合函数 `AVG`、`COUNT`、`MAX`、`MIN`、`SUM`、`STDDEV_SAMP` 和 `STDDEV_POP`，各自接受 `DISTINCT` 或 `ALL`。对顶点或边求 `MIN` 和 `MAX` 有歧义，必须给出转换或身份标识。`COLLECT_LIST` 拼作 `collect`。二元集合函数 `PERCENTILE_CONT` 和 `PERCENTILE_DISC` 无法从 Cypher 调用：二者都需要 `WITHIN GROUP`，而它在 Cypher 中是语法错误。 |
| 20.11 | `<property reference>` | 是 | `n.prop`、嵌套形式 `n.a.b` 和下标形式 `n.list[0]`。 |
| 20.12 | `<binding variable reference>` | 是 | 由模式、`WITH`、`LET`、`FOR` 或 `YIELD` 绑定的名称。 |
| 20.13 | `<path value expression>` | 部分 | `MATCH p = (…)` 绑定的路径是 `graphpath` 类型的一等值。 |
| 20.15 | `<list value expression>` | 部分 | `[a, b, c]`、下标、`IN` 和列表推导式。`LIST[…]` 是语法错误。 |
| 20.17 | `<list value constructor>` | 部分 | 同 20.15。 |
| 20.18 | `<record constructor>` | 部分 | `{a: 1, b: 2}` 构造映射，`.a` 读回字段。`RECORD { … }` 拼法是语法错误。 |
| 20.19 | `<field>` | 是 | 对映射的字段访问 `({a: 1}).a`。 |
| 20.20 | `<boolean value expression>` | 是 | `AND`、`OR`、`NOT`、`XOR` 和 `IS [NOT] UNKNOWN`。 |
| 20.21 | `<numeric value expression>` | 是 | `+`、`-`、`*`、`/`、`%`、`^`。 |
| 20.22 | `<numeric value function>` | 是 | `abs`、`ceil`、`floor`、`round`、`sign`、`sqrt`、`exp`、`ln`、`log`、`log10`、`power`、`mod`、`pi`、三角函数、`degrees`、`radians`、`char_length`、`octet_length` 和 `rand`。 |
| 20.23 | `<string value expression>` | 是 | 用 `\|\|` 拼接，也用 `+` 拼接。 |
| 20.24 | `<character string function>` | 部分 | `upper`、`lower`、`btrim`、`ltrim`、`rtrim`、`trim`、`substring(s, from, count)`、`left`、`right`、`replace`、`reverse`、`split`。`NORMALIZE` 和 `SUBSTRING(s FROM a FOR b)` 拼法在 Cypher 中是语法错误。 |
| 20.26 | `<datetime value expression>` | 部分 | 通过 PostgreSQL 类型进行日期和时间戳算术。 |
| 20.27 | `<datetime value function>` | 部分 | `CURRENT_DATE`、`CURRENT_TIME`、`CURRENT_TIMESTAMP`、`LOCALTIME`、`LOCALTIMESTAMP`。不识别标准使用的下划线拼法，如 `LOCAL_TIME`。 |
| 21.1 | 名称与变量 | 部分 | 未加引号标识符折叠为小写；双引号标识符保留大小写。标准的反引号标识符是语法错误。 |
| 21.2 | `<literal>` | 部分 | 整数（包括十六进制、八进制、二进制和下划线分隔形式）、浮点数、字符串、`true`、`false` 和 `null`、列表、映射。类型化字面量——`DATE '…'`、`DURATION '…'`、字节串——以及把 `UNKNOWN` 用作值都是语法错误。 |
| 21.3 | `<token>`、`<separator>` 与 `<identifier>` | 部分 | `--` 和 `/* */` 按标准界定注释。这使 openCypher 的匿名箭头 `-->` 和 `--` 不可用——见[Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)。 |

## 不支持的特性 {#features-not-supported}

这些子条款定义的语法都不被接受。存在替代路径时，注释给出 AgensGraph 的做法。

| 子条款 | 名称 | 支持 | 注释 |
| --- | --- | --- | --- |
| 7.1 | `<session set command>` | 否 | `SESSION SET` 是语法错误。用 `SET graph_path = name` 设置工作图；它是 PostgreSQL 设置，遵循 PostgreSQL 的会话和事务作用域。 |
| 7.2 | `<session reset command>` | 否 | 用 `RESET graph_path` 或 `RESET ALL`。 |
| 7.3 | `<session close command>` | 否 | 关闭连接。 |
| 7.4 | `<session parameter specification>` | 否 | 无。 |
| 10.1 | `<graph variable definition>` | 否 | 无。查询寻址一个图，由 `graph_path` 命名。 |
| 10.2 | `<binding table variable definition>` | 否 | 用 `WITH` 或 `LET` 绑定，或在 Cypher 外用 SQL 公用表表达式携带中间结果。 |
| 10.3 | `<value variable definition>` | 否 | 用受支持的 `LET`，即 14.7。 |
| 11.2 | `<binding table expression>` | 否 | 无。 |
| 11.3 | `<object expression primary>` | 否 | 无。 |
| 12.1 | `<linear catalog-modifying statement>` | 否 | 目录更改是 PostgreSQL DDL 语句，不能组合进查询流水线。 |
| 12.2 | `<create schema statement>` | 否 | 图*就是*模式；`CREATE GRAPH` 创建它。SQL `CREATE SCHEMA` 也存在，但不会创建图。 |
| 12.3 | `<drop schema statement>` | 否 | `DROP GRAPH`。 |
| 12.6 | `<create graph type statement>` | 否 | 无。标签无类型；提升为列的属性例外，它获得该列的类型。见[`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)。 |
| 12.7 | `<drop graph type statement>` | 否 | 无。 |
| 12.8 | `<call catalog-modifying procedure statement>` | 否 | 无。 |
| 13.6 | `<call data-modifying procedure statement>` | 否 | `CALL` 体内的写子句会被拒绝。 |
| 14.1 | `<composite query statement>` | 否 | 复合查询语句可选的 `USE` 前缀没有对应物；复合查询表达式本身（14.2）受支持。 |
| 14.12 | `<select statement>` | 否 | `SELECT … FROM MATCH (…)` 是语法错误。对 Cypher 子查询使用 SQL `SELECT` 可完成同样工作：见[SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。 |
| 16.1 | `<at schema clause>` | 否 | 语句运行在当前连接的数据库中。 |
| 16.2 | `<use graph clause>` | 否 | `SET graph_path = name`。 |
| 16.6 | `<path pattern prefix>` | 否 | 路径模式（`WALK`、`TRAIL`、`SIMPLE`、`ACYCLIC`）和路径搜索前缀（`ALL`、`ANY`、`ANY SHORTEST`、`ALL SHORTEST`、`SHORTEST k`、`SHORTEST k GROUPS`）都不能解析。`shortestpath()`、`allshortestpaths()` 和 `dijkstra()` 覆盖最短路径搜索。 |
| 16.12 | `<simplified path pattern expression>` | 否 | `-/ … /->` 形式是语法错误。 |
| 16.15 | `<group by clause>` | 否 | 显式 `GROUP BY` 在 Cypher 中是语法错误。分组是隐式的：`RETURN` 或 `WITH` 的非聚合项就是分组键。SQL 中可用 SQL `GROUP BY`。 |
| 17.1–17.8 | `<schema reference>` 及其他对象引用 | 否 | 对象用 PostgreSQL 模式限定名命名。标准的目录路径 `/dir/schema/graph` 不能解析。 |
| 18.1–18.10 | `<nested graph type specification>` 及其他类型元素 | 否 | 无。 |
| 19.6 | `<value type predicate>` | 否 | `IS TYPED` 和 `IS ::` 是语法错误。转换后比较，或使用 `pg_typeof`。 |
| 19.7 | `<normalized predicate>` | 否 | 无。 |
| 19.8 | `<directed predicate>` | 否 | 每条边都是有向的。 |
| 19.9 | `<labeled predicate>` | 否 | `IS LABELED` 是语法错误，表达式中的 `n:Label` 同样如此。写 `label(n) = 'person'`。 |
| 19.10 | `<source/destination predicate>` | 否 | `IS SOURCE OF` 和 `IS DESTINATION OF` 是语法错误。比较身份标识：`id(a) = id(startNode(r))`。 |
| 19.11 | `<all_different predicate>` | 否 | 逐对比较身份标识。 |
| 19.12 | `<same predicate>` | 否 | `id(a) = id(b)`。 |
| 19.13 | `<property_exists predicate>` | 否 | `PROPERTY_EXISTS(n, key)` 是语法错误。写 `exists(n.key)`。 |
| 20.4 | `<dynamic parameter specification>` | 否 | 由驱动的参数占位符 `$1` 代替。 |
| 20.5 | `<let value expression>` | 否 | 表达式内的 `LET … IN` 是语法错误。`LET` 语句（14.7）受支持。 |
| 20.10 | `<element_id function>` | 否 | `element_id()` 不存在。`id()` 返回身份标识，类型是 `graphid`。 |
| 20.14 | `<path value constructor>` | 否 | 路径来自模式，而不是构造器。 |
| 20.16 | `<list value function>` | 否 | `trim(list, n)` 和 `elements()` 不存在。`head`、`last`、`tail`、`size` 和 `cardinality` 存在。 |
| 20.25 | `<byte string function>` | 否 | PostgreSQL 的 `bytea` 函数可从 SQL 访问。 |
| 20.28 | `<duration value expression>` | 否 | PostgreSQL 的 `interval` 类型覆盖时长，但只能从 SQL 使用：`INTERVAL '1 day'` 在 Cypher 中是语法错误。 |
| 20.29 | `<duration value function>` | 否 | `duration()` 不存在。 |
| 21.4 | `<GQL terminal character>` | 否 | 词法分析器是 PostgreSQL 的，并为 Cypher 扩展；未实现标准的字符集规则。 |
| 22.1–22.20 | 附加通用规则 | 否 | 这些子条款定义的是标准的求值机制而不是语法。AgensGraph 通过 PostgreSQL 规划器和执行器求值查询，因此未按原文实现。 |
| 23.1 | GQLSTATUS | 否 | 错误携带 SQLSTATE。见[错误码](/zh/agensgraph/appendix/error-codes/)。 |
| 23.2 | 诊断记录 | 否 | 诊断来自 PostgreSQL 的错误报告字段。 |

## 超出标准的扩展 {#extensions-beyond-the-standard}

AgensGraph 接受许多 ISO/IEC 39075 未定义的内容。其中一部分是产品先行支持的 openCypher；另一部分存在的原因是图存储在 PostgreSQL 中，并且两半都可寻址。

| 扩展 | 增加的能力 |
| --- | --- |
| 在 Cypher 子查询上执行 SQL 语句，以及在标签表上执行 Cypher | Cypher 查询是表表达式，标签是表，因此一条语句可以连接图数据和关系数据。见[SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。 |
| `LOAD FROM table AS r CREATE (…)` | 从关系（包括外部表）的行创建图元素。见[加载数据](/zh/agensgraph/guides/loading-data/)。 |
| 标签继承 | `CREATE VLABEL child INHERITS (parent)` 创建标签层级，匹配父标签时也返回子标签。`MATCH (n:parent ONLY)` 把匹配限制为父标签。见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。 |
| `SET n += map` | 把映射合并进属性，而不是替换属性。 |
| `dijkstra()`、`shortestpath()`、`allshortestpaths()` | 加权与非加权最短路径搜索，代替标准的路径搜索前缀。 |
| 提升属性 | `ALTER VLABEL movie ADD COLUMN year int GENERATED` 为属性提供类型化且可索引的列，属性读取会解析到该列。见[`ALTER VLABEL`](/zh/agensgraph/reference/ddl/alter-label/)。 |
| 图 DDL | `CREATE VLABEL`、`CREATE ELABEL`、`CREATE PROPERTY INDEX`、`CREATE CONSTRAINT`、`REINDEX VLABEL` 和 `ALTER VLABEL`。见[数据定义](/zh/agensgraph/reference/ddl/)。 |
| openCypher 子句 | `UNWIND`、带 `ON CREATE` 和 `ON MATCH` 的 `MERGE`，以及 `WITH`。 |
| `COUNT { }`、`COLLECT { }`、`ARRAY { }`、`x IN { }` | 标准没有对应形式的四个子查询值表达式——20.9 只定义 `COUNT(*)`、`COUNT(expr)` 和对行聚合的 `COLLECT_LIST`。`COUNT { }` 和 `COLLECT { }` 来自 openCypher，`ARRAY { }` 来自 SQL 的 `ARRAY(subquery)`，`x IN { }` 来自 SQL 的 `IN (subquery)`。见[子查询值表达式](/zh/agensgraph/reference/clauses/subquery-expressions/)。 |
| openCypher 运算符与函数 | `STARTS WITH`、`ENDS WITH`、`CONTAINS`、`=~`、列表推导式、`all`/`any`/`none`/`single`、`keys`、`properties`、`id`、`label`、`labels`、`type`、`startNode`、`endNode`、`nodes`、`relationships`、`length`、`range`、`head`、`last`、`tail`、`toString`、`toInteger`、`toFloat`。 |
| PostgreSQL 全部能力 | 图查询可使用每个 SQL 类型、函数、索引方法、扩展和设置，向量搜索和全文搜索正依赖于此。见[向量搜索](/zh/agensgraph/guides/search/vector/)。 |

## 另见 {#see-also}

- [Cypher、GQL 和 SQL](/zh/agensgraph/concepts/languages/)——三种语言如何在一条语句中关联
- [Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)——AgensGraph 与其他 Cypher 实现的差异
- [关键字](/zh/agensgraph/appendix/keywords/)——标准新语句保留的词
- [AgensGraph 2.18.6.1 发布说明](/zh/agensgraph/release-notes/2.18/)——本版本新增的 GQL 语句
