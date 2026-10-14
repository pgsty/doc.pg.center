---
title: "Konfiguration der PostgreSQL-Protokollierung"
linkTitle: "PostgreSQL-Protokollierung"
weight: 40
description: "Abfrageprotokollierung, log_line_prefix, Locale und ergänzende Statistikdaten für pgBadger konfigurieren"
search_keywords: [--prefix, lc_messages, log_autovacuum_min_duration, log_checkpoints, log_connections, log_disconnections, log_duration, log_error_verbosity, log_line_prefix, log_lock_waits, log_min_duration_statement, log_statement, log_temp_files, prefix, stderr, syslog]
icon: fa-solid fa-database
module: [PGBADGER]
categories: [Aufgabe]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger kann nur Informationen auswerten, die PostgreSQL in das Protokoll schreibt. Beginnen Sie mit einem analysierbaren Präfix und einer gezielt gewählten Richtlinie für die Anweisungsprotokollierung. Fügen Sie anschließend die Betriebsereignisse hinzu, die Sie analysieren möchten.

## Mindestkonfiguration für die Abfrageprotokollierung {#minimum-query-logging}

Um Abfragetext und -dauer zu erfassen, aktivieren Sie die dauerabhängige Protokollierung von Anweisungen:

```postgresql
log_min_duration_statement = 0
```

`0` protokolliert jede abgeschlossene Anweisung. Auf einem stark ausgelasteten Server sollten Sie einen höheren Schwellenwert in Millisekunden wählen, um das Protokollvolumen zu begrenzen. Prüfen Sie den zusätzlichen Aufwand und die Zunahme des Speicherbedarfs, bevor Sie in der Produktion einen niedrigen Schwellenwert aktivieren.

Wenn Sie nur Dauer und Anzahl der Abfragen, aber nicht den Abfragetext benötigen, verwenden Sie:

```postgresql
log_min_duration_statement = -1
log_duration = on
```

Verwenden Sie vorzugsweise `log_min_duration_statement`, wenn Sie Berichte über die langsamsten Abfragen und die Gesamtabfragezeit benötigen.

## Erforderliche Präfixfelder {#required-prefix-fields}

Ein benutzerdefinierter `log_line_prefix` muss die beiden folgenden Felder enthalten:

- ein Zeitfeld: `%t`, `%m` oder `%n`;
- ein Prozess- oder Sitzungsfeld: `%p` oder `%c`.

Ein minimales `stderr`-Präfix ist:

```postgresql
log_line_prefix = '%t [%p]: '
```

Ein nützlicheres Präfix protokolliert Benutzer, Datenbank, Anwendung und Client:

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

Das entsprechende Präfix für ein syslog-Ziel lässt die bereits durch syslog bereitgestellten Zeitstempel- und Prozessfelder weg:

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

Eine weitere unterstützte Reihenfolge der Schlüssel ist:

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

Wenn Ihr Präfix keiner von pgBadger erkannten Form entspricht, übergeben Sie den exakten Wert mit `--prefix`. Geben Sie ihn genau wie in `postgresql.conf` an; vereinfachen oder verändern Sie ihn nicht.

## Empfohlene Ereigniseinstellungen {#recommended-event-settings}

Aktivieren Sie die Ereignisklassen, die im Bericht erscheinen sollen:

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

Diese Einstellungen können erheblichen Protokollverkehr erzeugen. Insbesondere protokollieren `log_temp_files = 0` und `log_autovacuum_min_duration = 0` jedes passende Ereignis; passen Sie die Werte an die Arbeitslast und das Aufbewahrungsbudget an.

## Servernachrichten auf Englisch beibehalten {#message-locale}

Der Parser erkennt PostgreSQL-Servernachrichten auf Englisch. Verwenden Sie entweder:

```postgresql
lc_messages = 'en_US.UTF-8'
```

oder:

```postgresql
lc_messages = 'C'
```

Locale-Einstellungen wie `fr_FR.UTF-8` werden vom Parser des Originalprojekts nicht unterstützt.

## Widersprüchliche Einstellungen für Anweisungen vermeiden {#statement-setting-conflicts}

Aktivieren Sie `log_min_duration_statement`, `log_duration` und `log_statement = 'all'` nicht gemeinsam. Dieselbe Ausführung kann mehrfach protokolliert werden, was zu fälschlich überhöhten pgBadger-Zählern und einer erheblich größeren Protokollmenge führt.

| Ziel | Empfohlene Einstellung |
|---|---|
| Abfragetext und Zeitmessung | `log_min_duration_statement = 0` oder ein gewählter Schwellenwert |
| Dauer und Anzahl allein | `log_min_duration_statement = -1`, `log_duration = on` |
| Umfassende Protokollierung von Anweisungen | Behandeln Sie `log_statement` als separate Protokollierungsrichtlinie; kombinieren Sie die drei Einstellungen nicht für pgBadger-Statistiken |

Prüfen Sie nach dem Neuladen von PostgreSQL mehrere echte Protokolleinträge, bevor Sie eine umfangreiche Analyse ausführen. Stellen Sie sicher, dass die Felder für Zeitstempel, Prozess-/Sitzungskennung, Benutzer, Datenbank, Anwendung und Client dem ausgewählten Format entsprechen.
