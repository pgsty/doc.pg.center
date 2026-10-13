---
title: etcd im Vergleich mit anderen Schlüssel-Wert-Speichern
weight: 2875
description: Geschichte und Verwendung von etcd im Vergleich mit anderen Werkzeugen
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/why.md"
aliases: [/etcd/learning/why/]
---

Der Name „etcd“ entstand aus zwei Ideen: dem Unix-Verzeichnis "/etc" und verteilten Systemen, auf Englisch „distributed systems“. Im Verzeichnis "/etc" liegen Konfigurationsdaten eines einzelnen Systems, während etcd Konfigurationsinformationen für große verteilte Systeme speichert. Aus „/etc“ und dem Anfangsbuchstaben von „distributed“ wird somit „etcd“.

etcd ist als allgemeine Grundlage für große verteilte Systeme ausgelegt. Diese Systeme tolerieren keinen Split-Brain-Betrieb und nehmen dafür Einschränkungen der Verfügbarkeit in Kauf. etcd speichert Metadaten konsistent und fehlertolerant. Ein etcd-Cluster soll einen Schlüssel-Wert-Speicher mit erstklassiger Stabilität, Zuverlässigkeit, Skalierbarkeit und Leistung bieten.

Verteilte Systeme verwenden etcd als konsistenten Schlüssel-Wert-Speicher für Konfigurationsverwaltung, Diensterkennung und die Koordination verteilter Arbeit. Viele [Organisationen][production-users] nutzen etcd für Produktivsysteme wie Container-Scheduler, Dienste zur Diensterkennung und verteilte Datenspeicherung. Häufige verteilte Entwurfsmuster mit etcd sind [Leader-Wahlen][etcd-etcdctl-elect], [verteilte Sperren][etcd-etcdctl-lock] und die Überwachung der Erreichbarkeit von Rechnern.

## Anwendungsfälle {#use-cases}

- Container Linux von CoreOS: Anwendungen auf [Container Linux][container-linux] erhalten automatische Linux-Kernel-Updates ohne Ausfallzeit. Container Linux koordiniert Updates mit [locksmith]. Locksmith implementiert über etcd ein verteiltes Semaphor, das sicherstellt, dass zu jedem Zeitpunkt nur ein Teil des Clusters neu startet.
- [Kubernetes][kubernetes] speichert Konfigurationsdaten für Diensterkennung und Clusterverwaltung in etcd. Die Konsistenz von etcd ist für die korrekte Einplanung und den Betrieb von Diensten entscheidend. Der Kubernetes-API-Server speichert den Clusterzustand dauerhaft in etcd. Er verwendet die Watch-API von etcd, um den Cluster zu überwachen und kritische Konfigurationsänderungen auszurollen.

## Vergleichstabelle {#comparison-chart}

Vielleicht erscheint etcd bereits passend. Wie bei jeder Technologieentscheidung ist jedoch Vorsicht geboten. Diese Dokumentation wurde vom etcd-Team verfasst. Obwohl ein unvoreingenommener Vergleich von Technik und Funktionen das Ziel ist, begünstigen Fachkenntnisse und Vorlieben der Autoren offensichtlich etcd. Nur nach Anweisung verwenden.

Die folgende Tabelle bietet einen schnellen Überblick über die Unterschiede zwischen etcd und seinen beliebtesten Alternativen. Weitere Erläuterungen und Einzelheiten zu jeder Spalte folgen in den Abschnitten nach der Tabelle.

