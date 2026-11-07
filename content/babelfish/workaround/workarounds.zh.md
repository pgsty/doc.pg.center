---
title: 变通方案列表
linkTitle: 变通方案概览
description: 使用 PostgreSQL 功能替代不受支持的 SQL Server 功能。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_workaround/workarounds_toc.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!NOTE] 文档快照
> 本文译自上游网站，中文翻译由 PGSTY 文档项目整理。上游自 2023 年起将新文档迁至 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)；请结合所用版本的[发行说明](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)核对功能支持。

本节介绍如何用 PostgreSQL 功能替代不受支持的 SQL Server 语法或功能。其他熟悉的 SQL Server 功能，也可以使用 PostgreSQL 工具替代。下表链接到对应的 PostgreSQL 文档：

| SQL Server 功能 | PostgreSQL 功能 |
| --- | --- |
| SQL Server 复制 | [PostgreSQL 复制](https://www.postgresql.org/docs/current/high-availability.html) |
| DBCC CLEANTABLE | [PostgreSQL VACUUM](https://www.postgresql.org/docs/current/routine-vacuuming.html) |
| SQL Profiler | [auto_explain](https://www.postgresql.org/docs/current/auto-explain.html) |

## 变通方案列表 {#workaround-list}

- [动态定义游标](/zh/babelfish/workaround/dynamically-defined-cursor/)
- [重建表索引](/zh/babelfish/workaround/rebuilding-table-indexes/)
