---
title: Запись в etcd
description: Добавление пары ключ-значение в кластер etcd
weight: 250
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
aliases: [/etcd/tasks/developer/writing-to-etcd/]
---

## Предварительные условия {#prerequisites}

- Установите `etcdctl`

## Процедура {#procedure}

Используйте подкоманду `put` для записи пары «ключ — значение»:

```shell
etcdctl --endpoints=$ENDPOINTS put foo "Hello World!"
```
где:
- `foo` — имя ключа
- `"Hello World!"` — значение, заключённое в кавычки
