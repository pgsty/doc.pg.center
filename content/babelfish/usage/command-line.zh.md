---
title: 连接 Babelfish 的客户端工具
linkTitle: 客户端工具
description: 使用 SQL Server 或 PostgreSQL 客户端连接对应端口。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/command-line.md
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

## 使用客户端工具连接 Babelfish {#using-client-tools-to-connect-to-babelfish}

可以使用 SQL Server 客户端连接 Babelfish 的 TDS 端口。在 Windows 上，SQL Server Management Studio（SSMS）和 `sqlcmd` 都是合适的选择；在 Linux 上，可以使用 `sqlcmd`。

其他支持 TDS 协议的客户端也可以使用，但不属于 Babelfish 官方支持的范围，例如 Linux 上的 FreeTDS 命令行工具 `tsql`。

任何 PostgreSQL 客户端都可以连接 Babelfish 的 PostgreSQL 端口。例如，`psql` 和 pgAdmin 都是支持 PostgreSQL 协议、可在 Windows 和 Linux 上运行的开源客户端。
