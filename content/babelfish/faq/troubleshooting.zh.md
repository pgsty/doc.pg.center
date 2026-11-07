---
title: Babelfish 故障排查
linkTitle: 故障排查
description: 排查 TDS 连接故障，收集服务器崩溃回溯。
weight: 30
type: docs
upstream_source: babelfish
upstream_link: https://github.com/babelfish-for-postgresql/babelfish_project_website/blob/f468c5ed3d38849502ee924cb3e236357404d14d/_faq/troubleshooting.md
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

## Babelfish 故障排查 {#babelfish-troubleshooting}

本节介绍使用 Babelfish 时常见的问题及可能的解决办法。

### Babelfish 已启动，但无法运行 SQL Server 代码 {#babelfish-starts-but-i-cant-run-sql-server-code}

可能有多种原因。最常见的是，启动 Babelfish 前没有在 `postgresql.conf` 的 `shared_preload_libraries` 中加入所需 TDS 库。原文将库名写作 `babelfish_tds`；请以所用发行包的安装说明为准。如果启动 PostgreSQL 前未更新此参数，处理 SQL Server 命令所需的库便不会加载，Babelfish 也就无法工作。

详细安装和配置方法见[安装页面](/zh/babelfish/installation/compiling-babelfish-from-source/)。

另一种可能是防火墙阻断了 TDS 端口。确保端口 1433 开放、可供客户端连接。可以使用 telnet 检查，下面是成功连接的例子：

```bash
[user@server ~]$ telnet localhost 1433
Trying ::1...
Connected to localhost.
Escape character is '^]'.
whatever message   
Connection closed by foreign host.
```

下面则是连接被拒绝的情况：

```bash
[user@server ~]$ telnet localhost 1433
#Trying ::1...
telnet: connect to address ::1: Connection refused
Trying 127.0.0.1...
telnet: connect to address 127.0.0.1: Connection refused

```

### Babelfish 中断了连接 {#babelfish-aborts-my-connection}

网络故障或 Babelfish 服务器崩溃都可能导致连接意外终止。可以稳定复现的连接丢失往往与崩溃有关。

可以向团队提供数据库崩溃时的回溯信息。[PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Getting_a_stack_trace_of_a_running_PostgreSQL_backend_on_Linux/BSD) 介绍了如何获取回溯以供后续分析。

取得回溯后，[创建 issue](https://github.com/babelfish-for-postgresql/babelfish_extensions/issues)，详细描述崩溃情况并附上回溯。
