---
title: "Benchmark zum Speicherverbrauch der Speicherschicht"
weight: 5125
description: "Leistungsmessungen für die etcd-Speicherschicht (Index im Arbeitsspeicher und Seitencache)"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/benchmarks/etcd-storage-memory-benchmark.md"
aliases: [/etcd/benchmarks/etcd-storage-memory-benchmark/]
---

<!---todo: link storage to storage design doc-->
Zwei Komponenten der etcd-Speicherschicht beanspruchen physischen Speicher. Der etcd-Prozess legt einen *Index im Arbeitsspeicher* an, um Schlüssel schneller nachzuschlagen. Der vom Betriebssystem verwaltete *Seitencache* des Prozesses hält kürzlich vom Datenträger gelesene Daten zur schnellen Wiederverwendung vor.

Der Index im Arbeitsspeicher enthält alle Schlüssel in einer [B-Baum][btree]-Datenstruktur, zusammen mit Zeigern auf die Daten (die Werte) auf dem Datenträger. Jeder Schlüssel im B-Baum kann mehrere Zeiger enthalten, die auf verschiedene Versionen seiner Werte verweisen. Der theoretische Speicherverbrauch des Index lässt sich daher mit folgender Formel näherungsweise berechnen:

`N * (c1 + avg_key_size) + N * (avg_versions_of_key) * (c2 + size_of_pointer)`

Dabei ist `c1` der Zusatzaufwand für Schlüsselmetadaten und `c2` der Zusatzaufwand für Versionsmetadaten.

Die Grafik zeigt den detaillierten Aufbau des B-Baum-Index im Arbeitsspeicher.

```


                                In mem index

                               +------------+
                               | key || ... |
  +--------------+             |     ||     |
  |              |             +------------+
  |              |             | v1  || ... |
  |   disk    <----------------|     ||     | Tree Node
  |              |             +------------+
  |              |             | v2  || ... |
  |           <----------------+     ||     |
  |              |             +------------+
  +--------------+       +-----+    |   |   |
                         |     |    |   |   |
                         |     +------------+
                         |
                         |
                         ^
                      ------+
                      | ... |
                      |     |
                      +-----+
                      | ... | Tree Node
                      |     |
                      +-----+
                      | ... |
                      |     |
                      ------+
```

Der [Seitencache][pagecache] wird vom Betriebssystem verwaltet und in diesem Dokument nicht näher behandelt.

## Testumgebung {#testing-environment}

etcd-Version
- Git-Stand https://github.com/etcd-io/etcd/commit/776e9fb7be7eee5e6b58ab977c8887b4fe4d48db

GCE-Rechnertyp n1-standard-2

- 7.5 GB Arbeitsspeicher
- 2x CPUs

## Speicherverbrauch des Index im Arbeitsspeicher {#in-memory-index-memory-usage}

Dieser Test misst ausschließlich den Speicherverbrauch des Index im Arbeitsspeicher. Ziel ist, die oben genannten Werte `c1` und `c2` zu bestimmen und die feste Grenze des Speicherverbrauchs der Speicherschicht zu verstehen.

Wir berechnen den Speicherverbrauch mit der Go-Funktion runtime.ReadMemStats. Dazu ermitteln wir die Differenz der insgesamt zugewiesenen Bytes vor und nach dem Erstellen des Index. Dies bildet den Speicherverbrauch des Index selbst nicht exakt ab, zeigt aber das ungefähre Verbrauchsmuster.

| N    | Versionen | Schlüsselgröße | Speicherverbrauch |
|------|----------|----------|--------------|
| 100K | 1        | 64bytes  | 22MB         |
| 100K | 5        | 64bytes  | 39MB         |
| 1M   | 1        | 64bytes  | 218MB        |
| 1M   | 5        | 64bytes  | 432MB        |
| 100K | 1        | 256bytes | 41MB         |
| 100K | 5        | 256bytes | 65MB         |
| 1M   | 1        | 256bytes | 409MB        |
| 1M   | 5        | 256bytes | 506MB        |


Aus den Ergebnissen lassen sich `c1=120bytes` und `c2=30bytes` berechnen. Da `c1` und `c2` die einzigen Unbekannten in der Formel sind, reichen zwei Datensätze zu ihrer Berechnung aus. Die Werte `c1=120bytes` und `c2=30bytes` sind die Mittelwerte der 4 berechneten Wertepaarungen für `c1` und `c2`. Bei kleinen Schlüssel-Wert-Paaren ist der Zusatzaufwand für Schlüsselmetadaten mit 50% weiterhin beträchtlich. Gegenüber dem alten Speicher mit mindestens 1000% Zusatzaufwand ist dies jedoch eine erhebliche Verbesserung.

## Gesamter Speicherverbrauch {#overall-memory-usage}

Der gesamte Speicherverbrauch erfasst, wie viel RSS etcd mit der Speicherschicht beansprucht. Die Größe der Werte sollte den gesamten Speicherverbrauch von etcd nur wenig beeinflussen, da die Werte auf dem Datenträger liegen und nur häufig verwendete Werte im Arbeitsspeicher verbleiben, verwaltet vom Seitencache des Betriebssystems.

| N    | Versionen | Schlüsselgröße | Wertgröße | Speicherverbrauch |
|------|----------|----------|------------|--------------|
| 100K | 1        | 64bytes  | 256bytes   | 40MB         |
| 100K | 5        | 64bytes  | 256bytes   | 89MB         |
| 1M   | 1        | 64bytes  | 256bytes   | 470MB        |
| 1M   | 5        | 64bytes  | 256bytes   | 880MB        |
| 100K | 1        | 64bytes  | 1KB        | 102MB        |
| 100K | 5        | 64bytes  | 1KB        | 164MB        |
| 1M   | 1        | 64bytes  | 1KB        | 587MB        |
| 1M   | 5        | 64bytes  | 1KB        | 836MB        |

Die Ergebnisse zeigen, dass die Größe der Werte den Speicherverbrauch nicht wesentlich beeinflusst. Er steigt geringfügig, weil der Seitencache des Betriebssystems mehr Daten vorhält.

[btree]: https://en.wikipedia.org/wiki/B-tree
[pagecache]: https://en.wikipedia.org/wiki/Page_cache
