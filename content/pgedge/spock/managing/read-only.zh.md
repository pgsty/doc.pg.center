---
title: 在只读模式下使用 Spock
description: 配置 Spock 节点只读模式，并理解本地写入、复制和维护行为。
weight: 200
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/read_only.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



Spock 支持以只读模式运行节点。只读状态由名为 `spock.readonly` 的 GUC 参数管理，该参数可设置为三个值之一：

| 值 | 说明 |
|---------|-------------|
| `off` | 没有限制。所有用户都可以写入。这是默认值。 |
| `local` | 非超级用户的本地会话为只读。应用工作进程的复制写入仍被允许，因此入站复制会正常继续。超级用户仍可执行写操作。（为向后兼容，接受旧别名 `user`。） |
| `all` | 非超级用户的本地会话和应用工作进程都被阻止写入。超级用户仍可执行写操作。当你需要同时停止本地应用写入和入站复制时，使用此模式。 |
{.wide .expand}

该设置位于集群级别：要么所有数据库都是只读，要么所有数据库都是可读写（常规设置）。

只读模式通过为受影响会话设置 PostgreSQL 的 `transaction_read_only` 标志来强制执行。这意味着任何会修改数据的语句——包括 DML（`INSERT`、`UPDATE`、`DELETE`）、DDL、`TRUNCATE` 和 DCL（`GRANT`、`REVOKE`）——都会被 PostgreSQL 标准的只读事务检查拒绝。

这些数据库在 SQL 层处于只读模式：不过，checkpointer、background writer、walwriter 和 autovacuum launcher 仍在运行。这意味着数据库文件并非只读，而且在某些情况下数据库仍可能写入磁盘。

## 设置只读模式 {#setting-read-only-mode}

只有超级用户能修改 `spock.readonly` 参数。可以使用 `ALTER SYSTEM` 命令更改该值：

```sql
-- Block non-superuser local writes; inbound replication continues
ALTER SYSTEM SET spock.readonly = 'local';
SELECT pg_reload_conf();

-- Block all non-superuser writes including replication
ALTER SYSTEM SET spock.readonly = 'all';
SELECT pg_reload_conf();

-- Restore normal operation
ALTER SYSTEM SET spock.readonly = 'off';
SELECT pg_reload_conf();
```

只为当前会话设置模式：

```sql
SET spock.readonly TO local;
```

查询当前状态：

```sql
SHOW spock.readonly;
```

## 超级用户写入与出站复制 {#superuser-writes-and-outbound-replication}

在 `local` 和 `all` 两种模式下，超级用户都不受只读限制，可以执行写操作。**readonly 设置对 walsender（出站复制）没有影响。**无论只读模式如何，超级用户做出的任何写入都会被捕获到 WAL，并出站复制到集群中的其他节点。

要执行**不应**复制到其他节点的修复操作，请使用 [`spock.repair_mode()`](/pgedge/spock/reference/) 抑制 DML/DDL 语句的出站复制：

```sql
BEGIN;
SELECT spock.repair_mode(true);

-- Perform repair DML/DDL here...

SELECT spock.repair_mode(false);
COMMIT;
```

## `all` 模式的行为 {#behavior-of-all-mode}

在 `all` 模式下，应用工作进程会检测到该设置，并停止消费入站 WAL——在内部，每个工作进程会抛出 FATAL 并退出；清除只读状态后，manager 会重启它。当模式切换回 `off` 或 `local` 时，复制会从之前停止的位置恢复，**前提是上游复制槽仍保留必要的 WAL**。让节点长时间处于 `all` 模式之前，请为槽保留（`max_slot_wal_keep_size`、磁盘容量）做好规划；如果节点只读期间上游槽被回收，复制就无法从先前位置恢复，节点需要重新同步。

注意：
 - 只有超级用户能设置和取消设置 `spock.readonly` 参数。
 - 通过 GUC 参数，你可以通过标准 PostgreSQL 配置机制轻松管理节点的只读状态。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/managing/read_only.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
