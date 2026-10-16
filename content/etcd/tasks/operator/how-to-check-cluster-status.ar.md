---
title: كيفية التحقق من حالة العنقود
description: دليل التحقق من حالة عنقود etcd
weight: 1000
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-check-cluster-status.md"
---

## المتطلبات الأساسية {#prerequisites}

* ثبّت [`etcd` و`etcdctl`](/ar/etcd/install/)

## التحقق من الحالة العامة {#check-overall-status}

`endpoint status` للتحقق من الحالة العامة لكل نقطة نهاية محددة في الخيار `--endpoints`:

```bash
etcdctl endpoint status (--endpoints=$ENDPOINTS|--cluster)
```

### الخيارات {#options}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## التحقق من الصحة {#check-health}

`endpoint health` للتحقق من صحة كل نقطة نهاية محددة في الخيار `--endpoints`:

```bash
etcdctl endpoint health (--endpoints=$ENDPOINTS|--cluster)
```

### الخيارات {#options-1}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## التحقق من تجزئة KV {#check-kv-hash}

`endpoint hashkv` للتحقق من تجزئة محفوظات KV لكل نقطة نهاية محددة في الخيار `--endpoints`:

```bash
etcdctl endpoint hashkv (--endpoints=$ENDPOINTS|--cluster) [rev=$REV]
```

### الخيارات {#options-2}

```bash
--cluster[=false]: use all endpoints from the cluster member list
--rev=0: maximum revision to hash (default: latest revision)
```

## خيارات موروثة من الأوامر الأصل {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
-w, --write-out="simple": set the output format (fields, json, protobuf, simple, table)
```

### أمثلة {#examples}

```shell
etcdctl --write-out=table --endpoints=$ENDPOINTS endpoint status

+------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT      |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
| 10.240.0.17:2379 | 4917a7ab173fabe7 |  3.5.0  |   45 kB |      true |      false |         4 |      16726 |              16726 |        |
| 10.240.0.18:2379 | 59796ba9cd1bcd72 |  3.5.0  |   45 kB |     false |      false |         4 |      16726 |              16726 |        |
| 10.240.0.19:2379 | 94df724b66343e6c |  3.5.0  |   45 kB |     false |      false |         4 |      16726 |              16726 |        |
+------------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------|
```

```shell
etcdctl --endpoints=$ENDPOINTS endpoint health

10.240.0.17:2379 is healthy: successfully committed proposal: took = 3.345431ms
10.240.0.19:2379 is healthy: successfully committed proposal: took = 3.767967ms
10.240.0.18:2379 is healthy: successfully committed proposal: took = 4.025451ms
```

```shell
etcdctl --cluster endpoint hashkv  --write-out=table

+------------------+------------+---------------+
|     ENDPOINT     |    HASH    | HASH REVISION |
+------------------+------------+---------------+
| 10.240.0.17:2379 | 3892279174 |             3 |
| 10.240.0.18:2379 | 3892279174 |             3 |
| 10.240.0.19:2379 | 3892279174 |             3 |
+------------------+------------+---------------+
```
