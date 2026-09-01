---
title: Как создавать блокировки
description: Руководство по созданию распределенных блокировок в etcd
weight: 800
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
---

LOCK приобретает распределённый мьютекс с указанным именем. Как только блокировка будет получена, она будет удерживаться до завершения работы etcdctl.

## Предварительные требования {#prerequisites}

* Установите [`etcd` и `etcdctl`](/ru/etcd/install/)

## Создание блокировки {#creating-a-lock}

`lock` для распределённой блокировки:

![08_etcdctl_lock_2016050501](/etcd/tasks/img/create-lock.gif)

```shell
etcdctl --endpoints=$ENDPOINTS lock mutex1
```

### Параметры {#options}
- endpoints — определяет список адресов машин в кластере, разделённых запятыми.
- ttl — время ожидания в секундах сессии блокировки.
