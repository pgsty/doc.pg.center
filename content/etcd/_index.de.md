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
upstream_source: etcd-20261121
categories: [Konzept]
search_keywords: [v3.7.4, "Go 1.26.11", force-new-cluster, NewJournalWriter]
upstream_link: "https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7"
cascade:
  upstream_source: etcd-20261121
  type: docs
  module: [ETCD]
---

etcd ist ein verteilter Schlüssel-Wert-Speicher mit starker Konsistenz. Diese Anleitungen behandeln die Installation und den Betrieb von etcd, die Entwicklung von Anwendungen mit seinen APIs, den internen Aufbau, Leistungsmessungen sowie Upgrades und Downgrades von Clustern innerhalb der Versionsreihe 3.7.

Beginnen Sie mit dem [Schnellstart](/de/etcd/quickstart/) für einen lokalen Ein-Mitglied-Cluster, der [Installation](/de/etcd/install/) für unterstützte Installationswege oder dem [Betriebshandbuch](/de/etcd/op-guide/) für Produktionsumgebungen.

## etcd v3.7.4 {#etcd-v3-7-4}

Die aktuelle Wartungsversion ist [v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4), veröffentlicht am 19. November 2026. Die Installations-, Docker- und Kubernetes-Beispiele dieser Ausgabe beziehen sich auf diese Version.

- Korrigiert die Wiederherstellung mit `--force-new-cluster`, wenn der konsistente Index des Backends vor dem WAL liegt.
- Verwendet einen atomaren Zeiger für den Alarm-Store, um eine Race-Condition zu vermeiden.
- Korrigiert eine Panic beim Start während des Abspielens alter v2-WAL-Einträge für Mitgliederattribute.
- Wird mit Go 1.26.11 gebaut.

Siehe das [fixierte Upstream-Changelog](https://github.com/etcd-io/etcd/blob/1ce5a2b779143279c89ed8c7e33a42e51fb697fa/CHANGELOG/CHANGELOG-3.7.md#v374-tbc). Dessen Überschrift sagt noch „TBC“; das veröffentlichte Release-Tag belegt die Verfügbarkeit.

## etcd v3.7.3 {#etcd-v3-7-3}

Die vorherige Wartungsversion war [v3.7.3](https://github.com/etcd-io/etcd/releases/tag/v3.7.3).

- Behebt Datenrennen zwischen `Hash` und `Restore` im MVCC-Speicher sowie in `RangeStream`-Operationen, die nur Schlüssel zurückgeben. Außerdem wird eine Regression der Replikationsleistung behoben, die dadurch entstand, dass der Leader `MsgApp`-Nachrichten in umgekehrter Reihenfolge sendete.
- Wird mit Go 1.26.10 gebaut und aktualisiert die Abhängigkeiten OpenTelemetry und `golang.org/x/net`, um gemeldete Sicherheitsprobleme zu beheben.
- Markiert `NewJournalWriter` in `client/pkg/v3/logutil` als veraltet; die Entfernung ist für v3.8 geplant.

Die vollständigen Änderungen stehen im [Upstream-Änderungsprotokoll](https://github.com/etcd-io/etcd/blob/f164b70fdf458a17aba05dfefc685d7de4c9ca37/CHANGELOG/CHANGELOG-3.7.md#v373-2026-10-22).
