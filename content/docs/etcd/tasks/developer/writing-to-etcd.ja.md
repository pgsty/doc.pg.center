---
title: etcdへの書き込み
description: etcdクラスターにキー・バリューペアを追加する
weight: 250
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
aliases: [/etcd/tasks/developer/writing-to-etcd/]
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
