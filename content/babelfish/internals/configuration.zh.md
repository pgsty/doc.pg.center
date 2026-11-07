---
title: 配置参数
linkTitle: 配置参数
description: 逐项查阅 T-SQL 与 TDS 参数、默认值、取值范围和不可修改的设置。
weight: 20
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_internals/configuration.md
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

## Babelfish 配置参数 {#babelfish-configuration-parameters}

可以使用 Babelfish 配置参数调整行为，以满足实际需求。其中一些参数只能在创建集群前修改，另一些则不应修改。

各参数说明如下。

### `babelfishpg_tsql.ansi_defaults` {#babelfishpgtsqlansidefaults}

启用 `ANSI_DEFAULTS` 时，会启用 `ANSI_NULLS`、`ANSI_NULL_DFLT_ON`、`IMPLICIT_TRANSACTIONS`、`ANSI_PADDING`、`QUOTED_IDENTIFIER`、`ANSI_WARNINGS` 和 `CURSOR_CLOSE_ON_COMMIT`。驱动和提供程序会将 `CURSOR_CLOSE_ON_COMMIT` 与 `IMPLICIT_TRANSACTIONS` 设为 `OFF`，因此即使 `ANSI_DEFAULTS` 为 `ON`，建立连接时 `CURSOR_CLOSE_ON_COMMIT` 实际也为 `OFF`。

### `babelfishpg_tsql.ansi_nulls` {#babelfishpgtsqlansinulls}

指定等于（`=`）和不等于（`<>`）比较运算符用于 `NULL` 值时符合 ISO 标准的行为。

### `babelfishpg_tsql.concat_null_yields_null` {#babelfishpgtsqlconcatnullyieldsnull}

启用后，与 `NULL` 值进行连接会得到 `NULL` 结果。

### `babelfishpg_tsql.database_name` {#babelfishpgtsqldatabasename}

预定义的 Babelfish 数据库名，默认为 `babelfish_db`。

### `babelfishpg_tsql.datefirst` {#babelfishpgtsqldatefirst}

用 1 到 7 之间的数字设置一周的第一天。

### `babelfishpg_tsql.default_locale` {#babelfishpgtsqldefaultlocale}

创建新排序规则时使用的默认区域设置，默认为 `en_US`。数据库初始化后不应修改此值。设置此参数需要超级用户权限。

### `babelfishpg_tsql.disable_batch_auto_commit` {#babelfishpgtsqldisablebatchautocommit}

禁用过程中的自动提交，默认为 `false`。

### `babelfishpg_tsql.disable_txn_in_triggers` {#babelfishpgtsqldisabletxnintriggers}

禁用触发器中的事务，默认为 `false`。T-SQL 触发器结束时如果没有活动事务，就会终止。

### `babelfishpg_tsql.fmtonly` {#babelfishpgtsqlfmtonly}

控制与 SQL Server `FMTONLY` 选项相关的兼容行为。

### `babelfishpg_tsql.implicit_transactions` {#babelfishpgtsqlimplicittransactions}

启用隐式事务。此参数设为 `on` 时，如果当前没有运行中的事务，服务器会为符合条件的命令启动隐式事务。

### `babelfishpg_tsql.migration_mode` {#babelfishpgtsqlmigrationmode}

指定是否支持多个 T-SQL 数据库。有效值为 `single-db`、`multi-db` 和 `NULL`（等同于 `single-db`）。详见[单数据库与多数据库部署](/zh/babelfish/installation/single-multiple/)。

数据库初始化后不应修改此参数。

### `babelfishpg_tsql.nocount` {#babelfishpgtsqlnocount}

控制 T-SQL 兼容的 `NOCOUNT` 选项。

### `babelfishpg_tsql.noexec` {#babelfishpgtsqlnoexec}

控制 SQL Server 兼容的 `NOEXEC` 选项。

### `babelfishpg_tsql.quoted_identifier` {#babelfishpgtsqlquotedidentifier}

指示 Babelfish 将双引号字符串解释为带引号的标识符。

### `babelfishpg_tsql.rowcount` {#babelfishpgtsqlrowcount}

指示 Babelfish 在返回指定行数后停止处理查询。

### `babelfishpg_tsql.server_collation_name` {#babelfishpgtsqlservercollationname}

指定默认[服务器排序规则](/zh/babelfish/usage/locales/)的名称，默认为 `sql_latin1_general_cp1_ci_as`。数据库初始化后不应修改此设置。

### `babelfishpg_tsql.showplan_all` {#babelfishpgtsqlshowplanall}

控制 SQL Server 兼容的 `SHOWPLAN_ALL` 选项。

### `babelfishpg_tsql.showplan_text` {#babelfishpgtsqlshowplantext}

控制 SQL Server 兼容的 `SHOWPLAN_TEXT` 选项。

### `babelfishpg_tsql.showplan_xml` {#babelfishpgtsqlshowplanxml}

控制 SQL Server 兼容的 `SHOWPLAN_XML` 选项。

### `babelfishpg_tsql.trace_tree` {#babelfishpgtsqltracetree}

指示 Babelfish 在生成代码之前转储已编译的解析树。

### `babelfishpg_tsql.trace_exec_codes` {#babelfishpgtsqltraceexeccodes}

指示 Babelfish 跟踪迭代执行器的执行代码。

### `babelfishpg_tsql.trace_exec_counts` {#babelfishpgtsqltraceexeccounts}

