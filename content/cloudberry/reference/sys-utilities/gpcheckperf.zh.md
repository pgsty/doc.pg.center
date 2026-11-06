---
title: "gpcheckperf"
description: "验证指定主机的硬件基准性能。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpcheckperf.md"
---

## 概要 {#synopsis}

```shell
gpcheckperf -d <test_directory> [-d <test_directory> ...] 
    {-f <hostfile_gpcheckperf> | - h <hostname> [-h hostname ...]} 
    [-r ds] [-B <block_size>] [-S <file_size>] [-D] [-v|-V]

gpcheckperf -d <temp_directory>
    {-f <hostfile_gpchecknet> | - h <hostname> [-h< hostname> ...]} 
    [ -r n|N|M [--duration <time>] [--netperf] ] [-D] [-v | -V]

gpcheckperf -?

gpcheckperf --version
```

## 说明 {#description}

`gpcheckperf` 工具在指定主机上启动会话，并运行以下性能测试：

- **磁盘 I/O 测试（dd 测试）** — 要测试逻辑磁盘或文件系统的顺序吞吐性能，此工具使用标准 UNIX 工具 **dd** 命令。它会计算向磁盘写入和从磁盘读取大文件所需的时间，并计算磁盘 I/O 性能，单位为每秒兆字节（MB）。默认情况下，测试使用的文件大小按主机总随机访问内存（RAM）的两倍计算。这可以确保测试真正测试磁盘 I/O，而不是使用内存缓存。
- **内存带宽测试（stream）** — 要测试内存带宽，此工具使用 STREAM 基准测试程序测量可持续内存带宽（MB/s）。此测试用于确认系统性能不会受到系统内存带宽相对于 CPU 计算性能不足的限制。在数据集较大的应用中（如 Apache Cloudberry），内存带宽低是主要性能问题。如果内存带宽显著低于 CPU 的理论带宽，CPU 可能会花费大量时间等待数据从系统内存到达。
- **网络性能测试（gpnetbench*）** — 要测试网络性能（以及 Apache Cloudberry Interconnect 的性能），此工具运行网络基准程序，将 5 秒的数据流从当前主机传输到测试中包含的每台远程主机。数据会并行传输到每台远程主机，并以每秒兆字节（MB）报告网络传输速率的最小值、最大值、平均值和中位数。如果汇总传输速率低于预期（小于 100 MB/s），可以使用 `-r n` 选项串行运行网络测试，以获取每台主机的结果。要运行全矩阵带宽测试，可以指定 `-r M`，让每台主机都向其他每台指定主机发送和接收数据。此测试最适合用于验证交换网络是否能够承受全矩阵工作负载。

要指定测试主机，请使用 `-f` 选项指定包含主机名列表的文件，或使用 `-h` 选项在命令行上指定单个主机名。如果运行网络性能测试，主机文件中的所有条目必须是同一子网内的网络接口。如果 Segment 主机配置了位于不同子网的多个网络接口，请针对每个子网分别运行网络测试。

还必须至少指定一个测试目录（使用 `-d`）。运行 `gpcheckperf` 的用户必须拥有对所有远程主机上指定测试目录的写权限。对于磁盘 I/O 测试，测试目录应对应 Segment 数据目录（主目录和／或镜像目录）。对于内存带宽和网络测试，需要使用临时目录存放测试程序文件。

使用 `gpcheckperf` 前，参与性能测试的主机之间必须建立信任关系。如果尚未完成，可使用 `gpssh-exkeys` 工具更新已知主机文件并在主机之间交换公钥。注意，`gpcheckperf` 会调用 `gpssh` 和 `gpsync`，因此这些 Cloudberry 工具也必须位于 `$PATH` 中。

## 选项 {#options}

**`-B block_size`**

指定磁盘 I/O 测试使用的块大小（单位为 KB 或 MB）。默认值为 32KB，与 Apache Cloudberry 页大小相同。最大块大小为 1 MB。

**`-d test_directory`**

对于磁盘 I/O 测试，指定要测试的文件系统目录位置。必须拥有对参与性能测试的所有主机上测试目录的写权限。可以多次使用 `-d` 选项指定多个测试目录（例如，测试主数据目录和镜像数据目录的磁盘 I/O）。

**`-d temp_directory`**

对于网络和 stream 测试，指定一个目录，在测试期间将测试程序文件复制到该目录。必须拥有对参与测试的所有主机上此目录的写权限。

**`-D (display per-host results)`**

报告磁盘 I/O 测试中每台主机的性能结果。默认仅报告性能最低和最高的主机，以及所有主机的总性能和平均性能。

