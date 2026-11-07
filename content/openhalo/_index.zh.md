---
type: docs
upstream_source: openhalo
upstream_link: https://github.com/HaloTech-Co-Ltd/openHalo/blob/90fc8d777c3f111d4c8d236625bb15b5d4b19d7c/README.md
title: OpenHalo 文档
linkTitle: OpenHalo
description: 在 PostgreSQL 上使用 MySQL 协议与 SQL 兼容能力：配置、语法、数据类型与迁移边界。
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

OpenHalo 使 PostgreSQL 能够运行原本面向 MySQL 编写的应用。上游项目旨在减少应用迁移所需的修改，并改善查询性能。

迁移旧 MySQL 数据库可能耗时且需要较多资源。[HMT](https://github.com/HaloLab001/hmt-web) 是 HaloLab 开源的迁移工具，可以自动迁移数据库模式和数据；但迁移应用时，通常仍需要重写与数据库交互的代码。

OpenHalo 支持 MySQL 的 SQL 方言和通信协议，让原本面向 MySQL 的应用只需较少代码修改即可运行。因此，从 MySQL 5.7 及更新版本迁入时，需要修改的应用代码可以减少，进而缩短迁移时间、降低风险与成本。

IMT Atlantique 的学生团队维护了 [OpenHalo 兼容性测试与性能基准项目](https://github.com/fxcollot/openHaloDocumentation)。Halo Database 1.0.16 官方手册还提供了专门的 [MySQL 兼容参考](https://doc.halodbtech.com/multi-mode-compatibility/mysql)。

## 优势 {#benefits}

### 减少迁移时间与风险 {#migration}

OpenHalo 支持常用的 MySQL 方言和语义，减少与数据库调用有关的代码修改，也降低修改应用时引入新错误的风险。

### 改善性能 {#performance}

上游指出，OpenHalo 无需额外操作或费用即可改善性能，尤其是复杂 SQL 语句的性能。

### 按自己的节奏迁移 {#pace}

OpenHalo 支持常用的 MySQL 查询工具、命令和驱动程序，可以继续使用熟悉的工具。

## 工作原理 {#how-it-works}

OpenHalo 支持常用的 MySQL SQL 方言与通信协议。旧应用可以像连接 MySQL 一样连接 OpenHalo，无需大规模重写代码。

![OpenHalo 协议架构](/openhalo/assets/how-it-works.png)

[编译与配置 OpenHalo](/openhalo/quick-start/)。

## MySQL 兼容参考 {#mysql-compatibility}

如果目标是让现有 MySQL 应用通过 OpenHalo 或 Halo Database 运行，请从以下页面开始：

- [MySQL 兼容](/openhalo/mysql-compatibility/)
- [配置与连接](/openhalo/mysql-configuration/)
- [兼容的 MySQL 语句](/openhalo/mysql-statements/)
- [兼容的 MySQL 数据类型](/openhalo/mysql-data-types/)
- [已知兼容边界](/openhalo/mysql-compatibility-gaps/)

{.cards}
