---
title: "Inkrementelle Berichte"
linkTitle: "Inkrementelle Berichte"
weight: 60
description: "Tägliche und wöchentliche Berichte erstellen, die Aufbewahrung steuern, Ausgaben neu erstellen und monatliche Zusammenfassungen hinzufügen"
search_keywords: [--day-report, --explode, --extra-files, --incremental, --iso-week-number, --last-parsed, --month-report, --no-week, --noreport, --outdir, --rebuild, --retention, --start-monday, day, day-report, explode, extra, extra-files, files, incremental, iso, iso-week-number, last, last-parsed, monday, month, month-report, no, no-week, noreport, number, outdir, parsed, rebuild, report, retention, start, start-monday, week]
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [Aufgabe]
aliases: [/pgbadger/incremental-reports/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

Im inkrementellen Modus speichert pgBadger die ausgewerteten Statistiken im Binärformat. Daraus erstellt es pro Tag einen HTML-Bericht, pro Woche einen kumulativen Bericht und einen kalenderartigen Index, der diese Berichte miteinander verknüpft. Der Modus ist für die wiederholte Verarbeitung rotierter Protokolle vorgesehen, ohne dieselben Einträge erneut zu zählen.

## Tägliche und wöchentliche Berichte erstellen {#daily-and-weekly}

Führen Sie pgBadger nach der täglichen Protokollrotation aus und geben Sie ein dauerhaftes Ausgabeverzeichnis an:

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

`-I` aktiviert den inkrementellen Modus und `-O` wählt das Verzeichnis für den Binärzustand, den Kalenderindex und die erzeugten Berichte aus. pgBadger verwaltet seinen inkrementellen Zustand selbst in diesem Verzeichnis. Daher benötigen Sie `--last-parsed` nur, wenn Sie die Zustandsdatei ausdrücklich an einem anderen Ort ablegen möchten.

Verwenden Sie ein separates HTML-Verzeichnis, während Sie den Binärzustand im ursprünglichen Verzeichnis beibehalten:

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

Behandeln Sie die Binärdateien als Quelldaten für spätere Neuerstellungen. Sichern Sie sie oder bewahren Sie die ursprünglichen Protokolle auf, wenn Sie Berichte später erneut erzeugen möchten.

## Aufbewahrung {#retention}

Bewahren Sie nur eine festgelegte Anzahl von Wochen auf:

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

Ältere Wochen- und Tagesverzeichnisse werden automatisch entfernt. Testen Sie die Richtlinie an einer Kopie außerhalb der Produktion, bevor Sie sie für Ihre einzige Berichtshistorie aktivieren.

## Gemeinsam genutzte Ressourcen separat speichern {#shared-assets}

Standardmäßig betten HTML-Berichte ihre JavaScript- und CSS-Dateien ein. In einem Verzeichnis mit vielen inkrementellen Berichten speichert `-X` / `--extra-files` gemeinsam genutzte Ressourcen separat und verringert dadurch die mehrfach gespeicherte Datenmenge in der Ausgabe:

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

Alle Berichte und das zugehörige versionierte Ressourcenverzeichnis müssen gemeinsam verschoben werden.

## Vorhandene Berichte neu erstellen {#rebuild}

Erstellen Sie nach einem pgBadger-Upgrade oder einer Korrektur an der Berichtserzeugung die HTML-Ausgabe aus den aufbewahrten Binärdaten neu:

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

Verwenden Sie `-E` / `--explode` erneut, wenn die ursprünglichen Berichte pro Datenbank generiert wurden.

> Verwenden Sie die lange Option `--rebuild`. In der aktuellen Befehlsreferenz steht `-R` für `--retention`; wer `-R` fälschlich als Kurzform für die Neuerstellung verwendet, wendet die falsche Option an.

## Monatlichen Bericht hinzufügen {#monthly-reports}

Tägliche und wöchentliche Berichte werden automatisch erstellt. Die monatliche Aggregation müssen Sie ausdrücklich anstoßen, da sie bei einer umfangreichen Historie aufwendig sein kann:

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

Der erzeugte Monatsbericht wird dem Kalenderindex hinzugefügt. Wenn Sie den Befehl erneut ausführen, wird dieser Monat aus den verfügbaren Binärdaten neu erstellt. Für eine nach Datenbank getrennte Historie verwenden Sie auch hier `-E`:

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

Die vollständige Befehlsreferenz beschreibt außerdem `--day-report YYYY-MM-DD`, `--no-week`, `--noreport`, `--start-monday` und `--iso-week-number` für komplexere Zeitpläne.

Öffnen Sie das [mitgelieferte Beispiel für inkrementelle Berichte](/third_party/pgbadger/examples/report/index.html), um den Kalender, die Wochenverknüpfungen und die Hierarchie der Tagesberichte ohne Netzwerkverbindung zu prüfen.
