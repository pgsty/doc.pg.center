---
title: "节点管理"
description: "使用本节的命令管理复制集群中的节点。"
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/node_mgmt.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
translation_notice: en
translation_status: translated
---



使用本节的命令管理复制集群中的节点。

| 命令 | 说明 |
| --- | --- |
| [spock.node_add_interface](/zh/pgedge/spock/reference/functions/spock-node-add-interface/) | 为节点添加接口。 |
| [spock.node_create](/zh/pgedge/spock/reference/functions/spock-node-create/) | 创建 `spock` 节点。 |
| [spock.node_drop](/zh/pgedge/spock/reference/functions/spock-node-drop/) | 删除 `spock` 节点。 |
| [spock.node_drop_interface](/zh/pgedge/spock/reference/functions/spock-node-drop-interface/) | 移除已有接口。 |
| [spock.node_info](/zh/pgedge/spock/reference/functions/spock-node-info/) | 返回本地 Spock 节点的信息。 |
| [spock.node_alter](/zh/pgedge/spock/reference/functions/spock-node-alter/) | 修改本节点的位置、国家或地区及其他信息，合并 info 并校验其中的 tiebreaker。 |
| [spock.node_refresh_info](/zh/pgedge/spock/reference/functions/spock-node-refresh-info/) | 刷新本节点缓存的一个或全部对等节点的位置、国家或地区及其他信息。 |


## 创建节点 {#creating-a-node}

用 psql 连接服务器，运行 `spock.node_create` 创建 Spock 节点。

```sql
SELECT spock.node_create(node_name, dsn)
```

参数如下。

- 节点名称。
- 节点所在服务器的 DSN。


> [!NOTE]
> DSN 是到待创建节点的连接串。例如，要以 `carol` 的身份连接 IP 为 `10.1.1.1` 的 `acctg` 数据库，可写为 `host=10.1.1.1 user=carol dbname=acctg`。
>

`location`、`country` 和 `info` 都是标记节点的可选参数，默认 `null`。

以下列命令为例：

```sql
SELECT spock.node_create('n1', 'host=178.12.15.12 user=carol dbname=accounting');
```

它创建节点 `n1`，通过用户 `carol` 的凭据连接 `178.12.15.12` 上的 `accounting` 数据库。

## 删除节点 {#dropping-a-node}

用 psql 连接服务器，执行 `spock.node_drop` 删除 Spock 节点。

```sql
SELECT spock.node_drop(node_name, ifexists)
```

参数如下。

- 节点名称。
- 布尔参数 `ifexists` 设为 `true` 时，若节点不存在也不报错。

以下列命令为例：

```sql
SELECT spock.node_drop('n1', true);
```

这会删除名为 `n1` 的节点。由于 `ifexists` 为 `true`，节点不存在时也不报错。

## 自动传播节点元数据 {#automatic-node-metadata-propagation}

无论使用 [`spock.node_alter`](/zh/pgedge/spock/reference/functions/spock-node-alter/) 还是直接执行 `UPDATE spock.node SET ... WHERE node_id = (SELECT node_id FROM spock.node_info())`，本节点的 `location`、`country` 或 `info` 发生变化后，都会自动传播给它的所有*直接*订阅方。直接订阅方无须手工刷新。

该消息不会沿级联拓扑转发。例如 A → B → C 中，只有直接订阅 A 的 B 收到变更。除非 C 也订阅 A，否则 C 的 `spock.node` 通常没有 A 的记录。

若本地已有该节点的行，但未应用变更消息，就会保留旧值。例如，包含该消息的事务通过 `skip_lsn` 跳过，或被异常处理丢弃。此时可在该节点运行 [`spock.node_refresh_info`](/zh/pgedge/spock/reference/functions/spock-node-refresh-info/) 手动追平。重新同步表不会重放这些消息，但 `spock.sub_resync_table()` 发现提供方记录与缓存不同时会给出警告。

仅当消息中的节点名在本地对应的 `node_id` 与发送节点一致时，才会应用传入的变更。若名称在本地未知（不会据此自动建行），或名称与发送方的 `node_id` 对不上本地记录，就跳过并记录 `WARNING`。此检查用于防范对端损坏或配置错误，正常运行时不应触发。

## 节点管理函数 {#node-management-functions}

使用以下 SQL 函数可动态添加和删除节点。

### spock.node_create {#spocknode_create}

使用 `spock.node_create` 创建复制节点。

`spock.node_create(node_name name, dsn text, location text DEFAULT NULL, country text DEFAULT NULL, info jsonb DEFAULT NULL)`

参数如下。

- `node_name` 为新节点名称，每个数据库只允许一个节点。
- `dsn` 为该节点的连接串。若节点将作为提供方，订阅方必须能通过它连接。
- `location`（可选）是节点物理位置的文本标签。
- `country`（可选）是节点所在国家或地区的文本标签。
- `info`（可选）是存放其他节点元数据的 JSON 对象。`tiebreaker` 键可覆盖默认的同分裁决值。有关各节点如何独立缓存该值，以及在整个集群修改它时的影响，见 conflict_types.md 的 Tiebreaker 一节。

