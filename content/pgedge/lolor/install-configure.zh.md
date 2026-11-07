---
title: 安装并配置 lolor
description: 安装 lolor 扩展，配置 shared_preload_libraries、节点编号，并把大对象表加入 Spock 复制集。
weight: 200
upstream_source: pgedge-lolor
upstream_link: https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/install_configure.md
upstream_modified: true
upstream_ref: ac3893a7707a
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



lolor 支持 PostgreSQL 16 及之后的版本。

lolor 随 pgEdge Distributed Postgres 和 pgEdge Enterprise Postgres 提供，因此 pgEdge 部署会为你提供该扩展。Control Plane 会在标准集群设置过程中把 lolor 软件包安装到每个节点。

如果你自行管理 PostgreSQL，可以从[源码](https://github.com/pgEdge/lolor)编译并安装该扩展，流程与其他使用 PGXS 构建的 PostgreSQL 扩展相同。确保 PATH 环境变量包含 `pg_config`（位于 PostgreSQL 安装目录下）所在目录。

```
export PATH=/opt/pg16/bin:$PATH

# compile
make USE_PGXS=1
make USE_PGXS=1 install
```

lolor 必须在服务器启动时加载。将其加入 `shared_preload_libraries`，该设置位于 `postgresql.conf`，然后重启；当库按需加载时，`CREATE EXTENSION lolor`、`LOAD 'lolor'` 以及任何会触达 lolor 函数的调用都会以 `lolor must be loaded via "shared_preload_libraries"` 失败；lolor 未安装或禁用时，原生 `pg_catalog.lo_*` 函数不受影响。删除扩展时保护大对象的防护机制是对象访问钩子，只有库被预加载时它才会存在于每个 backend。

```
shared_preload_libraries = 'lolor'
```

然后连接 PostgreSQL 数据库，并使用以下命令创建扩展：

```
CREATE EXTENSION lolor;
```

## 配置 lolor {#configuring-lolor}

在复制集群中使用该扩展前，必须在每个节点上设置 `lolor.node` 参数。取值范围是 1 到 15（0 表示未设置）；它会被编码到 lolor 生成的每个大对象 OID 的低四位，因此每个节点必须使用不同值。

```
lolor.node = 1
```

也可以修改 `search_path`，以从 `lolor` schema 选取大对象相关表：

```
SET search_path=lolor,"$user",public,pg_catalog
```

lolor 会把 `pg_catalog.lo_*` 中的既有方法重命名为 `pg_catalog.lo_*_orig`，并引入这些方法的新版本。如果移除扩展，重命名后的 `pg_catalog.lo_*_orig` 函数会恢复其初始名称。

使用 Spock 复制大对象时，`pg_largeobject` 和 `pg_largeobject_metadata` 表必须属于你的复制集。连接 lolor 数据库，并使用 `spock.repset_add_table` 添加它们：

```sql
-- 'default' is Spock's built-in replication set; subscriptions consume it automatically.
SELECT spock.repset_add_table('default', 'lolor.pg_largeobject');
SELECT spock.repset_add_table('default', 'lolor.pg_largeobject_metadata');
```

---

[上游原文](https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/install_configure.md) · `ac3893a7707a` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
