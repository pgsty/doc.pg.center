---
title: "Häufig gestellte Fragen"
linkTitle: "FAQ"
weight: 70
description: "Häufig gestellte Fragen zu Backups, Wiederherstellung, Konfiguration und Fehlerbehebung mit pgBackRest."
icon: fa-solid fa-circle-question
module: [PGBACKREST]
categories: [Referenz]
aliases: [/pgbackrest/faq/]
upstream_link: "https://pgbackrest.org/faq.html"
---

--------

## Einführung {#introduction}

Die häufig gestellten Fragen erläutern konkrete Fragen, die im Benutzerhandbuch, in der Konfigurationsreferenz oder in der Befehlsreferenz möglicherweise nicht behandelt werden. Falls sich hier keine Einzelheiten zu Ihrem Problem finden, ist auch die [Issue-Liste von pgBackRest auf GitHub](https://github.com/pgbackrest/pgbackrest/issues) eine nützliche Anlaufstelle.


--------

## Was tun bei der Fehlermeldung "could not find WAL segment"? {#what-if-i-get-the-could-not-find-wal-segment-error}

Dieser Fehler kann viele verschiedene Ursachen haben, darunter:

- ein falsch konfigurierter `archive_command`
- fehlerhafte pgBackRest-Konfigurationsdateien
- Netzwerk- oder Berechtigungsprobleme
- Konfigurationsprobleme eines Drittanbieterprodukts (z. B. S3, Swift oder Minio)
- eine große Menge WAL in der Warteschlange für die Archivierung

Folgende Schritte werden empfohlen:

- Den `archive_command` in PostgreSQL prüfen.
- Die pgBackRest-Konfiguration auf jedem Host prüfen (z. B. gehören die `pg*`-Einstellungen auf den Repository-Host und die `repo*`-Einstellungen auf den pg-Host).
- Den Befehl `check` ausführen und dabei `--archive-timeout` auf einen Wert über dem in der pgBackRest-Konfigurationsdatei festgelegten Wert (oder dem Standardwert) setzen, um festzustellen, ob die WAL-Warteschlange mehr Zeit zum Leeren benötigt. Erzeugt das System viel WAL, sollte die [asynchrone Archivierung](/de/docs/pgbackrest/user-guide/#asynchronous-archiving) in Betracht gezogen werden.


--------

## Wie lässt sich ein Backup-Satz manuell löschen? {#how-do-i-manually-purge-a-backup-set}

Ein vollständiger Backup-Satz kann mit der Option `--set` entfernt werden, wie unter [Befehlsreferenz: Expire](/de/docs/pgbackrest/command/expire/) erläutert.


--------

## Wie lassen sich Optionen für jeden Befehl separat konfigurieren? {#how-can-i-configure-options-independently-for-each-command}

pgBackRest kann Optionen in der Konfigurationsdatei für jeden Befehl separat festlegen. [Stanza für den Cluster konfigurieren](/de/docs/pgbackrest/user-guide/#configure-cluster-stanza) beschreibt diese Funktion und die Rangfolge der Optionen.

Beispielsweise lässt sich die Option `process-max` für jeden Befehl optimieren:

```ini
[global]
# used where not overridden
process-max=2

[global:backup]
# more cores for backup
process-max=4

[global:restore]
# all the cores for restore
process-max=8

[global:archive-push]
# more cores for archive-push
process-max=3

[global:archive-get]
# fewer cores for archive-get
process-max=1
```


--------

## Darf der Name meines S3-Buckets Punkte enthalten? {#can-i-use-dots-periods-in-my-s3-bucket-name}

RFC-2818 erlaubt nicht, dass Platzhalter auf einen Punkt (.) passen. Deshalb dürfen S3-Bucket-Namen keine Punkte enthalten. Enthält der S3-Bucket-Name Punkte, tritt ein Fehler wie "unable to find hostname 'my.backup.bucket.s3.amazonaws.com' in certificate common name or subject alternative names" auf.

Eine Ausnahme ist `repo-s3-uri-style=path`: Hier wird der Bucket der URI statt dem Host vorangestellt. Da der Bucket nicht Teil des Hostnamens ist, wird das Zertifikat allein mit dem Endpunkt abgeglichen, und Punkte im Bucket-Namen sind unproblematisch. URIs im Pfadstil werden allerdings nicht von allen S3-kompatiblen Objektspeichern unterstützt.


--------

## Wo gibt es Pakete für ältere pgBackRest-Versionen? {#where-can-i-find-packages-for-older-versions-of-pgbackrest}

Das Repository [apt.postgresql.org](https://apt.postgresql.org) führt ein [Archiv älterer Versionen](https://apt-archive.postgresql.org). Debian hält außerdem [Snapshots](https://snapshot.debian.org/binary/pgbackrest/) aller Test-Builds vor.


--------

## Warum scheitert ein Backup-Versuch bei `backup-standby=y`, wenn die Standby-Datenbank ausgefallen ist? {#why-does-a-backup-attempt-fail-when-backup-standbyy-and-the-standby-database-is-down}

Backups vom Standby sollen in der Regel den Primärserver entlasten. Bei einem Ausfall des Standbys auf Backups vom Primärserver zu wechseln, widerspricht daher oft diesem Ziel. Den Primärserver zusätzlich zu belasten, wenn im System bereits Fehler vorliegen, wird nicht empfohlen. Backups sind nicht kritisch, solange ein hinreichend aktuelles vorhanden ist; entscheidend ist, dass die WAL-Archivierung Schritt hält. Sobald das System wieder stabil ist, bleibt genügend Zeit für ein Backup.

Ist ein Backup unbedingt erforderlich, besteht die Lösung darin, weitere Standbys bereitzustellen oder `backup-standby` zu entfernen. Dies lässt sich auf der Befehlszeile mit `--no-backup-standby` überschreiben, sodass für ein einmaliges Backup keine Neukonfiguration erforderlich ist.


--------

## Sollte das Repository auf einem Standby-Host eingerichtet werden? {#should-i-setup-my-repository-on-a-standby-host}

Nein. Wenn Primär- und Standby-Datenbanken konfiguriert sind, sollten die pgBackRest-Konfigurationsdateien symmetrisch sein, damit Failover nahtlos funktionieren. Andernfalls müssen die Konfigurationen bei einem Failover geändert werden, oder es können weitere Probleme entstehen.

Weitere Informationen enthält der Abschnitt [Dedizierter Repository-Host](/de/docs/pgbackrest/user-guide/#dedicated-repository-host) im Benutzerhandbuch.


--------

## Warum scheint die zeitbasierte Point-in-Time-Recovery nicht zu funktionieren? {#time-based-point-in-time-recovery-does-not-appear-to-work-why}

Der häufigste Fehler bei einer zeitbasierten Point-in-Time-Recovery ist die Auswahl eines Backups, das nach der Zielzeit abgeschlossen wurde. Bei `--type=time` ohne die Option `--set` durchsucht pgBackRest die konfigurierten Repositorys nach einem Backup, das vor der mit `--target=` angegebenen Zeit abgeschlossen wurde. Wird kein geeignetes Backup gefunden, meldet pgBackRest einen Fehler, statt das neueste Backup wiederherzustellen. Ein nach der Zielzeit abgeschlossenes Backup kann durch WAL-Wiedergabe nicht auf diesen früheren Zeitpunkt zurückgeführt werden.

Für die Option `--set` zunächst den Befehl `info` ausführen und ein Backup auswählen, dessen Endzeitpunkt vor dem Zielzeitpunkt liegt. Bei der Wiederherstellung dann `--set=BACKUP_LABEL` angeben, wobei `BACKUP_LABEL` den gewählten Backup-Satz bezeichnet.

Weitere Informationen enthält der Abschnitt [Point-in-Time-Recovery](/de/docs/pgbackrest/user-guide/#point-in-time-recovery) im Benutzerhandbuch.


--------

## Was bedeutet das Suffix im WAL-Archiv? {#what-does-the-wal-archive-suffix-mean}

Das Suffix ist die SHA1-Prüfsumme zur Überprüfung der Dateiintegrität. Es kann nicht weggelassen werden.


--------

## Dauert die Wiederherstellung bestimmter Backup-Typen (vollständig, differenziell, inkrementell) länger? {#does-it-take-longer-to-restore-specific-backup-types-full-differential-incremental}

Die verschiedenen Backup-Typen benötigen dieselbe Wiederherstellungszeit. Die Wiederherstellung ruft Dateien anhand des Backup-Manifests ab, das bei inkrementellen oder differenziellen Backups auf Dateien eines früheren Backups verweisen kann. Die Zeit für das *Erstellen* eines Backups kann sich je nach Backup-Typ unterscheiden. Die Datenbankgröße bestimmt hingegen die Wiederherstellungszeit, sofern Datenträger-I/O, Netzwerk-I/O usw. gleich sind.


--------

## Wie lässt sich ein Backup zur Verwendung in einer vom Netzwerk isolierten Umgebung exportieren? {#how-can-i-export-a-backup-for-use-in-a-network-isolated-environment}

pgBackRest verwendet das Repository nicht nur zum Speichern von Backups und WAL-Archiven, sondern auch für wesentliche Metadaten, die für Funktionen wie Komprimierung, Verschlüsselung und Dateibündelung erforderlich sind. Deshalb funktioniert es in der Regel nicht, lediglich ein Backup zusammen mit einer Teilmenge der WAL-Dateien zu kopieren, sofern nicht sehr spezifische und restriktive Bedingungen erfüllt sind.

Es gibt jedoch eine Alternative, wenn ein eigenständiger Export einer Datenbank erstellt werden soll, der sich beispielsweise per USB übertragen lässt. Ein Backup mit aktivierter Option [`--archive-copy`](/de/docs/pgbackrest/command/backup/#copy-archive-option---archive-copy) stellt sicher, dass die erforderlichen WAL-Segmente zusammen mit dem Backup gespeichert werden. Dieses anschließend mit [`--type=none`](/de/docs/pgbackrest/command/restore/#type-option---type) `--pg1-path=/your/target/path` wiederherstellen. Dadurch entsteht ein wiederhergestelltes PostgreSQL-Datenverzeichnis, in dem alle erforderlichen WAL-Dateien bereits in `pg_wal` liegen, ähnlich dem Ergebnis von `pg_basebackup`.

Dieses Verzeichnis kann dann auf ein anderes System kopiert werden. PostgreSQL sollte daraus eine Recovery durchführen können, ohne auf das pgBackRest-Repository zugreifen zu müssen.

Bei der Recovery dieses Backups wird die Timeline nicht gewechselt. Deshalb sollte dieser Cluster kein WAL in das ursprüngliche Repository übertragen, aus dem er exportiert wurde. Befindet sich der neue Cluster in einer vom Netzwerk isolierten Umgebung, sollte dies kein Problem darstellen.
