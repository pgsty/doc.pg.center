---
title: 恢复加密备份
linkTitle: 恢复加密备份
description: 恢复旧密钥加密的备份时，确保 KMS 中的主密钥仍然可访问。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/how-to/restore-backups.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 560
upstream_source: percona
---

要恢复使用旧密钥创建的加密备份，必须确保该密钥仍保存在密钥管理系统（KMS）中。备份在磁盘上仍为**加密状态**，`pg_tde` 使用正确密钥透明地访问数据。

## pg_tde 如何使用旧密钥加载备份 {#how-pgtde-uses-old-keys-to-load-backups}

* **KMS：** 保存备份时使用的主密钥。
* **加密备份：** 包含使用当时可用密钥加密的数据。
* **当前服务器：** 只要能通过 KMS 访问密钥，`pg_tde` 就会自动加载备份。

表的内部密钥保存在备份中。运行时，`pg_tde` 从配置的 KMS 获取主密钥，用其解密内部密钥，从而访问加密表数据。

> [!NOTE]
> 如果所需密钥被删除或丢失，备份将**无法**读取。
>
> 如果密钥仍存在，但 KMS 配置发生变化，可以使用 [`pg_tde_change_key_provider`](/zh/percona/command-line-tools/pg-tde-change-key-provider/) 更新配置。
>
> 但是，如果密钥已从所有可访问的 KMS 来源中删除，加密备份将**无法恢复**。
