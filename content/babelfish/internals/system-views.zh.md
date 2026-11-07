---
title: Babelfish 系统视图
linkTitle: 系统视图
description: 查阅 sys 模式中兼容 SQL Server 的系统视图。
weight: 50
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/system-views.md
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

## Babelfish 系统视图 {#babelfish-system-views}

应用有时需要访问兼容 Microsoft SQL Server 的系统视图或服务器端函数才能正常工作，图形用户界面尤其如此。一些应用也必须通过系统视图收集数据库信息才能完成工作。

因此，支持系统视图十分重要。本文记录的可用视图如下：

- `sys.all_columns`
- `sys.all_objects`
- `sys.all_views`
- `sys.columns`
- `sys.databases`
- `sys.foreign_key_columns`
- `sys.foreign_keys`
- `sys.identity_columns`
- `sys.indexes`
- `sys.key_constraints`
- `sys.objects`
- `sys.pg_namespace_ext`
- `sys.procedures`
- `sys.schemas`
- `sys.server_principals`
- `sys.sp_columns_100_view`
- `sys.sp_tables_view`
- `sys.spt_columns_view_managed`
- `sys.spt_tablecollations_view`
- `sys.sql_modules`
- `sys.syscharsets`
- `sys.sysdatabases`
- `sys.sysforeignkeys`
- `sys.sysindexes`
- `sys.sysobjects`
- `sys.sysprocesses`
- `sys.system_objects`
- `sys.tables`
- `sys.types`
- `sys.views`

这些视图的内容和结构会在技术允许的范围内尽可能兼容 Microsoft SQL Server。详细功能说明见 [Microsoft 文档](https://docs.microsoft.com/en-us/sql/relational-databases/system-catalog-views/object-catalog-views-transact-sql?view=sql-server-ver15)。
