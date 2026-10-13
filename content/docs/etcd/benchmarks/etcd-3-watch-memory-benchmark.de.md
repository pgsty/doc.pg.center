---
title: "Benchmark zum Speicherverbrauch von Watches"
weight: 5250
description: "Leistungsmessungen für etcd-Watcher"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-3-watch-memory-benchmark.md"
aliases: [/etcd/benchmarks/etcd-3-watch-memory-benchmark/]
---

> [!NOTE]
> Die Watch-Funktionen werden aktiv weiterentwickelt; ihr Speicherverbrauch kann sich dabei ändern. Wir erwarten nicht, dass er die unten angegebenen Werte wesentlich übersteigt.

Ein wesentliches Ziel von etcd ist die Unterstützung sehr vieler Watcher mit einer außerordentlich großen Zahl von Watch-Registrierungen. Angestrebt werden O(10k) Clients, O(100K) Watch-Streams (O(10) Streams pro Client) und insgesamt O(10M) Watch-Registrierungen (O(100) pro Stream). Der Speicherverbrauch der einzelnen Watch-Registrierungen macht den größten Teil des gesamten Speicherverbrauchs von etcd aus und steht deshalb im Mittelpunkt der aktuellen und künftigen Optimierungen.


Drei zusammengehörige Komponenten der Watch-Funktion von etcd beanspruchen physischen Speicher: jede `grpc.Conn`, jeder Watch-Stream und jede einzelne Watch-Registrierung. `grpc.Conn` verwaltet die tatsächliche TCP-Verbindung und weitere gRPC-Verbindungszustände. Jede `grpc.Conn` beansprucht O(10kb) Speicher und kann mehrere Watch-Streams haben.

Jeder Watch-Stream ist eine eigenständige HTTP2-Verbindung, die weitere O(10kb) Speicher beansprucht.
Mehrere Watch-Registrierungen können sich einen Watch-Stream teilen.

Eine Watch-Registrierung ist die eigentliche Struktur, die Änderungen im Schlüssel-Wert-Speicher verfolgt. Jede Registrierung sollte nur < O(1kb) beanspruchen.

```
                                          +-------+
                                          | watch |
                              +---------> | foo   |
                              |           +-------+
                       +------+-----+
                       |   stream   |
      +--------------> |            |
      |                +------+-----+     +-------+
      |                       |           | watch |
      |                       +---------> | bar   |
+-----+------+                            +-------+
|            |         +------------+
|   conn     +-------> |   stream   |
|            |         |            |
+-----+------+         +------------+
      |
      |
      |
      |                +------------+
      +--------------> |   stream   |
                       |            |
                       +------------+
```

Der theoretische Speicherverbrauch von Watch lässt sich mit folgender Formel näherungsweise berechnen:
`memory = c1 * number_of_conn + c2 * avg_number_of_stream_per_conn + c3 * avg_number_of_watch_stream`

## Testumgebung {#testing-environment}

etcd-Version
- Git-Stand https://github.com/etcd-io/etcd/commit/185097ffaa627b909007e772c175e8fefac17af3

GCE-Rechnertyp n1-standard-2
- 7.5 GB Arbeitsspeicher
- 2x CPUs

## Gesamter Speicherverbrauch {#overall-memory-usage}

Der gesamte Speicherverbrauch erfasst, wie viel [RSS][rss] etcd mit den Client-Watchern beansprucht. Obwohl das Ergebnis um bis zu 10% schwanken kann, ist es aussagekräftig: Ziel ist, den ungefähren Speicherverbrauch und das Muster der Speicherzuweisungen zu verstehen.

Aus dem Benchmark-Ergebnis lassen sich näherungsweise `c1 = 17kb`, `c2 = 18kb` und `c3 = 350bytes` berechnen. Jede zusätzliche Clientverbindung beansprucht also 17kb Speicher, jeder zusätzliche Stream 18kb und jede weitere Watch-Registrierung nur 350bytes. Ein einzelner etcd-Server kann im Normalfall Millionen von Watch-Registrierungen mit wenigen GB Arbeitsspeicher verwalten.


| Clients | Streams pro Client | Watch-Registrierungen pro Stream | Watch-Registrierungen insgesamt | Speicherverbrauch |
|---------|---------|-----------|----------------|--------------|
| 1k |  1 |   1 |   1k |   50MB |
| 2k |  1 |   1 |   2k |   90MB |
| 5k |  1 |   1 |   5k |  200MB |
| 1k | 10 |   1 |  10k |  217MB |
| 2k | 10 |   1 |  20k |  417MB |
| 5k | 10 |   1 |  50k |  980MB |
| 1k | 50 |   1 |  50k | 1001MB |
| 2k | 50 |   1 | 100k | 1960MB |
| 5k | 50 |   1 | 250k | 4700MB |
| 1k | 50 |  10 | 500k | 1171MB |
| 2k | 50 |  10 |   1M | 2371MB |
| 5k | 50 |  10 | 2.5M | 5710MB |
| 1k | 50 | 100 |   5M | 2380MB |
| 2k | 50 | 100 |  10M | 4672MB |
| 5k | 50 | 100 |  25M |  *OOM* |

[rss]: https://en.wikipedia.org/wiki/Resident_set_size
