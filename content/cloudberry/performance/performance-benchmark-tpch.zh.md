---
title: "TPC-H：Apache Cloudberry 决策支持基准测试"
description: "在现有 Apache Cloudberry 集群上自动运行 TPC-H 基准测试。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/benchmark/performance-benchmark-tpch.md"
---

本工具基于基准测试工具 [TPC-H](https://www.tpc.org/tpch/default5.asp)。
本仓库指导你在 Apache Cloudberry Sandbox 中现有的 Apache Cloudberry 集群上自动运行 TPC-H 基准测试。

> [!NOTE]
> TPC-H 是一套决策支持基准测试，由面向业务的即席查询和并发数据修改组成。其查询和填充数据库的数据具有广泛的行业代表性。该基准测试展示了决策支持系统检查大量数据、执行复杂查询并回答关键业务问题的能力。更多信息请参见 [TPC-H 官方网站](https://www.tpc.org/tpch/)。

## 背景 {#context}

### 支持的 TPC-H 版本 {#supported-tpc-h-versions}

TPC 历年来发布了以下 TPC-H 标准：

| TPC-H 基准测试版本 | 发布日期 | 标准规范 |
|-|-|-|
| 3.0.1 | 04/28, 2022| https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf |
| 3.0.0 | 02/18, 2021 | https://tpc.org/TPC_Documents_Current_Versions/pdf/tpc-h_v3.0.0.pdf|

## 设置 {#setup}

### 前提条件 {#prerequisites}

本教程是前面训练营步骤的后续内容。请确保 Apache Cloudberry Sandbox 环境已经准备就绪并正常运行。

### TPC-H 工具依赖 {#tpc-h-tools-dependencies}

请确保 `cdw` 上已安装 `gcc` 和 `make`，以便编译 `dbgen`（数据生成）和 `qgen`（查询生成）。

可以在 `cdw` 上安装这些依赖：

```bash
docker exec -it $(docker ps -q) /bin/bash
yum -y install gcc make
```

源代码来自 http://tpc.org/tpc_documents_current_versions/current_specifications5.asp.

### 软件包 {#packages}

TPC-H 和 TPC-DS 软件包已放置在 "cdw:/tmp/" 目录下。

```bash
[gpadmin@cdw tmp]$ ls -rlt
-rw-rw-r--  1 root    root    24520013 Jul 27 14:18 TPC-H-CBDB.tar.gz
-rw-rw-r--  1 root    root     7096941 Jul 27 14:18 TPC-DS-CBDB.tar.gz
```

### 执行 {#execution}

要运行基准测试，请以 `gpadmin` 身份登录 Apache Cloudberry Sandbox 中的 `cdw`，并执行以下命令：

```bash
su - gpadmin
tar xzf TPC-H-CBDB.tar.gz
cd ~/TPC-H-CBDB
./run.sh
```

TPC-H 基准测试需要运行几分钟才能得到最终报告，具体时间取决于机器硬件。可以在同一目录下查看 TPC-H 执行日志文件，其名称与下面的示例类似。

```
tpch_20230727_145051.log
```
