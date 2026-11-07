---
title: "Platform Extension Framework (PXF) for Apache Cloudberry"
linkTitle: "PXF"
description: "Apache Cloudberry Platform Extension Framework documentation index."
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

The Apache Cloudberry Platform Extension Framework (PXF) provides parallel, high throughput data access and federated queries across heterogeneous data sources via built-in connectors that map an Apache Cloudberry external table definition to an external data source. PXF has its roots in the Apache HAWQ project.

[Apache Cloudberry PXF](https://github.com/apache/cloudberry-pxf) is derived from the now-archived [`greenplum-db/pxf-archive`](https://github.com/greenplum-db/pxf-archive) project (at version 6.10.1-SNAPSHOT). It has been extensively customized and optimized for Apache Cloudberry, and now evolves independently with its own release cadence.

> [!NOTE]
> This documentation is derived from the original `greenplum-db/pxf-archive` 6.10.1 documentation. Content has been added, revised, and removed to reflect the actual behavior of Apache Cloudberry PXF.

-  [Overview of PXF](/cloudberry/pxf/overview_pxf/)
-  [Transitioning to Apache Cloudberry](/cloudberry/pxf/transition_to_cloudberry/)
-   [Introduction to PXF](/cloudberry/pxf/intro/)
    This topic introduces PXF concepts and usage.
-   [Administering PXF](/cloudberry/pxf/administering/configuring/about_pxf_dir/)
    This set of topics details the administration of PXF including configuration and management procedures.
-   [Accessing Hadoop with PXF](/cloudberry/pxf/access-hadoop/)
    This set of topics describe the PXF Hadoop connectors, the data types they support, and the profiles that you can use to read from and write to HDFS.
-   [Accessing Azure, Google Cloud Storage, and S3-Compatible Object Stores with PXF](/cloudberry/pxf/access-objectstores/)
    This set of topics describe the PXF object storage connectors, the data types they support, and the profiles that you can use to read data from and write data to the object stores.
-   [Accessing an SQL Database with PXF (JDBC)](/cloudberry/pxf/access-jdbc/)
    This topic describes how to use the PXF JDBC connector to read from and write to an external SQL database such as Postgres or MySQL.
-   [Accessing Files on a Network File System with PXF](/cloudberry/pxf/access-nfs/)
    This topic describes how to use PXF to access files on a network file system that is mounted on your Apache Cloudberry hosts.
-   [Troubleshooting PXF](/cloudberry/pxf/troubleshooting/)
    This topic details the service-level and database-level logging configuration procedures for PXF. It also identifies some common PXF errors and describes how to address PXF memory issues.
-   [PXF Utility Reference](/cloudberry/pxf/ref/)
    The PXF utility reference.
