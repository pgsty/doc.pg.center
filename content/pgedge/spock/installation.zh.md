---
title: 安装并配置 Spock 扩展
description: 使用 pgEdge Postgres 软件包安装 Spock，或从源码构建，并配置 PostgreSQL 逻辑复制。
weight: 20
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/install_spock.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 安装与配置
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



Spock 扩展可以通过 pgEdge Postgres 软件包安装，也可以从源码构建。pgEdge Postgres 部署提供简化的升级路径，让你能够快速、轻松地利用重要的新特性。

Spock 是开源项目，代码可在 [GitHub](https://github.com/pgEdge) 上审阅。


> [!WARNING]
>
> Spock 使用存储在 `spock` schema 中的文件来提供复制功能。不要直接删除、创建或修改 `spock` schema 中的文件；应使用 Spock 函数和过程管理复制。
>

关于使用 Spock 创建双节点集群的详细信息，请参见[创建双节点集群](/zh/pgedge/spock/two-node/)。


## 使用 pgEdge Enterprise Postgres 安装 Spock {#installing-spock-with-pgedge-enterprise-postgres}

任何 [pgEdge Enterprise Postgres](https://docs.pgedge.com/enterprise) 安装都会自动附带最新版 Spock 扩展。pgEdge 部署让你可以快速、方便地使用以下特性：

- 你所选 PostgreSQL 版本的最新次要版本。
- Spock [函数和过程](/pgedge/spock/reference/)。
- [ACE 一致性监控](https://docs.pgedge.com/platform/ace)。
- [Snowflake 序列](https://docs.pgedge.com/platform/snowflake)。
- [pgBackRest](https://docs.pgedge.com/platform/managing/pgbackrest)，提供更简单的备份与恢复能力。
- [LOLOR](https://docs.pgedge.com/lolor/v1-2-2/) 大对象支持。
- 用于 active-active 分布式集群的管理工具。


## 从源码构建扩展 {#building-the-extension-from-source}

Spock 是一个[开源项目](https://github.com/pgEdge/spock)，你可以使用 GitHub 项目页面发布的源码自行构建。Spock 扩展必须构建在打过补丁的 PostgreSQL 版本专属构建上；补丁会提供钩子，让 `spock` 能够访问 PostgreSQL 引擎。

要给 PostgreSQL 源码打补丁，请先从 [PostgreSQL 项目](https://www.postgresql.org/ftp/source/)下载源码，并进入源码目录。然后克隆 `spock` 目录：

```bash
git clone https://github.com/pgEdge/spock.git
```

接着应用 `.diff` 文件；这些文件来自 `spock/patches/version` 目录，并与构建版本匹配。应用补丁的命令如下：

```bash
patch -p1 < path_to_patch/patch_name
```

应用版本专属补丁后，即可按 [PostgreSQL 文档](https://www.postgresql.org/docs/current/installation.html)中的说明配置、`make` 并 `make install` PostgreSQL 服务器。构建完成后，将 `pg_config` 文件所在位置加入 `PATH` 变量：

```bash
export PATH=path_to_pg_config_file
```

在执行 `make` 和 `make install` 之前，请安装 [jansson 库](https://jansson.readthedocs.io/en/1.1/gettingstarted.html)，以满足 Spock 的前置要求。

然后进入 `spock` 目录，使用与其他 PostgreSQL 扩展类似的构建流程：

```bash
make
make install
```


## 为 Spock 复制配置 PostgreSQL {#configuring-postgres-for-spock-replication}

在将要承载 spock 实例的每个节点上安装 PostgreSQL 后，使用 [initdb](https://www.postgresql.org/docs/18/app-initdb.html) 初始化 PostgreSQL 集群。初始化集群后，可以连接 psql，并查询服务器以获得文件位置和集群详情：

```sql
[sdouglas@lima-pg3 pg18]$ sudo -u postgres psql -U postgres -p 5432
psql (18.1)
Type "help" for help.

postgres=# SHOW data_directory;
SHOW config_file;
SHOW hba_file;

     data_directory     
------------------------
 /var/lib/pgsql/18/data
(1 row)

              config_file               
----------------------------------------
 /var/lib/pgsql/18/data/postgresql.conf
(1 row)

              hba_file              
------------------------------------
 /var/lib/pgsql/18/data/pg_hba.conf
(1 row)
```

然后使用你选择的编辑器更新 `postgresql.conf`，将必需的 PostgreSQL 参数添加到文件末尾：

```sql
wal_level = logical
max_worker_processes = 20   # see the sizing guide below
max_replication_slots = 10
max_wal_senders = 10
shared_preload_libraries = 'spock'
track_commit_timestamp = on
output_plugin_libraries = 'pgoutput, test_decoding, spock_output'
                            # only on servers that have this parameter; see below
```

上述值是小型集群（两到三个节点、一个复制数据库）的可用起点，并不是万能配置：Spock 会启动一个 supervisor、一个 slot sync worker、实例中每个数据库一个后台 worker，以及每个订阅一个后台 worker；订阅数量随节点数乘以被复制数据库数扩展，并且 `max_worker_processes` 会与并行查询 worker 共享。进入生产环境前，请参见[为 Spock 规划 PostgreSQL 资源](/zh/pgedge/spock/sizing/)中的公式和按集群给出的建议。

只有当服务器拥有 `output_plugin_libraries` 参数时才设置它——该参数由 2026 年的一次安全修复引入；如果其中没有列出 `spock_output`，逻辑解码会以 `library "spock_output" may not be used as an output
plugin` 失败。该检查在每次启动解码时都会运行，因此在次要版本升级后也会使已建立集群停止，并且适用于每个节点。在较旧版本中该参数不存在，设置它会导致服务器无法启动。如何检查请参见[配置 Spock](/zh/pgedge/spock/configuration/)。

关于复制源状态的说明：

- PostgreSQL 15-17：`max_replication_slots` 参数同时控制 replication slot 数量和复制源状态数量；为该参数估算容量时，需要同时考虑 slot 和复制源（每个订阅一个复制源，订阅按被复制的数据库计数）。
- PostgreSQL 18+：引入了新参数 `max_active_replication_origins`，单独控制复制源状态数量；默认值为 10，对拥有大量订阅的集群可能不足；在全互联拓扑中，至少设置为该节点应用的订阅数，即 `(nodes - 1) x replicated databases`，并留出余量（容量规划与 `max_replication_slots` 类似）。

修改 PostgreSQL 参数后，使用操作系统对应的命令重启 PostgreSQL 服务器：

```bash
[sdouglas@lima-pg3 pg18]$ sudo systemctl restart postgresql-18
[sdouglas@lima-pg3 pg18]$ sudo systemctl status postgresql-18
● postgresql-18.service - PostgreSQL 18 database server
     Loaded: loaded (/usr/lib/systemd/system/postgresql-18.service; enabled; preset: disabled)
     Active: active (running) since Wed 2026-02-11 11:44:11 EST; 7s ago
```

然后连接 psql 命令行并创建 spock 扩展：

```sql
postgres=# CREATE EXTENSION spock;
CREATE EXTENSION
postgres=#
```

在每个将承载 spock 的节点上，修改 [`pg_hba.conf` 文件](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)，允许 `n1` 与 `n2` 之间建立连接。以下片段仅作示例，不建议用于生产系统，因为它会让系统接受来自任意客户端的连接：

```sql
host    all          all          <node_1_IP_address>/32    trust
host    all          all          <node_2_IP_address>/32    trust

host    replication  all          <node_1_IP_address>/32    trust
host    replication  all          <node_2_IP_address>/32    trust
```

### 创建复制场景 {#creating-a-replication-scenario}

配置节点后，连接第一个 provider 节点的 psql 命令行，并使用 `spock.node_create` 命令创建 provider 节点：

```sql
SELECT spock.node_create(
    node_name := 'provider1',
    dsn := 'host=providerhost port=5432 dbname=db'
);
```

然后将 `public` schema 中的表加入 `default` 复制集：

```sql
SELECT spock.repset_add_all_tables('default', ARRAY['public']);
```

provider 节点配置完成后，可以添加订阅者。首先创建订阅者节点：

```sql
SELECT spock.node_create(
    node_name := 'subscriber1',
    dsn := 'host=thishost port=5432 dbname=db'
);
```

然后创建订阅；该订阅会在订阅者节点上启动同步和复制：

```sql
SELECT spock.sub_create(
    subscription_name := 'subscription1',
    provider_dsn := 'host=providerhost port=5432 dbname=db'
);

SELECT spock.sub_wait_for_sync('subscription1');
```

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/install_spock.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
