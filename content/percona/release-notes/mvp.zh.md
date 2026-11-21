---
title: MVP（2023-12-12）
linkTitle: MVP
description: pg_tde 最初的 MVP：堆表与 TOAST 加密、Vault 和本地 keyring、复制支持。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/release-notes/mvp.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 940
upstream_source: percona-20261121
---

> [!NOTE] 历史版本
> 本页记录发布当时的能力。当前部署要求请查阅[支持的版本](/zh/percona/index/supported-versions/)和[已知限制](/zh/percona/index/tde-limitations/)。


`pg_tde` 的最小可行产品（MVP）版本引入以下功能：

* 加密堆表，包括 TOAST。
* 加密密钥保存在 HashiCorp Vault 服务器或本地 keyring 文件（用于开发）中。
* 通过独立 JSON 配置文件配置密钥存储。
* 支持复制。
