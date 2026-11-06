---
title: "gpfdist"
description: "向 Apache Cloudberry Segment 提供数据文件，或将 Segment 数据写出到文件。"
weight: 130
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpfdist.md"
---

## 概要 {#synopsis}

```shell
gpfdist [-d <directory>] [-p <http_port>] [-P <last_http_port>] [-l <log_file>]
   [-t <timeout>] [-S] [-w <time>] [-v | -V] [-s] [-m <max_length>]
   [--ssl <certificate_path> [--sslclean <wait_time>] ]
   [--compress] [--multi_thread <num_threads>]
   [-c <config.yml>]

gpfdist -? | --help 

gpfdist --version
```

## 说明 {#description}

`gpfdist` 是 Apache Cloudberry 的并行文件分发程序。可读外部表和 `gpload` 使用它向所有 Apache Cloudberry Segment 并行提供外部表文件。可写外部表使用它并行接收 Apache Cloudberry Segment 的输出流，并将其写入文件。

外部表要使用 `gpfdist`，其定义中的 `LOCATION` 子句必须使用 `gpfdist://` 协议指定外部表数据（参阅 Apache Cloudberry 命令 `CREATE EXTERNAL TABLE`）。

> **注意** 如果指定了 `--ssl` 选项以启用 SSL 安全传输，请使用 `gpfdists://` 协议创建外部表。

使用 `gpfdist` 可以保证读写外部表时达到最大并行度，从而提供最佳性能，并简化外部表的管理。

对于可读外部表，当用户对其执行 `SELECT` 时，`gpfdist` 会解析数据文件，并将数据均匀地提供给 Apache Cloudberry 系统中的所有 Segment 实例。对于可写外部表，当用户向其执行 `INSERT` 时，`gpfdist` 会接收各 Segment 的并行输出流，并写入输出文件。

> **注意** `gpfdist` 读取数据时，如果遇到数据格式错误，错误消息会包含指示错误位置的行号。`gpfdist` 会尝试捕获出错行。但是，对于某些格式错误，`gpfdist` 可能无法捕获准确的行。

对于可读外部表，如果加载文件使用 `gzip` 或 `bzip2` 压缩（扩展名为 `.gz` 或 `.bz2`），`gpfdist` 会在加载时即时解压数据。对于可写外部表，如果目标文件的扩展名为 `.gz`，`gpfdist` 会使用 `gzip` 压缩数据。

> **注意** 在 Windows 平台上运行 `gpfdist` 工具时，可读和可写外部表均不支持压缩。

通过 `gpfdist` 或 `gpfdists` 协议读写数据时，Apache Cloudberry 会在 HTTP 请求头中加入 `X-GP-PROTO`，表示请求来自 Apache Cloudberry。此工具会拒绝请求头中不包含 `X-GP-PROTO` 的 HTTP 请求。

通常，你会希望在 ETL 机器上运行 `gpfdist`，而不是在安装了 Apache Cloudberry 的主机上运行。要在另一台主机上安装 `gpfdist`，只需将工具复制到该主机，并将 `gpfdist` 加入 `$PATH`。

> **注意** 使用 IPv6 时，始终用方括号括起数字形式的 IP 地址。

## 选项 {#options}

**`-d directory`**

`gpfdist` 为可读外部表提供文件，或为可写外部表创建输出文件的目录。如果未指定，默认为当前目录。

**`-l log_file`**

记录标准输出消息的日志文件的完全限定路径及文件名。

**`-p http_port`**

`gpfdist` 提供文件服务的 HTTP 端口。默认为 8080。

**`-P last_http_port`**

`gpfdist` 尝试提供文件服务的 HTTP 端口范围（从 http_port 到 last_http_port，含两端）的最后一个端口号。`gpfdist` 使用该范围内第一个成功绑定的端口提供文件服务。

**`-t timeout`**

设置允许 Apache Cloudberry 与 `gpfdist` 进程建立连接的时间。默认为 5 秒。允许的值为 2 到 7200 秒（2 小时）。在网络流量较大的系统上，可能需要增大此值。

**`-m max_length`**

设置允许的最大数据行长度，单位为字节。默认为 32768。当用户数据包含很宽的行时（或出现 `line too long` 错误消息时），应使用此选项。其他情况下不应使用，因为它会增加资源分配。有效范围为 32K 到 256MB。（Windows 系统上的上限为 1MB。）

> **注意** 如果指定较大的最大行长度，同时运行大量 `gpfdist` 并发连接，可能出现内存问题。例如，将此值设为最大值 256MB，并运行 96 个并发 `gpfdist` 进程，约需 24GB 内存（`(96 + 1) x 246MB`）。

**`-s`**

启用简化日志记录。指定此选项后，仅将 `WARN` 及更高级别的消息写入 `gpfdist` 日志文件，不写入 `INFO` 级别消息。如果未指定此选项，所有 `gpfdist` 消息都会写入日志文件。

可指定此选项来减少写入日志文件的信息。

**`-S (use O_SYNC)`**

使用 `O_SYNC` 标志打开文件，以执行同步 I/O。对所得文件描述符的任何写入都会阻塞 `gpfdist`，直到数据实际写入底层硬件。

**`-w time`**

