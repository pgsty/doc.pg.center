---
title: Actualizar etcd de 3.4 a 3.5
weight: 6650
description: Procesos, listas de verificación y notas sobre la actualización de etcd de 3.4 a 3.5
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_5.md"
---

En el caso general, la actualización de etcd 3.4 a 3.5 puede realizarse sin tiempo de inactividad, mediante una actualización progresiva:
 - uno por uno, detén los procesos etcd v3.4 y reemplázalos por procesos etcd v3.5
 - después de ejecutar todos los procesos v3.5, las nuevas funcionalidades de v3.5 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.



### Listas de verificación para la actualización {#upgrade-checklists}

> [!WARNING]
> Cuando se [migra desde v2 sin datos v3](https://github.com/etcd-io/etcd/issues/9480), el servidor etcd v3.2+ entra en pánico cuando etcd restaura a partir de instantáneas existentes pero no hay ningún archivo v3 `ETCD_DATA_DIR/member/snap/db`. Esto ocurre cuando el servidor se había migrado desde v2 sin datos v3 previos. Esto también evita la pérdida accidental de datos v3 (por ejemplo, el archivo `db` podría haberse movido). etcd exige que la migración posterior a v3 solo pueda realizarse con datos v3. No actualices a versiones v3 más recientes hasta que el servidor v3.0 contenga datos v3.

> [!WARNING]
> Si tu clúster habilita la autenticación, la actualización progresiva desde 3.4 o una versión anterior no se admite, porque 3.5 [cambia el formato de las entradas de WAL relacionadas con la autenticación](https://github.com/etcd-io/etcd/pull/11943).

Cambios destacados que rompen la compatibilidad en 3.5.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` {#deprecated-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.5 promovió las métricas Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` a `etcd_mvcc_db_total_size_in_bytes`, para fomentar la supervisión del almacenamiento de etcd. Y v3.5 depreca por completo `etcd_debugging_mvcc_db_total_size_in_bytes`.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_put_total` {#deprecated-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.5 promovió las métricas Prometheus `etcd_debugging_mvcc_put_total` a `etcd_mvcc_put_total`, para fomentar la supervisión del almacenamiento de etcd. Y v3.5 depreca por completo `etcd_debugging_mvcc_put_total`.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_delete_total` {#deprecated-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.5 promovió las métricas Prometheus `etcd_debugging_mvcc_delete_total` a `etcd_mvcc_delete_total`, para fomentar la supervisión del almacenamiento de etcd. Y v3.5 depreca por completo `etcd_debugging_mvcc_delete_total`.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_txn_total` {#deprecated-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.5 promovió las métricas Prometheus `etcd_debugging_mvcc_txn_total` a `etcd_mvcc_txn_total`, para fomentar la supervisión del almacenamiento de etcd. Y v3.5 depreca por completo `etcd_debugging_mvcc_txn_total`.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_range_total` {#deprecated-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.5 promovió las métricas Prometheus `etcd_debugging_mvcc_range_total` a `etcd_mvcc_range_total`, para fomentar la supervisión del almacenamiento de etcd. Y v3.5 depreca por completo `etcd_debugging_mvcc_range_total`.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de `etcd --logger capnslog` {#deprecated-etcd---logger-capnslog}

v3.5 usa `--logger=zap` como valor predeterminado para admitir múltiples salidas de registro y el registro estructurado.

**`etcd --logger=capnslog` quedó obsoleto en v3.5**, y ahora `--logger=zap` es el valor predeterminado.

```diff
-etcd --logger=capnslog
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 añadió la compatibilidad con `etcd --logger=zap` para el registro estructurado y múltiples salidas de registro. La motivación principal es fomentar la supervisión automatizada de etcd, en lugar de revisar los registros del servidor cuando empieza a fallar. El desarrollo futuro hará que etcd registre lo menos posible y que sea más fácil de supervisar con métricas y alertas. **`etcd --logger=capnslog` quedará obsoleto en v3.5.**

#### Deprecación de `etcd --log-output` {#deprecated-etcd---log-output}

v3.4 renombró [`etcd --log-output` a `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624) para admitir múltiples salidas de registro.

**`etcd --log-output` quedó obsoleto en v3.5.**

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr
```

#### Deprecación de la opción `etcd --debug` (ahora `--log-level=debug`) {#deprecated-etcd---debug-flag-now---log-leveldebug}

**La opción `etcd --debug` quedó obsoleta.**

```diff
-etcd --debug
+etcd --log-level debug
```

#### Deprecación de `etcd --log-package-levels` {#deprecated-etcd---log-package-levels}

**La opción `etcd --log-package-levels` para `capnslog` quedó obsoleta.**

Ahora, **`etcd --logger=zap`** es el valor predeterminado.

```diff
-etcd --log-package-levels 'etcdmain=CRITICAL,etcdserver=DEBUG'
+etcd --logger=zap --log-outputs=stderr
```

#### Deprecación de `[CLIENT-URL]/config/local/log` {#deprecated-client-urlconfiglocallog}

**El endpoint `/config/local/log` está quedando obsoleto en v3.5, al igual que la opción `etcd --log-package-levels`.**

```diff
-$ curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
-# debug logging enabled
```

#### Cambio en los endpoints HTTP de la pasarela gRPC (`/v3beta` obsoleto) {#changed-grpc-gateway-http-endpoints-deprecated-v3beta}

Antes

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Después

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

`/v3beta` se eliminó en la versión 3.5.



### Listas de verificación para la actualización del servidor {#server-upgrade-checklists}

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue de etcd existente a 3.5, el clúster en ejecución debe ser 3.4 o superior. Si es anterior a 3.4, [actualiza primero a 3.4](/es/etcd/upgrades/upgrade_3_4/) antes de actualizar a 3.5.

Además, para garantizar una actualización progresiva sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre los servicios que dependen de etcd en un entorno de ensayo antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [degradar](#downgrade) a la versión existente de etcd. Ten en cuenta que el comando `snapshot` solo hace copia de seguridad de los datos v3. Para los datos v2, consulta [copia de seguridad del almacén de datos v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster de etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión 3.5. Internamente, los miembros de etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

Nota: Si el clúster solo tiene datos v3 y ningún dato v2, no está sujeto a esta limitación.

Si el clúster está sirviendo un conjunto de datos v2 de más de 50MB, cada miembro recién actualizado puede tardar hasta dos minutos en ponerse al día con el clúster existente. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. En otras palabras, lo más seguro es esperar 2 minutos entre la actualización de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único podría tardar aún más tiempo. Los administradores de clústeres etcd muy grandes de esta magnitud pueden contactar sin compromiso al [equipo de etcd][etcd-contact] antes de actualizar, y con gusto les proporcionaremos consejos sobre el procedimiento.

#### Degradación {#downgrade}

Si todos los miembros se han actualizado a v3.5, el clúster se actualizará a v3.5 y la degradación desde este estado completado **no es posible**. Sin embargo, si algún miembro individual sigue en v3.4, el clúster y sus operaciones permanecen en «v3.4» y, desde este estado de clúster mixto, es posible volver a usar un binario etcd v3.4 en todos los miembros.

[Descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para que sea posible degradar el clúster incluso después de que se haya actualizado por completo.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.4 de 3 miembros que se ejecuta en una máquina local.

#### Paso 1: comprobar los requisitos de actualización {#step-1-check-upgrade-requirements}

¿El clúster está en buen estado y ejecuta v3.4.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.0","etcdcluster":"3.4.0"}
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
{"level":"info","ts":1526585787.148433,"caller":"snapshot/v3_snapshot.go:109","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":1526585787.1485257,"caller":"snapshot/v3_snapshot.go:120","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":1526585787.1519694,"caller":"snapshot/v3_snapshot.go:133","msg":"fetched snapshot","endpoint":"localhost:2379","took":0.003502721}
{"level":"info","ts":1526585787.1520295,"caller":"snapshot/v3_snapshot.go:142","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### Paso 3: detener un servidor etcd existente {#step-3-stop-one-existing-etcd-server}

Cuando se detiene cada proceso etcd, otros miembros del clúster registrarán errores esperados. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente):

```bash
{"level":"info","ts":1526587281.2001143,"caller":"etcdserver/server.go:2249","msg":"updating cluster version","from":"3.0","to":"3.4"}
{"level":"info","ts":1526587281.2010646,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}
{"level":"info","ts":1526587281.2012327,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}
{"level":"info","ts":1526587281.2013083,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}



^C{"level":"info","ts":1526587299.0717514,"caller":"osutil/interrupt_unix.go:63","msg":"received signal; shutting down","signal":"interrupt"}
{"level":"info","ts":1526587299.0718873,"caller":"embed/etcd.go:285","msg":"closing etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
{"level":"info","ts":1526587299.0722554,"caller":"etcdserver/server.go:1341","msg":"leadership transfer starting","local-member-id":"7339c4e5e833c029","current-leader-member-id":"7339c4e5e833c029","transferee-member-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.0723994,"caller":"raft/raft.go:1107","msg":"7339c4e5e833c029 [term 3] starts to transfer leadership to 729934363faa4a24"}
{"level":"info","ts":1526587299.0724802,"caller":"raft/raft.go:1113","msg":"7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log"}
{"level":"info","ts":1526587299.0737045,"caller":"raft/raft.go:797","msg":"7339c4e5e833c029 [term: 3] received a MsgVote message with higher term from 729934363faa4a24 [term: 4]"}
{"level":"info","ts":1526587299.0737681,"caller":"raft/raft.go:656","msg":"7339c4e5e833c029 became follower at term 4"}
{"level":"info","ts":1526587299.073831,"caller":"raft/raft.go:882","msg":"7339c4e5e833c029 [logterm: 3, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 3, index: 9] at term 4"}
{"level":"info","ts":1526587299.0738947,"caller":"raft/node.go:312","msg":"raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 4"}
{"level":"info","ts":1526587299.0748374,"caller":"raft/node.go:306","msg":"raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 4"}
{"level":"info","ts":1526587299.1726425,"caller":"etcdserver/server.go:1362","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"729934363faa4a24","took":0.100389359}
{"level":"info","ts":1526587299.1728148,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1751974,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1752589,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.177348,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1774004,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.177515,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1777067,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34636->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1778402,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"warn","ts":1526587299.1780295,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015","error":"read tcp 127.0.0.1:34634->127.0.0.1:32380: use of closed network connection"}
{"level":"info","ts":1526587299.1780987,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781602,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"b548c2511513015"}
{"level":"info","ts":1526587299.1781986,"caller":"rafthttp/peer.go:333","msg":"stopping remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1802843,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1803446,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream MsgApp v2","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1824749,"caller":"rafthttp/stream.go:291","msg":"closed TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.18255,"caller":"rafthttp/stream.go:301","msg":"stopped TCP streaming connection with remote peer","stream-writer-type":"stream Message","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.18261,"caller":"rafthttp/pipeline.go:86","msg":"stopped HTTP pipelining with remote peer","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1827736,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"read tcp 127.0.0.1:51482->127.0.0.1:22380: use of closed network connection"}
{"level":"info","ts":1526587299.182845,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1830168,"caller":"rafthttp/stream.go:436","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24","error":"context canceled"}
{"level":"warn","ts":1526587299.1831107,"caller":"rafthttp/peer_status.go:65","msg":"peer became inactive","peer-id":"729934363faa4a24","error":"failed to read 729934363faa4a24 on stream Message (context canceled)"}
{"level":"info","ts":1526587299.1831737,"caller":"rafthttp/stream.go:459","msg":"stopped stream reader with remote peer","stream-reader-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"info","ts":1526587299.1832306,"caller":"rafthttp/peer.go:340","msg":"stopped remote peer","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":1526587299.1837125,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1840093,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"b548c2511513015","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1842315,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"warn","ts":1526587299.1844475,"caller":"rafthttp/http.go:424","msg":"failed to find remote peer in cluster","local-member-id":"7339c4e5e833c029","remote-peer-id-stream-handler":"7339c4e5e833c029","remote-peer-id-from":"729934363faa4a24","cluster-id":"7dee9ba76d59ed53"}
{"level":"info","ts":1526587299.2056687,"caller":"embed/etcd.go:473","msg":"stopping serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.205819,"caller":"embed/etcd.go:480","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
{"level":"info","ts":1526587299.2058413,"caller":"embed/etcd.go:289","msg":"closed etcd server","name":"s1","data-dir":"/tmp/etcd/s1","advertise-peer-urls":["http://localhost:2380"],"advertise-client-urls":["http://localhost:2379"]}
```

#### Paso 4: reiniciar el servidor etcd con la misma configuración {#step-4-restart-the-etcd-server-with-same-configuration}

Reinicia el servidor etcd con la misma configuración pero con el nuevo binario de etcd.

```diff
-etcd-old --name s1 \
+etcd-new --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state new
```

El nuevo etcd v3.5 publicará su información en el clúster. En este punto, el clúster sigue operando con el protocolo v3.4, que es la versión común más baja.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Verifica que cada miembro, y luego el clúster completo, quede en buen estado con el nuevo binario etcd v3.5:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Los miembros no actualizados registrarán advertencias como la siguiente hasta que todo el clúster se haya actualizado.

Esto es esperado y cesará después de que todos los miembros del clúster etcd se hayan actualizado a v3.5:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.5.0
:45.945154 W | etcdserver: the local etcd version 3.4.0 is not up-to-date
```

#### Paso 5: repetir el *paso 3* y el *paso 4* para el resto de los miembros {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Cuando todos los miembros estén actualizados, el clúster informará que la actualización a 3.5 se realizó correctamente:

Miembro 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.5"}`

Miembro 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`

Miembro 3:

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
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

[etcd-contact]: https://groups.google.com/g/etcd-dev
