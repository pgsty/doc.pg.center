---
title: Понижение версии etcd с v3.6 до v3.5
weight: 6650
description: Процессы, контрольные списки и примечания по понижению версии etcd с v3.6 до v3.5
categories: [Задача]
upstream_link: "https://github.com/etcd-io/website/blob/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7/downgrades/downgrade_3_6.md"
aliases: [/etcd/downgrades/downgrade_3_6/]
---

В общем случае переход с etcd v3.6 на v3.5 можно выполнить как скользящее понижение версии без простоя:

- поочерёдно останавливать процессы etcd v3.6 и заменять их процессами etcd v3.5
- после включения понижения версии новые возможности v3.6 становятся недоступны кластеру

До [начала понижения версии](#downgrade-procedure) прочитайте оставшуюся часть руководства и подготовьтесь.

### Контрольные списки понижения версии {#downgrade-checklists}

Основные нарушающие совместимость изменения между v3.6 и v3.5:

#### Различия во флагах {#difference-in-flags}

Если в конфигурации v3.6 используются какие-либо из следующих флагов, при переходе на v3.5 обязательно удалите или переименуйте их либо измените значение по умолчанию.

> [!NOTE]
> Различия приведены для версий v3.6.0 и v.3.5.18. Фактический результат зависит от корректирующей версии; сначала проверьте его командой `diff <(etcd-3.6/bin/etcd -h | grep \\-\\-) <(etcd-3.5/bin/etcd -h | grep \\-\\-)`.

```diff
# flags not available in v3.5
-etcd --discovery-token ''
-etcd --discovery-endpoints ''
-etcd --discovery-dial-timeout '2s'
-etcd --discovery-request-timeout '5s'
-etcd --discovery-keepalive-time '2s'
-etcd --discovery-keepalive-timeout '6s'
-etcd --discovery-insecure-transport 'true'
-etcd --discovery-insecure-skip-tls-verify 'false'
-etcd --discovery-cert ''
-etcd --discovery-key ''
-etcd --discovery-cacert ''
-etcd --discovery-user ''
-etcd --discovery-password ''
-etcd --feature-gates
-etcd --log-format

# same flag with different names
-etcd --bootstrap-defrag-threshold-megabytes
+etcd --experimental-bootstrap-defrag-threshold-megabytes
-etcd --compaction-batch-limit
+etcd --experimental-compaction-batch-limit
-etcd --compact-hash-check-time
+etcd --experimental-compact-hash-check-time
-etcd --compaction-sleep-interval
+etcd --experimental-compaction-sleep-interval
-etcd --corrupt-check-time
+etcd --experimental-corrupt-check-time
-etcd --enable-distributed-tracing
+etcd --experimental-enable-distributed-tracing
-etcd --distributed-tracing-address
+etcd --experimental-distributed-tracing-address
-etcd --distributed-tracing-instance-id
+etcd --experimental-distributed-tracing-instance-id
-etcd --distributed-tracing-sampling-rate
+etcd --experimental-distributed-tracing-sampling-rate
-etcd --distributed-tracing-service-name
+etcd --experimental-distributed-tracing-service-name
-etcd --downgrade-check-time
+etcd --experimental-downgrade-check-time
-etcd --max-learners
+etcd --experimental-max-learners
-etcd --memory-mlock
+etcd --experimental-memory-mlock
-etcd --peer-skip-client-san-verification
+etcd --experimental-peer-skip-client-san-verification
-etcd --snapshot-catchup-entries
+etcd --experimental-snapshot-catchup-entries
-etcd --warning-apply-duration
+etcd --experimental-warning-apply-duration
-etcd --warning-unary-request-duration
+etcd --experimental-warning-unary-request-duration
-etcd --watch-progress-notify-interval
+etcd --experimental-watch-progress-notify-interval

# equivalent flags of v3.6 feature gates
-etcd --feature-gates=CompactHashCheck=true
+etcd --experimental-compact-hash-check-enabled=true
-etcd --feature-gates=InitialCorruptCheck=true
+etcd --experimental-enable-initial-corrupt-check=true
-etcd --feature-gates=LeaseCheckpoint=true
+etcd --experimental-enable-lease-checkpoint=true
-etcd --feature-gates=LeaseCheckpointPersist=true
+etcd --experimental-enable-lease-checkpoint-persist=true
-etcd --feature-gates=StopGRPCServiceOnDefrag=true
+etcd --experimental-stop-grpc-service-on-defrag=true
-etcd --feature-gates=TxnModeWriteWithSharedBuffer=false
+etcd --experimental-txn-mode-write-with-shared-buffer=false

# same flag different defaults
-etcd --snapshot-count=10000
+etcd --snapshot-count=100000
-etcd --v2-deprecation='write-only'
+etcd --v2-deprecation='not-yet'
-etcd --discovery-fallback='exit'
+etcd --discovery-fallback='proxy'

```

#### Различия в метриках Prometheus {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.5
-etcd_network_known_peers
-etcd_server_feature_enabled
```

### Контрольные списки понижения версии сервера {#server-downgrade-checklists}

#### Требования к понижению версии {#downgrade-requirements}

Для плавного скользящего понижения версии работающий кластер должен быть исправен. Перед продолжением проверьте его работоспособность командой `etcdctl endpoint health`.

#### Подготовка {#preparation}

Перед понижением версии etcd обязательно протестируйте зависящие от него службы в промежуточном окружении, прежде чем развёртывать изменение в рабочем окружении.

До начала [загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). Если при понижении версии возникнет проблема, эту копию можно использовать для [отката](#rollback) к существующей версии etcd.

До начала загрузите последний выпуск etcd v3.5.

#### Смешанные версии {#mixed-versions}

Во время понижения версии кластер etcd поддерживает участников разных версий и работает по протоколу наименьшей общей версии. Кластер считается переведённым на более старую версию после включения операции командой `etcdctl downgrade enable 3.5`. На внутреннем уровне общая версия кластера устанавливается равной целевой версии понижения и определяет сообщаемую версию и поддерживаемые возможности.

#### Откат {#rollback}

Перед понижением версии кластера etcd создайте и [загрузите его резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup). При необходимости снимок позволяет восстановить состояние кластера до обновления. Если во время понижения версии возникнут проблемы, сначала следует определить и устранить их первопричину.

Если понижение версии началось после выполнения `etcdctl downgrade enabled`, но кластер всё ещё находится в состоянии смешанных версий и хотя бы один участник остаётся на v3.6, текущую операцию можно отменить командой `etcdctl downgrade cancel`, а всех уже переведённых участников перезапустить с исходными двоичными файлами v3.6.

После перевода всех участников на v3.5 понижение версии кластера считается завершённым. Чтобы вернуться к исходной версии после полного понижения, необходимо следовать официальному [руководству по обновлению](/ru/docs/etcd/upgrades/upgrade_3_6/), обеспечивая согласованность и предотвращая повреждение данных.

### Процедура понижения версии {#downgrade-procedure}

В этом примере показано понижение версии работающего на локальной машине кластера etcd v3.6 из 3 участников.

#### Шаг 1: проверка требований к понижению версии {#step-1-check-downgrade-requirements}

Кластер исправен и использует v3.6.x?

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint health
<<COMMENT
localhost:2379 is healthy: successfully committed proposal: took = 2.118638ms
localhost:22379 is healthy: successfully committed proposal: took = 3.631388ms
localhost:32379 is healthy: successfully committed proposal: took = 2.157051ms
COMMENT

curl http://localhost:2379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:22379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

curl http://localhost:32379/version
<<COMMENT
{"etcdserver":"3.6.0-alpha.0","etcdcluster":"3.6.0","storage":"3.6.0"}
COMMENT

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         10 |                 10 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         10 |                 10 |        |                          |             false |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.6.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         10 |                 10 |        |                          |             false |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

#### Шаг 2: загрузка резервной копии снимка с лидера {#step-2-download-snapshot-backup-from-leader}

[Загрузите резервную копию снимка](/ru/docs/etcd/op-guide/maintenance/#snapshot-backup), чтобы обеспечить путь понижения версии при возникновении проблем.

#### Шаг 3: проверка целевой версии понижения {#step-3-validate-downgrade-target-version}

Перед включением понижения проверьте целевую версию:

- Поддерживается понижение только на одну дополнительную версию за раз. Например, переход с v3.6 на v3.4 недопустим.
- Не переходите к следующему шагу до успешного завершения проверки.

```bash
etcdctl downgrade validate 3.5
<<COMMENT
Downgrade validate success, cluster version 3.6
COMMENT
```

#### Шаг 4: включение понижения версии {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.5
<<COMMENT
Downgrade enable success, cluster version 3.6
COMMENT
```

После включения понижения кластер начнёт работать по протоколу v3.5 — целевой версии операции. Кроме того, etcd автоматически перенесёт схему на целевую версию, что обычно происходит очень быстро. Прежде чем переходить к следующему шагу, проверьте состояние конечных точек и убедитесь, что версия хранилища всех серверов изменена на v3.5.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

> [!NOTE]
> После включения понижения кластер продолжает работать по протоколу v3.5, даже если все серверы всё ещё используют двоичный файл v3.6, пока операция не отменена командой `etcdctl downgrade cancel`

#### Шаг 5: остановка одного существующего сервера etcd {#step-5-stop-one-existing-etcd-server}

Перед остановкой сервера проверьте, является ли он лидером. Рекомендуется понижать версию лидера последним.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         2 |         12 |                 12 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

Если останавливаемый сервер является лидером, часть простоя можно предотвратить, выполнив `move-leader` на другой сервер до остановки текущего.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 91bc3c398fb3c146

etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         13 |                 13 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT
```

При остановке каждого процесса etcd другие участники кластера записывают в журнал ожидаемые ошибки. Это нормально, поскольку соединение с участником кластера (временно) разорвано:

```bash
{"level":"warn","ts":"2025-02-28T17:35:43.795069Z","caller":"etcdserver/cluster_util.go:259","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:43.795149Z","caller":"etcdserver/cluster_util.go:160","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368651Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"483.01µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368726Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_RAFT_MESSAGE","remote-peer-id":"8211f1d0f64f3269","rtt":"735.659µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### Шаг 6: перезапуск сервера etcd с той же конфигурацией (за исключением удалённых или заменённых в v3.5 флагов) {#step-6-restart-the-etcd-server-with-same-configuration-minus-the-flags-that-are-removed-or-replaced-in-v35}

Перезапустите сервер etcd с прежней конфигурацией, но с новым двоичным файлом etcd.

```diff
-etcd-3.6/bin --name s1 \
+etcd-3.5/bin --name s1 \
  --data-dir /tmp/etcd/s1 \
  --listen-client-urls http://localhost:2379 \
  --advertise-client-urls http://localhost:2379 \
  --listen-peer-urls http://localhost:2380 \
  --initial-advertise-peer-urls http://localhost:2380 \
  --initial-cluster s1=http://localhost:2380,s2=http://localhost:22380,s3=http://localhost:32380 \
  --initial-cluster-token tkn \
  --initial-cluster-state existing
```

Убедитесь, что сначала каждый участник, а затем весь кластер становятся исправными с новым двоичным файлом etcd v3.5:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        |    VERSION    | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 |        3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         14 |                 14 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         14 |                 14 |        |                    3.5.0 |              true |
| localhost:32379 | fd422379fda50e48 | 3.6.0-alpha.0 |           3.5.0 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         14 |                 14 |        |                    3.5.0 |              true |
+-----------------+------------------+---------------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 4.650967ms
localhost:2379 is healthy: successfully committed proposal: took = 4.634377ms
localhost:32379 is healthy: successfully committed proposal: took = 5.047777ms
COMMENT
```

> [!NOTE]
> Для сервера v3.5 значение `DOWNGRADE ENABLED` равно false, поскольку сведения о понижении версии не реализованы в конечной точке состояния v3.5. На этом этапе понижение версии для кластера всё ещё включено.

#### Шаг 7: повторение *шага 5* и *шага 6* для остальных участников {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

После понижения версии всех участников проверьте работоспособность и состояние кластера, убедившись, что дополнительная версия всех участников равна v3.5, а версия хранилища пуста:

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 endpoint status -w=table
<<COMMENT
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|    ENDPOINT     |        ID        | VERSION | STORAGE VERSION | DB SIZE | IN USE | PERCENTAGE NOT IN USE | QUOTA | IS LEADER | IS LEARNER | RAFT TERM | RAFT INDEX | RAFT APPLIED INDEX | ERRORS | DOWNGRADE TARGET VERSION | DOWNGRADE ENABLED |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
|  localhost:2379 | 8211f1d0f64f3269 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         26 |                 26 |        |                          |             false |
| localhost:22379 | 91bc3c398fb3c146 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |      true |      false |         3 |         26 |                 26 |        |                          |             false |
| localhost:32379 | fd422379fda50e48 |  3.5.18 |                 |   20 kB |  16 kB |                   20% |   0 B |     false |      false |         3 |         26 |                 26 |        |                          |             false |
+-----------------+------------------+---------+-----------------+---------+--------+-----------------------+-------+-----------+------------+-----------+------------+--------------------+--------+--------------------------+-------------------+
COMMENT

etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:22379 is healthy: successfully committed proposal: took = 4.650967ms
localhost:2379 is healthy: successfully committed proposal: took = 4.634377ms
localhost:32379 is healthy: successfully committed proposal: took = 5.047777ms
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

В журнале лидера должно появиться сообщение, подобное следующему:

```bash
{"level":"info","ts":"2025-02-28T17:59:50.019862Z","caller":"etcdserver/server.go:2749","msg":"the cluster has been downgraded","cluster-version":"3.5.0"}
```
