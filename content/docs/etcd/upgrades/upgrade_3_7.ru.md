---
title: Обновление etcd с v3.6 до v3.7
weight: 6700
description: Процессы, контрольные списки и примечания по обновлению etcd с v3.6 до v3.7
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
aliases: [/etcd/upgrades/upgrade_3_7/]
---

В общем случае переход с etcd v3.6 на v3.7 можно выполнить как скользящее обновление без простоя:

- поочерёдно останавливать процессы etcd v3.6 и заменять их процессами etcd v3.7
- после запуска всех процессов v3.7 кластеру становятся доступны новые возможности v3.7

До [начала обновления](#upgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.

### Контрольные списки обновления {#upgrade-checklists}

#### Обновление 3.6 {#update-36}

> [!IMPORTANT]
> Перед обновлением до 3.7 убедитесь, что все участники 3.6 обновлены до 3.6.11 или более поздней версии. Предыдущие корректирующие выпуски 3.6 могут быть несовместимы со скользящим обновлением до 3.7.

#### Хранилище V2 {#v2-store}

Хранилище v2 полностью удалено в v3.7. HTTP API v2 (`--enable-v2`), эмуляция v2 поверх v3 (`--experimental-enable-v2v3`), служба обнаружения v2, пакет `client/v2` и загрузка файлов снимков v2 больше не существуют. Ссылки на нарушающие совместимость изменения приведены в [CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

При обновлении кластера 3.6 эти флаги уже отсутствуют, и никаких действий не требуется. Если переход выполняется со старого выпуска с пользовательскими данными v2, до обновления следуйте [руководству по миграции v2](https://etcd.io/docs/v3.4/op-guide/v2-migration/).

#### Рефакторинг Go {#go-refactoring}

v3.7 содержит значительный внутренний рефакторинг, который не влияет на обычное обновление, но его следует учитывать при обновлении пользовательских интеграций:

- Переход с `gogo/protobuf` на стандартный `google.golang.org/protobuf` (отслеживается в [#14533](https://github.com/etcd-io/etcd/issues/14533)).
- Переход с устаревших библиотек журналирования и тегов `go-grpc-middleware` v1 на перехватчики v2 ([#20420](https://github.com/etcd-io/etcd/pull/20420)).
- Перехватчики gRPC OpenTelemetry обновлены до `otelgrpc` v0.61.0: устаревшие `UnaryServerInterceptor` и `StreamServerInterceptor` заменены на `NewServerHandler` ([#20017](https://github.com/etcd-io/etcd/pull/20017)).

Если etcd встраивается как библиотека, приложение собирается с API `clientv3` или зависит от внутренних пакетов, перед обновлением изучите [CHANGELOG](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

### Удалённые флаги {#flags-removed}

В v3.7 удалены все устаревшие флаги `--experimental-*` ([#19959](https://github.com/etcd-io/etcd/pull/19959)). В v3.6 каждый из них был заменён либо одноимённым неэкспериментальным флагом, либо записью `--feature-gates`. Если какие-либо из этих флагов всё ещё заданы, замените их эквивалентами v3.6 **до** скользящего обновления до v3.7, иначе процесс v3.7 не запустится.

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

Соответствие каждого удалённого флага его неэкспериментальному эквиваленту или записи `--feature-gates` приведено в [руководстве по обновлению с v3.5 до v3.6](/ru/docs/etcd/upgrades/upgrade_3_6/).

### Добавленные флаги {#flags-added}

Нет.

### Флаги с новыми значениями по умолчанию {#flags-with-new-defaults}

Нет.

### Контрольные списки обновления сервера {#server-upgrade-checklists}

#### Требования к обновлению {#upgrade-requirements}

Для обновления существующего развёртывания etcd до v3.7 работающий кластер должен иметь версию v3.6.11 или более позднюю. Если он использует более старую дополнительную версию, сначала [обновитесь до v3.6](/ru/docs/etcd/upgrades/upgrade_3_6/); etcd поддерживает обновление только на одну дополнительную версию за раз.

Кроме того, для плавного скользящего обновления работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед обновлением etcd обязательно протестируйте службы, зависящие от etcd, в промежуточном окружении, прежде чем развёртывать обновление в рабочем окружении.

До начала [загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). Если при обновлении возникнет проблема, эту копию можно использовать для [отката](#rollback) к существующей версии etcd.

#### Смешанные версии {#mixed-versions}

Во время обновления кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается обновлённым только после обновления всех участников до v3.7. Участники etcd согласуют между собой общую версию кластера, которая определяет сообщаемую версию и поддерживаемые возможности.

#### Откат {#rollback}

Перед обновлением кластера etcd создайте и [загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). При необходимости этот снимок можно использовать для восстановления состояния кластера до обновления. Если во время обновления возникнут проблемы, пользователям следует сначала определить и устранить их первопричину. Пока кластер остаётся в состоянии смешанных версий и хотя бы один участник работает на v3.6, можно либо заменить двоичный файл или образ старой версией v3.6, либо непосредственно восстановить кластер из снимка. В таком смешанном состоянии кластер продолжает работать как кластер v3.6, что позволяет откатиться без формальной процедуры понижения версии.

Однако после обновления всех участников до v3.7 кластер считается полностью обновлённым, и откат заменой двоичных файлов больше невозможен. В этом случае остаётся только восстановиться из снимка, сделанного перед обновлением, либо при неудачном обновлении следовать официальному [руководству по понижению версии](/ru/docs/etcd/downgrades/downgrading-etcd/).

### Процедура обновления {#upgrade-procedure}

В этом примере показано обновление работающего на локальной машине кластера etcd v3.6 из 3 участников. Приведённый ниже вывод получен при реальном запуске etcd v3.6.12 и etcd v3.7.0-rc.0 на одном узле с тремя портами обратной петли.

#### Шаг 1: проверка требований к обновлению {#step-1-check-upgrade-requirements}

Кластер исправен и использует v3.6.11 или более позднюю версию?

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

#### Шаг 2: загрузка резервной копии снимка с лидера {#step-2-download-snapshot-backup-from-leader}

[Загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup), чтобы обеспечить путь понижения версии в случае возникновения проблем.

Лидер etcd гарантированно содержит последние данные приложения, поэтому снимок следует получать с лидера:

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

#### Шаг 3: остановка одного существующего сервера etcd {#step-3-stop-one-existing-etcd-server}

При остановке каждого процесса etcd другие участники кластера записывают в журнал ожидаемые ошибки. Это нормально, поскольку соединение с участником кластера (временно) разорвано. Перед завершением лидер передаст лидерство:

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
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

Новый etcd v3.7 опубликует свои сведения в кластере. На этом этапе кластер всё ещё работает по протоколу v3.6 — наименьшей общей версии.

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с новым двоичным файлом etcd v3.7:

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

До обновления всего кластера необновлённые и уже обновлённый участники будут записывать сообщения о состоянии смешанных версий. Это ожидаемо и прекратится после обновления всех участников кластера etcd до v3.7.

#### Шаг 5: повторение *шага 3* и *шага 4* для остальных участников {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

После обновления всех участников кластер сообщит об успешном переходе на v3.7:

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
