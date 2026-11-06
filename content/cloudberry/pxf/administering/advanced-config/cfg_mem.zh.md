---
title: "内存与线程"
description: "配置 PXF 的内存和线程。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/advanced-config/cfg_mem.md"
---

由于单个 PXF Service（JVM）要为 Segment 主机上的多个 Segment 提供服务，PXF 堆大小可能成为运行时的限制因素。在并发工作负载下，或对大文件执行查询时，这一点更为明显。你可能会遇到查询挂起或失败的情况，原因是内存不足，或 Java 垃圾回收影响了响应时间。为避免或解决这些问题，请先尝试增大 Java 最大堆大小，或减少 Tomcat 的最大线程数，具体取决于哪种做法最适合你的系统配置。你也可以将 PXF 配置为在检测到内存不足状况时[自动终止服务器](#auto-terminating-the-pxf-server)（默认已启用）或[转储 Java 堆](#dumping-the-java-heap)。


## 增加 PXF 的 JVM 内存 {#increasing-the-jvm-memory-for-pxf}

在 Apache Cloudberry 主机上运行的每个 PXF Service 都配置了默认的 Java 最大堆大小 2GB 和初始堆大小 1GB。如果 Apache Cloudberry 集群中的主机内存充足，请尝试将最大堆大小增大到 3-4GB 之间的某个值。如有可能，请将初始堆大小和最大堆大小设置为相同的值。

请执行以下步骤，为 Apache Cloudberry 集群中每台主机上运行的 PXF Service 增大堆大小。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 编辑 `$PXF_BASE/conf/pxf-env.sh` 文件。例如：

    ```shell
    gpadmin@coordinator$ vi $PXF_BASE/conf/pxf-env.sh
    ```

3. 在 `pxf-env.sh` 文件中找到 `PXF_JVM_OPTS` 设置，并将 `-Xmx` 和/或 `-Xms` 选项更新为所需的值。例如：

    ```shell
    PXF_JVM_OPTS="-Xmx3g -Xms3g"
    ```

3. 保存文件并退出编辑器。

4. 使用 `pxf cluster sync` 命令将更新后的 `pxf-env.sh` 文件复制到 Apache Cloudberry 集群。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

5. 按照[重启 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#restarting-pxf)中的说明，在每台 Apache Cloudberry 主机上重启 PXF。


## 配置内存不足状况的处理动作 {#configuring-out-of-memory-condition-actions}

在内存不足（OOM）的情况下，PXF 会针对查询返回以下错误：

```text
java.lang.OutOfMemoryError: Java heap space
```

你可以配置 PXF JVM 在检测到 OOM 状况时是否启用以下动作：

- 自动终止 PXF Service（默认启用）。
- 转储 Java 堆（默认停用）。

### 自动终止 PXF 服务器 {#auto-terminating-the-pxf-server}

默认情况下，PXF 的配置是：当 PXF JVM 在某台 Apache Cloudberry 主机上检测到内存不足状况时，会自动运行一个脚本，终止该主机上运行的 PXF Service。`$PXF_BASE/conf/pxf-env.sh` 配置文件中的 `PXF_OOM_KILL` 环境变量控制这一自动终止行为。

启用自动终止后，当 PXF JVM 检测到 OOM 状况并终止主机上的 PXF Service 时：

- PXF 会在 Segment 主机的 `$PXF_LOGDIR/pxf-oom.log` 中记录以下消息：

    ```shell
    =====> <date> PXF Out of memory detected <======
    =====> <date> PXF shutdown scheduled <======
    =====> <date> Stopping PXF <======
    ```

- 在你重启该主机上的 PXF Service 之前，对 PXF 外部表运行的任何查询都会失败，并返回以下错误：

    ```shell
    ... Failed to connect to <host> port 5888: Connection refused
    ```

**当主机上的 PXF Service 以这种方式关闭后，你必须显式重启该主机上的 PXF Service。** 有关 `pxf start` 命令的更多信息，请参阅 [pxf](/cloudberry/pxf/ref/pxf/) 参考页。

有关停用/启用该 PXF 配置属性的说明，请参阅下文的配置[步骤](#procedure)。
 
### 转储 Java 堆 {#dumping-the-java-heap}

在内存不足的情况下，捕获 Java 堆转储可能有助于判断是哪些因素导致了资源耗尽。你可以通过在 `$PXF_BASE/conf/pxf-env.sh` 配置文件中设置 `PXF_OOM_DUMP_PATH` 环境变量，将 PXF 配置为在检测到 OOM 状况时把堆转储写入文件。默认情况下，PXF 在发生 OOM 时不转储 Java 堆。

如果选择在发生 OOM 时启用堆转储，则必须将 `PXF_OOM_DUMP_PATH` 设置为某个文件或目录的绝对路径：

- 如果指定的是目录，PXF JVM 会将堆转储写入文件 `<directory>/java_pid<pid>.hprof`，其中 `<pid>` 标识 PXF Service 实例的进程 ID。JVM 每次发生 OOM 时，都会向该目录写入一个新文件。
- 如果指定的是文件，且该文件不存在，则 PXF JVM 会在检测到 OOM 时将堆转储写入该文件。如果该文件已存在，JVM 不会转储堆。

请确保 `gpadmin` 用户对转储文件或目录具有写权限。

**注意**：堆转储文件通常相当大。如果你为 PXF 启用了 OOM 时的堆转储，并为 `PXF_OOM_DUMP_PATH` 指定了目录，多次 OOM 将在该目录中生成多个文件，可能占用大量磁盘空间。如果为 `PXF_OOM_DUMP_PATH` 指定的是文件，则只要文件名不变，磁盘用量就保持恒定。你必须重命名转储文件，或配置不同的 `PXF_OOM_DUMP_PATH`，才能生成后续的堆转储。

有关启用/停用该 PXF 配置属性的说明，请参阅下文的配置[步骤](#procedure)。

#### 步骤 {#procedure}

PXF Service 在 OOM 时的自动终止默认处于停用状态。OOM 时生成堆转储默认也处于停用状态。要配置其中一个或两个属性，请执行以下步骤：

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 编辑 `$PXF_BASE/conf/pxf-env.sh` 文件。例如：

    ```shell
    gpadmin@coordinator$ vi $PXF_BASE/conf/pxf-env.sh
    ```

3. 如果要配置（即关闭或重新开启）PXF Service 在 OOM 时的自动终止，请在 `pxf-env.sh` 文件中找到 `PXF_OOM_KILL` 属性。如果该设置被注释掉，请取消注释，然后更新其值。例如，要关闭此行为，请将值设置为 `false`：

    ```shell
    export PXF_OOM_KILL=false
    ```

4. 如果要配置（即开启或重新关闭）PXF Service 遇到 OOM 状况时的自动堆转储，请在 `pxf-env.sh` 文件中找到 `PXF_OOM_DUMP_PATH` 设置。

    1. 要开启此行为，请将 `PXF_OOM_DUMP_PATH` 属性值设置为希望 PXF JVM 转储 Java 堆的文件系统位置。例如，要转储到名为 `/home/gpadmin/pxfoom_segh1` 的文件：

        ```shell
        export PXF_OOM_DUMP_PATH=/home/pxfoom_segh1
        ```

    2. 开启堆转储后若要将其关闭，请注释掉 `PXF_OOM_DUMP_PATH` 属性设置：

        ```shell
        #export PXF_OOM_DUMP_PATH=/home/pxfoom_segh1
        ```

5. 保存 `pxf-env.sh` 文件并退出编辑器。

6. 使用 `pxf cluster sync` 命令将更新后的 `pxf-env.sh` 文件复制到 Apache Cloudberry 集群。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

7. 按照[重启 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#restarting-pxf)中的说明，在每台 Apache Cloudberry 主机上重启 PXF。


## 资源受限的 PXF Segment 主机的另一种选择 {#another-option-for-resource-constrained-pxf-segment-hosts}

如果增大最大堆大小不适合你的 Apache Cloudberry 部署，请尝试减少为 PXF 内嵌的 Tomcat Web 服务器配置的并发工作线程数。减少运行线程数可防止任何 PXF 服务器耗尽内存，同时确保当前查询仍能运行至完成（只是会稍慢一些）。Tomcat 的默认行为是将请求排队，直到有线程空闲或队列耗尽。

PXF 默认的 Tomcat 最大线程数为 200。`pxf-application.properties` 配置文件中的 `pxf.max.threads` 属性控制此设置。

如果你计划对外部 Hive 数据存储中的大量文件运行大型工作负载，或者读取压缩的 ORC 或 Parquet 数据，请考虑指定较小的 `pxf.max.threads` 值。大型工作负载需要更多内存，而较低的线程数会限制并发，从而限制内存消耗。

**注意**：请记住，线程数增加会使内存消耗随之增加。

请执行以下步骤，为 Apache Cloudberry 部署中每台主机上运行的 PXF Service 设置 Tomcat 最大线程数。

1. 登录 Apache Cloudberry Coordinator 主机：

    ```shell
    $ ssh gpadmin@<coordinator>
    ```

2. 编辑 `$PXF_BASE/conf/pxf-application.properties` 文件。例如：

    ```shell
    gpadmin@coordinator$ vi $PXF_BASE/conf/pxf-application.properties
    ```

3. 在 `pxf-application.properties` 文件中找到 `pxf.max.threads` 设置。如果该设置被注释掉，请取消注释，然后更新为所需的值。例如，要将 Tomcat 最大线程数减少到 100：

    ```shell
    pxf.max.threads=100
    ```

3. 保存文件并退出编辑器。

4. 使用 `pxf cluster sync` 命令将更新后的 `pxf-application.properties` 文件复制到 Apache Cloudberry 集群。例如：

    ```shell
    gpadmin@coordinator$ pxf cluster sync
    ```

5. 按照[重启 PXF](/cloudberry/pxf/administering/cfginitstart_pxf/#restarting-pxf)中的说明，在每台 Apache Cloudberry 主机上重启 PXF。
