---
title: 谓词函数
linkTitle: 谓词函数
description: 返回是或否答案的函数。
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/predicate.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


返回是或否答案的函数。四个列表量词 `all`、`any`、`none` 和 `single` 是语法形式，而不是普通调用。每个量词接收一个变量、一个列表和一个 `WHERE` 子句，并使用三值逻辑归约逐元素结果；因此包含 null 的列表可能使答案为 null，而不是 false。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## all {#all}

```
all ( variable IN list WHERE predicate ) -> boolean
```

当谓词对列表中每个元素都成立时，返回 true。

**注意事项**

- 空列表返回 true。
- 如果谓词对某个元素为 null，对其余所有元素为 true，则结果为 null。只要有一个元素为 false，无论其他元素是否为 null，结果都是 false。
- 谓词会对每个元素求值；不会短路。
- 该调用会被下推为 `cypher_all()`。谓词内部发出的错误消息会使用这个名称。

```cypher
MATCH (m:movie) WHERE all(x IN m.embedding WHERE x > -0.1) RETURN m.title ORDER BY m.title;
```

```
        title
---------------------
 "Blade Runner 2049"
```

## any {#any}

```
any ( variable IN list WHERE predicate ) -> boolean
```

当谓词对列表中至少一个元素成立时，返回 true。

**注意事项**

- 空列表返回 false。
- 只要有一个元素为 true，即使其他元素为 null，结果也是 true。
- 如果没有任何元素为 true，且任一元素为 null，则结果为 null。

```cypher
MATCH (p:person)-[:acted_in]->(m:movie)
WITH p, collect(m.genre) AS genres
WHERE any(g IN genres WHERE g = 'Adventure')
RETURN p.name AS actor;
```

```
    actor
-------------
 "Sam Neill"
```

## exists {#exists}

```
exists ( pattern ) -> boolean
exists ( property_reference ) -> boolean
```

使用模式时，只要模式至少匹配一次，就返回 true。使用属性引用时，只要该属性存在且不为 null，就返回 true。

**注意事项**

- 这两种形式是不同的构造，不是同一个函数的重载。模式形式会变成 `EXISTS` 子查询，属性形式会变成 `IS NOT NULL` 测试。
- 属性形式的参数必须是属性引用，例如 `m.year`。任意表达式会被解释为模式，并且无法解析。
- `exists()` 内部的模式可以绑定外层查询中的变量，如下例中的 `(p)`；但它引入的任何变量在外层不可见。

```cypher
MATCH (m:movie {title:'Inception'}) RETURN exists(m.year) AS has_year, exists(m.budget) AS has_budget;
```

```
 has_year | has_budget
----------+------------
 t        | f
```

```cypher
MATCH (p:person) WHERE exists((p)-[:directed]->()) RETURN p.name ORDER BY p.name LIMIT 3;
```

```
        name
---------------------
 "Andrew Niccol"
 "Christopher Nolan"
 "Denis Villeneuve"
```

## isEmpty {#isempty}

```
isEmpty ( value jsonb ) -> boolean
```

当列表没有元素，或映射没有键时，返回 true。

**注意事项**

- 参数必须解析为 `jsonb`。裸字符串字面量的类型是 `unknown`，因此也会匹配范围和多重范围的 `isempty`：

```cypher
RETURN isEmpty('');
```

```
ERROR:  function isempty(unknown) is not unique
LINE 1: RETURN isEmpty('');
               ^
HINT:  Could not choose a best candidate function. You might need to add explicit type casts.
```

  请改为显式转换：`isEmpty(''::jsonb)`。
- 属性引用本身已是 `jsonb`，因此 `isEmpty(n.tags)` 不需要转换。
- 空字符串返回 true；它是空的 `jsonb` 标量。

```cypher
RETURN isEmpty([]) AS empty_list, isEmpty([1]) AS one_element, isEmpty({}) AS empty_map;
```

```
 empty_list | one_element | empty_map
------------+-------------+-----------
 t          | f           | t
```

## none {#none}

```
none ( variable IN list WHERE predicate ) -> boolean
```

当谓词对列表中没有任何元素成立时，返回 true。它是 [`any`](#any) 的否定形式。

**注意事项**

- 空列表返回 true。
- 只要有一个元素为 true，结果就是 false。如果没有任何元素为 true，且任一元素为 null，则结果为 null。

```cypher
MATCH (m:movie) WHERE none(x IN m.embedding WHERE x > 0.4) RETURN count(*) AS films;
```

```
 films
-------
 15
```

## single {#single}

```
single ( variable IN list WHERE predicate ) -> boolean
```

当谓词对列表中恰好一个元素成立时，返回 true。

**注意事项**

- 空列表返回 false。
- 任一元素的结果为 null 都会使整个答案为 null，因为这个 null 本来可能是第二个匹配项。

```cypher
MATCH (p:person)-[:directed]->(m:movie)
WITH p, collect(m.year) AS years
WHERE single(y IN years WHERE y > 2010)
RETURN p.name AS director, years ORDER BY p.name;
```

```
      director       |          years
---------------------+--------------------------
 "Christopher Nolan" | [2010, 2014]
 "Denis Villeneuve"  | [2017]
 "Joss Whedon"       | [2012]
 "Lana Wachowski"    | [2003, 1999, 2021, 2003]
 "Neill Blomkamp"    | [2013]
```

## 三值结果并排对比 {#three-valued-results-side-by-side}

这些量词在列表包含 null 和列表为空时差别最大。下面两行都是真实输出：

```cypher
RETURN all(x IN [1, null] WHERE x > 0) AS every, any(x IN [1, null] WHERE x > 0) AS some,
       none(x IN [null] WHERE x > 0) AS not_any, single(x IN [1, null] WHERE x > 0) AS exactly_one;
```

```
 every | some | not_any | exactly_one
-------+------+---------+-------------
       | t    |         |
```

```cypher
RETURN all(x IN [] WHERE x = 0) AS every, any(x IN [] WHERE x = 0) AS some,
       none(x IN [] WHERE x = 0) AS not_any, single(x IN [] WHERE x = 0) AS exactly_one;
```

```
 every | some | not_any | exactly_one
-------+------+---------+-------------
 t     | f    | t       | f
```

`RETURN` 会让布尔列保持为 `boolean`，而不是装箱为 `jsonb`。因此这些结果打印为 `t`、`f` 和表示 null 的空白，而不是 `true`、`false` 和 `null`。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

对属性使用 `exists()` 是 openCypher 对 `IS NOT NULL` 的较早拼写。不支持 pattern-comprehension 和 `exists { ... }` 块形式；请使用上文的模式形式或[子查询表达式](/zh/agensgraph/reference/clauses/subquery-expressions/)。

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [子查询表达式](/zh/agensgraph/reference/clauses/subquery-expressions/) — `EXISTS`、`COUNT`、`COLLECT`
- [列表函数](/zh/agensgraph/reference/functions/list/) — 构建这些量词作用的列表
