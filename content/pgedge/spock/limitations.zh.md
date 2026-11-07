---
title: 限制与约束
description: 汇总 Spock 在复制标识、序列、触发器、版本兼容、过滤器和 DDL 方面的限制。
weight: 110
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/limitations.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 使用限制
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



Spock 有若干限制和约束；用户在设计并实现复制场景时应了解它们。

## 需要超级用户权限 {#superuser-privileges-are-required}

目前，配置复制和管理需要超级用户权限才能使用 Spock 扩展。

## `UNLOGGED` 和 `TEMPORARY` 表不会被复制 {#unlogged-and-temporary-tables-are-not-replicated}

`UNLOGGED` 和 `TEMPORARY` 表不会被复制，也不能被复制，这与物理流复制类似。

## 一次一个数据库 {#one-database-at-a-time}

要复制多个数据库，必须为每个数据库分别建立提供者或订阅者关系。无法一次性为 PostgreSQL 安装中的所有数据库配置复制。

## 需要 PRIMARY KEY 或 REPLICA IDENTITY {#primary-key-or-replica-identity-required}

对于缺少 `PRIMARY
KEY` 或其他有效复制标识（例如使用索引）的表，`UPDATE` 和 `DELETE` 无法复制；该索引必须唯一、不是部分索引、不可延迟，并且只包含标记为 NOT NULL 的列。由于没有唯一标识符，复制无法找到应当更新或删除的元组。

对于 UPDATE 或 DELETE 操作，不支持把 `REPLICA IDENTITY FULL` 作为独立的复制标识。不过，在具有主键的表上与 Delta-Apply 列配合使用时，支持该设置。对于没有主键或 Delta-Apply 配置的表，UPDATE 和 DELETE 操作需要 PRIMARY KEY 或显式 REPLICA IDENTITY USING INDEX。

## 只能有唯一索引、唯一约束或 PK 中的一个 {#only-one-unique-index-or-constraint-or-pk}

如果配置了多个上游，或者下游接受本地写入，下游被复制表上只应存在一个 `UNIQUE` 索引。冲突解析一次只能使用一个索引；因此，如果某行满足 `PRIMARY KEY` 但违反下游侧的 `UNIQUE` 约束，冲突行可能产生 `ERROR`。

如果下游消费者只从某个上游接收写入，而不从任何其他来源接收写入，上游可以拥有额外的唯一约束。规则是，下游约束不得比上游约束更严格。

允许使用部分二级唯一索引，但冲突解析会忽略它们。

`spock.check_all_uc_indexes` 是一个实验性 [GUC](/zh/pgedge/spock/configuration/)，允许 Spock 考虑所有唯一约束，而不仅仅是主键或复制标识，从而增加 `INSERT` 冲突解析能力。

## 唯一约束不能是可延迟的 {#unique-constraints-must-not-be-deferrable}

在 INSERT 冲突解析期间，可延迟的唯一约束和主键会被静默跳过。这意味着，如果表上唯一的唯一约束是可延迟的，就不会检测到 INSERT 冲突，可能导致订阅者节点上出现重复行。

在下游端，spock 还可能发出以下错误：

```sql
ERROR: spock doesn't support index rechecks needed for deferrable indexes
DETAIL: relation "public"."test_relation" has deferrable indexes: "index1",
"index2"
```

建议：确保所有表至少有一个不可延迟的唯一约束（最好是主键），以便可靠检测冲突。

## 不支持复制队列冲刷 {#no-replication-queue-flush}

不支持在主节点上冻结事务，并等待所有仍在队列中的事务从槽中重放完成。

这意味着应用表结构变更时必须小心。如果存在尚未复制的事务，而提供者和订阅者的表结构同时以某种方式变更，使订阅者表与队列中的事务不再兼容，复制将停止。

管理员应确保在进行模式变更之前停止对提供者的写入，或者使用 `spock.replicate_ddl` 函数把模式变更排入队列，使其在订阅者上的一个一致点重放。

在多主配置中，仅使用 `spock.replicate_ddl` 并不够。提供者提交模式变更之后，订阅者可能仍会以旧结构生成新事务。用户必须确保在进行模式变更之前，所有节点都停止写入，并且所有槽都已追上。

