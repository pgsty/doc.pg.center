---
title: 术语表
linkTitle: 术语表
description: 本手册使用的词汇，并为每个术语链接到正式讲解它的页面。
type: docs
weight: 60
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/appendix/glossary.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


本手册使用的词汇，并为每个术语链接到正式讲解它的页面。术语按描述对象分组，而不是按字母排序，因为其中一些术语只有放在一起才有意义。

## 模型 {#the-model}

property graph（属性图）
: 一种数据模型：数据是由边连接的一组顶点，顶点和边都携带命名值。AgensGraph 把一个属性图和一组关系表存放在同一数据库中，并且一条语句可以同时读取二者。见[属性图模型](/zh/agensgraph/concepts/property-graph-model/)。

graph（图）
: 一个有名称的属性图。它是一组标签的容器，也是 `graph_path` 选择的单位。图是 PostgreSQL 模式，用 `CREATE GRAPH` 创建。见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

vertex（顶点）
: 图中的一个实体：一个人、一部电影、一个账户。顶点有一个身份标识、恰好一个标签和一组属性。它打印为 `label[graphid]{properties}`，例如 `movie[3.7]{"title": "Avatar"}`。见[属性图模型](/zh/agensgraph/concepts/property-graph-model/)。

edge（边）
: 两个顶点之间的一条有向连接，带有自己的标签和属性。边不能脱离两个端点存在。每条边都是有向的，但模式可以从任一方向遍历它。见[属性图模型](/zh/agensgraph/concepts/property-graph-model/)。

property（属性）
: 顶点或边上的一个命名值，例如 `title`、`year` 或 `weight`。属性是无模式的：同一标签的两个顶点不必携带相同键。它们存放在每个元素的一个 `jsonb` 文档中。属性键不是标识符，因此不受关键字保留和大小写折叠影响。见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

label（标签）
: 对顶点或边分类的名称，也是存储单位：标签是 PostgreSQL 表。顶点恰好有一个标签，并且创建后不能更改。没有标签集合。见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

vlabel（顶点标签）
: 顶点标签，即由 `CREATE VLABEL` 创建的类型。它的表为 `(id graphid, properties jsonb)`，并继承所在图的 `ag_vertex`。见[数据定义](/zh/agensgraph/reference/ddl/)。

elabel（边标签）
: 边标签，即由 `CREATE ELABEL` 创建的类型。它的表在顶点标签的列之外增加 `start` 和 `end`，并继承所在图的 `ag_edge`。见[数据定义](/zh/agensgraph/reference/ddl/)。

label inheritance（标签继承）
: 一个标签可以继承另一个标签，因此匹配父标签时也会返回每个子标签的行。这就是一个实体同时扮演多个角色的方式，用来代替标签集合。`MATCH (n:parent ONLY)` 可以退出继承。见[标签继承](/zh/agensgraph/concepts/label-inheritance/)。

## 身份与寻址 {#identity-and-addressing}

graphid
: 顶点或边的身份标识，也是一等类型。它是一个 64 位值，打印为两个数字：*标签 id*`.`*本地 id*。因此 `3.7` 是标签 3 的第 7 行。`id(n)` 返回它；`n.id` 不会，因为 `id` 只是一个普通属性名。见[限制](/zh/agensgraph/appendix/limits/)。

graph_path
: 指定语句作用于哪个图的设置。它没有默认值：未设置 `graph_path` 时，每条图语句都会以 `ERROR: graph_path is NULL` 拒绝。可在会话中用 `SET graph_path = name` 设置，也可按角色或集群设置。见[配置](/zh/agensgraph/operations/configuration/)。

## 查询 {#querying}

path（路径）
: 由顶点和边交替组成的序列，由模式产生而不是由构造函数产生。`MATCH p = (a)-[e]->(b)` 会把一条路径绑定为 `graphpath` 类型的值，随后 `nodes()`、`relationships()` 和 `length()` 可以读取它。见[读取图](/zh/agensgraph/querying/reading/)。

traversal（遍历）
: 沿边从一个顶点到达其他顶点。图查询以此代替按键连接。深度未知的遍历写作带量词的边，`-[r*1..3]->`。见[读取图](/zh/agensgraph/querying/reading/)。

property index（属性索引）
: 属性表达式上的索引，用 `CREATE PROPERTY INDEX ON label (key)` 创建。它是 PostgreSQL 索引，键是建立在 `properties` 文档上的表达式；普通 `CREATE INDEX` 无法表达这个键。见[图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)。

promoted column（提升列）
: 拥有真实列和已声明类型的属性，由 `properties` 文档生成并存储。属性读取会解析到该列，因此它上面的普通索引可以服务查询，值也保留自己的类型。示例数据集中的 `movie.year` 就是一个提升列。见[`CREATE VLABEL`](/zh/agensgraph/reference/ddl/create-vlabel/)和[`ALTER VLABEL`](/zh/agensgraph/reference/ddl/alter-label/)。

## 语言 {#the-languages}

Cypher
: AgensGraph 一直接受的图查询语言。它是声明式语言，通过在 ASCII 中画出模式来匹配。AgensGraph 的方言与其他实现接近但不相同。见[Cypher、GQL 和 SQL](/zh/agensgraph/concepts/languages/)与[Cypher 兼容性](/zh/agensgraph/appendix/cypher-compatibility/)。

GQL
: ISO/IEC 39075:2024，图查询语言的国际标准。2.18 版实现了其中相当大的一部分，包括语句 `LET`、`NEXT`、`FILTER`、`FINISH`、`INSERT` 和 `FOR`。GQL 不是独立模式：它的语句与 Cypher 语句可在同一条流水线中自由混合。见[GQL 一致性](/zh/agensgraph/appendix/gql-conformance/)。

## 另见 {#see-also}

- [属性图模型](/zh/agensgraph/concepts/property-graph-model/)——带完整示例的模型说明
- [图如何存储](/zh/agensgraph/concepts/graph-on-postgresql/)——上述每个术语如何存储
- [示例数据集](/zh/agensgraph/get-started/example-dataset/)——所有示例使用的图
