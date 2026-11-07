---
title: 使用 Spock 创建双节点集群
description: 逐步创建一个使用 Spock 的双节点 active-active 复制集群。
weight: 40
upstream_source: pgedge-spock
upstream_link: https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/two_node_cluster.md
upstream_modified: true
upstream_ref: 4ac1aec2f080
source_kind: pinned-main-snapshot
linkTitle: 双节点教程
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---


> [!NOTE] 本站校注
> 原文第三步中 `pg_hba.conf` 的示例路径误写为 `postgresql.conf`。认证规则应写入实例实际使用的 `pg_hba.conf`；可用 `SHOW hba_file;` 查询路径。详见[已知上游问题](/zh/pgedge/about/maintenance/#upstream-issues)。


安装并初始化 PostgreSQL、创建 Spock 扩展之后，可以按以下步骤配置双节点集群。下文示例创建的集群包含两个节点，名称分别为 `n1` 和 `n2`，它们在端口 `5432` 上监听 PostgreSQL 服务器连接。

1. 连接每个节点，并使用以下命令初始化集群：

    `sudo /usr/pgsql-17/bin/postgresql-17-setup initdb`

    `sudo systemctl enable postgresql-17`

2. 使用你选择的编辑器打开 `postgresql.conf` 文件（位于 `/var/lib/pgsql/17/data/postgresql.conf`），并将以下参数添加到文件底部：

    `wal_level = 'logical'`

    `max_worker_processes = 20`

    `max_replication_slots = 10`

    `max_wal_senders = 10`

    `shared_preload_libraries = 'spock'`

    `track_commit_timestamp = on`

    这些值面向复制单个数据库的双节点示例。进入生产环境前，或添加节点/数据库时，请根据拓扑使用[为 Spock 规划 PostgreSQL 资源](/zh/pgedge/spock/sizing/)规划容量——订阅按数据库创建，因此 slot、walsender 和 worker 会随节点数乘以被复制数据库数扩展；`max_worker_processes` 还会与并行查询 worker 共享，并且实例中每个数据库需要一个槽位，supervisor 需要一个，slot sync worker 再需要一个。

3. 编辑 [`pg_hba.conf` 文件](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)（位于 `/var/lib/pgsql/current/data/postgresql.conf`），允许 `n1` 与 `n2` 之间建立连接；以下命令仅作示例，不建议用于生产系统，因为它们会让系统接受来自任意客户端的连接：

    `host all all 0.0.0.0/0 trust`

    `local replication all trust`

    `host replication all 0.0.0.0/0 trust`

4. 使用 [`spock.node_create`](/pgedge/spock/reference/functions/spock-node-create/) 命令创建 provider 与订阅者节点；在 `n1` 上使用命令：

    `SELECT spock.node_create (node_name := 'n1', dsn := 'host=<n1_ip_address> port=<n1_port> dbname=<db_name>');`

    在 `n2` 上：

      `SELECT spock.node_create (node_name := 'n2', dsn := 'host=<n2_ip_address> port=<n2_port> dbname=<db_name>');`

5. 在 `n1` 上，使用 [`spock.repset_add_all_tables`](/pgedge/spock/reference/functions/spock-repset-add-all-tables/) 命令将 `public` schema 中的表加入 `default` 复制集。如果在其他 schema 中操作，请按需自定义命令：

    `SELECT spock.repset_add_all_tables('default', ARRAY['public']);`

6. 在 n2 上，使用 [`spock.sub_create`](/pgedge/spock/reference/functions/spock-sub-create/) 命令创建 n2 到 n1 的订阅；订阅名为 `sub_n2_n1`：

    `SELECT spock.sub_create (subscription_name := 'sub_n2_n1', provider_dsn := 'host=<n1_ip_address> port=<n1 port> dbname=<db_name>');`

    `SELECT spock.sub_wait_for_sync('sub_n2_n1');`

7. 在 `n1` 上创建到 `n2` 的对应订阅，名称为 `sub_n1_n2`：

    `SELECT spock.sub_create (subscription_name := 'sub_n1_n2', provider_dsn := 'host=<n2_ip_address> port=<n2_port> dbname=<db_name>');`

8. 为确保 [DDL 语句修改自动复制](/zh/pgedge/spock/managing/spock-autoddl/)，请使用 PostgreSQL 客户端连接每个节点并调用以下 SQL 命令：

    `ALTER SYSTEM SET spock.enable_ddl_replication=on;`

    `ALTER SYSTEM SET spock.include_ddl_repset=on;`

    `ALTER SYSTEM SET spock.allow_ddl_from_functions=on;`

    `SELECT pg_reload_conf();`

9. 然后检查每个节点的状态：

```sql
  SELECT * FROM spock.node;
   node_id | node_name | location | country | info
  ---------+-------------+----------+---------+------
   22201 | subscriber1 | | |
   53107 | provider1 | | |
  (2 rows)

  SELECT * FROM spock.sub_show_status();
   subscription_name | status | provider_node | provider_dsn | slot_name | replication_sets | forward_origins
  -------------------+-------------+---------------+------------------------------------------+--------------------------------------+---------------------------------------+-----------------
   subscription1 | replicating | provider1 | host=localhost port=5432 dbname=postgres | spk_postgres_provider1_subscription1 | {default,default_insert_only,ddl_sql} |
  (1 row)
```

检查系统是否复制的简单测试是：连接 `n1` 上的 PostgreSQL 服务器并添加对象（例如表），然后确认它在 `n2` 上可用。类似地，可以在 `n2` 上创建对象，并确认它已出现在 `n1` 上。

---

[上游原文](https://github.com/pgEdge/spock/blob/4ac1aec2f0807dc7ee806ab99a6e99a4556186df/docs/two_node_cluster.md) · `4ac1aec2f080` · Copyright (c) 2021–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
