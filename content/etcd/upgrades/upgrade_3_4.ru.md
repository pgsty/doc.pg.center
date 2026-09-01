---
title: Обновление etcd с 3.3 до 3.4
weight: 6700
description: Процессы, контрольные списки и примечания по обновлению etcd с 3.3 до 3.4
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_4.md"
---

В общем случае переход с etcd 3.3 на 3.4 можно выполнить как скользящее обновление без простоя:
 - поочерёдно останавливать процессы etcd v3.3 и заменять их процессами etcd v3.4
 - после запуска всех процессов v3.4 кластеру становятся доступны новые возможности v3.4

До [начала обновления](#upgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.



### Контрольные списки обновления {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается, если etcd восстанавливается из существующих снимков, но файл v3 `ETCD_DATA_DIR/member/snap/db` отсутствует. Это происходит, когда сервер был перенесён с v2 и ранее не содержал данных v3. Такое поведение также предотвращает случайную потерю данных v3 (например, если файл `db` перемещён). etcd требует, чтобы после миграции на v3 работа продолжалась только при наличии данных v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данные v3.

Основные нарушающие совместимость изменения в 3.4.

#### Использование `ETCDCTL_API=3 etcdctl` по умолчанию {#make-etcdctl_api3-etcdctl-default}

Теперь `ETCDCTL_API=3` используется по умолчанию.

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

#### Использование `etcd --enable-v2=false` по умолчанию {#make-etcd---enable-v2false-default}

Теперь [`etcd --enable-v2=false`](https://github.com/etcd-io/etcd/pull/10935) используется по умолчанию.

Это означает, что без явного `etcd --enable-v2=true` сервер etcd v3.4 не обслуживает запросы API v2.

Если использовался API v2, обязательно включите API v2 в v3.4:

```diff
-etcd
+etcd --enable-v2=true
```

Остальные API HTTP продолжат работать (например, `[CLIENT-URL]/metrics`, `[CLIENT-URL]/health` и шлюз gRPC v3).

#### Устаревшие флаги `etcd --ca-file` и `etcd --peer-ca-file` {#deprecated-etcd---ca-file-and-etcd---peer-ca-file-flags}

Флаги `--ca-file` и `--peer-ca-file` устарели; они объявлены устаревшими начиная с v2.1.

Обратите внимание: задание этого параметра автоматически включает аутентификацию по клиентскому сертификату независимо от значения `--client-cert-auth`.

```diff
-etcd --ca-file ca-client.crt
+etcd --trusted-ca-file ca-client.crt
```

```diff
-etcd --peer-ca-file ca-peer.crt
+etcd --peer-trusted-ca-file ca-peer.crt
```

#### Устаревшая ошибка `grpc.ErrClientConnClosing` {#deprecated-grpcerrclientconnclosing-error}

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

#### Требование `grpc.WithBlock` для клиентского подключения {#require-grpcwithblock-for-client-dial}

[Новый клиентский балансировщик](/ru/etcd/learning/design-client/) использует асинхронный разрешитель для передачи конечных точек функции подключения gRPC. Поэтому клиенту v3.4 требуется параметр подключения `grpc.WithBlock`, чтобы дождаться установления нижележащего соединения.

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

#### Объявление метрики Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` устаревшей {#deprecating-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.4 метрика Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` переведена в `etcd_mvcc_db_total_size_in_bytes`.

Для обратной совместимости `etcd_debugging_mvcc_db_total_size_in_bytes` всё ещё предоставляется в v3.4. В v3.5 она будет полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Объявление метрики Prometheus `etcd_debugging_mvcc_put_total` устаревшей {#deprecating-etcd_debugging_mvcc_put_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.4 метрика Prometheus `etcd_debugging_mvcc_put_total` переведена в `etcd_mvcc_put_total`.

Для обратной совместимости `etcd_debugging_mvcc_put_total` всё ещё предоставляется в v3.4. В v3.5 она будет полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Объявление метрики Prometheus `etcd_debugging_mvcc_delete_total` устаревшей {#deprecating-etcd_debugging_mvcc_delete_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.4 метрика Prometheus `etcd_debugging_mvcc_delete_total` переведена в `etcd_mvcc_delete_total`.

Для обратной совместимости `etcd_debugging_mvcc_delete_total` всё ещё предоставляется в v3.4. В v3.5 она будет полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Объявление метрики Prometheus `etcd_debugging_mvcc_txn_total` устаревшей {#deprecating-etcd_debugging_mvcc_txn_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.4 метрика Prometheus `etcd_debugging_mvcc_txn_total` переведена в `etcd_mvcc_txn_total`.

Для обратной совместимости `etcd_debugging_mvcc_txn_total` всё ещё предоставляется в v3.4. В v3.5 она будет полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Объявление метрики Prometheus `etcd_debugging_mvcc_range_total` устаревшей {#deprecating-etcd_debugging_mvcc_range_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.4 метрика Prometheus `etcd_debugging_mvcc_range_total` переведена в `etcd_mvcc_range_total`.

Для обратной совместимости `etcd_debugging_mvcc_range_total` всё ещё предоставляется в v3.4. В v3.5 она будет полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Объявление флага `etcd --log-output` устаревшим (теперь `--log-outputs`) {#deprecating-etcd---log-output-flag-now---log-outputs}

Для поддержки нескольких направлений вывода журнала [`etcd --log-output` переименован в `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624). **`etcd --logger=capnslog` не поддерживает несколько направлений вывода.**

**`etcd --log-output`** будет объявлен устаревшим в v3.5. **`etcd --logger=capnslog` будет объявлен устаревшим в v3.5**.

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+# only "--logger=zap" supports multiple writers
+etcd --logger=zap --log-outputs=stderr,a.log
```

В v3.4 добавлена поддержка `etcd --logger=zap --log-outputs=stderr` для структурированного ведения журнала и нескольких направлений вывода. Основная цель — содействовать автоматизированному мониторингу etcd вместо просмотра серверных журналов уже после начала сбоя. В дальнейшем etcd будет записывать как можно меньше сообщений, а его мониторинг с помощью метрик и оповещений станет проще. **`etcd --logger=capnslog` будет объявлен устаревшим в v3.5**.

#### Изменение типа поля `log-outputs` в `etcd --config-file` на `[]string` {#changed-log-outputs-field-type-in-etcd---config-file-to-string}

Поскольку `log-outputs` (прежнее имя поля — `log-output`) теперь принимает несколько получателей, тип поля `log-outputs` в файле конфигурации YAML etcd необходимо изменить на `[]string`, как показано ниже:

```diff
 # Specify 'stdout' or 'stderr' to skip journald logging even when running under systemd.
-log-output: default
+log-outputs: [default]
```

#### Переименование `embed.Config.LogOutput` в `embed.Config.LogOutputs` {#renamed-embedconfiglogoutput-to-embedconfiglogoutputs}

Для поддержки нескольких направлений вывода [**`embed.Config.LogOutput`** переименован в **`embed.Config.LogOutputs`**](https://github.com/etcd-io/etcd/pull/9624), а [тип `embed.Config.LogOutput` изменён с `string` на `[]string`](https://github.com/etcd-io/etcd/pull/9579).

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.LogOutput = "stderr"
+cfg.LogOutputs = []string{"stderr"}
```

#### В v3.5 `capnslog` объявляется устаревшим {#v35-deprecates-capnslog}

**В v3.5 флаг `etcd --log-package-levels` для `capnslog` будет объявлен устаревшим**; по умолчанию будет использоваться `etcd --logger=zap --log-outputs=stderr`. **В v3.5 конечная точка `[CLIENT-URL]/config/local/log` будет объявлена устаревшей.**

```diff
-etcd
+etcd --logger zap
```

#### Объявление флага `etcd --debug` устаревшим (теперь `--log-level=debug`) {#deprecating-etcd---debug-flag-now---log-leveldebug}

В v3.4 флаг [`etcd --debug`](https://github.com/etcd-io/etcd/pull/10947) объявлен устаревшим. Вместо него используйте `etcd --log-level=debug`.

```diff
-etcd --debug
+etcd --logger zap --log-level debug
```

#### Устаревшее поле `pkg/transport.TLSInfo.CAFile` {#deprecated-pkgtransporttlsinfocafile-field}

Поле `pkg/transport.TLSInfo.CAFile` объявлено устаревшим.

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

#### Изменение `embed.Config.SnapCount` на `embed.Config.SnapshotCount` {#changed-embedconfigsnapcount-to-embedconfigsnapshotcount}

Для согласованности с именем флага `etcd --snapshot-count` поле `embed.Config.SnapCount` переименовано в `embed.Config.SnapshotCount`:

```diff
import "github.com/coreos/etcd/embed"

cfg := embed.NewConfig()
-cfg.SnapCount = 100000
+cfg.SnapshotCount = 100000
```

#### Изменение `etcdserver.ServerConfig.SnapCount` на `etcdserver.ServerConfig.SnapshotCount` {#changed-etcdserverserverconfigsnapcount-to-etcdserverserverconfigsnapshotcount}

Для согласованности с именем флага `etcd --snapshot-count` поле `etcdserver.ServerConfig.SnapCount` переименовано в `etcdserver.ServerConfig.SnapshotCount`:

```diff
import "github.com/coreos/etcd/etcdserver"

srvcfg := etcdserver.ServerConfig{
-  SnapCount: 100000,
+  SnapshotCount: 100000,
```

#### Изменение сигнатур функций в пакете `wal` {#changed-function-signature-in-package-wal}

Сигнатуры функций `wal` изменены для поддержки структурированного средства ведения журнала.

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

#### Изменение типа `IntervalTree` в пакете `pkg/adt` {#changed-intervaltree-type-in-package-pkgadt}

Теперь `pkg/adt.IntervalTree` определён как `interface`.

```diff
import (
    "fmt"

    "go.etcd.io/etcd/pkg/adt"
)

func main() {
-    ivt := &adt.IntervalTree{}
+    ivt := adt.NewIntervalTree()
```

#### Устаревший `embed.Config.SetupLogging` {#deprecated-embedconfigsetuplogging}

`embed.Config.SetupLogging` удалён для предотвращения неверной конфигурации журналирования; теперь она настраивается автоматически.

```diff
import "github.com/coreos/etcd/embed"

cfg := &embed.Config{Debug: false}
-cfg.SetupLogging()
```

#### Изменённые конечные точки HTTP шлюза gRPC (`/v3beta` заменена на `/v3`) {#changed-grpc-gateway-http-endpoints-replaced-v3beta-with-v3}

До

```bash
curl -L http://localhost:2379/v3beta/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

После

```bash
curl -L http://localhost:2379/v3/kv/put \
  -X POST -d '{"key": "Zm9v", "value": "YmFy"}'
```

Запросы к конечным точкам `/v3beta` перенаправляются на `/v3`, а `/v3beta` будет удалена в выпуске 3.5.

#### Устаревшие теги образов контейнеров {#deprecated-container-image-tags}

Теги образов `latest` и дополнительной версии объявлены устаревшими:

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

### Контрольные списки обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.4 работающий кластер должен иметь версию 3.3 или более позднюю. Если версия старше 3.3, перед переходом на 3.4 [обновитесь до 3.3](/ru/etcd/upgrades/upgrade_3_3/).

Кроме того, для плавного скользящего обновления работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в промежуточном окружении, прежде чем развёртывать обновление в рабочем окружении.

До начала [загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup). Если при обновлении возникнет проблема, эту копию можно использовать для [понижения версии](#downgrade) до существующей версии etcd. Обратите внимание: команда `snapshot` сохраняет только данные v3. О данных v2 см. раздел [резервное копирование хранилища v2](https://etcd.io/docs/v2.3/admin_guide/#backing-up-the-datastore).

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается обновлённым только после обновления всех участников до 3.4. Участники etcd согласуют между собой общую версию кластера, которая определяет сообщаемую версию и поддерживаемые возможности.

#### Ограничения {#limitations}

Примечание: это ограничение не относится к кластеру, содержащему только данные v3 и не содержащему данные v2.

Если кластер обслуживает набор данных v2 объёмом более 50MB, каждому только что обновлённому участнику может потребоваться до двух минут, чтобы догнать существующий кластер. Для оценки общего объёма данных проверьте размер недавнего снимка. Иными словами, безопаснее всего ждать 2 минуты между обновлениями участников.

При значительно большем общем объёме данных, 100MB или более, этот однократный процесс может занять ещё больше времени. Администраторы столь крупных кластеров etcd могут перед обновлением обратиться к [команде etcd][etcd-contact] за рекомендациями по процедуре.

#### Понижение версии {#downgrade}

После обновления всех участников до v3.4 кластер также переходит на v3.4, и понижение версии из этого завершённого состояния **невозможно**. Однако пока хотя бы один участник остаётся на v3.3, кластер и его операции имеют версию "v3.3", а из смешанного состояния можно вернуться к использованию двоичного файла etcd v3.3 на всех участниках.

[Загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup), чтобы сохранить возможность понижения версии кластера даже после полного обновления.

### Процедура обновления {#upgrade-procedure}

В этом примере показано обновление работающего на локальной машине кластера etcd v3.3 из 3 участников.

#### Шаг 1: проверка требований к обновлению {#step-1-check-upgrade-requirements}

Кластер исправен и использует v3.3.x?

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

#### Шаг 2: загрузка резервной копии снимка с лидера {#step-2-download-snapshot-backup-from-leader}

[Загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup), чтобы обеспечить путь понижения версии при возникновении проблем.

Лидер etcd гарантированно содержит последние данные приложения, поэтому снимок следует получать с лидера:

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

#### Шаг 3: остановка одного существующего сервера etcd {#step-3-stop-one-existing-etcd-server}

При остановке каждого процесса etcd другие участники кластера записывают в журнал ожидаемые ошибки. Это нормально, поскольку соединение с участником кластера (временно) разорвано:

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

#### Шаг 4: перезапуск сервера etcd с той же конфигурацией {#step-4-restart-the-etcd-server-with-same-configuration}

Перезапустите сервер etcd с прежней конфигурацией, но с новым двоичным файлом etcd.

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

Новый etcd v3.4 опубликует свои сведения в кластере. На этом этапе кластер всё ещё работает по протоколу v3.3 — наименьшей общей версии.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.3"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.3"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с новым двоичным файлом etcd v3.4:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

До обновления всего кластера необновлённые участники будут записывать в журнал подобные предупреждения.

Это ожидаемо и прекратится после обновления всех участников кластера etcd до v3.4:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.4.0
:45.945154 W | etcdserver: the local etcd version 3.3.5 is not up-to-date
```

#### Шаг 5: повторение *шага 3* и *шага 4* для остальных участников {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

После обновления всех участников кластер сообщит об успешном переходе на 3.4:

Участник 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.4"}`

Участник 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.3","from":"3.4"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

Участник 3:

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
