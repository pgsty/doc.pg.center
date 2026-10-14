---
title: Запись в etcd
description: Добавление пары «ключ — значение» в кластер etcd
weight: 250
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tasks/developer/writing-to-etcd.md"
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
