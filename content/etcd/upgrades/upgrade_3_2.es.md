---
title: Actualizar etcd de la versión 3.1 a la 3.2
weight: 6800
description: Procesos, listas de verificación y notas sobre la actualización de etcd de la versión 3.1 a la 3.2
categories: [Tarea]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

En el caso general, actualizar de etcd 3.1 a 3.2 puede hacerse sin tiempo de inactividad, mediante una actualización gradual:
 - uno por uno, detén los procesos etcd v3.1 y reemplázalos por procesos etcd v3.2
 - tras ejecutar todos los procesos v3.2, las nuevas funcionalidades de v3.2 están disponibles para el clúster

Antes de [iniciar una actualización](#upgrade-procedure), lee el resto de esta guía para prepararte.

### Listas de verificación para la actualización {#upgrade-checklists}

> [!WARNING]
> Al [migrar desde v2 sin datos v3](https://github.com/etcd-io/etcd/issues/9480), el servidor etcd v3.2+ entra en pánico cuando etcd restaura desde instantáneas existentes pero no existe un archivo v3 `ETCD_DATA_DIR/member/snap/db`. Esto ocurre cuando el servidor había migrado desde v2 sin datos v3 previos. Esto también evita la pérdida accidental de datos v3 (por ejemplo, el archivo `db` podría haberse movido). etcd exige que la operación posterior a la migración a v3 solo pueda realizarse con datos v3. No actualices a versiones v3 más recientes hasta que el servidor v3.0 contenga datos v3.

Cambios de ruptura destacados en 3.2.

#### Cambio del valor predeterminado de `snapshot-count` {#changed-default-snapshot-count-value}

Un valor más alto de `--snapshot-count` mantiene más entradas de Raft en memoria hasta la instantánea, lo que provoca un [uso de memoria más alto y recurrente](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). Como el líder retiene las últimas entradas de Raft durante más tiempo, una réplica lenta dispone de más tiempo para ponerse al día antes de la instantánea del líder. `--snapshot-count` es un compromiso entre un mayor uso de memoria y una mejor disponibilidad de las réplicas lentas.

Desde v3.2, el valor predeterminado de `--snapshot-count` [ha cambiado de 10,000 a 100,000](https://github.com/etcd-io/etcd/pull/7160).

#### Cambio en la dependencia gRPC (>=3.2.10) {#changed-grpc-dependency-3210}

3.2.10 o posterior ahora requiere [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5` (<=3.2.9 requiere `v1.2.1`).

##### `grpclog.Logger` obsoleto {#deprecated-grpcloglogger}

`grpclog.Logger` ha quedado obsoleto en favor de [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). `clientv3.Logger` es ahora `grpclog.LoggerV2`.

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

##### `grpc.ErrClientConnTimeout` obsoleto {#deprecated-grpcerrclientconntimeout}

Anteriormente, el error `grpc.ErrClientConnTimeout` se devolvía en los tiempos de espera de conexión del cliente. 3.2 en su lugar devuelve `context.DeadlineExceeded` (consulta [#8504](https://github.com/etcd-io/etcd/issues/8504)).

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

#### Cambio en los límites máximos de tamaño de las peticiones (>=3.2.10) {#changed-maximum-request-size-limits-3210}

3.2.10 y 3.2.11 permiten límites de tamaño de petición personalizados en el lado servidor. >=3.2.12 permite límites de tamaño de petición personalizados tanto para el servidor como para el **lado cliente**. En versiones anteriores (v3.2.10, v3.2.11), el tamaño de respuesta del cliente estaba limitado a solo 4 MiB.

Los límites de peticiones del lado servidor pueden configurarse con el flag `--max-request-bytes`:

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

**Si no se especifica, el límite del lado servidor es por defecto 1.5 MiB**.

Los límites de peticiones del lado cliente deben configurarse en función de los límites del lado servidor.

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

**Si no se especifica, el límite de envío del lado cliente es por defecto 2 MiB (1.5 MiB + bytes de sobrecarga de gRPC) y el límite de recepción `math.MaxInt32`**. Consulta el [godoc de clientv3](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config) para más detalles.

#### Cambio en los wrappers brutos del cliente gRPC {#changed-raw-grpc-client-wrappers}

3.2.12 o posterior cambia las firmas de las funciones del wrapper de cliente gRPC de `clientv3`. Este cambio era necesario para admitir [`grpc.CallOption` personalizados en los límites de tamaño de mensaje](https://github.com/etcd-io/etcd/pull/9047).

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

#### Cambio en la API `clientv3.Lease.TimeToLive` {#changed-clientv3leasetimetolive-api}

Anteriormente, la API `clientv3.Lease.TimeToLive` devolvía `lease.ErrLeaseNotFound` para un ID de concesión inexistente. 3.2 en su lugar devuelve TTL=-1 en su respuesta y ningún error (consulta [#7305](https://github.com/etcd-io/etcd/pull/7305)).

Antes

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

Después

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### Traslado de `clientv3.NewFromConfigFile` a `clientv3.yaml.NewConfig` {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

`clientv3.NewFromConfigFile` se ha trasladado a `yaml.NewConfig`.

Antes

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

Después

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### Cambio en `--listen-peer-urls` y `--listen-client-urls` {#change-in---listen-peer-urls-and---listen-client-urls}

3.2 ahora rechaza nombres de dominio para `--listen-peer-urls` y `--listen-client-urls` (3.1 solo mostraba avisos), ya que un nombre de dominio no es válido para el enlace a una interfaz de red. Asegúrate de que esas URLs tengan el formato correcto `scheme://IP:port`.

Consulta la [incidencia #6336](https://github.com/etcd-io/etcd/issues/6336) para más contexto.

### Listas de verificación para la actualización del servidor {#server-upgrade-checklists}

#### Requisitos de actualización {#upgrade-requirements}

Para actualizar un despliegue etcd existente a 3.2, el clúster en ejecución debe ser la versión 3.1 o superior. Si es anterior a 3.1, [actualiza primero a 3.1](/es/etcd/upgrades/upgrade_3_1) antes de actualizar a 3.2.

Además, para garantizar una actualización gradual sin contratiempos, el clúster en ejecución debe estar en buen estado. Comprueba el estado del clúster con el comando `etcdctl endpoint health` antes de continuar.

#### Preparación {#preparation}

Antes de actualizar etcd, prueba siempre en un entorno de preproducción los servicios que dependen de etcd antes de desplegar la actualización en el entorno de producción.

Antes de comenzar, [haz una copia de seguridad de los datos de etcd](/es/etcd/op-guide/maintenance#snapshot-backup). Si algo sale mal con la actualización, es posible usar esta copia de seguridad para [revertir la actualización](#downgrade) y volver a la versión de etcd existente. Ten en cuenta que el comando `snapshot` solo hace copia de seguridad de los datos v3. Para los datos v2, consulta [copia de seguridad del almacén de datos v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Versiones mixtas {#mixed-versions}

Durante la actualización, un clúster etcd admite versiones mixtas de miembros etcd y opera con el protocolo de la versión común más baja. El clúster solo se considera actualizado cuando todos sus miembros se han actualizado a la versión 3.2. Internamente, los miembros etcd negocian entre sí para determinar la versión global del clúster, que controla la versión notificada y las funcionalidades admitidas.

#### Limitaciones {#limitations}

Nota: Si el clúster solo tiene datos v3 y ningún dato v2, no está sujeto a esta limitación.

Si el clúster sirve un conjunto de datos v2 de más de 50MB, cada miembro recién actualizado puede tardar hasta dos minutos en ponerse al día con el clúster existente. Comprueba el tamaño de una instantánea reciente para estimar el tamaño total de los datos. Dicho de otro modo, lo más seguro es esperar 2 minutos entre la actualización de cada miembro.

Para un tamaño total de datos mucho mayor, de 100MB o más, este proceso único puede tardar aún más tiempo. Los administradores de clústeres etcd muy grandes de esta magnitud pueden contactar libremente con el [equipo de etcd][etcd-contact] antes de actualizar, y estaremos encantados de asesorar sobre el procedimiento.

#### Revertir la actualización {#downgrade}

Si todos los miembros se han actualizado a v3.2, el clúster quedará actualizado a v3.2, y revertir la actualización desde este estado completado **no es posible**. Sin embargo, si un solo miembro sigue en v3.1, el clúster y sus operaciones siguen siendo «v3.1», y desde este estado de clúster mixto es posible volver a utilizar un binario etcd v3.1 en todos los miembros.

Haz una [copia de seguridad del directorio de datos](/es/etcd/op-guide/maintenance#snapshot-backup) de todos los miembros etcd para que revertir el clúster a la versión anterior siga siendo posible incluso después de que se haya actualizado por completo.

### Procedimiento de actualización {#upgrade-procedure}

Este ejemplo muestra cómo actualizar un clúster etcd v3.1 de 3 miembros que se ejecuta en una máquina local.

#### 1. Comprueba los requisitos de actualización {#1-check-upgrade-requirements}

¿Está el clúster en buen estado y ejecutando la versión v3.1.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. Detén el proceso etcd existente {#2-stop-the-existing-etcd-process}

Cuando se detiene cada proceso etcd, los demás miembros del clúster registrarán errores predecibles. Esto es normal, ya que la conexión con un miembro del clúster se ha roto (temporalmente):

```
2017-04-27 14:13:31.491746 I | raft: c89feb932daef420 [term 3] received MsgTimeoutNow from 6d4f535bae3ab960 and starts an election to get leadership.
2017-04-27 14:13:31.491769 I | raft: c89feb932daef420 became candidate at term 4
2017-04-27 14:13:31.491788 I | raft: c89feb932daef420 received MsgVoteResp from c89feb932daef420 at term 4
2017-04-27 14:13:31.491797 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.491805 I | raft: c89feb932daef420 [logterm: 3, index: 9] sent MsgVote request to 9eda174c7df8a033 at term 4
2017-04-27 14:13:31.491815 I | raft: raft.node: c89feb932daef420 lost leader 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524084 I | raft: c89feb932daef420 received MsgVoteResp from 6d4f535bae3ab960 at term 4
2017-04-27 14:13:31.524108 I | raft: c89feb932daef420 [quorum:2] has received 2 MsgVoteResp votes and 0 vote rejections
2017-04-27 14:13:31.524123 I | raft: c89feb932daef420 became leader at term 4
2017-04-27 14:13:31.524136 I | raft: raft.node: c89feb932daef420 elected leader c89feb932daef420 at term 4
2017-04-27 14:13:31.592650 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream MsgApp v2 reader)
2017-04-27 14:13:31.592825 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message reader)
2017-04-27 14:13:31.693275 E | rafthttp: failed to dial 6d4f535bae3ab960 on stream Message (dial tcp [::1]:2380: getsockopt: connection refused)
2017-04-27 14:13:31.693289 I | rafthttp: peer 6d4f535bae3ab960 became inactive
2017-04-27 14:13:31.936678 W | rafthttp: lost the TCP streaming connection with peer 6d4f535bae3ab960 (stream Message writer)
```

En este punto es buena idea [hacer una copia de seguridad de los datos de etcd](/es/etcd/op-guide/maintenance#snapshot-backup) para disponer de una vía de retorno en caso de que surjan problemas:

```
$ etcdctl snapshot save backup.db
```

#### 3. Sustituye el binario por etcd v3.2 e inicia el nuevo proceso etcd {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

El nuevo etcd v3.2 publicará su información en el clúster:

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Comprueba que cada miembro, y después el clúster completo, queda en buen estado con el nuevo binario etcd v3.2:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Los miembros actualizados registrarán avisos como el siguiente hasta que todo el clúster esté actualizado. Esto es de esperar y cesará cuando todos los miembros del clúster etcd se hayan actualizado a v3.2:

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. Repite del paso 2 al paso 3 para todos los demás miembros {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Finalizar {#5-finish}

Cuando todos los miembros estén actualizados, el clúster notificará la actualización correcta a 3.2:

```
2017-04-27 14:15:54.536901 N | etcdserver/membership: updated the cluster version from 3.1 to 3.2
2017-04-27 14:15:54.537035 I | etcdserver/api: enabled capabilities for version 3.2
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.517902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
