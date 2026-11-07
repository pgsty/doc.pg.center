---
title: Ubuntu 或 Debian 上的单节点 Citus 集群
description: 使用 deb 软件包在 Ubuntu 或 Debian 上部署单节点 Citus。
weight: 40
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/single-node-debian?view=citus-14
upstream_ref: citus-14; 8445a2831f01
translation_status: translated
---

本节介绍如何使用 deb 软件包，在自己的 Linux 主机上部署单节点 Citus 集群。

## 1. 安装 PostgreSQL 18 与 Citus 扩展 {#1-install-postgresql-17-and-the-citus-extension}

```sh
# Add Citus repository for package manager
curl https://install.citusdata.com/community/deb.sh | sudo bash

# install the server and initialize db
sudo apt-get -y install postgresql-18-citus-14.0
```

## 2. 初始化集群 {#2-initialize-the-cluster}

在磁盘上创建新的数据库集群。为方便通过 PostgreSQL 的 Unix 域套接字连接，使用 `postgres` 用户执行操作。

```sh
# this user has access to sockets in /var/run/postgresql
sudo su - postgres

# include path to PostgreSQL binaries
export PATH=$PATH:/usr/lib/postgresql/18/bin

cd ~
mkdir citus
initdb -D citus
```

Citus 是 PostgreSQL 扩展。要让 PostgreSQL 加载它，需要将其加入配置参数 `shared_preload_libraries`：

```sh
echo "shared_preload_libraries = 'citus'" >> citus/postgresql.conf
```

## 3. 启动数据库服务器 {#3-start-the-database-server}

为新目录启动一个 PostgreSQL 实例：

```sh
pg_ctl -D citus -o "-p 9700" -l citus_logfile start
```

将 Citus 加入 `shared_preload_libraries` 后，它会通过钩子接入 PostgreSQL 的内部机制，替换查询规划器与执行器。接下来加载 Citus 面向用户的对象，例如可调用的函数：

```sh
psql -p 9700 -c "CREATE EXTENSION citus;"
```

## 4. 验证安装 {#4-verify-that-installation-succeeded}

执行以下命令，确认安装成功且 Citus 已加载：

```sh
psql -p 9700 -c "select citus_version();"
```

你应当看到 Citus 扩展的详细信息。

安装完成后即可使用 Citus 集群。[多租户应用教程](/citus/tutorials/tutorial-multi-tenant/)介绍了如何在几分钟内准备好带示例数据的 Citus 集群。

## 相关内容 {#related-content}

- [单节点概览](/citus/installation/single-node/)
- [Docker 单节点安装](/citus/installation/single-node-docker/)
- [Fedora、CentOS 或 Red Hat 单节点安装](/citus/installation/single-node-rhel/)
