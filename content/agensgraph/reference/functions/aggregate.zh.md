---
title: 聚合函数
linkTitle: 聚合函数
description: 将一组行归约为单个值的函数。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/aggregate.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


将一组行归约为单个值的函数。Cypher 的分组方式与 SQL 相同：`RETURN` 或 `WITH` 列表中每个未聚合的表达式都是一个分组键。如果完全没有键，整个结果就是一个组。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## avg {#avg}

```
avg ( expression numeric ) -> numeric
```

返回组中非空值的算术平均值。

**注意事项**

- 属性以 `jsonb` 形式到达，并被转换为 `numeric`，因此结果是 `numeric`，保留完整精度，而不是舍入为 `double precision`。
- 值为 null 的行会被跳过。没有非空值的组返回 null。

```cypher
MATCH (m:movie) RETURN avg(m.year) AS mean_year;
```

```
       mean_year
-----------------------
 2002.0555555555555556
```

## collect {#collect}

```
collect ( expression anyelement ) -> jsonb
collect ( v vertex ) -> vertex[]
collect ( e edge ) -> edge[]
collect ( p graphpath ) -> graphpath[]
```

按组内行的顺序把组中的值收集到一个列表。

**注意事项**

- `vertex`、`edge` 或 `graphpath` 参数产生原生数组，而不是 `jsonb` 数组：`vertex[]`、`edge[]` 或 `graphpath[]`。其他所有参数都产生 `jsonb`。**2.18 新增**
- Cypher 的下标从 0 开始索引原生数组，与 `jsonb` 列表相同。
- 会收集 null 值。`collect(DISTINCT expr)` 会移除重复值。
- `length()` 可统计这四种结果类型中任一种的元素数量。

```cypher
MATCH (p:person)-[:directed]->(m:movie)
WITH p, collect(m.title) AS films
RETURN p.name AS director, films ORDER BY p.name LIMIT 2;
```

```
      director       |             films
---------------------+-------------------------------
 "Andrew Niccol"     | ["Gattaca"]
 "Christopher Nolan" | ["Inception", "Interstellar"]
```

直接收集图元素本身会得到这些元素的数组：

```cypher
MATCH (:movie {title:'The Matrix'})-[e:related_to]->()
WITH collect(e) AS edges
RETURN length(edges) AS n, pg_typeof(edges) AS type;
```

```
 n |   type
---+----------
 3 | "edge[]"
```

## count {#count}

```
count ( * ) -> bigint
count ( expression ) -> bigint
```

统计组中的行数。`count(*)` 统计每一行；`count(expression)` 统计表达式不为 null 的行。

**注意事项**

- 对整个顶点或边执行 `count(v)` 时统计的是元素标识：解析器会把参数替换为其 `graphid`，因此不会读取属性包。
- `count(DISTINCT expression)` 统计不同的非空值。
- 没有行的组返回 0，而不是 null。

```cypher
MATCH (m:movie)
RETURN count(*) AS films, count(m.genre) AS with_genre, count(DISTINCT m.genre) AS genres;
```

```
 films | with_genre | genres
-------+------------+--------
 18    | 18         | 3
```

## max {#max}

```
max ( expression jsonb ) -> jsonb
max ( expression numeric ) -> numeric
```

返回组中的最大值。

**注意事项**

- `jsonb` 参数按 `jsonb` 自身的类型顺序排序，其中每个数字都排在每个字符串之前。从带类型列读取的 numeric 或 text 属性按该列的类型比较。
- null 会被跳过；没有非空值的组返回 null。

```cypher
MATCH (m:movie) RETURN min(m.year) AS earliest, max(m.year) AS latest;
```

```
 earliest | latest
----------+--------
 1982     | 2021
```

## min {#min}

```
min ( expression jsonb ) -> jsonb
min ( expression numeric ) -> numeric
```

