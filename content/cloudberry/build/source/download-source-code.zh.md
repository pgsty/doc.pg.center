---
title: "下载源码"
description: "以 gpadmin 用户身份下载 Apache Cloudberry 发布版本或开发分支及其子模块。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/download-source-code.md"
---

## 从现在开始使用 `gpadmin` 用户 {#use-the-gpadmin-user-from-now-on}

从这里开始，以 `gpadmin` 用户身份执行命令：

```bash
sudo su - gpadmin
```

## 克隆 Apache Cloudberry 仓库（2.x 分支） {#clone-the-apache-cloudberry-repository-2x-branch}

将 Apache Cloudberry 发布版源码克隆到 `gpadmin` 用户的主目录：

```bash
git clone https://github.com/apache/cloudberry.git ~/cloudberry
cd ~/cloudberry
git fetch --tags

# For Apache Cloudberry 2.2.0
git checkout tags/2.2.0-incubating

# For Apache Cloudberry 2.1.0
git checkout tags/2.1.0-incubating

# For Apache Cloudberry 2.0.0
git checkout tags/2.0.0-incubating

git submodule update --init --recursive
```

> [!NOTE] 注意
> `git submodule update --init --recursive` 命令会初始化构建所需的子模块。在 Apache Cloudberry 2.0 和 2.1 中，只有启用 PAX 支持构建时才需要这些子模块；如果不计划启用 PAX，可以跳过此步骤。从 Apache Cloudberry 2.2 起，其他组件也作为子模块提供，例如启用 `--with-yezzey` 时所需的 `gpcontrib/yezzey`，因此除非确定不需要任何子模块，否则应运行此命令。

> [!WARNING] 警告
> 在 Ubuntu 容器中克隆源码时，可能会遇到以下错误：`error: git-remote-https died of signal 4`。
>
> 可以设置以下环境变量来避免此错误：`export GNUTLS_CPUID_OVERRIDE=0x1`。

## 下载源码归档 {#download-the-source-code-archive}

也可以从 [Apache Cloudberry 发布页面](https://cloudberry.apache.org/releases)下载源码归档。

- Apache Cloudberry 2.2.0

```bash
tar xvzf apache-cloudberry-2.2.0-incubating-src.tar.gz
mv apache-cloudberry-2.2.0-incubating cloudberry
```

- Apache Cloudberry 2.1.0

```bash
tar xvzf apache-cloudberry-2.1.0-incubating-src.tar.gz
mv apache-cloudberry-2.1.0-incubating cloudberry
```

- Apache Cloudberry 2.0.0

```bash
tar xvzf apache-cloudberry-2.0.0-incubating-src.tar.gz
mv apache-cloudberry-2.0.0-incubating cloudberry
```

> [!NOTE] 注意
> 最新的 2.x.0 发布版源码归档已经包含子模块，因此从归档解压后无需手动下载子模块。
