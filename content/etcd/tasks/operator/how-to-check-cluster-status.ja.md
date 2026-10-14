---
title: "クラスターの状態を確認する方法"
description: "etcdクラスターの状態を確認するためのガイド"
weight: 1000
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-check-cluster-status.md"
---

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/etcd/install/)をインストールします。

## 全体の状態の確認 {#check-overall-status}

`endpoint status`を使用して、`--endpoints`フラグで指定した各エンドポイントの全体の状態を確認します。

```bash
etcdctl endpoint status (--endpoints=$ENDPOINTS|--cluster)
```

### オプション {#options}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## 健全性の確認 {#check-health}

`endpoint health`を使用して、`--endpoints`フラグで指定した各エンドポイントが正常かどうかを確認します。

```bash
etcdctl endpoint health (--endpoints=$ENDPOINTS|--cluster)
```

### オプション {#options-1}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## KVハッシュの確認 {#check-kv-hash}

`endpoint hashkv`を使用して、`--endpoints`フラグで指定した各エンドポイントのKV履歴のハッシュを確認します。

```bash
etcdctl endpoint hashkv (--endpoints=$ENDPOINTS|--cluster) [rev=$REV]
```

### オプション {#options-2}

```bash
--cluster[=false]: use all endpoints from the cluster member list
--rev=0: maximum revision to hash (default: latest revision)
```

## 親コマンドから継承したオプション {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
-w, --write-out="simple": set the output format (fields, json, protobuf, simple, table)
```

### 例 {#examples}

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
