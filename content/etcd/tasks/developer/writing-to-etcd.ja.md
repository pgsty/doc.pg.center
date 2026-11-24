---
title: etcdへの書き込み
description: etcdクラスターにキー・バリューペアを追加する
weight: 250
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## 前提条件 {#prerequisites}

- `etcdctl`をインストールします。

## 手順 {#procedure}

`put`サブコマンドを使用して、キー・バリューペアを書き込みます。

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
各要素の意味は次のとおりです。
- `foo`はキーの名前です。
- `"Hello World!"`は引用符で囲んだ値です。
