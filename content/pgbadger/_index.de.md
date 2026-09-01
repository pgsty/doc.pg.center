---
title: "Dokumentation zu pgBadger 13.2"
linkTitle: pgBadger
weight: 40
description: "Schnelle Analyse von PostgreSQL- und PgBouncer-Protokollen mit detaillierten, in sich geschlossenen Berichten"
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [Konzept]
aliases: [/docs/pgbadger/, /docs/pgbadger/documentation/]
upstream_source: pgbadger
upstream_link: "https://github.com/darold/pgbadger"
cascade:
  upstream_source: pgbadger
  type: docs
  module: [PGBADGER]
---

![pgBadger-Logo](/img/docs/pgbadger/logo.png "pgBadger")

**pgBadger** ist ein schnelles, eigenständiges und in Perl geschriebenes Analyseprogramm für PostgreSQL-Protokolle. Es liest PostgreSQL- oder PgBouncer-Protokolle und erzeugt detaillierte Ausgaben als HTML, Text, Binärdaten, JSON oder Roh-CSV. Die HTML-Berichte sind in sich geschlossen, interaktiv und zoombar; zur Anzeige genügt ein Webbrowser.

## Warum pgBadger {#why-pgbadger}

pgBadger ist für große Protokolle und den betrieblichen Einsatz konzipiert:

- ein einziges Perl-Programm ohne obligatorische Module außerhalb der Perl-Standardbibliothek;
- automatische Erkennung von `stderr`, `syslog`, `csvlog`, `jsonlog`, RDS, Cloud SQL, logplex, Redshift und PgBouncer-Eingabe;
- direktes Lesen lokaler Dateien, der Standardeingabe, entfernter Dateien über SSH sowie von HTTP-, FTP- oder SFTP-URLs;
- mit gzip, bzip2, lz4, xz, zip oder zstd komprimierte Eingaben;
- parallele Analyse einer großen Datei oder vieler kleiner Dateien;
- tägliche und wöchentliche inkrementelle Berichte sowie monatliche Berichte auf Abruf;
- Filter nach Zeit, Datenbank, Benutzer, Client, Anwendung, Prozess, Sitzung und Abfragemuster.

## Was die Berichte enthalten {#report-coverage}

Die PostgreSQL-Berichte umfassen:

- Gesamtaktivität und Abfragestatistiken;
- langsame, häufige, besonders zeitintensive, wartende und abgebrochene Abfragen;
- temporäre Dateien, Prüfpunkte, Sperren, Sitzungen und Verbindungen;
- Autovacuum- und Autoanalyze-Aktivität nach Tabelle;
- Fehler und Ereignisse nach Schweregrad und Kategorie;
- Verteilungen nach Datenbank, Benutzer, Client, Anwendung und Anweisungstyp.

Für PgBouncer-Eingaben kommen Durchsatz, durchschnittliche Abfragedauer, gleichzeitige Sitzungen, die Verteilung von Verbindungen und Sitzungen, die Nutzung des reservierten Pools sowie Berichte zu häufigen Fehlern und Ereignissen hinzu.

## Dokumentationsübersicht {#documentation-map}

Lesen Sie die Dokumentation in dieser Reihenfolge, oder verwenden Sie die Seitenleiste, um direkt zu einer Aufgabe zu springen:

1. [Laden Sie pgBadger samt seinen optionalen Modulen herunter und installieren Sie es](download/).
2. Überprüfen Sie die vollständige [Befehlszeilenreferenz](command-line/).
3. Konfigurieren Sie die [PostgreSQL-Protokollierung](postgresql-logging/) mit einem analysierbaren Präfix.
4. Wählen Sie den geeigneten [Modus für die Parallelverarbeitung](parallel-processing/).
5. Erstellen Sie [inkrementelle Berichte](incremental-reports/) sicher.
6. Wählen Sie ein [Ausgabeformat](output-formats/) und sehen Sie sich die [lokalen Beispiele](sample-reports/) an.
7. Informieren Sie sich über die [Versionsgeschichte](releases/), [Support und Mitwirkung](support/) sowie die [Lizenz](license/).

## Links zum Originalprojekt {#upstream-links}

- [Projekt-Website](https://pgbadger.darold.net/)
- [Quellcode](https://github.com/darold/pgbadger)
- [Veröffentlichungen](https://github.com/darold/pgbadger/releases)
- [Issue-Tracker](https://github.com/darold/pgbadger/issues)
