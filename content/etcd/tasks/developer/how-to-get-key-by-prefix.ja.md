---
title: プレフィックスでキーを取得する方法
description: プレフィックスでetcdのキーを抽出するためのガイド
weight: 300
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## 前提条件 {#pre-requisites}

* [etcdctlをインストール](/ja/etcd/install/)します。
* [ローカルクラスターをセットアップ](/ja/etcd/dev-guide/local_cluster/)します。

## プレフィックスでキーを取得する {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### グローバルオプション {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### オプション {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### 例 {#example}

![etcdctlによるプレフィックスを指定したキーの取得例](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
