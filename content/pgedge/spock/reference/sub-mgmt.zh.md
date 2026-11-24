---
title: "订阅管理函数"
description: "在多主复制环境中，各节点可持有一个或多个订阅。每个订阅标识发布节点，本地订阅方作为其复制目标。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/sub_mgmt.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



在多主复制环境中，各节点可持有一个或多个订阅。每个订阅标识发布节点，本地订阅方作为其复制目标。


| 命令 | 说明 |
| --- | --- |
| [spock.sub_create](/zh/pgedge/spock/reference/functions/spock-sub-create/) | 创建订阅。 |
| [spock.sub_drop](/zh/pgedge/spock/reference/functions/spock-sub-drop/) | 删除订阅。 |
| [spock.sub_disable](/zh/pgedge/spock/reference/functions/spock-sub-disable/) | 禁用订阅并断开与提供方的连接。 |
| [spock.sub_enable](/zh/pgedge/spock/reference/functions/spock-sub-enable/) | 启用已禁用的订阅。 |
| [spock.sub_alter_interface](/zh/pgedge/spock/reference/functions/spock-sub-alter-interface/) | 切换连接提供方所用的接口。 |
| [spock.sub_alter_sync](/zh/pgedge/spock/reference/functions/spock-sub-alter-sync/) | 一次同步所有尚未同步的表。 |
| [spock.sub_alter_options](/zh/pgedge/spock/reference/functions/spock-sub-alter-options/) | 一次原子地修改一个或多个订阅选项。 |
| [spock.sub_resync_table](/zh/pgedge/spock/reference/functions/spock-sub-resync-table/) | 重新同步单张表。 |
| [spock.sub_wait_for_sync](/zh/pgedge/spock/reference/functions/spock-sub-wait-for-sync/) | 执行 `spock.sub_create` 或 `spock.sub_alter_sync` 后等待订阅同步完成。 |
| [spock.table_wait_for_sync](/zh/pgedge/spock/reference/functions/spock-table-wait-for-sync/) | 只等待订阅的初始同步和指定表。 |
| [spock.sub_show_status](/zh/pgedge/spock/reference/functions/spock-sub-show-status/) | 查看订阅状态和基本信息。 |
| [spock.sub_show_table](/zh/pgedge/spock/reference/functions/spock-sub-show-table/) | 查看表的同步状态。 |
| [spock.sub_add_repset](/zh/pgedge/spock/reference/functions/spock-sub-add-repset/) | 向订阅添加复制集。 |
| [spock.sub_remove_repset](/zh/pgedge/spock/reference/functions/spock-sub-remove-repset/) | 从订阅移除复制集。 |

## 创建订阅 {#creating-a-subscription}

使用 psql 连接服务器，运行 `spock.sub_create`，让当前节点订阅发布节点。

```sql
SELECT spock.sub_create(subscription_name, provider_dsn, replication_sets,
    synchronize_structure, synchronize_data, forward_origins, apply_delay,
    force_text_transfer, enabled, skip_schema)
```

参数如下。

