---
title: "Beispielberichte"
linkTitle: "Beispielberichte"
weight: 80
description: "Vollständige, auf Fehler beschränkte und inkrementelle pgBadger-Berichte aus dem lokalen Website-Snapshot öffnen"
icon: fa-solid fa-chart-column
module: [PGBADGER]
categories: [Referenz]
aliases: [/pgbadger/sample-reports/]
upstream_link: "https://pgbadger.darold.net/#reports"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

Die Beispielberichte wurden im Mai 2022 mit pgBadger 11.8 erzeugt. Die Originalbeispiele sind lokal auf dieser Website eingebunden. Daher bleiben Berichtsnavigation, Diagramme, Stylesheets und Skripte verfügbar, ohne auf den Server des Originalprojekts zugreifen zu müssen.

| Beispiel | Was es zeigt | Lokale Kopie |
|---|---|---|
| Vollständiger Bericht | PostgreSQL-Aktivität zusammen mit PgBouncer-Statistiken | [Öffnen Sie den vollständigen Bericht](/third_party/pgbadger/examples/sample.html) |
| Inkrementeller Bericht | Kalenderindex, wöchentliche Aggregation und tägliche Seiten | [Öffnen Sie den inkrementellen Index](/third_party/pgbadger/examples/report/index.html) |
| Fehler und Ereignisse | Ein Bericht, der auf Fehler und betriebliche Ereignisse beschränkt ist | [Öffnen Sie den Fehlerbericht](/third_party/pgbadger/examples/errors.html) |

## Vollständiger Bericht {#complete-report}

Der vollständige Bericht ist eine in sich geschlossene HTML-Datei. Über die obere Navigationsleiste können Sie globale Statistiken, Abfragen, Sitzungen, Verbindungen, temporäre Dateien, Checkpoints, Autovacuum-Aktivität, Sperren und PgBouncer-spezifische Diagramme untersuchen.

Die Daten dienen ausschließlich Demonstrationszwecken und stellen keinen aktuellen Leistungsbenchmark dar. Die Werte, PostgreSQL-Versionen und die eingebettete pgBadger-Benutzeroberfläche (UI) entsprechen dem Stand zum Zeitpunkt der Berichtserstellung.

## Hierarchie inkrementeller Berichte {#incremental-hierarchy}

Das inkrementelle Beispiel bewahrt die vollständige Linkstruktur:

```text
report/
├── index.html
├── 2012/
│   ├── week-49/index.html
│   ├── week-50/index.html
│   └── 12/06 … 12/index.html
└── 11/
    ├── pgbadger.min.css
    ├── pgbadger.min.js
    └── bundled chart and UI assets
```

Der oberste Index verweist auf zwei wöchentliche und sieben tägliche Berichte. Alle relativen Links wurden beibehalten. Wenn Sie nur `index.html` verschieben, wird das Beispiel daher unbrauchbar; bewahren Sie den vollständigen Verzeichnisbaum zusammen auf.

## Sicherheit und Datenschutz {#security-and-privacy}

Reale Berichte können SQL-Text, Bind-Werte, Datenbank- und Benutzernamen, Anwendungsnamen, Client-Adressen, Fehlerdetails und Lastmuster offenlegen. Bevor ein Bericht veröffentlicht wird:

- verwenden Sie `--anonymize`, wenn Literalwerte nicht benötigt werden;
- wenden Sie Ein- und Ausschlussfilter vor der Berichtserstellung an;
- prüfen Sie das endgültige HTML oder die exportierten Daten, nicht nur die Befehlszeile;
- schützen Sie den Speicherort der Berichte ebenso sorgfältig wie Betriebsprotokolle.
