---
title: "使用 gpfdist 向 Apache Cloudberry 加载数据"
linkTitle: "使用 gpfdist 加载数据"
description: "要从本地主机文件或可通过内部网络访问的文件加载数据，可以在 `CREATE EXTERNAL TABLE` 语句中使用 `gpfdist` 协议。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-using-gpfdist.md"
---

gpfdist 是一个文件服务器工具，运行在 Apache Cloudberry Coordinator 或 Standby Coordinator 以外的主机上。`gpfdist` 将该主机上某个目录中的文件提供给 Apache Cloudberry Segment。

当 gpfdist 提供外部数据时，Apache Cloudberry 系统中的所有 Segment 都可以并行读写外部表数据。

支持的数据格式包括：

- CSV 和 TXT
- `FORMAT` 子句支持的任意分隔文本格式
<!-- - XML and JSON (requires conversion to text format via YAML configuration file) -->

使用 `gpfdist` 加载数据的一般步骤如下：

1. 在 Apache Cloudberry Coordinator 或 Standby Coordinator 以外的主机上安装 gpfdist。请参阅[安装 gpfdist](#step-1-install-gpfdist)。
2. 在该主机上启动 gpfdist。请参阅[启动和停止 gpfdist](#step-2-start-and-stop-gpfdist)。
3. 使用 `gpfdist` 协议创建外部表。请参阅[结合 gpfdist 和外部表的使用示例](#step-3-use-gpfdist-with-external-tables-to-load-data)。

> [!DETAILS] 关于 gpfdist
> ## 关于 gpfdist {#about-gpfdist}
>
> 使用 gpfdist 之前，你可能需要了解它的工作原理。本节概述 gpfdist 以及如何将其与外部表结合使用。
>
> ### 关于 gpfdist 和外部表 {#about-gpfdist-and-external-tables}
>
> `gpfdist` 文件服务器工具位于 Apache Cloudberry Coordinator 主机以及每个 Segment 主机的 `$GPHOME/bin` 目录中。启动 `gpfdist` 实例时，需要指定监听端口和目录路径，该目录用于存放待读取的文件或写入文件。例如，以下命令在后台运行 `gpfdist`，监听 `8801` 端口，并提供 `/home/gpadmin/external_files` 目录中的文件：
>
> ```shell
> $ gpfdist -p 8801 -d /home/gpadmin/external_files &
> ```
>
> `CREATE EXTERNAL TABLE` 命令的 `LOCATION` 子句将外部表定义关联到一个或多个 `gpfdist` 实例。如果外部表可读，`gpfdist` 服务器会从指定目录的文件中读取数据记录，将它们打包成数据块，并在响应 Apache Cloudberry Segment 请求时发送该数据块。Segment 将收到的数据解包为行，再根据外部表的分布策略分发这些行。如果外部表可写，Segment 会通过请求将行组成的数据块发送给 gpfdist，由 gpfdist 将它们写入外部文件。
>
> 外部数据文件中的行可以采用 CSV 格式，或 `CREATE EXTERNAL TABLE` 命令的 `FORMAT` 子句支持的任意分隔文本格式。
>
> <!-- In addition, `gpfdist` can be configured with a YAML-formatted file to transform external data files between a supported text format and another format, for example XML or JSON. See <ref\> for an example that shows how to use `gpfdist` to read external XML files into a Apache Cloudberry readable external table. -->
>
> 对于可读外部表，`gpfdist` 会自动解压 `gzip`（`.gz`）和 `bzip2`（.`bz2`）文件。可以使用通配符（`*`）或其他 C 风格的模式匹配来表示多个待读取文件。外部文件路径被视为相对于启动 `gpfdist` 实例时指定的目录。
>
> ### 关于 gpfdist 设置和性能 {#about-gpfdist-setup-and-performance}
>
> 可以在多台主机上运行 `gpfdist` 实例，也可以在每台主机上运行多个 `gpfdist` 实例。这样便可以合理部署 `gpfdist` 服务器，充分利用所有可用网络带宽和 Apache Cloudberry 的并行能力，实现较高的数据加载和导出速率。
>
> - 允许网络流量同时使用提取、转换、加载（ETL）主机上的所有网络接口。在 ETL 主机的每个接口上运行一个 gpfdist 实例，然后在外部表定义的 `LOCATION` 子句中声明每个网络接口卡（NIC）的主机名（请参阅[创建外部表的示例](#example-1---run-single-gpfdist-instance-on-a-single-nic-machine)）。
>
> - 将外部表数据均匀分配给 ETL 主机上的多个 gpfdist 实例。例如，在具有两个 NIC 的 ETL 系统上运行两个 gpfdist 实例（每个 NIC 一个），并将外部表数据文件均匀分配给这两个 gpfdist 服务器，以优化数据加载性能。
>
> > [!TIP]
> > 向 gpfdist 提交文件时，使用竖线（`|`）分隔格式化文本。Apache Cloudberry 会用单引号或双引号包围以逗号分隔的文本字符串。gpfdist 必须去掉这些引号才能解析字符串。使用竖线分隔格式化文本可以省去这一步，从而提高性能。
>
> ### 控制 Segment 并行度 {#control-segment-parallelism}
>
> `gp_external_max_segs` 服务器配置参数控制可同时访问单个 gpfdist 实例的 Segment 实例数量，默认值为 64。你可以设置 Segment 数量，使部分 Segment 处理外部数据文件，其他 Segment 执行其他数据库处理。在 Coordinator 实例的 `postgresql.conf` 文件中设置此参数。

## 步骤 1：安装 gpfdist {#step-1-install-gpfdist}

gpfdist 安装在 Apache Cloudberry Coordinator 主机安装目录的 `$GPHOME/bin` 下。请在 Apache Cloudberry Coordinator 或 Standby Coordinator 以外的机器上运行 gpfdist，例如专门用于 ETL 处理的机器。在 Coordinator 或 Standby Coordinator 上运行 gpfdist 可能影响查询执行性能。

## 步骤 2：启动和停止 gpfdist {#step-2-start-and-stop-gpfdist}

可以在当前目录或任何指定目录中启动 gpfdist。默认端口为 `8080`。

在当前目录中输入：

```shell
gpfdist &
```

如果要使用其他目录，请指定提供文件的目录，也可以指定运行时使用的 HTTP 端口。

在后台启动 gpfdist，并将输出消息和错误记录到日志文件：

```shell
$ gpfdist -d /var/load_files -p 8081 -l /home/`gpadmin`/log &
```

在同一个 ETL 主机上运行多个 gpfdist 实例时，请为每个实例使用不同的基础目录和端口。例如：

```shell
$ gpfdist -d /var/load_files1 -p 8081 -l /home/`gpadmin`/log1 &
$ gpfdist -d /var/load_files2 -p 8082 -l /home/`gpadmin`/log2 &
```

日志保存在 `/home/gpadmin/log` 中。

> [!NOTE]
> 停止在后台运行的 gpfdist：
>
> 首先查找其进程 ID：
>
> ```shell
> $ ps -ef | grep gpfdist
> ```
>
> 然后停止该进程，例如（本例中的进程 ID 为 `3457`）：
>
> ```shell
> $ kill 3457
> ```

## 步骤 3：结合 gpfdist 和外部表加载数据 {#step-3-use-gpfdist-with-external-tables-to-load-data}

以下示例说明创建外部表时，如何使用 gpfdist 将数据加载到 Apache Cloudberry。

> [!TIP]
> 使用 IPv6 时，务必将数字形式的 IP 地址放在方括号中。

### 示例 1：在单 NIC 机器上运行单个 gpfdist 实例 {#example-1---run-single-gpfdist-instance-on-a-single-nic-machine}

使用 gpfdist 协议创建可读外部表 ext_expenses。文件以竖线（`|`）作为列分隔符。

```sql
=# CREATE EXTERNAL TABLE ext_expenses ( name text,
    date date, amount float4, category text, desc1 text )
    LOCATION ('gpfdist://etlhost-1:8081/*')
FORMAT 'TEXT' (DELIMITER '|');
```

### 示例 2：运行多个 gpfdist 实例 {#example-2--run-multiple-gpfdist-instances}

使用 gpfdist 协议，从所有扩展名为 txt 的文件创建可读外部表 `ext_expenses`。列分隔符为竖线（`|`），NULL（' '）用空格表示。

```sql
=# CREATE EXTERNAL TABLE ext_expenses ( name text, 
   date date,  amount float4, category text, desc1 text ) 
   LOCATION ('gpfdist://etlhost-1:8081/*.txt', 
             'gpfdist://etlhost-2:8081/*.txt')
   FORMAT 'TEXT' ( DELIMITER '|' NULL ' ') ;
```

<!-- ### Example 3 — Run multiple gpfdists instances

Creates a readable external table, `ext_expenses`, from all files with the txt extension using the gpfdists protocol. The column delimiter is a pipe (`|`) and NULL (' ') is a space.

1. Run gpfdist with the `--ssl` option.
2. Run the following SQL command to create an external table.

```sql
=# CREATE EXTERNAL TABLE ext_expenses ( name text, 
   date date,  amount float4, category text, desc1 text ) 
   LOCATION ('gpfdists://etlhost-1:8081/*.txt', 
             'gpfdists://etlhost-2:8082/*.txt')
   FORMAT 'TEXT' ( DELIMITER '|' NULL ' ');
``` -->

### 示例 3：运行带错误日志记录的单个 gpfdist 实例 {#example-3--single-gpfdist-instance-with-error-logging}

使用 gpfdist 协议，从所有扩展名为 txt 的文件创建可读外部表 `ext_expenses`。列分隔符为竖线（`|`），NULL（' '）用空格表示。

对该外部表的访问采用单行错误隔离模式。Apache Cloudberry 在内部捕获输入数据的格式错误，并记录错误说明。<!-- See Viewing Bad Rows in the Error Log for information about investigating error rows.--> 你可以查看错误、修复问题，然后重新加载被拒绝的数据。如果某个 Segment 上的错误数量大于 `5`（`SEGMENT REJECT LIMIT` 的值），则整个外部表操作失败，不处理任何行。

```sql
=# CREATE EXTERNAL TABLE ext_expenses ( name text, 
   date date, amount float4, category text, desc1 text ) 
   LOCATION ('gpfdist://etlhost-1:8081/*.txt', 
             'gpfdist://etlhost-2:8082/*.txt')
   FORMAT 'TEXT' ( DELIMITER '|' NULL ' ')
   LOG ERRORS SEGMENT REJECT LIMIT 5;
```

从 CSV 格式的文本文件创建可读表 `ext_expenses`：

```sql
=# CREATE EXTERNAL TABLE ext_expenses ( name text, 
   date date,  amount float4, category text, desc1 text ) 
   LOCATION ('gpfdist://etlhost-1:8081/*.txt', 
             'gpfdist://etlhost-2:8082/*.txt')
   FORMAT 'CSV' ( DELIMITER ',' )
   LOG ERRORS SEGMENT REJECT LIMIT 5;
```

### 示例 4：使用 gpfdist 创建可写外部表 {#example-4---create-a-writable-external-table-with-gpfdist}

创建可写外部表 `sales_out`，使用 gpfdist 将输出数据写入文件 `sales.out`。列分隔符为竖线（`|`），NULL（`' '`）用空格表示。文件将创建在启动 gpfdist 文件服务器时指定的目录中。

```sql
=# CREATE WRITABLE EXTERNAL TABLE sales_out (LIKE sales) 
   LOCATION ('gpfdist://etl1:8081/sales.out')
   FORMAT 'TEXT' ( DELIMITER '|' NULL ' ')
   DISTRIBUTED BY (txn_id);
```
