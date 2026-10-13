---
title: "Wartung"
weight: 4450
description: "Anleitung zur regelmäßigen Wartung von etcd-Clustern"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/maintenance.md"
aliases: [/etcd/op-guide/maintenance/]
---

## Überblick {#overview}

Ein etcd-Cluster muss regelmäßig gewartet werden, um zuverlässig zu bleiben. Je nach Anforderungen der etcd-Anwendung lässt sich diese Wartung gewöhnlich automatisieren und ohne Ausfallzeiten oder erhebliche Leistungseinbußen durchführen.

Alle Wartungsaufgaben in etcd dienen der Verwaltung der Speicherressourcen, die der etcd-Schlüsselraum belegt. Speicherplatzkontingente sichern gegen eine unzureichende Begrenzung der Schlüsselraumgröße ab: Wird der Speicherplatz eines etcd-Mitglieds knapp, löst ein Kontingent clusterweite Alarme aus, die das System in einen Wartungsmodus mit eingeschränktem Funktionsumfang versetzen. Damit weiterhin Platz für Schreibzugriffe auf den Schlüsselraum vorhanden ist, muss dessen Historie kompaktiert werden. Der Speicherplatz selbst kann durch Defragmentierung der etcd-Mitglieder zurückgewonnen werden. Regelmäßige Snapshot-Backups des Zustands eines etcd-Mitglieds ermöglichen schließlich die Wiederherstellung nach unbeabsichtigtem logischem Datenverlust oder nach Datenbeschädigungen durch Bedienfehler.

## Aufbewahrung des Raft-Logs {#raft-log-retention}

`etcd --snapshot-count` legt fest, wie viele angewendete Raft-Einträge vor der Kompaktierung im Arbeitsspeicher gehalten werden. Sobald `--snapshot-count` erreicht ist, speichert der Server zunächst die Snapshot-Daten dauerhaft auf dem Datenträger und entfernt anschließend alte Einträge. Fordert ein langsamer Follower Logs vor einem kompaktierten Index an, sendet der Leader den Snapshot und zwingt den Follower damit, seinen Zustand zu überschreiben.

