---
title: プレフィックスでキーを取得する方法
description: プレフィックスでetcdのキーを抽出するためのガイド
weight: 300
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
aliases: [/etcd/tasks/developer/how-to-get-key-by-prefix/]
---

## 前提条件 {#pre-requisites}

* [etcdctlをインストール](/ja/docs/etcd/install/)します。
* [ローカルクラスターをセットアップ](/ja/docs/etcd/dev-guide/local_cluster/)します。

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

![03_etcdctl_get_by_prefix_2016050501](/docs/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
