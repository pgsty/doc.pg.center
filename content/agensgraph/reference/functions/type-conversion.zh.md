---
title: 类型转换函数
linkTitle: 类型转换函数
description: 把值转换为其他类型的函数。
type: docs
weight: 90
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/type-conversion.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


把值转换为其他类型的函数。这里有两类函数。`to…` 函数读取值；当值没有命名目标类型时返回 null。`to…OrNull` 变体做同样的事情，但从不抛出错误。

cast 是另一种转换方式；Cypher 接受 `::` 加大多数类型名：

```cypher
RETURN '42'::int AS i, 42::numeric AS n, 'true'::boolean AS b, '2020-01-01'::date AS d;
```

```
 i  | n  | b |      d
----+----+---+--------------
 42 | 42 | t | "2020-01-01"
```

`::timestamp` 和 `::time` 是例外：

```cypher
RETURN pg_typeof('2020-01-01 10:00'::timestamp);
```

```
ERROR:  syntax error at or near "timestamp"
LINE 1: RETURN pg_typeof('2020-01-01 10:00'::timestamp);
                                             ^
```

Cypher cast 接受普通类型名，并对 numeric、字符、位串、json 和 interval 的拼写有自身规则。它没有日期时间拼写的规则。`TIMESTAMP` 和 `TIME` 是关键字，因此转换到其中任一类型都需要这样的规则，而规则不存在。`date`、`timestamptz` 和 `timetz` 不是关键字，会作为普通类型名到达并可用。`::timestamptz` 是常用的解决方法；另一种方法是把 Cypher 包在 SQL 中。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## toBoolean {#toboolean}

```
toBoolean ( value text ) -> boolean
toBoolean ( value "any" ) -> boolean
```

返回值所命名的布尔值；未命名布尔值时返回 null。

**注意事项**

- 接受任意大小写的 `true`、`false`、`t`、`f`、`on`、`off`、`1` 和 `0`。其他值返回 null，而不是抛出错误。
- 它比 cast 更严格：`toBoolean('yes')` 是 null，而 `'yes'::boolean` 是 true。
- `RETURN` 会让布尔值保持未装箱状态，因此打印为 `t` 或 `f`，null 打印为空白。

```cypher
RETURN toBoolean('TRUE') AS t, toBoolean('false') AS f, toBoolean(true) AS already;
```

```
 t | f | already
---+---+---------
 t | f | t
```

## toBooleanOrNull {#tobooleanornull}

```
toBooleanOrNull ( value text ) -> boolean
toBooleanOrNull ( value "any" ) -> boolean
```

