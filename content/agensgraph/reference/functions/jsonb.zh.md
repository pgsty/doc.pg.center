---
title: jsonb 操作符与函数
linkTitle: jsonb 操作符与函数
description: 属性就是 jsonb。
type: docs
weight: 100
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/jsonb.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


属性**就是** `jsonb`。顶点是复合类型 `(id graphid, properties jsonb)`，边另加 `start` 和 `end`。因此你在 Cypher 中读到的每个属性，以及在 SQL 中访问的每个属性列，都是 PostgreSQL `jsonb` 类型的值。在阅读本页其他内容前，先理解这一点带来的两个结果：字符串属性会带引号返回；整个 `jsonb` 操作符集都适用于它。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## 属性访问操作符 {#property-access-operators}

这四个操作符左侧接收 `jsonb` 值。双箭头的两个返回 `text`；单箭头的两个返回 `jsonb`。

| 操作符 | 右操作数 | 返回 | 结果 |
| --- | --- | --- | --- |
| `->` | `text` 键或 `integer` 下标 | `jsonb` | 该键或下标处的值 |
| `->>` | `text` 键或 `integer` 下标 | `text` | 同一个值；字符串不带引号 |
| `#>` | `text[]` 路径 | `jsonb` | 该路径处的值 |
| `#>>` | `text[]` 路径 | `text` | 同一个值；字符串不带引号 |

```sql
SELECT properties -> 'name' AS quoted, properties ->> 'name' AS plain
FROM moviekb.person ORDER BY id LIMIT 1;
```

```
     quoted     |    plain
----------------+--------------
 "Keanu Reeves" | Keanu Reeves
```

```psql
SELECT '{"a":{"b":[1,2]}}'::jsonb #> '{a,b}' AS at_path,
       '{"a":{"b":[1,2]}}'::jsonb #>> '{a,b,0}' AS at_path_text;
```

```
 at_path | at_path_text
---------+--------------
 [1, 2]  | 1
```

## 取出未加引号的标量 {#getting-an-unquoted-scalar-out}

Cypher 的 `RETURN` 会把标量输出列装箱为 `jsonb`。因此 `RETURN m.title` 打印 `"Inception"`，包含引号；`RETURN m.title::text` 也一样。引号是 JSON 的一部分，不是 `psql` 的显示痕迹。

解决方法是 `#>> '{}'`：空路径选中整个文档，`#>>` 以 `text` 返回它。把 Cypher 包在 SQL 中，并在那里应用该操作符：

```cypher
SELECT t AS boxed, t #>> '{}' AS unboxed
FROM (MATCH (m:movie {title:'Inception'}) RETURN m.title AS t) q;
```

```
    boxed    |  unboxed
-------------+-----------
 "Inception" | Inception
```

凡是 Cypher 结果必须与普通 `text` 连接或比较的场合，都可以使用这个惯用法。连接到关系表就是其中一种情况。

## 包含与存在操作符 {#containment-and-existence-operators}

| 操作符 | 右操作数 | 返回 true 的条件 |
| --- | --- | --- |
| `@>` | `jsonb` | 左文档包含右文档 |
| `<@` | `jsonb` | 左文档被右文档包含 |
| `?` | `text` | 该键或字符串元素存在 |
| `?\|` | `text[]` | 任一键存在 |
| `?&` | `text[]` | 所有键都存在 |

```psql
SELECT properties @> '{"name":"Keanu Reeves"}' AS contains,
       properties ? 'born' AS has_born,
       properties ?& ARRAY['name','born'] AS has_both
FROM moviekb.person ORDER BY id LIMIT 1;
```

```
 contains | has_born | has_both
----------+----------+----------
 t        | t        | t
```

属性索引不能服务其中任何一个操作符；每个都是对整个属性包的包含测试，而不是对单个键的比较。`properties` 上的 GIN 索引可以。

## 修改操作符 {#modification-operators}

| 操作符 | 右操作数 | 结果 |
| --- | --- | --- |
| `\|\|` | `jsonb` | 两个文档合并；共享键取右侧的值 |
| `-` | `text` 键或 `integer` 下标 | 去掉该键或元素的文档 |
| `#-` | `text[]` 路径 | 去掉该路径处值的文档 |

```psql
SELECT '{"a":1}'::jsonb || '{"b":2}'::jsonb AS merged,
       '{"a":1,"b":2}'::jsonb - 'a' AS without_a,
       '{"a":{"b":1}}'::jsonb #- '{a,b}' AS without_path;
```

```
      merged      | without_a | without_path
------------------+-----------+--------------
 {"a": 1, "b": 2} | {"b": 2}  | {"a": {}}
```

