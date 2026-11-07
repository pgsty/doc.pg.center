---
title: 图视图
linkTitle: 图视图
description: pg_catalog 中的两个视图以可读形式呈现图目录，并把 oid 和标签 id 解析为名称。
type: docs
weight: 20
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/system_catalogs/views.html
upstream_source: agensgraph
upstream_modified: true
translation_status: complete
---


`pg_catalog` 中的两个视图以可读形式呈现图目录，把 oid 和标签 id 解析成名称。二者都是普通视图，因此可以对它们做连接和过滤。

## ag_property_indexes {#ag_property_indexes}

每个属性索引一行，并带有一条能重建该索引的语句。

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `graphname` | `name` | 索引所属的图。 |
| `labelname` | `name` | 索引所在的标签。 |
| `indexname` | `name` | 索引名。 |
| `tablespace` | `name` | 表空间；使用默认表空间时为 null。 |
| `unique` | `boolean` | 索引是否唯一。 |
| `indexdef` | `text` | 重建该索引的 `CREATE PROPERTY INDEX` 语句。 |
| `owner` | `name` | 拥有索引的角色。 |
| `size` | `text` | 已格式化的索引大小。 |
| `description` | `text` | 索引上的注释（如果有）。 |

[示例数据集](/zh/agensgraph/get-started/example-dataset/)没有属性索引，所以先创建两个，便于观察结果：

```cypher
CREATE PROPERTY INDEX ON movie (title);
CREATE PROPERTY INDEX ON person (name);
```

```sql
SELECT labelname, indexname, indexdef, size
FROM pg_catalog.ag_property_indexes
WHERE graphname = 'moviekb' ORDER BY labelname, indexname;
```

```
 labelname |    indexname    |                              indexdef                              |  size
-----------+-----------------+--------------------------------------------------------------------+-------
 movie     | movie_title_idx | CREATE PROPERTY INDEX movie_title_idx ON movie USING btree (title) | 16 kB
 person    | person_name_idx | CREATE PROPERTY INDEX person_name_idx ON person USING btree (name) | 16 kB
```

查看完后，可用 `DROP PROPERTY INDEX movie_title_idx;` 再次删除它们。

有用的列是 `indexdef`。它返回属性层面的语句，而不是服务端实际构建的表达式索引；在为模式编写脚本时，需要的正是这种形式。[agens 客户端](/zh/agensgraph/reference/agens/)中的 `\dGi` 输出相同信息。

这个视图既列出[提升列](/zh/agensgraph/querying/typed-columns/)上的索引，也列出属性包上的索引。因此，查询“这个标签上有哪些索引”只需看这里。

## ag_graphmeta_view {#ag_graphmeta_view}

图中出现的每种边形态一行，使用名称而不是标签 id。

| 列 | 类型 | 说明 |
| --- | --- | --- |
| `graphname` | `name` | 图。 |
| `start` | `name` | 边起始顶点的标签。 |
| `edge` | `name` | 边标签。 |
| `end` | `name` | 边结束顶点的标签。 |
| `edgecount` | `bigint` | 这种形态的边有多少条。 |

```sql
SELECT * FROM pg_catalog.ag_graphmeta_view WHERE graphname = 'moviekb';
```

```
 graphname | start  |    edge    |  end  | edgecount
-----------+--------+------------+-------+-----------
 moviekb   | movie  | related_to | movie |        11
 moviekb   | person | directed   | movie |        21
 moviekb   | person | acted_in   | movie |        25
```

这是 AgensGraph 能给出的关于图实际形态最清楚的图景。调优查询前先读它：它会告诉你哪些遍历存在，以及每种遍历有多大。规划器使用的是同样的行。

只有在元数据已收集的情况下，这个视图才有数据。关于 `auto_gather_graphmeta` 和 `regather_graphmeta()` 见[图元数据](/zh/agensgraph/system-catalogs/graph-metadata/)；如果数字看起来不对，再检查 `ag_graph.graphmeta_valid`。
