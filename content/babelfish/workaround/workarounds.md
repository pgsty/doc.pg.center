---
title: Workarounds
linkTitle: Workaround overview
description: PostgreSQL alternatives for unsupported SQL Server features.
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_workaround/workarounds_toc.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

You can use the workarounds in this section to replace unsupported SQL Server syntax or functionality with PostgreSQL functionality or features. Other familiar SQL Server functionality can be replaced by PostgreSQL tools and utilities.  The following table provides links to the PostgreSQL documentation for PostgreSQL features:

| SQL Server feature | PostgreSQL feature | 
| ------- | ------- | 
| SQL Server Replication | [PostgreSQL Replication ](https://www.postgresql.org/docs/current/high-availability.html) |
| DBCC CLEANTABLE | [PostgreSQL VACCUUM utilities](https://www.postgresql.org/docs/current/routine-vacuuming.html) |
| SQL Profiler | [auto_explain ](https://www.postgresql.org/docs/current/auto-explain.html) |



## Workaround List {#workaround-list}

- [Dynamically defined cursors](/babelfish/workaround/dynamically-defined-cursor/)
- [Rebuilding table indexes](/babelfish/workaround/rebuilding-table-indexes/)
