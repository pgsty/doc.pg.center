---
title: 路径
linkTitle: 路径
description: 固定模式提出的问题，其形状你已经知道。(a)-[]->(b)-[]->(c) 始终是两跳。
type: docs
weight: 40
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/querying/paths.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


固定模式提出的问题，其形状你已经知道。`(a)-[]->(b)-[]->(c)` 始终是两跳。图真正擅长的问题，是形状未知的问题：这两个人如何连接、从这里能到达哪里、哪条路线成本最低。

三种工具回答这些问题，且彼此不同。变长边枚举某个长度范围内的每条路径。`shortestpath` 找到一条长度最小的路径。`dijkstra` 找到一条*权重*最小的路径，而它常常不是同一条路径。

本文所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行，其 `related_to` 边带有 `weight`。下面两节还需要一个四个站点的小图，现在先创建它。它有一条成本为 10 的直达 A → B 路段、一条每段成本为 1 的三段绕行，以及一条让 A → B → A 形成环的返程路段：

```cypher
CREATE GRAPH routelab;
SET graph_path = routelab;
CREATE VLABEL stop;
CREATE ELABEL leg;
CREATE (:stop {name: 'A'}), (:stop {name: 'B'}), (:stop {name: 'C'}), (:stop {name: 'D'});
MATCH (a:stop {name:'A'}), (b:stop {name:'B'}) CREATE (a)-[:leg {cost: 10}]->(b);
MATCH (a:stop {name:'A'}), (c:stop {name:'C'}) CREATE (a)-[:leg {cost: 1}]->(c);
MATCH (c:stop {name:'C'}), (d:stop {name:'D'}) CREATE (c)-[:leg {cost: 1}]->(d);
MATCH (d:stop {name:'D'}), (b:stop {name:'B'}) CREATE (d)-[:leg {cost: 1}]->(b);
MATCH (b:stop {name:'B'}), (a:stop {name:'A'}) CREATE (b)-[:leg {cost: 1}]->(a);
```

下面每个代码块都会按需要把 `graph_path` 设为这两个图之一。

## 可变跳数 {#a-variable-number-of-hops}

边标签后的 `*` 使长度变成范围。边界写在星号之后：

| 写法 | 含义 |
| --- | --- |
| `-[:related_to*2]->` | 恰好两条边 |
| `-[:related_to*1..3]->` | 一、二或三条边 |
| `-[:related_to*2..]->` | 两条或更多 |
| `-[:related_to*..3]->` | 最多三条，且至少一条 |
| `-[:related_to*]->` | 一条或更多，无上界 |
| `-[:related_to*0..1]->` | 顶点自身，或相距一条边 |

固定长度的行为像完整写出的模式：

```cypher
SET graph_path = moviekb;
MATCH (a:movie {title: 'The Matrix'})-[:related_to*2]->(b:movie) RETURN b.title AS reached ORDER BY reached;
```

```
           reached            
------------------------------
 "Inception"
 "Terminator 2: Judgment Day"
 "The Matrix Revolutions"
```

范围会对其中每个长度取并集，所以较短的可达结果也会返回：

```cypher
MATCH (a:movie {title: 'The Matrix'})-[:related_to*1..2]->(b:movie) RETURN b.title AS reached ORDER BY reached;
```

```
           reached            
------------------------------
 "Inception"
 "Terminator 2: Judgment Day"
 "The Matrix Reloaded"
 "The Matrix Revolutions"
 "The Terminator"
 "Total Recall"
```

下界为零包含起始顶点，它不与任何内容匹配：

```cypher
MATCH (a:movie {title: 'The Matrix'})-[:related_to*0..1]->(b:movie) RETURN b.title AS reached ORDER BY reached;
```

```
        reached        
-----------------------
 "The Matrix"
 "The Matrix Reloaded"
 "The Terminator"
 "Total Recall"
```

省略上界表示“边能走多远就走多远”：

