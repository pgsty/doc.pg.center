---
title: "并行处理"
linkTitle: "并行处理"
weight: 50
description: "在单个日志分块并行与多个日志并行之间做出选择"
icon: fa-solid fa-gauge-high
module: [PGBADGER]
categories: [任务]
aliases: [/docs/pgbadger/parallel-processing/]
---

> 来源：固定上游 [`README.md`](https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md) 的 “Parallel Processing” 章节。

pgBadger 提供两种互补的多进程模式。选择时应关注输入日志的形态，而不只是 CPU 数量。

| 选项 | 并行单位 | 最适合 | 主要限制 |
|---|---|---|---|
| `-j N` / `--jobs N` | 一个日志文件的多个分块 | 单个可定位的大日志 | 分块边界可能重复或漏掉少量查询 |
| `-J N` / `--Jobs N` | 完整日志文件 | 大量相互独立的日志 | 只有文件数量足以填满工作进程时才有明显收益 |

## 使用 `-j` 拆分单个大文件 {#single-file-jobs}

```console
$ pgbadger -j 8 /var/log/postgresql/postgresql.log
```

上游算法把每个文件分成 `N` 个字节区间，为每个区间 fork 一个解析进程，把统计结果写入临时二进制文件，最后合并生成报告。

```text
对于每个日志文件：
    把文件划分为 N 个分块
    确定每个分块的起止偏移量
    在对应偏移量启动 N 个解析进程
    每个进程写入一份临时二进制统计文件
等待所有工作进程结束
合并二进制文件并生成报告
```

日志记录和多行语句不会恰好与字节偏移对齐，因此每个文件约有最多 `N` 条查询可能在边界处被截断、遗漏，或更常见地被重复计数。该模式适合大文件的聚合分析，不适合要求每条记录计数完全精确的取证流程。

## 使用 `-J` 并行处理多个文件 {#multiple-file-jobs}

```console
$ pgbadger -J 8 /var/log/postgresql/postgresql-*.log
```

每个工作进程独占一个完整文件，因此不会出现分块边界误差。它在有数百个小文件，并且 CPU 与 I/O 能力充足时最有效。上游文档也允许 `-J` 处理相互独立的压缩文件；使用 `-j` 对单文件分块则要求输入未压缩且可随机定位。

## 上游基准测试 {#benchmark}

上游手册给出了以下 8 CPU 主机测试。它适合用来比较两种算法，不应当作现代硬件的耗时预测。

单个 9.5 GB 文件：

| 选项 | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 1h41m18 | 50m25 | 25m39 | 15m58 |
| `-J` | 1h41m18 | 54m28 | 41m16 | 34m45 |

两百个 10 MB 文件，共 2 GB：

| 选项 | 1 CPU | 2 CPU | 4 CPU | 8 CPU |
|---|---:|---:|---:|---:|
| `-j` | 20m15 | 9m56 | 5m20 | 4m20 |
| `-J` | 20m15 | 9m49 | 5m00 | 2m40 |

实用默认值是：少量大文件使用 `-j`，大量小文件使用 `-J`。在输入和平台允许时可以组合两种模式，但仍需实测；日志解析很可能先受到存储吞吐量限制，而不是 CPU 限制。

## 限制与临时文件 {#limits-and-temporary-files}

- `-j` 不能用于压缩或 CSV 输入，并且依赖进程 fork，因此不适用于 Windows。
- 上游远程输入路径不支持远程 CSV 解析。
- 并行分析会在指定临时目录中创建形如 `tmp_pgbadgerXXXX.bin` 的文件；默认使用系统临时目录。
- pgBadger 运行期间不要清理这些文件。可用 `--tempdir` 把它们放到容量充足的存储上。
- 从较小的工作进程数开始，观察 CPU、读取吞吐量、临时空间占用与总耗时后再调大。

