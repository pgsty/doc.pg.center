---
title: "系统监控与维护"
description: "确保 Apache Cloudberry 高可用和最佳性能的定期维护最佳实践。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/system-monitor-and-maintain-best-practices.md"
---

- [使用 ANALYZE 更新统计信息](/cloudberry/performance/update-stats-using-analyze/)

- [管理数据库膨胀](/cloudberry/tutorials/best-practices/manage-bloat/)

## 监控系统 {#monitor-the-system}

Apache Cloudberry 提供了有助于监控系统的工具。

`gp_toolkit` 模式包含多个视图，可以使用 SQL 命令查询系统目录、日志文件和运行环境，以获取系统状态信息。

`gp_stats_missing` 视图显示没有统计信息、需要运行 `ANALYZE` 的表。

### gpstate {#gpstate}

`gpstate` 工具程序显示 Cloudberry 系统的状态，包括哪些 Segment 已停机、Coordinator 和 Segment 配置信息（主机、数据目录等）、系统使用的端口，以及主 Segment 与对应镜像 Segment 的映射。

运行 `gpstate -Q`，获取 Coordinator 系统目录中标记为“down”的 Segment 列表。

要获取 Cloudberry 系统的详细状态信息，运行 `gpstate -s`。

### gpcheckperf {#gpcheckperf}

`gpcheckperf` 工具测试主机列表的基准硬件性能。结果有助于识别硬件问题。该工具执行以下检查：

- 磁盘 I/O 测试——使用操作系统 `dd` 命令写入和读取大型文件，测量 I/O 性能。它报告每秒的读写速率，单位为 MB。
- 内存带宽测试——使用 STREAM 基准测试测量可持续内存带宽，单位为每秒 MB。
- 网络性能测试——运行 `gpnetbench` 网络基准程序（可选 `netperf)`），测试网络性能。测试有三种模式：并行对测试（`-r N`）、串行对测试（`-r n`）或全矩阵测试（`-r M)`）。报告传输速率的最小值、最大值、平均值和中位数，单位为每秒 MB。

要从 `gpcheckperf` 获取有效数值，必须停止数据库系统。即使系统正在运行且没有查询活动，`gpcheckperf` 的数值也可能不准确。

`gpcheckperf` 要求性能测试涉及的主机之间已建立可信主机设置。它会调用 `gpssh` 和 `gpsync`，因此这些工具也必须位于 `PATH` 中。可以单独指定要检查的主机（`-h *host1* -h *host2* ...`），也可以使用 `-f *hosts_file*`，其中 `*hosts_file*` 是包含待检查主机列表的文本文件。如果存在多个子网，为每个子网创建独立主机文件，以便分别测试各个子网。

默认情况下，`gpcheckperf` 运行磁盘 I/O 测试、内存测试和串行对网络性能测试。运行磁盘 I/O 测试时，必须使用 `-d` 选项指定要测试的文件系统。以下命令测试 `subnet_1_hosts` 文件中列出的主机的磁盘 I/O 和内存带宽：

```shell
gpcheckperf -f subnet_1_hosts -d /data1 -d /data2 -r ds
```

`-r` 选项选择要运行的测试：磁盘 I/O（`d`）、内存带宽（`s`）、网络并行对测试（`N`）、网络串行对测试（`n`）、网络全矩阵测试（`M`）。每次执行只能选择一种网络模式。

### 使用操作系统工具监控 {#monitor-with-operating-system-utilities}

可以使用以下 Linux/UNIX 工具评估主机性能：

- `iostat` 允许监控 Segment 主机上的磁盘活动。
- `top` 显示操作系统进程的动态视图。
- `vmstat` 显示内存使用统计信息。

可以使用 `gpssh` 在多个主机上运行工具。

### 最佳实践 {#best-practices}

- 执行“推荐的监控与维护任务”。
- 在安装时以及之后定期运行 `gpcheckperf`，保存输出，以便比较系统性能随时间的变化。
- 使用所有可用工具，了解系统在不同负载下的行为。
- 检查任何异常事件，确定其原因。
- 定期查看执行计划监控系统上的查询活动，确保查询以最佳方式运行。
- 检查计划，确定是否使用了索引，以及是否按预期执行了分区消除。
