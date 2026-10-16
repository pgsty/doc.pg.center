---
title: Degradación de etcd de 3.5 a 3.4
weight: 6700
description: Procesos, listas de verificación y notas sobre la degradación de etcd de 3.5 a 3.4
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_5.md"
---

En el caso general, la degradación de etcd 3.5 a 3.4 puede ser una degradación gradual sin tiempo de inactividad:

- uno a uno, detén los procesos de etcd 3.5 y reemplázalos por procesos de etcd 3.4
- después de iniciar cualquier proceso 3.4, las nuevas funcionalidades de 3.5 dejan de estar disponibles para el clúster

Antes de [iniciar una degradación](#downgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la degradación {#downgrade-checklists}

> [!WARNING]
> Si tu clúster tiene la autenticación activada, la degradación gradual desde 3.5 no se admite, porque 3.5 [cambia el formato de las entradas WAL relacionadas con la autenticación](https://github.com/etcd-io/etcd/pull/11943). Puedes seguir las [instrucciones de autenticación](/es/etcd/op-guide/authentication/rbac/) para desactivar la autenticación y eliminar primero todos los usuarios.

Principales cambios con ruptura de compatibilidad de 3.5 a 3.4:

#### Diferencias en las opciones {#difference-in-flags}

Si usas alguna de las opciones siguientes en tus configuraciones 3.5, asegúrate de eliminarlas, renombrarlas o cambiar el valor predeterminado al degradar a 3.4.

> [!NOTE]
> La diferencia se basa en las versiones 3.5.14 y v.3.4.33. La diferencia real dependerá de tu versión de parche; compruébalo primero con `diff <(etcd-3.5/bin/etcd -h | grep \\-\\-) <(etcd-3.4/bin/etcd -h | grep \\-\\-)`.

```diff
# flags not available in 3.4
-etcd --socket-reuse-port
-etcd --socket-reuse-address
-etcd --raft-read-timeout
-etcd --raft-write-timeout
-etcd --v2-deprecation
-etcd --client-cert-file
-etcd --client-key-file
-etcd --peer-client-cert-file
-etcd --peer-client-key-file
-etcd --self-signed-cert-validity
-etcd --enable-log-rotation --log-rotation-config-json=some.json
-etcd --experimental-enable-distributed-tracing --experimental-distributed-tracing-address='localhost:4317' --experimental-distributed-tracing-service-name='etcd' --experimental-distributed-tracing-instance-id='' --experimental-distributed-tracing-sampling-rate='0'
-etcd --experimental-compact-hash-check-enabled --experimental-compact-hash-check-time='1m'
-etcd --experimental-downgrade-check-time
-etcd --experimental-memory-mlock
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-stop-grpc-service-on-defrag

# same flag with different names
-etcd --backend-bbolt-freelist-type=map
+etcd --experimental-backend-bbolt-freelist-type=array

# same flag different defaults
-etcd --pre-vote=true
+etcd --pre-vote=false

-etcd --logger=zap
+etcd --logger=capnslog
```

#### `etcd --logger zap` {#etcd---logger-zap}

3.4 usa `--logger=capnslog` de forma predeterminada, mientras que 3.5 usa `--logger=zap` de forma predeterminada.

Si quieres seguir usando `zap`, hay que especificarlo explícitamente.

```diff
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

#### Diferencias en las métricas de Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in 3.4
-etcd_debugging_mvcc_db_compaction_last
```

### Listas de verificación para la degradación del servidor {#server-downgrade-checklists}

#### Requisitos de la degradación {#downgrade-requirements}

Para garantizar una degradación gradual sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster usando el comando `etcdctl endpoint health` antes de continuar.

La versión 3.4 a la que se va a degradar debe ser >= 3.4.32.

#### Preparación {#preparation}

Antes de degradar etcd, prueba siempre en un entorno de preproducción los servicios que dependen de etcd antes de desplegar la degradación en el entorno de producción.

Antes de comenzar, [descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la degradación, es posible usar esta copia de seguridad para [revertir](#rollback) y volver a la versión de etcd existente. Ten en cuenta que el comando `snapshot` solo respalda los datos v3. Para los datos v2, consulta [copia de seguridad del almacén de datos v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

Antes de comenzar, descarga la última versión de etcd 3.4 y asegúrate de que su versión sea >= 3.4.32.

#### Versiones mixtas {#mixed-versions}

Durante la degradación, un clúster de etcd admite versiones mixtas de miembros de etcd y opera con el protocolo de la versión común más baja. El clúster se considera degradado en cuanto cualquiera de sus miembros se degrada a la versión 3.4. Internamente, los miembros de etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

Nota: Si el clúster solo tiene datos v3 y ningún dato v2, no está sujeto a esta limitación.

Si el clúster sirve un conjunto de datos v2 de más de 50MB, cada miembro recién degradado puede tardar hasta dos minutos en ponerse al día con el clúster existente. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. En otras palabras, lo más seguro es esperar 2 minutos entre la degradación de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único puede tardar aún más tiempo. Los administradores de clústeres de etcd muy grandes de esta magnitud pueden contactar con el [equipo de etcd][etcd-contact] antes de degradar, y con gusto les ofreceremos consejo sobre el procedimiento.

#### Reversión {#rollback}

Si algún miembro se ha degradado a 3.4, la versión del clúster se degradará a 3.4 y las operaciones serán compatibles con «3.4». Tendrás que seguir las instrucciones de [Actualización de etcd de 3.4 a 3.5](/es/etcd/upgrades/upgrade_3_5/) para revertir.

Descarga la [copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para que sea posible revertir la degradación incluso después de que el clúster se haya degradado por completo.

### Procedimiento de degradación {#downgrade-procedure}

Este ejemplo muestra cómo degradar un clúster de etcd 3.5 de 3 miembros que se ejecuta en una máquina local.

#### Paso 1: comprobar los requisitos de la degradación {#step-1-check-downgrade-requirements}

¿Está el clúster en buen estado y ejecutando la versión 3.5.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.0","etcdcluster":"3.5.0"}
COMMENT
```

#### Paso 2: descargar la copia de seguridad de la instantánea desde el líder {#step-2-download-snapshot-backup-from-leader}

[Descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para disponer de una vía de reversión en caso de que surjan problemas.

#### Paso 3: detener un servidor de etcd existente {#step-3-stop-one-existing-etcd-server}

Antes de detener el servidor, comprueba si es el líder

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |      true |      false |         2 |          9 |                  9 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

Si el servidor que se va a detener es el líder, puedes evitar algo de tiempo de inactividad transfiriendo el liderazgo a otro servidor con `move-leader` antes de detener este servidor.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |      true |      false |         3 |         11 |                 11 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

Cuando se detiene cada proceso de etcd, los demás miembros del clúster registrarán errores esperados. Esto es normal, ya que se ha roto (temporalmente) la conexión con un miembro del clúster:

```bash
{"level":"info","ts":"2024-05-14T20:25:47.051124Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"91bc3c398fb3c146 became leader at term 3"}
{"level":"info","ts":"2024-05-14T20:25:47.051139Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: 91bc3c398fb3c146 elected leader 91bc3c398fb3c146 at term 3"}

^C{"level":"warn","ts":"2024-05-14T20:27:09.094119Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.09427Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.095535Z","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"8211f1d0f64f3269","error":"failed to dial 8211f1d0f64f3269 on stream MsgApp v2 (peer 8211f1d0f64f3269 failed to find local node 91bc3c398fb3c146)"}
{"level":"warn","ts":"2024-05-14T20:27:09.43915Z","caller":"rafthttp/stream.go:223","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269"}
{"level":"warn","ts":"2024-05-14T20:27:11.085646Z","caller":"etcdserver/cluster_util.go:294","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:11.085718Z","caller":"etcdserver/cluster_util.go:158","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:13.557385Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"416.079µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### Paso 4: reiniciar el servidor de etcd con la misma configuración + `--next-cluster-version-compatible` {#step-4-restart-the-etcd-server-with-same-configuration----next-cluster-version-compatible}

Reinicia el servidor de etcd con la misma configuración, pero con el nuevo binario de etcd y `--next-cluster-version-compatible`.

```diff
-etcd-3.5/bin --name s1 \
+etcd-3.4/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
  --next-cluster-version-compatible
```

El nuevo etcd 3.4 publicará su información en el clúster. En este punto, el clúster empezará a operar con el protocolo 3.4, que es la versión común más baja.

```bash
> `{"level":"info","ts":"2024-05-13T21:05:43.981445Z","caller":"membership/cluster.go:561","msg":"set initial cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982188Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982312Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.0","from":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982376Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:44.000672Z","caller":"etcdserver/server.go:2152","msg":"published local member to cluster through raft","local-member-id":"8211f1d0f64f3269","local-member-attributes":"{Name:infra1 ClientURLs:[http://127.0.0.1:2379]}","request-path":"/0/members/8211f1d0f64f3269/attributes","cluster-id":"ef37ad9dc622a7c4","publish-timeout":"7s"}`

> `{"level":"info","ts":"2024-05-13T21:05:46.452631Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.5","from":"3.4"}`
```

Comprueba que cada miembro, y luego el clúster entero, se encuentran en buen estado con el nuevo binario de etcd 3.4:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Los miembros aún no degradados registrarán información como la siguiente

```bash
{"level":"info","ts":"2024-05-13T21:05:46.450764Z","caller":"etcdserver/server.go:2633","msg":"updating cluster version using v2 API","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452419Z","caller":"membership/cluster.go:576","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452547Z","caller":"etcdserver/server.go:2652","msg":"cluster version is updated","cluster-version":"3.4"}
```

#### Paso 5: repetir el *paso 3* y el *paso 4* para el resto de los miembros {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Cuando todos los miembros estén degradados, comprueba el estado de salud y la versión del clúster:

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
