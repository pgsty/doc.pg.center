---
title: Comment surveiller des clés
description: Guide de la surveillance des clés etcd
weight: 600
categories: [Tâche]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
aliases: [/etcd/tasks/developer/how-to-watch-keys/]
---

## Prérequis {#prerequisites}

* Installer [`etcd` et `etcdctl`](/fr/docs/etcd/install/)

## Surveillance des clés {#watching-keys}
`watch` pour être notifié des modifications futures :

```bash
etcdctl watch $KEY [$END_KEY]
```

### Options {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### Options héritées des commandes parentes {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Exemples {#examples}
![06_etcdctl_watch_2016050501](/docs/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
