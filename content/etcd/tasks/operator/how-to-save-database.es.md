---
title: Cómo guardar la base de datos
description: Guía para tomar una instantánea de la base de datos etcd
weight: 1100
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
---

## Requisitos previos {#pre-requisites}

* [Instala etcdctl y etcdutl](/es/etcd/install/)
* [Configura un clúster local](/es/etcd/dev-guide/local_cluster/)

## Tomar una instantánea de una base de datos {#snapshot-a-database}

`snapshot` para guardar una instantánea de la base de datos etcd en un momento dado:

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### Opciones globales {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

La instantánea solo puede solicitarse a un nodo etcd, por lo que el parámetro `--endpoints` debe contener un único endpoint.

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### Ejemplo {#example}

![11_etcdctl_snapshot_2016051001](/etcd/tasks/img/save-database.gif)

```shell
ENDPOINTS=$HOST_1:2379
etcdctl --endpoints=$ENDPOINTS snapshot save my.db

Snapshot saved at my.db
```

```shell
etcdutl --write-out=table snapshot status my.db

+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| c55e8b8 |        9 |         13 | 25 kB      |
+---------+----------+------------+------------+
```
