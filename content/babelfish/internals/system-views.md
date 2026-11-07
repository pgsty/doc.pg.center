---
title: Babelfish system views
linkTitle: System views
description: SQL Server-compatible system views exposed through the sys schema.
weight: 50
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/system-views.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Babelfish system views {#babelfish-system-views}

Once in a while, an application has to access an Microsoft SQL Server-compatible system view
or a server side function to
work properly. This is especially true for graphical user interfaces. However,
accessing an Microsoft SQL Server-compatible system view is also necessary for some applications
which have to collect information from the database to function properly.

Providing support for system views is therefore important. The following views
are currently available:

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

The content and the structure of these views are as compatible with Microsoft SQL Server as
technically possible. If you want to find out more check out the [Microsoft
documentation](https://docs.microsoft.com/en-us/sql/relational-databases/system-catalog-views/object-catalog-views-transact-sql?view=sql-server-ver15)
describing this functionality.
