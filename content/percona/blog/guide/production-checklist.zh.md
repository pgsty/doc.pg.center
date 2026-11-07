---
author: PGSTY
title: pg_tde 生产部署检查清单
description: 在生产环境启用 TDE 前，需要完成的安装、密钥托管、WAL、备份和恢复检查。
date: 2026-11-07
tags:
- operations
- security
- backup
translation_notice: false
upstream_link: https://github.com/percona/pg_tde
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
upstream_source: percona
type: docs
---


本文为 PGSTY 基于上游文档整理的导读。


启用加密前，应当把密钥提供商和恢复路径写得和数据库配置一样具体。

## 检查清单 {#checklist}

- 确认 Percona PostgreSQL 与 pg_tde 版本兼容。
- 通过 `shared_preload_libraries` 加载 `pg_tde`，并在需要加密的每个数据库中创建扩展。
- 生产环境使用外部 KMS 或兼容 KMIP 的提供商；keyring 文件只用于开发和测试。
- 创建并验证主密钥，再创建加密表。
- 在新表和已有表的临时副本上测试 `tde_heap`。
- 开启 WAL 加密时，使用 pg_tde 感知的归档和恢复工具。
- 备份提供商配置，并记录服务器读取历史密钥的方式。
- 测试恢复、创建副本、大版本升级和提供商不可用时的处理流程。
- 记录不在加密范围内的对象，包括临时文件和统计信息。

## 相关文档 {#related-documentation}

- [安装 pg_tde](/zh/percona/install/)
- [配置密钥管理](/zh/percona/global-key-provider-configuration/overview/)
- [验证加密](/zh/percona/test/)
- [配置 WAL 加密](/zh/percona/wal-encryption/)
- [了解限制](/zh/percona/index/tde-limitations/)
