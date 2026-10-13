---
title: Upgrade von etcd 3.0 auf 3.1
weight: 6850
description: Verfahren, Checklisten und Hinweise zum Upgrade von etcd 3.0 auf 3.1
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_1.md"
aliases: [/etcd/upgrades/upgrade_3_1/]
---

Im Allgemeinen kann das Upgrade von etcd 3.0 auf 3.1 als Rolling Upgrade ohne Ausfallzeit erfolgen:
 - Die etcd-v3.0-Prozesse nacheinander stoppen und durch etcd-v3.1-Prozesse ersetzen.
 - Sobald alle v3.1-Prozesse laufen, stehen dem Cluster die neuen Funktionen von v3.1 zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Upgrade beginnen](#upgrade-procedure).

### Checklisten für das Upgrade {#upgrade-checklists}

> [!WARNING]
> Bei der [Migration von v2 ohne v3-Daten](https://github.com/etcd-io/etcd/issues/9480) löst der etcd-Server v3.2+ eine Panic aus, wenn etcd aus vorhandenen Snapshots wiederhergestellt wird, aber keine v3-Datei `ETCD_DATA_DIR/member/snap/db` vorhanden ist. Dies tritt auf, wenn der Server von v2 migriert wurde, ohne zuvor v3-Daten zu enthalten. Dadurch wird auch ein versehentlicher Verlust von v3-Daten verhindert (z. B. könnte die Datei `db` verschoben worden sein). etcd verlangt, dass weitere Migrationen nach der Migration auf v3 nur mit v3-Daten erfolgen können. Führen Sie kein Upgrade auf neuere v3-Versionen durch, bevor der v3.0-Server v3-Daten enthält.

#### Überwachung {#monitoring}

Die folgenden Metriken aus v3.0.x sind zugunsten von [go-grpc-prometheus](https://github.com/grpc-ecosystem/go-grpc-prometheus) veraltet:

- `etcd_grpc_requests_total`
- `etcd_grpc_requests_failed_total`
- `etcd_grpc_active_streams`
- `etcd_grpc_unary_requests_duration_seconds`

#### Upgrade-Voraussetzungen {#upgrade-requirements}

Um eine bestehende etcd-Installation auf 3.1 zu aktualisieren, muss der laufende Cluster Version 3.0 oder höher verwenden. Falls er eine ältere Version als 3.0 verwendet, führen Sie vor dem Upgrade auf 3.1 zunächst ein [Upgrade auf 3.0](/de/docs/etcd/upgrades/upgrade_3_0) durch.

Außerdem muss der laufende Cluster fehlerfrei sein, damit das Rolling Upgrade reibungslos verläuft. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl endpoint health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Upgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Upgrade in der Produktionsumgebung durchführen.

[Erstellen Sie vor Beginn ein Backup der etcd-Daten](/de/docs/etcd/op-guide/maintenance/#snapshot-backup). Falls beim Upgrade etwas schiefgeht, können Sie mit diesem Backup ein [Downgrade](#downgrade) auf die bestehende etcd-Version durchführen. Beachten Sie, dass der Befehl `snapshot` nur die v3-Daten sichert. Informationen zu v2-Daten finden Sie unter [Backup des v2-Datenspeichers](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore).

#### Gemischte Versionen {#mixed-versions}

Während des Upgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt erst als aktualisiert, wenn alle Mitglieder auf Version 3.1 aktualisiert wurden. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Einschränkungen {#limitations}

Hinweis: Wenn der Cluster nur v3-Daten und keine v2-Daten enthält, gilt diese Einschränkung nicht.

Wenn der Cluster einen v2-Datenbestand von mehr als 50MB bereitstellt, kann es bis zu zwei Minuten dauern, bis jedes neu aktualisierte Mitglied zum bestehenden Cluster aufgeschlossen hat. Prüfen Sie die Größe eines aktuellen Snapshots, um die Gesamtdatenmenge abzuschätzen. Anders ausgedrückt ist es am sichersten, zwischen den Upgrades der einzelnen Mitglieder jeweils 2 Minuten zu warten.

Bei einer deutlich größeren Gesamtdatenmenge von 100MB oder mehr kann dieser einmalige Vorgang noch länger dauern. Administratoren sehr großer etcd-Cluster dieser Größenordnung können vor dem Upgrade das [etcd-Team][etcd-contact] kontaktieren; wir beraten Sie gern zum Vorgehen.

#### Downgrade {#downgrade}

Wenn alle Mitglieder auf v3.1 aktualisiert wurden, wird der Cluster auf v3.1 aktualisiert; ein Downgrade aus diesem abgeschlossenen Zustand ist **nicht möglich**. Solange jedoch noch ein einziges Mitglied v3.0 verwendet, bleiben der Cluster und sein Betrieb auf „v3.0“. Aus diesem Zustand mit gemischten Versionen ist es möglich, auf allen Mitgliedern wieder eine etcd-v3.0-Binärdatei zu verwenden.

[Erstellen Sie ein Backup des Datenverzeichnisses](/de/docs/etcd/op-guide/maintenance#snapshot-backup) aller etcd-Mitglieder, um ein Downgrade des Clusters auch nach einem vollständig abgeschlossenen Upgrade zu ermöglichen.

### Upgrade-Verfahren {#upgrade-procedure}

Dieses Beispiel zeigt das Upgrade eines etcd-v3.0-Clusters mit 3 Mitgliedern, der auf einem lokalen Rechner läuft.

#### 1. Upgrade-Voraussetzungen prüfen {#1-check-upgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v3.0.x?

```
$ ETCDCTL_API=3 etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 6.600684ms
localhost:22379 is healthy: successfully committed proposal: took = 8.540064ms
localhost:32379 is healthy: successfully committed proposal: took = 8.763432ms

$ curl http://localhost:2379/version
{"etcdserver":"3.0.16","etcdcluster":"3.0.0"}
```

#### 2. Den bestehenden etcd-Prozess stoppen {#2-stop-the-existing-etcd-process}

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

```
2017-01-17 09:34:18.352662 I | raft: raft.node: 1640829d9eea5cfb elected leader 1640829d9eea5cfb at term 5
2017-01-17 09:34:18.359630 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.359679 W | etcdserver: cannot get the version of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
2017-01-17 09:34:18.548116 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream Message writer)
2017-01-17 09:34:19.147816 W | rafthttp: lost the TCP streaming connection with peer fd32987dcd0511e0 (stream MsgApp v2 writer)
2017-01-17 09:34:34.364907 W | etcdserver: failed to reach the peerURL(http://localhost:2380) of member fd32987dcd0511e0 (Get http://localhost:2380/version: dial tcp 127.0.0.1:2380: getsockopt: connection refused)
```

An dieser Stelle empfiehlt es sich, [ein Backup der etcd-Daten zu erstellen](/de/docs/etcd/op-guide/maintenance#snapshot-backup), um bei Problemen ein Downgrade durchführen zu können:

```
$ etcdctl snapshot save backup.db
```

#### 3. Die etcd-v3.1-Binärdatei einsetzen und den neuen etcd-Prozess starten {#3-drop-in-etcd-v31-binary-and-start-the-new-etcd-process}

Das neue etcd v3.1 veröffentlicht seine Informationen im Cluster:

```
2017-01-17 09:36:00.996590 I | etcdserver: published {Name:my-etcd-1 ClientURLs:[http://localhost:2379]} to cluster 46bc3ce73049e678
```

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.1-Binärdatei wieder fehlerfrei ist:

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:22379 is healthy: successfully committed proposal: took = 5.540129ms
localhost:32379 is healthy: successfully committed proposal: took = 7.321671ms
localhost:2379 is healthy: successfully committed proposal: took = 10.629901ms
```

Aktualisierte Mitglieder protokollieren Warnungen wie die folgenden, bis der gesamte Cluster aktualisiert ist. Dies ist zu erwarten und endet, sobald alle etcd-Cluster-Mitglieder auf v3.1 aktualisiert wurden:

```
2017-01-17 09:36:38.406268 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:38.406295 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
2017-01-17 09:36:42.407695 W | etcdserver: the local etcd version 3.0.16 is not up-to-date
2017-01-17 09:36:42.407730 W | etcdserver: member fd32987dcd0511e0 has a higher version 3.1.0
```

#### 4. Schritt 2 bis Schritt 3 für alle anderen Mitglieder wiederholen {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Abschluss {#5-finish}

Sobald alle Mitglieder aktualisiert wurden, meldet der Cluster den erfolgreichen Abschluss des Upgrades auf 3.1:

```
2017-01-17 09:37:03.100015 I | etcdserver: updating the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104263 N | etcdserver/membership: updated the cluster version from 3.0 to 3.1
2017-01-17 09:37:03.104374 I | etcdserver/api: enabled capabilities for version 3.1
```

```
$ ETCDCTL_API=3 /etcdctl endpoint health --endpoints=localhost:2379,localhost:22379,localhost:32379
localhost:2379 is healthy: successfully committed proposal: took = 2.312897ms
localhost:22379 is healthy: successfully committed proposal: took = 2.553476ms
localhost:32379 is healthy: successfully committed proposal: took = 2.516902ms
```

[etcd-contact]: https://groups.google.com/g/etcd-dev
