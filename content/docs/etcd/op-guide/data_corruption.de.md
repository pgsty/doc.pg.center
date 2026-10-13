---
title: "Datenbeschädigung"
weight: 5000
description: "Datenbeschädigung und Recovery in etcd"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/data_corruption.md"
aliases: [/etcd/op-guide/data_corruption/]
---

etcd verfügt über eine integrierte automatische Erkennung von Datenbeschädigungen, damit die Zustände der Mitglieder nicht voneinander abweichen.

> [!NOTE]
> In etcd 3.7 die nachfolgenden Funktionsschalter und Optionen für Zeitintervalle verwenden. Die früheren experimentellen Optionen zur Prüfung auf Datenbeschädigungen wurden entfernt; siehe [Konfigurationsoptionen](/de/docs/etcd/op-guide/configuration/#feature-gates).

## Erkennung von Datenbeschädigungen aktivieren {#enabling-data-corruption-detection}

Datenbeschädigungen lassen sich mit folgenden Prüfungen erkennen:
* Anfangsprüfung, aktiviert mit der Option `--feature-gates=InitialCorruptCheck=true`.
* Regelmäßige Prüfung folgender Hashwerte:
  * Hashwert der kompaktierten Revision, aktiviert mit der Option `--feature-gates=CompactHashCheck=true`.
  * Hashwert der neuesten Revision, aktiviert mit der Option `--corrupt-check-time`.

Die Anfangsprüfung erfolgt während der Initialisierung des etcd-Mitglieds.
Das Mitglied vergleicht seinen persistenten Zustand mit dem der anderen Mitglieder und beendet sich bei einer Abweichung.

Beide regelmäßigen Prüfungen werden in einem bereits laufenden Cluster vom Leader ausgeführt.
Der Leader vergleicht seinen persistenten Zustand mit dem der anderen Mitglieder und löst bei einer Abweichung einen CORRUPT ALARM aus.
Beide Prüfungen dienen demselben Zweck. Es lohnt sich jedoch, beide zu aktivieren, um Leistung und Erkennungszeit gegeneinander abzuwägen.
* Prüfung des Hashwerts der kompaktierten Revision – erfordert regelmäßige Kompaktierung, verursacht minimale Leistungseinbußen und kommt mit langsamen Followern zurecht.
* Prüfung des Hashwerts der neuesten Revision – verursacht hohe Leistungseinbußen und kommt weder mit langsamen Followern noch mit häufigen Kompaktierungen zurecht.

### Hashwert der kompaktierten Revision prüfen {#compacted-revision-hash-check}

Bei Aktivierung mit der Option `--feature-gates=CompactHashCheck=true` wird die Prüfung einmal pro Minute ausgeführt.
Dies lässt sich mit der Option `--compact-hash-check-time` in folgendem Format anpassen: `1m` – jede Minute, `1h` – jede Stunde.
Diese Prüfung erweitert die Kompaktierung um die Berechnung einer Prüfsumme, die zwischen Clustermitgliedern verglichen werden kann.
Sie erfordert keinen zusätzlichen Datenbankscan und ist dadurch sehr kostengünstig, setzt aber eine regelmäßige Kompaktierung im Cluster voraus.

### Hashwert der neuesten Revision prüfen {#latest-revision-hash-check}

Die Aktivierung erfolgt mit der Option `--corrupt-check-time`; dabei muss ein Ausführungsintervall in folgendem Format angegeben werden: `1m` – jede Minute, `1h` – jede Stunde.
Wegen der hohen Leistungseinbußen wird ein Intervall von einigen Stunden empfohlen.
Für die Prüfung muss der gesamte etcd-Inhalt bei der angegebenen Revision gescannt werden, um eine Prüfsumme zu berechnen.

## Ein Mitglied mit beschädigten Daten wiederherstellen {#restoring-a-corrupted-member}

Es gibt drei Möglichkeiten, ein Mitglied mit beschädigten Daten wiederherzustellen:
* Persistenten Zustand des Mitglieds löschen
* Mitglied ersetzen
* Gesamten Cluster wiederherstellen

Nach der Wiederherstellung des Mitglieds kann der CORRUPT ALARM aufgehoben werden.

### Persistenten Zustand des Mitglieds löschen {#purge-member-persistent-state}

Der Zustand eines Mitglieds lässt sich wie folgt löschen:
1. Die etcd-Instanz stoppen.
2. Ein Backup des etcd-Datenverzeichnisses erstellen.
3. Das Unterverzeichnis `snap` aus dem etcd-Datenverzeichnis verschieben.
6. `etcd` mit `--initial-cluster-state=existing` und den in `--initial-cluster` aufgeführten Clustermitgliedern starten.

Das etcd-Mitglied sollte daraufhin einen aktuellen Snapshot vom Leader herunterladen.

### Mitglied ersetzen {#replace-member}

Ein Mitglied lässt sich wie folgt ersetzen:
1. Die etcd-Instanz stoppen.
2. Ein Backup des etcd-Datenverzeichnisses erstellen.
3. Das Datenverzeichnis entfernen.
4. Das Mitglied durch Ausführen von `etcdctl member remove` aus dem Cluster entfernen.
5. Es durch Ausführen von `etcdctl member add` wieder hinzufügen
6. `etcd` mit `--initial-cluster-state=existing` und den in `--initial-cluster` aufgeführten Clustermitgliedern starten.

### Gesamten Cluster wiederherstellen {#restore-whole-cluster}

Der Cluster lässt sich wiederherstellen, indem ein Snapshot des aktuellen Leaders gespeichert und auf allen Mitgliedern wiederhergestellt wird.
`etcdctl snapshot save` gegen den Leader ausführen und dem [Verfahren zur Wiederherstellung eines Clusters](/de/docs/etcd/op-guide/recovery/) folgen.
