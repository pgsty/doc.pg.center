---
title: 如何检查集群状态
description: etcd 集群状态检查指南
weight: 1000
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-check-cluster-status.md"
---

## 先决条件 {#prerequisites}

* 安装 [`etcd` 和 `etcdctl`](/zh/etcd/install/)

## 检查整体状态 {#check-overall-status}

使用 `endpoint status` 检查 `--endpoints` 标志中指定的每个端点的总体状态：

```bash
etcdctl endpoint status (--endpoints=$ENDPOINTS|--cluster)
```

### 选项 {#options}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## 检查健康状况 {#check-health}

使用 `endpoint health` 检查 `--endpoints` 标志中指定的每个端点的健康状态：

```bash
etcdctl endpoint health (--endpoints=$ENDPOINTS|--cluster)
```

### 选项 {#options-1}

```bash
--cluster[=false]: use all endpoints from the cluster member list
```

## 检查键值哈希 {#check-kv-hash}

使用 `endpoint hashkv` 检查 `--endpoints` 标志中指定的每个端点的 KV 历史哈希值：

```bash
etcdctl endpoint hashkv (--endpoints=$ENDPOINTS|--cluster) [rev=$REV]
```

### 选项 {#options-2}

```bash
--cluster[=false]: use all endpoints from the cluster member list
--rev=0: maximum revision to hash (default: latest revision)
```

## 继承自父命令的选项 {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
-w, --write-out="simple": set the output format (fields, json, protobuf, simple, table)
```

### 示例 {#examples}

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
