---
title: pg_tde 2.1.2（2026-03-02）
linkTitle: 2.1.2
description: pg_tde 2.1.2：Vault/OpenBao 挂载验证改进、命令行工具更新和历史已知问题。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/release-notes-v2.1.2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 840
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

## 版本亮点 {#release-highlights}

### 文档更新 {#documentation-updates}

* 重新组织[架构文档](/zh/percona/architecture/overview/)，拆分为更小、更聚焦的小节，提高可读性。
* [技术参考概览](/zh/percona/advanced-topics/tech-reference/)使用便于浏览的卡片，帮助快速进入主题。
* 新增独立的[使用参考](/zh/percona/advanced-topics/usage-guide/)，介绍主要 `pg_tde` 操作。

## 已知问题 {#known-issues}

* `pg_rewind` 和 `pg_tde_rewind`

    在使用 `pg_tde` 的集群中，对已经分叉的节点执行 `pg_rewind` 或 `pg_tde_rewind`，可能因集群间内部加密密钥不同而损坏表或索引。

    查询可能报错：

    ```bash
    ERROR: invalid page in block 0 of relation "base/..."
    ```

    这是已知问题。

    详见 [pg_tde 的限制](/zh/percona/index/tde-limitations/)。

* 启用 `pg_tde` 时，目前不支持 `pg_upgrade`。

    使用 `pg_tde` 的 PostgreSQL 集群目前不能通过 `pg_upgrade` 升级。

* `pg_tde_basebackup` 运行期间，不要创建、修改或轮换全局密钥提供商及其密钥。这可能导致从备份初始化的备库或集群在 WAL 重放时失败，并损坏加密数据（表、索引和其他关系）。

* 使用 `--wal-method=fetch` 运行 `pg_tde_basebackup` 会产生警告。

    这是预期行为，将在后续版本处理。

* ARM64 架构上的 Rocky Linux 8 默认 `mlock` 限制等于内存页大小，为 64 Kb。父进程已经达到内存上限，导致使用 `pg_tde` 的子进程无法再分配一个内存页。

    为避免这一问题，可以将 `mlock` 限制提高到至少两倍内存页大小：

    * 使用 `ulimit -l <value>` 临时修改当前会话。
    * 在 `/etc/security/limits.conf` 中设置新的硬限制，需要超级用户权限。

    请谨慎调整，因为这也会影响系统中的其他进程。

## 变更日志 {#changelog}

### 改进 {#improvements}

* [PG-2088](https://perconadev.atlassian.net/browse/PG-2088)、[PG-2179](https://perconadev.atlassian.net/browse/PG-2179)：改进 Vault/OpenBao KV v2 挂载点验证。令牌无权访问挂载元数据端点时，扩展不再失败；仅具备必要 KV v2 读写权限的令牌也可正常使用。

### 缺陷修复 {#bugs-fixed}

* 更新 `pg_tde` 命令行工具，合入 PostgreSQL 18.2 和 17.8 的上游缺陷修复与稳定性改进。
