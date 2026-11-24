---
title: Как получить ключи по префиксу
description: Руководство по извлечению ключей etcd по их префиксу
weight: 300
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7/tasks/developer/how-to-get-key-by-prefix.md"
---

## Предварительные требования {#pre-requisites}

* [Установите etcdctl](/ru/etcd/install/)
* [Настройте локальный кластер](/ru/etcd/dev-guide/local_cluster/)

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

![03_etcdctl_get_by_prefix_2016050501](/etcd/tasks/img/get-by-prefix.gif)

```shell
etcdctl --endpoints=$ENDPOINTS put web1 value1
etcdctl --endpoints=$ENDPOINTS put web2 value2
etcdctl --endpoints=$ENDPOINTS put web3 value3

etcdctl --endpoints=$ENDPOINTS get web --prefix
```
