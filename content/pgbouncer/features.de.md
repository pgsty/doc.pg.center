---
title: "Funktionen"
weight: 10
description: "PgBouncer-Funktionen — Pooling-Modi und SQL-Kompatibilität"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [Konzept]
upstream_link: "https://www.pgbouncer.org/features.html"
---

- Mehrere Pooling-Modi mit unterschiedlich restriktiver Verbindungszuweisung:

  **Sitzungs-Pooling**
  : Die am wenigsten restriktive Methode. Wenn ein Client eine Verbindung herstellt, wird ihm für die gesamte Dauer der Clientverbindung eine Serververbindung zugewiesen. Trennt der Client die Verbindung, wird die Serververbindung wieder in den Pool zurückgegeben. Dieser Modus unterstützt sämtliche PostgreSQL-Funktionen.

  **Transaktions-Pooling**
  : Eine Serververbindung wird einem Client nur für die Dauer einer Transaktion zugewiesen. Sobald PgBouncer erkennt, dass die Transaktion beendet ist, wird die Serververbindung wieder in den Pool zurückgegeben. Dieser Modus ist mit einigen sitzungsbezogenen Funktionen von PostgreSQL nicht kompatibel. Er kann nur eingesetzt werden, wenn die Anwendung darauf abgestimmt ist und keine inkompatiblen Funktionen verwendet. Die folgende Tabelle führt diese Funktionen auf.

  **Statement-Pooling**
  : Die restriktivste Methode. Sie entspricht dem Transaktions-Pooling, lässt jedoch keine Transaktionen mit mehreren Anweisungen zu. Damit wird auf der Clientseite der „Autocommit“-Modus erzwungen; der Modus ist vor allem für PL/Proxy vorgesehen.

- Geringer Speicherbedarf (standardmäßig 2 kB pro Verbindung), da PgBouncer vollständige Pakete nicht auf einmal einlesen muss.

- PgBouncer ist nicht an einen einzelnen Backend-Server gebunden. Die Zieldatenbanken können sich auf unterschiedlichen Hosts befinden.

- Unterstützt für die meisten Einstellungen eine Neukonfiguration im laufenden Betrieb.

- Unterstützt [rollierende Neustarts und Upgrades](/de/pgbouncer/usage/#shutdown-wait_for_clients) mit mehreren Prozessen und [`so_reuseport`](/de/pgbouncer/config/#so_reuseport). Der bisherige Neustart im laufenden Betrieb (`-R`) wurde in 1.26.0 entfernt.

--------

## SQL-Funktionsmatrix für Pooling-Modi {#sql-feature-map-for-pooling-modes}

Die folgende Tabelle zeigt verschiedene PostgreSQL-Funktionen und ihre Kompatibilität mit den Pooling-Modi von PgBouncer. Beachten Sie, dass das *Transaktions-Pooling* das vom Client erwartete Serververhalten bewusst verändert. Es kann daher nur verwendet werden, wenn die Anwendung darauf abgestimmt ist und keine inkompatiblen Funktionen nutzt.

| Funktion                          | Sitzungs-Pooling  | Transaktions-Pooling  |
|----------------------------------|:-----------------:|:---------------------:|
| Startparameter [^0]              | Ja                | Ja                    |
| SET/RESET                        | Ja                | Für nachverfolgte Parameter [^0] |
| LISTEN                           | Ja                | Nie                   |
| NOTIFY                           | Ja                | Ja                    |
| WITHOUT HOLD CURSOR              | Ja                | Ja                    |
| WITH HOLD CURSOR                 | Ja                | Nie                   |
| Auf Protokollebene vorbereitete Ausführungspläne | Ja        | Ja [^1]               |
| PREPARE / DEALLOCATE             | Ja                | Nie                   |
| Temporäre Tabellen mit ON COMMIT DROP | Ja             | Ja                    |
| Temporäre Tabellen mit PRESERVE/DELETE ROWS | Ja       | Nie                   |
| Zurücksetzen zwischengespeicherter Pläne | Ja                | Ja                    |
| LOAD-Anweisung                   | Ja                | Nie                   |
| Advisory Locks auf Sitzungsebene | Ja                | Nie                   |

[^0]: Seit 1.26.0 verfolgt PgBouncer alle vom Server gemeldeten Parameter nach, die Clients ändern können: `application_name`, `client_encoding`, `DateStyle`, `default_transaction_read_only` (PostgreSQL 14+), `IntervalStyle`, `scram_iterations` (PostgreSQL 16+), `search_path` (PostgreSQL 18+), `session_authorization`, `standard_conforming_strings` und `TimeZone`. Bei Parametern, die der Server nicht meldet, werden nur die Startwerte nachverfolgt; spätere Änderungen durch `SET` werden nicht nachverfolgt. Einzelheiten und Hinweise zu Parametern von Erweiterungen finden sich unter [`track_extra_parameters`](/de/pgbouncer/config/#track_extra_parameters) und [`ignore_startup_parameters`](/de/pgbouncer/config/#ignore_startup_parameters).

[^1]: Die Unterstützung vorbereiteter Anweisungen auf Protokollebene ist aktiviert, wenn [`max_prepared_statements`](/de/pgbouncer/config/#max_prepared_statements) ungleich null ist. Der Standardwert ist 200; der Wert 0 deaktiviert diese Unterstützung. `PREPARE` / `DEALLOCATE` auf SQL-Ebene bleibt mit Transaktions-Pooling inkompatibel; ausgenommen sind `DEALLOCATE ALL` und `DISCARD ALL` bei aktivierter Nachverfolgung.
