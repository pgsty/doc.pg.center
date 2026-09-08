---
title: ロックの作成方法
description: etcdで分散ロックを作成するためのガイド
weight: 800
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
aliases: [/etcd/tasks/developer/how-to-create-locks/]
---

LOCKは、指定された名前の分散ミューテックスを取得します。取得したロックは、etcdctlが終了するまで保持されます。

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/docs/etcd/install/)をインストールします。

## ロックの作成 {#creating-a-lock}

分散ロックに使用する`lock`：

![08_etcdctl_lock_2016050501](/docs/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### オプション {#options}
- endpoints - クラスター内のマシンのアドレスを、コンマ区切りのリストで指定します。
- ttl - ロックセッションのタイムアウトを秒単位で指定します。
