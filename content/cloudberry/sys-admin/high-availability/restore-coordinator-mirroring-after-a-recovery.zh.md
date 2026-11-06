---
title: "恢复后重建 Coordinator 镜像"
description: "为恢复系统而激活 Standby Coordinator 后，它就成为主 Coordinator。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/restore-coordinator-mirroring-after-a-recovery.md"
---

如果该实例与原 Coordinator 主机具备相同的能力和可靠性，可以继续将其作为主 Coordinator 运行。

必须初始化新的 Standby Coordinator，才能继续提供 Coordinator 镜像；除非已在激活上一个 Standby Coordinator 时完成此操作。在活动 Coordinator 主机上运行 [`gpinitstandby`](/cloudberry/reference/sys-utilities/gpinitstandby/)，配置新的 Standby Coordinator。参见[启用 Coordinator 镜像](/cloudberry/sys-admin/high-availability/enable-mirroring/enable-coordinator-mirroring/)。

可以在原主机上恢复主 Coordinator 和 Standby Coordinator 实例。此过程会交换两台主机上的主备角色，只有在强烈希望让 Coordinator 实例回到恢复操作前的原主机上运行时，才应执行。

> [!NOTE]
> 将主 Coordinator 和 Standby Coordinator 实例恢复到原主机不是在线操作，必须先停止 Coordinator 才能执行。
>
> 有关 Apache Cloudberry 工具的信息，参见 [Apache Cloudberry 工具指南](/cloudberry/reference/sys-utilities/)。

## 恢复后重建 Coordinator 镜像 {#to-restore-the-coordinator-mirroring-after-a-recovery}

1. 确保原 Coordinator 主机已能可靠运行，并确认最初导致故障的原因已排除。
2. 在原 Coordinator 主机上，移动或删除数据目录 `gpseg-1`。以下示例将该目录移至 `backup_gpseg-1`：

    ```shell
    $ mv /data/coordinator/gpseg-1 /data/coordinator/backup_gpseg-1
    ```

    Standby Coordinator 配置成功后，即可删除备份目录。

3. 在原 Coordinator 主机上初始化 Standby Coordinator。例如，在当前 Coordinator 主机 scdw 上运行以下命令：

    ```shell
    $ gpinitstandby -s cdw
    ```

4. 初始化完成后，检查 Standby Coordinator cdw 的状态。使用 [`gpstate`](/cloudberry/reference/sys-utilities/gpstate/) 的 `-f` 选项检查 Standby Coordinator 状态：

    ```shell
    $ gpstate -f
    ```

    Standby Coordinator 的状态应为 `passive`，WAL 发送进程的状态应为 `streaming`。

## 将 Coordinator 和 Standby Coordinator 实例恢复到原主机（可选） {#to-restore-the-coordinator-and-standby-instances-on-original-hosts-optional}

> [!NOTE]
> 执行本节步骤前，务必先按照上一节[恢复后重建 Coordinator 镜像](#to-restore-the-coordinator-mirroring-after-a-recovery)的说明完成镜像恢复。

1. 停止原 Standby Coordinator 主机上运行的 Apache Cloudberry Coordinator 实例。例如：

    ```shell
    $ gpstop -m
    ```

2. 在原 Coordinator 主机 cdw（当前为 Standby Coordinator）上运行 `gpactivatestandby` 工具。例如：

    ```shell
    $ gpactivatestandby -d $COORDINATOR_DATA_DIRECTORY
    ```

    其中，`-d` 选项指定要激活的主机的数据目录。

    > [!NOTE]
    > 运行 `gpactivatestandby` 前，务必先运行 `gpstate -f`，确认 Standby Coordinator 已与当前 Coordinator 节点同步。如果已同步，`gpstate -f` 输出的最后一行应类似于：`20230607:06:50:06:004205 gpstate:test1-m:gpadmin-[INFO]:--Sync state: sync`。

3. 工具执行完成后，使用 `gpstate` 的 `-b` 选项显示系统状态摘要：

    ```shell
    $ gpstate -b
    ```

    Coordinator 实例状态应为 `Active`。未配置 Standby Coordinator 时，命令会将其状态显示为 `No coordinator standby configured`。

4. 在 Standby Coordinator 主机上，移动或删除数据目录 `gpseg-1`。以下示例移动该目录：

    ```shell
    $ mv /data/coordinator/gpseg-1 /data//backup_gpseg-1
    ```

    Standby Coordinator 配置成功后，即可删除备份目录。

5. 原 Coordinator 主机恢复运行主 Apache Cloudberry Coordinator 后，可以在原 Standby Coordinator 主机上初始化 Standby Coordinator。例如：

    ```shell
    $ gpinitstandby -s scdw
    ```

    命令完成后，可以在主 Coordinator 主机上运行 `gpstate -f` 命令，检查 Standby Coordinator 状态。

## 检查 Coordinator 镜像进程状态（可选） {#to-check-the-status-of-the-coordinator-mirroring-process-optional}

可以使用 `gpstate` 工具的 `-f` 选项，显示 Standby Coordinator 主机的详细信息。

```shell
$ gpstate -f
```

Standby Coordinator 的状态应为 `passive`，WAL 发送进程的状态应为 `streaming`。
