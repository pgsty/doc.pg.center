---
title: القراءة من etcd
description: قراءة قيمة في عنقود etcd
weight: 200
categories: [مهمة]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## المتطلبات الأساسية {#prerequisites}

- ثبّت `etcdctl`


## الإجراء {#procedure}

استخدم الأمر الفرعي `get` للقراءة من etcd:

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

حيث:
- `foo` هو المفتاح المطلوب
- `Hello World!` هي القيمة المسترجَعة

أو، للحصول على مخرجات منسّقة:

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

حيث يُرجِع `write-out="json"` مخرجات JSON مع ترميز كلٍّ من المفتاح والقيمة بتنسيق base64.
