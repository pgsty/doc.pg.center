---
title: "Hardwareempfehlungen"
weight: 4400
description: "Hardwarehinweise für die Verwaltung von etcd-Clustern"
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/hardware.md"
---

etcd läuft für Entwicklung und Tests in der Regel auch mit begrenzten Ressourcen gut; die Entwicklung mit etcd auf einem Laptop oder einer günstigen Cloud-Instanz ist üblich. Für den produktiven Betrieb von etcd-Clustern helfen jedoch einige Hardwarehinweise bei der sachgerechten Verwaltung. Diese Empfehlungen sind keine starren Regeln, sondern ein guter Ausgangspunkt für eine robuste Produktivinstallation. Wie immer sollten Installationen vor dem produktiven Einsatz mit simulierten Arbeitslasten getestet werden.

## CPUs {#cpus}

Nur wenige etcd-Installationen benötigen viel CPU-Leistung. Typische Cluster kommen für einen reibungslosen Betrieb mit zwei bis vier Kernen aus.
Stark ausgelastete etcd-Installationen, die Tausende von Clients oder Zehntausende von Anfragen pro Sekunde bedienen, sind meist durch die CPU begrenzt, da etcd Anfragen aus dem Arbeitsspeicher bedienen kann. Solche Installationen benötigen gewöhnlich acht bis sechzehn dedizierte Kerne.


## Arbeitsspeicher {#memory}

etcd hat einen vergleichsweise geringen Speicherbedarf, seine Leistung hängt aber dennoch von ausreichend Arbeitsspeicher ab. Ein etcd-Server speichert Schlüssel-Wert-Daten umfassend zwischen und verwendet den größten Teil des übrigen Speichers zur Verwaltung von Watchern. Typischerweise reichen 8GB aus. Für große Installationen mit Tausenden von Watchern und Millionen von Schlüsseln entsprechend 16GB bis 64GB Arbeitsspeicher vorsehen.


## Datenträger {#disks}

Schnelle Datenträger sind der wichtigste Faktor für Leistung und Stabilität einer etcd-Installation.

Ein langsamer Datenträger erhöht die Latenz von etcd-Anfragen und kann die Clusterstabilität beeinträchtigen. Da das Konsensprotokoll von etcd auf der dauerhaften Speicherung von Metadaten in einem Log beruht, muss eine Mehrheit der Clustermitglieder jede Anfrage auf den Datenträger schreiben. Zusätzlich schreibt etcd seinen Zustand schrittweise als Checkpoints auf den Datenträger, um dieses Log kürzen zu können. Dauern diese Schreiboperationen zu lange, können Heartbeats ihr Zeitlimit überschreiten und eine Wahl auslösen, was die Clusterstabilität beeinträchtigt. Ob ein Datenträger für etcd schnell genug ist, lässt sich im Allgemeinen mit einem Benchmarkwerkzeug wie [fio][fio] ermitteln. Ein Beispiel steht [hier][fio-blog-post].

etcd reagiert sehr empfindlich auf die Schreiblatenz von Datenträgern. Typischerweise sind 50 sequenzielle IOPS erforderlich (z. B. eine Festplatte mit 7200 RPM). Für stark ausgelastete Cluster werden 500 sequenzielle IOPS empfohlen (z. B. eine typische lokale SSD oder ein leistungsfähiges virtualisiertes Blockgerät). Die meisten Cloud-Anbieter veröffentlichen parallele statt sequenzieller IOPS; die veröffentlichten parallelen IOPS können 10x höher als die sequenziellen IOPS sein. Um die tatsächlichen sequenziellen IOPS zu messen, empfiehlt sich ein Datenträger-Benchmarkwerkzeug wie [diskbench][diskbench] oder [fio][fio].

etcd benötigt nur eine mäßige Datenträgerbandbreite. Eine höhere Bandbreite verkürzt aber die Wiederherstellungszeit, wenn ein ausgefallenes Mitglied zum Cluster aufschließen muss. Typischerweise lassen sich mit 10MB/s 100MB Daten innerhalb von 15 Sekunden wiederherstellen. Für große Cluster werden mindestens 100MB/s empfohlen, um 1GB Daten innerhalb von 15 Sekunden wiederherzustellen.

Für die Speicherung von etcd nach Möglichkeit eine SSD verwenden. Eine SSD bietet gewöhnlich niedrigere und weniger schwankende Schreiblatenzen als eine rotierende Festplatte und verbessert damit Stabilität und Zuverlässigkeit von etcd. Bei rotierenden Festplatten die schnellstmöglichen Modelle wählen (15,000 RPM). RAID 0 ist ebenfalls ein wirksames Mittel, die Datenträgergeschwindigkeit zu erhöhen, sowohl bei Festplatten als auch bei SSDs. Bei mindestens drei Clustermitgliedern sind RAID-Varianten mit Spiegelung und/oder Parität nicht erforderlich; die konsistente Replikation von etcd sorgt bereits für Hochverfügbarkeit.


