---
title: "关于配置文件"
description: "PXF 配置文件参考。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/configuring/config_files.md"
---

`$PXF_BASE/conf` 包含以下用户可自定义的配置文件：

- `pxf-application.properties` - PXF Service 应用程序配置属性
- `pxf-env.sh` - PXF 命令和 JVM 特定的运行时配置属性
- `pxf-log4j2.xml` - PXF 日志配置属性
- `pxf-profiles.xml` - 自定义 PXF Profile 定义


## 修改 PXF 配置 {#modifying-the-pxf-configuration}

更新 PXF 配置文件后，必须将更改同步到 Apache Cloudberry 集群中的所有主机，然后重启 PXF，更改才会生效。

步骤：

1. 更新相关的配置文件。

1. 将 PXF 配置同步到 Apache Cloudberry 集群中的所有主机：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

1. 在所有 Apache Cloudberry 主机上（重新）启动 PXF：

    ```shell
    gpadmin@coordinator$ pxf cluster restart
    ```


## pxf-application.properties {#pxf-applicationproperties}

`pxf-application.properties` 文件提供以下 PXF Service 应用程序配置属性：

| 参数 | 说明 | 默认值 |
|-----------|---------------| ------------|
| pxf.connection.timeout | Tomcat 服务器读取操作的连接超时时间（-1 表示无限超时）。 | 5m（5 分钟） |
| pxf.connection.upload-timeout | Tomcat 服务器写入操作的连接超时时间（-1 表示无限超时）。 | 5m（5 分钟） |
| [pxf.max.threads](/cloudberry/pxf/administering/advanced-config/cfg_mem/#another-option-for-resource-constrained-pxf-segment-hosts) | PXF Tomcat 线程的最大数量。 | 200 |
| pxf.task.pool.allow&#8209;core&#8209;thread&#8209;timeout | 标识是否允许核心流式处理线程超时。 | false |
| pxf.task.pool.core-size | 核心流式处理线程的数量。 | 8 |
| pxf.task.pool.queue-capacity | 核心流式处理线程池队列的容量。 | 0 |
| pxf.task.pool.max-size | 允许的核心流式处理线程的最大数量。 | 若已设置则为 pxf.max.threads，否则为 200 |
| [pxf.log.level](/cloudberry/pxf/administering/advanced-config/cfg_logging/) | PXF Service 的日志级别。 | info  |
| pxf.fragmenter-cache.expiration | 片段缓存中的条目过期并被移除所需经过的时间。 | 10s（10 秒） |
| [server.address](/cloudberry/pxf/administering/advanced-config/cfghostport/) | PXF 服务器的监听地址。 | localhost |

要更改 PXF Service 应用程序属性的值，可能需要先在 `pxf-application.properties` 文件中添加该属性或取消其注释，然后才能设置新值。


## pxf-env.sh {#pxf-envsh}

`pxf-env.sh` 文件提供以下 PXF JVM 配置属性：

| 参数 | 说明 | 默认值 |
|-----------|---------------| ------------|
| [JAVA_HOME](/cloudberry/pxf/administering/configuring/)    | Java JRE 主目录的路径。 | `/usr/java/default` |
| [PXF_LOGDIR](/cloudberry/pxf/administering/advanced-config/cfg_logging/#configuring-the-log-directory)   | PXF 日志目录。 | `$PXF_BASE/logs` |
| PXF_RUNDIR   | PXF 运行目录。 | `$PXF_BASE/run` |
| [PXF_JVM_OPTS](/cloudberry/pxf/administering/advanced-config/cfg_mem/#increasing-the-jvm-memory-for-pxf)  | PXF Java 虚拟机的默认选项。 | `-Xmx2g -Xms1g` |
| [PXF_OOM_KILL](/cloudberry/pxf/administering/advanced-config/cfg_mem/#configuring-out-of-memory-condition-actions)  | 启用/停用 PXF 在发生 OutOfMemoryError (OOM) 时的自动终止。 | `true (activated)` |
| [PXF_OOM_DUMP_PATH](/cloudberry/pxf/administering/advanced-config/cfg_mem/#configuring-out-of-memory-condition-actions)  | PXF 在发生 OOM 时生成的转储文件的绝对路径。 | 无转储文件（空） |
| [PXF_LOADER_PATH](/cloudberry/pxf/administering/reg_jar_depend/)  | 供 PXF 进行类加载的其他目录和 JAR。 | （空） |
| [LD_LIBRARY_PATH](/cloudberry/pxf/administering/reg_jar_depend/)  | 供 PXF 加载的其他目录和原生库。 | （空） |

要为 PXF JVM 配置属性设置新值，可能需要先在 `pxf-env.sh` 文件中取消该属性的注释，然后才能设置新值。


## pxf-log4j2.xml {#pxf-log4j2xml}

`pxf-log4j2.xml` 文件配置 PXF 及其子组件的日志。默认情况下，PXF 配置为以 `info` 级别记录日志，并对某些第三方库以 `warn` 或 `error` 级别记录日志，以减少冗余输出。

[日志](/cloudberry/pxf/administering/advanced-config/cfg_logging/)高级配置主题介绍了如何为 PXF 启用更详细的客户端级别和服务器级别日志。

## pxf-profiles.xml {#pxf-profilesxml}

PXF 在 [`pxf-profiles-default.xml`](https://github.com/apache/cloudberry-pxf/blob/main/server/pxf-service/src/main/resources/pxf-profiles-default.xml) 文件中定义其默认 Profile。如果选择添加自定义 Profile，请在 `pxf-profiles.xml` 中配置该 Profile。
