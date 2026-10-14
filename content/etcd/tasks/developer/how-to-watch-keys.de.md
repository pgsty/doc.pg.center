---
title: "Schlüssel überwachen"
description: "Anleitung zum Überwachen von etcd-Schlüsseln"
weight: 600
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
---

## Voraussetzungen {#prerequisites}

* [`etcd` und `etcdctl`](/de/etcd/install/) installieren

## Schlüssel überwachen {#watching-keys}
`watch` für Benachrichtigungen über künftige Änderungen:

```bash
etcdctl watch $KEY [$END_KEY]
```

### Optionen {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### Von übergeordneten Befehlen geerbte Optionen {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Beispiele {#examples}
![06_etcdctl_watch_2016050501](/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
