---
title: Actualizar etcd de 3.3 a 3.4
weight: 6700
description: Procesos, listas de verificación y notas sobre la actualización de etcd de 3.3 a 3.4
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
---

En el caso general, la actualización de etcd 3.3 a 3.4 puede realizarse sin tiempo de inactividad, mediante una actualización progresiva:
 - uno por uno, detén los procesos etcd v3.3 y reemplázalos por procesos etcd v3.4
 - después de ejecutar todos los procesos v3.4, las nuevas funcionalidades de v3.4 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.



### Listas de verificación para la actualización {#upgrade-checklists}

> [!WARNING]
> Cuando se [migra desde v2 sin datos v3](https://github.com/etcd-io/etcd/issues/9480), el servidor etcd v3.2+ entra en pánico cuando etcd restaura a partir de instantáneas existentes pero no hay ningún archivo v3 `ETCD_DATA_DIR/member/snap/db`. Esto ocurre cuando el servidor se había migrado desde v2 sin datos v3 previos. Esto también evita la pérdida accidental de datos v3 (por ejemplo, el archivo `db` podría haberse movido). etcd exige que la migración posterior a v3 solo pueda realizarse con datos v3. No actualices a versiones v3 más recientes hasta que el servidor v3.0 contenga datos v3.

Cambios destacados que rompen la compatibilidad en 3.4.

#### `ETCDCTL_API=3 etcdctl` como valor predeterminado {#make-etcdctl_api3-etcdctl-default}

`ETCDCTL_API=3` es ahora el valor predeterminado.

```diff
etcdctl set foo bar
Error: unknown command "set" for "etcdctl"

-etcdctl set foo bar
+ETCDCTL_API=2 etcdctl set foo bar
bar

ETCDCTL_API=3 etcdctl put foo bar
OK

-ETCDCTL_API=3 etcdctl put foo bar
+etcdctl put foo bar
```

#### `etcd --enable-v2=false` como valor predeterminado {#make-etcd---enable-v2false-default}

[`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935) es ahora el valor predeterminado.

Esto significa que, a menos que se especifique `etcd --enable-v2=true`, el servidor etcd v3.4 no atendería solicitudes de la API v2.

Si se usaba la API v2, asegúrate de habilitar la API v2 en v3.4:

```diff
-etcd
+etcd --enable-v2=true
```

Otras API HTTP seguirán funcionando (p. ej., `[CLIENT-URL]/metrics`, `[CLIENT-URL]/health`, la pasarela gRPC v3).

#### Deprecación de las opciones `etcd --ca-file` y `etcd --peer-ca-file` {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

Las opciones `--ca-file` y `--peer-ca-file` están obsoletas; lo están desde v2.1.

Ten en cuenta que establecer este parámetro también habilitará automáticamente la autenticación de certificados de cliente sin importar el valor configurado en `--client-cert-auth`.

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### Deprecación del error `grpc.ErrClientConnClosing` {#deprecated-grpcerrclientconnclosing-error}

`grpc.ErrClientConnClosing` ha quedado [obsoleto en gRPC >= 1.10](https://github.com/grpc/grpc-go/pull/1854).

```diff
import (
+	"go.etcd.io/etcd/clientv3"

	"google.golang.org/grpc"
+	"google.golang.org/grpc/codes"
+	"google.golang.org/grpc/status"
)

_, err := kvc.Get(ctx, "a")
-if err == grpc.ErrClientConnClosing {
+if clientv3.IsConnCanceled(err) {

// or
+s, ok := status.FromError(err)
+if ok {
+  if s.Code() == codes.Canceled
```

#### Requerir `grpc.WithBlock` para la conexión del cliente {#require-grpcwithblock-for-client-dial}

[El nuevo balanceador del cliente](/es/etcd/learning/design-client/) utiliza un resolutor asíncrono para pasar los endpoints a la función de conexión de gRPC. Como resultado, el cliente v3.4 requiere la opción de conexión `grpc.WithBlock` para esperar hasta que la conexión subyacente esté activa.

```diff
import (
	"time"
	"go.etcd.io/etcd/clientv3"
+	"google.golang.org/grpc"
)

+// "grpc.WithBlock()" to block until the underlying connection is up
ccfg := clientv3.Config{
  Endpoints:            []string{"localhost:2379"},
  DialTimeout:          time.Second,
+ DialOptions:          []grpc.DialOption{grpc.WithBlock()},
  DialKeepAliveTime:    time.Second,
  DialKeepAliveTimeout: 500 * time.Millisecond,
}
```

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

v3.4 promueve las métricas Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` a `etcd_mvcc_db_total_size_in_bytes`, para fomentar la supervisión del almacenamiento de etcd.

`etcd_debugging_mvcc_db_total_size_in_bytes` todavía se sirve en v3.4 por compatibilidad con versiones anteriores. Quedará completamente obsoleta en v3.5.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_put_total` {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

v3.4 promueve las métricas Prometheus `etcd_debugging_mvcc_put_total` a `etcd_mvcc_put_total`, para fomentar la supervisión del almacenamiento de etcd.

`etcd_debugging_mvcc_put_total` todavía se sirve en v3.4 por compatibilidad con versiones anteriores. Quedará completamente obsoleta en v3.5.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_delete_total` {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

v3.4 promueve las métricas Prometheus `etcd_debugging_mvcc_delete_total` a `etcd_mvcc_delete_total`, para fomentar la supervisión del almacenamiento de etcd.

`etcd_debugging_mvcc_delete_total` todavía se sirve en v3.4 por compatibilidad con versiones anteriores. Quedará completamente obsoleta en v3.5.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_txn_total` {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

v3.4 promueve las métricas Prometheus `etcd_debugging_mvcc_txn_total` a `etcd_mvcc_txn_total`, para fomentar la supervisión del almacenamiento de etcd.

`etcd_debugging_mvcc_txn_total` todavía se sirve en v3.4 por compatibilidad con versiones anteriores. Quedará completamente obsoleta en v3.5.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de las métricas Prometheus `etcd_debugging_mvcc_range_total` {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

v3.4 promueve las métricas Prometheus `etcd_debugging_mvcc_range_total` a `etcd_mvcc_range_total`, para fomentar la supervisión del almacenamiento de etcd.

`etcd_debugging_mvcc_range_total` todavía se sirve en v3.4 por compatibilidad con versiones anteriores. Quedará completamente obsoleta en v3.5.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Ten en cuenta que las métricas del espacio de nombres `etcd_debugging_*` se han marcado como experimentales. A medida que mejoremos la guía de supervisión, es posible que promovamos más métricas.

#### Deprecación de la opción `etcd --log-output` (ahora `--log-outputs`) {#deprecating-etcd---log-output-flag-now---log-outputs}

Se renombró [`etcd --log-output` a `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624) para admitir múltiples salidas de registro. **`etcd --logger=capnslog` no admite múltiples salidas de registro.**

**`etcd --log-output`** quedará obsoleto en v3.5. **`etcd --logger=capnslog` quedará obsoleto en v3.5**.

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

v3.4 añade la compatibilidad con `etcd --logger=zap --log-outputs=stderr` para el registro estructurado y múltiples salidas de registro. La motivación principal es fomentar la supervisión automatizada de etcd, en lugar de revisar los registros del servidor cuando empieza a fallar. El desarrollo futuro hará que etcd registre lo menos posible y que sea más fácil de supervisar con métricas y alertas. **`etcd --logger=capnslog` quedará obsoleto en v3.5**.

#### Cambio del tipo del campo `log-outputs` en `etcd --config-file` a `[]string` {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

Ahora que `log-outputs` (nombre de campo antiguo `log-output`) acepta múltiples destinos de escritura, el campo `log-outputs` del archivo YAML de configuración de etcd debe cambiarse al tipo `[]string` como se muestra a continuación:

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### Renombrado `embed.Config.LogOutput` a `embed.Config.LogOutputs` {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

Se renombró [**`embed.Config.LogOutput`** a **`embed.Config.LogOutputs`**](https://github.com/etcd-io/etcd/pull/9624) para admitir múltiples salidas de registro. Y se cambió [el tipo de `embed.Config.LogOutput` de `string` a `[]string`](https://github.com/etcd-io/etcd/pull/9579) para admitir múltiples salidas de registro.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### v3.5 depreca `capnslog` {#v35-deprecates-capnslog}

**v3.5 deprecará la opción `etcd --log-package-levels` para `capnslog`**; `etcd --logger=zap --log-outputs=stderr` será el valor predeterminado. **v3.5 deprecará el endpoint `[CLIENT-URL]/config/local/log`.**

```diff
-etcd
+etcd --logger zap
```

#### Deprecación de la opción `etcd --debug` (ahora `--log-level=debug`) {#deprecating-etcd---debug-flag-now---log-leveldebug}

v3.4 depreca la opción [`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947). En su lugar, usa la opción `etcd --log-level=debug`.

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### Deprecación del campo `pkg/transport.TLSInfo.CAFile` {#deprecated-pkgtransporttlsinfocafile-field}

El campo `pkg/transport.TLSInfo.CAFile` está obsoleto.

```diff
import "github.com/coreos/etcd/pkg/transport"

tlsInfo := transport.TLSInfo{
    CertFile: "/tmp/test-certs/test.pem",
    KeyFile: "/tmp/test-certs/test-key.pem",
-   CAFile: "/tmp/test-certs/trusted-ca.pem",
+   TrustedCAFile: "/tmp/test-certs/trusted-ca.pem",
}
tlsConfig, err := tlsInfo.ClientConfig()
if err != nil {
    panic(err)
}
```

#### Cambio de `embed.Config.SnapCount` a `embed.Config.SnapshotCount` {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

Para mantener la coherencia con el nombre de la opción `etcd --snapshot-count`, el campo `embed.Config.SnapCount` fue renombrado a `embed.Config.SnapshotCount`:

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### Cambio de `etcdserver.ServerConfig.SnapCount` a `etcdserver.ServerConfig.SnapshotCount` {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

Para mantener la coherencia con el nombre de la opción `etcd --snapshot-count`, el campo `etcdserver.ServerConfig.SnapCount` fue renombrado a `etcdserver.ServerConfig.SnapshotCount`:

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### Cambio de firmas de funciones en el paquete `wal` {#changed-function-signature-in-package-wal}

Se cambiaron las firmas de las funciones de `wal` para admitir el registro estructurado.

```diff
import "github.com/coreos/etcd/wal"
+import "go.uber.org/zap"

+lg, _ = zap.NewProduction()

-wal.Open(dirpath, snap)
+wal.Open(lg, dirpath, snap)

-wal.OpenForRead(dirpath, snap)
+wal.OpenForRead(lg, dirpath, snap)

-wal.Repair(dirpath)
+wal.Repair(lg, dirpath)

-wal.Create(dirpath, metadata)
+wal.Create(lg, dirpath, metadata)
```

#### Cambio del tipo `IntervalTree` en el paquete `pkg/adt` {#changed-intervaltree-type-in-package-pkgadt}

`pkg/adt.IntervalTree` ahora se define como una interfaz (`interface`).

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### Deprecación de `embed.Config.SetupLogging` {#deprecated-embedconfigsetuplogging}

`embed.Config.SetupLogging` se ha eliminado para evitar configuraciones de registro incorrectas, y ahora se configura automáticamente.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### Cambio en los endpoints HTTP de la pasarela gRPC (`/v3beta` reemplazado por `/v3`) {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

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

Las solicitudes a los endpoints `/v3beta` se redirigirán a `/v3`, y `/v3beta` se eliminará en la versión 3.5.

#### Deprecación de las etiquetas de imagen de contenedor {#deprecated-container-image-tags}

Las etiquetas de imagen `latest` y de versión menor están obsoletas:

```diff
-docker pull gcr.io/etcd-development/etcd:latest
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.0

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.1

-docker pull gcr.io/etcd-development/etcd:v3.4
+docker pull gcr.io/etcd-development/etcd:v3.4.2
```

### Listas de verificación para la actualización del servidor {#server-upgrade-checklists}

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue de etcd existente a 3.4, el clúster en ejecución debe ser 3.3 o superior. Si es anterior a 3.3, [actualiza primero a 3.3](/es/etcd/upgrades/upgrade_3_3/) antes de actualizar a 3.4.

Además, para garantizar una actualización progresiva sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre los servicios que dependen de etcd en un entorno de ensayo antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [degradar](#downgrade) a la versión existente de etcd. Ten en cuenta que el comando `snapshot` solo hace copia de seguridad de los datos v3. Para los datos v2, consulta [copia de seguridad del almacén de datos v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster de etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión 3.4. Internamente, los miembros de etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

Nota: Si el clúster solo tiene datos v3 y ningún dato v2, no está sujeto a esta limitación.

Si el clúster está sirviendo un conjunto de datos v2 de más de 50MB, cada miembro recién actualizado puede tardar hasta dos minutos en ponerse al día con el clúster existente. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. En otras palabras, lo más seguro es esperar 2 minutos entre la actualización de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único podría tardar aún más tiempo. Los administradores de clústeres etcd muy grandes de esta magnitud pueden contactar sin compromiso al [equipo de etcd][etcd-contact] antes de actualizar, y con gusto les proporcionaremos consejos sobre el procedimiento.

#### Degradación {#downgrade}

Si todos los miembros se han actualizado a v3.4, el clúster se actualizará a v3.4 y la degradación desde este estado completado **no es posible**. Sin embargo, si algún miembro individual sigue en v3.3, el clúster y sus operaciones permanecen en «v3.3» y, desde este estado de clúster mixto, es posible volver a usar un binario etcd v3.3 en todos los miembros.

[Descarga la copia de seguridad de la instantánea](/es/etcd/op-guide/maintenance/#snapshot-backup) para que sea posible degradar el clúster incluso después de que se haya actualizado por completo.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.3 de 3 miembros que se ejecuta en una máquina local.

#### Paso 1: comprobar los requisitos de actualización {#step-1-check-upgrade-requirements}

¿El clúster está en buen estado y ejecuta v3.3.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.3.5","etcdcluster":"3.3.0"}
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
10.237579 I | etcdserver: updating the cluster version from 3.0 to 3.3
10.238315 N | etcdserver/membership: updated the cluster version from 3.0 to 3.3
10.238451 I | etcdserver/api: enabled capabilities for version 3.3


^C21.192174 N | pkg/osutil: received interrupt signal, shutting down...
21.192459 I | etcdserver: 7339c4e5e833c029 starts leadership transfer from 7339c4e5e833c029 to 729934363faa4a24
21.192569 I | raft: 7339c4e5e833c029 [term 8] starts to transfer leadership to 729934363faa4a24
21.192619 I | raft: 7339c4e5e833c029 sends MsgTimeoutNow to 729934363faa4a24 immediately as 729934363faa4a24 already has up-to-date log
WARNING: 2018/05/17 12:45:21 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 0  <nil>}
WARNING: 2018/05/17 12:45:21 grpc: addrConn.transportMonitor exits due to: grpc: the connection is closing
21.193589 I | raft: 7339c4e5e833c029 [term: 8] received a MsgVote message with higher term from 729934363faa4a24 [term: 9]
21.193626 I | raft: 7339c4e5e833c029 became follower at term 9
21.193651 I | raft: 7339c4e5e833c029 [logterm: 8, index: 9, vote: 0] cast MsgVote for 729934363faa4a24 [logterm: 8, index: 9] at term 9
21.193675 I | raft: raft.node: 7339c4e5e833c029 lost leader 7339c4e5e833c029 at term 9
21.194424 I | raft: raft.node: 7339c4e5e833c029 elected leader 729934363faa4a24 at term 9
21.292898 I | etcdserver: 7339c4e5e833c029 finished leadership transfer from 7339c4e5e833c029 to 729934363faa4a24 (took 100.436391ms)
21.292975 I | rafthttp: stopping peer 729934363faa4a24...
21.293206 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 writer)
21.293225 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293437 I | rafthttp: closed the TCP streaming connection with peer 729934363faa4a24 (stream Message writer)
21.293459 I | rafthttp: stopped streaming with peer 729934363faa4a24 (writer)
21.293514 I | rafthttp: stopped HTTP pipelining with peer 729934363faa4a24
21.293590 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293610 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream MsgApp v2 reader)
21.293680 W | rafthttp: lost the TCP streaming connection with peer 729934363faa4a24 (stream Message reader)
21.293700 I | rafthttp: stopped streaming with peer 729934363faa4a24 (stream Message reader)
21.293711 I | rafthttp: stopped peer 729934363faa4a24
21.293720 I | rafthttp: stopping peer b548c2511513015...
21.293987 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 writer)
21.294063 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294467 I | rafthttp: closed the TCP streaming connection with peer b548c2511513015 (stream Message writer)
21.294561 I | rafthttp: stopped streaming with peer b548c2511513015 (writer)
21.294742 I | rafthttp: stopped HTTP pipelining with peer b548c2511513015
21.294867 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream MsgApp v2 reader)
21.294892 I | rafthttp: stopped streaming with peer b548c2511513015 (stream MsgApp v2 reader)
21.294990 W | rafthttp: lost the TCP streaming connection with peer b548c2511513015 (stream Message reader)
21.295004 E | rafthttp: failed to read b548c2511513015 on stream Message (context canceled)
21.295013 I | rafthttp: peer b548c2511513015 became inactive
21.295024 I | rafthttp: stopped streaming with peer b548c2511513015 (stream Message reader)
21.295035 I | rafthttp: stopped peer b548c2511513015
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
+ --initial-cluster-state new \
+ --logger zap \
+ --log-outputs stderr
```

El nuevo etcd v3.4 publicará su información en el clúster. En este punto, el clúster sigue operando con el protocolo v3.3, que es la versión común más baja.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Verifica que cada miembro, y luego el clúster completo, quede en buen estado con el nuevo binario etcd v3.4:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Los miembros no actualizados registrarán advertencias como la siguiente hasta que todo el clúster se haya actualizado.

Esto es esperado y cesará después de que todos los miembros del clúster etcd se hayan actualizado a v3.4:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### Paso 5: repetir el *paso 3* y el *paso 4* para el resto de los miembros {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Cuando todos los miembros estén actualizados, el clúster informará que la actualización a 3.4 se realizó correctamente:

Miembro 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

Miembro 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

Miembro 3:

> `{"level":"info","ts":1526586949.0921423,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"b548c2511513015","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0922918,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`


```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
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

[etcd-contact]: https://groups.google.com/g/etcd-dev
