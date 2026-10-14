---
title: Как проверить состояние кластера
description: Руководство по проверке состояния кластера etcd
weight: 1000
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-check-cluster-status.md"
---

## Предварительные условия {#prerequisites}

* Установите [`etcd` и `etcdctl`](/ru/etcd/install/)

## Проверка общего состояния {#check-overall-status}

Команда `endpoint status` проверяет общее состояние каждой конечной точки, указанной флагом `--endpoints`:

```bash
etcdctl endpoint status (--endpoints=$ENDPOINTS|--cluster)
```

### Параметры {#options}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## Проверка работоспособности {#check-health}

Команда `endpoint health` проверяет работоспособность каждой конечной точки, указанной флагом `--endpoints`:

```bash
etcdctl endpoint health (--endpoints=$ENDPOINTS|--cluster)
```

### Параметры {#options-1}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## Проверка хеша KV {#check-kv-hash}

Команда `endpoint hashkv` проверяет хеш истории KV каждой конечной точки, указанной флагом `--endpoints`:

```bash
etcdctl endpoint hashkv (--endpoints=$ENDPOINTS|--cluster) [rev=$REV]
```

### Параметры {#options-2}

```bash
--cluster[=false]: use all endpoints from the cluster member list
--rev=0: maximum revision to hash (default: latest revision)
```

## Параметры, унаследованные от родительских команд {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
-w, --write-out="simple": set the output format (fields, json, protobuf, simple, table)
```

### Примеры {#examples}

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
