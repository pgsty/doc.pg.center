---
title: 创建 Spock 集群：端到端安装指南
description: 从 pgEdge 软件包或源码安装 Spock，并完成双节点 active-active 复制集群的配置与验证。
weight: 30
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/getting_started.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 快速上手
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



本指南带你安装 Spock，并创建一个双节点 active-active 复制集群。

开始之前，请确认满足以下前置条件：

- 每个节点必须是具有网络连通性的物理机或虚拟机。
- 你必须拥有两个节点的管理员权限。
- 需要基本熟悉 PostgreSQL 和命令行操作。

安装流程如下。

1. 添加 pgEdge 仓库，并安装附带 Spock 的 pgEdge PostgreSQL。
2. 为逻辑复制配置 PostgreSQL 参数。
3. 在两个节点上创建 Spock 扩展。
4. 设置节点定义和双向订阅。
5. 在集群中启用自动 DDL 复制。
6. 测试集群，验证双向复制正常工作。

## 安装 pgEdge Enterprise Postgres（推荐路径） {#install-pgedge-enterprise-postgres-recommended-path}

本节介绍如何使用 pgEdge 仓库安装附带 Spock 的 pgEdge Enterprise Postgres。

首先，在每个节点上将 pgEdge 仓库添加到系统。

对于 RHEL/Rocky Linux/AlmaLinux 10，先安装 EPEL：

```bash
sudo dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
```

在 RHEL 10 上，还要启用 CodeReady Builder 仓库：

```bash
sudo subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms
```

在 Rocky Linux 10 或 AlmaLinux 10 上，则启用等价的 CRB 仓库：

```bash
sudo dnf config-manager --set-enabled crb
```

