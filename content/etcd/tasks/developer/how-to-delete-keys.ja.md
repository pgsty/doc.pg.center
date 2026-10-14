---
title: キーの削除方法
description: etcdのキーを削除する方法を説明します
weight: 400
categories: [タスク]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-delete-keys.md"
---

## 前提条件 {#prerequisites}

* [`etcd`と`etcdctl`](/ja/etcd/install/)をインストールします。

## キーの追加または削除 {#add-or-delete-keys}

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

![etcdctlによるキーの削除例](/etcd/tasks/img/delete-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put key myvalue
etcdctl --endpoints=$ENDPOINTS del key

etcdctl --endpoints=$ENDPOINTS put k1 value1
etcdctl --endpoints=$ENDPOINTS put k2 value2
etcdctl --endpoints=$ENDPOINTS del k --prefix
```
