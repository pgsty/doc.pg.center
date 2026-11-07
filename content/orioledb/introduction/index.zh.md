---
title: OrioleDB 概览
linkTitle: 概览
description: 面向 PostgreSQL 的新一代存储引擎：使用指南、内部架构与开发文档。
weight: 10
type: docs
search_keywords: ["OrioleDB", "introduction"]
upstream_link: https://www.orioledb.com/docs
upstream_source: orioledb
upstream_modified: true
icon: fa-solid fa-dove
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
---


OrioleDB 是一个 **PostgreSQL 存储扩展**，使用 PostgreSQL 的可插拔存储系统。

它的设计目标是直接替代 PostgreSQL 现有的存储引擎，充分利用现代硬件和云基础设施，为 PostgreSQL 工作负载提供更好的性能与扩展性。

## 示例 {#example}

OrioleDB 通过 PostgreSQL 表访问方法（Table Access Method，TAM）提供可插拔存储引擎。下面演示如何使用 OrioleDB 创建表：

``` sql
-- Enable the OrioleDB extension
CREATE EXTENSION orioledb;

CREATE TABLE blog_post
(
  id int8 NOT NULL,
  title text NOT NULL,
  body text NOT NULL,
  PRIMARY KEY(id)
) USING orioledb; -- Use the OrioleDB storage engine
```

## PostgreSQL 的可插拔存储 {#pluggable-storage-in-postgresql}

可插拔存储允许开发者在同一个数据库中，为不同表使用不同存储引擎。开发者可以根据具体需要选择存储方法：有些表针对高事务负载优化，有些面向分析，还有些用于归档。

示例：

``` sql
create table analytics_data
(
  id int8,
  created_at timestamptz,
  event text
) using parquet; -- Store data in a analytical optimized storage engine

create table timeseries_data
(
  id int8,
  created_at timestamptz,
  event text
) using timeseries; -- Store data in a time-series optimized storage engine
```

