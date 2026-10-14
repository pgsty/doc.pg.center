---
title: "Patroni REST API"
weight: 40
icon: fa-solid fa-book
description: "Справочник по конечным точкам REST API Patroni и их рабочему поведению."
module: [PATRONI]
categories: [Справочник]
aliases: [/patroni/rest_api/]
upstream_link: "https://patroni.readthedocs.io/en/latest/rest_api.html"
---

<a id="rest_api"></a>
Patroni предоставляет обширный REST API. Сам Patroni использует его во время выбора лидера, инструмент [patronictl](/ru/docs/patroni/patronictl#patronictl) — для аварийных и плановых переключений, повторной инициализации, перезапусков и перезагрузки конфигурации, а HAProxy и другие балансировщики — для проверок работоспособности HTTP. API также можно применять для мониторинга. Ниже перечислены конечные точки REST API Patroni.

--------

## Конечные точки проверки работоспособности {#health-check-endpoints}

На все запросы проверки `GET` Patroni возвращает документ JSON с состоянием узла и код состояния HTTP. Если документ JSON не нужен, вместо `GET` можно использовать метод `HEAD` или `OPTIONS`.

- Следующие запросы REST API Patroni возвращают код HTTP **200**, только когда узел Patroni работает как первичный сервер и владеет блокировкой лидера:

  - `GET /`
  - `GET /primary`
  - `GET /read-write`

- `GET /standby-leader`: возвращает код HTTP **200**, только когда узел Patroni является лидером [резервного кластера](/ru/docs/patroni/standby_cluster#standby_cluster).

- `GET /leader`: возвращает код HTTP **200**, когда узел Patroni владеет блокировкой лидера. В отличие от `GET /primary` и `GET /standby-leader`, эта проверка не зависит от того, работает ли PostgreSQL как `primary` или `standby_leader`.

- `GET /replica`: конечная точка проверки реплики. Возвращает код HTTP **200**, только когда узел Patroni находится в состоянии `running`, его роль — `replica`, а тег `noloadbalance` не задан.

- `GET /replica?replication_state=<required state>`: конечная точка проверки реплики. Помимо проверок `replica` она проверяет соответствие состояния репликации требуемому. Особенно полезна с `replication_state=streaming`, чтобы исключить реплики, которые ещё догоняют кластер при восстановлении из архива.

- `GET /replica?lag=<max-lag>`: конечная точка проверки реплики. Помимо проверок `replica` она проверяет отставание репликации и возвращает код **200**, только если оно меньше заданного значения. Для повышения производительности ключ cluster.last_leader_operation из DCS используется как позиция wal лидера при вычислении отставания реплики. max-lag задаётся в байтах целым числом или понятным человеку значением, например 16kB, 64MB, 1GB.

  - `GET /replica?lag=1048576`
  - `GET /replica?lag=1024kB`
  - `GET /replica?lag=10MB`
  - `GET /replica?lag=1GB`

- `GET /replica?tag_key1=value1&tag_key2=value2`: конечная точка проверки реплики. Дополнительно проверяет пользовательские теги `key1` и `key2` и их значения в разделе **tags** конфигурации yaml. Если тег не определён для экземпляра или его значение не совпадает со значением запроса, возвращается код HTTP 503.

  В следующих запросах проверяется состояние leader или standby-leader, поэтому Patroni игнорирует все пользовательские теги.

  - `GET /?tag_key1=value1&tag_key2=value2`
  - `GET /leader?tag_key1=value1&tag_key2=value2`
  - `GET /primary?tag_key1=value1&tag_key2=value2`
  - `GET /read-write?tag_key1=value1&tag_key2=value2`
  - `GET /standby_leader?tag_key1=value1&tag_key2=value2`
  - `GET /standby-leader?tag_key1=value1&tag_key2=value2`

- `GET /read-only`: аналогична предыдущей конечной точке, но также включает первичный сервер.

- `GET /synchronous` или `GET /sync`: возвращает код HTTP **200**, только когда узел Patroni работает как синхронный резервный сервер.

- `GET /read-only-sync`: аналогична предыдущей конечной точке, но также включает первичный сервер.

- `GET /quorum`: возвращает код HTTP **200**, только когда этот узел Patroni указан как узел кворума в `synchronous_standby_names` первичного сервера.

- `GET /read-only-quorum`: аналогична предыдущей конечной точке, но также включает первичный сервер.

- `GET /asynchronous` или `GET /async`: возвращает код HTTP **200**, только когда узел Patroni работает как асинхронный резервный сервер.

- `GET /asynchronous?lag=<max-lag>` или `GET /async?lag=<max-lag>`: конечная точка проверки асинхронного резервного сервера. Помимо проверок `asynchronous` или `async` она проверяет отставание репликации и возвращает код **200**, только если оно меньше заданного значения. Для повышения производительности ключ cluster.last_leader_operation из DCS используется как позиция wal лидера при вычислении отставания реплики. max-lag задаётся в байтах целым числом или понятным человеку значением, например 16kB, 64MB, 1GB.

  - `GET /async?lag=1048576`
  - `GET /async?lag=1024kB`
  - `GET /async?lag=10MB`
  - `GET /async?lag=1GB`

- `GET /health`: возвращает код HTTP **200**, только когда PostgreSQL запущен и работает.

- `GET /liveness`: возвращает код HTTP **200**, если цикл сигналов активности Patroni работает правильно, и **503**, если последняя итерация на первичном сервере была более `ttl` секунд назад или более `2*ttl` назад на реплике. Можно использовать для `livenessProbe`.

- `GET /readiness?lag=<max-lag>&mode=apply|write`: возвращает код HTTP **200**, когда узел Patroni является лидером либо когда PostgreSQL запущен, реплицируется и не слишком отстаёт от лидера. Параметр lag задаёт допустимое отставание резервного сервера и по умолчанию равен `maximum_lag_on_failover`. Параметр `lag` можно указать в байтах или понятных человеку значениях, например 16kB, 64MB или 1GB. Параметр `mode` определяет, должен ли WAL быть воспроизведён (apply) или только получен (write). По умолчанию используется apply.

  При использовании как `readinessProbe` Kubernetes конечная точка допускает готовность недавно запущенных подов только после того, как они догнали лидера. В сочетании с PodDisruptionBudget это защищает от слишком раннего завершения лидера при скользящем перезапуске узлов. Кроме того, не успевающие за репликацией реплики не обслуживают трафик только для чтения. Конечную точку можно использовать для `readinessProbe`, когда конечные точки Kubernetes нельзя применять для выборов лидера (OpenShift).

Конечная точка `liveness` очень легковесна и не выполняет SQL. Проверки следует настроить так, чтобы они начинали завершаться ошибкой примерно к моменту истечения ключа лидера. При значении `ttl` по умолчанию `30s` пример выглядит так:

```yaml
readinessProbe:
  httpGet:
    scheme: HTTP
    path: /readiness
    port: 8008
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
livenessProbe:
  httpGet:
    scheme: HTTP
    path: /liveness
    port: 8008
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

--------

## Конечная точка мониторинга {#monitoring-endpoint}

Patroni использует `GET /patroni` при выборе лидера. Её также может использовать система мониторинга. Создаваемый этой конечной точкой документ JSON имеет ту же структуру, что и документы конечных точек проверки работоспособности.

**Пример:** исправный кластер

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "primary",
  "server_version": 160004,
  "xlog": {
    "location": 67395656
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "dcs_last_seen": 1692356718,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**Пример:** кластер без блокировки

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "received_location": 67419744,
    "replayed_location": 67419744,
    "replayed_timestamp": null,
    "paused": false
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "cluster_unlocked": true,
  "dcs_last_seen": 1692356928,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**Пример:** кластер без блокировки с включённым [отказоустойчивым режимом DCS](/ru/docs/patroni/dcs_failsafe_mode#dcs_failsafe_mode)

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "location": 67420024
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "cluster_unlocked": true,
  "failsafe_mode_is_active": true,
  "dcs_last_seen": 1692356928,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

**Пример:** кластер с включённым [режимом паузы](/ru/docs/patroni/pause#pause)

``` bash
$ curl -s http://localhost:8008/patroni  | jq .
{
  "state": "running",
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "role": "replica",
  "server_version": 160004,
  "xlog": {
    "location": 67420024
  },
  "timeline": 1,
  "replication": [
    {
      "usename": "replicator",
      "application_name": "patroni2",
      "client_addr": "10.89.0.6",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    },
    {
      "usename": "replicator",
      "application_name": "patroni3",
      "client_addr": "10.89.0.2",
      "state": "streaming",
      "sync_state": "async",
      "sync_priority": 0
    }
  ],
  "pause": true,
  "dcs_last_seen": 1724874295,
  "tags": {
    "clonefrom": true
  },
  "database_system_identifier": "7268616322854375442",
  "patroni": {
    "version": "4.0.0",
    "scope": "demo",
    "name": "patroni1"
  }
}
```

Получите метрики Patroni в формате Prometheus через конечную точку `GET /metrics`.

``` bash
$ curl http://localhost:8008/metrics

# HELP patroni_version Patroni semver without periods. \
# TYPE patroni_version gauge
patroni_version{scope="batman",name="patroni1"} 040000
# HELP patroni_postgres_running Value is 1 if Postgres is running, 0 otherwise.
# TYPE patroni_postgres_running gauge
patroni_postgres_running{scope="batman",name="patroni1"} 1
# HELP patroni_postmaster_start_time Epoch seconds since Postgres started.
# TYPE patroni_postmaster_start_time gauge
patroni_postmaster_start_time{scope="batman",name="patroni1"} 1724873966.352526
# HELP patroni_primary Value is 1 if this node is the leader, 0 otherwise.
# TYPE patroni_primary gauge
patroni_primary{scope="batman",name="patroni1"} 1
# HELP patroni_xlog_location Current location of the Postgres transaction log, 0 if this node is not the leader.
# TYPE patroni_xlog_location counter
patroni_xlog_location{scope="batman",name="patroni1"} 22320573386952
# HELP patroni_standby_leader Value is 1 if this node is the standby_leader, 0 otherwise.
# TYPE patroni_standby_leader gauge
patroni_standby_leader{scope="batman",name="patroni1"} 0
# HELP patroni_replica Value is 1 if this node is a replica, 0 otherwise.
# TYPE patroni_replica gauge
patroni_replica{scope="batman",name="patroni1"} 0
# HELP patroni_sync_standby Value is 1 if this node is a sync standby replica, 0 otherwise.
# TYPE patroni_sync_standby gauge
patroni_sync_standby{scope="batman",name="patroni1"} 0
# HELP patroni_quorum_standby Value is 1 if this node is a quorum standby replica, 0 otherwise.
# TYPE patroni_quorum_standby gauge
patroni_quorum_standby{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_received_location Current location of the received Postgres transaction log, 0 if this node is not a replica.
# TYPE patroni_xlog_received_location counter
patroni_xlog_received_location{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_replayed_location Current location of the replayed Postgres transaction log, 0 if this node is not a replica.
# TYPE patroni_xlog_replayed_location counter
patroni_xlog_replayed_location{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_replayed_timestamp Current timestamp of the replayed Postgres transaction log, 0 if null.
# TYPE patroni_xlog_replayed_timestamp gauge
patroni_xlog_replayed_timestamp{scope="batman",name="patroni1"} 0
# HELP patroni_xlog_paused Value is 1 if the Postgres xlog is paused, 0 otherwise.
# TYPE patroni_xlog_paused gauge
patroni_xlog_paused{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_streaming Value is 1 if Postgres is streaming, 0 otherwise.
# TYPE patroni_postgres_streaming gauge
patroni_postgres_streaming{scope="batman",name="patroni1"} 1
# HELP patroni_postgres_in_archive_recovery Value is 1 if Postgres is replicating from archive, 0 otherwise.
# TYPE patroni_postgres_in_archive_recovery gauge
patroni_postgres_in_archive_recovery{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_server_version Version of Postgres (if running), 0 otherwise.
# TYPE patroni_postgres_server_version gauge
patroni_postgres_server_version{scope="batman",name="patroni1"} 160004
# HELP patroni_cluster_unlocked Value is 1 if the cluster is unlocked, 0 if locked.
# TYPE patroni_cluster_unlocked gauge
patroni_cluster_unlocked{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_mode_is_active Value is 1 if failsafe mode is active, 0 otherwise.
# TYPE patroni_failsafe_mode_is_active gauge
patroni_failsafe_mode_is_active{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_mode_enabled Value is 1 if failsafe_mode is enabled, 0 otherwise.
# TYPE patroni_failsafe_mode_enabled gauge
patroni_failsafe_mode_enabled{scope="batman",name="patroni1"} 0
# HELP patroni_failsafe_member Value is 1 if this node is a member of failsafe, 0 otherwise.
# TYPE patroni_failsafe_member gauge
patroni_failsafe_member{scope="batman",name="patroni1"} 0
# HELP patroni_postgres_timeline Postgres timeline of this node (if running), 0 otherwise.
# TYPE patroni_postgres_timeline gauge
patroni_postgres_timeline{scope="batman",name="patroni1"} 24
# HELP patroni_dcs_last_seen Epoch timestamp when DCS was last contacted successfully by Patroni.
# TYPE patroni_dcs_last_seen gauge
patroni_dcs_last_seen{scope="batman",name="patroni1"} 1724874235
# HELP patroni_pending_restart Value is 1 if the node needs a restart, 0 otherwise.
# TYPE patroni_pending_restart gauge
patroni_pending_restart{scope="batman",name="patroni1"} 1
# HELP patroni_is_paused Value is 1 if auto failover is disabled, 0 otherwise.
# TYPE patroni_is_paused gauge
patroni_is_paused{scope="batman",name="patroni1"} 1
# HELP patroni_postgres_state Numeric representation of Postgres state.
# Values: 0=initdb, 1=initdb_failed, 2=custom_bootstrap, 3=custom_bootstrap_failed, 4=creating_replica, 5=running, 6=starting, 7=bootstrap_starting, 8=start_failed, 9=restarting, 10=restart_failed, 11=stopping, 12=stopped, 13=stop_failed, 14=crashed
# TYPE patroni_postgres_state gauge
patroni_postgres_state{scope="batman",name="patroni1"} 5
# HELP patroni_failover_priority Failover priority of this node.
# TYPE patroni_failover_priority gauge
patroni_failover_priority{scope="batman",name="patroni1"} 1
```

### Значения состояния PostgreSQL {#postgresql-state-values}

Метрика `patroni_postgres_state` предоставляет числовое представление текущего состояния экземпляра PostgreSQL. Это полезно системам мониторинга и оповещений, отслеживающим изменения состояния во времени. Числовые значения создаются статическим методом `PostgresqlState.get_metrics_description()`.

| Значение | Имя состояния          | Описание                             |
|-------|-------------------------|--------------------------------------|
| 0     | initdb                  | Инициализация нового кластера        |
| 1     | initdb_failed           | Ошибка инициализации нового кластера |
| 2     | custom_bootstrap        | Выполнение пользовательского сценария инициализации |
| 3     | custom_bootstrap_failed | Ошибка пользовательского сценария инициализации |
| 4     | creating_replica        | Создание реплики с первичного сервера |
| 5     | running                 | PostgreSQL работает нормально       |
| 6     | starting                | PostgreSQL запускается               |
| 7     | bootstrap_starting      | Запуск после пользовательской инициализации |
| 8     | start_failed            | Ошибка запуска PostgreSQL            |
| 9     | restarting              | PostgreSQL перезапускается           |
| 10    | restart_failed          | Ошибка перезапуска PostgreSQL        |
| 11    | stopping                | PostgreSQL останавливается           |
| 12    | stopped                 | PostgreSQL остановлен                |
| 13    | stop_failed             | Ошибка остановки PostgreSQL          |
| 14    | crashed                 | PostgreSQL аварийно завершился       |

Значения состояния PostgreSQL

> [!NOTE]
> Эти числовые значения фиксированы и никогда не изменятся для сохранения обратной совместимости с существующими системами мониторинга. Новым состояниям будут назначаться новые числа без изменения существующих.

--------

## Конечные точки состояния кластера {#cluster-status-endpoints}

- Конечная точка `GET /cluster` создаёт документ JSON с текущей топологией и состоянием кластера:

``` bash
$ curl -s http://localhost:8008/cluster | jq .
{
  "members": [
    {
      "name": "patroni1",
      "role": "leader",
      "state": "running",
      "api_url": "http://10.89.0.4:8008/patroni",
      "host": "10.89.0.4",
      "port": 5432,
      "timeline": 5,
      "tags": {
        "clonefrom": true
      }
    },
    {
      "name": "patroni2",
      "role": "replica",
      "state": "streaming",
      "api_url": "http://10.89.0.6:8008/patroni",
      "host": "10.89.0.6",
      "port": 5433,
      "timeline": 5,
      "tags": {
        "clonefrom": true
      },
      "receive_lag": 0,
      "receive_lsn": "0/4000060",
      "replay_lag": 0,
      "replay_lsn": "0/4000060",
      "lag": 0,
      "lsn": "0/4000060"
    }
  ],
  "scope": "demo",
  "scheduled_switchover": {
    "at": "2023-09-24T10:36:00+02:00",
    "from": "patroni1",
    "to": "patroni3"
  }
}
```

- Конечная точка `GET /history` показывает историю плановых и аварийных переключений кластера. Формат очень похож на содержимое файлов истории в каталоге `pg_wal`; единственное отличие — поле времени создания новой временной шкалы.

``` bash
$ curl -s http://localhost:8008/history | jq .
[
  [
    1,
    25623960,
    "no recovery target specified",
    "2019-09-23T16:57:57+02:00"
  ],
  [
    2,
    25624344,
    "no recovery target specified",
    "2019-09-24T09:22:33+02:00"
  ],
  [
    3,
    25624752,
    "no recovery target specified",
    "2019-09-24T09:26:15+02:00"
  ],
  [
    4,
    50331856,
    "no recovery target specified",
    "2019-09-24T09:35:52+02:00"
  ]
]
```

<a id="config_endpoint"></a>

--------

## Конечная точка конфигурации {#config-endpoint}

`GET /config`: получить текущую версию динамической конфигурации:

``` bash
$ curl -s http://localhost:8008/config | jq .
{
  "ttl": 30,
  "loop_wait": 10,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5,
      "max_connections": "100"
    }
  }
}
```

`PATCH /config`: изменить существующую конфигурацию.

``` bash
$ curl -s -XPATCH -d \
    '{"loop_wait":5,"ttl":20,"postgresql":{"parameters":{"max_connections":"101"}}}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "loop_wait": 5,
  "maximum_lag_on_failover": 1048576,
  "retry_timeout": 10,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5,
      "max_connections": "101"
    }
  }
}
```

Приведённый вызов REST API изменяет существующую конфигурацию и возвращает новую.

Проверим, что узел обработал конфигурацию. Сначала он должен начать выводить строки журнала каждые 5 секунд (loop_wait=5). Изменение «max_connections» требует перезапуска, поэтому должен появиться флаг «pending_restart»:

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "postmaster_start_time": "2024-08-28 19:39:26.352526+00:00",
  "xlog": {
    "location": 2197818976
  },
  "timeline": 1,
  "dcs_last_seen": 1724874545,
  "database_system_identifier": "7408277255830290455",
  "pending_restart": true,
  "pending_restart_reason": {
    "max_connections": {
      "old_value": "100",
      "new_value": "101"
    }
  },
  "patroni": {
    "version": "4.0.0",
    "scope": "batman",
    "name": "patroni1"
  },
  "state": "running",
  "role": "primary",
  "server_version": 160004
}
```

Удаление параметров:

Чтобы удалить или сбросить параметр, измените его на `null`:

``` bash
$ curl -s -XPATCH -d \
    '{"postgresql":{"parameters":{"max_connections":null}}}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "loop_wait": 5,
  "retry_timeout": 10,
  "maximum_lag_on_failover": 1048576,
  "postgresql": {
    "use_slots": true,
    "use_pg_rewind": true,
    "parameters": {
      "hot_standby": "on",
      "unix_socket_directories": ".",
      "wal_level": "hot_standby",
      "max_wal_senders": 5,
      "max_replication_slots": 5
    }
  }
}
```

Приведённый вызов удаляет `postgresql.parameters.max_connections` из динамической конфигурации.

`PUT /config`: также можно безусловно полностью перезаписать существующую динамическую конфигурацию:

``` bash
$ curl -s -XPUT -d \
    '{"maximum_lag_on_failover":1048576,"retry_timeout":10,"postgresql":{"use_slots":true,"use_pg_rewind":true,"parameters":{"hot_standby":"on","wal_level":"hot_standby","unix_socket_directories":".","max_wal_senders":5}},"loop_wait":3,"ttl":20}' \
    http://localhost:8008/config | jq .
{
  "ttl": 20,
  "maximum_lag_on_failover": 1048576,
  "retry_timeout": 10,
  "postgresql": {
    "use_slots": true,
    "parameters": {
      "hot_standby": "on",
      "unix_socket_directories": ".",
      "wal_level": "hot_standby",
      "max_wal_senders": 5
    },
    "use_pg_rewind": true
  },
  "loop_wait": 3
}
```

--------

## Конечные точки планового и аварийного переключения {#switchover-and-failover-endpoints}

<a id="switchover_api"></a>

### Плановое переключение {#switchover}

Конечная точка `/switchover` работает только в исправном кластере с лидером. Она также позволяет запланировать переключение на заданное время.

При вызове `/switchover` кандидата можно указать, но, в отличие от `/failover`, это не обязательно. Если кандидат не задан, после понижения лидера в выборах участвуют все подходящие узлы кластера.

В теле JSON запроса `POST` необходимо указать поле `leader`. Поля `candidate` и `scheduled_at` необязательны и позволяют запланировать переключение на определённое время.

В зависимости от ситуации запросы возвращают разные коды и тела HTTP. Код **200** означает успешное завершение планового или аварийного переключения. При успешном планировании Patroni возвращает код HTTP **202**. При ошибке возвращается один из кодов **400**, **412** или **503** с подробностями в теле ответа.

`DELETE /switchover` удаляет текущее запланированное переключение.

**Пример:** переключение на любой исправный резервный сервер

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1"}'
Successfully switched over to "postgresql2"
```

**Пример:** переключение на определённый узел

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql1","candidate":"postgresql2"}'
Successfully switched over to "postgresql2"
```

**Пример:** запланировать переключение с лидера на любой другой исправный резервный сервер кластера в определённое время.

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
Switchover scheduled
```

### Аварийное переключение {#failover}

Конечная точка `/failover` позволяет выполнить ручное аварийное переключение при отсутствии исправных узлов, например на асинхронный резервный сервер, если все синхронные недостаточно исправны для повышения. Однако отсутствие лидера не является обязательным условием: аварийное переключение можно запустить и в исправном кластере.

В теле JSON запроса `POST` необходимо указать поле `candidate`. Если задано поле `leader`, вместо этого запускается плановое переключение.

**Пример:**

``` bash
$ curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
Successfully failed over to "postgresql1"
```

> [!WARNING]
> [Будьте предельно осторожны](/ru/docs/patroni/rest_api#failover_healthcheck) при использовании этой конечной точки: в некоторых ситуациях она может привести к потере данных. В большинстве случаев потребности администратора удовлетворяет [конечная точка планового переключения](/ru/docs/patroni/rest_api#switchover_api).

Конечные точки `POST /switchover` и `POST /failover` используются соответственно [patronictl_switchover](/ru/docs/patroni/patronictl#patronictl_switchover) и [patronictl_failover](/ru/docs/patroni/patronictl#patronictl_failover).

`DELETE /switchover` используется командой [patronictl flush cluster-name switchover](/ru/docs/patroni/patronictl#patronictl_flush_parameters).

|                              | Аварийное переключение | Плановое переключение             |
|------------------------------|----------|------------------------------------|
| Требуется указать лидера     | нет      | да                                 |
| Требуется указать кандидата  | да       | нет                                |
| Можно выполнить в паузе      | да       | да (только на заданного кандидата) |
| Можно запланировать          | нет      | да (если кластер не на паузе)      |

Сравнение аварийного и планового переключения

<a id="failover_healthcheck"></a>

### Исправный резервный сервер {#healthy-standby}

Чтобы участвовать в выборах лидера при плановом переключении или стать лидером как кандидат аварийного либо планового переключения, участнику следует пройти несколько проверок:

- быть доступным через API Patroni;
- не иметь тег `nofailover`, равный `true`;
- иметь полностью работоспособный сторожевой таймер, если того требует конфигурация;
- при плановом переключении в исправном кластере или автоматическом аварийном переключении не превышать максимальное отставание репликации (параметр [конфигурации](/ru/docs/patroni/config/dynamic#dynamic) `maximum_lag_on_failover`);
- при плановом переключении в исправном кластере или автоматическом аварийном переключении не иметь номер временной шкалы меньше шкалы кластера, если параметр [конфигурации](/ru/docs/patroni/config/dynamic#dynamic) `check_timeline` равен `true`;
- в [синхронном режиме](/ru/docs/patroni/replication_modes#synchronous_mode):
  - при плановом переключении с кандидатом или без него быть перечисленным среди участников ключа `/sync`;
  - при аварийном переключении как в исправном, так и в неисправном кластере эта проверка пропускается.

> [!WARNING]
> При ручном аварийном переключении в кластере без лидера кандидату разрешается повышение, даже если:
>
> - при включённом синхронном режиме его нет среди участников ключа `/sync`;
> - его отставание превышает допустимый максимум;
> - номер его временной шкалы меньше последней известной шкалы кластера.

<a id="restart_endpoint"></a>

--------

## Конечная точка перезапуска {#restart-endpoint}

- `POST /restart`: перезапускает Postgres на определённом узле вызовом `POST /restart`. В теле JSON запроса `POST` можно необязательно указать условия перезапуска:
  - **restart_pending**: логическое значение; при `true` Patroni перезапускает PostgreSQL только при ожидающем перезапуске для применения изменений конфигурации.
  - **role**: выполнять перезапуск, только если текущая роль узла совпадает с ролью запроса POST.
  - **postgres_version**: выполнять перезапуск, только если текущая версия postgres меньше указанной в запросе POST.
  - **timeout**: время ожидания начала приёма соединений PostgreSQL. Переопределяет `primary_start_timeout`.
  - **schedule**: временная метка с часовым поясом для планирования перезапуска в будущем.
- `DELETE /restart`: удаляет запланированный перезапуск

Конечные точки `POST /restart` и `DELETE /restart` используются соответственно [patronictl_restart](/ru/docs/patroni/patronictl#patronictl_restart) и [patronictl flush cluster-name restart](/ru/docs/patroni/patronictl#patronictl_flush_parameters).

<a id="reload_endpoint"></a>

--------

## Конечная точка перезагрузки конфигурации {#reload-endpoint}

Вызов `POST /reload` требует от Patroni повторно прочитать и применить файл конфигурации. Это эквивалентно отправке процессу Patroni сигнала `SIGHUP`. Если изменены параметры Postgres, требующие перезапуска, например **shared_buffers**, Postgres всё равно нужно явно перезапустить через конечную точку `POST /restart` или [patronictl_restart](/ru/docs/patroni/patronictl#patronictl_restart).

Конечная точка перезагрузки используется [patronictl_reload](/ru/docs/patroni/patronictl#patronictl_reload).

--------

## Конечная точка повторной инициализации {#reinitialize-endpoint}

`POST /reinitialize`: повторно инициализирует каталог данных PostgreSQL на заданном узле. Разрешено выполнять только на репликах. Вызов удаляет каталог данных и запускает `pg_basebackup` либо другой [метод создания реплики](/ru/docs/patroni/replica_bootstrap#custom_replica_creation).

Вызов может завершиться ошибкой, если Patroni циклически пытается восстановить или перезапустить отказавший Postgres. Чтобы обойти проблему, укажите `{"force":true}` в теле запроса.

В теле запроса можно указать {"from-leader":true}, чтобы получить basebackup непосредственно с узла-лидера. Это полезно при повторной инициализации после отказа всех узлов-реплик.

Конечная точка повторной инициализации используется [patronictl_reinit](/ru/docs/patroni/patronictl#patronictl_reinit).
