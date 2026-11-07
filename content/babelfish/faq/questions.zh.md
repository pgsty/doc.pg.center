---
title: Babelfish 常见问题
linkTitle: 常见问题
description: 解答许可、版本、客户端、兼容性、性能及缺陷报告等问题。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_faq/index.md
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

## Babelfish 常见问题 {#babelfish-frequently-asked-questions}

本页收录关于 Babelfish 及 Microsoft SQL Server 兼容性的常见问题。

## Babelfish 可以免费使用吗？ {#can-we-use-babelfish-for-free}

可以。Babelfish 是开源软件，可按 [Apache 2.0 许可证](https://www.apache.org/licenses/LICENSE-2.0) 和 [PostgreSQL 许可证](https://www.postgresql.org/about/licence/)免费使用。

Babelfish 支持 TDS 7.1 及更高版本。

### 有哪些 Babelfish 版本？ {#which-babelfish-versions-are-available}

完整版本列表见 [GitHub 下载页面](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/releases)。

### 如何查看正在运行的 Babelfish 版本？ {#how-can-i-find-out-which-version-of-babelfish-i-am-running}

连接 TDS 端口，查询 `@@version` 变量：

```sql
1> SELECT @@version;
2> GO
version                                                                                                                                                                                                                                                         
---------------------------------------------------------------------
Babelfish for PostgreSQL with SQL Server Compatibility - 12.0.2000.8
Oct 19 2021 13:21:04
Copyright (c) Amazon Web Services
PostgreSQL 13.4 on x86_64-pc-linux-gnu                                                                                              
(1 rows affected)
```

也可以使用以下命令：

```sh
1> SELECT SERVERPROPERTY('BabelfishVersion')
2> GO
serverproperty
1.0.0
(1 row affected)

1> SELECT SERVERPROPERTY('Babelfish')
2> GO
serverproperty
1
(1 row affected)
```

## 能同时通过 TDS 和 PostgreSQL 协议使用同一数据库吗？ {#can-i-use-a-database-with-the-tds-protocol-and-the-postgresql-protocol-at-the-same-time}

可以。同一数据库可以同时支持 PostgreSQL 语法和 SQL Server（TDS 协议）语法，但请阅读[互操作指南](/zh/babelfish/usage/interoperability/)。

### 哪些 TDS 客户端已知可与 Babelfish 配合使用？ {#which-tds-clients-are-known-to-work-with-babelfish}

以下客户端已知可以使用：

- OLEDB Provider / MSOLEDBSQL。
- OLEDB Driver / SQLOLEDB（已废弃）。
- Ado.NET Entity Framework。
- SQL Server Native Client 11.0（已废弃）。
- 开放数据库连接（ODBC）。
- Java 数据库连接（JDBC）。

FreeTDS 等其他工具也已知可以工作，但不属于官方支持范围。

注意：作为 Microsoft JDBC 驱动替代品的开源 [jTDS 驱动](https://github.com/milesibastos/jTDS/)不受支持。

## Babelfish 可以作为 PostgreSQL 扩展使用吗？ {#can-babelfish-be-used-as-an-extension-for-postgresql}

Babelfish 需要社区版 PostgreSQL 尚未包含的[钩子](/zh/babelfish/internals/postgresql-hooks/)，因此必须使用专门的 PostgreSQL 源码树。详情见[安装指南](/zh/babelfish/installation/compiling-babelfish-from-source/)。

## Microsoft SQL Server 与 Babelfish 的性能有何差异？ {#what-is-the-performance-difference-between-microsoft-sql-server-and-babelfish}

这高度依赖查询类型。有些操作更快，有些更慢，没有适用于所有情况的统一答案。

## Babelfish 支持多少并发用户？ {#how-many-concurrent-users-does-babelfish-support}

并发用户数没有硬性上限，但实际并发查询量受系统 CPU、I/O 等资源限制。

## 可以运行 T-SQL 查询吗？ {#can-i-run-t-sql-queries}

可以。Babelfish 支持大量 T-SQL 语言功能，例如：

```sql
CREATE PROCEDURE [HumanResources].[uspUpdateEmployeePersonalInfo]
    @BusinessEntityID [int], 
    @NationalIDNumber [nvarchar](15), 
    @BirthDate [datetime], 
    @MaritalStatus [nchar](1), 
    @Gender [nchar](1)
WITH EXECUTE AS CALLER
AS $$
BEGIN
    -- SET NOCOUNT ON;

    BEGIN TRY
        UPDATE [HumanResources].[Employee] 
        SET [NationalIDNumber] = @NationalIDNumber 
            ,[BirthDate] = @BirthDate 
            ,[MaritalStatus] = @MaritalStatus 
            ,[Gender] = @Gender 
        WHERE [BusinessEntityID] = @BusinessEntityID;
    END TRY
    BEGIN CATCH
        EXECUTE [dbo].[uspLogError];
    END CATCH;
END; $$ LANGUAGE 'pltsql';
```

## Babelfish 会支持新的 PostgreSQL 版本吗？ {#will-babelfish-be-available-for-new-versions-of-postgresql}

上游持续推动将 [Babelfish 钩子](/zh/babelfish/internals/postgresql-hooks/)纳入 PostgreSQL。在此之前，会在扩展之外单独提供包含全部钩子的代码树，并为后续 PostgreSQL 版本维护这一代码树。

## 如何报告缺陷？ {#how-can-i-report-a-bug}

访问 [GitHub Babelfish Extensions 仓库](https://github.com/babelfish-for-postgresql/babelfish_extensions/issues)，创建问题报告。

请提供复现步骤、软件版本及安装环境的其他相关信息，以便复现并定位原因。如果问题导致崩溃，请尽量附上 [gdb 回溯](https://ftp.gnu.org/old-gnu/Manuals/gdb/html_node/gdb_42.html)。
