---
title: "从 Segment 故障中恢复"
description: "本节介绍一个或多个 Segment 或主机停止运行后，如何恢复这些故障 Segment。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/recover-from-segment-failures.md"
---

选择哪种恢复方式，主要取决于你的情况符合以下 3 种场景中的哪一种：

- 在当前主机上原地恢复

- 恢复到集群内的另一台主机

- 恢复到集群外的新主机

在这些场景中，具体步骤还取决于：

- 采用增量恢复还是全量恢复

- 恢复全部 Segment 还是其中一部分

> [!NOTE]
> 只有恢复到当前主机（原地恢复）时，才能使用增量恢复。

本节分为以下部分：

- [前提条件](#prerequisites)
- [恢复场景](#recovery-scenarios)
- [恢复后任务](#post-recovery-tasks)

## 前提条件 {#prerequisites}

- 所有 Segment 均已启用镜像。
- 已识别出故障 Segment。必要时参见[检查故障 Segment](/cloudberry/sys-admin/high-availability/check-for-failed-segments/)。
- Coordinator 主机能够连接 Segment 主机。
- 导致 Segment 故障的网络或硬件问题均已解决。

## 恢复场景 {#recovery-scenarios}

本节介绍 3 种不同的 Segment 恢复场景。请点击链接查看各场景的详细操作步骤。

- [在当前主机上原地恢复](#recover-in-place-to-current-host)
    - [增量恢复](#incremental-recovery)
    - [全量恢复](#full-recovery)
    - [差异恢复](#differential-recovery)
- [恢复到集群内的另一台主机](#recover-to-a-different-host-within-the-cluster)
- [恢复到集群外的新主机](#recover-to-a-different-host-within-the-cluster)

### 在当前主机上原地恢复 {#recover-in-place-to-current-host}

在当前主机上原地恢复时，可选择增量恢复（默认）、全量恢复或差异恢复。

#### 增量恢复 {#incremental-recovery}

按以下步骤执行增量恢复：

1. 要恢复全部 Segment，运行不带选项的 `gprecoverseg`：

    ```shell
    gprecoverseg
    ```

2. 要恢复部分 Segment：
    1.  在自选位置手动创建 `recover_config_file` 文件。每个待恢复 Segment 占一行，格式为 `failedAddress|failedPort|failedDataDirectory` 或 `failedHostname|failedAddress|failedPort|failedDataDirectory`。

        如果有多个 Segment，为每个待恢复 Segment 单独写一行，指定故障 Segment 的主机名（可选）、地址、端口号和数据目录。例如：

        ```
        failedAddress1|failedPort1|failedDataDirectory1
        failedAddress2|failedPort2|failedDataDirectory2
        failedAddress3|failedPort3|failedDataDirectory3
        ```

        或者

        ```
        failedHostname1|failedAddress1|failedPort1|failedDataDirectory1
        failedHostname2|failedAddress2|failedPort2|failedDataDirectory2
        failedHostname3|failedAddress3|failedPort3|failedDataDirectory3
        ```

    2.  也可以使用以下命令生成示例恢复文件，并按需编辑生成的文件：

        ```shell
        $ gprecoverseg -o /home/gpadmin/recover_config_file
        ```

    3.  将 `recover_config_file` 传递给 `gprecoverseg -i` 命令：

        ```shell
        $ gprecoverseg -i /home/gpadmin/recover_config_file  
        ```

3. 执行[恢复后任务](#post-recovery-tasks)中列出的操作。

#### 全量恢复 {#full-recovery}

1. 要恢复全部 Segment，运行 `gprecoverseg -F`：

    ```shell
    gprecoverseg -F
    ```

2. 要恢复指定 Segment：
    1.  在自选位置手动创建 `recover_config_file` 文件。每个待恢复 Segment 占一行，格式如下：

        ```
        failedAddress1|failedPort1|failedDataDirectory1<SPACE>failedAddress2|failedPort2|failedDataDirectory2
        ```

        或者

        ```
        failedHostname1|failedAddress1|failedPort1|failedDataDirectory1<SPACE>failedHostname2|failedAddress2|failedPort2|failedDataDirectory2
        ```

        注意，两部分之间用实际的**空格**分隔。

    2.  也可以使用以下命令生成示例恢复文件，再编辑生成的文件，使其符合所需恢复配置：

        ```shell
        $ gprecoverseg -o /home/gpadmin/recover_config_file
        ```

    3.  运行以下命令，传入上一步生成的配置文件：

        ```shell
        $ gprecoverseg -i recover_config_file
        ```

3. 执行[恢复后任务](#post-recovery-tasks)中列出的操作。

#### 差异恢复 {#differential-recovery}

按以下步骤执行差异恢复：

1. 运行 `gprecoverseg --differential`

### 恢复到集群内的另一台主机 {#recover-to-a-different-host-within-the-cluster}

> [!NOTE]
> 恢复到集群内的另一台主机时，只能使用全量恢复。

按以下步骤，将全部或部分 Segment 恢复到集群内的另一台主机：

1. 在自选位置手动创建 `recover_config_file` 文件。每个待恢复 Segment 占一行，格式如下：

    ```
    failedAddress|failedPort|failedDataDirectory<SPACE>newAddress|newPort|newDataDirectory
    ```

    或者

    ```
    failedHostname|failedAddress|failedPort|failedDataDirectory<SPACE>newHostname|newAddress|newPort|newDataDirectory
    ```

    注意，故障 Segment 的详细信息与目标恢复位置的详细信息之间用实际的**空格**分隔。

    也可以使用以下命令生成示例恢复文件，再编辑生成的文件，使其符合所需恢复配置：

    ```shell
    $ gprecoverseg -o -p /home/gpadmin/recover_config_file
    ```

2. 运行以下命令，传入上一步生成的配置文件：

    ```shell
    $ gprecoverseg -i recover_config_file
    ```

3. 执行[恢复后任务](#post-recovery-tasks)中列出的操作。

### 恢复到集群外的新主机 {#recover-to-a-new-host-outside-of-the-cluster}

如果计划更新 Segment 所在主机的硬件，请按以下步骤操作。

> [!NOTE]
> 恢复到新主机时，只能使用全量恢复。

#### 新主机要求 {#requirements-for-new-host}

新主机必须：

- 安装并配置与故障主机相同的 Apache Cloudberry 软件

- 具有与故障主机相同的硬件和操作系统配置（主机名、操作系统版本、已应用的操作系统配置参数、区域设置、gpadmin 用户账户、已创建的数据目录位置、已交换的 SSH 密钥、网络接口数量、网络接口命名约定等均相同）

- 具有足够的磁盘空间来容纳这些 Segment

- 能够与所有其他现有 Segment 和 Cloudberry Coordinator 进行免密连接。

#### 恢复到新主机的步骤 {#steps-to-recover-to-a-new-host}

1. 启动新主机。
2. 运行以下命令，将全部 Segment 恢复到新主机：

    ```shell
    gprecoverseg -p <new_host_name>
    ```

    也可以指定多台主机。但同时恢复到两台主机时，务必避免触发双重故障场景。

    ```
    gprecoverseg -p <new_host_name1>,<new_host_name2>
    ```

    > [!NOTE]
    > 如果多台 Segment 主机故障，可以用逗号分隔的列表指定恢复目标主机。不过，强烈建议每次只恢复到一台主机。如果必须同时恢复到多台主机，务必确保不会发生主 Segment 及其对应镜像同时离线的双重故障。

3. 执行[恢复后任务](#post-recovery-tasks)中列出的操作。

### 恢复后任务 {#post-recovery-tasks}

`gprecoverseg` 完成后，执行以下步骤：

1. 验证 Segment 状态和首选角色：

    ```sql
    select * from gp_segment_configuration
    ```

2. 监控镜像同步进度：

    ```shell
    gpstate -e
    ```

3. 必要时运行以下命令，使 Segment 回到首选角色：

    ```shell
    gprecoverseg -r
    ```
