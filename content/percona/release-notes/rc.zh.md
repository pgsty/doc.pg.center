---
title: 发布候选版 1
linkTitle: RC 1
description: pg_tde RC1：WAL 加密重构、默认主密钥、权限控制与 tde_heap_basic 弃用。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/rc.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 900
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

本版本提供以下功能和改进：

* **重新设计 WAL 加密，提高性能。**

    WAL 加密方案经过重新设计。启用加密并启动服务器后，`pg_tde` 从第一次 WAL 写入开始加密整个 WAL 文件；加密范围记录在内部密钥元数据中。这改善了原生复制场景下的 WAL 加密流程，并提高大规模数据库的性能。

* **用于单租户的默认加密密钥。**

    可以为整个数据库集群设置默认主密钥，供所有未设置自定义主密钥的数据库和表使用。这简化了每个用户拥有独立数据库实例的单租户环境中的加密配置与管理。

* **可以修改密钥提供商配置。**

    提供商配置变化后，不再需要新建提供商并设置新主密钥。现在可以通过[函数](/zh/percona/functions/#key-provider-management)修改当前数据库或整个集群的提供商配置，解除原有限制，并采用 PostgreSQL 原生、常见的操作方式。

* **密钥管理权限。**

    新增函数分别管理全局和数据库密钥管理权限，提供更细粒度的控制，并允许将密钥管理任务委派给不同角色。

* **主密钥和提供商的更多信息。**

    新增函数显示主密钥和提供商的附加信息，帮助理解当前配置并排查密钥管理问题。

* **弃用 tde_heap_basic 访问方法。**

    `tde_heap_basic` 的加密能力有限且影响性能；由于索引不加密，用于生产还存在潜在安全风险。因此上游决定弃用该访问方法，并在未来版本移除。请改用 Percona Server for PostgreSQL 17 提供的 `tde_heap`。该发行版是 PostgreSQL 社区版的兼容替代品。

## 升级注意事项 {#upgrade-considerations}

由于代码发生重大变化，`pg_tde` RC 不向后兼容 Beta2，不能直接升级。必须先[卸载](/zh/percona/how-to/uninstall/) Beta2，再[安装](/zh/percona/install/)并配置新的候选发布版本。

## 已知问题 {#known-issues}

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

* 即使关联的主密钥仍在使用，此版本也允许删除全局密钥提供商。这一已知问题将在下一版本修复。目前请避免删除全局密钥提供商。

## 变更日志 {#changelog}

### 新功能 {#new-features}

* [PG-1234](https://perconadev.atlassian.net/browse/PG-1234)：增加函数，分别管理全局和数据库密钥管理权限。
* [PG-1255](https://perconadev.atlassian.net/browse/PG-1255)：增加删除密钥提供商的功能。
* [PG-1256](https://perconadev.atlassian.net/browse/PG-1256)：通过默认主密钥支持单租户。
* [PG-1258](https://perconadev.atlassian.net/browse/PG-1258)：增加显示主密钥和提供商附加信息的函数。
* [PG-1294](https://perconadev.atlassian.net/browse/PG-1294)：重新设计 WAL 加密。
* [PG-1303](https://perconadev.atlassian.net/browse/PG-1303)：弃用 tde_heap_basic 访问方法。

## 改进 {#improvements}

* [PG-858](https://perconadev.atlassian.net/browse/PG-858)：重构内部密钥和主密钥的 LWLock，使本地数据库能够继承全局密钥提供商。
* [PG-1243](https://perconadev.atlassian.net/browse/PG-1243)：调查特定阈值和大数据库的性能问题，更新提示位处理文档。
* [PG-1310](https://perconadev.atlassian.net/browse/PG-1310)：通过 GUC 参数强制指定访问方法。
* [PG-1361](https://perconadev.atlassian.net/browse/PG-1361)：修复 pg_tde 的可迁移性。
* [PG-1380](https://perconadev.atlassian.net/browse/PG-1380)：`pg_tde_is_encrypted()` 支持索引和序列。

### 缺陷修复 {#bugs-fixed}

* [PG-821](https://perconadev.atlassian.net/browse/PG-821)：修复配置复制时 `pg_basebackup` 失败的问题。
* [PG-847](https://perconadev.atlassian.net/browse/PG-847)：修复启用集群校验和后，`pg_basebackup` 和 `pg_checksum` 处理 `pg_tde` 创建的文件时报错的问题。
* [PG-1004](https://perconadev.atlassian.net/browse/PG-1004)：修复 `pg_checksums` 验证 `pg_tde` 表校验和时失败的问题。现在 `pg_checksum` 通过检查关系是否有自定义存储管理器（SMGR）密钥来跳过加密关系。
* [PG-1373](https://perconadev.atlassian.net/browse/PG-1373)：用 `memcpy()` 或 `strlcpy()` 替代 `strncpy()`，避免字符串可能缺少终止符的问题。
* [PG-1378](https://perconadev.atlassian.net/browse/PG-1378)：修复 `ALTER TABLE` 创建的 TOAST 表未加密的问题。
* [PG-1379](https://perconadev.atlassian.net/browse/PG-1379)：修复事件触发器中的序列和修改表处理。
* [PG-1222](https://perconadev.atlassian.net/browse/PG-1222)：修复不同数据库中具有相同 `RelFileNumber` 的关系被混淆的问题。
* [PG-1400](https://perconadev.atlassian.net/browse/PG-1400)：修正帮助中的 pg_tde_change_key_provider 名称。
* [PG-1401](https://perconadev.atlassian.net/browse/PG-1401)：执行 ALTER TABLE SET access method 时，仅根据新的加密设置决定新状态，修复加密状态继承问题。
* [PG-1414](https://perconadev.atlassian.net/browse/PG-1414)：修正配置 WAL 加密时的错误信息，使其引用正确函数。
* [PG-1450](https://perconadev.atlassian.net/browse/PG-1450)：重复调用 `pg_tde_delete_key_provider()` 时忽略已删除记录，修正函数行为。
* [PG-1451](https://perconadev.atlassian.net/browse/PG-1451)：修复创建未加密表时仍反复报告无法获取主密钥的问题。在事件触发器开始函数及文件创建时检查当前事务 ID；如果设置事件触发器数据期间事务发生变化，就重置触发器。
* [PG-1473](https://perconadev.atlassian.net/browse/PG-1473)：仅允许具备密钥查看权限的用户执行 `pg_tde_verify_principal_key()` 和 `pg_tde_verify_global_principal_key()`。
* [PG-1474](https://perconadev.atlassian.net/browse/PG-1474)：在 Vault/KMIP 获取函数中设置密钥名称，修复重新指定到同名提供商时主密钥引用损坏的问题。
* [PG-1476](https://perconadev.atlassian.net/browse/PG-1476)：数据库只有一个默认密钥时，为 WAL 创建新的主密钥，修复启用 WAL 加密后服务器无法启动的问题。
* [PG-1479](https://perconadev.atlassian.net/browse/PG-1479)、[PG-1480](https://perconadev.atlassian.net/browse/PG-1480)：修正默认密钥轮换的参数顺序，解决修改全局提供商并重启后无法访问数据的问题。
* [PG-1489](https://perconadev.atlassian.net/browse/PG-1489)：在副本服务器创建 `pg_tde` 目录，修复密钥和提供商配置的复制。
