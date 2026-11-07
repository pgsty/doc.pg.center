---
title: lolor 发布说明
description: 记录 lolor 1.3.0、1.2.3 与 1.2.2 的功能、安全修复、迁移行为和升级注意事项。
weight: 200
upstream_source: pgedge-lolor
upstream_link: https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/lolor_release_notes.md
upstream_modified: true
upstream_ref: ac3893a7707a
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



## lolor 1.3.0 {#lolor-130}

* 新增 PostgreSQL 原生存储与 lolor 存储之间的双向大对象迁移，在 C 中实现为 relation 到 relation 的直接复制（`lolor.migrate_storage()`），而不是循环调用大对象 API：
  * `lolor.migrate_from_native(peer_oids oid[] DEFAULT NULL)` 将原生 PostgreSQL 大对象移入 lolor 存储。它是 `CREATE EXTENSION lolor` 之后的手动步骤，需要超级用户，返回移动的对象数；迁移被拒绝时返回 -1。
  * `lolor.migrate_to_native()` 将对象移回原生存储，无论 lolor 是否启用。它是删除扩展前的手动步骤；仍有对象留在 lolor 存储中时删除会被拒绝，删除本身不再迁移任何内容。
  * 两个方向都保留 OID、owner、ACL、注释和精确页面布局，因此稀疏对象保持稀疏。移回原生存储时，所有权和 ACL 会记录到 `pg_shdepend`，因此 `DROP ROLE`、`REASSIGN OWNED` 和 `DROP OWNED` 再次能看到这些对象。对象位于 lolor 存储期间，注释暂存在 `lolor.pg_largeobject_description`。原生对象按与 `DROP` 相同的簿记（依赖、注释和标签）移除，但不取 `DROP` 所需的逐对象锁，因此包含大对象数量超过锁表容量的数据库也能迁移，而无需提高 `max_locks_per_transaction`。
  * 迁移时会对照正在运行的服务器验证存储布局。lolor 存储无法表示 security label；遇到时 `migrate_from_native()` 会拒绝。OID 冲突会报告冲突的 OID。
  * 迁移在提交前对两个存储持有 `ShareRowExclusiveLock`。普通大对象访问取 `RowExclusiveLock`，该锁与自身不冲突；否则并发 `lo_write()` 可能被静默丢失。方向相反的迁移按固定顺序取锁，不会死锁。
  * 只要有任何其他会话连接到数据库，两个迁移函数都会拒绝执行，并且只允许从客户端会话运行。
  * 安装 spock 时，两个函数都在 `spock.repair_mode()` 下运行。如果存在 spock 无法抑制的逻辑 slot——非 spock slot，或没有 spock 时的任何 slot——它们会拒绝执行，而不是让订阅者把迁移解码为行变更。
  * 迁移是节点本地的：原生大对象永远不会复制，因此必须直接连接每个节点并在其上运行迁移。不要通过 DDL 复制发送它；那会在每个订阅者的应用工作进程中运行。原生 OID 没有节点编码，因此应把其他节点的 OID（来自 `lolor.native_lo_oids()`）作为 `peer_oids` 传入，把跨节点碰撞变成拒绝，并在之后跨节点比较 `lolor.digest()`。
  * 只要仍有对象引用已删除的角色，`migrate_to_native()` 就会以明确错误拒绝，而不是在中途以 “role N was concurrently dropped” 失败；用 `lo_unlink()` 删除这些对象后重试。
