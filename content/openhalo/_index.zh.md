---
type: docs
upstream_source: openhalo
upstream_link: ""
title: OpenHalo 文档
linkTitle: OpenHalo
description: 维护中的 OpenHalo 18 手册、版本修改、兼容边界与验收结论，以及历史 PG14 和 Halo Database 参考。
weight: -70
sidebar_root_for: self
sidebar_root_link_self: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: openhalo
no_list: true
icon: fa-solid fa-circle-nodes
---

OpenHalo 为 PostgreSQL 提供 MySQL 线协议与 SQL 兼容能力。本栏目明确区分名称相近但分属不同演进分支与产品的**四套体系**：

1. **PGSTY OpenHalo 18（`pgsty/openhalo`）** — 带协议、执行器、序列、外键与排序规则钩子的 PostgreSQL 18.6 内核，配对 `aux_mysql` 扩展（`main` 分支源码标签 `v18.6.1` 即 `2627e6f` 搭载 `aux_mysql 1.9`，已纳入 2026-11-10 通过验收的提交 `6a93e8f`；早期标签 `v18.6` 包含 `1.5`，`18.6.1` 多平台二进制安装包仍待完成包级验收）。
2. **上游 openHalo 1.0（`HaloTech-Co-Ltd/openHalo`，PG14）** — 基于 PostgreSQL 14.18 的开源分支，将 MySQL 协议与解析分析修改直接编译进约 320 个内核文件。
3. **商业 Halo Database（`1.0.16`）** — 易景科技的商业多模数据库，使用独立的监听、租户、认证与过程语言参数（`cluster_net_services`、`mysql.default_tenant`、`plmyssql`）。
4. **原生 PostgreSQL 18** — 未修改的上游 PostgreSQL，与 OpenHalo 18 共享系统目录存储布局，但不包含 OpenHalo 的协议、解析树与计划节点 ABI 钩子。

复制配置参数或评估兼容能力前，请先确认实际运行的二进制与扩展版本。

## 选择适用手册 {#benefits}

| 版本 | 产品与基线 | 状态与适用范围 |
| --- | --- | --- |
| [OpenHalo 18 / aux_mysql 1.9](/openhalo/18/) | 基于 PostgreSQL 18.6 的 `pgsty/openhalo`（源码标签 `v18.6.1` / `2627e6f`；已验收源码 `6a93e8f`；旧标签 `v18.6` / `1.5`） | **当前维护手册。** 涵盖功能、修改记录、兼容边界、构建配置、迁移审计及 2026-11-10 最终源码验收（`6a93e8f`）；多平台二进制安装包仍待完成包级验收。 |
| [PG14 构建指南（历史）](/openhalo/quick-start/) | `HaloTech-Co-Ltd/openHalo` 提交 `90fc8d7`（PostgreSQL 14.18） | **历史参考。** 保留上游 PG14 构建命令与 `database_compat_mode` 设置，不兼容 OpenHalo 18。 |
| [Halo Database 1.0.16 参考（历史）](/openhalo/mysql-compatibility/) | 商业 Halo Database 1.0.16 官方手册快照（2026-11-07） | **外部产品摘要。** 记录另一商业产品的 `cluster_net_services`、`ENUM`/`SET` 与参数，不是 OpenHalo 18 支持矩阵。 |
| [PG14 兼容性测试报告（历史）](/openhalo/mysql-compatibility-gaps/) | OpenHalo `1.0.14.18 (251127)` 独立学生测试报告（`80a8d07`） | **历史测试证据。** PG14 上的 57 项测试快照，仅作背景保留。 |
| [OpenHalo 18 初次复核（历史）](/openhalo/mysql57-compatibility-review/) | `pgsty/openhalo` 提交 `9dc937f`（`aux_mysql 1.5`，2026-11-07） | **历史 NO-GO 基线。** 记录 `1.9` 修复前的七项阻断缺陷与对照结果，请结合[修改记录](/openhalo/18/changes/)与[最终验收](/openhalo/18/acceptance/)阅读。 |
{.wide .expand}

## OpenHalo 18 手册 {#migration}