设置 Apache Cloudberry 在关闭命名管道等目标文件之前延迟的秒数。默认值为 0，即不延迟。最大值为 7200 秒（2 小时）。

对于包含多个 Segment 的 Apache Cloudberry，不同 Segment 向文件写入数据时可能存在时间间隔。可以指定 Apache Cloudberry 关闭文件前的等待时间，确保所有数据都写入文件。

**`--ssl certificate_path`**

为通过 `gpfdist` 传输的数据启用 SSL 加密。使用 `--ssl certificate_path` 选项运行 `gpfdist` 后，只能通过 `gpfdist://` 协议从此文件服务器加载数据。有关 `gpfdist://` 协议的信息，请参阅[加载和卸载数据](/cloudberry/data-loading/files/load-data-using-gpfdist/)。

certificate_path 指定的位置必须包含以下文件：

- 服务器证书文件 `server.crt`
- 服务器私钥文件 `server.key`
- 受信任的证书颁发机构文件 `root.crt`

不能将根目录（`/`）指定为 certificate_path。

**`--sslclean wait_time`**

使用 `--ssl` 选项运行此工具时，设置它在完成与 Apache Cloudberry Segment 之间的数据写入后，到关闭 SSL 会话并清理 SSL 资源之前延迟的秒数。默认值为 0，即不延迟。最大值为 500 秒。增加延迟会降低传输速度。

某些情况下，复制大量数据时可能出现错误：`gpfdist server closed connection`。可以添加延迟来避免此错误，例如 `--sslclean 5`。

**`--compress`**

在数据传输期间启用压缩。指定此选项后，`gpfdist` 使用 Zstandard（`zstd`）压缩算法。

Windows 平台不支持此选项。

**`--multi_threads num_threads`**

设置 `gpfdist` 在数据传输期间使用的最大线程数，以并行执行操作。指定此选项后，`gpfdist` 会在传输前自动压缩数据（压缩也并行执行）。

`gpfdist` 最多支持 256 个线程。

Windows 平台不支持此选项。

**`-c config.yaml`**

指定规则，供 `gpfdist` 在加载或提取数据时选择要应用的转换。`gpfdist` 配置文件是 YAML 1.1 文档。

Windows 平台不支持此选项。

**`-v (verbose)`**

详细模式显示进度和状态消息。

**`-V (very verbose)`**

详细模式显示此工具生成的所有输出消息。

**`-? (help)`**

显示在线帮助。

**`--version`**

显示此工具的版本。

## 注意事项 {#notes}

服务器配置参数 `verify_gpfdists_cert` 控制 Apache Cloudberry 与 `gpfdist` 工具通信、读写外部数据源时是否启用 SSL 证书认证。测试 Apache Cloudberry 外部表与提供外部数据的 `gpfdist` 工具之间的通信时，可以将此参数设为 `false` 以禁用认证。值为 `false` 时，会忽略以下 SSL 异常：

- Apache Cloudberry 不信任 `gpfdist` 使用的自签名 SSL 证书。
- SSL 证书中的主机名与运行 `gpfdist` 的主机名不匹配。

> **小心** 禁用 SSL 证书认证后，不再验证 `gpfdists` SSL 证书，会带来安全风险。

当 Apache Cloudberry 尝试向 `gpfdist` 写入数据，而 `gpfdist` 服务器没有响应时，可以通过服务器配置参数 `gpfdist_retry_timeout` 控制返回错误前的等待时间。默认为 300 秒（5 分钟）。

如果 `gpfdist` 工具挂起且没有读写活动，可以在下次挂起时生成核心转储，以帮助调试。将环境变量 `GPFDIST_WATCHDOG_TIMER` 设为无活动时等待多少秒后强制 `gpfdist` 退出。设置此环境变量后，如果 `gpfdist` 挂起，它会在指定秒数后停止，创建核心转储，并将相关信息写入日志文件。

以下示例在 Linux 系统上设置环境变量，使 `gpfdist` 在 300 秒（5 分钟）无活动后退出。

```shell
export GPFDIST_WATCHDOG_TIMER=300
```

启用压缩后，`gpfdist` 可以在保持较低网络使用量的同时传输更多数据。注意，压缩可能比较耗时，并可能降低传输速度。使用多线程执行时，压缩所需的总时间可能减少，从而在保持较低网络占用的同时加快数据传输。

## 示例 {#examples}

使用端口 8081 提供指定目录中的文件（并在后台启动 `gpfdist`）：

```shell
gpfdist -d /var/load_files -p 8081 &
```

在后台启动 `gpfdist`，并将输出和错误重定向到日志文件：

```shell
gpfdist -d /var/load_files -p 8081 -l /home/gpadmin/log &
```

要使用四个线程启用多线程数据传输（隐式启用压缩），请按以下方式启动 `gpfdist`：

```shell
gpfdist -d /var/load_files -p 8081 --multi_thread 4
```

停止在后台运行的 `gpfdist`：

--首先找到其进程 ID：

```shell
ps ax | grep gpfdist
```

--然后停止该进程，例如：

```shell
kill 3456
```

## 另请参阅 {#see-also}

[gpload](/cloudberry/reference/sys-utilities/gpload/), `CREATE EXTERNAL TABLE`
