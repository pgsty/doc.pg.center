---
title: "REST API de Patroni"
weight: 40
icon: fa-solid fa-book
description: "Referencia de los endpoints de la REST API de Patroni y sus comportamientos operativos."
module: [PATRONI]
categories: [Referencia]
upstream_link: "https://patroni.readthedocs.io/en/latest/rest_api.html"
---

<a id="rest_api"></a>
Patroni dispone de una REST API completa, que es utilizada por el propio Patroni durante la carrera por el liderazgo, por la herramienta [patronictl](/es/patroni/patronictl#patronictl) para ejecutar conmutaciones por error/switchovers/reinicializaciones/reinicios/recargas, por HAProxy o cualquier otro tipo de balanceador de carga para realizar comprobaciones de estado HTTP y, por supuesto, también podría usarse para monitorización. A continuación encontrarás la lista de endpoints de la REST API de Patroni.

--------

## Endpoints de comprobación de estado {#health-check-endpoints}

Para todas las peticiones `GET` de comprobación de estado, Patroni devuelve un documento JSON con el estado del nodo, junto con el código de estado HTTP. Si no quieres o no necesitas el documento JSON, puedes considerar el uso del método `HEAD` u `OPTIONS` en lugar de `GET`.

- Las siguientes peticiones a la REST API de Patroni devolverán el código de estado HTTP **200** solo cuando el nodo de Patroni se esté ejecutando como primario con el bloqueo de líder:

  - `GET /`
  - `GET /primary`
  - `GET /read-write`

- `GET /standby-leader`: devuelve el código de estado HTTP **200** solo cuando el nodo de Patroni se está ejecutando como líder en un [clúster en espera](/es/patroni/standby_cluster#standby_cluster).

- `GET /leader`: devuelve el código de estado HTTP **200** cuando el nodo de Patroni tiene el bloqueo de líder. A diferencia de `GET /primary` y `GET /standby-leader`, esta comprobación no depende de si PostgreSQL se está ejecutando como `primary` o como `standby_leader`.

- `GET /replica`: endpoint de comprobación de estado de la réplica. Devuelve el código de estado HTTP **200** solo cuando el nodo de Patroni está en el estado `running`, el rol es `replica` y la etiqueta `noloadbalance` no está establecida.

- `GET /replica?replication_state=<required state>`: endpoint de comprobación de la réplica. Además de las comprobaciones de `replica`, también comprueba si el estado de replicación coincide con el requerido. Útil principalmente con `replication_state=streaming`, para excluir réplicas que aún se están poniendo al día en la recuperación desde archivo.

- `GET /replica?lag=<max-lag>`: endpoint de comprobación de la réplica. Además de las comprobaciones de `replica`, también comprueba la latencia de replicación y devuelve el código de estado **200** solo cuando está por debajo del valor especificado. Por motivos de rendimiento se utiliza la clave cluster.last_leader_operation del DCS como posición WAL del líder y para calcular la latencia en la réplica. max-lag puede especificarse en bytes (entero) o en valores legibles por humanos, por ejemplo 16kB, 64MB, 1GB.

  - `GET /replica?lag=1048576`
  - `GET /replica?lag=1024kB`
  - `GET /replica?lag=10MB`
  - `GET /replica?lag=1GB`

- `GET /replica?tag_key1=value1&tag_key2=value2`: endpoint de comprobación de la réplica. También comprueba las etiquetas definidas por el usuario `key1` y `key2` y sus respectivos valores en la sección **tags** de la gestión de la configuración yaml. Si la etiqueta no está definida para una instancia, o si el valor en la configuración yaml no coincide con el valor consultado, devolverá el código de estado HTTP 503.

  En las siguientes peticiones, dado que se comprueba el estado de líder o de líder en espera, Patroni no aplica ninguna de las etiquetas definidas por el usuario y estas serán ignoradas.

  - `GET /?tag_key1=value1&tag_key2=value2`
  - `GET /leader?tag_key1=value1&tag_key2=value2`
  - `GET /primary?tag_key1=value1&tag_key2=value2`
  - `GET /read-write?tag_key1=value1&tag_key2=value2`
  - `GET /standby_leader?tag_key1=value1&tag_key2=value2`
  - `GET /standby-leader?tag_key1=value1&tag_key2=value2`

- `GET /read-only`: como el endpoint anterior, pero incluye también al primario.

- `GET /synchronous` o `GET /sync`: devuelve el código de estado HTTP **200** solo cuando el nodo de Patroni se está ejecutando como nodo en espera síncrono.

- `GET /read-only-sync`: como el endpoint anterior, pero incluye también al primario.

- `GET /quorum`: devuelve el código de estado HTTP **200** solo cuando este nodo de Patroni está listado como nodo de cuórum en `synchronous_standby_names` del primario.

- `GET /read-only-quorum`: como el endpoint anterior, pero incluye también al primario.

- `GET /asynchronous` o `GET /async`: devuelve el código de estado HTTP **200** solo cuando el nodo de Patroni se está ejecutando como nodo en espera asíncrono.

- `GET /asynchronous?lag=<max-lag>` o `GET /async?lag=<max-lag>`: endpoint de comprobación del nodo en espera asíncrono. Además de las comprobaciones de `asynchronous` o `async`, también comprueba la latencia de replicación y devuelve el código de estado **200** solo cuando está por debajo del valor especificado. Por motivos de rendimiento se utiliza la clave cluster.last_leader_operation del DCS como posición WAL del líder y para calcular la latencia en la réplica. max-lag puede especificarse en bytes (entero) o en valores legibles por humanos, por ejemplo 16kB, 64MB, 1GB.

  - `GET /async?lag=1048576`
  - `GET /async?lag=1024kB`
  - `GET /async?lag=10MB`
  - `GET /async?lag=1GB`

- `GET /health`: devuelve el código de estado HTTP **200** solo cuando PostgreSQL está levantado y en ejecución.

- `GET /liveness`: devuelve el código de estado HTTP **200** si el bucle de latido de Patroni se está ejecutando correctamente y **503** si la última ejecución fue hace más de `ttl` segundos en el primario o `2*ttl` en la réplica. Podría usarse para `livenessProbe`.

- `GET /readiness?lag=<max-lag>&mode=apply|write`: devuelve el código de estado HTTP **200** cuando el nodo de Patroni se está ejecutando como líder o cuando PostgreSQL está levantado, replicando y no demasiado retrasado respecto al líder. El parámetro lag establece cuánto se permite que un nodo en espera se retrase, y su valor predeterminado es `maximum_lag_on_failover`. El lag puede especificarse en bytes o en valores legibles por humanos, por ejemplo 16kB, 64MB o 1GB. Mode establece si el WAL debe reproducirse (apply) o solo recibirse (write). El valor predeterminado es apply.

  Cuando se usa como `readinessProbe` de Kubernetes, garantizará que los pods recién iniciados solo pasen a estar listos cuando hayan alcanzado al líder. Esto, combinado con un PodDisruptionBudget, protege contra una terminación demasiado temprana del líder durante un reinicio progresivo de los nodos. También garantizará que las réplicas que no puedan mantener el ritmo de la replicación no atiendan tráfico de solo lectura. El endpoint podría usarse para `readinessProbe` cuando no es posible usar los endpoints de Kubernetes para las elecciones de líder (OpenShift).

El endpoint `liveness` es muy ligero y no ejecuta ninguna consulta SQL. Las sondas deben configurarse de manera que empiecen a fallar aproximadamente en el momento en que la clave de líder esté por expirar. Con el valor predeterminado de `ttl`, que es `30s`, unas sondas de ejemplo tendrían este aspecto:

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

## Endpoint de monitorización {#monitoring-endpoint}

El `GET /patroni` lo utiliza Patroni durante la carrera por el liderazgo. También podría ser usado por tu sistema de monitorización. El documento JSON producido por este endpoint tiene la misma estructura que el JSON producido por los endpoints de comprobación de estado.

**Ejemplo:** Un clúster saludable

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

**Ejemplo:** Un clúster desbloqueado

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

**Ejemplo:** Un clúster desbloqueado con el [modo a prueba de fallos del DCS](/es/patroni/dcs_failsafe_mode#dcs_failsafe_mode) habilitado

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

**Ejemplo:** Un clúster con el [modo de pausa](/es/patroni/pause#pause) habilitado

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

Recupera las métricas de Patroni en formato Prometheus a través del endpoint `GET /metrics`.

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

### Valores de estado de PostgreSQL {#postgresql-state-values}

La métrica `patroni_postgres_state` proporciona una representación numérica del estado actual de la instancia de PostgreSQL. Esto es útil para los sistemas de monitorización y alerta que necesitan seguir los cambios de estado a lo largo del tiempo. Los valores numéricos se generan utilizando el método estático `PostgresqlState.get_metrics_description()`.

| Valor | Nombre del estado       | Descripción                                 |
|-------|-------------------------|---------------------------------------------|
| 0     | initdb                  | Inicializando el clúster nuevo              |
| 1     | initdb_failed           | La inicialización del clúster nuevo falló   |
| 2     | custom_bootstrap        | Ejecutando un script de bootstrap personalizado |
| 3     | custom_bootstrap_failed | El script de bootstrap personalizado falló  |
| 4     | creating_replica        | Creando una réplica a partir del primario   |
| 5     | running                 | PostgreSQL se está ejecutando con normalidad |
| 6     | starting                | PostgreSQL se está iniciando                |
| 7     | bootstrap_starting      | Iniciándose tras un bootstrap personalizado |
| 8     | start_failed            | El inicio de PostgreSQL falló               |
| 9     | restarting              | PostgreSQL se está reiniciando              |
| 10    | restart_failed          | El reinicio de PostgreSQL falló             |
| 11    | stopping                | PostgreSQL se está deteniendo               |
| 12    | stopped                 | PostgreSQL está detenido                    |
| 13    | stop_failed             | La detención de PostgreSQL falló            |
| 14    | crashed                 | PostgreSQL ha caído                         |

Valores de estado de PostgreSQL

> [!NOTE]
> Estos valores numéricos son fijos y nunca cambiarán, para mantener la compatibilidad con los sistemas de monitorización existentes. Si en el futuro se añaden estados nuevos, se les asignarán nuevos valores numéricos sin cambiar los existentes.

--------

## Endpoints de estado del clúster {#cluster-status-endpoints}

- El endpoint `GET /cluster` genera un documento JSON que describe la topología y el estado actuales del clúster:

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

- El endpoint `GET /history` ofrece una vista del historial de switchovers/conmutaciones por error del clúster. El formato es muy similar al contenido de los archivos de historial del directorio `pg_wal`. La única diferencia es el campo de marca de tiempo que muestra cuándo se creó la nueva línea de tiempo.

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

## Endpoint de configuración {#config-endpoint}

`GET /config`: obtiene la versión actual de la configuración dinámica:

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

`PATCH /config`: cambia la configuración existente.

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

La llamada anterior a la REST API parchea la configuración existente y devuelve la configuración nueva.

Comprobemos que el nodo procesó esta configuración. En primer lugar, debería empezar a imprimir líneas de registro cada 5 segundos (loop_wait=5). El cambio de "max_connections" requiere un reinicio, por lo que la bandera "pending_restart" debería quedar expuesta:

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

Eliminación de parámetros:

Si quieres eliminar (restablecer) algún ajuste, simplemente parchéalo con `null`:

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

La llamada anterior elimina `postgresql.parameters.max_connections` de la configuración dinámica.

`PUT /config`: también es posible realizar la reescritura completa de una configuración dinámica existente de manera incondicional:

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

## Endpoints de switchover y conmutación por error {#switchover-and-failover-endpoints}

<a id="switchover_api"></a>

### Switchover {#switchover}

El endpoint `/switchover` solo funciona cuando el clúster está saludable (hay un líder). También permite programar un switchover para un momento dado.

Al llamar al endpoint `/switchover` se puede especificar un candidato, pero no es obligatorio, a diferencia del endpoint `/failover`. Si no se proporciona un candidato, todos los nodos elegibles del clúster participarán en la carrera por el liderazgo después de que el líder ceda su rol.

En el cuerpo JSON de la petición `POST` debes especificar el campo `leader`. Los campos `candidate` y `scheduled_at` son opcionales y pueden usarse para programar un switchover en un momento específico.

Según la situación, las peticiones pueden devolver diferentes códigos y cuerpos de estado HTTP. El código de estado **200** se devuelve cuando el switchover o la conmutación por error se completó con éxito. Si el switchover se programó con éxito, Patroni devolverá el código de estado HTTP **202**. En caso de que algo salga mal, se devolverá el código de error (uno de **400**, **412** o **503**) con algunos detalles en el cuerpo de la respuesta.

`DELETE /switchover` puede usarse para eliminar el switchover programado actualmente.

**Ejemplo:** realiza un switchover a cualquier nodo en espera saludable

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1"}'
Successfully switched over to "postgresql2"
```

**Ejemplo:** realiza un switchover a un nodo específico

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql1","candidate":"postgresql2"}'
Successfully switched over to "postgresql2"
```

**Ejemplo:** programa un switchover del líder a cualquier otro nodo en espera saludable del clúster en un momento específico.

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
Switchover scheduled
```

### Conmutación por error {#failover}

El endpoint `/failover` puede usarse para realizar una conmutación por error manual cuando no hay nodos saludables (por ejemplo, hacia un nodo en espera asíncrono si todos los nodos en espera síncronos no están lo suficientemente saludables para ser promovidos). Sin embargo, no existe el requisito de que el clúster no tenga líder: la conmutación por error también puede ejecutarse en un clúster saludable.

En el cuerpo JSON de la petición `POST` debes especificar el campo `candidate`. Si se especifica el campo `leader`, se desencadena un switchover en su lugar.

**Ejemplo:**

``` bash
$ curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
Successfully failed over to "postgresql1"
```

> [!WARNING]
> [Ten mucho cuidado](/es/patroni/rest_api#failover_healthcheck) al usar este endpoint, ya que puede provocar pérdida de datos en ciertas situaciones. En la mayoría de los casos, [el endpoint de switchover](/es/patroni/rest_api#switchover_api) satisface las necesidades del administrador.

Los endpoints `POST /switchover` y `POST /failover` los usan [patronictl_switchover](/es/patroni/patronictl#patronictl_switchover) y [patronictl_failover](/es/patroni/patronictl#patronictl_failover), respectivamente.

`DELETE /switchover` lo usa [patronictl flush cluster-name switchover](/es/patroni/patronictl#patronictl_flush_parameters).

|                              | Conmutación por error | Switchover                          |
|------------------------------|-----------------------|-------------------------------------|
| Requiere líder especificado  | no                    | sí                                  |
| Requiere candidato especificado | sí                 | no                                  |
| Puede ejecutarse en pausa    | sí                    | sí (solo a un candidato específico) |
| Puede programarse            | no                    | sí (si no está en pausa)            |

Comparación entre conmutación por error y switchover

<a id="failover_healthcheck"></a>

### Nodo en espera saludable {#healthy-standby}

Hay un par de comprobaciones que un miembro de un clúster debe superar para poder participar en la carrera por el liderazgo durante un switchover o para convertirse en líder como candidato de failover/switchover:

- ser accesible mediante la API de Patroni;
- no tener la etiqueta `nofailover` establecida en `true`;
- tener el watchdog totalmente funcional (si la configuración lo requiere);
- en caso de un switchover en un clúster saludable o de una conmutación por error automática, no exceder el retraso máximo de replicación (`maximum_lag_on_failover`, [parámetro de configuración](/es/patroni/config/dynamic#dynamic));
- en caso de un switchover en un clúster saludable o de una conmutación por error automática, no tener un número de línea de tiempo menor que la línea de tiempo del clúster si el [parámetro de configuración](/es/patroni/config/dynamic#dynamic) `check_timeline` está establecido en `true`;
- en el [modo síncrono](/es/patroni/replication_modes#synchronous_mode):
  - En caso de un switchover (tanto con como sin candidato): estar listado entre los miembros de la clave `/sync`;
  - Para una conmutación por error, tanto en clústeres saludables como no saludables, esta comprobación se omite.

> [!WARNING]
> En caso de una conmutación por error manual en un clúster sin líder, se permitirá que un candidato se promueva incluso si:
>
> - no está entre los miembros de la clave `/sync` cuando el modo síncrono está habilitado;
> - su retraso excede el retraso máximo de replicación permitido;
> - tiene un número de línea de tiempo menor que la última línea de tiempo conocida del clúster.

<a id="restart_endpoint"></a>

--------

## Endpoint de reinicio {#restart-endpoint}

- `POST /restart`: puedes reiniciar Postgres en el nodo específico realizando la llamada `POST /restart`. En el cuerpo JSON de la petición `POST` es posible especificar opcionalmente algunas condiciones de reinicio:
  - **restart_pending**: booleano; si se establece en `true`, Patroni reiniciará PostgreSQL solo cuando haya un reinicio pendiente para aplicar algunos cambios en la configuración de PostgreSQL.
  - **role**: realiza el reinicio solo si el rol actual del nodo coincide con el rol indicado en la petición POST.
  - **postgres_version**: realiza el reinicio solo si la versión actual de postgres es menor que la especificada en la petición POST.
  - **timeout**: cuánto debemos esperar antes de que PostgreSQL empiece a aceptar conexiones. Sobrescribe `primary_start_timeout`.
  - **schedule**: marca de tiempo con zona horaria; programa el reinicio en algún momento del futuro.
- `DELETE /restart`: elimina el reinicio programado

Los endpoints `POST /restart` y `DELETE /restart` los usan [patronictl_restart](/es/patroni/patronictl#patronictl_restart) y [patronictl flush cluster-name restart](/es/patroni/patronictl#patronictl_flush_parameters), respectivamente.

<a id="reload_endpoint"></a>

--------

## Endpoint de recarga {#reload-endpoint}

La llamada `POST /reload` ordenará a Patroni volver a leer y aplicar el archivo de configuración. Es el equivalente a enviar la señal `SIGHUP` al proceso de Patroni. Si cambiaste algunos de los parámetros de Postgres que requieren un reinicio (como **shared_buffers**), todavía tendrás que hacer explícitamente el reinicio de Postgres, ya sea llamando al endpoint `POST /restart` o con la ayuda de [patronictl_restart](/es/patroni/patronictl#patronictl_restart).

El endpoint de recarga lo usa [patronictl_reload](/es/patroni/patronictl#patronictl_reload).

--------

## Endpoint de reinicialización {#reinitialize-endpoint}

`POST /reinitialize`: reinicializa el directorio de datos de PostgreSQL en el nodo especificado. Solo se permite su ejecución en réplicas. Una vez invocado, eliminará el directorio de datos e iniciará `pg_basebackup` o algún [método de creación de réplicas](/es/patroni/replica_bootstrap#custom_replica_creation) alternativo.

La llamada puede fallar si Patroni está en un bucle intentando recuperar (reiniciar) un Postgres fallido. Para superar este problema se puede especificar `{"force":true}` en el cuerpo de la petición.

Puedes especificar {"from-leader":true} en el cuerpo de la petición para obtener directamente el basebackup desde el nodo líder. Esto es útil al ejecutar la reinicialización cuando fallan todos los nodos réplica.

El endpoint de reinicialización lo usa [patronictl_reinit](/es/patroni/patronictl#patronictl_reinit).
