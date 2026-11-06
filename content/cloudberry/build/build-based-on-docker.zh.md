---
title: "使用 Docker 开发镜像构建"
description: "本指南介绍如何使用基于 Docker 的开发环境构建 Apache Cloudberry。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/build/build-based-on-docker.md"
---

这种方式尤其适合在不同系统上保持一致的构建环境，并节省环境配置时间。

## 前提条件 {#prerequisites}

- Docker：确保系统已安装 Docker。可从 [Docker 官网](https://www.docker.com/get-started)下载并安装。
- 硬盘空间：确保至少有 10 GB 可用磁盘空间，用于存放 Docker 镜像和构建产物。

## 运行 Docker 开发镜像 {#run-the-docker-dev-image}

运行以下命令，使用 Apache Cloudberry 开发镜像启动 Docker 容器：

```bash {tab="Rocky Linux 8"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-rocky8-latest
```
```bash {tab="Rocky Linux 9"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-rocky9-latest
```
```bash {tab="Rocky Linux 10"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-rocky10-latest
```
```bash {tab="Ubuntu 22.04"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-ubuntu22.04-latest
```
```bash {tab="Ubuntu 24.04"}
docker run --name cbdb-dev -it --rm -h cdw --shm-size=2gb apache/incubator-cloudberry:cbdb-build-ubuntu24.04-latest
```

> [!NOTE] 注意
> 从 Apache Cloudberry 2.2 起，支持 Rocky Linux 10 和 Ubuntu 24.04。

说明：
- `--name=cbdb-dev` 将容器名称设为 `cbdb-dev`，可按需更改。
- `-it` 以交互模式运行容器，便于在容器内执行命令。
- `--rm` 在退出容器后将其删除。如果希望保留容器以便后续使用，可移除此选项。
- `-h cdw` 将容器的主机名设为 `cdw`（Coordinator Data Warehouse）。
- `--shm-size=2gb` 设置容器的共享内存大小，以便测试套件成功运行。Cloudberry 集群的共享内存资源不足时，测试可能失败，此时可能需要通过该选项增大容器的共享内存。

此开发环境已完成以下配置：
- 创建具有所需权限的 `gpadmin` 用户。
- 设置环境变量和路径。
- 配置所需的系统资源限制。
- 安装必要的依赖项。

现在你已进入 Docker 容器，Apache Cloudberry 开发环境也已就绪。继续操作前，请确认已使用 `gpadmin` 用户登录容器，如下所示：

```
======================================================================

                          ++++++++++       ++++++
                        ++++++++++++++   +++++++
                       ++++        +++++ ++++
                      ++++          +++++++++
                   =+====         =============+
                 ========       =====+      =====
                ====  ====     ====           ====
               ====    ===     ===             ====
               ====            === ===         ====
               ====            ===  ==--       ===
                =====          ===== --       ====
                 =====================     ======
                   ============================
                                     =-----=
     ____  _                    _  _
    / ___|| |  ___   _   _   __| || |__    ___  _ __  _ __  _   _
   | |    | | / _ \ | | | | / _` || '_ \  / _ \| '__|| '__|| | | |
   | |___ | || (_) || |_| || (_| || |_) ||  __/| |   | |   | |_| |
    \____||_| \____  \__,_| \__,_||_.__/  \___||_|   |_|    \__, |
                                                            |___/
----------------------------------------------------------------------

Welcome to the Apache Cloudberry Build Environment!

Container OS ........ : Rocky Linux 9.5 (Blue Onyx)
User ................ : gpadmin
Container hostname .. : cdw
IP Address .......... : 170.17.0.1
CPU Info ............ : Intel(R) Xeon(R) Gold 6151 CPU @ 3.00GHz
CPU(s) .............. : 8
Memory .............. : 15Gi total
======================================================================

[gpadmin@cdw ~]$
```

## 后续步骤 {#whats-next}

- [下载源码](/cloudberry/build/source/download-source-code/)
- [配置 Apache Cloudberry 构建](/cloudberry/build/source/configure/)
- [构建并安装 Apache Cloudberry 及 contrib 扩展](/cloudberry/build/source/build-and-install/)
- [搭建 Cloudberry 演示集群](/cloudberry/build/source/set-demo-cluster/)（从 `Set up Cloudberry environment variables` 这一步开始）
- [安装后操作](/cloudberry/build/source/post-installation/)

也可以直接运行以下命令，更快地完成上述步骤：

> [!NOTE] 注意
> 从 2.1.0 版本起可用。

```bash
## Download the source code
git clone --recurse-submodules --branch REL_2_STABLE --single-branch --depth=1 https://github.com/apache/cloudberry.git

## Change directory
cd /home/gpadmin/cloudberry

## Set up the SRC_DIR environment variable and create a directory for build logs
export SRC_DIR=/home/gpadmin/cloudberry
mkdir -p ${SRC_DIR}/build-logs

# Since Cloudberry 2.2
# Pre-stage the Python packages for `--with-pythonsrc-ext` before building
make -C gpMgmt/bin download-python-deps

## Configure, build, and install Cloudberry
./devops/build/automation/cloudberry/scripts/configure-cloudberry.sh
./devops/build/automation/cloudberry/scripts/build-cloudberry.sh

## Set up a Cloudberry Demo Cluster
./devops/build/automation/cloudberry/scripts/create-cloudberry-demo-cluster.sh

## Start a Cloudberry Demo Cluster
source /usr/local/cloudberry-db/cloudberry-env.sh
source /home/gpadmin/cloudberry/gpAux/gpdemo/gpdemo-env.sh
psql -p 7000 postgres
```
