---
title: "Support und Mitwirkung"
linkTitle: "Support"
weight: 100
description: "Fehler melden, Funktionswünsche einreichen, Patches beisteuern und professionellen PostgreSQL-Support finden"
icon: fa-solid fa-life-ring
module: [PGBADGER]
categories: [Aufgabe]
aliases: [/pgbadger/support/]
upstream_link: "https://pgbadger.darold.net/#support"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

pgBadger wird als offenes Projekt gepflegt. Fehlerberichte, Funktionsvorschläge, Dokumentationskorrekturen und Patches werden über das Repository des Originalprojekts auf GitHub verwaltet.

## Fehler und Funktionswünsche {#bugs-and-features}

1. Aktualisieren Sie pgBadger auf die neueste veröffentlichte Version und prüfen Sie, ob das Verhalten weiterhin auftritt.
2. Suchen Sie in den [offenen Issues](https://github.com/darold/pgbadger/issues) und [geschlossenen Issues](https://github.com/darold/pgbadger/issues?q=is%3Aissue+is%3Aclosed) nach einer vorhandenen Lösung.
3. Reduzieren Sie das Problem auf einen möglichst kleinen, bereinigten Protokollauszug und die kürzeste Befehlszeile, mit denen es sich noch reproduzieren lässt.
4. Entfernen Sie Anmeldeinformationen, sensible SQL, Bind-Werte, Hostnamen, Adressen und Geschäftsdaten.
5. Erstellen Sie ein [neues Issue](https://github.com/darold/pgbadger/issues/new) und geben Sie die pgBadger-Version, das Betriebssystem, das Eingabeformat, die genauen Optionen sowie das beobachtete und das erwartete Ergebnis an.

Geben Sie bei Abstürzen oder Parserfehlern nur die unbedingt erforderlichen, bereinigten Protokollzeilen an, mit denen sich der Fehler reproduzieren lässt. Ein vollständiges Produktionsprotokoll oder ein erzeugter Bericht eignet sich nur selten für ein öffentliches Issue.

## Einen Patch beisteuern {#contribute-a-patch}

Das Projekt enthält eine `.editorconfig`-Datei für eine einheitliche Formatierung. Halten Sie Befehlszeilenhilfe, POD und erzeugte Markdown-Dokumentation synchron, wenn sich eine Änderung auf das für Benutzer sichtbare Verhalten auswirkt.

Der Arbeitsablauf für die Dokumentation im Originalprojekt lautet:

```console
$ perl Makefile.PL
$ make README
```

`doc/pgBadger.pod` ist die maßgebliche ausführliche Quelle. `pgbadger --help` liefert die Kurzreferenz, während die README-Dateien daraus erzeugte Ansichten sind. Führen Sie die relevanten Tests aus, bevor Sie einen Pull Request einreichen.

- [Quellrepository](https://github.com/darold/pgbadger)
- [Pull Requests](https://github.com/darold/pgbadger/pulls)
- [Beitragsleitfaden](https://github.com/darold/pgbadger/blob/master/CONTRIBUTING.md)
- [Entwicklungsnotizen](https://github.com/darold/pgbadger/blob/master/HACKING.md)

## Kommerzieller Support {#commercial-support}

Die Lizenz des pgBadger-Projekts garantiert weder Wartung noch Support. Für kostenpflichtige Hilfe bei PostgreSQL-Protokollierung, Leistungsanalyse oder Berichtsautomatisierung nutzen Sie das [Verzeichnis professioneller PostgreSQL-Dienstleister](https://www.postgresql.org/support/professional_support/).
