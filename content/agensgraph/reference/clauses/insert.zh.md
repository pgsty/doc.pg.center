---
title: INSERT 子句
linkTitle: INSERT 子句
description: 创建模式描述的顶点和边。
type: docs
weight: 110
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/reference/clauses/insert.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


**GQL 子句**  **2.18 新增**

创建模式描述的顶点和边。它是 Cypher 中 `CREATE` 子句的 GQL 名称。

## 语法概要 {#synopsis}

```text
INSERT [ path_variable = ] pattern [, [ path_variable = ] pattern ] ...
```

**记法：** 大写为关键字，小写为占位符，`[ ]` 表示可选，`...` 表示可重复。参见[语法约定](/zh/agensgraph/reference/syntax/)。

## 描述 {#description}

`INSERT` 与 [`CREATE`](/zh/agensgraph/reference/clauses/create/)
是同一个子句的两个名称。解析器会为二者构建相同的树，因此它们接受相同模式、引发相同错误并产生相同执行计划。

- 模式中的每个元素都会被创建；已绑定到作用域内变量的元素除外。该元素会被复用为端点，不会被复制。
- 一个 `INSERT` 对每个输入行运行一次。前面没有子句时，它运行一次。
- 模式绑定的变量对其后的子句可见，也对同一 `INSERT` 中后面的模式可见。
- 每条边都恰好需要一个标签和一个方向。标签必须已经存在，除非开启
  `enable_graph_ddl` 以隐式创建它们。

## 参数 {#parameters}

path_variable
: 可选名称，绑定到模式创建的整条路径。返回它会得到一个 `graphpath`
  值，按顺序列出新顶点和新边。

pattern
: 顶点或路径模式，如[语法](/zh/agensgraph/reference/syntax/)所述。属性映射可以内联编写
  （`{title: 'Tenet'}`），也可以用 `=` 从表达式整体提供，包括 SQL 子查询。

## 示例 {#examples}

所有示例都基于[示例数据集](/zh/agensgraph/get-started/example-dataset/)运行。

添加一部电影。`INSERT` 与 `CREATE` 可以互换。切换标签页比较：

{{< tabs >}}
{{< tab label="GQL — INSERT" >}}
```cypher
INSERT (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```
{{< /tab >}}
{{< tab label="Cypher — CREATE" >}}
```cypher
CREATE (:movie {title: 'Tenet', year: 2020, genre: 'Action'});
```
{{< /tab >}}
{{< /tabs >}}
```
UPDATE 1
```

二者的执行计划相同：

```cypher
EXPLAIN (COSTS OFF) INSERT (:movie {title: 'Tenet'});
```

```
  QUERY PLAN
--------------
 Graph Create
   ->  Result
(2 rows)
```

### 返回创建的内容 {#return-what-you-created}

`INSERT` 与其他子句一样绑定变量，因此后面的 `RETURN` 可以报告它们：

```cypher
INSERT (p:person {name: 'John David Washington', born: 1984}) RETURN p.name AS person;
```

```
         person
-------------------------
 "John David Washington"
(1 row)
```

### 把新元素连接到图中已有元素 {#attach-a-new-element-to-one-already-in-the-graph}

由前面 `MATCH` 绑定的变量是端点，不是新顶点，因此只创建边：

```cypher
MATCH (p:person {name: 'Christopher Nolan'}), (m:movie {title: 'Tenet'})
INSERT (p)-[:directed]->(m)
RETURN count(*) AS edges;
```

```
 edges
-------
 1
(1 row)
```

### 在一个子句中构建多个模式 {#build-several-patterns-in-one-clause}

模式用逗号分隔，可以引用更早模式绑定的变量：

```cypher
MATCH (m:movie {title: 'Tenet'})
INSERT (a:person {name: 'Robert Pattinson', born: 1986}),
       (b:person {name: 'Elizabeth Debicki', born: 1990}),
       (a)-[:acted_in {role: 'Neil'}]->(m),
       (b)-[:acted_in {role: 'Kat'}]->(m);
```

```
UPDATE 4
```

