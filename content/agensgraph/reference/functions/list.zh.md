---
title: 列表函数
linkTitle: 列表函数
description: 作用于列表和映射的函数。
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/list.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


作用于列表和映射的函数。Cypher 列表是 `jsonb` 数组，因此这些函数接收并返回 `jsonb`。但对图元素执行 `collect()` 会产生原生数组；带数组重载的函数可同时作用于两者。

Cypher 列表下标从 0 开始；切片 `list[a..b]` 不包含上界。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## array_size {#array_size}

```
array_size ( list jsonb ) -> integer
array_size ( list json ) -> integer
array_size ( list anyarray ) -> integer
```

返回数组中的元素数量。

**注意事项**

- 仅适用于数组。与 [`cardinality`](#cardinality) 不同，它不统计映射的键。
- 三个重载让同一个名称可作用于 Cypher 列表、`json` 值和 PostgreSQL 数组。

```cypher
RETURN array_size([1,2,3]) AS n;
```

```
 n
---
 3
```

## cardinality {#cardinality}

**2.18 新增**

```
cardinality ( value jsonb ) -> jsonb
cardinality ( p graphpath ) -> jsonb
```

返回列表中的元素数、映射中的条目数，或路径中的顶点数和边数。

**注意事项**

- 字符串会被拒绝。字符串请使用 [`length`](/zh/agensgraph/reference/functions/scalar/#length)。

```cypher
RETURN cardinality('abc');
```

```
ERROR:  cardinality(): list or map is expected but "abc"
```
- 对路径执行时统计顶点*和*边，因此一条边的路径结果为 3；对同一路径执行 [`length`](/zh/agensgraph/reference/functions/path/#length) 的结果为 1。
- PostgreSQL 自身的 `cardinality(anyarray)` 仍适用于原生数组，并返回 `integer` 而不是 `jsonb`。

```cypher
RETURN cardinality([1,2,3]) AS list, cardinality({a:1,b:2}) AS map;
```

```
 list | map
------+-----
 3    | 2
```

```cypher
MATCH p=(:person {name:'Christopher Nolan'})-[:directed]->(:movie {title:'Inception'})
RETURN cardinality(p) AS elements;
```

```
 elements
----------
 3
```

## head {#head}

```
head ( list jsonb ) -> jsonb
head ( list anyarray ) -> anyelement
```

返回列表的第一个元素。

**注意事项**

- 空列表返回 null，而不是抛出错误。
- 数组重载返回元素自身的类型，因此对顶点执行 `head(collect(n))` 返回 `vertex`。

```cypher
RETURN head([10,20,30]) AS first, last([10,20,30]) AS final, tail([10,20,30]) AS rest;
```

```
 first | final |   rest
-------+-------+----------
 10    | 30    | [20, 30]
```

## keys {#keys}

```
keys ( map jsonb ) -> jsonb
```

返回映射或图元素属性的键名列表。

**注意事项**

- 顺序是 `jsonb` 自身的键顺序：先按键长，再按字节顺序。它既不是插入顺序，也不是字母顺序。如需固定顺序，请对结果排序。
- 接受顶点或边参数，因为它会被转换为其属性映射。

```cypher
MATCH (p:person {name:'Keanu Reeves'}) RETURN keys(p) AS property_names;
```

```
  property_names
------------------
 ["born", "name"]
```

```cypher
RETURN keys({title:'Inception', year:2010}) AS map_keys;
```

```
     map_keys
-------------------
 ["year", "title"]
```

## last {#last}

```
last ( list jsonb ) -> jsonb
last ( list anyarray ) -> anyelement
```

返回列表的最后一个元素。空列表返回 null。示例见 [`head`](#head)。

## range {#range}

```
range ( start integer, stop integer ) -> jsonb
range ( start integer, stop integer, step integer ) -> jsonb
```

返回从 `start` 到 `stop` 的整数列表，两端都包含在内。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `start` | `integer` | 列表中的第一个值。 |
| `stop` | `integer` | 列表可能到达的最后一个值。步长正好落在该值上时才包含它。 |
| `step` | `integer` | 步长。省略时向上计数为 1，向下计数为 −1。 |

**注意事项**

- 结果是 `jsonb`，不是 PostgreSQL 数组，因此可以像任何 Cypher 列表一样下标访问和迭代。
- 两端都包含。只有当步长正好落在 `stop` 上时，`stop` 才出现在列表中：`range(1,10,3)` 在 10 结束，而 `range(1,9,3)` 在 7 结束。
- `stop` 小于 `start` 时向下计数，不需要负步长。

```cypher
RETURN range(1,5) AS up, range(1,10,3) AS step, range(5,1) AS down, range(5,1,-2) AS down_step;
```

```
       up        |     step      |      down       | down_step
-----------------+---------------+-----------------+-----------
 [1, 2, 3, 4, 5] | [1, 4, 7, 10] | [5, 4, 3, 2, 1] | [5, 3, 1]
```

## tail {#tail}

```
tail ( list jsonb ) -> jsonb
tail ( list anyarray ) -> anyarray
```

返回列表中除第一个元素之外的所有元素。

**注意事项**

- 空列表返回空列表，而不是 null；这一点不同于 `head` 和 `last`。

```cypher
RETURN head([]) AS first, tail([]) AS rest;
```

```
 first | rest
-------+------
       | []
```

## unnest {#unnest}

**2.18 新增**

```
unnest ( from_json jsonb ) -> setof jsonb
```

把列表展开为每个元素一行。

**注意事项**

- 这是集合返回函数。在 Cypher 中，它会使所在子句的行成倍增加。`FOR x IN list` 是同一思想的子句形式；当需要把元素绑定到名称时，它更易读。
- 输出列名为 `value`，因此在 SQL 中写 `SELECT value FROM unnest(...)`。
- PostgreSQL 的 `unnest(anyarray)` 仍适用于原生数组。

```cypher
MATCH (m:movie {title:'The Matrix'}) RETURN unnest(m.embedding) AS component;
```

```
  component
-------------
 -0.07594558
 0.04081754
 0.29592122
 -0.11921061
```

## 反转与切分 {#reversing-and-splitting}

两个生成列表的函数随其来源字符串一起说明：[`reverse`](/zh/agensgraph/reference/functions/string/#reverse) 既反转字符串也反转列表；[`split`](/zh/agensgraph/reference/functions/string/#split) 把字符串切分成列表。类型转换页包含三个列表类型转换：[`toStringList`](/zh/agensgraph/reference/functions/type-conversion/#tostringlist)、[`toIntegerList`](/zh/agensgraph/reference/functions/type-conversion/#tointegerlist) 和 [`toFloatList`](/zh/agensgraph/reference/functions/type-conversion/#tofloatlist)。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

这里的 `range()` 与 openCypher 一样包含 `stop`。不支持 openCypher 的 `reduce()`；请使用列表推导或 `FOR`。不支持模式推导。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [聚合函数](/zh/agensgraph/reference/functions/aggregate/) — 构建列表的 `collect`
- [谓词函数](/zh/agensgraph/reference/functions/predicate/) — `all`、`any`、`none`、`single`、`isEmpty`
- [jsonb 操作符与函数](/zh/agensgraph/reference/functions/jsonb/) — 列表底层使用的操作符
