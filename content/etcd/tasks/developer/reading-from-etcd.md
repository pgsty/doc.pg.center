---
title: Reading from etcd
description: Reading a value in an etcd cluster
weight: 200
categories: [Task]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## Prerequisites

- Install `etcdctl`


## Procedure

Use the `get` subcommand to read from etcd:

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

where:
- `foo` is the requested key
- `Hello World!` is the retrieved value

Or, for formatted output:

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

where `write-out="json"` returns JSON output with both the key and value encoded in base64.