- [概览、产品关系与版本标识](/openhalo/18/) — OpenHalo 18 与 PG14、Halo Database、原生 PostgreSQL 的关系，以及五级兼容约定。
- [功能集合](/openhalo/18/features/) — 协议、SQL、DML、事务、类型、排序规则、索引、生成列与元数据的支持程度、示例与迁移影响。
- [v18.6 以来的修改](/openhalo/18/changes/) — 从最初七项阻断到 WP1–WP10、最终正确性修复与排序性能恢复的完整链路。
- [兼容边界](/openhalo/18/compatibility/) — 精确行为、有意映射、仅回显设置、明确不支持的功能、原生 PG 会话影响与错误码速查。
- [构建与配置](/openhalo/18/configuration/) — 内核与扩展配套构建、`initdb`、`caching_sha2_password`、`mysql.*` 参数上下文与废弃配置对照。
- [迁移与升级](/openhalo/18/migration/) — MySQL 5.7 导入、PG14 逻辑迁移、真实 `1.5 → 1.9` 升级、不会自动修复的历史对象及备份恢复。
- [最终验收与发布条件](/openhalo/18/acceptance/) — 固定提交 `6a93e8f` 源码结论、SHA-256 指纹、性能实测、未验证范围与剩余交付条件。
{.cards}

## 架构 {#how-it-works}

OpenHalo 18 由同一个 PostgreSQL 18.6 postmaster 同时监听 `5432`（PostgreSQL）与 `3306`（MySQL）。每个 MySQL 连接运行在常规 PostgreSQL 后端进程中，统一受 `max_connections`、`pg_hba.conf`、`pg_stat_activity` 与 PostgreSQL 密码校验信息约束。MySQL 数据库对应指定 PostgreSQL 数据库（`mysql.database`，默认 `postgres`）中的模式（schema），两种协议可直接读写同一批表。

协议帧解析、`caching_sha2_password` 认证、`COM_STMT_*` 二进制预备协议、MySQL 语法解析器、原始解析树改写、事务包装与兼容函数库位于 `contrib/aux_mysql`，由内核中的冲突判定、外键、原子序列推进与排序规则钩子支撑。内核与 `aux_mysql` 必须从同一提交配套构建并验证。

下图来自历史上游 PG14 项目，仅用于说明双协议共存思路，不代表 OpenHalo 18 的当前 ABI 或部署规范。

![历史 OpenHalo 协议架构](/openhalo/assets/how-it-works.png)

## 性能证据 {#performance}

协议兼容并不意味着在所有负载上都快于 MySQL。在 2026-11-10 的 30 万行验收基准测试（`aarch64`，Rocky Linux 9.8）中，候选 `6a93e8f` 消除了早先 `1.9` 的数倍排序退化（`ORDER BY` 中位数 `63.82 ms`，优于已发布 `v18.6` 的 `102.24 ms`），并将 `FIND_IN_SET` 扫描耗时从 `3.049 s` 降至 `0.677 s`——但由于 `FIND_IN_SET` 当前仍为 SQL 函数实现，其耗时仍比 MySQL 5.7.32（`0.073 s`）慢约 9 倍。推断业务性能前，请先阅读[实测数据、方法与硬件适用范围](/openhalo/18/acceptance/#performance)。

## 迁移决策 {#pace}

在模式、SQL 写法与事务假设符合约定边界的前提下，现有应用可继续使用标准 MySQL 驱动与命令行工具渐进迁移。切换前请先核对[兼容边界](/openhalo/18/compatibility/)与[迁移审计](/openhalo/18/migration/)——重点检查 `BIGINT UNSIGNED`（`0..INT64_MAX`）、字符类型拒绝 `NUL`（`1366`）、四个精确排序规则名称与 `1105` 近似映射、读写 `REPEATABLE READ` 到 PostgreSQL `READ COMMITTED` 的映射、普通 `UPDATE` 匹配行数计数，以及需要人工修复的历史 `1.5` 对象。从 OpenHalo PG14 升级到 OpenHalo 18 必须采用逻辑迁移。

## 历史参考 {#mysql-compatibility}

> [!WARNING]
> **切勿将历史页面中的配置复制到 OpenHalo 18。** 以下历史页面出现的 `database_compat_mode`、`--with-uuid=ossp`、`cluster_net_services`、`mysql.default_tenant`、`plmyssql` 与 `password_encryption = 'mysql_native_password'` 等设置分属 PG14 openHalo 或商业 Halo Database 1.0.16，在 OpenHalo 18 中不受支持或会直接报错。

以下页面保留原有产品语境、证据记录与固定 URL：

- [PG14 构建与配置](/openhalo/quick-start/)
- [Halo Database 1.0.16 MySQL 兼容](/openhalo/mysql-compatibility/)
- [Halo Database 1.0.16 配置与连接](/openhalo/mysql-configuration/)
- [Halo Database 1.0.16 MySQL 语句](/openhalo/mysql-statements/)
- [Halo Database 1.0.16 数据类型](/openhalo/mysql-data-types/)
- [历史 PG14 OpenHalo 兼容测试报告](/openhalo/mysql-compatibility-gaps/)
- [OpenHalo 18 初次复核，2026-11-07（`9dc937f`）](/openhalo/mysql57-compatibility-review/)
{.cards}
