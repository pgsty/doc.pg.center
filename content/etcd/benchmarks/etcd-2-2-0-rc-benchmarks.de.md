---
title: "Benchmarks für etcd v2.2.0-rc"
weight: 5625
description: "Leistungsmessungen für etcd v2.2.0-rc"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-2-2-0-rc-benchmarks.md"
---

## Physischer Rechner {#physical-machine}

GCE-Rechnertyp n1-highcpu-2

- 1x dedizierte lokale SSD, unter /var/lib/etcd eingebunden
- 1x dedizierter langsamer Datenträger für das Betriebssystem
- 1.8 GB Arbeitsspeicher
- 2x CPUs

## etcd-Cluster {#etcd-cluster}

3 Mitglieder mit etcd 2.2.0-rc, jeweils auf einem eigenen Rechner.

Versionsdetails:

```
etcd Version: 2.2.0-alpha.1+git
Git SHA: 59a5a7e
Go Version: go1.4.2
Go OS/Arch: linux/amd64
```

Außerdem bilden wir aus 3 Mitgliedern mit etcd 2.1.0 im Alpha-Stadium einen Cluster, um die Ausgangsleistung zu ermitteln. Der verwendete etcd-Commit ist [c7146bd5][c7146bd5], derselbe wie im [etcd-2.1-Benchmark][etcd-2.1-benchmark].

## Testverfahren {#testing}

Einen weiteren Rechner einrichten und mit dem [HTTP-Benchmarkwerkzeug hey][hey] Anfragen an jedes etcd-Mitglied senden. Eine ausführliche Anleitung enthält der [Leitfaden zur Benchmark-Entwicklung][hack-benchmark].

## Leistung {#performance}

### Einen einzelnen Schlüssel lesen {#reading-one-single-key}

| Schlüsselgröße in Bytes | Anzahl der Clients | etcd-Zielserver | Lese-QPS | 90. Latenzperzentil (ms) |
|-------------------|-------------------|--------------------|----------|---------------|
| 64                | 1                 | nur Leader        | 2804 (-5%) | 0.4 (+0%) |
| 64                | 64                | nur Leader        | 17816 (+0%) | 5.7 (-6%) |
| 64                | 256               | nur Leader        | 18667 (-6%) | 20.4 (+2%) |
| 256               | 1                 | nur Leader        | 2181 (-15%) | 0.5 (+25%) |
| 256               | 64                | nur Leader        | 17435 (-7%) | 6.0 (+9%) |
| 256               | 256               | nur Leader        | 18180 (-8%) | 21.3 (+3%) |
| 64                | 64                | alle Server        | 46965 (-4%) | 2.1 (+0%) |
| 64                | 256               | alle Server        | 55286 (-6%) | 7.4 (+6%) |
| 256               | 64                | alle Server        | 46603 (-6%) | 2.1 (+5%) |
| 256               | 256               | alle Server        | 55291 (-6%) | 7.3 (+4%) |

### Einen einzelnen Schlüssel schreiben {#writing-one-single-key}

| Schlüsselgröße in Bytes | Anzahl der Clients | etcd-Zielserver | Schreib-QPS | 90. Latenzperzentil (ms) |
|-------------------|-------------------|--------------------|-----------|---------------|
| 64                | 1                 | nur Leader        | 76 (+22%)  | 19.4 (-15%) |
| 64                | 64                | nur Leader        | 2461 (+45%) | 31.8 (-32%) |
| 64                | 256               | nur Leader        | 4275 (+1%) | 69.6 (-10%) |
| 256               | 1                 | nur Leader        | 64 (+20%)  | 16.7 (-30%) |
| 256               | 64                | nur Leader        | 2385 (+30%) | 31.5 (-19%) |
| 256               | 256               | nur Leader        | 4353 (-3%) | 74.0 (+9%) |
| 64                | 64                | alle Server        | 2005 (+81%) | 49.8 (-55%) |
| 64                | 256               | alle Server        | 4868 (+35%) | 81.5 (-40%) |
| 256               | 64                | alle Server        | 1925 (+72%) | 47.7 (-59%) |
| 256               | 256               | alle Server        | 4975 (+36%) | 70.3 (-36%) |

### Erklärung der Leistungsänderungen {#performance-changes-explanation}

- Die Lese-QPS sinken in den meisten Szenarien um 5~8%. Der Grund ist, dass etcd für jede Speicheroperation Speichermetriken erfasst. Diese sind für Überwachung und Fehlersuche wichtig, weshalb der Rückgang vertretbar ist.

- Die Schreib-QPS an den Leader steigen um 20~30%. Dies liegt daran, dass wir die Raft-Hauptschleife von der Schleife zum Anwenden der Einträge entkoppeln, sodass sie sich nicht gegenseitig blockieren.

- Die Schreib-QPS an alle Server steigen um 30~80%, weil Follower den neuesten Commit-Index früher erhalten und Vorschläge schneller festschreiben können.

[c7146bd5]: https://github.com/etcd-io/etcd/commits/c7146bd5f2c73716091262edc638401bb8229144
[etcd-2.1-benchmark]: /de/etcd/benchmarks/etcd-2-1-0-alpha-benchmarks/
[hack-benchmark]: https://github.com/etcd-io/etcd/tree/v2.3.8/hack/benchmark
[hey]: https://github.com/rakyll/hey
