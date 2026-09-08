---
title: "API REST Patroni"
weight: 40
icon: fa-solid fa-book
description: "Référence des points d'extrémité de l'API REST de Patroni et de leurs comportements opérationnels."
module: [PATRONI]
categories: [Référence]
aliases: [/patroni/rest_api/]
upstream_link: "https://patroni.readthedocs.io/en/latest/rest_api.html"
---

<a id="rest_api"></a>
Patroni dispose d'une API REST riche, utilisée par Patroni lui-même lors de la course au leader, par l'outil [patronictl](/fr/docs/patroni/patronictl#patronictl) afin d'effectuer des basculements, des basculements planifiés, des réinitialisations, des redémarrages ou des rechargements, par HAProxy ou tout autre équilibreur de charge pour effectuer des vérifications de santé HTTP, et bien entendu également utilisée pour la surveillance. Ci-dessous figure la liste des points d'accès de l'API REST de Patroni.

--------

## Points de terminaison de vérification de santé {#health-check-endpoints}

Pour toutes les requêtes de vérification de santé `GET`, Patroni renvoie un document JSON indiquant l'état du nœud, accompagné du code d'état HTTP. Si vous ne souhaitez pas ou n'avez pas besoin du document JSON, vous pouvez envisager d'utiliser la méthode `HEAD` ou `OPTIONS` au lieu de `GET`.

- Les requêtes suivantes vers l'API REST de Patroni renvoient le code d'état HTTP **200** uniquement lorsque le nœud Patroni fonctionne en tant que primaire avec verrou de leader :

  - `GET /`
  - `GET /primary`
  - `GET /read-write`

- `GET /standby-leader` : renvoie le code d’état HTTP **200** uniquement lorsque le nœud Patroni est en cours d’exécution en tant que leader dans un [cluster de secours](/fr/docs/patroni/standby_cluster#standby_cluster).

- `GET /leader` : renvoie le code d’état HTTP **200** lorsque le nœud Patroni détient le verrou leader. La différence principale avec les deux précédents points d’accès est qu’elle ne tient pas compte de l’état d’exécution de PostgreSQL en tant que `primary` ou `standby_leader`.

- `GET /replica` : point de terminaison de vérification de santé de la réplique. Il renvoie le code d’état HTTP **200** uniquement lorsque le nœud Patroni est dans l’état `running`, que son rôle est `replica` et que l’étiquette `noloadbalance` n’est pas définie.

- `GET /replica?replication_state=<required state>` : point de contrôle de réplique. En plus des vérifications effectuées par `replica`, il vérifie également que l'état de réplication correspond à celui requis. Principalement utile avec `replication_state=streaming`, afin d'exclure les répliques encore en cours de synchronisation pendant une récupération archivée.

- `GET /replica?lag=<max-lag>` : point de contrôle de réplique. En plus des vérifications effectuées par `replica`, il vérifie également le délai de réplication et renvoie le code d’état **200** uniquement lorsque ce délai est inférieur à la valeur spécifiée. La clé cluster.last_leader_operation provenant du DCS est utilisée pour la position WAL du leader et le calcul du délai sur la réplique, pour des raisons de performance. max-lag peut être spécifié en octets (entier) ou sous forme lisible par l’humain, par exemple 16kB, 64MB, 1GB.

  - `GET /replica?lag=1048576`
  - `GET /replica?lag=1024kB`
  - `GET /replica?lag=10MB`
  - `GET /replica?lag=1GB`

- `GET /replica?tag_key1=value1&tag_key2=value2` : point de contrôle de réplique. En outre, il vérifie également les balises définies par l'utilisateur `key1` et `key2` ainsi que leurs valeurs respectives dans la section **tags** de la configuration YAML. Si une balise n'est pas définie pour une instance, ou si la valeur dans la configuration YAML ne correspond pas à la valeur demandée, le service renvoie le code d'état HTTP 503.

Dans les requêtes suivantes, comme nous vérifions l'état de leader ou de standby-leader, Patroni ne prend pas en compte les étiquettes définies par l'utilisateur, qui seront ignorées.

  - `GET /?tag_key1=value1&tag_key2=value2`
  - `GET /leader?tag_key1=value1&tag_key2=value2`
  - `GET /primary?tag_key1=value1&tag_key2=value2`
  - `GET /read-write?tag_key1=value1&tag_key2=value2`
  - `GET /standby_leader?tag_key1=value1&tag_key2=value2`
  - `GET /standby-leader?tag_key1=value1&tag_key2=value2`

- `GET /read-only` : comme le point d'accès précédent, mais inclut également le primaire.

- `GET /synchronous` ou `GET /sync` : renvoie le code d’état HTTP **200** uniquement lorsque le nœud Patroni fonctionne en réplica synchrone.

- `GET /read-only-sync` : comme le point d'accès précédent, mais inclut également le primaire.

- `GET /quorum` : renvoie le code d'état HTTP **200** uniquement lorsque ce nœud Patroni est répertorié comme nœud de quorum dans `synchronous_standby_names` sur le primaire.

- `GET /read-only-quorum` : comme le point d'accès précédent, mais inclut également le primaire.

- `GET /asynchronous` ou `GET /async` : renvoie le code d’état HTTP **200** uniquement lorsque le nœud Patroni fonctionne en réplica asynchrone.

- `GET /asynchronous?lag=<max-lag>` ou `GET /async?lag=<max-lag>` : point de contrôle de basculement asynchrone. En plus des vérifications provenant de `asynchronous` ou `async`, il vérifie également le délai de réplication et renvoie le code d’état **200** uniquement lorsque ce délai est inférieur à la valeur spécifiée. La clé cluster.last_leader_operation provenant du DCS est utilisée pour la position WAL du leader et le calcul du délai sur la réplique, pour des raisons de performance. max-lag peut être spécifié en octets (entier) ou sous forme lisible par l’humain, par exemple 16kB, 64MB, 1GB.

  - `GET /async?lag=1048576`
  - `GET /async?lag=1024kB`
  - `GET /async?lag=10MB`
  - `GET /async?lag=1GB`

- `GET /health` : renvoie le code d'état HTTP **200** uniquement lorsque PostgreSQL est en cours d'exécution.

- `GET /liveness` : renvoie le code d'état HTTP **200** si la boucle de battement de cœur Patroni fonctionne correctement, et **503** si la dernière exécution remonte à plus de `ttl` secondes sur le serveur primaire ou à plus de `2*ttl` secondes sur la réplique. Peut être utilisé pour `livenessProbe`.

- `GET /readiness?lag=<max-lag>&mode=apply|write` : renvoie le code d’état HTTP **200** lorsque le nœud Patroni fonctionne en tant que leader ou lorsque PostgreSQL est actif, en réplication et pas trop en retard par rapport au leader. Le paramètre lag définit la marge maximale de retard autorisée pour une instance de secours, avec une valeur par défaut de `maximum_lag_on_failover`. Le retard peut être spécifié en octets ou en valeurs lisibles par l’humain, par exemple 16kB, 64MB ou 1GB. Le paramètre mode indique si le WAL doit être appliqué (rejoué) ou simplement reçu (écrit). La valeur par défaut est apply.

Lorsqu’il est utilisé comme Kubernetes `readinessProbe`, il garantit que les nouveaux pods démarrés ne deviennent prêts qu’après avoir rattrapé le leader. Cela, combiné à un PodDisruptionBudget, protège contre une terminaison prématurée du leader lors d’un redémarrage progressif des nœuds. Il garantit également que les répliques incapables de suivre la réplication ne traitent pas le trafic en lecture seule. Ce point d’accès peut être utilisé pour `readinessProbe` lorsque l’utilisation des endpoints Kubernetes pour les élections de leader n’est pas possible (OpenShift).

Le point d'entrée `liveness` est très léger et n'exécute aucune requête SQL. Les sondes doivent être configurées de manière à commencer à échouer environ au moment où la clé leader expire. Avec la valeur par défaut de `ttl`, qui est `30s`, les sondes devraient ressembler à l'exemple suivant :

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

## Point de terminaison de surveillance {#monitoring-endpoint}

Le `GET /patroni` est utilisé par Patroni lors de la course au leader. Il peut également être utilisé par votre système de surveillance. Le document JSON produit par cette extension a la même structure que le JSON produit par les points d'entrée de vérification de santé.

**Exemple** : un cluster sain

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

**Exemple** : un cluster déverrouillé

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

**Exemple :** Un cluster déverrouillé avec le mode de sécurité du [DCS](/fr/docs/patroni/dcs_failsafe_mode#dcs_failsafe_mode) activé

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

**Exemple :** Un cluster avec le mode [pause](/fr/docs/patroni/pause#pause) activé

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

Récupérez les métriques Patroni au format Prometheus via l'endpoint `GET /metrics`.

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

### Valeurs d'état PostgreSQL {#postgresql-state-values}

La métrique `patroni_postgres_state` fournit une représentation numérique de l'état actuel de l'instance PostgreSQL. Cela est utile pour les systèmes de surveillance et d'alerte qui doivent suivre les changements d'état au fil du temps. Les valeurs numériques sont générées à l'aide de la méthode statique `PostgresqlState.get_metrics_description()`.

| Valeur | Nom d'état               | Description                          |
|-------|--------------------------|--------------------------------------|
| 0     | initdb                   | Initialisation du nouveau cluster    |
| 1     | initdb_failed            | Échec de l'initialisation du nouveau cluster |
| 2     | custom_bootstrap         | Exécution du script d'amorçage personnalisé |
| 3     | custom_bootstrap_failed  | Échec du script d'amorçage personnalisé |
| 4     | creating_replica         | Création d'une réplique à partir du primaire |
| 5     | running                  | PostgreSQL fonctionne normalement    |
| 6     | starting                 | PostgreSQL démarre                     |
| 7     | bootstrap_starting       | Démarrage après l'amorçage personnalisé |
| 8     | start_failed             | Échec du démarrage de PostgreSQL     |
| 9     | restarting               | PostgreSQL redémarre                   |
| 10    | restart_failed           | Échec du redémarrage de PostgreSQL   |
| 11    | stopping                 | PostgreSQL s'arrête                    |
| 12    | stopped                  | PostgreSQL est arrêté                  |
| 13    | stop_failed              | Échec de l'arrêt de PostgreSQL       |
| 14    | crashed                  | PostgreSQL a planté                    |

Valeurs d'état de PostgreSQL

> [!NOTE]
> Ces valeurs numériques sont fixes et ne changeront jamais afin de préserver la compatibilité ascendante avec les systèmes de surveillance existants. Si de nouveaux états sont ajoutés à l’avenir, ils seront affectés à de nouvelles valeurs numériques sans modifier les valeurs existantes.

--------

## Points de terminaison d'état du cluster {#cluster-status-endpoints}

- L’endpoint `GET /cluster` génère un document JSON décrivant la topologie et l’état actuels du cluster :

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

-  Le point d'accès `GET /history` fournit une vue sur l'historique des basculements ou des basculements planifiés du cluster. Le format est très similaire au contenu des fichiers d'historique dans le répertoire `pg_wal`. La seule différence réside dans le champ horodatage, qui indique quand la nouvelle ligne temporelle a été créée.

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

## Point d'entrée de configuration {#config-endpoint}

`GET /config` : Obtenir la version actuelle de la configuration dynamique :

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

`PATCH /config` : Modifiez la configuration existante.

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

L'appel d'API REST ci-dessus met à jour la configuration existante et renvoie la configuration mise à jour.

Vérifions que le nœud a bien appliqué cette configuration. Tout d'abord, il doit commencer à imprimer des lignes de journalisation toutes les 5 secondes (loop_wait=5). Le changement de "max_connections" nécessite un redémarrage, donc le drapeau "pending_restart" doit être exposé :

``` bash
$ curl -s http://localhost:8008/patroni | jq .
{
  "database_system_identifier": "6287881213849985952",
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

Suppression des paramètres :

Si vous souhaitez supprimer (réinitialiser) un paramètre, appliquez une mise à jour avec `null` :

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

L'appel ci-dessus retire `postgresql.parameters.max_connections` de la configuration dynamique.

`PUT /config` : Il est également possible d'effectuer la réécriture complète d'une configuration dynamique existante sans condition :

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

## Points de terminaison de basculement planifié et de basculement {#switchover-and-failover-endpoints}

<a id="switchover_api"></a>

### basculement planifié {#switchover}

Le point de terminaison `/switchover` ne fonctionne que lorsque le cluster est sain (un leader est présent). Il permet également de planifier un basculement planifié à une heure donnée.

Lors de l'appel de l'endpoint `/switchover`, un candidat peut être spécifié mais n'est pas obligatoire, contrairement à l'endpoint `/failover`. Si aucun candidat n'est fourni, tous les nœuds du cluster éligibles participeront à la course au leader après le départ du leader.

Dans le corps JSON de la requête `POST`, vous devez spécifier le champ `leader`. Les champs `candidate` et `scheduled_at` sont facultatifs et peuvent être utilisés pour planifier un basculement à une heure précise.

Selon la situation, les requêtes peuvent renvoyer des codes d’état HTTP et des corps différents. Le code d’état **200** est retourné lorsque le basculement planifié ou le basculement s’est terminé avec succès. Si le basculement planifié a été correctement planifié, Patroni renvoie le code d’état HTTP **202**. En cas d’erreur, un code d’état d’erreur (l’un des codes **400**, **412** ou **503**) est retourné, accompagné de détails dans le corps de la réponse.

`DELETE /switchover` peut être utilisé pour supprimer le basculement planifié actuellement prévu.

**Exemple :** effectuer un basculement planifié vers une station de secours saine

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d '{"leader":"postgresql1"}'
Successfully switched over to "postgresql2"
```

**Exemple :** effectuer un basculement planifié vers un nœud spécifique

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql1","candidate":"postgresql2"}'
Successfully switched over to "postgresql2"
```

**Exemple :** planifier un basculement planifié du leader vers un autre nœud de secours sain du cluster à une heure précise.

``` bash
$ curl -s http://localhost:8008/switchover -XPOST -d \
    '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}'
Switchover scheduled
```

### basculement {#failover}

Le point de terminaison `/failover` peut être utilisé pour effectuer un basculement manuel lorsque aucun nœud sain n'est disponible (par exemple, vers un réplica asynchrone si tous les réplicas synchrones ne sont pas suffisamment sains pour être promus). Toutefois, il n'existe aucune obligation pour un cluster de ne pas avoir de leader : le basculement peut également être exécuté sur un cluster sain.

Dans le corps JSON de la requête `POST`, vous devez spécifier le champ `candidate`. Si le champ `leader` est spécifié, un basculement planifié est déclenché à la place.

**Exemple :**

``` bash
$ curl -s http://localhost:8008/failover -XPOST -d '{"candidate":"postgresql1"}'
Successfully failed over to "postgresql1"
```

> [!AVERTISSEMENT]
> [Faites preuve de prudence](/fr/docs/patroni/rest_api#failover_healthcheck) lors de l'utilisation de cette API, car cela peut entraîner une perte de données dans certaines situations. Dans la plupart des cas, [l'endpoint de basculement planifié](/fr/docs/patroni/rest_api#switchover_api) répond aux besoins de l'administrateur.

Les points de terminaison `POST /switchover` et `POST /failover` sont utilisés par [patronictl_switchover](/fr/docs/patroni/patronictl#patronictl_switchover) et [patronictl_failover](/fr/docs/patroni/patronictl#patronictl_failover) respectivement.

`DELETE /switchover` est utilisé par [patronictl flush cluster-name basculement planifié](/fr/docs/patroni/patronictl#patronictl_flush_parameters).

|                              | Basculer | Basculer planifié                  |
|------------------------------|----------|------------------------------------|
| Nécessite un leader spécifié | non      | oui                                |
| Nécessite un candidat spécifié | oui    | non                                |
| Peut être exécuté en pause   | oui      | oui (uniquement vers un candidat spécifique) |
| Peut être planifié           | non      | oui (si non en pause)              |

Comparaison entre basculement et basculement planifié

<a id="failover_healthcheck"></a>

### Standby sain {#healthy-standby}

Plusieurs vérifications doivent être effectuées par un membre d’un cluster afin de pouvoir participer à la course au rôle de leader lors d’un basculement planifié ou de devenir leader en tant que candidat au basculement ou au basculement planifié :

- -  être accessible via l'API Patroni ;
- -  ne pas avoir l'étiquette `nofailover` définie sur `true` ;
- -  avoir le watchdog entièrement fonctionnel (si requis par la configuration) ;
- -  en cas de basculement planifié dans un cluster sain ou de basculement automatique, ne pas dépasser le décalage maximal de réplication (`maximum_lag_on_failover` [paramètre de configuration](/fr/docs/patroni/config/dynamic#dynamic)) ;
- -  en cas de basculement planifié dans un cluster sain ou de basculement automatique, ne pas avoir un numéro de timeline inférieur à celui du cluster si `check_timeline` [paramètre de configuration](/fr/docs/patroni/config/dynamic#dynamic) est défini sur `true` ;
- -  en mode [synchrone](/fr/docs/patroni/replication_modes#synchronous_mode) :
  -   -  En cas de basculement planifié (avec ou sans candidat) : être inclus dans la liste des membres `/sync` ;
  -   -  En cas de basculement dans des clusters sains ou défaillants, cette vérification est omise.

> [!AVERTISSEMENT]
> En cas de basculement manuel dans un cluster sans leader, un candidat peut être promu même si :   - il n'est pas membre du `/sync` lorsque le mode synchrone est activé ;   - son retard dépasse le retard maximal de réplication autorisé ;   - son numéro de timeline est inférieur au dernier numéro de timeline connu du cluster.

<a id="restart_endpoint"></a>

--------

## Point d'arrêt de redémarrage {#restart-endpoint}

- `POST /restart` : Vous pouvez redémarrer Postgres sur le nœud spécifique en effectuant l'appel `POST /restart`. Dans le corps JSON de la requête `POST`, il est possible de spécifier de manière optionnelle certaines conditions de redémarrage :
  - **restart_pending** : booléen, si défini à `true`, Patroni redémarrera PostgreSQL uniquement lorsque le redémarrage est en attente afin d'appliquer certaines modifications de configuration de PostgreSQL.
  - **role** : effectuer le redémarrage uniquement si le rôle actuel du nœud correspond au rôle fourni dans la requête POST.
  - **postgres_version** : effectuer le redémarrage uniquement si la version actuelle de PostgreSQL est inférieure à celle spécifiée dans la requête POST.
  - **timeout** : durée d'attente avant que PostgreSQL ne commence à accepter les connexions. Remplace `primary_start_timeout`.
  - **schedule** : horodatage avec fuseau horaire, planifier le redémarrage à une date future.
- `DELETE /restart` : supprimer le redémarrage planifié

Les points de terminaison `POST /restart` et `DELETE /restart` sont utilisés par [patronictl_restart](/fr/docs/patroni/patronictl#patronictl_restart) et [patronictl flush cluster-name restart](/fr/docs/patroni/patronictl#patronictl_flush_parameters) respectivement.

<a id="reload_endpoint"></a>

--------

## Point de terminaison de rechargement {#reload-endpoint}

L'appel `POST /reload` ordonne à Patroni de relire et d'appliquer le fichier de configuration. Cela équivaut à envoyer le signal `SIGHUP` au processus Patroni. Si vous avez modifié certains paramètres de Postgres nécessitant un redémarrage (comme **shared_buffers**), vous devez toujours effectuer explicitement le redémarrage de Postgres en appelant l'endpoint `POST /restart` ou à l'aide de [patronictl restart](/fr/docs/patroni/patronictl#patronictl_restart).

Le point de terminaison reload est utilisé par [patronictl_reload](/fr/docs/patroni/patronictl#patronictl_reload).

--------

## Réinitialiser le point de terminaison {#reinitialize-endpoint}

`POST /reinitialize` : réinitialiser le répertoire de données PostgreSQL sur le nœud spécifié. Cette opération ne peut être exécutée qu'aux répliques. Une fois appelée, elle supprime le répertoire de données et déclenche `pg_basebackup` ou une autre méthode alternative de création de réplique [replica creation method](/fr/docs/patroni/replica_bootstrap#custom_replica_creation).

L'appel peut échouer si Patroni est en boucle de récupération (redémarrage) d'une instance Postgres défaillante. Pour contourner ce problème, il est possible de spécifier `{"force":true}` dans le corps de la requête.

Vous pouvez spécifier {"from-leader":true} dans le corps de la requête pour obtenir directement un basebackup depuis le nœud leader. Cela est utile lors de l'exécution d'un reinit lorsque tous les nœuds répliques échouent.

Le point de terminaison de réinitialisation est utilisé par [patronictl_reinit](/fr/docs/patroni/patronictl#patronictl_reinit).