- `subscription_name` 是订阅的唯一名称。
- `provider_dsn` 是连接提供方的连接串。
- `replication_sets` 是要订阅的已有复制集的名称数组，默认 `{default,default_insert_only,ddl_sql}`。
- `synchronize_structure` 是布尔值，决定是否将提供方的结构同步到订阅方，默认 `false`。
- `synchronize_data` 决定是否从提供方同步数据到订阅方，本版默认值为 `false`。调用时宜显式指定，具体签名见本版本的函数参考。
- `forward_origins` 是要转发的来源名称数组。支持的取值，以及与其他启用的订阅并用时的限制，见下文[来源转发](#origin-forwarding)。
- `apply_delay` 指定延迟复制的时长，默认 `0` 秒。
- 将 `force_text_transfer` 设为 `true`，可以强制提供方按文本表示复制所有列。这样较慢，但可用于在订阅方改变复制列的类型。默认 `false`。
- `enabled` 决定是否在创建后立即启动订阅，默认 `true`。
- `skip_schema` 为模式名数组。应用工作进程会忽略这些模式中的变更。默认 `{}`，即不跳过任何模式。

以下列命令为例：

```sql
SELECT spock.sub_create('accts',
    'host=178.12.15.12 user=carol dbname=accounting',
    ARRAY['payables']);
```

此例创建名为 `accts` 的订阅，使用 `carol` 的凭据连接 `178.12.15.12` 上的 `accounting` 数据库。新订阅接收 `payables` 复制集。

## 删除订阅 {#dropping-a-subscription}

使用 psql 连接服务器，调用 `spock.sub_drop` 删除订阅。

```sql
SELECT spock.sub_drop(subscription_name, ifexists)
```

参数如下。

- `subscription_name` 是已有订阅名称。
- 若 `ifexists` 为 `true`，指定订阅不存在时不会报错。默认是 `false`。

以下列命令为例：

```sql
SELECT spock.sub_drop('accts', true);
```

删除名为 `accts` 的订阅。最后一个参数为 `true`（`ifexists = true`），因此订阅不存在也不报错。

## 来源转发 {#origin-forwarding}

`forward_origins` 决定应用工作进程是否也处理由直接提供方从更上游对等节点转来的事务（级联或多跳拓扑）。默认值 `{}` 只接收提供方本地产生的变更，是两节点普通双向复制所用的设置，可防止变更绕回来源节点。`{all}` 则转发任意来源的变更。

转发工作进程会推进本地对应被转发对端的订阅的复制来源进度。例如可预先建立一个禁用的订阅，以后从正确位置恢复，而不必重新全量同步。同一对端至多匹配一个本地订阅，否则会因匹配不唯一而复制失败。如果匹配的订阅也已启用，其应用进程会占用同一复制来源。因此 Spock 要求启用了来源转发的订阅必须是本节点唯一启用的订阅。

- 本节点已有其他订阅启用时，下列操作都会失败：在 `spock.sub_create` 中指定 `enabled := true` 和 `{all}`、用 `spock.sub_enable` 启动开启转发的订阅，或通过 `spock.sub_alter_options` 在已启用的订阅上开启转发。
- 若本节点已有订阅正在转发来源，使用 `spock.sub_create` 配合 `enabled := true` 或使用 `spock.sub_enable` 启用另一订阅均会失败。
- 若订阅保持禁用，始终可以修改 `forward_origins`。只有实际启用时才执行上述互斥检查。

## 订阅管理函数 {#subscription-management-functions-1}

使用以下函数及选项管理订阅。

### spock.sub_create {#spocksub_create}

使用 `spock.sub_create` 从当前节点创建到提供方的订阅。

`spock.sub_create(subscription_name name, provider_dsn text, replication_sets text[], synchronize_structure boolean, synchronize_data boolean, forward_origins text[], apply_delay interval, force_text_transfer boolean, enabled boolean, skip_schema text[])`

命令返回时，后台工作可能尚未完成。

参数如下。

- `subscription_name` 是订阅的唯一名称。
- `provider_dsn` 是连接提供方的连接串。
- `replication_sets` 是要订阅的已有复制集名称数组，默认 `{default,default_insert_only,ddl_sql}`。
- `synchronize_structure` 指定是否从提供方向订阅方同步结构，默认 `false`。
- `synchronize_data` 指定是否从提供方向订阅方同步数据，本版默认为 `false`。
- `forward_origins` 是要转发的来源名数组。支持的取值和多订阅限制见上文[来源转发](#origin-forwarding)。
- `apply_delay` 指定复制的延迟秒数，默认 `0` 秒。
- 将 `force_text_transfer` 设为 `true`，会强制提供方用文本表示传输所有列。速度较慢，但可用于改变订阅方复制列的类型。默认 `false`。
- `enabled` 决定是否在创建后立即启动订阅，默认 `true`。
- `skip_schema` 是应用进程应跳过变更的模式名数组，默认 `{}`。

复制连接会使用 `subscription_name` 作为 `application_name`，因此可在 `pg_stat_replication` 监控视图中看到该名称。将 Spock 用于同步复制时，也可在 `synchronous_standby_names` 中引用它。

使用 `spock.sub_wait_for_sync(subscription_name)` 等待订阅在后台启动复制，并完成必要的结构或数据同步。

### spock.sub_drop {#spocksub_drop}

使用 `spock.sub_drop` 断开订阅并将其从目录中删除。

`spock.sub_drop(subscription_name name, ifexists bool)`

参数如下。

- `subscription_name` 是已有订阅名称。
- `ifexists` 控制订阅不存在时如何处理。为 `true` 时不报错，默认 `false`。

### spock.sub_disable {#spocksub_disable}

使用 `spock.sub_disable` 禁用订阅并断开与提供方的连接。

`spock.sub_disable(subscription_name name, immediate bool)`

参数如下。

- `subscription_name` 是已有订阅名称。
- `immediate` 决定何时停止订阅。设为 `true` 时立即停止，设为 `false`（默认）则等当前事务结束后停止。

### spock.sub_enable {#spocksub_enable}

使用 `spock.sub_enable` 启用已禁用的订阅。

`spock.sub_enable(subscription_name name, immediate bool)`

参数如下。
- `subscription_name` 是已有订阅名称。
- `immediate` 决定何时启动订阅。设为 `true` 时立即启动，设为 `false`（默认）则等当前事务结束后启动。

若本节点另有订阅已启用来源转发，此操作会失败，详见上文[来源转发](#origin-forwarding)。

### spock.sub_alter_interface {#spocksub_alter_interface}

使用 `spock.sub_alter_interface` 为订阅改用提供方的另一个连接接口。

`spock.sub_alter_interface(subscription_name name, interface_name name)`

参数如下。

- `subscription_name` 是已有订阅名称。
- `interface_name` 是当前提供方节点上已有接口的名称。

### spock.sub_alter_sync {#spocksub_alter_sync}

使用 `spock.sub_alter_sync` 一次发起所有复制集中尚未同步的表的同步。

`spock.sub_alter_sync(subscription_name name, truncate boolean DEFAULT false)`

各表会依次复制并同步。命令立即返回，如需等待完成，可调用 `spock.sub_wait_for_sync`。

参数如下。

- `subscription_name` 是已有订阅名称。
- `truncate` 决定复制前是否截断表。若为 `true`，会先截断再复制，默认 `false`。

### spock.sub_resync_table {#spocksub_resync_table}

使用 `spock.sub_resync_table` 重新同步一张已有的表。

`spock.sub_resync_table(subscription_name name, relation regclass)`

待同步表不能被任何外键约束引用。

安排重新同步后，如果提供方的本地缓存 `spock.node` 记录与提供方自身记录不同，函数会发出 `WARNING`，详见 [spock.sub_resync_table](/zh/pgedge/spock/reference/functions/spock-sub-resync-table/)。


> [!WARNING]
> 按默认设置，函数会立即截断表，然后才开始同步。同步期间该表可能为空。命令不会等待完成，如需等待，可用 `spock.table_wait_for_sync`。
>

参数如下。

- `subscription_name` 是已有订阅名称。
- `relation` 为已有表名，可带模式限定。

### spock.sub_wait_for_sync {#spocksub_wait_for_sync}

在 `spock.sub_create` 或 `spock.sub_alter_sync` 之后，使用 `spock.sub_wait_for_sync` 等待订阅完成同步。

`spock.sub_wait_for_sync(subscription_name name)`

函数会等待订阅的初始结构／数据同步（如有），也会等待排队逐表重新同步的表全部完成。

参数如下。

- `subscription_name` 是已有订阅名称。

若更改复制集时已请求重新同步，最好先在提供方运行 `SELECT spock.wait_slot_confirm_lsn(NULL, NULL)`，然后才在订阅方调用 `spock.sub_wait_for_sync`。

### spock.table_wait_for_sync {#spocktable_wait_for_sync}

使用 `spock.table_wait_for_sync` 只等待订阅的初始同步和指定表的同步。

`spock.table_wait_for_sync(subscription_name name, relation regclass)`

类似 `spock.sub_wait_for_sync`，但只等待订阅初始同步和具名表，忽略其他待重新同步的表。

### spock.wait_slot_confirm_lsn {#spockwait_slot_confirm_lsn}

使用 `spock.wait_slot_confirm_lsn` 等待本节点各复制槽确认到达函数调用时的 WAL 插入位置。需要检查多个提供方时，应在相应提供方执行。

`SELECT spock.wait_slot_confirm_lsn(NULL, NULL)`

各槽的 `confirmed_flush_lsn` 达到或越过调用时 `pg_current_wal_insert_lsn()` 的位置后，函数返回。

可选参数如下。

- 第一个参数可指定只等待一个复制槽。
- 第二个参数可指定要等待的 LSN，取代调用时的插入位置。通常两个参数均保留 `NULL`。

可据此确保所有订阅方均已收到提供方截至某一位置的变更。

### spock.sub_show_status {#spocksub_show_status}

使用 `spock.sub_show_status` 查看订阅的状态与基本信息。

`spock.sub_show_status(subscription_name name DEFAULT NULL)`

参数如下。

- `subscription_name` 可选，指定已有订阅名。省略或传入 `NULL` 时，返回本节点全部订阅的状态。

每个订阅返回一行，列为 `subscription_name`、`status`、`provider_node`、`provider_dsn`、`slot_name`、`replication_sets`、`forward_origins`。

### spock.sub_show_table {#spocksub_show_table}

使用 `spock.sub_show_table` 查看指定表的同步状态。

`spock.sub_show_table(subscription_name name, relation regclass)`

参数如下。

- `subscription_name` 是已有订阅名称。
- `relation` 为已有表名，可带模式限定。

### spock.sub_add_repset {#spocksub_add_repset}

使用 `spock.sub_add_repset` 将一个复制集加入订阅。

`spock.sub_add_repset(subscription_name name, replication_set name)`

它只启用该复制集后续事件的接收，不会同步已有数据。

参数如下。

- `subscription_name` 是已有订阅名称。
- `replication_set` 是要加入指定订阅的复制集名。

### spock.sub_remove_repset {#spocksub_remove_repset}

使用 `spock.sub_remove_repset` 从订阅中移除一个复制集。

`spock.sub_remove_repset(subscription_name name, replication_set name)`

参数如下。

- `subscription_name` 是已有订阅名称。
- `replication_set` 是要移除的复制集名。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/sub_mgmt.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
