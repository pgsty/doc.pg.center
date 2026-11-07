---
title: 发布候选版 2
linkTitle: RC 2
description: pg_tde RC2：提供商权限收紧、Vault WAL 加密、自动 WAL 密钥轮换与完整修复记录。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/rc2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 890
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

本版本提供以下功能和改进：

* **将密钥提供商配置限制为超级用户。**

    数据库所有者不能再直接配置提供商，必须由管理提供商配置的超级用户处理。这一安全改进明确区分用户和管理员的职责。

* **WAL 加密支持 Vault。**

    `pg_tde` 支持通过 Vault keyring 安全存储和管理 WAL 加密密钥。

* **服务器启动时自动生成 WAL 内部密钥。**

    每次服务器启动，都会生成新的内部密钥，用于加密后续 WAL 记录（假定启用了 WAL 加密）。已有 WAL 记录和密钥不变，在不影响历史数据的前提下保证连续性和安全的密钥管理。

* **删除表时正确移除关系级加密密钥。**

    过去，关联表删除后，加密关系密钥仍然保留，可能在映射文件留下孤立条目。现在删除加密表时，也会从密钥映射中移除对应密钥。

* **修复加密分区移入外部表空间时的数据丢失。**

    修复将加密分区表移动到外部表空间时可能丢失数据的问题。

* **新增默认主密钥的查看和验证函数。**

    增加函数，方便查看和验证默认主密钥状态。

* **修复提供商切换不一致导致的 SQL 失败。**

    修复服务器运行期间切换提供商后 SQL 查询可能失败的问题。主密钥分散在多个 keyring 后端时会变得不可访问，触发一次只能使用一个提供商的设计约束。现在 `pg_tde` 在变更提供商时强制一致性，防止密钥状态损坏和查询错误。

## 升级注意事项 {#upgrade-considerations}

由于代码发生重大变化，`pg_tde` RC2 不向后兼容 Beta2，不能直接升级。必须先[卸载](/zh/percona/how-to/uninstall/) Beta2，再[安装](/zh/percona/install/)并配置新的候选发布版本。

## 已知问题 {#known-issues}

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

### 新功能 {#new-features}

