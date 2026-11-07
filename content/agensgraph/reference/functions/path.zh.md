---
title: 路径函数
linkTitle: 路径函数
description: 作用于 graphpath 的函数，以及生成 graphpath 的三种寻路形式。
type: docs
weight: 80
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/functions/path.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


作用于 `graphpath` 的函数，以及生成 `graphpath` 的三种寻路形式。`graphpath` 是 `MATCH p = (...)` 绑定的顶点和边交替序列。

通过命名来绑定路径：`MATCH p = (a)-[r]->(b)`。这些函数接收的是*变量*，不是模式。

示例基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

## allshortestpaths {#allshortestpaths}

```
allshortestpaths ( pattern ) -> graphpath
```

查找两个顶点之间的每一条最短路径。当它命名路径变量时，每条路径返回一行；当它作为表达式使用时，返回路径数组。

**注意事项**

- 模式必须恰好包含一个关系，否则解析器抛出 `only one relationship is allowed`。请给这个关系指定长度范围，例如 `*..4`，而不是写出多跳。
- 任何地方都不支持多类型关系模式，`allshortestpaths` 也不例外。请匹配无类型边，并用 `WHERE label(r) IN [...]` 过滤。
- 作为表达式，它产生 `graphpath[]`，因此对其执行 `length()` 统计的是找到的路径数，不是一条路径中的边数。

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
RETURN length(allshortestpaths((a)-[:related_to*..4]->(b))) AS paths_found;
```

```
 paths_found
-------------
 1
```

## dijkstra {#dijkstra}

```
dijkstra ( pattern, weight ) -> graphpath
dijkstra ( pattern, weight, condition ) -> graphpath
dijkstra ( pattern, weight, LIMIT count ) -> graphpath
dijkstra ( pattern, weight, condition, LIMIT count ) -> graphpath
```

查找两个顶点之间的最小代价路径，每条边的代价等于 `weight` 的求值结果。

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| `pattern` | 路径链 | 两个顶点之间恰好一个关系，例如 `(a)-[e:related_to]->(b)`。如果 `weight` 读取关系的属性，请给关系指定变量。 |
| `weight` | 数值表达式 | 遍历一条边的代价。对每条被考虑的边都必须大于 0。 |
| `condition` | 布尔表达式 | 可选的边过滤条件。只有满足它的边会被遍历。 |
| `count` | `integer` | 可选。要返回的备选路径数，按代价从低到高。必须大于 0。 |

**注意事项**

- 作为模式部分书写时，它绑定路径：`p = dijkstra(...)`。写成 `(p, w) = dijkstra(...)` 时，它同时绑定路径*和*总权重；后者没有其他获取方式。
- 没有 `LIMIT` 时，数量默认为 1，因此返回一条路径。
- 该模式既不接受属性约束，也不接受变长关系。请改在 `WHERE` 中过滤。

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'}),
      p = dijkstra((a:movie {title:'The Matrix'})-[e:related_to]->(b), e.weight)
RETURN p;
```

```
ERROR:  property constraint is not supported
LINE 2:       p = dijkstra((a:movie {title:'The Matrix'})-[e:related...
                            ^
```

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'}),
      p = dijkstra((a)-[e:related_to*]->(b), e.weight)
RETURN p;
```

```
ERROR:  variable length relationship is not supported
```

- 第三个位置参数是条件，因此在那里放数字会抛出 `cannot cast 1 (jsonb type numeric) to boolean`。
- 另外两种拒绝发生在运行时到达边之后，因此取决于数据而不只是查询。求值为 0 或更小的权重报告 `WEIGHT must be larger than 0`；`LIMIT 0` 报告 `LIMIT must be larger than 0`。
- 作为裸表达式使用而不赋值时，它产生 `graphpath[]`。

最小代价路线不是最短路线。经过 *Total Recall* 的两跳代价为 4 + 2，在这个图中胜过单跳备选：

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'}),
      (p, w) = dijkstra((a)-[e:related_to]->(b), e.weight)
RETURN [x IN nodes(p) | x.title] AS route, w AS weight;
```

```
                    route                    | weight
---------------------------------------------+--------
 ["The Matrix", "Total Recall", "Inception"] | 6
```

让远端端点不受约束时，会得到到每部可达电影的最小代价路线：

```cypher
MATCH p = dijkstra((a:movie)-[e:related_to]->(b:movie), e.weight, LIMIT 1)
WHERE a.title = 'The Matrix'
RETURN [x IN nodes(p) | x.title] AS route ORDER BY route;
```

```
                                            route
---------------------------------------------------------------------------------------------
 ["The Matrix"]
 ["The Matrix", "The Matrix Reloaded"]
 ["The Matrix", "The Terminator"]
 ["The Matrix", "Total Recall"]
 ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"]
 ["The Matrix", "The Terminator", "Terminator 2: Judgment Day"]
 ["The Matrix", "Total Recall", "Inception"]
 ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions", "The Matrix Resurrections"]
```

没有 `ORDER BY` 时，行没有特定顺序；上面的排序只是让页面结果可复现。

> [!NOTE]
> `dijkstra` 找到的路径与其他 `graphpath` 一样，所以 `nodes()`、`relationships()` 和 `length()` 都能读取它。其他路径没有的信息是总权重，只有 `(p, w) =` 形式会暴露它。

## edges {#edges}

```
edges ( p graphpath ) -> edge[]
```

