---
title: Lecture depuis etcd
description: "Lecture d'une valeur dans un cluster etcd"
weight: 200
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
aliases: [/etcd/tasks/developer/reading-from-etcd/]
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

Or, pour une sortie formatée :

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

où `write-out="json"` fait que la valeur est sortie au format JSON (notez que la clé n'est pas renvoyée).
