---
title: Writing to etcd
description: Adding a KV pair to an etcd cluster
weight: 250
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
aliases: [/etcd/tasks/developer/writing-to-etcd/]
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
