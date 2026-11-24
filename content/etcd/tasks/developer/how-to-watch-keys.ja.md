---
title: キーの監視方法
description: etcdのキーを監視するためのガイド
weight: 600
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
---

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/etcd/install/)をインストールします。

## キーの監視 {#watching-keys}
今後の変更の通知を受け取る`watch`：

```bash
etcdctl watch $KEY [$END_KEY]
```

### オプション {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### 親コマンドから継承されるオプション {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### 例 {#examples}
![etcdctlによるキーの監視例](/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
