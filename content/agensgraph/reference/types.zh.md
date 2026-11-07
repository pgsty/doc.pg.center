---
title: 数据类型
linkTitle: 数据类型
description: AgensGraph 在 PostgreSQL 类型集合之外新增五个类型：graphid、vertex、edge、graphpath 和 rowid。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/types.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 在 PostgreSQL 类型集合之外新增五个类型：`graphid`、`vertex`、`edge`、`graphpath` 和 `rowid`。图存储的其他内容都是 `jsonb`，位于标签的 `properties` 列中。每个 PostgreSQL 类型仍然可用，并按 PostgreSQL 文档的行为运行。

这五个类型在 `pg_type` 中使用固定 OID 定义，因此在每个数据库中都相同，且不需要扩展。

| 类型 | 存储 | 保存内容 |
| --- | --- | --- |
| `graphid` | 8 字节，按值 | 一个顶点或边的身份标识。 |
| `vertex` | 组合类型，变长 | id、属性映射，以及行的物理位置。 |
| `edge` | 组合类型，变长 | id、两个端点 id、属性映射，以及行的位置。 |
| `graphpath` | 组合类型，变长 | 顶点数组和边数组。 |
| `rowid` | 10 字节，按引用 | 表 OID 和行指针。内部使用。 |

## graphid {#graphid}

`graphid` 是顶点或边的身份标识。边用它表示端点。它是分成两部分的 64 位值：高 16 位是**标签 id**，低 48 位是**本地 id**，即每个标签自己的序列。它打印为 *labid*`.`*locid*。

