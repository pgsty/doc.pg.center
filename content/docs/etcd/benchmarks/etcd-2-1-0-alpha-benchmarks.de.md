---
title: "Benchmarks für etcd v2.1.0"
weight: 5875
description: "Leistungsmessungen für etcd v2.1.0"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-1-0-alpha-benchmarks.md"
aliases: [/etcd/benchmarks/etcd-2-1-0-alpha-benchmarks/]
---

## Physische Rechner {#physical-machines}

GCE-Rechnertyp n1-highcpu-2

- 1x dedizierte lokale SSD, unter /var/lib/etcd eingebunden
- 1x dedizierter langsamer Datenträger für das Betriebssystem
- 1.8 GB Arbeitsspeicher
- 2x CPUs
- etcd-Version 2.1.0 alpha

## etcd-Cluster {#etcd-cluster}

3 etcd-Mitglieder, jeweils auf einem eigenen Rechner

## Testverfahren {#testing}

Einen weiteren Rechner einrichten und mit dem [HTTP-Benchmarkwerkzeug hey][hey] Anfragen an jedes etcd-Mitglied senden. Eine ausführliche Anleitung enthält der [Leitfaden zur Benchmark-Entwicklung][hack-benchmark].

## Leistung {#performance}

### Einen einzelnen Schlüssel lesen {#reading-one-single-key}

| Schlüsselgröße in Bytes | Anzahl der Clients | etcd-Zielserver | Lese-QPS | 90. Latenzperzentil (ms) |
|-------------------|-------------------|--------------------|----------|---------------|
| 64                | 1                 | nur Leader        | 1534     | 0.7        |
| 64                | 64                | nur Leader        | 10125    | 9.1      |
| 64                | 256               | nur Leader        | 13892    | 27.1      |
| 256               | 1                 | nur Leader        | 1530     | 0.8       |
| 256               | 64                | nur Leader        | 10106    | 10.1      |
| 256               | 256               | nur Leader        | 14667    | 27.0      |
| 64                | 64                | alle Server        | 24200    | 3.9      |
| 64                | 256               | alle Server        | 33300    | 11.8      |
| 256               | 64                | alle Server        | 24800    | 3.9      |
| 256               | 256               | alle Server        | 33000    | 11.5      |

### Einen einzelnen Schlüssel schreiben {#writing-one-single-key}

| Schlüsselgröße in Bytes | Anzahl der Clients | etcd-Zielserver | Schreib-QPS | 90. Latenzperzentil (ms) |
|-------------------|-------------------|--------------------|-----------|---------------|
| 64                | 1                 | nur Leader        | 60        | 21.4 |
| 64                | 64                | nur Leader        | 1742      | 46.8 |
| 64                | 256               | nur Leader        | 3982      | 90.5 |
| 256               | 1                 | nur Leader        | 58        | 20.3 |
| 256               | 64                | nur Leader        | 1770      | 47.8 |
| 256               | 256               | nur Leader        | 4157      | 105.3 |
| 64                | 64                | alle Server        | 1028      | 123.4 |
| 64                | 256               | alle Server        | 3260      | 123.8 |
| 256               | 64                | alle Server        | 1033      | 121.5 |
| 256               | 256               | alle Server        | 3061      | 119.3 |

[hack-benchmark]: https://github.com/etcd-io/etcd/tree/main/hack/benchmark
[hey]: https://github.com/rakyll/hey
