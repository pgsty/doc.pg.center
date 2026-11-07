---
title: 构建 Docker 镜像
linkTitle: Docker 构建
description: 构建和测试 OrioleDB 的 Alpine、Ubuntu 及 PostGIS Docker 镜像。
weight: 30
type: docs
search_keywords: ["OrioleDB", "docker builds"]
upstream_link: https://www.orioledb.com/docs/contributing/docker-builds
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-box
---


本文介绍如何构建并测试 OrioleDB Docker 镜像。

#### 前提条件 {#prerequisites}

开始前，请确保本机已安装 Docker。若尚未安装，可从 Docker 官方网站下载：<https://docs.docker.com/get-docker/>。

- `docker -v`

## 快速入门 {#quickstart}

打开终端，进入 OrioleDB 项目目录：

- `cd path/to/orioledb`

构建基于 Alpine 的 PostgreSQL 18 与 OrioleDB 扩展：

- `docker build -t orioletest:18 -f docker/Dockerfile --pull --network=host --progress=plain --build-arg PG_MAJOR="18" .`

启动服务器：

- `docker run --name orioletest18 -v orioletest18data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=oriole123 -d orioletest:18`

通过 psql 连接：

- `docker exec -ti orioletest18 psql -U postgres`

应看到类似的 psql 信息：

```
psql (18.6 OrioleDB beta 18 PGTAG=patches18_2 alpine:3.21+clang build:2026-09-23T12:00:00+00:00 18.6)
Type "help" for help.
postgres=#
```

启用 OrioleDB 扩展：

- `create extension if not exists orioledb;`

测试一些命令：

```
postgres=# select orioledb_version();
 orioledb_version 
------------------
 OrioleDB beta 18
(1 row)

postgres=# CREATE TABLE oriole_test (a int) USING orioledb;
CREATE TABLE
postgres=# INSERT INTO  oriole_test VALUES (1), (2);
INSERT 0 2
postgres=# SELECT * FROM oriole_test;
 a
---
 1
 2
(2 rows)

postgres=# VACUUM ANALYZE oriole_test;
VACUUM

postgres=# \d+ oriole_test
                                       Table "public.oriole_test"
 Column |  Type   | Collation | Nullable | Default | Storage | Compression | Stats target | Description
--------+---------+-----------+----------+---------+---------+-------------+--------------+-------------
 a      | integer |           |          |         | plain   |             |              |
Access method: orioledb


postgres=# \d+
                                           List of relations
 Schema |         Name         | Type  |  Owner   | Persistence | Access method |  Size   | Description
--------+----------------------+-------+----------+-------------+---------------+---------+-------------
 public | oriole_test          | table | postgres | permanent   | orioledb      | 16 kB   |
 public | orioledb_index       | view  | postgres | permanent   |               | 0 bytes |
 public | orioledb_index_descr | view  | postgres | permanent   |               | 0 bytes |
 public | orioledb_table       | view  | postgres | permanent   |               | 0 bytes |
 public | orioledb_table_descr | view  | postgres | permanent   |               | 0 bytes |
(5 rows)

postgres=# \dx
                                       List of installed extensions
   Name   | Version | Default version |   Schema   |                     Description
----------+---------+-----------------+------------+------------------------------------------------------
 orioledb | 1.9     | 1.9             | public     | OrioleDB -- the next generation transactional engine
 plpgsql  | 1.0     | 1.0             | pg_catalog | PL/pgSQL procedural language
(2 rows)

postgres=# \dx+ orioledb
                     Objects in extension "orioledb"
                           Object description
-------------------------------------------------------------------------
 access method orioledb
 function fetch_read_page_checkpoint_stats()
 function orioledb_commit_hash()
 function orioledb_compression_max_level()
 function orioledb_evict_pages(oid,integer)
 function orioledb_get_complete_oxid()
 function orioledb_get_complete_xid()
 function orioledb_get_current_heap_xid()
 function orioledb_get_current_logical_xid()
 function orioledb_get_current_oxid()
 function orioledb_get_evicted_trees()
 function orioledb_get_index_descrs()
 function orioledb_get_proc_retain_undo_locations()
 function orioledb_get_rewind_evicted_length()
 function orioledb_get_rewind_queue_length()
 function orioledb_get_table_descrs()
 function orioledb_get_undo_meta()
 function orioledb_get_xid_meta()
 function orioledb_has_retained_undo()
 function orioledb_idx_structure(oid,text,character varying,integer)
 function orioledb_index_description(oid,oid,oid,text)
 function orioledb_index_oids()
 function orioledb_index_rows(oid)
 function orioledb_insert_sys_xid_undo_location(integer,bigint)
 function orioledb_int4range_immutable(text)
 function orioledb_page_stats()
 function orioledb_parallel_debug_start()
 function orioledb_parallel_debug_stop()
 function orioledb_print_pool_pages(integer)
 function orioledb_read_sys_xid_undo_location(integer)
 function orioledb_recovery_synchronized()
 function orioledb_relation_size(oid)
 function orioledb_rewind_by_time(integer,boolean)
 function orioledb_rewind_by_time(integer)
 function orioledb_rewind_set_complete(integer,bigint)
 function orioledb_rewind_sync()
 function orioledb_rewind_to_timestamp(timestamp with time zone,boolean)
 function orioledb_rewind_to_timestamp(timestamp with time zone)
 function orioledb_rewind_to_transaction(integer,bigint,boolean)
 function orioledb_rewind_to_transaction(integer,bigint)
 function orioledb_sys_tree_check(integer,boolean)
 function orioledb_sys_tree_rows(integer)
 function orioledb_sys_tree_structure(integer,character varying,integer)
 function orioledb_table_description(oid,oid,oid)
 function orioledb_table_description(oid)
 function orioledb_table_oids()
 function orioledb_table_pages(oid)
 function orioledb_tableam_handler(internal)
 function orioledb_tbl_are_indices_equal(regclass,regclass)
 function orioledb_tbl_bin_structure(oid,boolean,integer)
 function orioledb_tbl_check(oid,boolean)
 function orioledb_tbl_compression_check(bigint,oid,integer[])
 function orioledb_tbl_indices(oid,boolean,boolean)
 function orioledb_tbl_indices(oid)
 function orioledb_tbl_structure(oid,character varying,integer)
 function orioledb_test_back_refind_skip_tail(oid,integer)
 function orioledb_test_corrupt_page_undo(oid)
 function orioledb_test_endkey_returned_skip(oid,integer)
 function orioledb_tree_stat(regclass)
 function orioledb_ucm_check()
 function orioledb_undo_size()
 function orioledb_upgrade_refresh()
 function orioledb_version()
 function orioledb_write_pages(oid)
 function pg_stopevent_reset(text)
 function pg_stopevent_set(text,jsonpath,text)
 function pg_stopevent_set(text,jsonpath)
 function pg_stopevents()
 function reset_read_page_checkpoint_stats()
 function s3_get(text)
 function s3_put(text,text)
 function verify_orioledb(regclass,boolean)
 type orioledb_index
 type orioledb_index_descr
 type orioledb_index_descr[]
 type orioledb_index[]
 type orioledb_table
 type orioledb_table_descr
 type orioledb_table_descr[]
 type orioledb_table[]
 view orioledb_index
 view orioledb_index_descr
 view orioledb_table
 view orioledb_table_descr
(84 rows)
```

