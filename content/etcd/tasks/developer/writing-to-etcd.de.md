---
title: "In etcd schreiben"
description: "Ein KV-Paar zu einem etcd-Cluster hinzufügen"
weight: 250
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
---

## Voraussetzungen {#prerequisites}

- `etcdctl` installieren

## Vorgehensweise {#procedure}

Mit dem Unterbefehl `put` ein Schlüssel-Wert-Paar schreiben:

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
Dabei gilt:
- `foo` ist der Schlüsselname
- `"Hello World!"` ist der in Anführungszeichen eingeschlossene Wert
