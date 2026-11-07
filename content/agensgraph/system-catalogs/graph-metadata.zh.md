---
title: 图元数据
linkTitle: 图元数据
description: '<!-- check-examples: skip because every example needs the meta extension. -->'
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/system_catalogs/graph-metadata.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


<!-- check-examples: skip because every example needs the `meta` extension. -->

# 图元数据

## 简介 {#introduction}

meta 扩展是一组面向 AgensGraph 的辅助函数，用于简化图元数据的操作。它的函数可以探索图结构、校验标签、估算大小、分析关系并处理 Cypher 类型。

这些函数让你能用更少的重复操作和更低的成本在 AgensGraph 中检查、监控和管理图。

## 安装 {#installation}

meta 扩展包含在 AgensGraph 的 contrib 目录中。安装它之前，请先构建并安装启用了 contrib 模块的 AgensGraph。

安装完成后，可用以下语句把扩展加入任何数据库：

```sql
CREATE EXTENSION meta;
```

这会使所有 meta 函数在该数据库中可用。

## 函数 {#functions}

meta 扩展包含以下函数：

### meta.graphs {#metagraphs}

**说明**  
返回所有可用图的列表。

**参数**  
- 无

**返回**  
- 图名集合

**示例**  
```sql
SELECT * FROM meta.graphs();

 graphname
-----------
 social
 company
 test
```

### meta.labels {#metalabels}

**说明**  
返回给定图的所有标签。结果不包含系统标签 `ag_vertex` 和 `ag_edge`。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。

**参数**  
- `graph`（name，可选）：图名。默认为当前 `graph_path`。

**返回**  
- `label_name`（name）：指定图中所有标签的名称，不含系统标签 `ag_vertex` 和 `ag_edge`。

**示例**  
```sql
SELECT * FROM meta.labels('social');

 label_name
------------
 Person
 Product
 Transaction
```

### meta.vertex_labels {#metavertex_labels}

**说明**  
返回给定图中定义的所有顶点标签。系统标签 `ag_vertex` 不在其中。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置来确定图。

**参数**  
- `graph`（name，可选）：图名。默认为当前 `graph_path`。

**返回**  
- `label_name`（name）：指定图中所有顶点标签的名称。

**示例**  
```sql
SELECT * FROM meta.vertex_labels('social');

 label_name
------------
 Person
 Product
 Comment
```

### meta.edge_labels {#metaedge_labels}

**说明**
返回给定图中定义的所有边标签。系统标签 ag_edge 不在其中。如果未提供 graph 参数，函数使用当前 graph_path 设置来确定图。

**参数**

- `graph`（name，可选）：图名。默认为当前 `graph_path`。

**返回**

- `label_name`（name）：指定图中所有边标签的名称。

**示例**
```sql
SELECT * FROM meta.edge_labels('social');

 label_name
------------
 Follows
 Likes
 Purchases
```

### meta.label_id {#metalabel_id}

**说明**  
返回给定图中特定标签的内部 id。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。标签在图中不存在时抛出异常。

**参数**  
- `label`（name，必填）：要获取 id 的标签名。  
- `graph`（name，可选）：图名。默认为当前 `graph_path`。

**返回**  
- `labid`（int）：指定标签的内部 id。

**示例**  
```sql
SELECT meta.label_id('Person', 'social');

 labid
-------
     5
```

### meta.label_kind {#metalabel_kind}

**说明**  
返回给定图中标签的种类（`v` 表示顶点，`e` 表示边）。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。标签不存在时返回 `NULL`。

**参数**  
- `label`（name，必填）：要获取种类的标签名。  
- `graph`（name，可选）：图名。默认为当前 `graph_path`。

**返回**  
- `kind`（char）：表示标签种类的单个字符（`v` 或 `e`）。

**示例**  
```sql
SELECT meta.label_kind('Person', 'social');

 kind
------
 v
```

### meta.label_name {#metalabel_name}

**说明**  
根据特定图中标签的 ID（`labid`）或 OID 返回标签名。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。标签不存在时发出提示。

**参数**  
- `labelid`（int，必填）：标签的 ID 或 OID。  
- `graph`（name，可选）：图名。默认为当前 `graph_path`。

**返回**  
- `label_name`（text）：标签名。

**示例**  
```sql
SELECT meta.label_name(5, 'social');

 label_name
------------
 Person
```

### meta.graph_size {#metagraph_size}

**说明**  
返回图的总大小，包括其所有标签。如果未提供 `graph_name` 参数，函数使用当前 `graph_path` 设置。大小可以按人类可读格式返回，也可以按原始字节数返回。

**参数**  
- `graph_name`（name，可选）：图名。默认为当前 `graph_path`。  
- `pretty`（boolean，可选）：为 `true`（默认）时返回人类可读的大小（例如 `42 MB`）；为 `false` 时以文本形式返回字节数。

**返回**  
- `size`（text）：图的总大小。

