---
title: "Leistung"
weight: 4550
description: "Leistung verstehen: Latenz und Durchsatz"
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/performance.md"
aliases: [/etcd/op-guide/performance/]
---

## Leistung verstehen {#understanding-performance}

etcd bietet eine stabile, dauerhaft hohe Leistung. Zwei Faktoren bestimmen die Leistung: Latenz und Durchsatz. Die Latenz ist die Zeit bis zum Abschluss einer Operation. Der Durchsatz ist die Gesamtzahl der in einem bestimmten Zeitraum abgeschlossenen Operationen. Nimmt etcd gleichzeitige Clientanfragen an, steigt die mittlere Latenz gewöhnlich mit dem Gesamtdurchsatz. In gängigen Cloud-Umgebungen, etwa auf einer standardmäßigen `n-4`-Instanz bei Google Compute Engine (GCE) oder einem vergleichbaren AWS-Instanztyp, schließt ein etcd-Cluster mit drei Mitgliedern bei geringer Last eine Anfrage in weniger als einer Millisekunde ab und kann bei hoher Last mehr als 30,000 Anfragen pro Sekunde verarbeiten.

etcd verwendet den Raft-Konsensalgorithmus, um Anfragen zwischen Mitgliedern zu replizieren und Einigkeit herzustellen. Die Konsensleistung, insbesondere die Commit-Latenz, wird durch zwei physikalische Grenzen bestimmt: die Latenz der Netzwerk-IO und die Latenz der Datenträger-IO. Die Mindestdauer einer etcd-Anfrage ergibt sich aus der Netzwerkumlaufzeit (Round Trip Time, RTT) zwischen den Mitgliedern zuzüglich der Zeit, die `fdatasync` benötigt, um die Daten dauerhaft zu speichern. Innerhalb eines Rechenzentrums kann die RTT mehrere Hundert Mikrosekunden betragen. Eine typische RTT innerhalb der USA liegt bei etwa 50ms und kann zwischen Kontinenten bis zu 400ms erreichen. Die typische fdatasync-Latenz einer rotierenden Festplatte liegt bei etwa 10ms, bei SSDs häufig unter 1ms. Um den Durchsatz zu erhöhen, bündelt etcd mehrere Anfragen und übergibt sie gemeinsam an Raft. Diese Bündelung ermöglicht etcd auch bei hoher Last einen hohen Durchsatz.

Weitere Teilsysteme beeinflussen die Gesamtleistung von etcd. Jede serialisierte etcd-Anfrage muss die boltdb-basierte MVCC-Speicherengine durchlaufen, was gewöhnlich einige zehn Mikrosekunden dauert. Regelmäßig erstellt etcd inkrementelle Snapshots der zuletzt angewendeten Anfragen und führt sie mit dem vorherigen Snapshot auf dem Datenträger zusammen. Dieser Vorgang kann eine Latenzspitze verursachen. Auf SSDs ist dies gewöhnlich unproblematisch, auf HDD kann sich die beobachtete Latenz jedoch verdoppeln. Auch laufende Kompaktierungen können die Leistung von etcd beeinflussen. Ihre Auswirkung ist glücklicherweise oft gering, da die Kompaktierung zeitlich gestaffelt erfolgt und so nicht mit regulären Anfragen um Ressourcen konkurriert. Das RPC-System gRPC bietet etcd eine klar definierte, erweiterbare API, verursacht aber auch zusätzliche Latenz, insbesondere bei lokalen Lesezugriffen.

## Benchmarks {#benchmarks}

Die Leistung von etcd lässt sich mit dem enthaltenen CLI-Werkzeug [benchmark](https://github.com/etcd-io/etcd/tree/main/tools/benchmark) messen.

Als Grundlage für einige Leistungskennzahlen dient ein etcd-Cluster mit drei Mitgliedern und folgender Hardwarekonfiguration:

- Google Cloud Compute Engine
- 3 Rechner mit 8 vCPUs + 16GB Arbeitsspeicher + 50GB SSD
- 1 Rechner (Client) mit 16 vCPUs + 30GB Arbeitsspeicher + 50GB SSD
- Ubuntu 17.04
- etcd 3.2.0, go 1.8.3

Mit dieser Konfiguration erreicht etcd ungefähr folgende Schreibleistung:

| Anzahl der Schlüssel | Schlüsselgröße in Bytes | Wertgröße in Bytes | Anzahl der Verbindungen | Anzahl der Clients | etcd-Zielserver | Mittlere Schreib-QPS | Mittlere Latenz pro Anfrage | Mittlerer Server-RSS |
|---------------:|------------------:|--------------------:|----------------------:|------------------:|--------------------|------------------:|----------------------------:|-------------------:|
| 10,000 | 8 | 256 | 1 | 1 | nur Leader | 583 | 1.6ms | 48 MB |
| 100,000 | 8 | 256 | 100 | 1000 | nur Leader | 44,341 | 22ms |  124MB |
| 100,000 | 8 | 256 | 100 | 1000 | alle Mitglieder |  50,104 | 20ms |  126MB |

Beispielbefehle:

```sh
# write to leader
benchmark --endpoints=${HOST_1} --target-leader --conns=1 --clients=1 \
    put --key-size=8 --sequential-keys --total=10000 --val-size=256
benchmark --endpoints=${HOST_1} --target-leader  --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256

# write to all members
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    put --key-size=8 --sequential-keys --total=100000 --val-size=256
```

Linearisierbare Leseanfragen beziehen ein Quorum von Clustermitgliedern in die Konsensbildung ein, um die neuesten Daten abzurufen. Serialisierbare Leseanfragen sind günstiger, da sie von einem beliebigen einzelnen etcd-Mitglied statt von einem Quorum bedient werden; dafür können sie veraltete Daten zurückgeben. etcd erreicht folgende Leseleistung:

| Anzahl der Anfragen | Schlüsselgröße in Bytes | Wertgröße in Bytes | Anzahl der Verbindungen | Anzahl der Clients | Konsistenz | Mittlere Lese-QPS | Mittlere Latenz pro Anfrage |
|-------------------:|------------------:|--------------------:|----------------------:|------------------:|-------------|-----------------:|----------------------------:|
| 10,000 | 8 | 256 | 1 | 1 | Linearisierbar | 1,353 | 0.7ms |
| 10,000 | 8 | 256 | 1 | 1 | Serialisierbar | 2,909 | 0.3ms |
| 100,000 | 8 | 256 | 100 | 1000 | Linearisierbar | 141,578 | 5.5ms |
| 100,000 | 8 | 256 | 100 | 1000 | Serialisierbar | 185,758 | 2.2ms |

Beispielbefehle:

```sh
# Single connection read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=l --total=10000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=1 --clients=1 \
    range YOUR_KEY --consistency=s --total=10000

# Many concurrent read requests
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=l --total=100000
benchmark --endpoints=${HOST_1},${HOST_2},${HOST_3} --conns=100 --clients=1000 \
    range YOUR_KEY --consistency=s --total=100000
```

Beim erstmaligen Einrichten eines etcd-Clusters in einer neuen Umgebung wird empfohlen, den Benchmarktest auszuführen, um eine angemessene Leistung sicherzustellen. Latenz und Durchsatz des Clusters können empfindlich auf geringe Unterschiede in der Umgebung reagieren.
