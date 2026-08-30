---
title: 如何删除键
description: 删除 etcd 键的指南
weight: 400
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-delete-keys.md"
---

## 先决条件 {#prerequisites}

* 安装 [`etcd` 和 `etcdctl`](/zh/etcd/install/)

## 添加或删除键 {#add-or-delete-keys}

`del` 用于删除指定的键或键范围：

```bash
etcdctl del $KEY [$END_KEY]
```

### 选项 {#options}

```bash
--prefix[=false]: delete keys with matching prefix
--prev-kv[=false]: return deleted key-value pairs
--from-key[=false]: delete keys that are greater than or equal to the given key using byte compare
--range[=false]: delete range of keys without delay
```

### 继承自父命令的选项 {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### 示例 {#examples}

![04_etcdctl_delete_2016050601](/etcd/tasks/img/delete-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put key myvalue
etcdctl --endpoints=$ENDPOINTS del key

etcdctl --endpoints=$ENDPOINTS put k1 value1
etcdctl --endpoints=$ENDPOINTS put k2 value2
etcdctl --endpoints=$ENDPOINTS del k --prefix
```
