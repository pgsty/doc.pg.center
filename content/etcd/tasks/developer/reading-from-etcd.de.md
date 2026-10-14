---
title: "Aus etcd lesen"
description: "Einen Wert aus einem etcd-Cluster lesen"
weight: 200
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/reading-from-etcd.md"
---

## Voraussetzungen {#prerequisites}

- `etcdctl` installieren


## Vorgehensweise {#procedure}

Mit dem Unterbefehl `get` aus etcd lesen:

```shell
$ etcdctl --endpoints=$ENDPOINTS get foo
foo
Hello World!
$
```

Dabei gilt:
- `foo` ist der angeforderte Schlüssel
- `Hello World!` ist der abgerufene Wert

Für eine formatierte Ausgabe:

```
$ etcdctl --endpoints=$ENDPOINTS --write-out="json" get foo
{"header":{"cluster_id":289318470931837780,"member_id":14947050114012957595,"revision":3,"raft_term":4,
"kvs":[{"key":"Zm9v","create_revision":2,"mod_revision":3,"version":2,"value":"SGVsbG8gV29ybGQh"}]}}
$
```

Dabei gibt `write-out="json"` JSON aus, in dem sowohl der Schlüssel als auch der Wert base64-kodiert sind.
