---
title: 如何保存数据库
description: etcd 数据库快照创建指南
weight: 1100
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
aliases: [/etcd/tasks/operator/how-to-save-database/]
---

## 先决条件 {#pre-requisites}

* [安装 etcdctl 和 etcdutl](/zh/docs/etcd/install/)
* [设置本地集群](/zh/docs/etcd/dev-guide/local_cluster/)

## 快照数据库 {#snapshot-a-database}

`snapshot` 用于保存 etcd 数据库的指定时间点快照：

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### 全局选项 {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

快照只能从一个 etcd 节点请求，因此 `--endpoints` 标志中应仅包含一个端点。

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### 示例 {#example}

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
