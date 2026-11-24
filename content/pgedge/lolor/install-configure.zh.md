---
title: 安装并配置 lolor
description: 安装 lolor 扩展，配置 shared_preload_libraries、节点编号，并把大对象表加入 Spock 复制集。
weight: 200
upstream_source: pgedge-lolor-20261121
upstream_link: https://github.com/pgEdge/lolor/blob/1548836b0df0819e5415a9d0574afd93e9a64f1d/docs/install_configure.md
upstream_modified: true
upstream_ref: 1548836b0df0
source_kind: pinned-main-snapshot
translation_status: translated
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

lolor 必须随服务器启动加载。请将它加入 `postgresql.conf` 中的 `shared_preload_libraries`，然后重启服务器。如果按需加载库，`CREATE EXTENSION lolor`、`LOAD 'lolor'` 以及任何调用 lolor 函数的操作都会报错 `lolor must be loaded via "shared_preload_libraries"`。未安装或已禁用 lolor 时，原生 `pg_catalog.lo_*` 函数不受影响。删除扩展时，lolor 依靠对象访问钩子保护大对象。只有预加载此库，才能保证每个后端进程都安装了该钩子。

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

还可以修改 `search_path`，从 `lolor` 模式查找大对象相关的表。

```
SET search_path=lolor,"$user",public,pg_catalog
```

lolor 会把 `pg_catalog.lo_*` 中的既有方法重命名为 `pg_catalog.lo_*_orig`，并引入这些方法的新版本。如果移除扩展，重命名后的 `pg_catalog.lo_*_orig` 函数会恢复其初始名称。

使用 Spock 复制大对象时，`pg_largeobject`、`pg_largeobject_metadata` 和 `pg_largeobject_description` 三张表必须属于你的复制集。第三张表保存从原生存储迁入的各个对象的注释；如果不复制它，`lo_unlink()` 会在其他节点上留下该注释，后来添加或重新同步的节点也收不到这些注释。连接 lolor 数据库，并使用 `spock.repset_add_table` 添加它们：

```sql
-- 'default' is Spock's built-in replication set; subscriptions consume it automatically.
SELECT spock.repset_add_table('default', 'lolor.pg_largeobject');
SELECT spock.repset_add_table('default', 'lolor.pg_largeobject_metadata');
SELECT spock.repset_add_table('default', 'lolor.pg_largeobject_description');
```

---

[上游原文](https://github.com/pgEdge/lolor/blob/1548836b0df0819e5415a9d0574afd93e9a64f1d/docs/install_configure.md) · `1548836b0df0` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
