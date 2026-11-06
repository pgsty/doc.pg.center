---
title: "日志"
description: "配置 PXF 服务日志。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/advanced-config/cfg_logging.md"
---

PXF 提供两类消息日志：服务级日志和客户端级日志。

PXF 自行管理其服务级日志，并支持以下日志级别（按严重程度从高到低排列）：

- fatal
- error
- warn
- info
- debug
- trace

PXF Service 的默认配置记录 `info` 及更严重级别的日志。对于某些第三方库，PXF Service 仅记录 `warn` 或 `error` 及更严重级别的日志，以减少输出量。

- PXF 会捕获写入 `stdout` 和 `stderr` 的消息，并将其写入 `$PXF_LOGDIR/pxf-app.out` 文件。该文件可能包含 PXF 在日志完全配置好之前记录的服务启动消息，也可能包含调试输出。
- PXF 在启动之后记录的消息会写入 `$PXF_LOGDIR/pxf-service.log` 文件。

您可以根据需要更改 PXF 日志目录。

客户端级日志由 Apache Cloudberry 客户端管理；本主题详细介绍如何为 `psql` 客户端配置日志。

为 PXF 启用更详细的服务级或客户端级日志有助于故障排查。

## 配置日志目录 {#configuring-the-log-directory}

PXF 默认的日志配置会将日志消息写入 `$PXF_LOGDIR`，其中默认日志目录为 `PXF_LOGDIR=$PXF_BASE/logs`。

要更改 PXF 日志目录，您必须更新 `pxf-env.sh` 配置文件中的 `$PXF_LOGDIR` 属性，将配置更改同步到 Apache Cloudberry 集群，然后重启 PXF。

**注意：** 新的日志目录必须存在于所有 Apache Cloudberry 主机上，并且 `gpadmin` 用户必须能够访问。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 使用文本编辑器取消 `$PXF_BASE/conf/pxf-env.sh` 中 `export PXF_LOGDIR` 行的注释，并将其值替换为新的 PXF 日志目录。例如：

    ```xml
    # Path to Log directory
    export PXF_LOGDIR="/new/log/dir"
    ```

2. 使用 `pxf cluster sync` 命令，将更新后的 `pxf-env.sh` 文件复制到 Apache Cloudberry 集群中的所有主机：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

