---
title: Comment sauvegarder la base de données
description: Guide de prise d’un instantané de la base de données etcd
weight: 1100
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
---

## Prérequis {#pre-requisites}

* [Installer etcdctl, etcdutl](/fr/etcd/install/)
* [Configurer un cluster local](/fr/etcd/dev-guide/local_cluster/)

## Effectuer un instantané d'une base de données {#snapshot-a-database}

`snapshot` pour sauvegarder un instantané de la base de données etcd à un instant donné :

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### Options globales {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

Un instantané ne peut être demandé qu'à un nœud etcd, donc le drapeau `--endpoints` ne devrait contenir qu'un seul point de terminaison.

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### Exemple {#example}

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
