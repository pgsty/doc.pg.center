---
title: Graph metadata
linkTitle: Graph metadata
description: '<!-- check-examples: skip because every example needs the meta extension. -->'
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/system_catalogs/graph-metadata.html
upstream_source: agensgraph
upstream_modified: true
---


<!-- check-examples: skip because every example needs the `meta` extension. -->

# Graph metadata

## Introduction {#introduction}

The meta extension is a collection of helper functions for AgensGraph that simplify working with graph metadata.
Its functions explore graph structures, validate labels, estimate sizes, analyze relationships, and handle Cypher types.

They let you inspect, monitor, and manage graphs in AgensGraph with less repetition and less effort.

## Installation {#installation}
The meta extension is included in the contrib directory of AgensGraph.
To install it, first build and install AgensGraph with the contrib modules enabled.

Once it is installed, you can add the extension to any database with:

```sql
CREATE EXTENSION meta;
```

That makes all meta functions available in the database.

## Functions {#functions}

The meta extension includes the following functions:

### meta.graphs {#metagraphs}

**Description**  
Returns the list of all graphs available.

**Arguments**  
- None

**Returns**  
- Set of graph names

**Example**  
```sql
SELECT * FROM meta.graphs();

 graphname
-----------
 social
 company
 test
```

### meta.labels {#metalabels}

**Description**  
Returns all labels for a given graph. The system labels `ag_vertex` and `ag_edge` are not included in the result. If the `graph` argument is not provided, the function uses the current `graph_path` setting.

**Arguments**  
- `graph` (name, optional): Name of the graph. Defaults to the current `graph_path`.

**Returns**  
- `label_name` (name): Names of all labels in the specified graph, excluding system labels `ag_vertex` and `ag_edge`.

**Example**  
```sql
SELECT * FROM meta.labels('social');

 label_name
------------
 Person
 Product
 Transaction
```

### meta.vertex_labels {#metavertex_labels}

**Description**  
Returns all vertex labels defined in a given graph. The system label `ag_vertex` is excluded. If the `graph` argument is not provided, the function uses the current `graph_path` setting to determine the graph.

**Arguments**  
- `graph` (name, optional): Name of the graph. Defaults to the current `graph_path`.

**Returns**  
- `label_name` (name): Names of all vertex labels in the specified graph.

**Example**  
```sql
SELECT * FROM meta.vertex_labels('social');

 label_name
------------
 Person
 Product
 Comment
```

### meta.edge_labels {#metaedge_labels}

**Description**
Returns all edge labels defined in a given graph. The system label ag_edge is excluded. If the graph argument is not provided, the function uses the current graph_path setting to determine the graph.

**Arguments**

- `graph` (name, optional): Name of the graph. Defaults to the current `graph_path`.

**Returns**

- `label_name` (name): Names of all edge labels in the specified graph.

**Example**
```sql
SELECT * FROM meta.edge_labels('social');

 label_name
------------
 Follows
 Likes
 Purchases
```

### meta.label_id {#metalabel_id}

**Description**  
Returns the internal id of a specific label in a given graph. If the `graph` argument is not provided, the function uses the current `graph_path` setting. Raises an exception if the label does not exist in the graph.

**Arguments**  
- `label` (name, required): the name of the label whose id is to be retrieved.  
- `graph` (name, optional): name of the graph. defaults to the current `graph_path`.

**Returns**  
- `labid` (int): internal id of the specified label.

**Example**  
```sql
SELECT meta.label_id('Person', 'social');

 labid
-------
     5
```

### meta.label_kind {#metalabel_kind}

**Description**  
Returns the kind of a label (`v` for vertex, `e` for edge) in a given graph. If the `graph` argument is not provided, the function uses the current `graph_path` setting. Returns `NULL` if the label does not exist.

**Arguments**  
- `label` (name, required): the name of the label whose kind is to be retrieved.  
- `graph` (name, optional): name of the graph. defaults to the current `graph_path`.

**Returns**  
- `kind` (char): single character representing the label kind (`v` or `e`).

**Example**  
```sql
SELECT meta.label_kind('Person', 'social');

 kind
------
 v
```

### meta.label_name {#metalabel_name}

**Description**  
Returns the name of a label given its ID (`labid`) or OID in a specific graph. If the `graph` argument is not provided, the function uses the current `graph_path` setting. Raises a notice if the label does not exist.

**Arguments**  
- `labelid` (int, required): the ID or OID of the label.  
- `graph` (name, optional): name of the graph. defaults to the current `graph_path`.

**Returns**  
- `label_name` (text): the name of the label.

**Example**  
```sql
SELECT meta.label_name(5, 'social');

 label_name
------------
 Person
```

