---
title: 标量函数
linkTitle: 标量函数
description: 接收值并返回单个值的函数。
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/scalar.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


接收值并返回单个值的函数。它们覆盖图元素的组成部分、`graphid` 的各个部分，以及字符串或列表的长度。这里的服务器信息函数报告构建版本和最近一次写入的结果。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## agversion {#agversion}

```
agversion ( ) -> text
```

返回正在运行服务器的 AgensGraph 版本，不包含 `version()` 也会携带的 PostgreSQL 部分。

**注意事项**

- `agversion` 也是只读设置，所以 `SHOW agversion` 返回同一字符串。函数形式可用于表达式内部。
- 该值是本分支自身的版本，不是 PostgreSQL 的。要同时查看两者，请读取 `version()`。

```sql
SELECT agversion();
```

```
 agversion
------------
 2.18.6.1
```

## ag_get_graphconstraintdef {#ag_get_graphconstraintdef}

```
ag_get_graphconstraintdef ( constraint oid ) -> text
```

根据 OID 重建图约束的 `CREATE CONSTRAINT` 命令。它是 `pg_get_constraintdef` 的图对应形式，也是 `pg_dump` 使用的函数。

## ag_get_propindexdef {#ag_get_propindexdef}

```
ag_get_propindexdef ( index oid ) -> text
```

根据 OID 重建属性索引的 `CREATE PROPERTY INDEX` 命令。

**注意事项**

- 属性索引是 `properties` 列上的表达式索引，所以 `pg_get_indexdef` 会把它打印为 SQL。此函数改为打印 Cypher 形式。

## coalesce {#coalesce}

```
coalesce ( value [, value ] ... ) -> jsonb
```

返回第一个不为 null 的参数。

**注意事项**

- 这是表达式形式而不是函数，因此不会出现在函数目录列表中。
- 属性引用总是 `jsonb`。只要任一参数是 `jsonb`，所有参数都会转换为 `jsonb`，结果也是 `jsonb`。否则参数会选定一个共同类型并保留它；因此对两个顶点执行 `coalesce(v1, v2)` 返回 `vertex`。
- 因此，把图元素与其他类型混合会失败，因为元素不能装箱。请改传 `m::jsonb`。
- 第一个非 null 参数之后的参数不会被求值。

```cypher
MATCH (m:movie {title:'Inception'}) RETURN coalesce(m, 0);
```

```
ERROR:  COALESCE types vertex and integer cannot be matched
LINE 1: MATCH (m:movie {title:'Inception'}) RETURN coalesce(m, 0);
                                                               ^
```

```cypher
MATCH (m:movie {title:'Inception'}) RETURN coalesce(m.budget, m.year, 0) AS first_present;
```

```
 first_present
---------------
 2010
```

## datetime {#datetime}

```
datetime ( ) -> timestamp with time zone
datetime ( timezone "any" ) -> timestamp without time zone
datetime ( year integer, month integer, mday integer, hour integer, min integer, sec integer, millisec integer, nanosec integer, timezone "any" ) -> timestamp without time zone
```

返回当前事务时间戳、命名时区的当前时间，或由各部分构建的时间戳。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `year`、`month`、`mday` | `integer` | 日历日期。 |
| `hour`、`min`、`sec` | `integer` | 一天中的时间。 |
| `millisec`、`nanosec` | `integer` | 秒以下部分。超出微秒分辨率的纳秒会被截断。 |
| `timezone` | `"any"` | 时区名或缩写，例如 `'Asia/Seoul'`。 |

**注意事项**

- 无参数形式是 stable 的，因此一个查询的每一行看到同一时刻；不同事务之间会变化。
- 时区形式返回 `timestamp without time zone`：该时区的钟面读数，时区本身被丢弃。
- `RETURN` 会把结果装箱为 ISO 8601 形式的 `jsonb` 字符串。

```sql
SELECT datetime('Asia/Seoul'), datetime(2020, 1, 2, 3, 4, 5, 0, 0, 'UTC');
```

```
          datetime          |      datetime
----------------------------+---------------------
 2026-09-02 16:52:34.625259 | 2020-01-02 03:04:05
```

## endNode {#endnode}

```
endNode ( e edge ) -> vertex
```

