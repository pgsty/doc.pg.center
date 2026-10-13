---
title: 如何根据前缀获取键
description: 按前缀获取 etcd 键的指南
weight: 300
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
aliases: [/etcd/tasks/developer/how-to-get-key-by-prefix/]
---

## 先决条件 {#pre-requisites}

* [安装 etcdctl](/zh/docs/etcd/install/)
* [设置本地集群](/zh/docs/etcd/dev-guide/local_cluster/)

## 按前缀获取键 {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### 全局选项 {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### 选项 {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### 示例 {#example}

![03_etcdctl_get_by_prefix_2016050501](/docs/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
