---
title: "注册库依赖"
description: "向 PXF 注册 JAR 依赖。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/reg_jar_depend.md"
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

你使用 PXF 访问存储在外部系统上的数据。根据外部数据存储的不同，这种访问可能需要为该外部数据存储安装和/或配置其他组件或服务。

PXF 依赖这些附加组件提供的 JAR 文件和其他配置信息。在大多数情况下，PXF 会根据你使用的连接器按需管理内部 JAR 依赖。

如果需要向 PXF 注册 JAR 或原生库依赖，可以将库复制到 PXF 已知的位置，*或者*告知 PXF 一个自定义位置，然后必须同步并重启 PXF。


## 注册 JAR 依赖 {#registering-a-jar-dependency}

PXF 按以下顺序从以下目录加载 JAR 依赖：

1. 你在 `$PXF_BASE/conf/pxf-env.sh` 配置文件的 `PXF_LOADER_PATH` 环境变量中指定的目录。`pxf-env.sh` 文件包含以下被注释掉的代码块：

    ```text
    # Additional locations to be class-loaded by PXF
    # export PXF_LOADER_PATH=
    ```

    你需要取消 `PXF_LOADER_PATH` 设置的注释，并指定一个或多个以冒号分隔的目录名。

2. 默认的 PXF JAR 目录 `$PXF_BASE/lib`。

要为 PXF 添加 JAR 依赖（例如 MySQL 驱动 JAR 文件），必须登录 Apache Cloudberry Coordinator 主机，将 JAR 文件复制到 PXF 用户配置运行时库目录（`$PXF_BASE/lib`），将 PXF 配置同步到 Apache Cloudberry 集群，然后在每台主机上重启 PXF。例如：

```shell
$ ssh gpadmin@<coordinator>
gpadmin@coordinator$ cp new_dependent_jar.jar $PXF_BASE/lib/
gpadmin@coordinator$ pxf cluster sync
gpadmin@coordinator$ pxf cluster restart
```

或者，你也可以在 `pxf-env.sh` 的 `PXF_LOADER_PATH` 环境变量中指定该 JAR 的文件系统位置。如果选择这种注册方式，则必须确保在同步并重启 PXF 之前，将 JAR 文件复制到 Apache Cloudberry Standby Coordinator 主机和 Segment 主机上的相同位置。


## 注册原生库依赖 {#registering-a-native-library-dependency}

PXF 按以下顺序从以下目录加载原生库：

1. 你在 `$PXF_BASE/conf/pxf-env.sh` 配置文件的 `LD_LIBRARY_PATH` 环境变量中指定的目录。`pxf-env.sh` 文件包含以下被注释掉的代码块：

    ```text
    # Additional native libraries to be loaded by PXF
    # export LD_LIBRARY_PATH=
    ```

    你需要取消 `LD_LIBRARY_PATH` 设置的注释，并指定一个或多个以冒号分隔的目录名。

2. 默认的 PXF 原生库目录 `$PXF_BASE/lib/native`。
3. 默认的 Hadoop 原生库目录 `/usr/lib/hadoop/lib/native`。

因此，向 PXF 注册原生库时有三种文件位置选项：

- 仅在 Apache Cloudberry Coordinator 主机上，将库复制到默认的 PXF 原生库目录 `$PXF_BASE/lib/native`。下次同步 PXF 时，PXF 会将该原生库复制到 Apache Cloudberry 集群中的所有主机。
- 在 Apache Cloudberry Coordinator 主机、Standby Coordinator 主机和每台 Segment 主机上，将库复制到默认的 Hadoop 原生库目录 `/usr/lib/hadoop/lib/native`。
- 在 Apache Cloudberry Coordinator 主机、Standby Coordinator 主机和每台 Segment 主机上，将库复制到相同的自定义位置，并取消注释 `pxf-env.sh` 的 `LD_LIBRARY_PATH` 环境变量并向其中添加该目录路径。


### 步骤 {#procedure}

1. 将原生库文件复制到以下位置之一：
    - Apache Cloudberry Coordinator 主机上的 `$PXF_BASE/lib/native` 目录。（你可能需要创建此目录。）
    - 所有 Apache Cloudberry 主机上的 `/usr/lib/hadoop/lib/native` 目录。
    - 所有 Apache Cloudberry 主机上的用户自定义位置；请记下该原生库的文件系统位置。

2. 如果将原生库复制到了自定义位置：

    1. 在你选择的编辑器中打开 `$PXF_BASE/conf/pxf-env.sh` 文件，并取消 `LD_LIBRARY_PATH` 设置的注释：

        ```text
        # Additional native libraries to be loaded by PXF
        export LD_LIBRARY_PATH=
        ```

    2. 在 `LD_LIBRARY_PATH` 环境变量中指定自定义位置。例如，如果将名为 `dependent_native_lib.so` 的库复制到了所有 Apache Cloudberry 主机的 `/usr/local/lib`，则应按如下方式设置 `LD_LIBRARY_PATH`：

        ```shell
        export LD_LIBRARY_PATH=/usr/local/lib
        ```

    3. 保存文件并退出编辑器。

3. 将 PXF 配置从 Apache Cloudberry Coordinator 主机同步到 Standby Coordinator 主机和 Segment 主机。

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

    如果将原生库复制到了 `$PXF_BASE/lib/native` 目录，此命令会将该库复制到 Apache Cloudberry Standby Coordinator 主机和 Segment 主机上的相同位置。

    如果更新了 `pxf-env.sh` 的 `LD_LIBRARY_PATH` 环境变量，此命令会将该配置更改复制到 Apache Cloudberry Standby Coordinator 主机和 Segment 主机。

4. 在所有 Apache Cloudberry 主机上重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster restart
    ```
