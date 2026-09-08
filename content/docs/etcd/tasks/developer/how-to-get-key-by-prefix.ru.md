---
title: Как получить ключи по префиксу
description: Руководство по извлечению ключей etcd по их префиксу
weight: 300
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
aliases: [/etcd/tasks/developer/how-to-get-key-by-prefix/]
---

## Предварительные требования {#pre-requisites}

* [Установите etcdctl](/ru/docs/etcd/install/)  
* [Настройте локальный кластер](/ru/docs/etcd/dev-guide/local_cluster/)

## Получить ключи по префиксу {#get-keys-by-prefix}

```bash
$ etcdctl --endpoints=$ENDPOINTS get PREFIX --prefix
```

### Глобальные параметры {#global-options}

```bash
--endpoints=[127.0.0.1:2379], gRPC endpoints
```

### Параметры {#options}

```bash
--prefix, get a range of keys with matching prefix
```

### Пример {#example}

![03_etcdctl_get_by_prefix_2016050501](/docs/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