|  | etcd | ZooKeeper | Consul | NewSQL (Cloud Spanner, CockroachDB, TiDB) |
| --- | --- | --- | --- | --- |
| Grundoperationen für Nebenläufigkeit | [Lock-RPCs][etcd-v3lock], [Election-RPCs][etcd-v3election], [Sperren per Befehlszeile][etcd-etcdctl-lock], [Wahlen per Befehlszeile][etcd-etcdctl-elect], [Rezepte][etcd-recipe] in Go | Externe [Curator-Rezepte][curator] in Java | [Native Sperr-API][consul-lock] | [Selten][newsql-leader], wenn überhaupt |
| Linearisierbare Lesezugriffe | [Ja][etcd-linread] | Nein | [Ja][consul-linread] | Manchmal |
| Mehrversions-Nebenläufigkeitskontrolle | [Ja][etcd-mvcc] | Nein | Nein | Manchmal |
| Transaktionen | [Feldvergleiche, Lesen, Schreiben][etcd-txn] | [Versionsprüfungen, Schreiben][zk-txn] | [Feldvergleich, Sperren, Lesen, Schreiben][consul-txn] | Im SQL-Stil |
| Änderungsbenachrichtigungen | [Historische und aktuelle Schlüsselintervalle][etcd-watch] | [Aktuelle Schlüssel und Verzeichnisse][zk-watch] | [Aktuelle Schlüssel und Präfixe][consul-watch] | Trigger (manchmal) |
| Benutzerberechtigungen | [Rollenbasiert][etcd-rbac] | [ACLs][zk-acl] | [ACLs][consul-acl] | Unterschiedlich ([GRANT][cockroach-grant] pro Tabelle, [Rollen][spanner-roles] pro Datenbank) |
| API für HTTP/JSON | [Ja][etcd-json] | Nein | [Ja][consul-json] | Selten |
| Neukonfiguration der Mitgliedschaft | [Ja][etcd-reconfig] | [>3.5.0][zk-reconfig] | [Ja][consul-reconfig] | Ja |
| Maximal zuverlässig nutzbare Datenbankgröße | Mehrere Gigabyte | Hunderte Megabyte (manchmal mehrere Gigabyte) | Hunderte MB | Terabyte und mehr |
| Minimale Latenz zur Linearisierung von Lesezugriffen | Netzwerk-RTT | Keine Linearisierung von Lesezugriffen | RTT + fsync | Uhrzeitbarrieren (Atomuhr, NTP) |

### ZooKeeper {#zookeeper}

ZooKeeper löst dasselbe Problem wie etcd: die Koordination verteilter Systeme und die Speicherung von Metadaten. etcd kann jedoch auf Entwicklungs- und Betriebserfahrungen mit dem Entwurf und der Implementierung von ZooKeeper zurückgreifen. Diese Erfahrungen haben den Entwurf von etcd geprägt und dabei geholfen, große Systeme wie Kubernetes zu unterstützen. Zu den Verbesserungen von etcd gegenüber ZooKeeper gehören:

* Dynamische Neukonfiguration der Clustermitgliedschaft
* Stabile Lese- und Schreibzugriffe unter hoher Last
* Ein Datenmodell mit Mehrversions-Nebenläufigkeitskontrolle
* Zuverlässige Schlüsselüberwachung, die niemals unbemerkt Ereignisse verwirft
* Lease-Grundoperationen, die Verbindungen von Sitzungen entkoppeln
* APIs für sichere verteilte gemeinsame Sperren

Darüber hinaus unterstützt etcd unmittelbar zahlreiche Sprachen und Frameworks. ZooKeeper verwendet sein eigenes, ausschließlich dort eingesetztes Jute-RPC-Protokoll, das die [unterstützten Sprachanbindungen][zk-bindings] begrenzt. Das Client-Protokoll von etcd basiert dagegen auf [gRPC][grpc], einem verbreiteten RPC-Framework mit Anbindungen für Go, C++, Java und weitere Sprachen. gRPC lässt sich außerdem als JSON über HTTP serialisieren, sodass auch allgemeine Befehlszeilenwerkzeuge wie `curl` damit kommunizieren können. Dank dieser Auswahl lassen sich Systeme mit ihren nativen Werkzeugen auf etcd aufbauen, statt sie mit einem einzigen festen Technologiesatz um etcd herum zu entwickeln.

Unter Berücksichtigung von Funktionen, Unterstützung und Stabilität sind neue Anwendungen, die ZooKeeper als konsistenten Schlüssel-Wert-Speicher einsetzen wollen, gut beraten, stattdessen etcd zu wählen.

### Consul {#consul}

Consul ist ein umfassendes Framework zur Diensterkennung. Es bietet integrierte Health Checks, Ausfallerkennung und DNS-Dienste. Außerdem stellt Consul einen Schlüssel-Wert-Speicher mit RESTful-HTTP-APIs bereit. [Beim Stand von Consul 1.0][dbtester-comparison-results] skaliert dieser Speicher bei Schlüssel-Wert-Operationen weniger gut als Systeme wie etcd oder ZooKeeper. Systeme mit Millionen Schlüsseln leiden unter hohen Latenzen und Speicherdruck. Der Schlüssel-Wert-API fehlen insbesondere Mehrversionsschlüssel, bedingte Transaktionen und zuverlässige Streaming-Watches.

