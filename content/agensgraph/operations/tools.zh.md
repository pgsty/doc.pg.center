---
title: 服务端工具
linkTitle: 服务端工具
description: AgensGraph 自带工具就是 PostgreSQL 工具，因此 PostgreSQL 参考完整适用，本页不再重复。
type: docs
weight: 50
upstream_link: https://tech.skaiworldwide.com/docs/en/agensgraph/18.6.1/operations/tools.html
upstream_source: agensgraph
upstream_modified: true
translation_notice: en
translation_status: complete
---


AgensGraph 自带工具就是 PostgreSQL 工具，因此 [PostgreSQL 服务端工具参考](https://www.postgresql.org/docs/18/reference-server.html)完整适用，本页不再重复。本页说明差异，以及图给你最常用工具增加的内容。

交互客户端及其图元命令参见 [agens 客户端](/zh/agensgraph/reference/agens/)。

## AgensGraph 对工具集的增改 {#what-agensgraph-adds-to-the-tool-set}

两个工具以第二个名字发布：

| AgensGraph 名称 | PostgreSQL 名称 | 差异 |
| --- | --- | --- |
| `agens` | `psql` | 仅品牌差异。两者都会安装，图元命令在两者中都可用。 |
| `ag_ctl` | `pg_ctl` | 仅品牌差异。两者都会安装。 |

```shell
agens --version
```

```
agens (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
```

> [!NOTE]
> 开发分支构建会显示 `-devel` 后缀。

```shell
psql --version
```

```
psql (PostgreSQL) 18.6 (AgensGraph 2.18.6.1)
```

其余工具——`initdb`、`pg_dump`、`pg_dumpall`、`pg_restore`、`pg_upgrade`、`pg_basebackup`、`pg_controldata`、`pg_checksums`、`vacuumdb`、`reindexdb`、`createdb` 等——保留 PostgreSQL 名称和 PostgreSQL 行为。

`AGDATA` 与 `PGDATA` 一样可作为默认数据目录；`export AGDATA=/path/to/data` 后可以省略 `-D`。只有三个二进制会读取它——`initdb`、`pg_ctl` 和 `ag_ctl`——而且优先级不一致：`initdb` 优先 `AGDATA`，`pg_ctl` 和 `ag_ctl` 优先 `PGDATA`。其他每个工具只接受 `PGDATA`。

## 启动与停止 {#starting-and-stopping}

```shell
ag_ctl -D /path/to/data -l /path/to/data/server.log start
ag_ctl -D /path/to/data status
ag_ctl -D /path/to/data reload
ag_ctl -D /path/to/data stop -m fast
```

在 systemd 下，使用 PostgreSQL 自己的 unit 约定并指向 AgensGraph 二进制即可；这里没有图相关内容。参见[部署](/zh/agensgraph/operations/deployment/)。

## 导出图 {#dumping-a-graph}

`pg_dump` 和 `pg_dumpall` 无需特殊选项即可处理图，因为图是模式，标签是表。因此转储包含 `CREATE GRAPH`、`CREATE VLABEL`、`CREATE ELABEL` 语句和标签数据。

```shell
pg_dump -d mydb -f mydb.sql
pg_dump -d mydb -Fc -f mydb.dump
```

导出单个图时，指定它的模式名：

```shell
pg_dump -d mydb --schema=moviekb -f moviekb.sql
```

四个图相关要点：

* **两个工具都不检查 AgensGraph 版本。** 只有 PostgreSQL 自己的 `server_version` 范围检查适用，因此把较新的转储恢复到较旧服务端时，问题会表现为中途解析失败，而不是一开始被拒绝。
* **带普通列的标签转储会用 `SET enable_graph_ddl = on` 包住自己的 `ALTER TABLE` 语句。** 这个设置任意角色都可写，所以普通用户能恢复它——除非该角色被 `ALTER ROLE … SET` 强制关闭。
* **如果任何图使用[提升列](/zh/agensgraph/querying/typed-columns/)，2.18 转储不能恢复到 2.17**：生成的 `CREATE VLABEL` 形式不是 2.17 解析器接受的写法，而且在纯文本流中，这条语句之后的内容都会丢失。
* **基于 Cypher 查询定义的视图按 Cypher 降级得到的 SQL 导出**，而不是按你写的 Cypher。它可以恢复并工作，但取回的定义不是你写下的定义。参见[组合 SQL 与 Cypher](/zh/agensgraph/querying/combining-sql-and-cypher/)。

恢复后重建图元数据并重新收集统计信息——精确命令见[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/#step-6-post-upgrade-tasks)，它们适用于任何恢复，不只是升级。

## 跨主版本升级 {#upgrading-between-major-versions}

`pg_upgrade` 无需特殊处理即可用于图，但有两个 AgensGraph 相关条件：

* 如果标签带有 `id`、`start`、`end` 和 `properties` 之外的列，它会拒绝该图，而不是破坏物理列布局。
* 升级后 `ag_graphmeta` 为空，图被标记无效；在运行 `regather_graphmeta()` 之前，规划器的扫描裁剪不会启用。

[升级到 2.18](/zh/agensgraph/release-notes/upgrade-to-2.18/)是完整流程；[升级实例](/zh/agensgraph/release-notes/upgrade-walkthrough/)是带真实输出的示例。

## 基础备份与 WAL {#base-backups-and-wal}

`pg_basebackup`、WAL 归档、`pg_receivewal`、`pg_verifybackup` 和 `pg_rewind` 都按图的真实形态处理它——同一集群中的模式和表。因此物理备份会在同一时间点一起捕获图数据和关系数据。参见[备份与恢复](/zh/agensgraph/operations/backup/)。
