---
title: Обновление etcd от 3.1 до 3.2
weight: 6800
description: "Процессы, списки действий и примечания по обновлению etcd с 3.1 до 3.2"
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_2.md"
aliases: [/etcd/upgrades/upgrade_3_2/]
---

В общем случае, обновление от etcd 3.1 до 3.2 может быть обновлением с нулевым временем простоя:
- по одному, останавливайте процессы etcd v3.1 и заменяйте их процессами etcd v3.2
- после запуска всех процессов v3.2, новые функции в v3.2 становятся доступны для кластера

Перед [обновлением](#upgrade-procedure) внимательно прочитайте оставшуюся часть этого руководства для подготовки.

### Обновление списков проверки {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается при восстановлении из снимка без файла v3 `ETCD_DATA_DIR/member/snap/db`. Это происходит после миграции с v2 без прежних данных v3 и предотвращает случайную потерю v3, например при перемещении `db`. После миграции на v3 etcd требует данные v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данные v3.

Изменения, требующие пересборки, в 3.2.

#### Изменено стандартное значение `snapshot-count` {#changed-default-snapshot-count-value}

Большее значение `--snapshot-count` удерживает до снимка больше записей Raft
в памяти, вызывая [периодически повышенное потребление памяти](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156).
Лидер дольше хранит последние записи, и медленный последователь получает больше
времени догнать его до снимка. `--snapshot-count` — компромисс между памятью и
доступностью медленных последователей.

Начиная с v3.2 значение `--snapshot-count` по умолчанию [изменено с 10,000 на 100,000](https://github.com/etcd-io/etcd/pull/7160).

#### Изменена зависимость gRPC (>=3.2.10) {#changed-grpc-dependency-3210}

Выпуск 3.2.10 или более поздний теперь требует [grpc/grpc-go](https://github.com/grpc/grpc-go/releases) `v1.7.5` (<=3.2.9 требует `v1.2.1`).

##### Устаревшая `grpclog.Logger` {#deprecated-grpcloglogger}

`grpclog.Logger` был устаревшим в пользу [`grpclog.LoggerV2`](https://github.com/grpc/grpc-go/blob/master/grpclog/loggerv2.go). `clientv3.Logger` теперь `grpclog.LoggerV2`.

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

##### Устаревшая `grpc.ErrClientConnTimeout` {#deprecated-grpcerrclientconntimeout}

Ранее, `grpc.ErrClientConnTimeout` ошибка возвращалась при таймаутах на подключении клиента. 3.2 теперь возвращает `context.DeadlineExceeded` (см. [#8504](https://github.com/etcd-io/etcd/issues/8504)).

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

#### Изменены.raw оболочки клиентов gRPC {#changed-raw-grpc-client-wrappers}

3.2.12 или более поздняя версия изменяет сигнатуры функций оболочки gRPC клиентского `clientv3`. Этот изменения были необходимы для поддержки пользовательских [ограничений размера сообщений `grpc.CallOption`. ](https://github.com/etcd-io/etcd/pull/9047)

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

#### Изменена `clientv3.Lease.TimeToLive` API {#changed-clientv3leasetimetolive-api}

Прежде, `clientv3.Lease.TimeToLive` API возвращал `lease.ErrLeaseNotFound` при несуществующем идентификаторе арены. 3.2 вместо этого возвращает TTL=-1 в ответе и не выдает ошибку (см. [#7305](https://github.com/etcd-io/etcd/pull/7305)).

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

### Проверки для обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.2 кластер должен быть версии 3.1 или выше. Если это раньше 3.1, рекомендуется [обновить до 3.1](/ru/docs/etcd/upgrades/upgrade_3_1) перед обновлением до 3.2.

Также, для обеспечения плавного обновления кластер должен быть здоровым. Проверьте состояние кластера с помощью команды `etcdctl endpoint health` перед продолжением.

#### Подготовка {#preparation}

Перед обновлением etcd всегда протестируйте сервисы, зависящие от etcd, в стендовой среде перед развертыванием обновления в производственную среду.

Перед началом [сделайте резервную копию данных etcd](/ru/docs/etcd/op-guide/maintenance#snapshot-backup). Если что-то пойдет не так с обновлением, можно использовать эту резервную копию для [понижения версии](#downgrade) обратно к существующей версии etcd. Пожалуйста, примечание: команда `snapshot` выполняет только резервное копирование v3 данных. Для v2 данных см. [резервное копирование v2 хранилища данных](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Смешанные версии {#mixed-versions}

При обновлении кластер etcd поддерживает смешанные версии участников etcd и работает с протоколом самой низкой общей версии. Кластер считается обновленным только после того, как все его участники будут обновлены до версии 3.2. Внутри кластерные участники переговариваются между собой, чтобы определить общую версию кластера, которая контролирует отчетываемую версию и поддерживаемые функции.

#### Ограничения {#limitations}

Примечание: если кластер содержит только данные версии 3 и нет данных версии 2, то он не подлежит этому ограничению.

Если кластер обслуживает набор данных версии v2 размером более 50MB, каждый новый обновленный участник может потребовать до двух минут для того, чтобы синхронизироваться с существующим кластером. Проверьте размер последнего снимка, чтобы оценить общий размер данных. Иными словами, наиболее безопасно ждать 2 минут между обновлением каждого участника.

Для гораздо большего объема данных, превышающего 100MB, этот одноразовый процесс может занять еще больше времени. Администраторы очень больших кластеров etcd такого масштаба могут обратиться к команде [etcd][etcd-contact] перед обновлением, и мы с удовольствием предоставим рекомендации по процедуре.

#### Понижение версии {#downgrade}

Если все участники были обновлены до v3.2, кластер будет обновлен до v3.2, и понижение версии из этого завершенного состояния **невозможно**. Если хотя бы один участник остается v3.1, кластер и его операции остаются "v3.1", и из этого смешанного состояния кластера возможно вернуться к использованию etcd-бинарного файла версии v3.1 на всех участниках.

Создайте [резервную копию каталога данных](/ru/docs/etcd/op-guide/maintenance#snapshot-backup)
всех участников, чтобы понижение версии оставалось возможным после полного обновления.

### Процедура обновления {#upgrade-procedure}

Этот пример показывает, как обновить кластер etcd, работающий локально, состоящий из участника 3-члена v3.1.

#### 1. Проверьте требования к обновлению {#1-check-upgrade-requirements}

Я здоров и работает ли кластер v3.1.x?

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

Это хорошая идея на данном этапе создать [резервную копию данных etcd](/ru/docs/etcd/op-guide/maintenance#snapshot-backup), чтобы обеспечить возможность понижения версии в случае возникновения любых проблем:

```
$ etcdctl snapshot save backup.db
```

#### 3. Замените встраиваемую версию etcd v3.2 и запустите новый процесс etcd {#3-drop-in-etcd-v32-binary-and-start-the-new-etcd-process}

The новое v3.2 etcd будет публиковать свои данные в кластер:

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

Обновленные участники будут регистрировать предупреждения вида следующий до тех пор, пока весь кластер не будет обновлен. Это ожидаемо и прекратится после того, как все участники кластера etcd будут обновлены до v3.2:

```
2017-04-27 14:15:17.071804 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
2017-04-27 14:15:21.073110 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073142 W | etcdserver: member 6d4f535bae3ab960 has a higher version 3.2.0
2017-04-27 14:15:21.073157 W | etcdserver: the local etcd version 3.1.7 is not up-to-date
2017-04-27 14:15:21.073164 W | etcdserver: member c89feb932daef420 has a higher version 3.2.0
```

#### 4. Повторите шаг 2 до шага 3 для всех других участников {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Завершить {#5-finish}

Когда все участники будут обновлены, кластер будет сообщать о успешном переходе к 3.2:

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
