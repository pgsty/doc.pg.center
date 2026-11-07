---
title: Beta 2（2024-12-16）
linkTitle: Beta 2
description: pg_tde Beta 2 历史版本：tde_heap、索引加密、全局 WAL 加密和 KMIP 支持。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/beta2.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 910
upstream_source: percona
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


Percona 提供的 `pg_tde` 扩展为 PostgreSQL 增加[透明数据加密（TDE）](/zh/percona/index/about-tde/)，帮助保护敏感的静态数据。

[开始使用](/zh/percona/install/)

> [!IMPORTANT]
>
> 此版本的 Percona 透明数据加密扩展**尚不建议用于生产环境**。欢迎测试并[提供反馈](https://forums.percona.com/c/postgresql/pg-tde-transparent-data-encryption-tde/82)，帮助改进产品，使其更快达到生产可用状态。

## 版本亮点 {#release-highlights}

本版本为不同数据库提供两种 `pg_tde`：

* PostgreSQL 社区版仅提供 `tde_heap_basic` 访问方法，支持表加密和加密表数据的 WAL 加密，索引数据仍不加密。
* Percona Server for PostgreSQL 版本提供 `tde_heap` 访问方法，可以加密加密表的索引数据，提高敏感数据安全性。为向后兼容，也保留 `tde_heap_basic`。

## 变更日志 {#changelog}

Beta 2 引入以下功能和改进：

### 新功能 {#new-features}

* 增加 `tde_heap` 访问方法，支持加密表的索引加密和全局 WAL 数据加密。使用它必须安装 Percona Server for PostgreSQL，详见[安装指南](/zh/percona/install/)。
* 增加事件触发器，识别加密表上的索引创建操作，并将索引保存在自定义存储中。
* 支持通过 [OASIS 密钥管理互操作协议（KMIP）](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html)安全传输密钥。KMIP 实现已使用 PyKMIP 服务器和 HashiCorp Vault Enterprise KMIP Secrets Engine 测试。

### 改进 {#improvements}

* WAL 加密改进：

    * 增加全局密钥，用于加密全局空间的 WAL 数据。
    * 增加 WAL 密钥管理。

* Keyring 改进：

    * 重命名函数，使名称明确反映主密钥管理用途。
    * 改进跨数据库和全局空间的 keyring 提供商管理。
    * Keyring 配置改用通用 JSON API，简化代码处理，并允许 `pg_waldump` 等前端工具读取相关代码，改善调试。

* `pg_tde_is_encrypted` 支持 `pg_tde_is_encrypted('schema.table');` 形式的自定义模式。
* 内部 TDE 文件由数据库目录迁移到统一的 `$PGDATA/pg_tde`。
* 改进未将 `pg_tde` 加入 `shared_preload_libraries` 时的错误报告。
* 改进 `tde_heap_basic` 顺序读取的内存使用。
* 改进 `tde_heap_basic` 的 select 语句处理。
* 为部分命令行工具增加加密支持。

### 缺陷修复 {#bugs-fixed}

* 修复 `tde_heap_basic` 和 TOAST 记录相关的多个问题。
* 修复多处内存泄漏。
