---
title: LOLOR
description: lolor 将 PostgreSQL 风格大对象存储在可复制的非 catalog 表中，并提供双向迁移与一致性检查。
weight: 20
upstream_source: pgedge-lolor
upstream_link: https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/index.md
upstream_modified: true
upstream_ref: ac3893a7707a
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
linkTitle: LOLOR
icon: fa-solid fa-book-open
sidebar_root_for: self
no_list: true
type: docs
sidebar_root_menu: false
---


> [!NOTE] 版本说明
> 本文档来自上游 `main` 的固定源码快照；与原站的版本化文档可能存在差异。部署前请核对[版本与来源](/zh/pgedge/about/attribution/)。


[lolor](https://github.com/pgEdge/lolor) 是一个扩展，使 PostgreSQL 风格的大对象与逻辑复制兼容。

PostgreSQL 按 [pg_largeobject](https://www.postgresql.org/docs/current/catalog-pg-largeobject.html) 表所述，以相关数据块的形式支持大对象。大对象为存储在 catalog 中特殊大对象结构里的用户数据提供流式访问。存储在 catalog 表中的大对象在复制期间需要特殊处理；lolor 扩展可以将大对象存储在非 catalog 表中，从而帮助实现大对象复制。

lolor 在 `lolor` schema 中创建并管理与大对象相关的表：

```
lolor.pg_largeobject
lolor.pg_largeobject_metadata
```

PostgreSQL 大对象允许在数据库内存储大文件。每个大对象由创建时分配的 OID 标识。lolor 将对象以较小分段存储在独立系统表中，并为大对象生成关联 OID，这些 OID 与原生大对象的 OID 不同。

使用 `lolor` 扩展要求 PostgreSQL 16 或更新版本。


## 迁移大对象 {#migrating-large-objects}

两个方向的迁移都是手动步骤：由你决定何时将既有大对象移入 lolor 存储，并在删除扩展前将其移回。删除扩展永远不会移动数据：只要仍有对象位于 lolor 存储中，删除就会被拒绝。

### 原生大对象迁移到 lolor（手动） {#native-to-lolor-manual}

如果数据库已经包含 PostgreSQL 原生大对象，请在启用扩展后调用 `migrate_from_native()`。迁移会保留原始 OID、owner、ACL 和数据，因此既有应用引用仍然有效。

```sql
CREATE EXTENSION lolor;
SELECT lolor.migrate_from_native();
```

该函数返回迁移的大对象数量。没有原生大对象时调用它是安全的。此步骤有意不自动执行：它需要超级用户权限，并应在维护窗口中执行。

### lolor 迁移回原生（在 DROP EXTENSION 之前） {#lolor-to-native-before-drop-extension}

将大对象移回 PostgreSQL 原生存储，然后删除扩展：

```sql
SELECT lolor.migrate_to_native();
DROP EXTENSION lolor;
```

两个方向都会保留 OID、owner、ACL、注释和数据，并逐页复制，因此稀疏大对象保持稀疏。

一个辅助函数支持跨节点验证迁移：

```sql
SELECT * FROM lolor.digest();         -- per-object checksum, compare across nodes
```

只要扩展处于启用状态或任何对象仍在 lolor 存储中，对象访问钩子会在所有可达路径（`DROP EXTENSION`、`DROP SCHEMA lolor CASCADE`、`DROP OWNED BY`）上拒绝删除扩展。删除本身只会恢复原生 `pg_catalog.lo_*` 名称。如果确实要丢弃 lolor 存储中的内容，超级用户可以在执行删除的会话中设置 `lolor.allow_unsafe_drop = on`。它会跳过所有检查，而且该删除也不会恢复原生函数名，因此如果 lolor 已启用，请先运行 `lolor.disable()`。lolor 启用时，正常删除会将原生函数名称改回，因此它与 `lolor.disable()` 有相同要求：没有其他会话连接到数据库，并且必须在客户端会话中执行。禁用的 lolor 不会重命名任何内容，删除也没有这些要求。

只要有任何其他会话连接到数据库，`lolor.enable()` 和 `lolor.disable()` 就会拒绝执行，并且只允许从客户端会话运行。在 `enable()` 或 `disable()` 后重新连接客户端会话：libpq 会按连接缓存大对象函数 OID。

两个辅助函数用于查找并修复角色已被删除的对象：

```sql
SELECT * FROM lolor.check_orphans();  -- objects referring to a dropped role
SELECT lolor.fix_orphans('some_role');  -- reassign them and drop dead ACL entries
```

安装了 spock 扩展时，两个迁移函数都会在 `spock.repair_mode()` 下运行，因此移动元组的迁移 DML **不会**复制到其他节点。这对 `migrate_to_native()` 至关重要：否则它对 lolor 表的删除会被复制，而原生重建仍留在本地，从而破坏其他节点上的大对象。

即使有 spock，只要存在非 spock 逻辑复制 slot（例如 `pgoutput`、`wal2json`），迁移仍会被拒绝，因为 repair mode 只抑制 spock 自己的 output plugin，而这些消费者仍会解码迁移 DML：`migrate_to_native()` 会引发 `ERROR`，`migrate_from_native()` 会发出警告并返回 -1，不做任何事。请在迁移前删除相关 slot。

没有 spock 时，迁移 DML 无法从逻辑解码中排除，因此只要数据库中存在逻辑复制 slot，两个函数都会拒绝迁移：`migrate_from_native()` 会引发 `WARNING` 并返回 -1，不做任何事（0 保留给“没有可迁移对象”），而 `migrate_to_native()` 会引发 `ERROR`。请在迁移前删除所有逻辑复制 slot；仅禁用订阅并不足够，因为其 slot 会保留变更，并在复制恢复时投递它们。

## 限制 {#limitations}

- 使用 lolor 扩展期间，不能使用 PostgreSQL 原生大对象功能。
- 对于保存在 lolor 存储中的对象，lolor 不支持以下语句：`ALTER LARGE OBJECT`、`GRANT ON LARGE OBJECT`、`COMMENT ON LARGE OBJECT` 和 `REVOKE ON LARGE OBJECT`。对象处于原生存储期间设置的 owner、ACL 和注释会在两个方向的迁移中保留。
- 只要任何其他会话连接到数据库，`lolor.enable()`、`lolor.disable()`、迁移函数、`CREATE EXTENSION lolor`，以及 lolor 启用时删除扩展，都会拒绝执行；规则与 `ALTER DATABASE ... RENAME` 相同：重命名的函数保留其 OID，因此已经解析过 `lo_*` 函数的会话会继续调用旧实现，元组移动也无法对其他 backend 做成原子操作。调用会话必须在 `enable()` 或 `disable()` 后重新连接。这些操作也只允许从客户端会话运行，因此复制 DDL 无法在应用工作进程中驱动它们。只有客户端会话计入：复制应用工作进程等后台 worker 不会按名称调用 `lo_*` 函数。为了可靠计数，这些操作都会先对数据库取得排他锁，使新的数据库连接等待到操作事务结束。单用户模式下它们无需会话检查即可运行。
- 对于 `lolor.enable()`、`lolor.disable()`、迁移函数、`lolor.check_orphans()`、`lolor.fix_orphans()` 和删除扩展，已加载库与已安装扩展必须是同一版本。安装新的库文件后，在每个数据库中运行 `ALTER EXTENSION lolor UPDATE` 再使用它们；在此之前它们会拒绝执行并指出两个版本。
- lolor 存储中的对象是普通表中的行，因此不能参与 `pg_shdepend`。`DROP ROLE`、`DROP OWNED BY` 和 `REASSIGN OWNED BY` 看不到它们：拥有它们或出现在其 ACL 中的角色可以不经警告被删除，而 `REASSIGN OWNED` / `DROP OWNED` 不会触及它们。删除角色前，在每个启用了 lolor 的数据库中运行 `REASSIGN OWNED BY` 或 `DROP OWNED BY`，再运行 `DROP ROLE`。对于拥有扩展的角色，应使用 `REASSIGN OWNED BY`：`DROP OWNED BY` 会连扩展一起移除，并且在仍有对象位于 lolor 存储中时会被拒绝。之后在每个这样的数据库中运行 `lolor.check_orphans()`，并用 `lolor.fix_orphans(new_owner)` 修复其报告；存在 orphan 时 `lolor.migrate_to_native()` 会拒绝执行。
- 角色 OID 来自集群范围计数器并会回绕，因此新角色可能获得已删除角色的 OID，并静默成为该角色 orphan 对象的 owner 或被授权者。这无法事后检测，也是删除角色后应尽快运行 `lolor.check_orphans()` 的另一个原因。
- 大对象迁移是节点本地的。原生大对象位于 `pg_catalog.pg_largeobject`，该表永远不会被复制，因此每个节点持有独立集合，而 `migrate_from_native()` 只迁移本地节点对象；安装 spock 时，迁移 DML 在 repair mode 中运行，不会被复制。请在每个持有原生大对象的节点上直接连接该节点执行迁移。该函数拒绝在应用工作进程中运行，因此通过 DDL 复制发送它会在每个订阅者上失败。迁移后的对象保留其原始原生 OID，这些 OID 没有节点编码：如果不同节点在同一 OID 下持有不同对象，各节点的 lolor 内容会发散，之后对这些对象的复制变更可能冲突。新创建的大对象没有碰撞风险，因为新 OID 通过 `lolor.node` 做节点编码，并与既有行检查。要让该风险变成错误而不是静默发散，可使用 `lolor.native_lo_oids()` 收集其他节点的 OID 并传入：`SELECT lolor.migrate_from_native(peer_oids => ARRAY[...])` 会在任何碰撞时拒绝执行。迁移完每个节点后，跨节点比较 `lolor.digest()` 以确认它们已收敛。

## 继续阅读 {#continue-reading}

- [安装并配置 lolor](/zh/pgedge/lolor/install-configure/)
- [lolor 发布说明](/zh/pgedge/lolor/lolor-release-notes/)
- [在 lolor 中使用 pg_upgrade](/zh/pgedge/lolor/pg-upgrade-with-lolor/)
- [使用 lolor](/zh/pgedge/lolor/using-lolor/)

---

[上游原文](https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/index.md) · `ac3893a7707a` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