该标签统计的是这一个子句创建的四个元素：

```cypher
MATCH (p:person)-[r:acted_in]->(:movie {title: 'Tenet'})
RETURN p.name AS actor, r.role AS role ORDER BY actor;
```

```
        actor        |  role
---------------------+--------
 "Elizabeth Debicki" | "Kat"
 "Robert Pattinson"  | "Neil"
(2 rows)
```

### 从 SQL 查询取得属性映射 {#take-a-property-map-from-a-sql-query}

`= expression` 形式可以一次性提供整个映射。用它把表中的属性加载出来：

```cypher
INSERT (:movie = (SELECT jsonb_build_object('title', 'Dunkirk', 'year', 2017)));
```

```
UPDATE 1
```

```cypher
MATCH (m:movie {title: 'Dunkirk'}) RETURN m.year AS year;
```

```
 year
------
 2017
(1 row)
```

## 说明 {#notes}

该子句报告普通的图写入命令标签 `UPDATE n`，而不是 `CREATE`
标签。当你只想写入而不投影时，可将它与 [`FINISH`](/zh/agensgraph/reference/clauses/finish/) 搭配。

即使你写的是 `INSERT`，拒绝信息也会使用 `CREATE`，因为两种拼写构建的是同一个子句。以下几类值得了解：

| 模式 | 错误 |
| --- | --- |
| `INSERT ()-[]->()` | `only one relationship type is allowed for CREATE` |
| `INSERT ()-[:acted_in\|directed]->()` | `only one relationship type is allowed for CREATE` |
| `INSERT ()-[:directed]-()` | `only directed relationships are allowed in CREATE` |
| `INSERT (:ag_vertex)` | `specifying default label is not allowed` |
| `INSERT ()-[:ag_edge]->()` | `cannot create edge on default label` |
| `INSERT (:directed)` | `label "directed" is edge label` |
| `INSERT ()-[:movie]->()` | `label "movie" is vertex label` |
| 已绑定 `m` 时使用 `INSERT (m)` | `there must be at least one relationship` |

> [!NOTE]
> `insert` 在 2.18 中成为保留关键字。在语法仍无歧义的位置，它仍可不加引号使用——例如变量名
> `MATCH (insert:person)`，以及模式中的标签名 `MATCH (n:insert)`。它不能用作
> `CREATE VLABEL` 名称、命名 `RETURN` 别名的 `ORDER BY` 键，或 SQL 表名/列名；在这些位置请写
> `"insert"` 或改名。

## 兼容性 {#compatibility}

> [!NOTE] GQL conformance
> :class: gql-conformance
>
> 基于 §16.5 的 *insert graph pattern*，实现 GQL *INSERT statement*
> （ISO/IEC 39075:2024 §13.2）。
>
> - **支持**——插入节点和边、每条语句多个模式、复用已绑定元素作为端点、内联属性映射，以及覆盖被插入模式的路径变量。
> - **不支持**——标准的类型化图检查（§18），它需要图类型；AgensGraph
>   的图是非类型化的，因此插入会根据已有标签校验，而不是根据声明的节点或边类型校验。
>
> 在 [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)中跟踪状态。

### openCypher {#opencypher}

openCypher 将该子句写作 `CREATE`，AgensGraph 接受它作为同义词。`INSERT`
名称来自 GQL，也来自 SQL；在 SQL 中，它对表执行同样的工作。

## 另见 {#see-also}

- [`CREATE`](/zh/agensgraph/reference/clauses/create/)——Cypher 同义词，同一个子句
- [`MERGE`](/zh/agensgraph/reference/clauses/merge/)——只创建尚不存在的内容
- [`FOR`](/zh/agensgraph/reference/clauses/for/) **GQL**——按列表元素驱动 `INSERT`
- [`FINISH`](/zh/agensgraph/reference/clauses/finish/) **GQL**——只写入而不投影
- [语法](/zh/agensgraph/reference/syntax/)——`INSERT` 使用的模式语法
- [GQL 兼容性矩阵](/zh/agensgraph/appendix/gql-conformance/)
