---
title: "pgBackRest 2.59.3 Dokumentation"
linkTitle: pgBackRest
weight: 20
icon: fa-solid fa-couch
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
description: "Zuverlässige Backups und Wiederherstellung für PostgreSQL — Dokumentation und Referenz zu pgBackRest."
module: [PGBACKREST]
categories: [Konzept]
aliases: [/pgbackrest/]
upstream_source: pgbackrest
upstream_ref: v2.59.3
upstream_link: "https://pgbackrest.org/"
cascade:
  upstream_source: pgbackrest
  upstream_ref: v2.59.3
  type: docs
  module: [PGBACKREST]
---

--------

## Einführung {#introduction}

pgBackRest ist eine zuverlässige Lösung für Backups und Wiederherstellung mit PostgreSQL, die sich nahtlos bis zu den größten Datenbanken und Arbeitslasten skalieren lässt.

Diese Dokumentationskopie behandelt pgBackRest [v2.59.3](https://github.com/pgbackrest/pgbackrest/releases/tag/release/2.59.3). Versionshinweise stehen auf der Seite [Versionen](/de/docs/pgbackrest/release/).

Version 2.59.3 behebt die mögliche Erzeugung schwacher Verschlüsselungsunterschlüssel und Salts. Ein Upgrade ersetzt vorhandene schwache Unterschlüssel einer Stanza nicht; Prüfungen und Abhilfemaßnahmen finden Sie unter [Schwache Unterschlüssel und Salts bei der Verschlüsselung](/de/docs/pgbackrest/news/#weak-encryption).

Wenn Ihnen pgBackRest gefällt, geben Sie uns einen Stern auf [GitHub](https://github.com/pgbackrest/pgbackrest)!


--------

## Neuigkeiten {#news}

**4. Oktober 2026** - [Schwache Unterschlüssel und Salts bei der Verschlüsselung](/de/docs/pgbackrest/news/#weak-encryption)

**4. Oktober 2026** - [pgBackRest 2.59.3 veröffentlicht](/de/docs/pgbackrest/news/#release-2-59-3)

**27. September 2026** - [pgBackRest 2.59.2 veröffentlicht](/de/docs/pgbackrest/news/#release-2-59-2)


--------

## Sponsoren {#sponsors}

Ohne Sponsoring gäbe es pgBackRest nicht. Neue Funktionen zu entwickeln, Fehler zu beheben, Beiträge zu prüfen, Fragen aus der Community zu beantworten und das Projekt zu pflegen, erfordert viel Zeit. Wenn Sie pgBackRest in Ihrem Unternehmen einsetzen, ziehen Sie bitte ein [Sponsoring](https://github.com/sponsors/dwsteele) in Betracht.

Unsere Sponsoren: [AWS](https://aws.amazon.com), [Supabase](https://supabase.com), [pgEdge](https://pgedge.com), [Tiger Data](https://tigerdata.com), [Percona](https://percona.com), [Eon](https://eon.io), [Xata](https://xata.io), [Dalibo](https://dalibo.com) und [Data Egret](https://dataegret.com/).

Wir danken unseren Sponsoren für ihre Investitionen in Open-Source-Infrastruktur, die der gesamten PostgreSQL-Community zugutekommt.

Frühere Sponsoren: [Crunchy Data](https://crunchydata.com), [Resonate](https://resonate.com).


--------

## Funktionen {#features}


### Parallele Backups und Wiederherstellung {#parallel-backup--restore}

Die Komprimierung ist bei Backups meist der Engpass. pgBackRest löst dieses Problem durch parallele Verarbeitung und effizientere Komprimierungsalgorithmen wie `lz4` und `zstd`.


### Lokaler oder entfernter Betrieb {#local-or-remote-operation}

Ein eigenes Protokoll ermöglicht pgBackRest Backups, Wiederherstellung und Archivierung lokal oder über TLS/SSH mit minimalem Konfigurationsaufwand. Die Protokollschicht stellt auch eine Schnittstelle für PostgreSQL-Abfragen bereit. Dadurch ist ein Fernzugriff auf PostgreSQL nie erforderlich, was die Sicherheit erhöht.


### Mehrere Repositorys {#multiple-repositories}

Mehrere Repositorys ermöglichen beispielsweise ein lokales Repository mit kurzer Aufbewahrungsdauer für schnelle Wiederherstellungen und ein entferntes Repository mit längerer Aufbewahrungsdauer für Redundanz und unternehmensweiten Zugriff.


### Vollständige, differenzielle und inkrementelle Backups (auf Datei- oder Blockebene) {#full-differential--incremental-backups-at-file-or-block-level}

Vollständige, differenzielle und inkrementelle Backups werden unterstützt. pgBackRest ist nicht von den Problemen mit der Zeitauflösung von `rsync` betroffen. Differenzielle und inkrementelle Backups sind daher sicher, ohne dass für jede Datei eine Prüfsumme berechnet werden muss. Backups auf Blockebene sparen Speicherplatz, indem nur geänderte Teile von Dateien kopiert werden.


### Backup-Rotation und Bereinigung des Archivs {#backup-rotation--archive-expiration}

Für vollständige und differenzielle Backups lassen sich Aufbewahrungsregeln festlegen, die beliebige Zeiträume abdecken. Das WAL-Archiv kann für alle Backups oder ausschließlich für die neuesten Backups vorgehalten werden. Im letzteren Fall bleibt das WAL, das ältere Backups in einen konsistenten Zustand versetzt, im Archiv erhalten.


### Backup-Integrität {#backup-integrity}

Für jede Datei im Backup werden Prüfsummen berechnet und bei einer Wiederherstellung oder Überprüfung erneut geprüft. Nach dem Kopieren der Dateien wartet das Backup, bis jedes WAL-Segment, das für die Konsistenz des Backups erforderlich ist, das Repository erreicht hat.

Backups im Repository können im selben Format wie ein gewöhnlicher PostgreSQL-Cluster gespeichert werden (einschließlich Tablespaces). Bei deaktivierter Komprimierung und aktivierten Hardlinks kann ein Snapshot eines Backups im Repository erstellt und ein PostgreSQL-Cluster direkt auf diesem Snapshot gestartet werden. Dies ist bei Datenbanken im Terabyte-Bereich vorteilhaft, deren herkömmliche Wiederherstellung viel Zeit beansprucht.

Alle Operationen verwenden fsync auf Datei- und Verzeichnisebene, um die Dauerhaftigkeit sicherzustellen.


### Seitenprüfsummen {#page-checksums}

Wenn Seitenprüfsummen aktiviert sind, prüft pgBackRest die Prüfsummen jeder Datei, die während eines Backups kopiert wird. Bei einem vollständigen Backup werden alle Seitenprüfsummen geprüft, bei differenziellen und inkrementellen Backups die Prüfsummen in geänderten Dateien.

Fehlgeschlagene Prüfungen halten das Backup nicht an. Stattdessen werden Warnungen auf der Konsole und im Dateiprotokoll ausgegeben, die genau angeben, welche Seiten die Prüfung nicht bestanden haben.

Diese Funktion ermöglicht es, Beschädigungen auf Seitenebene frühzeitig zu erkennen, bevor Backups mit gültigen Kopien der Daten abgelaufen sind.


### Backups fortsetzen {#backup-resume}

Ein unterbrochenes Backup kann an der Stelle fortgesetzt werden, an der es angehalten wurde. Bereits kopierte Dateien werden mit den Prüfsummen im Manifest verglichen, um ihre Integrität sicherzustellen. Da dieser Vorgang vollständig auf dem Repository-Host erfolgen kann, entlastet er den PostgreSQL-Host. Er spart zudem Zeit, da die Prüfsummenberechnung schneller ist als das Komprimieren und erneute Übertragen der Daten.


### Komprimierung und Prüfsummen im Datenstrom {#streaming-compression--checksums}

Komprimierung und Prüfsummenberechnung erfolgen im Datenstrom, während Dateien in das Repository kopiert werden, unabhängig davon, ob sich das Repository lokal oder auf einem entfernten Host befindet.

Liegt das Repository auf einem Repository-Host, erfolgt die Komprimierung auf dem PostgreSQL-Host. Die Dateien werden komprimiert übertragen und auf dem Repository-Host lediglich gespeichert. Bei deaktivierter Komprimierung wird für die Übertragung eine niedrige Komprimierungsstufe verwendet, um die verfügbare Bandbreite effizient zu nutzen und gleichzeitig den CPU-Aufwand zu minimieren.


### Delta-Wiederherstellung {#delta-restore}

Das Manifest enthält Prüfsummen für jede Datei im Backup. Diese können die Verarbeitung bei einer Wiederherstellung erheblich beschleunigen. Bei einer Delta-Wiederherstellung werden zunächst alle Dateien entfernt, die nicht im Backup enthalten sind, und anschließend Prüfsummen für die verbleibenden Dateien berechnet. Dateien, die mit dem Backup übereinstimmen, bleiben unverändert; die übrigen Dateien werden wie gewohnt wiederhergestellt. Parallele Verarbeitung kann die Wiederherstellungszeit drastisch verkürzen.


### WAL parallel und asynchron archivieren und abrufen {#parallel-asynchronous-wal-push--get}

Eigene Befehle dienen dazu, WAL in das Archiv zu übertragen und aus dem Archiv abzurufen. Beide Befehle unterstützen parallele Verarbeitung zur Beschleunigung und arbeiten asynchron, um PostgreSQL möglichst schnell zu antworten.

Die WAL-Archivierung erkennt automatisch mehrfach übertragene WAL-Segmente und dedupliziert sie, wenn sie identisch sind. Andernfalls wird ein Fehler ausgelöst. Bei der asynchronen WAL-Archivierung kann die Übertragung an einen anderen Prozess ausgelagert werden, der WAL-Segmente für maximalen Durchsatz parallel komprimiert. Für Datenbanken mit sehr hohem Schreibvolumen kann diese Funktion entscheidend sein.

Der asynchrone WAL-Abruf hält eine lokale Warteschlange dekomprimierter WAL-Segmente vor, die zum Einspielen bereitstehen. Dadurch steht PostgreSQL das WAL schneller zur Verfügung, was die Einspielgeschwindigkeit maximiert. Verbindungen und Speichersysteme mit höherer Latenz (etwa S3) profitieren davon am meisten.

Beide Befehle stellen durch den Vergleich von PostgreSQL-Versionen und Systemkennungen sicher, dass Datenbank und Repository zueinander passen. Dadurch wird eine Fehlkonfiguration des WAL-Archivpfads praktisch ausgeschlossen.


### Unterstützung für Tablespaces und Verknüpfungen {#tablespace--link-support}

Tablespaces werden vollständig unterstützt und können bei der Wiederherstellung beliebigen neuen Speicherorten zugeordnet werden. Mit einem einzigen Befehl lassen sich auch alle Tablespaces einem gemeinsamen Speicherort zuordnen, was für Wiederherstellungen zu Entwicklungszwecken nützlich ist.

Verknüpfungen werden für jede Datei und jedes Verzeichnis im PostgreSQL-Cluster unterstützt. Bei der Wiederherstellung können alle Verknüpfungen an ihren ursprünglichen Speicherorten wiederhergestellt, einige oder alle Verknüpfungen neu zugeordnet oder einige oder alle Verknüpfungen als normale Dateien oder Verzeichnisse im Clusterverzeichnis wiederhergestellt werden.


### Unterstützung für S3-, Azure- und GCS-kompatible Objektspeicher {#s3-azure-and-gcs-compatible-object-store-support}

pgBackRest-Repositorys können in S3-, Azure- und GCS-kompatiblen Objektspeichern liegen und damit praktisch unbegrenzte Kapazität und Aufbewahrung ermöglichen.


### Verschlüsselung {#encryption}

pgBackRest kann das Repository verschlüsseln, um Backups unabhängig von ihrem Speicherort zu schützen.


### Schutz vor Ransomware und Schadsoftware {#ransomware--malware-protection}

Liegt das Repository auf einem versionierten Objektspeicher, kann pgBackRest dessen Zustand zu einem bestimmten Zeitpunkt lesen. Werden Backups versehentlich oder durch Schadsoftware oder Ransomware gelöscht oder beschädigt, lässt sich ein Zielzeitpunkt verwenden, um Daten aus der Zeit vor dem Schaden wiederherzustellen.

S3-, Azure- und GCS-kompatible Objektspeicher unterstützen Versionierung. Objektsperren bei S3 und vorläufiges Löschen bei GCS oder Azure können zusätzlichen Schutz vor Manipulation bieten.


### Kompatibilität mit zehn PostgreSQL-Versionen {#compatibility-with-ten-versions-of-postgresql}

pgBackRest unterstützt zehn PostgreSQL-Versionen: die fünf unterstützten Versionen und die letzten fünf Versionen, deren Unterstützung beendet ist (EOL). So bleibt ausreichend Zeit für das Upgrade auf eine unterstützte Version.


--------

## Erste Schritte {#getting-started}

pgBackRest soll einfach zu konfigurieren und zu betreiben sein:

- [Benutzerhandbücher](/de/docs/pgbackrest/user-guide/) für verschiedene Betriebssysteme und PostgreSQL-Versionen.
- Befehlsreferenzen für Operationen über die Befehlszeile: [backup](/de/docs/pgbackrest/command/backup/), [restore](/de/docs/pgbackrest/command/restore/), [check](/de/docs/pgbackrest/command/check/) und [info](/de/docs/pgbackrest/command/info/).
- [Konfigurationsreferenz](/de/docs/pgbackrest/configuration/) zum Erstellen von pgBackRest-Konfigurationen.


--------

## Beiträge {#contributions}

Beiträge zu pgBackRest sind jederzeit willkommen! Unsere [Richtlinien für Beiträge](https://github.com/pgbackrest/pgbackrest/blob/main/CONTRIBUTING.md) erläutern, wie Sie Funktionen, Verbesserungen oder Problemmeldungen beitragen können.


--------

## Unterstützung {#support}

pgBackRest ist vollständig kostenlos und quelloffen unter der [MIT](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)-Lizenz. Sie können es ohne jegliche Einschränkungen privat oder kommerziell nutzen. Fehlerberichte werden sehr ernst genommen und so schnell wie möglich bearbeitet. Bitte melden Sie Fehler [hier](https://github.com/pgbackrest/pgbackrest/issues).

Eine belastbare Strategie zur Wiederherstellung nach Ausfällen mit geeigneten Replikations- und Backup-Konzepten auszuarbeiten, kann sehr komplex und anspruchsvoll sein. Möglicherweise benötigen Sie Unterstützung bei der Architekturplanung und im laufenden Betrieb, damit Ihr Unternehmen weiterhin reibungslos arbeiten kann.

Unsere [Sponsoren](#sponsors) bieten Produkte und Dienstleistungen mit pgBackRest-Unterstützung an und können Ihnen bei der Vorsorge für und Wiederherstellung nach Ausfällen helfen.