```cypher
MATCH (a:movie {title: 'The Matrix'})-[:related_to*]->(b:movie) RETURN count(*) AS reachable;
```

```
 reachable 
-----------
         7
```

### 它不会无限循环 {#it-cannot-loop-forever}

在带环图上，无界遍历会终止，因为路径不得两次使用同一条边。`routelab` 有一个环 A → B → A。请求从 A 回到 A、最多八条边的路径：

```cypher
SET graph_path = routelab;
MATCH p = (a:stop {name: 'A'})-[:leg*..8]->(a)
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS route ORDER BY hops;
```

```
 hops |           route           
------+---------------------------
 2    | ["A", "B", "A"]
 4    | ["A", "C", "D", "B", "A"]
```

只有两条路径，不是无限条：每条都是不重复使用边的走法。*顶点*可以重复，这里的 `A` 就在两端出现。

这个保证关乎正确性，不关乎成本。稠密图上的无界搜索仍可能在边耗尽前枚举大量路径。只要对范围上界有任何概念，就给它一个上界。

## 绑定路径 {#binding-the-path}

模式前的 `p = ` 绑定整条路径，三个函数负责拆解：`length(p)` 是边数，`nodes(p)` 是按顺序排列的顶点，`relationships(p)` 是边。

```cypher
SET graph_path = moviekb;
MATCH p = (a:movie {title: 'The Matrix'})-[:related_to*2]->(b:movie)
RETURN length(p) AS hops,
       [x IN nodes(p) | x.title] AS route,
       [r IN relationships(p) | r.weight] AS weights
ORDER BY route;
```

```
 hops |                              route                              | weights 
------+-----------------------------------------------------------------+---------
 2    | ["The Matrix", "The Matrix Reloaded", "The Matrix Revolutions"] | [1, 1]
 2    | ["The Matrix", "The Terminator", "Terminator 2: Judgment Day"]  | [3, 1]
 2    | ["The Matrix", "Total Recall", "Inception"]                     | [4, 2]
```

`[x IN list | expression]` 是列表推导式，也是把路线渲染得可读的方法。`edges(p)` 是 `relationships(p)` 的同义词。

跨两个标签的路径需要每个属性一个推导式，因为 `person` 没有 `title`，`movie` 没有 `name`：

```cypher
MATCH p = shortestpath((a:person {name: 'Keanu Reeves'})-[e:acted_in*..6]-(b:person {name: 'Carrie-Anne Moss'}))
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS people, [x IN nodes(p) | x.title] AS films;
```

```
 hops |                   people                   |           films            
------+--------------------------------------------+----------------------------
 2    | ["Keanu Reeves", null, "Carrie-Anne Moss"] | [null, "The Matrix", null]
```

返回路径本身会完整打印每个元素；探索时有用，其他场合信息过多。`label(x)` 是查看路线形状的紧凑方式。

## 最短路径 {#the-shortest-path}

`shortestpath` 接受带一条变长边的模式，返回一条长度最小的路径；如果没有，则不返回行。它不是“按长度排序的所有路径，限制 1”。它是双向搜索，两个前沿相遇即停止，因此不会枚举被拒绝的路径。

```cypher
MATCH p = shortestpath((a:person {name: 'Keanu Reeves'})-[e*..6]-(b:person {name: 'Arnold Schwarzenegger'}))
RETURN length(p) AS hops,
       [x IN nodes(p) | label(x)] AS labels,
       [r IN relationships(p) | label(r)] AS via;
```

```
 hops |                 labels                 |                  via                   
------+----------------------------------------+----------------------------------------
 3    | ["person", "movie", "movie", "person"] | ["acted_in", "related_to", "acted_in"]
```

这个查询有三点是刻意安排的。边不带类型且无方向，因为路线跨越两个不同的边标签，一个正向、一个反向。

上界 6 的存在，是因为在无标签边上做无界最短路径搜索是本手册中最昂贵的查询。并且两个端点都绑定到了变量。