## FOREIGN KEYS {#foreign-keys}

复制过程不强制执行外键约束——即使会违反 `FOREIGN KEY`，提供者侧成功的内容仍会被应用到订阅者。

## TRUNCATE {#truncate}

使用 `TRUNCATE ... CASCADE` 时，`CASCADE` 选项只会在提供者侧应用。

（要正确处理这一点，PostgreSQL 中的外键可能需要增加 `ON TRUNCATE CASCADE` 支持。）

`TRUNCATE ... RESTART IDENTITY` 会被复制。序列重启会应用到订阅者节点。注意，如果序列没有通过 pgEdge Snowflake 管理，这可能导致序列值发散。

## 序列 {#sequences}

我们强烈建议使用 pgEdge [Snowflake
Sequences](https://github.com/pgEdge/snowflake)，而不是使用下述旧式序列。

添加到复制集的序列状态会周期性复制，而不是实时复制。被复制的值使用动态缓冲区，使订阅者实际收到序列的未来状态。这能最大限度降低订阅者对序列 `last_value` 的认识落后于提供者的机会，但不能完全消除这种可能性。

在数据库发生大事件（例如数据装载）之后，或在线升级期间，可能需要调用 `sync_sequence`，确保所有订阅者都有给定序列的最新信息。

在多节点系统上，通常建议序列使用 `bigserial` 和 `bigint` 类型，因为更小的序列可能很快到达序列空间末尾。

希望在提供者和订阅者上拥有独立序列的用户，可以避免把序列加入复制集，并创建步长大于或等于节点数的序列，然后为每个节点设置不同偏移量。对 `CREATE
SEQUENCE` 或 `ALTER SEQUENCE` 使用 `INCREMENT BY` 选项，并使用 `setval(...)` 设置起点。

## 触发器 {#triggers}

应用进程和初始 COPY 进程都在 `session_replication_role` 设置为 `replica` 的状态下运行，这意味着 `ENABLE REPLICA` 和 `ENABLE ALWAYS` 触发器会被触发。

## PostgreSQL 版本差异 {#postgresql-version-differences}

Spock 可以跨 PostgreSQL 主版本复制。尽管如此，长期跨版本复制不被视为设计目标，虽然它往往可以工作。跨版本复制时，更容易出现变更在提供者上有效、在订阅者上无效的问题。

从旧版本复制到新版本更安全，因为 PostgreSQL 保持稳固的向后兼容性，但只有有限的前向兼容性。只有在相同 PostgreSQL 版本之间复制，或从较低版本复制到较高版本时，才支持初始模式同步。

在不同次要版本之间复制完全没有区别。

## 数据库编码差异 {#database-encoding-differences}

Spock 不支持在不同编码的数据库之间复制。集群中所有节点的编码必须匹配。虽然 `UTF-8` 常用于并推荐用于国际字符支持，但只要在所有节点上保持一致，任何编码都可以接受。

## 大对象 {#large-objects}

PostgreSQL 的逻辑解码设施不支持解码[大对象](https://www.postgresql.org/docs/current/largeobjects.html)的变更；我们建议使用 [LOLOR 扩展](https://github.com/pgEdge/lolor)管理大对象。

注意，DDL 限制仍然适用，因此使用 `replicate_ddl_command()` 时需要格外小心。

## Delta-Apply 列要求 {#delta-apply-column-requirements}

配置为 Delta-Apply 冲突解析的列必须有 `NOT NULL` 约束。如果在应用增量期间遇到 NULL 值，应用工作进程会报错：

```text
ERROR: delta apply column can't operate NULL values
```

启用此特性之前，确保所有 Delta-Apply 列都定义为 `NOT NULL`。

## 混合使用 Spock 与原生逻辑复制 {#mixed-spock-and-native-logical-replication}

Spock 使用自己的 16 位 node_id（由节点名哈希派生）在提交时间戳中跟踪事务复制源，而不是 PostgreSQL 的 RepOriginId。两个 ID 空间重叠（0-65535）；如果 Spock 与 PostgreSQL 原生逻辑复制在同一个数据库中运行，这可能造成歧义。

建议：避免在同一个数据库中同时运行 Spock 和原生逻辑复制订阅。

## 行过滤器与列过滤器 {#row-and-column-filters}

行过滤器和列过滤器有以下限制。

### 不能过滤系统列 {#system-columns-cannot-be-filtered}

系统列（例如 `oid` 或 `xmin`）不能用于行过滤器或列过滤器。列过滤器和行过滤器在带 OID 的表上能正确工作，但系统列本身不能被过滤。

### 行过滤器表达式约束 {#row-filter-expression-constraints}

行过滤器是普通 PostgreSQL 表达式，具有与 CHECK 约束相同的限制。

易变函数（如 `random()` 或 `now()`）可以用于行过滤器，但它们在求值时可能产生不同结果，并导致停止复制的错误。请谨慎使用易变函数。

### 行过滤器会话上下文 {#row-filter-session-context}

行过滤器在复制会话上下文中运行，而不是在原始会话上下文中运行。这意味着特定于会话的表达式（如 `CURRENT_USER`）会使用复制会话的值，而不是原始会话的值。

### 列过滤器行为 {#column-filter-behavior}

使用列过滤器时，请注意以下行为：

- 删除被过滤的列会自动将其从过滤器中移除。
- 新列不会自动加入现有过滤器。
- 必须手动更新列过滤器以包含新列。

## 分区表 {#partitioned-tables}

分区表有特定的复制限制。

### 新分区不会自动复制 {#new-partitions-not-automatically-replicated}

初始同步之后添加的分区，必须使用 `spock.repset_add_partition()` 函数手动添加。

父表会在初始同步期间同步，但各个分区不会直接同步。同步之后创建的新分区需要显式加入复制集。

### 分离的分区不会自动移除 {#detached-partitions-not-automatically-removed}

分离分区不会自动将其从复制中移除。你必须使用 `spock.repset_remove_partition()` 更新集群元数据，并从复制集中移除该分区。

## DDL 复制限制 {#ddl-replication-limitations}

某些 DDL 语句是有意不复制的。

### 不复制的 DDL 语句 {#ddl-statements-not-replicated}

以下类型的 DDL 语句不会被复制：

- `CREATE DATABASE`——不复制数据库创建。
- `CREATE TABLE...AS...`——该语句会被复制，但可能不安全，因为表会在加入复制集之前被复制。

在有三个或更多节点的多节点集群中，某些 DDL 语句（例如 `DROP TABLE`）可能导致复制问题。

### DDL 复制最佳实践 {#ddl-replication-best-practices}

为获得最佳结果，只有当所有节点上的模式完全匹配时才启用自动 DDL 复制。也就是说，要么所有数据库都没有对象，要么所有数据库拥有完全相同的对象，并且所有表都在复制集中。

## Spock 模式 {#spock-schema}

`spock` 模式由 Spock 内部管理，并有以下限制。

### 禁止直接修改 {#direct-modification-prohibited}

不要直接删除、创建或修改 `spock` 模式中的文件。使用 Spock 函数和过程管理复制。直接修改模式可能损坏复制元数据，并导致复制失败。

## 只读模式 {#read-only-mode}

只读模式有以下限制。

### 仅在 SQL 层只读 {#read-only-at-sql-level-only}

`spock.readonly` 参数在 SQL 层对非超级用户实施只读限制。但是，后台进程（checkpointer、background writer、WAL writer 和 autovacuum）仍会继续运行，并可能写入磁盘。

这意味着数据库文件并非真正只读；即使启用只读模式，仍可能发生某些磁盘写入。

## 跳过复制位置 {#replication-position-skipping}

使用 `spock.sub_alter_skiplsn()` 跳过复制位置有以下关键限制。

### 跳过的数据不会重放或修复 {#skipped-data-not-replayed-or-repaired}

`spock.sub_alter_skiplsn()` 操作不会重放或修复被跳过的数据。订阅者会永久忽略旧 LSN 与指定 LSN 之间的任何变更。

只有在理解数据影响并接受跳过的变更会在订阅者节点上丢失时，才使用此函数。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/limitations.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
