---
title: 在 lolor 中使用 pg_upgrade
description: 说明满足哪些条件时可以在安装 lolor 的集群上使用 pg_upgrade，以及升级前后的启用和禁用步骤。
weight: 200
upstream_source: pgedge-lolor
upstream_link: https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/pg_upgrade_with_lolor.md
upstream_modified: true
upstream_ref: ac3893a7707a
source_kind: pinned-main-snapshot
translation_status: machine-draft
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

接着执行升级。以下是一个 `pg_ugrade` 命令示例：

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

之后重新连接所有客户端会话。`lolor.enable()` 和 `lolor.disable()` 会更改每个 `pg_catalog.lo_*` 名称对应的函数 OID，而 libpq 会在每个连接中解析一次这些 OID，并在连接生命周期内缓存。如果某个会话在切换前使用过大对象，它会继续调用之前的实现。

---

[上游原文](https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/pg_upgrade_with_lolor.md) · `ac3893a7707a` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
