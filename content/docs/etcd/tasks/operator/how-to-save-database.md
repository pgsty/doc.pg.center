---
title: How to save the database
description: Guide to taking a snapshot of the etcd database
weight: 1100
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
aliases: [/etcd/tasks/operator/how-to-save-database/]
---

## Pre-requisites

* [Install etcdctl, etcdutl](/docs/etcd/install/)
* [Setup a local cluster](/docs/etcd/dev-guide/local_cluster/)

## Snapshot a database

`snapshot` to save point-in-time snapshot of etcd database:

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### Global Options

#### etcdctl

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

Snapshot can only be requested from one etcd node, so `--endpoints` flag should contain only one endpoint.

#### etcdutl

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### Example

![11_etcdctl_snapshot_2016051001](/docs/etcd/tasks/img/save-database.gif)

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
