---
title: "Документация Patroni 4.1.5"
linkTitle: Patroni
weight: 10
icon: fa-solid fa-heart-pulse
description: "Обзор документации Patroni по высокой доступности PostgreSQL."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PATRONI]
categories: [Концепция]
aliases: [/patroni/]
upstream_source: patroni
upstream_link: "https://patroni.readthedocs.io/en/latest/index.html"
cascade:
  upstream_source: patroni
  type: docs
  module: [PATRONI]
---

> [!WARNING]
> Работа Patroni на **системах с ограниченной памятью и Python 3.11+**

Если Patroni работает в системе со строгими ограничениями памяти, например с `vm.overcommit_memory=2` (рекомендуется для PostgreSQL), и используется Python 3.11 или новее, может наблюдаться неожиданное поведение:

- Patroni выглядит исправным
- PostgreSQL продолжает работать
- **REST API Patroni перестаёт отвечать**
- Операционная система сообщает, что Patroni прослушивает порт REST API
- Журналы Patroni выглядят нормально, однако однократно могут появиться сообщения `Exception ignored in thread started by: <object repr() failed>`, `MemoryError`
- Журналы ядра могут содержать сообщения наподобие `not enough memory for the allocation`

Это поведение вызвано [ошибкой в Python 3.11+](https://github.com/python/cpython/issues/140746). При строгих ограничениях памяти запуск нового потока может зависнуть на неопределённое время, если свободной памяти недостаточно.

## Рекомендуемое решение {#recommended-solution}

В последних выпусках Patroni (4.1.1+, 4.0.8+) влияние этой проблемы уменьшено: все необходимые потоки запускаются на раннем этапе запуска, прежде чем система окажется под давлением нехватки памяти.

## Дополнительные рекомендации (Linux, glibc) {#additional-recommendations-linux-glibc}

При работе с `vm.overcommit_memory=2` (рекомендуется для PostgreSQL) также рекомендуется запускать Patroni со следующими переменными окружения:

- `MALLOC_ARENA_MAX=1` — уменьшает объём виртуальной памяти, выделяемой glibc для многопоточных приложений
- `PG_MALLOC_ARENA_MAX=` — сбрасывает значение `MALLOC_ARENA_MAX` для процессов PostgreSQL, запускаемых Patroni.

Кроме того, можно настроить следующие параметры конфигурации Patroni:

- `thread_stack_size` — размер стека потоков, запускаемых Patroni. Уменьшение этого значения сокращает потребление памяти процессом Patroni. Значение по умолчанию, заданное Patroni, — `512kB`. Увеличьте `thread_stack_size`, если Patroni аварийно завершается из-за проблем со стеком; в противном случае значения по умолчанию достаточно.
- `thread_pool_size` — размер пула потоков, используемого Patroni для асинхронных задач и связи по REST API с другими участниками во время выбора лидера или отказоустойчивых проверок. Значение по умолчанию — `5`, чего достаточно для кластеров из трёх узлов.
- `restapi.thread_pool_size` — размер пула потоков для обработки запросов REST API. Значение по умолчанию — `5`, что позволяет параллельно обрабатывать до пяти запросов REST API. Обратите внимание: запросы, включающие SQL-запросы, фактически выполняются последовательно, поскольку используется одно соединение с базой данных, поэтому увеличение этого значения обычно не даёт преимуществ.

--------

Patroni — шаблон для решений высокой доступности (HA) PostgreSQL на Python. Для максимальной применимости Patroni поддерживает различные распределённые хранилища конфигурации, такие как [ZooKeeper](https://zookeeper.apache.org/), [etcd](https://github.com/coreos/etcd), [Consul](https://github.com/hashicorp/consul) и [Kubernetes](https://kubernetes.io). Надеемся, он будет полезен инженерам баз данных, администраторам баз данных, инженерам DevOps и SRE, которые хотят быстро развернуть PostgreSQL высокой доступности в центрах обработки данных — или где-либо ещё.

Мы называем Patroni «шаблоном», потому что это далеко не универсальная или готовая к работе система репликации. У неё будут свои подводные камни. Используйте её осмотрительно. Существует множество способов обеспечить высокую доступность PostgreSQL; их список приведён в [документации PostgreSQL](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling).

Поддерживаемые в настоящее время версии PostgreSQL: от 9.3 до 18.

**Примечание для пользователей Citus**: начиная с версии 3.0 Patroni хорошо интегрируется с расширением базы данных [Citus](https://github.com/citusdata/citus) для Postgres. Дополнительные сведения об использовании высокой доступности Patroni вместе с распределённым кластером Citus см. на [странице поддержки Citus](/ru/docs/patroni/citus#citus) в документации Patroni.

**Примечание для пользователей Kubernetes**: Patroni может работать непосредственно поверх Kubernetes. См. главу [Kubernetes](/ru/docs/patroni/kubernetes#kubernetes) документации Patroni.

<img src="/img/docs/patroni/patroni-logo.png" width="128" height="128" alt="изображение" />
