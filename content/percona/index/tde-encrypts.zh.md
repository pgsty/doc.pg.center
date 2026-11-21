---
title: 加密数据范围
linkTitle: 加密范围
description: pg_tde 加密表数据、TOAST、临时表、索引和集群 WAL，但不加密表元数据。
type: docs
translation_notice: en
upstream_link: https://github.com/percona/pg_tde/blob/5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a/documentation/docs/index/tde-encrypts.md
upstream_name: percona/pg_tde documentation
upstream_copyright: 版权所有 © 2024–2025 Percona LLC 及其关联方
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 5dd7a9e4e3599d88546f5de67ff0f4ef3fe51a9a
upstream_modified: true
weight: 160
upstream_source: percona-20261121
---

`pg_tde` 加密以下组成部分：

* 使用该扩展的表中的**用户数据**，包括关联的 TOAST 数据。表元数据（列名、数据类型等）不加密。
* 针对使用该扩展创建的数据表，在查询执行期间创建的**临时表**。
* 整个数据库集群的**预写式日志（WAL）数据**，包括已加密表和未加密表的 WAL 数据。
* 加密表上的**索引**。

[了解表访问方法](/zh/percona/index/table-access-method/)