MySQL 已经具有类似能力。从 MySQL 5.5 开始，默认存储引擎由 `MyISAM` 改为 `InnoDB`。可插拔存储的更多历史见[此文](https://supabase.com/blog/postgres-pluggable-strorage)。

## 在现有 PostgreSQL 安装中使用 OrioleDB {#using-orioledb-with-existing-postgresql-installations}

OrioleDB 目前需要为 PostgreSQL 应用一组补丁，增强可插拔存储 API 和其他子系统。这些补丁都已提交给 PostgreSQL 社区，正在接受审查。

这组补丁的一个关键特点是保持二进制兼容性。也就是说，可以切换到打过补丁的 PostgreSQL 二进制文件，同时保留原有数据目录。现有表会继续使用默认的 `heap` 引擎，直到将其切换为 `orioledb`。也可以切回未经修改的 PostgreSQL 二进制文件，只需先把 `orioledb` 表转换回堆表。

我们的目标是让所有补丁进入上游。补丁被接受后，OrioleDB 就能在任何 PostgreSQL 安装中运行，无需额外修改。这也会让整个 PostgreSQL 社区都能创建自己的可插拔存储引擎。

在此之前，可以使用[预构建 Docker 镜像](https://hub.docker.com/r/orioledb/orioledb)试用 OrioleDB。镜像包含打过补丁的 PostgreSQL，并预装了 OrioleDB。请按照[快速入门](/zh/orioledb/usage/getting-started/)操作。

## 补丁集 {#patch-set}

完整补丁集见[此处](https://github.com/orioledb/postgres/commits/patches16/)。以下补丁已提交给 PostgreSQL 社区，用于增强 TAM 接口和其他子系统。

| | 名称 | 链接 | 版本 |
|----|----|----|----|
| ✅ | 为 rbtree 补充缺失的不等式查找 | [链接](https://github.com/postgres/postgres/commit/e57519a4637a8d88ae993ac1273d2b59d03a0f75) | PostgreSQL 16 |
| ✅ | 在文档中说明如何为 pgbench 指定 TableAM | [链接](https://github.com/postgres/postgres/commit/f77ff083350eb5a2625a4dbfca61d15b66c4918b) | PostgreSQL 16 |
| ✅ | 移除 Tuplesortstate.copytup 函数 | [链接](https://github.com/postgres/postgres/commit/d47da3162b4d77c888c895dd36e4ef9cb92fcf19) | PostgreSQL 16 |
| ✅ | 添加 Tuplesortstate.removeabbrev 函数 | [链接](https://github.com/postgres/postgres/commit/cadfdd1edff103d696bbfcdd126c2dee516aed9b) | PostgreSQL 16 |
| ✅ | 将缩写逻辑移入 puttuple_common() | [链接](https://github.com/postgres/postgres/commit/033dd02db2248ed792332b950431ced4771b8304) | PostgreSQL 16 |
| ✅ | 将内存管理从 writetup() 和 tuplesort_put\*() 中分离 | [链接](https://github.com/postgres/postgres/commit/097366c45f5dfe142eb232dc6d348ca0705a63a9) | PostgreSQL 16 |
| ✅ | 从 Tuplesortstate 中分离 TuplesortPublic | [链接](https://github.com/postgres/postgres/commit/ec92fe98356a8a36427fe9ef52873b50fe17852e) | PostgreSQL 16 |
| ✅ | 从 tuplesort.c 中分离 tuplesortvariants.c | [链接](https://github.com/postgres/postgres/commit/d0b193c0fad13cf35122b0d3dc805c76e323e8bf) | PostgreSQL 16 |
| ✅ | 修正 writuple() 函数注释中的拼写错误 | [链接](https://github.com/postgres/postgres/commit/924954c670355f2a0ca1dd4173574a28fc0eedec) | PostgreSQL 16 |
| ✅ | 在自定义执行器节点中支持自定义槽 | [链接](https://github.com/postgres/postgres/commit/cee120951427fe39a54ab800abfa2834d85b8771) | PostgreSQL 16 |
| ✉️ | 允许表访问方法在 rd_amcache 中存储复杂数据结构 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 允许表访问方法的 tuple_insert() 返回不同的槽 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 添加 TupleTableSlotOps.is_current_xact_tuple() 方法 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 允许在 tuple_update() 和 tuple_delete() 中锁定已更新的元组 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 添加 EvalPlanQual delete returning 隔离测试 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 泛化表访问方法接口中的关系分析 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 为表访问方法提供自定义 reloptions | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
| ✉️ | 允许表访问方法的插入方法控制索引插入 | [链接](https://commitfest.postgresql.org/48/4958/) | PostgreSQL 18 |
{.wide .expand}

##### 图例 {#legend}

✅：补丁已被接受。\
✉️：补丁已提交，正在由 PostgreSQL 社区审查。\
✏️：补丁仍在开发。\

## 特性 {#features}

OrioleDB 为更强大的存储模型创造了可能，使其能够针对云环境和现代硬件架构优化。

### 开源 {#open-source}

OrioleDB 采用标准 PostgreSQL 许可证发布。我们的目标是让所有必要补丁进入上游，使 OrioleDB 无需修改即可运行于任意 PostgreSQL 安装。

### 面向现代硬件 {#designed-for-modern-hardware}

OrioleDB 的设计避开了传统架构在数十乃至数百核服务器上的 CPU 瓶颈，并针对 SSD、NVRAM 等现代存储技术优化。

### 减少维护需求 {#reduced-maintenance-needs}

OrioleDB 使用撤销日志和页面合并机制，消除了专门垃圾回收进程的需求。它还默认使用 64 位事务标识符，消除了众所周知且令人头痛的事务 ID 回卷问题。

### 面向分布式系统 {#designed-to-be-distributed}

OrioleDB 实现了支持并行应用的行级预写日志。这种日志架构针对基于 Raft 共识的复制进行了优化，可用于实现主动—主动多主架构。

## 技术差异 {#differentiators}

OrioleDB 的关键技术特点如下。

### 无缓冲区映射与无锁页面读取 {#no-buffer-mapping-and-lock-less-page-reading}

OrioleDB 的内存页通过直接链接连接存储页，消除了缓冲区映射及其相关瓶颈。内存页读取也不涉及原子操作。这些设计共同显著提升了 PostgreSQL 的纵向扩展能力。

### 基于撤销日志的 MVCC {#mvcc-is-based-on-the-undo-log-concept}

在 OrioleDB 中，旧元组版本不会让主存储膨胀，而是移入由撤销链组成的撤销日志。页级撤销记录使系统能够尽早回收已删除元组占用的空间。这些机制与页面合并配合，在大多数情况下消除了膨胀，也不再需要专门对表执行 VACUUM\*，从而消除了系统性能下降和数据库故障的一项常见重要原因。

\* 维护[桥接索引](/zh/orioledb/usage/getting-started/#experimental-support-of-indexes-other-than-btree)（即非 B 树索引）以及保持规划器统计信息最新，仍然需要 VACUUM 和 ANALYZE。

### 写时复制检查点与行级 WAL {#copy-on-write-checkpoints-and-row-level-wal}

OrioleDB 使用写时复制检查点，确保任何时刻都有结构一致的数据快照。这种方式适合现代 SSD，也让行级 WAL 成为可能。行级 WAL 容易并行应用（已实现）、体积紧凑，并适合主动—主动多主架构（计划中）。

## 相关资源 {#resources}

### Hacker News {#hacker-news}

- [OrioleDB：解决 PostgreSQL 的一些棘手问题](https://news.ycombinator.com/item?id=30462695)
- [PostgreSQL：告别 VACUUM 与膨胀](https://news.ycombinator.com/item?id=36740921)
- [OrioleDB 进入 Beta 阶段](https://news.ycombinator.com/item?id=36392765)

### 解决 PostgreSQL 的棘手问题 {#solving-postgresql-wicked-problems}

本次演讲介绍新引擎如何与 PostgreSQL 内核集成，以及如何解决 PostgreSQL 的棘手问题。

视频：<https://www.youtube-nocookie.com/embed/coaJCB_H9cU?si=MHdGlhg-KOAPRlQ8>
