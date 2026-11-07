---
title: Babelfish 的用途
linkTitle: Babelfish 的用途
description: 了解 T-SQL、TDS 协议与 PostgreSQL 双端口访问方式。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/purpose.md
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

Babelfish for PostgreSQL 为 PostgreSQL 数据库增加接收 Microsoft SQL Server 客户端连接的能力。与传统迁移相比，原本为 SQL Server 编写的应用，只需较少代码修改、无需更换数据库驱动，即可直接使用 PostgreSQL。参见[迁移到 Babelfish](/zh/babelfish/usage/migration/)。

Babelfish 为 PostgreSQL 集群提供额外端点，使其理解 SQL Server 的线上协议和常用语句。使用表格数据流（Tabular Data Stream，TDS）协议的客户端可以直接连接 PostgreSQL 上的 TDS 监听端口。Babelfish 支持 TDS 7.1 及更高版本。协议详情见 Microsoft 的 [[MS-TDS]: Tabular Data Stream Protocol](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-tds/b46a581a-39de-4745-b076-ec4dbb7d13ec)。

一个应用可以使用 Babelfish TDS 连接，另一个应用同时使用原生 PostgreSQL 连接，访问同一份数据。客户端端口可以在初始化时指定，也可以之后通过 PostgreSQL 参数调整，参见[配置 Babelfish](/zh/babelfish/internals/configuration/)。

默认端口如下：

- SQL Server 方言：1433。
- PostgreSQL 方言：5432。

Babelfish 运行 Transact-SQL（T-SQL）语言。

### 加入 Babelfish 社区 {#join-the-babelfish-community}

欢迎加入社区，一起改进项目，参见[参与贡献](/zh/babelfish/contributing/)。
