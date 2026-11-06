---
title: "Apache Cloudberry 2.x 文档"
linkTitle: "Cloudberry"
description: "Apache Cloudberry（孵化中）2.x 构建、部署、数据加载、查询、调优、安全与运维文档。中文译文准备中。"
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
2.2.0-incubating 版本采用 PostgreSQL 14.10 内核，2.0 与 2.1 版本采用 PostgreSQL 14.4。Coordinator 接收客户端连接并分派查询，各个 Segment 存储数据并并行执行各自承担的查询部分。

本文档集对应上游 2.x 文档，覆盖当前的
[2.2.0-incubating](https://cloudberry.apache.org/releases/2.2.0-incubating) 版本。

> [!NOTE] 中文译文准备中
> 各页面已提供中文标题，正文尚未翻译，每页都附有英文原文链接。可以先从
> <a href="/cloudberry/introduction/cbdb-overview/" hreflang="en" lang="en">功能概览</a>、
> <a href="/cloudberry/introduction/cbdb-architecture/" hreflang="en" lang="en">架构</a>和
> <a href="/cloudberry/reference/" hreflang="en" lang="en">参考</a>的英文版读起。

上游网站另行发布两部相关手册：
[平台扩展框架（PXF）](/cloudberry/pxf/)与
[Apache Cloudberry 内核原理](/cloudberry/core-internals/)。
