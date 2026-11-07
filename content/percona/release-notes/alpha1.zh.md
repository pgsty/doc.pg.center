---
title: Alpha 1（2024-03-28）
linkTitle: Alpha 1
description: pg_tde Alpha 1 历史版本：主密钥轮换、按数据库加密和动态 keyring 配置。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/release-notes/alpha1.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 930
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

扩展 Alpha1 版本引入以下主要功能：

* 支持轮换数据加密所用主密钥，减少长期暴露于潜在攻击的风险，并帮助满足 GDPR、HIPAA 和 PCI DSS 等安全标准。
* 支持为不同数据库设置不同加密配置，例如对部分数据库中特定表使用不同密钥，同时让其他表保持未加密。
* Keyring 配置的多项改进：

    * 每个数据库可以单独配置 keyring。
    * 可以动态修改配置，无需重启服务器。
    * 配置从配置文件改为分别保存在各数据库的目录中。
    * 可以从外部来源（文件或 HTTP(S) 请求）读取 keyring 参数，避免将秘密保存在未加密目录中。

## 改进 {#improvements}

* 仓库和 Docker 镜像从 `postgres-tde-ext` 重命名为 `pg_tde`，扩展名称不变。
* 修改数据和内部密钥的初始化向量（IV）计算方式。

## 缺陷修复 {#bugs-fixed}

* 修复 TOAST 相关崩溃。
* 修复 DELETE 语句引发的崩溃。
* 修复性能问题。
* 修复 `pg_tde` 向 Vault 服务器发送大量返回 404 的请求。
* 修复与旧版 OpenSSL 的兼容性。
* 修复与旧版 Curl 的兼容性。
