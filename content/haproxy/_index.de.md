---
title: "HAProxy 3.4.8 Dokumentation"
linkTitle: HAProxy
weight: 50
description: "Vollständige deutsche Markdown-Ausgabe der HAProxy-3.4-Handbücher für Einstieg, Konfiguration und Verwaltung."
icon: fa-solid fa-network-wired
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
no_list: true
module: [HAPROXY]
categories: [Referenz]
upstream_source: haproxy-20261121
upstream_link: "https://docs.haproxy.org/3.4/intro.html"
cascade:
  upstream_source: haproxy-20261121
  type: docs
  module: [HAPROXY]
---

**HAProxy** ist ein freier, schneller und zuverlässiger Reverse-Proxy für Hochverfügbarkeit, TCP- und HTTP-Lastverteilung sowie die Verwaltung des Anwendungsverkehrs. Diese Sammlung enthält die vollständige deutsche Übersetzung der drei grundlegenden HAProxy-3.4-Handbücher, neu gegliedert als eine flache Markdown-Lesefolge für OINK.

Diese Ausgabe folgt der offiziellen **3.4.8 LTS**-Version vom 18. November 2026, fixiert auf [Tag v3.4.8](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8). Die geprüften Übersetzungen enthalten die 3.4.8-Aktualisierungen.

## Handbuch auswählen {#choose-a-manual}

- [Einsteigerhandbuch](/de/haproxy/load-balancing/) — 9 Themen zu Lastverteilung, HAProxy-Architektur, Funktionen, Dimensionierung, Versionen und Ökosystem.
- [Konfigurationshandbuch](/de/haproxy/http-fundamentals/) — 12 Kapitel zu Proxys, ACLs, Samples, Protokollierung, Filtern und sämtlichen Optionsgruppen.
- [Verwaltungshandbuch](/de/haproxy/prerequisites/) — 13 Kapitel zu Start, Neuladen, Ressourcen, Protokollierung, Statistiken, Runtime-CLI, Fehlerbehebung und Sicherheit.
{.cards}

## Umfang dieser Ausgabe {#edition-coverage}

| Handbuch | Originalquelle | Lokale Gliederung |
| --- | ---: | ---: |
| Einsteigerhandbuch | 1,695 Zeilen | 9 flache Themenseiten |
| Konfigurationshandbuch | 33,277 Zeilen | 12 flache Kapitelseiten |
| Verwaltungshandbuch | 5,305 Zeilen | 13 flache Kapitelseiten |

Alle 34 Leseseiten liegen direkt im HAProxy-Dokumentationsverzeichnis. Drei nicht verlinkte Trennelemente gliedern die Handbücher in der Seitenleiste, ohne zusätzliche Verzeichnisebenen oder Einträge in der Seitennavigation einzuführen.

Die vollständigen Originalhandbücher sind in der oben verlinkten Upstream-Revision verfügbar. Der [Lizenzhinweis des Originalprojekts](/third_party/haproxy/LICENSE) und der [GPLv2-Text](/third_party/haproxy/GPL-2.0) werden zusammen mit den Handbüchern veröffentlicht. Die chinesische Begleitausgabe (vereinfachtes Chinesisch) enthält die geprüften Aktualisierungen für 3.4.8.
