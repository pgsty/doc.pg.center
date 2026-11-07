---
title: Using other client tools
linkTitle: Other drivers
description: Supported TDS connectivity drivers and client limitations.
weight: 50
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_client/other-tools.md
upstream_ref: main @ f468c5ed3d38
upstream_notice: /babelfish/site/attribution/
---


> [!NOTE] Website documentation snapshot
> Upstream moved new documentation to [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki) in 2023. Check the [release notes](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases) for the version you use; this page preserves the website documentation.

## Using other tools {#using-other-tools}

Client applications that use a connectivity driver compliant with TDS version 7.1 or higher, 
should be able to connect to Babelfish, except for use of the Bulk Copy API. 

Please [report back](https://github.com/babelfish-for-postgresql/babelfish_extensions/issues)
if you face an issue. 

### Supported connectivity drivers {#supported-connectivity-drivers}

The following interfaces are officially supported:

- Open Database Connectivity (ODBC)
- OLEDB Provider/MSOLEDBSQL
- Java Database Connectivity (JDBC) version 8.2.2 (mssql-jdbc-8.2.2) and higher
- Microsoft SqlClient Data Provider for SQL Server
- .NET Data Provider for SQL Server
- SQL Server Native Client 11.0 (deprecated)
- OLEDB Driver/SQLOLEDB (deprecated)

More connectivity drivers might be added in the future.  Since Babelfish supports the TDS 
protocol, most TDS-based client applications are expected to work with Babelfish.
