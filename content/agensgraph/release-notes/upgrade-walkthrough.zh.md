---
title: "升级演练"
linkTitle: "升级演练"
description: "在小型集群上将 AgensGraph 从 2.17 升级到 2.18，逐步核对命令输出、图数据、索引和统计信息。"
type: docs
weight: 30
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/release_notes/upgrade-walkthrough.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: translated
---


<!-- check-examples: skip because the examples need a 2.17 cluster and a freshly
     initialised 2.18 cluster. The output was captured from a real upgrade. -->

# 升级演练

本例在一个小型集群上完整演示从 2.17 升级到 2.18 的过程，列出实际执行的命令及其输出。参数和要求见[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/)。

示例集群中有一个图和一张普通表，可以分别验证它们是否随升级迁移。

```cypher
CREATE GRAPH social;
SET graph_path = social;
CREATE VLABEL person;
CREATE ELABEL knows;
CREATE (:person {name: 'Ann', age: 30}), (:person {name: 'Bo', age: 41});
MATCH (a:person {name: 'Ann'}), (b:person {name: 'Bo'}) CREATE (a)-[:knows {since: 2019}]->(b);
CREATE PROPERTY INDEX ON person (name);
```

```sql
CREATE TABLE audit (id serial primary key, note text);
INSERT INTO audit(note) VALUES ('before upgrade');
```

在 2.17 上执行查询，得到以下结果。

```cypher
MATCH (n:person)-[r:knows]->(m:person) RETURN n.name, r.since, m.name;
```

```
 name  | since | name
-------+-------+------
 "Ann" | 2019  | "Bo"
```

## 1. 记下旧集群的数据校验和设置 {#1-note-the-old-clusters-checksum-setting}

此设置决定初始化新集群时要用哪个选项。选错后，升级会在开始前就停止。

```shell
$OLD/bin/pg_controldata -D $OLDDATA | grep checksum
```

```
Data page checksum version:           0
```

值为 0 表示未启用数据校验和，这是 PostgreSQL 17 的默认设置。

## 2. 停止旧服务器 {#2-stop-the-old-server}

```shell
$OLD/bin/ag_ctl -D $OLDDATA stop
```

## 3. 初始化 2.18 集群 {#3-initialize-the-218-cluster}

旧集群报告的值是 `0`，因此初始化新集群时必须指定 `--no-data-checksums`。PostgreSQL 18 默认启用校验和，省略该选项就会出现下一节所示的错误。

```shell
$NEW/bin/initdb -D $NEWDATA -U postgres --encoding=UTF8 --no-data-checksums
```

```shell
$NEW/bin/pg_controldata -D $NEWDATA | grep checksum
```

```
Data page checksum version:           0
```

此时两个集群的校验和设置一致。

### 设置不一致时的表现 {#what-it-looks-like-when-they-do-not}

如果初始化 2.18 集群时省略上述选项，`pg_upgrade --check` 的完整输出如下。

```
Performing Consistency Checks
-----------------------------
Checking cluster versions                                     ok

old cluster does not use data checksums but the new one does
Failure, exiting
```

命令在第二项检查就会停止，尚未更改任何数据。只需使用正确选项重新初始化新集群即可。

## 4. 检查兼容性 {#4-check-compatibility}

```shell
$NEW/bin/pg_upgrade -b $OLD/bin -B $NEW/bin -d $OLDDATA -D $NEWDATA -U postgres --check
```

```
Performing Consistency Checks
-----------------------------
Checking cluster versions                                     ok
Checking database connection settings                         ok
Checking database user is the install user                    ok
Checking for prepared transactions                            ok
Checking for contrib/isn with bigint-passing mismatch          ok
Checking for valid logical replication slots                  ok
Checking for subscription state                               ok
Checking data type usage                                      ok
Checking for objects affected by Unicode update               ok
Checking for not-null constraint inconsistencies              ok
Checking for presence of required libraries                   ok
Checking database user is the install user                    ok
Checking for prepared transactions                            ok
Checking for new cluster tablespace directories               ok

*Clusters are compatible*
```

## 5. 执行升级 {#5-run-the-upgrade}

```shell
$NEW/bin/pg_upgrade -b $OLD/bin -B $NEW/bin -d $OLDDATA -D $NEWDATA -U postgres
```

