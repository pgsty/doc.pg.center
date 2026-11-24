---
title: 教程：通过滚动更新升级 PostgreSQL 版本
description: 使用 Zodan 的 add_node 和 remove_node 过程，逐个替换节点并升级 PostgreSQL 大版本。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/zodan_rolling_pg_version_tutorial.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---

Zodan 的 `add_node` 和 `remove_node` 过程可以在节点之间迁移数据，不受各节点 PostgreSQL 大版本不同的影响。因此，用于逐步升级 Spock 的节点替换策略，也能升级 PostgreSQL 本身。升级时需要：

- 使用目标 PostgreSQL 大版本构建替代节点。
- 将其加入集群。
- 确认它正在复制。
- 移除被替代的旧节点。

替代节点在旧节点移除之前就已完全运行并参与复制，因此集群节点数始终不低于最优数量，应用不会中断，实现 PostgreSQL 版本的零停机滚动升级。如果节点还配有用于高可用的物理备库，初始化该备库并将其纳入 Patroni 管理，也在同一轮逐节点操作中完成，以便开始下一个节点之前维持高可用保障。

本教程将运行 PostgreSQL 16 的三节点集群（`n1`、`n2`、`n3`）滚动升级到 PostgreSQL 18，依次替换为 `n1b`、`n2b` 和 `n3b`。如果同时升级 Spock，两项升级可合并到每个节点的一轮添加、验证、移除流程中。

