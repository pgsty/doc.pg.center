---
title: Babelfish 如何处理查询
linkTitle: 查询处理
description: 了解 pltsql 解析器如何处理、执行并物化 T-SQL 查询。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/babelfish-query-handling.md
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

## Babelfish 查询处理 {#babelfish-query-handling}

Microsoft SQL Server 与 PostgreSQL 的查询处理方式差异很大。Babelfish 使用协议钩子，并提供相应的软件机制，让你能够调整和影响查询的处理方式。

### 处理查询 {#processing-a-query}

T-SQL 与 PostgreSQL 所用的 SQL 在语法上存在许多差异。为接受 T-SQL 查询，Babelfish 使用随 `pltsql` 扩展一起分发的解析器。

客户端通过 TDS 协议把查询发送给 Babelfish 后，`pltsql` 扩展中的解析器钩子便会解析、分析并执行查询。该扩展还负责把 PostgreSQL 类型正确转换为 TDS 线上传输类型。采用这种方式后，查询的处理、执行及结果物化都由扩展完成，无需扩展 PostgreSQL 的 SQL 解析器，使其理解 T-SQL 及其语义。
