---
title: Docker & Podman deployment IvorySQL
linkTitle: Docker & Podman deployment
description: 'IvorySQL v5.6 documentation: Docker & Podman deployment IvorySQL.'
type: docs
weight: 100
upstream_link: https://github.com/IvorySQL/ivorysql_docs/blob/7c3f4a67e7d3dc92d3046ad54cac4de196aef4f1/EN/modules/ROOT/pages/4.6.4.adoc
upstream_source: ivorysql
upstream_license: LicenseRef-IvorySQL-Docs-en
upstream_modified: true
---

> [!TIP]
>
> In addition to Docker Hub, the IvorySQL community also provides a Harbor registry for users in China. Replace the image prefix used in this chapter with `registry.highgo.com/`, e.g. `registry.highgo.com/ivorysql/ivorysql:5.6-ubi8`.

## 1. Running IvorySQL in docker {#running-ivorysql-in-docker}

- Get IvorySQL image from Docker Hub

```
$ docker pull ivorysql/ivorysql:5.6-ubi8
```

- Running IvorySQL

```
$ docker run --name ivorysql -p 5434:5432 -e IVORYSQL_PASSWORD=your_password -d ivorysql/ivorysql:5.6-ubi8
```

- Check if the IvorySQL container is running successfully

```
$ docker ps | grep ivorysql
CONTAINER ID   IMAGE               COMMAND                   CREATED          STATUS          PORTS                              NAMES
6faa2d0ed705   ivorysql/ivorysql:5.6-ubi8   "docker-entrypoint.s…"   50 seconds ago   Up 49 seconds   5866/tcp, 0.0.0.0:5434->5432/tcp   ivorysql
```

## 2. Running with Podman {#running-with-podman}

- Pull IvorySQL Image from Docker Hub

```
[highgo@manager-node1 ~]$ podman pull ivorysql/ivorysql:5.6-ubi8
✔ docker.io/ivorysql/ivorysql:5.6-ubi8
Trying to pull docker.io/ivorysql/ivorysql:5.6-ubi8...
Getting image source signatures
Copying blob 5885448c5c88 done   |
Copying blob 6c502b378234 done   |
Copying blob 8b4f2b90d6b6 done   |
Copying blob 9b000f2935f6 done   |
Copying blob 806f782da874 done   |
Copying blob e4c51845a9eb done   |
Copying blob dcb1e9a04275 done   |
Copying blob 285a279173f8 done   |
Copying blob 1f6f247b9ae0 done   |
Copying blob 3cc81bed8614 done   |
Copying blob 863c87bf25eb done   |
Copying blob 4f4fb700ef54 done   |
Copying config 88e1bbeda8 done   |
Writing manifest to image destination
88e1bbeda81c51d88e12cbd2b19730498f1343d1c64bb3dddc8ffcb08a1f965f
```

- Run IvorySQL Container

```
$ podman run --name ivorysql -p 5434:5432 -e IVORYSQL_PASSWORD=123456 -d ivorysql/ivorysql:5.6-ubi8
```

- Check if IvorySQL Container is Running Successfully

```
[highgo@manager-node1 ~]$ podman ps | grep ivorysql
CONTAINER ID            IMAGE                       COMMAND          CREATED          STATUS          PORTS                                 NAMES
368dee58d5ef  docker.io/ivorysql/ivorysql:5.6-ubi8  postgres    20 seconds ago  Up 20 seconds  0.0.0.0:5434->5432/tcp, 1521/tcp, 5866/tcp  ivorysql

[highgo@manager-node1 ~]$ podman exec -it ivorysql /bin/bash
[root@8cc631eb413d /]#
ivorysql=# select version();
                                                        version
------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 18.0 (IvorySQL 5.6) on x86_64-pc-linux-gnu, compiled by gcc (GCC) 8.5.0 20210514 (Red Hat 8.5.0-28), 64-bit
(1 row)

ivorysql=#
```