退出数据库：`\q`

停止服务器：

- `docker stop orioletest18`

删除容器：

- `docker container rm orioletest18`

删除 Docker 镜像：

- `docker rmi orioletest:18`

删除数据卷：

- `docker volume rm orioletest18data`

## 构建 Docker 镜像 {#building-docker-images-1}

选择以下命令之一构建镜像。

#### 构建 PostgreSQL 18 与 OrioleDB 扩展 {#to-build-postgresql-18--orioledb-extension}

```
docker build -t orioletest:18 -f docker/Dockerfile --pull --network=host --progress=plain --build-arg PG_MAJOR="18" .
```

#### 构建 PostgreSQL 17 与 OrioleDB 扩展 {#to-build-postgresql-17--orioledb-extension}

```
docker build -t orioletest:17 -f docker/Dockerfile --pull --network=host --progress=plain --build-arg PG_MAJOR="17" .
```

## 支持的环境变量 {#supported-environment-variables}

本项目力求兼容 Docker 官方 PostgreSQL 镜像，因此也支持其中的环境变量：

- `POSTGRES_PASSWORD`
- `POSTGRES_USER`
- `POSTGRES_DB`
- `POSTGRES_INITDB_ARGS`
- `POSTGRES_INITDB_WALDIR`
- `POSTGRES_HOST_AUTH_METHOD`
- `PGDATA`

更多信息：<https://github.com/docker-library/docs/blob/master/postgres/README.md>

## 可用的构建参数 {#available-docker-build-args}

完整构建参数请查看 Dockerfile。

- Alpine Linux：`./Dockerfile`
  - 支持 \[ `edge 3.21 3.20 3.19 3.18` \]
  - 示例：`--build-arg ALPINE_VERSION="3.21" -f docker/Dockerfile `
- Ubuntu Linux：`./Dockerfile.ubuntu`
  - 支持 \[ `devel 25.04 24.10 24.04 22.04 plucky oracular noble jammy` \]
  - 示例：`--build-arg UBUNTU_VERSION="24.04" -f docker/Dockerfile.ubuntu `

其他重要参数：

