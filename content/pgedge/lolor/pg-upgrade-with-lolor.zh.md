---
title: 在 lolor 中使用 pg_upgrade
description: 说明满足哪些条件时可以在安装 lolor 的集群上使用 pg_upgrade，以及升级前后的启用和禁用步骤。
weight: 200
upstream_source: pgedge-lolor-20261121
upstream_link: https://github.com/pgEdge/lolor/blob/1548836b0df0819e5415a9d0574afd93e9a64f1d/docs/pg_upgrade_with_lolor.md
upstream_modified: true
upstream_ref: 1548836b0df0
source_kind: pinned-main-snapshot
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



`pg_upgrade` 工具用于升级 PostgreSQL 版本。

只要使用 lolor 1.2.2 或更新版本，就可以使用 `pg_upgrade` 搭配已安装的 `lolor` 扩展。如果使用较旧版本的 lolor，需要先升级扩展。

两个集群都必须把 `lolor` 列在 `shared_preload_libraries` 中；否则新集群无法加载 lolor 的库，恢复扩展会失败。

运行 `pg_upgrade` 前，必须禁用 `lolor`。执行 pg_upgrade 后，可以启用 lolor。使用 `psql` 或其他客户端禁用 lolor：

```
db1_17=# SELECT lolor.disable();
```

接着执行升级。下面给出一条 `pg_upgrade` 命令示例。

```
# pg_upgrade --old-datadir=/data/db1_17 \
		--new-datadir=/data/db1_18 \
		--old-bindir=/usr/lib/postgresql/17/bin \
		--new-bindir=/usr/lib/postgresql/18/bin \
		--link
```

然后使用 psql 启用 `lolor`：

```
db1_18=# SELECT lolor.enable();
```

随后应重新建立所有客户端连接。`lolor.enable()` 和 `lolor.disable()` 会改变各个 `pg_catalog.lo_*` 名称对应的函数 OID。libpq 只在每个连接上解析一次这些 OID，并将其缓存到连接结束。如果会话在切换前使用过大对象，又没有重新连接，它就会继续调用原来的实现。

---

[上游原文](https://github.com/pgEdge/lolor/blob/1548836b0df0819e5415a9d0574afd93e9a64f1d/docs/pg_upgrade_with_lolor.md) · `1548836b0df0` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
