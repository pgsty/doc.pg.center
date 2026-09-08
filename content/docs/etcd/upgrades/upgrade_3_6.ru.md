---
title: Обновление etcd с v3.5 до v3.6
weight: 6600
description: Процессы, контрольные списки и примечания по обновлению etcd с v3.5 до v3.6
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_6.md"
aliases: [/etcd/upgrades/upgrade_3_6/]
---

В общем случае переход с etcd v3.5 на v3.6 можно выполнить как скользящее обновление без простоя:

- поочерёдно останавливать процессы etcd v3.5 и заменять их процессами etcd v3.6
- после запуска всех процессов v3.6 кластеру становятся доступны новые возможности v3.6

До [начала обновления](#upgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.

### Контрольные списки обновления {#upgrade-checklists}

#### Обновление 3.5 {#update-35}

> [!IMPORTANT]
> Перед обновлением до 3.6 убедитесь, что [все участники 3.5 обновлены до 3.5.32 или более поздней версии](https://etcd.io/blog/2026/july-patch-release/). Корректирующие выпуски с 3.5.24 по 3.5.26 устраняют несколько потенциальных препятствий обновлению; в [3.5.32](https://etcd.io/blog/2026/july-patch-release/) добавлен `--v2-deprecation=write-only-skip-check`, а `etcdutl check v2store` расширен для проверки не только снимка v2, но и записей WAL.

#### Хранилище V2 {#v2-store}

> [!NOTE]
> Если флаг `--enable-v2` не настроен или равен false, дальнейшие действия не требуются.

Если `--enable-v2` **настроен**, выполните `etcdutl check v2store`, чтобы проверить наличие в v2store пользовательских данных, не относящихся к составу кластера. Если таких данных нет, флаг можно безопасно удалить. В противном случае обратитесь к [руководству по миграции v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/).

### Добавленные флаги {#flags-added}

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

### Удалённые флаги {#flags-removed}

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

### Устаревшие флаги {#flags-deprecated}

**Флаг `etcd --experimental-bootstrap-defrag-threshold-megabytes` объявлен устаревшим.**

```diff

-etcd --experimental-bootstrap-defrag-threshold-megabytes

+etcd --bootstrap-defrag-threshold-megabytes

```

**Флаг `etcd --experimental-compaction-batch-limit` объявлен устаревшим.**

```diff

-etcd --experimental-compaction-batch-limit

+etcd --compaction-batch-limit

```

**Флаг `etcd --experimental-compact-hash-check-time` объявлен устаревшим.**

```diff

-etcd --experimental-compact-hash-check-time

+etcd --compact-hash-check-time

```

**Флаг `etcd --experimental-compaction-sleep-interval` объявлен устаревшим.**

```diff

-etcd --experimental-compaction-sleep-interval

+etcd --compaction-sleep-interval

```

**Флаг `etcd --experimental-corrupt-check-time` объявлен устаревшим.**

```diff

-etcd --experimental-corrupt-check-time

+etcd --corrupt-check-time

```

**Флаг `etcd --experimental-enable-distributed-tracing` объявлен устаревшим.**

```diff

-etcd --experimental-enable-distributed-tracing

+etcd --enable-distributed-tracing

```

**Флаг `etcd --experimental-distributed-tracing-address` объявлен устаревшим.**

```diff

-etcd --experimental-distributed-tracing-address

+etcd --distributed-tracing-address

```

**Флаг `etcd --experimental-distributed-tracing-instance-id` объявлен устаревшим.**

```diff

-etcd --experimental-distributed-tracing-instance-id

+etcd --distributed-tracing-instance-id

```

**Флаг `etcd --experimental-distributed-tracing-sampling-rate` объявлен устаревшим.**

```diff

-etcd --experimental-distributed-tracing-sampling-rate

+etcd --distributed-tracing-sampling-rate

```

**Флаг `etcd --experimental-distributed-tracing-service-name` объявлен устаревшим.**

```diff

-etcd --experimental-distributed-tracing-service-name

+etcd --distributed-tracing-service-name

```

**Флаг `etcd --experimental-downgrade-check-time` объявлен устаревшим.**

```diff

-etcd --experimental-downgrade-check-time

+etcd --downgrade-check-time

```

**Флаг `etcd --experimental-max-learners` объявлен устаревшим.**

```diff

-etcd --experimental-max-learners

+etcd --max-learners

```

**Флаг `etcd --experimental-memory-mlock` объявлен устаревшим.**

```diff

-etcd --experimental-memory-mlock

+etcd --memory-mlock

```

**Флаг `etcd --experimental-peer-skip-client-san-verification` объявлен устаревшим.**

```diff

-etcd --experimental-peer-skip-client-san-verification

+etcd --peer-skip-client-san-verification

```

**Флаг `etcd --experimental-snapshot-catchup-entries` объявлен устаревшим.**

```diff

-etcd --experimental-snapshot-catchup-entries

+etcd --snapshot-catchup-entries

```

**Флаг `etcd --experimental-warning-apply-duration` объявлен устаревшим.**

```diff

-etcd --experimental-warning-apply-duration

+etcd --warning-apply-duration

```

**Флаг `etcd --experimental-warning-unary-request-duration` объявлен устаревшим.**

```diff

-etcd --experimental-warning-unary-request-duration

+etcd --warning-unary-request-duration

```

**Флаг `etcd --experimental-watch-progress-notify-interval` объявлен устаревшим.**

```diff

-etcd --experimental-watch-progress-notify-interval

+etcd --watch-progress-notify-interval

```

### Эквивалентные флаги функций v3.5 {#equivalent-flags-of-v35-feature-gates}

**эквивалентный флаг функции для `etcd --experimental-compact-hash-check-enabled=true`**

```diff

-etcd --experimental-compact-hash-check-enabled=true

+etcd --feature-gates=CompactHashCheck=true

```

**эквивалентный флаг функции для `etcd --experimental-initial-corrupt-check=true`**

```diff

-etcd --experimental-initial-corrupt-check=true

+etcd --feature-gates=InitialCorruptCheck=true

```

**эквивалентный флаг функции для `etcd --experimental-enable-lease-checkpoint=true`**

```diff

-etcd --experimental-enable-lease-checkpoint=true

+etcd --feature-gates=LeaseCheckpoint=true

```

**эквивалентный флаг функции для `etcd --experimental-enable-lease-checkpoint-persist=true`**

```diff

-etcd --experimental-enable-lease-checkpoint-persist=true

+etcd --feature-gates=LeaseCheckpointPersist=true

```

**эквивалентный флаг функции для `etcd --experimental-stop-grpc-service-on-defrag=true`**

```diff

-etcd --experimental-stop-grpc-service-on-defrag=true

+etcd --feature-gates=StopGRPCServiceOnDefrag=true

```

**эквивалентный флаг функции для `etcd --experimental-txn-mode-write-with-shared-buffer=false`**

```diff

-etcd --experimental-txn-mode-write-with-shared-buffer=false

+etcd --feature-gates=TxnModeWriteWithSharedBuffer=false

```

### Флаги с новыми значениями по умолчанию {#flags-with-new-defaults}

**Исходное значение флага по умолчанию `etcd --snapshot-count=100000`**

```diff

-etcd --snapshot-count=100000

+etcd --snapshot-count=10000

```

**Исходное значение флага по умолчанию `etcd --v2-deprecation='not-yet'`**

```diff

-etcd --v2-deprecation='not-yet'

+etcd --v2-deprecation='write-only'

```

**Исходное значение флага по умолчанию `etcd --discovery-fallback='proxy'`**

```diff

-etcd --discovery-fallback='proxy'

+etcd --discovery-fallback='exit'

```

### Различия в метриках Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics added in v3.6
+etcd_network_known_peers
+etcd_server_feature_enabled
```

### Контрольные списки обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до v3.6 работающий кластер должен иметь версию v3.5 или более позднюю. Если версия старше v3.5, перед переходом на v3.6 [обновитесь до v3.5](/ru/docs/etcd/upgrades/upgrade_3_4/).

Кроме того, для плавного скользящего обновления работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в промежуточном окружении, прежде чем развёртывать обновление в рабочем окружении.

До начала [загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). Если при обновлении возникнет проблема, эту копию можно использовать для [отката](#rollback) к существующей версии etcd. Обратите внимание: команда `snapshot` сохраняет только данные v3.

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается обновлённым только после обновления всех участников до v3.6. Участники etcd согласуют между собой общую версию кластера, которая определяет сообщаемую версию и поддерживаемые возможности.

#### Откат {#rollback}

Перед обновлением кластера etcd создайте и [загрузите его резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). При необходимости снимок позволяет восстановить состояние кластера до обновления. Если во время обновления возникнут проблемы, сначала следует определить и устранить их первопричину. Пока кластер находится в состоянии смешанных версий и хотя бы один участник остаётся на v3.5, можно либо заменить двоичный файл или образ старой версией v3.5, либо непосредственно восстановить кластер из снимка. В таком смешанном состоянии кластер продолжает работать как кластер v3.5, что позволяет откатиться без формальной процедуры понижения версии.

Однако после обновления всех участников до v3.6 кластер считается полностью обновлённым, и откат заменой двоичных файлов больше невозможен. В этом случае восстановиться можно только из снимка, сделанного перед обновлением. Чтобы вернуться к исходной версии после полного обновления, необходимо следовать официальному руководству по понижению версии, обеспечивая согласованность и предотвращая повреждение данных.

### Процедура обновления {#upgrade-procedure}

В этом примере показано обновление работающего на локальной машине кластера etcd v3.5 из 3 участников.

#### Шаг 1: проверка требований к обновлению {#step-1-check-upgrade-requirements}

Кластер исправен и использует v3.5.x?

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

#### Шаг 2: загрузка резервной копии снимка с лидера {#step-2-download-snapshot-backup-from-leader}

[Загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup), чтобы обеспечить путь понижения версии при возникновении проблем.

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
{"level":"info","ts":"2025-03-01T04:34:10.336768+0530","caller":"snapshot/v3_snapshot.go:65","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2025-03-01T04:34:10.342373+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:212","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2025-03-01T04:34:10.342433+0530","caller":"snapshot/v3_snapshot.go:73","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2025-03-01T04:34:10.346482+0530","logger":"client","caller":"v3@v3.5.18/maintenance.go:220","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2025-03-01T04:34:10.348801+0530","caller":"snapshot/v3_snapshot.go:88","msg":"fetched snapshot","endpoint":"localhost:2379","size":"20 kB","took":"now"}
{"level":"info","ts":"2025-03-01T04:34:10.348933+0530","caller":"snapshot/v3_snapshot.go:97","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
COMMENT
```

#### Шаг 3: остановка одного существующего сервера etcd {#step-3-stop-one-existing-etcd-server}

При остановке каждого процесса etcd другие участники кластера записывают в журнал ожидаемые ошибки. Это нормально, поскольку соединение с участником кластера (временно) разорвано:

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

#### Шаг 4: перезапуск сервера etcd с той же конфигурацией {#step-4-restart-the-etcd-server-with-same-configuration}

Перезапустите сервер etcd с прежней конфигурацией, но с новым двоичным файлом etcd.

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

Новый etcd v3.6 опубликует свои сведения в кластере. На этом этапе кластер всё ещё работает по протоколу v3.5 — наименьшей общей версии.

> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.889+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"bf9071f4639c75cc","from":"3.0","to":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.828+0530","caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
>
> `{"level":"info","ts":"2025-03-01T04:40:36.894+0530","caller":"etcdserver/server.go:1686","msg":"published local member to cluster through raft","local-member-id":"bf9071f4639c75cc","local-member-attributes":"{Name:node1 ClientURLs:[http://127.0.0.1:2379]}","cluster-id":"59a05384c9b79ee","publish-timeout":"7s"}`

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с новым двоичным файлом etcd v3.6:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.704998ms
localhost:22379 is healthy: successfully committed proposal: took = 2.331754ms
localhost:32379 is healthy: successfully committed proposal: took = 2.490705ms
COMMENT
```

До обновления всего кластера необновлённые участники будут записывать в журнал подобные предупреждения.

Это ожидаемо и прекратится после обновления всех участников кластера etcd до v3.6:

```bash
{"level":"warn","ts":"2025-03-01T04:40:37.545960+0530","caller":"etcdserver/cluster_util.go:189","msg":"leader found higher-versioned member","local-member-version":"3.5.18","remote-member-id":"bf9071f4639c75cc","remote-member-version":"3.6.0-alpha.0"}
```

#### Шаг 5: повторение *шага 3* и *шага 4* для остальных участников {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

После обновления всех участников кластер сообщит об успешном переходе на v3.6:

Участник 1:

> `{"level":"info","ts":"2025-03-01T04:58:32.375+0530","caller":"etcdserver/server.go:2149","msg":"updating cluster version using v3 API","from":"3.5","to":"3.6"}`
> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"etcdserver/server.go:2164","msg":"cluster version is updated","cluster-version":"3.6"}`

Участник 2:

> `{"level":"info","ts":"2025-03-01T04:58:32.377+0530","caller":"membership/cluster.go:539","msg":"updated cluster version","cluster-id":"59a05384c9b79ee","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.6"}`

Участник 3:

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
