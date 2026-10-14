---
title: Как создавать блокировки
description: Руководство по созданию распределённых блокировок в etcd
weight: 800
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/how-to-create-locks.md"
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
- ttl — срок действия сессии блокировки в секундах.
