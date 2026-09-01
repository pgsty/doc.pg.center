---
title: Как проводить выборы лидера в кластере etcd
description: Шаги проведения выборов лидера с помощью клиента etcdctl
weight: 900
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/tasks/operator/how-to-conduct-elections.md"
---

## Предварительные требования {#prerequisites}

- Убедитесь, что установлен [`etcd`](/ru/etcd/install/) и [`etcdctl`](/ru/etcd/install/).
- Проверьте наличие активного кластера etcd.

## Проведение выборов лидера {#conduct-leader-election}

Команда `etcdctl` используется для проведения выборов лидера в кластере etcd. Она гарантирует, что в один момент времени только один клиент может стать лидером.

`etcdctl --endpoints=$ENDPOINTS elect <election-name> [proposal]`

```shell
etcdctl --endpoints=$ENDPOINTS elect election-name p1
```

### Параметры {#options}

- `--endpoints : $ENDPOINTS`

Адрес каждого участника кластера etcd.

- `election-name` строка

Строка-идентификатор для выборов. Все участники, конкурирующие за лидерство, должны использовать одно и то же имя выборов.

- `leader-name` строка

Значение предложения нового лидера.

### Пример {#example}

```shell
./etcdctl elect my-election proposal1
my-election/694d99fafea88404
proposal1

another election:
./etcdctl elect new-election proposal1
new-election/694d99fafea8840f
proposal1
```
