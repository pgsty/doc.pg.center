---
title: 自动 DDL 复制
description: 配置 Spock 的自动 DDL 复制、DDL 拦截和相关日志消息。
weight: 200
upstream_source: pgedge-spock-20261121
upstream_link: https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/spock_autoddl.md
upstream_modified: true
upstream_ref: d05e2e2b6a82
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



spock 扩展可以自动复制 DDL 语句。要启用自动 DDL 复制，请把以下参数设置为 `on`：

* `spock.enable_ddl_replication` 通过 default 复制集启用 DDL 语句复制。某些 DDL 语句是有意不复制的（例如 `CREATE DATABASE`）。其他 DDL 语句会被复制，但可能导致复制问题（例如 `CREATE TABLE... AS...` 语句）。对于 `CREATE TABLE... AS...`，DDL 语句会在表加入复制集之前复制，可能导致潜在的数据不规则。还有一些 DDL 语句会被复制，但在 3 个及以上节点的集群中可能产生问题（即 `DROP TABLE`）。

* `spock.include_ddl_repset` 让 spock 在每个节点上创建表时，自动把表加入复制集。带主键的表会加入 `default` 复制集，不带主键的表会加入 `default_insert_only` 复制集。修改表以添加或删除主键，也会修改该表所属的复制集。把表设置为 `unlogged` 会把该表从复制中移除。分离分区不会把表从复制中移除。

* `spock.allow_ddl_from_functions` 让 spock 自动复制函数内部调用的 DDL 语句。如果预期每个函数都会在每个节点上执行，请把 `spock.allow_ddl_from_functions` 设置为 `off`。设置为 `off` 时，从函数复制的语句遵循为 `include_ddl_repset` 描述的相同规则。如果表具有主键，它会被加入 `default` 复制集；否则会被加入 `default_insert_only` 复制集。

若要在整个集群的维护期间禁止 DDL（包括可自动复制的 DDL），请在每个节点上设置以下参数。

* `spock.deny_all_ddl`——布尔值，默认为 `false`。设置为 `true` 时，Spock 会拒绝在该节点上执行的任何 DDL 语句。这在敏感维护窗口期间，或在添加、修复节点时，可用作保护措施。超级用户可以在运行时更改此设置（`PGC_SUSET`）；不需要重新加载服务器。

最好只在所有节点上的数据库模式完全匹配时才把这些参数设置为 `on`——要么所有数据库都没有对象，要么所有数据库拥有完全相同的对象，并且所有表都已加入复制集。


> [!NOTE]
>
> 也可以调用 `spock.replicate_ddl()` 显式执行并复制指定的 DDL。函数会检查传入语句的类型，识别为 DDL 后才执行并复制。
>

在自动复制过程中，spock 会生成提供执行信息的消息。以下是每条消息的描述：

- `DDL statement replicated.`

  此消息是 INFO 级别消息。每当 DDL 语句成功复制时都会显示。要让这些消息出现在服务器日志文件中，配置必须设置 `log_min_messages=INFO`。

- `DDL statement replicated, but could be unsafe.`

  此消息用作警告。当某些 DDL 语句虽然成功复制，但被认为可能不安全时，会生成此消息。例如，`CREATE TABLE... AS...` 这样的语句会触发此警告。

- `This DDL statement will not be replicated.`

  当自动复制处于活动状态，但特定 DDL 不受支持或被有意排除在复制之外时，会生成此警告消息。

- `table 'test' was added to default replication set.`

  这是一条 LOG 消息，在设置 `spock.include_ddl_repset` 时提供给定表所用复制集的信息。

---

[上游原文](https://github.com/pgEdge/spock/blob/d05e2e2b6a82796d86e3c16ffb0d3fc38b1b329c/docs/managing/spock_autoddl.md) · `d05e2e2b6a82` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
