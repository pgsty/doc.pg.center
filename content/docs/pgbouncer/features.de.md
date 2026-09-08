---
title: "Funktionen"
weight: 10
description: "PgBouncer-Funktionen — Pooling-Modi und SQL-Kompatibilität"
icon: fa-solid fa-wand-magic-sparkles
module: [PGBOUNCER]
categories: [Konzept]
aliases: [/pgbouncer/features/]
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

- Unterstützt Neustarts und Upgrades im laufenden Betrieb, ohne Clientverbindungen zu trennen.

--------

## SQL-Funktionsmatrix für Pooling-Modi {#sql-feature-map-for-pooling-modes}

Die folgende Tabelle zeigt verschiedene PostgreSQL-Funktionen und ihre Kompatibilität mit den Pooling-Modi von PgBouncer. Beachten Sie, dass das *Transaktions-Pooling* das vom Client erwartete Serververhalten bewusst verändert. Es kann daher nur verwendet werden, wenn die Anwendung darauf abgestimmt ist und keine inkompatiblen Funktionen nutzt.

| Funktion                          | Sitzungs-Pooling  | Transaktions-Pooling  |
|----------------------------------|:-----------------:|:---------------------:|
| Startparameter [^0]              | Ja                | Ja                    |
| SET/RESET                        | Ja                | Nie                   |
| LISTEN                           | Ja                | Nie                   |
| NOTIFY                           | Ja                | Ja                    |
| CURSOR WITHOUT HOLD              | Ja                | Ja                    |
| CURSOR WITH HOLD                 | Ja                | Nie                   |
| Auf Protokollebene vorbereitete Anweisungen | Ja        | Ja [^1]               |
| PREPARE / DEALLOCATE             | Ja                | Nie                   |
| Temporäre Tabellen mit ON COMMIT DROP | Ja             | Ja                    |
| Temporäre Tabellen mit PRESERVE/DELETE ROWS | Ja       | Nie                   |
| Zurücksetzen zwischengespeicherter Pläne | Ja                | Ja                    |
| LOAD-Anweisung                   | Ja                | Nie                   |
| Advisory Locks auf Sitzungsebene | Ja                | Nie                   |

[^0]: Zu den Startparametern gehören `client_encoding`, `DateStyle`, `IntervalStyle`, `Timezone`, `standard_conforming_strings` und `application_name`. PgBouncer erkennt Änderungen an diesen Parametern und kann so gewährleisten, dass sie für den Client konsistent bleiben. Wenn PgBouncer weitere Parameter unterstützen soll, lesen Sie die Beschreibungen von [`track_extra_parameters`](/de/docs/pgbouncer/config/#track_extra_parameters) und [`ignore_startup_parameters`](/de/docs/pgbouncer/config/#ignore_startup_parameters).

[^1]: Um diese Unterstützung zu aktivieren, müssen Sie [`max_prepared_statements`](/de/docs/pgbouncer/config/#max_prepared_statements) auf einen Wert ungleich null setzen.
