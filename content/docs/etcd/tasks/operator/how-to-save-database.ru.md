---
title: Как сохранить базу данных
description: Руководство по созданию снимка базы данных etcd
weight: 1100
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
aliases: [/etcd/tasks/operator/how-to-save-database/]
---

## Предварительные требования {#pre-requisites}

* [Установите etcdctl, etcdutl](/ru/docs/etcd/install/)
* [Настройте локальный кластер](/ru/docs/etcd/dev-guide/local_cluster/)

## Сделать снимок базы данных {#snapshot-a-database}

`snapshot` для создания снимка базы данных etcd в определённый момент времени:

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### Глобальные параметры {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

Снимок можно запрашивать только у одного узла etcd, поэтому во флаге `--endpoints` следует указывать только одну конечную точку.

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### Пример {#example}

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