* 新增辅助函数 `lolor.digest()` 和 `lolor.native_lo_oids()`，用于节点本地迁移后的跨节点检查。
* 新增辅助函数 `lolor.check_orphans()` 和 `lolor.fix_orphans(new_owner)`，用于 owner、被授权者或授权者已被删除的对象。lolor 存储中的对象无法参与 `pg_shdepend`，因此 `DROP ROLE` 注意不到它们；`check_orphans()` 列出这些对象以及悬空的引用，`fix_orphans()` 像 `REASSIGN OWNED` 一样重新分配失效 owner、在 ACL 中替换它们，使它们此前作出的授权保留，并删除仍指向缺失角色的条目。
* **安全修复：任何数据库用户此前都可以执行 `lo_import()` 和 `lo_export()`。** 这两个函数以 PostgreSQL 运行账户在服务器上读写文件，因此核心版本撤销其 `EXECUTE` 权限，不再授予 `PUBLIC`。lolor 通过把原函数重命名为 `*_orig` 来替换它们；ACL 属于函数而不是名称，所以限制仍留在暂存的原函数上，而每个替换函数都得到默认的 `EXECUTE TO PUBLIC`。任何用户都可以用 `lo_import()` 读取任意服务器文件，或用 `lo_export()` 覆盖文件。替换函数现在会在安装时锁定，升级也会在既有安装的任一状态下撤销权限。1.0 到 1.2.2 版本受影响。
* 扩展不再标记为 `trusted`。安装 lolor 会为整个数据库重命名 `pg_catalog` 中的函数，非超级用户不应能够执行该操作。
* **修复 `DROP ROLE` 以 “unrecognized object class” 失败的问题。** 创建大对象时会记录一条 `pg_shdepend` 行，其 `classId` 是 `lolor.pg_largeobject` 的 OID；这是一个普通表而非 catalog。任何创建过大对象的角色都因此无法删除，而且这些行永远不会清理，因为 `inv_drop()` 以 `PERFORM_DELETION_SKIP_ORIGINAL` 删除。lolor 不再记录这些行，升级也会删除既有行。
  * 清理按数据库进行，因此必须在每个启用了 lolor 的数据库中运行 `ALTER EXTENSION lolor UPDATE`。在此之前，集群中任何位置的 `DROP ROLE` 都会继续报告 “owner of objects in database X”。
  * 如果数据库在较早版本上运行过 `DROP EXTENSION lolor`，这些行仍会存在，并指向已经不存在的表，而升级脚本不会在那里运行。在该数据库中以超级用户手动清理：用 `SELECT DISTINCT classid FROM pg_shdepend WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database()) AND classid NOT IN (SELECT oid FROM pg_class)` 找到过期 class OID，然后执行 `DELETE FROM pg_shdepend WHERE dbid = <that dbid> AND classid IN (<those OIDs>)`。