## Netzwerk {#network}

etcd-Installationen mit mehreren Mitgliedern profitieren von einem schnellen und zuverlässigen Netzwerk. Da etcd sowohl Konsistenz als auch Partitionstoleranz gewährleisten muss, führt ein unzuverlässiges Netzwerk mit Unterbrechungen durch Partitionen zu schlechter Verfügbarkeit. Niedrige Latenz ermöglicht eine schnelle Kommunikation zwischen etcd-Mitgliedern. Hohe Bandbreite kann die Wiederherstellungszeit eines ausgefallenen Mitglieds verkürzen. Für gängige etcd-Installationen reicht 1GbE aus. Bei großen etcd-Clustern verkürzt ein 10GbE-Netzwerk die mittlere Wiederherstellungszeit.

etcd-Mitglieder nach Möglichkeit innerhalb eines einzigen Rechenzentrums bereitstellen, um zusätzliche Latenz zu vermeiden und die Wahrscheinlichkeit von Netzwerkpartitionen zu verringern. Wird ein separater Ausfallbereich in einem anderen Rechenzentrum benötigt, ein möglichst nahe gelegenes Rechenzentrum wählen. Weitere Informationen zu Installationen über mehrere Rechenzentren hinweg enthält die Dokumentation zur [Optimierung][tuning].


## Beispiele für Hardwarekonfigurationen {#example-hardware-configurations}

Im Folgenden stehen einige beispielhafte Hardwarekonfigurationen für AWS- und GCE-Umgebungen. Wie bereits erwähnt, gilt auch hier: Administratoren sollten eine etcd-Installation vor dem produktiven Einsatz mit einer simulierten Arbeitslast testen.

Diese Konfigurationen setzen voraus, dass die Rechner ausschließlich für etcd vorgesehen sind. Werden darauf neben etcd weitere Anwendungen ausgeführt, können Ressourcenkonflikte entstehen und den Cluster instabil machen.

### Kleiner Cluster {#small-cluster}

Ein kleiner Cluster bedient weniger als 100 Clients und weniger als 200 Anfragen pro Sekunde und speichert höchstens 100MB Daten.

Beispielarbeitslast: ein Kubernetes-Cluster mit 50 Knoten

| Anbieter | Typ | vCPUs | Arbeitsspeicher (GB) | Maximale parallele IOPS | Datenträgerbandbreite (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.large | 2 | 8 | 3600 | 56.25 |
| GCE | n1-standard-2 + 50GB PD SSD | 2 | 7.5 | 1500 | 25 |


### Mittlerer Cluster {#medium-cluster}

Ein mittlerer Cluster bedient weniger als 500 Clients und weniger als 1,000 Anfragen pro Sekunde und speichert höchstens 500MB Daten.

Beispielarbeitslast: ein Kubernetes-Cluster mit 250 Knoten

| Anbieter | Typ | vCPUs | Arbeitsspeicher (GB) | Maximale parallele IOPS | Datenträgerbandbreite (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.xlarge | 4 | 16 | 6000 | 93.75 |
| GCE | n1-standard-4 + 150GB PD SSD | 4 | 15 | 4500 | 75 |


### Großer Cluster {#large-cluster}

Ein großer Cluster bedient weniger als 1,500 Clients und weniger als 10,000 Anfragen pro Sekunde und speichert höchstens 1GB Daten.

Beispielarbeitslast: ein Kubernetes-Cluster mit 1,000 Knoten

| Anbieter | Typ | vCPUs | Arbeitsspeicher (GB) | Maximale parallele IOPS | Datenträgerbandbreite (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.2xlarge | 8 | 32 | 8000 | 125 |
| GCE | n1-standard-8 + 250GB PD SSD | 8 | 30 | 7500 | 125 |


### Sehr großer Cluster {#xlarge-cluster}

Ein sehr großer Cluster bedient mehr als 1,500 Clients und mehr als 10,000 Anfragen pro Sekunde und speichert mehr als 1GB Daten.

Beispielarbeitslast: ein Kubernetes-Cluster mit 3,000 Knoten

| Anbieter | Typ | vCPUs | Arbeitsspeicher (GB) | Maximale parallele IOPS | Datenträgerbandbreite (MB/s) |
|----------|------|-------|--------|------|----------------|
| AWS | m4.4xlarge | 16 | 64 | 16,000 | 250 |
| GCE | n1-standard-16 + 500GB PD SSD | 16 | 60 | 15,000 | 250 |


[diskbench]: https://github.com/ongardie/diskbenchmark
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[tuning]: /de/etcd/tuning/
