---
title: 教程：使用 pg_upgrade 原地升级 PostgreSQL 版本
description: 当可用存储不足以容纳第二份完整数据时，使用 pg_upgrade 原地升级节点的数据目录。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/pg_upgrade_rolling_tutorial.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---

如果数据库太大，系统剩余存储无法容纳第二份完整副本，可以使用 `pg_upgrade` 原地升级节点现有的数据目录。

`pg_upgrade` 将节点现有的数据目录原地迁移到新的 PostgreSQL 大版本。使用 `--link` 时，它在新旧集群文件之间创建硬链接，而不复制文件。新数据目录与旧目录共享磁盘块，无需将存储用量翻倍。

代价是该节点需要停机。与滚动替换策略不同，这里没有一个新建节点在旁等待、在升级期间接管流量。节点会停止，运行 `pg_upgrade`，再以新版本启动，随后重新加入集群。应用能够零停机，只是因为其余节点在此期间继续提供服务；节点本身并非零停机。

本教程将运行 PostgreSQL 16 的三节点集群（`n1`、`n2`、`n3`）逐个节点升级到 PostgreSQL 18，不为任何节点的数据保留第二份完整副本。`pg_upgrade` 仍需为每个节点准备一个新的空数据目录，但链接模式下存放的是指向旧文件的硬链接，而非文件副本。如果节点还有用于高可用的物理备库，重建备库并将其纳入 Patroni 管理，也在同一轮逐节点操作中完成，以便开始下一个节点之前恢复高可用保障。

## 前提条件与警告 {#prerequisites-and-warnings}

> [!WARNING]
>
> 重要前提条件与警告
>
> - 集群至少需要三个节点。一个节点停机升级期间，至少还要有两个节点为应用提供服务。
> - 负载均衡器、连接池或应用必须能够在节点停机升级前停止向其路由流量，并在之后恢复。这里没有替代节点自动接收流量。
> - 在每个节点上禁用自动 DDL 复制（`spock.enable_ddl_replication = off`），整个升级期间不要在集群中执行 DDL。
> - `pg_upgrade --link` 要求新旧数据目录位于同一文件系统，才能创建硬链接。如果文件系统不支持硬链接，或目录位于不同卷，`pg_upgrade` 会报错 `could not create hard
>   link between old and new data directories` 并停止，不会回退到复制模式。
> - `--link` 模式将新旧集群的数据文件关联在一起。新集群启动后，无法再运行旧集群；旧的 `postgresql.conf`、`pg_hba.conf` 和其他节点特有配置只能作为迁移到新版本的参考，不能用于回退。
> - 在任何 PostgreSQL 版本上，`pg_upgrade` 都不会迁移 Spock 的复制源。本流程在升级前记录它们、升级后恢复（步骤 2 和 19），并删除及重建其他节点对本节点的订阅，且不复制数据（步骤 3 和 20）。
> - 节点停机期间，其他节点会为它的订阅保留 WAL。如果设置了 `max_slot_wal_keep_size`，必须确保足以覆盖整个升级窗口，否则复制槽可能失效，节点就需要完整重建。
> - `spock.show_all_subscription_status()` 和 `spock.show_all_nodes()` 是 Zodan 过程。请在调用它们的节点加载 Spock 发行包中的 `zodan.sql`，它依赖 `dblink` 扩展。
> - 实际升级之前，对节点运行 `pg_upgrade --check`，并解决报告的所有问题。
> - 节点大版本改变后，其物理备库不能继续流复制；必须从升级后的节点重建备库，不能将两者一同原地升级。
>

> [!NOTE]
>
> 示例将所有实例运行在同一主机上，使用 `127.0.0.1`。如果节点与备库或集群节点分布在不同主机，请在连接字符串、`listen`、`connect_address` 和 etcd URL 中使用各主机都能访问的地址，并让同一 scope 的所有 Patroni 成员连接同一 DCS。将 `<...>` 密码占位符替换为各自唯一的密码。
>

## 使用 pg_upgrade 升级集群 {#upgrading-the-cluster-with-pg_upgrade}