### meta.graph_size {#metagraph_size}

**Description**  
Returns the total size of a graph, including all its labels. If the `graph_name` argument is not provided, the function uses the current `graph_path` setting. The size can be returned in a human-readable format or as raw bytes.

**Arguments**  
- `graph_name` (name, optional): the name of the graph. defaults to the current `graph_path`.  
- `pretty` (boolean, optional): if `true` (default), returns a human-readable size (e.g., `42 MB`). if `false`, returns the size in bytes as text.

**Returns**  
- `size` (text): total size of the graph.

**Examples**
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

**Description**  
Returns the total size of a specific label, including its indexes. If the `graph` argument is not provided, the function uses the current `graph_path` setting. The size can be returned in a human-readable format or as raw bytes.

**Arguments**  
- `labelname` (text): the name of the label.  
- `graph` (name, optional): the graph that contains the label. defaults to the current `graph_path`.  
- `pretty` (boolean, optional): if `true` (default), returns a human-readable size (e.g., `42 MB`). if `false`, returns the size in bytes as text.

**Returns**  
- `size` (text): total size of the label including indexes.

**Examples**
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

**Description**  
Returns the exact number of nodes or edges for the specified label. If the `graph` argument is not provided, the function uses the current `graph_path` setting.

**Arguments**  
- `labelname` (text): the label whose elements are being counted.  
- `graph` (name, optional): the graph that contains the label. defaults to the current `graph_path`.

**Returns**  
- `count` (bigint): the exact number of elements (nodes or edges) in the label.

**Example**  
```sql
-- Count all nodes in the 'person' label
SELECT meta.count('person');

-- Count all edges in the 'friendship' label of the 'social' graph
SELECT meta.count('friendship', 'social');
```

### meta.estimated_count {#metaestimated_count}

**Description**  
Returns an estimated number of elements (nodes or edges) for a given label based on PostgreSQL statistics (`pg_class.reltuples`). If the `graph` argument is not provided, the function uses the current `graph_path` setting. This is faster than `meta.count` but may be inaccurate.
> Note: If statistics are not available, the function may return NULL. Run `ANALYZE "graph"."label"` to gather statistics.

**Arguments**  
- `labelname` (text): the label whose estimated element count is returned.  
- `graph` (name, optional): the graph containing the label. defaults to the current `graph_path`.

**Returns**  
- `estimated_count` (bigint): estimated number of elements in the label.

**Example**  
```sql
-- Get estimated count of nodes in the 'person' label
SELECT meta.estimated_count('person');

-- Get estimated count of edges in the 'friendship' label of the 'social' graph
SELECT meta.estimated_count('friendship', 'social');
```

### meta.graph_exists {#metagraph_exists}

**Description**  
Checks whether a graph with the specified name exists.

**Arguments**  
- `graph` (name): Name of the graph to check.

**Returns**  
- `boolean`: `true` if the graph exists, `false` otherwise.

**Example**  
```sql
SELECT meta.graph_exists('social');

 ?column? 
----------
 t
```

### meta.label_exists {#metalabel_exists}

**Description**  
Checks whether a label exists in the specified graph. If the graph is not provided, it uses the current `graph_path` setting.

**Arguments**  
- `labelname` (text): Name of the label to check.  
- `graph` (name, optional): Name of the graph. Defaults to `graph_path` if not provided.

**Returns**  
- `boolean`: `true` if the label exists, `false` otherwise.

**Example**  
```sql
SELECT meta.label_exists('Person', 'social');

 ?column? 
----------
 t
```

### meta.vertex_label_exists {#metavertex_label_exists}

**Description**  
Checks whether a vertex label exists in the specified graph. If the graph is not provided, it uses the current `graph_path` setting.

**Arguments**  
- `labelname` (text): Name of the vertex label to check.  
- `graph` (name, optional): Name of the graph. Defaults to `graph_path` if not provided.

**Returns**  
- `boolean`: `true` if the vertex label exists, `false` otherwise.

**Example**  
```sql
SELECT meta.vertex_label_exists('Person', 'social');

 ?column? 
----------
 t
```

### meta.edge_label_exists {#metaedge_label_exists}

**Description**  
Checks whether an edge label exists in the specified graph. If the graph is not provided, it uses the current `graph_path` setting.

**Arguments**  
- `labelname` (text): Name of the edge label to check.  
- `graph` (name, optional): Name of the graph. Defaults to `graph_path` if not provided.

**Returns**  
- `boolean`: `true` if the edge label exists, `false` otherwise.

**Example**  
```sql
SELECT meta.edge_label_exists('Follows', 'social');

 ?column? 
----------
 t
```

### meta.get_child_labels {#metaget_child_labels}

