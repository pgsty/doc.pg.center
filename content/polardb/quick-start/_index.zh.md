---
title: Docker 快速体验
description: 通过 DockerHub 或阿里云 ACR 镜像，快速体验 PolarDB PostgreSQL 单机实例。
weight: 10
upstream_link: https://github.com/polardb/polardb-pg-docs/blob/b4733b0350888242afeba432a6837458c348a937/docs/zh/README.md
upstream_source: polardb
upstream_modified: true
type: docs
---


> [!WARNING]
> 上游体验镜像中的 postgres 用户没有设置密码，仅供本地体验。完整前提与操作见[快速部署](/zh/polardb/deploying/quick-start/)。

<span id="通过-docker-快速使用"></span>

### 通过 Docker 快速使用 {#quick-start-with-docker}

拉取 PolarDB for PostgreSQL 的 [单机实例镜像](https://hub.docker.com/r/polardb/polardb_pg_local_instance/tags)，运行容器并试用 PolarDB-PG：

```bash {tab="DockerHub"}
# 拉取镜像并运行容器
docker pull polardb/polardb_pg_local_instance:15
docker run -it --cap-add=SYS_PTRACE --privileged=true --rm polardb/polardb_pg_local_instance:15 psql
# 测试可用性
postgres=# SELECT version();
                                   version
----------------------------------------------------------------------
 PostgreSQL 15.x (PolarDB 15.x.x.x build xxxxxxxx) on {your_platform}
(1 row)
```

```bash {tab="阿里云 ACR"}
# 拉取镜像并运行容器
docker pull registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_local_instance:15
docker run -it --cap-add=SYS_PTRACE --privileged=true --rm registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_local_instance:15 psql
# 测试可用性
postgres=# SELECT version();
                                   version
----------------------------------------------------------------------
 PostgreSQL 15.x (PolarDB 15.x.x.x build xxxxxxxx) on {your_platform}
(1 row)
```
