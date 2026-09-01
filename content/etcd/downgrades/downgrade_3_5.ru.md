---
title: Понижение версии etcd от 3.5 до 3.4
weight: 6650
description: "Процессы, списки действий и примечания по уменьшению версии etcd от 3.5 до 3.4"
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/downgrades/downgrade_3_5.md"
---

В общем случае, понижение версии от etcd 3.5 к 3.4 может быть безостановочным и ролевым:

- по одному останавливайте процессы etcd 3.5 и заменяйте их на процессы etcd 3.4
- после запуска любых процессов 3.4 новые функции в 3.5 больше не доступны для кластера

Перед [началом понижения версии](#downgrade-procedure) прочитайте остальную часть руководства и подготовьтесь.

### Проверочные списки для понижения версии {#downgrade-checklists}

содержимое/enhttps://etcd.io/docs/v3.5/op-guide/authentication/rbac.md

> [!WARNING]
> Если в кластере включена аутентификация, поэтапное понижение с 3.5 не поддерживается: 3.5 [изменяет формат связанных с аутентификацией записей WAL](https://github.com/etcd-io/etcd/pull/11943). Сначала следуйте [инструкциям по аутентификации](/ru/etcd/op-guide/authentication/rbac/), чтобы отключить её и удалить всех пользователей.

Изменения, требующие пересборки, от 3.5 до 3.4:

#### Разница в флагах {#difference-in-flags}

Если вы используете какие-либо из следующих флагов в своей конфигурации 3.5, обязательно убедитесь, что при устаревании до 3.4 вы либо удалили, либо переименовали эти флаги, либо изменили их значение по умолчанию.

> [!NOTE]
> Разница основана на версии 3.5.14 и v.3.4.33. Фактическая разница будет зависеть от вашей версии патча, свяжитесь с `diff <(etcd-3.5/bin/etcd -h | grep \\-\\-) <(etcd-3.4/bin/etcd -h | grep \\-\\-)` первым.

```diff
# flags not available in 3.4
-etcd --socket-reuse-port
-etcd --socket-reuse-address
-etcd --raft-read-timeout
-etcd --raft-write-timeout
-etcd --v2-deprecation
-etcd --client-cert-file
-etcd --client-key-file
-etcd --peer-client-cert-file
-etcd --peer-client-key-file
-etcd --self-signed-cert-validity
-etcd --enable-log-rotation --log-rotation-config-json=some.json
-etcd --experimental-enable-distributed-tracing --experimental-distributed-tracing-address='localhost:4317' --experimental-distributed-tracing-service-name='etcd' --experimental-distributed-tracing-instance-id='' --experimental-distributed-tracing-sampling-rate='0'
-etcd --experimental-compact-hash-check-enabled --experimental-compact-hash-check-time='1m'
-etcd --experimental-downgrade-check-time
-etcd --experimental-memory-mlock
-etcd --experimental-txn-mode-write-with-shared-buffer
-etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --experimental-stop-grpc-service-on-defrag

# same flag with different names
-etcd --backend-bbolt-freelist-type=map
+etcd --experimental-backend-bbolt-freelist-type=array

# same flag different defaults
-etcd --pre-vote=true
+etcd --pre-vote=false

-etcd --logger=zap
+etcd --logger=capnslog
```

#### `etcd --logger zap` {#etcd---logger-zap}

3.4 по умолчанию равно `--logger=capnslog`, а 3.5 по умолчанию равно `--logger=zap`.

Если вы хотите продолжить использование `zap`, его нужно явно указать.

```diff
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

#### Разница в метриках Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in 3.4
-etcd_debugging_mvcc_db_compaction_last
```

### Проверки при понижении версии сервера {#server-downgrade-checklists}

#### Требования для понижения версии {#downgrade-requirements}

Для обеспечения плавного понижения версии кластер должен быть здоровым. Перед продолжением проверьте состояние кластера с помощью команды `etcdctl endpoint health`.

Понижение версии к 3.4 должно быть >= 3.4.32.

#### Подготовка {#preparation}

Перед понижением версии etcd всегда тестируйте сервисы, зависящие от etcd, в стендовой среде перед развертыванием понижения в производственную среду.

Перед началом, [скачайте резервную копию снимка](/ru/etcd/op-guide/maintenance/#snapshot-backup). Если что-то пойдет не так с понижением версии, возможно использование этой резервной копии для [восстановления](#rollback) обратно к существующей версии etcd. Пожалуйста, примечание: `snapshot` команда выполняет только резервное копирование v3 данных. Для v2 данных см. [восстановление v2 хранилища данных](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

Перед началом скачайте последний выпуск etcd 3.4, и убедитесь, что его версия >= 3.4.32.

#### Смешанные версии {#mixed-versions}

При децентрализации кластер etcd поддерживает смешанные версии участников etcd и работает с протоколом наименьшей общей версии. Кластер считается децентрализованным, если любой из его участников был децентрализован до версии 3.4. Внутри кластера участники переговариваются между собой для определения общей версии кластера, которая контролирует отчетываемую версию и поддерживаемые функции.

#### Ограничения {#limitations}

Примечание: если кластер содержит только данные версии 3 и нет данных версии 2, то он не подлежит этому ограничению.

Если кластер обслуживает набор данных версии v2 размером более 50MB, каждый новый участник, который был уменьшен в версии, может потребовать до двух минут для того, чтобы подтянуться до состояния существующего кластера. Проверьте размер последнего снимка, чтобы оценить общую величину данных. В противном случае, наиболее безопасно ждать 2 минут между уменьшением каждого участника.

Для значительно большего объема данных, превышающего 100MB или более , этот одноразовый процесс может занять еще больше времени. Администраторы очень больших кластеров etcd такого масштаба могут обратиться к команде [etcd][etcd-contact] перед устареванием, и мы с удовольствием предоставим рекомендации по процедуре.

#### Откат {#rollback}

Если какой-либо участник был уменьшен до 3.4, версия кластера будет уменьшена до 3.4, и операции будут "3.4" совместимы. Вам потребуется следовать инструкциям [Обновление etcd от 3.4 до 3.5](/ru/etcd/upgrades/upgrade_3_5/) для отката.

Пожалуйста, скачайте резервную копию снимка[ для того, чтобы возможность деинсталляции кластера была сохранена даже после его полной деинсталляции](/ru/etcd/op-guide/maintenance/#snapshot-backup).

### Приемник понижения версии {#downgrade-procedure}

Этот пример показывает, как понизить версию кластера etcd, работающего локально, состоящего из участника 3-члена 3.5.

#### Шаг 1: проверьте требования к понижению версии {#step-1-check-downgrade-requirements}

Я здоров и работает ли кластер 3.5.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
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

#### Шаг 2: скачать резервную копию снимка с лидера {#step-2-download-snapshot-backup-from-leader}

Загрузите резервную копию снимка[, ](/ru/etcd/op-guide/maintenance/#snapshot-backup) для обеспечения пути понижения версии в случае возникновения любых проблем.

#### Шаг 3: остановите один из существующих серверов etcd {#step-3-stop-one-existing-etcd-server}

Перед остановкой сервера проверьте, является ли он лидером

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |      true |      false |         2 |          9 |                  9 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         2 |          9 |                  9 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

Если сервер, который нужно остановить, является лидером, можно избежать некоторого времени простоя, перед остановкой этого сервера `move-leader` на другой сервер.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|    ENDPOINT     |        ID        | VERSION | DB SIZE | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.13 |   20 kB |      true |      false |         3 |         11 |                 11 |        |
| localhost:32379 | fd422379fda50e48 |  3.5.13 |   20 kB |     false |      false |         3 |         11 |                 11 |        |
+-----------------+------------------+---------+---------+-----------+------------+-----------+------------+--------------------+--------+
COMMENT
```

Когда процесс etcd останавливается, ожидаемые ошибки будут записаны другими участниками кластера. Это нормально, так как соединение участника было (временно) прервано:

```bash
{"level":"info","ts":"2024-05-14T20:25:47.051124Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"91bc3c398fb3c146 became leader at term 3"}
{"level":"info","ts":"2024-05-14T20:25:47.051139Z","logger":"raft","caller":"etcdserver/zap_raft.go:77","msg":"raft.node: 91bc3c398fb3c146 elected leader 91bc3c398fb3c146 at term 3"}

^C{"level":"warn","ts":"2024-05-14T20:27:09.094119Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream MsgApp v2","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.09427Z","caller":"rafthttp/stream.go:421","msg":"lost TCP streaming connection with remote peer","stream-reader-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269","error":"EOF"}
{"level":"warn","ts":"2024-05-14T20:27:09.095535Z","caller":"rafthttp/peer_status.go:66","msg":"peer became inactive (message send to peer failed)","peer-id":"8211f1d0f64f3269","error":"failed to dial 8211f1d0f64f3269 on stream MsgApp v2 (peer 8211f1d0f64f3269 failed to find local node 91bc3c398fb3c146)"}
{"level":"warn","ts":"2024-05-14T20:27:09.43915Z","caller":"rafthttp/stream.go:223","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"91bc3c398fb3c146","remote-peer-id":"8211f1d0f64f3269"}
{"level":"warn","ts":"2024-05-14T20:27:11.085646Z","caller":"etcdserver/cluster_util.go:294","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:11.085718Z","caller":"etcdserver/cluster_util.go:158","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2024-05-14T20:27:13.557385Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"416.079µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### Шаг 4: перезапустите сервер etcd с той же конфигурацией + `--next-cluster-version-compatible` {#step-4-restart-the-etcd-server-with-same-configuration----next-cluster-version-compatible}

Перезапустите сервер etcd с той же конфигурацией, но с новой версией бинарного файла etcd и `--next-cluster-version-compatible`.

```diff
-etcd-3.5/bin --name s1 \
+etcd-3.4/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
  --next-cluster-version-compatible
```

The новое 3.4 etcd будет публиковать информацию в кластер. В этот момент кластер начнет функционировать по протоколу 3.4, который является наименьшей общей версией.

```bash
> `{"level":"info","ts":"2024-05-13T21:05:43.981445Z","caller":"membership/cluster.go:561","msg":"set initial cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982188Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982312Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.0","from":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982376Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:44.000672Z","caller":"etcdserver/server.go:2152","msg":"published local member to cluster through raft","local-member-id":"8211f1d0f64f3269","local-member-attributes":"{Name:infra1 ClientURLs:[http://127.0.0.1:2379]}","request-path":"/0/members/8211f1d0f64f3269/attributes","cluster-id":"ef37ad9dc622a7c4","publish-timeout":"7s"}`

> `{"level":"info","ts":"2024-05-13T21:05:46.452631Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.5","from":"3.4"}`
```

Убедитесь, что с новым двоичным файлом etcd 3.4 каждый участник, а затем весь кластер становятся исправными:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Необновленные участники будут логировать информацию подобную следующей

```bash
{"level":"info","ts":"2024-05-13T21:05:46.450764Z","caller":"etcdserver/server.go:2633","msg":"updating cluster version using v2 API","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452419Z","caller":"membership/cluster.go:576","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452547Z","caller":"etcdserver/server.go:2652","msg":"cluster version is updated","cluster-version":"3.4"}
```

#### Шаг 5: повторите шаг 3 и шаг 4 для остальных участников {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

При сбое всех участников проверьте состояние здоровья и версию кластера:

```bash
endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 492.834µs
localhost:22379 is healthy: successfully committed proposal: took = 1.015025ms
localhost:32379 is healthy: successfully committed proposal: took = 1.853077ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.4.32","etcdcluster":"3.4.0"}
COMMENT
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
