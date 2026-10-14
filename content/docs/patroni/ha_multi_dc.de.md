---
title: "Hochverfügbarkeit über mehrere Rechenzentren"
weight: 170
icon: fa-solid fa-globe
description: "Hochverfügbarkeitsarchitekturen mit Patroni-Replikation über mehrere Rechenzentren."
module: [PATRONI]
categories: [Konzept]
aliases: [/patroni/ha_multi_dc/]
upstream_link: "https://patroni.readthedocs.io/en/latest/ha_multi_dc.html"
---

<a id="ha_multi_dc"></a>
Die Hochverfügbarkeit eines PostgreSQL-Clusters über mehrere Rechenzentren basiert auf synchroner oder asynchroner Replikation (siehe [Replikationsmodi](/de/docs/patroni/replication_modes#replication_modes)).

In beiden Fällen sind folgende Grundsätze wichtig:

- Postgres kann nur dann als Primärserver oder Standby-Leader laufen, wenn es den Leader-Schlüssel besitzt und aktualisieren kann.
- Die Anzahl der etcd-, ZooKeeper- oder Consul-Knoten sollte ungerade sein: 3 oder 5!

--------

## Synchrone Replikation {#synchronous-replication}

Ein Cluster über mehrere Rechenzentren (DC), der den Ausfall einer Zone automatisch verkraften soll, benötigt mindestens 3 Zonen.

Das Architekturdiagramm sieht folgendermaßen aus:

![Bild](/img/docs/patroni/multi-dc-synchronous-replication.png)

Ein Cluster aus etcd, ZooKeeper oder Consul muss über die verschiedenen Rechenzentren verteilt werden, mit mindestens 3 Knoten und jeweils einem Knoten pro Zone.

Für Postgres müssen mindestens 2 Knoten in unterschiedlichen Rechenzentren bereitgestellt werden. Anschließend muss `synchronous_mode: true` in der globalen [dynamischen Konfiguration](/de/docs/patroni/config/dynamic#dynamic) gesetzt werden.

Dies aktiviert synchrone Replikation; der Primärserver wählt einen der Knoten als synchronen Knoten aus.

--------

## Asynchrone Replikation {#asynchronous-replication}

Bei nur zwei Rechenzentren ist es besser, zwei unabhängige etcd-Cluster zu betreiben und im zweiten Rechenzentrum einen Patroni-[Standby-Cluster](/de/docs/patroni/standby_cluster#standby_cluster) einzurichten. Fällt der erste Standort aus, kann der [standby_cluster](/de/docs/patroni/standby_cluster#standby_cluster) MANUELL hochgestuft werden.

Das Architekturdiagramm sieht folgendermaßen aus:

![Bild](/img/docs/patroni/multi-dc-asynchronous-replication.png)

Eine automatische Hochstufung ist nicht möglich, da DC2 den Zustand von DC1 niemals sicher bestimmen kann.

In diesem Szenario sollte `pg_ctl promote` nicht verwendet werden. Stattdessen muss der funktionsfähige Cluster „manuell hochgestuft“ werden, indem der Abschnitt [standby_cluster](/de/docs/patroni/standby_cluster#standby_cluster) aus der [dynamischen Konfiguration](/de/docs/patroni/config/dynamic#dynamic) entfernt wird.

> [!WARNING]
> Läuft der Quellcluster noch und wird der Standby-Cluster hochgestuft, entsteht eine Split-Brain-Situation.

Um zum „ursprünglichen“ Zustand zurückzukehren, gibt es nur zwei Möglichkeiten:

- Den Abschnitt standby_cluster wieder hinzufügen. Dies löst `pg_rewind` aus. Damit `pg_rewind` ordnungsgemäß funktioniert, muss der Cluster mit `data page checksums` (Option `--data-checksums` für `initdb`) initialisiert worden sein und/oder `wal_log_hints` muss auf `on` gesetzt sein. Dennoch kann `pg_rewind` aus anderen Gründen fehlschlagen.
- Den Standby-Cluster vollständig neu aufbauen.

Vor der Hochstufung des Standby-Clusters muss manuell sichergestellt werden, dass der Quellcluster heruntergefahren ist (STONITH). Sobald DC1 wieder verfügbar ist, muss dessen Cluster in einen Standby-Cluster umgewandelt werden.

Zuvor kann die Datenbank manuell untersucht werden, um alle Änderungen zu extrahieren, die zwischen dem Ausfall der Netzwerkverbindung von DC1 zu DC2 und dem manuellen Stoppen des Clusters in DC1 erfolgt sind.

Die extrahierten Änderungen können anschließend auch manuell auf den Cluster in DC2 angewendet werden.
