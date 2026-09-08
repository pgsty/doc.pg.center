---
title: キーの削除方法
description: etcdのキーを削除する方法を説明します
weight: 400
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-delete-keys.md"
aliases: [/etcd/tasks/developer/how-to-delete-keys/]
---

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/docs/etcd/install/)をインストールします。

## キーの追加と削除 {#add-or-delete-keys}

指定したキーまたはキー範囲を削除する`del`：

```bash
etcdctl del $KEY [$END_KEY]
```

### オプション {#options}

```bash
--prefix[=false]: delete keys with matching prefix
--prev-kv[=false]: return deleted key-value pairs
--from-key[=false]: delete keys that are greater than or equal to the given key using byte compare
--range[=false]: delete range of keys without delay
```

### 親コマンドから継承されるオプション {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### 例 {#examples}

![04_etcdctl_delete_2016050601](/docs/etcd/tasks/img/delete-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put key myvalue
etcdctl --endpoints=$ENDPOINTS del key

etcdctl --endpoints=$ENDPOINTS put k1 value1
etcdctl --endpoints=$ENDPOINTS put k2 value2
etcdctl --endpoints=$ENDPOINTS del k --prefix
```