> [!WARNING]
>
> 重要前提条件与警告
>
> - 每个替代节点在加入过程中都不应允许用户访问。
> - 在每个节点上禁用自动 DDL 复制（`spock.enable_ddl_replication = off`），整个升级期间不要在集群中执行 DDL。
> - 源节点和替代节点的用户必须完全一致。继续之前，在替代节点创建所需用户；两端所有用户的权限必须相同。
> - Zodan 在继续操作前会验证源节点的所有用户都存在于替代节点，防止因缺少用户权限导致复制失败。
> - 每次添加或移除期间，集群所有节点都必须可由 Spock 访问。
> - 每次 `add_node` 和 `remove_node` 都要从正在添加或移除的节点调用。
> - 调用 `add_node` 或 `remove_node` 的节点必须安装 `dblink` 扩展。
> - 如果节点的 PostgreSQL 构建具有 `output_plugin_libraries` 参数（[每一步之前检查 PostgreSQL 版本兼容性](#checking-postgresql-version-compatibility-before-each-step)中列出的补丁版本及之后版本），该参数必须包含 `spock_output`，否则 Spock 逻辑解码会失败。更早的构建没有此参数，不得设置。
> - 步骤中途失败后不要立即重试。先按下方[故障排查](#troubleshooting)确认工作流创建的所有对象均已清除。
> - `add_node` 每次等待节点间同步事件的时限为 180 秒。如果复制延迟超过此窗口，调用会抛出异常。开始前确认网络延迟和复制延迟在可接受范围内，或通过 [`spock.sync_timeout`](/zh/pgedge/spock/configuration/#spocksync_timeout) 增大会话等待时限。
> - 替代节点报告 `replicating` 状态之前，不要移除旧节点。
> - 始终保持至少两个节点运行；绝不要在同一窗口中同时移除倒数第二个旧节点和第一个新节点。
> - PostgreSQL 滚动更新只能向前升级。与 Spock 版本不匹配不同，Zodan 不会自行检查 PostgreSQL 版本的先后顺序，参见[每一步之前检查 PostgreSQL 版本兼容性](#checking-postgresql-version-compatibility-before-each-step)。
>

> [!NOTE]
>
> 示例将所有实例运行在同一主机上，使用 `127.0.0.1`。如果节点与备库或集群节点分布在不同主机，请在连接字符串、`listen`、`connect_address` 和 etcd URL 中使用各主机都能访问的地址，并让同一 scope 的所有 Patroni 成员连接同一 DCS。将 `<...>` 密码占位符替换为各自唯一的密码。
>

## 每一步之前检查 PostgreSQL 版本兼容性 {#checking-postgresql-version-compatibility-before-each-step}

Zodan 的 `check_spock_version_compatibility` 过程由 `add_node` 自动调用，但它只检查 Spock 扩展版本，不检查 PostgreSQL 服务器版本。添加替代节点之前，可以自行对照源节点确认其 PostgreSQL 补丁版本号：

```sql
SELECT * FROM dblink(
  'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
  'SHOW server_version_num'
) AS t(source_version int);

SELECT * FROM dblink(
  'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>',
  'SHOW server_version_num'
) AS t(replacement_version int);
```

替代节点的 `server_version_num` 必须大于或等于源节点。下表列出各 PostgreSQL 大版本首次具有 `output_plugin_libraries` 参数的补丁版本。这些版本及之后版本必须在其中列出 `spock_output`；更早版本不要设置：

| PostgreSQL 大版本 | 最低补丁版本 |
|---|---|
| 15 | 15.19 |
| 16 | 16.15 |
| 17 | 17.11 |
| 18 | 18.6 |
{.wide .expand}

## 准备替代节点 {#preparing-a-replacement-node}

每个替代节点都需要自己的主机（同机部署时使用独立端口）、数据目录，以及目标版本的 PostgreSQL 和 Spock，必须在调用 `add_node` 前准备好。按[安装 pgEdge Enterprise Postgres](/zh/pgedge/spock/getting-started/#install-pgedge-enterprise-postgres-recommended-path)的说明，在替代节点主机添加 pgEdge 仓库，并安装目标版本的 pgEdge Enterprise Postgres 和 Spock。在 RHEL、Rocky Linux 或 AlmaLinux 上安装 PostgreSQL 18：

```bash
sudo dnf install -y pgedge-postgres18-server pgedge-postgres18-contrib pgedge-spock50_18
```

在 Ubuntu 或 Debian 上：

```bash
sudo apt install -y pgedge-postgresql-18 pgedge-postgresql-18-spock50
```

示例中，替代节点与旧节点位于同一主机，使用独立端口；`n1b` 使用 `5442`。通过目标 PostgreSQL 版本初始化其数据目录：

```bash
initdb -D /path/to/data/n1b --username=postgres
```

首次启动替代节点之前，编辑 `postgresql.conf`：

- 按[配置 Spock](/zh/pgedge/spock/configuration/)设置 Spock 所需参数，沿用源节点的值。
- 按目标版本配置复制源跟踪容量。

> [!NOTE]
>
> `shared_preload_libraries` 只在服务器启动时生效，因此应现在设置，不要等执行 `CREATE EXTENSION spock` 后再设置。
>

PostgreSQL 15 至 17 通过 `max_replication_slots` 参数跟踪复制源；PostgreSQL 18 及之后使用 `max_active_replication_origins`。将相应参数设为所需订阅数：

```ini
wal_level = logical
max_worker_processes = 20
max_replication_slots = 10
max_wal_senders = 10
shared_preload_libraries = 'spock'
track_commit_timestamp = on
output_plugin_libraries = 'pgoutput, test_decoding, spock_output'

# PostgreSQL 18 and later only:
max_active_replication_origins = 10
```

复制现有节点使用的所有 `spock.*` 设置，例如冲突解决设置，以使替代节点行为一致。没有 `wal_level = logical`，`add_node` 无法在替代节点创建所需的槽，但它不会停止；只有使用 `verb := true` 调用时，才会以通知形式报告该失败。

在替代节点的端口上启动 PostgreSQL，然后用 `psql` 连接，确认设置生效：

```bash
pg_ctl -D /path/to/data/n1b -o "-p 5442" start
```

```bash
psql -p 5442 -c "SHOW shared_preload_libraries;"
psql -p 5442 -c "SHOW output_plugin_libraries;"
```

创建与源节点完全一致的数据库和用户：

```bash
psql -p 5442 -c "CREATE DATABASE inventory;"
psql -p 5442 -c "CREATE USER pgedge WITH PASSWORD '<pgedge-password>';"
psql -p 5442 -c "GRANT ALL ON DATABASE inventory TO pgedge;"
```

安装针对目标 PostgreSQL 版本构建的 Spock 扩展：

```bash
psql -p 5442 -d inventory -c "CREATE EXTENSION spock;"
psql -p 5442 -d inventory -c "CREATE EXTENSION dblink;"
```

如果旧节点配有用于高可用的物理备库，且替代节点目标版本为 PostgreSQL 18 或更新版本，还应在加入集群之前配置服务器原生的 `sync_replication_slots` 机制，因为 Spock 自己的故障切换工作进程不在 PostgreSQL 18+ 上运行。下面两种方法都需要复制角色、已知的超级用户密码，以及允许两者连接的 `pg_hba.conf` 条目。在选择路径之前，先在替代节点上统一配置：

```bash
psql -p 5442 -c \
  "CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD '<replicator-password>';"
psql -p 5442 -c "ALTER ROLE postgres WITH PASSWORD '<postgres-password>';"
```

在 `/path/to/data/n1b/pg_hba.conf` 中添加条目，允许备库主机建立复制连接；如果选择下方 Patroni 路径，还要允许 Patroni 自身健康检查所用的超级用户连接：

```
host replication replicator 127.0.0.1/32 md5
host all          postgres   127.0.0.1/32 md5
```

```bash
psql -p 5442 -c "SELECT pg_reload_conf();"
```

选择以下方法之一：

- 通过 Patroni 管理主备对，见下方[在集群中滚动更新](#rolling-the-update-across-the-cluster)的步骤 3。
- 手动配置原生路径：

    1. 在替代节点上创建物理复制槽，供未来备库进行流复制：

        ```sql
        SELECT pg_create_physical_replication_slot('n1b_standby_slot');
        ```

    2. 通过该槽进行流复制，将替代节点的基础备份写入备库数据目录：

        ```bash
        pg_basebackup -h 127.0.0.1 -p 5442 -U replicator \
          -D /path/to/data/n1b_standby -S n1b_standby_slot -X stream -P
        touch /path/to/data/n1b_standby/standby.signal
        ```

        `standby.signal` 使服务器以备库身份启动；`pg_basebackup -R` 也会写入它，但还会在 `postgresql.auto.conf` 中写入不含 `dbname` 的 `primary_conninfo`，覆盖后续步骤设置的值，而槽同步需要 `dbname`。

    3. 在替代节点的 `postgresql.conf` 中设置 `synchronized_standby_slots`，指定该槽：

        ```ini
        synchronized_standby_slots = 'n1b_standby_slot'
        ```

    4. 在备库自身的 `postgresql.conf` 中指向替代节点，并启用原生槽同步：

        ```ini
        sync_replication_slots = on
        primary_conninfo = 'host=127.0.0.1 port=5442 dbname=inventory user=replicator password=<replicator-password>'
        primary_slot_name = 'n1b_standby_slot'
        hot_standby_feedback = on
        ```

    5. 启动备库后，确认槽已同步：

        ```sql
        SELECT slot_name, synced, failover, invalidation_reason
        FROM pg_replication_slots
        WHERE NOT temporary;
        ```

完整参考见[逻辑复制槽故障切换（高可用备库）](/zh/pgedge/spock/logical-slot-failover/)，其中包括 PostgreSQL 15/16 路径及现有槽的升级。

## 在集群中滚动更新 {#rolling-the-update-across-the-cluster}

对每个节点执行一轮以下四步，示例中依次从 `n1` 到 `n3`。完成一个节点的全部步骤后，再开始下一个。

1. 连接准备好的替代节点，加载 Zodan 工作流：

    ```sql
    \i /path/to/zodan.sql
    ```

    > [!NOTE]
    >
    > `zodan.sql` 和 `zodremove.sql` 都位于 [Spock GitHub 仓库](https://github.com/pgEdge/spock)的 [samples/Z0DAN](https://github.com/pgEdge/spock/tree/main/samples/Z0DAN) 目录中。
    >

    然后添加替代节点，从集群中任一可访问且已追平的节点获取数据。首次替换时，直接选择被替换节点最简单：

    ```sql
    CALL spock.add_node(
        src_node_name := 'n1',
        src_dsn := 'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
        new_node_name := 'n1b',
        new_node_dsn := 'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>',
        verb := true,
        new_node_location := 'Los Angeles',
        new_node_country := 'USA',
        new_node_info := '{"role": "n1-replacement", "pg_version": "18"}'::jsonb
    );
    ```

2. 对旧节点采取操作之前，确认替代节点完全追平，且两个方向都在复制：

    ```sql
    CALL spock.show_all_subscription_status(
      'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>',
      true
    );
    ```

    涉及 `n1b` 的每个订阅都应报告 `replicating`，包括 `add_node` 自动创建的与 `n2`、`n3` 之间双向订阅。

3. 如果准备退役的节点配有用于高可用的物理备库，请为 `n1b` 构建对应备库，将主备对纳入 Patroni 管理，然后切换到它。如果集群不使用物理备库，跳过此步。

    `n1b` 或其未来备库运行 Patroni 之前，必须先安装 Patroni 和 DCS（分布式配置存储），并确保两台主机均可访问。本教程使用最常见的 Patroni DCS 选择 `etcd`。在两台主机安装 Patroni：

    ```bash
    pip install patroni[etcd]
    ```

    这会安装 Patroni 的 etcd 客户端库，不是 etcd 服务器本身。如果没有现成 etcd 集群为 Spock 集群中其他 Patroni 主备对提供服务，请安装并启动一个。软件包名称和安装方式随平台变化；软件包管理器不提供时，可查看 [etcd 发布页面](https://github.com/etcd-io/etcd/releases)。生产 etcd 部署需要奇数个成员（3 或 5）以构成法定多数；下面配置的是适用于本教程的单成员 etcd：

    ```yaml
    # /etc/etcd/etcd.yml
    name: etcd0
    data-dir: /path/to/data/etcd0
    listen-client-urls: http://127.0.0.1:2379
    advertise-client-urls: http://127.0.0.1:2379
    listen-peer-urls: http://127.0.0.1:2380
    initial-advertise-peer-urls: http://127.0.0.1:2380
    initial-cluster: etcd0=http://127.0.0.1:2380
    initial-cluster-token: n1b-etcd
    initial-cluster-state: new
    ```

    ```bash
    etcd --config-file /etc/etcd/etcd.yml
    ```

    继续之前，确认 `n1b` 及其备库主机均可访问 DCS：

    ```bash
    etcdctl --endpoints=127.0.0.1:2379 endpoint health
    ```

    将 `n1b` 纳入 Patroni，作为新 Patroni 集群的领导者，而不要让 Patroni 从头初始化。`n1b` 已初始化，并已运行 `add_node` 填充的数据。Patroni 只会对空 `data_dir` 执行初始化，因此指向 `n1b` 已有数据的目录，会使 Patroni 接管运行中的实例，作为集群首个成员：

    ```yaml
    scope: n1b-cluster
    namespace: /service/
    name: n1b

    restapi:
      listen: 127.0.0.1:8541
      connect_address: 127.0.0.1:8541

    etcd3:
      hosts: 127.0.0.1:2379

    postgresql:
      listen: 127.0.0.1:5442
      connect_address: 127.0.0.1:5442
      data_dir: /path/to/data/n1b
      bin_dir: /usr/pgsql-18/bin   # /usr/lib/postgresql/18/bin on Ubuntu or Debian
      parameters:
        sync_replication_slots: on
        hot_standby_feedback: on
      callbacks:
        on_role_change: /path/to/set_synchronized_standby_slots.sh
      authentication:
        replication:
          username: replicator
          password: <replicator-password>
        superuser:
          username: postgres
          password: <postgres-password>
    ```

    `sync_replication_slots` 和 `hot_standby_feedback` 是原生槽同步在备库上所需的两个设置；请在 `n1b` 和 `n1b_standby` 上都设置，不要只配置当前备库，因为提升后任一节点都可能成为备库。这里有意未将 `synchronized_standby_slots` 放入 `postgresql.parameters`：下方 `on_role_change` 回调会直接在当前主库设置它。如果将其声明为 Patroni 管理的静态参数，就会与回调冲突；Patroni 会把受管参数恢复为自身配置中的值，从而在每次提升后撤销回调的更新。

    启动 Patroni，接管运行中的实例：

    ```bash
    patroni /path/to/n1b_patroni.yml
    ```

    再让第二个 Patroni 实例指向相同的 `scope` 和 DCS 端点，成员名设为 `n1b_standby`，使用空 `data_dir`。Patroni 在 DCS 中找到现有集群，首次启动时自行从 `n1b` 执行 `pg_basebackup` 填充空目录：使用下方 `authentication.replication` 配置块中的凭据，以 `replicator` 角色通过前面 `pg_hba.conf` 条目允许的复制连接访问。这条路径无需手动执行 `pg_basebackup`，Patroni 初始化过程会代为运行：

    ```yaml
    scope: n1b-cluster
    namespace: /service/
    name: n1b_standby

    restapi:
      listen: 127.0.0.1:8542
      connect_address: 127.0.0.1:8542

    etcd3:
      hosts: 127.0.0.1:2379

    postgresql:
      listen: 127.0.0.1:5452
      connect_address: 127.0.0.1:5452
      data_dir: /path/to/data/n1b_standby
      bin_dir: /usr/pgsql-18/bin   # /usr/lib/postgresql/18/bin on Ubuntu or Debian
      parameters:
        sync_replication_slots: on
        hot_standby_feedback: on
      callbacks:
        on_role_change: /path/to/set_synchronized_standby_slots.sh
      authentication:
        replication:
          username: replicator
          password: <replicator-password>
        superuser:
          username: postgres
          password: <postgres-password>
    ```

    ```bash
    patroni /path/to/n1b_standby_patroni.yml
    ```

    确认 `n1b_standby` 已加入并开始流复制，再继续：

    ```bash
    patronictl -c /path/to/n1b_patroni.yml list n1b-cluster
    ```

    在依赖它执行故障切换之前，还要在 `n1b` 上确认备库所用的槽已同步：

    ```sql
    SELECT slot_name, synced, failover, invalidation_reason
    FROM pg_replication_slots
    WHERE NOT temporary;
    ```

    `synchronized_standby_slots` 指定 Patroni 管理的物理槽。Patroni 自动创建的槽以成员而非角色命名；名为 `n1b_standby` 的槽只在 `n1b_standby` 不是主库时存在。上面两份 Patroni 配置中的 `on_role_change` 回调，会在未来提升时将设置重置为当时的备库成员。Patroni 只在启动和重新加载时读取本地配置，因此为已运行的成员添加回调后，需要重新加载：

    ```bash
    patronictl -c /path/to/n1b_patroni.yml reload n1b-cluster
    ```

    将以下脚本部署到 `n1b`，设置 `SIBLING_MEMBER` 为 `n1b_standby`、`LOCAL_PORT` 为 `5442`；在 `n1b_standby` 上则分别设为 `n1b` 和 `5452`。每当本节点成为主库，它会将 `synchronized_standby_slots` 设为另一成员的名称：

    ```bash
    #!/bin/bash
    # Patroni on_role_change callback.
    # Patroni invokes this script as:
    #   <script> <action> <role> <scope>
    # so the role is $2, not $1.
    # Resets synchronized_standby_slots to the sibling member's name
    # whenever Patroni promotes this node to primary.
    ROLE="$2"
    SIBLING_MEMBER="n1b_standby"
    LOCAL_PORT="5442"

    if [ "$ROLE" = "master" ] || [ "$ROLE" = "primary" ]; then
      psql -p "${LOCAL_PORT}" -U postgres -c \
        "ALTER SYSTEM SET synchronized_standby_slots = '${SIBLING_MEMBER}';"
      psql -p "${LOCAL_PORT}" -U postgres -c "SELECT pg_reload_conf();"
    fi
    ```

    回调仅在未来提升时触发，因此现在趁 `n1b` 仍为领导者，手动设置初始值：

    ```bash
    psql -p 5442 -U postgres -c \
      "ALTER SYSTEM SET synchronized_standby_slots = 'n1b_standby';"
    psql -p 5442 -U postgres -c "SELECT pg_reload_conf();"
    ```

    当 `n1b_standby` 正在流复制，且两个节点都已部署回调后，执行切换：将依赖旧节点备库的 VIP、DNS 记录，或用于读流量及灾难恢复的连接字符串，指向新 Patroni 集群。确认切换完成之前，让旧节点的备库继续运行；步骤 4 会移除旧主库，其余集群恢复健康后即可停止旧备库。

    将来提升 `n1b_standby` 是独立于本次切换的事件，需要单独规划：`n2` 和 `n3` 上的 Spock 订阅使用前面 `add_node` 调用中的原始地址 `host=127.0.0.1 port=5442` 连接 `n1b`，Patroni 不会替它们修改地址。如果只能通过 VIP 或 DNS 记录访问 `n1b`，且 Patroni（或配合它运行的 `keepalived`）将地址移交给当前主库，那么调用 `add_node` 时，将 `new_node_dsn` 指向该稳定地址，而非节点的原始主机和端口；提升后就无需额外执行 Spock 操作。如果主备对前面没有这一层地址抽象，就需要提升后在仍指向旧地址的每个订阅者节点上手动修改订阅。

    `node_add_interface` 只写入本地节点系统目录，不会复制。由于 `sub_alter_interface` 在本地查找接口，请在每个需要修改订阅的节点上执行，这里是 `n2` 和 `n3`：

    ```sql
    SELECT spock.node_add_interface('n1b', 'n1b_standby_interface',
      'host=127.0.0.1 dbname=inventory port=5452 user=pgedge password=<pgedge-password>');
    ```

    然后在这些节点上分别执行 `sub_alter_interface`：

    ```sql
    SELECT spock.sub_alter_interface('sub_n1b_n2', 'n1b_standby_interface');
    ```

    `spock.gen_sub_name(provider_node, subscriber_node)` 为订阅命名，因此 `sub_n1b_n2` 表示位于 `n2`、提供者为 `n1b` 的订阅。修改指向之前，请在每个节点执行 `SELECT sub_name FROM spock.subscription;`，确认实际集群中的准确名称。

4. 将应用流量从 `n1` 转移到 `n1b`，并确认不再有新连接到达 `n1`。`remove_node` 会立即删除所有以 `n1` 为提供者或订阅者的订阅，不等待任何条件；因此，`n1` 上届时尚未传到其他节点的写入会丢失。确认 `n1` 不再接受写入后，在其上发出同步事件：

    ```sql
    -- On n1
    SELECT spock.sync_event();
    ```

    在其他每个节点等待该事件，传入返回的 LSN。`result` 列必须返回 `t`：

    ```sql
    -- On n1b, n2 and n3
    CALL spock.wait_for_sync_event(NULL, 'n1'::name, '<lsn-from-sync_event>'::pg_lsn, 600);
    ```

    然后在待退役节点加载移除工作流，将其从集群移除：

    ```sql
    \i /path/to/zodremove.sql
    ```

    ```sql
    CALL spock.remove_node(
      'n1',
      'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
      true
    );
    ```

    `remove_node` 不删除退役节点的数据库、数据目录或日志；确认其余集群健康后，停止该实例并回收资源。

用 `n1b` 替换 `n1` 后，对 `n2` 和 `n3` 重复步骤 1 至 4。每个新节点都可从集群中已有的新旧节点获取数据，但源节点的 PostgreSQL 版本不得高于替代节点自身。

## 重新启用 DDL 复制 {#re-enabling-ddl-replication}

所有节点替换完毕后，按照[升级 Spock](/zh/pgedge/spock/upgrading/)的说明，在每个节点重新开启自动 DDL 复制：

```sql
ALTER SYSTEM SET spock.enable_ddl_replication = on;
SELECT pg_reload_conf();
```

## 验证升级结果 {#verifying-the-rollout}

替换所有节点后，确认整个集群都运行目标 PostgreSQL 版本，且复制拓扑正常：

```sql
SELECT * FROM dblink(
  'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>',
  'SHOW server_version'
) AS t(pg_version text);

CALL spock.show_all_nodes(
  'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>',
  true
);

CALL spock.show_all_subscription_status(
  'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>',
  true
);
```

修改端口，对每个节点分别执行一次 `dblink` 查询。`show_all_nodes` 列出节点；`show_all_subscription_status` 报告各订阅的状态。

将升级视为完成之前，需要在输出中确认下表内容：

| 字段 | 确认内容 |
|---|---|
| PostgreSQL 版本 | 每个节点都报告目标版本。 |
| 节点名称 | 仅剩 `n1b`、`n2b` 和 `n3b`，不再列出旧节点。 |
| 订阅状态 | 每对节点之间的每个订阅都报告 `replicating`。 |
{.wide .expand}

## 故障排查 {#troubleshooting}

- **`add_node` 报错 `cannot synchronize structure from provider
  running PostgreSQL`，或替代节点的应用工作进程以 `cannot synchronize structure from upstream server version` 退出。** 替代节点的 `pg_dump` 不能转储比自身更新的 PostgreSQL 版本。指定源节点运行的 PostgreSQL 大版本高于替代节点。请用相同或更高的 PostgreSQL 大版本重建替代节点，或改用版本不高于替代节点的其他源节点，再重试。

- **逻辑解码报错 `library "spock_output" may not be
  used as an output plugin`。** 该节点构建具有 `output_plugin_libraries` 参数，但未包含 `spock_output`。将其加入 `postgresql.conf`，执行 `SELECT pg_reload_conf();`，无需重启。不要在不支持该参数的构建上设置它：无法识别的参数会阻止服务器启动。

- **`add_node` 报告无法创建复制槽。** 检查替代节点的 `wal_level = logical` 和 `max_replication_slots`。只有使用 `verb := true` 时，`add_node` 才会以通知形式报告槽创建失败，并继续执行；随后创建的订阅不会复制。

- **大型数据库上 `add_node` 等待同步事件超时。** 再次调用 `add_node` 前，通过 [`spock.sync_timeout`](/zh/pgedge/spock/configuration/#spocksync_timeout) 增大会话等待时限。

- **`add_node` 中途失败。** 不要立即重试。先在部分加入的节点加载 `zodremove.sql` 并调用 `spock.remove_node()`，清除它创建的订阅和复制槽，再重新添加。

更多信息参见：

- [使用 Zodan 修改集群](/zh/pgedge/spock/modify/zodan/)
- [使用 Zodan 脚本与工作流](/zh/pgedge/spock/modify/zodan/zodan-readme/)
- [教程：零停机向集群添加节点](/zh/pgedge/spock/modify/zodan/zodan-tutorial/)
- [逻辑复制槽故障切换（高可用备库）](/zh/pgedge/spock/logical-slot-failover/)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/zodan_rolling_pg_version_tutorial.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
