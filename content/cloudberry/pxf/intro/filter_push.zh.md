---
title: "PXF 过滤条件下推概述"
description: "PXF 如何将查询过滤条件下推到外部数据源。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/intro/filter_push.md"
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

PXF 支持过滤条件下推。启用过滤条件下推后，可以提取 `SELECT` 查询 `WHERE` 子句中的约束条件，并将其传递给外部数据源进行过滤。这一过程可以提升查询性能，也可以减少传输到 Apache Cloudberry 的数据量。

您可以通过设置 `gp_external_enable_filter_pushdown` 服务器配置参数，为包括 `pxf` 在内的所有外部表协议启用或停用过滤条件下推。该配置参数的默认值为 `on`；将其设置为 `off` 即可停用过滤条件下推。例如：

```sql
SHOW gp_external_enable_filter_pushdown;
SET gp_external_enable_filter_pushdown TO 'on';
```

**注意：** 某些外部数据源不支持过滤条件下推。此外，某些数据类型或运算符也可能不支持过滤条件下推。如果查询访问的数据源不支持对该查询的约束条件进行过滤条件下推，则查询会在不使用过滤条件下推的情况下运行（数据在传输到 Apache Cloudberry 之后才会被过滤）。

PXF 过滤条件下推可用于以下数据类型（取决于具体的连接器和 profile）：

- `INT2`、`INT4`、`INT8`
- `CHAR`、`TEXT`、`VARCHAR`
- `FLOAT`
- `NUMERIC`（访问 `STORED AS Parquet` 时，`hive` profile 不可用）
- `BOOL`
- `DATE`、`TIMESTAMP`（仅适用于 JDBC 连接器、使用 S3 Select 时的 S3 连接器、`hive:rc` 和 `hive:orc` profile，以及访问 `STORED AS` `RCFile` 或 `ORC` 时的 `hive` profile）

PXF 通过不同连接器暴露的 profile 访问数据源，过滤条件下推的支持情况由具体的连接器实现决定。
下列 PXF profile 支持过滤条件下推的某些方面，以及不同的算术和逻辑运算：

|Profile | `<`, `>`, `<=`, `>=`, `=`, `<>` | LIKE | IS [NOT] NULL | IN | AND | OR | NOT |
|-------|:------------------------:|:----:|:----:|:----:|:----:|:----:|:----:|
| jdbc | Y | Y<sup>4</sup> | Y | N | Y | Y | Y | 
| *:parquet | Y<sup>1</sup> | N | Y<sup>1</sup> | Y<sup>1</sup> | Y<sup>1</sup> | Y<sup>1</sup> | Y<sup>1</sup> |
| *:orc (all except hive:orc) | Y<sup>1,3</sup> | N | Y<sup>1,3</sup> | Y<sup>1,3</sup> | Y<sup>1,3</sup> | Y<sup>1,3</sup> | Y<sup>1,3</sup> |
| s3:parquet and s3:text with S3-Select | Y |  N | Y | Y | Y | Y | Y |
| hbase | Y | N | Y | N | Y | Y | N |
| hive:text | Y<sup>2</sup> | N | N | N | Y<sup>2</sup> | Y<sup>2</sup> | N |
| hive:rc, hive (accessing stored as RCFile) | Y<sup>2</sup> |  N | Y | Y | Y, Y<sup>2</sup> | Y, Y<sup>2</sup> | Y |
| hive:orc, hive (accessing stored as ORC) | Y, Y<sup>2</sup> |  N | Y | Y | Y, Y<sup>2</sup> | Y, Y<sup>2</sup> | Y |
| hive (accessing stored as Parquet) | Y, Y<sup>2</sup> | N | N | Y | Y, Y<sup>2</sup> | Y, Y<sup>2</sup> | Y |
| hive:orc and VECTORIZE=true | Y<sup>2</sup> |  N | N | N | Y<sup>2</sup> | Y<sup>2</sup> | N |

<br/><sup>1</sup>&nbsp;由 PXF 而不是远端系统应用谓词，从而降低 CPU 使用率和内存占用。
<br/><sup>2</sup>&nbsp;PXF 支持基于分区键的分区裁剪。
<br/><sup>3</sup>&nbsp;PXF 的过滤基于文件级、条带级和行级 ORC 统计信息。
<br/><sup>4</sup>&nbsp;PXF `jdbc` profile 仅对 `TEXT` 字段支持 `LIKE` 运算符。

对于上表中未提及的任何 profile，PXF 均不支持过滤条件下推，包括：`*:avro`、`*:AvroSequenceFile`、`*:SequenceFile`、`*:json`、`*:text`、`*:csv`、`*:fixedwidth` 和 `*:text:multi`。

总之，必须同时满足以下所有条件，才会发生过滤条件下推：

* 您通过将 `gp_external_enable_filter_pushdown` 服务器配置参数设置为 `'on'`，启用了外部表过滤条件下推。
* 您用来访问外部数据源的 Apache Cloudberry 协议必须支持过滤条件下推。`pxf` 外部表协议支持下推。
* 您访问的外部数据源必须支持下推。例如，HBase 和 Hive 支持下推。
* 对于在使用 `pxf` 协议创建的外部表上执行的查询，底层的 PXF 连接器也必须支持过滤条件下推。例如，PXF Hive、HBase 和 JDBC 连接器支持下推，支持读取 ORC 和 Parquet 数据的 PXF 连接器同样如此。
  - 有关 Hive 对该特性的支持的更多信息，请参阅 Hive [分区裁剪](/cloudberry/pxf/access-hadoop/hive_pxf/#partition-pruning)。