etcd und Consul lösen unterschiedliche Probleme. Für einen verteilten konsistenten Schlüssel-Wert-Speicher ist etcd die bessere Wahl. Für eine umfassende Diensterkennung im Cluster reichen die Funktionen von etcd nicht aus; dafür eignen sich Kubernetes, Consul oder SmartStack.

### NewSQL (Cloud Spanner, CockroachDB, TiDB) {#newsql-cloud-spanner-cockroachdb-tidb}

Sowohl etcd als auch NewSQL-Datenbanken wie [Cockroach][cockroach], [TiDB][tidb] und [Google Spanner][spanner] bieten starke Datenkonsistenzgarantien und Hochverfügbarkeit. Die deutlich unterschiedlichen Systementwurfsparameter führen jedoch zu deutlich unterschiedlichen Client-APIs und Leistungseigenschaften.

NewSQL-Datenbanken sind für horizontale Skalierung über Rechenzentren hinweg ausgelegt. Sie verteilen Daten üblicherweise auf mehrere konsistente Replikationsgruppen, sogenannte Shards, die weit auseinanderliegen können, und speichern Datenmengen im Terabyte-Bereich und darüber. Für verteilte Koordination eignet sich diese Skalierung schlecht: Das Warten auf Uhren verursacht hohe Latenzen, und Aktualisierungen werden mit weitgehend lokalen Abhängigkeitsgraphen erwartet. Die Daten sind in Tabellen organisiert und lassen sich mit SQL-artigen Abfragen mit umfangreicherer Semantik als bei etcd abfragen. Dafür steigt jedoch die Komplexität der Verarbeitung sowie der Planung und Optimierung von Abfragen.

Für Metadatenspeicherung oder die Koordination verteilter Anwendungen eignet sich etcd. Sollen mehr als einige GB Daten gespeichert werden oder sind vollständige SQL-Abfragen erforderlich, eignet sich eine NewSQL-Datenbank.

## etcd für Metadaten verwenden {#using-etcd-for-metadata}

etcd repliziert alle Daten innerhalb einer einzigen konsistenten Replikationsgruppe. Für bis zu einige GB Daten mit konsistenter Reihenfolge ist dies der effizienteste Ansatz. Jede Änderung des Clusterzustands, die mehrere Schlüssel betreffen kann, erhält aus einem monoton steigenden Zähler eine global eindeutige ID, in etcd Revision genannt. Anhand dieser ID lässt sich die Reihenfolge bestimmen. Da es nur eine Replikationsgruppe gibt, muss die Änderungsanfrage zur Bestätigung nur das Raft-Protokoll durchlaufen. Durch die Begrenzung des Konsenses auf eine Replikationsgruppe erreicht etcd verteilte Konsistenz mit einem einfachen Protokoll bei geringer Latenz und hohem Durchsatz.

Die Replikation von etcd lässt sich mangels Daten-Sharding nicht horizontal skalieren. NewSQL-Datenbanken verteilen Daten dagegen üblicherweise auf mehrere konsistente Replikationsgruppen und speichern Datenmengen im Terabyte-Bereich und darüber. Um jeder Änderung eine global eindeutige, steigende ID zuzuweisen, muss jede Anfrage jedoch ein zusätzliches Koordinationsprotokoll zwischen den Replikationsgruppen durchlaufen. Dieser zusätzliche Schritt kann Konflikte um die globale ID verursachen und geordnete Anfragen zur Wiederholung zwingen. Das Ergebnis ist ein komplexerer Ansatz mit üblicherweise schlechterer Leistung als etcd bei strikter Reihenfolge.

Wenn eine Anwendung vor allem Metadaten oder deren Reihenfolge verarbeitet, etwa zur Prozesskoordination, eignet sich etcd. Benötigt sie einen großen Datenspeicher über mehrere Rechenzentren hinweg und ist nicht stark auf eine strikte globale Reihenfolge angewiesen, eignet sich eine NewSQL-Datenbank.

## etcd für verteilte Koordination verwenden {#using-etcd-for-distributed-coordination}

