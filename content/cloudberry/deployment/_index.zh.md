---
title: "部署 Apache Cloudberry"
linkTitle: "生产环境部署"
description: "本指南介绍如何在生产环境中部署 Apache Cloudberry。"
weight: 30
icon: "fa-solid fa-server"
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/deployment/index.md"
---

本指南涵盖从硬件规划到集群初始化和登录的完整部署流程。

指南包含以下主题：

- **[平台要求](/cloudberry/deployment/platform-requirements/)** — Apache Cloudberry 主机的硬件和软件要求。
- **[估算存储容量](/cloudberry/deployment/capacity_planning/)** — 如何估算数据所需的磁盘空间。
- **[配置系统](/cloudberry/deployment/prepare-to-deploy/)** — 操作系统层面的配置，包括内核参数、SELinux、防火墙、NTP 和用户设置。
- **[使用 RPM/DEB 软件包安装](/cloudberry/deployment/install_cloudberry/)** — 在所有主机上安装 Apache Cloudberry 软件。
- **[创建数据存储区域](/cloudberry/deployment/create_data_dirs/)** — 为 Coordinator 和 Segment 实例设置数据目录。
- **[验证硬件与网络](/cloudberry/deployment/validate/)** — 验证网络、磁盘 I/O 和内存带宽性能。
- **[初始化 Apache Cloudberry](/cloudberry/deployment/init_cloudberry/)** — 使用 `gpinitsystem` 初始化数据库集群。
- **[登录 Apache Cloudberry](/cloudberry/deployment/login_cloudberry/)** — 部署后连接数据库。
- **[以单计算节点部署 Apache Cloudberry](/cloudberry/deployment/single-node/)** — 在不配置 Segment 节点的情况下部署 Apache Cloudberry，用于开发或测试。
