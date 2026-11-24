---
title: Lecture depuis etcd
description: "Lecture d'une valeur dans un cluster etcd"
weight: 200
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## Prérequis {#prerequisites}

- Installer `etcdctl`


## Procédure {#procedure}

Utilisez la sous-commande `get` pour lire depuis etcd :

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

où :
- `foo` est la clé demandée
- `Hello World!` est la valeur récupérée

Ou, pour une sortie formatée :

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

où `write-out="json"` renvoie une sortie JSON dont la clé et la valeur sont toutes deux encodées en base64.
