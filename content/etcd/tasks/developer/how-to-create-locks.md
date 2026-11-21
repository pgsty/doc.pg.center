---
title: How to create locks
description: Guide to creating distributed locks in etcd
weight: 800
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

LOCK acquires a distributed mutex with a given name. Once the lock is acquired, it will be held until etcdctl is terminated.

## Prerequisites

* Install [`etcd` and `etcdctl`](/etcd/install/)

## Creating a lock

`lock` for distributed lock:

![08_etcdctl_lock_2016050501](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Options
- endpoints - defines a comma-delimited list of machine addresses in the cluster.
- ttl - time out in seconds of lock session.
