---
title: "验证硬件与网络"
description: "使用 gpcheckperf 验证 Apache Cloudberry 主机的网络、磁盘 I/O 和内存带宽性能。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/validate.md"
---

Cloudberry 提供了名为 [gpcheckperf](/cloudberry/reference/sys-utilities/gpcheckperf/) 的管理工具，可用于识别 Apache Cloudberry 阵列中各台机器的硬件和系统层面问题。`gpcheckperf` 会在指定主机上启动会话，并运行以下性能测试：

-   网络性能（`gpnetbench*`）
-   磁盘 I/O 性能（`dd` 测试）
-   内存带宽（`stream` 测试）

使用 `gpcheckperf` 之前，必须在参与性能测试的主机之间建立信任关系。如果尚未完成这项配置，可以使用 [gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/) 工具更新已知主机文件，并在主机之间交换公钥。注意，`gpcheckperf` 会调用 [gpssh](/cloudberry/reference/sys-utilities/gpssh/) 和 [gpsync](/cloudberry/reference/sys-utilities/gpsync/)，因此这些 Apache Cloudberry 工具必须位于 `$PATH` 中。

## 验证网络性能 {#validating-network-performance}

要测试网络性能，请运行 `gpcheckperf`，并选择一种网络测试选项：并行配对测试（`-r N`）、串行配对测试（`-r n`）或全矩阵测试（`-r M`）。该工具会运行网络基准测试程序，从当前主机向参与测试的每台远程主机持续传输 5 秒的数据流。默认情况下，数据会并行传输到每台远程主机，并以兆字节（MB）每秒为单位报告网络传输速率的最小值、最大值、平均值和中位数。如果汇总的传输速率低于预期（小于 100 MB/s），可以使用 `-r n` 选项串行运行网络测试，以获得每台主机的结果。要运行全矩阵带宽测试，可以指定 `-r M`，使每台主机都与指定的其他所有主机相互收发数据。此测试最适合用于验证交换网络能否承受全矩阵负载。

Apache Cloudberry 阵列中的大多数系统都配置了多块网卡（NIC），每块网卡位于各自的子网中。测试网络性能时，务必分别测试每个子网。例如，假设每台主机有两块网卡，网络配置如下：

|Cloudberry 主机|子网 1 网卡|子网 2 网卡|
|--------------|------------|------------|
|Segment 1|sdw1-1|sdw1-2|
|Segment 2|sdw2-1|sdw2-2|
|Segment 3|sdw3-1|sdw3-2|

需要创建四个不同的主机文件，供 `gpcheckperf` 网络测试使用：

|hostfile_gpchecknet_ic1|hostfile_gpchecknet_ic2|
|-------------------------|-------------------------|
|sdw1-1|sdw1-2|
|sdw2-1|sdw2-2|
|sdw3-1|sdw3-2|

然后对每个子网分别运行一次 `gpcheckperf`。例如，要测试的主机数量为*偶数*时，采用并行配对测试模式：

```
$ gpcheckperf -f hostfile_gpchecknet_ic1 -r N -d /tmp > subnet1.out
$ gpcheckperf -f hostfile_gpchecknet_ic2 -r N -d /tmp > subnet2.out
```

如果要测试的主机数量为*奇数*，可以采用串行测试模式（`-r n`）。

## 验证磁盘 I/O 和内存带宽 {#validating-disk-io-and-memory-bandwidth}

要测试磁盘和内存带宽性能，请运行 `gpcheckperf`，并指定磁盘和 stream 测试选项（`-r ds`）。磁盘测试使用 `dd` 命令（标准 UNIX 工具）测试逻辑磁盘或文件系统的顺序吞吐性能。内存测试使用 STREAM 基准测试程序测量持续内存带宽。结果以 MB 每秒（MB/s）为单位报告。

### 运行磁盘和 stream 测试 {#running-the-disk-and-stream-tests}

1.  以 `gpadmin` 用户身份登录 Coordinator 主机。
2.  使用 source 加载 Apache Cloudberry 安装目录中的 `cloudberry-env.sh` 路径文件。例如：

    ```
    $ source /usr/local/cloudberry-db/cloudberry-env.sh
    ```

3.  创建名为 `hostfile_gpcheckperf` 的主机文件，每台 Segment 主机只列出一个主机名。不要包含 Coordinator 主机。例如：

    ```
    sdw1
    sdw2
    sdw3
    sdw4
    ```

4.  使用刚创建的 `hostfile_gpcheckperf` 文件运行 `gpcheckperf` 工具。使用 `-d` 选项指定要在每台主机上测试的文件系统（必须对这些目录具有写入权限）。应测试所有主 Segment 和镜像 Segment 数据目录所在的位置。例如：

    ```
    $ gpcheckperf -f hostfile_gpcheckperf -r ds -D \
      -d /data1/primary -d  /data2/primary \
      -d /data1/mirror -d  /data2/mirror
    ```

5.  由于需要在主机之间复制很大的文件，该工具可能需要一段时间才能完成测试。完成后，将显示磁盘写入、磁盘读取和 Stream 测试的汇总结果。
