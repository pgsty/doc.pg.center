---
title: "Apache Cloudberry 平台扩展框架（PXF）"
linkTitle: "PXF"
description: "Apache Cloudberry 平台扩展框架文档索引。"
weight: 140
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/index.md"
type: "docs"
section_index: "cards"
outputs: ["HTML", "RSS", "print", "markdown"]
upstream_source: "pxf"
cascade: {"type": "docs", "upstream_source": "pxf"}
sidebar_root_menu: false
icon: fa-solid fa-plug
---

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

Apache Cloudberry 平台扩展框架（Platform Extension Framework，PXF）通过内置连接器，将 Apache Cloudberry 外部表定义映射到外部数据源，从而提供并行、高吞吐的数据访问能力，并支持跨异构数据源的联邦查询。PXF 源自 Apache HAWQ 项目。

[Apache Cloudberry PXF](https://github.com/apache/cloudberry-pxf) 派生自现已归档的 [`greenplum-db/pxf-archive`](https://github.com/greenplum-db/pxf-archive) 项目（版本为 6.10.1-SNAPSHOT）。它针对 Apache Cloudberry 进行了大量定制和优化，现已独立演进，并拥有自己的发布节奏。

> [!NOTE]
> 本文档派生自原 `greenplum-db/pxf-archive` 6.10.1 版本的文档，并经过增补、修订和删减，以反映 Apache Cloudberry PXF 的实际行为。

-  [PXF 概述](/cloudberry/pxf/overview_pxf/)
-  [迁移到 Apache Cloudberry](/cloudberry/pxf/transition_to_cloudberry/)
-   [PXF 简介](/cloudberry/pxf/intro/)
    本主题介绍 PXF 的概念和用法。
-   [管理 PXF](/cloudberry/pxf/administering/configuring/about_pxf_dir/)
    这组主题详细介绍 PXF 的管理，包括配置和管理流程。
-   [使用 PXF 访问 Hadoop](/cloudberry/pxf/access-hadoop/)
    这组主题介绍 PXF 的 Hadoop 连接器、其支持的数据类型，以及可用于读写 HDFS 的 profile。
-   [使用 PXF 访问 Azure、Google Cloud Storage 和兼容 S3 的对象存储](/cloudberry/pxf/access-objectstores/)
    这组主题介绍 PXF 的对象存储连接器、其支持的数据类型，以及可用于从对象存储读取和向对象存储写入数据的 profile。
-   [使用 PXF（JDBC）访问 SQL 数据库](/cloudberry/pxf/access-jdbc/)
    本主题介绍如何使用 PXF JDBC 连接器读取和写入外部 SQL 数据库，例如 Postgres 或 MySQL。
-   [使用 PXF 访问网络文件系统上的文件](/cloudberry/pxf/access-nfs/)
    本主题介绍如何使用 PXF 访问挂载在 Apache Cloudberry 主机上的网络文件系统中的文件。
-   [PXF 故障排查](/cloudberry/pxf/troubleshooting/)
    本主题详细介绍 PXF 服务级和数据库级日志的配置流程，同时列出一些常见的 PXF 错误，并说明如何处理 PXF 内存问题。
-   [PXF 实用程序参考](/cloudberry/pxf/ref/)
    PXF 实用程序参考。