**示例**
```sql
SELECT meta.graph_size('social');

 graph_size
------------
 123 MB

SELECT meta.graph_size('social', false);

 graph_size
------------
 129394816
```

### meta.label_size {#metalabel_size}

**说明**  
返回特定标签的总大小，包括其索引。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。大小可以按人类可读格式返回，也可以按原始字节数返回。

**参数**  
- `labelname`（text）：标签名。  
- `graph`（name，可选）：包含标签的图。默认为当前 `graph_path`。  
- `pretty`（boolean，可选）：为 `true`（默认）时返回人类可读的大小（例如 `42 MB`）；为 `false` 时以文本形式返回字节数。

**返回**  
- `size`（text）：标签总大小，包括索引。

**示例**
```sql
SELECT meta.label_size('person');

 label_size
------------
 42 MB

SELECT meta.label_size('person', pretty => false);

 label_size
------------
 44040192
```

### meta.count {#metacount}

**说明**  
返回指定标签的节点或边的确切数量。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。

**参数**  
- `labelname`（text）：要统计元素的标签。  
- `graph`（name，可选）：包含标签的图。默认为当前 `graph_path`。

**返回**  
- `count`（bigint）：标签中元素（节点或边）的确切数量。

**示例**  
```sql
-- Count all nodes in the 'person' label
SELECT meta.count('person');

-- Count all edges in the 'friendship' label of the 'social' graph
SELECT meta.count('friendship', 'social');
```

### meta.estimated_count {#metaestimated_count}

**说明**  
基于 PostgreSQL 统计信息（`pg_class.reltuples`）返回给定标签元素（节点或边）的估算数量。如果未提供 `graph` 参数，函数使用当前 `graph_path` 设置。它比 `meta.count` 更快，但可能不准确。
> 注意：统计信息不可用时，函数可能返回 NULL。运行 `ANALYZE "graph"."label"` 可收集统计信息。

**参数**  
- `labelname`（text）：要返回元素估算数的标签。  
- `graph`（name，可选）：包含标签的图。默认为当前 `graph_path`。

**返回**  
- `estimated_count`（bigint）：标签中元素的估算数量。

**示例**  
```sql
-- Get estimated count of nodes in the 'person' label
SELECT meta.estimated_count('person');

-- Get estimated count of edges in the 'friendship' label of the 'social' graph
SELECT meta.estimated_count('friendship', 'social');
```

### meta.graph_exists {#metagraph_exists}

**说明**  
检查指定名称的图是否存在。

**参数**  
- `graph`（name）：要检查的图名。

**返回**  
- `boolean`：图存在为 `true`，否则为 `false`。

**示例**  
```sql
SELECT meta.graph_exists('social');

 ?column? 
----------
 t
```

### meta.label_exists {#metalabel_exists}

**说明**  
检查标签是否存在于指定图。如果未提供图，则使用当前 `graph_path` 设置。

**参数**  
- `labelname`（text）：要检查的标签名。  
- `graph`（name，可选）：图名。未提供时默认为 `graph_path`。

**返回**  
- `boolean`：标签存在为 `true`，否则为 `false`。

**示例**  
```sql
SELECT meta.label_exists('Person', 'social');

 ?column? 
----------
 t
```

### meta.vertex_label_exists {#metavertex_label_exists}

**说明**  
检查顶点标签是否存在于指定图。如果未提供图，则使用当前 `graph_path` 设置。

**参数**  
- `labelname`（text）：要检查的顶点标签名。  
- `graph`（name，可选）：图名。未提供时默认为 `graph_path`。

**返回**  
- `boolean`：顶点标签存在为 `true`，否则为 `false`。

**示例**  
```sql
SELECT meta.vertex_label_exists('Person', 'social');

 ?column? 
----------
 t
```

### meta.edge_label_exists {#metaedge_label_exists}

**说明**  
检查边标签是否存在于指定图。如果未提供图，则使用当前 `graph_path` 设置。

**参数**  
- `labelname`（text）：要检查的边标签名。  
- `graph`（name，可选）：图名。未提供时默认为 `graph_path`。

**返回**  
- `boolean`：边标签存在为 `true`，否则为 `false`。

**示例**  
```sql
SELECT meta.edge_label_exists('Follows', 'social');

 ?column? 
----------
 t
```

### meta.get_child_labels {#metaget_child_labels}

**说明**  
返回继承自指定父标签的所有子标签。如果未提供图，则使用当前 `graph_path` 设置。

**参数**  
- `parent_label`（text）：父标签名。  
- `graph`（name，可选）：图名。未提供时默认为 `graph_path`。

**返回**  
- `table(labelname name)`：子标签名集合。

**示例**  
```sql
SELECT * FROM meta.get_child_labels('Person', 'social');

 labelname 
-----------
 Employee
 Customer
```

### meta.get_parent_labels {#metaget_parent_labels}

**说明**  
返回指定子标签继承的所有父标签。如果未提供图，则使用当前 `graph_path` 设置。