对每个节点执行一轮以下步骤，示例中依次从 `n1` 到 `n3`。完成一个节点的全部步骤后，再开始下一个。

1. 在负载均衡器、连接池或应用层停止向待升级节点发送流量，并确认不再有新连接到达。

2. 确保其他所有节点都已应用 `n1` 提交的全部变更，并记录升级将丢失的信息。流量排空后，在 `n1` 发出同步事件：

    ```sql
    -- On n1
    SELECT spock.sync_event();
    ```

    在其他每个节点等待该事件，传入返回的 LSN。`result` 列必须返回 `t`：

    ```sql
    -- On n2, then on n3
    CALL spock.wait_for_sync_event(NULL, 'n1'::name, '<lsn-from-sync_event>'::pg_lsn, 600);
    ```

    然后在 `n1` 确认每个槽的确认位置都已越过该 LSN；以下查询必须返回零行：

    ```sql
    -- On n1
    SELECT slot_name, confirmed_flush_lsn
    FROM pg_replication_slots
    WHERE slot_type = 'logical'
      AND (confirmed_flush_lsn IS NULL
           OR confirmed_flush_lsn < '<lsn-from-sync_event>'::pg_lsn);
    ```

    物理槽（例如备库用于流复制的槽）的 `confirmed_flush_lsn` 始终为 `NULL`，因此查询仅限逻辑槽。

    `pg_upgrade` 不会迁移 Spock 的复制源，因此要记录 `n1` 各订阅已应用到的位置。每行都必须显示 LSN；`NULL` 表示订阅没有复制源，升级前必须先解决：

    ```sql
    -- On n1
    SELECT s.sub_name, s.sub_slot_name, o.remote_lsn
    FROM spock.subscription s
    LEFT JOIN pg_replication_origin_status o
           ON o.external_id = s.sub_slot_name;
    ```

    还要在其他每个节点上记录其对 `n1` 的订阅定义，以便步骤 20 按原样重建：

    ```sql
    -- On n2 (sub_n1_n2), then on n3 (sub_n1_n3)
    SELECT sub_name, sub_replication_sets, sub_forward_origins,
           sub_apply_delay, sub_force_text_transfer, sub_skip_schema
    FROM spock.subscription
    WHERE sub_name = '<subscription-to-n1-on-this-node>';
    ```

    `spock.gen_sub_name(provider_node, subscriber_node)` 为订阅命名，因此 `sub_n1_n2` 表示位于 `n2`、提供者为 `n1` 的订阅。在每个节点上执行 `SELECT sub_name FROM spock.subscription;`，确认实际集群中的名称。

3. 禁用 `n1` 自身的订阅，使其停止应用变更，并等待 `n1` 上的 `SELECT * FROM spock.sub_show_status();` 不再显示任何 `replicating` 状态：

    ```sql
    -- On n1, once per subscription
    SELECT spock.sub_disable('sub_n2_n1');
    SELECT spock.sub_disable('sub_n3_n1');
    ```

    在 `n1` 仍运行时，删除其他每个节点对它的订阅。只有能够连接 `n1`，`sub_drop` 才会删除 `n1` 上该订阅的槽；之后再删除订阅会在 `n1` 上留下槽。这里不会丢失数据，因为步骤 2 已确认每个节点都应用了 `n1` 的全部变更：

    ```sql
    -- On n2, then the matching subscription on n3
    SELECT spock.sub_drop('sub_n1_n2');
    ```

    如果本节点已由 Patroni 管理，请先暂停 Patroni，避免下面手动停止 PostgreSQL 时触发自动重启。Patroni 官方文档明确将大版本升级列为此模式的使用场景。`--wait` 仅在每个成员都已获知暂停状态后返回，避免后续停止操作与暂停发生竞争：

    ```bash
    patronictl -c /path/to/n1_patroni.yml pause --wait n1-cluster
    ```

    记录节点当前运行的 Spock 版本；步骤 4 会用到，服务器停机后就无法再查询：

    ```sql
    SELECT extversion FROM pg_extension WHERE extname = 'spock';
    ```

    然后停止该节点上的 PostgreSQL：

    ```bash
    pg_ctl -D /path/to/data/n1 stop
    ```

