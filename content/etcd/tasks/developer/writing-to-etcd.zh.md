---
title: 向 etcd 写入
description: 向 etcd 集群添加一个键值对
weight: 250
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## 先决条件 {#prerequisites}

- 安装 `etcdctl`

## 步骤 {#procedure}

使用 `put` 子命令写入键值对：

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
其中：
- `foo` 为键名称
- `"Hello World!"` 为用引号括起的值
