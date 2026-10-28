---
title: "etcd 3.7 Dokumentation"
linkTitle: "etcd 3.7"
description: "Offizielle etcd-3.7-Anleitungen für Entwicklung, Betrieb, Upgrades, APIs und interne Abläufe."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
weight: 60
icon: fa-solid fa-gear
sidebar_root_for: self
sidebar_root_link_self: true
section_index: cards
section_index_columns: 3
upstream_source: etcd
categories: [Konzept]
search_keywords: [v3.7.3, "Go 1.26.10", NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7"
cascade:
  upstream_source: etcd
  type: docs
  module: [ETCD]
---

etcd ist ein verteilter Schlüssel-Wert-Speicher mit starker Konsistenz. Diese Anleitungen behandeln die Installation und den Betrieb von etcd, die Entwicklung von Anwendungen mit seinen APIs, den internen Aufbau, Leistungsmessungen sowie Upgrades und Downgrades von Clustern innerhalb der Versionsreihe 3.7.

Beginnen Sie mit dem [Schnellstart](/de/etcd/quickstart/) für einen lokalen Ein-Mitglied-Cluster, der [Installation](/de/etcd/install/) für unterstützte Installationswege oder dem [Betriebshandbuch](/de/etcd/op-guide/) für Produktionsumgebungen.

## etcd v3.7.3 {#etcd-v3-7-3}

Die aktuelle Wartungsversion ist [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3). Die Installations-, Docker- und Kubernetes-Beispiele dieser Ausgabe beziehen sich auf diese Version.

- Behebt Datenrennen zwischen `Hash` und `Restore` im MVCC-Speicher sowie in `RangeStream`-Operationen, die nur Schlüssel zurückgeben. Außerdem wird eine Regression der Replikationsleistung behoben, die dadurch entstand, dass der Leader `MsgApp`-Nachrichten in umgekehrter Reihenfolge sendete.
- Wird mit Go 1.26.10 gebaut und aktualisiert die Abhängigkeiten OpenTelemetry und `golang.org/x/net`, um gemeldete Sicherheitsprobleme zu beheben.
- Markiert `NewJournalWriter` in `client/pkg/v3/logutil` als veraltet; die Entfernung ist für v3.8 geplant.

Die vollständigen Änderungen stehen im [Upstream-Änderungsprotokoll](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22).
