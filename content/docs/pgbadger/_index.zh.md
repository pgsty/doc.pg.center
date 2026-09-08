---
title: "pgBadger 13.2 中文文档"
linkTitle: pgBadger
weight: 40
description: "快速分析 PostgreSQL 与 PgBouncer 日志，生成完整且可独立浏览的报告"
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [概念]
aliases: [/docs/pgbadger/documentation/, /pgbadger/]
upstream_source: pgbadger
upstream_link: "https://github.com/darold/pgbadger"
cascade:
  upstream_source: pgbadger
  type: docs
  module: [PGBADGER]
---

![pgBadger 标志](/img/docs/pgbadger/logo.png "pgBadger")

**pgBadger** 是一款使用 Perl 编写的高性能独立 PostgreSQL 日志分析器。它可以读取 PostgreSQL 或 PgBouncer 日志，并生成 HTML、文本、二进制、JSON 或原始 CSV 输出。HTML 报告自带全部资源，图表可交互、缩放并保存为 PNG，只需浏览器即可查看。

## 为什么使用 pgBadger {#why-pgbadger}

pgBadger 面向大规模日志与日常运维场景设计：

- 单个 Perl 程序，不强制依赖非核心 Perl 模块；
- 自动识别 `stderr`、`syslog`、`csvlog`、`jsonlog`、RDS、Cloud SQL、logplex、Redshift 与 PgBouncer 日志；
- 可读取本地文件、标准输入、SSH 远程文件，以及 HTTP、FTP 或 SFTP URL；
- 支持 gzip、bzip2、lz4、xz、zip 与 zstd 压缩输入；
- 可并行分析一个大文件，或同时处理多个小文件；
- 自动生成每日、每周报告，并按需生成月度累计报告；
- 可按时间、数据库、用户、客户端、应用、进程、会话和查询模式过滤。

## 报告包含什么 {#report-coverage}

PostgreSQL 报告覆盖：

- 整体活动与查询统计；
- 最慢、最频繁、总耗时最高、等待与被取消的查询；
- 临时文件、检查点、锁、会话与连接；
- 按表统计的 autovacuum 与 autoanalyze 活动；
- 按严重级别和类别汇总的错误与事件；
- 按数据库、用户、客户端、应用与语句类型展示的分布。

分析 PgBouncer 日志时，还会生成吞吐量、平均查询耗时、并发会话、连接与会话分布、保留连接池使用情况，以及高频错误/事件报告。

## 文档阅读顺序 {#documentation-map}

可以按以下顺序阅读，也可以从侧边栏直接进入所需主题：

1. [下载并安装](/zh/docs/pgbadger/download/) pgBadger 与可选模块。
2. 查阅完整的[命令行参考](/zh/docs/pgbadger/command-line/)。
3. 配置带有可解析前缀的 [PostgreSQL 日志](/zh/docs/pgbadger/postgresql-logging/)。
4. 为日志规模选择合适的[并行处理](/zh/docs/pgbadger/parallel-processing/)模式。
5. 安全构建[增量报告](/zh/docs/pgbadger/incremental-reports/)。
6. 选择[输出格式](/zh/docs/pgbadger/output-formats/)，并查看[本地示例](/zh/docs/pgbadger/sample-reports/)。
7. 跟踪[版本历史](/zh/docs/pgbadger/releases/)，了解[支持渠道](/zh/docs/pgbadger/support/)与[许可证](/zh/docs/pgbadger/license/)。

## 上游链接 {#upstream-links}

- [项目网站](https://pgbadger.darold.net/)
- [源代码](https://github.com/darold/pgbadger)
- [版本发布](https://github.com/darold/pgbadger/releases)
- [问题追踪](https://github.com/darold/pgbadger/issues)