**`--duration time`**

指定网络测试的持续时间，单位可以是秒（s）、分钟（m）、小时（h）或天（d）。默认值为 15 秒。

**`-f hostfile_gpcheckperf`**

对于磁盘 I/O 和 stream 测试，指定一个文件的名称，其中每行列出一台参与性能测试的主机。必须提供主机名，也可以为每台主机指定备用用户名和／或 SSH 端口号。主机文件的语法如下，每行一个主机：

```shell
[<username>@]<hostname>[:<ssh_port>]
```

**`-f hostfile_gpchecknet`**

对于网络性能测试，主机文件中的所有条目必须是同一子网内的主机地址。如果 Segment 主机配置了位于不同子网的多个网络接口，请针对每个子网分别运行网络测试。例如（包含Interconnect 子网 1 的 Segment 主机地址名的主机文件）：

```shell
sdw1-1
sdw2-1
sdw3-1
```

**`-h hostname`**

指定参与性能测试的单个主机名（或主机地址）。可以多次使用 `-h` 选项来指定多个主机名。

**`--netperf`**

指定使用 `netperf` 二进制文件执行网络测试，而不是 Cloudberry 网络测试。要使用此选项，必须从 [https://github.com/HewlettPackard/netperf](https://github.com/HewlettPackard/netperf) 下载 `netperf`，并将其安装到所有 Cloudberry 主机（Coordinator 和 Segment）的 `$GPHOME/bin/lib` 中。

**`-r ds{n|N|M}`**

指定要运行的性能测试。默认值为 `dsn`：

- 磁盘 I/O 测试（`d`）
- Stream 测试（`s`）
- 网络性能测试：串行（`n`）、并行（`N`）或全矩阵（`M`）模式。可选的 `--duration` 选项指定网络测试运行的时长（单位为秒）。要使用并行（`N`）模式，必须在偶数台主机上运行测试。

如果希望使用 `netperf`（[https://github.com/HewlettPackard/netperf](https://github.com/HewlettPackard/netperf)）而不是 Cloudberry 网络测试，可以下载它并将其安装到所有 Cloudberry 主机（Coordinator 和 Segment）的 `$GPHOME/bin/lib` 中。然后指定可选的 `--netperf` 选项，使用 `netperf` 二进制文件，而不是默认的 `gpnetbench*` 工具。

**`-S file_size`**

指定磁盘 I/O 测试中所有通过 `-d` 指定的目录使用的总文件大小。file_size 应等于主机总 RAM 的两倍。如果未指定，默认值按运行 `gpcheckperf` 的主机总 RAM 的两倍计算。这可以确保测试真正测试磁盘 I/O，而不是使用内存缓存。可以用 KB、MB 或 GB 指定大小。

**`-v (verbose) | -V (very verbose)`**

详细模式显示性能测试运行时的进度和状态消息。非常详细模式显示此工具生成的所有输出消息。

**`--version`**

显示此工具的版本。

**`-? (help)`**

显示在线帮助。

## 示例 {#examples}

在文件 host_file 中列出的所有主机上运行磁盘 I/O 和内存带宽测试，使用 /data1 和 /data2 作为测试目录：

```shell
$ gpcheckperf -f hostfile_gpcheckperf -d /data1 -d /data2 -r ds
```

仅在主机 sdw1 和 sdw2 上运行磁盘 I/O 测试，使用 /data1 作为测试目录。显示每台主机的结果，并以详细模式运行：

```shell
$ gpcheckperf -h sdw1 -h sdw2 -d /data1 -r d -D -v
```

运行并行网络测试，使用 `/tmp` 作为测试目录；`hostfile_gpcheck_ic*` 指定同一Interconnect 子网内的所有网络接口主机地址名：

```shell
$ gpcheckperf -f hostfile_gpchecknet_ic1 -r N -d /tmp
$ gpcheckperf -f hostfile_gpchecknet_ic2 -r N -d /tmp
```

运行与上例相同的测试，但使用 `netperf` 代替 Cloudberry 网络测试（注意，所有 Cloudberry 主机的 `$GPHOME/bin/lib` 中都必须安装 `netperf`）：

```shell
$ gpcheckperf -f hostfile_gpchecknet_ic1 -r N --netperf -d /tmp
$ gpcheckperf -f hostfile_gpchecknet_ic2 -r N --netperf -d /tmp
```

## 另请参阅 {#see-also}

[gpssh](/cloudberry/reference/sys-utilities/gpssh/), [gpsync](/cloudberry/reference/sys-utilities/gpsync/)
