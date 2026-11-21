---
title: Writing to etcd
description: Adding a KV pair to an etcd cluster
weight: 250
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
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