输出的末尾如下。

```
Copying old pg_multixact/offsets to new server                ok
Deleting files from new pg_multixact/members                  ok
Copying old pg_multixact/members to new server                ok
Setting next multixact ID and offset for new cluster          ok
Resetting WAL archives                                        ok
Setting frozenxid and minmxid counters in new cluster         ok
Restoring global objects in the new cluster                   ok
Restoring database schemas in the new cluster                 ok
Copying user relation files                                   ok
Setting next OID for new cluster                              ok
Sync data directory to disk                                   ok
Creating script to delete old cluster                         ok
Checking for extension updates                                ok

Upgrade Complete
----------------
Some statistics are not transferred by pg_upgrade.
Once you start the new server, consider running these two commands:
    .../bin/vacuumdb -U postgres --all --analyze-in-stages --missing-stats-only
    .../bin/vacuumdb -U postgres --all --analyze-only
Running this script will delete the old cluster's data files:
    ./delete_old_cluster.sh
```

## 6. 启动新服务器并核对迁移结果 {#6-start-the-new-server-and-check-what-came-across}

```shell
$NEW/bin/ag_ctl -D $NEWDATA -l $NEW/logfile start
```

```sql
SELECT version();
```

```
 PostgreSQL 18.6 (AgensGraph 2.18.6.1) on x86_64-pc-linux-gnu, compiled by gcc ...
```

检查图数据，包括边的属性。

```cypher
SET graph_path = social;
MATCH (n:person)-[r:knows]->(m:person) RETURN n.name, r.since, m.name;
```

```
 name  | since | name
-------+-------+------
 "Ann" | 2019  | "Bo"
```

检查属性索引。

```psql
\d social.person
```

```
                              Table "social.person"
   Column   |  Type   | Nullable |                     Default
------------+---------+----------+-------------------------------------------------
 id         | graphid | not null | graphid(graph_labid('social.person'), nextval(…))
 properties | jsonb   | not null | jsonb_build_object()
Indexes:
    "person_pkey" PRIMARY KEY, btree (id)
    "person_name_idx" btree ((properties.'name'))
```

再检查普通表。

```sql
SELECT * FROM audit;
```

```
 id |      note
----+----------------
  1 | before upgrade
```

## 7. 完成升级后的三项工作 {#7-the-three-post-upgrade-tasks}

### 收集统计信息 {#statistics}

```shell
$NEW/bin/vacuumdb -U postgres --all --analyze-in-stages
```

### 重建图元数据 {#graph-metadata}

二进制升级后，`ag_graphmeta` 为空，图的元数据被标为无效。因此，规划器不会对扫描进行剪枝。

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

```
 graphname | graphmeta_valid
-----------+-----------------
 social    | f
```

为每个图分别重建一次元数据。

```sql
SET graph_path = social;
SELECT regather_graphmeta();
```

```
NOTICE:  regathering graphmeta...
 regather_graphmeta
--------------------
 t
```

```sql
SELECT graphname, graphmeta_valid FROM pg_catalog.ag_graph;
```

```
 graphname | graphmeta_valid
-----------+-----------------
 social    | t
```

### 调整边标签的统计信息 {#edge-label-statistics}

升级会保留 2.17 使用的统计目标值。

```sql
SELECT attname, attstattarget FROM pg_attribute
WHERE attrelid = 'social.knows'::regclass AND attname IN ('start', 'end')
ORDER BY 1;
```

```
 attname | attstattarget
---------+---------------
 end     |         10000
 start   |         10000
```

对于大型边标签，10000 这个目标值会明显增加规划耗时。2.18 新建边标签时使用 1000。可用以下命令将升级后的标签调整为相同的值。

```sql
ALTER TABLE social.knows ALTER COLUMN start SET STATISTICS 1000;
ALTER TABLE social.knows ALTER COLUMN "end" SET STATISTICS 1000;
ANALYZE social.knows;
```

## 8. 删除旧集群 {#8-remove-the-old-cluster}

确认新集群工作正常后，才执行以下命令。

```shell
./delete_old_cluster.sh
```

在运行此脚本之前，2.17 的数据目录仍然完好。只要升级时没有使用 `--link`，就可以通过停止新服务器、启动旧服务器来回退。
