---
title: Downgrade von etcd v3.6 auf v3.5
weight: 6650
description: Verfahren, Checklisten und Hinweise zum Downgrade von etcd v3.6 auf v3.5
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_6.md"
aliases: [/etcd/downgrades/downgrade_3_6/]
---

Im Allgemeinen kann das Downgrade von etcd v3.6 auf v3.5 als schrittweises Downgrade ohne Ausfallzeit erfolgen:

- Die etcd-v3.6-Prozesse nacheinander stoppen und durch etcd-v3.5-Prozesse ersetzen.
- Nach dem Aktivieren des Downgrades stehen dem Cluster die neuen Funktionen von v3.6 nicht mehr zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Downgrade beginnen](#downgrade-procedure).

### Checklisten für das Downgrade {#downgrade-checklists}

Wichtige inkompatible Änderungen von v3.6 auf v3.5:

#### Unterschiede bei Flags {#difference-in-flags}

Wenn Sie eines der folgenden Flags in Ihren v3.6-Konfigurationen verwenden, entfernen Sie es beim Downgrade auf v3.5, benennen Sie es um oder ändern Sie den Standardwert entsprechend.

> [!NOTE]
> Der Vergleich basiert auf den Versionen v3.6.0 und v.3.5.18. Die tatsächlichen Unterschiede hängen von Ihrer Patch-Version ab; prüfen Sie sie zunächst mit `diff <(etcd-3.6/bin/etcd -h | grep \\-\\-) <(etcd-3.5/bin/etcd -h | grep \\-\\-)`.

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

#### Unterschiede bei Prometheus-Metriken {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.5
-etcd_network_known_peers
-etcd_server_feature_enabled
```

### Checklisten für das Server-Downgrade {#server-downgrade-checklists}

#### Downgrade-Voraussetzungen {#downgrade-requirements}

Damit das schrittweise Downgrade reibungslos verläuft, muss der laufende Cluster fehlerfrei sein. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Downgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Downgrade in der Produktionsumgebung durchführen.

[Laden Sie vor Beginn das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Downgrade etwas schiefgeht, können Sie mit diesem Backup ein [Rollback](#rollback) auf die bestehende etcd-Version durchführen.

Laden Sie vor Beginn das neueste Release von etcd v3.5 herunter.

#### Gemischte Versionen {#mixed-versions}

Während des Downgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt als heruntergestuft, sobald das Downgrade mit `etcdctl downgrade enable 3.5` aktiviert wurde. Intern wird die Gesamtversion des Clusters auf die Zielversion des Downgrades gesetzt, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Rollback {#rollback}

Erstellen Sie vor dem Downgrade Ihres etcd-Clusters ein Snapshot-Backup des Clusters und [laden Sie es herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Mit diesem Snapshot lässt sich der Cluster bei Bedarf in seinen Zustand vor dem Downgrade zurückversetzen. Falls während des Downgrades Probleme auftreten, sollten Benutzer zunächst deren Ursache ermitteln und beheben.

Wenn das Downgrade nach Ausführung von `etcdctl downgrade enable` begonnen hat und sich der Cluster noch in einem Zustand mit gemischten Versionen befindet, also mindestens ein Mitglied weiterhin v3.6 verwendet, können Benutzer das laufende Downgrade durch Ausführen von `etcdctl downgrade cancel` abbrechen und alle heruntergestuften Mitglieder mit den ursprünglichen v3.6-Binärdateien neu starten.

Sobald alle Mitglieder auf v3.5 heruntergestuft wurden, gilt das Downgrade des Clusters als vollständig abgeschlossen. Wenn Benutzer danach zur ursprünglichen Version zurückkehren möchten, sollten sie dem offiziellen [Upgrade-Leitfaden](/de/docs/etcd/upgrades/upgrade_3_6/) folgen, um Konsistenz zu gewährleisten und Datenbeschädigungen zu vermeiden.

### Downgrade-Verfahren {#downgrade-procedure}

Dieses Beispiel zeigt das Downgrade eines etcd-v3.6-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft.

#### Schritt 1: Downgrade-Voraussetzungen prüfen {#step-1-check-downgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.6.x?

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

#### Schritt 2: Snapshot-Backup vom Leader herunterladen {#step-2-download-snapshot-backup-from-leader}

[Laden Sie das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup), um das Downgrade bei Problemen rückgängig machen zu können.

#### Schritt 3: Zielversion des Downgrades validieren {#step-3-validate-downgrade-target-version}

Validieren Sie die Zielversion des Downgrades, bevor Sie das Downgrade aktivieren:

- Wir unterstützen nur Downgrades um jeweils eine Nebenversion. Ein Downgrade von v3.6 auf v3.4 ist beispielsweise nicht zulässig.
- Fahren Sie erst mit dem nächsten Schritt fort, wenn die Validierung erfolgreich war.

```bash
etcdctl downgrade validate 3.5
<<COMMENT
Downgrade validate success, cluster version 3.6
COMMENT
```

#### Schritt 4: Downgrade aktivieren {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.5
<<COMMENT
Downgrade enable success, cluster version 3.6
COMMENT
```

Nach dem Aktivieren des Downgrades beginnt der Cluster, das Protokoll von v3.5 zu verwenden, der Zielversion des Downgrades. Außerdem migriert etcd das Schema automatisch auf die Zielversion des Downgrades, was normalerweise sehr schnell geschieht. Prüfen Sie den Endpunktstatus und bestätigen Sie, dass die Speicherversion aller Server auf v3.5 migriert wurde, bevor Sie mit dem nächsten Schritt fortfahren.

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
> Sobald das Downgrade aktiviert wurde, verwendet der Cluster weiterhin das Protokoll von v3.5, auch wenn auf allen Servern noch die v3.6-Binärdatei läuft, sofern das Downgrade nicht mit `etcdctl downgrade cancel` abgebrochen wird.

#### Schritt 5: Einen bestehenden etcd-Server stoppen {#step-5-stop-one-existing-etcd-server}

Prüfen Sie vor dem Stoppen des Servers, ob er der Leader ist. Wir empfehlen, den Leader zuletzt herunterzustufen.

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

Wenn der zu stoppende Server der Leader ist, können Sie einen Teil der Ausfallzeit vermeiden, indem Sie vor dem Stoppen dieses Servers mit `move-leader` die Führungsrolle auf einen anderen Server übertragen.

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

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

```bash
{"level":"warn","ts":"2025-02-28T17:35:43.795069Z","caller":"etcdserver/cluster_util.go:259","msg":"failed to reach the peer URL","address":"http://127.0.0.1:12380/version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:43.795149Z","caller":"etcdserver/cluster_util.go:160","msg":"failed to get version","remote-member-id":"8211f1d0f64f3269","error":"Get \"http://127.0.0.1:12380/version\": dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368651Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_SNAPSHOT","remote-peer-id":"8211f1d0f64f3269","rtt":"483.01µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
{"level":"warn","ts":"2025-02-28T17:35:44.368726Z","caller":"rafthttp/probing_status.go:68","msg":"prober detected unhealthy status","round-tripper-name":"ROUND_TRIPPER_RAFT_MESSAGE","remote-peer-id":"8211f1d0f64f3269","rtt":"735.659µs","error":"dial tcp 127.0.0.1:12380: connect: connection refused"}
```

#### Schritt 6: Den etcd-Server mit derselben Konfiguration neu starten (ohne die in v3.5 entfernten oder ersetzten Flags) {#step-6-restart-the-etcd-server-with-same-configuration-minus-the-flags-that-are-removed-or-replaced-in-v35}

Starten Sie den etcd-Server mit derselben Konfiguration, aber mit der neuen etcd-Binärdatei neu.

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

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.5-Binärdatei wieder fehlerfrei ist:

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
> Beim v3.5-Server wird `DOWNGRADE ENABLED` als false angezeigt, weil die Downgrade-Informationen im Statusendpunkt von v3.5 nicht implementiert sind. Für den Cluster ist das Downgrade zu diesem Zeitpunkt weiterhin aktiviert.

#### Schritt 7: *Schritt 5* und *Schritt 6* für die übrigen Mitglieder wiederholen {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

Sobald alle Mitglieder heruntergestuft wurden, prüfen Sie den Zustand und Status des Clusters und bestätigen Sie, dass die Nebenversion aller Mitglieder v3.5 und die Speicherversion leer ist:

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

Im Protokoll des Leaders sollten Sie eine Meldung ähnlich der folgenden sehen können:

```bash
{"level":"info","ts":"2025-02-28T17:59:50.019862Z","caller":"etcdserver/server.go:2749","msg":"the cluster has been downgraded","cluster-version":"3.5.0"}
```
