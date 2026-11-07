---
title: PolarDB 文档
description: 从部署实例到日常运维，按任务阅读 PolarDB PostgreSQL 的功能与架构文档。
type: docs
icon: fa-solid fa-cloud
weight: -90
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
outputs:
- HTML
- RSS
- print
- markdown
- LLMSFULL
cascade:
  type: docs
  upstream_source: polardb
upstream_source: polardb
upstream_link: https://github.com/polardb/polardb-pg-docs/tree/b4733b0350888242afeba432a6837458c348a937
linkTitle: PolarDB
---


PolarDB for PostgreSQL 是阿里云研发的数据库，采用存储计算分离架构。本手册整理上游的部署、使用与内核资料；先选择与你当前任务对应的入口。

- [部署指南](/zh/polardb/deploying/)
  从 Docker 体验开始，进一步部署本地文件系统或 PFS 集群。
- [使用与运维](/zh/polardb/operation/)
  备份恢复、计算与存储扩容、问题诊断、性能测试。
- [功能参考](/zh/polardb/features/)
  高性能、高可用、安全、ePQ 与第三方扩展。
- [架构与原理](/zh/polardb/theory/)
  共享存储、HTAP、缓冲区、DDL 同步和 LogIndex。
- [上手开发](/zh/polardb/development/)
  配置容器开发环境，编译和调试数据库内核。
- [参与社区](/zh/polardb/contributing/)
  贡献代码和文档，提交问题，了解编码规范。
{.cards columns=2}

## 第一次使用 {#first-steps}

1. 阅读[架构简介](/zh/polardb/deploying/introduction/)，理解计算节点与共享存储的关系。
2. 跟随[快速部署](/zh/polardb/deploying/quick-start/)，用 Docker 启动体验实例。
3. 在[进阶部署](/zh/polardb/deploying/deploy/)中选择本地存储或共享存储路径。
4. 部署完成后，查看[备份恢复](/zh/polardb/operation/backup-and-restore/)与[计算节点扩缩容](/zh/polardb/operation/scale-out/)。
{.steps}

## 使用这份手册 {#reading}

右上角搜索支持中文、功能名与参数名。文章提供目录、代码复制、图片放大、Markdown 导出和整节打印；存在中英文原文的文章还可以使用双语对照阅读。

版本徽章沿用上游定义，例如 `V11 / v1.1.17-`。功能适用范围、参数默认值和命令应以具体文章所述版本为准。[历史版本规划](/zh/polardb/roadmap/)保留了上游当时的计划。

本手册来源于 [polardb/polardb-pg-docs](https://github.com/polardb/polardb-pg-docs)，版权归 **Alibaba Group, Inc.** 等原权利人所有，按 **Apache License 2.0** 发布。每篇文章页尾可回到对应原文；完整信息见[版权与来源](/zh/polardb/site/attribution/)。
