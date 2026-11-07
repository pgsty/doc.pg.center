---
title: 什么是透明数据加密
linkTitle: 什么是 TDE
description: 了解透明数据加密如何保护静态数据，以及 pg_tde 的优势与限制。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/index/about-tde.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 130
upstream_source: percona
---

透明数据加密（TDE）保护静态数据：即使底层存储遭到入侵，没有正确的解密密钥，数据仍然无法读取。这对处理敏感、受监管或高价值信息的环境尤为关键。

加密过程在后台透明运行，对数据库操作的影响很小。

通过以下链接了解 `pg_tde` 如何保护 PostgreSQL 部署：

[了解 pg_tde 的优势](/zh/percona/index/how-tde-helps/)
[了解 pg_tde 的限制](/zh/percona/index/tde-limitations/)
[查看完整功能列表](/zh/percona/features/)
[开始安装](/zh/percona/install/)