指示 Babelfish 跟踪迭代执行器的执行次数。

### `babelfishpg_tsql.trace_exec_time` {#babelfishpgtsqltraceexectime}

指示 Babelfish 跟踪迭代执行器的执行时间。

### `babelfishpg_tsql.textsize` {#babelfishpgtsqltextsize}

设置 `TEXTSIZE`。

### `babelfishpg_tsql.version` {#babelfishpgtsqlversion}

设置 `@@VERSION` 函数的输出。

### `babelfishpg_tsql.xact_abort` {#babelfishpgtsqlxactabort}

指示 Babelfish 如何控制发生错误时的事务行为。

### `babelfishpg_tds.default_server_name` {#babelfishpgtdsdefaultservername}

指定预定义的 Babelfish 默认服务器名，默认为 Microsoft SQL Server。

### `babelfishpg_tds.listen_addresses` {#babelfishpgtdslistenaddresses}

设置 TDS 监听的主机名或 IP 地址。

### `babelfishpg_tds.port` {#babelfishpgtdsport}

指定 TDS 协议使用的端口，不是标准 PostgreSQL 端口。有效范围为 1–65535，默认为 1433。

### `babelfishpg_tds.set_db_session_property` {#babelfishpgtdssetdbsessionproperty}

指定 TDS 连接使用的数据库会话属性，即在登录过程中设置 `babelfishpg_tsql.database_name`。未设置 `database_name` 会报错。

### `babelfishpg_tds.tds_debug_log_level` {#babelfishpgtdstdsdebugloglevel}

指定 TDS 调试级别。有效值为 0、1、2、3，其中 0 关闭日志，默认为 1。

### `babelfishpg_tds.tds_default_numeric_precision` {#babelfishpgtdstdsdefaultnumericprecision}

当引擎未指定精度时，设置 TDS 列元数据中发送的 numeric 类型默认精度。有效范围为 1–38，默认为 8。

### `babelfishpg_tds.tds_default_numeric_scale` {#babelfishpgtdstdsdefaultnumericscale}

当引擎未指定小数位数时，设置 TDS 列元数据中发送的 numeric 类型默认小数位数。有效范围为 0–38，默认为 8。

### `babelfishpg_tds.tds_default_packet_size` {#babelfishpgtdstdsdefaultpacketsize}

指定所有接入客户端的默认数据包大小。有效范围为 512–32767，默认为 4096。

### `babelfishpg_tds.tds_default_protocol_version` {#babelfishpgtdstdsdefaultprotocolversion}

指定所有接入客户端的默认 TDS 协议版本。有效值如下：

- TDSv7.0
- TDSv7.1
- TDSv7.1.1
- TDSv7.2
- TDSv7.3A
- TDSv7.3B
- TDSv7.4
- DEFAULT

### `babelfishpg_tds.tds_ssl_encrypt` {#babelfishpgtdstdssslencrypt}

指定 Babelfish 使用的 SSL 加密设置，默认为 `false`。

### `babelfishpg_tds.tds_ssl_max_protocol_version` {#babelfishpgtdstdssslmaxprotocolversion}

设置 TDS 会话使用的最高 SSL/TLS 协议版本，默认为 `TLSv1.2`。有效值如下：

- TLSv1
- TLSv1.1
- TLSv1.2

### `babelfishpg_tds.tds_ssl_min_protocol_version` {#babelfishpgtdstdssslminprotocolversion}

上游原文将此项也描述为 TDS 会话的“最高”SSL/TLS 协议版本（参数名为 `min`），默认值为 `TLSv1`。有效值如下：

- TLSv1
- TLSv1.1
- TLSv1.2

### `babelfishpg_tds.trigger_fault_enabled` {#babelfishpgtdstriggerfaultenabled}

控制故障注入触发器。

### `babelfishpg_tds.unix_socket_directories` {#babelfishpgtdsunixsocketdirectories}

UNIX socket 目录，默认为 `/tmp`。

### `babelfishpg_tds.unix_socket_group` {#babelfishpgtdsunixsocketgroup}

控制 UNIX socket 的组设置。

### `babelfishpg_tds.unix_socket_permissions` {#babelfishpgtdsunixsocketpermissions}

控制 UNIX socket 权限，默认为 `0700`。

## 不应修改的参数 {#parameters-that-should-not-be-modified}

源码中可能出现以下参数，但不应修改：

- `babelfishpg_tsql.allow_antlr_to_unsupported_grammar_for_testing`
- `babelfishpg_tsql.ansi_null_dflt_off`
- `babelfishpg_tsql.ansi_null_dflt_on`
- `babelfishpg_tsql.ansi_padding`
- `babelfishpg_tsql.ansi_warnings`
- `babelfishpg_tsql.arithabort`
- `babelfishpg_tsql.arithignore`
- `babelfishpg_tsql.cursor_close_on_commit`
- `babelfishpg_tsql.disable_internal_savepoint`
- `babelfishpg_tsql.language`
- `babelfishpg_tsql.numeric_roundabort`

以下参数仅用于特定开发用途。不支持以任何方式使用 `babelfishpg_tsql.sql_dialect`，否则可能发生错误、故障或不正确的功能行为：

- `babelfishpg_tsql.sql_dialect`

以下参数计划从源码中移除，也不应修改：

- `babelfishpg_tsql.dump_antlr_query_graph`
- `babelfishpg_tsql.enable_antlr_detailed_log`