返回组中的最小值。[`max`](#max) 的注意事项同样适用于此，不作改变。

## percentileCont {#percentilecont}

```
percentileCont ( list jsonb, percentile numeric ) -> double precision
```

返回数字列表的分位数，并在跨越所请求位置的两个值之间插值。

**注意事项**

- 这是作用于列表的普通函数，不是聚合函数。要取组的分位数，应先构建列表：`percentileCont(collect(m.year), 0.5)`。
- 参数必须是列表。标量会被拒绝，而错误消息会显示另一个函数名：

```cypher
RETURN percentileCont(2010, 0.5);
```

```
ERROR:  reverse(): list is expected but 2010
```
- 列表元素少于两个，或百分位数超出 0 到 1 的范围时，返回 null。
- 非数字元素会被忽略，而不会被拒绝。

```cypher
MATCH (m:movie) RETURN percentileCont(collect(m.year), 0.5) AS median;
```

```
 median
--------
 2002.5
```

## percentileDisc {#percentiledisc}

```
percentileDisc ( list jsonb, percentile numeric ) -> double precision
```

返回数字列表的分位数，并向下舍入到列表中实际存在的元素。其注意事项与 [`percentileCont`](#percentilecont) 相同。

```cypher
MATCH (m:movie) RETURN percentileDisc(collect(m.year), 0.5) AS median;
```

```
 median
--------
 2002
```

## stdev {#stdev}

```
stdev ( expression numeric ) -> numeric
```

返回组中值的样本标准差，即除以 *n* − 1 的估计值。

**注意事项**

- 解析器会把名称改写为 `stddev_samp`，因此结果列和错误消息使用的是该名称。
- 未加引号的标识符会折叠为小写，所以 `stDev` 和 `STDEV` 是同一个调用。
- `stdDev` 是*另一个*函数：它折叠为 `stddev`，这是 PostgreSQL 自身对 `stddev_samp` 的别名。它计算的结果相同。
- 只有一行的组返回 null。

```cypher
MATCH (m:movie) RETURN stdev(m.year) AS sample_sd, stdevp(m.year) AS population_sd;
```

```
      sample_sd      |    population_sd
---------------------+---------------------
 11.3628508344062724 | 11.0427061006209596
```

## stdevp {#stdevp}

```
stdevp ( expression numeric ) -> numeric
```

返回组中值的总体标准差，即除以 *n* 的估计值。解析器会把名称改写为 `stddev_pop`，`stDevP` 是同一个调用。

## sum {#sum}

```
sum ( expression numeric ) -> numeric
```

返回组中非空值的总和。

**注意事项**

- null 会被跳过。没有非空值的组返回 null，而不是 0。
- 输入不会被去重：模式匹配到两次的值会被加两次。如果这不是想要的结果，请使用 `sum(DISTINCT expr)`。

```cypher
MATCH (p:person)-[:acted_in]->(:movie) RETURN sum(p.born) AS born_total;
```

```
 born_total
------------
 49017
```

## 兼容性 {#compatibility}

### openCypher {#opencypher}

`stDev` 和 `stDevP` 是 openCypher 对样本标准差和总体标准差的命名；两种拼写在本文档中均可使用。openCypher 的 `percentileCont` 和 `percentileDisc` 是每行取一个值的聚合函数。本文档中的函数接收已完成的列表，因此为 openCypher 编写的查询需要在第一个参数外使用 `collect()`。

### ISO/IEC 39075 {#isoiec-39075}

`avg`、`count`、`max`、`min`、`stddev_pop`、`stddev_samp` 和 `sum` 是 GQL 聚合函数，拼写与标准一致。`collect` 对应 GQL 的 `COLLECT` 值表达式；该表达式与[子查询表达式](/zh/agensgraph/reference/clauses/subquery-expressions/)一起说明。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [谓词函数](/zh/agensgraph/reference/functions/predicate/) — `all`、`any`、`none`、`single`
- [列表函数](/zh/agensgraph/reference/functions/list/) — 处理 `collect` 生成的列表