在 Cypher 中，这些操作改由子句表达：`SET n += {city:'Seoul'}` 合并，`REMOVE n.city` 删除键。

## jsonb 算术操作符 {#arithmetic-operators-on-jsonb}

PostgreSQL 已经赋予 `-` 和 `||` 在 `jsonb` 上的含义，所以 AgensGraph 不能把它们复用于算术。它新增了八个名称包在反引号中的操作符。当你在属性上写 `+`、`-`、`*`、`/`、`%` 或 `^` 时，Cypher 解析器会生成这些操作符。

| 操作符 | 实现者 | OID | 含义 |
| --- | --- | --- | --- |
| ``` `+` ``` | `jsonb_add` | 7176 | 加法；两个字符串或两个列表时为拼接 |
| ``` `-` ``` | `jsonb_sub` | 7178 | 减法 |
| ``` `*` ``` | `jsonb_mul` | 7180 | 乘法 |
| ``` `/` ``` | `jsonb_div` | 7182 | 除法；两个操作数都是整数时为整数除法 |
| ``` `%` ``` | `jsonb_mod` | 7184 | 取模 |
| ``` `^` ``` | `jsonb_pow` | 7186 | 幂运算 |
| ``` `+` ```（前缀） | `jsonb_uplus` | 7190 | 一元加 |
| ``` `-` ```（前缀） | `jsonb_uminus` | 7191 | 一元减 |

反引号在这个分支的词法分析器（`scan.l:369`）中是操作符字符，因此这些名称在 SQL 中也可以输入。两个操作数都必须是 `jsonb`：

```sql
SELECT '"a"'::jsonb `+` '"b"'::jsonb AS strings, '[1]'::jsonb `+` '[2]'::jsonb AS lists;
```

```
 strings | lists
---------+--------
 "ab"    | [1, 2]
```

> [!NOTE]
> Cypher 算术请使用普通操作符，例如 `n.a + n.b`，让解析器选择这些操作符。这里列出反引号名称，是为了让你能在 `EXPLAIN` 计划、错误消息或 `pg_operator` 列表中识别它们。实现函数也可以直接调用：`jsonb_add('1'::jsonb, '2'::jsonb)` 返回 3。

## ag_property_text {#ag_property_text}

**2.18 新增**

```
ag_property_text ( properties jsonb, key text, expected_kind "char" ) -> text
```

以 `text` 返回属性值，但仅在存储值属于所要求的 JSON 种类时。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `properties` | `jsonb` | 要读取的属性包。 |
| `key` | `text` | 属性名。 |
| `expected_kind` | `"char"` | 数字为 `'n'`，字符串为 `'s'`，布尔值为 `'b'`。 |

**注意事项**

- 它支撑带类型列的属性提升。`->>` 返回值的文本，而文本不携带种类，所以通过它无法区分字符串 `"5"` 和数字 `5`。整数列会为保存字符串的属性返回 5。此函数先询问种类。
- 种类不匹配会**抛出错误**，不会返回 null：`property "n" holds a number`，详细信息为 `A column promoting this property holds strings.`
- 属性不存在，或存在但为 JSON null 时，返回 null。
- 它不适合手写。在 Cypher 中用 `n.key` 读属性，在 SQL 中用 `properties ->> 'key'`。

```psql
SELECT ag_property_text('{"name":"x","n":5}'::jsonb, 'n', 'n') AS number,
       ag_property_text('{"name":"x"}'::jsonb, 'missing', 's') AS absent;
```

```
 number | absent
--------+--------
 5      |
```

## cypher_to_jsonb {#cypher_to_jsonb}

```
cypher_to_jsonb ( value anyelement ) -> jsonb
```

按 Cypher 的规则把值装箱为 `jsonb`；这些规则在字符串类型上与 `to_jsonb` 不同。

**注意事项**

