---
title: "从 Web 服务加载数据"
description: "在 Apache Cloudberry 中，要从 Web 服务或任何可通过命令行访问的来源加载数据，可以创建外部 Web 表。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-from-web-services.md"
---

支持的数据格式为 `TEXT` 和 `CSV`。

外部 Web 表允许 Apache Cloudberry 将动态数据源作为常规数据库表处理。由于 Web 表数据可能在查询运行期间发生变化，因此无法重新扫描这些数据。

`CREATE EXTERNAL WEB TABLE` 创建 Web 表定义。你可以定义基于命令或基于 URL 的外部 Web 表。这两种定义形式不同，请勿混用。

## 基于命令的外部 Web 表 {#command-based-external-web-tables}

基于命令的 Web 表以 Shell 命令或脚本的输出作为表数据。在 `CREATE EXTERNAL WEB TABLE` 的 `EXECUTE` 子句中指定命令。数据的状态以命令运行时为准。`EXECUTE` 子句会在指定的 Coordinator 和/或 Segment 主机上运行 Shell 命令或脚本。该命令或脚本必须位于 `EXECUTE` 子句所定义的相应主机上。

默认情况下，当活动 Segment 有输出行需要处理时，命令会在 Segment 主机上运行。例如，如果每个 Segment 主机运行 4 个有输出行需要处理的主 Segment 实例，则命令会在每个 Segment 主机上运行 4 次。你可以选择限制运行 Web 表命令的 Segment 实例数量。Web 表定义的 `ON` 子句中列出的所有 Segment 都会并行运行该命令。

你在外部表定义中指定的命令从数据库中运行，无法访问 `.bashrc` 或 `.profile` 中的环境变量。请在 `EXECUTE` 子句中设置环境变量。例如：

```sql
=# CREATE EXTERNAL WEB TABLE output (output text)
    EXECUTE 'PATH=/home/gpadmin/programs; export PATH; myprogram.sh' 
    FORMAT 'TEXT';
```

脚本必须可由 `gpadmin` 用户执行，并且位于 Coordinator 或 Segment 主机上的相同位置。

以下命令定义一个运行脚本的 Web 表。该脚本会在有 Segment 需要处理输出行的每个 Segment 主机上运行。

```sql
=# CREATE EXTERNAL WEB TABLE log_output 
    (linenum int, message text) 
    EXECUTE '/var/load_scripts/get_log_data.sh' ON HOST 
    FORMAT 'TEXT' (DELIMITER '|');
```

## 基于 URL 的外部 Web 表 {#url-based-external-web-tables}

基于 URL 的 Web 表使用 HTTP 协议从 Web 服务器访问数据。Web 表数据是动态的，无法重新扫描这些数据。

使用 `http://` 指定 Web 服务器上文件的 `LOCATION`。Web 数据文件必须位于 Apache Cloudberry Segment 主机可以访问的 Web 服务器上。指定的 URL 数量对应于在运行时并行访问 Web 表的 Segment 实例数量。例如，如果向一个具有 8 个主 Segment 的 Apache Cloudberry 系统指定 2 个外部文件，则查询运行时 8 个 Segment 中的 2 个会并行访问 Web 表。

以下示例命令定义一个从多个 URL 获取数据的 Web 表。

```sql
=# CREATE EXTERNAL WEB TABLE ext_expenses (name text, 
  date date, amount float4, category text, description text) 
  LOCATION ( 

  'http://intranet.company.com/expenses/sales/file.csv',
  'http://intranet.company.com/expenses/exec/file.csv',
  'http://intranet.company.com/expenses/finance/file.csv',
  'http://intranet.company.com/expenses/ops/file.csv',
  'http://intranet.company.com/expenses/marketing/file.csv',
  'http://intranet.company.com/expenses/eng/file.csv' 

   )
  FORMAT 'CSV' ( HEADER );
```
