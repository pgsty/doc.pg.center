---
title: Actualizar etcd de v3.6 a v3.7
weight: 6550
description: Procesos, listas de verificación y notas sobre la actualización de etcd de v3.6 a v3.7
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
---

En el caso general, la actualización de etcd v3.6 a v3.7 puede realizarse sin tiempo de inactividad, mediante una actualización progresiva:

- uno por uno, detén los procesos etcd v3.6 y reemplázalos por procesos etcd v3.7
- después de ejecutar todos los procesos v3.7, las nuevas funcionalidades de v3.7 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la actualización {#upgrade-checklists}

#### Actualización de 3.6 {#update-36}

> [!IMPORTANT]
> Antes de actualizar a 3.7, asegúrate de que todos tus miembros 3.6 estén actualizados a 3.6.11 o posterior. Es posible que las versiones de parche de 3.6 anteriores no sean compatibles con una actualización progresiva a 3.7.

#### Almacén V2 {#v2-store}

El almacén v2 se eliminó por completo en v3.7. La API HTTP v2 (`--enable-v2`), la emulación de v2 sobre v3 (`--experimental-enable-v2v3`), el servicio de descubrimiento v2, el paquete `client/v2` y la carga de archivos de instantánea v2 ya no existen. Consulta las referencias de los cambios que rompen la compatibilidad en el [CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

Si actualizas desde un clúster 3.6, estas opciones ya están ausentes y no se requiere ninguna acción. Si vienes de una versión anterior con datos v2 personalizados, sigue la [guía de migración de v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/) antes de actualizar.

#### Refactorización de Go {#go-refactoring}

v3.7 contiene una refactorización interna sustancial que no afecta a quienes realizan una actualización normal, pero conviene tenerla presente al actualizar integraciones personalizadas:

- Migración de `gogo/protobuf` al estándar `google.golang.org/protobuf` (seguimiento en [#14533](https://github.com/etcd-io/etcd/issues/14533)).
- Migración de las bibliotecas obsoletas de registro y etiquetas de `go-grpc-middleware` v1 a los interceptores v2 ([#20420](https://github.com/etcd-io/etcd/pull/20420)).
- Los interceptores gRPC de OpenTelemetry se actualizaron a `otelgrpc` v0.61.0, reemplazando los obsoletos `UnaryServerInterceptor` y `StreamServerInterceptor` por `NewServerHandler` ([#20017](https://github.com/etcd-io/etcd/pull/20017)).

Si incrustas etcd como biblioteca, compilas contra la API `clientv3` o dependes de paquetes internos, revisa el [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md) antes de actualizar.

### Opciones eliminadas {#flags-removed}

Todas las opciones obsoletas `--experimental-*` se eliminaron en v3.7 ([#19959](https://github.com/etcd-io/etcd/pull/19959)). En v3.6, cada una de ellas fue reemplazada por una opción no experimental con el mismo nombre o por una entrada de `--feature-gates`. Si todavía tienes alguna configurada, reemplázala por su equivalente de v3.6 **antes** de pasar a v3.7; de lo contrario, el proceso de v3.7 no podrá iniciarse.

```diff
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-compact-hash-check-enabled
-etcd --experimental-compact-hash-check-time
-etcd --experimental-compaction-batch-limit
-etcd --experimental-compaction-sleep-interval
-etcd --experimental-corrupt-check-time
-etcd --experimental-distributed-tracing-address
-etcd --experimental-distributed-tracing-instance-id
-etcd --experimental-distributed-tracing-sampling-rate
-etcd --experimental-distributed-tracing-service-name
-etcd --experimental-downgrade-check-time
-etcd --experimental-enable-distributed-tracing
-etcd --experimental-enable-lease-checkpoint
-etcd --experimental-enable-lease-checkpoint-persist
-etcd --experimental-initial-corrupt-check
-etcd --experimental-memory-mlock
-etcd --experimental-peer-skip-client-san-verification
-etcd --experimental-snapshot-catchup-entries
-etcd --experimental-stop-grpc-service-on-defrag
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-warning-apply-duration
-etcd --experimental-warning-unary-request-duration
-etcd --experimental-watch-progress-notify-interval
```

Consulta la [guía de actualización de v3.5 a v3.6](/es/etcd/upgrades/upgrade_3_6/) para conocer la correspondencia de cada opción eliminada con su equivalente no experimental o su entrada de `--feature-gates`.

### Opciones añadidas {#flags-added}

Ninguna.

### Opciones con nuevos valores predeterminados {#flags-with-new-defaults}

Ninguna.

### Listas de verificación para la actualización del servidor {#server-upgrade-checklists}

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue de etcd existente a v3.7, el clúster en ejecución debe ser v3.6.11 o posterior. Si está en una versión menor anterior, [actualiza primero a v3.6](/es/etcd/upgrades/upgrade_3_6/); etcd solo admite la actualización de una versión menor a la vez.

Además, para garantizar una actualización progresiva sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre los servicios que dependen de etcd en un entorno de ensayo antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [revertir](#rollback) a la versión existente de etcd.

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster de etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión v3.7. Internamente, los miembros de etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Reversión {#rollback}

Antes de actualizar tu clúster de etcd, crea y [descarga una copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) de tu clúster de etcd. Esta instantánea se puede usar para restaurar el clúster a su estado anterior a la actualización si es necesario. Si los usuarios encuentran problemas durante la actualización, primero deben identificar y resolver la causa raíz. Si el clúster todavía está en un estado de versiones mixtas, en el que al menos un miembro permanece en v3.6, pueden reemplazar el binario o la imagen por la versión v3.6 anterior o restaurar el clúster directamente con la instantánea. En este estado mixto, el clúster sigue operando como un clúster v3.6, lo que permite revertir sin seguir un proceso formal de degradación.

Sin embargo, una vez que todos los miembros se hayan actualizado a v3.7, el clúster se considera completamente actualizado y la reversión mediante binarios ya no es posible. En ese caso, las únicas opciones de recuperación son restaurar el clúster desde la instantánea tomada antes de la actualización o seguir la [guía oficial de degradación](/es/etcd/downgrades/downgrading-etcd/) por si la actualización sale mal.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.6 de 3 miembros que se ejecuta en una máquina local. La salida siguiente proviene de una ejecución real contra etcd v3.6.12 y etcd v3.7.0-rc.0 en un único host con tres puertos de loopback.

#### Paso 1: comprobar los requisitos de actualización {#step-1-check-upgrade-requirements}

¿El clúster está en buen estado y ejecuta v3.6.11 o posterior?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 7.681459ms
localhost:22379 is healthy: successfully committed proposal: took = 7.691750ms
localhost:32379 is healthy: successfully committed proposal: took = 7.698000ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.12","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

#### Paso 2: descargar la copia de seguridad de la instantánea desde el líder {#step-2-download-snapshot-backup-from-leader}

[Descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para disponer de una ruta de degradación en caso de que surjan problemas.

Se garantiza que el líder de etcd tiene los datos de aplicación más recientes; por ello, obtén la instantánea desde el líder:

```bash
for p in 2379 22379 32379; do
  echo -n "localhost:$p leader="
  curl -sL http://localhost:$p/metrics | grep "^etcd_server_is_leader " | awk '{print $2}'
done
<<COMMENT
localhost:2379 leader=1
localhost:22379 leader=0
localhost:32379 leader=0
COMMENT

etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-06-02T07:01:41.863225+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-06-02T07:01:41.866451+0300","logger":"client","caller":"v3@v3.6.12/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-06-02T07:01:41.874080+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-06-02T07:01:41.877203+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"13.822583ms","etcd-version":"3.6.0"}
{"level":"info","ts":"2026-06-02T07:01:41.877303+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.6.0
COMMENT
```

#### Paso 3: detener un servidor etcd existente {#step-3-stop-one-existing-etcd-server}

Cuando se detiene cada proceso etcd, otros miembros del clúster registrarán errores esperados. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente). El líder transferirá el liderazgo antes de salir:

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
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

El nuevo etcd v3.7 publicará su información en el clúster. En este punto, el clúster sigue operando con el protocolo v3.6, que es la versión común más baja.

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

Verifica que cada miembro, y luego el clúster completo, quede en buen estado con el nuevo binario etcd v3.7:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | LEADER | RAFT TERM |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  false |         3 |
| localhost:22379 | 729934363faa4a24 |     3.6.12 |           3.6.0 |   98 kB |  false |         3 |
| localhost:32379 |  b548c2511513015 |     3.6.12 |           3.6.0 |   98 kB |   true |         3 |
+-----------------+------------------+------------+-----------------+---------+--------+-----------+
COMMENT
```

Los miembros no actualizados y el miembro actualizado registrarán mensajes sobre el estado de versiones mixtas hasta que todo el clúster se haya actualizado. Esto es esperado y cesará después de que todos los miembros del clúster etcd se hayan actualizado a v3.7.

#### Paso 5: repetir el *paso 3* y el *paso 4* para el resto de los miembros {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Cuando todos los miembros estén actualizados, el clúster informará que la actualización a v3.7 se realizó correctamente:

> `{"level":"info","ts":"2026-06-02T07:02:36.054783+0300","caller":"etcdserver/server.go:2311","msg":"updating cluster version using v3 API","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059345+0300","caller":"membership/cluster.go:593","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.6","to":"3.7"}`
>
> `{"level":"info","ts":"2026-06-02T07:02:36.059409+0300","caller":"etcdserver/server.go:2326","msg":"cluster version is updated","cluster-version":"3.7"}`

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 550.833µs
localhost:32379 is healthy: successfully committed proposal: took = 733.458µs
localhost:22379 is healthy: successfully committed proposal: took = 714.416µs
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
```
