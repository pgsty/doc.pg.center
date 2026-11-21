---
title: 复制集管理
description: 复制集控制数据库中哪些表参与复制，以及复制这些表上的哪些操作。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/repset_mgmt.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
type: docs
---

复制集用于控制数据库中哪些表参与复制，以及复制这些表上的哪些操作。使用以下命令创建和管理复制集。

| 命令 | 说明
|----------|-------------
| [spock.repset_create](/pgedge/spock/reference/functions/spock-repset-create/) | 创建复制集。
| [spock.repset_alter](/pgedge/spock/reference/functions/spock-repset-alter/) | 修改现有复制集。
| [spock.repset_drop](/pgedge/spock/reference/functions/spock-repset-drop/) | 删除复制集。
| [spock.repset_add_table](/pgedge/spock/reference/functions/spock-repset-add-table/) | 将表添加到复制集。
| [spock.repset_add_all_tables](/pgedge/spock/reference/functions/spock-repset-add-all-tables/) | 添加指定模式中的所有表。
| [spock.repset_remove_table](/pgedge/spock/reference/functions/spock-repset-remove-table/) | 从复制集中移除表。
| [spock.repset_add_seq](/pgedge/spock/reference/functions/spock-repset-add-seq/) | 将序列添加到复制集。
| [spock.repset_add_all_seqs](/pgedge/spock/reference/functions/spock-repset-add-all-seqs/) | 添加指定模式中的所有序列。
| [spock.repset_remove_seq](/pgedge/spock/reference/functions/spock-repset-remove-seq/) | 从复制集中移除序列。
| [spock.sub_add_repset](/pgedge/spock/reference/functions/spock-sub-add-repset/) | 为订阅者添加复制集。
| [spock.sub_remove_repset](/pgedge/spock/reference/functions/spock-sub-remove-repset/) | 从订阅者中移除复制集。

## 创建复制集 {#creating-a-replication-set}

要使用 Spock 创建复制集，请通过 psql 连接服务器，然后执行 `spock.repset_create` 命令：

```sql
SELECT spock.repset_create(replication_set_name, replicate_insert,
    replicate_update, replicate_delete, replicate_truncate)
```

参数包括：

- `replication_set_name` 是复制集的名称。

其余四个参数用于指定要复制的操作类型：

- `replicate_insert` 为 `true` 时复制 `INSERT` 语句；默认值为 `true`。
- `replicate_update` 为 `true` 时复制 `UPDATE` 语句；默认值为 `true`。
- `replicate_delete` 为 `true` 时复制 `DELETE` 语句；默认值为 `true`。
- `replicate_truncate` 为 `true` 时复制 `TRUNCATE` 语句；默认值为 `true`。

例如，以下命令：

```sql
SELECT spock.repset_create('accts', true, true, true, false);
```

添加名为 `accts` 的复制集，复制除 `TRUNCATE` 以外的所有上述语句。

## 将表添加到复制集 {#adding-a-table-to-a-replication-set}

要使用 Spock 将表添加到复制集，请通过 psql 连接服务器，然后调用 `spock.repset_add_table` 命令：

```sql
SELECT spock.repset_add_table(set_name name, relation regclass,
    synchronize_data boolean DEFAULT false, columns text[] DEFAULT NULL,
    row_filter text DEFAULT NULL, include_partitions boolean DEFAULT true)
```

参数包括：

- `set_name` 是现有复制集的名称。
- `relation` 是要添加的表的名称或 OID。
- `synchronize_data` 是布尔值，指示服务器在所有相关订阅者上同步表数据；默认值为 `false`。
- `columns` 指定要复制的列列表；默认值为 `NULL`（所有列）。
- `row_filter` 是行过滤表达式；默认值为 `NULL`（不过滤）。
- `include_partitions` 是布尔值；设为 `true` 可包含所有分区；默认值为 `true`。

例如，以下命令：

```sql
SELECT spock.repset_add_table('accts', 'payables');
```

将名为 `payables` 的表添加到名为 `accts` 的复制集。由于没有指定列，将复制所有列。

## 保留模式与扩展 {#reserved-schemas-and-extensions}

Spock 会对某些保留模式和扩展作特殊处理。它们列在 `spock.reserved_object` 系统目录中，该目录是以下三种行为的唯一依据：

