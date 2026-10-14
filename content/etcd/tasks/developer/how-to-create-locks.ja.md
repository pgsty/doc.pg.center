---
title: ロックの作成方法
description: etcdで分散ロックを作成するためのガイド
weight: 800
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

LOCKは、指定された名前の分散ミューテックスを取得します。取得したロックは、etcdctlが終了するまで保持されます。

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/etcd/install/)をインストールします。

## ロックの作成 {#creating-a-lock}

分散ロックに使用する`lock`：

![etcdctlによる分散ロックの作成例](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### オプション {#options}
- endpoints - クラスター内のマシンのアドレスを、コンマ区切りのリストで指定します。
- ttl - ロックセッションのタイムアウトを秒単位で指定します。