etcd bietet direkt Grundoperationen für verteilte Koordination, darunter Ereignis-Watches, Leases, Wahlen und verteilte gemeinsame Sperren. Bei letzteren müssen Benutzer allerdings nicht offensichtliche Eigenschaften beachten, die unten erläutert werden. Diese Grundoperationen werden von den etcd-Entwicklern gepflegt und unterstützt. Sie externen Bibliotheken zu überlassen, würde die Verantwortung für die Entwicklung grundlegender verteilter Software abgeben und das System im Wesentlichen unvollständig lassen. NewSQL-Datenbanken erwarten üblicherweise, dass Drittanbieter solche Grundoperationen entwickeln. Ebenso verfügt ZooKeeper bekanntlich über eine separate, unabhängige [Bibliothek][curator] mit Koordinationsrezepten. Consul bietet eine native Sperr-API, weist aber sogar entschuldigend darauf hin, dass sie „[keine absolut sichere Methode][consul-bulletproof]“ sei.

Theoretisch lassen sich diese Grundoperationen auf jedem Speichersystem mit starker Konsistenz aufbauen. Die Algorithmen sind jedoch oft subtil: Schnell entsteht ein scheinbar funktionierender Sperralgorithmus, der plötzlich an gleichzeitig aufwachenden Wartenden, dem Thundering-Herd-Problem, oder Zeitabweichungen scheitert. Außerdem hängen weitere von etcd unterstützte Grundoperationen wie transaktionaler Speicher vom MVCC-Datenmodell ab; starke Konsistenz allein reicht nicht aus.

Für verteilte Koordination kann die Wahl von etcd Betriebsprobleme vermeiden helfen und Entwicklungsaufwand sparen.

### Hinweise zur Verwendung von Sperren und Leases {#notes-on-the-usage-of-lock-and-lease}
etcd bietet [Sperr-APIs][etcd-v3lock], die auf [dem Lease-Mechanismus][lease] und [dessen Implementierung in etcd][etcdlease] basieren. Die Grundidee: Ein Server gewährt einem anfragenden Client ein Token namens Lease und ordnet ihm eine TTL zu. Stellt der Server fest, dass mehr Zeit als die TTL vergangen ist, widerruft er die Lease. Solange der Client eine nicht widerrufene Lease hält, kann er beanspruchen, den Zugriff auf eine zugeordnete Ressource zu besitzen. Bei etcd ist diese Ressource ein Schlüssel im Schlüsselraum. Auf diesem Prinzip beruhen die Sperr-APIs von etcd. Für sich allein gewährleisten sie jedoch keinen gegenseitigen Ausschluss. Die Bezeichnung „lock“ hat [historische Gründe][chubby]. Wie unten beschrieben, können die Sperr-APIs den gegenseitigen Ausschluss jedoch optimieren.

Der wichtigste Aspekt des Lease-Mechanismus ist, dass die TTL als physisches Zeitintervall definiert ist. Server und Client messen den Zeitablauf jeweils mit ihrer eigenen Uhr. Daher kann der Server die Lease bereits widerrufen haben, während der Client weiterhin behauptet, sie zu besitzen.

Wie gewährleistet der Lease-Mechanismus dann den gegenseitigen Ausschluss der Sperren? Tatsächlich gewährleistet er selbst keinen gegenseitigen Ausschluss. Der Besitz einer Lease garantiert nicht, dass ihr Besitzer eine Sperre auf der Ressource hält.

Wenn etcd-Sperren den gegenseitigen Zugriff auf Schlüssel von etcd selbst steuern, wird der gegenseitige Ausschluss durch die Validierung von Versionsnummern implementiert. In anderen Systemen wie Consul wird dies manchmal Compare and Swap genannt. In etcd-RPCs wie `Put` oder `Txn` lassen sich erforderliche Bedingungen für Revisionsnummer und Lease-ID der Operationen angeben. Sind diese nicht erfüllt, kann die Operation fehlschlagen. Mit diesem Mechanismus stellt etcd verteilte Sperren für Clients bereit. Ein Client weiß also, dass er die Sperre eines Schlüssels erwirbt, wenn der etcd-Cluster seine Anfragen erfolgreich abschließt.

Die Literatur zu verteilten Sperren beschreibt ähnliche Entwürfe:
* Die [Veröffentlichung zu Chubby][chubby] führt den Begriff *Sequencer* ein. Nach unserem Verständnis entspricht er nahezu der Kombination aus Revisionsnummer und Lease-ID in etcd.
* In [Verteilte Sperren implementieren][fencing] stellt Martin Kleppmann das Konzept des *Fencing-Tokens* vor. Nach Auffassung der Autoren entspricht dieses Token bei etcd der Revisionsnummer.
* [Praktische Anwendungen synchronisierter Uhren in verteilten Systemen][physicalclock] beschreibt, wie Thor verteilte Sperren auf Grundlage von Versionsnummernvalidierung und Leases implementiert.

