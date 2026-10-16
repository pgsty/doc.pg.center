---
title: Actualizar etcd de 3.2 a 3.3
weight: 6750
description: Procesos, listas de verificación y notas sobre la actualización de etcd de 3.2 a 3.3
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
---

En el caso general, la actualización de etcd 3.2 a 3.3 puede realizarse sin tiempo de inactividad, mediante una actualización progresiva:
 - uno por uno, detén los procesos etcd v3.2 y reemplázalos por procesos etcd v3.3
 - después de ejecutar todos los procesos v3.3, las nuevas funcionalidades de v3.3 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la actualización {#upgrade-checklists}

> [!WARNING]
> Cuando se [migra desde v2 sin datos v3](https://github.com/etcd-io/etcd/issues/9480), el servidor etcd v3.2+ entra en pánico cuando etcd restaura a partir de instantáneas existentes pero no hay ningún archivo v3 `ETCD_DATA_DIR/member/snap/db`. Esto ocurre cuando el servidor se había migrado desde v2 sin datos v3 previos. Esto también evita la pérdida accidental de datos v3 (por ejemplo, el archivo `db` podría haberse movido). etcd exige que la migración posterior a v3 solo pueda realizarse con datos v3. No actualices a versiones v3 más recientes hasta que el servidor v3.0 contenga datos v3.

> [!WARNING]
> si habilitas la autenticación y utilizas concesiones (con un TTL de concesión pequeño), existe una alta probabilidad de encontrarse con este [problema](https://github.com/etcd-io/etcd/issues/11689), que provocará una inconsistencia de datos. Se recomienda encarecidamente actualizar primero a 3.2.31+ para corregir este problema y luego actualizar a 3.3. Además, si un usuario sin permisos envía una solicitud `LeaseRevoke` al nodo 3.3 durante el proceso de actualización, todavía puede provocar corrupción de datos, por lo que lo mejor es asegurarte de que tu entorno no contenga llamadas anómalas de este tipo antes de actualizar; consulta [#11691](https://github.com/etcd-io/etcd/pull/11691) para más detalles.


Cambios destacados que rompen la compatibilidad en 3.3.

#### Cambio del tipo de valor de la opción `etcd --auto-compaction-retention` a `string` {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

La opción `--auto-compaction-retention` se ha modificado para [aceptar valores de tipo cadena](https://github.com/etcd-io/etcd/pull/8563) con [una granularidad más fina](https://github.com/etcd-io/etcd/issues/8503). Ahora que `--auto-compaction-retention` acepta valores de tipo cadena, el campo `auto-compaction-retention` del archivo YAML de configuración de etcd debe cambiarse al tipo `string`. Anteriormente, `--config-file etcd.config.yaml` podía tener el campo `auto-compaction-retention: 24`; ahora debe ser `auto-compaction-retention: "24"` o `auto-compaction-retention: "24h"`. Si se configura como `--auto-compaction-mode periodic --auto-compaction-retention "24h"`, el valor de duración de tiempo de la opción `--auto-compaction-retention` debe ser válido para la función [`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration) de Go.

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### Cambio de `*etcdserver.ServerConfig` a `etcdserver.ServerConfig` {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

`etcdserver.EtcdServer` ha cambiado el tipo de su campo miembro `*etcdserver.ServerConfig` a `etcdserver.ServerConfig`. Y `etcdserver.NewServer` ahora recibe `etcdserver.ServerConfig`, en lugar de `*etcdserver.ServerConfig`.

Antes y después (por ejemplo, [k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55))

```diff
import "github.com/coreos/etcd/etcdserver"

type EtcdServer struct {
	*etcdserver.EtcdServer
-	config *etcdserver.ServerConfig
+	config etcdserver.ServerConfig
}

func NewEtcd(dataDir string) *EtcdServer {
-	config := &etcdserver.ServerConfig{
+	config := etcdserver.ServerConfig{
		DataDir: dataDir,
        ...
	}
	return &EtcdServer{config: config}
}

func (e *EtcdServer) Start() error {
	var err error
	e.EtcdServer, err = etcdserver.NewServer(e.config)
    ...
```

#### Adición del campo `embed.Config.LogOutput` {#added-embedconfiglogoutput-struct}

> [!WARNING]
> Ten en cuenta que este campo fue renombrado a `embed.Config.LogOutputs` con tipo `[]string` en v3.4. Consulta la [guía de actualización a v3.4](/es/etcd/upgrades/upgrade_3_4/) para más detalles.

El campo `LogOutput` se añade a `embed.Config`:

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

Anteriormente, las advertencias del servidor gRPC se registraban en etcdserver.

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

A partir de v3.3, los registros del servidor gRPC están deshabilitados de forma predeterminada.

> [!WARNING]
> Ten en cuenta que el método `embed.Config.SetupLogging` quedó obsoleto en v3.4. Consulta la [guía de actualización a v3.4](/es/etcd/upgrades/upgrade_3_4/) para más detalles.

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

Establece el campo `embed.Config.Debug` en `true` para habilitar los registros del servidor gRPC.

#### Cambio en la respuesta del endpoint `/health` {#changed-health-endpoint-response}

Anteriormente, `[endpoint]:[client-port]/health` devolvía un valor JSON serializado manualmente. 3.3 ahora define la estructura [`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health).

Ten en cuenta que en v3.3.0-rc.0, v3.3.0-rc.1 y v3.3.0-rc.2, `etcdhttp.Health` tenía campos `"health"` y `"errors"` de tipo booleano. Por compatibilidad con versiones anteriores, revertimos el campo `"health"` al tipo `string` y eliminamos el campo `"errors"`. La información adicional sobre el estado se proporcionará en API separadas.

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### Cambio en los endpoints HTTP de la pasarela gRPC (`/v3alpha` reemplazado por `/v3beta`) {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

Antes

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Después

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Las solicitudes a los endpoints `/v3alpha` se redirigirán a `/v3beta`, y `/v3alpha` se eliminará en la versión 3.4.

#### Cambio en los límites máximos de tamaño de las solicitudes {#changed-maximum-request-size-limits}

3.3 ahora permite límites de tamaño de solicitud personalizados tanto para el servidor como para el **lado del cliente**. En versiones anteriores (v3.2.10, v3.2.11), el tamaño de respuesta del cliente estaba limitado a solo 4 MiB.

Los límites de solicitudes del lado del servidor se pueden configurar con la opción `--max-request-bytes`:

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

O configura el campo `embed.Config.MaxRequestBytes`:

```go
import "github.com/coreos/etcd/embed"
import "github.com/coreos/etcd/etcdserver/api/v3rpc/rpctypes"

// limit requests to 5 MiB
cfg := embed.NewConfig()
cfg.MaxRequestBytes = 5 * 1024 * 1024

// client writes exceeding 5 MiB will be rejected
_, err := cli.Put(ctx, "foo", [LARGE VALUE...])
err == rpctypes.ErrRequestTooLarge
```

**Si no se especifica, el límite del lado del servidor se establece de forma predeterminada en 1.5 MiB**.

Los límites de solicitudes del lado del cliente deben configurarse en función de los límites del lado del servidor.

```bash
# limits request size to 1 MiB
etcd --max-request-bytes 1048576
```

```go
import "github.com/coreos/etcd/clientv3"

cli, _ := clientv3.New(clientv3.Config{
    Endpoints: []string{"127.0.0.1:2379"},
    MaxCallSendMsgSize: 2 * 1024 * 1024,
    MaxCallRecvMsgSize: 3 * 1024 * 1024,
})


// client writes exceeding "--max-request-bytes" will be rejected from etcd server
_, err := cli.Put(ctx, "foo", strings.Repeat("a", 1*1024*1024+5))
err == rpctypes.ErrRequestTooLarge


// client writes exceeding "MaxCallSendMsgSize" will be rejected from client-side
_, err = cli.Put(ctx, "foo", strings.Repeat("a", 5*1024*1024))
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: trying to send message larger than max (5242890 vs. 2097152)"


// some writes under limits
for i := range []int{0,1,2,3,4} {
    _, err = cli.Put(ctx, fmt.Sprintf("foo%d", i), strings.Repeat("a", 1*1024*1024-500))
    if err != nil {
        panic(err)
    }
}
// client reads exceeding "MaxCallRecvMsgSize" will be rejected from client-side
_, err = cli.Get(ctx, "foo", clientv3.WithPrefix())
err.Error() == "rpc error: code = ResourceExhausted desc = grpc: received message larger than max (5240509 vs. 3145728)"
```

**Si no se especifica, el límite de envío del lado del cliente se establece de forma predeterminada en 2 MiB (1.5 MiB + bytes de sobrecarga de gRPC) y el límite de recepción en `math.MaxInt32`**. Consulta el [godoc de clientv3](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config) para más detalles.

#### Cambio en las firmas de las funciones envolventes del cliente gRPC sin procesar {#changed-raw-grpc-client-wrapper-function-signatures}

3.3 cambia las firmas de las funciones del wrapper del cliente gRPC de `clientv3`. Este cambio era necesario para admitir [`grpc.CallOption` personalizadas en los límites de tamaño de mensaje](https://github.com/etcd-io/etcd/pull/9047).

Antes y después

```diff
-func NewKVFromKVClient(remote pb.KVClient) KV {
+func NewKVFromKVClient(remote pb.KVClient, c *Client) KV {

-func NewClusterFromClusterClient(remote pb.ClusterClient) Cluster {
+func NewClusterFromClusterClient(remote pb.ClusterClient, c *Client) Cluster {

-func NewLeaseFromLeaseClient(remote pb.LeaseClient, keepAliveTimeout time.Duration) Lease {
+func NewLeaseFromLeaseClient(remote pb.LeaseClient, c *Client, keepAliveTimeout time.Duration) Lease {

-func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient) Maintenance {
+func NewMaintenanceFromMaintenanceClient(remote pb.MaintenanceClient, c *Client) Maintenance {

-func NewWatchFromWatchClient(wc pb.WatchClient) Watcher {
+func NewWatchFromWatchClient(wc pb.WatchClient, c *Client) Watcher {
```

#### Cambio del tipo de error de la API `Snapshot` de clientv3 {#changed-clientv3-snapshot-api-error-type}

Anteriormente, la API `Snapshot` de clientv3 devolvía un error de tipo [`grpc/*status.statusError`] sin procesar. v3.3 ahora traduce esos errores a los tipos de error públicos correspondientes, para mantener la coherencia con otras API.

Antes

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err.Error() == "rpc error: code = Canceled desc = context canceled"

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err.Error() == "rpc error: code = DeadlineExceeded desc = context deadline exceeded"
```

Después

```go
import "context"

// reading snapshot with canceled context should error out
ctx, cancel := context.WithCancel(context.Background())
rc, _ := cli.Snapshot(ctx)
cancel()
_, err := io.Copy(f, rc)
err == context.Canceled

// reading snapshot with deadline exceeded should error out
ctx, cancel = context.WithTimeout(context.Background(), time.Second)
defer cancel()
rc, _ = cli.Snapshot(ctx)
time.Sleep(2 * time.Second)
_, err = io.Copy(f, rc)
err == context.DeadlineExceeded
```

#### Cambio en la salida del comando `etcdctl lease timetolive` {#changed-etcdctl-lease-timetolive-command-output}

Anteriormente, el comando `lease timetolive LEASE_ID` sobre una concesión expirada mostraba `-1s` para los segundos restantes. 3.3 ahora muestra mensajes más claros.

Antes


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

Después

```bash
lease 2d8257079fa1bc0c already expired
```

#### Cambio en las importaciones de `golang.org/x/net/context` {#changed-golangorgxnetcontext-imports}

`clientv3` ha marcado `golang.org/x/net/context` como obsoleto. Si un proyecto incorpora `golang.org/x/net/context` en su directorio vendor para otra parte del código (p. ej., el código de protocol buffer generado por etcd) e importa `github.com/coreos/etcd/clientv3`, se requiere Go 1.9+ para compilar.

Antes

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

Después

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### Cambio en la dependencia gRPC {#changed-grpc-dependency}

3.3 ahora requiere [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5`.

##### Deprecación de `grpclog.Logger` {#deprecated-grpcloglogger}

`grpclog.Logger` ha quedado obsoleto en favor de [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). `clientv3.Logger` ahora es `grpclog.LoggerV2`.

Antes

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

Después

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### Deprecación de `grpc.ErrClientConnTimeout` {#deprecated-grpcerrclientconntimeout}

Anteriormente, el error `grpc.ErrClientConnTimeout` se devolvía al agotarse los tiempos de espera de conexión del cliente. 3.3 en su lugar devuelve `context.DeadlineExceeded` (consulta [#8504](https://github.com/etcd-io/etcd/issues/8504)).

Antes

```go
// expect dial time-out on ipv4 blackhole
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == grpc.ErrClientConnTimeout {
	// handle errors
}
```

Después

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### Cambio en el registro de contenedores oficial {#changed-official-container-registry}

etcd ahora utiliza [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) como registro de contenedores principal y [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) como secundario.

Antes

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

Después

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### Actualizaciones a >= v3.3.14 {#upgrades-to--v3314}

[v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) tuvo que incluir algunas funcionalidades de 3.4, al tiempo que se intentaba minimizar la diferencia entre las implementaciones del balanceador del cliente. Esta versión corrige el problema [«kube-apiserver 1.13.x se niega a funcionar cuando el primer etcd-server no está disponible» (kubernetes#72102)](https://github.com/kubernetes/kubernetes/issues/72102).

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

[El nuevo balanceador del cliente](/es/etcd/learning/design-client/) utiliza un resolutor asíncrono para pasar los endpoints a la función de conexión de gRPC. Como resultado, [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) o posterior requiere la opción de conexión `grpc.WithBlock` para esperar hasta que la conexión subyacente esté activa.

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

Consulta el [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md) para obtener la lista completa de cambios.

### Listas de verificación para la actualización del servidor {#server-upgrade-checklists}

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue de etcd existente a 3.3, el clúster en ejecución debe ser 3.2 o superior. Si es anterior a 3.2, [actualiza primero a 3.2](/es/etcd/upgrades/upgrade_3_2/) antes de actualizar a 3.3.

Además, para garantizar una actualización progresiva sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre los servicios que dependen de etcd en un entorno de ensayo antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [realiza una copia de seguridad de los datos de etcd](/es/etcd/op-guide/maintenance/#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [degradar](#downgrade) a la versión existente de etcd. Ten en cuenta que el comando `snapshot` solo hace copia de seguridad de los datos v3. Para los datos v2, consulta [copia de seguridad del almacén de datos v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster de etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión 3.3. Internamente, los miembros de etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

Nota: Si el clúster solo tiene datos v3 y ningún dato v2, no está sujeto a esta limitación.

Si el clúster está sirviendo un conjunto de datos v2 de más de 50MB, cada miembro recién actualizado puede tardar hasta dos minutos en ponerse al día con el clúster existente. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. En otras palabras, lo más seguro es esperar 2 minutos entre la actualización de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único podría tardar aún más tiempo. Los administradores de clústeres etcd muy grandes de esta magnitud pueden contactar sin compromiso al [equipo de etcd][etcd-contact] antes de actualizar, y con gusto les proporcionaremos consejos sobre el procedimiento.

#### Degradación {#downgrade}

Si todos los miembros se han actualizado a v3.3, el clúster se actualizará a v3.3 y la degradación desde este estado completado **no es posible**. Sin embargo, si algún miembro individual sigue en v3.2, el clúster y sus operaciones permanecen en «v3.2» y, desde este estado de clúster mixto, es posible volver a usar un binario etcd v3.2 en todos los miembros.

Haz una [copia de seguridad del directorio de datos](/es/etcd/op-guide/maintenance/#snapshot-backup) de todos los miembros etcd para que sea posible degradar el clúster incluso después de que se haya actualizado por completo.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.2 de 3 miembros que se ejecuta en una máquina local.

#### 1. Comprobar los requisitos de actualización {#1-check-upgrade-requirements}

¿El clúster está en buen estado y ejecuta v3.2.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. Detener el proceso etcd existente {#2-stop-the-existing-etcd-process}

Cuando se detiene cada proceso etcd, otros miembros del clúster registrarán errores esperados. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente):

```
14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

En este punto es buena idea [hacer una copia de seguridad de los datos de etcd](/es/etcd/op-guide/maintenance/#snapshot-backup) para disponer de una ruta de degradación en caso de que surjan problemas:

```
$ etcdctl snapshot save backup.db
```

#### 3. Sustituir por el binario etcd v3.3 e iniciar el nuevo proceso etcd {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

El nuevo etcd v3.3 publicará su información en el clúster:

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Verifica que cada miembro, y luego el clúster completo, quede en buen estado con el nuevo binario etcd v3.3:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Los miembros actualizados registrarán advertencias como la siguiente hasta que todo el clúster se haya actualizado. Esto es esperado y cesará después de que todos los miembros del clúster etcd se hayan actualizado a v3.3:

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. Repetir los pasos 2 a 3 para todos los demás miembros {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Finalizar {#5-finish}

Cuando todos los miembros estén actualizados, el clúster informará que la actualización a 3.3 se realizó correctamente:

```
14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.2 to 3.3
14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.3
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
