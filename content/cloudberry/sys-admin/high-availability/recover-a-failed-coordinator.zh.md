---
title: "恢复故障 Coordinator"
description: "如果主 Coordinator 故障，Apache Cloudberry 系统将无法访问，WAL 复制也会停止。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/high-availability/recover-a-failed-coordinator.md"
---

使用 [`gpactivatestandby`](/cloudberry/reference/sys-utilities/gpactivatestandby/) 激活 Standby Coordinator。激活时，Apache Cloudberry 会重建 Coordinator 主机在最后一次成功提交事务时的状态。

以下步骤假设系统已经配置 Standby Coordinator 主机。参见[启用 Coordinator 镜像](/cloudberry/sys-admin/high-availability/enable-mirroring/enable-coordinator-mirroring/)。

## 激活 Standby Coordinator {#to-activate-the-standby-coordinator}

1. 在要激活的 Standby Coordinator 主机上运行 `gpactivatestandby` 工具。例如：

    ```shell
    $ export PGPORT=5432
    $ gpactivatestandby -d /data/coordinator/gpseg-1
    ```

    其中，`-d` 指定要激活的 Coordinator 主机的数据目录。

    激活后，Standby Coordinator 成为 Apache Cloudberry 集群中的*活动* Coordinator，也就是*主* Coordinator。

    > [!NOTE]
    > 运行 `gpactivatestandby` 前，务必先运行 `gpstate -f`，确认 Standby Coordinator 已与当前 Coordinator 节点同步。如果已同步，`gpstate -f` 输出的最后一行应类似于：`20230607:06:50:06:004205 gpstate:test1-m:gpadmin-[INFO]:--Sync state: sync`。

2. 工具执行完成后，使用 `gpstate` 的 `-b` 选项显示系统状态摘要：

    ```shell
    $ gpstate -b
    ```

    Coordinator 实例状态应为 `Active`。未配置 Standby Coordinator 时，命令会将其状态显示为 `No coordinator standby configured`。如果已配置新的 Standby Coordinator，其状态为 `Passive`。

3. 可选：如果尚未在激活上一个 Standby Coordinator 时完成此操作，可以在活动 Coordinator 主机上运行 `gpinitstandby`，配置新的 Standby Coordinator。

    > [!NOTE]
    > 需要初始化新的 Standby Coordinator，才能继续提供 Coordinator 镜像。

    关于恢复原 Coordinator 和 Standby Coordinator 配置，参见[恢复后重建 Coordinator 镜像](/cloudberry/sys-admin/high-availability/restore-coordinator-mirroring-after-a-recovery/)。