按顺序返回路径的边。[`relationships`](#relationships) 是同一个函数在 Cypher 常用名称下的形式。

## end_vertex {#end_vertex}

```
end_vertex ( e edge ) -> vertex
```

返回边指向的顶点。`endNode` 是同一个函数在 Cypher 常用名称下的形式；两者都列在[标量函数页](/zh/agensgraph/reference/functions/scalar/#endnode)。

**注意事项**

- 读取顶点意味着获取它的行。如果只需要标识，请使用 [`end_id`](/zh/agensgraph/reference/functions/scalar/#end_id)；它只读取边自身的列。

## length {#length}

```
length ( p graphpath ) -> jsonb
length ( vs vertex[] ) -> jsonb
length ( es edge[] ) -> jsonb
length ( ps graphpath[] ) -> jsonb
```

对路径返回其中的边数。对数组返回其中的元素数。

**注意事项**

- 是边数，不是元素数：一条边的路径长度为 1，而同一路径的 [`cardinality`](/zh/agensgraph/reference/functions/list/#cardinality) 是 3。
- 因为 `allshortestpaths()` 和未赋值的 `dijkstra()` 产生 `graphpath[]`，对其执行 `length()` 统计的是路径。
- 对字符串、列表或映射，`length` 是另一个函数；见标量函数页的 [`length`](/zh/agensgraph/reference/functions/scalar/#length)。

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'The Matrix Resurrections'})
RETURN length(shortestpath((a)-[:related_to*]->(b))) AS hops;
```

```
 hops
------
 3
```

## nodes {#nodes}

```
nodes ( p graphpath ) -> vertex[]
```

按顺序返回路径的顶点，从路径起点开始。

**注意事项**

- 结果是原生数组 `vertex[]`，因此 Cypher 的 `RETURN` 不会把它装箱为 `jsonb`。下标仍从 0 开始。
- `vertices` 是同一个函数的另一个名称。
- 传入路径*变量*。内联写的模式不是表达式，无法解析。
- 打印整个顶点很少是你想要的结果，因为每个顶点都携带完整属性包。请像下面这样用列表推导投影需要的字段。

```cypher
MATCH p=(:person {name:'Christopher Nolan'})-[:directed]->(:movie {title:'Inception'})
RETURN [x IN nodes(p) | x.name] AS names, [x IN nodes(p) | x.title] AS titles;
```

```
            names            |       titles
-----------------------------+---------------------
 ["Christopher Nolan", null] | [null, "Inception"]
```

路径中的每个顶点都会被投影，因此某个顶点没有的键会返回 null。

## relationships {#relationships}

```
relationships ( p graphpath ) -> edge[]
```

按顺序返回路径的边。与 [`edges`](#edges) 相同。

```cypher
MATCH p=(:person {name:'Christopher Nolan'})-[:directed]->(:movie {title:'Inception'})
RETURN relationships(p) AS edges;
```

```
           edges
----------------------------
 [directed[6.8][4.8,3.5]{}]
```

## shortestpath {#shortestpath}

```
shortestpath ( pattern ) -> graphpath
```

按边数查找两个顶点之间的一条最短路径。如果多条路径等长，返回其中一条。

**注意事项**

- 模式必须恰好包含一个关系，并且该关系携带长度范围。逐跳写出会被拒绝：

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'Inception'})
RETURN shortestpath((a)-[:related_to]->()-[:related_to]->(b));
```

```
ERROR:  only one relationship is allowed
LINE 2: RETURN shortestpath((a)-[:related_to]->()-[:related_to]->(b)...
                            ^
```
- 多条等短路径中返回哪一条没有定义。需要全部时请使用 [`allshortestpaths`](#allshortestpaths)。
- 路径不存在时返回零行，而不是返回 null 路径。
- 这里同样不支持多类型关系模式。

```cypher
MATCH (a:movie {title:'The Matrix'}), (b:movie {title:'The Matrix Resurrections'})
RETURN [x IN nodes(shortestpath((a)-[:related_to*]->(b))) | x.title] AS route;
```

```
                                            route
---------------------------------------------------------------------------------------------
 ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions", "The Matrix Resurrections"]
```

## start_vertex {#start_vertex}

```
start_vertex ( e edge ) -> vertex
```

返回边离开的顶点。`startNode` 是同一个函数在 Cypher 常用名称下的形式；见 [`startNode`](/zh/agensgraph/reference/functions/scalar/#startnode)。

顶点是复合类型，因此可以直接从结果读取属性：

```cypher
MATCH (:person {name:'Keanu Reeves'})-[e:acted_in]->(:movie {title:'The Matrix'})
RETURN start_vertex(e).name AS actor, end_vertex(e).title AS film;
```

```
     actor      |     film
----------------+--------------
 "Keanu Reeves" | "The Matrix"
```

## vertices {#vertices}

```
vertices ( p graphpath ) -> vertex[]
```

按顺序返回路径的顶点。与 [`nodes`](#nodes) 相同。

## 兼容性 {#compatibility}

### openCypher {#opencypher}

`shortestPath` 和 `allShortestPaths` 不区分大小写，因此 openCypher 的大小写拼写可用。openCypher 没有 `dijkstra`；其中的加权最短路径来自过程库。

openCypher 允许关系模式命名多个类型，例如 `-[r:acted_in|directed]->`。在所有长度和所有寻路形式中，这都会抛出 `multiple types for relationship not supported`。请匹配无类型关系并改测标签：

```cypher
MATCH (p:person)-[r]->(m:movie) WHERE label(r) IN ['acted_in','directed'] RETURN count(r) AS n;
```

```
 n
----
 46
```

## 另见 {#see-also}

- [全部函数](/zh/agensgraph/reference/functions/all-functions/) — 所有函数汇总在一张表中
- [标量函数](/zh/agensgraph/reference/functions/scalar/) — `startNode`、`endNode`、`start_id`、`end_id`
- [列表函数](/zh/agensgraph/reference/functions/list/) — 作用于路径的 `cardinality`
- [语法](/zh/agensgraph/reference/syntax/) — 路径模式和可变长度