- 这是 Cypher 的 `RETURN` 在标量输出列外插入的函数。它会出现在计划中发生装箱的位置。
- 它是 strict 的，因此 null 保持为 null。
- 解析器拒绝把图元素包在其中。这个拒绝会让 `coalesce(m, 0)` 和顶点的 `jsonb` 列表失败。限制位于解析器的 `coerce_to_jsonb()`，不在函数中。对 `vertex` 按名称调用时，函数返回整个复合值，包括 `id` 和 `tid`；这*不是* `v::jsonb` 给出的属性包。要取属性包，请使用 [`vertex_to_jsonb`](#vertex_to_jsonb) 或 cast。

```sql
SELECT cypher_to_jsonb('abc'::text) AS from_text, cypher_to_jsonb(42) AS from_integer;
```

```
 from_text | from_integer
-----------+--------------
 "abc"     | 42
```

## edge_to_jsonb {#edge_to_jsonb}

```
edge_to_jsonb ( e edge ) -> jsonb
```

返回边的属性包。这是 cast `e::jsonb` 使用的函数，返回值与 [`properties(e)`](/zh/agensgraph/reference/functions/scalar/#properties) 相同。

**注意事项**

- 不包含端点，只包含属性。请用 [`start_id`](/zh/agensgraph/reference/functions/scalar/#start_id) 和 [`end_id`](/zh/agensgraph/reference/functions/scalar/#end_id) 读取端点。

```cypher
MATCH ()-[e:related_to]->() WITH e LIMIT 1 RETURN edge_to_jsonb(e) AS bag;
```

```
      bag
---------------
 {"weight": 1}
```

## graphid_in_jsonb_array {#graphid_in_jsonb_array}

```
graphid_in_jsonb_array ( id graphid, elements jsonb ) -> boolean
```

当某个 `graphid` 是 `jsonb` 数组中的图元素之一时，返回 true。

**注意事项**

- 解析器为 `id(n) IN [...]` 生成此函数，使元素列表无需逐个解包即可测试。`graphid` 装箱为 `jsonb` 字符串，此函数与该形式比较。
- 手写时，它就是普通的成员测试。

```sql
SELECT graphid_in_jsonb_array('4.1'::graphid, '["4.1","4.2"]'::jsonb) AS present;
```

```
 present
---------
 t
```

## jsonb_array_length {#jsonb_array_length}

```
jsonb_array_length ( list jsonb ) -> integer
```

以 `integer` 返回 `jsonb` 数组中的元素数量。

**注意事项**

- PostgreSQL 自身的函数。[`cardinality`](/zh/agensgraph/reference/functions/list/#cardinality) 和 [`length`](/zh/agensgraph/reference/functions/scalar/#length) 是 Cypher 拼写，返回 `jsonb`；此函数返回原生 `integer`，并且对非数组值抛出错误。

```sql
SELECT jsonb_array_length('[1,2,3]');
```

```
 jsonb_array_length
--------------------
                  3
```

## to_jsonb {#to_jsonb}

```
to_jsonb ( value anyelement ) -> jsonb
```

把任意 SQL 值转换为 `jsonb`；复合类型映射为对象，数组映射为数组。

**注意事项**

- 这是把关系行放入图的方法。`LOAD FROM t AS r CREATE (:label = to_jsonb(row_to_json(r)))` 会把每一行变成属性包。
- 对图元素，它转换整个复合值，而不是属性包。`v::jsonb` 和 [`vertex_to_jsonb`](#vertex_to_jsonb) 给出属性包。

```sql
SELECT to_jsonb(42) AS number, to_jsonb('x'::text) AS string;
```

```
 number | string
--------+--------
 42     | "x"
```

## vertex_to_jsonb {#vertex_to_jsonb}

```
vertex_to_jsonb ( v vertex ) -> jsonb
```

返回顶点的属性包。这是 cast `v::jsonb` 使用的函数，返回值与 [`properties(v)`](/zh/agensgraph/reference/functions/scalar/#properties) 相同。

```cypher
MATCH (n:person {name:'Keanu Reeves'}) RETURN vertex_to_jsonb(n) AS bag;
```

```
                  bag
----------------------------------------
 {"born": 1964, "name": "Keanu Reeves"}
```

## 顺序与比较 {#ordering-and-comparison}

`jsonb` 有自身的全序，且不同于这些值按自身类型排序的顺序。种类优先：先是 null，然后是字符串、数字、布尔值、数组、对象。只有同类值才按值比较：

```psql
SELECT v FROM (VALUES ('1'::jsonb),('"a"'),('true'),('null'),('[1]'),('{"k":1}')) t(v) ORDER BY v;
```

```
    v
----------
 null
 "a"
 1
 true
 [1]
 {"k": 1}
```

凡是 Cypher 结果排序或聚合的地方，这一点都有影响。`jsonb` 列上的 `min()` 和 `max()` 遵循该顺序；因此当属性在某些行是数字、另一些行是字符串时，排序不会符合读者预期。如果顺序必须符合类型自身，请通过带类型列读取，或转换类型。

两个整数相除也会得到整数，因为 `jsonb` 保留这个区别：

```cypher
RETURN 7 / 2 AS integer_division, 7.0 / 2 AS real_division;
```

```
 integer_division |   real_division
------------------+--------------------
 3                | 3.5000000000000000
```

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [标量函数](/zh/agensgraph/reference/functions/scalar/) — `properties`、`keys`、`length`
- [类型转换函数](/zh/agensgraph/reference/functions/type-conversion/) — `to…` 系列
- [组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/) — `#>> '{}'` 发挥作用的地方