* [PG-817](https://perconadev.atlassian.net/browse/PG-817)：为 `pstress` 增加模糊测试，加强验证和健壮性。
* [PG-824](https://perconadev.atlassian.net/browse/PG-824)：确保对 `pg_tde.map`、`pg_tde.dat` 和文件系统密钥提供商文件执行 fsync。
* [PG-830](https://perconadev.atlassian.net/browse/PG-830)：使用 Vault keyring 实现完整 WAL 加密。
* [PG-831](https://perconadev.atlassian.net/browse/PG-831)：测试 WAL 恢复、流复制和逻辑复制兼容性。
* [PG-855](https://perconadev.atlassian.net/browse/PG-855)：增加贡献指南，帮助新开发者参与 pg_tde。
* [PG-938](https://perconadev.atlassian.net/browse/PG-938)：评估使用 `pg_basebackup` 自动验证 pg_tde 备份。
* [PG-962](https://perconadev.atlassian.net/browse/PG-962)：自动化测试 PostgreSQL 重启后的数据完整性。
* [PG-1001](https://perconadev.atlassian.net/browse/PG-1001)：验证临时表加密行为。
* [PG-1099](https://perconadev.atlassian.net/browse/PG-1099)：开发裸机性能基准测试自动化。
* [PG-1289](https://perconadev.atlassian.net/browse/PG-1289)：增加测试用例，验证与不同 PostgreSQL 版本的兼容性。
* [PG-1444](https://perconadev.atlassian.net/browse/PG-1444)：删除表时移除关系级加密密钥。
* [PG-1455](https://perconadev.atlassian.net/browse/PG-1455)：在加密 IV 中引入随机基数，提高安全性。
* [PG-1458](https://perconadev.atlassian.net/browse/PG-1458)：增加默认主密钥的查看与验证函数。
* [PG-1460](https://perconadev.atlassian.net/browse/PG-1460)：服务器启动时自动轮换 WAL 内部密钥。
* [PG-1461](https://perconadev.atlassian.net/browse/PG-1461)：为 WAL 密钥实现随机 IV 初始化。
* [PG-1506](https://perconadev.atlassian.net/browse/PG-1506)：KMIP 提供商配置支持客户端证书参数。

## 改进 {#improvements}

* [PG-826](https://perconadev.atlassian.net/browse/PG-826)：记录使用 pg_tde 加密和解密已有表的方法。
* [PG-827](https://perconadev.atlassian.net/browse/PG-827)：修复 smgr 分支上的 CI 流水线测试。
* [PG-834](https://perconadev.atlassian.net/browse/PG-834)：解决 smgr 分支上 `CREATE ... USING pg_tde` 的问题。
* [PG-1427](https://perconadev.atlassian.net/browse/PG-1427)：测试并修复 KMIP 实现，支持 Thales。
* [PG-1507](https://perconadev.atlassian.net/browse/PG-1507)：在 TDE 事件触发器中处理 ALTER TYPE。
* [PG-1508](https://perconadev.atlassian.net/browse/PG-1508)：修复修改继承表时加密状态不一致的问题。
* [PG-1550](https://perconadev.atlassian.net/browse/PG-1550)：限制数据库所有者创建密钥提供商，提高安全性。
* [PG-1586](https://perconadev.atlassian.net/browse/PG-1586)：验证并修复 KMIP 与 Fortanix HSM 的兼容性。

### 缺陷修复 {#bugs-fixed}

* [PG-1397](https://perconadev.atlassian.net/browse/PG-1397)：修复启用 WAL 加密时复制发生段错误的问题。
* [PG-1413](https://perconadev.atlassian.net/browse/PG-1413)：解决切换加密后 WAL magic number 无效的问题。
* [PG-1416](https://perconadev.atlassian.net/browse/PG-1416)：修复密钥提供商切换不一致导致的 SQL 查询失败。
* [PG-1468](https://perconadev.atlassian.net/browse/PG-1468)：修复密钥轮换后副本无法读取 WAL 的问题。
* [PG-1491](https://perconadev.atlassian.net/browse/PG-1491)：修正 `pg_tde_is_encrypted()` 对分区表的行为。
* [PG-1493](https://perconadev.atlassian.net/browse/PG-1493)：修复加密分区表移入外部表空间时的数据丢失。
* [PG-1503](https://perconadev.atlassian.net/browse/PG-1503)：阻止删除仍与主密钥关联的全局提供商。
* [PG-1504](https://perconadev.atlassian.net/browse/PG-1504)：确保分区 `tde_heap` 表正确继承加密状态。
* [PG-1510](https://perconadev.atlassian.net/browse/PG-1510)：为 PostgreSQL 文件分支使用不同密钥和 IV，避免冲突。
* [PG-1530](https://perconadev.atlassian.net/browse/PG-1530)：修复切换 WAL 加密后无法读取 WAL 的问题。
* [PG-1532](https://perconadev.atlassian.net/browse/PG-1532)：解决 pg_tde 不在默认模式中时重写所属序列报错的问题。
* [PG-1535](https://perconadev.atlassian.net/browse/PG-1535)：防止调用 `pg_tde_principal_key_info()` 导致服务器崩溃。
* [PG-1537](https://perconadev.atlassian.net/browse/PG-1537)：修复面向用户的函数接受 NULL 输入时崩溃的问题。
* [PG-1539](https://perconadev.atlassian.net/browse/PG-1539)：妥善处理主密钥头部验证错误。
* [PG-1540](https://perconadev.atlassian.net/browse/PG-1540)：确保为序列指定正确加密状态。
* [PG-1541](https://perconadev.atlassian.net/browse/PG-1541)：解决密钥轮换后的 WAL 解密失败。
* [PG-1543](https://perconadev.atlassian.net/browse/PG-1543)：修复存在多个服务器密钥时的验证错误。
* [PG-1545](https://perconadev.atlassian.net/browse/PG-1545)：解决执行 `pg_tde_grant_grant_management_to_role()` 报错的问题。
* [PG-1546](https://perconadev.atlassian.net/browse/PG-1546)：修复角色授权函数的错误行为。
* [PG-1551](https://perconadev.atlassian.net/browse/PG-1551)：改进 WAL 存储代码对短读取和错误的处理。
* [PG-1571](https://perconadev.atlassian.net/browse/PG-1571)：修复主密钥损坏或不匹配导致的 WAL 解密失败。
* [PG-1573](https://perconadev.atlassian.net/browse/PG-1573)：防止 WAL 重放期间未持有锁导致崩溃。
* [PG-1574](https://perconadev.atlassian.net/browse/PG-1574)：确保流复制副本能够读取加密 WAL。
* [PG-1576](https://perconadev.atlassian.net/browse/PG-1576)：解决面向用户的函数处理格式错误 JSON 时崩溃的问题。