- `exclude_from_dump`：订阅同步结构时，结构同步转储不包含此对象。如果订阅者上已存在这些对象，再恢复它们会失败。
- `block_in_repset`：此模式中或属于此扩展的表不得加入复制集。
- `replicate_ddl`：为 `false` 时，AutoDDL 将此对象的 DDL 限于本地节点执行；语句在发出它的节点运行，不会发送到其他节点。默认值为 `true`。

  对扩展而言，`CREATE EXTENSION`、`ALTER EXTENSION`、`DROP
  EXTENSION`、`COMMENT ON EXTENSION` 和 `SECURITY LABEL ON EXTENSION` 仅在本地执行，需要在每个节点上分别运行。启用 DDL 复制时，如果一条 `DROP EXTENSION` 同时指定本地扩展和参与复制的扩展，该语句会被拒绝；请分别删除。对于参与复制的扩展，如果它依赖本地扩展，`CREATE EXTENSION ... CASCADE` 也会被拒绝，即使所需扩展已全部安装。请先在每个节点上创建本地扩展，再执行不带 `CASCADE` 的 `CREATE EXTENSION`。`spock.replicate_ddl()` 会拒绝对本地扩展执行上述所有语句。对本地扩展执行的语句通过 `CASCADE` 产生的所有操作也仅限本地节点：依赖该扩展的对象仅在本地删除，`CREATE EXTENSION
  ... CASCADE` 安装的扩展也仅在本地安装。

  如果语句未直接指定本地扩展，却将其移除，则不会被拦截：例如对其依赖的扩展执行 `DROP EXTENSION ... CASCADE`，对它所在的模式执行 `DROP
  SCHEMA ... CASCADE`，或对其所有者执行 `DROP OWNED BY`。这类语句会被复制，每个对端随后都必须在应用工作进程中删除该本地扩展。请先在每个节点上删除本地扩展。

  对模式而言，只有 Spock 能识别目标模式的 DDL 才会留在本地：`CREATE`
  `SCHEMA`/`TABLE`/`TABLE AS`/`SEQUENCE`/`VIEW`/`INDEX`、`ALTER TABLE`，以及对这些对象类型执行的 `DROP`。针对该模式的其他 DDL（如 `GRANT`、`COMMENT`、`TRUNCATE` 或 `ALTER ... SET SCHEMA`）不作此分类，仍照常复制。只有当一条 `DROP` 指定的*所有*对象均为本地对象时，它才会留在本地。不要在一条 `DROP` 中混用本地对象和参与复制的对象，因为发出的命令无法被改写为只删除参与复制的对象。

Spock 预置以下内置条目，它们不能移除或修改：

| 对象 | exclude_from_dump | block_in_repset | replicate_ddl
|-------------------|-------------------|-----------------|---------------
| `spock` | 是 | 是 | 是
| `snowflake` | 是 | 是 | 是
| `lolor` | 是 | 否 | 是
| `coldfront` | 是 | 否 | 是
| `pgedge_ace`（仅模式） | 是 | 是 | 否

`spock`、`snowflake`、`lolor` 和 `coldfront` 各有一条 `schema` 记录和一条 `extension` 记录。上表的 `replicate_ddl` 列表示 `schema` 记录中的值。`extension` 记录的 `replicate_ddl = true`（参与复制），只有 `lolor` 例外，其扩展记录为 `false`：lolor 拒绝由应用工作进程创建或删除，因此 `CREATE`、`ALTER` 和 `DROP EXTENSION
lolor` 要在每个节点分别运行，而不通过复制执行。`exclude_from_dump`/`block_in_repset` 同时适用于两种记录。

`lolor` 被排除在转储之外，但有意允许其加入复制集：它的表必须复制，才能使大对象在每个节点执行 `DROP EXTENSION` 后都得以保留，而非仅在发出删除语句的节点保留。

`coldfront` 是 pgEdge 的分层存储扩展。每个节点通过自身的 `CREATE EXTENSION coldfront` 创建其对象，因此结构同步会跳过它们。其表仍可加入复制集，因为 Coldfront 会自行将其中若干表添加到 `default` 集合，包括 bakery 认领表和分层视图注册表，以协调网状集群中的写入。分层视图背后的冷数据位于 PostgreSQL 外部的共享 Iceberg 存储中，不由 Spock 复制。

`pgedge_ace` 是 pgEdge ACE 工具使用的模式。它保存节点本地的配置和状态，而非应用数据：对上述可分类语句，其 DDL 保留在本地（`replicate_ddl=no`），其表也始终不能加入复制集（`block_in_repset=yes`）。因此，`CREATE SCHEMA pgedge_ace` 及其下的表只保留在发出这些语句的节点上。

要额外保留自己的模式或扩展，请使用 `spock.reserved_object_add`：

```sql
-- keep a custom schema out of structure sync and out of replication sets
SELECT spock.reserved_object_add('ace', 'schema');

-- exclude an extension from the dump but still allow its tables in repsets
SELECT spock.reserved_object_add('myext', 'extension', p_block_in_repset := false);

-- keep a custom schema node-local: AutoDDL will not replicate its DDL
SELECT spock.reserved_object_add('myschema', 'schema', p_replicate_ddl := false);
```

