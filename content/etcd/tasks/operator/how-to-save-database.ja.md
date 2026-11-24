---
title: データベースの保存方法
description: etcdデータベースのスナップショットを取得するためのガイド
weight: 1100
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/operator/how-to-save-database.md"
---

## 前提条件 {#pre-requisites}

* [etcdctlとetcdutlをインストール](/ja/etcd/install/)します。
* [ローカルクラスターをセットアップ](/ja/etcd/dev-guide/local_cluster/)します。

## データベースのスナップショットを取得する {#snapshot-a-database}

etcdデータベースのある時点のスナップショットを保存する`snapshot`：

```bash
etcdctl --endpoints=$ENDPOINT snapshot save DB_NAME
```

### グローバルオプション {#global-options}

#### etcdctl {#etcdctl}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

スナップショットを要求できるetcdノードは1つだけなので、`--endpoints`フラグにはエンドポイントを1つだけ指定することをお勧めします。

#### etcdutl {#etcdutl}

```bash
-w, --write-out string   set the output format (fields, json, protobuf, simple, table) (default "simple")
```

### 例 {#example}

![etcdctlによるデータベースのスナップショット保存例](/etcd/tasks/img/save-database.gif)

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
