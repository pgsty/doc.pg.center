---
title: How to get keys by prefix
description: Guide to extracting etcd keys by their prefix
weight: 300
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## Pre-requisites

* [Install etcdctl](/etcd/install/)
* [Setup a local cluster](/etcd/dev-guide/local_cluster/)

## Get keys by prefix

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### Global Options

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### Options

```bash
--prefix, get a range of keys with matching prefix
```

### Example

![03_etcdctl_get_by_prefix_2016050501](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