返回值所命名的布尔值，或 null。当 [`toBoolean`](#toboolean) 完全无法读取某个类型并可能抛出错误时，此函数返回 null。

```cypher
RETURN toBooleanOrNull('yes') AS unrecognised, toBooleanOrNull('true') AS recognised;
```

```
 unrecognised | recognised
--------------+------------
              | t
```

## toFloat {#tofloat}

**2.18 新增**

```
toFloat ( value "any" ) -> double precision
```

返回值所命名的浮点数，或 null。

**注意事项**

- 只有一个接收 `"any"` 的重载，因此无需转换即可接受字符串、整数或 `jsonb` 属性。
- 不是数字的值返回 null，而不是抛出错误。
- 结果是 `double precision`。Cypher 的 `RETURN` 会把它装箱为 `jsonb` 数字。

```cypher
RETURN toFloat('3.5') AS from_string, toFloat(7) AS from_integer, toFloat('abc') AS unreadable;
```

```
 from_string | from_integer | unreadable
-------------+--------------+------------
 3.5         | 7            |
```

## toFloatList {#tofloatlist}

```
toFloatList ( list jsonb ) -> jsonb
toFloatList ( list anyarray ) -> double precision[]
```

把列表的每个元素转换为浮点数。

**注意事项**

- **命中的重载决定返回类型。** Cypher 列表是 `jsonb`，所以 `toFloatList([...])` 返回 `jsonb`。只有 PostgreSQL 数组参数才给出 `double precision[]`，并且该形式可从 SQL 调用。
- 不是数字的元素变为 null；列表保持原长度。

```cypher
RETURN toFloatList(['1.4','2.5','true']) AS floats, pg_typeof(toFloatList(['1.4'])) AS type;
```

```
      floats      |  type
------------------+---------
 [1.4, 2.5, null] | "jsonb"
```

```sql
SELECT toFloatList(ARRAY['1.5','2']) AS floats, pg_typeof(toFloatList(ARRAY['1.5','2'])) AS type;
```

```
 floats  |        type
---------+--------------------
 {1.5,2} | double precision[]
```

## toInteger {#tointeger}

**2.18 新增**

```
toInteger ( value "any" ) -> bigint
```

返回值所命名的整数，或 null。

**注意事项**

- 向零截断，而不是舍入：`toInteger(3.7)` 是 3。
- 布尔值会转换，true 变为 1。
- 不是数字的值返回 null，而不是抛出错误。
- 结果是 `bigint`。

```cypher
RETURN toInteger('42') AS from_string, toInteger(3.7) AS truncated,
       toInteger('abc') AS unreadable, toInteger(true) AS from_boolean;
```

```
 from_string | truncated | unreadable | from_boolean
-------------+-----------+------------+--------------
 42          | 3         |            | 1
```

## toIntegerList {#tointegerlist}

```
toIntegerList ( list jsonb ) -> jsonb
toIntegerList ( list anyarray ) -> bigint[]
```

把列表的每个元素转换为整数。命中的重载决定返回类型，规则与 [`toFloatList`](#tofloatlist) 完全相同：Cypher 列表给出 `jsonb`，PostgreSQL 数组给出 `bigint[]`。

```cypher
RETURN toIntegerList(['1','2','x']) AS integers;
```

```
   integers
--------------
 [1, 2, null]
```

## toString {#tostring}

```
toString ( value jsonb ) -> jsonb
```

返回值的字符串形式。

**注意事项**

- 已经是字符串的值原样返回。
- 数字、布尔值、列表和映射都会转换。结果是 `jsonb` 字符串，因此 `RETURN` 打印时会带引号。

```cypher
RETURN toString(11.5) AS number, toString('already a string') AS string, toString(true) AS boolean;
```

```
 number |       string       | boolean
--------+--------------------+---------
 "11.5" | "already a string" | "true"
```

## toStringList {#tostringlist}

```
toStringList ( list jsonb ) -> jsonb
toStringList ( list anyarray ) -> text[]
```

把列表的每个元素转换为字符串。命中的重载决定返回类型，规则与 [`toFloatList`](#tofloatlist) 相同：Cypher 列表给出 `jsonb`，PostgreSQL 数组给出 `text[]`。

```cypher
RETURN toStringList([1, 2.5, true]) AS strings;
```

```
       strings
----------------------
 ["1", "2.5", "true"]
```

## toStringOrNull {#tostringornull}

```
toStringOrNull ( value "any" ) -> text
```

返回值的字符串形式；值没有字符串形式时返回 null。

**注意事项**

- 与 [`toString`](#tostring) 不同，它返回 `text` 而不是 `jsonb`。Cypher 的 `RETURN` 会把它装箱回 `jsonb` 字符串，因此页面上两者看起来相同；SQL 中不同。
- 列表返回 null：列表没有单一字符串形式。

```cypher
RETURN toStringOrNull(11.5) AS number, toStringOrNull([1,2]) AS list,
       pg_typeof(toStringOrNull(1)) AS type;
```

```
 number | list |  type
--------+------+--------
 "11.5" |      | "text"
```

## 不支持的转换 {#what-is-not-converted}

如上所述，Cypher 中不能写 `::timestamp` 和 `::time`。也没有 `toMap`、`toList` 和 `toDate`。用 `{...}` 构建映射，用 `[...]` 构建列表，用 `::date` 读取日期。

图元素只能转换为它的属性包。`v::jsonb` 给出该映射，与 [`properties(v)`](/zh/agensgraph/reference/functions/scalar/#properties) 的值相同。没有从映射转回顶点的转换。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

`toInteger`、`toFloat`、`toString` 和 `toBoolean` 是 openCypher 的名称，行为与 openCypher 描述一致。唯一例外是无法读取的值会返回 null，而不是抛出错误。`…OrNull` 变体和三个列表转换是扩展。

openCypher 的 `toInteger` 会舍入；这里会截断。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [字符串函数](/zh/agensgraph/reference/functions/string/) — `split`、`toLower`、`toUpper`
- [列表函数](/zh/agensgraph/reference/functions/list/) — 这些转换生成的列表
- [jsonb 操作符与函数](/zh/agensgraph/reference/functions/jsonb/) — `to_jsonb` 和 `#>> '{}'` 惯用法
