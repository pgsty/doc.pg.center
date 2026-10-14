---
title: Downgrade von etcd v3.7 auf v3.6
weight: 6600
description: Verfahren, Checklisten und Hinweise zum Downgrade von etcd v3.7 auf v3.6
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/downgrades/downgrade_3_7.md"
---

Im Allgemeinen kann das Downgrade von etcd v3.7 auf v3.6 als schrittweises Downgrade ohne Ausfallzeit erfolgen:

- Die etcd-v3.7-Prozesse nacheinander stoppen und durch etcd-v3.6-Prozesse ersetzen.
- Nach dem Aktivieren des Downgrades stehen dem Cluster die neuen Funktionen von v3.7 nicht mehr zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Downgrade beginnen](#downgrade-procedure).

### Checklisten für das Downgrade {#downgrade-checklists}

Wichtige Unterschiede zwischen v3.7 und v3.6:

#### Unterschiede bei Flags {#difference-in-flags}

v3.7 führt keine neuen Flags ein. Ein v3.6-Prozess akzeptiert daher jedes Flag einer v3.7-Konfiguration, und beim Downgrade sind keine Konfigurationsänderungen erforderlich.

> [!NOTE]
> Der Vergleich basiert auf den Versionen v3.7.0-rc.0 und v3.6.13. Die tatsächlichen Unterschiede hängen von Ihrer Patch-Version ab; prüfen Sie sie zunächst mit `diff <(etcd-3.7/bin/etcd -h | grep \\-\\-) <(etcd-3.6/bin/etcd -h | grep \\-\\-)`.

Die veralteten `--experimental-*`-Flags, die in v3.7 entfernt wurden, sind in v3.6 noch vorhanden. Fügen Sie sie nach dem Downgrade jedoch nicht wieder hinzu; verwenden Sie ihre nicht experimentellen Gegenstücke oder `--feature-gates`-Einträge, die in beiden Versionen funktionieren.

#### Unterschiede bei Prometheus-Metriken {#difference-in-prometheus-metrics}

```diff
# metrics not available in v3.6
-etcd_server_request_duration_seconds
-etcd_debugging_server_watch_send_loop_control_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_progress_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_seconds
-etcd_debugging_server_watch_send_loop_watch_stream_duration_per_event_seconds
```

### Checklisten für das Server-Downgrade {#server-downgrade-checklists}

#### Downgrade-Voraussetzungen {#downgrade-requirements}

Damit das schrittweise Downgrade reibungslos verläuft, muss der laufende Cluster fehlerfrei sein. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Downgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Downgrade in der Produktionsumgebung durchführen.

[Laden Sie vor Beginn das Snapshot-Backup herunter](/de/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Downgrade etwas schiefgeht, können Sie mit diesem Backup ein [Rollback](#rollback) auf die bestehende etcd-Version durchführen.

Laden Sie vor Beginn das neueste Release von etcd v3.6 herunter.

#### Gemischte Versionen {#mixed-versions}

Während des Downgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt als heruntergestuft, sobald das Downgrade mit `etcdctl downgrade enable 3.6` aktiviert wurde. Intern wird die Gesamtversion des Clusters auf die Zielversion des Downgrades gesetzt, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Rollback {#rollback}

Erstellen Sie vor dem Downgrade Ihres etcd-Clusters ein Snapshot-Backup des Clusters und [laden Sie es herunter](/de/etcd/op-guide/maintenance/#snapshot-backup). Mit diesem Snapshot lässt sich der Cluster bei Bedarf in seinen Zustand vor dem Downgrade zurückversetzen. Falls während des Downgrades Probleme auftreten, sollten Benutzer zunächst deren Ursache ermitteln und beheben.

Wenn das Downgrade nach Ausführung von `etcdctl downgrade enable` begonnen hat und sich der Cluster noch in einem Zustand mit gemischten Versionen befindet, also mindestens ein Mitglied weiterhin v3.7 verwendet, können Benutzer das laufende Downgrade durch Ausführen von `etcdctl downgrade cancel` abbrechen und alle heruntergestuften Mitglieder mit den ursprünglichen v3.7-Binärdateien neu starten.

Sobald alle Mitglieder auf v3.6 heruntergestuft wurden, gilt das Downgrade des Clusters als vollständig abgeschlossen. Wenn Benutzer danach zur ursprünglichen Version zurückkehren möchten, sollten sie dem offiziellen [Upgrade-Leitfaden](/de/etcd/upgrades/upgrade_3_7/) folgen, um Konsistenz zu gewährleisten und Datenbeschädigungen zu vermeiden.

### Downgrade-Verfahren {#downgrade-procedure}

Dieses Beispiel zeigt das Downgrade eines etcd-v3.7-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft. Die folgende Ausgabe stammt aus einem tatsächlichen Durchlauf mit etcd v3.7.0-rc.0 und etcd v3.6.13 auf einem einzelnen Host mit drei Loopback-Ports; der Cluster war kurz zuvor von v3.6.13 aktualisiert worden.

#### Schritt 1: Downgrade-Voraussetzungen prüfen {#step-1-check-downgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.7.x?

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

#### Schritt 2: Snapshot-Backup vom Leader herunterladen {#step-2-download-snapshot-backup-from-leader}

[Laden Sie das Snapshot-Backup herunter](/de/etcd/op-guide/maintenance/#snapshot-backup), um das Downgrade bei Problemen rückgängig machen zu können:

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

#### Schritt 3: Zielversion des Downgrades validieren {#step-3-validate-downgrade-target-version}

Validieren Sie die Zielversion des Downgrades, bevor Sie das Downgrade aktivieren:

- Wir unterstützen nur Downgrades um jeweils eine Nebenversion. Ein Downgrade von v3.7 auf v3.5 ist beispielsweise nicht zulässig.
- Fahren Sie erst mit dem nächsten Schritt fort, wenn die Validierung erfolgreich war.

```bash
etcdctl downgrade validate 3.6
<<COMMENT
Downgrade validate success, cluster version 3.7
COMMENT
```

#### Schritt 4: Downgrade aktivieren {#step-4-enable-downgrade}

```bash
etcdctl downgrade enable 3.6
<<COMMENT
Downgrade enable success, cluster version 3.7
COMMENT
```

Nach dem Aktivieren des Downgrades beginnt der Cluster, das Protokoll von v3.6 zu verwenden, der Zielversion des Downgrades. Außerdem migriert etcd das Schema automatisch auf die Zielversion des Downgrades, was normalerweise sehr schnell geschieht. Prüfen Sie den Endpunktstatus und bestätigen Sie, dass die Speicherversion aller Server auf v3.6 migriert wurde, bevor Sie mit dem nächsten Schritt fortfahren.

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
> Sobald das Downgrade aktiviert wurde, verwendet der Cluster weiterhin das Protokoll von v3.6, auch wenn auf allen Servern noch die v3.7-Binärdatei läuft, sofern das Downgrade nicht mit `etcdctl downgrade cancel` abgebrochen wird.

#### Schritt 5: Einen bestehenden etcd-Server stoppen {#step-5-stop-one-existing-etcd-server}

Prüfen Sie vor dem Stoppen des Servers, ob er der Leader ist. Wir empfehlen, den Leader zuletzt herunterzustufen. Wenn der zu stoppende Server der Leader ist, können Sie einen Teil der Ausfallzeit vermeiden, indem Sie vor dem Stoppen dieses Servers mit `move-leader` die Führungsrolle auf einen anderen Server übertragen.

```bash
etcdctl --endpoints=localhost:2379,localhost:22379,localhost:32379 move-leader 729934363faa4a24
<<COMMENT
Leadership transferred from 7339c4e5e833c029 to 729934363faa4a24
COMMENT
```

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

```bash
{"level":"warn","ts":"2026-07-02T06:48:14.518460+0300","caller":"rafthttp/stream.go:227","msg":"lost TCP streaming connection with remote peer","stream-writer-type":"stream Message","local-member-id":"7339c4e5e833c029","remote-peer-id":"729934363faa4a24"}
{"level":"warn","ts":"2026-07-02T06:48:15.913169+0300","caller":"etcdserver/cluster_util.go:261","msg":"failed to reach the peer URL","address":"http://localhost:22380/version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:15.913364+0300","caller":"etcdserver/cluster_util.go:162","msg":"failed to get version","remote-member-id":"729934363faa4a24","error":"Get \"http://localhost:22380/version\": dial tcp [::1]:22380: connect: connection refused"}
{"level":"warn","ts":"2026-07-02T06:48:16.856521+0300","caller":"version/monitor.go:212","msg":"remotes server has mismatching etcd version","remote-member-id":"b548c2511513015","current-server-version":"3.7.0","target-version":"3.6.0"}
```

#### Schritt 6: Den etcd-Server mit derselben Konfiguration neu starten {#step-6-restart-the-etcd-server-with-same-configuration}

Starten Sie den etcd-Server mit derselben Konfiguration, aber mit der etcd-v3.6-Binärdatei neu.

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

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der etcd-v3.6-Binärdatei wieder fehlerfrei ist:

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
> Anders als v3.5 meldet der Statusendpunkt von v3.6 die Downgrade-Informationen. Daher zeigen heruntergestufte Mitglieder bis zum Abschluss des Downgrades weiterhin `DOWNGRADE ENABLED` als true sowie ihre Speicherversion an.

#### Schritt 7: *Schritt 5* und *Schritt 6* für die übrigen Mitglieder wiederholen {#step-7-repeat-step-5-and-step-6-for-rest-of-the-members}

Sobald alle Mitglieder heruntergestuft wurden, wird das Downgrade automatisch abgeschlossen und `DOWNGRADE ENABLED` auf false zurückgesetzt. Prüfen Sie den Zustand und Status des Clusters und bestätigen Sie, dass die Nebenversion aller Mitglieder und die Speicherversion v3.6 sind:

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

Im Protokoll des Leaders sollten Sie eine Meldung ähnlich der folgenden sehen können:

```bash
{"level":"info","ts":"2026-07-02T06:48:32.312205+0300","caller":"version/monitor.go:143","msg":"the cluster has been downgraded","cluster-version":"3.6.0"}
```
