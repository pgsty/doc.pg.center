---
title: "Befehlsreferenz"
linkTitle: "Befehle"
weight: 40
description: "pgBackRest-Befehlsreferenz mit allen Optionen für Backup-, Wiederherstellungs-, Archiv- und Verwaltungsvorgänge."
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [Referenz]
aliases: [/pgbackrest/command/]
upstream_link: "https://pgbackrest.org/command.html"
---

## Einführung {#introduction}

Befehle führen die verschiedenen pgBackRest-Funktionen aus. Hier sind sämtliche Befehlsoptionen aufgeführt: Jede auf einen Befehl anwendbare Option wird bei diesem Befehl genannt, auch wenn sie für weitere Befehle gilt. Dazu gehören alle Optionen, die auch in `pgbackrest.conf` konfiguriert werden können.

Nicht boolesche Optionen aus `pgbackrest.conf` lassen sich über die Befehlszeile mit dem Präfix `reset-` auf ihren Standardwert zurücksetzen. Damit kann ein Backup direkt auf einem Repository-Host wiederhergestellt werden. Normalerweise meldet pgBackRest einen Fehler, weil es erkennt, dass sich die Datenbank auf einem entfernten Host befindet und Wiederherstellungen nicht aus der Ferne möglich sind. Mit `--reset-pg1-host` in der Befehlszeile ignoriert pgBackRest den entfernten Datenbank-Host und führt die Wiederherstellung lokal aus. Möglicherweise muss ein neuer Wert für `--pg1-path` angegeben werden, um die Wiederherstellung in einem bestimmten Pfad zu erzwingen, also nicht in dem auf dem Datenbank-Host verwendeten Pfad.

Mit dem Präfix `no-` lässt sich eine boolesche Option über die Befehlszeile auf false setzen.

Jede Option kann über eine Umgebungsvariable gesetzt werden. Dazu werden das Präfix `PGBACKREST_` und der Optionsname in Großbuchstaben verwendet, wobei `-` durch `_` ersetzt wird. Beispielsweise wird `pg1-path` zu `PGBACKREST_PG1_PATH` und `stanza` zu `PGBACKREST_STANZA`. Boolesche Optionen werden wie in einer Konfigurationsdatei angegeben, etwa `PGBACKREST_COMPRESS="n"`; Varianten mit `reset-*` sind nicht zulässig. Für Optionen, die mehrfach in der Befehlszeile oder einer Konfigurationsdatei angegeben werden können, werden die Werte durch Doppelpunkte getrennt, etwa `PGBACKREST_DB_INCLUDE="db1:db2"`.

Befehlszeilenoptionen haben Vorrang vor Umgebungsvariablen; diese haben wiederum Vorrang vor Optionen aus der Konfigurationsdatei.

Informationen zu den Optionentypen finden Sie in der [Einführung zur Konfiguration](/de/docs/pgbackrest/configuration/#introduction)

## Befehle {#commands}

| Befehl | Zusammenfassung |
|---|---|
| [**`annotate`**](/de/docs/pgbackrest/command/annotate/) | Backup-Anmerkungen nach der Erstellung des Backups hinzufügen, ändern oder entfernen. |
| [**`archive-get`**](/de/docs/pgbackrest/command/archive-get/) | Archivierte WAL-Segmente für Wiederherstellung, PITR oder die Recovery eines Replikats abrufen. |
| [**`archive-push`**](/de/docs/pgbackrest/command/archive-push/) | WAL-Segmente von PostgreSQL entgegennehmen und an die konfigurierten Repositorys übertragen. |
| [**`backup`**](/de/docs/pgbackrest/command/backup/) | Backups im Ziel-Repository erstellen (standardmäßig im Repository mit der höchsten Priorität). |
| [**`check`**](/de/docs/pgbackrest/command/check/) | Die Backup- und Archivkonfiguration einer Stanza und die Funktionsfähigkeit der WAL-Archivierung prüfen. |
| [**`expire`**](/de/docs/pgbackrest/command/expire/) | Backups und archivierte WAL gemäß den konfigurierten Aufbewahrungsregeln entfernen. |
| [**`help`**](/de/docs/pgbackrest/command/help/) | Allgemeine Hilfe oder Hilfe zu einem Befehl oder einer Option anzeigen. |
| [**`info`**](/de/docs/pgbackrest/command/info/) | Status und Metadaten von Stanzas und Backups im Text- oder JSON-Format anzeigen. |
| [**`repo-get`**](/de/docs/pgbackrest/command/repo-get/) | Repository-Dateien für Verwaltung, Untersuchung und Tests lesen (wie `cat`). |
| [**`repo-ls`**](/de/docs/pgbackrest/command/repo-ls/) | Repository-Dateien und -Pfade für Verwaltung, Untersuchung und Tests auflisten (wie `ls`). |
| [**`restore`**](/de/docs/pgbackrest/command/restore/) | Ein Backup wiederherstellen (standardmäßig das neueste), optional mit Point-in-Time-Recovery. |
| [**`server`**](/de/docs/pgbackrest/command/server/) | Den pgBackRest-TLS-Server für den Zugriff auf entfernte Hosts ohne SSH ausführen. |
| [**`server-ping`**](/de/docs/pgbackrest/command/server-ping/) | Einen pgBackRest-TLS-Server mit einem Ping darauf prüfen, ob er Verbindungen annimmt. |
| [**`stanza-create`**](/de/docs/pgbackrest/command/stanza-create/) | Stanza-Metadaten in allen konfigurierten Repositorys erstellen. |
| [**`stanza-delete`**](/de/docs/pgbackrest/command/stanza-delete/) | Alle Backups und Archive einer Stanza dauerhaft entfernen. |
| [**`stanza-upgrade`**](/de/docs/pgbackrest/command/stanza-upgrade/) | Stanza-Metadaten nach einem Upgrade auf eine neue PostgreSQL-Hauptversion aktualisieren. |
| [**`start`**](/de/docs/pgbackrest/command/start/) | Die Ausführung von pgBackRest-Prozessen nach einem vorherigen `stop` wieder zulassen. |
| [**`stop`**](/de/docs/pgbackrest/command/stop/) | Neue pgBackRest-Prozesse verhindern und laufende Prozesse optional zwangsweise beenden. |
| [**`verify`**](/de/docs/pgbackrest/command/verify/) | Die Gültigkeit der Backup- und Archivdaten im Repository prüfen. |
| [**`version`**](/de/docs/pgbackrest/command/version/) | Die installierte pgBackRest-Version anzeigen. |
{.full-width}
