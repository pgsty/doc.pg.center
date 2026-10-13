---
title: "Benchmarks für etcd v3"
weight: 5375
description: "Leistungsmessungen für etcd v3"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-3-demo-benchmarks.md"
aliases: [/etcd/benchmarks/etcd-3-demo-benchmarks/]
---

## Physische Rechner {#physical-machines}

GCE-Rechnertyp n1-highcpu-2

- 1x dedizierte lokale SSD, unter /var/lib/etcd eingebunden
- 1x dedizierter langsamer Datenträger für das Betriebssystem
- 1.8 GB Arbeitsspeicher
- 2x CPUs
- etcd-Version 2.2.0

## etcd-Cluster {#etcd-cluster}

1 etcd-Mitglied im v3-Demomodus

## Testverfahren {#testing}

Das [Benchmarkwerkzeug für etcd v3][etcd-v3-benchmark] verwenden.

## Leistung {#performance}

### Einen einzelnen Schlüssel lesen {#reading-one-single-key}

| Schlüsselgröße in Bytes | Anzahl der Clients | Lese-QPS | 90. Latenzperzentil (ms) |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2716  | 0.4      |
| 256               | 64                | 16623 | 6.1      |
| 256               | 256               | 16622 | 21.7     |

Die Leistung ist nahezu gleich wie mit einem leeren Server-Handler.

### Einen einzelnen Schlüssel nach dem Schreiben lesen {#reading-one-single-key-after-putting}

| Schlüsselgröße in Bytes | Anzahl der Clients | Lese-QPS | 90. Latenzperzentil (ms) |
|-------------------|-------------------|----------|---------------|
| 256               | 1                 | 2269  | 0.5      |
| 256               | 64                | 13582 | 8.6      |
| 256               | 256               | 13262 | 47.5     |

Mit einem leeren Server-Handler beeinflusst ein einzelner put-Vorgang die Leistung nicht. Der Leistungsrückgang dürfte daher durch das Speicherpaket verursacht werden.

[etcd-v3-benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
