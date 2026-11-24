---
title: "教程：不停机向 Spock 集群添加节点"
description: "通过逐步示例，在不停机的情况下向三节点集群添加第四个节点。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/zodan_tutorial.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



本教程演示如何在不停机的情况下为三节点集群添加第四个节点。现有节点是 `n1`（源节点）、`n2` 和 `n3`，新节点是 `n4`。


> [!WARNING]
>
> 前置条件与注意事项
>
> - 添加节点期间，不应允许用户连接新节点。
> - 在集群的所有节点上禁用 `auto_ddl`。
> - 添加节点期间不要执行变更结构的 DDL。
> - 源节点和目标节点必须具有相同的用户。开始前，先在目标节点上创建所需用户，并确保两端每位用户的权限一致。
> - 加入集群之前，ZODAN 会检查源节点的所有用户是否都存在于新节点，避免因缺少用户权限而导致复制失败。
> - 源节点与目标节点的 Spock 配置必须一致。
> - 添加节点的整个过程中，Spock 都必须能够访问集群的所有节点。
> - 应在待加入的新节点上执行该过程。
> - 执行 `SELECT spock.add_node()` 等命令的节点上必须安装 `dblink` 扩展。
> - 新节点须满足本节列出的全部条件。
> - 若流程失败，先确认已清理该流程创建的所有对象，再重试相关命令。
> - 自动过程 `spock.add_node()` 默认对每次节点间同步事件等待 180 秒（3 分钟）。复制延迟超过此窗口会抛出异常。开始前应核对网络和复制延迟，或按下文[设置同步超时](#setting-the-synchronisation-timeout)，通过 [`spock.sync_timeout`](/zh/pgedge/spock/configuration/#spocksync_timeout) 增加本会话的等待上限。手工流程直接调用 `spock.wait_for_sync_event()`，须自行指定超时（示例为 1200 秒），不使用上述默认值或 `spock.sync_timeout`。
>

## 手工创建节点 {#creating-a-node-manually}

若未使用 `spock.node_create` 创建新节点，需要执行以下步骤。

- 用 `initdb` 初始化新节点。
- 创建数据库。
- 创建数据库用户。
- 按照 [GitHub 仓库](https://github.com/pgEdge/spock) 的说明构建并为数据库安装 Spock。
- 在 `postgresql.conf` 的 `shared_preload_libraries` 中加入 `spock`。
- 重启服务器，使配置生效。
- 使用 `CREATE EXTENSION spock` 创建 Spock 扩展。

## 示例配置与新节点创建步骤 {#sample-configuration-and-new-node-creation-steps}

示例集群使用以下配置。

- 数据库：`inventory`
- 用户：`pgedge`
- 密码：`1safepassword`
- n1（源节点）：端口 5432
- n2（副本）：端口 5433
- n3（副本）：端口 5434
- n4（新节点）：端口 5435
- 主机：127.0.0.1

下列命令为新节点 n4 初始化数据库并安装 Spock。

```bash
# Initialize database
initdb -D /path/to/data

# Start Postgres
pg_ctl -D /path/to/data start

# Create database and user
psql -c "CREATE DATABASE inventory;"
psql -c "CREATE USER pgedge WITH PASSWORD '1safepassword';"
psql -c "GRANT ALL ON DATABASE inventory TO pgedge;"

# Install Spock extension
psql -d inventory -c "CREATE EXTENSION spock;"
psql -d inventory -c "CREATE EXTENSION dblink;"
```

## 用 Zodan 过程添加节点 {#using-the-zodan-procedure-to-add-a-node}

创建节点后，可用 [Zodan 脚本](/zh/pgedge/spock/modify/zodan/zodan-readme/) 将其加入集群。

先连接待加入 pgEdge 集群的新节点。下例通过 `psql` 建立连接。

```bash
psql -h 127.0.0.1 -p 5435 -d inventory -U pgedge
```

用以下命令加载 Zodan 过程。

```sql
\i /path/to/zodan.sql
```

在新节点调用 `spock.add_node()` 建立节点定义。示例通过 `spock.add_node` 将 `n4` 加入集群。

```sql
CALL spock.add_node(
    src_node_name := 'n1',
    src_dsn := 'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=1safepassword',
    new_node_name := 'n4',
    new_node_dsn := 'host=127.0.0.1 dbname=inventory port=5435 user=pgedge password=1safepassword',
    verb := true,
    new_node_location := 'Los Angeles',
    new_node_country := 'USA',
    new_node_info := '{"key": "value"}'::jsonb
);
```

`spock.add_node` 执行加入集群所需的步骤，下文逐项解释。

如果中途出错，可载入 `zodremove.sql` 脚本，调用 `spock.remove_node` 来移除节点或撤销已完成的部分步骤。应在待移除的节点上调用 `spock.remove_node`。

### 设置同步超时 {#setting-the-synchronisation-timeout}

`spock.add_node()` 会在多个步骤等待同步，例如等待对端收到同步事件、新节点追平进度，或订阅进入复制状态。每次默认最多等待 180 秒（3 分钟），适合几秒即可加入节点的小集群。大型数据库追赶进度可能需要数分钟甚至数小时，使用默认值会在操作完成前超时。

如需延长时间，在调用 add_node 之前，在同一会话设置 [`spock.sync_timeout`](/zh/pgedge/spock/configuration/#spocksync_timeout)。

```sql
SET spock.sync_timeout = '2h';
```

新值适用于该过程的每一次同步等待，会话结束后即恢复。长时间的节点添加操作无须更改整个集群的配置。要对所有会话生效，可在 `postgresql.conf` 中设置。

该参数限制整次等待的时长。为防止一个无响应的对端耗尽全部等待时间，某些步骤还会单独限制每次远端探测，这些较短的超时仍各自生效。


## 手工将节点加入集群 {#manually-adding-a-node-to-a-cluster}

以下是 Zodan 添加节点时执行的步骤。也可依次手工操作，达到与上述 `spock.add_node` 相同的目的。

### 检查 Spock 版本兼容性 {#check-the-spock-version-compatibility}

先确认 n1、n2、n3、n4 的 Spock 版本完全一致，以免设置复制时出现不兼容。


> [!NOTE]
>
> 若有节点版本不同，流程将报错并中止。
>

在执行编排的节点上运行下列命令检查 Spock 版本。

```sql
-- Check source node version
SELECT version
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=pgedge password=1safepassword',
    'SELECT extversion FROM pg_extension WHERE extname = ''spock'''
) AS t(version text);
-- Expected: matches the version installed on every node in the cluster

-- Check new node version
SELECT version
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=pgedge password=1safepassword',
    'SELECT extversion FROM pg_extension WHERE extname = ''spock'''
) AS t(version text);
-- Expected: matches the version installed on every node in the cluster

-- Check all existing cluster nodes (n2, n3)
SELECT node_name, version
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'SELECT n.node_name,
            (SELECT extversion FROM pg_extension WHERE extname = ''spock'') as version
     FROM spock.node n'
) AS t(node_name text, version text);

-- Expected output: every node reports the same Spock version, e.g.
--  node_name |  version
-- -----------+----------
--  n1        | 5.0.6
--  n2        | 5.0.6
--  n3        | 5.0.6
```

### 验证前置条件 {#validate-prerequisites}

将新节点加入复制集群前，须确认其状态适合初始化。

按以下条件检查 `n4` 是否为干净的新节点。

- n4 上必须已创建数据库并安装 Spock 扩展。
- n4 不能含有用户数据或已有复制配置。
- 确认集群中尚无名为 n4 的节点。


> [!NOTE]
>
> 任一条件不满足，流程都会中止以避免冲突。
>

#### 确认 n4 上已有数据库 {#confirm-that-the-database-exists-on-n4}

尝试连接 n4 上的目标数据库。如果数据库尚未创建，应先创建它。

下面的查询检查目标数据库是否存在于 n4。

```sql
SELECT 1
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT 1'
) AS t(dummy int);
-- If no error, database exists
```

#### 确认 n4 不含用户创建的表 {#confirm-that-n4-has-no-user-created-tables}

新节点的用户模式中不能有用户表。系统表和扩展的表可以保留。如果存在用户表，ZODAN 会中止，以免同步覆盖原有数据。

下面的查询检查 n4 是否有用户创建的表。

```sql
SELECT count(*)
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT count(*) FROM pg_tables
     WHERE schemaname NOT IN (''information_schema'', ''pg_catalog'', ''pg_toast'', ''spock'')
     AND schemaname NOT LIKE ''pg_temp_%''
     AND schemaname NOT LIKE ''pg_toast_temp_%'''
) AS t(count integer);
-- Expected: 0
```

#### 确认集群中尚无 n4 {#confirm-that-n4-does-not-exist-in-the-cluster}

检查集群中是否已登记名为 n4 的节点。如果存在，ZODAN 会中止，以免重名。查询如下。

```sql
-- On orchestrator node (connected to n1)
SELECT count(*) FROM spock.node WHERE node_name = 'n4';
-- Expected: 0
```

#### 确认 n4 不含订阅 {#confirm-that-n4-contains-no-subscriptions}

下面的查询检查 n4 上是否已有订阅。

```sql
SELECT count(*)
FROM spock.subscription s
JOIN spock.node n ON s.sub_origin = n.node_id
WHERE n.node_name = 'n4';
-- Expected: 0
```

#### 确认 n4 不含复制集 {#confirm-that-n4-contains-no-replication-sets}

下面的查询检查 n4 是否已有复制集。

```sql
SELECT count(*)
FROM spock.replication_set rs
JOIN spock.node n ON rs.set_nodeid = n.node_id
WHERE n.node_name = 'n4';
-- Expected: 0
```

### 在 n4 上创建复制节点 {#create-a-replication-node-on-n4}

确认新节点状态后即可开始添加。在 n4 上创建 Spock 节点对象。

- 这会将 n4 登记为复制集群的参与节点。
- 此后 n4 就有了表明自己属于该集群的节点标识。


> [!NOTE]
>
> 完成这一步后，可在各节点的 `spock.node` 表中看到 n4。
>

#### 在 n4 上创建节点 {#create-a-node-on-n4}

用 `dblink` 连接 n4，运行 `spock.node_create()` 登记节点。DSN 告知其他节点如何连接 n4。

以下示例通过 `spock.node_create` 将 n4 登记为集群成员。

```sql
-- Via dblink to n4
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT spock.node_create(
        node_name := ''n4'',
        dsn := ''host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword'',
        location := ''Los Angeles'',
        country := ''USA'',
        info := ''{\"key\": \"value\"}''::jsonb
    )'
) AS t(node_id oid);

-- Expected output:
--  node_id
-- ---------
--    16389
```

#### 确认初始节点数 {#confirm-the-initial-node-count}

下面的查询取得当前节点数量。

```sql
SELECT count(*)
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'SELECT count(*) FROM spock.node'
) AS t(count integer);
-- Expected: 4 (n1, n2, n3, n4)
```


### 创建暂时禁用的订阅和复制槽 {#create-disabled-subscriptions-and-slots}

此阶段的关键是记下复制位置，步骤如下。

- 创建从 n2 到 n4 和从 n3 到 n4 的订阅，暂时禁用。
- 建立各订阅前先触发 `sync_event()`。它返回一个 LSN（日志序列号），用来标记复制流中的位置。
- 将这些位置写入临时表，留待后用。
- 以后可以据此核实订阅从正确的位置开始工作，防止漏数据或重复复制。
- 订阅暂时禁用，让 n4 先从源节点 n1 一次性同步全部初始数据。


> [!NOTE]
>
> 此时只是准备好 n2 到 n4 和 n3 到 n4 的订阅，稍后才开始传输数据。
>

#### 列出现有节点 {#identify-all-existing-nodes}

查询集群中的 n1、n2、n3、n4 及其连接串。下例返回所有节点及其 DSN。

```sql
SELECT n.node_name, i.if_dsn
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'SELECT n.node_name, i.if_dsn
     FROM spock.node n
     JOIN spock.node_interface i ON n.node_id = i.if_nodeid'
) AS t(node_name text, if_dsn text);

-- Expected output:
--  node_name |                              if_dsn
-- -----------+------------------------------------------------------------------
--  n1        | host=127.0.0.1 dbname=inventory port=5432 user=alice password=...
--  n2        | host=127.0.0.1 dbname=inventory port=5433 user=alice password=...
--  n3        | host=127.0.0.1 dbname=inventory port=5434 user=alice password=...
--  n4        | host=127.0.0.1 dbname=inventory port=5435 user=alice password=...
```

#### 从 n2 到 n4：在 n2 触发同步事件并保存 LSN {#for-n2-to-n4-trigger-sync-event-on-n2-and-store-lsn}

在 n2 上调用 `sync_event()`，在复制流中写入标记，返回相应的 LSN。将该位置（0/1A7D1E0）存入临时表。以后启用 sub_n2_n4 时，可用这个 LSN 核实订阅到达了预定位置，以免漏过变更。

下列命令触发同步事件并保存 LSN。

```sql
-- Trigger sync event on n2
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
    'SELECT spock.sync_event()'
) AS t(sync_lsn pg_lsn);
-- Returns: 0/1A7D1E0

-- Store in temp table
CREATE TEMP TABLE IF NOT EXISTS temp_sync_lsns (
    origin_node text PRIMARY KEY,
    sync_lsn text NOT NULL
);

INSERT INTO temp_sync_lsns (origin_node, sync_lsn)
VALUES ('n2', '0/1A7D1E0')
ON CONFLICT (origin_node) DO UPDATE SET sync_lsn = EXCLUDED.sync_lsn;
```

#### 在 n2 上创建复制槽 {#create-a-replication-slot-on-n2}

复制槽保留 n2 上尚需发送给 n4 的变更。即使订阅尚未启用，复制槽也会立即开始保留变更，以免遗漏现在到订阅启用之间的数据。

下列命令在 n2 上创建复制槽。

```sql
-- On n2
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
    'SELECT slot_name, lsn
     FROM pg_create_logical_replication_slot(
         ''spk_inventory_n2_sub_n2_n4'',
         ''spock_output''
     )'
) AS t(slot_name text, lsn pg_lsn);

-- Expected output:
--         slot_name         |    lsn
-- --------------------------+------------
--  spk_inventory_n2_sub_n2_n4 | 0/1A7D1E8
```

#### 在 n4 上创建来自 n2 的禁用订阅 {#create-disabled-subscription-on-n4-from-n2}

在 n4 创建订阅对象，设置 `enabled := false`。这表示 n4 稍后将订阅 n2；此时它已知道 n2 上的槽，但还不会拉取数据。

```sql
-- On n4
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT spock.sub_create(
        subscription_name := ''sub_n2_n4'',
        provider_dsn := ''host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword'',
        replication_sets := ARRAY[''default'', ''default_insert_only'', ''ddl_sql''],
        synchronize_structure := false,
        synchronize_data := false,
        forward_origins := ARRAY[]::text[],
        apply_delay := ''0''::interval,
        enabled := false,
        force_text_transfer := false,
        skip_schema := ARRAY[]::text[]
    )'
) AS t(subscription_id oid);
```

#### 为 n3 到 n4 重复以上步骤 {#repeat-the-previous-steps-for-n3-to-n4}

下列命令为 n3 到 n4 执行相同操作。

```sql
-- Trigger sync event on n3
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
    'SELECT spock.sync_event()'
) AS t(sync_lsn pg_lsn);
-- Returns: 0/1B8E2F0

-- Store LSN
INSERT INTO temp_sync_lsns (origin_node, sync_lsn)
VALUES ('n3', '0/1B8E2F0')
ON CONFLICT (origin_node) DO UPDATE SET sync_lsn = EXCLUDED.sync_lsn;

-- Create replication slot on n3
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
    'SELECT slot_name, lsn
     FROM pg_create_logical_replication_slot(
         ''spk_inventory_n3_sub_n3_n4'',
         ''spock_output''
     )'
) AS t(slot_name text, lsn pg_lsn);

-- Create disabled subscription on n4 from n3
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT spock.sub_create(
        subscription_name := ''sub_n3_n4'',
        provider_dsn := ''host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword'',
        replication_sets := ARRAY[''default'', ''default_insert_only'', ''ddl_sql''],
        synchronize_structure := false,
        synchronize_data := false,
        forward_origins := ARRAY[]::text[],
        apply_delay := ''0''::interval,
        enabled := false,
        force_text_transfer := false,
        skip_schema := ARRAY[]::text[]
    )'
) AS t(subscription_id oid);
```

### 配置跨节点复制 {#configure-cross-node-replication}

接下来为从 n4 到 n2、n3 的反向复制做准备。**译校说明**：以下为上游教程记录的步骤。示例 SQL 实际连接 n2、n3 在当地建槽，而逻辑槽只能保留所在节点的 WAL。若要由 n4 发布，须核实 n4 上实际使用的发送端复制槽。不能以 n2、n3 上的槽已存在来判断 n4 的变更已得到保留。

- 原文在 n2 和 n3 创建复制槽，并将它们描述为用于保留来自 n4 的变更。
- 原文将这些槽与后续在 n2、n3 上创建、用于从 n4 接收数据的订阅对应。
- 提前建槽的意图是在建立订阅前就开始保留变更。


> [!NOTE]
>
> 目的是防止设置期间写入 n4 的数据丢失。实际保留位置取决于槽所在的发布节点。
>

#### 在 n2 上为后续订阅 sub_n4_n2 创建槽 {#create-a-slot-on-n2-for-a-future-subscription-sub_n4_n2}

在 n2 创建名为 `spk_inventory_n2_sub_n4_n2` 的复制槽。按上游教程，该槽对应将来从 n4 到 n2 的路径，此时尚无订阅使用它。请注意本节开头对复制方向的说明。

以下命令在 n2 上建槽。

```sql
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
    'SELECT slot_name, lsn
     FROM pg_create_logical_replication_slot(
         ''spk_inventory_n2_sub_n4_n2'',
         ''spock_output''
     )'
) AS t(slot_name text, lsn pg_lsn);
```

#### 在 n3 上为后续订阅 sub_n4_n3 创建槽 {#create-a-slot-on-n3-for-a-future-subscription-sub_n4_n3}

以下命令在 n3 上建槽。

```sql
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
    'SELECT slot_name, lsn
     FROM pg_create_logical_replication_slot(
         ''spk_inventory_n3_sub_n4_n3'',
         ''spock_output''
     )'
) AS t(slot_name text, lsn pg_lsn);
```


### 在其他节点触发同步，在源节点等待 {#trigger-a-sync-on-other-nodes-wait-on-source}

从 n1 向 n4 复制数据前，先确认 n1 已收到 n2 和 n3 的最新数据。

- 必须先将 n2 或 n3 上已发生的写入完整复制到 n1。
- 例如，用户一秒前在 n2 插入了一行。若向 n4 复制 n1 的数据前这一行尚未到达 n1，n4 的副本就会缺少它。
- 在 n2 触发同步事件，等 n1 收到该事件，即能确认 n1 已收到 n2 截至标记位置的全部变更。


> [!NOTE]
>
> 在 n2 触发 `sync_event`，向 n2 的复制流插入标记，在 n1 等待标记到达。再对 n3 重复操作。
>

#### 将 n2 同步到 n1 {#sync-n2-to-n1}

在 n2 调用 `sync_event()`，返回 LSN（0/1C9F400）。在 n1 等待复制到该位置。`wait_for_sync_event()` 完成时，n1 已收到 n2 截至该 LSN（含）的全部变更。

以下命令触发同步事件并等待完成。

```sql
-- Trigger sync event on n2
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
    'SELECT spock.sync_event()'
) AS t(sync_lsn pg_lsn);
-- Returns: 0/1C9F400

-- Wait for sync event on n1
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'CALL spock.wait_for_sync_event(true, ''n2'', ''0/1C9F400''::pg_lsn, 1200)'
) AS t(result bool);
```

#### 将 n3 同步到 n1 {#sync-n3-to-n1}

同样在 n3 触发 `sync_event()`，取得 LSN（0/1D0E510），再在 n1 等待。两次同步结束后，n1 都已追到 n2、n3 的标记位置。

以下命令在 n3 触发同步事件，并在 n1 等待完成。

```sql
-- Trigger sync event on n3
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
    'SELECT spock.sync_event()'
) AS t(sync_lsn pg_lsn);
-- Returns: 0/1D0E510

-- Wait for sync event on n1
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'CALL spock.wait_for_sync_event(true, ''n3'', ''0/1D0E510''::pg_lsn, 1200)'
) AS t(result bool);
```

### 将源节点数据复制到新订阅 {#copy-the-source-to-new-subscription}

此步骤执行大批量数据复制。

- 在 n4 创建并启用来自 n1 的订阅，设置 `synchronize_structure=true` 和 `synchronize_data=true`。
- Spock 会从 n1 转储完整结构（表、索引和约束等），恢复到 n4，再将所有表数据从 n1 复制到 n4。
- 创建订阅之前，先找出 n4 上需要排除的已有模式，如监控或管理工具的模式，形成 `skip_schema` 列表。Spock 将它交给 `pg_dump --exclude-schema`，复制数据时也跳过这些模式中的表，避免覆盖 n4 本地的工具和扩展。


> [!NOTE]
>
> 耗时随数据库大小而异，可能从几分钟到几小时。例如，同步 100 GB 数据库可能需要 30 分钟以上。
>

#### 检测 n4 上已有的模式 {#detect-existing-schemas-on-n4}

查询 n4 的 `information_schema`，找出用户创建的模式，排除 `pg_catalog`、`information_schema`、`spock`、`public` 等默认或系统相关模式。若找到 `mgmt_tools`、`monitoring` 等本地模式，则将它们排除在复制之外。

以下查询列出 n4 上已有的模式。

```sql
SELECT string_agg(schema_name, ',') as schemas
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT schema_name
     FROM information_schema.schemata
     WHERE schema_name NOT IN (''information_schema'', ''pg_catalog'', ''pg_toast'', ''spock'', ''public'')
     AND schema_name NOT LIKE ''pg_temp_%''
     AND schema_name NOT LIKE ''pg_toast_temp_%'''
) AS t(schema_name text);
-- Returns: 'mgmt_tools,monitoring' (if any exist)
```

#### 在 n4 创建并启用来自 n1 的订阅 {#create-an-enabled-subscription-on-n4-from-n1}

在 n4 创建以 n1 为提供方的订阅 `sub_n1_n4`。

主要参数如下。

- `synchronize_structure := true`：从 n1 转储并恢复结构。
- `synchronize_data := true`：从 n1 复制所有表数据。
- `enabled := true`：立即开始复制。
- `skip_schema := ARRAY['mgmt_tools','monitoring']::text[]`：排除检测到的模式。
- `forward_origins := ARRAY[]::text[]`：不转发源自其他节点的变更。

Spock 在内部执行以下操作。
- 在 n1 运行 pg_dump，并传入 --exclude-schema=mgmt_tools --exclude-schema=monitoring。
- 将转储恢复到 n4。
- 逐个处理 n1 复制集中的表，跳过 mgmt_tools 和 monitoring 模式，再用 COPY 将其余表的数据从 n1 传到 n4。
- 初始同步结束后，开始将 n1 的后续变更流式发送到 n4。

```sql
-- Build skip_schema array based on detected schemas
-- If schemas found: ARRAY['mgmt_tools','monitoring']::text[]
-- If no schemas: ARRAY[]::text[]

SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT spock.sub_create(
        subscription_name := ''sub_n1_n4'',
        provider_dsn := ''host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword'',
        replication_sets := ARRAY[''default'', ''default_insert_only'', ''ddl_sql''],
        synchronize_structure := true,
        synchronize_data := true,
        forward_origins := ARRAY[]::text[],
        apply_delay := ''0''::interval,
        enabled := true,
        force_text_transfer := false,
        skip_schema := ARRAY[''mgmt_tools'',''monitoring'']::text[]
    )'
) AS t(subscription_id oid);
```

### 在源节点触发同步，在新节点等待 {#trigger-a-sync-on-the-source-node-and-wait-on-the-new-node}

批量复制完成后，n4 可能还需要追赶复制期间在 n1 上发生的变更。

- 继续下一步前，应确认 n4 已完全追上 n1。
- 在 n1 触发 `sync_event`，标记当前复制位置，然后在 n4 等待该标记到达。标记到达并处理后，n4 已收到并应用 n1 截至此位置的所有变更。


> [!NOTE]
>
> 例如，10:00 开始复制 100 GB 数据，用户在 10:00 至 10:30 向 n1 插入了 1000 行。10:30 批量复制结束时，这 1000 行可能仍在传输。必须等 n4 应用完全部 1000 行再继续，以免漏数据。
>

#### 在 n1 触发同步事件 {#trigger-a-sync-event-on-n1}

在 n1 复制流的当前位置插入标记，返回的 LSN（0/1E1F620）精确标识它在 n1 事务日志中的位置。

以下命令在 n1 触发同步事件。

```sql
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'SELECT spock.sync_event()'
) AS t(sync_lsn pg_lsn);
-- Returns: 0/1E1F620
```

#### 在 n4 等待同步事件 {#wait-for-sync-event-on-n4}

在 n4 等待 LSN 为 0/1E1F620 的标记到达并处理。此调用会阻塞，直到来自 n1 的订阅复制到该位置。本手工示例将超时设为 1200 秒（20 分钟），可根据环境调整，防止故障时无限等待。自动过程 `spock.add_node()` 的内部同步等待默认较短，为 180 秒。

以下命令在 n4 等待同步事件。

```sql
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'CALL spock.wait_for_sync_event(true, ''n1'', ''0/1E1F620''::pg_lsn, 1200)'
) AS t(result bool);
```


### 核对提交时间戳并推进复制槽 {#check-the-commit-timestamp-and-advance-slots}

这一步可避免重复传输数据。

n4 已经从 n1 取得完整数据，其中也包括最初源自 n2、n3 的数据。此时订阅 sub_n2_n4 和 sub_n3_n4 尚未启用，n2、n3 上的复制槽一直保留着变更。


> [!WARNING]
>
> 若直接启用这些订阅，n4 可能重复收到同一批数据，例如先经 n1 收到 n2 的数据，又直接从 n2 收到一次。
>

用 `lag_tracker` 找出 n4 最近处理的、源自 n2 的变更的提交时间戳，即使它是经 n1 转发的也可以。随后推进 n2 的复制槽，跳过该时间戳之前已同步的数据。启用 sub_n2_n4 后，只需发送初始同步之后的新变更。


> [!NOTE]
>
> 对每个副本执行以下操作：在 n4 的 `lag_tracker` 上取得来自 n2 的最近变更的 `commit_timestamp`，在 n2 用 `get_lsn_from_commit_ts()` 将它换算为 LSN，再将 n2 的复制槽推进到该位置。对 n3 重复这些步骤。
>

#### 取得 n2 到 n4 的提交时间戳 {#get-the-commit-timestamp-for-n2-to-n4}

在 n4 的 `lag_tracker` 中查找满足 `origin_name='n2'` 和 `receiver_name='n4'` 的行。`commit_timestamp` 指明 n4 最近一次收到源自 n2 的变更所对应的提交时间。即使变更经过 n1，`lag_tracker` 仍记录最初来源。

下面的查询取得提交时间戳。

```sql
SELECT commit_timestamp
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT commit_timestamp
     FROM spock.lag_tracker
     WHERE origin_name = ''n2'' AND receiver_name = ''n4'''
) AS t(commit_timestamp timestamp);
-- Returns: 2025-01-15 10:30:45.123456
```

#### 推进 n2 上的复制槽 {#advance-the-slot-on-n2}

先用 `spock.get_lsn_from_commit_ts()` 将时间戳（2025-01-15 10:30:45.123456）换算为 n2 日志中相应的 LSN，再用 `pg_replication_slot_advance()` 将槽推进到该位置。上游称该位置为 `restart_lsn`；对于逻辑槽，应以函数返回的实际位置和 confirmed_flush_lsn 核实推进结果。

槽 `spk_inventory_n2_sub_n2_n4` 一直保留 n2 上的变更。推进到指定 LSN，会跳过 n4 已有的那部分数据，随后只需处理 n4 仍缺少的新变更。

下列命令转换时间戳并推进复制槽。

```sql
-- Get LSN from commit timestamp
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
    'WITH lsn_cte AS (
         SELECT spock.get_lsn_from_commit_ts(
             ''spk_inventory_n2_sub_n2_n4'',
             ''2025-01-15 10:30:45.123456''::timestamp
         ) AS lsn
     )
     SELECT pg_replication_slot_advance(''spk_inventory_n2_sub_n2_n4'', lsn)
     FROM lsn_cte'
) AS t(slot_name name, end_lsn pg_lsn);
```

#### 为 n3 到 n4 重复操作 {#repeat-for-n3-to-n4}

下列命令为 n3 到 n4 执行相同操作。

```sql
-- Get commit timestamp
SELECT commit_timestamp
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT commit_timestamp
     FROM spock.lag_tracker
     WHERE origin_name = ''n3'' AND receiver_name = ''n4'''
) AS t(commit_timestamp timestamp);
-- Returns: 2025-01-15 10:30:46.789012

-- Advance the slot on n3
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
    'WITH lsn_cte AS (
         SELECT spock.get_lsn_from_commit_ts(
             ''spk_inventory_n3_sub_n3_n4'',
             ''2025-01-15 10:30:46.789012''::timestamp
         ) AS lsn
     )
     SELECT pg_replication_slot_advance(''spk_inventory_n3_sub_n3_n4'', lsn)
     FROM lsn_cte'
) AS t(slot_name name, end_lsn pg_lsn);
```


### 启用暂时禁用的订阅 {#enable-disabled-subscriptions}

启用副本节点向新节点发送数据的订阅，并用此前保存的同步 LSN 验证进度。


> [!NOTE]
>
> 启用此前禁用的 sub_n2_n4 和 sub_n3_n4，用当时记录的 LSN 核实起始进度。
>

创建 sub_n2_n4 并在 n2 触发 `sync_event` 时，得到 LSN 0/1A7D1E0，标记了最初准备复制槽的时间点。到现在可能已过去数小时，槽始终保留着变更。需要确认订阅确实覆盖最初标记的进度，没有越过尚未处理的数据。

每启用一个订阅，都用保存的 LSN 调用 `wait_for_sync_event()`，确认订阅至少已经处理到该同步点，再继续操作。

此前已推进复制槽以跳过重复数据。因此，启用后的订阅只发送初始同步之后发生的新变更。

#### 在 n4 上启用 sub_n2_n4 {#enable-sub_n2_n4-on-n4}

在 n4 调用 `spock.sub_enable()`。订阅工作进程会启动、连接 n2，并开始从复制槽拉取变更。

以下示例启用订阅。

```sql
-- Enable the subscription
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT spock.sub_enable(
        subscription_name := ''sub_n2_n4'',
        immediate := true
    )'
) AS t(result bool);
```

#### 等待此前记录的 n2 同步事件 {#wait-for-stored-sync-event-from-n2}

取出保存的 LSN（0/1A7D1E0），传给 `wait_for_sync_event()`。这是 ZODAN 的关键校验，确认订阅已追到最初设置时标记的位置，保证数据一致。

下面的查询取出保存的 LSN 并等待同步事件。

```sql
-- Retrieve stored LSN
SELECT sync_lsn FROM temp_sync_lsns WHERE origin_node = 'n2';
-- Returns: 0/1A7D1E0

-- Wait for that sync event on n4
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'CALL spock.wait_for_sync_event(true, ''n2'', ''0/1A7D1E0''::pg_lsn, 1200)'
) AS t(result bool);
```

#### 确认订阅正在复制 {#verify-the-subscription-is-replicating}

通过 `sub_show_status()` 查看订阅状态。预期为 `status='replicating'`，表示工作进程已连接 n2 并正在应用变更。若在此阶段仍为 down、initializing 等其他状态，应进一步检查。

下面在 n4 检查订阅状态。

```sql
-- Check subscription status on n4
SELECT subscription_name, status, provider_node
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT subscription_name, status, provider_node
     FROM spock.sub_show_status()
     WHERE subscription_name = ''sub_n2_n4'''
) AS t(subscription_name text, status text, provider_node text);

-- Expected output:
--  subscription_name |   status    | provider_node
-- -------------------+-------------+---------------
--  sub_n2_n4         | replicating | n2
```

#### 对 sub_n3_n4 重复上述步骤 {#repeat-the-steps-for-sub_n3_n4}

下列命令启用订阅并验证复制。

```sql
-- Enable subscription
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT spock.sub_enable(
        subscription_name := ''sub_n3_n4'',
        immediate := true
    )'
) AS t(result bool);

-- Retrieve stored LSN
SELECT sync_lsn FROM temp_sync_lsns WHERE origin_node = 'n3';
-- Returns: 0/1B8E2F0

-- Wait for stored sync event
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'CALL spock.wait_for_sync_event(true, ''n3'', ''0/1B8E2F0''::pg_lsn, 1200)'
) AS t(result bool);

-- Verify status
SELECT subscription_name, status, provider_node
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
    'SELECT subscription_name, status, provider_node
     FROM spock.sub_show_status()
     WHERE subscription_name = ''sub_n3_n4'''
) AS t(subscription_name text, status text, provider_node text);
```


### 在其他节点创建来自新节点的订阅 {#create-subscriptions-from-other-nodes-to-new-node}

本步骤打通反向路径，使 n4 与其他节点可以双向复制。

此前数据从其他节点流向 n4。现在在 n1、n2、n3 上创建以 n4 为提供方的订阅，让数据从 n4 流向这些节点。

应等 n4 具备完整数据后再让其他节点订阅它。如果过早建立订阅，其他节点可能尝试从空的 n4 同步。

n1、n2、n3 已有全部数据，因此这些订阅应使用 `synchronize_structure=false` 和 `synchronize_data=false`，只接收此后直接在 n4 上发生的新变更，无须复制已有数据。

此时集群形成完整双向复制。

- n1 发往 n4，n4 也发往 n1。
- n2 发往 n4，n4 也发往 n2。
- n3 发往 n4，n4 也发往 n3。


#### 在 n1 创建 sub_n4_n1 {#create-sub_n4_n1-on-n1}

在接收节点 n1 上建立订阅，并将 n4 指定为提供方。订阅对象位于接收端。此后，直接在 n4 上发生的 INSERT、UPDATE 和 DELETE 都会复制到 n1。

以下示例创建订阅。

```sql
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'SELECT spock.sub_create(
        subscription_name := ''sub_n4_n1'',
        provider_dsn := ''host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword'',
        replication_sets := ARRAY[''default'', ''default_insert_only'', ''ddl_sql''],
        synchronize_structure := false,
        synchronize_data := false,
        forward_origins := ARRAY[]::text[],
        apply_delay := ''0''::interval,
        enabled := true,
        force_text_transfer := false,
        skip_schema := ARRAY[]::text[]
    )'
) AS t(subscription_id oid);
```

#### 在 n2 创建 sub_n4_n2 {#create-sub_n4_n2-on-n2}

同样，在 n2 创建从 n4 拉取数据的订阅，n2 随后会收到 n4 的变更。

以下命令在 n2 创建订阅。

```sql
SELECT *
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
    'SELECT spock.sub_create(
        subscription_name := ''sub_n4_n2'',
        provider_dsn := ''host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword'',
        replication_sets := ARRAY[''default'', ''default_insert_only'', ''ddl_sql''],
        synchronize_structure := false,
        synchronize_data := false,
        forward_origins := ARRAY[]::text[],
        apply_delay := ''0''::interval,
        enabled := true,
        force_text_transfer := false,
        skip_schema := ARRAY[]::text[]
    )'
) AS t(subscription_id oid);
```

#### 在 n3 创建 sub_n4_n3 {#create-sub_n4_n3-on-n3}

以下命令在 n3 创建订阅。

```sql
SELECT * FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
    'SELECT spock.sub_create(
        subscription_name := ''sub_n4_n3'',
        provider_dsn := ''host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword'',
        replication_sets := ARRAY[''default'', ''default_insert_only'', ''ddl_sql''],
        synchronize_structure := false,
        synchronize_data := false,
        forward_origins := ARRAY[]::text[],
        apply_delay := ''0''::interval,
        enabled := true,
        force_text_transfer := false,
        skip_schema := ARRAY[]::text[]
    )'
) AS t(subscription_id oid);
```

### 监控复制延迟 {#monitor-replication-lag}

接下来确认 n4 能跟上 n1 的进度。

在 n4 监控 lag_tracker，查看事务在 n1 提交到在 n4 应用之间的时间差，以判断 n1 到 n4 的复制是否跟得上。

如果延迟持续增长，例如由 5 秒变为 10 秒、30 秒，说明 n4 无法跟上 n1 的写入负载。可能原因包括：

- 网络带宽不足。
- n4 的硬件性能低于 n1。
- 长事务阻塞复制。

本例期望延迟低于 59 秒，或 lag_bytes=0（n4 已处理完所有变更）。若延迟持续较低，说明 n4 已成功接入。

下面的查询用于监控复制延迟。

```sql
-- Monitor lag from n1 → n4 on n4
DO $$
DECLARE
    lag_interval interval;
    lag_bytes bigint;
BEGIN
    LOOP
        SELECT now() - commit_timestamp, replication_lag_bytes
        INTO lag_interval, lag_bytes
        FROM dblink(
            'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
            'SELECT now() - commit_timestamp, replication_lag_bytes
             FROM spock.lag_tracker
             WHERE origin_name = ''n1'' AND receiver_name = ''n4'''
        ) AS t(lag_interval interval, lag_bytes bigint);

        RAISE NOTICE 'n1 → n4 lag: % (bytes: %)',
            COALESCE(lag_interval::text, 'NULL'),
            COALESCE(lag_bytes::text, 'NULL');

        EXIT WHEN lag_interval IS NOT NULL
                  AND (extract(epoch FROM lag_interval) < 59 OR lag_bytes = 0);

        PERFORM pg_sleep(1);
    END LOOP;

    RAISE NOTICE 'Replication lag monitoring complete';
END;
$$;

-- Expected output:
-- NOTICE:  n1 → n4 lag: 00:00:02.345 (bytes: 1024)
-- NOTICE:  n1 → n4 lag: 00:00:01.123 (bytes: 512)
-- NOTICE:  n1 → n4 lag: 00:00:00.456 (bytes: 0)
-- NOTICE:  Replication lag monitoring complete
```


### 显示所有节点 {#show-all-nodes}

确认所有节点均已登记。下列查询显示全部已登记节点。

```sql
SELECT n.node_id, n.node_name, n.location, n.country, i.if_dsn
FROM dblink(
    'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
    'SELECT n.node_id, n.node_name, n.location, n.country, i.if_dsn
     FROM spock.node n
     JOIN spock.node_interface i ON n.node_id = i.if_nodeid
     ORDER BY n.node_name'
) AS t(node_id integer, node_name text, location text, country text, if_dsn text);

-- Expected output:
--  node_id | node_name |  location   | country |                           if_dsn
-- ---------+-----------+-------------+---------+------------------------------------------------------------
--    16385 | n1        | New York    | USA     | host=127.0.0.1 dbname=inventory port=5432 user=alice ...
--    16386 | n2        | Chicago     | USA     | host=127.0.0.1 dbname=inventory port=5433 user=alice ...
--    16387 | n3        | Boston      | USA     | host=127.0.0.1 dbname=inventory port=5434 user=alice ...
--    16389 | n4        | Los Angeles | USA     | host=127.0.0.1 dbname=inventory port=5435 user=alice ...
```

### 显示所有订阅的状态 {#show-the-status-of-all-subscriptions}

确认所有订阅均在复制。下面的查询列出各节点上的订阅状态。

```sql
-- Get subscriptions from all nodes
SELECT node_name, subscription_name, status, provider_node
FROM (
    -- n1 subscriptions
    SELECT 'n1' as node_name, *
    FROM dblink(
        'host=127.0.0.1 dbname=inventory port=5432 user=alice password=1safepassword',
        'SELECT subscription_name, status, provider_node FROM spock.sub_show_status()'
    ) AS t(subscription_name text, status text, provider_node text)

    UNION ALL

    -- n2 subscriptions
    SELECT 'n2' as node_name, *
    FROM dblink(
        'host=127.0.0.1 dbname=inventory port=5433 user=alice password=1safepassword',
        'SELECT subscription_name, status, provider_node FROM spock.sub_show_status()'
    ) AS t(subscription_name text, status text, provider_node text)

    UNION ALL

    -- n3 subscriptions
    SELECT 'n3' as node_name, *
    FROM dblink(
        'host=127.0.0.1 dbname=inventory port=5434 user=alice password=1safepassword',
        'SELECT subscription_name, status, provider_node FROM spock.sub_show_status()'
    ) AS t(subscription_name text, status text, provider_node text)

    UNION ALL

    -- n4 subscriptions
    SELECT 'n4' as node_name, *
    FROM dblink(
        'host=127.0.0.1 dbname=inventory port=5435 user=alice password=1safepassword',
        'SELECT subscription_name, status, provider_node FROM spock.sub_show_status()'
    ) AS t(subscription_name text, status text, provider_node text)
) combined
ORDER BY node_name, subscription_name;

-- Expected output (12 rows):
--  node_name | subscription_name |   status    | provider_node
-- -----------+-------------------+-------------+---------------
--  n1        | sub_n2_n1         | replicating | n2
--  n1        | sub_n3_n1         | replicating | n3
--  n1        | sub_n4_n1         | replicating | n4
--  n2        | sub_n1_n2         | replicating | n1
--  n2        | sub_n3_n2         | replicating | n3
--  n2        | sub_n4_n2         | replicating | n4
--  n3        | sub_n1_n3         | replicating | n1
--  n3        | sub_n2_n3         | replicating | n2
--  n3        | sub_n4_n3         | replicating | n4
--  n4        | sub_n1_n4         | replicating | n1
--  n4        | sub_n2_n4         | replicating | n2
--  n4        | sub_n3_n4         | replicating | n3
```


### 验证 {#verification}

执行以下测试，确认 n1 与 n4 之间的复制正常。

先创建测试表并插入数据。

```sql
-- On n1
CREATE TABLE test_replication (id serial primary key, data text, created_at timestamp default now());
INSERT INTO test_replication (data) VALUES ('Test from n1');

-- On n4 (wait a few seconds)
SELECT * FROM test_replication;
-- Expected: Row appears on n4
```

### 测试 n4 与 n1 之间的复制 {#test-replication-between-n4-and-n1}

在 n4 插入数据。

```sql
INSERT INTO test_replication (data) VALUES ('Test from n4');
```
随后在 n1 验证复制结果。

```sql
-- On n1 (wait a few seconds)
SELECT * FROM test_replication;
-- Expected: Both rows appear on n1
```


### 最终集群拓扑 {#our-final-cluster-topology}

```
        ┌──────┐
        │  n1  │ (source)
        └──┬───┘
     ┌─────┼─────┬─────┐
     │     │     │     │
  ┌──▼──┐ │  ┌──▼──┐ ┌▼────┐
  │ n2  │◄┼──┤ n3  │ │ n4  │ (new)
  └──┬──┘ │  └──┬──┘ └┬────┘
     │    │     │     │
     └────┴─────┴─────┘
```

现在所有节点都已实现双向复制。

- n1、n2、n3 和 n4 两两双向连接。
- 共有 12 个订阅，每个节点订阅其余三个节点。


## 故障排查 {#troubleshooting}

以下命令可用于诊断节点添加过程中遇到的问题。

### 订阅停留在 initializing 或 down 状态 {#subscription-status-stuck-in-initializing-or-down}

可使用下列命令检查哪个节点的复制状态出现异常。

```sql
-- Check subscription status
SELECT * FROM spock.sub_show_status();

-- Check table sync status
SELECT * FROM spock.sub_show_table('sub_n2_n4', 'public.test_replication');

-- Check logs
SELECT * FROM pg_stat_replication;
```

### 添加节点时超时 {#node-addition-fails-with-a-timeout}

若 `spock.add_node()` 在等待同步事件或等待新节点追平进度时超时，可能是数据库较大，超过了默认的 3 分钟上限。使用 `spock.remove_node` 移除未完全加入的节点，再按[设置同步超时](#setting-the-synchronisation-timeout) 延长等待时间后重试。

```sql
SET spock.sync_timeout = '2h';
```

先用下文的延迟查询估算实际追赶时间，再选择超时值。

### 复制延迟过高 {#replication-lag-too-high}

用下列命令在订阅方检查复制延迟。

```sql
-- Check lag on receiver node
SELECT origin_name, receiver_name,
       now() - commit_timestamp as lag,
       replication_lag_bytes
FROM spock.lag_tracker
ORDER BY lag DESC;
```

### 复制槽不再推进 {#slot-not-advancing}

用下列命令检查复制槽状态。

```sql
-- Check slot status
SELECT slot_name, slot_type, active, restart_lsn, confirmed_flush_lsn
FROM pg_replication_slots
WHERE slot_name LIKE 'spk_%';
```

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/modify/zodan/zodan_tutorial.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
