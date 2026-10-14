---
title: Чтение из etcd
description: Чтение значения в кластере etcd
weight: 200
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
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

где `write-out="json"` задаёт вывод в формате JSON. Ответ содержит и ключ, и значение, закодированные в base64.
