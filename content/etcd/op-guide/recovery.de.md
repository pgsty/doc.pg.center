---
title: "Recovery nach einem Totalausfall"
weight: 4275
description: "Snapshot- und Wiederherstellungsfunktionen von etcd v3"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/recovery.md"
---

etcd ist dafür ausgelegt, Rechnerausfälle zu verkraften. Ein etcd-Cluster erholt sich automatisch von vorübergehenden Ausfällen (z. B. Neustarts von Rechnern) und toleriert bei N Mitgliedern bis zu *(N-1)/2* dauerhafte Ausfälle. Fällt ein Mitglied dauerhaft aus, etwa durch einen Hardwaredefekt oder eine Datenbeschädigung auf dem Datenträger, verliert es den Zugriff auf den Cluster. Verliert der Cluster dauerhaft mehr als *(N-1)/2* Mitglieder, kommt es zum Totalausfall: Das Quorum geht unwiederbringlich verloren. Ohne Quorum kann der Cluster keinen Konsens mehr erreichen und daher keine weiteren Aktualisierungen annehmen.

Für die Recovery nach einem Totalausfall bietet etcd v3 Snapshot- und Wiederherstellungsfunktionen, mit denen sich der Cluster ohne Verlust von v3-Schlüsseldaten neu erstellen lässt. Zur Wiederherstellung von v2-Schlüsseln siehe das [v2-Administrationshandbuch][v2_recover].

[v2_recover]: https://etcd.io/docs/v2.3/admin_guide#disaster-recovery

## Einen Snapshot des Schlüsselraums erstellen {#snapshotting-the-keyspace}

Für die Wiederherstellung eines Clusters wird zunächst ein Snapshot des Schlüsselraums eines etcd-Mitglieds benötigt. Ein Snapshot kann entweder mit `etcdctl snapshot save` von einem laufenden Mitglied erstellt oder durch Kopieren der Datei `member/snap/db` aus einem etcd-Datenverzeichnis gewonnen werden. Der folgende Befehl speichert beispielsweise einen Snapshot des von `$ENDPOINT` bereitgestellten Schlüsselraums in der Datei `snapshot.db`:

```sh
$ ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
```

Bei einem Snapshot aus der Datei `member/snap/db` können Daten verloren gehen, die noch nicht in diese Datei geschrieben wurden, sich aber bereits im Ordner wal (Write-Ahead-Log) befinden.

## Status eines Snapshots {#status-of-a-snapshot}

Mit dem Befehl `etcdutl snapshot status` lässt sich ermitteln, welche Revision und welchen Hashwert ein Snapshot enthält:

```sh
$ etcdutl snapshot status snapshot.db -w table
+---------+----------+------------+------------+
|  HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+---------+----------+------------+------------+
| 7ef846e |   485261 |      11642 |      94 MB |
+---------+----------+------------+------------+
```

## Einen Cluster wiederherstellen {#restoring-a-cluster}

### Revisionsunterschied {#revision-difference}

Bei der Wiederherstellung eines Clusters können bestehende Clients feststellen, dass die Revision um viele Hundert oder Tausend zurückspringt. Ein Snapshot enthält nämlich nur die Datenhistorie bis zum Zeitpunkt seiner Erstellung, während der aktuelle Zustand bereits weiter fortgeschritten sein kann.

Dies ist besonders beim Betrieb von Kubernetes mit etcd problematisch. Dort können Controller und Operatoren sogenannte `informers` verwenden, die als lokale Caches dienen und über Watches über Aktualisierungen benachrichtigt werden. Die Wiederherstellung auf eine ältere Revision aktualisiert diese Caches möglicherweise nicht korrekt und kann dadurch unvorhersehbares und inkonsistentes Verhalten der Controller verursachen.

Bei der Wiederherstellung aus einem Snapshot wird dringend empfohlen, die nachfolgend beschriebene „Revisionserhöhung“ zu verwenden, wenn bekannte Nutzer der Watch-API vorhanden sind, lokale Kopien von etcd-Daten zwischengespeichert werden oder generell Kubernetes eingesetzt wird.

### Aus einem Snapshot wiederherstellen {#restoring-from-snapshot}

Zur Wiederherstellung eines Clusters genügt eine einzelne Snapshot-Datei "db". Eine Clusterwiederherstellung mit `etcdutl snapshot restore` erstellt neue etcd-Datenverzeichnisse; alle Mitglieder sollten denselben Snapshot verwenden. Bei der Wiederherstellung werden einige Snapshot-Metadaten überschrieben, insbesondere die Mitglieds-ID und die Cluster-ID. Das Mitglied verliert damit seine bisherige Identität. Dieses Überschreiben verhindert, dass das neue Mitglied versehentlich einem bestehenden Cluster beitritt. Um einen Cluster aus einem Snapshot zu starten, muss die Wiederherstellung daher einen neuen logischen Cluster erstellen.

Eine einfache Wiederherstellung lässt sich wie folgt ausführen:

```sh
$ etcdutl snapshot restore snapshot.db --data-dir output-dir
```

### Integritätsprüfungen {#integrity-checks}