- `--build-arg PG_MAJOR="17"`
  - 选择 PostgreSQL 大版本，默认为 `17`。
  - 可选 `16`、`17`、`18`。
- `--build-arg BUILD_CC_COMPILER="gcc"`
  - 选择 C 编译器，默认为 `clang`。
  - 可选 `clang` 或 `gcc`。

例如，使用 Alpine `3.21`、`gcc` 编译器和 PostgreSQL `17` 构建镜像：

``` bash
docker build --pull --network=host --progress=plain \
    --build-arg ALPINE_VERSION="3.21" \
    --build-arg BUILD_CC_COMPILER="gcc" \
    --build-arg PG_MAJOR="17" \
    -f docker/Dockerfile \
    -t orioletest:17-gcc-alpine3.21 .
```

使用 Ubuntu `devel`、`clang` 编译器和 PostgreSQL `18` 构建镜像：

``` bash
docker build --pull --network=host --progress=plain \
    --build-arg UBUNTU_VERSION="devel" \
    --build-arg BUILD_CC_COMPILER="clang" \
    --build-arg PG_MAJOR="18" \
    -f docker/Dockerfile.ubuntu \
    -t orioletest:18-clang-ubuntu-devel .
```

`devel` 是最新的 Ubuntu 开发版本，可能不稳定。

## 实验性 OrioleDB 与 PostGIS 扩展构建 {#experimental-orioledb--postgis-extension-build}

已知限制：

- 尚不支持 OrioleDB 的 `gist`、`sp-gist` 等相关索引。

#### 步骤 1：创建 `orioletest:17-gcc-alpine3.21` 镜像 {#step-1-create-image-orioletest17-gcc-alpine321}

``` bash
docker build --pull --network=host --progress=plain \
    --build-arg ALPINE_VERSION="3.21" \
    --build-arg BUILD_CC_COMPILER="gcc" \
    --build-arg PG_MAJOR="17" \
    -f docker/Dockerfile \
    -t orioletest:17-gcc-alpine3.21 .
```

#### 步骤 2：构建 `oriolegis:17-3.5-alpine` 镜像 {#step2-build-the-oriolegis17-35-alpine-image}

在新目录中执行以下命令：

``` bash
git clone --depth=1 https://github.com/postgis/docker-postgis.git
cd ./docker-postgis/17-3.5/alpine
docker build --network=host --progress=plain \
     --build-arg BASE_IMAGE=orioletest:17-gcc-alpine3.21 \
     -t oriolegis:17-3.5-alpine .
```

## 开发者说明 {#developer-notes}

要在本机构建全部 Docker 镜像变体，请运行：

- `./ci/local_docker_matrix.sh`
- 或实验性的 `./ci/docker_matrix.sh --help`

##### Ubuntu {#ubuntu}

- 支持的基础镜像，包含安全更新：
  - <https://hub.docker.com/_/ubuntu>
- 支持的基础镜像架构：
  - \[ amd64, arm32v7, arm64v8, ppc64le, riscv64, s390x\]

##### Alpine {#alpine}

- 支持的基础镜像，包含安全更新：
  - <https://hub.docker.com/_/alpine>
- 支持的基础镜像架构：
  - \[ amd64, arm32v6, arm32v7, arm64v8, i386, ppc64le, riscv64, s390x \]

#### macOS {#macos}

macOS 上可能需要通过 Homebrew 安装 `bash` 和 `gnu-getopt`：

``` bash
brew install bash gnu-getopt
```

更新 `/etc/shells`：

``` bash
echo /opt/homebrew/bin/bash >> /etc/shells
```

可能还需在 `.bashrc` 或 `.zshrc` 中更新 `PATH`：

```
PATH=/opt/homebrew/bin:/opt/homebrew/opt/gnu-getopt/bin:$PATH
```

##### 其他 {#other}

- 测试：如果能够在 `amd64` 以外的架构上测试，请告知我们。

- 某些 QEMU 版本无法模拟 PostgreSQL JIT，此时请使用 `jit=off`。

- 安全：没有限定主机绑定地址的端口，例如使用 `-p 5432:5432` 而非 `-p 127.0.0.1:5432:5432`，可从外部访问。即使 UFW 已阻止该端口，也仍然如此，因为 Docker 管理自己的 iptables 规则。参见[详细说明](https://docs.docker.com/network/iptables/)。简单密码加开放端口可能导致[挖矿程序入侵](https://github.com/docker-library/postgres/issues/770#issuecomment-704460980)。

- Windows：如遇问题，请使用 Windows Subsystem for Linux（WSL2）。

- 扩展现有 OrioleDB Docker 镜像并不容易。不能直接使用 Ubuntu PostgreSQL 软件包，例如 `postgresql-16-mobilitydb`，需要从源码构建。
