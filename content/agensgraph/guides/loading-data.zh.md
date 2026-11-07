---
title: 加载数据
linkTitle: 加载数据
description: 把数据写入图有三种方式，合适的选择取决于数据量。
type: docs
weight: 10
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/guides/loading-data.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


把数据写入图有三种方式，合适的选择取决于数据量。

| 途径 | 适合 | 速度 |
| --- | --- | --- |
| Cypher `CREATE` / `MERGE` | 最多几十万个元素；任何希望由 Cypher 执行检查的场景 | 单行最慢，最安全 |
| 从表 `LOAD FROM` | 已经在表中的数据，或由外部表暴露的文件 | 快，而且保持在 Cypher 内 |
| `COPY` 到标签表 | 数百万个元素，来自你可控制的文件 | 大幅领先，最快 |

无论使用哪一种，[批量加载期间的索引](#indexes-during-a-bulk-load)一节都适用，[加载之后](#after-the-load)清单也一样。跳过第二个清单，是刚加载的图查询表现不好的常见原因。

## Cypher CREATE {#cypher-create}

这是最直观的途径，在它变得太慢之前都可以使用。请批量执行：一条语句创建多个元素，优于多条语句各创建一个：

```cypher
CREATE (:person {name: 'Ann', born: 1990}),
       (:person {name: 'Bo',  born: 1985}),
       (:person {name: 'Cy',  born: 1979});
```

边需要先找到两个端点，因此在同一条语句中匹配它们：

```cypher
MATCH (a:person {name: 'Ann'}), (b:person {name: 'Bo'})
CREATE (a)-[:knows {since: 2019}]->(b);
```

每次用一个 `MATCH` 加载边，正是这条途径慢的原因：每条语句都要重新查找端点。如果批量加载边，请使用另外两条途径，让服务端把查找作为连接完成。

如果加载可能执行两次而你希望它幂等，用 `MERGE` 替代 `CREATE`；但要注意它会给每个元素带来一次查找。

## 从表 LOAD FROM {#load-from-a-table}

`LOAD FROM` 从普通表读取行并交给 Cypher 写入子句，因此端点查找变成一次连接，而不是每行一次查询。数据已经是关系形态时，这是自然途径。文件也算：只要 `file_fdw` 把它暴露为外部表即可。

假设这些行已经进入两个临时表：

```sql
CREATE TABLE staging_people (name text, born int);
INSERT INTO staging_people VALUES ('Ann', 1990), ('Bo', 1985);

CREATE TABLE staging_knows (from_name text, to_name text, since int);
INSERT INTO staging_knows VALUES ('Ann', 'Bo', 2019);
```

然后一条语句把每行变成一个顶点：

```cypher
LOAD FROM staging_people AS row
CREATE (:person {name: row.name, born: row.born});
```

也可以把整行作为属性映射：

```cypher
LOAD FROM staging_people AS row
CREATE (:person = to_jsonb(row_to_json(row)));
```

边才是重点，因为速度正来自连接：

```cypher
LOAD FROM staging_knows AS row
MATCH (a:person {name: row.from_name}), (b:person {name: row.to_name})
CREATE (a)-[:knows {since: row.since}]->(b);
```

运行前，请为参与匹配的属性建索引；见下文。

### 把文件作为表读取 {#reading-a-file-as-a-table}

`file_fdw` 把服务端文件系统上的文件变成只读表。它是一个 contrib 模块，因此构建时需要 `make install-world`（参见[安装 AgensGraph](/zh/agensgraph/get-started/install/#build-and-install)）：

> [!NOTE]
> 下面两个代码块需要 `file_fdw`，因此是本页唯一没有构建 contrib 模块就无法运行的部分。

<!-- check-examples: skip-next needs the file_fdw contrib module -->
```sql
CREATE EXTENSION file_fdw;
CREATE SERVER import FOREIGN DATA WRAPPER file_fdw;

CREATE FOREIGN TABLE staging_people (name text, born int)
SERVER import
OPTIONS (filename '/data/people.csv', format 'csv', header 'true');
```

然后按上文执行 `LOAD FROM staging_people AS row …`。文件在服务端读取，所以路径是服务端路径，服务端用户也必须能读取它。

如果文件在你的机器上而不是服务端上，请先用 [agens 客户端](/zh/agensgraph/reference/agens/)中的 `\copy` 把它装入普通表，再从该表 `LOAD FROM`。

## COPY 到标签表 {#copy-into-the-label-tables}

这是最快的途径，适合数百万个元素。[标签就是表](/zh/agensgraph/concepts/graph-on-postgresql/)，因此可以直接向它 `COPY`。你直接写 `properties` 列，让 `id` 列的默认值自行填充。

用 SQL 写入标签受开关保护，因此加载期间要打开它：

```psql
SET enable_graph_dml = on;

COPY moviekb.person (properties) FROM STDIN;
{"name": "Ann", "born": 1990}
{"name": "Bo", "born": 1985}
\.
```

边还要提供两个端点 id，格式为 `labid.locid`：

```psql
SET enable_graph_dml = on;

COPY moviekb.acted_in (start, "end", properties) FROM STDIN;
4.1	3.1	{"role": "Neo"}
4.2	3.1	{"role": "Trinity"}
\.
```

因此工作在于生成这些 id。有两种方式：

**用算术构造。** 如果编号由你控制，`graphid()` 可以用标签 id 和局部 id 组成 id：

```sql
SELECT graphid(graph_labid('moviekb.person'::cstring), 100::int8);
```

```
 made_id
---------
 4.100
```

因此，一个分配行号的加载器可以同时输出顶点 id 以及引用这些 id 的边端点，完全不需要查找。这是可能达到的最快加载。

**或用连接解析。** 先加载顶点，然后按业务键连接临时表来构造边行：

```sql
CREATE TABLE staging_roles (person_name text, movie_title text, role text);
INSERT INTO staging_roles VALUES ('Keanu Reeves', 'The Matrix', 'Neo (again)');

SET enable_graph_dml = on;

INSERT INTO moviekb.acted_in (start, "end", properties)
SELECT p.id, m.id, jsonb_build_object('role', s.role)
FROM staging_roles s
  JOIN moviekb.person p ON p.properties->>'name'  = s.person_name
  JOIN moviekb.movie  m ON m.properties->>'title' = s.movie_title;
```

这是一条面向集合的语句，而不是每条边一次查询，这正是它的意义。请先为参与连接的键建索引。

```sql
DROP TABLE staging_roles;
```

> [!WARNING]
> `COPY` 和 `INSERT` 会绕过 Cypher 执行的检查。没有任何机制阻止你写入一条 `start` 指向不存在顶点的边；结果是任何查询都无法正确遍历这个图。加载前验证端点，加载后再把 `enable_graph_dml` 关闭。

## 批量加载期间的索引 {#indexes-during-a-bulk-load}

在数百万行到达时维护索引代价很高。创建标签时可以关闭其索引：

```cypher
CREATE VLABEL bulk_person DISABLE INDEX;
```

也可以稍后关闭：

```cypher
ALTER VLABEL bulk_person DISABLE INDEX;
```

加载数据，然后重建：

```cypher
REINDEX VLABEL bulk_person;
```

> [!NOTE]
> 没有 `ENABLE INDEX`。`ALTER VLABEL person ENABLE INDEX` 是语法错误；让索引恢复可用的是 `REINDEX`。运行它之前，标签的索引存在但不可用，查询会退回顺序扫描，唯一约束也不会被强制执行。

还有两点有助于大型加载：

**在数据之后创建属性索引，而不是之前**——在完整标签上一次性构建索引，远比逐行维护便宜。[把属性提升为列](/zh/agensgraph/querying/typed-columns/)也一样：`ALTER` 会重写整个标签，所以应在加载之后提升一次，而不是之前。

**对可以重载的数据考虑非日志标签。** 它完全跳过 WAL：

```cypher
CREATE UNLOGGED VLABEL staging_person;
```

非日志标签不能在崩溃后保留，也不会被复制。因此它适合临时数据和你能够重建的图，不适合最终数据。

在 reindex 前调高 `maintenance_work_mem`；它一次只被一个命令使用，因此临时设一个较大的值是安全的。参见[配置](/zh/agensgraph/operations/configuration/#memory)。

## 加载之后 {#after-the-load}

三个步骤，没有一步可选。

**如果禁用了索引，按上文重建索引。**

**提升你要过滤和排序的属性**（如果你确实打算这么做）。`ALTER VLABEL person ADD COLUMN age int GENERATED` 会为属性 `age` 在 jsonb 包旁边建立真正的 `int` 列，在写入时填充；列上的索引就是普通列索引。查询继续命名的是属性键——`p.age` 仍然读取 `age`，列名不会出现在 Cypher 中。如果列名需要不同于键名，使用 `GENERATED (sourceKey)`。参见[把属性提升为列](/zh/agensgraph/querying/typed-columns/)。

**收集统计信息。** 规划器对刚加载的标签没有统计信息，而图遍历计划对统计信息非常敏感：

```sql
ANALYZE moviekb.person;
ANALYZE moviekb.acted_in;
```

**收集图元数据。** `ag_graphmeta` 记录图中出现了哪些“起点标签、边标签、终点标签”三元组，以及每种组合包含多少条边。规划器可以据此剪除模式不可能到达的标签扫描：

```cypher
SELECT regather_graphmeta();
```

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

然后检查加载结果的形状，这也是发现加载出错的最快方式：

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

意外出现的边形状，或正好是应有数量整数倍的计数，都会在这里立即显现。

加载完成后清理临时表和草稿标签：

```sql
DROP TABLE staging_people, staging_knows;
```

```cypher
DROP VLABEL bulk_person;
DROP VLABEL IF EXISTS staging_person;
```

## 导出 {#exporting}

`pg_dump` 可以覆盖一个图；指定模式名即可导出一个图。参见[备份与恢复](/zh/agensgraph/operations/backup/)。如果导出的是数据而不是结构，`COPY … TO` 可用于标签表；把 Cypher 查询包在 SQL 中，则可以准确导出你想要的形状：

```psql
\copy (SELECT p.properties->>'name' AS name, m.properties->>'title' AS film
       FROM moviekb.acted_in r
         JOIN moviekb.person p ON p.id = r.start
         JOIN moviekb.movie  m ON m.id = r."end") TO 'roles.csv' CSV HEADER
```
