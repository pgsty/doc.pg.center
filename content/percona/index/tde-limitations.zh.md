---
title: pg_tde 的限制
linkTitle: 已知限制
description: pg_tde 的加密范围限制、扩展兼容性、恢复要求，以及支持和不支持的 WAL 工具。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/tde-limitations.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 200
upstream_source: percona
---

## Percona Server for PostgreSQL 的已知不兼容项 {#known-incompatibilities-in-percona-server-for-postgresql}

`pg_tde` 所需的内部改动可能导致某些 PostgreSQL 扩展无法在 Percona Server for PostgreSQL 上运行。

即使没有安装或启用 `pg_tde`，这些不兼容问题也可能出现。

### 分布式系统和基于扩展的系统 {#distributed-and-extension-based-systems}

> [!WARNING] 不支持 Citus 和 TimescaleDB
> Percona Server for PostgreSQL 与 Citus 等分布式 PostgreSQL 扩展以及 TimescaleDB 等时序扩展不兼容。
>
> 这一限制源于与 `pg_tde` 有关的 PostgreSQL 内部改动，与是否启用扩展无关。

## 使用 pg_tde 时的限制 {#limitations-when-using-pgtde}

`pg_tde` 2.2.2 的限制：

* PostgreSQL 内部系统表（包括统计信息和元数据）不加密。
* 查询超过 `work_mem` 时创建的临时文件不加密。这些文件可能在长时间运行的查询期间或服务器崩溃后保留，从而使敏感数据以明文形式暴露在磁盘上。

## shared_preload_libraries 未加载 pg_tde 时的恢复 {#recovery-without-pgtde-in-sharedpreloadlibraries}

> [!DANGER] 未加载 pg_tde 就恢复加密集群，存在数据损坏风险
> 恢复包含加密表的 PostgreSQL 集群时，必须通过 `shared_preload_libraries` 配置参数加载 `pg_tde` 扩展。

## ALTER DATABASE ... SET TABLESPACE {#alter-database-set-tablespace}

> [!WARNING] pg_tde 对更改数据库表空间的支持有限
> `ALTER DATABASE ... SET TABLESPACE` 会绕过 PostgreSQL 存储管理器（SMGR），而 `pg_tde` 依赖 SMGR 实施加密。
>
> - 如果数据库的默认表空间中存在加密对象，该操作会被拒绝。
> - 如果默认表空间中没有加密对象，则允许操作。
>
> 只检查默认表空间中的对象。`pg_tde` 不会检查其他表空间中的对象。
>
> 要逐个移动加密表，请使用 `ALTER TABLE ... SET TABLESPACE`。该命令经过 SMGR，与 `pg_tde` 兼容。

## 当前不支持的 WAL 工具 {#currently-unsupported-wal-tools}

以下工具目前不支持 `pg_tde` WAL 加密：

* `pg_createsubscriber`
* `pg_receivewal`
* `Barman`
* `pg_verifybackup` 默认会因校验和或 WAL 密钥大小不匹配而失败。可以使用 `-s`（跳过校验和）和 `-n`（`--no-parse-wal`）选项验证备份，作为临时解决办法。
* 未配置 `pg_tde_archive_decrypt` 和 `pg_tde_restore_encrypt`，或启用了 `archive-async`、`archive-header-check`、`checksum-page` 的 pgBackRest。

## 支持的 WAL 工具 {#supported-wal-tools}

Percona 已测试并确认以下工具可用于 `pg_tde` WAL 加密：

* Patroni，配置示例见下方 [Patroni 配置文件](#example-patroni-configuration)。
* `pg_tde_basebackup`（使用 `--wal-method=stream` 或 `--wal-method=none`），详见[启用 WAL 加密时的备份](/zh/percona/how-to/backup-wal-enabled/)。
* `pg_tde_resetwal`
* `pg_tde_rewind`
* `pg_tde_upgrade`
* `pg_tde_waldump`
* 配置了 `pg_tde_archive_decrypt` 和 `pg_tde_restore_encrypt`，并关闭 `archive-async`、`archive-header-check`、`checksum-page` 的 pgBackRest。

## Patroni 配置示例 {#example-patroni-configuration}

以下配置示例经过 Percona 测试。

> [!DETAILS] 展开经过 Percona 测试的 Patroni 配置
> ```yaml
> # Example Patroni configuration file maintained by Percona
> # Source: https://github.com/jobinau/pgscripts/blob/main/patroni/patroni.yml
> scope: tde
> name: pg1
> restapi:
>   listen: 0.0.0.0:8008
>   connect_address: pg1:8008
> etcd3:
>   host: etcd1:2379
> bootstrap:
>   dcs:
>     ttl: 30
>     loop_wait: 10
>     retry_timeout: 10
>     maximum_lag_on_failover: 1048576
>     postgresql:
>       use_pg_rewind: true
>       use_slots: true
>       parameters:
>         archive_command: "/lib/postgresql/17/bin/pg_tde_archive_decrypt %f %p \"pgbackrest --stanza=tde archive-push %%p\""
>         archive_timeout: 600s
>         archive_mode: "on"
>         logging_collector: "on"
>         restore_command: "/lib/postgresql/17/bin/pg_tde_restore_encrypt %f %p \"pgbackrest --stanza=tde archive-get %%f \\\"%%p\\\"\""
>       pg_hba:
>         - local all all peer
>         - host all all 0.0.0.0/0 scram-sha-256
>         - host all all ::/0 scram-sha-256
>         - local replication all peer
>         - host replication all 0.0.0.0/0 scram-sha-256
>         - host replication all ::/0 scram-sha-256
>   initdb:
>     - encoding: UTF8
>     - data-checksums
>     - set: shared_preload_libraries=pg_tde
>   post_init: /usr/local/bin/setup_cluster.sh
> postgresql:
>   listen: 0.0.0.0:5432
>   connect_address: pg1:5432
>   data_dir: /var/lib/postgresql/patroni-17
>   bin_dir: /lib/postgresql/17/bin
>   bin_name:
>     pg_basebackup: pg_tde_basebackup
>     pg_rewind: pg_tde_rewind
>   pgpass: /var/lib/postgresql/patronipass
>   authentication:
>     replication:
>       username: replicator
>       password: rep-pass
>     superuser:
>       username: postgres
>       password: secretpassword
>   parameters:
>     unix_socket_directories: /tmp
>     # Use unix_socket_directories: /var/run/postgresql for Debian/Ubuntu distributions
> watchdog:
>   mode: off
> tags:
>   nofailover: false
>   noloadbalance: false
>   clonefrom: false
>   nosync: false
> ```

> [!WARNING]
> 上述示例经过 Percona 测试，但不同 Patroni 版本有所差异，尤其是 `etcd` 等服务发现后端。请根据实际环境、版本和安全要求调整配置。

## 下一步 {#next-steps}

规划安装之前，先确认与 `pg_tde` 兼容的 PostgreSQL 版本和部署类型。

[查看版本与支持的部署方式](/zh/percona/index/supported-versions/)

准备好配置加密后，即可开始安装。

[开始安装 pg_tde](/zh/percona/install/)
