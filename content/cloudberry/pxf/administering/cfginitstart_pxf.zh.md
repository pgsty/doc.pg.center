---
title: "启动、停止和重启 PXF"
description: "启动、停止和重启 PXF 服务。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/cfginitstart_pxf.md"
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


PXF 提供两个管理命令：

- [`pxf cluster`](/cloudberry/pxf/ref/pxf-cluster/) - 管理 Apache Cloudberry 集群中的所有 PXF Service 实例
- [`pxf`](/cloudberry/pxf/ref/pxf/) - 管理特定 Apache Cloudberry 主机上的 PXF Service 实例

> <b>注意：</b>本主题中的步骤假定你已将 <code>&lt;PXF_INSTALL_DIR>/bin</code> 目录添加到 `$PATH`。


## 启动 PXF {#starting-pxf}

配置 PXF 之后，必须在 Apache Cloudberry 集群的每台主机上启动 PXF。PXF Service 启动后，以 `gpadmin` 用户身份在默认端口 5888 上运行。只有 `gpadmin` 用户可以启动和停止 PXF Service。

如果要更改默认的 PXF 配置，必须在启动 PXF 之前更新配置；如果 PXF 已在运行，则需要重启 PXF。有关用户可自定义的 PXF 配置属性以及配置更新步骤，请参阅[关于 PXF 配置文件](/cloudberry/pxf/administering/configuring/config_files/)。


### 前提条件 {#prerequisites}

在 Apache Cloudberry 集群中启动 PXF 之前，请确保：

- Apache Cloudberry 集群已启动并正在运行。
- 你此前已配置 PXF。
 
### 步骤 {#procedure}

请执行以下步骤，在 Apache Cloudberry 集群的每台主机上启动 PXF。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

3. 运行 `pxf cluster start` 命令，在每台主机上启动 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster start
    ```

## 停止 PXF {#stopping-pxf}

如果必须停止 PXF（例如升级 PXF 时），则必须在 Apache Cloudberry 集群的每台主机上停止 PXF。只有 `gpadmin` 用户可以停止 PXF Service。

### 前提条件 {#prerequisites-1}

在 Apache Cloudberry 集群中停止 PXF 之前，请确保 Apache Cloudberry 集群已启动并正在运行。
 
### 步骤 {#procedure-1}

请执行以下步骤，在 Apache Cloudberry 集群的每台主机上停止 PXF。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

3. 运行 `pxf cluster stop` 命令，在每台主机上停止 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster stop
    ```

## 重启 PXF {#restarting-pxf}

如果必须重启 PXF（例如更新了 `$PXF_BASE/conf` 中的 PXF 用户配置文件），可运行 `pxf cluster restart`，在 Apache Cloudberry 集群的所有主机上先停止再启动 PXF。

只有 `gpadmin` 用户可以重启 PXF Service。

### 前提条件 {#prerequisites-2}

在 Apache Cloudberry 集群中重启 PXF 之前，请确保 Apache Cloudberry 集群已启动并正在运行。
 
### 步骤 {#procedure-2}

请执行以下步骤，在 Apache Cloudberry 集群中重启 PXF。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster restart
    ```