Ein höherer Wert für `--snapshot-count` hält bis zum Snapshot mehr Raft-Einträge im Arbeitsspeicher und verursacht damit eine [wiederkehrend höhere Speichernutzung](https://github.com/kubernetes/kubernetes/issues/60589#issuecomment-371977156). Da der Leader die neuesten Raft-Einträge länger aufbewahrt, hat ein langsamer Follower mehr Zeit, vor dem nächsten Snapshot des Leaders aufzuschließen. `--snapshot-count` stellt somit einen Kompromiss zwischen höherem Speicherbedarf und besserer Verfügbarkeit langsamer Follower dar.

In v3.2 wurde der Standardwert von `--snapshot-count` [von 10,000 auf 100,000 geändert](https://github.com/etcd-io/etcd/pull/7160). In v3.7.0 beträgt der Standardwert 10,000.

Werte von `--snapshot-count` über 100,000 können den Schreibdurchsatz beeinträchtigen. Eine größere Anzahl von Objekten im Arbeitsspeicher kann die [Markierungsphase des Go-GC, `runtime.scanobject`](https://golang.org/src/runtime/mgc.go), verlangsamen; eine seltene Speicherfreigabe verlangsamt außerdem die Speicherzuweisung. Die Leistung hängt von Arbeitslast und Systemumgebung ab. Generell beeinträchtigt eine zu häufige Kompaktierung jedoch Clusterverfügbarkeit und Schreibdurchsatz. Eine zu seltene Kompaktierung ist ebenfalls schädlich, da sie den Garbage Collector von Go zu stark belastet. Weitere Untersuchungsergebnisse bietet [Leistungsaspekte von etcd und Raft verstehen](https://www.slideshare.net/mitakeh/understanding-performance-aspects-of-etcd-and-raft).

## Kompaktierung der Historie: Schlüssel-Wert-Datenbank der v3-API {#history-compaction-v3-api-key-value-database}

Da etcd eine genaue Historie seines Schlüsselraums führt, sollte diese regelmäßig kompaktiert werden, um Leistungseinbußen und letztlich eine Erschöpfung des Speicherplatzes zu vermeiden. Die Kompaktierung der Schlüsselraumhistorie entfernt alle Informationen zu Schlüsseln, die vor einer bestimmten Revision des Schlüsselraums ersetzt wurden. Der von diesen Schlüsseln belegte Platz steht danach für weitere Schreibzugriffe auf den Schlüsselraum zur Verfügung.

Der Schlüsselraum lässt sich automatisch mit der zeitfensterbasierten Aufbewahrungsrichtlinie von `etcd` oder manuell mit `etcdctl` kompaktieren. `etcdctl` ermöglicht eine genaue Steuerung der Kompaktierung; die automatische Kompaktierung eignet sich für Anwendungen, die die Schlüsselhistorie nur für einen bestimmten Zeitraum benötigen.

Eine mit `etcdctl` ausgelöste Kompaktierung funktioniert wie folgt:

```sh
# compact up to revision 3
$ etcdctl compact 3
```

Revisionen vor der Kompaktierungsrevision sind danach nicht mehr zugänglich:

```sh
$ etcdctl get --rev=2 somekey
Error:  rpc error: code = 11 desc = etcdserver: mvcc: required revision has been compacted
```

### Automatische Kompaktierung {#auto-compaction}

`etcd` lässt sich mit den Optionen `--auto-compaction-mode` und `--auto-compaction-retention` so konfigurieren, dass es den Schlüsselraum automatisch kompaktiert. Es gibt zwei Kompaktierungsmodi: `periodic` (Standard) und `revision`.

#### Periodische Kompaktierung {#periodic-compaction}

Die periodische Kompaktierung bewahrt ein zeitbasiertes Fenster der Schlüsselraumhistorie auf:

```sh
# keep one hour of history
$ etcd --auto-compaction-retention=1h
```

Der Aufbewahrungswert legt fest, wie viel Historie erhalten bleibt. Ein Datensatz wird erst ungefähr diese Zeitspanne nach seiner Erstellung kompaktiert. Dadurch können langsame Watcher innerhalb des Aufbewahrungsfensters noch aufschließen.

Ist die Aufbewahrungsdauer größer als 1 Stunde, kompaktiert etcd stündlich und behält dabei das vollständige Aufbewahrungsfenster bei. Beträgt die Aufbewahrungsdauer 1 Stunde oder weniger, erfolgt die Kompaktierung im Abstand dieser Dauer.

Bei `--auto-compaction-retention=10h` wartet etcd beispielsweise 10 Stunden bis zur ersten Kompaktierung und kompaktiert danach stündlich:

```text
0hr  (rev = 1)
1hr  (rev = 10)
...
8hr  (rev = 80)
9hr  (rev = 90)
10hr (rev = 100, Compact(1))
11hr (rev = 110, Compact(10))
...
```

Die empfohlenen Werte hängen vom Anwendungsfall ab:

- Häufige Aktualisierungen derselben Schlüssel: ein kurzer Zeitraum wie `1h` oder `30m`
- Seltene Aktualisierungen: ein längerer Zeitraum wie `24h`, `48h` oder `72h`
- Allgemeiner Standardwert: `10h`

#### Revisionsbasierte Kompaktierung {#revision-compaction}

Die revisionsbasierte Kompaktierung bewahrt eine feste Anzahl von Revisionen auf:

```sh
# keep 1000 revisions
$ etcd --auto-compaction-mode=revision --auto-compaction-retention=1000
```

etcd prüft alle 5 Minuten und kompaktiert bei `"latest revision" - 1000`. Ist die neueste Revision beispielsweise 30000, erfolgt die Kompaktierung bei Revision 29000.

## Defragmentierung {#defragmentation}

Nach der Kompaktierung des Schlüsselraums kann die Backend-Datenbank intern fragmentiert sein. Interne Fragmentierung bezeichnet Platz, den das Backend wiederverwenden kann, der aber weiterhin Speicherplatz belegt. Beim Kompaktieren alter Revisionen entstehen Lücken in der Backend-Datenbank, wodurch `etcd` intern fragmentiert wird. Fragmentierter Platz steht `etcd` zur Verfügung, dem Dateisystem des Hosts jedoch nicht. Das Löschen von Anwendungsdaten gibt also keinen Speicherplatz auf dem Datenträger frei.

Die Defragmentierung gibt diesen Speicherplatz an das Dateisystem zurück. Sie wird für jedes Mitglied einzeln ausgelöst, um clusterweite Latenzspitzen vermeiden zu können.

Ein etcd-Mitglied mit dem Befehl `etcdctl defrag` defragmentieren:

```sh
$ etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
```

> [!WARNING]
> Die Defragmentierung eines laufenden Mitglieds blockiert während des Neuaufbaus seines Zustands alle Lese- und Schreibzugriffe auf Daten.

> [!WARNING]
> Eine Defragmentierungsanfrage wird nicht im Cluster repliziert, sondern nur auf dem lokalen Knoten ausgeführt. Alle Mitglieder mit der Option `--endpoints` angeben oder mit `--cluster` alle Clustermitglieder automatisch ermitteln lassen.

Defragmentierung für alle Endpunkte des Clusters ausführen, zu dem der Standardendpunkt gehört:

```bash
$ etcdctl defrag --cluster
Finished defragmenting etcd member[http://127.0.0.1:2379]
Finished defragmenting etcd member[http://127.0.0.1:22379]
Finished defragmenting etcd member[http://127.0.0.1:32379]
```

Um ein etcd-Datenverzeichnis direkt zu defragmentieren, während etcd nicht läuft, folgenden Befehl verwenden:

```sh
etcdutl defrag --data-dir <path-to-etcd-data-dir>
```

## Speicherplatzkontingent {#space-quota}

Das Speicherplatzkontingent in `etcd` stellt einen zuverlässigen Clusterbetrieb sicher. Ohne ein solches Kontingent kann `etcd` bei einem übermäßig großen Schlüsselraum an Leistung verlieren oder schlicht den gesamten Speicherplatz aufbrauchen, was zu unvorhersehbarem Clusterverhalten führt. Überschreitet die Backend-Datenbank des Schlüsselraums eines beliebigen Mitglieds das Kontingent, löst `etcd` einen clusterweiten Alarm aus. Dieser versetzt den Cluster in einen Wartungsmodus, der nur das Lesen und Löschen von Schlüsseln erlaubt. Erst nachdem genügend Platz im Schlüsselraum freigegeben, die Backend-Datenbank defragmentiert und der Kontingentalarm aufgehoben wurde, kann der Cluster den normalen Betrieb wieder aufnehmen.

Standardmäßig verwendet `etcd` ein konservatives Speicherplatzkontingent, das für die meisten Anwendungen geeignet ist. Es lässt sich jedoch auf der Befehlszeile in Bytes konfigurieren:

```sh
# set a very small 16 MiB quota
$ etcd --quota-backend-bytes=$((16*1024*1024))
```

Das Kontingent lässt sich mit einer Schleife ausschöpfen:

```sh
# fill keyspace
$ while [ 1 ]; do dd if=/dev/urandom bs=1024 count=1024  | ETCDCTL_API=3 etcdctl put key  || break; done
...
Error:  rpc error: code = 8 desc = etcdserver: mvcc: database space exceeded
# confirm quota space is exceeded
$ ETCDCTL_API=3 etcdctl --write-out=table endpoint status
+----------------+------------------+-----------+---------+-----------+-----------+------------+
|    ENDPOINT    |        ID        |  VERSION  | DB SIZE | IS LEADER | RAFT TERM | RAFT INDEX |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
| 127.0.0.1:2379 | bf9071f4639c75cc | 2.3.0+git | 18 MB   | true      |         2 |       3332 |
+----------------+------------------+-----------+---------+-----------+-----------+------------+
# confirm alarm is raised
$ ETCDCTL_API=3 etcdctl alarm list
memberID:13803658152347727308 alarm:NOSPACE
```

Durch das Entfernen überflüssiger Daten aus dem Schlüsselraum und die Defragmentierung der Backend-Datenbank liegt der Cluster wieder innerhalb des Kontingents:

```sh
# get current revision
$ rev=$(ETCDCTL_API=3 etcdctl --endpoints=:2379 endpoint status --write-out="json" | egrep -o '"revision":[0-9]*' | egrep -o '[0-9].*')
# compact away all old revisions
$ ETCDCTL_API=3 etcdctl compact $rev
compacted revision 1516
# defragment away excessive space
$ ETCDCTL_API=3 etcdctl defrag
Finished defragmenting etcd member[127.0.0.1:2379]
# disarm alarm
$ ETCDCTL_API=3 etcdctl alarm disarm
memberID:13803658152347727308 alarm:NOSPACE
# test puts are allowed again
$ ETCDCTL_API=3 etcdctl put newkey 123
OK
```

Die Metrik `etcd_mvcc_db_total_size_in_use_in_bytes` zeigt die tatsächliche Datenbankbelegung nach einer Kompaktierung der Historie. `etcd_debugging_mvcc_db_total_size_in_bytes` zeigt dagegen die Datenbankgröße einschließlich freien Platzes, der noch auf Defragmentierung wartet. Letztere steigt nur, wenn Erstere nahe an ihr liegt. Nähern sich beide Metriken dem Kontingent, ist daher eine Kompaktierung der Historie erforderlich, um das Auslösen des Speicherplatzkontingents zu vermeiden.

Ab v3.4 heißt `etcd_debugging_mvcc_db_total_size_in_bytes` nun `etcd_mvcc_db_total_size_in_bytes`.

> [!WARNING]
> Eine Put/Txn/LeaseGrant-Anfrage kann den Fehler `ErrGRPCNoSpace` zurückgeben, obwohl der Schreibzugriff im Backend erfolgreich ist. etcd prüft das Speicherplatzkontingent sowohl auf der API-Schicht als auch auf der internen Apply-Schicht. Die Apply-Schicht löst lediglich den Alarm `NOSPACE` aus, ohne die weitere Ausführung der Transaktion zu blockieren.

## Snapshot-Backup {#snapshot-backup}

Regelmäßige Snapshots des `etcd`-Clusters dienen als dauerhaftes Backup des etcd-Schlüsselraums. Durch regelmäßige Snapshots der Backend-Datenbank eines etcd-Mitglieds lässt sich ein `etcd`-Cluster auf einen Zeitpunkt mit einem nachweislich intakten Zustand zurücksetzen.

Ein Snapshot wird mit `etcdctl` erstellt:

```sh
$ etcdctl snapshot save backup.db
$ etcdutl --write-out=table snapshot status backup.db
+----------+----------+------------+------------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE |
+----------+----------+------------+------------+
| fe01cf57 |       10 |          7 | 2.1 MB     |
+----------+----------+------------+------------+
```