* **lolor 现在必须列在 `shared_preload_libraries` 中。** 按需加载会被拒绝：`CREATE EXTENSION lolor`、`LOAD 'lolor'`，以及任何触达 lolor 函数的调用，都会以 `lolor must be loaded via "shared_preload_libraries"` 失败；lolor 未安装或禁用时，原生 `pg_catalog.lo_*` 函数不受影响。下述删除防护是对象访问钩子，只有预加载库时它才存在于每个 backend 和 worker 中；库缺失或损坏现在会在服务器启动时失败，而不是等到第一次 `lo_open()`。按以下顺序升级：安装新的库文件，把 `lolor` 加入 `shared_preload_libraries`，重启，然后在每个数据库中运行 `ALTER EXTENSION lolor UPDATE`。在文件安装和重启之间，任何按需加载新库的会话都会得到该错误，因此应尽快重启。
* 删除扩展受对象访问钩子保护。只要 lolor 处于启用状态，或仍有对象留在 lolor 存储中，`DROP EXTENSION`、`DROP SCHEMA lolor CASCADE`、`DROP OWNED BY` 以及所有可达扩展的路径都会拒绝；检查由执行删除的 backend 在删除时刻查询 catalog。**删除操作本身不再迁移对象**：先运行 `lolor.migrate_to_native()`。事件触发器只会恢复原生 `pg_catalog.lo_*` 名称。新的超级用户设置 `lolor.allow_unsafe_drop` 会跳过两项检查并丢弃 lolor 存储内容。由于删除会把原生函数名称改回，它与 `lolor.disable()` 要求相同：没有其他会话连接到数据库，并且必须在客户端会话中执行。
* `lolor.enable()` 和 `lolor.disable()` 只允许从客户端会话运行，因此复制 DDL 无法在应用工作进程中执行它们；在那里被拒绝会让该节点的复制永远重试。
* `CREATE EXTENSION lolor` 与 `lolor.enable()` 要求相同，因为安装脚本会以同样方式重命名原生函数：没有其他会话连接到数据库，并且必须在客户端会话中执行。
* `lolor.enable()`、`lolor.disable()` 和 `lolor.is_enabled()` 现在在 `pg_catalog` 中探测精确函数签名。它们之前按 `proname` 在所有 schema 中匹配，因此任何在任一 schema 拥有 `CREATE` 权限的用户都可以定义名为 `lolor_lo_open` 的函数，把 lolor 卡在永久“不一致状态”，该状态还会阻止 `DROP EXTENSION`。这两个函数现在都会发出客户端会话必须重连的通知，因为 libpq 会按连接缓存大对象函数 OID；只要有任何其他会话连接到数据库，它们也会拒绝执行，因为重命名后的函数保留其 OID，其他会话无法被强制看到切换。
* `lolor.enable()`、`lolor.disable()`、迁移函数和删除操作背后的会话检查现在在 C 中完成，并在计数前对数据库取得排他锁，因此同一时刻连接的会话要么被计入，要么等待到操作事务结束。之前它使用 `pg_stat_activity` 快照，可能漏掉这样的会话。单用户模式不再被拒绝。
* 对 `lolor.enable()`、`lolor.disable()`、迁移函数、`lolor.check_orphans()`、`lolor.fix_orphans()` 和删除扩展，已加载库与已安装扩展版本不同时会拒绝。如果库文件是新版本而安装的扩展是旧版本，删除操作会运行旧版本的 `disable()`，其中仍包含本版本修复的非限定函数查找。请先运行 `ALTER EXTENSION lolor UPDATE`。
* 修复 `lolor.node` 上界。该 GUC 之前接受 0..16，但生成的 OID 为节点 ID 保留四位，因此节点 16 无法容纳：它生成的每个 OID 的节点字段读回都是 0。上界现在由编码推导（`LOLOR_MAX_NODE_ID`），即 0..15。**如果你配置了 `lolor.node = 16`**，服务器仍会启动，但会记录 `16 is outside the valid range for parameter "lolor.node" (0 .. 15)` 并回退到 0；这实际上正是它此前使用的节点 ID。请设置为 0..15 中的值，并对照真正使用 0 的节点检查 OID 碰撞。
* 扩大测试覆盖：dump/restore、流复制和逻辑复制、standby 提升、删除路径、迁移保真与锁、跨节点 OID 碰撞的 TAP 测试；`lo_lseek`、`lo_tell`、`lo_truncate`、64 位接口、稀疏对象、注释往返、`pg_shdepend` 恢复、权限强制执行、orphan 辅助函数和名称抢占的回归测试。回归套件在自带预加载实例上运行。
* 安全加固：处理 Codacy/Flawfinder 警告。

## lolor 1.2.3 {#lolor-123}

* 新增 PostgreSQL 19 支持
* 新增仓库内发布工作流和 RPM/DEB 打包
* 改进 CI：从源码构建测试集群，把 PostgreSQL 19 加入测试矩阵，并限制测试运行时间

## lolor 1.2.2 {#lolor-122}

* 修复 lolor 升级
* 修复 pg_upgrade 相关问题。注意，此修复面向之后的 pg_upgrade 升级。升级扩展本身时 `ALTER EXTENSION UPDATE` 可用；因此如果要运行 pg_upgrade，请先把扩展更新到 1.2.2，再运行 pg_upgrade
* 处理 CVE CVE-2022-26520、GHSA-673j-qm5f-xpv8
* 更新 PATH 以匹配原生 PostgreSQL 打包布局
* 提高表 OID 缓存安全性

---

[上游原文](https://github.com/pgEdge/lolor/blob/ac3893a7707a65f71f494f260b1e3cd88f171770/docs/lolor_release_notes.md) · `ac3893a7707a` · Copyright (c) 2024–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
