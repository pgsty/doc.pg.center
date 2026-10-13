---
title: 如何创建锁
description: etcd 分布式锁创建指南
weight: 800
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
aliases: [/etcd/tasks/developer/how-to-create-locks/]
---

LOCK 使用指定名称获取一个分布式互斥锁。锁获取成功后，将一直持有，直至 etcdctl 终止。

## 先决条件 {#prerequisites}

* 安装 [`etcd` 和 `etcdctl`](/zh/docs/etcd/install/)

## 创建锁 {#creating-a-lock}

`lock` 用于分布式锁：

![08_etcdctl_lock_2016050501](/docs/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### 选项 {#options}
- endpoints - 定义集群中机器地址的逗号分隔列表。
- ttl - 锁会话的超时时间，单位为秒。