4. 在主机上安装目标 PostgreSQL 版本及 Spock，与现有安装并存；参见[安装 pgEdge Enterprise Postgres](/pgedge/spock/getting-started/#install-pgedge-enterprise-postgres-recommended-path)。在 RHEL、Rocky Linux 或 AlmaLinux 上安装 PostgreSQL 18：

    ```bash
    sudo dnf install -y pgedge-postgres18-server pgedge-postgres18-contrib pgedge-spock50_18
    ```

    在 Ubuntu 或 Debian 上：

    ```bash
    sudo apt install -y pgedge-postgresql-18 pgedge-postgresql-18-spock50
    ```

    `pg_upgrade` 按步骤 3 记录的版本在新集群中重建 Spock 扩展，而新服务器会加载为目标 PostgreSQL 版本安装的 Spock 库。应为目标版本安装相同版本的 Spock。如果目标版本的软件包只有更新的 Spock，请在步骤 8 启动节点后、步骤 19 之前，在每个安装了 Spock 的数据库中执行 `ALTER EXTENSION spock UPDATE;`。其余节点在轮到自己之前保持原版本，因此升级过程中集群会混合运行不同 Spock 版本，与[升级 Spock](/pgedge/spock/upgrading/)中的逐节点流程相同。在通过 Zodan 添加节点之前，先完成所有节点的升级：`add_node` 要求新节点的 Spock 版本不低于任何现有节点。

5. 使用目标 PostgreSQL 版本初始化新数据目录。`pg_upgrade` 将数据迁入已初始化的集群，不会自行创建集群。目标为 PostgreSQL 16 或更新版本时，`pg_upgrade` 会自行将旧集群的编码和区域设置复制到新集群，因此 `initdb` 不需要指定编码或区域选项。数据校验和设置不会复制，必须与旧集群一致，否则 `pg_upgrade` 会停止。从已停止的数据目录读取该设置：

    ```bash
    pg_controldata /path/to/data/n1 | grep "checksum version"
    ```

    如果校验和版本为 `1`，启用校验和：

    ```bash
    /path/to/pg18/bin/initdb -D /path/to/data/n1_new --data-checksums
    ```

    如果为 `0`，显式禁用。PostgreSQL 18 的 `initdb` 默认启用校验和，因此省略选项并不能匹配未启用校验和的旧集群：

    ```bash
    /path/to/pg18/bin/initdb -D /path/to/data/n1_new --no-data-checksums
    ```

    `pg_upgrade` 不迁移配置文件；新数据目录中只有 `initdb` 写入的默认配置。请现在配置，在步骤 6 之前完成：旧集群为 PostgreSQL 17 或更新版本时，`pg_upgrade --check` 会读取新集群的 `wal_level`、`max_replication_slots` 和 `output_plugin_libraries`；如果这些设置不能承载旧集群的逻辑槽，检查就会失败。原样复制 `pg_hba.conf`，因为认证规则不会随 PostgreSQL 版本改变：

    ```bash
    cp /path/to/data/n1/pg_hba.conf /path/to/data/n1_new/pg_hba.conf
    ```

    然后将 Spock 设置加入新数据目录的 `postgresql.conf`；如果旧节点的值更大，沿用旧值。`max_replication_slots` 至少要等于旧节点的逻辑槽数量：

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

    `output_plugin_libraries` 仅从下表所列补丁版本开始提供。只有新二进制文件支持此参数时才能设置；更早的补丁版本无法识别它，服务器会拒绝启动。使用 `SELECT current_setting('output_plugin_libraries', true);` 检查；参数不存在时返回 NULL。下表列出各大版本首次支持它的补丁版本：

    | PostgreSQL 大版本 | 最低补丁版本 |
    |---|---|
    | 15 | 15.19 |
    | 16 | 16.15 |
    | 17 | 17.11 |
    | 18 | 18.6 |

6. 先使用目标版本的二进制文件运行 `pg_upgrade --check`，确认没有阻碍升级的问题：

    ```bash
    /path/to/pg18/bin/pg_upgrade \
      --old-datadir /path/to/data/n1 \
      --new-datadir /path/to/data/n1_new \
      --old-bindir /path/to/pg16/bin \
      --new-bindir /path/to/pg18/bin \
      --link --check
    ```

    检查时也传入 `--link`，以验证两个目录之间可以创建硬链接。

    然后执行实际升级，添加 `--link`，通过硬链接复用数据文件而非复制：

    ```bash
    /path/to/pg18/bin/pg_upgrade \
      --old-datadir /path/to/data/n1 \
      --new-datadir /path/to/data/n1_new \
      --old-bindir /path/to/pg16/bin \
      --new-bindir /path/to/pg18/bin \
      --link
    ```

7. 启动之前，将旧 `postgresql.conf` 中节点所需的其他设置（内存、日志、连接限制等）迁入新配置。对旧 `postgresql.auto.conf`（保存所有通过 `ALTER SYSTEM` 设置的值）以及旧配置通过 `include` 引入的文件也作同样处理；`pg_upgrade` 不迁移这些文件。请对照目标版本文档逐项检查，而不要整份照搬，因为参数可能在大版本之间重命名或移除。

8. 启动新版本 PostgreSQL：

    ```bash
    pg_ctl -D /path/to/data/n1_new -o "-p 5432" start
    ```

9. 如果该节点配有用于高可用的物理备库，现在停止备库：主库大版本改变后，物理复制无法继续。如果没有物理备库，跳过步骤 9 至 18。

    ```bash
    pg_ctl -D /path/to/data/n1_standby stop
    ```

10. 在备库主机上安装目标 PostgreSQL 版本，与现有安装并存，方式与步骤 4 安装主库相同。

    ### 更新 Patroni 以使用升级后的实例 {#updating-patroni-to-use-the-upgraded-instance}

11. 如果这对主备已由 Patroni 管理，可以复用本节点原有的 Patroni 集群及其背后的 DCS（分布式配置存储），无需重新部署。

    **可选：** 如果首次将本节点及备库纳入 Patroni，请先在两台主机上安装 Patroni 和 DCS。本教程使用最常见的 Patroni DCS 选择 `etcd`：

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
    initial-cluster-token: n1-etcd
    initial-cluster-state: new
    ```

    ```bash
    etcd --config-file /etc/etcd/etcd.yml
    ```

    无论 DCS 刚刚启动，还是已经为这对主备服务，继续之前都应确认两台主机均可访问它：

    ```bash
    etcdctl --endpoints=127.0.0.1:2379 endpoint health
    ```

12. 将本节点的 Patroni 配置指向升级后的实例。如果首次纳入 Patroni，请为其编写配置，使它成为新 Patroni 集群的领导者，而不要让 Patroni 从头初始化。数据目录已初始化，并已运行 `pg_upgrade` 产生的数据；Patroni 只会对空 `data_dir` 执行初始化。将其指向已有数据的目录，会使 Patroni 接管运行中的实例，作为集群首个成员。如果升级前已由 Patroni 管理，请修改现有配置的 `data_dir` 和 `bin_dir` 为下方值，而非新写配置文件。`pg_upgrade` 保留角色和密码，前面的步骤 5 也已复制 `pg_hba.conf`，因此已有备库使用的 `replicator` 角色及其 `pg_hba.conf` 条目可原样继续使用。

    **可选：** 仅当 `postgres` 超级用户尚未设置密码时，为其设置密码：

    ```bash
    psql -p 5432 -c "ALTER ROLE postgres WITH PASSWORD '<postgres-password>';"
    ```

    ```yaml
    scope: n1-cluster
    namespace: /service/
    name: n1

    restapi:
      listen: 127.0.0.1:8541
      connect_address: 127.0.0.1:8541

    etcd3:
      hosts: 127.0.0.1:2379

    postgresql:
      listen: 127.0.0.1:5432
      connect_address: 127.0.0.1:5432
      data_dir: /path/to/data/n1_new
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

13. 如果节点此前已由 Patroni 管理，DCS 仍记录旧集群的系统标识符，而 `pg_upgrade` 为升级后的集群生成了新标识符。Patroni 拒绝管理系统标识符不匹配的数据目录，因此在接管升级后的实例之前，必须移除旧集群状态。停止 `n1` 和 `n1_standby` 上的 Patroni 进程，再从 DCS 移除该 scope 的状态。`patronictl remove` 会要求输入集群名称并确认：

    ```bash
    patronictl -c /path/to/n1_patroni.yml remove n1-cluster
    ```

    这只删除 `n1-cluster` 的 DCS 键，不删除任何数据目录。它也会删除该 scope 的动态配置，结束步骤 3 的暂停状态，并移除通过 `patronictl edit-config` 应用的设置。请先使用 `patronictl -c /path/to/n1_patroni.yml show-config n1-cluster` 记录这些设置，在 Patroni 运行后重新应用。

    无论节点此前已由 Patroni 管理，还是首次纳入，都使用步骤 12 的配置在 `n1` 启动 Patroni。DCS 中没有集群状态，而 PostgreSQL 已在有数据的 `data_dir` 上运行时，Patroni 会将其接管为领导者，而非初始化新实例：

    ```bash
    patroni /path/to/n1_patroni.yml
    ```

    然后将 `n1_standby` 作为新成员启动：其旧数据目录属于不兼容的旧大版本，不能复用。在备库自身的主机上运行 Patroni，指向相同的 `scope` 和 DCS，成员名设为 `n1_standby`，使用空 `data_dir`。Patroni 在 DCS 中发现集群，首次启动时自行从 `n1` 执行 `pg_basebackup`，填充空目录。如果 `n1_standby` 原来已由 Patroni 管理，将其现有配置改为以下值：

    ```yaml
    scope: n1-cluster
    namespace: /service/
    name: n1_standby

    restapi:
      listen: 127.0.0.1:8542
      connect_address: 127.0.0.1:8542

    etcd3:
      hosts: 127.0.0.1:2379

    postgresql:
      listen: 127.0.0.1:5442
      connect_address: 127.0.0.1:5442
      data_dir: /path/to/data/n1_standby_new
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
    patroni /path/to/n1_standby_patroni.yml
    ```

14. 确认 `n1_standby` 已加入并开始流复制，再继续：

    ```bash
    patronictl -c /path/to/n1_patroni.yml list n1-cluster
    ```

15. 还要在 `n1` 上确认备库所用的槽已同步：

    ```sql
    SELECT slot_name, synced, failover, invalidation_reason
    FROM pg_replication_slots
    WHERE NOT temporary;
    ```

16. `synchronized_standby_slots` 指定的是 Patroni 管理的物理槽。Patroni 会在当前主库上为每个备库成员自动创建一个槽，以该成员而非角色命名。现在槽名为 `n1_standby`，位于 `n1`；如果将来提升 `n1_standby`，该槽会消失，改为在 `n1_standby` 上出现名为 `n1` 的新槽，表示作为新备库的 `n1`。上面两份 Patroni 配置中的 `on_role_change` 回调，会在未来提升时将设置重置为当时的备库成员。Patroni 只在启动和重新加载时读取本地配置，因此为已运行的成员添加回调后，需要重新加载：

    ```bash
    patronictl -c /path/to/n1_patroni.yml reload n1-cluster
    ```

    将以下脚本部署到 `n1`，设置 `SIBLING_MEMBER` 为 `n1_standby`、`LOCAL_PORT` 为 `5432`；在 `n1_standby` 上则分别设为 `n1` 和 `5442`。每当本节点成为主库，它会将 `synchronized_standby_slots` 设为另一成员的名称：

    ```bash
    #!/bin/bash
    # Patroni on_role_change callback.
    # Patroni invokes this script as:
    #   <script> <action> <role> <scope>
    # so the role is $2, not $1.
    # Resets synchronized_standby_slots to the sibling member's name
    # whenever Patroni promotes this node to primary.
    ROLE="$2"
    SIBLING_MEMBER="n1_standby"
    LOCAL_PORT="5432"

    if [ "$ROLE" = "master" ] || [ "$ROLE" = "primary" ]; then
      psql -p "${LOCAL_PORT}" -U postgres -c \
        "ALTER SYSTEM SET synchronized_standby_slots = '${SIBLING_MEMBER}';"
      psql -p "${LOCAL_PORT}" -U postgres -c "SELECT pg_reload_conf();"
    fi
    ```

17. 回调仅在未来提升时触发，因此现在趁 `n1` 仍为领导者，手动设置初始值：

    ```bash
    psql -p 5432 -U postgres -c \
      "ALTER SYSTEM SET synchronized_standby_slots = 'n1_standby';"
    psql -p 5432 -U postgres -c "SELECT pg_reload_conf();"
    ```

18. 将来提升 `n1_standby` 是独立于本次配置的事件，需要单独规划：`n2` 和 `n3` 上的 Spock 订阅通过创建时配置的地址连接 `n1`，Patroni 不会替它们调整该地址。如果只能通过 VIP 或 DNS 记录访问 `n1`，且 Patroni（或配合它运行的 `keepalived`）将该地址移交给当前主库，则提升后无需额外执行 Spock 操作。如果主备对前面没有这一层地址抽象，就需要提升后在仍指向旧地址的每个订阅者节点上手动修改订阅。

    `node_add_interface` 只写入本地节点系统目录，不会复制。由于 `sub_alter_interface` 在本地查找接口，请在每个需要修改订阅的节点上执行，这里是 `n2` 和 `n3`：

    ```sql
    SELECT spock.node_add_interface('n1', 'n1_standby_interface',
      'host=127.0.0.1 dbname=inventory port=5442 user=pgedge password=<pgedge-password>');
    ```

    然后在这些节点上分别执行 `sub_alter_interface`。它指定的订阅由步骤 20 重建，因此本操作只适用于步骤 20 完成之后：

    ```sql
    SELECT spock.sub_alter_interface('sub_n1_n2', 'n1_standby_interface');
    ```

    `spock.gen_sub_name(provider_node, subscriber_node)` 为订阅命名，因此 `sub_n1_n2` 表示位于 `n2`、提供者为 `n1` 的订阅。修改指向之前，请在每个节点执行 `SELECT sub_name FROM spock.subscription;`，确认实际集群中的准确名称。

19. 在 `n1` 的订阅重新运行之前，将其复制源恢复到步骤 2 记录的位置。对每个订阅，如果 `pg_upgrade` 未保留复制源，则先创建，再推进到记录的 LSN：

    ```sql
    -- On n1, once per row recorded in step 2
    SELECT pg_replication_origin_create('<sub_slot_name>')
    WHERE NOT EXISTS (SELECT 1 FROM pg_replication_origin
                      WHERE roname = '<sub_slot_name>');
    SELECT pg_replication_origin_advance('<sub_slot_name>', '<remote_lsn>'::pg_lsn);
    ```

    确认每个复制源现在都显示记录的 LSN：

    ```sql
    SELECT external_id, remote_lsn FROM pg_replication_origin_status;
    ```

20. 在其他每个节点上，按步骤 2 记录的定义重建其对 `n1` 的订阅。不要复制数据：步骤 2 已确认每个节点持有 `n1` 的全部变更，而 `n1` 此后没有接受写入。下面示例重建 `n2` 上提供者为 `n1` 的订阅：

    ```sql
    -- On n2, then the matching subscription on n3
    SELECT spock.sub_create(
      subscription_name     := 'sub_n1_n2',
      provider_dsn          := 'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
      replication_sets      := '<recorded sub_replication_sets>',
      forward_origins       := '<recorded sub_forward_origins>',
      apply_delay           := '<recorded sub_apply_delay>',
      force_text_transfer   := <recorded sub_force_text_transfer>,
      skip_schema           := '<recorded sub_skip_schema>',
      synchronize_structure := false,
      synchronize_data      := false
    );
    ```

    不要在这里设置 `synchronize_data := true`。数据同步会直接将数据复制到现有表中，不会先清空，因此会因节点已持有的行而失败。

21. 重新启用 `n1` 自身的订阅，然后确认所有以 `n1` 为提供者或订阅者的订阅都报告 `replicating`：

    ```sql
    -- On n1, once per subscription
    SELECT spock.sub_enable('sub_n2_n1', true);
    SELECT spock.sub_enable('sub_n3_n1', true);
    ```

    再检查集群中每个订阅的状态：

    ```sql
    CALL spock.show_all_subscription_status(
      'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
      true
    );
    ```

22. 在负载均衡器、连接池或应用层恢复向该节点路由流量。

`n1` 升级完成后，对 `n2` 和 `n3` 重复步骤 1 至 22。

每个节点的备库都必须通过对*该节点*执行 `pg_basebackup` 来构建，绝不能从其他节点构建。`n2_standby` 必须从 `n2` 而非 `n1` 进行流复制，即使 Spock 使它们的表数据保持一致。

> [!NOTE]
>
> 物理备库绑定于它所跟随实例的确切系统标识符和 Spock 系统目录行（该实例自己的 `spock.node`/`spock.subscription` 条目），提升后才能具有该实例完全相同的身份。如果从 `n1` 构建备库，却提升它来替代 `n2`，它仍带有 `n1` 的身份和订阅，会破坏网状拓扑，而不是替代 `n2`。
>

每个节点及其物理备库（如有）也必须置于各自的 Patroni scope（`n2-cluster`、`n3-cluster`）中，各有自己的领导者；绝不能将 `n2` 或 `n3` 加入 `n1-cluster`。Patroni 在每个 scope 中选举一个主库，而 `n1`、`n2` 和 `n3` 在 Spock 网状集群中始终是独立主库，并非彼此的备库。DCS 部署本身仍可共享：只要各 scope 名称唯一，同一个 etcd 集群就能为所有节点的 Patroni scope 提供服务。

## 重新启用 DDL 复制 {#re-enabling-ddl-replication}

所有节点升级完毕后，按照[升级 Spock](/pgedge/spock/upgrading/)的说明，在每个节点重新开启自动 DDL 复制：

```sql
ALTER SYSTEM SET spock.enable_ddl_replication = on;
SELECT pg_reload_conf();
```

## 验证升级结果 {#verifying-the-rollout}

所有节点完成升级后，确认整个集群都运行目标 PostgreSQL 版本，且复制拓扑正常：

```sql
SELECT * FROM dblink(
  'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
  'SHOW server_version'
) AS t(pg_version text);

CALL spock.show_all_subscription_status(
  'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=<pgedge-password>',
  true
);
```

修改端口，对每个节点分别执行一次 `dblink` 查询。

将升级视为完成之前，需要在输出中确认下表内容：

| 字段 | 确认内容 |
|---|---|
| PostgreSQL 版本 | 每个节点都报告目标版本。 |
| 订阅状态 | 每对节点之间的每个订阅都报告 `replicating`。 |
{.wide .expand}

## 故障排查 {#troubleshooting}

- **`pg_upgrade --check` 报告扩展版本不兼容。** 升级前，在节点上安装为目标 PostgreSQL 版本构建的 Spock；`pg_upgrade` 会检查旧集群中的每个扩展在新集群中都有相应的可用库。

- **`pg_upgrade --link` 报错 `could not create hard link between
  old and new data directories`。** 新旧数据目录位于不同文件系统或卷。将新数据目录放到与旧目录相同的文件系统上，或不使用 `--link`，接受完整复制所需的存储开销。

- **升级后节点上的订阅因复制源不存在而失败。** 启用订阅前未恢复复制源。请禁用订阅，按步骤 19 从步骤 2 记录的位置恢复复制源，再重新启用。

- **应用仍将流量发送到停机升级的节点。** 确认步骤 1 的负载均衡器、连接池或应用路由确实将节点移出服务列表，且先于步骤 3 的停机操作完成，而不是依靠连接失败来重定向流量。

更多信息参见：

- [修改集群](/pgedge/spock/modify/)
- [逻辑复制槽故障切换（高可用备库）](/pgedge/spock/logical-slot-failover/)
- [教程：通过滚动更新升级 PostgreSQL 版本](/pgedge/spock/modify/zodan/zodan-rolling-pg-version-tutorial/)

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/pg_upgrade_rolling_tutorial.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/pgedge/about/license/)。
