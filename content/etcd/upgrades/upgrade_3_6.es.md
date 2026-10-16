---
title: Actualizar etcd de v3.5 a v3.6
weight: 6600
description: Procesos, listas de verificación y notas sobre la actualización de etcd de v3.5 a v3.6
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_6.md"
---

En el caso general, la actualización de etcd v3.5 a v3.6 puede realizarse sin tiempo de inactividad, mediante una actualización progresiva:

- uno por uno, detén los procesos etcd v3.5 y reemplázalos por procesos etcd v3.6
- después de ejecutar todos los procesos v3.6, las nuevas funcionalidades de v3.6 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la actualización {#upgrade-checklists}

#### Actualización de 3.5 {#update-35}

> [!IMPORTANT]
> Antes de actualizar a 3.6, asegúrate de que [todos tus miembros 3.5 estén actualizados a 3.5.32 o posterior](https://etcd.io/blog/2026/july-patch-release/). Las versiones de parche 3.5.24 a 3.5.26 corrigen varios posibles bloqueos de la actualización; [3.5.32](https://etcd.io/blog/2026/july-patch-release/) añade `--v2-deprecation=write-only-skip-check` y amplía `etcdutl check v2store` para inspeccionar también los registros de WAL además de la instantánea v2.

#### Almacén V2 {#v2-store}

> [!NOTE]
> Si la opción `--enable-v2` no está configurada o está establecida en false, no se requiere ninguna acción adicional.

Si `--enable-v2` **sí** está configurada, ejecuta el comando `etcdutl check v2store` para comprobar si el v2store contiene datos ajenos a la membresía (personalizados). Si no hay datos personalizados, la opción se puede eliminar de forma segura. De lo contrario, consulta la [guía de migración de v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/) para más detalles.

### Opciones añadidas {#flags-added}

```diff
+etcd --discovery-token ''
+etcd --discovery-endpoints ''
+etcd --discovery-dial-timeout '2s'
+etcd --discovery-request-timeout '5s'
+etcd --discovery-keepalive-time '2s'
+etcd --discovery-keepalive-timeout '6s'
+etcd --discovery-insecure-transport 'true'
+etcd --discovery-insecure-skip-tls-verify 'false'
+etcd --discovery-cert ''
+etcd --discovery-key ''
+etcd --discovery-cacert ''
+etcd --discovery-user ''
+etcd --discovery-password ''
+etcd --feature-gates
+etcd --log-format
```

### Opciones eliminadas {#flags-removed}

```diff
-etcd --enable-v2
-etcd --experimental-enable-v2v3
-etcd --proxy
-etcd --proxy-failure-wait
-etcd --proxy-refresh-interval
-etcd --proxy-dial-timeout
-etcd --proxy-write-timeout
-etcd --proxy-read-timeout
```

### Opciones obsoletas {#flags-deprecated}

**La opción `etcd --experimental-bootstrap-defrag-threshold-megabytes` quedó obsoleta.**

```diff

-etcd --experimental-bootstrap-defrag-threshold-megabytes

+etcd --bootstrap-defrag-threshold-megabytes

```

**La opción `etcd --experimental-compaction-batch-limit` quedó obsoleta.**

```diff

-etcd --experimental-compaction-batch-limit

+etcd --compaction-batch-limit

```

**La opción `etcd --experimental-compact-hash-check-time` quedó obsoleta.**

```diff

-etcd --experimental-compact-hash-check-time

+etcd --compact-hash-check-time

```

**La opción `etcd --experimental-compaction-sleep-interval` quedó obsoleta.**

```diff

-etcd --experimental-compaction-sleep-interval

+etcd --compaction-sleep-interval

```

**La opción `etcd --experimental-corrupt-check-time` quedó obsoleta.**

```diff

-etcd --experimental-corrupt-check-time

+etcd --corrupt-check-time

```

**La opción `etcd --experimental-enable-distributed-tracing` quedó obsoleta.**

```diff

-etcd --experimental-enable-distributed-tracing

+etcd --enable-distributed-tracing

```

**La opción `etcd --experimental-distributed-tracing-address` quedó obsoleta.**

```diff

-etcd --experimental-distributed-tracing-address

+etcd --distributed-tracing-address

```

**La opción `etcd --experimental-distributed-tracing-instance-id` quedó obsoleta.**

```diff

-etcd --experimental-distributed-tracing-instance-id

+etcd --distributed-tracing-instance-id

```

**La opción `etcd --experimental-distributed-tracing-sampling-rate` quedó obsoleta.**

```diff

-etcd --experimental-distributed-tracing-sampling-rate

+etcd --distributed-tracing-sampling-rate

```

**La opción `etcd --experimental-distributed-tracing-service-name` quedó obsoleta.**

```diff

-etcd --experimental-distributed-tracing-service-name

+etcd --distributed-tracing-service-name

```

**La opción `etcd --experimental-downgrade-check-time` quedó obsoleta.**

```diff

-etcd --experimental-downgrade-check-time

+etcd --downgrade-check-time

```

**La opción `etcd --experimental-max-learners` quedó obsoleta.**

```diff

-etcd --experimental-max-learners

+etcd --max-learners

```

**La opción `etcd --experimental-memory-mlock` quedó obsoleta.**

```diff

-etcd --experimental-memory-mlock

+etcd --memory-mlock

```

**La opción `etcd --experimental-peer-skip-client-san-verification` quedó obsoleta.**

```diff

-etcd --experimental-peer-skip-client-san-verification

+etcd --peer-skip-client-san-verification

```

**La opción `etcd --experimental-snapshot-catchup-entries` quedó obsoleta.**

```diff

-etcd --experimental-snapshot-catchup-entries

+etcd --snapshot-catchup-entries

```

**La opción `etcd --experimental-warning-apply-duration` quedó obsoleta.**

```diff

-etcd --experimental-warning-apply-duration

+etcd --warning-apply-duration

```

**La opción `etcd --experimental-warning-unary-request-duration` quedó obsoleta.**

```diff

-etcd --experimental-warning-unary-request-duration

+etcd --warning-unary-request-duration

```

**La opción `etcd --experimental-watch-progress-notify-interval` quedó obsoleta.**

```diff

-etcd --experimental-watch-progress-notify-interval

+etcd --watch-progress-notify-interval

```

### Migrar las opciones experimentales de v3.5 a feature gates {#equivalent-flags-of-v35-feature-gates}

**Feature gate correspondiente a `etcd --experimental-compact-hash-check-enabled=true`**

```diff

-etcd --experimental-compact-hash-check-enabled=true

+etcd --feature-gates=CompactHashCheck=true

```

**Feature gate correspondiente a `etcd --experimental-initial-corrupt-check=true`**

```diff

-etcd --experimental-initial-corrupt-check=true

+etcd --feature-gates=InitialCorruptCheck=true

```

**Feature gate correspondiente a `etcd --experimental-enable-lease-checkpoint=true`**

```diff

-etcd --experimental-enable-lease-checkpoint=true

+etcd --feature-gates=LeaseCheckpoint=true

```

**Feature gate correspondiente a `etcd --experimental-enable-lease-checkpoint-persist=true`**

```diff

-etcd --experimental-enable-lease-checkpoint-persist=true

+etcd --feature-gates=LeaseCheckpointPersist=true

```

**Feature gate correspondiente a `etcd --experimental-stop-grpc-service-on-defrag=true`**

```diff

-etcd --experimental-stop-grpc-service-on-defrag=true

+etcd --feature-gates=StopGRPCServiceOnDefrag=true

```

**Feature gate correspondiente a `etcd --experimental-txn-mode-write-with-shared-buffer=false`**

```diff

-etcd --experimental-txn-mode-write-with-shared-buffer=false

+etcd --feature-gates=TxnModeWriteWithSharedBuffer=false

```

### Opciones con nuevos valores predeterminados {#flags-with-new-defaults}

**Opción con el valor predeterminado original `etcd --snapshot-count=100000`**

```diff

-etcd --snapshot-count=100000

+etcd --snapshot-count=10000

```

**Opción con el valor predeterminado original `etcd --v2-deprecation='not-yet'`**

```diff

-etcd --v2-deprecation='not-yet'

+etcd --v2-deprecation='write-only'

```

**Opción con el valor predeterminado original `etcd --discovery-fallback='proxy'`**

```diff

-etcd --discovery-fallback='proxy'

+etcd --discovery-fallback='exit'

```

### Diferencia en las métricas Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics added in v3.6
+etcd_network_known_peers
+etcd_server_feature_enabled
```

### Listas de verificación para la actualización del servidor {#server-upgrade-checklists}

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue de etcd existente a v3.6, el clúster en ejecución debe ser v3.5 o superior. Si es anterior a v3.5, [actualiza primero a v3.5](/es/etcd/upgrades/upgrade_3_5/) antes de actualizar a v3.6.

Además, para garantizar una actualización progresiva sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre los servicios que dependen de etcd en un entorno de ensayo antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [revertir](#rollback) a la versión existente de etcd. Ten en cuenta que el comando `snapshot` solo hace copia de seguridad de los datos v3.

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster de etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión v3.6. Internamente, los miembros de etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Reversión {#rollback}

Antes de actualizar tu clúster de etcd, crea y [descarga una copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) de tu clúster de etcd. Esta instantánea se puede usar para restaurar el clúster a su estado anterior a la actualización si es necesario. Si los usuarios encuentran problemas durante la actualización, primero deben identificar y resolver la causa raíz. Si el clúster todavía está en un estado de versiones mixtas —en el que al menos un miembro permanece en v3.5—, pueden reemplazar el binario o la imagen por la versión v3.5 anterior o restaurar el clúster directamente con la instantánea. En este estado mixto, el clúster sigue operando como un clúster v3.5, lo que permite revertir sin seguir un proceso formal de degradación.

Sin embargo, una vez que todos los miembros se hayan actualizado a v3.6, el clúster se considera completamente actualizado y el simple reemplazo de los binarios ya no constituye una reversión válida. Las opciones de recuperación son restaurar el clúster desde la instantánea tomada antes de la actualización o seguir la guía oficial de degradación para volver a la versión original, garantizando la consistencia y evitando la corrupción de datos.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.5 de 3 miembros que se ejecuta en una máquina local.

#### Paso 1: comprobar los requisitos de actualización {#step-1-check-upgrade-requirements}

¿El clúster está en buen estado y ejecuta v3.5.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.555774ms
localhost:32379 is healthy: successfully committed proposal: took = 2.631133ms
localhost:22379 is healthy: successfully committed proposal: took = 3.020958ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.5.18","etcdcluster":"3.5.0"}
COMMENT
```

#### Paso 2: descargar la copia de seguridad de la instantánea desde el líder {#step-2-download-snapshot-backup-from-leader}

[Descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para disponer de una ruta de degradación en caso de que surjan problemas.

Se garantiza que el líder de etcd tiene los datos de aplicación más recientes; por ello, obtén la instantánea desde el líder:

```bash
curl -sL http://localhost:2379/metrics | grep etcd_server_is_leader
<<COMMENT
# HELP etcd_server_is_leader Whether or not this member is a leader. 1 if is, 0 otherwise.
# TYPE etcd_server_is_leader gauge
etcd_server_is_leader 1
COMMENT

curl -sL http://localhost:22379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

curl -sL http://localhost:32379/metrics | grep etcd_server_is_leader
<<COMMENT
etcd_server_is_leader 0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2025-03-01T04:34:10.336768+0530","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2025-03-01T04:34:10.342373+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-01T04:34:10.342433+0530","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2025-03-01T04:34:10.346482+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-01T04:34:10.348801+0530","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"localhost:2379","size":"20 kB","took":"now"}
{"level":"info","ts":"2025-03-01T04:34:10.348933+0530","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### Paso 3: detener un servidor etcd existente {#step-3-stop-one-existing-etcd-server}

Cuando se detiene cada proceso etcd, otros miembros del clúster registrarán errores esperados. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente):

```bash
{"level":"info","ts":"2025-03-01T04:31:50.654520+0530","caller":"etcdserver/server.go:2676","msg":"cluster version is updated","cluster-version":"3.5"}
{"level":"info","ts":"2025-03-01T04:34:10.345927+0530","caller":"v3rpc/maintenance.go:130","msg":"sending database snapshot to client","total-bytes":20480,"size":"20 kB"}
{"level":"info","ts":"2025-03-01T04:34:10.346094+0530","caller":"v3rpc/maintenance.go:170","msg":"sending database sha256 checksum to client","total-bytes":20480,"checksum-size":32}
{"level":"info","ts":"2025-03-01T04:34:10.346108+0530","caller":"v3rpc/maintenance.go:179","msg":"successfully sent database snapshot to client","total-bytes":20480,"size":"20 kB","took":"now"}
^C
{"level":"info","ts":"2025-03-01T04:35:01.443045+0530","caller":"osutil/interrupt_unix.go:64","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":"2025-03-01T04:35:01.443088+0530","caller":"embed/etcd.go:408","msg":"closing etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
{"level":"info","ts":"2025-03-01T04:35:01.443417+0530","caller":"etcdserver/server.go:1503","msg":"leadership transfer starting","local-member-id":"bf9071f4639c75cc","current-leader-member-id":"bf9071f4639c75cc","transferee-member-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443441+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term 2] starts to transfer leadership to 91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.443455+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc sends MsgTimeoutNow to 91bc3c398fb3c146 immediately as 91bc3c398fb3c146 already has up-to-date log"}
{"level":"warn","ts":"2025-03-01T04:35:01.443517+0530","caller":"embed/serve.go:179","msg":"stopping insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"warn","ts":"2025-03-01T04:35:01.443548+0530","caller":"embed/serve.go:181","msg":"stopped insecure grpc server due to error","error":"accept tcp 127.0.0.1:2379: use of closed network connection"}
{"level":"info","ts":"2025-03-01T04:35:01.445536+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [term: 2] received a MsgVote message with higher term from 91bc3c398fb3c146 [term: 3]"}
{"level":"info","ts":"2025-03-01T04:35:01.445556+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc became follower at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445565+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"bf9071f4639c75cc [logterm: 2, index: 12, vote: 0] cast MsgVote for 91bc3c398fb3c146 [logterm: 2, index: 12] at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.445572+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc lost leader bf9071f4639c75cc at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.446773+0530","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: bf9071f4639c75cc elected leader 91bc3c398fb3c146 at term 3"}
{"level":"info","ts":"2025-03-01T04:35:01.544062+0530","caller":"etcdserver/server.go:1520","msg":"leadership transfer finished","local-member-id":"bf9071f4639c75cc","old-leader-member-id":"bf9071f4639c75cc","new-leader-member-id":"91bc3c398fb3c146","took":"100.640374ms"}
{"level":"info","ts":"2025-03-01T04:35:01.544160+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.544956+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.544984+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545050+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545065+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545099+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545156+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545178+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"91bc3c398fb3c146","error":"failed to read 91bc3c398fb3c146 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545199+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"warn","ts":"2025-03-01T04:35:01.545246+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545263+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545272+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"91bc3c398fb3c146"}
{"level":"info","ts":"2025-03-01T04:35:01.545282+0530","caller":"rafthttp/peer.go:330","msg":"stopping remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545307+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545328+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545359+0530","caller":"rafthttp/stream.go:286","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545379+0530","caller":"rafthttp/stream.go:294","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545410+0530","caller":"rafthttp/pipeline.go:85","msg":"stopped HTTP pipelining with remote peer","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545467+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"warn","ts":"2025-03-01T04:35:01.545485+0530","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"fd422379fda50e48","error":"failed to read fd422379fda50e48 on stream MsgApp v2 (context canceled)"}
{"level":"info","ts":"2025-03-01T04:35:01.545504+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545560+0530","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48","error":"context canceled"}
{"level":"info","ts":"2025-03-01T04:35:01.545577+0530","caller":"rafthttp/stream.go:442","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"bf9071f4639c75cc","remote-peer-id":"fd422379fda50e48"}
{"level":"info","ts":"2025-03-01T04:35:01.545592+0530","caller":"rafthttp/peer.go:335","msg":"stopped remote peer","remote-peer-id":"fd422379fda50e48"}
{"level":"warn","ts":"2025-03-01T04:35:01.545669+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545698+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545732+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"91bc3c398fb3c146","cluster-id":"59a05384c9b79ee"}
{"level":"warn","ts":"2025-03-01T04:35:01.545765+0530","caller":"rafthttp/http.go:413","msg":"failed to find remote peer in cluster","local-member-id":"bf9071f4639c75cc","remote-peer-id-stream-handler":"bf9071f4639c75cc","remote-peer-id-from":"fd422379fda50e48","cluster-id":"59a05384c9b79ee"}
{"level":"info","ts":"2025-03-01T04:35:01.549658+0530","caller":"embed/etcd.go:613","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550532+0530","caller":"embed/etcd.go:618","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":"2025-03-01T04:35:02.550561+0530","caller":"embed/etcd.go:410","msg":"closed etcd server","name":"node1","data-dir":"/tmp/etcd-node1","advertise-peer-urls":["http://127.0.0.1:2380"],"advertise-client-urls":["http://127.0.0.1:2379"]}
```

#### Paso 4: reiniciar el servidor etcd con la misma configuración {#step-4-restart-the-etcd-server-with-same-configuration}

Reinicia el servidor etcd con la misma configuración pero con el nuevo binario de etcd.

```diff
-etcd-old --name ${name} \
+etcd-new --name ${name} \
  --data-dir /path/to/${name}.etcd \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

El nuevo etcd v3.6 publicará su información en el clúster. En este punto, el clúster sigue operando con el protocolo v3.5, que es la versión común más baja.

> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.889+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"bf9071f4639c75cc","from":"3.0","to":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.894+0530","caller":"etcdserver/server.go:1686","msg":"published local member to cluster through raft","local-member-id":"bf9071f4639c75cc","local-member-attributes":"{Name:node1 ClientURLs:[http://127.0.0.1:2379]}","cluster-id":"59a05384c9b79ee","publish-timeout":"7s"}`

Verifica que cada miembro, y luego el clúster completo, quede en buen estado con el nuevo binario etcd v3.6:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.704998ms
localhost:22379 is healthy: successfully committed proposal: took = 2.331754ms
localhost:32379 is healthy: successfully committed proposal: took = 2.490705ms
COMMENT
```

Los miembros no actualizados registrarán advertencias como la siguiente hasta que todo el clúster se haya actualizado.

Esto es esperado y cesará después de que todos los miembros del clúster etcd se hayan actualizado a v3.6:

```bash
{"level":"warn","ts":"2025-03-01T04:40:37.545960+0530","caller":"etcdserver/cluster_util.go:189","msg":"leader found higher-versioned member","local-member-version":"3.5.18","remote-member-id":"bf9071f4639c75cc","remote-member-version":"3.6.0-alpha.0"}
```

#### Paso 5: repetir el *paso 3* y el *paso 4* para el resto de los miembros {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Cuando todos los miembros estén actualizados, el clúster informará que la actualización a v3.6 se realizó correctamente:

Miembro 1:

> `{"level":"info","ts":"2025-03-01T04:58:32.375+0530","caller":"etcdserver/server.go:2149","msg":"updating cluster version using v3 API","from":"3.5","to":"3.6"}`
> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"etcdserver/server.go:2164","msg":"cluster version is updated","cluster-version":"3.6"}`

Miembro 2:

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.6"}`

Miembro 3:

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"fd422379fda50e48","from":"3.5","to":"3.6"}`

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0"}
COMMENT
```
