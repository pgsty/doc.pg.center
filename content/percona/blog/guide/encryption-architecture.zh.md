---
author: PGSTY
title: pg_tde 如何沿 PostgreSQL 存储路径保持数据加密
description: 从 tde_heap、Storage Manager、内部密钥、主密钥到 WAL 加密，理解 pg_tde 的实际工作路径。
date: 2026-11-07
tags:
- architecture
- encryption
- wal
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/architecture/encryption-architecture.md
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


只有加密真正经过存储路径，保护才有意义。pg_tde 使用 `tde_heap` 标记需要加密的表，再通过 PostgreSQL Storage Manager 在页面落盘前加密、进入缓存前解密。

## 两层密钥结构 {#the-two-key-hierarchy}

每个加密数据文件都有内部密钥；主密钥保护内部密钥，并保存在 keyring 或外部 KMS 中。这样轮换保护密钥时，不必立即重写每个数据页。

## WAL 的位置 {#where-wal-fits}

WAL 加密是集群级设置。WAL 页面使用内部密钥，内部密钥由服务器主密钥保护；WAL 读取端根据密钥元数据决定哪些记录需要解密。

## 对运维的影响 {#operator-consequence}

密钥提供商可用且认证信息正确时，表可以正常读取；提供商或凭据缺失时，读取可能失败。[密钥管理指南](/zh/percona/global-key-provider-configuration/overview/)和[恢复限制](/zh/percona/index/tde-limitations/)应与数据库配置放在同一份运行手册中。
