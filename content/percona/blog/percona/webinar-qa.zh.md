---
title: PostgreSQL TDE 线上讲座问答
description: 这篇讲座补充问答讨论了外部密钥托管、表级加密，以及当时 pg_tde 所依赖的 PostgreSQL 补丁。它有助于区分数据加密本身与配套的访问控制、密钥备份和恢复职责。
type: docs
translation_notice: false
date: '2025-08-13'
author: PGSTY
tags:
- Percona
- history
upstream_link: https://github.com/percona/pg_tde/tree/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_source: percona
---


原作者：**Michal Nosek** · 原文发布：**2025-08-13** · 来源：[Percona 博客](https://www.percona.com/blog/webinar-qa-no-more-workarounds-open-source-postgresql-tde-is-here/)。本站导读：PGSTY。

这篇讲座补充问答讨论了外部密钥托管、表级加密，以及当时 pg_tde 所依赖的 PostgreSQL 补丁。它有助于区分数据加密本身与配套的访问控制、密钥备份和恢复职责。

[阅读 Percona 完整原文](https://www.percona.com/blog/webinar-qa-no-more-workarounds-open-source-postgresql-tde-is-here/)。

> [!NOTE] 历史文章
> 本文反映发布当时的状态。当前操作请查阅[对应文档](/zh/percona/global-key-provider-configuration/overview/)及[支持的版本](/zh/percona/index/supported-versions/)。
