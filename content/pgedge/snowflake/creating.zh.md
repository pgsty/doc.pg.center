---
title: 在新集群中创建 Snowflake 序列
description: 说明托管部署如何自动分配 snowflake.node，以及自管或源码安装如何手动配置节点标识符。
weight: 200
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/creating.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



使用 Snowflake 序列之前，集群中的每个节点必须拥有唯一的 `snowflake.node` 标识符。取值范围是 1 到 1023，并且在集群内每个节点上必须互不相同。

## 在托管部署中设置 snowflake.node {#setting-snowflakenode-in-a-managed-deployment}

pgEdge 部署会为你分配 `snowflake.node`，其值来自每个节点在集群中的位置：

* Control Plane 从节点序号设置 `snowflake.node`。
* pgEdge Helm chart 从每个节点名称推导 `snowflake.node`。
* pgEdge Ansible playbook 从节点 zone 设置 `snowflake.node`。

使用这些方法部署时，无需再为节点标识符执行其他配置。

## 手动设置 snowflake.node {#setting-snowflakenode-manually}

对于自管安装或源码安装，需要自行设置该值。使用 `ALTER SYSTEM` 分配唯一节点号，然后重新加载服务器使更改生效。以下示例将节点标识符设置为 `10`：

```sql
ALTER SYSTEM SET snowflake.node = 10;
SELECT pg_reload_conf();
```

也可以直接把参数加入 `postgresql.conf` 文件。下面这一行将主机标识为节点 `11`：

```ini
snowflake.node = 11
```

编辑 `postgresql.conf` 后，重新加载服务器使更改生效。可以从 psql 重新加载：

```sql
SELECT pg_reload_conf();
```

也可以使用 `pg_ctl` 重新加载服务器：

```sh
pg_ctl reload -D "/path/to/your/data/directory"
```

Snowflake 配置完成后，可以先[转换](/zh/pgedge/snowflake/converting/) PostgreSQL 序列，再开始使用 Snowflake 序列。

---

[上游原文](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/creating.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
