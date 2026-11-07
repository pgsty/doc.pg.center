---
title: Babelfish 兼容性
linkTitle: 早期兼容性表
description: 保留未发布设计资料中的早期兼容性记录，不代表当前支持程度。
weight: 10
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_architecture/compatibility.md
upstream_ref: main @ f468c5ed3d38
translation_notice: en
upstream_modified: true
translation_status: complete
translation_credit: PGSTY 文档项目
upstream_notice: /zh/babelfish/site/attribution/
upstream_license: LicenseRef-Babelfish-Website-ZH
---



> [!WARNING] 历史设计资料
> 此文件来自上游源码中未发布为文档栏目的一组早期设计资料，保留用于研究项目历史，不代表当前功能支持。当前说明见 [GitHub Wiki](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki)。中文翻译：PGSTY 文档项目。

## Babelfish 兼容性 {#babelfish-compatibility}

## SQL Server 与 PostgreSQL 之间的兼容性 {#compatibility-between-sql-server-and-postgresql}

Babelfish 通过直接在 PostgreSQL 中实现 SQL Server 的数据类型和函数来提供兼容性，并支持相同的线上协议，使 SQL Server 应用可以透明地与 PostgreSQL 通信。因此，可以继续使用熟悉的 SQL Server 查询与开发工具。Babelfish 兼容 SQL Server Management Studio（SSMS）、T-SQL 方言和 SQL Server 数据库驱动。

原文所述版本只支持 Microsoft SQL Server 的数据库引擎组件，不支持 SQL Server Integration Services、Business Intelligence（BI）、Reporting Services 或 Analysis Services 等其他组件。

下表记录 SQL Server 数据库引擎的部分功能，以及当时 Babelfish 的行为差异。

