---
title: Babelfish for PostgreSQL 文档
linkTitle: 项目概览
description: 了解 Babelfish 的用途、五个组件与贡献方式。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_docs/index.md
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

## Babelfish for PostgreSQL 文档 {#babelfish-for-postgresql-documentation}

本站收录 [Babelfish for PostgreSQL](/zh/babelfish/) 的技术文档。该开源项目采用 [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) 和 [PostgreSQL](https://www.postgresql.org/about/licence/) 许可证，为 PostgreSQL 增加兼容 Microsoft SQL Server 的端点。借助 Babelfish，PostgreSQL 能够理解 SQL Server 专有的 SQL 方言 T-SQL，并支持 TDS 通信协议。因此，原本为 SQL Server 编写的应用，有机会只做少量代码修改、无需更换数据库驱动，便可在 PostgreSQL 上运行。

[开始安装](/zh/babelfish/installation/compiling-babelfish-from-source/)

---

## 为什么使用 Babelfish for PostgreSQL？ {#why-use-babelfish-for-postgresql}

Babelfish 可能适合以下场景：

- 将兼容 SQL Server 的源代码迁移到基于开源软件的数据库。
- 迁离不提供源代码的专有或遗留应用。

Babelfish 的功能由五个组件提供：

| 组件 | 用途 |
| --- | --- |
| [Babelfish 服务器补丁](https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish) | 为 PostgreSQL 提供 Babelfish 所需的钩子。 |
| [Babelfish TDS 扩展](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_tds) | 提供使用 TDS（SQL Server）网络协议的第二个端点。 |
| [Babelfish 语言扩展](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_tsql) | 提供兼容 T-SQL 的过程语言，使用 ANTLR 解析器。 |
| [Babelfish Money 类型](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_money) | 支持 SQL Server 的 money 类型，是开源 fixed-decimal 扩展的变体。 |
| [Babelfish Common](https://github.com/babelfish-for-postgresql/babelfish_extensions/tree/BABEL_1_0_0/contrib/babelfishpg_common) | 支持 SQL Server 的各种数据类型。 |

组件详情见[软件架构](/zh/babelfish/internals/software-architecture/)。

## 参与项目 {#get-involved}

项目欢迎关于问题、缺陷修复、新功能、插件和文档的贡献与反馈。参与方式见[贡献指南](/zh/babelfish/contributing/)。

所有组件均在 [GitHub](https://github.com/babelfish-for-postgresql) 上提供，采用 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0.html) 和 [PostgreSQL 许可证](https://www.postgresql.org/about/licence/)。感谢 PostgreSQL 团队以及 [Babelfish 项目贡献者](/zh/babelfish/site/contributors/)。
