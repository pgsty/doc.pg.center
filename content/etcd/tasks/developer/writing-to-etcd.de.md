---
title: "In etcd schreiben"
description: "Ein KV-Paar zu einem etcd-Cluster hinzufügen"
weight: 250
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
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