**Description**  
Returns all child labels that inherit from the specified parent label. If the graph is not provided, it uses the current `graph_path` setting.

**Arguments**  
- `parent_label` (text): Name of the parent label.  
- `graph` (name, optional): Name of the graph. Defaults to `graph_path` if not provided.

**Returns**  
- `table(labelname name)`: A set of child label names.

**Example**  
```sql
SELECT * FROM meta.get_child_labels('Person', 'social');

 labelname 
-----------
 Employee
 Customer
```

### meta.get_parent_labels {#metaget_parent_labels}

**Description**  
Returns all parent labels from which the specified child label inherits. If the graph is not provided, it uses the current `graph_path` setting.

**Arguments**  
- `child_label` (text): Name of the child label.  
- `graph` (name, optional): Name of the graph. Defaults to `graph_path` if not provided.

**Returns**  
- `table(labelname name)`: A set of parent label names.

**Example**  
```sql
SELECT * FROM meta.get_parent_labels('Employee', 'social');

 labelname 
-----------
 Person
```

### meta.cypher_type {#metacypher_type}

**Description**  
Determines the corresponding Cypher type of a given value. Supports standard types, JSON/JSONB, and numeric distinctions.

**Arguments**  
- `element` (anyelement): The value whose Cypher type should be determined.

**Returns**  
- `text`: The Cypher type as a string. Possible values include `INTEGER`, `FLOAT`, `STRING`, `BOOLEAN`, `MAP`, `LIST`, or `NUMBER`.

**Example**  
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

**Description**  
Returns a JSONB object mapping each key of the input JSONB object to its corresponding Cypher type. Raises an error if the input is not a JSON object.

**Arguments**  
- `properties` (jsonb): A JSONB object whose keys will be mapped to Cypher types.

**Returns**  
- `jsonb`: A JSONB object where each key corresponds to the input keys and the values are the detected Cypher types (`INTEGER`, `FLOAT`, `STRING`, `BOOLEAN`, `MAP`, `LIST`, `NULL` or `NUMBER`).

**Example**  
```psql
SELECT meta.cypher_types('{"key": "value", "arr": [1, 2, 3], "num": 123, "float": 45.67, "bool": true, "null": null}'::jsonb);
                                              cypher_types                                               
---------------------------------------------------------------------------------------------------------
 {"arr": "LIST", "key": "STRING", "num": "INTEGER", "bool": "BOOLEAN", "null": "NULL", "float": "FLOAT"}
```

### meta.is_cypher_type {#metais_cypher_type}

**Description**  
Checks if a given value matches the specified Cypher type. Supports types: `NULL`, `INTEGER`, `FLOAT`, `STRING`, `BOOLEAN`, `MAP`, `LIST`, and `NUMBER`.

**Arguments**  
- `value` (anyelement): The value to check.  
- `expected_type` (text): The expected Cypher type.

**Returns**  
- `boolean`: `true` if the value matches the expected type, `false` otherwise.

**Example**  
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

**Description**  
Returns the number of self-loops (edges where the start and end vertices are the same) in a specified graph.  
If no relationship is provided, all edges are considered regardless of edge label. If no graph is provided, the `graph_path` setting is used.

**Arguments**  
- `relationship` (text, optional): The name of the relationship/edge label to check. Defaults to `ag_edge`.  
- `graph` (text, optional): The graph name. Defaults to the `graph_path` setting.

**Returns**  
- `bigint`: Number of self-loop edges.

**Example**  
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

**Description**  
Calculates the edge density of a graph, defined as the ratio of existing edges to the maximum possible number of edges.  
If no graph is provided, the `graph_path` setting is used.

**Arguments**  
- `graph` (name, optional): The graph name. Defaults to the `graph_path` setting.

**Returns**  
- `float`: Edge density of the graph.

**Example**  
```sql
-- Calculate edge density for the current graph
SELECT meta.edge_density() AS result;

-- Calculate edge density for a specific graph
SELECT meta.edge_density('social_graph') AS result;
```

### meta.estimated_edge_density {#metaestimated_edge_density}

**Description**  
Provides an estimated edge density of a graph using PostgreSQL statistics (`pg_class.reltuples`) instead of exact counts.  
This is faster for large graphs but may be inaccurate. Uses `graph_path` if no graph name is provided.

**Arguments**  
- `graph` (name, optional): The graph name. Defaults to the `graph_path` setting.

**Returns**  
- `float`: Estimated edge density of the graph.

**Example**  
```sql
-- Estimate edge density for the current graph
SELECT meta.estimated_edge_density() AS result;

-- Estimate edge density for a specific graph
SELECT meta.estimated_edge_density('social_graph') AS result;
```
