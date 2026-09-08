---
title: etcdからの読み取り
description: etcdクラスターの値を読み取る
weight: 200
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## 前提条件 {#prerequisites}

- `etcdctl`をインストールします。


## 手順 {#procedure}

`get`サブコマンドを使用して、etcdから読み取ります。

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

各要素の意味は次のとおりです。
- `foo`は要求したキーです。
- `Hello World!`は取得した値です。

出力形式を指定する場合は、次のように実行します。

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

ここで、`write-out="json"`を指定すると、値はJSON形式で出力されます（キーは返されない点に注意してください）。