3. 按照[重启 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#restarting-pxf)中的说明，在每台 Apache Cloudberry 主机上重启 PXF。

## 配置服务级日志 {#configuring-service-level-logging}

PXF 使用 Apache Log4j 2 记录服务级日志。与 PXF Service 相关的日志消息会被捕获到 `$PXF_LOGDIR/pxf-app.out` 和 `$PXF_LOGDIR/pxf-service.log` 中。PXF Service 的默认配置记录 `info` 及更严重级别的日志。

您可以只更改单台 Apache Cloudberry 主机上 PXF Service 的日志级别，也可以更改 Apache Cloudberry 集群中所有主机上的日志级别。

> <b>注意：</b>启用 `debug` 和 `trace` 日志级别后，PXF 会提供更详细的日志。这些级别的日志输出量很大，会对性能和存储产生影响。收集到所需信息后，请务必将其关闭。

### 为特定主机配置 {#configuring-for-a-specific-host}

您可以通过两种方式更改运行在特定 Apache Cloudberry 主机上的 PXF Service 的日志级别：

- 在 `pxf restart` 命令行上设置 `PXF_LOG_LEVEL` 环境变量。
- 通过更新属性来设置日志级别。

**步骤**：

1. 登录 Apache Cloudberry 主机：

    ```shell
    $ ssh gpadmin@<gphost>
    ```

1. 选择以下方法之一：
    - 在 `pxf restart` 命令行上设置日志级别。例如，将日志级别从 `info`（默认值）更改为 `debug`：

        ```shell
        gpadmin@gphost$ PXF_LOG_LEVEL=debug pxf restart
        ```
    - 在 `pxf-application.properties` 文件中设置日志级别：
        1. 使用文本编辑器取消 `$PXF_BASE/conf/pxf-application.properties` 文件中以下行的注释，并设置所需的日志级别。例如，将日志级别从 `info`（默认值）更改为 `debug`：

            ```xml
            pxf.log.level=debug
            ```
        1. 在该主机上重启 PXF：

            ```shell
            gpadmin@gphost$ pxf restart
            ```

4. 现在 `debug` 日志已启用。请记下当前时间；该时间可帮助您在 `$PXF_LOGDIR/pxf-service.log` 中定位相关的日志消息。

    ```shell
    $ date
    Wed Oct  4 09:30:06 MDT 2017
    $ psql -d <dbname>
    ```

1. 执行会使用 PXF Service 的操作。

5. 收集并检查 `pxf-service.log` 中的日志消息。

6. 根据最初设置日志级别的方式，在该主机上恢复 `info` 级别的日志：
    - 命令行方式：

        ```shell
        gpadmin@gphost$ pxf restart
        ```
    - 属性文件方式：注释掉该行，或将属性值设回 `info`，然后在该主机上重启 PXF。


### 为整个集群配置 {#configuring-for-the-cluster}

要更改运行在 Apache Cloudberry 集群中每台主机上的 PXF 服务的日志级别：

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

1. 使用文本编辑器取消 `$PXF_BASE/conf/pxf-application.properties` 文件中以下行的注释，并设置所需的日志级别。例如，将日志级别从 `info`（默认值）更改为 `debug`：

    ```xml
    pxf.log.level=debug
    ```

1. 使用 `pxf cluster sync` 命令，将更新后的 `pxf-application.properties` 文件复制到 Apache Cloudberry 集群中的所有主机。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1.  在每台 Apache Cloudberry 主机上重启 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster restart
    ```

1. 执行会使用 PXF Service 的操作，然后收集并检查 `$PXF_LOGDIR/pxf-service.log` 中的信息。

1. 使用 `pxf.log.level=info` 重复上述步骤，恢复 `info` 级别的日志。


## 配置客户端级日志 {#configuring-client-level-logging}

数据库级的客户端会话日志可以帮助您了解 PXF Service 的内部操作。

在 `psql` 会话中将 `client_min_messages` 服务器配置参数设置为 `DEBUG2`，即可启用 Apache Cloudberry 客户端的调试消息日志。该日志配置会将消息写入 `stdout`，并适用于您在该会话中执行的所有操作，包括对 PXF 外部表的操作。例如：

```shell
$ psql -d <dbname>
```

```sql
dbname=# SET client_min_messages=DEBUG2;
dbname=# SELECT * FROM hdfstest;
...
DEBUG2:  churl http header: cell #26: X-GP-URL-HOST: localhost  (seg0 slice1 127.0.0.1:7002 pid=10659)
CONTEXT:  External table pxf_hdfs_textsimple, line 1 of file pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:text
DEBUG2:  churl http header: cell #27: X-GP-URL-PORT: 5888  (seg0 slice1 127.0.0.1:7002 pid=10659)
CONTEXT:  External table pxf_hdfs_textsimple, line 1 of file pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:text
DEBUG2:  churl http header: cell #28: X-GP-DATA-DIR: data%2Fpxf_examples%2Fpxf_hdfs_simple.txt  (seg0 slice1 127.0.0.1:7002 pid=10659)
CONTEXT:  External table pxf_hdfs_textsimple, line 1 of file pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:text
DEBUG2:  churl http header: cell #29: X-GP-TABLE-NAME: pxf_hdfs_textsimple  (seg0 slice1 127.0.0.1:7002 pid=10659)
CONTEXT:  External table pxf_hdfs_textsimple, line 1 of file pxf://data/pxf_examples/pxf_hdfs_simple.txt?PROFILE=hdfs:text
...
```

收集并检查写入 `stdout` 的日志消息。

**注意**：`DEBUG2` 数据库客户端会话日志会影响性能。收集到所需信息后，请记得关闭 `DEBUG2` 日志。

```sql
dbname=# SET client_min_messages=NOTICE;
```
