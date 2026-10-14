---
title: Обновление etcd от 3.1 до 3.2
weight: 6800
description: "Процессы, списки действий и примечания по обновлению etcd с 3.1 до 3.2"
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
---

В общем случае переход с etcd 3.1 на 3.2 можно выполнить как поэтапное обновление без простоя:
 - поочерёдно останавливать процессы etcd v3.1 и заменять их процессами etcd v3.2
 - после запуска всех процессов v3.2 кластеру станут доступны новые возможности v3.2

Перед [обновлением](#upgrade-procedure) внимательно прочитайте оставшуюся часть этого руководства для подготовки.

### Контрольные списки обновления {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается при восстановлении из существующих снимков без файла v3 `ETCD_DATA_DIR/member/snap/db`. Это происходит, когда сервер был перенесён с v2 и ранее не содержал данных v3. Это также предотвращает случайную потерю данных v3 (например, файл `db` мог быть перемещён). etcd требует, чтобы миграция на более новые версии v3 выполнялась только при наличии данных v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данных v3.

Основные нарушающие совместимость изменения в 3.2.

#### Изменено стандартное значение `snapshot-count` {#changed-default-snapshot-count-value}

Большее значение `--snapshot-count` удерживает до снимка больше записей Raft
в памяти, вызывая [периодически повышенное потребление памяти](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156).
Лидер дольше хранит последние записи, и медленный последователь получает больше
времени догнать его до снимка. `--snapshot-count` — компромисс между памятью и
доступностью медленных последователей.

Начиная с v3.2 значение `--snapshot-count` по умолчанию [изменено с 10,000 на 100,000](https://github.com/etcd-io/etcd/pull/7160).

#### Изменена зависимость gRPC (>=3.2.10) {#changed-grpc-dependency-3210}

Выпуск 3.2.10 или более поздний теперь требует [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5` (<=3.2.9 требует `v1.2.1`).

##### Устаревший `grpclog.Logger` {#deprecated-grpcloglogger}

`grpclog.Logger` устарел в пользу [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). `clientv3.Logger` теперь `grpclog.LoggerV2`.

Перед

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

Ранее при истечении тайм-аута клиентского подключения возвращалась ошибка `grpc.ErrClientConnTimeout`. Вместо неё 3.2 возвращает `context.DeadlineExceeded` (см. [#8504](https://github.com/etcd-io/etcd/issues/8504)).

Перед

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

#### Изменены максимальные ограничения размера запроса (>=3.2.10) {#changed-maximum-request-size-limits-3210}

Версии 3.2.10 и 3.2.11 позволяют настраивать ограничение размера запроса на
сервере. >=3.2.12 позволяет задавать его и на сервере, и **на клиенте**. В
предыдущих версиях (v3.2.10, v3.2.11) ответ клиенту был ограничен 4 MiB.

Серверные ограничения на запросы можно настроить с помощью флага `--max-request-bytes`:

```bash
# limits request size to 1.5 KiB
etcd --max-request-bytes 1536

# client writes exceeding 1.5 KiB will be rejected
etcdctl put foo [LARGE VALUE...]
# etcdserver: request is too large
```

Или настройте поле `embed.Config.MaxRequestBytes`:

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

**Если значение не задано, серверное ограничение по умолчанию равно 1.5 MiB**.

Клиентские ограничения на запросы должны быть настроены в соответствии с серверными ограничениями.

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

**Если значения не заданы, клиентское ограничение отправки по умолчанию равно
2 MiB (1.5 MiB + накладные байты gRPC), а получения — `math.MaxInt32`**.
Подробнее см. [godoc clientv3](https://pkg.go.dev/github.com/etcd-io/etcd/clientv3#Config).

#### Изменены низкоуровневые (raw) оболочки клиента gRPC {#changed-raw-grpc-client-wrappers}

3.2.12 или более поздняя версия изменяет сигнатуры функций низкоуровневой (raw) оболочки gRPC клиента `clientv3`. Эти изменения были необходимы для поддержки пользовательских [`grpc.CallOption`](https://github.com/etcd-io/etcd/pull/9047) для ограничений размера сообщений.

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

#### Изменение API `clientv3.Lease.TimeToLive` {#changed-clientv3leasetimetolive-api}

Ранее API `clientv3.Lease.TimeToLive` возвращал ошибку `lease.ErrLeaseNotFound`, если указанный идентификатор аренды не существовал. Вместо неё 3.2 возвращает в ответе TTL=-1 и не выдаёт ошибку (см. [#7305](https://github.com/etcd-io/etcd/pull/7305)).

Перед

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp == nil
err == lease.ErrLeaseNotFound
```

После

```go
// when leaseID does not exist
resp, err := TimeToLive(ctx, leaseID)
resp.TTL == -1
err == nil
```

#### Перемещен `clientv3.NewFromConfigFile` в `clientv3.yaml.NewConfig` {#moved-clientv3newfromconfigfile-to-clientv3yamlnewconfig}

`clientv3.NewFromConfigFile` перенесен в `yaml.NewConfig`.

Перед

```go
import "github.com/coreos/etcd/clientv3"
clientv3.NewFromConfigFile
```

После

```go
import clientv3yaml "github.com/coreos/etcd/clientv3/yaml"
clientv3yaml.NewConfig
```

#### Изменение в `--listen-peer-urls` и `--listen-client-urls` {#change-in---listen-peer-urls-and---listen-client-urls}

3.2 теперь отвергает доменные имена для `--listen-peer-urls` и `--listen-client-urls` (3.1 только выводит предупреждения), так как доменное имя недопустимо для привязки к сетевому интерфейсу. Убедитесь, что эти URL правильно форматированы как `scheme://IP:port`.

См. [issue #6336](https://github.com/etcd-io/etcd/issues/6336) для более подробной информации.

### Контрольные списки обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.2 кластер должен быть версии 3.1 или выше. Если версия ниже 3.1, перед обновлением до 3.2 [обновитесь до 3.1](/ru/etcd/upgrades/upgrade_3_1).

Для плавного поэтапного обновления работающий кластер также должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в промежуточной среде, прежде чем развёртывать обновление в производственной среде.

Перед началом [сделайте резервную копию данных etcd](/ru/etcd/op-guide/maintenance#snapshot-backup). Если что-то пойдет не так с обновлением, можно использовать эту резервную копию для [понижения версии](#downgrade) обратно к существующей версии etcd. Обратите внимание: команда `snapshot` выполняет резервное копирование только данных v3. Для данных v2 см. [резервное копирование v2 хранилища данных](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Смешанные версии {#mixed-versions}

При обновлении кластер etcd поддерживает смешанные версии участников etcd и работает с протоколом самой низкой общей версии. Кластер считается обновленным только после того, как все его участники будут обновлены до версии 3.2. Участники etcd согласуют общую версию кластера, которая определяет сообщаемую версию и поддерживаемые возможности.

#### Ограничения {#limitations}

Примечание: это ограничение не относится к кластеру, содержащему только данные версии 3 без данных версии 2.

Если кластер обслуживает набор данных версии v2 размером более 50MB, каждому только что обновлённому участнику может потребоваться до двух минут, чтобы догнать существующий кластер. Проверьте размер последнего снимка, чтобы оценить общий размер данных. Иными словами, безопаснее всего ждать 2 минуты между обновлениями участников.

При значительно большем объёме данных, 100MB или более, этот одноразовый процесс может занять еще больше времени. Администраторы очень больших кластеров etcd такого масштаба могут обратиться к команде [etcd][etcd-contact] перед обновлением, и мы с удовольствием предоставим рекомендации по процедуре.

#### Понижение версии {#downgrade}

Если все участники были обновлены до v3.2, кластер будет обновлен до v3.2, и понижение версии из этого завершенного состояния **невозможно**. Если хотя бы один участник остается v3.1, кластер и его операции остаются "v3.1", и из этого смешанного состояния кластера возможно вернуться к использованию etcd-бинарного файла версии v3.1 на всех участниках.

Создайте [резервную копию каталога данных](/ru/etcd/op-guide/maintenance#snapshot-backup)
всех участников, чтобы понижение версии оставалось возможным после полного обновления.

### Процедура обновления {#upgrade-procedure}

Этот пример показывает, как обновить кластер etcd v3.1 из 3 участников, работающий на локальной машине.

#### 1. Проверьте требования к обновлению {#1-check-upgrade-requirements}

Исправен ли кластер и работает ли он на версии v3.1.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.1.7","etcdcluster":"3.1.0"}
```

#### 2. Остановите существующий процесс etcd {#2-stop-the-existing-etcd-process}

Когда процесс etcd останавливается, ожидаемые ошибки будут записаны другими участниками кластера. Это нормально, так как соединение участника было (временно) прервано:

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

На этом этапе рекомендуется создать [резервную копию данных etcd](/ru/etcd/op-guide/maintenance#snapshot-backup), чтобы обеспечить возможность понижения версии в случае возникновения любых проблем:

```
$ etcdctl snapshot save backup.db
```

#### 3. Замените двоичный файл etcd на v3.2 и запустите новый процесс etcd {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

Новый etcd v3.2 будет публиковать свои данные в кластер:

```
2017-04-27 14:14:25.363225 I | etcdserver: published {Name:s1 ClientURLs:[http://localhost:2379]} to cluster a9ededbffcb1b1f1
```

Убедитесь, что с новым двоичным файлом etcd v3.2 каждый участник, а затем весь кластер становятся исправными:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321771ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Обновленные участники будут регистрировать предупреждения следующего вида до тех пор, пока весь кластер не будет обновлен. Это ожидаемо и прекратится после того, как все участники кластера etcd будут обновлены до v3.2:

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. Повторите шаги 2–3 для остальных участников {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Завершите обновление {#5-finish}

Когда все участники будут обновлены, кластер будет сообщать об успешном переходе к 3.2:

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
