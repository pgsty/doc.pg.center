---
title: 使用其他客户端工具
linkTitle: 其他驱动
description: 查阅受支持的 TDS 连接驱动及客户端限制。
weight: 50
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_client/other-tools.md
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

## 使用其他工具 {#using-other-tools}

客户端使用符合 TDS 7.1 或更高版本的连接驱动时，应能够连接 Babelfish，但 Bulk Copy API 除外。

如遇问题，请[向上游反馈](https://github.com/babelfish-for-postgresql/babelfish_extensions/issues)。

### 支持的连接驱动 {#supported-connectivity-drivers}

官方支持以下接口：

- 开放数据库连接（ODBC）。
- OLEDB Provider / MSOLEDBSQL。
- Java 数据库连接（JDBC）8.2.2（`mssql-jdbc-8.2.2`）及更高版本。
- Microsoft SqlClient Data Provider for SQL Server。
- .NET Data Provider for SQL Server。
- SQL Server Native Client 11.0（已废弃）。
- OLEDB Driver / SQLOLEDB（已废弃）。

未来可能增加其他连接驱动。由于 Babelfish 支持 TDS 协议，大多数基于 TDS 的客户端应用应能与其配合使用。
