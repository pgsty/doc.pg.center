---
title: How to create locks
description: Guide to creating distributed locks in etcd
weight: 800
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
aliases: [/etcd/tasks/developer/how-to-create-locks/]
---

LOCK acquires a distributed mutex with a given name. Once the lock is acquired, it will be held until etcdctl is terminated.

## Prerequisites

* Install [`etcd` and `etcdctl`](/docs/etcd/install/)

## Creating a lock

`lock` for distributed lock:

![08_etcdctl_lock_2016050501](/docs/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Options
- endpoints - defines a comma-delimited list of machine addresses in the cluster.
- ttl - time out in seconds of lock session.
