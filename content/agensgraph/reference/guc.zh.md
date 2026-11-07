---
title: 服务端设置
linkTitle: 服务端设置
description: AgensGraph 在 PostgreSQL 的数百个设置之外新增十一个设置。
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/guc.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


AgensGraph 在 PostgreSQL 的数百个设置之外新增十一个设置。本页记录这十一个。其他所有设置都是 PostgreSQL 的且未改变，见 [PostgreSQL 服务端配置章节](https://www.postgresql.org/docs/18/runtime-config.html)。关于在哪里以及*如何*设置，见[配置](/zh/agensgraph/operations/configuration/)；该页覆盖 `postgresql.conf`、`ALTER SYSTEM`、`ALTER DATABASE`、`ALTER ROLE` 和 `SET`。

十一个设置中的 `graph_path` 是每个运行 Cypher 的会话都需要的。其余设置都有可用默认值，在你有理由改变之前可以忽略。

## 设置列表 {#the-settings}

下表每个默认值都是 `pg_settings.boot_val`，从运行中的服务端读取：

```sql
SELECT name, vartype AS type, boot_val AS default, coalesce(unit,'') AS unit, context
FROM pg_settings
WHERE name IN ('allow_null_properties','auto_gather_graphmeta','cypher_allow_unsafe_ddl',
               'eager_mem','enable_eager','enable_graph_ddl','enable_graph_dml',
               'enable_graph_endpoint_elision','enable_multiple_update',
               'enable_property_promotion','graph_path')
ORDER BY name;
```

```
             name              |  type   | default | unit |  context
-------------------------------+---------+---------+------+-----------
 allow_null_properties         | bool    | off     |      | user
 auto_gather_graphmeta         | bool    | off     |      | superuser
 cypher_allow_unsafe_ddl       | bool    | off     |      | user
 eager_mem                     | integer | 4096    | kB   | user
 enable_eager                  | bool    | on      |      | user
 enable_graph_ddl              | bool    | off     |      | user
 enable_graph_dml              | bool    | off     |      | superuser
 enable_graph_endpoint_elision | bool    | on      |      | user
 enable_multiple_update        | bool    | on      |      | user
 enable_property_promotion     | bool    | on      |      | user
 graph_path                    | string  |         |      | user
```

两个 context 值按如下方式理解：

`user`
: 任何角色都可以在任何会话的任何时间更改。它也可以设置在 `postgresql.conf`、按数据库或按角色设置。

`superuser`
: 只有超级用户，或被授予该参数 `SET` 权限的角色，可以在会话中更改。其他角色会得到 `permission denied to set parameter`。

请查询 `pg_settings`，不要读 `postgresql.conf.sample`。安装目录中的示例文件把 `enable_eager` 和 `enable_multiple_update` 写成 `off`。二者真正的默认值都是 `on`，从该文件复制的表格会有两行错误。

## agversion：预设而不是设置 {#agversion-a-preset-rather-than-a-setting}

`agversion` 报告 AgensGraph 版本。它的 context 是 `internal`，因此是*预设*：服务端告诉你的内容，而不是你配置的内容。它不能出现在 `postgresql.conf` 中，设置它会被拒绝：

```sql
SET agversion = '1';
```

```
ERROR:  parameter "agversion" cannot be changed
```

```sql
SELECT name, setting, context, category FROM pg_settings WHERE name = 'agversion';
```

```
   name    |  setting   | context  |    category
-----------+------------+----------+----------------
 agversion | 2.18.6.1 | internal | Preset Options
```

用 `SHOW` 读取它，这是确认所连接版本的常规方式：

```sql
SHOW agversion;
```

```
 agversion
------------
 2.18.6.1
```

`version()` 和 `server_version` 报告该版本构建所基于的 PostgreSQL 版本。客户端如果两个都需要知道，就应该都读取。

## graph_path {#graph_path}

```
string · default '' (empty) · context user
```

指定会话工作的图。Cypher 或 GQL 语句中每个未限定标签名都会在这个图中解析。每条图 DDL 语句也在这个图中创建或修改标签。它是 `search_path` 的图对应物，也是不能跳过的设置。

没有它，什么都不会解析：

```cypher
RESET graph_path;
MATCH (n:person) RETURN count(n);
```

```
ERROR:  graph_path is NULL
HINT:  Use SET graph_path
```

设置后，同一语句可以运行：

```sql
SET graph_path = moviekb;
SHOW graph_path;
```

```
 graph_path
------------
 moviekb
```

`CURRENT_GRAPH` 在语句内以裸关键字读取同一个值：

```cypher
SELECT CURRENT_GRAPH;
```

```
 current_graph
---------------
 moviekb
```

### 恰好一个图名 {#exactly-one-graph-name}

与 `search_path` 不同，`graph_path` 不是列表。逗号分隔的值不会被解析成两个名称，而是被当作一个名称，并且这个名称不存在：

```sql
SET graph_path = 'moviekb, twins';
```

```
ERROR:  invalid value for parameter "graph_path": "moviekb, twins"
DETAIL:  graph "moviekb, twins" does not exist.
```

因此一个会话读写一个图。要在一条语句中访问两个图，请使用 SQL，它把图视为两个模式。模式见[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。

### 何时校验值 {#when-the-value-is-checked}

不存在的图会在 `SET` 时被拒绝，而不是查询时：

```sql
SET graph_path = nosuchgraph;
```

```
ERROR:  invalid value for parameter "graph_path": "nosuchgraph"
DETAIL:  graph "nosuchgraph" does not exist.
```

名称是标识符，不加引号会折叠为小写。用混合大小写名称创建的图需要引号：

```cypher
CREATE GRAPH "MixedCase";
SET graph_path = MixedCase;
```

```
ERROR:  invalid value for parameter "graph_path": "mixedcase"
DETAIL:  graph "mixedcase" does not exist.
```

```sql
SET graph_path = "MixedCase";
SHOW graph_path;
```

```
 graph_path
------------
 MixedCase
```

```cypher
DROP GRAPH "MixedCase" CASCADE;
SET graph_path = moviekb;
```

### 为数据库或角色设置一个值 {#one-value-for-a-database-or-a-role}

`SET` 只持续到会话结束。两个更大范围可避免重复设置；二者都在下一次连接生效，而不是当前连接立即生效。

为连接到某个数据库的所有人设置：

```sql
ALTER DATABASE docs SET graph_path = moviekb;
```

```
ALTER DATABASE
```

为某个角色设置，无论它连接哪个数据库：

```sql
ALTER ROLE analyst SET graph_path = moviekb;
```

```
ALTER ROLE
```

二者在 `pg_db_role_setting` 中可见，角色设置优先于数据库设置：

```sql
SELECT r.rolname, s.setconfig FROM pg_db_role_setting s
JOIN pg_roles r ON r.oid = s.setrole WHERE r.rolname = 'analyst';
```

```
 rolname |      setconfig
---------+----------------------
 analyst | {graph_path=moviekb}
```

之后连接的角色已经拥有该值：

```sql
SHOW graph_path;
```

```
 graph_path
------------
 moviekb
```

`ALTER DATABASE … RESET graph_path` 和 `ALTER ROLE … RESET graph_path` 会再次删除设置。`postgresql.conf` 中的集群级默认值也可以，但很少是你想要的：它会让集群中每个数据库都声称有这个图。

值会对照目录校验，所以 `ALTER DATABASE db SET graph_path` 必须在连接到 `db` 时运行。校验查找的是*当前*数据库中的图。在其他数据库中运行会失败：

```sql
ALTER DATABASE docs SET graph_path = moviekb;
```

```
ERROR:  invalid value for parameter "graph_path": "moviekb"
DETAIL:  graph "moviekb" does not exist.
```

## allow_null_properties {#allow_null_properties}

```
bool · default off · context user
```

决定 null 属性值是存储还是丢弃。

关闭时，赋 null 会删除属性。设置为 null 的属性与从未存在的属性是同一回事。开启时，null 存储为 JSON null，键保留。

```cypher
CREATE GRAPH nulls;
SET graph_path = nulls;
CREATE VLABEL t;
CREATE (:t {name: 'a', extra: null});
SET allow_null_properties = on;
CREATE (:t {name: 'b', extra: null});
MATCH (n:t) RETURN n ORDER BY id(n);
```

```
                 n
------------------------------------
 t[3.1]{"name": "a"}
 t[3.2]{"name": "b", "extra": null}
```

当导入数据的缺失值和 null 值含义不同、且需要保留这个区别时开启它。典型情形是从关系型数据源导入。

代价是存储的 null 是“键存在但没有值”。各测试对此并不一致：

```cypher
MATCH (n:t) RETURN exists(n.extra) AS exists, n.extra IS NULL AS is_null,
                   properties(n) ? 'extra' AS key_present;
```

```
 exists | is_null | key_present
--------+---------+-------------
 f      | t       | t
```

无论设置如何，`REMOVE n.extra` 都会删除键。它仍然是清除属性的方式。

```cypher
RESET allow_null_properties;
DROP GRAPH nulls CASCADE;
SET graph_path = moviekb;
```

## auto_gather_graphmeta {#auto_gather_graphmeta}

```
bool · default off · context superuser
```

作为每次图写入的副作用，保持 `ag_graphmeta` 为最新。

对图中每个（起始标签、边标签、结束标签）三元组，`ag_graphmeta` 记录有多少条边。规划器用它剪除扫描：不可能匹配某个标签的 `MATCH` 完全不会扫描该标签。该设置关闭时，这张表只保持到上一次调用 `regather_graphmeta()` 时的状态。

开启它会立即触发一次完整收集，因此从那一刻起表是正确的：

```sql
SET auto_gather_graphmeta = on;
```

```
NOTICE:  regathering graphmeta...
SET
```

```sql
SELECT g.graphname, se.labname AS start, e.labname AS edge, ee.labname AS "end", m.edgecount
FROM pg_catalog.ag_graphmeta m
JOIN pg_catalog.ag_graph g ON g.oid = m.graph
JOIN pg_catalog.ag_label e  ON e.graphid  = m.graph AND e.labid  = m.edge
JOIN pg_catalog.ag_label se ON se.graphid = m.graph AND se.labid = m.start
JOIN pg_catalog.ag_label ee ON ee.graphid = m.graph AND ee.labid = m."end"
WHERE g.graphname = 'moviekb' ORDER BY 3;
```

```
 graphname | start  |    edge    |  end  | edgecount
-----------+--------+------------+-------+-----------
 moviekb   | person | acted_in   | movie |        25
 moviekb   | person | directed   | movie |        21
 moviekb   | movie  | related_to | movie |        11
```

```cypher
RESET auto_gather_graphmeta;
```

读多写少的图可以开启它，因为准确元数据值得每次写入多做一点工作。写入密集的加载应保持关闭，之后调用 `regather_graphmeta()`。`pg_upgrade` 或恢复之后也必须调用它。[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)介绍这张表及其支持的剪枝。

## cypher_allow_unsafe_ddl {#cypher_allow_unsafe_ddl}

```
bool · default off · context user
```

跳过通常阻止目录不再正确描述图的两项目录检查。它的用途是修复图，而不是在图中工作。

**它允许 `graph_path` 指向不存在的图。**检查从 `SET` 时移到查询时，消息不同：

```sql
SET cypher_allow_unsafe_ddl = on;
SET graph_path = nosuchgraph;
SHOW graph_path;
```

```
 graph_path
-------------
 nosuchgraph
```

```cypher
MATCH (n) RETURN count(n);
```

```
ERROR:  current graph_path "nosuchgraph" is invalid
HINT:  Use SET graph_path
```

```cypher
RESET cypher_allow_unsafe_ddl;
SET graph_path = moviekb;
```

**它允许以错误种类删除标签。**通常，对边标签执行 `DROP VLABEL` 会被拒绝。开启该设置后会成功：

```cypher
CREATE GRAPH unsafe;
SET graph_path = unsafe;
CREATE ELABEL e;
DROP VLABEL e;
```

```
ERROR:  DROP VLABEL cannot DROP edge label
```

```cypher
SET cypher_allow_unsafe_ddl = on;
DROP VLABEL e;
```

```
DROP VLABEL
```

```cypher
RESET cypher_allow_unsafe_ddl;
DROP GRAPH unsafe CASCADE;
SET graph_path = moviekb;
```

二者只在一种情况下有用：目录与表不一致，而你正试图拆解这个图。只为需要它的语句开启，并立即重置。

## eager_mem {#eager_mem}

```
integer · default 4096 · unit kB · context user · minimum 1024
```

一个 eager 计划节点在落盘前可用的内存量。它是 eager 计划的 `work_mem`，并且和 `work_mem` 一样按节点计算，而不是按查询或连接计算。

```sql
SHOW eager_mem;
SET eager_mem = '64MB';
SHOW eager_mem;
```

```
 eager_mem
-----------
 4MB
(1 row)

SET
 eager_mem
-----------
 64MB
(1 row)
```

最小值是 1 MB，小于该值会被拒绝而不是调整到边界：

```sql
SET eager_mem = '512kB';
```

```
ERROR:  512 kB is outside the valid range for parameter "eager_mem" (1024 kB .. 2147483647 kB)
```

```sql
RESET eager_mem;
```

当读取自身写入内容的写查询开始落盘时提高它；见 [`enable_eager`](#enable_eager)。默认 4 MB 与 `work_mem` 一样是保守起点。物化大型中间结果的语句会超过它。

## enable_eager {#enable_eager}

```
bool · default on · context user
```

允许规划器构建 *eager* 计划：先物化写操作的输出，再让后续子句读取它。

有些语句需要这种计划。例如 `CREATE` 后跟一个可能匹配刚创建内容的 `MERGE`。二者不能逐行交错执行，因为第二个子句会看到写了一半的图。所以规划器把第一个子句的结果放入缓冲区。`EXPLAIN` 将该节点标记为 `eager`：

```cypher
CREATE GRAPH eager;
SET graph_path = eager;
CREATE VLABEL src;
CREATE VLABEL dst;
CREATE (:src {n: 1}), (:src {n: 2});
EXPLAIN (COSTS OFF) MATCH (a:src) CREATE (:dst {n: a.n}) MERGE (:dst {n: a.n + 10});
```

```
                                                   QUERY PLAN
----------------------------------------------------------------------------------------------------------------
 Graph Merge
   ->  Nested Loop CypherMerge Join
         Join Filter: ("<0000000000>".properties.'n' = ((_agens_default_s_1.a).properties.'n' `+` '10'::jsonb))
         ->  Subquery Scan on _agens_default_s_1
               ->  Graph Create eager
                     ->  Seq Scan on src a
         ->  Seq Scan on dst "<0000000000>"
```

关闭它不会让这样的语句改用另一种方式运行，而是让它失败：

```cypher
SET enable_eager = off;
MATCH (a:src) CREATE (:dst {n: a.n}) MERGE (:dst {n: a.n + 10});
```

```
ERROR:  eagerness plan is not allowed.
```

```cypher
RESET enable_eager;
DROP GRAPH eager CASCADE;
SET graph_path = moviekb;
```

因此它不像 PostgreSQL 的 `enable_hashjoin` 那样是基于成本的开关。保持开启。只有想确认语句是否依赖 eager 计划时才关闭；在尝试降低大写入成本时这一点有用。

## enable_graph_ddl {#enable_graph_ddl}

```
bool · default off · context user
```

允许 SQL DDL 改变图标签的形状。

标签的列使它成为图标签，图目录描述这些列。`ALTER TABLE` 不会更新该目录。用它重塑标签可能让图继续描述已经不成立的内容。关闭时，这些尝试会被拒绝，并提示能让目录保持同步的语句：

```sql
ALTER TABLE moviekb.movie ADD COLUMN note text;
```

```
ERROR:  cannot add a column to graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

```sql
ALTER TABLE moviekb.movie DROP COLUMN properties;
```

```
ERROR:  cannot drop a column of graph label "movie" with ALTER TABLE
HINT:  Use ALTER VLABEL or ALTER ELABEL instead, which keeps the graph catalog in step.
```

```sql
ALTER TABLE moviekb.movie NO INHERIT moviekb.ag_vertex;
```

```
ERROR:  cannot remove a parent label from graph label "movie" with ALTER TABLE
HINT:  A label's parents are fixed when it is created.
```

被拒绝操作的完整清单是：添加、删除或更改列类型；取消或更改列的生成表达式；删除非空约束（无论按列名还是约束名指定）；添加或移除父标签。同一设置也拒绝重命名标签列以及把标签移到另一个模式。

开启它解除了以上全部限制。它不授予任何权限：能修改标签的人仍然决定其结果。它只是要求重塑是有意的。

有两件事它永远不会解除。`id`、`start`、`end` 或 `properties` 的类型完全不能更改，因为每个顶点和边都由这些列构成：

```sql
SET enable_graph_ddl = on;
ALTER TABLE moviekb.movie ALTER COLUMN properties TYPE text;
```

```
ERROR:  cannot change the type of column "properties" of graph label "movie"
DETAIL:  Every vertex and edge is made of that column.
```

```sql
RESET enable_graph_ddl;
```

重命名或删除表本身仍然被拒绝，并有各自的消息（`cannot rename table "movie"`、`cannot drop table … because vlabel … requires it`）。请使用 `ALTER VLABEL … RENAME TO` 和 `DROP VLABEL`。

无论你是否自己设置，都会遇到这个设置。对带普通列的标签，`pg_dump` 会把 `ALTER TABLE` 语句包在 `SET enable_graph_ddl = on` 中，使恢复可以工作。见[服务端工具](/zh/agensgraph/operations/tools/)。

## enable_graph_dml {#enable_graph_dml}

```
bool · default off · context superuser
```

允许对图标签执行 SQL `INSERT`、`UPDATE`、`DELETE` 和 `MERGE`。

用 SQL 读标签不需要设置。写需要设置，因为 Cypher 写路径会保持图一致：端点存在、id 与标签匹配，以及与它们配套的元数据。关闭时，每个 SQL 写操作都被拒绝：

```psql
INSERT INTO moviekb.movie (properties) VALUES ('{"title": "x"}');
```

```
ERROR:  DML query to graph objects is not allowed
```

```psql
UPDATE moviekb.movie SET properties = '{}';
```

```
ERROR:  DML query to graph objects is not allowed
```

```sql
DELETE FROM moviekb.movie;
```

```
ERROR:  DML query to graph objects is not allowed
```

开启它会放弃“图表示的就是它所说内容”的保证。向边标签 `INSERT` 不检查端点是否存在，因此可以创建悬空边。Cypher 无法产生这样的边：

```psql
CREATE GRAPH dangling;
SET graph_path = dangling;
CREATE VLABEL v;
CREATE ELABEL e;
CREATE (:v {n: 1});
SET enable_graph_dml = on;
INSERT INTO dangling.e (start, "end", properties)
VALUES ('3.1'::graphid, '99.99'::graphid, '{}');
RESET enable_graph_dml;
```

```
INSERT 0 1
```

结果是两个不同查询对同一条边有不同结论。绑定两个端点的模式找不到它，因为与缺失顶点的连接失败：

```cypher
MATCH (a)-[r:e]->(b) RETURN a, r, b;
```

```
 a | r | b
---+---+---
(0 rows)
```

不绑定任何端点的模式会统计到它，因为不需要连接：

```cypher
MATCH ()-[r:e]->() RETURN count(r) AS edges;
```

```
 edges
-------
 1
```

```cypher
DROP GRAPH dangling CASCADE;
SET graph_path = moviekb;
```

为仔细编写的批量加载开启它，或为修复 Cypher 无法访问的行开启，然后再次关闭。它是两个 `superuser` 设置之一。普通角色尝试 `SET enable_graph_dml = on` 会得到 `ERROR:  permission denied to set parameter "enable_graph_dml"`，不能为自己开启。

## enable_graph_endpoint_elision {#enable_graph_endpoint_elision}

```
bool · default on · context user
```

允许规划器删除查询从未使用的模式端点扫描。

`->()` 这样的匿名端点只贡献一个连接。如果端点不带标签和属性过滤，这个连接也不可能删除行。规划器会移除它。当命名端点只用于约束标签时，也会被移除。对边端点 id 的标签测试就是边自身上的 `graphid` 范围检查：

```cypher
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->() RETURN count(r);
```

```
                                       QUERY PLAN
-----------------------------------------------------------------------------------------
 Aggregate
   ->  Seq Scan on acted_in r
         Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
```

没有它，同一查询连接三个关系，并为根本不会查看的端点扫描整个顶点层级：

```cypher
SET enable_graph_endpoint_elision = off;
EXPLAIN (COSTS OFF) MATCH (p:person)-[r:acted_in]->() RETURN count(r);
```

```
                                             QUERY PLAN
-----------------------------------------------------------------------------------------------------
 Aggregate
   ->  Hash Join
         Hash Cond: (r."end" = "<0000000001>".id)
         ->  Hash Join
               Hash Cond: (r.start = p.id)
               ->  Seq Scan on acted_in r
                     Filter: ((start >= '4.0'::graphid) AND (start <= '4.281474976710655'::graphid))
               ->  Hash
                     ->  Seq Scan on person p
         ->  Hash
               ->  Append
                     ->  Seq Scan on ag_vertex "<0000000001>_1"
                     ->  Seq Scan on movie "<0000000001>_2"
                     ->  Seq Scan on person "<0000000001>_3"
```

```sql
RESET enable_graph_endpoint_elision;
```

这是十一个设置中唯一会由 `EXPLAIN (SETTINGS)` 报告的设置，因此从更改过它的会话取出的计划会说明这一点。只为比较计划时关闭。

## enable_multiple_update {#enable_multiple_update}

```
bool · default on · context user
```

决定同一语句多次写入同一元素时保持静默还是发出警告。

模式多次匹配一个元素的语句会按每次匹配写入一次。开启时静默发生。关闭时，服务端为每次重复发出警告。写入仍会发生，因此这是诊断开关而不是限制：

```cypher
CREATE GRAPH repeats;
SET graph_path = repeats;
CREATE VLABEL t;
CREATE (:t {n: 0}), (:t {n: 0});
MATCH (a:t) MATCH (b:t) SET b.n = b.n + 1 RETURN count(b) AS rows;
MATCH (n:t) RETURN n ORDER BY id(n);
```

```
 rows
------
 4
```

```
       n
----------------
 t[3.1]{"n": 1}
 t[3.2]{"n": 1}
```

交叉连接产生四行，每个顶点被到达两次，但 `n` 只增加一。关闭设置后，同一语句会说明这一点：

```cypher
SET enable_multiple_update = off;
MATCH (a:t) MATCH (b:t) SET b.n = b.n + 1 RETURN count(b) AS rows;
```

```
WARNING:  graph element(3,1) has been SET multiple times
WARNING:  graph element(3,2) has been SET multiple times
 rows
------
 4
```

```cypher
RESET enable_multiple_update;
DROP GRAPH repeats CASCADE;
SET graph_path = moviekb;
```

当你想弄清 `SET` 为什么没有按预期工作时关闭它。重复写入通常说明模式匹配到了比预期更多的内容。警告给出标签 id 和本地 id，即元素的 `graphid`。

## enable_property_promotion {#enable_property_promotion}

```
bool · default on · context user
```

决定 Cypher 属性读取在存在提升类型列时是否由该列回答。

属性可以物化为真实类型的真实列；见[把属性提升为列](/zh/agensgraph/querying/typed-columns/)。开启时，`n.key` 读取该列并按列类型返回。关闭时，每次读取都走 `jsonb` 属性包并按 `jsonb` 返回：

```cypher
CREATE GRAPH promoted;
SET graph_path = promoted;
CREATE VLABEL item (score int GENERATED);
CREATE (:item {score: 3}), (:item {score: 20}), (:item {score: 100});
MATCH (n:item) RETURN n.score AS score, pg_typeof(n.score) AS type ORDER BY n.score;
```

```
 score |   type
-------+-----------
     3 | "integer"
    20 | "integer"
   100 | "integer"
```

```cypher
SET enable_property_promotion = off;
MATCH (n:item) RETURN n.score AS score, pg_typeof(n.score) AS type ORDER BY n.score;
```

```
 score |  type
-------+---------
 3     | "jsonb"
 20    | "jsonb"
 100   | "jsonb"
```

> [!WARNING]
> 与只影响成本的规划器开关不同，关闭它可能改变查询**结果**。解析后的 `n.key` 使用类型列的原生语义——数字或排序规则顺序、类型感知比较——而 `jsonb` 回退使用 `jsonb` 的顺序和比较。排序、范围谓词或跨类型比较可能得到不同结果。

```cypher
RESET enable_property_promotion;
DROP GRAPH promoted CASCADE;
SET graph_path = moviekb;
```

保持开启。关闭它只为确认提升列是否改变了查询答案。确认后重新开启，并改为修正查询或列。

## 另见 {#see-also}

- [配置](/zh/agensgraph/operations/configuration/)——设置可以放在哪里，以及对图工作负载重要的 PostgreSQL 设置
- [语法](/zh/agensgraph/reference/syntax/)——`graph_path` 的值遵循的词法规则
- [数据类型](/zh/agensgraph/reference/types/)——`allow_null_properties` 和 `enable_property_promotion` 如何改变属性类型
- [图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)——`auto_gather_graphmeta` 维护的表
- [服务端工具](/zh/agensgraph/operations/tools/)——`pg_dump`、`pg_upgrade` 及其依赖的设置
- [PostgreSQL: server configuration](https://www.postgresql.org/docs/18/runtime-config.html)——其他所有设置
