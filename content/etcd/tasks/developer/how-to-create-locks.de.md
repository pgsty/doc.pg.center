---
title: "Sperren erstellen"
description: "Anleitung zum Erstellen verteilter Sperren in etcd"
weight: 800
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

LOCK erwirbt einen verteilten Mutex mit einem bestimmten Namen. Sobald die Sperre erworben wurde, bleibt sie bis zum Beenden von etcdctl bestehen.

## Voraussetzungen {#prerequisites}

* [`etcd` und `etcdctl`](/de/etcd/install/) installieren

## Eine Sperre erstellen {#creating-a-lock}

`lock` für eine verteilte Sperre:

![08_etcdctl_lock_2016050501](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Optionen {#options}
- endpoints – definiert eine durch Kommas getrennte Liste der Rechneradressen im Cluster.
- ttl – Zeitüberschreitung der Sperrsitzung in Sekunden.
