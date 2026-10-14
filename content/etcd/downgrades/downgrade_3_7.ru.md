---
title: Понижение версии etcd с v3.7 до v3.6
weight: 6600
description: Процессы, контрольные списки и примечания по понижению версии etcd с v3.7 до v3.6
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
---

В общем случае переход с etcd v3.7 на v3.6 можно выполнить как поэтапное понижение версии без простоя:

- поочерёдно останавливать процессы etcd v3.7 и заменять их процессами etcd v3.6
- после включения понижения версии новые возможности v3.7 становятся недоступны кластеру

До [начала понижения версии](#downgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.

### Контрольные списки понижения версии {#downgrade-checklists}

Основные различия между v3.7 и v3.6:

#### Различия во флагах {#difference-in-flags}

v3.7 не добавляет новых флагов, поэтому процесс v3.6 принимает все флаги конфигурации v3.7 и при понижении версии изменять конфигурацию не требуется.

> [!NOTE]
> Различия приведены для версий v3.7.0-rc.0 и v3.6.13. Фактический результат зависит от корректирующей версии; сначала проверьте его командой `diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`.

Удалённые в v3.7 устаревшие флаги `--experimental-*` всё ещё существуют в v3.6, но не добавляйте их обратно после понижения. Используйте неэкспериментальные эквиваленты или записи `--feature-gates`, работающие в обеих версиях.

#### Различия в метриках Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### Контрольные списки понижения версии сервера {#server-downgrade-checklists}

#### Требования к понижению версии {#downgrade-requirements}

Для плавного поэтапного понижения версии работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед понижением версии etcd обязательно протестируйте зависящие от него службы в промежуточном окружении, прежде чем развёртывать понижение в рабочем окружении.

До начала [загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup). Если при понижении версии возникнет проблема, эту копию можно использовать для [отката](#rollback) к существующей версии etcd.

До начала загрузите последний выпуск etcd v3.6.

#### Смешанные версии {#mixed-versions}

Во время понижения версии кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается переведённым на более старую версию после включения операции командой `etcdctl downgrade enable 3.6`. На внутреннем уровне общая версия кластера устанавливается равной целевой версии понижения и определяет сообщаемую версию и поддерживаемые возможности.

#### Откат {#rollback}

Перед понижением версии кластера etcd создайте и [загрузите его резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup). При необходимости снимок позволяет восстановить состояние кластера до понижения. Если во время операции возникнут проблемы, сначала следует определить и устранить их первопричину.

Если понижение началось после выполнения `etcdctl downgrade enable`, но кластер всё ещё находится в состоянии смешанных версий и хотя бы один участник остаётся на v3.7, текущую операцию можно отменить командой `etcdctl downgrade cancel`, а всех уже переведённых участников перезапустить с исходными двоичными файлами v3.7.

После перевода всех участников на v3.6 понижение версии кластера считается завершённым. Чтобы вернуться к исходной версии после полного понижения, необходимо следовать официальному [руководству по обновлению](/ru/etcd/upgrades/upgrade_3_7/), обеспечивая согласованность и предотвращая повреждение данных.

### Процедура понижения версии {#downgrade-procedure}

В этом примере показано понижение версии работающего на локальной машине кластера etcd v3.7 из 3 участников. Приведённый вывод получен при реальном запуске etcd v3.7.0-rc.0 и etcd v3.6.13 на одном узле с тремя локальными портами loopback в кластере, незадолго до этого обновлённом с v3.6.13.

#### Шаг 1: проверка требований к понижению версии {#step-1-check-downgrade-requirements}

Кластер исправен и использует v3.7.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 1.052416ms
localhost:32379 is healthy: successfully committed proposal: took = 1.11625ms
localhost:22379 is healthy: successfully committed proposal: took = 1.114291ms
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

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.7.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         20 |                 20 |        |                          |             false |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### Шаг 2: загрузка резервной копии снимка с лидера {#step-2-download-snapshot-backup-from-leader}

[Загрузите резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup), чтобы при необходимости восстановить состояние кластера до понижения версии:

```bash
etcdctl --endpoints=localhost:2379 snapshot save backup.db
<<COMMENT
{"level":"info","ts":"2026-07-02T06:48:11.091982+0300","caller":"snapshot/v3_snapshot.go:83","msg":"created temporary db file","path":"backup.db.part"}
{"level":"info","ts":"2026-07-02T06:48:11.092253+0300","logger":"client","caller":"v3/maintenance.go:236","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":"2026-07-02T06:48:11.099884+0300","caller":"snapshot/v3_snapshot.go:96","msg":"fetching snapshot","endpoint":"localhost:2379"}
{"level":"info","ts":"2026-07-02T06:48:11.100394+0300","logger":"client","caller":"v3/maintenance.go:302","msg":"completed snapshot read; closing"}
{"level":"info","ts":"2026-07-02T06:48:11.103116+0300","caller":"snapshot/v3_snapshot.go:111","msg":"fetched snapshot","endpoint":"localhost:2379","size":"98 kB","took":"10.9815ms","etcd-version":"3.7.0"}
{"level":"info","ts":"2026-07-02T06:48:11.103296+0300","caller":"snapshot/v3_snapshot.go:121","msg":"saved","path":"backup.db"}
Snapshot saved at backup.db
Server version 3.7.0
COMMENT
```

#### Шаг 3: проверка целевой версии понижения {#step-3-validate-downgrade-target-version}

Перед включением понижения проверьте целевую версию:

- Поддерживается понижение только на одну минорную версию за раз. Например, переход с v3.7 на v3.5 недопустим.
- Не переходите к следующему шагу до успешного завершения проверки.

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### Шаг 4: включение понижения версии {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

После включения понижения кластер начнёт работать по протоколу v3.6 — целевой версии операции. Кроме того, etcd автоматически перенесёт схему на целевую версию, что обычно происходит очень быстро. Прежде чем переходить к следующему шагу, проверьте состояние конечных точек и убедитесь, что версия хранилища всех серверов изменена на v3.6.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         22 |                 22 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> После включения понижения кластер продолжает работать по протоколу v3.6, даже если все серверы всё ещё используют двоичный файл v3.7, пока операция не отменена командой `etcdctl downgrade cancel`

#### Шаг 5: остановка одного существующего сервера etcd {#step-5-stop-one-existing-etcd-server}

Перед остановкой сервера проверьте, является ли он лидером. Рекомендуется понижать версию лидера последним. Если останавливаемый сервер является лидером, часть простоя можно предотвратить, выполнив `move-leader` на другой сервер до остановки текущего.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

При остановке каждого процесса etcd другие участники кластера записывают в журнал ожидаемые ошибки. Это нормально, поскольку соединение с участником кластера (временно) разорвано:

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### Шаг 6: перезапуск сервера etcd с той же конфигурацией {#step-6-restart-the-etcd-server-with-same-configuration}

Перезапустите сервер etcd с прежней конфигурацией, но с двоичным файлом etcd v3.6.

```diff
-etcd-3.7/bin/etcd --name s2 \
+etcd-3.6/bin/etcd --name s2 \
  --data-dir /tmp/etcd/s2 \
  --listen-client-urls http://localhost:22379 \
  --advertise-client-urls http://localhost:22379 \
  --listen-peer-urls http://localhost:22380 \
  --initial-advertise-peer-urls http://localhost:22380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с двоичным файлом etcd v3.6:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |  VERSION   | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:22379 | 729934363faa4a24 |     3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
| localhost:32379 |  b548c2511513015 | 3.7.0-rc.0 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         5 |         23 |                 23 |        |                    3.6.0 |              true |
+-----------------+------------------+------------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 939.625µs
localhost:32379 is healthy: successfully committed proposal: took = 981.459µs
localhost:22379 is healthy: successfully committed proposal: took = 1.11075ms
COMMENT
```

> [!NOTE]
> В отличие от v3.5 конечная точка состояния v3.6 сообщает сведения о понижении, поэтому до завершения операции переведённые участники продолжают показывать `DOWNGRADE ENABLED` как true и свою версию хранилища.

#### Шаг 7: повторение *шага 5* и *шага 6* для остальных участников {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

После понижения версии всех участников операция автоматически завершается, а `DOWNGRADE ENABLED` сбрасывается в false. Проверьте работоспособность и состояние кластера, убедившись, что минорная версия всех участников и версия хранилища равны v3.6:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA  | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 7339c4e5e833c029 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:22379 | 729934363faa4a24 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |      true |      false |         6 |         30 |                 30 |        |                          |             false |
| localhost:32379 |  b548c2511513015 |  3.6.13 |           3.6.0 |   98 kB |  98 kB |                    0% | 2.1 GB |     false |      false |         6 |         30 |                 30 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+--------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 5.176958ms
localhost:32379 is healthy: successfully committed proposal: took = 5.177875ms
localhost:2379 is healthy: successfully committed proposal: took = 5.191625ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.13","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT
```

В журнале лидера должно появиться сообщение, подобное следующему:

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
