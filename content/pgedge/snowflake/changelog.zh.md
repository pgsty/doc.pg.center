---
title: Snowflake 变更日志
description: 记录 Snowflake 扩展 2.6.1、2.6.0 和 2.5.0 的新增、变更、修复与安全/CI 更新。
weight: 200
upstream_source: pgedge-snowflake-20261121
upstream_link: https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/changelog.md
upstream_modified: true
upstream_ref: 9506e1bd5c1f
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



这里记录 Snowflake 扩展的所有重要变更。

## 2.6.1 {#261}

### 变更 {#changed-261}

- 版本号更新为 2.6.1（系统目录没有变更）。包含自 2.6.0 以来的发布打包和 CI 更新。

## 2.6.0  {#260}

### 新增 {#added}

- 新增 PostgreSQL 19 支持


## 2.5.0  {#250}

### 新增 {#added-1}

- 支持 PG18：新增 PG18 测试配置，并调整 Docker
  构建以在 PG18 上跳过 LLVM bitcode 编译。

### 变更 {#changed}

- 采用三段式版本号（`MAJOR.MINOR.PATCH`）。当前扩展版本为 `2.5.0`。

### 修复 {#fixed}

- 修复转换为 Snowflake 序列后的转储和恢复问题。过去，`convert_sequence_to_snowflake()` 将 `MAXVALUE` 保留为 `(old last_value + 1)`，而 `snowflake.nextval()` 生成的 Snowflake 序列值可以超过这个上限。因此，`pg_dump` 可能生成一条在恢复时报错的 `setval()` 调用。现在转换序列时会指定 `AS bigint MAXVALUE 9223372036854775807`。由早期版本转换的序列会在升级时自动修复。（SUP-140）
- 修复将序列转换为 Snowflake 的 SQL 命令。

### 安全 / CI {#security--ci}

- 将 GitHub Actions 固定到完整的提交 SHA，防范供应链攻击。
- 移除测试运行器和辅助子进程中的 `shell=True`，消除相应的 shell 注入风险。使用 `shlex.split()` 正确拆分参数。
- 修复 `execute_sqlite_query` 的 SQL 注入警告，并补上缺少的参数。对内部测试辅助程序的子进程调用，抑制 Bandit B603 警告。
- 修复新版 BuildKit 下 Dockerfile 对 `ARG` 的处理。
- 将版权年份更新为 2026 年。

---

[上游原文](https://github.com/pgEdge/snowflake/blob/9506e1bd5c1f8f8c22df43bdc3efd2b00398ddd8/docs/changelog.md) · `9506e1bd5c1f` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
