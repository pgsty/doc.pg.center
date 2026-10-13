---
title: "Benchmarks für etcd v2.2.0"
weight: 5750
description: "Leistungsmessungen für etcd v2.2.0"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-benchmarks.md"
aliases: [/etcd/benchmarks/etcd-2-2-0-benchmarks/]
---

## Physische Rechner {#physical-machines}

GCE-Rechnertyp n1-highcpu-2

- 1x dedizierte lokale SSD, als etcd-Datenverzeichnis eingebunden
- 1x dedizierter langsamer Datenträger für das Betriebssystem
- 1.8 GB Arbeitsspeicher
- 2x CPUs

## etcd-Cluster {#etcd-cluster}

3 etcd-2.2.0-Mitglieder, jeweils auf einem eigenen Rechner.

Versionsdetails:

```
etcd Version: 2.2.0
Git SHA: e4561dd
Go Version: go1.5
Go OS/Arch: linux/amd64
```

## Testverfahren {#testing}

Einen weiteren Rechner außerhalb des etcd-Clusters einrichten und das [HTTP-Benchmarkwerkzeug `hey`](https://github.com/rakyll/hey) mit einem Patch zur Wiederverwendung von Verbindungen ausführen, um Anfragen an jedes Clustermitglied zu senden. Die [Benchmark-Anleitung](https://github.com/etcd-io/etcd/tree/v2.3.8/hack/benchmark) enthält den Patch und die Schritte zum Reproduzieren unserer Vorgehensweise.

Die Leistung wird aus den Ergebnissen von 100 Benchmark-Durchläufen berechnet.

## Leistung {#performance}

### Leseleistung für einen einzelnen Schlüssel {#single-key-read-performance}

| Schlüsselgröße in Bytes | Anzahl der Clients | etcd-Zielserver | Durchschnitt der Lese-QPS | Standardabweichung der Lese-QPS | Durchschnitt des 90. Latenzperzentils (ms) | Standardabweichung der Latenz |
|-------------------|-------------------|--------------------|------------------|-----------------|--------------------------------------|----------------|
| 64 | 1 | nur Leader | 2303 | 200 | 0.49 | 0.06 |
| 64 | 64 | nur Leader | 15048 | 685 | 7.60 | 0.46 |
| 64 | 256 | nur Leader | 14508 | 434 | 29.76 | 1.05 |
| 256 | 1 | nur Leader | 2162 | 214 | 0.52 | 0.06 |
| 256 | 64 | nur Leader | 14789 | 792 | 7.69| 0.48 |
| 256 | 256 | nur Leader | 14424 | 512 | 29.92 | 1.42 |
| 64 | 64 | alle Server | 45752 | 2048 | 2.47 | 0.14 |
| 64 | 256 | alle Server | 46592 | 1273 | 10.14 | 0.59 |
| 256 | 64 | alle Server | 45332 | 1847 | 2.48| 0.12 |
| 256 | 256 | alle Server | 46485 | 1340 | 10.18 | 0.74 |

### Schreibleistung für einen einzelnen Schlüssel {#single-key-write-performance}

| Schlüsselgröße in Bytes | Anzahl der Clients | etcd-Zielserver | Durchschnitt der Schreib-QPS | Standardabweichung der Schreib-QPS | Durchschnitt des 90. Latenzperzentils (ms) | Standardabweichung der Latenz |
|-------------------|-------------------|--------------------|------------------|-----------------|--------------------------------------|----------------|
| 64 | 1 | nur Leader | 55 | 4 | 24.51 | 13.26 |
| 64 | 64 | nur Leader | 2139 | 125 | 35.23 | 3.40 |
| 64 | 256 | nur Leader | 4581 | 581 | 70.53 | 10.22 |
| 256 | 1 | nur Leader | 56 | 4 | 22.37| 4.33 |
| 256 | 64 | nur Leader | 2052 | 151 | 36.83 | 4.20 |
| 256 | 256 | nur Leader | 4442 | 560 | 71.59 | 10.03 |
| 64 | 64 | alle Server | 1625 | 85 | 58.51 | 5.14 |
| 64 | 256 | alle Server | 4461 | 298 | 89.47 | 36.48 |
| 256 | 64 | alle Server | 1599 | 94 | 60.11| 6.43 |
| 256 | 256 | alle Server | 4315 | 193 | 88.98 | 7.01 |

## Leistungsänderungen {#performance-changes}

- Da etcd jetzt für jeden API-Aufruf Metriken erfasst, scheinen die Lese-QPS in den meisten Szenarien geringfügig zu sinken. Angesichts der umfangreichen Informationen für Überwachung und Fehlersuche wurde dieser minimale Leistungsverlust als vertretbar eingeschätzt.

- Die Schreib-QPS an Cluster-Leader scheinen leicht gestiegen zu sein. Ursache ist die Entkopplung der Hauptschleife von den Schleifen zum Anwenden der Einträge in der Raft-Logik von etcd. Dadurch entfallen mehrere gegenseitige Blockierungen.

- Die Schreib-QPS an alle Mitglieder scheinen erheblich gestiegen zu sein, weil Follower den neuesten Commit-Index jetzt früher erhalten und Vorschläge schneller festschreiben.