**参数**  
- `child_label`（text）：子标签名。  
- `graph`（name，可选）：图名。未提供时默认为 `graph_path`。

**返回**  
- `table(labelname name)`：父标签名集合。

**示例**  
```sql
SELECT * FROM meta.get_parent_labels('Employee', 'social');

 labelname 
-----------
 Person
```

### meta.cypher_type {#metacypher_type}

**说明**  
判断给定值对应的 Cypher 类型。支持标准类型、JSON/JSONB 和数字区分。

**参数**  
- `element`（anyelement）：要判断 Cypher 类型的值。

**返回**  
- `text`：字符串形式的 Cypher 类型。可能值包括 `INTEGER`、`FLOAT`、`STRING`、`BOOLEAN`、`MAP`、`LIST` 或 `NUMBER`。

**示例**  
```psql
SELECT meta.cypher_type(42) AS result;
result
-------
INTEGER

SELECT meta.cypher_type('{"key": "value"}'::jsonb) AS result;
result
-------
MAP
```

### meta.cypher_types {#metacypher_types}

**说明**  
返回一个 JSONB 对象，把输入 JSONB 对象的每个键映射到对应的 Cypher 类型。输入不是 JSON 对象时抛出错误。

**参数**  
- `properties`（jsonb）：键将被映射到 Cypher 类型的 JSONB 对象。

**返回**  
- `jsonb`：一个 JSONB 对象，键与输入相同，值是检测到的 Cypher 类型（`INTEGER`、`FLOAT`、`STRING`、`BOOLEAN`、`MAP`、`LIST`、`NULL` 或 `NUMBER`）。

**示例**  
```psql
SELECT meta.cypher_types('{"key": "value", "arr": [1, 2, 3], "num": 123, "float": 45.67, "bool": true, "null": null}'::jsonb);
                                              cypher_types                                               
---------------------------------------------------------------------------------------------------------
 {"arr": "LIST", "key": "STRING", "num": "INTEGER", "bool": "BOOLEAN", "null": "NULL", "float": "FLOAT"}
```

### meta.is_cypher_type {#metais_cypher_type}

**说明**  
检查给定值是否匹配指定 Cypher 类型。支持类型：`NULL`、`INTEGER`、`FLOAT`、`STRING`、`BOOLEAN`、`MAP`、`LIST` 和 `NUMBER`。

**参数**  
- `value`（anyelement）：要检查的值。  
- `expected_type`（text）：预期的 Cypher 类型。

**返回**  
- `boolean`：值匹配预期类型为 `true`，否则为 `false`。

**示例**  
```sql
SELECT meta.is_cypher_type(123, 'INTEGER') AS result;
result
-------
t

SELECT meta.is_cypher_type('Alice', 'STRING') AS result;
result
-------
t

SELECT meta.is_cypher_type('NULL'::jsonb, 'NULL') AS result;
result
-------
t
```

### meta.count_self_loops {#metacount_self_loops}

**说明**  
返回指定图中自环（起点和终点为同一顶点的边）的数量。  
如果未提供关系，则不考虑边标签，统计所有边。如果未提供图，则使用 `graph_path` 设置。

**参数**  
- `relationship`（text，可选）：要检查的关系/边标签名。默认为 `ag_edge`。  
- `graph`（text，可选）：图名。默认为 `graph_path` 设置。

**返回**  
- `bigint`：自环边数量。

**示例**  
```psql
MATCH (a:person {name: 'Bob'})
CREATE (a)-[:"KNOWS"]->(a);
MATCH (a:animal {name: 'Spot'})
CREATE (a)-[:"HAS_PET"]->(a);
SELECT meta.count_self_loops(graph=>'social');
 count_self_loops 
------------------
                2
(1 row)

SELECT meta.count_self_loops('HAS_PET');
 count_self_loops 
------------------
                1
(1 row)
```

### meta.edge_density {#metaedge_density}

**说明**  
计算图的边密度，定义为现有边数与最大可能边数之比。  
如果未提供图，则使用 `graph_path` 设置。

**参数**  
- `graph`（name，可选）：图名。默认为 `graph_path` 设置。

**返回**  
- `float`：图的边密度。

**示例**  
```sql
-- Calculate edge density for the current graph
SELECT meta.edge_density() AS result;

-- Calculate edge density for a specific graph
SELECT meta.edge_density('social_graph') AS result;
```

### meta.estimated_edge_density {#metaestimated_edge_density}

**说明**  
使用 PostgreSQL 统计信息（`pg_class.reltuples`）而不是精确计数，提供图的边密度估算。  
这对大图更快，但可能不准确。未提供图名时使用 `graph_path`。

**参数**  
- `graph`（name，可选）：图名。默认为 `graph_path` 设置。

**返回**  
- `float`：图的边密度估算值。

**示例**  
```sql
-- Estimate edge density for the current graph
SELECT meta.estimated_edge_density() AS result;

-- Estimate edge density for a specific graph
SELECT meta.estimated_edge_density('social_graph') AS result;
```