Die Integrität eines Snapshots kann bei der Wiederherstellung optional geprüft werden. Ein mit `etcdctl snapshot save` erstellter Snapshot enthält einen Integritätshash, den `etcdutl snapshot restore` prüft. Wird der Snapshot aus dem Datenverzeichnis kopiert, fehlt dieser Hash; die Wiederherstellung ist dann nur mit `--skip-hash-check` möglich.


### Mit Revisionserhöhung wiederherstellen {#restoring-with-revision-bump}

Damit die Revisionen nach einer Wiederherstellung niemals zurückgehen, kann die Option `--bump-revision` angegeben werden. Sie nimmt eine 64-Bit-Ganzzahl entgegen, die angibt, wie viele Revisionen zur aktuellen Revision des Snapshots addiert werden sollen. Da jeder Schreibzugriff auf etcd die Revision um eins erhöht, kann eine Erhöhung um 1'000'000'000 einen eine Woche alten Snapshot abdecken, sofern etcd weniger als 1500 Schreibzugriffe pro Sekunde verarbeitet.

Im Zusammenhang mit Kubernetes-Controllern ist es wichtig, mit `--mark-compacted` auch alle Revisionen einschließlich der Erhöhung als kompaktiert zu markieren. Dies stellt sicher, dass alle Watches beendet werden und etcd keine Anfragen zu Revisionen beantwortet, die nach der Snapshot-Erstellung entstanden sind. Dadurch werden die Informer-Caches effektiv ungültig.

Ein vollständiger Aufruf kann so aussehen:

```sh
$ etcdutl snapshot restore snapshot.db --bump-revision 1000000000 --mark-compacted --data-dir output-dir
```

### Mit aktualisierter Mitgliedschaft wiederherstellen {#restoring-with-updated-membership}

Die Mitglieder eines etcd-Clusters werden in etcd selbst gespeichert und über den Raft-Konsensalgorithmus verwaltet. Ist das Quorum vollständig verloren, kann neu entschieden werden, wo und wie der neue Cluster gebildet wird, beispielsweise mit vollständig neuen Mitgliedern.

Bei der Wiederherstellung aus einem Snapshot kann die neue Mitgliedschaft wie folgt direkt in den Datenspeicher übernommen werden:

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
```

Dies stellt sicher, dass sich der neu aufgebaute Cluster ausschließlich mit den anderen wiederhergestellten Mitgliedern mit dem angegebenen Token verbindet und nicht mit älteren Mitgliedern, die möglicherweise noch laufen und Verbindungen aufzubauen versuchen.

Alternativ kann beim Start von etcd `--force-new-cluster` angegeben werden, um die Clustermitgliedschaft zu überschreiben und vorhandene Anwendungsdaten beizubehalten. Davon wird jedoch dringend abgeraten, da dies eine Panic auslöst, wenn andere Mitglieder des vorherigen Clusters noch laufen. Unbedingt regelmäßig Snapshots speichern.


### End-2-End-Beispiel {#end-2-end-example}

Einen Snapshot von einem laufenden Cluster erstellen:

```sh
$ etcdctl snapshot save snapshot.db
```

Aufbauend auf dem vorherigen Beispiel werden im Folgenden neue etcd-Datenverzeichnisse (`m1.etcd`, `m2.etcd`, `m3.etcd`) für einen Cluster mit drei Mitgliedern erstellt:

```sh
$ etcdutl snapshot restore snapshot.db \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host1:2380
$ etcdutl snapshot restore snapshot.db \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host2:2380
$ etcdutl snapshot restore snapshot.db \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380 \
  --initial-cluster-token etcd-cluster-1 \
  --initial-advertise-peer-urls http://host3:2380
```

Anschließend `etcd` mit den neuen Datenverzeichnissen starten:

```sh
$ etcd \
  --name m1 \
  --data-dir m1_data_dir.etcd \
  --listen-client-urls http://host1:2379 \
  --advertise-client-urls http://host1:2379 \
  --listen-peer-urls http://host1:2380 &
$ etcd \
  --name m2 \
  --data-dir m2_data_dir.etcd \
  --listen-client-urls http://host2:2379 \
  --advertise-client-urls http://host2:2379 \
  --listen-peer-urls http://host2:2380 &
$ etcd \
  --name m3 \
  --data-dir m3_data_dir.etcd \
  --listen-client-urls http://host3:2379 \
  --advertise-client-urls http://host3:2379 \
  --listen-peer-urls http://host3:2380 &
```

Der wiederhergestellte etcd-Cluster sollte nun verfügbar sein und den Schlüsselraum aus dem Snapshot bereitstellen.

Ab etcd v3.6 kann `etcdctl` nur zum Erstellen eines Snapshots der Daten verwendet werden; zur Wiederherstellung aus einem Snapshot dient `etcdutl`. Wird `--data-dir` nicht angegeben, ist der Standardwert von `--data-dir` gleich `<name>.etcd`, wobei `<name>` dem Wert von `--name` entspricht. Wurde beispielsweise `--data-dir` nicht angegeben und heißen die Mitglieder `m1`, `m2` und `m3`, lauten die `--data-dir`-Verzeichnisse `m1.etcd`, `m2.etcd` und `m3.etcd`.
