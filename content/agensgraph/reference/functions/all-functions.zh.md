---
title: 全部函数
linkTitle: 全部函数
description: 本页以一张按字母排序的表格列出参考中的全部函数，共 126 个条目。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/all-functions.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


本页以一张按字母排序的表格列出本参考记载的全部函数，共 126 个条目。即使不知道函数所属类别，也可以按名称查找。**函数**列链接到完整条目，其中包含注意事项和可运行示例。**签名**列显示目录保存的每个重载。

当两个条目同名时，它们是具有两个 OID 和两种含义的两个函数。字符串上的 `length` 不是路径上的 `length`，签名列能区分它们。

| 函数 | 签名 | 说明 | 可用性 |
| --- | --- | --- | --- |
| [`abs`](/zh/agensgraph/reference/functions/numeric/#abs) | <code>abs ( x jsonb ) -&gt; jsonb</code><br><code>abs ( x numeric ) -&gt; numeric</code> | 返回一个数的绝对值。 | 2.17 及更早 |
| [`acos`](/zh/agensgraph/reference/functions/numeric/#acos) | <code>acos ( x jsonb ) -&gt; jsonb</code><br><code>acos ( x double precision ) -&gt; double precision</code> | 以弧度返回 `x` 的反余弦值。 | 2.17 及更早 |
| [`ag_get_graphconstraintdef`](/zh/agensgraph/reference/functions/scalar/#ag_get_graphconstraintdef) | <code>ag_get_graphconstraintdef ( constraint oid ) -&gt; text</code> | 根据其 OID 重建图约束的 `CREATE CONSTRAINT` 命令。 | 2.17 及更早 |
| [`ag_get_propindexdef`](/zh/agensgraph/reference/functions/scalar/#ag_get_propindexdef) | <code>ag_get_propindexdef ( index oid ) -&gt; text</code> | 根据其 OID 重建属性索引的 `CREATE PROPERTY INDEX` 命令。 | 2.17 及更早 |
| [`ag_property_text`](/zh/agensgraph/reference/functions/jsonb/#ag_property_text) | <code>ag_property_text ( properties jsonb, key text, expected_kind "char" ) -&gt; text</code> | 以 `text` 形式返回属性值，但仅当存储的值为所请求的 JSON 类型时。 | 2.18 新增 |
| [`agversion`](/zh/agensgraph/reference/functions/scalar/#agversion) | <code>agversion ( ) -&gt; text</code> | 正在运行的服务器的 AgensGraph 版本。 | 2.17 及更早 |
| [`all`](/zh/agensgraph/reference/functions/predicate/#all) | <code>all ( variable IN list WHERE predicate ) -&gt; boolean</code> | 当谓词对列表中每个元素都成立时返回 true。 | 2.17 及更早 |
| [`allshortestpaths`](/zh/agensgraph/reference/functions/path/#allshortestpaths) | <code>allshortestpaths ( pattern ) -&gt; graphpath</code> | 两个顶点之间的所有最短路径。 | 2.17 及更早 |
| [`any`](/zh/agensgraph/reference/functions/predicate/#any) | <code>any ( variable IN list WHERE predicate ) -&gt; boolean</code> | 当谓词对列表中至少一个元素成立时返回 true。 | 2.17 及更早 |
| [`array_size`](/zh/agensgraph/reference/functions/list/#array_size) | <code>array_size ( list jsonb ) -&gt; integer</code><br><code>array_size ( list json ) -&gt; integer</code><br><code>array_size ( list anyarray ) -&gt; integer</code> | 返回数组中的元素个数。 | 2.17 及更早 |
| [`asin`](/zh/agensgraph/reference/functions/numeric/#asin) | <code>asin ( x jsonb ) -&gt; jsonb</code><br><code>asin ( x double precision ) -&gt; double precision</code> | 以弧度返回 `x` 的反正弦值。 | 2.17 及更早 |
| [`atan`](/zh/agensgraph/reference/functions/numeric/#atan) | <code>atan ( x jsonb ) -&gt; jsonb</code><br><code>atan ( x double precision ) -&gt; double precision</code> | 以弧度返回 `x` 的反正切值。 | 2.17 及更早 |
| [`atan2`](/zh/agensgraph/reference/functions/numeric/#atan2) | <code>atan2 ( y jsonb, x jsonb ) -&gt; jsonb</code><br><code>atan2 ( y double precision, x double precision ) -&gt; double precision</code> | 以弧度返回 `y / x` 的反正切值，使用两个符号确定象限。 | 2.17 及更早 |
| [`avg`](/zh/agensgraph/reference/functions/aggregate/#avg) | <code>avg ( expression numeric ) -&gt; numeric</code> | 返回组中非空值的算术平均值。 | 2.17 及更早 |
| [`cardinality`](/zh/agensgraph/reference/functions/list/#cardinality) | <code>cardinality ( value jsonb ) -&gt; jsonb</code><br><code>cardinality ( p graphpath ) -&gt; jsonb</code> | 返回列表中的元素个数、映射中的条目个数，或路径中的顶点和边个数。 | 2.18 新增 |
| [`ceil`](/zh/agensgraph/reference/functions/numeric/#ceil) | <code>ceil ( x jsonb ) -&gt; jsonb</code><br><code>ceil ( x numeric ) -&gt; numeric</code> | 返回不小于 `x` 的最小整数。 | 2.17 及更早 |
| [`coalesce`](/zh/agensgraph/reference/functions/scalar/#coalesce) | <code>coalesce ( value [, value ] ... ) -&gt; jsonb</code> | 返回第一个非空的参数。 | 2.17 及更早 |
| [`collect`](/zh/agensgraph/reference/functions/aggregate/#collect) | <code>collect ( expression anyelement ) -&gt; jsonb</code><br><code>collect ( v vertex ) -&gt; vertex[]</code><br><code>collect ( e edge ) -&gt; edge[]</code><br><code>collect ( p graphpath ) -&gt; graphpath[]</code> | 将组的值聚合成一个列表；图元素返回原生数组。 | 2.17 及更早 |
| [`cos`](/zh/agensgraph/reference/functions/numeric/#cos) | <code>cos ( x jsonb ) -&gt; jsonb</code><br><code>cos ( x double precision ) -&gt; double precision</code> | 返回以弧度表示的角度的余弦值。 | 2.17 及更早 |
| [`cosd`](/zh/agensgraph/reference/functions/numeric/#cosd) | <code>cosd ( x double precision ) -&gt; double precision</code> | 返回以度数表示的角度的余弦值。 | 2.17 及更早 |
| [`cot`](/zh/agensgraph/reference/functions/numeric/#cot) | <code>cot ( x jsonb ) -&gt; jsonb</code><br><code>cot ( x double precision ) -&gt; double precision</code> | 返回以弧度表示的角度的余切值——正切值的倒数。 | 2.17 及更早 |
| [`count`](/zh/agensgraph/reference/functions/aggregate/#count) | <code>count ( * ) -&gt; bigint</code><br><code>count ( expression ) -&gt; bigint</code> | 统计组中的行数。 | 2.17 及更早 |
| [`cypher_to_jsonb`](/zh/agensgraph/reference/functions/jsonb/#cypher_to_jsonb) | <code>cypher_to_jsonb ( value anyelement ) -&gt; jsonb</code> | 使用 Cypher 规则将值包装为 `jsonb`；拒绝图类型。 | 2.17 及更早 |
| [`datetime`](/zh/agensgraph/reference/functions/scalar/#datetime) | <code>datetime ( ) -&gt; timestamp with time zone</code><br><code>datetime ( timezone "any" ) -&gt; timestamp without time zone</code><br><code>datetime ( year integer, month integer, mday integer, hour integer, min integer, sec integer, millisec integer, nanosec integer, timezone "any" ) -&gt; timestamp without time zone</code> | 当前事务时间戳、命名时区的时间，或由各部分构建的时间戳。 | 2.17 及更早 |
| [`degrees`](/zh/agensgraph/reference/functions/numeric/#degrees) | <code>degrees ( x jsonb ) -&gt; jsonb</code><br><code>degrees ( x double precision ) -&gt; double precision</code> | 将弧度转换为度数。 | 2.17 及更早 |
| [`dijkstra`](/zh/agensgraph/reference/functions/path/#dijkstra) | <code>dijkstra ( pattern, weight ) -&gt; graphpath</code><br><code>dijkstra ( pattern, weight, condition ) -&gt; graphpath</code><br><code>dijkstra ( pattern, weight, LIMIT count ) -&gt; graphpath</code><br><code>dijkstra ( pattern, weight, condition, LIMIT count ) -&gt; graphpath</code> | 查找两个顶点之间的最小代价路径；每条边的代价等于 `weight` 的求值结果。 | 2.17 及更早 |
| [`e`](/zh/agensgraph/reference/functions/numeric/#e) | <code>e ( ) -&gt; numeric</code> | 以 `numeric` 形式返回欧拉数。 | 2.17 及更早 |
| [`edge_to_jsonb`](/zh/agensgraph/reference/functions/jsonb/#edge_to_jsonb) | <code>edge_to_jsonb ( e edge ) -&gt; jsonb</code> | 返回边的属性包。 | 2.17 及更早 |
| [`edges`](/zh/agensgraph/reference/functions/path/#edges) | <code>edges ( p graphpath ) -&gt; edge[]</code> | 按顺序返回路径中的边。 | 2.17 及更早 |
| [`end_id`](/zh/agensgraph/reference/functions/scalar/#end_id) | <code>end_id ( e edge ) -&gt; graphid</code> | 返回边指向的顶点的 `graphid`，而不读取该顶点。 | 2.17 及更早 |
| [`end_vertex`](/zh/agensgraph/reference/functions/path/#end_vertex) | <code>end_vertex ( e edge ) -&gt; vertex</code> | 返回边指向的顶点。 | 2.17 及更早 |
| [`endNode`](/zh/agensgraph/reference/functions/scalar/#endnode) | <code>endNode ( e edge ) -&gt; vertex</code> | 返回边指向的顶点。 | 2.17 及更早 |
| [`exists`](/zh/agensgraph/reference/functions/predicate/#exists) | <code>exists ( pattern ) -&gt; boolean</code><br><code>exists ( property_reference ) -&gt; boolean</code> | 当模式至少匹配一次，或属性存在且非空时返回 true。 | 2.17 及更早 |
| [`exp`](/zh/agensgraph/reference/functions/numeric/#exp) | <code>exp ( x jsonb ) -&gt; jsonb</code><br><code>exp ( x numeric ) -&gt; numeric</code> | 返回 *e* 的 `x` 次幂。 | 2.17 及更早 |
| [`floor`](/zh/agensgraph/reference/functions/numeric/#floor) | <code>floor ( x jsonb ) -&gt; jsonb</code><br><code>floor ( x numeric ) -&gt; numeric</code> | 返回不大于 `x` 的最大整数。 | 2.17 及更早 |
| [`get_last_graph_write_stats`](/zh/agensgraph/reference/functions/scalar/#get_last_graph_write_stats) | <code>get_last_graph_write_stats ( ) -&gt; record</code> | 返回本次会话中最近一次图写操作所更改的内容，以五个计数器表示。 | 2.17 及更早 |
| [`get_time`](/zh/agensgraph/reference/functions/scalar/#get_time) | <code>get_time ( ) -&gt; time without time zone</code><br><code>get_time ( timezone "any" ) -&gt; time without time zone</code> | 返回本地或命名时区的当前时间。 | 2.17 及更早 |
| [`graph_labid`](/zh/agensgraph/reference/functions/scalar/#graph_labid) | <code>graph_labid ( qualified_label cstring ) -&gt; integer</code> | 返回名为 `graph.label` 的标签的标签 id。 | 2.17 及更早 |
| [`graphid`](/zh/agensgraph/reference/functions/scalar/#graphid) | <code>graphid ( labid integer, locid bigint ) -&gt; graphid</code><br><code>graphid ( id numeric ) -&gt; graphid</code> | 根据标签 id 和本地 id，或其打印形式构建 `graphid`。 | 2.17 及更早 |
| [`graphid_in_jsonb_array`](/zh/agensgraph/reference/functions/jsonb/#graphid_in_jsonb_array) | <code>graphid_in_jsonb_array ( id graphid, elements jsonb ) -&gt; boolean</code> | 当 `graphid` 是 `jsonb` 数组中的图元素之一时返回 true。 | 2.17 及更早 |
| [`graphid_labid`](/zh/agensgraph/reference/functions/scalar/#graphid_labid) | <code>graphid_labid ( id graphid ) -&gt; integer</code> | 返回 `graphid` 的标签部分——小数点前的数字。 | 2.17 及更早 |
| [`graphid_locid`](/zh/agensgraph/reference/functions/scalar/#graphid_locid) | <code>graphid_locid ( id graphid ) -&gt; bigint</code> | 返回 `graphid` 的本地部分——小数点后的数字，来自标签的序列。 | 2.17 及更早 |
| [`head`](/zh/agensgraph/reference/functions/list/#head) | <code>head ( list jsonb ) -&gt; jsonb</code><br><code>head ( list anyarray ) -&gt; anyelement</code> | 返回列表的第一个元素。 | 2.17 及更早 |
| [`id`](/zh/agensgraph/reference/functions/scalar/#id) | <code>id ( v vertex ) -&gt; graphid</code><br><code>id ( e edge ) -&gt; graphid</code> | 返回图元素的标识。 | 2.17 及更早 |
| [`isEmpty`](/zh/agensgraph/reference/functions/predicate/#isempty) | <code>isEmpty ( value jsonb ) -&gt; boolean</code> | 当列表无元素或映射无键时返回 true。 | 2.17 及更早 |
| [`jsonb_add`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_add ( a jsonb, b jsonb ) -&gt; jsonb</code> | 实现反引号 `+` 操作符：加法，或两个字符串或两个列表的拼接。 | 2.17 及更早 |
| [`jsonb_array_length`](/zh/agensgraph/reference/functions/jsonb/#jsonb_array_length) | <code>jsonb_array_length ( list jsonb ) -&gt; integer</code> | 以 `integer` 形式返回 `jsonb` 数组中的元素个数。 | 2.17 及更早 |
| [`jsonb_div`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_div ( a jsonb, b jsonb ) -&gt; jsonb</code> | 实现反引号 `/` 操作符。当两个操作数均为整数时执行整数除法。 | 2.17 及更早 |
| [`jsonb_mod`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_mod ( a jsonb, b jsonb ) -&gt; jsonb</code> | 实现反引号 `%` 操作符。 | 2.17 及更早 |
| [`jsonb_mul`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_mul ( a jsonb, b jsonb ) -&gt; jsonb</code> | 实现反引号 `*` 操作符。 | 2.17 及更早 |
| [`jsonb_pow`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_pow ( a jsonb, b jsonb ) -&gt; jsonb</code> | 实现反引号 `^` 操作符。 | 2.17 及更早 |
| [`jsonb_sub`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_sub ( a jsonb, b jsonb ) -&gt; jsonb</code> | 实现反引号二元 `-` 操作符。 | 2.17 及更早 |
| [`jsonb_uminus`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_uminus ( a jsonb ) -&gt; jsonb</code> | 实现反引号前缀 `-` 操作符。 | 2.17 及更早 |
| [`jsonb_uplus`](/zh/agensgraph/reference/functions/jsonb/#arithmetic-operators-on-jsonb) | <code>jsonb_uplus ( a jsonb ) -&gt; jsonb</code> | 实现反引号前缀 `+` 操作符。 | 2.17 及更早 |
| [`keys`](/zh/agensgraph/reference/functions/list/#keys) | <code>keys ( map jsonb ) -&gt; jsonb</code> | 返回映射的键名列表，或图元素属性的键名列表。 | 2.17 及更早 |
| [`label`](/zh/agensgraph/reference/functions/scalar/#label) | <code>label ( v vertex ) -&gt; jsonb</code><br><code>label ( e edge ) -&gt; jsonb</code> | 以 `jsonb` 字符串形式返回图元素创建时所用标签的名称。 | 2.17 及更早 |
| [`labels`](/zh/agensgraph/reference/functions/scalar/#labels) | <code>labels ( v vertex ) -&gt; jsonb</code> | 返回顶点自身的标签及其继承的所有标签，最近的在前。 | 2.17 及更早 |
| [`last`](/zh/agensgraph/reference/functions/list/#last) | <code>last ( list jsonb ) -&gt; jsonb</code><br><code>last ( list anyarray ) -&gt; anyelement</code> | 返回列表的最后一个元素。 | 2.17 及更早 |
| [`left`](/zh/agensgraph/reference/functions/string/#left) | <code>left ( string jsonb, n jsonb ) -&gt; jsonb</code><br><code>left ( string text, n integer ) -&gt; text</code> | 返回字符串的前 `n` 个字符。 | 2.17 及更早 |
| [`length`](/zh/agensgraph/reference/functions/path/#length) | <code>length ( p graphpath ) -&gt; jsonb</code><br><code>length ( vs vertex[] ) -&gt; jsonb</code><br><code>length ( es edge[] ) -&gt; jsonb</code><br><code>length ( ps graphpath[] ) -&gt; jsonb</code> | 路径中的边，或图元素数组中的元素。 | 2.17 及更早 |
| [`length`](/zh/agensgraph/reference/functions/scalar/#length) | <code>length ( value jsonb ) -&gt; jsonb</code> | 字符串中的字符，列表中的元素，或映射中的键。 | 2.17 及更早 |
| [`ln`](/zh/agensgraph/reference/functions/numeric/#ln) | <code>ln ( x double precision ) -&gt; double precision</code><br><code>ln ( x numeric ) -&gt; numeric</code> | 返回 `x` 的自然对数。函数 `log` 在 Cypher 中解析为自然对数。 | 2.17 及更早 |
| [`localdatetime`](/zh/agensgraph/reference/functions/scalar/#localdatetime) | <code>localdatetime ( ) -&gt; timestamp with time zone</code><br><code>localdatetime ( timezone "any" ) -&gt; timestamp without time zone</code> | 返回当前事务时间戳，或命名时区的当前钟面读数。 | 2.17 及更早 |
| [`log`](/zh/agensgraph/reference/functions/numeric/#log) | <code>log ( x jsonb ) -&gt; jsonb</code> | 返回 `x` 的自然对数——非以 10 为底，且无底数参数。 | 2.17 及更早 |
| [`log10`](/zh/agensgraph/reference/functions/numeric/#log10) | <code>log10 ( x double precision ) -&gt; double precision</code><br><code>log10 ( x numeric ) -&gt; numeric</code> | 返回 `x` 的以 10 为底的对数。 | 2.17 及更早 |
| [`lower`](/zh/agensgraph/reference/functions/string/#lower) | <code>lower ( string text ) -&gt; text</code> | 返回小写形式的字符串。 | 2.17 及更早 |
| [`lTrim`](/zh/agensgraph/reference/functions/string/#ltrim) | <code>lTrim ( string jsonb ) -&gt; jsonb</code> | 移除字符串开头的空白字符。 | 2.17 及更早 |
| [`max`](/zh/agensgraph/reference/functions/aggregate/#max) | <code>max ( expression jsonb ) -&gt; jsonb</code><br><code>max ( expression numeric ) -&gt; numeric</code> | 返回组中的最大值。 | 2.17 及更早 |
| [`min`](/zh/agensgraph/reference/functions/aggregate/#min) | <code>min ( expression jsonb ) -&gt; jsonb</code><br><code>min ( expression numeric ) -&gt; numeric</code> | 返回组中的最小值。 | 2.17 及更早 |
| [`nodes`](/zh/agensgraph/reference/functions/path/#nodes) | <code>nodes ( p graphpath ) -&gt; vertex[]</code> | 按顺序返回路径中的顶点。 | 2.17 及更早 |
| [`none`](/zh/agensgraph/reference/functions/predicate/#none) | <code>none ( variable IN list WHERE predicate ) -&gt; boolean</code> | 当谓词对列表中无元素成立时返回 true——即 `any` 的否定。 | 2.17 及更早 |
| [`percentileCont`](/zh/agensgraph/reference/functions/aggregate/#percentilecont) | <code>percentileCont ( list jsonb, percentile numeric ) -&gt; double precision</code> | 返回数值列表的百分位数，通过相邻值插值计算。 | 2.17 及更早 |
| [`percentileDisc`](/zh/agensgraph/reference/functions/aggregate/#percentiledisc) | <code>percentileDisc ( list jsonb, percentile numeric ) -&gt; double precision</code> | 返回数值列表的百分位数，向下取整至列表中的值。 | 2.17 及更早 |
| [`pi`](/zh/agensgraph/reference/functions/numeric/#pi) | <code>pi ( ) -&gt; double precision</code> | 返回 π。 | 2.17 及更早 |
| [`properties`](/zh/agensgraph/reference/functions/scalar/#properties) | <code>properties ( v vertex ) -&gt; jsonb</code><br><code>properties ( e edge ) -&gt; jsonb</code> | 以映射形式返回图元素的完整属性包。 | 2.17 及更早 |
| [`radians`](/zh/agensgraph/reference/functions/numeric/#radians) | <code>radians ( x jsonb ) -&gt; jsonb</code><br><code>radians ( x double precision ) -&gt; double precision</code> | 将度数转换为弧度。 | 2.17 及更早 |
| [`rand`](/zh/agensgraph/reference/functions/numeric/#rand) | <code>rand ( ) -&gt; jsonb</code> | 返回 0 到 1 之间的半开区间内的数。 | 2.17 及更早 |
| [`range`](/zh/agensgraph/reference/functions/list/#range) | <code>range ( start integer, stop integer ) -&gt; jsonb</code><br><code>range ( start integer, stop integer, step integer ) -&gt; jsonb</code> | 返回从 `start` 到 `stop`（包含两端）的整数列表。 | 2.17 及更早 |
| [`regather_graphmeta`](/zh/agensgraph/reference/functions/scalar/#regather_graphmeta) | <code>regather_graphmeta ( ) -&gt; boolean</code> | 清空 `ag_graphmeta` 并通过扫描当前图中的每个边标签重建它。 | 2.17 及更早 |
| [`relationships`](/zh/agensgraph/reference/functions/path/#relationships) | <code>relationships ( p graphpath ) -&gt; edge[]</code> | 按顺序返回路径中的边。 | 2.17 及更早 |
| [`replace`](/zh/agensgraph/reference/functions/string/#replace) | <code>replace ( string jsonb, old jsonb, new jsonb ) -&gt; jsonb</code> | 将一个子字符串的所有出现替换为另一个子字符串。 | 2.17 及更早 |
| [`reverse`](/zh/agensgraph/reference/functions/string/#reverse) | <code>reverse ( string text ) -&gt; text</code><br><code>reverse ( list jsonb ) -&gt; jsonb</code><br><code>reverse ( list anyarray ) -&gt; anyarray</code> | 反转列表，或作为字面量或转换为 `text` 的字符串。 | 2.17 及更早 |
| [`right`](/zh/agensgraph/reference/functions/string/#right) | <code>right ( string jsonb, n jsonb ) -&gt; jsonb</code><br><code>right ( string text, n integer ) -&gt; text</code> | 返回字符串的最后 `n` 个字符。 | 2.17 及更早 |
| [`round`](/zh/agensgraph/reference/functions/numeric/#round) | <code>round ( x jsonb ) -&gt; jsonb</code><br><code>round ( x numeric [, scale integer ] ) -&gt; numeric</code> | 将 `x` 四舍五入到最接近的整数，半值远离零。 | 2.17 及更早 |
| [`rTrim`](/zh/agensgraph/reference/functions/string/#rtrim) | <code>rTrim ( string jsonb ) -&gt; jsonb</code> | 移除字符串末尾的空白字符。 | 2.17 及更早 |
| [`shortestpath`](/zh/agensgraph/reference/functions/path/#shortestpath) | <code>shortestpath ( pattern ) -&gt; graphpath</code> | 通过边数找到两个顶点之间的一条最短路径。 | 2.17 及更早 |
| [`sign`](/zh/agensgraph/reference/functions/numeric/#sign) | <code>sign ( x jsonb ) -&gt; jsonb</code><br><code>sign ( x numeric ) -&gt; numeric</code> | 根据 `x` 的符号返回 −1、0 或 1。 | 2.17 及更早 |
| [`sin`](/zh/agensgraph/reference/functions/numeric/#sin) | <code>sin ( x double precision ) -&gt; double precision</code> | 返回以弧度表示的角度的正弦值。 | 2.17 及更早 |
| [`sind`](/zh/agensgraph/reference/functions/numeric/#sind) | <code>sind ( x double precision ) -&gt; double precision</code> | 返回以度数表示的角度的正弦值。 | 2.17 及更早 |
| [`single`](/zh/agensgraph/reference/functions/predicate/#single) | <code>single ( variable IN list WHERE predicate ) -&gt; boolean</code> | 当谓词对列表中恰好一个元素成立时返回 true。 | 2.17 及更早 |
| [`size`](/zh/agensgraph/reference/functions/scalar/#size) | <code>size ( value ) -&gt; jsonb</code><br><code>size ( pattern ) -&gt; bigint</code> | 返回值的长度，或模式匹配的次数。 | 2.17 及更早 |
| [`split`](/zh/agensgraph/reference/functions/string/#split) | <code>split ( string text, delimiter text ) -&gt; anyarray</code> | 将字符串按分隔符切割成列表。 | 2.17 及更早 |
| [`sqrt`](/zh/agensgraph/reference/functions/numeric/#sqrt) | <code>sqrt ( x jsonb ) -&gt; jsonb</code><br><code>sqrt ( x numeric ) -&gt; numeric</code> | 返回 `x` 的平方根。 | 2.17 及更早 |
| [`start_id`](/zh/agensgraph/reference/functions/scalar/#start_id) | <code>start_id ( e edge ) -&gt; graphid</code> | 返回边离开的顶点的 `graphid`，而不读取该顶点。 | 2.17 及更早 |
| [`start_vertex`](/zh/agensgraph/reference/functions/path/#start_vertex) | <code>start_vertex ( e edge ) -&gt; vertex</code> | 返回边离开的顶点。 | 2.17 及更早 |
| [`startNode`](/zh/agensgraph/reference/functions/scalar/#startnode) | <code>startNode ( e edge ) -&gt; vertex</code> | 返回边离开的顶点。 | 2.17 及更早 |
| [`stdev`](/zh/agensgraph/reference/functions/aggregate/#stdev) | <code>stdev ( expression numeric ) -&gt; numeric</code> | 返回组中值的样本标准差。 | 2.17 及更早 |
| [`stdevp`](/zh/agensgraph/reference/functions/aggregate/#stdevp) | <code>stdevp ( expression numeric ) -&gt; numeric</code> | 返回组中值的总体标准差。 | 2.17 及更早 |
| [`str_size`](/zh/agensgraph/reference/functions/string/#str_size) | <code>str_size ( string text ) -&gt; integer</code> | 以 `integer` 形式返回字符串中的字符个数。 | 2.17 及更早 |
| [`string_contains`](/zh/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_contains ( a jsonb, b jsonb ) -&gt; boolean</code> | 实现 `CONTAINS`。当右字符串在左字符串中任意位置出现时返回 true。 | 2.17 及更早 |
| [`string_ends_with`](/zh/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_ends_with ( a jsonb, b jsonb ) -&gt; boolean</code> | 实现 `ENDS WITH`。当左字符串以右字符串结尾时返回 true。 | 2.17 及更早 |
| [`string_regex`](/zh/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_regex ( a jsonb, b jsonb ) -&gt; boolean</code> | 实现 `=~`。当左字符串与右字符串作为正则表达式匹配时返回 true。 | 2.17 及更早 |
| [`string_starts_with`](/zh/agensgraph/reference/functions/string/#matching-without-a-function) | <code>string_starts_with ( a jsonb, b jsonb ) -&gt; boolean</code> | 实现 `STARTS WITH`。当左字符串以右字符串开头时返回 true。 | 2.17 及更早 |
| [`substring`](/zh/agensgraph/reference/functions/string/#substring) | <code>substring ( string jsonb, start jsonb ) -&gt; jsonb</code><br><code>substring ( string jsonb, start jsonb, count jsonb ) -&gt; jsonb</code> | 返回字符串的一部分，从 `start` 开始，到末尾或持续 `count` 个字符。 | 2.17 及更早 |
| [`sum`](/zh/agensgraph/reference/functions/aggregate/#sum) | <code>sum ( expression numeric ) -&gt; numeric</code> | 返回组中非空值的总和。 | 2.17 及更早 |
| [`tail`](/zh/agensgraph/reference/functions/list/#tail) | <code>tail ( list jsonb ) -&gt; jsonb</code><br><code>tail ( list anyarray ) -&gt; anyarray</code> | 返回列表中除第一个以外的所有元素。 | 2.17 及更早 |
| [`tan`](/zh/agensgraph/reference/functions/numeric/#tan) | <code>tan ( x jsonb ) -&gt; jsonb</code><br><code>tan ( x double precision ) -&gt; double precision</code> | 返回以弧度表示的角度的正切值。 | 2.17 及更早 |
| [`tand`](/zh/agensgraph/reference/functions/numeric/#tand) | <code>tand ( x double precision ) -&gt; double precision</code> | 返回以度数表示的角度的正切值。 | 2.17 及更早 |
| [`to_jsonb`](/zh/agensgraph/reference/functions/jsonb/#to_jsonb) | <code>to_jsonb ( value anyelement ) -&gt; jsonb</code> | 将任意 SQL 值转换为 `jsonb`，复合类型转换为对象。 | 2.17 及更早 |
| [`toBoolean`](/zh/agensgraph/reference/functions/type-conversion/#toboolean) | <code>toBoolean ( value text ) -&gt; boolean</code><br><code>toBoolean ( value "any" ) -&gt; boolean</code> | 返回值所命名的布尔值，若无命名则返回 null。 | 2.17 及更早 |
| [`toBooleanOrNull`](/zh/agensgraph/reference/functions/type-conversion/#tobooleanornull) | <code>toBooleanOrNull ( value text ) -&gt; boolean</code><br><code>toBooleanOrNull ( value "any" ) -&gt; boolean</code> | 返回值所命名的布尔值，或 null。 | 2.17 及更早 |
| [`toFloat`](/zh/agensgraph/reference/functions/type-conversion/#tofloat) | <code>toFloat ( value "any" ) -&gt; double precision</code> | 返回值所命名的浮点数，或 null。 | 2.18 新增 |
| [`toFloatList`](/zh/agensgraph/reference/functions/type-conversion/#tofloatlist) | <code>toFloatList ( list jsonb ) -&gt; jsonb</code><br><code>toFloatList ( list anyarray ) -&gt; double precision[]</code> | 将列表中每个元素转换为浮点数。 | 2.17 及更早 |
| [`toInteger`](/zh/agensgraph/reference/functions/type-conversion/#tointeger) | <code>toInteger ( value "any" ) -&gt; bigint</code> | 返回值所命名的整数，或 null。 | 2.18 新增 |
| [`toIntegerList`](/zh/agensgraph/reference/functions/type-conversion/#tointegerlist) | <code>toIntegerList ( list jsonb ) -&gt; jsonb</code><br><code>toIntegerList ( list anyarray ) -&gt; bigint[]</code> | 将列表中每个元素转换为整数。 | 2.17 及更早 |
| [`toLower`](/zh/agensgraph/reference/functions/string/#tolower) | <code>toLower ( string jsonb ) -&gt; jsonb</code> | 返回小写形式的字符串。 | 2.17 及更早 |
| [`toString`](/zh/agensgraph/reference/functions/type-conversion/#tostring) | <code>toString ( value jsonb ) -&gt; jsonb</code> | 返回值的字符串形式。 | 2.17 及更早 |
| [`toStringList`](/zh/agensgraph/reference/functions/type-conversion/#tostringlist) | <code>toStringList ( list jsonb ) -&gt; jsonb</code><br><code>toStringList ( list anyarray ) -&gt; text[]</code> | 将列表中每个元素转换为字符串。 | 2.17 及更早 |
| [`toStringOrNull`](/zh/agensgraph/reference/functions/type-conversion/#tostringornull) | <code>toStringOrNull ( value "any" ) -&gt; text</code> | 返回值的字符串形式，若值无字符串形式则返回 null。 | 2.17 及更早 |
| [`toUpper`](/zh/agensgraph/reference/functions/string/#toupper) | <code>toUpper ( string jsonb ) -&gt; jsonb</code> | 返回大写形式的字符串。 | 2.17 及更早 |
| [`trim`](/zh/agensgraph/reference/functions/string/#trim) | <code>trim ( string jsonb ) -&gt; jsonb</code> | 移除字符串两端的空白字符。 | 2.17 及更早 |
| [`type`](/zh/agensgraph/reference/functions/scalar/#type) | <code>type ( e edge ) -&gt; jsonb</code> | 以 `jsonb` 字符串返回边标签名；值与 `label(e)` 相同，只是使用 Cypher 对关系类型的命名。 | 2.17 及更早 |
| [`unnest`](/zh/agensgraph/reference/functions/list/#unnest) | <code>unnest ( from_json jsonb ) -&gt; setof jsonb</code> | 将列表展开为每元素一行。 | 2.18 新增 |
| [`upper`](/zh/agensgraph/reference/functions/string/#upper) | <code>upper ( string text ) -&gt; text</code> | 返回大写形式的字符串。 | 2.17 及更早 |
| [`vertex_to_jsonb`](/zh/agensgraph/reference/functions/jsonb/#vertex_to_jsonb) | <code>vertex_to_jsonb ( v vertex ) -&gt; jsonb</code> | 返回顶点的属性包。 | 2.17 及更早 |
| [`vertices`](/zh/agensgraph/reference/functions/path/#vertices) | <code>vertices ( p graphpath ) -&gt; vertex[]</code> | 按顺序返回路径中的顶点。 | 2.17 及更早 |

`collect` 早于 2.18，但原生数组结果是随本版本出现的：即用 `vertex[]`、`edge[]` 和 `graphpath[]` 代替 `jsonb`。`all`、`any`、`none` 和 `single` 背后的三值实现同样如此。[2.18 发布说明](/zh/agensgraph/release-notes/2.18/)包含完整变更列表。

## 在其他位置说明的函数 {#functions-documented-elsewhere}

`meta` 模式为从 SQL 检查图、标签及其大小增加了函数：`meta.labels()`、`meta.count()`、`meta.label_size()` 等。它是扩展而不是核心目录的一部分，因此只有安装后数据库才有这些函数。它们在独立页面[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)中说明，此处不再重复。

PostgreSQL 自身提供的每个函数也都可以从 Cypher 查询调用，但需遵守本参考各页描述的类型规则。这些函数的参考是 [PostgreSQL 文档](https://www.postgresql.org/docs/18/functions.html)。

## 本参考未收录的内容 {#what-this-reference-leaves-out}

AgensGraph 新增函数占据对象标识范围 7000 到 8100。并非所有函数都供直接调用。该范围还包含类型输入/输出函数、B-tree 和 GIN 操作符类的比较与哈希支持，以及聚合 transition 和 final 函数。其中有规划器支持函数、两个 `pg_upgrade` 辅助函数，以及路径查找执行器解析的四个占位条目。本参考记载查询可使用的函数，省略这些内容。

## 列出你自己的构建提供的函数 {#list-what-your-own-build-exposes}

目录是给定服务器拥有哪些函数的权威来源。以下列出该范围内包括聚合在内的每个 AgensGraph 函数：

```sql
SELECT p.proname AS function,
       pg_catalog.pg_get_function_identity_arguments(p.oid) AS arguments,
       pg_catalog.format_type(p.prorettype, NULL) AS returns,
       CASE p.prokind WHEN 'a' THEN 'aggregate' ELSE 'function' END AS kind,
       obj_description(p.oid, 'pg_proc') AS description
FROM pg_catalog.pg_proc p
WHERE p.oid BETWEEN 7000 AND 8100
ORDER BY p.proname, p.oid;
```

在这台 2.18 服务器上返回 195 行。由于上面列出的支持条目，数量多于本参考记载的函数。如果只想计数：

```sql
SELECT count(*) FROM pg_catalog.pg_proc WHERE oid BETWEEN 7000 AND 8100;
```

```
 count
-------
   195
```

AgensGraph 未新增的同名函数不会出现，因为它属于 PostgreSQL。`avg`、`min`、`left` 和 `log10` 都在其中。去掉 `WHERE` 子句并按名称过滤即可查找它们。

## 另见 {#see-also}

- [聚合函数](/zh/agensgraph/reference/functions/aggregate/) — `avg`、`collect`、`count`、`min`、`max`、`sum`
- [谓词函数](/zh/agensgraph/reference/functions/predicate/) — `all`、`any`、`none`、`single`、`exists`、`isEmpty`
- [标量函数](/zh/agensgraph/reference/functions/scalar/) — `id`、`label`、`properties`、`size`、`length`
- [列表函数](/zh/agensgraph/reference/functions/list/) — `head`、`keys`、`range`、`tail`、`unnest`
- [字符串函数](/zh/agensgraph/reference/functions/string/) — `substring`、`split`、`toLower`、`trim`
- [数值函数](/zh/agensgraph/reference/functions/numeric/) — `abs`、`round`、`log`、三角函数族
- [路径函数](/zh/agensgraph/reference/functions/path/) — `nodes`、`relationships`、`shortestpath`、`dijkstra`
- [类型转换函数](/zh/agensgraph/reference/functions/type-conversion/) — `to…` 系列
- [jsonb 操作符与函数](/zh/agensgraph/reference/functions/jsonb/) — 每个属性底层的操作符
- [图元数据](/zh/agensgraph/system-catalogs/graph-metadata/) — `meta.*` 模式
