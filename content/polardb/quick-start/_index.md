---
title: Docker quick start
description: Try a local PolarDB for PostgreSQL instance with the upstream Docker images.
weight: 10
upstream_link: https://github.com/polardb/polardb-pg-docs/blob/b4733b0350888242afeba432a6837458c348a937/docs/README.md
upstream_source: polardb
upstream_modified: true
type: docs
---


> [!WARNING]
> The upstream demo image leaves the postgres account without a password and is intended for evaluation only.

### Quick Start with Docker {#quick-start-with-docker}

Pull the [local instance image](https://hub.docker.com/r/polardb/polardb_pg_local_instance/tags) of PolarDB for PostgreSQL based on local storage. Create and run the container, and try PolarDB-PG instance directly:

```bash {tab="DockerHub"}
# pull the instance image and run the container
docker pull polardb/polardb_pg_local_instance:15
docker run -it --cap-add=SYS_PTRACE --privileged=true --rm polardb/polardb_pg_local_instance:15 psql
# check
postgres=# SELECT version();
                                   version
----------------------------------------------------------------------
 PostgreSQL 15.x (PolarDB 15.x.x.x build xxxxxxxx) on {your_platform}
(1 row)
```

```bash {tab="Alibaba Cloud ACR"}
# pull the instance image and run the container
docker pull registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_local_instance:15
docker run -it --cap-add=SYS_PTRACE --privileged=true --rm registry.cn-hangzhou.aliyuncs.com/polardb_pg/polardb_pg_local_instance:15 psql
# check
postgres=# SELECT version();
                                   version
----------------------------------------------------------------------
 PostgreSQL 15.x (PolarDB 15.x.x.x build xxxxxxxx) on {your_platform}
(1 row)
```
