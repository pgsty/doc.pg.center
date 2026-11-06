---
title: "TPC-DS：Apache Cloudberry 决策支持基准测试"
description: "在现有 Apache Cloudberry 集群上自动运行 TPC-DS 基准测试。"
weight: 120
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/benchmark/performance-benchmark-tpcds.md"
---

本工具基于基准测试工具 [Pivotal TPC-DS](https://github.com/pivotal/TPC-DS)。本仓库提供了在现有 Apache Cloudberry 集群上自动运行 DS 基准测试的功能。

> [!NOTE]
> TPC-DS 是一套决策支持基准测试，对决策支持系统中普遍适用的多个方面进行建模，包括查询和数据维护。它对通用决策支持系统的性能提供具有代表性的评估。在给定的硬件、操作系统和数据处理系统配置下，基准测试通过受控、复杂、多用户的决策支持工作负载，衡量单用户模式下的查询响应时间、多用户模式下的查询吞吐量，以及数据维护性能。TPC 基准测试旨在为行业用户提供相关、客观的性能数据。有关 TPC-DS 的更多信息，请参见 [TPC 网站](https://www.tpc.org/tpcds/default5.asp)。

## 背景 {#context}

### 支持的 TPC-DS 版本 {#supported-tpc-ds-versions}

TPC 历年来发布了以下 TPC-DS 标准：

| TPC-DS 基准测试版本 | 发布日期 | 标准规范 |
|-|-|-|
| 3.2.0（最新） | 06/15, 2021 | http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v3.2.0.pdf |
| 2.1.0 | 11/12, 2015 | http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v2.1.0.pdf |
| 1.3.1（最早） | 02/19, 2015 | http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-ds_v1.3.1.pdf |

自本工具 1.2 版起，使用 TPC-DS 3.2.0。

## 设置 {#setup}

### 前提条件 {#prerequisites}

本教程是前面训练营步骤的后续内容。请确保 Apache Cloudberry Sandbox 环境已经准备就绪并正常运行。

以下所有示例都采用 Cloudberry 的标准主机命名约定：Coordinator 节点使用 `cdw`，Segment 节点使用 `sdw1..n`。

### TPC-DS 工具依赖 {#tpc-ds-tools-dependencies}

在 `cdw` 上安装依赖，以便编译 `dsdgen`（数据生成）和 `dsqgen`（查询生成）。

```bash
docker exec -it $(docker ps -q) /bin/bash
yum -y install gcc make byacc
```

源代码来自 http://tpc.org/tpc_documents_current_versions/current_specifications5.asp.

### 软件包 {#packages}

TPC-H 和 TPC-DS 软件包已位于 "cdw:/tmp/" 目录下。

```bash
[gpadmin@cdw tmp]$ ls -rlt
-rw-rw-r--  1 root    root    24520013 Jul 27 14:18 TPC-H-CBDB.tar.gz
-rw-rw-r--  1 root    root     7096941 Jul 27 14:18 TPC-DS-CBDB.tar.gz
```

### 执行 {#execution}

要运行基准测试，请以 `gpadmin` 身份登录 Cloudberry Sandbox 中的 `cdw`，并执行以下命令：

```bash
su - gpadmin
tar xzf TPC-DS-CBDB.tar.gz
cd ~/TPC-DS-CBDB
./run.sh
```

TPC-DS 基准测试需要运行几分钟才能得到最终报告，具体时间取决于机器硬件。可以在同一目录下查看 TPC-DS 执行日志文件，其名称与下面的示例类似。

```
tpcds_20231109_153553.log
```