[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/#identity-the-graphid)说明这个布局为什么对规划器重要。本节是形式化细节。

两个函数可以把组成部分拆开：

```sql
SELECT id, graphid_labid(id) AS labid, graphid_locid(id) AS locid
FROM moviekb.person WHERE properties->>'name' = 'Keanu Reeves';
```

```
 id  | labid | locid
-----+-------+-------
 4.1 |     4 |     1
```

`graphid(`*labid*`, `*locid*`)` 由组成部分构造一个值。标签的 `id` 列在默认表达式中调用的就是同一个函数。

### 范围 {#range}

标签 id 是 16 位，本地 id 是 48 位，所以最大的 `graphid` 是：

```sql
SELECT graphid(65535, 281474976710655) AS highest;
```

```
        highest
-----------------------
 65535.281474976710655
```

任一部分越界都会被拒绝，而不是截断：

```sql
SELECT graphid(65536, 1);
```

```
ERROR:  labid out of range: 65536
```

```sql
SELECT graphid(3, 281474976710656);
```

```
ERROR:  locid out of range: 281474976710656
```

0 保留为*无标签*，所以一个数据库最多有 65,535 个标签，一个标签最多有 2<sup>48</sup> − 1 个元素。这个保留是约定而不是检查，`graphid(0, 1)` 会构造 `0.1`。但没有任何机制会分配标签 id 0。[限制](/zh/agensgraph/appendix/limits/)把这些限制与 PostgreSQL 自身的限制汇总在一起。

### 类型转换 {#casts}

转换为 `graphid` 的 cast 只有一个，来自 `numeric`，而且是隐式转换。没有来自 `integer` 的转换，所以不带小数点写出的整数不能转换：

```sql
SELECT 1::graphid;
```

```
ERROR:  cannot cast type integer to graphid
LINE 1: SELECT 1::graphid;
                ^
```

请写出两个部分。带小数点的 numeric 字面量可以转换，*labid*`.`*locid* 形式的字符串可以解析：

```sql
SELECT 1.1::graphid AS from_numeric, '3.1'::graphid AS from_text;
```

```
 from_numeric | from_text
--------------+-----------
 1.1          | 3.1
```

`numeric` 转换按该类型打印的方式读取数字。因此 `1.1` 是标签 1、元素 1，不是数值一点一。没有小数位的 numeric 没有本地 id，会被拒绝：`1::numeric::graphid` 抛出 `invalid input syntax for type graphid: "1"`。

没有从 `graphid` 出去的转换。用 `graphid_labid()` 和 `graphid_locid()` 取得各部分，或让它按类型输出。

## vertex 与 edge {#vertex-and-edge}

`vertex` 是由三个字段组成的复合值：`id graphid`、`properties jsonb`，以及保存行物理位置的 `tid`。写操作用这个 `tid` 再次找到行。`edge` 具有同样三个字段，并增加 `start graphid` 和 `end graphid`。

它们的打印形式显示标签、id 和属性：

```cypher
MATCH (p:person {name: 'Keanu Reeves'}) RETURN p;
```

```
                         p
---------------------------------------------------
 person[4.1]{"born": 1964, "name": "Keanu Reeves"}
```

边在 id 和属性之间打印端点，起始端点在前：

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[r:acted_in]->(:movie {title: 'The Matrix'}) RETURN r;
```

```
                   r
---------------------------------------
 acted_in[5.1][4.1,3.1]{"role": "Neo"}
```

因此顶点的形状是 `label[id]{properties}`，边的形状是 `label[id][start,end]{properties}`。没有属性的元素打印空映射：`directed[6.8][4.8,3.5]{}`。

`tid` 字段不属于任一打印形式，也不应依赖。行更新时它会变化。

### 可以对它们做什么 {#what-you-can-do-with-them}

`vertex` 和 `edge` 各有六个比较运算符，没有其他运算符：

| 类型 | 运算符 |
| --- | --- |
| `graphid` | `=` `<>` `<` `<=` `>` `>=` |
| `vertex` | `=` `<>` `<` `<=` `>` `>=` |
| `edge` | `=` `<>` `<` `<=` `>` `>=` |
| `rowid` | `=` `<>` `<` `<=` `>` `>=` |
| `graphpath` | 无 |

**比较只基于身份标识。**`vertex_eq` 及其同类比较 `id` 字段，完全忽略属性。属性相同但 id 不同的两个顶点不相等：

```cypher
CREATE GRAPH twins;
SET graph_path = twins;
CREATE VLABEL pair;
CREATE (:pair {k: 1}), (:pair {k: 1});
MATCH (a:pair), (b:pair) WHERE id(a) < id(b)
RETURN a, b, a = b AS equal, properties(a) = properties(b) AS same_properties;
```

```
         a         |         b         | equal | same_properties
-------------------+-------------------+-------+-----------------
 pair[3.1]{"k": 1} | pair[3.2]{"k": 1} | f     | t
```

排序遵循同一规则。`a < b` 比较 `graphid` 值，因此先按标签顺序，再按标签内的插入顺序。该顺序全序且稳定，适合作为 `ORDER BY` 的决胜项。它不是数据本身有意义的排序。

```cypher
MATCH (a:person {name: 'Keanu Reeves'}), (b:person {name: 'Carrie-Anne Moss'})
RETURN a = b AS equal, a < b AS less, id(a) AS id_a, id(b) AS id_b;
```

```
 equal | less | id_a | id_b
-------+------+------+------
 f     | t    | 4.1  | 4.3
```

要比较属性，就比较属性本身：`properties(a) = properties(b)`，或者明确列出你关心的键。

两个类型都可以隐式转换为 `jsonb`。转换保留属性映射并丢弃身份标识：`pg_cast` 中的 `vertex_to_jsonb` 和 `edge_to_jsonb`。因此 `m::jsonb` 等价于 `properties(m)`。反方向没有转换。

## graphpath {#graphpath}

`graphpath` 是由两个数组组成的复合类型：`vertices vertex[]` 和 `edges edge[]`。*n* 条边的路径包含 *n* + 1 个顶点，因此绑定到单个顶点的路径有一个顶点、零条边：

```cypher
MATCH p = (a:person {name: 'Keanu Reeves'}) RETURN p;
```

```
                          p
-----------------------------------------------------
 [person[4.1]{"born": 1964, "name": "Keanu Reeves"}]
```

它打印为按游走顺序排列、用逗号分隔的方括号成员列表，顶点、边、顶点交替。两个数组交错输出，而不是打印成两个数组。因此一条边的路径打印三个成员，*n* 条边的路径打印 2*n* + 1 个成员。

用 `nodes()` 和 `edges()` 获取成员，它们返回两个数组。`length()` 是边数：

```cypher
MATCH p = (:person {name: 'Keanu Reeves'})-[:acted_in]->(:movie {title: 'The Matrix'})
RETURN length(p) AS hops, nodes(p)[0] AS first_vertex, edges(p)[0] AS only_edge;
```

```
 hops |                   first_vertex                    |               only_edge
------+---------------------------------------------------+---------------------------------------
 1    | person[4.1]{"born": 1964, "name": "Keanu Reeves"} | acted_in[5.1][4.1,3.1]{"role": "Neo"}
```

`graphpath` **没有自己的运算符**，既没有相等也没有排序。在 Cypher 中，比较两条路径会被拒绝。由于没有可调用的运算符，表达式回退到 `jsonb`，而路径不是 `jsonb` 值：

```cypher
MATCH p1 = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix'}),
      p2 = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix'})
RETURN p1 = p2;
```

```
ERROR:  graph object cannot be jsonb
LINE 3: RETURN p1 = p2;
               ^
```

在 SQL 中可以比较，走的是 PostgreSQL 复合值的通用运算符，它会逐字段遍历两个数组：

```psql
SELECT a = b AS equal, a < b AS less
FROM (MATCH p = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix'})
      RETURN p AS a) x,
     (MATCH p = (:person {name:'Keanu Reeves'})-[:acted_in]->(:movie {title:'The Matrix Reloaded'})
      RETURN p AS b) y;
```

```
 equal | less
-------+------
 f     | t
```

这个比较包含 `tid` 字段，因此比较的是整次游走的身份标识，而不是路径的含义。如果需要可解释的比较，请比较 `nodes(p)` 或 id。

`to_jsonb()` 在 Cypher 和 SQL 中都可以转换路径。结果暴露内部结构：两个数组以及每个成员的 `tid`。`pg_cast` 中没有 `graphpath` 到 `jsonb` 的转换。因此 `p::jsonb` 在 Cypher 中可用，因为它会降级为函数调用；在 SQL 中失败，错误为 `cannot cast type graphpath to jsonb`。

## rowid {#rowid}

`rowid` 把表 OID 和行指针配成一对。最短路径执行器在内部用它携带边身份标识。它有六个比较运算符和一个 btree 运算符类，但**没有输出函数**：

```sql
SELECT rowid('moviekb.person'::regclass, ctid) FROM moviekb.person LIMIT 1;
```

```
ERROR:  "rowid" type does not support output function
```

`rowid_tableoid()` 和 `rowid_ctid()` 读取两个部分，这是查看值的唯一方式：

```sql
SELECT rowid_tableoid(rowid('moviekb.person'::regclass, '(0,1)')) AS tableoid,
       rowid_ctid(rowid('moviekb.person'::regclass, '(0,1)')) AS ctid;
```

```
 tableoid | ctid
----------+-------
    16482 | (0,1)
```

OID 是 `moviekb.person` 在该数据库中碰巧取得的值，因此不同安装会不同。

Cypher 中没有任何内容产生 `rowid`，应用代码也没有理由使用它。它出现在这里是因为会出现在 `pg_type` 和 `\dT` 中。

## 图类型数组 {#arrays-of-graph-types}

`vertex[]`、`edge[]` 和 `graphpath[]` 是普通 PostgreSQL 数组类型，拥有自己的输出函数，因此按其元素相同的方括号样式打印。

`collect()` 作用于顶点、边或路径时返回这些原生数组之一；作用于其他任何值时返回 `jsonb`：

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
RETURN pg_typeof(collect(m)) AS collect_vertex, pg_typeof(collect(m.title)) AS collect_property;
```

```
 collect_vertex | collect_property
----------------+------------------
 "vertex[]"     | "jsonb"
```

原生数组保存元素本身，而不是每个元素的 `jsonb` 副本，所以成员保留身份标识。`films[0]` 是 `vertex`，可以读取它的属性，或在后续子句中沿它遍历。

一些列表函数同时携带 `jsonb` 重载和原生数组重载。调用哪个由参数决定。在 Cypher 中参数通常是 `jsonb`，结果也是 `jsonb`。在 SQL 中给同一函数真实数组，返回的也是真实数组。签名见[类型转换函数](/zh/agensgraph/reference/functions/type-conversion/)。

### 数组下标起点 {#array-index-origin}

Cypher 的列表下标从 0 开始并接受负数下标，这条规则也适用于原生数组：

```cypher
MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
WITH collect(m) AS films
RETURN films[0].title AS cypher_index_0, films[1].title AS cypher_index_1, size(films) AS n;
```

```
 cypher_index_0 |    cypher_index_1     | n
----------------+-----------------------+---
 "The Matrix"   | "The Matrix Reloaded" | 4
```

同一个数组从 SQL 访问时遵循 PostgreSQL 规则，下标从 1 开始，0 越界：

```psql
SELECT (films[1]).properties ->> 'title' AS sql_index_1,
       (films[0]).properties ->> 'title' AS sql_index_0
FROM (MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
      RETURN collect(m) AS films) q;
```

```
 sql_index_1 | sql_index_0
-------------+-------------
 The Matrix  | null
```

`unnest()` 把数组转回多行，这在 SQL 中通常正是需要的：

```psql
SELECT (v).id AS id, (v).properties ->> 'title' AS title
FROM (MATCH (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie)
      RETURN collect(m) AS films) q,
     unnest(q.films) AS v ORDER BY id;
```

```
 id  |          title
-----+--------------------------
 3.1 | The Matrix
 3.2 | The Matrix Reloaded
 3.3 | The Matrix Revolutions
 3.4 | The Matrix Resurrections
```

## 属性：jsonb {#properties-jsonb}

标签有一个类型为 `jsonb` 的 `properties` 列，该标签中每个顶点或边的所有属性都存放在这里。因此属性没有声明类型：它的类型就是其值所属的 JSON 类型。

### 属性值可以是什么 {#what-a-property-value-may-be}

全部六种 JSON 类型：

| JSON 类型 | Cypher 写法 | 说明 |
| --- | --- | --- |
| string | `'text'` | 单引号。转义遵循 JSON 规则。 |
| number | `42`、`1.5`、`1e3` | 一种 JSON 数字类型；不区分整数和浮点数。 |
| boolean | `true`、`false` | |
| array | `[1, 'two', null]` | 可以混合类型并嵌套。 |
| object | `{a: {b: 1}}` | 键不加引号时折叠为小写。 |
| null | `null` | 赋 null **删除**属性，除非 [`allow_null_properties`](/zh/agensgraph/reference/guc/#allow_null_properties) 开启。 |

```cypher
MATCH (m:movie {title: 'The Matrix'})-[r:related_to]->()
RETURN jsonb_typeof(m.title) AS title, jsonb_typeof(m.embedding) AS embedding,
       jsonb_typeof(r.weight) AS weight, jsonb_typeof(m.no_such_key) AS absent
LIMIT 1;
```

```
  title   | embedding |  weight  | absent
----------+-----------+----------+--------
 "string" | "array"   | "number" | null
```

缺失属性和 null 属性是同一回事。因此缺失键的 `jsonb_typeof` 是 null，而不是 `"null"`。

数字只有一种类型，但你写入的标度会被保存，并决定除法是否截断：

```cypher
CREATE GRAPH demo;
SET graph_path = demo;
CREATE VLABEL t;
CREATE (:t {a: 7, b: 7.0});
MATCH (n:t) RETURN n.a AS a, n.b AS b, n.a / 2 AS a_div, n.b / 2 AS b_div;
```

```
 a |  b  | a_div |       b_div
---+-----+-------+--------------------
 7 | 7.0 | 3     | 3.5000000000000000
```

`n.a` 和 `n.b` 的 `jsonb_typeof` 都是 `number`，且比较相等，所以这不是两个类型；这是一个会记住写入时小数位数的类型。

因为没有声明类型，不同类型值之间的顺序由 `jsonb` 比较决定：先是 null，然后是 string、number、boolean、array、object。这个顺序来自 PostgreSQL。它也是同一个属性提升为类型化列后，排序可能与从属性包中读出时不同的原因。

### RETURN 交回什么 {#what-a-return-hands-back}

Cypher 的 `RETURN` 会把每个标量输出列装箱为 `jsonb`。`boolean` 保持布尔值，图类型保持自身：

```psql
SELECT pg_typeof(a) AS property, pg_typeof(b) AS property_cast_to_text,
       pg_typeof(c) AS string_literal, pg_typeof(d) AS number_literal,
       pg_typeof(e) AS boolean, pg_typeof(f) AS id, pg_typeof(g) AS vertex,
       pg_typeof(h) AS path
FROM (MATCH p = (:person {name: 'Keanu Reeves'})-[:acted_in]->(m:movie {title: 'The Matrix'})
      RETURN m.title AS a, m.title::text AS b, 'x' AS c, 1 AS d, true AS e,
             id(m) AS f, m AS g, p AS h) q;
```

```
 property | property_cast_to_text | string_literal | number_literal | boolean |   id    | vertex |   path
----------+-----------------------+----------------+----------------+---------+---------+--------+-----------
 jsonb    | jsonb                 | jsonb          | jsonb          | boolean | graphid | vertex | graphpath
```

注意第二列：`RETURN` 内的 `::text` 转换会被装箱撤销，因此没有效果。字符串所以会带 JSON 引号打印：

```cypher
MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS title;
```

```
    title
--------------
 "The Matrix"
```

要得到普通标量，请在 SQL 中从 `jsonb` 取值。`#>> '{}'` 把整个文档提取为 text：

```psql
SELECT title #>> '{}' AS title
FROM (MATCH (m:movie {title: 'The Matrix'}) RETURN m.title AS title) q;
```

```
   title
------------
 The Matrix
```

[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)完整介绍包装方法。装箱只适用于来自属性的列。布尔表达式保持 `boolean`，`id(n)` 保持 `graphid`，图元素保持 `vertex`、`edge` 或 `graphpath`。已提升为类型化列的属性也不装箱：该读取由列回答，并按列自身类型返回。

### :: 转换 {#the--cast}

Cypher 的 `::` 接受的类型名集合比 SQL 小。它接受普通类型名或函数名，例如 `text`、`date`、`uuid`、`jsonb` 或 `inet`。它也接受 SQL 语法特殊处理的成组拼法：数字名（`int`、`integer`、`smallint`、`bigint`、`real`、`float`、`double precision`、`decimal`、`numeric`、`boolean`）、字符名（`char`、`varchar`、`character varying`），以及 `bit`、`bit varying`、`json` 和 `interval`。

```cypher
RETURN '42'::int AS i, '4.2'::numeric AS n, 'x'::text AS t, '101'::bit(3) AS b,
       '1 day'::interval AS iv, 'true'::boolean AS bo, '2020-01-01'::date AS d;
```

```
 i  |  n  |  t  |   b   |   iv    | bo |      d
----+-----+-----+-------+---------+----+--------------
 42 | 4.2 | "x" | "101" | "1 day" | t  | "2020-01-01"
```

原因在于转换如何命名类型。Cypher 转换接受普通类型名，也接受语言特殊处理的数字、字符、bit、json 和 interval 拼法。`TIMESTAMP` 和 `TIME` 也是特殊拼法，而它们恰好是被遗漏的两个。因此二者都被拒绝：

```cypher
RETURN '2020-01-01 10:00'::timestamp;
```

```
ERROR:  syntax error at or near "timestamp"
LINE 1: RETURN '2020-01-01 10:00'::timestamp;
                                   ^
```

```cypher
RETURN '10:00'::time;
```

```
ERROR:  syntax error at or near "time"
LINE 1: RETURN '10:00'::time;
                        ^
```

给类型名加引号。加引号的名称是标识符而不是关键字，因此会走那条有效的规则。它命中的是同一类型：

```cypher
RETURN '2020-01-01 10:00'::"timestamp" AS ts, '10:00'::"time" AS t;
```

```
          ts           |     t
-----------------------+------------
 "2020-01-01T10:00:00" | "10:00:00"
```

其他时间相关类型都是普通名称，不需要引号，包括 `date` 和 `timestamptz`：

```cypher
RETURN pg_typeof('2020-01-01'::date) AS d, pg_typeof('2020-01-01'::timestamptz) AS tz;
```

```
   d    |             tz
--------+----------------------------
 "date" | "timestamp with time zone"
```

另一条路径是在 Cypher 外转换，那里可以使用完整 SQL 语法：

```psql
SELECT (t #>> '{}')::timestamp AS released FROM (RETURN '2020-01-01 10:00' AS t) q;
```

```
      released
---------------------
 2020-01-01 10:00:00
```

注意两个结果的差异。在 Cypher 内，值被重新装箱为 `jsonb`，所以带引号按 JSON 的 ISO 形式打印。SQL 转换得到真正的 `timestamp`，由该类型的输出函数打印。

还有一个不对称要了解。对字符串字面量执行 `'…'::jsonb` 得到的是 `jsonb` **字符串**，不是解析后的文档，因为这个字面量已经是 JSON 字符串。要在 Cypher 中构造 `jsonb` 对象，请写映射字面量：

```cypher
RETURN '{"a": 1}'::jsonb AS as_string, {a: 1} AS as_map;
```

```
  as_string   |  as_map
--------------+----------
 "{\"a\": 1}" | {"a": 1}
```

## 可以使用哪些 PostgreSQL 类型 {#which-postgresql-types-you-can-use}

全部都可以。图与你的表在同一个数据库中，所以 [PostgreSQL 数据类型章节](https://www.postgresql.org/docs/18/datatype.html)中的每个类型都原样可用。这包括数字、字符、日期/时间、布尔、枚举、几何、网络地址、位串、文本搜索、UUID、XML、JSON、数组、复合、范围、域和对象标识符。扩展新增的任何类型也可用。

PostgreSQL 类型在三个位置与图相遇：

* **图旁边的普通表**，可在一条语句中与图连接。当你需要 `timestamptz`、`numeric(10,2)` 或 `tsvector` 的语义和运算符时，它们属于这里。
* **标签上的提升列**，把一个属性物化为真实类型的真实列，使该属性获得该类型的排序、比较和索引支持。
* **存放在属性或提升列中的扩展类型**。`pgvector` 的 `vector` 就是[向量搜索](/zh/agensgraph/guides/search/vector/)依赖的情形。

属性本身不能是这些类型。属性是 `jsonb`，写入属性的值会在入口转换为某个 JSON 类型。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

`vertex`、`edge` 和 `graphpath` 对应 openCypher 类型系统中的节点、关系和路径。这里的标量类型不是分开的：string、number、boolean、list 和 map 都是 `jsonb`。因此数字呈整数还是小数由值决定，而不是由声明类型决定。

时间值不是图类型。`date`、`timestamptz` 和 `interval` 属于 PostgreSQL，通过转换、普通列或提升列访问。没有图层面的 `datetime` 或 `duration`。完整差异清单见[Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)。

### ISO/IEC 39075 {#isoiec-39075}

标准中的属性图类型以同样方式对应到 `vertex`、`edge` 和 `graphpath`。提升列提供其类型化值模型，即属性带有声明类型。见[GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)。

## 另见 {#see-also}

- [语法](/zh/agensgraph/reference/syntax/)——字面量、运算符以及值的书写方式
- [服务端设置](/zh/agensgraph/reference/guc/)——`allow_null_properties` 和 `enable_property_promotion`
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)——标签表由什么组成
- [组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)——跨边界传递值
- [系统目录](/zh/agensgraph/system-catalogs/catalogs/)——`ag_graph`、`ag_label` 及其他目录
- [PostgreSQL: data types](https://www.postgresql.org/docs/18/datatype.html)——你可以使用的其他所有类型
