---
title: How to delete keys
description: Describes a way to delete etcd keys
weight: 400
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-delete-keys.md"
aliases: [/etcd/tasks/developer/how-to-delete-keys/]
---

## Prerequisites

* Install [`etcd` and `etcdctl`](/docs/etcd/install/)

## Add or delete keys

`del` to remove the specified key or range of keys:

```bash
etcdctl del $KEY [$END_KEY]
```

### Options

```bash
--prefix[=false]: delete keys with matching prefix
--prev-kv[=false]: return deleted key-value pairs
--from-key[=false]: delete keys that are greater than or equal to the given key using byte compare
--range[=false]: delete range of keys without delay
```

### Options inherited from parent commands

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Examples

![04_etcdctl_delete_2016050601](/docs/etcd/tasks/img/delete-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put key myvalue
etcdctl --endpoints=$ENDPOINTS del key

etcdctl --endpoints=$ENDPOINTS put k1 value1
etcdctl --endpoints=$ENDPOINTS put k2 value2
etcdctl --endpoints=$ENDPOINTS del k --prefix
```
