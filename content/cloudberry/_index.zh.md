---
title: "Apache Cloudberry 2.x 文档"
linkTitle: "Cloudberry"
description: "Apache Cloudberry（孵化中）2.x 构建、部署、数据加载、查询、调优、安全与运维文档。"
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 70
icon: fa-solid fa-cubes-stacked
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
module: [CLOUDBERRY]
categories: [概念]
upstream_source: cloudberry
search_keywords: [Greenplum, MPP, CBDB, "2.2.0", gpdb]
upstream_link: "https://github.com/apache/cloudberry-site/tree/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x"
cascade:
  upstream_source: cloudberry
  type: docs
  module: [CLOUDBERRY]
---

Apache Cloudberry（孵化中）是一个开源的大规模并行处理（MPP）数据库，源自 Greenplum Database 7，
2.2.0-incubating 版本采用 PostgreSQL 14.10 内核，2.0 与 2.1 版本采用 PostgreSQL 14.4。Coordinator 接收客户端连接并派发查询，各个 Segment 存储数据并并行执行各自承担的查询部分。

本文档集对应上游 2.x 文档，覆盖当前的
[2.2.0-incubating](https://cloudberry.apache.org/releases/2.2.0-incubating) 版本。可以先阅读
[功能概览](/cloudberry/introduction/cbdb-overview/)和
[架构](/cloudberry/introduction/cbdb-architecture/)，体验
[沙箱环境](/cloudberry/build/sandbox/)，或规划[生产部署](/cloudberry/deployment/)。
SQL 语法、工具、配置参数和系统目录见[参考手册](/cloudberry/reference/)。

上游网站另行发布两部相关手册：
[平台扩展框架（PXF）](/cloudberry/pxf/)与
[Apache Cloudberry 内核原理](/cloudberry/core-internals/)。
