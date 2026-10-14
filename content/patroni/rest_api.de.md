---
title: "Patroni REST API"
weight: 40
icon: fa-solid fa-book
description: "Referenz der REST-API-Endpunkte von Patroni und ihres Betriebsverhaltens."
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/rest_api.html"
---

<a id="rest_api"></a>
Patroni bietet eine umfangreiche REST API. Patroni selbst nutzt sie bei der Leader-Wahl, das Werkzeug [patronictl](/de/patroni/patronictl#patronictl) für Failover, Switchover, Neuinitialisierung, Neustart und Neuladen sowie HAProxy und andere Load-Balancer für HTTP Health Checks. Sie kann auch zur Überwachung verwendet werden. Nachfolgend sind die REST-API-Endpunkte von Patroni aufgeführt.

--------

## Endpunkte für Health Checks {#health-check-endpoints}

Bei allen `GET`-Anfragen für Health Checks gibt Patroni neben dem HTTP-Statuscode ein JSON-Dokument mit dem Zustand des Knotens zurück. Wenn das JSON-Dokument nicht gewünscht oder benötigt wird, kann anstelle von `GET` die Methode `HEAD` oder `OPTIONS` verwendet werden.

- Die folgenden Anfragen an die REST API von Patroni liefern den HTTP-Statuscode **200** nur dann, wenn der Patroni-Knoten als Primärserver mit Leader-Lock läuft:

  - `GET /`
  - `GET /primary`
  - `GET /read-write`

- `GET /standby-leader`: Liefert den HTTP-Statuscode **200** nur dann, wenn der Patroni-Knoten als Leader in einem [Standby-Cluster](/de/patroni/standby_cluster#standby_cluster) läuft.

- `GET /leader`: Liefert den HTTP-Statuscode **200**, wenn der Patroni-Knoten den Leader-Lock hält. Anders als bei `GET /primary` und `GET /standby-leader` hängt diese Prüfung nicht davon ab, ob PostgreSQL als `primary` oder als `standby_leader` läuft.

- `GET /replica`: Endpunkt für den Health Check eines Replikats. Liefert den HTTP-Statuscode **200** nur dann, wenn der Patroni-Knoten den Zustand `running` und die Rolle `replica` hat und das Tag `noloadbalance` nicht gesetzt ist.

- `GET /replica?replication_state=<required state>`: Endpunkt zur Prüfung eines Replikats. Prüft zusätzlich zu den Prüfungen von `replica`, ob der Replikationszustand dem geforderten Zustand entspricht. Vor allem mit `replication_state=streaming` nützlich, um Replikate auszuschließen, die noch mittels Archiv-Recovery aufholen.

- `GET /replica?lag=<max-lag>`: Endpunkt zur Prüfung eines Replikats. Prüft zusätzlich zu den Prüfungen von `replica` den Replikationsrückstand und liefert den Statuscode **200** nur dann, wenn er unter dem angegebenen Wert liegt. Aus Leistungsgründen wird der Schlüssel cluster.last_leader_operation aus dem DCS für die WAL-Position des Leaders und zur Berechnung des Rückstands des Replikats verwendet. max-lag kann in Bytes (als Ganzzahl) oder in lesbarer Form angegeben werden, z. B. 16kB, 64MB, 1GB.

  - `GET /replica?lag=1048576`
  - `GET /replica?lag=1024kB`
  - `GET /replica?lag=10MB`
  - `GET /replica?lag=1GB`

- `GET /replica?tag_key1=value1&tag_key2=value2`: Endpunkt zur Prüfung eines Replikats. Prüft zusätzlich die benutzerdefinierten Tags `key1` und `key2` und ihre jeweiligen Werte im Abschnitt **tags** der YAML-Konfiguration. Wenn das Tag für eine Instanz nicht definiert ist oder der Wert in der YAML-Konfiguration nicht mit dem abgefragten Wert übereinstimmt, wird der HTTP-Statuscode 503 zurückgegeben.

  Bei den folgenden Anfragen wird der Status als Leader oder Standby-Leader geprüft. Daher berücksichtigt Patroni keine benutzerdefinierten Tags und ignoriert sie.

  - `GET /?tag_key1=value1&tag_key2=value2`
  - `GET /leader?tag_key1=value1&tag_key2=value2`
  - `GET /primary?tag_key1=value1&tag_key2=value2`
  - `GET /read-write?tag_key1=value1&tag_key2=value2`
  - `GET /standby_leader?tag_key1=value1&tag_key2=value2`
  - `GET /standby-leader?tag_key1=value1&tag_key2=value2`

- `GET /read-only`: Wie der obige Endpunkt, schließt aber auch den Primärserver ein.

- `GET /synchronous` oder `GET /sync`: Liefert den HTTP-Statuscode **200** nur dann, wenn der Patroni-Knoten als synchroner Standby läuft.

- `GET /read-only-sync`: Wie der obige Endpunkt, schließt aber auch den Primärserver ein.

- `GET /quorum`: Liefert den HTTP-Statuscode **200** nur dann, wenn dieser Patroni-Knoten auf dem Primärserver in `synchronous_standby_names` als Quorum-Knoten aufgeführt ist.

- `GET /read-only-quorum`: Wie der obige Endpunkt, schließt aber auch den Primärserver ein.

- `GET /asynchronous` oder `GET /async`: Liefert den HTTP-Statuscode **200** nur dann, wenn der Patroni-Knoten als asynchroner Standby läuft.

- `GET /asynchronous?lag=<max-lag>` oder `GET /async?lag=<max-lag>`: Endpunkt zur Prüfung eines asynchronen Standbys. Prüft zusätzlich zu den Prüfungen von `asynchronous` oder `async` den Replikationsrückstand und liefert den Statuscode **200** nur dann, wenn er unter dem angegebenen Wert liegt. Aus Leistungsgründen wird der Schlüssel cluster.last_leader_operation aus dem DCS für die WAL-Position des Leaders und zur Berechnung des Rückstands des Replikats verwendet. max-lag kann in Bytes (als Ganzzahl) oder in lesbarer Form angegeben werden, z. B. 16kB, 64MB, 1GB.

  - `GET /async?lag=1048576`
  - `GET /async?lag=1024kB`
  - `GET /async?lag=10MB`
  - `GET /async?lag=1GB`

- `GET /health`: Liefert den HTTP-Statuscode **200** nur dann, wenn PostgreSQL läuft.

- `GET /liveness`: Liefert den HTTP-Statuscode **200**, wenn die Heartbeat-Schleife von Patroni ordnungsgemäß läuft, und **503**, wenn der letzte Durchlauf auf dem Primärserver mehr als `ttl` Sekunden oder auf dem Replikat mehr als `2*ttl` Sekunden zurückliegt. Kann für `livenessProbe` verwendet werden.

- `GET /readiness?lag=<max-lag>&mode=apply|write`: Liefert den HTTP-Statuscode **200**, wenn der Patroni-Knoten als Leader läuft oder wenn PostgreSQL läuft, repliziert und nicht zu weit hinter dem Leader zurückliegt. Der Parameter lag legt den zulässigen Rückstand eines Standbys fest; sein Standardwert ist `maximum_lag_on_failover`. Der Rückstand kann in Bytes oder in lesbarer Form angegeben werden, beispielsweise 16kB, 64MB oder 1GB. Der Parameter mode legt fest, ob das WAL wiedergegeben (apply) oder lediglich empfangen (write) werden muss. Der Standardwert ist apply.

  Bei Verwendung als Kubernetes-`readinessProbe` stellt der Endpunkt sicher, dass frisch gestartete Pods erst dann bereit sind, wenn sie zum Leader aufgeholt haben. Zusammen mit einem PodDisruptionBudget verhindert dies, dass der Leader bei einem schrittweisen Neustart der Knoten zu früh beendet wird. Außerdem wird sichergestellt, dass Replikate, die mit der Replikation nicht Schritt halten können, keinen schreibgeschützten Datenverkehr bedienen. Der Endpunkt kann für `readinessProbe` verwendet werden, wenn Kubernetes-Endpunkte nicht für die Leader-Wahl genutzt werden können (OpenShift).

Der Endpunkt `liveness` benötigt nur sehr wenige Ressourcen und führt kein SQL aus. Die Prüfungen sollten so konfiguriert werden, dass sie etwa zu dem Zeitpunkt fehlschlagen, zu dem der Leader-Schlüssel abläuft. Beim Standardwert `30s` für `ttl` könnten die Prüfungen beispielsweise wie folgt aussehen:

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

## Endpunkt zur Überwachung {#monitoring-endpoint}

Patroni verwendet `GET /patroni` bei der Leader-Wahl. Der Endpunkt kann auch vom Überwachungssystem genutzt werden. Das von diesem Endpunkt erzeugte JSON-Dokument hat dieselbe Struktur wie die JSON-Dokumente der Endpunkte für Health Checks.

**Beispiel:** Ein funktionsfähiger Cluster

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

**Beispiel:** Ein Cluster ohne Leader-Lock

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

**Beispiel:** Ein Cluster ohne Leader-Lock mit aktiviertem [DCS-Failsafe-Modus](/de/patroni/dcs_failsafe_mode#dcs_failsafe_mode)

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

**Beispiel:** Ein Cluster mit aktiviertem [Pausenmodus](/de/patroni/pause#pause)

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

Die Patroni-Metriken lassen sich über den Endpunkt `GET /metrics` im Prometheus-Format abrufen.

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

### PostgreSQL-Zustandswerte {#postgresql-state-values}

Die Metrik `patroni_postgres_state` bildet den aktuellen Zustand der PostgreSQL-Instanz als Zahl ab. Das ist für Überwachungs- und Alarmierungssysteme nützlich, die Zustandsänderungen im Zeitverlauf verfolgen müssen. Die Zahlenwerte werden mit der statischen Methode `PostgresqlState.get_metrics_description()` erzeugt.

| Wert | Zustandsname             | Beschreibung                         |
|-------|-------------------------|--------------------------------------|
| 0     | initdb                  | Neuer Cluster wird initialisiert     |
| 1     | initdb_failed           | Initialisierung des neuen Clusters fehlgeschlagen |
| 2     | custom_bootstrap        | Benutzerdefiniertes Bootstrap-Skript wird ausgeführt |
| 3     | custom_bootstrap_failed | Benutzerdefiniertes Bootstrap-Skript fehlgeschlagen |
| 4     | creating_replica        | Replikat wird vom Primärserver erstellt |
| 5     | running                 | PostgreSQL läuft ordnungsgemäß        |
| 6     | starting                | PostgreSQL wird gestartet            |
| 7     | bootstrap_starting      | Start nach benutzerdefiniertem Bootstrap |
| 8     | start_failed            | Start von PostgreSQL fehlgeschlagen  |
| 9     | restarting              | PostgreSQL wird neu gestartet        |
| 10    | restart_failed          | Neustart von PostgreSQL fehlgeschlagen |
| 11    | stopping                | PostgreSQL wird angehalten           |
| 12    | stopped                 | PostgreSQL ist angehalten            |
| 13    | stop_failed             | Anhalten von PostgreSQL fehlgeschlagen |
| 14    | crashed                 | PostgreSQL ist abgestürzt            |

PostgreSQL-Zustandswerte

> [!NOTE]
> Diese Zahlenwerte sind fest und werden niemals geändert, um die Abwärtskompatibilität mit bestehenden Überwachungssystemen zu wahren. Falls künftig neue Zustände hinzukommen, erhalten sie neue Zahlenwerte, ohne die bestehenden zu ändern.

--------

## Endpunkte für den Cluster-Status {#cluster-status-endpoints}

- Der Endpunkt `GET /cluster` erzeugt ein JSON-Dokument, das die aktuelle Topologie und den Zustand des Clusters beschreibt:

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

- Der Endpunkt `GET /history` bietet einen Überblick über die Switchover- und Failover-Historie des Clusters. Das Format ähnelt stark dem Inhalt der History-Dateien im Verzeichnis `pg_wal`. Der einzige Unterschied ist das Zeitstempelfeld, das angibt, wann die neue Timeline erstellt wurde.

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

## Endpunkt für die Konfiguration {#config-endpoint}

`GET /config`: Aktuelle Version der dynamischen Konfiguration abrufen:

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

`PATCH /config`: Bestehende Konfiguration ändern.

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

Der obige REST-API-Aufruf ändert die bestehende Konfiguration und gibt die neue Konfiguration zurück.

Nun prüfen, ob der Knoten diese Konfiguration verarbeitet hat. Zunächst sollte er alle 5 Sekunden Protokollzeilen ausgeben (loop_wait=5). Die Änderung von „max_connections“ erfordert einen Neustart, daher sollte das Flag „pending_restart“ angezeigt werden:

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

Parameter entfernen:

Um eine Einstellung zu entfernen (zurückzusetzen), genügt es, sie per Patch auf `null` zu setzen:

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

Der obige Aufruf entfernt `postgresql.parameters.max_connections` aus der dynamischen Konfiguration.

`PUT /config`: Eine bestehende dynamische Konfiguration kann auch bedingungslos vollständig überschrieben werden:

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

## Endpunkte für Switchover und Failover {#switchover-and-failover-endpoints}

<a id="switchover_api"></a>

### Switchover {#switchover}

Der Endpunkt `/switchover` funktioniert nur, wenn der Cluster funktionsfähig ist (ein Leader vorhanden ist). Er ermöglicht auch, einen Switchover zu einem bestimmten Zeitpunkt zu planen.

Beim Aufruf des Endpunkts `/switchover` kann ein Kandidat angegeben werden; anders als beim Endpunkt `/failover` ist dies jedoch nicht erforderlich. Wird kein Kandidat angegeben, nehmen alle geeigneten Knoten des Clusters an der Leader-Wahl teil, nachdem der Leader seine Rolle abgegeben hat.

Im JSON-Inhalt der `POST`-Anfrage muss das Feld `leader` angegeben werden. Die Felder `candidate` und `scheduled_at` sind optional und können verwendet werden, um einen Switchover zu einem bestimmten Zeitpunkt zu planen.

Je nach Situation können Anfragen unterschiedliche HTTP-Statuscodes und Antwortinhalte liefern. Der Statuscode **200** wird zurückgegeben, wenn der Switchover oder das Failover erfolgreich abgeschlossen wurde. Wurde der Switchover erfolgreich geplant, liefert Patroni den HTTP-Statuscode **202**. Ist ein Fehler aufgetreten, wird ein Fehlerstatuscode (**400**, **412** oder **503**) mit Einzelheiten im Antwortinhalt zurückgegeben.

Mit `DELETE /switchover` kann der aktuell geplante Switchover gelöscht werden.

**Beispiel:** Switchover zu einem beliebigen funktionsfähigen Standby durchführen

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1"}'
Successfully switched over to "postgresql2"
```

**Beispiel:** Switchover zu einem bestimmten Knoten durchführen

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql1","candidate":"postgresql2"}'
Successfully switched over to "postgresql2"
```

**Beispiel:** Switchover vom Leader zu einem beliebigen anderen funktionsfähigen Standby im Cluster zu einem bestimmten Zeitpunkt planen.

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
Switchover scheduled
```

### Failover {#failover}

Der Endpunkt `/failover` kann für ein manuelles Failover verwendet werden, wenn keine funktionsfähigen Knoten vorhanden sind (z. B. zu einem asynchronen Standby, wenn alle synchronen Standbys für eine Hochstufung nicht funktionsfähig genug sind). Ein fehlender Leader ist jedoch keine Voraussetzung: Ein Failover kann auch in einem funktionsfähigen Cluster ausgeführt werden.

Im JSON-Inhalt der `POST`-Anfrage muss das Feld `candidate` angegeben werden. Wird das Feld `leader` angegeben, wird stattdessen ein Switchover ausgelöst.

**Beispiel:**

``` bash
$ curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
Successfully failed over to "postgresql1"
```

> [!WARNING]
> Bei Verwendung dieses Endpunkts ist [äußerste Vorsicht geboten](/de/patroni/rest_api#failover_healthcheck), da er unter bestimmten Umständen zu Datenverlust führen kann. In den meisten Fällen erfüllt [der Switchover-Endpunkt](/de/patroni/rest_api#switchover_api) die Anforderungen des Administrators.

Die Endpunkte `POST /switchover` und `POST /failover` werden von [patronictl_switchover](/de/patroni/patronictl#patronictl_switchover) bzw. [patronictl_failover](/de/patroni/patronictl#patronictl_failover) verwendet.

`DELETE /switchover` wird von [patronictl flush cluster-name switchover](/de/patroni/patronictl#patronictl_flush_parameters) verwendet.

|                              | Failover | Switchover                         |
|------------------------------|----------|------------------------------------|
| Angabe eines Leaders erforderlich | nein | ja |
| Angabe eines Kandidaten erforderlich | ja | nein |
| Im Pausenmodus ausführbar | ja | ja (nur zu einem bestimmten Kandidaten) |
| Planbar | nein | ja (sofern nicht im Pausenmodus) |

Vergleich von Failover und Switchover

<a id="failover_healthcheck"></a>

### Funktionsfähiger Standby {#healthy-standby}

Ein Cluster-Mitglied sollte einige Prüfungen bestehen, um bei einem Switchover an der Leader-Wahl teilnehmen oder als Failover-/Switchover-Kandidat zum Leader werden zu können:

- über die Patroni API erreichbar sein;
- das Tag `nofailover` darf nicht auf `true` gesetzt sein;
- über einen voll funktionsfähigen Watchdog verfügen (falls die Konfiguration dies erfordert);
- bei einem Switchover in einem funktionsfähigen Cluster oder einem automatischen Failover den maximalen Replikationsrückstand nicht überschreiten ([Konfigurationsparameter](/de/patroni/config/dynamic#dynamic) `maximum_lag_on_failover`);
- bei einem Switchover in einem funktionsfähigen Cluster oder einem automatischen Failover keine kleinere Timeline-Nummer als die Cluster-Timeline haben, wenn der [Konfigurationsparameter](/de/patroni/config/dynamic#dynamic) `check_timeline` auf `true` gesetzt ist;
- im [synchronen Modus](/de/patroni/replication_modes#synchronous_mode):
  - Bei einem Switchover (mit oder ohne Kandidaten): unter den Mitgliedern des Schlüssels `/sync` aufgeführt sein;
  - Bei einem Failover sowohl in funktionsfähigen als auch in nicht funktionsfähigen Clustern entfällt diese Prüfung.

> [!WARNING]
> Bei einem manuellen Failover in einem Cluster ohne Leader darf ein Kandidat auch dann hochgestuft werden, wenn:
>
> - er bei aktiviertem synchronem Modus nicht unter den Mitgliedern des Schlüssels `/sync` aufgeführt ist;
> - sein Rückstand den maximal zulässigen Replikationsrückstand überschreitet;
> - seine Timeline-Nummer kleiner als die zuletzt bekannte Cluster-Timeline ist.

<a id="restart_endpoint"></a>

--------

## Endpunkt für Neustarts {#restart-endpoint}

- `POST /restart`: Mit dem Aufruf `POST /restart` kann Postgres auf dem jeweiligen Knoten neu gestartet werden. Im JSON-Inhalt der `POST`-Anfrage können optional Bedingungen für den Neustart angegeben werden:
  - **restart_pending**: Boolescher Wert. Bei `true` startet Patroni PostgreSQL nur dann neu, wenn ein Neustart aussteht, um Änderungen an der PostgreSQL-Konfiguration anzuwenden.
  - **role**: Neustart nur durchführen, wenn die aktuelle Rolle des Knotens mit der Rolle aus der POST-Anfrage übereinstimmt.
  - **postgres_version**: Neustart nur durchführen, wenn die aktuelle Postgres-Version kleiner als die in der POST-Anfrage angegebene ist.
  - **timeout**: Wartezeit, bis PostgreSQL Verbindungen annimmt. Überschreibt `primary_start_timeout`.
  - **schedule**: Zeitstempel mit Zeitzone; plant den Neustart für einen zukünftigen Zeitpunkt.
- `DELETE /restart`: Geplanten Neustart löschen

Die Endpunkte `POST /restart` und `DELETE /restart` werden von [patronictl_restart](/de/patroni/patronictl#patronictl_restart) bzw. [patronictl flush cluster-name restart](/de/patroni/patronictl#patronictl_flush_parameters) verwendet.

<a id="reload_endpoint"></a>

--------

## Endpunkt zum Neuladen {#reload-endpoint}

Der Aufruf `POST /reload` weist Patroni an, die Konfigurationsdatei erneut einzulesen und anzuwenden. Dies entspricht dem Senden des Signals `SIGHUP` an den Patroni-Prozess. Wenn Postgres-Parameter geändert wurden, die einen Neustart erfordern (z. B. **shared_buffers**), muss Postgres weiterhin ausdrücklich neu gestartet werden, entweder über den Endpunkt `POST /restart` oder mithilfe von [patronictl_restart](/de/patroni/patronictl#patronictl_restart).

Der Endpunkt zum Neuladen wird von [patronictl_reload](/de/patroni/patronictl#patronictl_reload) verwendet.

--------

## Endpunkt zur Neuinitialisierung {#reinitialize-endpoint}

`POST /reinitialize`: Initialisiert das PostgreSQL-Datenverzeichnis auf dem angegebenen Knoten neu. Der Aufruf darf nur auf Replikaten ausgeführt werden. Er entfernt das Datenverzeichnis und startet `pg_basebackup` oder eine alternative [Methode zur Replikaterstellung](/de/patroni/replica_bootstrap#custom_replica_creation).

Der Aufruf kann fehlschlagen, wenn Patroni in einer Schleife versucht, ein ausgefallenes Postgres wiederherzustellen (neu zu starten). Um dieses Problem zu umgehen, kann im Anfrageinhalt `{"force":true}` angegeben werden.

Im Anfrageinhalt kann {"from-leader":true} angegeben werden, um das Basis-Backup direkt vom Leader-Knoten zu beziehen. Dies ist nützlich, wenn die Neuinitialisierung bei einem Ausfall aller Replikatknoten ausgeführt wird.

Der Endpunkt zur Neuinitialisierung wird von [patronictl_reinit](/de/patroni/patronictl#patronictl_reinit) verwendet.
