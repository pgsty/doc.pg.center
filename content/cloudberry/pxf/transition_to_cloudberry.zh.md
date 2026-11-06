---
title: "迁移到 Apache Cloudberry（孵化中）"
description: "关于将 PXF 的使用从早期基于 Greenplum 的部署迁移到 Apache Cloudberry 的说明。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/transition_to_cloudberry.md"
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

PXF 项目迁移到 **Apache Cloudberry（孵化中）**，涉及一次重大的品牌重塑。作为这次迁移的一部分，Java 包命名空间已从 `org.greenplum` 更改为 `org.apache.cloudberry`。

这是一项面向用户的破坏性变更。如果您在 `$PXF_BASE/conf` 目录中自定义了 PXF 配置文件，则必须手动更新这些文件，以使用新的包名。

## 必需的配置更新 {#required-configuration-updates}

### Profile 配置（`pxf-profiles-default.xml`） {#profile-configurations-pxf-profiles-defaultxml}

PXF 使用 profile 来定义如何访问不同的数据源。这些 profile 指定了分片器（fragmenter）、访问器（accessor）和解析器（resolver）所用的 Java 类。

**需要执行的操作**：如果您在 `pxf-profiles-default.xml` 或 `conf` 目录中的其他 `.xml` 文件里创建了自定义 profile，或覆盖了默认 profile，则必须将所有出现的 `org.greenplum.pxf` 替换为 `org.apache.cloudberry.pxf`。

**示例**：
旧配置：
```xml
<fragmenter>org.greenplum.pxf.plugins.hdfs.HdfsDataFragmenter</fragmenter>
```
新配置：
```xml
<fragmenter>org.apache.cloudberry.pxf.plugins.hdfs.HdfsDataFragmenter</fragmenter>
```

### 日志配置（`pxf-log4j2.xml`） {#logging-configuration-pxf-log4j2xml}

日志配置使用包名来定义日志记录器及其级别。

**需要执行的操作**：更新您的 `$PXF_BASE/conf/pxf-log4j2.xml` 文件，使用新的日志记录器名称。

**示例**：
旧配置：
```xml
<Logger name="org.greenplum.pxf" level="${env:PXF_LOG_LEVEL:-${spring:pxf.log.level}}"/>
```
新配置：
```xml
<Logger name="org.apache.cloudberry.pxf" level="${env:PXF_LOG_LEVEL:-${spring:pxf.log.level}}"/>
```

### 现有外部表 {#existing-external-tables}

如果您创建的外部表在 `LOCATION` 子句中显式指定了类名（使用 `&FRAGMENTER=...`、`&ACCESSOR=...` 或 `&RESOLVER=...`），则这些表在更新为使用新包名之前都会失败。

**需要执行的操作**：删除并重新创建所有引用 `org.greenplum` 命名空间中类的外部表。

**示例**：
旧 DDL：
```sql
CREATE EXTERNAL TABLE my_table (...)
LOCATION ('pxf://path/to/data?FRAGMENTER=org.greenplum.pxf.api.examples.DemoFragmenter&...')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```
新 DDL：
```sql
CREATE EXTERNAL TABLE my_table (...)
LOCATION ('pxf://path/to/data?FRAGMENTER=org.apache.cloudberry.pxf.api.examples.DemoFragmenter&...')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

> [!NOTE]
> 使用内置 profile 的表（例如 `?PROFILE=hdfs:text`）不需要更改 DDL，前提是 `pxf-profiles-default.xml` 中的底层 profile 定义已经更新。

## 为什么要做这项变更？ {#why-this-change}

这项变更使 PXF 项目符合 **Apache Software Foundation** 的标准和 **Apache Cloudberry** 的品牌规范。使用 `org.apache.cloudberry` 命名空间可确保与其他 Apache 项目保持一致，并体现该项目的新归属。
