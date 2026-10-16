---
title: Degradación de etcd de v3.7 a v3.6
weight: 6600
description: Procesos, listas de verificación y notas sobre la degradación de etcd de v3.7 a v3.6
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
---

En el caso general, la degradación de etcd v3.7 a v3.6 puede ser una degradación gradual sin tiempo de inactividad:

- uno a uno, detén los procesos de etcd v3.7 y reemplázalos por procesos de etcd v3.6
- después de activar la degradación, las nuevas funcionalidades de v3.7 dejan de estar disponibles para el clúster

Antes de [iniciar una degradación](#downgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la degradación {#downgrade-checklists}

Diferencias destacadas entre v3.7 y v3.6:

#### Diferencias en las opciones {#difference-in-flags}

v3.7 no introduce ninguna opción nueva, por lo que un proceso v3.6 acepta todas las opciones de una configuración v3.7 y no se requiere ningún cambio de configuración al degradar.

> [!NOTE]
> La diferencia se basa en las versiones v3.7.0-rc.0 y v3.6.13. La diferencia real dependerá de tu versión de parche; compruébalo primero con `diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`.

Las opciones `--experimental-*` obsoletas que se eliminaron en v3.7 todavía existen en v3.6, pero no las vuelvas a añadir después de la degradación; usa sus equivalentes no experimentales o las entradas de `--feature-gates`, que funcionan en ambas versiones.

#### Diferencias en las métricas de Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### Listas de verificación para la degradación del servidor {#server-downgrade-checklists}

#### Requisitos de la degradación {#downgrade-requirements}

Para garantizar una degradación gradual sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster usando el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de degradar etcd, prueba siempre en un entorno de preproducción los servicios que dependen de etcd antes de desplegar la degradación en el entorno de producción.

Antes de comenzar, [descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la degradación, es posible usar esta copia de seguridad para [revertir](#rollback) y volver a la versión de etcd existente.

Antes de comenzar, descarga la última versión de etcd v3.6.

#### Versiones mixtas {#mixed-versions}

Durante la degradación, un clúster de etcd admite versiones mixtas de miembros de etcd y opera con el protocolo de la versión común más baja. El clúster se considera degradado en cuanto la degradación se activa con `etcdctl downgrade enable 3.6`. Internamente, la versión global del clúster se establece en la versión de destino de la degradación, que controla la versión notificada y las funcionalidades admitidas.

#### Reversión {#rollback}

Antes de degradar tu clúster de etcd, crea y [descarga una copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) de tu clúster de etcd. Esta instantánea se puede usar para restaurar el clúster a su estado anterior a la degradación si es necesario. Si los usuarios encuentran problemas durante la degradación, deben identificar y resolver primero la causa raíz.

Si la degradación comenzó después de ejecutar `etcdctl downgrade enable` y el clúster sigue en un estado de versiones mixtas, en el que al menos un miembro permanece en v3.7, los usuarios pueden cancelar el proceso de degradación en curso ejecutando `etcdctl downgrade cancel` y reiniciando todos los miembros degradados con los binarios v3.7 originales.

Una vez que todos los miembros se hayan degradado a v3.6, el clúster se considera totalmente degradado. Si los usuarios desean volver a la versión original después de completar una degradación total, deben seguir la [guía de actualización](/es/etcd/upgrades/upgrade_3_7/) oficial para garantizar la coherencia y evitar la corrupción de datos.

### Procedimiento de degradación {#downgrade-procedure}

Este ejemplo muestra cómo degradar un clúster de etcd v3.7 de 3 miembros que se ejecuta en una máquina local. La salida siguiente proviene de una ejecución real contra etcd v3.7.0-rc.0 y etcd v3.6.13 en un único host con tres puertos de loopback, sobre un clúster que había sido actualizado desde v3.6.13 poco antes.

#### Paso 1: comprobar los requisitos de la degradación {#step-1-check-downgrade-requirements}

¿Está el clúster en buen estado y ejecutando la versión v3.7.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.052416ms
localhost:32379 is healthy: successfully committed proposal: took = 1.11625ms
localhost:22379 is healthy: successfully committed proposal: took = 1.114291ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.7.0-rc.0","etcdcluster":"3.7.0","storage":"3.7.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### Paso 2: descargar la copia de seguridad de la instantánea desde el líder {#step-2-download-snapshot-backup-from-leader}

[Descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para disponer de una vía de reversión en caso de que surjan problemas:

```bash
etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-07-02T06:48:11.091982+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-07-02T06:48:11.092253+0300","logger":"client","caller":"v3/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-07-02T06:48:11.099884+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-07-02T06:48:11.100394+0300","logger":"client","caller":"v3/maintenance.go:302","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2026-07-02T06:48:11.103116+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"10.9815ms","etcd-version":"3.7.0"}
{"level":"info","ts":"2026-07-02T06:48:11.103296+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.7.0
COMMENT
```

#### Paso 3: validar la versión de destino de la degradación {#step-3-validate-downgrade-target-version}

Valida la versión de destino de la degradación antes de activarla:

- Solo se admite la degradación de una versión menor a la vez. Por ejemplo, degradar de v3.7 a v3.5 no está permitido.
- No pases al siguiente paso hasta que la validación sea correcta.

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### Paso 4: activar la degradación {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

Después de activar la degradación, el clúster empezará a operar con el protocolo v3.6, que es la versión de destino de la degradación. Además, etcd migrará automáticamente el esquema a la versión de destino de la degradación, lo que suele ocurrir muy rápido. Confirma que la versión de almacenamiento de todos los servidores se ha migrado a v3.6 comprobando el estado de los endpoints antes de pasar al siguiente paso.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> Una vez activada la degradación, el clúster seguirá operando con el protocolo v3.6 aunque todos los servidores sigan ejecutando el binario v3.7, a menos que la degradación se cancele con `etcdctl downgrade cancel`

#### Paso 5: detener un servidor de etcd existente {#step-5-stop-one-existing-etcd-server}

Antes de detener el servidor, comprueba si es el líder. Recomendamos degradar el líder al final. Si el servidor que se va a detener es el líder, puedes evitar algo de tiempo de inactividad transfiriendo el liderazgo a otro servidor con `move-leader` antes de detener este servidor.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

Cuando se detiene cada proceso de etcd, los demás miembros del clúster registrarán errores esperados. Esto es normal, ya que se ha roto (temporalmente) la conexión con un miembro del clúster:

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### Paso 6: reiniciar el servidor de etcd con la misma configuración {#step-6-restart-the-etcd-server-with-same-configuration}

Reinicia el servidor de etcd con la misma configuración, pero con el binario de etcd v3.6.

```diff
-etcd-3.7/bin/etcd --name s2 \
+etcd-3.6/bin/etcd --name s2 \
  --data-dir /tmp/etcd/s2 \
  --listen-client-urls http://localhost:22379 \
  --advertise-client-urls http://localhost:22379 \
  --listen-peer-urls http://localhost:22380 \
  --initial-advertise-peer-urls http://localhost:22380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

Comprueba que cada miembro, y luego el clúster entero, se encuentran en buen estado con el binario de etcd v3.6:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 |     3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 939.625µs
localhost:32379 is healthy: successfully committed proposal: took = 981.459µs
localhost:22379 is healthy: successfully committed proposal: took = 1.11075ms
COMMENT
```

> [!NOTE]
> A diferencia de v3.5, el endpoint de estado de v3.6 sí informa de los datos de la degradación, por lo que los miembros degradados siguen mostrando `DOWNGRADE ENABLED` como true y su versión de almacenamiento hasta que la degradación se completa.

#### Paso 7: repetir el *paso 5* y el *paso 6* para el resto de los miembros {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

Cuando todos los miembros están degradados, la degradación se completa automáticamente y `DOWNGRADE ENABLED` se restablece a false. Comprueba el estado de salud y el estado del clúster, y confirma que la versión menor de todos los miembros y la versión de almacenamiento son v3.6:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:32379 |  b548c2511513015 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 5.176958ms
localhost:32379 is healthy: successfully committed proposal: took = 5.177875ms
localhost:2379 is healthy: successfully committed proposal: took = 5.191625ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

En el registro del líder, deberías poder ver un mensaje similar al siguiente:

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
