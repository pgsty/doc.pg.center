---
title: Обновление etcd с 3.2 до 3.3
weight: 6750
description: Процессы, контрольные списки и примечания по обновлению etcd с 3.2 до 3.3
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_3.md"
aliases: [/etcd/upgrades/upgrade_3_3/]
---

В общем случае переход с etcd 3.2 на 3.3 можно выполнить как поэтапное обновление без простоя:
 - поочерёдно останавливать процессы etcd v3.2 и заменять их процессами etcd v3.3
 - после запуска всех процессов v3.3 кластеру становятся доступны новые возможности v3.3

До [начала обновления](#upgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.

### Контрольные списки обновления {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается, если etcd восстанавливается из существующих снимков, но файл v3 `ETCD_DATA_DIR/member/snap/db` отсутствует. Это происходит, когда сервер был перенесён с v2 и ранее не содержал данных v3. Такое поведение также предотвращает случайную потерю данных v3, например если файл `db` перемещён. etcd требует, чтобы после миграции на v3 работа продолжалась только при наличии данных v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данных v3.

> [!WARNING]
> Если включена аутентификация и используются аренды с малым ttl, высока вероятность столкнуться с [проблемой](https://github.com/etcd-io/etcd/issues/11689), приводящей к несогласованности данных. Настоятельно рекомендуется сначала обновиться до 3.2.31+ для её устранения, а затем до 3.3. Кроме того, если во время обновления пользователь без разрешения отправит запрос `LeaseRevoke` узлу 3.3, данные всё ещё могут быть повреждены. Перед обновлением лучше убедиться, что в окружении нет таких аномальных вызовов; подробнее см. [#11691](https://github.com/etcd-io/etcd/pull/11691).


Основные нарушающие совместимость изменения в 3.3.

#### Изменение типа значения флага `etcd --auto-compaction-retention` на `string` {#changed-value-type-of-etcd---auto-compaction-retention-flag-to-string}

Флаг `--auto-compaction-retention` изменён так, чтобы [принимать строковые значения](https://github.com/etcd-io/etcd/pull/8563) с [более высокой точностью](https://github.com/etcd-io/etcd/issues/8503). Поскольку теперь `--auto-compaction-retention` принимает строки, тип поля `auto-compaction-retention` в файле конфигурации YAML etcd необходимо изменить на `string`. Ранее `--config-file etcd.config.yaml` мог содержать `auto-compaction-retention: 24`, теперь требуется `auto-compaction-retention: "24"` или `auto-compaction-retention: "24h"`. При конфигурации `--auto-compaction-mode periodic --auto-compaction-retention "24h"` значение длительности флага `--auto-compaction-retention` должно быть допустимо для функции Go [`time.ParseDuration`](https://golang.org/pkg/time/#ParseDuration).

```diff
# etcd.config.yaml
+auto-compaction-mode: periodic
-auto-compaction-retention: 24
+auto-compaction-retention: "24"
+# Or
+auto-compaction-retention: "24h"
```

#### Изменение `*etcdserver.ServerConfig` на `etcdserver.ServerConfig` {#changed-etcdserveretcdserverserverconfig-to-etcdserveretcdserverserverconfig}

В `etcdserver.EtcdServer` тип поля участника изменён с `*etcdserver.ServerConfig` на `etcdserver.ServerConfig`. Кроме того, `etcdserver.NewServer` теперь принимает `etcdserver.ServerConfig` вместо `*etcdserver.ServerConfig`.

До и после (например, [k8s.io/kubernetes/test/e2e_node/services/etcd.go](https://github.com/kubernetes/kubernetes/blob/release-1.8/test/e2e_node/services/etcd.go#L50-L55))

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

#### Добавление поля `embed.Config.LogOutput` {#added-embedconfiglogoutput-struct}

> [!WARNING]
> Обратите внимание: в v3.4 поле переименовано в `embed.Config.LogOutputs` с типом `[]string`. Подробнее см. [руководство по обновлению до v3.4](/ru/docs/etcd/upgrades/upgrade_3_4/).

В `embed.Config` добавлено поле `LogOutput`:

```diff
package embed

type Config struct {
 	Debug bool `json:"debug"`
 	LogPkgLevels string `json:"log-package-levels"`
+	LogOutput string `json:"log-output"`
 	...
```

Ранее предупреждения сервера gRPC записывались в журнал etcdserver.

```
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
WARNING: 2017/11/02 11:35:51 grpc: addrConn.resetTransport failed to create client transport: connection error: desc = "transport: Error while dialing dial tcp: operation was canceled"; Reconnecting to {localhost:2379 <nil>}
```

Начиная с v3.3 журналы сервера gRPC по умолчанию отключены.

> [!WARNING]
> Обратите внимание: метод `embed.Config.SetupLogging` объявлен устаревшим в v3.4. Подробнее см. [руководство по обновлению до v3.4](/ru/docs/etcd/upgrades/upgrade_3_4/).

```go
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
cfg.SetupLogging()
```

Чтобы включить журналы сервера gRPC, задайте полю `embed.Config.Debug` значение `true`.

#### Изменение ответа конечной точки `/health` {#changed-health-endpoint-response}

Ранее `[endpoint]:[client-port]/health` возвращала вручную сериализованное значение JSON. В 3.3 определена структура [`etcdhttp.Health`](https://pkg.go.dev/github.com/etcd-io/etcd/etcdserver/api/etcdhttp#Health).

Обратите внимание: в v3.3.0-rc.0, v3.3.0-rc.1 и v3.3.0-rc.2 структура `etcdhttp.Health` содержит поля `"health"` и `"errors"` логического типа. Для обратной совместимости тип поля `"health"` возвращён к `string`, а поле `"errors"` удалено. Дополнительные сведения о работоспособности будут предоставляться отдельными API.

```bash
$ curl http://localhost:2379/health
{"health":"true"}
```

#### Изменение конечных точек HTTP шлюза gRPC (`/v3alpha` заменена на `/v3beta`) {#changed-grpc-gateway-http-endpoints-replaced-v3alpha-with-v3beta}

До

```bash
curl -L http://localhost:2379/v3alpha/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

После

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Запросы к конечным точкам `/v3alpha` перенаправляются на `/v3beta`, а `/v3alpha` будет удалена в выпуске 3.4.

#### Изменение ограничений максимального размера запроса {#changed-maximum-request-size-limits}

В 3.3 можно настраивать ограничения размера запросов как на стороне сервера, так и **на стороне клиента**. В предыдущих версиях (v3.2.10, v3.2.11) размер клиентского ответа был ограничен 4 MiB.

Серверное ограничение запросов настраивается флагом `--max-request-bytes`:

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

Либо полем `embed.Config.MaxRequestBytes`:

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

**Если значение не указано, серверное ограничение по умолчанию равно 1.5 MiB**.

Клиентские ограничения запросов необходимо настраивать с учётом серверных.

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

**Если значения не указаны, клиентское ограничение отправки по умолчанию равно 2 MiB (1.5 MiB плюс служебные байты gRPC), а ограничение получения — `math.MaxInt32`**. Подробнее см. [документацию clientv3](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config).

#### Изменение сигнатур функций низкоуровневой оболочки клиента gRPC {#changed-raw-grpc-client-wrapper-function-signatures}

В 3.3 изменены сигнатуры функций оболочки клиента gRPC `clientv3`. Изменение необходимо для поддержки [пользовательского `grpc.CallOption` для ограничений размера сообщений](https://github.com/etcd-io/etcd/pull/9047).

До и после

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

#### Изменение типа ошибки API `Snapshot` в clientv3 {#changed-clientv3-snapshot-api-error-type}

Ранее API `Snapshot` clientv3 возвращал необработанную ошибку типа [`grpc/*status.statusError`]. В v3.3 такие ошибки преобразуются в соответствующие общедоступные типы для согласованности с другими API.

До

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

После

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

#### Изменение вывода команды `etcdctl lease timetolive` {#changed-etcdctl-lease-timetolive-command-output}

Ранее команда `lease timetolive LEASE_ID` для истёкшей аренды выводила `-1s` как оставшееся время. В 3.3 сообщения стали понятнее.

До


```bash
lease 2d8257079fa1bc0c granted with TTL(0s), remaining(-1s)
```

После

```bash
lease 2d8257079fa1bc0c already expired
```

#### Изменение импортов `golang.org/x/net/context` {#changed-golangorgxnetcontext-imports}

В `clientv3` пакет `golang.org/x/net/context` объявлен устаревшим. Если проект включает `golang.org/x/net/context` в другой код, например сгенерированный код Protocol Buffer etcd, и импортирует `github.com/coreos/etcd/clientv3`, для компиляции требуется Go 1.9+.

До

```go
import "golang.org/x/net/context"
cli.Put(context.Background(), "f", "v")
```

После

```go
import "context"
cli.Put(context.Background(), "f", "v")
```

#### Изменение зависимости gRPC {#changed-grpc-dependency}

Теперь 3.3 требует [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5`.

##### Устаревший `grpclog.Logger` {#deprecated-grpcloglogger}

`grpclog.Logger` объявлен устаревшим в пользу [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). Теперь `clientv3.Logger` — это `grpclog.LoggerV2`.

До

```go
import "github.com/coreos/etcd/clientv3"
clientv3.SetLogger(log.New(os.Stderr, "grpc: ", 0))
```

После

```go
import "github.com/coreos/etcd/clientv3"
import "google.golang.org/grpc/grpclog"
clientv3.SetLogger(grpclog.NewLoggerV2(os.Stderr, os.Stderr, os.Stderr))

// log.New above cannot be used (not implement grpclog.LoggerV2 interface)
```

##### Устаревший `grpc.ErrClientConnTimeout` {#deprecated-grpcerrclientconntimeout}

Ранее при истечении тайм-аута клиентского подключения возвращалась ошибка `grpc.ErrClientConnTimeout`. Вместо неё 3.3 возвращает `context.DeadlineExceeded` (см. [#8504](https://github.com/etcd-io/etcd/issues/8504)).

До

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

После

```go
_, err := clientv3.New(clientv3.Config{
    Endpoints:   []string{"http://254.0.0.1:12345"},
    DialTimeout: 2 * time.Second
})
if err == context.DeadlineExceeded {
	// handle errors
}
```

#### Изменение официального реестра контейнеров {#changed-official-container-registry}

Теперь etcd использует [`gcr.io/etcd-development/etcd`](https://gcr.io/etcd-development/etcd) как основной реестр контейнеров, а [`quay.io/coreos/etcd`](https://quay.io/coreos/etcd) — как дополнительный.

До

```bash
docker pull quay.io/coreos/etcd:v3.2.5
```

После

```bash
docker pull gcr.io/etcd-development/etcd:v3.3.0
```

### Обновления до >= v3.3.14 {#upgrades-to--v3314}

В [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) пришлось включить некоторые возможности 3.4, стараясь свести к минимуму различия реализаций клиентского балансировщика. Выпуск исправляет проблему ["kube-apiserver 1.13.x refuses to work when first etcd-server is not available" (kubernetes#72102)](https://github.com/kubernetes/kubernetes/issues/72102).

`grpc.ErrClientConnClosing` [объявлена устаревшей в gRPC >= 1.10](https://github.com/grpc/grpc-go/pull/1854).

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

[Новый клиентский балансировщик](/ru/docs/etcd/learning/design-client/) использует асинхронный разрешитель для передачи конечных точек функции подключения gRPC. Поэтому [v3.3.14](https://github.com/etcd-io/etcd/releases/tag/v3.3.14) или более поздней версии требуется параметр подключения `grpc.WithBlock`, чтобы дождаться установления нижележащего соединения.

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

Полный список изменений приведён в [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.3.md).

### Контрольные списки обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.3 работающий кластер должен иметь версию 3.2 или более позднюю. Если версия ниже 3.2, перед переходом на 3.3 [обновитесь до 3.2](/ru/docs/etcd/upgrades/upgrade_3_2/).

Кроме того, для плавного поэтапного обновления работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в промежуточном окружении, прежде чем развёртывать обновление в рабочем окружении.

До начала [создайте резервную копию данных etcd](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). Если при обновлении возникнет проблема, эту копию можно использовать для [понижения версии](#downgrade) до существующей версии etcd. Обратите внимание: команда `snapshot` сохраняет только данные v3. О данных v2 см. раздел [резервное копирование хранилища v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается обновлённым только после обновления всех участников до 3.3. Участники etcd согласуют между собой общую версию кластера, которая определяет сообщаемую версию и поддерживаемые возможности.

#### Ограничения {#limitations}

Примечание: это ограничение не относится к кластеру, содержащему только данные v3 и не содержащему данных v2.

Если кластер обслуживает набор данных v2 объёмом более 50MB, каждому только что обновлённому участнику может потребоваться до двух минут, чтобы догнать существующий кластер. Для оценки общего объёма данных проверьте размер недавнего снимка. Иными словами, безопаснее всего ждать 2 минуты между обновлениями участников.

При значительно большем общем объёме данных, 100MB или более, этот однократный процесс может занять ещё больше времени. Администраторы столь крупных кластеров etcd могут перед обновлением обратиться к [команде etcd][etcd-contact] за рекомендациями по процедуре.

#### Понижение версии {#downgrade}

После обновления всех участников до v3.3 кластер также переходит на v3.3, и понижение версии из этого завершённого состояния **невозможно**. Однако пока хотя бы один участник остаётся на v3.2, кластер и его операции имеют версию "v3.2", а из смешанного состояния можно вернуться к использованию двоичного файла etcd v3.2 на всех участниках.

[Создайте резервную копию каталога данных](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup) всех участников etcd, чтобы сохранить возможность понижения версии кластера даже после полного обновления.

### Процедура обновления {#upgrade-procedure}

В этом примере показано обновление работающего на локальной машине кластера etcd v3.2 из 3 участников.

#### 1. Проверка требований к обновлению {#1-check-upgrade-requirements}

Кластер исправен и использует v3.2.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.2.7","etcdcluster":"3.2.0"}
```

#### 2. Остановка существующего процесса etcd {#2-stop-the-existing-etcd-process}

При остановке каждого процесса etcd другие участники кластера записывают в журнал ожидаемые ошибки. Это нормально, поскольку соединение с участником кластера (временно) разорвано:

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

На этом этапе рекомендуется [создать резервную копию данных etcd](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup), чтобы сохранить возможность понижения версии при возникновении проблем:

```
$ etcdctl snapshot save backup.db
```

#### 3. Установка двоичного файла etcd v3.3 и запуск нового процесса etcd {#3-drop-in-etcd-v33-binary-and-start-the-new-etcd-process}

Новый etcd v3.3 опубликует свои сведения в кластере:

```
14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с новым двоичным файлом etcd v3.3:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

До обновления всего кластера обновлённые участники будут записывать в журнал подобные предупреждения. Это ожидаемо и прекратится после обновления всех участников кластера etcd до v3.3:

```
14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
14:15:21.073110 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.3.0
14:15:21.073157 W | etcdserver: the local etcd version 3.2.7 is not up-to-date
14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.3.0
```

#### 4. Повторение шагов 2–3 для остальных участников {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Завершение {#5-finish}

После обновления всех участников кластер сообщит об успешном переходе на 3.3:

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
