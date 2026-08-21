---
title: 从 etcd 中读取
description: 在集群中读取值
weight: 200
categories: [任务]
upstream_link: "https://github.com/etcd-io/website/blob/a9ee660fdbf9584deb4af639c4dc63b01413e44f/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## 先决条件 {#prerequisites}

- 安装 `etcdctl`


## 步骤 {#procedure}

使用 `get` 子命令从 etcd 读取：

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

其中：
- `foo` 为请求的键
- `Hello World!` 为获取的值

或者，以格式化输出形式：

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

其中 `write-out="json"` 会导致值以 JSON 格式输出（注意：键不会被返回）。
