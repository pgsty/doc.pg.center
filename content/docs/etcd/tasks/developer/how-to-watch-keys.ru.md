---
title: Как наблюдать за ключами
description: Руководство по наблюдению за ключами etcd
weight: 600
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-watch-keys.md"
aliases: [/etcd/tasks/developer/how-to-watch-keys/]
---

## Предварительные требования {#prerequisites}

* Установите [`etcd` и `etcdctl`](/ru/docs/etcd/install/)

## Наблюдение за ключами {#watching-keys}
`watch` для получения уведомлений о будущих изменениях:

```bash
etcdctl watch $KEY [$END_KEY]
```

### Параметры {#options}

```bash
-i, --interactive[=false]: interactive mode
--prefix[=false]: watch on a prefix if prefix is set
--rev=0: Revision to start watching
--prev-kv[=false]: get the previous key-value pair before the event happens
--progress-notify[=false]: get periodic watch progress notification from server
```

### Параметры, унаследованные от родительских команд {#options-inherited-from-parent-commands}

```bash
--endpoints="127.0.0.1:2379": gRPC endpoints
```

### Примеры {#examples}
![06_etcdctl_watch_2016050501](/docs/etcd/tasks/img/watch-keys.gif)

```shell
etcdctl --endpoints=$ENDPOINTS watch stock1
etcdctl --endpoints=$ENDPOINTS put stock1 1000

etcdctl --endpoints=$ENDPOINTS watch stock --prefix
etcdctl --endpoints=$ENDPOINTS put stock1 10
etcdctl --endpoints=$ENDPOINTS put stock2 20
```
