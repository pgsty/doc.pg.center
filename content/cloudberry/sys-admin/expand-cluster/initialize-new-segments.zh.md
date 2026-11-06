---
title: "初始化新 Segment"
description: "使用 `gpexpand` 工具创建并初始化新的 Segment 实例，并创建扩容模式。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/initialize-new-segments.md"
---

第一次使用有效输入文件运行 [`gpexpand`](/cloudberry/reference/sys-utilities/gpexpand/) 时，工具会创建并初始化 Segment 实例，并创建扩容模式。完成这些步骤后，再次运行 `gpexpand` 时，工具会检测扩容模式是否已创建；如果已创建，则执行表重分布。

> [!NOTE]
> 为避免现有 Segment 与新 Segment 之间的目录不一致，初始化阶段务必确保没有 DDL 操作正在运行。

- [为系统扩容创建输入文件](#create-an-input-file-for-system-expansion)
- [运行 gpexpand 初始化新 Segment](#run-gpexpand-to-initialize-new-segments)
- [回滚失败的扩容设置](#roll-back-a-failed-expansion-setup)

## 为系统扩容创建输入文件 {#create-an-input-file-for-system-expansion}

开始扩容时，`gpexpand` 要求输入文件包含新 Segment 和主机的信息。如果运行 `gpexpand` 时未指定输入文件，工具会显示交互式问答，收集所需信息并自动创建输入文件。

如果使用交互式问答创建输入文件，可以在问答提示中指定一个包含扩容主机列表的文件。如果平台或命令 Shell 限制主机列表长度，则可能必须使用 `-f` 指定主机。

### 以交互模式创建输入文件 {#create-an-input-file-in-interactive-mode}

在交互模式下运行 `gpexpand` 创建输入文件前，请确认已知：

- 新主机的数量（或主机文件）
- 新主机名（或主机文件）
- 现有主机使用的镜像策略（如果有）
- 每台主机要添加的 Segment 数量（如果有）

工具根据这些信息、`gp_segment_configuration` 中存储的 `dbid`、`content` ID 和数据目录值自动生成输入文件，并将文件保存在当前目录中。

#### 在交互模式下创建输入文件 {#to-create-an-input-file-in-interactive-mode}

1. 以将运行 Apache Cloudberry 系统的用户登录 Coordinator 主机，例如 `gpadmin`。
2. 运行 `gpexpand`。工具会显示准备扩容操作的相关消息，并提示你退出或继续。

    可以选择使用 `-f` 指定主机文件。例如：

    ```shell
    $ gpexpand -f /home/gpadmin/<new_hosts_file>
    ```

3. 在提示处选择 `Y` 继续。
4. 除非已使用 `-f` 指定主机文件，否则系统会提示输入主机名。输入新增扩容主机的主机名列表，名称之间用逗号分隔。不要包含接口主机名。例如：

    ```shell
    > sdw4, sdw5, sdw6, sdw7
    ```

    如果只向现有主机添加 Segment，请在此提示处输入空行。不要指定 `localhost` 或任何现有主机名。

5. 输入系统使用的镜像策略（如果有）。可选值为 `spread|grouped|none`，默认值为 `grouped`。

    确保主机数量足以满足所选的分组策略。有关镜像的更多信息，请参见[规划镜像 Segment](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/)。

6. 输入要添加的新主 Segment 数量（如果有）。默认情况下，新主机初始化的主 Segment 数量与现有主机相同。输入大于零的数字可以增加每台主机的 Segment 数量。输入的数字表示将在所有主机上初始化的新增 Segment 数量。例如，如果现有主机当前各有两个 Segment，输入 `2` 会在现有主机上再初始化两个 Segment，并在新主机上初始化四个 Segment。
7. 如果正在添加新的主 Segment，请输入新 Segment 的主数据目录根路径。不要指定实际数据目录名；`gpexpand` 会根据现有数据目录名自动创建该目录名。

    例如，现有数据目录如下：

    ```shell
    /gpdata/primary/gp0
    /gpdata/primary/gp1
    ```

    接着，在提示处分别输入以下内容，为两个新的主 Segment 指定数据目录：

    ```shell
    /gpdata/primary
    /gpdata/primary
    ```

    初始化运行时，工具会在 `/gpdata/primary` 下创建新目录 `gp2` 和 `gp3`。

8. 如果正在添加新的镜像 Segment，请输入新 Segment 的镜像数据目录根路径。不要指定数据目录名；`gpexpand` 会根据现有数据目录名自动创建该目录名。

    例如，现有数据目录如下：

    ```shell
    /gpdata/mirror/gp0
    /gpdata/mirror/gp1
    ```

    接着，在提示处分别输入以下内容，为两个新的镜像 Segment 指定数据目录：

    ```shell
    /gpdata/mirror
    /gpdata/mirror
    ```

    初始化运行时，工具会在 `/gpdata/mirror` 下创建新目录 `gp2` 和 `gp3`。

    新 Segment 的这些主数据目录根路径和镜像数据目录根路径必须在主机上存在，并且运行 `gpexpand` 的用户必须拥有在其中创建目录的权限。

    输入完所有必需信息后，工具会生成输入文件，并将其保存到当前目录。例如：

    ```
    gpexpand_inputfile_yyyymmdd_145134
    ```

    如果 Cloudberry 集群配置了表空间，工具会自动生成一个额外的表空间映射文件。该文件供工具之后解析时使用，因此请确保在继续下一步前文件已存在。例如：

    ```
    gpexpand_inputfile_yyyymmdd_145134.ts
    ```

### 扩容输入文件格式 {#expansion-input-file-format}

除非扩容场景有特殊需求，否则请使用交互式问答过程创建输入文件。

扩容输入文件的格式为：

```
hostname|address|port|datadir|dbid|content|preferred_role
```

例如：

```
sdw5|sdw5-1|50011|/gpdata/primary/gp9|11|9|p
sdw5|sdw5-2|50012|/gpdata/primary/gp10|12|10|p
sdw5|sdw5-2|60011|/gpdata/mirror/gp9|13|9|m
sdw5|sdw5-1|60012|/gpdata/mirror/gp10|14|10|m
```

对于每个新 Segment，这种格式的扩容输入文件要求以下字段：

|参数|有效值|描述|
|---------|------------|-----------|
|hostname|主机名|Segment 主机的主机名。|
|port|可用的端口号|Segment 的数据库监听端口，在现有 Segment 的 *port* 基础端口号上递增。|
|datadir|目录名|根据 gp_segment_configuration 系统目录，Segment 的数据目录位置。|
|dbid|整数。不能与现有 dbid 值冲突。|Segment 的数据库 ID。输入值应从系统目录 `gp_segment_configuration` 中显示的现有 dbid 值开始依次递增。例如，要在现有包含十个 Segment、dbid 值为 1-10 的阵列中添加四个 Segment 实例，请列出新的 dbid 值 11、12、13 和 14。|
|content|整数。不能与现有 content 值冲突。|Segment 的 content ID。主 Segment 及其镜像应具有相同的 content ID，并从现有值开始依次递增。有关更多信息，请参见 `gp_segment_configuration` 参考中的 *content*。|
|preferred_role|`p` 或 `m`|确定该 Segment 是主 Segment 还是镜像 Segment。主 Segment 指定 `p`，镜像 Segment 指定 `m`。|

## 运行 gpexpand 初始化新 Segment {#run-gpexpand-to-initialize-new-segments}

创建输入文件后，运行 `gpexpand` 初始化新的 Segment 实例。

### 使用输入文件运行 gpexpand {#to-run-gpexpand-with-an-input-file}

1. 以将运行 Apache Cloudberry 系统的用户登录 Coordinator 主机，例如 `gpadmin`。
2. 使用 `-i` 指定输入文件，运行 `gpexpand` 工具。例如：

    ```shell
    $ gpexpand -i input_file
    ```

    工具会检测 Apache Cloudberry 系统是否存在扩容模式。如果存在 *gpexpand* 模式，请在开始新的扩容操作前使用 `gpexpand -c` 将其删除。请参见[删除扩容模式](/cloudberry/sys-admin/expand-cluster/post-expansion-tasks/)。

    新 Segment 初始化并创建扩容模式后，工具会打印成功消息并退出。

初始化过程完成后，可以连接 Apache Cloudberry 并查看扩容模式。*gpexpand* 模式位于 postgres 数据库中。有关更多信息，请参见[扩容模式简介](/cloudberry/sys-admin/expand-cluster/plan-system-expansion/)。

Segment 初始化完成后，[重新分布表](/cloudberry/sys-admin/expand-cluster/redistribute-tables/)，使现有数据在新 Segment 之间保持平衡。

## 监控集群扩容状态 {#monitor-the-cluster-expansion-state}

随时可以通过使用 `-x` 标志运行 `gpstate` 工具来检查集群扩容状态：

```shell
$ gpstate -x
```

如果 postgres 数据库中存在扩容模式，`gpstate -x` 会报告扩容进度。在第一个扩容阶段，`gpstate` 会报告新 Segment 初始化进度。在第二个阶段，`gpstate` 会报告表重分布进度，以及重分布处于暂停还是活动状态。

还可以查询扩容模式查看扩容状态。更多信息请参见[监控表重分布](/cloudberry/sys-admin/expand-cluster/redistribute-tables/)。

## 回滚失败的扩容设置 {#roll-back-a-failed-expansion-setup}

只有在扩容设置操作失败时，才可以回滚该操作（添加 Segment 实例和 Segment 主机）。

如果扩容在初始化步骤中失败，且此时数据库处于关闭状态，则必须先运行 `gpstart -m` 命令，以 Coordinator-only 模式重新启动数据库。

使用以下命令回滚失败的扩容：

```shell
gpexpand --rollback
```
