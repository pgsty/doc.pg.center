---
title: 无冲突 Delta-Apply 列
description: 配置 Delta-Apply 列和 Spock 冲突处理选项，以处理复制中的插入与删除冲突。
weight: 80
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/conflicts.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 增量应用
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



如果一个节点订阅了多个提供者，或者在订阅者节点上发生本地写入，就可能出现冲突。在没有 Spock 的情况下，逻辑复制在解析累计和（例如年初至今余额）的值时也可能遇到问题。


> [!NOTE]
>
> 假设一个持续更新的银行账户累计值当前余额为 `$1,000`。两笔事务发生冲突，因为它们分别来自两个不同的多主节点并相互重叠。事务 A 从该账户取款 `$1,000`。事务 B 同样从该账户取款 `$1,000`。正确余额是 `$-1,000`。Delta-Apply 算法修复了这个问题；具有这种场景的高冲突工作负载（例如类 tpc-c 基准测试）现在能以极快速度正确运行。
>

过去，Postgres 用户依赖特殊数据类型和编号方案来帮助避免冲突。与其他方案不同，Spock 强大而简单的无冲突 Delta-Apply 列用以下逻辑管理数据更新冲突：

- 旧值被捕获到 WAL 文件中。
- 一个新值来自某笔事务。
- 在新值覆盖旧值之前，根据上述两步生成一个增量值；该增量会被正确应用。


> [!NOTE]
>
> 简化表示为：local_value + (new_value - old_value)
>

注意，在发生冲突的事务中，Delta-Apply 列也会被正确计算并应用。

要把一个列设为无冲突 Delta-Apply 列，确保复制到给定记录的值是已提交变更的增量（旧值加上或减去任何新值），需要对该列应用以下设置：`log_old_value=true,
delta_apply_function=spock.delta_apply`。例如：

```sql
ALTER TABLE pgbench_accounts ALTER COLUMN abalance
  SET (log_old_value=true, delta_apply_function=spock.delta_apply);
ALTER TABLE pgbench_branches ALTER COLUMN bbalance
  SET (log_old_value=true, delta_apply_function=spock.delta_apply);
ALTER TABLE pgbench_tellers ALTER COLUMN tbalance
  SET (log_old_value=true, delta_apply_function=spock.delta_apply);
```

作为一种特殊的安全阀特性，如果你需要重置 `log_old_value` 列，可以临时将该列改为 `log_old_value` 为 `false`。

## 冲突配置选项 {#conflict-configuration-options}

你可以通过在 `postgresql.conf` 文件中设置或通过 `ALTER SYSTEM SET` 设置的配置选项，来配置 Spock 扩展的一些行为：

- `spock.conflict_resolution = last_update_wins` 为本地数据与传入变更之间检测到的任何冲突设置解析方法为 `last_update_wins`；保留提交时间戳最新的数据版本；注意，`track_commit_timestamp` PostgreSQL 设置也必须 `enabled`。
- `spock.conflict_log_level` 设置报告检测到的冲突时使用的日志级别；默认值为 `LOG`；如果该参数设置为低于 `log_min_messages` 的值，已解析的冲突不会写入服务器日志；接受的值与 `log_min_messages` PostgreSQL 设置相同（参见[可能取值](https://www.postgresql.org/docs/15/runtime-config-logging.html#RUNTIME-CONFIG-SEVERITY-LEVELS)）；此设置主要用于抑制冲突日志。


## 处理 `INSERT-RowExists` 或 `INSERT/INSERT` 冲突 {#handling-insert-rowexists-or-insertinsert-conflicts}

如果 Spock 遇到由约束冲突（唯一约束、主键或复制标识）导致的冲突，Spock 可以自动把 `INSERT` 转换为 `UPDATE`，更新已存在行的所有列。

默认情况下，当 `INSERT` 语句的目标行已经存在时，Spock 会检测到冲突，并把该操作转换为 `UPDATE` 语句，将变更应用到已存在行的所有列。该事件会记录在 `spock.resolutions` 表中。

扩展的约束冲突行为由 `spock.check_all_uc_indexes` 参数控制。默认值为 `off`；设置为 `on` 时，Spock 会执行以下操作：

- 扫描所有有效唯一约束（以及主键和复制标识）。
- 按 OID 顺序扫描非空唯一约束（包括主键或复制标识索引）。
- 定位并解析 `INSERT` 语句期间遇到的冲突行。


> [!WARNING]
>
> 如果 `spock.check_all_uc_indexes` 为 `enabled`，Spock 只会使用“最后写入者胜出”逻辑解析第一个识别到的冲突。如果发生第二个冲突，会在 `spock.resolutions` 表中记录一个异常，结果为 `Keep-Local` 或 `Apply-Remote`。
>
> 此特性是实验性的；启用此特性的风险由你自己承担。
>
>

## 处理 `DELETE-RowMissing` 冲突 {#handling-delete-rowmissing-conflicts}

鉴于 DELETE 语句的目的本来就是删除该行，我们不会把这些情况记录为异常，因为删除该行的预期结果显然已经以某种方式达成。相反，`DELETE-RowMissing` 冲突会自动写入 `spock.resolutions` 表，因为预期结果已经达成。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/conflicts.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