| SQL Server 功能 | SQL Server 标准行为 | Babelfish 行为差异 |
| --- | --- | --- |
| 应用程序角色 | 通过 `CREATE APPLICATION ROLE` 和 `sp_setapprole` 设置。 | 当时不支持。 |
| COMPATIBILITY_LEVEL | 使用 `COMPATIBILITY_LEVEL` 设置向后兼容级别。 | 接受但忽略 `ALTER DATABASE... SET COMPATIBILITY LEVEL`。 |
| `sysdatabases.cmptlevel` | 原文记为始终为 NULL。 | 接受但忽略 `ALTER DATABASE... SET COMPATIBILITY LEVEL`。 |
| 提示 | 支持表提示、查询提示和连接提示。 | 接受但忽略。 |
| 程序集模块与 CLR 例程 | 原文在此列记为不支持程序集及 CLR 例程（`CREATE ASSEMBLY`）。 | 当时不支持。 |
| 备份与恢复 | | PostgreSQL 数据库快照与 SQL Server 备份文件不兼容，备份和恢复的粒度也可能不同。 |
| `bcp`、批量复制、BULK INSERT | `bcp` 是常用导入导出工具。导出时按格式选项写入文件；导入时使用批量复制 API，直接把行装入 SQL Server 数据页，而不使用 `SQL INSERT`。 | 当时不支持。`BULK INSERT` 使用相同 API 从文件载入表，因此也不支持。此限制还影响使用该 API 的 ETL 等第三方工具。 |
| 未指定别名时的空列名 | 向客户端返回结果集时允许空列名，例如列为表达式、且未指定别名时。 | `sqlcmd` 返回空列名，而 PostgreSQL `psql` 返回自动生成的列名。 |
| 标识符大小写敏感性 | 默认不区分大小写，`MyTable` 与 `MYTABLE` 指向同一对象；也可以配置为区分大小写，使两者代表不同对象。 | 原文所述 Babelfish 只支持不区分大小写的标识符，即使源 SQL Server 区分大小写，也会把两者视为同一对象。 |
| 列默认值 | 可以通过 `ALTER TABLE ADD CONSTRAINT...DEFAULT...FOR...` 为默认值指定约束名，并通过 `ALTER TABLE...DROP CONSTRAINT...` 删除。 | PostgreSQL 的列默认值不关联约束名，因此会忽略该名称。删除默认值应使用 `ALTER TABLE...ALTER COLUMN..DROP DEFAULT...`。 |
| 公共语言运行时（CLR） | 支持 Microsoft CLR 过程、函数和触发器。 | 当时不支持。 |
| 约束 | 可通过 `ALTER TABLE...[NO]CHECK CONSTRAINT...` 启用或禁用单个约束。 | PostgreSQL 不支持这一行为；忽略语句并给出警告。 |
| 包含的数据库 | 登录在数据库级而非服务器级认证。 | 当时不支持。 |
| 数据加密 | 原文举出 `CREATE DATABASE ENCRYPTION KEY`（TDE）整库加密，以及 `ENCRYPTBYKEY`、`CREATE SYMMETRIC KEY` 等细粒度加密。 | 当时不支持。 |
| IDENTITY 列 | 支持 `tinyint`、`smallint`、`int`、`bigint`、`numeric`、`decimal`；后两种类型精度最高 38。 | PostgreSQL 的 `numeric`、`decimal` 标识列精度最高 19。 |
| 超过 63 字符的标识符 | 最长 128 字符。 | 最长 63 字符。Babelfish 将超长名称转换为包含原名哈希的名称。T-SQL 使用原名，PostgreSQL 访问使用转换后的名称。 |
| 语言定制 | 错误消息、星期和月份名称可以使用非默认语言。 | 原文所述版本只支持英语错误消息和日期名称。 |
| `NEWSEQUENTIALID()` | 生成保证大于此前一组 GUID 的值。 | 无法保证更大，只会像 `NEWID()` 一样生成新 GUID。 |
| 过程或函数参数上限 | 最多 2100 个参数。 | 最多 100 个参数。 |
| 远程对象访问 | 可以访问远程服务器上的表、视图和过程。 | 当时不支持。 |
| `ROWGUIDCOL` | | 忽略；引用 `$GUIDGOL` 的查询会产生语法错误（拼写保留原文）。 |
| 行级安全 | | 当时不支持通过 `CREATE SECURITY POLICY` 和内联表值函数实现的行级安全。 |
| `SEQUENCE` 对象 | 支持 `tinyint`、`smallint`、`int`、`bigint`、`numeric`、`decimal`；后两者精度最高 38。 | PostgreSQL 序列中的 `numeric`、`decimal` 精度最高 19。 |
| 索引和约束的 `CLUSTERED`、`UNCLUSTERED` 关键字 | | 当时不支持，忽略这些关键字。Babelfish 不支持由索引键决定行物理存储顺序的结构。聚簇索引会影响查询计划和性能，具体影响较复杂。 |
| 索引和约束的 `FILLFACTOR` | 与 SQL Server 特定的数据存储有关。 | 忽略。 |
| `NONCLUSTERED` | SQL Server 使用此关键字。 | 忽略；PostgreSQL 支持堆结构。 |
| `NOT FOR REPLICATION` | 与 SQL Server 特定的数据存储有关。 | 忽略。 |
| `ON` 文件组 | `CREATE TABLE` 和 `CREATE INDEX` 支持通过 `ON` 文件组指定存储位置。 | 与 PostgreSQL 无关，因此忽略。 |
| `SPARSE` | 与 SQL Server 特定的数据存储有关。 | 忽略。 |
| `TEXTIMAGE_ON` 文件组 | `CREATE TABLE` 和 `CREATE INDEX` 支持这一存储位置子句。 | 与 PostgreSQL 无关，因此忽略。 |
| `USE` 数据库名 | | 原文记为当时不支持。 |
| `DESC` 排序 | `UNIQUE` 和 `PRIMARY KEY` 约束可指定列按 `DESC` 排序，有助于优化相关查询。 | 约束不支持 `DESC`，统一采用默认 `ASC`。但显式创建的索引支持列按 `DESC` 排序。 |
| 时间精度 | 原文混合描述了 `datetime2` 的 7 位小数精度与 `datetime` 的 3 毫秒舍入：存入的毫秒可能改变。例如 `SELECT CAST('2016-12-26 23:59:59.999' as datetime)` 返回 `2016-12-27 00:00:00.000`。 | PostgreSQL 支持 6 位小数秒，不进行 SQL Server 式的 3 毫秒舍入，原文预计不会产生不良影响。 |
| 事务隔离级别 | 隔离级别不改变保护数据修改的锁：事务始终持有所改数据的排他锁直到结束。对于读取，隔离级别主要规定免受其他事务修改影响的程度。 | |
| 已提交读（read committed） | 使用锁，读取可能被写入阻塞。 | 使用[多版本并发控制](https://www.postgresql.org/docs/current/mvcc.html)（MVCC），读取不阻塞。 |
| 已提交读（启用 `read_committed_snapshot`） | 选项为 `ON` 时使用行版本，读取不阻塞，读者看到每条语句开始时的一致快照。 | 使用[多版本并发控制](https://www.postgresql.org/docs/current/mvcc.html)（MVCC），读取不阻塞。 |
| 未提交读（read uncommitted） | 允许读取未提交数据。 | 接受语法，但内部映射为已提交读。 |
| 可重复读（repeatable read） | 使用锁，并发更新可能导致死锁终止。 | 当时不支持。 |
| 可串行化（serializable） | 使用串行执行顺序。 | 当时不支持。 |
| 快照（snapshot） | 并发更新可能因快照冲突而终止。 | 用可重复读事务实现 SQL Server 快照，提供事务级读取一致性。PostgreSQL 的可重复读相当于快照隔离。 |
| LOGON 和 DDL 触发器 | | 当时不支持。 |
| `@@version` | | 内容与原生 SQL Server 不同。依赖原生格式提取次版本号等信息的代码可能无法正常工作。 |
