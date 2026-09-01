---
title: "Ausgabeformate"
linkTitle: "Ausgabeformate"
weight: 70
description: "HTML, Text, Binärdaten, JSON oder Roh-CSV als Ausgabeformat wählen und Zwischendateien zusammenführen"
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [Referenz]
aliases: [/docs/pgbadger/output-formats/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger bestimmt das Ausgabeformat anhand der Dateiendung oder über `-x` / `--extension`. Verwenden Sie `-o` / `--outfile` mehrfach, um in einem einzigen Analyselauf mehrere Formate zu erzeugen.

| Format | Typische Erweiterung | Empfohlener Einsatz |
|---|---|---|
| HTML | `.html` | interaktiver, gut lesbarer Bericht mit Diagrammen |
| Text | `.txt` | Prüfung im Terminal und einfache Archivierung |
| Binär | `.bin` | zusammenführbare Zwischenstatistiken und Neuerstellung von Berichten |
| JSON | `.json` | Integration mit anderer Software; erfordert `JSON::XS` |
| Roh-CSV | gewählte Ausgabedatei | zeilenorientierter Export mit `--dump-raw-csv` |

## HTML und Text {#html-and-text}

Die Standardausgabe ist `out.html`:

```console
$ pgbadger postgresql.log -o report.html
```

HTML enthält standardmäßig alle Skripte, Stylesheets, Schriftarten und Berichtsdaten, die für eine eigenständige Anzeige erforderlich sind. `-X` / `--extra-files` lagert gemeinsam genutzte JavaScript- und CSS-Dateien bei inkrementellen Berichten aus; bewahren Sie diese Ressourcen zusammen mit dem HTML-Verzeichnisbaum auf.

Geben Sie das Textformat ausdrücklich an:

```console
$ pgbadger -x text -o report.txt postgresql.log
```

Verwenden Sie `-` als Ausgabedateinamen, um ein unterstütztes Format auf die Standardausgabe zu schreiben.

## Binäre Zwischendaten {#binary-format}

Die Binärausgabe trennt die Analyse von der Darstellung. Erzeugen Sie stündliche Zwischenstände aus einer im Laufe des Tages wachsenden Protokolldatei:

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

Führen Sie ein oder mehrere Binärdateien in einem neuen Bericht zusammen:

```console
$ pgbadger -o sunday.html sunday/*.bin
```

Wenn der Server pro Stunde eine Protokolldatei schreibt, erstellen Sie für jede Rotation eine Binärdatei und erzeugen den kumulativen HTML-Bericht bei Bedarf neu:

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

Führen Sie nur Binärdateien aus kompatiblen pgBadger-Versionen zusammen. Lesen Sie vor dem Upgrade eines dauerhaft genutzten Berichtsverzeichnisses in den Versionshinweisen nach, ob die Binärformate kompatibel sind.

## JSON {#json-format}

Die JSON-Ausgabe ist für die maschinelle Weiterverarbeitung vorgesehen, etwa in Überwachungs- oder Berichtspipelines:

```console
$ pgbadger -o report.json postgresql.log
```

Installieren Sie zunächst `JSON::XS`. Fügen Sie `--prettify-json` hinzu, um die Lesbarkeit zu verbessern, wenn Dateigröße und Erstellungsdauer weniger wichtig sind.

## Roh- und abfrageorientierte Exporte {#raw-exports}

Die Befehlsreferenz bietet außerdem spezialisierte Exporte:

- `--dump-raw-csv` analysiert das Protokoll und schreibt zeilenorientierte CSV-Dateien, ohne einen Bericht zu erstellen;
- `--csv-separator` ändert das Trennzeichen für die Roh-CSV-Datei;
- `--dump-all-queries` gibt jede Abfrage nach dem Ersetzen der Bind-Parameter aus;
- `--normalized-only` schreibt normalisierte Abfragen;
- `--query-numbering` nummeriert die Abfragen in der Textausgabe.

Diese Modi können Anwendungs-SQL, Bezeichner, Benutzer, Client-Adressen oder Literalwerte enthalten. Prüfen Sie die Ausgabe vor der Freigabe und verwenden Sie `--anonymize`, wenn die geplante Analyse keine Literalwerte erfordert.