最后一点是硬性要求：

```cypher
MATCH p = shortestpath((:person {name: 'Keanu Reeves'})-[e*..6]-(:person {name: 'Arnold Schwarzenegger'}))
RETURN length(p);
```

```
ERROR:  node must be a reference to a specific node
```

即使从不使用名称，也要命名两端。这是唯一一处省略变量不仅浪费，而且会被拒绝的地方。

`allshortestpaths` 是同样的搜索，但返回该最小长度下的每条路径，而不是其中一条：

```cypher
MATCH p = allshortestpaths((a:movie {title: 'The Matrix'})-[:related_to*..4]->(b:movie {title: 'Inception'}))
RETURN length(p) AS hops, [x IN nodes(p) | x.title] AS route;
```

```
 hops |                    route                    
------+---------------------------------------------
 2    | ["The Matrix", "Total Recall", "Inception"]
```

这里只有一条路线，因为该数据集的 `related_to` 边构成树。如果图上有多条等长短路线，则每条返回一行。当平局正是有价值的信息时，你需要的就是这个结果。

两个函数都不接受边标签交替。`[:acted_in|directed*..4]` 会抛出 `ERROR: multiple types for relationship not supported`。保留边不带类型并在之后过滤；参见[读取图](/zh/agensgraph/querying/reading/#one-label-per-edge)。

## 最便宜路径 {#the-cheapest-path}

`shortestpath` 统计边数。边并不总是可互换的：它们可能携带距离、延迟、价格或相似度。此时统计边数回答的是错误问题。`dijkstra` 接受权重表达式并最小化总和。

在 `routelab` 上最容易看出差异；它有两条从 A 到 B 的有用路线：

```cypher
SET graph_path = routelab;
MATCH p = (a:stop {name: 'A'})-[:leg*..3]->(b:stop {name: 'B'})
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS route, [r IN relationships(p) | r.cost] AS costs
ORDER BY hops;
```

```
 hops |        route         |   costs   
------+----------------------+-----------
 1    | ["A", "B"]           | [10]
 3    | ["A", "C", "D", "B"] | [1, 1, 1]
```

`shortestpath` 选择一跳路线：

```cypher
MATCH p = shortestpath((a:stop {name: 'A'})-[:leg*..5]->(b:stop {name: 'B'}))
RETURN length(p) AS hops, [x IN nodes(p) | x.name] AS route;
```

```
 hops |   route    
------+------------
 1    | ["A", "B"]
```

`dijkstra` 选择三跳路线，因为它的成本是 3 而不是 10：

```cypher
MATCH (a:stop {name: 'A'}), (b:stop {name: 'B'})
MATCH (p, total) = dijkstra((a)-[e:leg]->(b), e.cost)
RETURN total AS cost, length(p) AS hops, [x IN nodes(p) | x.name] AS route;
```

```
 cost | hops |        route         
------+------+----------------------
 3    | 3    | ["A", "C", "D", "B"]
```

语法上有两点容易弄错。

**模式中是一跳，不是变长边。** `dijkstra` 自行扩展，所以你写单跳，它按需要走多远。里面的 `*` 会以 `ERROR: variable length relationship is not supported` 拒绝；多于一条边会以 `ERROR: only one relationship is allowed` 拒绝。

**权重表达式命名边变量。** `e.cost` 引用模式内绑定的 `e`，并在搜索扩展时逐边求值。

`(p, total) = dijkstra(...)` 绑定两件事：路径和沿路径的总权重。单变量形式 `p = dijkstra(...)` 只给出路径。

手册自带数据集的权重在 `related_to` 上：

```cypher
SET graph_path = moviekb;
MATCH (a:movie {title: 'The Matrix'}), (b:movie {title: 'Inception'})
MATCH (p, total) = dijkstra((a)-[e:related_to]->(b), e.weight)
RETURN total AS weight, [x IN nodes(p) | x.title] AS route, [r IN relationships(p) | r.weight] AS legs;
```

```
 weight |                    route                    |  legs  
--------+---------------------------------------------+--------
 6      | ["The Matrix", "Total Recall", "Inception"] | [4, 2]
```

第三个参数是限定条件：搜索对每条候选边应用的布尔表达式，因此可以排除边，而不必预过滤图。这里没有任何结果，因为从* The Matrix *通往* Inception *的唯一路线必须经过权重 4 的边：

```cypher
MATCH (a:movie {title: 'The Matrix'}), (b:movie {title: 'Inception'})
MATCH (p, total) = dijkstra((a)-[e:related_to]->(b), e.weight, e.weight < 3)
RETURN total AS weight, [x IN nodes(p) | x.title] AS route;
```

```
 weight | route 
--------+-------
(0 rows)
```

限定条件必须像所有条件一样是布尔值。括号内的 `LIMIT n` 限制返回多少条路径。两者都在 [`dijkstra`](/zh/agensgraph/reference/functions/path/) 中说明。

## 路径的代价 {#what-a-path-costs}

变长边的执行计划有自己的节点，并写明它遍历的标签和范围：

```cypher
EXPLAIN (COSTS OFF) MATCH (a:movie {title: 'The Matrix'})-[r:related_to*1..3]->(b:movie) RETURN b.title;
```

```
                          QUERY PLAN                          
--------------------------------------------------------------
 Nested Loop
   ->  Seq Scan on movie a
         Filter: (properties.'title' = '"The Matrix"'::jsonb)
   ->  Hash Join
         Hash Cond: (r."end" = b.id)
         ->  Subquery Scan on r
               ->  Graph VLE on related_to [1..3]
                     ->  Result
         ->  Hash
               ->  Seq Scan on movie b
```

`Graph VLE on related_to [1..3]` 是要读的内容。省略标签后，它会变成 `Graph VLE on ag_edge`，每一跳都会遍历图中每个边标签：

```cypher
EXPLAIN (COSTS OFF) MATCH (a:movie {title: 'The Matrix'})-[r*1..2]->(b:movie) RETURN b.title;
```

```
                          QUERY PLAN                          
--------------------------------------------------------------
 Nested Loop
   ->  Seq Scan on movie a
         Filter: (properties.'title' = '"The Matrix"'::jsonb)
   ->  Hash Join
         Hash Cond: (r."end" = b.id)
         ->  Subquery Scan on r
               ->  Graph VLE on ag_edge [1..2]
                     ->  Result
         ->  Hash
               ->  Seq Scan on movie b
```

`shortestpath` 显示为 `Shortestpath VLE [min..max]`，位于两个 `Hash2Side` 节点之上；这两个节点是双向搜索的两个前沿。`dijkstra` 显示为 `Dijkstra` 节点。三种情况下，每跳的工作都是在边标签的 `(start, "end")` 或 `("end", start)` 索引上查找。因此路径查询的代价是前沿触碰的边数。以下四项按效果顺序减少它：

1. **锚定一端**到有选择性且有索引的属性。从一个已知顶点遍历，与从全部顶点遍历是不同的查询。
2. **命名边标签。** 这是每跳一张表与每跳全部表的区别。
3. **限制长度。** 上界是执行器可以利用的承诺。
4. **对边标签执行 `ANALYZE`。** 遍历成本估算依赖度数估计，未分析的边标签没有度数可供估计。参见[调优查询](/zh/agensgraph/querying/performance/#statistics-on-edge-labels)。

## 清理 {#clean-up}

```cypher
DROP GRAPH routelab CASCADE;
```

## 接下来去哪里 {#where-to-go-next}

* [调优查询](/zh/agensgraph/querying/performance/)——读执行计划，以及改变计划形状的设置。
* [读取图](/zh/agensgraph/querying/reading/)——这些内容构建于其上的固定模式。
* [向量搜索](/zh/agensgraph/guides/search/vector/)——用相似度匹配作为遍历的锚点。