Warum bieten etcd und andere Systeme Leases, wenn sie gegenseitigen Ausschluss durch Versionsnummernvalidierung gewährleisten? Leases dienen als Optimierung, um die Anzahl abgebrochener Anfragen zu verringern.

Schlüssel in etcd lassen sich dank Leases und Versionsnummernvalidierung effizient sperren. Müssen Benutzer Ressourcen außerhalb von etcd schützen, müssen diese wie etcd-Schlüssel eine Versionsnummernvalidierung und konsistente Replikate bereitstellen. Die Sperrfunktion von etcd allein kann externe Ressourcen nicht schützen.

[chubby]: https://research.google/pubs/pub27897/
[cockroach]: https://github.com/cockroachdb/cockroach
[cockroach-grant]: https://www.cockroachlabs.com/docs/stable/grant.html
[consul-acl]: https://www.consul.io/docs/security/acl
[consul-bulletproof]: https://www.consul.io/docs/dynamic-app-config/sessions
[consul-json]: https://www.consul.io/api-docs#formatted-json-output
[consul-linread]: https://www.consul.io/api-docs#consistency
[consul-lock]: https://www.consul.io/commands/lock
[consul-reconfig]: https://developer.hashicorp.com/consul/tutorials/datacenter-operations/add-remove-servers
[consul-txn]: https://www.consul.io/api/kv#txn
[consul-watch]: https://www.consul.io/docs/dynamic-app-config/watches
[container-linux]: https://coreos.com/why
[curator]: http://curator.apache.org/
[dbtester-comparison-results]: https://github.com/coreos/dbtester/tree/master/test-results/2018Q1-02-etcd-zookeeper-consul
[etcd-commonname]: /de/docs/etcd/op-guide/authentication/#using-tls-common-name
[etcd-etcdctl-elect]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#elect-options-election-name-proposal
[etcd-etcdctl-lock]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#lock-options-lockname-command-arg1-arg2-
[etcd-json]: /de/docs/etcd/dev-guide/api_grpc_gateway/
[etcd-linread]: /de/docs/etcd/learning/api_guarantees/#linearizability
[etcd-mvcc]: /de/docs/etcd/learning/data_model/
[etcd-rbac]: /de/docs/etcd/op-guide/authentication/rbac
[etcd-recipe]: https://godoc.org/github.com/etcd-io/etcd/client/v3/experimental/recipes
[etcd-reconfig]: /de/docs/etcd/op-guide/runtime-configuration
[etcd-txn]: /de/docs/etcd/learning/api/#transaction
[etcd-v3election]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3election/v3electionpb
[etcd-v3lock]: https://pkg.go.dev/go.etcd.io/etcd/server/v3/etcdserver/api/v3lock/v3lockpb
[etcd-watch]: /de/docs/etcd/learning/api/#watch-streams
[etcdlease]: https://godoc.org/github.com/etcd-io/etcd/client/v3/leasing
[fencing]: https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
[grpc]: https://www.grpc.io
[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[locksmith]: https://github.com/coreos/locksmith
[newsql-leader]: http://dl.acm.org/citation.cfm?id=2960999
[physicalclock]: https://web.archive.org/web/20190725151657/http://www.dainf.cefetpr.br/~tacla/SDII/PracticalUseOfClocks.pdf
[production-users]: https://github.com/etcd-io/etcd/blob/main/ADOPTERS.md
[spanner]: https://cloud.google.com/spanner/
[spanner-roles]: https://cloud.google.com/spanner/docs/iam#roles
[tidb]: https://github.com/pingcap/tidb
[zk-acl]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#sc_ZooKeeperAccessControl
[zk-bindings]: https://zookeeper.apache.org/doc/r3.1.2/zookeeperProgrammers.html#ch_bindings
[zk-reconfig]: https://zookeeper.apache.org/doc/current/zookeeperReconfig.html
[zk-txn]: https://zookeeper.apache.org/doc/r3.4.3/api/org/apache/zookeeper/ZooKeeper.html#multi(java.lang.Iterable)
[zk-watch]: https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html#ch_zkWatches
