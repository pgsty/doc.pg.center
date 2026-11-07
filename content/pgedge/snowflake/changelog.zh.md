---
title: Snowflake 变更日志
description: 记录 Snowflake 扩展 2.6.0 和 2.5.0 的新增、变更、修复与安全/CI 更新。
weight: 200
upstream_source: pgedge-snowflake
upstream_link: https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/changelog.md
upstream_modified: true
upstream_ref: 429a16803c8c
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



这里记录 Snowflake 扩展的所有重要变更。

## 2.6.0  {#260}

### 新增 {#added}

- 新增 PostgreSQL 19 支持


## 2.5.0  {#250}

### 新增 {#added-1}

- 支持 PG18：新增 PG18 测试配置，并调整 Docker
  构建以在 PG18 上跳过 LLVM bitcode 编译。

### 变更 {#changed}

- 采用三位数（`MAJOR.MINOR.PATCH`）版本号。扩展
  版本现在是 `2.5.0`。

### 修复 {#fixed}

- 修复 snowflake 转换后序列的 dump/restore。
  `convert_sequence_to_snowflake()` 之前把 `MAXVALUE`
  保留为 `(old last_value + 1)`，但 `snowflake.nextval()`
  会绕过 `MAXVALUE` 并写入 snowflake 规模的值，因此 `pg_dump`
  可能生成无法恢复的 `setval()`。序列现在转换为
  `AS bigint MAXVALUE 9223372036854775807`，较早版本转换的
  序列会在升级时自动修复。(SUP-140)
- 修复用于把序列转换为 Snowflake 的 SQL 命令。

### 安全 / CI {#security--ci}

- 把 GitHub Actions 固定到完整 commit SHA，以加固供应链
  攻击防护。
- 从测试运行器和辅助子进程调用中移除 `shell=True` 和 shell
  注入风险；使用 `shlex.split()` 进行正确的参数分词。
- 修复 `execute_sqlite_query` 中的 SQL 注入警告和缺失参数，
  并抑制内部测试辅助子进程调用上的 Bandit B603 警告。
- 修复新版 BuildKit 下的 Dockerfile `ARG` 处理。
- 更新版权年份到 2026。

---

[上游原文](https://github.com/pgEdge/snowflake/blob/429a16803c8c6336fcfede7cce0ccd3de05216d8/docs/changelog.md) · `429a16803c8c` · Copyright (c) 2023–2026, pgEdge, Inc.; portions Copyright the PostgreSQL Global Development Group and The Regents of the University of California. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
