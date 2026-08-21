---
title: How to watch keys
description: Guide to watching etcd keys
weight: 600
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
---

## Prerequisites

* Install [`etcd` and `etcdctl`](/etcd/install/)

## Watching keys
`watch` to get notified of future changes:

```bash
etcdctl watch $KEY [$END_KEY]
```

### Options

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### Options inherited from parent commands

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Examples
![06_etcdctl_watch_2016050501](/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
