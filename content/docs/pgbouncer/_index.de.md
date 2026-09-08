---
title: "Dokumentation zu PgBouncer 1.25.2"
linkTitle: PgBouncer
weight: 30
description: >
  PgBouncer – ein leichtgewichtiger Verbindungspooler für PostgreSQL
icon: fa-solid fa-arrows-turn-to-dots
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBOUNCER]
categories: [Konzept]
aliases: [/pgbouncer/]
upstream_source: pgbouncer
upstream_link: "https://www.pgbouncer.org/"
cascade:
  upstream_source: pgbouncer
  type: docs
  module: [PGBOUNCER]
---

**PgBouncer** ist ein Verbindungspooler für PostgreSQL. Eine beliebige Client-Anwendung kann sich mit **PgBouncer** verbinden, als handele es sich um einen PostgreSQL-Server. **PgBouncer** stellt dann eine Verbindung zum eigentlichen Server her oder verwendet eine bereits bestehende Verbindung.

**PgBouncer** soll die Leistungseinbußen verringern, die beim Aufbau neuer Verbindungen zu PostgreSQL entstehen.

Damit die Transaktionssemantik beim Verbindungs-Pooling gewahrt bleibt, unterstützt **PgBouncer** mehrere Pooling-Modi, die sich in der Dauer der Verbindungszuweisung unterscheiden:

- **Sitzungs-Pooling**: Die am wenigsten restriktive Methode. Sobald ein Client eine Verbindung herstellt, wird ihm für die gesamte Verbindungsdauer eine Serververbindung zugewiesen. Trennt der Client die Verbindung, wird die Serververbindung wieder in den Pool zurückgegeben. Dies ist die Standardmethode.
- **Transaktions-Pooling**: Eine Serververbindung wird einem Client nur für die Dauer einer Transaktion zugewiesen. Sobald PgBouncer erkennt, dass die Transaktion beendet ist, wird die Serververbindung wieder in den Pool zurückgegeben.
- **Statement-Pooling**: Die restriktivste Methode. Die Serververbindung wird unmittelbar nach Abschluss einer Abfrage in den Pool zurückgegeben. Transaktionen mit mehreren Anweisungen sind in diesem Modus nicht zulässig.
