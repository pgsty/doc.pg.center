---
title: "扩容后任务"
description: "扩容完成后，必须根据环境执行不同的任务。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/expand-cluster/post-expansion-tasks.md"
---

- [删除扩容模式](#remove-the-expansion-schema)
- [在新主机上设置 PXF](#set-up-pxf-on-the-new-host)

## 删除扩容模式 {#remove-the-expansion-schema}

在 Cloudberry 系统上执行下一次扩容操作之前，必须删除现有的扩容模式。

扩容操作完成并验证后，可以安全地删除扩容模式。要在 Cloudberry 系统上再次执行扩容操作，请先删除现有的扩容模式。

1. 以运行 Apache Cloudberry 系统的用户（例如 `gpadmin`）登录 Coordinator 主机。
2. 使用 `-c` 选项运行 `gpexpand` 工具。例如：

    ```shell
    $ gpexpand -c
    ```

    > [!NOTE]
    > 某些系统要求按两次 Enter 键。

## 在新主机上设置 PXF {#set-up-pxf-on-the-new-host}

> [!TIP]
> 有关更多详细信息，请参见 [PXF](/cloudberry/pxf/) 指南。

如果 Apache Cloudberry 集群使用 PXF，则必须在新主机上执行一些配置步骤。

根据 PXF 版本和安装类型的不同，需要执行的步骤也不同。

### Apache Cloudberry PXF 2.x {#apache-cloudberry-pxf-2x}

- 必须在新主机上安装相同版本的 PXF `rpm` 或 `deb`。
- 登录 Cloudberry Coordinator 并运行以下命令：

    ```shell
    gpadmin@gpcoordinator$ pxf cluster register
    gpadmin@gpcoordinator$ pxf cluster sync
    ```
