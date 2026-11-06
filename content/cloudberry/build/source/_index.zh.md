---
title: "从源码构建 Apache Cloudberry：完整指南"
linkTitle: "从源码构建（完整指南）"
description: "本文面向希望探索 Apache Cloudberry，并可能参与贡献的开发者。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/index.md"
---

本文所述构建环境仅针对开发和测试用途进行了优化。

## 目标读者 {#target-audience}

- 有意为 Apache Cloudberry 作出贡献的开发者。
- 希望了解 Cloudberry 扩展功能的 PostgreSQL 开发者。
- 希望学习分布式查询处理的数据库爱好者。
- 考虑加入 Apache Cloudberry 社区的任何人。

本文介绍的构建过程支持以下开发活动：

- 调试和测试新功能。
- 使用开发工具探索代码库。
- 运行测试套件和验证检查。
- 修改代码并进行测试。

> [!TIP] 提示
> 如果你刚开始参与 Apache Cloudberry 或 PostgreSQL 开发：
>
> - 可以先构建 PostgreSQL，了解基本工作流程。
> - 加入项目的[邮件列表](https://cloudberry.apache.org/community/mailing-lists)，与其他开发者交流。
> - 查看项目的问题跟踪系统，了解当前的开发重点。
> - 探索代码库时，要做好构建耗时较长、需要反复测试的准备。

## Apache Cloudberry 构建流程 {#process-of-building-apache-cloudberry}

Apache Cloudberry（孵化中）的构建流程与 PostgreSQL 非常相似。如果你曾搭建过 PostgreSQL 开发环境，就会对 Cloudberry 的构建步骤感到熟悉。

如果你刚接触 Cloudberry 或 PostgreSQL，建议先尝试构建 PostgreSQL。PostgreSQL 开发社区提供了完善的文档和工具，可引导你完成构建。熟悉 PostgreSQL 的构建流程后，再转向 Cloudberry 会容易得多。

## 前提条件 {#prerequisites}

### 准备 Rocky Linux 8+ / Ubuntu 22.04+ 环境 {#provision-a-rocky-linux-8--ubuntu-2204-environment}

> [!NOTE] 注意
> 从 Apache Cloudberry 2.2 起，不再支持 Ubuntu 20.04，并新增对 Rocky Linux 10 和 Ubuntu 24.04 的支持。

- 可在任意平台上创建虚拟机或容器：

    - **云服务商**：可以使用 AWS、Google Cloud、Microsoft Azure 等云服务商提供的 Rocky Linux 8+ 或 Ubuntu 22.04+ 镜像。
    - **VirtualBox**：使用官方 [Rocky Linux 8+](https://rockylinux.org/download) / [Ubuntu 22.04+](https://ubuntu.com/download) ISO 镜像或 Vagrant box。
    - **Docker**：本文说明已在 Rocky Linux 8+ 和 Ubuntu 22.04 官方 Docker 基础镜像中验证，也应适用于基于这些镜像创建的容器。
      - 例如，可以运行以下命令启动 Rocky Linux 8 容器：

        ```bash
        docker run -it --shm-size=2gb -h cdw rockylinux/rockylinux:8

        # Start a Ubuntu 22.04 container:
        # docker run -it --shm-size=2gb -h cdw ubuntu:22.04
        ```

        主机名 `cdw`（Coordinator Data Warehouse）只是测试时启动容器所用的示例。

        为确保测试套件成功运行，可能需要使用 `--shm-size=2gb` 增大容器的共享内存。Cloudberry 集群的共享内存资源不足时，测试可能失败。

- 确保虚拟机或容器具备以下条件：
    - 能够连接互联网以安装软件包。
    - 可通过 SSH 或控制台进行交互。
    - 有足够的 CPU、内存和存储资源供开发环境使用。

> [!NOTE] 注意
> 各平台准备环境的具体步骤不同，因此本指南不作介绍。本文假定你已成功创建虚拟机或容器，并能以默认用户登录（例如 AWS 上 Rocky Linux 的默认用户 `rocky`）。

### 系统要求 {#system-requirements}

开发环境的最低要求如下：

- CPU：建议 4 核（最低 2 核）
  - CPU 架构：x86、x86_64、ARM、MIPS
- 内存：建议 8GB（最低 4GB）
- 存储：建议有 20GB 可用空间
- 网络：可用于下载软件包的宽带互联网连接

## 从源码构建 Apache Cloudberry {#build-apache-cloudberry-from-source-code}

以下步骤将引导你在 Rocky Linux 8+ 或 Ubuntu 22.04+ 上从源码构建 Apache Cloudberry。两个操作系统的构建流程类似，仅在软件包管理、依赖项和软件版本方面略有区别。

接下来，按照以下步骤从源码构建 Apache Cloudberry：
