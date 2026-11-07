---
title: OrioleDB 文档
linkTitle: OrioleDB
description: 安装与配置 OrioleDB，理解存储引擎原理，从源码构建并复现基准测试。
weight: -5
type: docs
search_keywords: ["OrioleDB", "orioledb"]
icon: fa-solid fa-dove
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
outputs: [HTML, RSS, print, markdown, LLMSFULL]
upstream_source: orioledb
upstream_link: https://www.orioledb.com/docs
upstream_notice: /zh/orioledb/attribution/
upstream_modified: true
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
cascade:
  type: docs
  upstream_source: orioledb
---

OrioleDB 是 PostgreSQL 的存储引擎，采用索引组织表、基于 undo 的 MVCC、写时复制检查点和行级 WAL。本手册涵盖安装配置、存储原理、开发构建与基准测试复现。

> [!NOTE] 版本说明
> 本版依据 **2026-11-06** 的上游网站快照整理。指南中的版本处于 Beta 阶段，需要带补丁的 PostgreSQL；基准测试使用 beta18。使用示例前，请先确认[安装要求和当前限制](/zh/orioledb/usage/getting-started/#current-limitations)。

- [概览](/zh/orioledb/introduction/) — 存储特性与 PostgreSQL 补丁。
- [使用指南](/zh/orioledb/usage/) — 安装配置、回退与升级。
- [架构原理](/zh/orioledb/architecture/) — B 树、undo 日志与恢复。
- [开发指南](/zh/orioledb/contributing/) — 源码构建与二进制兼容。
- [基准测试](/zh/orioledb/benchmarks/) — pgbench 与车辆跟踪测试。
- [来源与许可](/zh/orioledb/attribution/) — 来源快照、版权与编辑说明。
{.cards}

## 开始阅读 {#start}

先按[快速入门](/zh/orioledb/usage/getting-started/)创建第一张 OrioleDB 表，再查阅[配置参考](/zh/orioledb/usage/configuration/)。需要了解实现细节时，从[架构概览](/zh/orioledb/architecture/overview/)开始。

所有页面均有中英文版本。可用双语对照并排阅读，也可通过页面菜单打印或复制 Markdown。[完整 Markdown 手册](/zh/orioledb/llms-full.txt)可作为单个文件下载。
