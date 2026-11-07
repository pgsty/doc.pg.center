---
title: 管理 Babelfish 逃生舱
linkTitle: 逃生舱
description: 配置不受支持语法的处理方式，查阅各项逃生舱的默认值。
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_usage/escape_hatches.md
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

## Babelfish 逃生舱 {#babelfish-escape-hatches}

为了更好地处理可能失败的语句，Babelfish 允许定义“逃生舱”（escape hatch）。逃生舱是用户可调整的开关，用于指定遇到不受支持的功能或语法时 Babelfish 应如何处理。

可以使用 `sp_babelfish_configure` 存储过程查看或修改各个逃生舱的设置：

- 设为 `ignore` 时，Babelfish 会抑制对应语法原本会引发的错误。默认只影响当前会话；附加 `server` 关键字，还可以在集群级持久保存修改。
- 设为 `default` 时，恢复安装时的默认设置。
- 设为 `strict` 时，SQL 代码包含不受支持的语法可能会报错。要抑制这些错误，可以通过 TDS 端口运行以下命令，将所有逃生舱设为 `ignore`：

```none
sp_babelfish_configure '%', 'ignore', 'server', 'default'
```

下表列出逃生舱参数及其默认设置：

| 逃生舱参数 | 说明 | 默认值 |
| --- | --- | --- |
| `babelfishpg_tsql.escape_hatch_checkpoint` | 允许在过程代码中使用 `CHECKPOINT` 语句，但该语句尚未实现。 | ignore |
| `babelfishpg_tsql.escape_hatch_rowversion` | 控制 `ROWVERSION` 与 `TIMESTAMP` 数据类型的行为。 | strict |
| `babelfishpg_tsql.escape_hatch_constraint_name_for_default` | 控制默认约束名称的相关行为。 | ignore |
| `babelfishpg_tsql.escape_hatch_database_misc_options` | 控制 `CREATE DATABASE` 的以下选项：`CONTAINMENT`、`DB_CHAINING`、`TRUSTWORTHY`、`PERSISTENT_LOG_BUFFER`。 | ignore |
| `babelfishpg_tsql.escape_hatch_for_replication` | 控制创建或修改表时 `[NOT] FOR REPLICATION` 子句的行为。 | strict |
| `babelfishpg_tsql.escape_hatch_fulltext` | 控制 `FULLTEXT` 功能，例如 `CREATE/ALTER DATABASE` 中的 `DEFAULT_FULLTEXT_LANGUAG`、`CREATE FULLTEXT INDEX` 和 `sp_fulltext_database`。 | ignore |
| `babelfishpg_tsql.escape_hatch_index_clustering` | 控制索引以及 `PRIMARY KEY`、`UNIQUE` 约束中的 `CLUSTERED` 或 `NONCLUSTERED` 关键字。忽略 `CLUSTERED` 时，仍会创建索引或约束，如同指定了 `NONCLUSTERED`。 | ignore |
| `babelfishpg_tsql.escape_hatch_index_columnstore` | 控制 `COLUMNSTORE` 子句。设为 `ignore` 时，创建普通的 B 树索引。 | strict |
| `babelfishpg_tsql.escape_hatch_ignore_dup_key` | 控制 `CREATE`/`ALTER TABLE` 和 `CREATE INDEX` 的相关行为。设为 `strict` 时抛出错误，设为 `ignore` 时忽略错误。适用于 Babelfish 1.2.0 及以上版本。 | strict |
| `babelfishpg_tsql.escape_hatch_join_hints` | 控制 `JOIN` 运算中的关键字：`LOOP`、`HASH`、`MERGE`、`REMOTE`、`REDUCE`、`REDISTRIBUTE`、`REPLICATE`。 | ignore |
| `babelfishpg_tsql.escape_hatch_language_non_english` | 控制非英语屏幕消息的行为。Babelfish 当时只支持 `us_english` 消息。`SET LANGUAGE` 可以使用包含语言名称的变量，因此只能在运行时判断实际设置的语言。 | strict |
| `babelfishpg_tsql.escape_hatch_login_hashed_password` | `CREATE LOGIN` 和 `ALTER LOGIN` 不支持 `HASHED` 密码。 | strict |
| `babelfishpg_tsql.escape_hatch_login_misc_options` | 处理 `CREATE LOGIN` 和 `ALTER LOGIN` 中其他不支持的选项。 | strict |
| `babelfishpg_tsql.escape_hatch_login_old_password` | `ALTER LOGIN` 不支持 `OLD_PASSWORD` 选项。 | strict |
| `babelfishpg_tsql.escape_hatch_login_password_must_change` | `CREATE LOGIN` 和 `ALTER LOGIN` 不支持 `MUST_CHANGE` 密码选项。 | strict |
| `babelfishpg_tsql.escape_hatch_login_password_unlock` | `CREATE LOGIN` 和 `ALTER LOGIN` 不支持 `UNLOCK` 密码选项。 | strict |
| `babelfishpg_tsql.escape_hatch_nocheck_add_constraint` | 控制约束的 `WITH CHECK` 或 `NOCHECK` 子句。 | strict |
| `babelfishpg_tsql.escape_hatch_nocheck_existing_constraint` | 控制 `FOREIGN KEY` 或 `CHECK` 约束的相关行为。 | strict |
| `babelfishpg_tsql.escape_hatch_query_hints` | 控制查询提示。设为 `ignore` 时，服务器忽略通过 `OPTION (...)` 指定查询处理方式的提示，例如 `SELECT FROM ... OPTION(MERGE JOIN HASH, MAXRECURSION 10))`。 | ignore |
| `babelfishpg_tsql.escape_hatch_rowguidcol_column` | 控制创建或修改表时 `ROWGUIDCOL` 子句的行为。 | strict |
| `babelfishpg_tsql.escape_hatch_schemabinding_function` | 控制 `WITH SCHEMABINDING` 子句。默认忽略 `CREATE` 或 `ALTER FUNCTION` 中指定的该子句。 | ignore |
| `babelfishpg_tsql.escape_hatch_schemabinding_procedure` | 控制 `WITH SCHEMABINDING` 子句。默认忽略 `CREATE` 或 `ALTER PROCEDURE` 中指定的该子句。 | ignore |
| `babelfishpg_tsql.escape_hatch_schemabinding_trigger` | 控制 `WITH SCHEMABINDING` 子句。默认忽略 `CREATE` 或 `ALTER TRIGGER` 中指定的该子句。 | ignore |
| `babelfishpg_tsql.escape_hatch_schemabinding_view` | 控制 `WITH SCHEMABINDING` 子句。默认忽略 `CREATE` 或 `ALTER VIEW` 中指定的该子句。 | ignore |
| `babelfishpg_tsql.escape_hatch_session_settings` | 控制不受支持的会话级 `SET` 语句。 | ignore |
| `babelfishpg_tsql.escape_hatch_showplan_all` | 控制 `SET SHOWPLAN_ALL` 和 `SET STATISTICS PROFILE`。设为 `ignore` 时，两者的行为分别与 `SET BABELFISH_SHOWPLAN_ALL` 和 `SET BABELFISH_STATISTICS PROFILE` 相同；设为 `strict` 时，两者被静默忽略。查询计划按 PostgreSQL 风格显示，而不是 SQL Server 风格。更多信息见[查看查询计划（原链接已迁移）](https://github.com/babelfish-for-postgresql/babelfish-for-postgresql/wiki/Reviewing-Babelfish-query-performance)。 | strict |
| `babelfishpg_tsql.escape_hatch_storage_on_partition` | 控制定义分区时的 `ON partition_scheme` 列子句。原文所述版本尚未实现分区。 | strict |
| `babelfishpg_tsql.escape_hatch_storage_options` | 控制 `DATABASE`、`TABLE` 和 `INDEX` 的 `CREATE`/`ALTER` 语句中的存储选项，包括用于指定表、索引、约束及数据库存储位置（分区、文件组）的 `(LOG) ON`、`TEXTIMAGE_ON`、`FILESTREAM_ON` 子句。该设置适用于所有这些子句，包括 `ON PRIMARY` 和 `ON DEFAULT`；例外是通过 `ON partition_scheme (column)` 为表或索引指定分区。设为 `ignore` 时，`CREATE DATABASE` 的 `ON` 子句不会报错，`CREATE INDEX` 的 `SORT_IN_TEMPDB`、`DROP_EXISTING` 和 `ONLINE` 选项也不会报错。 | ignore |
| `babelfishpg_tsql.escape_hatch_table_hints` | 控制通过 `WITH (...)` 子句指定的表提示。 | ignore |
| `babelfishpg_tsql.escape_hatch_unique_constraint` | 原文描述为控制不受支持的会话级 `SET` 语句。设为 `ignore` 时，允许在定义了 `UNIQUE` 索引或约束的列中使用空值。从 3.6.0 及之后版本、4.2.0 及之后版本起废弃。 | strict |