返回边指向的顶点。`end_vertex` 是同一个函数的另一个名称；见路径函数页的 [`end_vertex`](/zh/agensgraph/reference/functions/path/#end_vertex)。

## end_id {#end_id}

```
end_id ( e edge ) -> graphid
```

返回边指向顶点的 `graphid`，不读取该顶点。

**注意事项**

- 边表把 `start` 和 `end` 存为列，因此除了边行本身，这个操作没有额外成本；`endNode()` 则必须获取顶点。
- 只要需要比较或分组标识，就应使用它。

```cypher
MATCH ()-[e:acted_in]->() WITH e ORDER BY id(e) LIMIT 1
RETURN start_id(e) AS from_id, end_id(e) AS to_id;
```

```
 from_id | to_id
---------+-------
 4.1     | 3.1
```

## get_last_graph_write_stats {#get_last_graph_write_stats}

```
get_last_graph_write_stats ( ) -> record
```

以一行五个计数器报告本会话最近一次图写入的变化：`insertedvertices`、`insertededges`、`deletedvertices`、`deletededges` 和 `updatedproperties`。

**注意事项**

- 计数器只描述最近一条图写入语句，不是会话总计。
- 不写入任何内容的语句会保留上一条语句的计数器，而不是清零；因此请在关心的写入之后立即读取该行。
- 请从 SQL 调用：它返回 record，而 Cypher 无法展开 record。

```sql
SELECT * FROM get_last_graph_write_stats();
```

```
 insertedvertices | insertededges | deletedvertices | deletededges | updatedproperties
------------------+---------------+-----------------+--------------+-------------------
                1 |             0 |               0 |            0 |                 0
```

## get_time {#get_time}

```
get_time ( ) -> time without time zone
get_time ( timezone "any" ) -> time without time zone
```

返回本地或命名时区的当前时间。

**注意事项**

- 两个形式都标记为 immutable，因此规划器会把调用折叠为常量。查询的每一行，以及预编译语句的每次执行，看到的都是同一时间。需要时间推进时，请从 stable 的 `localdatetime()` 或 SQL 的 `localtime` 读取。

```sql
SELECT get_time(), get_time('Asia/Seoul');
```

```
    get_time    |    get_time
----------------+-----------------
 12:52:34.62488 | 16:52:34.625259
```

## graphid {#graphid}

```
graphid ( labid integer, locid bigint ) -> graphid
graphid ( id numeric ) -> graphid
```

由标签 id 和本地 id 构建 `graphid`，或由 `graphid` 打印出的 `labid.locid` 数字构建。

**注意事项**

- 标签的 `id` 列默认值就是这样写的；参见[图如何映射到 PostgreSQL](/zh/agensgraph/concepts/graph-on-postgresql/)。
- numeric 形式是为了手写 SQL 方便。它不检查标签是否存在。

```sql
SELECT graphid(4, 1), graphid(4.1::numeric);
```

```
 graphid | graphid
---------+---------
 4.1     | 4.1
```

## graph_labid {#graph_labid}

```
graph_labid ( qualified_label cstring ) -> integer
```

返回以 `graph.label` 形式命名的标签的标签 id。

```sql
SELECT graph_labid('moviekb.person');
```

```
 graph_labid
-------------
           4
```

## graphid_labid {#graphid_labid}

```
graphid_labid ( id graphid ) -> integer
```

返回 `graphid` 的标签部分：点号前的数字。

**注意事项**

- `graphid` 把标签 id 打包在高 16 位，其余位保存本地 id。因此整个标签占据一段连续的 `graphid` 范围；标签测试可以用索引范围扫描回答，无需访问目录。

## graphid_locid {#graphid_locid}

```
graphid_locid ( id graphid ) -> bigint
```

返回 `graphid` 的本地部分：点号后的数字，取自标签的序列。

```cypher
MATCH (n:person {name:'Keanu Reeves'})
RETURN id(n) AS id, graphid_labid(id(n)) AS label_id, graphid_locid(id(n)) AS local_id;
```

```
 id  | label_id | local_id
-----+----------+----------
 4.1 | 4        | 1
```

## id {#id}

```
id ( v vertex ) -> graphid
id ( e edge ) -> graphid
```

返回图元素的标识。

**注意事项**

- 这不是目录函数。`vertex` 是复合类型 `(id, properties)`，`edge` 是 `(id, start, end, properties)`。因此 `id(v)` 是 PostgreSQL 对字段选择的功能表示法（`parse_func.c:1961`）。同一机制也提供 `properties(v)`。
- `n.id` **不是**同一个东西。它读取名为 `id` 的*属性*；示例数据集没有这个属性，所以返回 null。请写 `id(n)`。
- `RETURN` 让结果保持为 `graphid`，不装箱为 `jsonb`。聚合会装箱：`min(id(n))` 返回 `jsonb` 字符串 `"4.1"`。

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN id(n) AS identity, n.id AS property_named_id;
```

```
 identity | property_named_id
----------+-------------------
 4.1      |
```

## label {#label}

```
label ( v vertex ) -> jsonb
label ( e edge ) -> jsonb
```

以 `jsonb` 字符串返回图元素创建时使用的标签名。

**注意事项**

- `label` 和 [`labels`](#labels) 是不同函数，不是同一个函数的两种拼写。`label` 返回一个字符串，即元素自身标签。`labels` 返回一个列表，包含该标签及其继承的标签。
- `label` 既作用于顶点，也作用于边；`labels` 只作用于顶点。对边而言，`label(e)` 与 [`type(e)`](#type) 是同一个调用。

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN label(n) AS own, labels(n) AS own_and_inherited;
```

```
   own    | own_and_inherited
----------+-------------------
 "person" | ["person"]
```

两个答案只有在标签发生继承时才会不同。添加带父标签的标签：

```cypher
CREATE VLABEL creature;
CREATE VLABEL dragon INHERITS (creature);
CREATE (:dragon {name: 'Smaug'});
```

```cypher
MATCH (d:dragon) RETURN label(d) AS own, labels(d) AS own_and_inherited;
```

```
   own    |   own_and_inherited
----------+------------------------
 "dragon" | ["dragon", "creature"]
```

然后把它清理掉：

```cypher
MATCH (d:dragon) DETACH DELETE d;
DROP VLABEL dragon;
DROP VLABEL creature;
```

边没有 `labels()`：

```cypher
MATCH ()-[e:acted_in]->() WITH e LIMIT 1 RETURN labels(e);
```

```
ERROR:  function labels(edge) does not exist
LINE 1: MATCH ()-[e:acted_in]->() WITH e LIMIT 1 RETURN labels(e);
                                                        ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

## labels {#labels}

```
labels ( v vertex ) -> jsonb
```

返回一个列表，包含顶点自身标签及其继承的每个标签，最近的在前。

**注意事项**

- 仅适用于顶点。没有 `labels(edge)`。
- 无父标签时列表只有一个元素，这是常见情况。

## length {#length}

```
length ( value jsonb ) -> jsonb
```

返回字符串的字符数、列表的元素数或映射的键数。

**注意事项**

- [`size`](#size) 是此函数的 Cypher 拼写；解析器会改写它，因此结果列名为 `length`。
- 对路径或图元素数组，`length` 是含义不同的另一个函数：路径中的边数。见路径函数页的 [`length`](/zh/agensgraph/reference/functions/path/#length)。
- 数字返回其文本形式的长度，而不是抛出错误。

```cypher
RETURN length('The Matrix') AS characters, length([1,2,3]) AS elements, length({a:1,b:2}) AS keys;
```

```
 characters | elements | keys
------------+----------+------
 10         | 3        | 2
```

## localdatetime {#localdatetime}

```
localdatetime ( ) -> timestamp with time zone
localdatetime ( timezone "any" ) -> timestamp without time zone
```

返回当前事务时间戳，或命名时区的当前钟面读数。

**注意事项**

- 无参数形式返回与 `datetime()` 相同的值，包括相同类型。这两个名称为了 GQL 兼容而存在；两者都不会丢弃时区。
- 时区形式与 `datetime(zone)` 一样，返回 `timestamp without time zone`。
- 两个形式都是 stable 的，因此从它们取得的值会在事务之间推进；这不同于 [`get_time`](#get_time)。

## properties {#properties}

```
properties ( v vertex ) -> jsonb
properties ( e edge ) -> jsonb
```

以映射返回图元素的整个属性包。

**注意事项**

- 与 [`id`](#id) 一样，这是复合类型上的字段选择，不是目录函数，因此成本不会高于读取列。
- `vertex_to_jsonb` 和 `edge_to_jsonb` 返回同一映射，并且是 cast `v::jsonb` 使用的函数。
- 读取属性包会完整 detoast。如果只需要一个键，请只读取那个键。

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN properties(n) AS bag;
```

```
                  bag
----------------------------------------
 {"born": 1964, "name": "Keanu Reeves"}
```

## regather_graphmeta {#regather_graphmeta}

```
regather_graphmeta ( ) -> boolean
```

清空 `ag_graphmeta`，并扫描当前图中每个边标签来重建它。`ag_graphmeta` 记录出现过的标签三元组以及每个三元组由多少边构成；规划器用它跳过模式不可能匹配的标签表。

**注意事项**

- 扫描会读取图中每条边，因此成本随图规模增长。
- `auto_gather_graphmeta` 会在写入发生时保持表最新。关闭该设置完成批量加载后，请手动重建。
- 发出 `NOTICE: regathering graphmeta...` 并返回 true。

```sql
SELECT regather_graphmeta();
```

```
NOTICE:  regathering graphmeta...
 regather_graphmeta
--------------------
 t
```

## size {#size}

```
size ( value ) -> jsonb
size ( pattern ) -> bigint
```

对值返回其长度。对模式返回模式匹配的次数。

**注意事项**

- 两个形式通过起始字符区分。模式总以 `(` 开始，因此不能这样开始的输入会作为值读取。值形式会变成 [`length`](#length)，所以结果列名为 `length`。模式形式会变成计数子查询，因此列名为 `count`。
- `shortestpath` 或 `allshortestpaths` 参数保持既有含义，即找到的路径数，不会被解释为模式。

```cypher
MATCH (a:person {name:'Keanu Reeves'}) RETURN size((a)-[]->()) AS edges, size(a.name) AS name_length;
```

```
 edges | name_length
-------+-------------
 4     | 12
```

## startNode {#startnode}

```
startNode ( e edge ) -> vertex
```

返回边离开的顶点。`start_vertex` 是同一个函数的另一个名称；见路径函数页的 [`start_vertex`](/zh/agensgraph/reference/functions/path/#start_vertex)。

## start_id {#start_id}

```
start_id ( e edge ) -> graphid
```

返回边离开顶点的 `graphid`，不读取该顶点。[`end_id`](#end_id) 的注意事项同样适用。

## type {#type}

```
type ( e edge ) -> jsonb
```

以 `jsonb` 字符串返回边标签的名称。它与 `label(e)` 的值相同，只是采用了 Cypher 对关系类型的命名。

**注意事项**

- 仅适用于边。对顶点会被拒绝；请使用 [`label`](#label)。

```cypher
MATCH (m:movie {title:'Inception'}) RETURN type(m);
```

```
ERROR:  function type(vertex) does not exist
LINE 1: MATCH (m:movie {title:'Inception'}) RETURN type(m);
                                                   ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

```cypher
MATCH ()-[e:acted_in]->() WITH e LIMIT 1 RETURN type(e) AS relationship_type;
```

```
 relationship_type
-------------------
 "acted_in"
```

## 兼容性 {#compatibility}

### openCypher {#opencypher}

`id()` 返回 `graphid`，即标签 id 加序列号，而不是 openCypher 返回的整数。它在元素生命周期内稳定，且在整个图中唯一。但它不是小而密集的整数，对它做算术也没有意义。

openCypher 的 `labels()` 返回节点携带的每个标签，因为那里的节点可以携带多个标签。这里的顶点恰好有一个标签；`labels()` 返回该标签及其继承的标签。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [路径函数](/zh/agensgraph/reference/functions/path/) — `nodes`、`relationships`、路径上的 `length`
- [jsonb 操作符与函数](/zh/agensgraph/reference/functions/jsonb/) — 读取 `properties()` 返回的映射
- [图元数据函数](/zh/agensgraph/system-catalogs/graph-metadata/) — `meta.*` 模式
