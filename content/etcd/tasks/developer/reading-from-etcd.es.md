---
title: Lectura desde etcd
description: "Lectura de un valor en un clúster etcd"
weight: 200
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## Prerrequisitos {#prerequisites}

- Instala `etcdctl`


## Procedimiento {#procedure}

Usa el subcomando `get` para leer desde etcd:

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

donde:
- `foo` es la clave solicitada
- `Hello World!` es el valor recuperado

O bien, para una salida con formato:

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

donde `write-out="json"` devuelve una salida JSON con la clave y el valor codificados en base64.
