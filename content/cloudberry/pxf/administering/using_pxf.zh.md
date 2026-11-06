---
title: "授予用户访问 PXF 的权限"
description: "授予 Apache Cloudberry 用户访问 PXF 的权限。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/using_pxf.md"
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

Apache Cloudberry Platform Extension Framework (PXF) 实现了一个名为 `pxf` 的协议，你可以使用它创建引用外部数据存储中数据的外部表。PXF 协议和 Java 服务被打包为一个 Apache Cloudberry 扩展。

必须在计划使用该框架访问外部数据的每个数据库中启用 PXF 扩展。你还必须显式地将 `pxf` 协议的权限 `GRANT` 给需要访问的用户/角色。

## 在数据库中启用 PXF {#enabling-pxf-in-a-database}

必须在计划使用该扩展的每个 Apache Cloudberry 数据库中显式注册 PXF 扩展。你必须具有 Apache Cloudberry 管理员权限才能注册扩展。

对于要使用 PXF 的**_每个_**数据库，请执行以下步骤：

1. 以 `gpadmin` 用户身份连接到数据库：

    ```shell
    gpadmin@coordinator$ psql -d <dbname> -U gpadmin
    ```

2. 创建 PXF 扩展。你必须具有 Apache Cloudberry 管理员权限才能创建扩展。例如：

    ```sql
    dbname=# CREATE EXTENSION pxf;
    ```

    创建 `pxf` 扩展会注册 `pxf` 协议以及 PXF 访问外部数据所需的调用处理程序。


## 从数据库中注销 PXF {#unregistering-pxf-from-a-database}

当不再需要在特定数据库上使用 PXF 时，必须显式删除该数据库的 PXF 扩展。你必须具有 Apache Cloudberry 管理员权限才能删除扩展。

1. 以 `gpadmin` 用户身份连接到数据库：

    ```shell
    gpadmin@coordinator$ psql -d <dbname> -U gpadmin
    ```

2. 删除 PXF 扩展：

    ```sql
    dbname=# DROP EXTENSION pxf;
    ```

    如果当前定义了任何使用 `pxf` 协议的外部表，`DROP` 命令会失败。如果选择强制删除这些外部表，请添加 `CASCADE` 选项。


## 授予角色访问 PXF 的权限 {#granting-a-role-access-to-pxf}

要使用 PXF 读取外部数据，需要使用 `CREATE EXTERNAL TABLE` 命令创建指定 `pxf` 协议的外部表。必须专门将 `pxf` 协议的 `SELECT` 权限授予所有需要此类访问权限的非 `SUPERUSER` Apache Cloudberry 角色。

要授予特定角色对 `pxf` 协议的访问权限，请使用 `GRANT` 命令。例如，要授予名为 `bill` 的角色对使用 `pxf` 协议创建的外部表所引用数据的读取权限：

```sql
GRANT SELECT ON PROTOCOL pxf TO bill;
```

要使用 PXF 向外部数据存储写入数据，需要使用 `CREATE WRITABLE EXTERNAL TABLE` 命令创建指定 `pxf` 协议的外部表。必须专门将 `pxf` 协议的 `INSERT` 权限授予所有需要此类访问权限的非 `SUPERUSER` Apache Cloudberry 角色。例如：

```sql
GRANT INSERT ON PROTOCOL pxf TO bill;
```
