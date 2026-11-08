---
type: docs
upstream_source: halodb
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "Halo Database 1.0.16；2026-11-07 文档快照"
upstream_notice: /zh/attribution/#halodb
title: MySQL 兼容
linkTitle: MySQL 兼容
description: Halo 的 MySQL 协议、SQL 语法、数据类型、函数与兼容范围。
weight: 20
---

Halo Database 1.0.16 文档说明其兼容 MySQL 5.6 至 8.0 的常用功能，包括 MySQL 协议、数据类型、SQL 语法、操作符和系统函数。本栏目将这份参考资料整理成一套较短的使用与迁移指南。

开源的 [openHalo 项目](https://github.com/HaloTech-Co-Ltd/openHalo)属于相关源码，但其固定版本的 README 使用旧版配置接口。当前 Halo Database 文档与 openHalo 源码树分别记录版本，下面会明确区分。

## 参考页面 {#reference-pages}

- [配置并连接 MySQL 端点](/openhalo/mysql-configuration/)：Halo 16 配置、旧版 openHalo 参数、用户和 `mysql` 客户端。
- [兼容的 MySQL 语句](/openhalo/mysql-statements/)：`REPLACE`、`INSERT IGNORE`、`ON DUPLICATE KEY UPDATE`、`LIMIT`、预处理语句和用户变量。
- [兼容的 MySQL 数据类型](/openhalo/mysql-data-types/)：数字、字符、日期时间、`ENUM`、`SET` 和 `YEAR`。
- [已知兼容边界](/openhalo/mysql-compatibility-gaps/)：独立 OpenHalo 测试报告的版本化结果和迁移测试计划。
- [OpenHalo 18 与 MySQL 5.7 实测报告](/openhalo/mysql57-compatibility-review/)：固定提交 `9dc937f` 的独立构建、真实 MySQL 5.7.32 对照、迁移结果和阻断问题。

{.cards}

## 兼容层覆盖的内容 {#coverage}

官方参考资料将 MySQL 兼容面分为以下几类：

- 数据类型，包括整数和浮点数类型、字符类型、`ENUM`、`SET`、`DATE`、`DATETIME`、`TIMESTAMP` 和 `YEAR`；
- MySQL 特有语句形式，例如 `REPLACE INTO`、`INSERT IGNORE`、`ON DUPLICATE KEY UPDATE`、`INSERT ... SET`、`LIMIT`、SQL 级预处理语句和 `@` 用户变量；
- 日期、字符串、数值、加密、流程控制和聚合函数；
- 比较、逻辑和位运算操作符；
- MySQL 模式下的 `CREATE SCHEMA`、`DROP SCHEMA`，以及标准 MySQL 客户端和驱动。

完整的官方页面见：[SQL 语法](https://doc.halodbtech.com/multi-mode-compatibility/mysql/sql-syntax)、[数据类型](https://doc.halodbtech.com/multi-mode-compatibility/mysql/data-types)、[函数](https://doc.halodbtech.com/multi-mode-compatibility/mysql/functions)、[操作符](https://doc.halodbtech.com/multi-mode-compatibility/mysql/operators)和[其他兼容特性](https://doc.halodbtech.com/multi-mode-compatibility/mysql/misc-features)。

## MySQL 应用如何连接 {#connection-model}

MySQL 端点使用标准 MySQL 协议。在 Halo 16 的官方配置中，`cluster_net_services` 分配 MySQL 监听端口，`mysql.default_tenant` 指定默认数据库，并在运行 MySQL 兼容语法的数据库中安装 `aux_mysql`。具体顺序见[配置并连接](/openhalo/mysql-configuration/)。

官方文档把 MySQL 模式下的 `CREATE SCHEMA` 和 `DROP SCHEMA` 作为 MySQL 数据库操作。底层服务器仍然是 PostgreSQL 派生系统，因此数据库名、schema、角色、权限、事务行为和类型边界都应在确切的 Halo 版本上验证。

## 版本边界 {#version-boundary}

本栏目中的 OpenHalo 源码材料固定在 [`90fc8d7`](https://github.com/HaloTech-Co-Ltd/openHalo/tree/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c)。官方兼容参考针对 Halo Database 1.0.16。Halo Database 的配置示例不能证明同名参数一定存在于开源版本；旧版 OpenHalo 测试结果也不能当作当前 Halo Database 的完整支持矩阵。

兼容目标是常见应用行为，并不承诺所有 MySQL 管理命令、存储引擎功能、优化器提示、导出功能、存储程序或客户端扩展都可用。切换生产流量前，应在确切的服务端版本上运行应用的 schema、迁移、查询、事务、驱动和运维任务。

独立测试证据及其限制见[已知兼容边界](/openhalo/mysql-compatibility-gaps/)。

## 资料来源 {#sources}

本页为 [Halo Database MySQL 兼容参考](https://doc.halodbtech.com/multi-mode-compatibility/mysql)的原创摘要。上游未明确公开文档许可证；版本、版权与引用方式见[来源说明](/attribution/#halodb)。
