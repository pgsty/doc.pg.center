---
title: Обновление etcd с 3.4 до 3.5
weight: 6650
description: Процессы, контрольные списки и примечания по обновлению etcd с 3.4 до 3.5
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_5.md"
---

В общем случае переход с etcd 3.4 на 3.5 можно выполнить как поэтапное обновление без простоя:
 - поочерёдно останавливать процессы etcd v3.4 и заменять их процессами etcd v3.5
 - после запуска всех процессов v3.5 кластеру становятся доступны новые возможности v3.5

До [начала обновления](#upgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.



### Контрольные списки обновления {#upgrade-checklists}

> [!WARNING]
> При [миграции с v2 без данных v3](https://github.com/etcd-io/etcd/issues/9480) сервер etcd v3.2+ аварийно завершается, если etcd восстанавливается из существующих снимков, но файл v3 `ETCD_DATA_DIR/member/snap/db` отсутствует. Это происходит, когда сервер был перенесён с v2 и ранее не содержал данных v3. Такое поведение также предотвращает случайную потерю данных v3 (например, если файл `db` перемещён). etcd требует, чтобы после миграции на v3 работа продолжалась только при наличии данных v3. Не обновляйтесь до более новых версий v3, пока сервер v3.0 не содержит данных v3.

> [!WARNING]
> Если в кластере включена аутентификация, поэтапное обновление с 3.4 или более ранней версии не поддерживается, поскольку 3.5 [изменяет формат относящихся к аутентификации записей WAL](https://github.com/etcd-io/etcd/pull/11943).

Основные нарушающие совместимость изменения в 3.5.

#### Устаревшая метрика Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` {#deprecated-etcd_debugging_mvcc_db_total_size_in_bytes-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.5 метрика Prometheus `etcd_debugging_mvcc_db_total_size_in_bytes` переведена в `etcd_mvcc_db_total_size_in_bytes`. В v3.5 метрика `etcd_debugging_mvcc_db_total_size_in_bytes` полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_db_total_size_in_bytes
+etcd_mvcc_db_total_size_in_bytes
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Устаревшая метрика Prometheus `etcd_debugging_mvcc_put_total` {#deprecated-etcd_debugging_mvcc_put_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.5 метрика Prometheus `etcd_debugging_mvcc_put_total` переведена в `etcd_mvcc_put_total`. В v3.5 метрика `etcd_debugging_mvcc_put_total` полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_put_total
+etcd_mvcc_put_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Устаревшая метрика Prometheus `etcd_debugging_mvcc_delete_total` {#deprecated-etcd_debugging_mvcc_delete_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.5 метрика Prometheus `etcd_debugging_mvcc_delete_total` переведена в `etcd_mvcc_delete_total`. В v3.5 метрика `etcd_debugging_mvcc_delete_total` полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_delete_total
+etcd_mvcc_delete_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Устаревшая метрика Prometheus `etcd_debugging_mvcc_txn_total` {#deprecated-etcd_debugging_mvcc_txn_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.5 метрика Prometheus `etcd_debugging_mvcc_txn_total` переведена в `etcd_mvcc_txn_total`. В v3.5 метрика `etcd_debugging_mvcc_txn_total` полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_txn_total
+etcd_mvcc_txn_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Устаревшая метрика Prometheus `etcd_debugging_mvcc_range_total` {#deprecated-etcd_debugging_mvcc_range_total-prometheus-metrics}

Чтобы стимулировать мониторинг хранилища etcd, в v3.5 метрика Prometheus `etcd_debugging_mvcc_range_total` переведена в `etcd_mvcc_range_total`. В v3.5 метрика `etcd_debugging_mvcc_range_total` полностью объявлена устаревшей.

```diff
-etcd_debugging_mvcc_range_total
+etcd_mvcc_range_total
```

Обратите внимание: метрики пространства имён `etcd_debugging_*` помечены как экспериментальные. По мере улучшения руководства по мониторингу дополнительные метрики могут становиться стабильными.

#### Устаревший `etcd --logger capnslog` {#deprecated-etcd---logger-capnslog}

Для поддержки нескольких направлений вывода и структурированного ведения журнала v3.5 по умолчанию использует `--logger=zap`.

**`etcd --logger=capnslog` объявлен устаревшим в v3.5**, а теперь по умолчанию используется `--logger=zap`.

```diff
-etcd --logger=capnslog
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

В v3.4 добавлена поддержка `etcd --logger=zap` для структурированного ведения журнала и нескольких направлений вывода. Основная цель — содействовать автоматизированному мониторингу etcd вместо просмотра серверных журналов уже после начала сбоя. В дальнейшем etcd будет записывать как можно меньше сообщений, а его мониторинг с помощью метрик и оповещений станет проще. **`etcd --logger=capnslog` будет объявлен устаревшим в v3.5.**

#### Устаревший `etcd --log-output` {#deprecated-etcd---log-output}

Для поддержки нескольких направлений вывода журнала в v3.4 [`etcd --log-output` переименован в `--log-outputs`](https://github.com/etcd-io/etcd/pull/9624).

**`etcd --log-output` объявлен устаревшим в v3.5.**

```diff
-etcd --log-output=stderr
+etcd --log-outputs=stderr
```

#### Устаревший флаг `etcd --debug` (теперь `--log-level=debug`) {#deprecated-etcd---debug-flag-now---log-leveldebug}

**Флаг `etcd --debug` объявлен устаревшим.**

```diff
-etcd --debug
+etcd --log-level debug
```

#### Устаревший `etcd --log-package-levels` {#deprecated-etcd---log-package-levels}

**Флаг `etcd --log-package-levels` для `capnslog` объявлен устаревшим.**

Теперь по умолчанию используется **`etcd --logger=zap`**.

```diff
-etcd --log-package-levels 'etcdmain=CRITICAL,etcdserver=DEBUG'
+etcd --logger=zap --log-outputs=stderr
```

#### Устаревшая конечная точка `[CLIENT-URL]/config/local/log` {#deprecated-client-urlconfiglocallog}

**Конечная точка `/config/local/log`, как и флаг `etcd --log-package-levels`, объявляется устаревшей в v3.5.**

```diff
-$ curl http://127.0.0.1:2379/config/local/log -XPUT -d '{"Level":"DEBUG"}'
-# debug logging enabled
```

#### Изменённые конечные точки HTTP шлюза gRPC (устаревшая `/v3beta`) {#changed-grpc-gateway-http-endpoints-deprecated-v3beta}

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

`/v3beta` удалена в выпуске 3.5.



### Контрольные списки обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до 3.5 работающий кластер должен иметь версию 3.4 или более позднюю. Если версия ниже 3.4, перед переходом на 3.5 [обновитесь до 3.4](/ru/etcd/upgrades/upgrade_3_4/).

Кроме того, для плавного поэтапного обновления работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте зависящие от него службы в промежуточном окружении, прежде чем развёртывать обновление в рабочем окружении.

До начала [загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup). Если при обновлении возникнет проблема, эту копию можно использовать для [понижения версии](#downgrade) до существующей версии etcd. Обратите внимание: команда `snapshot` сохраняет только данные v3. О данных v2 см. раздел [резервное копирование хранилища v2](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается обновлённым только после обновления всех участников до 3.5. Участники etcd согласуют между собой общую версию кластера, которая определяет сообщаемую версию и поддерживаемые возможности.

#### Ограничения {#limitations}

Примечание: это ограничение не относится к кластеру, содержащему только данные v3 и не содержащему данных v2.

Если кластер обслуживает набор данных v2 объёмом более 50MB, каждому только что обновлённому участнику может потребоваться до двух минут, чтобы догнать существующий кластер. Для оценки общего объёма данных проверьте размер недавнего снимка. Иными словами, безопаснее всего ждать 2 минуты между обновлениями участников.

При значительно большем общем объёме данных, 100MB или более, этот однократный процесс может занять ещё больше времени. Администраторы столь крупных кластеров etcd могут перед обновлением обратиться к [команде etcd][etcd-contact] за рекомендациями по процедуре.

#### Понижение версии {#downgrade}

После обновления всех участников до v3.5 кластер также переходит на v3.5, и понижение версии из этого завершённого состояния **невозможно**. Однако пока хотя бы один участник остаётся на v3.4, кластер и его операции имеют версию "v3.4", а из смешанного состояния можно вернуться к использованию двоичного файла etcd v3.4 на всех участниках.

[Загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup), чтобы сохранить возможность понижения версии кластера даже после полного обновления.

### Процедура обновления {#upgrade-procedure}

В этом примере показано обновление работающего на локальной машине кластера etcd v3.4 из 3 участников.

#### Шаг 1: проверка требований к обновлению {#step-1-check-upgrade-requirements}

Кластер исправен и использует v3.4.x?

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

#### Шаг 2: загрузка резервной копии снимка с лидера {#step-2-download-snapshot-backup-from-leader}

[Загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup), чтобы сохранить возможность понижения версии при возникновении проблем.

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
  --initial-cluster-state new
```

Новый etcd v3.5 опубликует свои сведения в кластере. На этом этапе кластер всё ещё работает по протоколу v3.4 — наименьшей общей версии.

> `{"level":"info","ts":1526586617.1647713,"caller":"membership/cluster.go:485","msg":"set initial cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1648536,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":1526586617.1649303,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"7339c4e5e833c029","from":"3.0","from":"3.4"}`

> `{"level":"info","ts":1526586617.1649797,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.4"}`

> `{"level":"info","ts":1526586617.2107732,"caller":"etcdserver/server.go:1770","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","request-path":"/0/members/7339c4e5e833c029/attributes","cluster-id":"7dee9ba76d59ed53","publish-timeout":7}`

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с новым двоичным файлом etcd v3.5:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

До обновления всего кластера необновлённые участники будут записывать в журнал подобные предупреждения.

Это ожидаемо и прекратится после обновления всех участников кластера etcd до v3.5:

```
:41.942121 W | etcdserver: member 7339c4e5e833c029 has a higher version 3.5.0
:45.945154 W | etcdserver: the local etcd version 3.4.0 is not up-to-date
```

#### Шаг 5: повторение *шага 3* и *шага 4* для остальных участников {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

После обновления всех участников кластер сообщит об успешном переходе на 3.5:

Участник 1:

> `{"level":"info","ts":1526586949.0920913,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`
> `{"level":"info","ts":1526586949.0921566,"caller":"etcdserver/server.go:2272","msg":"cluster version is updated","cluster-version":"3.5"}`

Участник 2:

> `{"level":"info","ts":1526586949.092117,"caller":"membership/cluster.go:473","msg":"updated cluster version","cluster-id":"7dee9ba76d59ed53","local-member-id":"729934363faa4a24","from":"3.4","from":"3.5"}`
> `{"level":"info","ts":1526586949.0923078,"caller":"api/capability.go:76","msg":"enabled capabilities for version","cluster-version":"3.5"}`

Участник 3:

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
