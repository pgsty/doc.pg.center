---
title: Чтение из etcd
description: Чтение значения в кластере etcd
weight: 200
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
aliases: [/etcd/tasks/developer/reading-from-etcd/]
---

## Предварительные требования {#prerequisites}

- Установите `etcdctl`


## Процедура {#procedure}

Используйте подкоманду `get` для чтения из etcd:

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

где:
- `foo` — запрашиваемый ключ
- `Hello World!` — полученное значение

Или для форматированного вывода:

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

где `write-out="json"` заставляет выводить значение в формате JSON (обратите внимание, ключ не возвращается).
