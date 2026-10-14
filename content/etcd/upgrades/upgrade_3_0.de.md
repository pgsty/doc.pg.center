---
title: Upgrade von etcd 2.3 auf 3.0
weight: 6900
description: Verfahren, Checklisten und Hinweise zum Upgrade von etcd 2.3 auf 3.0
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/upgrades/upgrade_3_0.md"
---

Im Allgemeinen kann das Upgrade von etcd 2.3 auf 3.0 als Rolling Upgrade ohne Ausfallzeit erfolgen:
 - Die etcd-v2.3-Prozesse nacheinander stoppen und durch etcd-v3.0-Prozesse ersetzen.
 - Sobald alle v3.0-Prozesse laufen, stehen dem Cluster die neuen Funktionen von v3.0 zur Verfügung.

Lesen Sie zur Vorbereitung den Rest dieses Leitfadens, bevor Sie [mit dem Upgrade beginnen](#upgrade-procedure).

### Checklisten für das Upgrade {#upgrade-checklists}

> [!WARNING]
> Bei der [Migration von v2 ohne v3-Daten](https://github.com/etcd-io/etcd/issues/9480) löst der etcd-Server v3.2+ eine Panic aus, wenn etcd aus vorhandenen Snapshots wiederhergestellt wird, aber keine v3-Datei `ETCD_DATA_DIR/member/snap/db` vorhanden ist. Dies tritt auf, wenn der Server von v2 migriert wurde, ohne zuvor v3-Daten zu enthalten. Dadurch wird auch ein versehentlicher Verlust von v3-Daten verhindert (z. B. könnte die Datei `db` verschoben worden sein). etcd verlangt, dass weitere Migrationen nach der Migration auf v3 nur mit v3-Daten erfolgen können. Führen Sie kein Upgrade auf neuere v3-Versionen durch, bevor der v3.0-Server v3-Daten enthält.

#### Upgrade-Voraussetzungen {#upgrade-requirements}

Um eine bestehende etcd-Installation auf 3.0 zu aktualisieren, muss der laufende Cluster Version 2.3 oder höher verwenden. Falls er eine ältere Version als 2.3 verwendet, aktualisieren Sie vor dem Upgrade auf 3.0 zunächst auf [2.3](https://github.com/etcd-io/etcd/releases/tag/v2.3.8).

Außerdem muss der laufende Cluster fehlerfrei sein, damit das Rolling Upgrade reibungslos verläuft. Prüfen Sie den Zustand des Clusters mit dem Befehl `etcdctl cluster-health`, bevor Sie fortfahren.

#### Vorbereitung {#preparation}

Testen Sie vor einem etcd-Upgrade immer die von etcd abhängigen Dienste in einer Staging-Umgebung, bevor Sie das Upgrade in der Produktionsumgebung durchführen.

[Erstellen Sie vor Beginn ein Backup des etcd-Datenverzeichnisses](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore). Falls beim Upgrade etwas schiefgeht, können Sie mit diesem Backup ein [Downgrade](#downgrade) auf die bestehende etcd-Version durchführen.

#### Gemischte Versionen {#mixed-versions}

Während des Upgrades unterstützt ein etcd-Cluster Mitglieder mit gemischten etcd-Versionen und verwendet das Protokoll der niedrigsten gemeinsamen Version. Der Cluster gilt erst als aktualisiert, wenn alle Mitglieder auf Version 3.0 aktualisiert wurden. Intern handeln die etcd-Mitglieder untereinander die Gesamtversion des Clusters aus, die die gemeldete Version und die unterstützten Funktionen bestimmt.

#### Einschränkungen {#limitations}

Bei einer Gesamtdatenmenge von mehr als 50MB kann es bis zu 2 Minuten dauern, bis das neu aktualisierte Mitglied zum bestehenden Cluster aufgeschlossen hat. Prüfen Sie die Größe eines aktuellen Snapshots, um die Gesamtdatenmenge abzuschätzen. Anders ausgedrückt ist es am sichersten, zwischen den Upgrades der einzelnen Mitglieder jeweils 2 Minuten zu warten.

Bei einer deutlich größeren Gesamtdatenmenge von 100MB oder mehr kann dieser einmalige Vorgang noch länger dauern. Administratoren sehr großer etcd-Cluster dieser Größenordnung können vor dem Upgrade das [etcd-Team][etcd-contact] kontaktieren; wir beraten Sie gern zum Vorgehen.

#### Downgrade {#downgrade}

Wenn alle Mitglieder auf v3.0 aktualisiert wurden, wird der Cluster auf v3.0 aktualisiert; ein Downgrade aus diesem abgeschlossenen Zustand ist **nicht möglich**. Solange jedoch noch ein einziges Mitglied v2.3 verwendet, bleiben der Cluster und sein Betrieb auf „v2.3“. Aus diesem Zustand mit gemischten Versionen ist es möglich, auf allen Mitgliedern wieder eine etcd-v2.3-Binärdatei zu verwenden.

[Erstellen Sie ein Backup des Datenverzeichnisses](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore) aller etcd-Mitglieder, um ein Downgrade des Clusters auch nach einem vollständig abgeschlossenen Upgrade zu ermöglichen.

### Upgrade-Verfahren {#upgrade-procedure}

Dieses Beispiel beschreibt das Upgrade eines etcd-v2.3-Clusters mit drei Mitgliedern, der auf einem lokalen Rechner läuft.

#### 1. Upgrade-Voraussetzungen prüfen. {#1-check-upgrade-requirements}

Ist der Cluster fehlerfrei und läuft er mit v.2.3.x?

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy

$ curl http://localhost:2379/version
{"etcdserver":"2.3.x","etcdcluster":"2.3.8"}
```

#### 2. Den bestehenden etcd-Prozess stoppen {#2-stop-the-existing-etcd-process}

Wenn ein etcd-Prozess gestoppt wird, protokollieren die anderen Cluster-Mitglieder erwartete Fehler. Dies ist normal, da die Verbindung zu einem Cluster-Mitglied (vorübergehend) unterbrochen wurde:

```
2016-06-27 15:21:48.624124 E | rafthttp: failed to dial 8211f1d0f64f3269 on stream Message (dial tcp 127.0.0.1:12380: getsockopt: connection refused)
2016-06-27 15:21:48.624175 I | rafthttp: the connection with 8211f1d0f64f3269 became inactive
```

An dieser Stelle empfiehlt es sich, [ein Backup des etcd-Datenverzeichnisses zu erstellen](https://etcd.io/docs/v2.3/admin_guide#backing-up-the-datastore), um bei Problemen ein Downgrade durchführen zu können:

```
$ etcdctl backup \
      --data-dir /var/lib/etcd \
      --backup-dir /tmp/etcd_backup
```

#### 3. Die etcd-v3.0-Binärdatei einsetzen und den neuen etcd-Prozess starten {#3-drop-in-etcd-v30-binary-and-start-the-new-etcd-process}

Das neue etcd v3.0 veröffentlicht seine Informationen im Cluster:

```
09:58:25.938673 I | etcdserver: published {Name:infra1 ClientURLs:[http://localhost:12379]} to cluster 524400597fb1d5f6
```

Prüfen Sie, ob jedes Mitglied und anschließend der gesamte Cluster mit der neuen etcd-v3.0-Binärdatei wieder fehlerfrei ist:

```
$ etcdctl cluster-health
member 6e3bd23ae5f1eae0 is healthy: got healthy result from http://localhost:22379
member 924e2e83e93f2560 is healthy: got healthy result from http://localhost:32379
member 8211f1d0f64f3269 is healthy: got healthy result from http://localhost:12379
cluster is healthy
```


Aktualisierte Mitglieder protokollieren Warnungen wie die folgenden, bis der gesamte Cluster aktualisiert ist. Dies ist zu erwarten und endet, sobald alle etcd-Cluster-Mitglieder auf v3.0 aktualisiert wurden:

```
2016-06-27 15:22:05.679644 W | etcdserver: the local etcd version 2.3.7 is not up-to-date
2016-06-27 15:22:05.679660 W | etcdserver: member 8211f1d0f64f3269 has a higher version 3.0.0
```

#### 4. Schritt 2 bis Schritt 3 für alle anderen Mitglieder wiederholen {#4-repeat-step-2-to-step-3-for-all-other-members}

#### 5. Abschluss {#5-finish}

Sobald alle Mitglieder aktualisiert wurden, meldet der Cluster den erfolgreichen Abschluss des Upgrades auf 3.0:

```
2016-06-27 15:22:19.873751 N | membership: updated the cluster version from 2.3 to 3.0
2016-06-27 15:22:19.914574 I | api: enabled capabilities for version 3.0.0
```

```
$ ETCDCTL_API=3 etcdctl endpoint health
127.0.0.1:12379 is healthy: successfully committed proposal: took = 18.440155ms
127.0.0.1:32379 is healthy: successfully committed proposal: took = 13.651368ms
127.0.0.1:22379 is healthy: successfully committed proposal: took = 18.513301ms
```

## Weitere Hinweise {#further-considerations}

- Die Umgebungsvariablen von etcdctl wurden aktualisiert. Wenn `ETCDCTL_API=2 etcdctl cluster-health` ordnungsgemäß funktioniert, aber `ETCDCTL_API=3 etcdctl endpoints health` mit `Error:  grpc: timed out when dialing` antwortet, verwenden Sie unbedingt die [neuen Variablennamen](https://github.com/etcd-io/etcd/tree/main/etcdctl#etcdctl).

## Bekannte Probleme {#known-issues}

- etcd &lt; v3.1 funktioniert nicht ordnungsgemäß, wenn es mit Go &gt; v1.7 gebaut wurde. Weitere Informationen finden Sie in [Issue 6951](https://github.com/etcd-io/etcd/issues/6951).
- Wenn in den etcd-Serverprotokollen ein Fehler wie `transport: http2Client.notifyError got notified that the client transport was broken unexpected EOF.` erscheint, stellen Sie sicher, dass etcd als vorgefertigtes Release vorliegt oder mit (etcd v3.1+ &amp; go v1.7+) oder (etcd &lt;v3.1 &amp; go v1.6.x) gebaut wurde.
- Das Hinzufügen eines v3-Knotens zu einem v2.3-Cluster während des Upgrades wird nicht unterstützt und könnte Panics auslösen. Weitere Informationen finden Sie in [Issue 7249](https://github.com/etcd-io/etcd/issues/7429). Gemischte Versionen von etcd-Mitgliedern sind nur während der v3-Migration zulässig. Schließen Sie die Upgrades ab, bevor Sie die Mitgliedschaft ändern.

[etcd-contact]: https://groups.google.com/g/etcd-dev
