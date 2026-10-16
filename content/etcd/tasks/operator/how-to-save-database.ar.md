---
title: كيفية حفظ قاعدة البيانات
description: دليل أخذ لقطة لقاعدة بيانات etcd
weight: 1100
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
---

## المتطلبات المسبقة {#pre-requisites}

* [ثبّت etcdctl و etcdutl](/ar/etcd/install/)
* [أنشئ عنقودًا محليًا](/ar/etcd/dev-guide/local_cluster/)

## أخذ لقطة لقاعدة بيانات {#snapshot-a-database}

`snapshot` لحفظ لقطة من قاعدة بيانات etcd في نقطة زمنية محددة:

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### الخيارات العامة {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

لا يمكن طلب اللقطة إلا من عقدة etcd واحدة، لذا يجب أن يحتوي الخيار `--endpoints` على نقطة نهاية واحدة فقط.

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### مثال {#example}

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
