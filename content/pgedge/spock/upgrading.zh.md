---
title: 升级 Spock 扩展
description: 按节点安全地构建、安装并验证升级后的 Spock 扩展。
weight: 90
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/upgrading_spock.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 升级
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---




> [!NOTE]
> 如果你从源码构建 Spock 扩展，可以像处理任何其他
> [Postgres 扩展](https://www.postgresql.org/docs/17/extend-extensions.html#EXTEND-EXTENSIONS-UPDATES)一样移除、构建并升级 Spock 扩展。
>

如果你要升级一个安全的生产环境，请逐个关闭每个节点并执行以下步骤：

1. 禁用 Auto-DDL。
2. 停止 Postgres 服务器。
3. 为你的 Postgres 版本构建更新后的 Spock 二进制文件。
4. 重启 Postgres 服务器；这会触发扩展模式升级检查（Spock 的后台工作进程检测版本不匹配，并自动运行任何必要的模式迁移）。
5. 使用 psql 命令行验证正在使用的 Spock 版本和节点状态。
6. 升级集群中的所有节点之后，启用 Auto-DDL 并重启每个节点上的服务。

下面详细描述升级过程中的每个步骤。

## 禁用 Auto-DDL {#disabling-auto-ddl}

停止节点之前，禁用 DDL 复制，以防止升级期间发生模式变更。连接到每个节点并运行：

```sql
ALTER SYSTEM SET spock.enable_ddl_replication = off;
SELECT pg_reload_conf();
```

或者，在每个节点的 `postgresql.conf` 中设置以下参数：

```ini
spock.enable_ddl_replication = off
```

然后重新加载配置：

```sql
SELECT pg_reload_conf();
```


> [!WARNING]
> 如果新旧版本不兼容，这一步必不可少。
>

## 停止 Postgres 服务器 {#stopping-the-postgres-server}

升级 Spock 二进制文件之前，在你正在操作的服务器上停止 Postmaster：

```bash
pg_ctl -D /path/to/data1 stop -m fast
```


> [!WARNING]
> 如果新旧版本不兼容，这一步必不可少。
>

## 构建新的 Spock 二进制文件 {#building-the-new-spock-binaries}

构建扩展之前，你需要获取更新后的 Spock 源代码。如果你经常从源代码构建 Spock 扩展（源代码位于 https://github.com/pgEdge/spock），请使用 git 获取更新后的源码集；然后：

```bash
cd /path/to/spock-5.0.1
make clean
make
sudo make install
```

安装会复制以下文件：

- `spock.so` → `$(pg_config --pkglibdir)/`；
- `spock.control` → `$(pg_config --sharedir)/extension/`；
- `spock--5.0.1.sql` 和 `spock--5.0.0--5.0.1.sql` → `$(pg_config --sharedir)/extension/`。

接下来，你应验证更新后的 Spock 文件已经安装。可以使用以下命令确认版本更新。

检查库文件时间戳：

```bash
ls -l $(pg_config --pkglibdir)/spock.so
```

检查控制文件：

```bash
ls -l $(pg_config --sharedir)/extension/spock.control
```

检查升级后的 .sql 文件是否存在；例如：

```bash
ls -l $(pg_config --sharedir)/extension/spock--5.0.0--5.0.1.sql
```

## 重启 Postgres 服务器 {#restarting-the-postgres-server}

然后，使用 pg_ctl 重启 Postgres postmaster
进程：

```bash
pg_ctl -D /path/to/data1 restart
```

服务器重启时，Spock 的数据库管理器后台工作进程会自动检测版本不匹配，并升级扩展模式（通过 `spock.c` 中的 `spock_manage_extension()`）。


## 验证扩展升级 {#verifying-the-extension-upgrade}

构建扩展后，你可以验证正在使用的扩展版本以及复制集群的状态。使用 psql 命令行调用后面的命令。

使用 psql 连接数据库：

```bash
psql -d database_name -p port_number
```

验证正在使用的 Spock 版本：

```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'spock';
```

然后验证节点正在复制。使用以下命令检查订阅是否处于活动状态：

```sql
SELECT sub_name, sub_enabled, sub_slot_name, sub_replication_sets
FROM spock.subscription;
```

检查复制槽：

```sql
SELECT slot_name, active, restart_lsn FROM pg_replication_slots;
```

检查节点状态：

```sql
SELECT * FROM spock.node;
```

## 在每个节点上启用 Auto-DDL 并重启服务 {#enabling-auto-ddl-and-restarting-the-service-on-each-node}

升级集群中的所有节点后，使用 psql 连接每个节点并启用 DDL 复制：

```sql
ALTER SYSTEM SET spock.enable_ddl_replication = on;
SELECT pg_reload_conf();
```

或者，你可以在 `postgresql.conf` 文件中修改该参数：

```ini
spock.enable_ddl_replication = on
```

重新加载配置：

```sql
SELECT pg_reload_conf();
```

然后，在每个节点上重启服务：

```bash
pg_ctl -D /path/to/data1 restart
```

## 最终验证 {#final-verification}

在集群中的每台服务器上执行上述步骤后，使用以下命令验证每个节点的复制状态：

```sql
SELECT application_name, state, sync_state, write_lag, flush_lag, replay_lag
FROM pg_stat_replication;
```

你应确认：

- 所有节点报告一致的版本（目标版本）。
- 复制延迟极小或为零。
- PostgreSQL 或 Spock 日志中没有错误。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/upgrading_spock.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
