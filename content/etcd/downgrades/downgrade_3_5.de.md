---
title: Downgrade von etcd 3.5 auf 3.4
weight: 6700
description: Verfahren, Checklisten und Hinweise zum Downgrade von etcd 3.5 auf 3.4
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_5.md"
---

Im Allgemeinen kann das Downgrade von etcd 3.5 auf 3.4 als schrittweises Downgrade ohne Ausfallzeit erfolgen:

- Die etcd-3.5-Prozesse nacheinander stoppen und durch etcd-3.4-Prozesse ersetzen.
- Sobald ein 3.4-Prozess gestartet wurde, stehen dem Cluster die neuen Funktionen von 3.5 nicht mehr zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Downgrade beginnen](#downgrade-procedure).

### Checklisten für das Downgrade {#downgrade-checklists}


> [!WARNING]
> Wenn in Ihrem Cluster die Authentifizierung aktiviert ist, wird ein schrittweises Downgrade von 3.5 nicht unterstützt, da 3.5 [ein Format von WAL-Einträgen zur Authentifizierung ändert](https://github.com/etcd-io/etcd/pull/11943). Sie können den [Anweisungen zur Authentifizierung](/de/etcd/op-guide/authentication/rbac/) folgen, um zunächst die Authentifizierung zu deaktivieren und alle Benutzer zu löschen.

Wichtige inkompatible Änderungen von 3.5 auf 3.4:

#### Unterschiede bei Flags {#difference-in-flags}

Wenn Sie eines der folgenden Flags in Ihren 3.5-Konfigurationen verwenden, entfernen Sie es beim Downgrade auf 3.4, benennen Sie es um oder ändern Sie den Standardwert entsprechend.

> [!NOTE]
> Der Vergleich basiert auf den Versionen 3.5.14 und v.3.4.33. Die tatsächlichen Unterschiede hängen von Ihrer Patch-Version ab; prüfen Sie sie zunächst mit `diff <(etcd-3.5/bin/etcd -h | grep \\-\\-) <(etcd-3.4/bin/etcd -h | grep \\-\\-)`.

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

3.4 verwendet standardmäßig `--logger=capnslog`, während 3.5 standardmäßig `--logger=zap` verwendet.

Wenn Sie weiterhin `zap` verwenden möchten, müssen Sie es ausdrücklich angeben.

```diff
+etcd --logger=zap --log-outputs=stderr

+# to write logs to stderr and a.log file at the same time
+etcd --logger=zap --log-outputs=stderr,a.log
```

#### Unterschiede bei Prometheus-Metriken {#difference-in-prometheus-metrics}

```diff
# metrics not available in 3.4
-etcd_debugging_mvcc_db_compaction_last
```

### Checklisten für das Server-Downgrade {#server-downgrade-checklists}

#### Downgrade-Voraussetzungen {#downgrade-requirements}

Damit das schrittweise Downgrade reibungslos verläuft, muss der laufende Cluster fehlerfrei sein. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

Die 3.4-Version, auf die das Downgrade erfolgen soll, muss >= 3.4.32 sein.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Downgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Downgrade in der Produktionsumgebung durchführen.

[Laden Sie vor Beginn das Snapshot-Backup herunter](/de/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Downgrade etwas schiefgeht, können Sie mit diesem Backup ein [Rollback](#rollback) auf die bestehende etcd-Version durchführen. Beachten Sie, dass der Befehl `snapshot` nur die v3-Daten sichert. Informationen zu v2-Daten finden Sie unter [Backup des v2-Datenspeichers](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

Laden Sie vor Beginn das neueste Release von etcd 3.4 herunter und stellen Sie sicher, dass seine Version >= 3.4.32 ist.

#### Gemischte Versionen {#mixed-versions}

Während des Downgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt als heruntergestuft, sobald eines seiner Mitglieder auf Version 3.4 heruntergestuft wurde. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Einschränkungen {#limitations}

Hinweis: Wenn der Cluster nur v3-Daten und keine v2-Daten enthält, gilt diese Einschränkung nicht.

Wenn der Cluster einen v2-Datenbestand von mehr als 50MB bereitstellt, kann es bis zu zwei Minuten dauern, bis jedes neu heruntergestufte Mitglied zum bestehenden Cluster aufgeschlossen hat. Prüfen Sie die Größe eines aktuellen Snapshots, um die Gesamtdatenmenge abzuschätzen. Anders ausgedrückt ist es am sichersten, zwischen den Downgrades der einzelnen Mitglieder jeweils 2 Minuten zu warten.

Bei einer deutlich größeren Gesamtdatenmenge von 100MB oder mehr kann dieser einmalige Vorgang noch länger dauern. Administratoren sehr großer etcd-Cluster dieser Größenordnung können vor dem Downgrade das [etcd-Team][etcd-contact] kontaktieren; wir beraten Sie gern zum Vorgehen.

#### Rollback {#rollback}

Wenn ein Mitglied auf 3.4 heruntergestuft wurde, wird die Cluster-Version auf 3.4 heruntergestuft, und der Betrieb ist mit „3.4“ kompatibel. Für ein Rollback müssten Sie den Anweisungen zum [Upgrade von etcd 3.4 auf 3.5](/de/etcd/upgrades/upgrade_3_5/) folgen.

[Laden Sie das Snapshot-Backup herunter](/de/etcd/op-guide/maintenance/#snapshot-backup), um das Downgrade auch nach einem vollständig abgeschlossenen Downgrade des Clusters rückgängig machen zu können.

### Downgrade-Verfahren {#downgrade-procedure}

Dieses Beispiel zeigt das Downgrade eines etcd-3.5-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft.

#### Schritt 1: Downgrade-Voraussetzungen prüfen {#step-1-check-downgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit 3.5.x?

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

#### Schritt 2: Snapshot-Backup vom Leader herunterladen {#step-2-download-snapshot-backup-from-leader}

[Laden Sie das Snapshot-Backup herunter](/de/etcd/op-guide/maintenance/#snapshot-backup), um das Downgrade bei Problemen rückgängig machen zu können.

#### Schritt 3: Einen bestehenden etcd-Server stoppen {#step-3-stop-one-existing-etcd-server}

Prüfen Sie vor dem Stoppen des Servers, ob er der Leader ist.

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

Wenn der zu stoppende Server der Leader ist, können Sie einen Teil der Ausfallzeit vermeiden, indem Sie vor dem Stoppen dieses Servers mit `move-leader` die Führungsrolle auf einen anderen Server übertragen.

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

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

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

#### Schritt 4: Den etcd-Server mit derselben Konfiguration + `--next-cluster-version-compatible` neu starten {#step-4-restart-the-etcd-server-with-same-configuration----next-cluster-version-compatible}

Starten Sie den etcd-Server mit derselben Konfiguration, aber mit der neuen etcd-Binärdatei und `--next-cluster-version-compatible` neu.

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

Das neue etcd 3.4 veröffentlicht seine Informationen im Cluster. Zu diesem Zeitpunkt beginnt der Cluster, das Protokoll von 3.4 zu verwenden, der niedrigsten gemeinsamen Version.

```bash
> `{"level":"info","ts":"2024-05-13T21:05:43.981445Z","caller":"membership/cluster.go:561","msg":"set initial cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982188Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.0"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982312Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.0","from":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:43.982376Z","caller":"api/capability.go:77","msg":"enabled capabilities for version","cluster-version":"3.5"}`

> `{"level":"info","ts":"2024-05-13T21:05:44.000672Z","caller":"etcdserver/server.go:2152","msg":"published local member to cluster through raft","local-member-id":"8211f1d0f64f3269","local-member-attributes":"{Name:infra1 ClientURLs:[http://127.0.0.1:2379]}","request-path":"/0/members/8211f1d0f64f3269/attributes","cluster-id":"ef37ad9dc622a7c4","publish-timeout":"7s"}`

> `{"level":"info","ts":"2024-05-13T21:05:46.452631Z","caller":"membership/cluster.go:549","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"8211f1d0f64f3269","from":"3.5","from":"3.4"}`
```

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-3.4-Binärdatei wieder fehlerfrei ist:

```bash
etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
<<COMMENT
localhost:32379 is healthy: successfully committed proposal: took = 2.337471ms
localhost:22379 is healthy: successfully committed proposal: took = 1.130717ms
localhost:2379 is healthy: successfully committed proposal: took = 2.124843ms
COMMENT
```

Noch nicht heruntergestufte Mitglieder protokollieren Informationen wie die folgenden:

```bash
{"level":"info","ts":"2024-05-13T21:05:46.450764Z","caller":"etcdserver/server.go:2633","msg":"updating cluster version using v2 API","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452419Z","caller":"membership/cluster.go:576","msg":"updated cluster version","cluster-id":"ef37ad9dc622a7c4","local-member-id":"91bc3c398fb3c146","from":"3.5","to":"3.4"}
{"level":"info","ts":"2024-05-13T21:05:46.452547Z","caller":"etcdserver/server.go:2652","msg":"cluster version is updated","cluster-version":"3.4"}
```

#### Schritt 5: *Schritt 3* und *Schritt 4* für die übrigen Mitglieder wiederholen {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Sobald alle Mitglieder heruntergestuft wurden, prüfen Sie den Zustand und die Version des Clusters:

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
