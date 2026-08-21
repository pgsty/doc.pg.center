---
title: Writing to etcd
description: Adding a KV pair to an etcd cluster
weight: 250
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## Prerequisites

- Install `etcdctl`

## Procedure

Use the `put` subcommand to write a key-value pair:

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
where:
- `foo` is the key name
- `"Hello World!"` is the quote-delimited value