RHEL、OEL、Alma 和 Rocky 的版本专属命令见 [pgEdge Enterprise Postgres 文档](https://docs.pgedge.com/enterprise/el/configure-repo/)。

对于 Ubuntu/Debian：

在配置 pgedge 仓库的本地访问之前，应确认系统不包含社区 PostgreSQL 软件包。然后使用以下命令安装平台专属前置软件：

```bash
sudo apt-get update
sudo apt-get install -y curl
sudo apt-get install -y gnupg2
sudo apt-get install -y lsb-release
```

接着使用以下命令创建仓库：

```bash
sudo curl -sSL https://apt.pgedge.com/repodeb/pgedge-release_latest_all.deb -o /tmp/pgedge-release.deb
sudo dpkg -i /tmp/pgedge-release.deb
sudo rm -f /tmp/pgedge-release.deb
sudo apt update
```


> [!NOTE]
>
> 关于使用 pgEdge 仓库的详细信息，请参见 [pgEdge Enterprise Postgres 文档](https://docs.pgedge.com/enterprise/)。
>
>

创建仓库后，安装你偏好的 PostgreSQL 版本。示例使用 PostgreSQL 18。如果切换到 15、16、17 或 19，请更新下文片段中所有带版本号的软件包、路径和服务名。

对于 RHEL/Rocky Linux/AlmaLinux：

```bash
sudo dnf install -y pgedge-postgres18-server pgedge-postgres18-contrib pgedge-spock18
```

对于 Ubuntu/Debian：

```bash
sudo apt install -y pgedge-postgres18-server pgedge-postgres18-contrib pgedge-spock18
```

在每个节点上初始化 PostgreSQL 数据库集群。

对于 RHEL/Rocky Linux/AlmaLinux：

```bash
sudo /usr/pgsql-18/bin/postgresql-18-setup initdb
sudo systemctl enable postgresql-18
sudo systemctl start postgresql-18
```

对于 Ubuntu/Debian：

```bash
sudo /usr/lib/postgresql/18/bin/initdb -D /var/lib/postgresql/18/data
sudo systemctl enable postgresql-18
sudo systemctl start postgresql-18
```

以下示例中的 `psql` 命令连接 PostgreSQL 以验证安装：

```bash
sudo -u postgres psql -U postgres -p 5432
```

连接后，确认可以看到配置文件位置。

以下示例中的 `SHOW` 命令显示 PostgreSQL 配置文件位置：

```sql
postgres=# SHOW data_directory;
     data_directory
------------------------
 /var/lib/pgsql/18/data
(1 row)

postgres=# SHOW config_file;
              config_file
----------------------------------------
 /var/lib/pgsql/18/data/postgresql.conf
(1 row)

postgres=# SHOW hba_file;
              hba_file
------------------------------------
 /var/lib/pgsql/18/data/pg_hba.conf
(1 row)
```

pgEdge Enterprise Postgres 安装会自动包含以下组件：

- 你所选 PostgreSQL 版本的最新次要版本。
- Spock 扩展（预安装，可直接启用）。
- Spock 函数和过程。
- ACE 一致性监控。
- Snowflake 序列。
- 用于简化备份与恢复的 pgBackRest。
- LOLOR 大对象支持。
- active-active 分布式集群管理工具。

## 从源码安装（备选路径） {#install-from-source-alternative-path}

如果需要从源码构建 Spock，而不是使用 pgEdge Enterprise Postgres，请按以下步骤操作。

1. 从 [PostgreSQL 项目](https://www.postgresql.org/ftp/source/)下载 PostgreSQL 源码，并进入源码目录。

2. 使用以下命令克隆 Spock 仓库：

    ```bash
    git clone https://github.com/pgEdge/spock.git
    ```

3. 使用以下命令应用版本专属补丁：

    ```bash
    patch -p1 < spock/patches/version/patch_name
    ```

4. 按 [PostgreSQL 文档](https://www.postgresql.org/docs/current/installation.html)中的说明配置、构建并安装 PostgreSQL。

5. 使用以下命令将 `pg_config` 文件位置加入 PATH：

    ```bash
    export PATH=path_to_pg_config_file
    ```

6. 安装 [jansson 库](https://jansson.readthedocs.io/en/1.1/gettingstarted.html)（Spock 必需）。

7. 使用以下命令构建并安装 Spock：

    ```bash
    cd spock
    make
    make install
    ```

在两个节点上重复安装流程。

从源码构建后，在每个节点上使用 [initdb](https://www.postgresql.org/docs/18/app-initdb.html) 初始化 PostgreSQL 集群。

## 为 Spock 复制配置 PostgreSQL {#configure-postgresql-for-spock-replication}

在每个节点上编辑 `postgresql.conf`，并将必需参数添加到文件末尾。

以下示例中的配置参数启用逻辑复制并加载 Spock 扩展：

```sql
 wal_level = logical
max_worker_processes = 20   # see the sizing guide
max_replication_slots = 10  # two per subscriber, per replicated database,
                            # plus one per physical standby; 10 covers a
                            # four-node mesh replicating one database
max_wal_senders = 10        # keep equal to max_replication_slots
shared_preload_libraries = 'spock'
track_commit_timestamp = on # needed for conflict resolution
listen_addresses = '*'
output_plugin_libraries = 'pgoutput, test_decoding, spock_output'
                            # only on servers that have this parameter; see below
```


> [!NOTE] 规划 `max_worker_processes` 容量
>
> 该参数覆盖的 worker 不止每个节点一个：Spock 会运行一个 supervisor、一个 slot sync worker（每个节点都有，无论是 primary 还是 standby）、实例中每个可连接数据库（包括 `postgres` 和 `template1`）各一个 manager、每个订阅一个应用工作进程，以及在表同步期间每个订阅一个 sync worker。订阅按数据库创建，因此其数量是其他节点数*乘以*被复制数据库数。该池还会与并行查询 worker 共享。公式请参见[为 Spock 规划 PostgreSQL 资源](/zh/pgedge/spock/sizing/)。
>


> [!NOTE]
>
> 只有当服务器拥有 `output_plugin_libraries` 参数时才设置它——该参数由 2026 年的一次安全修复引入；如果其中没有列出 `spock_output`，逻辑解码会以 `library "spock_output" may not be used as an
> output plugin` 失败。该检查在每次启动解码时都会运行，因此在次要版本升级后也会使已建立集群停止，并且适用于每个节点。在较旧版本中该参数不存在，设置它会导致服务器无法启动。如何检查请参见[配置 Spock](/zh/pgedge/spock/configuration/)。
>


> [!NOTE]
>
> - PostgreSQL 15-17：`max_replication_slots` 参数同时控制 slot 和复制源状态。估算容量时需同时考虑两者（每个订阅一个复制源，订阅按被复制的数据库计数）。
>
> - PostgreSQL 18+：新参数 `max_active_replication_origins` 单独控制复制源状态。默认值为 10，可能不足。在全互联拓扑中，至少设置为该节点应用的订阅数，即 `(nodes - 1) x replicated
>   databases`，并留出余量。
>

修改 `postgresql.conf` 后，使用操作系统对应的命令重启 PostgreSQL。

以下示例中的 `systemctl` 命令重启并验证 PostgreSQL 服务：

```bash
sudo systemctl restart postgresql-18
sudo systemctl status postgresql-18
```

确认服务处于 active 并正在运行。

在每个节点上修改 [`pg_hba.conf`](https://www.postgresql.org/docs/18/auth-pg-hba-conf.html) 文件，允许节点之间建立连接。

为常规连接和复制连接添加条目。将 `<node_1_IP_address>` 和 `<node_2_IP_address>` 替换为实际 IP 地址。

以下示例中的配置条目允许来自两个节点的连接：

```conf
# Regular connections
host    all          all          <node_1_IP_address>/32    trust
host    all          all          <node_2_IP_address>/32    trust
host    all          all          <subnet_address>/24     trust

# Replication connections
host    replication  all          <node_1_IP_address>/32    trust
host    replication  all          <node_2_IP_address>/32    trust
```


> [!WARNING]
>
> 上例为简化使用了 `trust` 认证，不建议用于生产系统。生产环境应使用合适的认证方法，例如 `scram-sha-256` 或 `md5`。
>

修改 `pg_hba.conf` 后，重新加载服务器配置以应用更改（无需重启）：

```sql
SELECT pg_reload_conf();
```

## 创建 Spock 扩展 {#create-the-spock-extension}

在每个节点上连接 PostgreSQL 并创建 Spock 扩展。

以下示例中的 `CREATE EXTENSION` 命令创建 Spock 扩展：

```sql
sudo -u postgres psql -U postgres -p 5432

postgres=# CREATE EXTENSION spock;
CREATE EXTENSION
postgres=#
```


> [!WARNING]
>
> Spock 使用 `spock` schema 提供复制功能。不要直接删除、创建或修改 `spock` schema 中的文件。应使用 Spock 函数和过程管理复制。
>

## 创建节点并配置复制 {#create-nodes-and-configure-replication}

本节介绍如何在两个节点之间配置双向复制。本指南中节点分别命名为 `n1` 和 `n2`。

### 在节点 1（n1）上 {#on-node-1-n1}

按以下步骤创建节点定义，并将表加入复制集。

1. 使用以下命令创建节点定义：

    ```sql
    SELECT spock.node_create(
        node_name := 'n1',
        dsn := 'host=<n1_ip_address> port=<n1_port> dbname=<db_name>'
    );
    ```

2. 使用以下命令将表加入 default 复制集：

    ```sql
    SELECT spock.repset_add_all_tables('default', ARRAY['public']);
    ```

    如果操作所在 schema 不是 `public`，请相应调整 schema 名称。

### 在节点 2（n2）上 {#on-node-2-n2}

按以下步骤创建节点定义、添加表，并创建订阅。

1. 使用以下命令创建节点定义：

    ```sql
    SELECT spock.node_create(
        node_name := 'n2',
        dsn := 'host=<n2_ip_address> port=<n2_port> dbname=<db_name>'
    );
    ```

2. 使用以下命令将表加入 default 复制集：

    ```sql
    SELECT spock.repset_add_all_tables('default', ARRAY['public']);
    ```

3. 使用以下命令创建从 n2 到 n1 的订阅：

    ```sql
    SELECT spock.sub_create(
        subscription_name := 'sub_n2_n1',
        provider_dsn := 'host=<n1_ip_address> port=<n1_port> dbname=<db_name>'
    );

    SELECT spock.sub_wait_for_sync('sub_n2_n1');
    ```

### 在节点 1（n1）上 {#on-node-1-n1-1}

使用以下命令创建从 n1 到 n2 的反向订阅：

```sql
SELECT spock.sub_create(
    subscription_name := 'sub_n1_n2',
    provider_dsn := 'host=<n2_ip_address> port=<n2_port> dbname=<db_name>'
);

SELECT spock.sub_wait_for_sync('sub_n1_n2');
```

### 在两个节点（n1 与 n2）上 {#on-both-nodes-n1-and-n2}

为确保 DDL 语句在集群中自动复制，请在两个节点上运行这些命令。

以下示例中的 `ALTER SYSTEM` 命令启用自动 DDL 复制：

```sql
ALTER SYSTEM SET spock.enable_ddl_replication = on;
ALTER SYSTEM SET spock.include_ddl_repset = on;
SELECT pg_reload_conf();
```

这些设置启用以下功能：

- DDL 语句通过 default 复制集自动复制。
- 新表自动加入复制集；有主键的表加入 default 集，没有主键的表加入 default_insert_only 集。

## 验证集群 {#verify-the-cluster}

在每个节点上使用以下命令验证节点已正确配置。

以下示例中的 `SELECT` 命令显示已配置节点：

```sql
SELECT * FROM spock.node;
```

预期输出：

```sql
postgres=# SELECT * FROM spock.node;
-[ RECORD 1 ]----
node_id   | 26863
node_name | n2
location  |
country   |
info      |
-[ RECORD 2 ]----
node_id   | 49708
node_name | n1
location  |
country   |
info      |

```

然后使用以下命令验证订阅处于活动状态并正在复制。

以下示例中的 `SELECT` 命令显示订阅状态：

```sql
SELECT * FROM spock.sub_show_status();
```

预期输出：

```sql
 postgres=# SELECT * FROM spock.sub_show_status();
-[ RECORD 1 ]-----+--------------------------------------------------------------------
subscription_name | sub_n1
status            | replicating
provider_node     | n2
provider_dsn      | host=192.168.105.11 dbname=postgres user=postgres password=password
slot_name         | spk_postgres_n2_sub_n1
replication_sets  | {default,default_insert_only,ddl_sql}
forward_origins   |
```

`status` 字段应显示 `replicating`。

## 测试复制 {#test-replication}

按以下步骤执行简单复制测试。

1. 在 n1 上使用以下命令创建测试表：

    ```sql
    CREATE TABLE test (
        id SERIAL PRIMARY KEY,
        message TEXT
    );

    INSERT INTO test (message) VALUES ('Hello from n1');
    ```

2. 在 n2 上使用以下查询确认表存在且包含数据：

    ```sql
    SELECT * FROM test;
    ```

    预期输出：

    ```sql
    postgres=# SELECT * FROM test;
    -[ RECORD 1 ]------
    id      | 1
    message | Hello from n1
    ```

3. 在 n2 上使用以下命令插入新行：

    ```sql
    INSERT INTO test (message) VALUES ('Hello from n2');
    ```

4. 在 n1 上使用以下查询确认两行都存在：

    ```sql
    SELECT * FROM test;
    ```

    预期输出：

    ```sql
    postgres=# SELECT * FROM test;
    -[ RECORD 1 ]------
    id      | 1
    message | Hello from n1
    -[ RECORD 2 ]------
    id      | 2
    message | Hello from n2
    ```

两条消息都应出现在两个节点上，确认双向复制正常工作。

## 后续步骤 {#next-steps}

你的双节点 Spock 集群现已可用。以下文档介绍集群配置和管理的后续步骤。

- [配置 Spock](/zh/pgedge/spock/configuration/) 介绍冲突解决设置和高级配置选项。
- [Spock 函数参考](/pgedge/spock/reference/) 提供监控函数和复制管理的详细信息。
- [管理 DDL 复制](/zh/pgedge/spock/managing/spock-autoddl/) 说明如何控制自动 DDL 复制行为。

## 故障排查 {#troubleshooting}

如果遇到问题，请查看以下常见问题和解决方案。

- 如果复制没有启动，检查 `pg_hba.conf` 条目，并确认节点可以彼此连接。
- 当订阅卡在 initializing 时，确认 `max_replication_slots` 和 `max_wal_senders` 设置为足够大的值。正在同步的订阅除了其 apply 流持有的资源外，还需要在 provider 上使用第二个 slot 和 walsender；参见[为 Spock 规划 PostgreSQL 资源](/zh/pgedge/spock/sizing/)。
- 如果 DDL 没有复制，确认两个节点都启用了自动 DDL 复制设置。
- 如果错误信息不明确，请查看 PostgreSQL 日志中的详细错误消息。

更多信息请参见以下资源：

- [Spock 函数参考](/pgedge/spock/reference/) 提供详细函数文档。
- [高级配置选项](/zh/pgedge/spock/configuration/) 介绍其他配置参数。
- [管理 DDL 复制](/zh/pgedge/spock/managing/spock-autoddl/) 说明 DDL 复制功能。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/getting_started.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
