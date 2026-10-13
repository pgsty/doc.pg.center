---
title: Upgrade von etcd v3.6 auf v3.7
weight: 6550
description: Verfahren, Checklisten und Hinweise zum Upgrade von etcd v3.6 auf v3.7
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_7.md"
aliases: [/etcd/upgrades/upgrade_3_7/]
---

Im Allgemeinen kann das Upgrade von etcd v3.6 auf v3.7 als Rolling Upgrade ohne Ausfallzeit erfolgen:

- Die etcd-v3.6-Prozesse nacheinander stoppen und durch etcd-v3.7-Prozesse ersetzen.
- Sobald alle v3.7-Prozesse laufen, stehen dem Cluster die neuen Funktionen von v3.7 zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Upgrade beginnen](#upgrade-procedure).

### Checklisten für das Upgrade {#upgrade-checklists}

#### 3.6 aktualisieren {#update-36}

> [!IMPORTANT]
> Stellen Sie vor dem Upgrade auf 3.7 sicher, dass alle Ihre 3.6-Mitglieder auf 3.6.11 oder höher aktualisiert sind. Frühere 3.6-Patch-Releases sind möglicherweise nicht mit einem Rolling Upgrade auf 3.7 kompatibel.

#### V2-Speicher {#v2-store}

Der v2-Speicher wurde in v3.7 vollständig entfernt. Die v2-HTTP-API (`--enable-v2`), die v2-auf-v3-Emulation (`--experimental-enable-v2v3`), der v2-Discovery-Dienst, das Paket `client/v2` und das Laden von v2-Snapshot-Dateien sind sämtlich entfallen. Siehe die Verweise auf inkompatible Änderungen in [CHANGELOG-3.7](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

Wenn Sie von einem 3.6-Cluster aktualisieren, sind diese Flags bereits nicht mehr vorhanden, und es sind keine Maßnahmen erforderlich. Wenn Sie von einem älteren Release mit benutzerdefinierten v2-Daten wechseln, folgen Sie vor dem Upgrade dem [v2-Migrationsleitfaden](https://etcd.io/docs/v3.4/op-guide/v2-migration/).

#### Go-Refactoring {#go-refactoring}

v3.7 enthält umfangreiche interne Umstrukturierungen, die normale Upgrades nicht betreffen, bei Upgrades benutzerdefinierter Integrationen jedoch berücksichtigt werden sollten:

- Migration von `gogo/protobuf` zur Standardimplementierung `google.golang.org/protobuf` (verfolgt in [#14533](https://github.com/etcd-io/etcd/issues/14533)).
- Migration der veralteten Bibliotheken für Protokollierung und Tags aus `go-grpc-middleware` v1 zu den v2-Interceptors ([#20420](https://github.com/etcd-io/etcd/pull/20420)).
- Die OpenTelemetry-gRPC-Interceptors wurden auf `otelgrpc` v0.61.0 aktualisiert; dabei wurden die veralteten `UnaryServerInterceptor` und `StreamServerInterceptor` durch `NewServerHandler` ersetzt ([#20017](https://github.com/etcd-io/etcd/pull/20017)).

Wenn Sie etcd als Bibliothek einbetten, gegen die `clientv3`-API bauen oder von internen Paketen abhängen, prüfen Sie vor dem Upgrade das [Änderungsprotokoll](https://github.com/etcd-io/etcd/blob/main/CHANGELOG/CHANGELOG-3.7.md).

### Entfernte Flags {#flags-removed}

Alle veralteten `--experimental-*`-Flags wurden in v3.7 entfernt ([#19959](https://github.com/etcd-io/etcd/pull/19959)). In v3.6 wurde jedes davon entweder durch ein gleichnamiges nicht experimentelles Flag oder durch einen `--feature-gates`-Eintrag ersetzt. Wenn Sie noch eines dieser Flags gesetzt haben, ersetzen Sie es **vor** dem Rolling Upgrade auf v3.7 durch die entsprechende v3.6-Variante; andernfalls kann der v3.7-Prozess nicht starten.

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

Die Zuordnung jedes entfernten Flags zu seinem nicht experimentellen Gegenstück oder `--feature-gates`-Eintrag finden Sie im [Upgrade-Leitfaden von v3.5 auf v3.6](/de/docs/etcd/upgrades/upgrade_3_6/).

### Hinzugefügte Flags {#flags-added}

Keine.

### Flags mit neuen Standardwerten {#flags-with-new-defaults}

Keine.

### Checklisten für das Server-Upgrade {#server-upgrade-checklists}

#### Upgrade-Voraussetzungen {#upgrade-requirements}

Um eine bestehende etcd-Installation auf v3.7 zu aktualisieren, muss der laufende Cluster v3.6.11 oder höher verwenden. Falls er eine ältere Nebenversion verwendet, führen Sie zunächst ein [Upgrade auf v3.6](/de/docs/etcd/upgrades/upgrade_3_6/) durch; etcd unterstützt nur Upgrades um jeweils eine Nebenversion.

Außerdem muss der laufende Cluster fehlerfrei sein, damit das Rolling Upgrade reibungslos verläuft. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Upgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Upgrade in der Produktionsumgebung durchführen.

[Laden Sie vor Beginn das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Upgrade etwas schiefgeht, können Sie mit diesem Backup ein [Rollback](#rollback) auf die bestehende etcd-Version durchführen.

#### Gemischte Versionen {#mixed-versions}

Während des Upgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt erst als aktualisiert, wenn alle Mitglieder auf Version v3.7 aktualisiert wurden. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Rollback {#rollback}

Erstellen Sie vor dem Upgrade Ihres etcd-Clusters ein Snapshot-Backup des Clusters und [laden Sie es herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Mit diesem Snapshot lässt sich der Cluster bei Bedarf in seinen Zustand vor dem Upgrade zurückversetzen. Falls während des Upgrades Probleme auftreten, sollten Benutzer zunächst deren Ursache ermitteln und beheben. Solange sich der Cluster noch in einem Zustand mit gemischten Versionen befindet, also mindestens ein Mitglied weiterhin v3.6 verwendet, können sie entweder die Binärdatei oder das Image durch die alte Version v3.6 ersetzen oder den Cluster direkt aus dem Snapshot wiederherstellen. In diesem gemischten Zustand arbeitet der Cluster weiterhin als v3.6-Cluster, sodass ein Rollback ohne formelles Downgrade-Verfahren möglich ist.

Sobald jedoch alle Mitglieder auf v3.7 aktualisiert wurden, gilt der Cluster als vollständig aktualisiert, und ein Rollback durch Austausch der Binärdateien ist nicht mehr möglich. Falls das Upgrade schiefgeht, bestehen in diesem Fall die einzigen Recovery-Möglichkeiten darin, den vor dem Upgrade erstellten Snapshot wiederherzustellen oder dem offiziellen [Downgrade-Leitfaden](/de/docs/etcd/downgrades/downgrading-etcd/) zu folgen.

### Upgrade-Verfahren {#upgrade-procedure}

Dieses Beispiel zeigt das Upgrade eines etcd-v3.6-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft. Die folgende Ausgabe stammt aus einem tatsächlichen Durchlauf mit etcd v3.6.12 und etcd v3.7.0-rc.0 auf einem einzelnen Host mit drei Loopback-Ports.

#### Schritt 1: Upgrade-Voraussetzungen prüfen {#step-1-check-upgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.6.11 oder höher?

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

#### Schritt 2: Snapshot-Backup vom Leader herunterladen {#step-2-download-snapshot-backup-from-leader}

[Laden Sie das Snapshot-Backup herunter](/de/docs/etcd/op-guide/maintenance/#snapshot-backup), um bei Problemen ein Downgrade durchführen zu können.

Der etcd-Leader enthält garantiert die neuesten Anwendungsdaten. Rufen Sie den Snapshot daher vom Leader ab:

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

#### Schritt 3: Einen bestehenden etcd-Server stoppen {#step-3-stop-one-existing-etcd-server}

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde. Der Leader überträgt die Führungsrolle, bevor er sich beendet:

```bash
{"level":"info","ts":"2026-06-02T07:01:54.949299+0300","caller":"etcdserver/server.go:1274","msg":"leadership transfer finished","local-member-id":"7339c4e5e833c029","old-leader-member-id":"7339c4e5e833c029","new-leader-member-id":"b548c2511513015","took":"101.052625ms"}
{"level":"info","ts":"2026-06-02T07:01:54.949369+0300","caller":"etcdserver/server.go:2349","msg":"server has stopped; stopping cluster version's monitor"}
{"level":"info","ts":"2026-06-02T07:01:55.503219+0300","caller":"embed/etcd.go:626","msg":"stopped serving peer traffic","address":"127.0.0.1:2380"}
```

#### Schritt 4: Den etcd-Server mit derselben Konfiguration neu starten {#step-4-restart-the-etcd-server-with-same-configuration}

Starten Sie den etcd-Server mit derselben Konfiguration, aber mit der neuen etcd-Binärdatei neu.

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

Das neue etcd v3.7 veröffentlicht seine Informationen im Cluster. Zu diesem Zeitpunkt verwendet der Cluster weiterhin das Protokoll von v3.6, der niedrigsten gemeinsamen Version.

> `{"level":"info","ts":"2026-06-02T07:01:58.920780+0300","caller":"membership/cluster.go:296","msg":"set cluster version from store","cluster-version":"3.6"}`
>
> `{"level":"info","ts":"2026-06-02T07:01:58.979186+0300","caller":"etcdserver/server.go:1828","msg":"published local member to cluster through raft","local-member-id":"7339c4e5e833c029","local-member-attributes":"{Name:s1 ClientURLs:[http://localhost:2379]}","cluster-id":"7dee9ba76d59ed53","publish-timeout":"7s"}`

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.7-Binärdatei wieder fehlerfrei ist:

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

Noch nicht aktualisierte Mitglieder und das aktualisierte Mitglied protokollieren Meldungen zum Zustand mit gemischten Versionen, bis der gesamte Cluster aktualisiert wurde. Dies ist zu erwarten und endet, sobald alle etcd-Cluster-Mitglieder auf v3.7 aktualisiert wurden.

#### Schritt 5: *Schritt 3* und *Schritt 4* für die übrigen Mitglieder wiederholen {#step-5-repeat-step-3-and-step-4-for-rest-of-the-members}

Sobald alle Mitglieder aktualisiert wurden, meldet der Cluster den erfolgreichen Abschluss des Upgrades auf v3.7:

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
