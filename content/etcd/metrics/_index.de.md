---
title: "Metriken"
weight: 1350
description: "Metriken für Echtzeitüberwachung und Fehlersuche"
icon: fa-solid fa-chart-line
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/metrics/_index.md"
---

etcd verwendet [Prometheus][prometheus] zur Bereitstellung von Metriken. Sie lassen sich für Echtzeitüberwachung und Fehlersuche nutzen. etcd speichert seine Metriken nicht dauerhaft; beim Neustart eines Mitglieds werden sie zurückgesetzt.

Die verfügbaren Metriken lassen sich am einfachsten mit cURL am Metrikendpunkt `/metrics` abrufen. Das Format wird [in der Prometheus-Dokumentation](http://prometheus.io/docs/instrumenting/exposition_formats/) beschrieben.

Mit der [Prometheus-Einstiegsanleitung][prometheus-getting-started] lässt sich ein Prometheus-Server zum Sammeln von etcd-Metriken starten.

Die Benennung der Metriken folgt den empfohlenen [bewährten Verfahren von Prometheus][prometheus-naming]. Ein Metrikname enthält `etcd` oder `etcd_debugging` als Namensraumpräfix sowie ein Präfix für das Subsystem (zum Beispiel `wal` und `etcdserver`).

## Metriken im Namensraum etcd {#etcd-namespace-metrics}

Metriken mit dem Präfix `etcd` dienen der Überwachung und Alarmierung. Sie sind stabile Metriken auf hoher Abstraktionsebene. Änderungen an diesen Metriken werden in den Versionshinweisen aufgeführt.

Metriken zu etcd2 sind im [v2-Metrikleitfaden][v2-http-metrics] dokumentiert.

### Server {#server}

Diese Metriken beschreiben den Zustand des etcd-Servers. Um Ausfälle oder Probleme für die Fehlersuche zu erkennen, sollten die Servermetriken jedes etcd-Clusters im Produktivbetrieb genau überwacht werden.

Alle diese Metriken haben das Präfix `etcd_server_`

| Name                      | Beschreibung                                              | Typ    |
|---------------------------|----------------------------------------------------------|---------|
| has_leader                | Ob ein Leader vorhanden ist. 1 bedeutet vorhanden, 0 bedeutet nicht vorhanden.| Gauge   |
| leader_changes_seen_total | Anzahl der beobachteten Leader-Wechsel.                       | Counter |
| proposals_committed_total | Gesamtzahl der festgeschriebenen Konsensvorschläge.       | Gauge   |
| proposals_applied_total   | Gesamtzahl der angewendeten Konsensvorschläge.         | Gauge   |
| proposals_pending         | Aktuelle Anzahl der ausstehenden Vorschläge.                 | Gauge   |
| proposals_failed_total    | Gesamtzahl der beobachteten fehlgeschlagenen Vorschläge.               | Counter |

`has_leader` zeigt an, ob das Mitglied einen Leader hat. Ohne Leader ist ein Mitglied vollständig nicht verfügbar. Hat kein Mitglied im Cluster einen Leader, ist der gesamte Cluster vollständig nicht verfügbar.

`leader_changes_seen_total` zählt die Leader-Wechsel, die das Mitglied seit seinem Start beobachtet hat. Häufige Leader-Wechsel beeinträchtigen die Leistung von etcd erheblich. Sie weisen auch auf einen instabilen Leader hin, möglicherweise aufgrund von Netzwerkverbindungsproblemen oder übermäßiger Last auf dem etcd-Cluster.

`proposals_committed_total` erfasst die Gesamtzahl der festgeschriebenen Konsensvorschläge. In einem funktionsfähigen Cluster sollte dieser Gauge-Wert mit der Zeit steigen. Mehrere funktionsfähige Mitglieder eines etcd-Clusters können zum selben Zeitpunkt unterschiedliche Gesamtzahlen festgeschriebener Vorschläge haben. Mögliche Gründe dafür sind das Nachholen von Daten von Peers nach dem Start, ein Rückstand gegenüber dem Leader oder die Rolle als Leader, der deshalb die meisten Commits hat. Wichtig ist, diese Metrik über alle Clustermitglieder hinweg zu beobachten: Ein dauerhaft großer Rückstand eines einzelnen Mitglieds gegenüber seinem Leader deutet darauf hin, dass das Mitglied langsam oder nicht funktionsfähig ist.

`proposals_applied_total` erfasst die Gesamtzahl der angewendeten Konsensvorschläge. Der etcd-Server wendet jeden festgeschriebenen Vorschlag asynchron an. Der Unterschied zwischen `proposals_committed_total` und `proposals_applied_total` sollte normalerweise gering sein (selbst unter hoher Last innerhalb weniger Tausend). Steigt die Differenz weiter an, weist dies auf eine Überlastung des etcd-Servers hin. Das kann bei aufwendigen Abfragen geschehen, etwa umfangreichen Bereichsabfragen oder großen txn-Operationen.

`proposals_pending` zeigt an, wie viele Vorschläge zum Festschreiben anstehen. Eine steigende Zahl ausstehender Vorschläge deutet auf hohe Clientlast hin oder darauf, dass das Mitglied Vorschläge nicht festschreiben kann.

`proposals_failed_total` hängt normalerweise mit zwei Problemen zusammen: vorübergehenden Fehlern während einer Leader-Wahl oder längeren Ausfällen durch den Verlust des Quorums im Cluster.

### Datenträger {#disk}

Diese Metriken beschreiben den Zustand der Datenträgeroperationen.

Alle diese Metriken haben das Präfix `etcd_disk_`.

| Name                               | Beschreibung                                           | Typ      |
|------------------------------------|-------------------------------------------------------|-----------|
| wal_fsync_duration_seconds         | Latenzverteilungen der von wal aufgerufenen fsync-Operationen      | Histogram |
| backend_commit_duration_seconds    | Latenzverteilungen der vom Backend aufgerufenen commit-Operationen.| Histogram |

`wal_fsync` wird aufgerufen, wenn etcd seine Protokolleinträge auf dem Datenträger dauerhaft speichert, bevor es sie anwendet.

`backend_commit` wird aufgerufen, wenn etcd einen inkrementellen Snapshot seiner neuesten Änderungen auf dem Datenträger festschreibt.

Hohe Latenzen bei Datenträgeroperationen (`wal_fsync_duration_seconds` oder `backend_commit_duration_seconds`) weisen häufig auf Datenträgerprobleme hin. Sie können hohe Anfragelatenzen verursachen oder den Cluster instabil machen.

### Netzwerk {#network}

Diese Metriken beschreiben den Zustand des Netzwerks.

Alle diese Metriken haben das Präfix `etcd_network_`

| Name                            | Beschreibung                                                        | Typ          |
|---------------------------------|--------------------------------------------------------------------|---------------|
| peer_sent_bytes_total           | Gesamtzahl der an den Peer mit der ID `To` gesendeten Bytes.           | Counter(To)   |
| peer_received_bytes_total       | Gesamtzahl der vom Peer mit der ID `From` empfangenen Bytes.   | Counter(From) |
| peer_sent_failures_total        | Gesamtzahl der Sendefehler zum Peer mit der ID `To`.      | Counter(To)   |
| peer_received_failures_total    | Gesamtzahl der Empfangsfehler vom Peer mit der ID `From`. | Counter(From) |
| peer_round_trip_time_seconds    | Histogramm der Umlaufzeiten zwischen Peers.                           | Histogram(To) |
| client_grpc_sent_bytes_total    | Gesamtzahl der an gRPC-Clients gesendeten Bytes.                    | Counter       |
| client_grpc_received_bytes_total| Gesamtzahl der von gRPC-Clients empfangenen Bytes.                | Counter       |

`peer_sent_bytes_total` zählt die Gesamtzahl der an einen bestimmten Peer gesendeten Bytes. Normalerweise sendet das Leader-Mitglied mehr Daten als andere Mitglieder, da es die replizierten Daten überträgt.

`peer_received_bytes_total` zählt die Gesamtzahl der von einem bestimmten Peer empfangenen Bytes. Normalerweise empfangen Follower-Mitglieder nur Daten vom Leader-Mitglied.

### gRPC-Anfragen {#grpc-requests}

Diese Metriken werden über [go-grpc-prometheus][go-grpc-prometheus] bereitgestellt.

## Metriken im Namensraum etcd_debugging {#etcd_debugging-namespace-metrics}

Die Metriken mit dem Präfix `etcd_debugging` dienen der Fehlersuche. Sie hängen stark von der Implementierung ab und ändern sich häufig. In neuen etcd-Versionen können sie ohne Vorwarnung geändert oder entfernt werden. Einige dieser Metriken können zum Präfix `etcd` wechseln, sobald sie stabiler sind.

### Snapshot {#snapshot}

| Name                                       | Beschreibung                                                | Typ      |
|--------------------------------------------|------------------------------------------------------------|-----------|
| snapshot_save_total_duration_seconds       | Verteilungen der Gesamtlatenz der von snapshot aufgerufenen save-Operationen | Histogram |

Eine ungewöhnlich lange Snapshot-Dauer (`snapshot_save_total_duration_seconds`) weist auf Datenträgerprobleme hin und kann den Cluster instabil machen.

## Von Prometheus bereitgestellte Metriken {#prometheus-supplied-metrics}

Die Prometheus-Clientbibliothek stellt zahlreiche Metriken in den Namensräumen `go` und `process` bereit. Einige sind besonders interessant.

| Name                              | Beschreibung                                | Typ         |
|-----------------------------------|--------------------------------------------|--------------|
| process_open_fds                  | Anzahl offener Dateideskriptoren.           | Gauge        |
| process_max_fds                   | Maximale Anzahl offener Dateideskriptoren.   | Gauge        |

> [!NOTE]
> Prozessmetriken wie `process_open_fds` und `process_max_fds` werden derzeit auf Darwin-Systemen (macOS) nicht unterstützt.

Eine hohe Nutzung von Dateideskriptoren (`process_open_fds`), also nahe am Limit des Prozesses (`process_max_fds`), weist auf eine mögliche Erschöpfung der Dateideskriptoren hin. Sind keine Dateideskriptoren mehr verfügbar, kann etcd mit einer Panic abbrechen, weil es keine neuen WAL-Dateien erstellen kann.

## Generierte Liste der Metriken {#generated-list-of-metrics}

[go-grpc-prometheus]: https://github.com/grpc-ecosystem/go-grpc-prometheus
[prometheus]: https://prometheus.io/
[prometheus-getting-started]: https://prometheus.io/docs/introduction/getting_started/
[prometheus-naming]: https://prometheus.io/docs/practices/naming/
[v2-http-metrics]: https://etcd.io/docs/v2.3/metrics/#http-requests
