---
title: Snowflake
description: Snowflake 序列基于 int8 与 sequence，为分布式多主复制生成节点唯一、趋势有序的 64 位 ID。
weight: 30
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/index.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
linkTitle: Snowflake
icon: fa-solid fa-book-open
sidebar_root_for: self
no_list: true
type: docs
sidebar_root_menu: false
---


> [!NOTE] 版本说明
> 本文档来自上游 `main` 的固定源码快照；与原站的版本化文档可能存在差异。部署前请核对[版本与来源](/zh/pgedge/about/attribution/)。


使用 [`Snowflake` 序列](https://github.com/pgEdge/snowflake?tab=readme-ov-file#snowflake-sequences-for-postgresql)可以充分利用分布式多主复制解决方案提供的优势。Snowflake 是一个 PostgreSQL 扩展，提供基于 int8 和 sequence 的唯一 ID 方案，可选择用于替代 PostgreSQL 内建的 bigserial 数据类型。

在内部，snowflake 是 64 位整数，对外表示为 bigint 值。这 64 位被划分为若干位段：

* bit 63 —— 未使用（int8 的符号位）
* bits 22-62 —— 毫秒精度时间戳
* bits 12-21 —— 唯一的 pgEdge Distributed Postgres 节点号
* bits 0-11 —— 一毫秒内的计数器
* 时间戳是 41 位无符号值，表示毫秒精度，epoch 为 2023-01-01。
* 计数器是 12 位无符号值，每次分配 ID 时递增。它可提供每毫秒 4096 个唯一 ID，即每秒 400 万个 ID。
* 节点号是全局集群内 PostgreSQL 实例的 10 位唯一标识符。该值通过 `snowflake.node` GUC 在 `postgresql.conf` 文件中设置。

Snowflake 序列让你能够：

* 在不同区域添加或修改数据，同时确保事务序列唯一。
* 无需手动或管理式维护编号方案，即可保留唯一事务标识符。
* 准确识别全局分布式事务的执行顺序。

Snowflake 序列也能减轻网络延迟可能扰乱分布式事务序列的担忧。

一个 Snowflake 序列由时间戳、计数器和唯一节点标识符组成；这些组成部分的位宽设计确保可提供超过 18 万亿个唯一序列号。该扩展支持多种命令和[函数](/zh/pgedge/snowflake/snowflake-functions/)，可简化[创建新的 Snowflake 序列](/zh/pgedge/snowflake/creating/)或[转换既有序列](/zh/pgedge/snowflake/converting/)。

## 继续阅读 {#continue-reading}

- [Snowflake 变更日志](/zh/pgedge/snowflake/changelog/)
- [将 PostgreSQL 序列转换为 Snowflake 序列](/zh/pgedge/snowflake/converting/)
- [在新集群中创建 Snowflake 序列](/zh/pgedge/snowflake/creating/)
- [审查表元数据中的序列定义](/zh/pgedge/snowflake/review-seq/)
- [Snowflake 函数](/zh/pgedge/snowflake/snowflake-functions/)

---

[上游原文](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/index.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
