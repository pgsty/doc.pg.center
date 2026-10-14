---
title: 如何监听键值变化
description: etcd 键监听指南
weight: 600
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
---

## 先决条件 {#prerequisites}

* 安装 [`etcd` 和 `etcdctl`](/zh/etcd/install/)

## 监听键 {#watching-keys}
`watch` 以接收后续变更的通知：

```bash
etcdctl watch $KEY [$END_KEY]
```

### 选项 {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### 继承自父命令的选项 {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### 示例 {#examples}
![06_etcdctl_watch_2016050501](/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