### spock.node_drop {#spocknode_drop}

使用 `spock.node_drop` 删除复制节点。

`spock.node_drop(node_name name, ifexists bool)`

参数如下。

- `node_name` 为已有节点的名称。
- `ifexists` 决定节点不存在时如何处理。为 `true` 时不报错，默认 `false`。

### spock.node_add_interface {#spocknode_add_interface}

使用 `spock.node_add_interface` 为节点添加接口。

`spock.node_add_interface(node_name name, interface_name name, dsn text)`

创建节点时，`spock.node_create` 会使用指定的 `dsn` 创建与节点同名的默认接口。还可以为已有节点添加连接串不同的备用接口。

参数如下。

- `node_name` 为已有节点的名称。
- `interface_name` 为新接口名称。
- `dsn` 为新接口连接到节点时使用的连接串。

### spock.node_drop_interface {#spocknode_drop_interface}

使用 `spock.node_drop_interface` 删除节点上的一个已有接口。

`spock.node_drop_interface(node_name name, interface_name name)`

参数如下。

- `node_name` 为已有节点的名称。
- `interface_name` 为已有接口名称。

### spock.node_info {#spocknode_info}

使用 `spock.node_info` 获取本地 Spock 节点的信息。

`spock.node_info()`

该函数查询 Spock 系统目录，返回当前节点的标识符、名称、数据库信息及创建节点时设置的可选描述字段。

此函数仅读取数据。

返回一行，包含以下各列。

| 列 | 类型 | 说明 |
|--------|------|-------------|
| `node_id` | `oid` | 本地节点的对象标识符。 |
| `node_name` | `text` | 本地节点的名称。 |
| `sysid` | `text` | 该实例的 PostgreSQL 系统标识符。 |
| `dbname` | `text` | 当前数据库的名称。 |
| `replication_sets` | `text` | 与本节点关联的复制集名称，以逗号分隔。 |
| `location` | `text` | 可选的位置标签；创建时未设置则为 `NULL`。 |
| `country` | `text` | 可选的国家或地区标签；创建时未设置则为 `NULL`。 |
| `info` | `jsonb` | 可选的 JSON 元数据；创建时未设置则为 `NULL`。 |
{.wide .expand}

### spock.node_alter {#spocknode_alter}

使用 `spock.node_alter` 修改本节点自己的 `location`、`country` 或 `info`。`info` 按键合并。若补丁对象中包含 `tiebreaker`，其值必须是能由 32 位整数表示的 JSON 整数。

`spock.node_alter(p_location text DEFAULT NULL, p_country text DEFAULT NULL, p_info_patch jsonb DEFAULT NULL)`

`spock.node_refresh_info` 可针对对等节点，而此函数只修改本地节点，没有节点名参数。它最终执行与手写 `UPDATE` 相同的 `UPDATE spock.node`，因此传播机制也相同，见[自动传播节点元数据](#automatic-node-metadata-propagation)。完整说明和示例见 [spock_node_alter.md](/zh/pgedge/spock/reference/functions/spock-node-alter/)。

参数如下。

- `p_location`（可选）替换本节点的 `location`；省略则保留原值。
- `p_country`（可选）替换本节点的 `country`；省略则保留原值。
- `p_info_patch`（可选）合并到本节点已有的 `info` 中；省略则保留原值。补丁中的 `tiebreaker` 必须为可用 32 位整数表示的 JSON 数值，否则整次调用报错，任何内容都不会改变。

### spock.node_refresh_info {#spocknode_refresh_info}

使用 `spock.node_refresh_info` 刷新本地缓存中某个对等节点的 `location`、`country` 和 `info`，包括 `info` 中的 `tiebreaker` 键。

`spock.node_refresh_info(p_node_name name DEFAULT NULL)`

`spock.node` 是本地目录。在创建对等节点或首次创建其订阅时，才会首次填入该对端的记录。*直接*订阅方会自动接收之后的变更（见[自动传播节点元数据](#automatic-node-metadata-propagation)），但消息不会继续转发，如果承载消息的事务被跳过或丢弃，更新也就遗漏了。使用 `spock.node_refresh_info` 可按需追平，一次刷新全部已知对端，或只恢复某一对端的信息，无须等它再次变更。另见 [conflict_types.md](/zh/pgedge/spock/conflicts/) 的 Tiebreaker 一节。

参数如下。

- `p_node_name`（可选）指定待刷新的单个对等节点。省略时，尽力刷新除本地外的所有节点。若某一节点不可达、接口配置有误、DSN 指向其他节点或远端查询报错，只发出警告并继续处理其余节点。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/node_mgmt.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。