使用 `spock.reserved_object_remove('ace', 'schema')` 删除自己添加的条目。保留对象属于节点本地配置：请在集群的每个节点上作相同添加。运维人员添加的记录会经 `pg_dump`/`pg_restore` 保留；内置记录始终会重新预置。

## 从复制集中移除表 {#removing-a-table-from-a-replication-set}

要使用 Spock 从复制集中移除表，请通过 psql 连接服务器，然后调用 `spock.repset_remove_table` 命令：

```sql
SELECT spock.repset_remove_table(set_name name, relation regclass,
    include_partitions boolean DEFAULT true)
```

参数包括：

- `set_name` 是表所在的复制集名称。
- `relation` 是要移除的表的名称或 OID。
- `include_partitions` 是布尔值；设为 `true` 可同时移除分区表的各分区；默认值为 `true`。

例如，以下命令：

```sql
SELECT spock.repset_remove_table('accts', 'payables');
```

从名为 `accts` 的复制集中移除名为 `payables` 的表。

## 复制集管理函数 {#replication-set-management-functions}

以下函数用于管理复制集：

### spock.repset_create {#spockrepset_create}

使用 `spock.repset_create` 创建复制集。

`spock.repset_create(set_name name, replicate_insert bool,
replicate_update bool, replicate_delete bool, replicate_truncate bool)`

参数：

- `set_name` 是复制集的唯一名称。
- `replicate_insert` 为 `true` 时复制 `INSERT` 语句；默认值为 `true`。
- `replicate_update` 为 `true` 时复制 `UPDATE` 语句；默认值为 `true`。
- `replicate_delete` 为 `true` 时复制 `DELETE` 语句；默认值为 `true`。
- `replicate_truncate` 为 `true` 时复制 `TRUNCATE` 语句；默认值为 `true`。

### spock.repset_alter {#spockrepset_alter}

使用 `spock.repset_alter` 修改现有复制集的参数。

`spock.repset_alter(set_name name, replicate_insert bool DEFAULT NULL,
replicate_update bool DEFAULT NULL, replicate_delete bool DEFAULT NULL,
replicate_truncate bool DEFAULT NULL)`

参数：

- `set_name` 是此函数要修改的现有复制集的名称。
- `replicate_insert` 为 `true` 时复制 `INSERT` 语句。传入 `NULL`（默认值）保持当前值不变。
- `replicate_update` 为 `true` 时复制 `UPDATE` 语句。传入 `NULL`（默认值）保持当前值不变。
- `replicate_delete` 为 `true` 时复制 `DELETE` 语句。传入 `NULL`（默认值）保持当前值不变。
- `replicate_truncate` 为 `true` 时复制 `TRUNCATE` 语句。传入 `NULL`（默认值）保持当前值不变。

### spock.repset_drop {#spockrepset_drop}

使用 `spock.repset_drop` 删除指定复制集。

`spock.repset_drop(set_name name, ifexists boolean DEFAULT false)`

参数：

- `set_name` 是现有复制集的名称。
- `ifexists` 控制删除不存在的复制集时是否报错。为 `true` 时，复制集不存在也不报错；默认值为 `false`。

### spock.repset_add_table {#spockrepset_add_table}

使用 `spock.repset_add_table` 将表添加到复制集。

`spock.repset_add_table(set_name name, relation regclass,
synchronize_data boolean DEFAULT false, columns text[] DEFAULT NULL,
row_filter text DEFAULT NULL, include_partitions boolean DEFAULT true)`

参数：

- `set_name` 是现有复制集的名称。
- `relation` 是要添加到复制集的表的名称或 OID。
- `synchronize_data` 为 `true` 时，在订阅了指定复制集的所有订阅者上同步表数据；默认值为 `false`。
- `columns` 是要复制的列列表。通常需要复制所有列，此时设为 `NULL`（默认值）。
- `row_filter` 是行过滤表达式；默认值为 `NULL`（不过滤）。
- `include_partitions` 为 `true` 时，同时添加分区表的各分区；默认值为 `true`。

> [!WARNING]
> 使用有效行过滤器同步数据时需要谨慎。对一张表而言，将 `synchronize_data=true` 与有效的 `row_filter` 一同使用，通常是一次性操作。修改 `row_filter` 后再次执行，不会将数据同步到订阅者。可能需要调用 `spock.sub_resync_table()` 解决。
>

### spock.repset_add_all_tables {#spockrepset_add_all_tables}

