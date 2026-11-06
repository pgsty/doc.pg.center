---
title: "关于 PXF 部署拓扑"
description: "PXF 部署拓扑。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/administering/deployment_topos.md"
---

PXF 默认的部署拓扑是同机部署（co-located）：在每台 Apache Cloudberry 主机上安装 PXF，PXF Service 在每台 Apache Cloudberry Segment 主机上启动并运行。

你使用 [pxf cluster](/cloudberry/pxf/ref/pxf-cluster/) 命令管理同机部署拓扑中部署的 PXF 服务。


## 备选部署拓扑 {#alternate-deployment-topology}

在非 Apache Cloudberry 主机上运行 PXF Service 是一种备选部署拓扑。如果选择此拓扑，则必须同时在非 Apache Cloudberry 主机和所有 Apache Cloudberry 主机上安装 PXF。

在备选部署拓扑中，你需要在每台主机上使用 [pxf](/cloudberry/pxf/ref/pxf/) 命令单独管理 PXF 服务；在此拓扑中不能使用 `pxf cluster` 命令统一管理 PXF 服务。

如果选择备选部署拓扑，则必须显式配置每台 Apache Cloudberry 主机，以标识 PXF Service 运行所在的主机和监听地址。这些步骤分别在[配置主机](/cloudberry/pxf/administering/advanced-config/cfghostport/#configuring-the-host)和[配置监听地址](/cloudberry/pxf/administering/advanced-config/cfghostport/#configuring-the-listen-address)中介绍。