使用 `spock.repset_add_all_tables` 将指定模式中的所有表添加到复制集。

`spock.repset_add_all_tables(set_name name, schema_names text[],
synchronize_data boolean DEFAULT false)`

仅添加现有表；以后创建的表不会自动加入。

参数：

- `set_name` 是现有复制集的名称。
- `schema_names` 是现有模式名称的数组，将从这些模式中添加表。
- `synchronize_data` 为 `true` 时，指示 Spock 在订阅了指定复制集的所有节点上同步表数据；默认值为 `false`。

### spock.repset_remove_table {#spockrepset_remove_table}

使用 `spock.repset_remove_table` 从复制集中移除表。

`spock.repset_remove_table(set_name name, relation regclass,
include_partitions boolean DEFAULT true)`

参数：

- `set_name` 是现有复制集的名称。
- `relation` 是要从复制集中移除的表的名称或 OID。
- `include_partitions` 为 `true` 时，同时移除分区表的各分区；默认值为 `true`。

### spock.repset_add_seq {#spockrepset_add_seq}

使用 `spock.repset_add_seq` 将序列添加到复制集。

`spock.repset_add_seq(set_name name, relation regclass,
synchronize_data boolean DEFAULT false)`

参数：

- `set_name` 是现有复制集的名称。
- `relation` 是要添加到复制集的序列的名称或 OID。
- `synchronize_data` 为 `true` 时，指示 Spock 在订阅了指定复制集的所有节点上同步序列；默认值为 `false`。

### spock.repset_add_all_seqs {#spockrepset_add_all_seqs}

使用 `spock.repset_add_all_seqs` 添加指定模式中的所有序列。

`spock.repset_add_all_seqs(set_name name, schema_names text[],
synchronize_data boolean DEFAULT false)`

仅添加现有序列；以后创建的序列不会自动加入。

参数：

- `set_name` 是现有复制集的名称。
- `schema_names` 是现有模式名称的数组，将从这些模式中添加序列。
- `synchronize_data` 设为 `true` 可立即同步序列值；默认值为 `false`。

### spock.repset_remove_seq {#spockrepset_remove_seq}

使用 `spock.repset_remove_seq` 从复制集中移除序列。

`spock.repset_remove_seq(set_name name, relation regclass)`

参数：

- `set_name` 是现有复制集的名称。
- `relation` 是要从复制集中移除的序列的名称或 OID。

可以查询 `spock.tables` 视图，了解各表属于哪些复制集。

### spock.sub_add_repset {#spocksub_add_repset}

使用 `spock.sub_add_repset` 为订阅者添加复制集。

`spock.sub_add_repset(subscription_name name, replication_set name)`

此函数不执行复制同步，只启用事件接收。

参数：

- `subscription_name` 是现有订阅的名称。
- `replication_set` 是要添加的复制集名称。

### spock.sub_remove_repset {#spocksub_remove_repset}

使用 `spock.sub_remove_repset` 从订阅者中移除复制集。

`spock.sub_remove_repset(subscription_name name, replication_set name)`

参数：

- `subscription_name` 是现有订阅的名称。
- `replication_set` 是要移除的复制集名称。

### spock.reserved_object_add {#spockreserved_object_add}

使用 `spock.reserved_object_add` 保留一个模式或扩展（参见[保留模式与扩展](#reserved-schemas-and-extensions)）。如果对象已被保留，则更新其标志。内置对象不能修改。

`spock.reserved_object_add(p_name name, p_kind text, p_exclude_from_dump bool
DEFAULT true, p_block_in_repset bool DEFAULT true, p_replicate_ddl bool
DEFAULT true)`

参数：

- `p_name` 是模式或扩展的名称。
- `p_kind` 为 `'schema'` 或 `'extension'`。
- `p_exclude_from_dump` 将对象排除在结构同步转储之外；默认值为 `true`。
- `p_block_in_repset` 阻止对象加入复制集；默认值为 `true`。
- `p_replicate_ddl`：传入 `false` 将对象限于本地节点，使 AutoDDL 不向其他节点发送其 DDL（如 `pgedge_ace` 和 `lolor` 扩展）。默认值为 `true`，显式传入 `NULL` 也视为 `true`。

### spock.reserved_object_remove {#spockreserved_object_remove}

使用 `spock.reserved_object_remove` 移除自己添加的保留对象。内置对象受保护，不能移除。

`spock.reserved_object_remove(p_name name, p_kind text)`

参数：

- `p_name` 是模式或扩展的名称。
- `p_kind` 为 `'schema'` 或 `'extension'`。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/spock_functions/repset_mgmt.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/pgedge/about/license/)。
