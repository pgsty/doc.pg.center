---
title: "FAQ"
weight: 1200
description: "Häufig gestellte Fragen"
icon: fa-solid fa-circle-question
categories: [Referenz]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/faq.md"
---

## Allgemeines zu etcd {#etcd-general}

### Was ist etcd? {#what-is-etcd}

etcd ist ein konsistenter, verteilter Schlüssel-Wert-Speicher. Es wird hauptsächlich als separater Koordinationsdienst in verteilten Systemen verwendet und ist für kleine Datenmengen ausgelegt, die vollständig in den Arbeitsspeicher passen.

### Wie wird etcd ausgesprochen? {#how-do-you-pronounce-etcd}

etcd wird **/ˈɛtsiːdiː/** ausgesprochen und bedeutet „verteiltes `etc`-Verzeichnis“.

### Müssen Clients Anfragen an den etcd-Leader senden? {#do-clients-have-to-send-requests-to-the-etcd-leader}

[Raft][raft] arbeitet mit einem Leader; dieser bearbeitet alle Clientanfragen, die einen Konsens im Cluster erfordern. Der Client muss jedoch nicht wissen, welcher Knoten der Leader ist. Jede an einen Follower gesendete Anfrage, die Konsens benötigt, wird automatisch an den Leader weitergeleitet. Anfragen ohne Konsensanforderung (etwa serialisierbare Lesezugriffe) kann jedes Clustermitglied verarbeiten.

## Konfiguration {#configuration}

### Worin unterscheiden sich listen-<client,peer>-urls, advertise-client-urls und initial-advertise-peer-urls? {#what-is-the-difference-between-listen-clientpeer-urls-advertise-client-urls-or-initial-advertise-peer-urls}

`listen-client-urls` und `listen-peer-urls` legen die lokalen Adressen fest, an die sich der etcd-Server bindet, um eingehende Verbindungen anzunehmen. Um einen Port auf allen Schnittstellen zu überwachen, `0.0.0.0` als IP-Adresse zum Lauschen angeben.

`advertise-client-urls` und `initial-advertise-peer-urls` legen die Adressen fest, über die etcd-Clients oder andere etcd-Mitglieder den etcd-Server erreichen sollten. Die bekannt gegebenen Adressen müssen von den entfernten Rechnern erreichbar sein. In einer Produktionsumgebung keine Adressen wie `localhost` oder `0.0.0.0` bekannt geben, da diese von entfernten Rechnern nicht erreichbar sind.

### Warum aktualisiert eine Änderung von `--listen-peer-urls` oder `--initial-advertise-peer-urls` nicht die in `etcdctl member list` bekannt gegebenen Peer-URLs? {#why-doesnt-changing---listen-peer-urls-or---initial-advertise-peer-urls-update-the-advertised-peer-urls-in-etcdctl-member-list}

Die bekannt gegebenen Peer-URLs eines Mitglieds stammen beim ersten Clusterstart aus `--initial-advertise-peer-urls`. Werden nach dem Start des Mitglieds die Adressen zum Lauschen für Peers oder die anfänglich bekannt gegebenen Peer-Adressen geändert, beeinflusst dies die veröffentlichten Peer-URLs nicht. Änderungen müssen vom Quorum bestätigt werden, um einen Split-Brain-Zustand der Mitgliedschaftskonfiguration zu vermeiden. Mit `etcdctl member update` lassen sich die Peer-URLs eines Mitglieds aktualisieren.

## Bereitstellung {#deployment}

### Systemanforderungen {#system-requirements}

Da etcd Daten auf den Datenträger schreibt, hängt seine Leistung stark von dessen Leistung ab. Daher wird eine SSD dringend empfohlen. Um zu prüfen, ob ein Datenträger für etcd schnell genug ist, kann ein Benchmarkwerkzeug wie [fio][fio] verwendet werden. Ein Beispiel dazu gibt es [hier][fio-blog-post]. Um Leistungseinbußen oder eine unbeabsichtigte Überlastung des Schlüssel-Wert-Speichers zu verhindern, setzt etcd eine konfigurierbare Speicherplatzquote durch, die standardmäßig 2GB beträgt. Um Auslagerung oder Speichermangel zu vermeiden, sollte der Rechner mindestens so viel RAM haben, wie die Quote vorsieht. Für normale Umgebungen wird eine maximale Größe von 8GB empfohlen; überschreitet der konfigurierte Wert diese Grenze, warnt etcd beim Start. Bei CoreOS wird ein etcd-Cluster üblicherweise auf dedizierten Rechnern mit CoreOS Container Linux betrieben, die *mindestens* einen Zweikernprozessor, 2GB RAM und 80GB SSD-Speicher besitzen. **Die Leistung hängt wesentlich von der Arbeitslast ab; vor dem Produktiveinsatz bitte testen**. Weitere Empfehlungen stehen unter [Hardware][hardware-setup].

Die stabilste Produktionsumgebung ist Linux auf der amd64-Architektur; weitere Informationen unter [Unterstützte Plattformen][supported-platform].

### Warum eine ungerade Anzahl von Clustermitgliedern? {#why-an-odd-number-of-cluster-members}

In einem etcd-Cluster muss die Mehrheit der Knoten, das Quorum, Änderungen am Clusterzustand zustimmen. Bei einem Cluster mit n Mitgliedern beträgt das Quorum (n/2)+1. Bei einem Cluster mit ungerader Mitgliederzahl erhöht das Hinzufügen eines Knotens immer die für das Quorum erforderliche Knotenzahl. Obwohl ein zusätzlicher Knoten wegen der höheren Rechnerzahl vorteilhaft erscheint, verschlechtert sich die Fehlertoleranz: Ohne Quorumverlust dürfen weiterhin genauso viele Knoten ausfallen, doch es gibt mehr Knoten, die ausfallen können. Kann der Cluster keine weiteren Ausfälle mehr verkraften, ist das Hinzufügen eines Knotens vor dem Entfernen von Knoten gefährlich. Kann sich der neue Knoten nicht beim Cluster registrieren (etwa wegen einer falsch konfigurierten Adresse), geht das Quorum dauerhaft verloren.

### Wie groß darf ein Cluster maximal sein? {#what-is-maximum-cluster-size}

Theoretisch gibt es keine feste Grenze. Ein etcd-Cluster sollte jedoch wahrscheinlich nicht mehr als sieben Knoten haben. Der [Google-Chubby-Sperrdienst][chubby], der etcd ähnelt und bei Google seit vielen Jahren weit verbreitet ist, empfiehlt fünf Knoten. Ein etcd-Cluster mit 5 Mitgliedern kann den Ausfall von zwei Mitgliedern verkraften, was in den meisten Fällen ausreicht. Größere Cluster bieten zwar eine bessere Fehlertoleranz, ihre Schreibleistung leidet jedoch darunter, dass Daten auf mehr Rechner repliziert werden müssen.

### Was bedeutet Fehlertoleranz? {#what-is-failure-tolerance}

Ein etcd-Cluster arbeitet, solange ein Quorum seiner Mitglieder hergestellt werden kann. Geht das Quorum durch vorübergehende Netzwerkfehler (etwa Partitionierungen) verloren, setzt etcd den Betrieb automatisch und sicher fort, sobald das Netzwerk wieder funktioniert und das Quorum wiederhergestellt ist; Raft gewährleistet die Clusterkonsistenz. Für den Fall eines Stromausfalls speichert etcd das Raft-Protokoll dauerhaft auf dem Datenträger. Es spielt das Protokoll bis zum Zeitpunkt des Ausfalls erneut ab und nimmt wieder am Cluster teil. Bei einem dauerhaften Hardwareausfall kann der Knoten durch [Rekonfiguration im laufenden Betrieb][runtime reconfiguration] aus dem Cluster entfernt werden.

Eine ungerade Mitgliederzahl wird empfohlen. Ein Cluster mit ungerader Mitgliederzahl verkraftet dieselbe Zahl von Ausfällen wie ein Cluster mit gerader Mitgliederzahl, benötigt dafür aber weniger Knoten. Der Vergleich zeigt den Unterschied:

| Clustergröße | Mehrheit | Fehlertoleranz |
|:-:|:-:|:-:|
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 2 | 1 |
| 4 | 3 | 1 |
| 5 | 3 | 2 |
| 6 | 4 | 2 |
| 7 | 4 | 3 |
| 8 | 5 | 3 |
| 9 | 5 | 4 |

Ein Mitglied hinzuzufügen, um eine gerade Clustergröße zu erreichen, bringt keine zusätzliche Fehlertoleranz. Ebenso gewährleistet eine ungerade Mitgliederzahl bei einer Aufteilung des Netzwerks in zwei Partitionen, dass stets eine Mehrheitspartition vorhanden ist, die weiterarbeiten und nach dem Ende der Partitionierung als maßgebliche Datenquelle dienen kann.

### Funktioniert etcd bei Bereitstellungen über Regionen oder Rechenzentren hinweg? {#does-etcd-work-in-cross-region-or-cross-data-center-deployments}

Eine Bereitstellung über mehrere Regionen verbessert die Fehlertoleranz von etcd, da die Mitglieder in getrennten Ausfallbereichen liegen. Der Preis ist eine höhere Latenz für Konsensanfragen über Rechenzentrumsgrenzen hinweg. Da etcd für den Konsens ein Quorum seiner Mitglieder benötigt, fällt diese zusätzliche Latenz ins Gewicht: Mindestens die Mehrheit der Clustermitglieder muss auf Konsensanfragen antworten. Außerdem müssen Clusterdaten auf alle Peers repliziert werden, wodurch auch Bandbreitenkosten entstehen.

Bei längeren Latenzen kann die Standardkonfiguration von etcd häufige Wahlen oder Heartbeat-Zeitüberschreitungen verursachen. Hinweise zum Anpassen der Zeitüberschreitungen für Bereitstellungen mit hoher Latenz enthält der Abschnitt [Optimierung][tuning].

## Betrieb {#operation}

### Wie wird ein Backup eines etcd-Clusters erstellt? {#how-to-backup-a-etcd-cluster}

etcdctl stellt den Befehl `snapshot` zum Erstellen von Backups bereit. Weitere Einzelheiten unter [Backup][backup].

### Sollte vor dem Entfernen eines nicht funktionsfähigen Mitglieds ein neues hinzugefügt werden? {#should-i-add-a-member-before-removing-an-unhealthy-member}

Beim Ersetzen eines etcd-Knotens ist es wichtig, zuerst das Mitglied zu entfernen und dann seinen Ersatz hinzuzufügen.

etcd verwendet verteilten Konsens auf Basis eines Quorummodells: (n/2)+1 Mitglieder, also die Mehrheit, müssen einem Vorschlag zustimmen, bevor er im Cluster festgeschrieben werden kann. Solche Vorschläge umfassen Schlüssel-Wert-Aktualisierungen und Änderungen der Mitgliedschaft. Dieses Modell schließt Inkonsistenzen durch Split Brain vollständig aus. Der Nachteil ist, dass ein dauerhafter Quorumverlust katastrophal ist.

Für die Mitgliedschaft bedeutet dies: Ist in einem Cluster mit 3 Mitgliedern 1 Mitglied ausgefallen, kann der Cluster weiterhin Fortschritte machen, denn das Quorum beträgt 2 und 2 Mitglieder sind noch aktiv. Wird dem Cluster mit 3 Mitgliedern jedoch ein neues Mitglied hinzugefügt, steigt das Quorum auf 3, da für die Mehrheit von 4 Mitgliedern 3 Stimmen erforderlich sind. Wegen des gestiegenen Quorums bringt das zusätzliche Mitglied keinen Gewinn an Fehlertoleranz; der Ausfall eines weiteren Knotens würde den Cluster weiterhin unwiederherstellbar machen.

Außerdem birgt das neue Mitglied ein Risiko: Es könnte falsch konfiguriert sein oder dem Cluster nicht beitreten können. Dann lässt sich das Quorum nicht wiederherstellen. Der Cluster hat zwei ausgefallene und zwei aktive Mitglieder, benötigt aber drei Stimmen für eine Änderung der Mitgliedschaft, um das misslungene Hinzufügen rückgängig zu machen. etcd lehnt standardmäßig Versuche ab, Mitglieder hinzuzufügen, wenn sie den Cluster auf diese Weise zum Ausfall bringen könnten.

Wird dagegen zuerst das ausgefallene Mitglied aus der Clustermitgliedschaft entfernt, sinkt die Mitgliederzahl auf 2 und das Quorum bleibt bei 2. Auch das anschließende Hinzufügen eines neuen Mitglieds hält das Quorum bei 2. Selbst wenn sich der neue Knoten nicht starten lässt, können die verbleibenden aktiven Mitglieder das neue Mitglied daher weiterhin durch ein Quorum entfernen.

### Warum akzeptiert etcd meine Änderungen der Mitgliedschaft nicht? {#why-wont-etcd-accept-my-membership-changes}

etcd setzt `strict-reconfig-check`, um Rekonfigurationsanfragen abzulehnen, die zum Quorumverlust führen würden. Auf das Quorum zu verzichten ist sehr riskant, insbesondere bei einem bereits beeinträchtigten Cluster. Bei Quorumverlust mag es verlockend sein, die Quorumprüfung zu deaktivieren, um ein neues Mitglied hinzuzufügen. Dies könnte jedoch den gesamten Cluster inkonsistent machen. Für viele Anwendungen würde das Problem dadurch noch schlimmer; eine Beschädigung der Datenträgergeometrie gehört zu den erschreckendsten möglichen Folgen.

### Warum verliert etcd bei Spitzen der Datenträgerlatenz seinen Leader? {#why-does-etcd-lose-its-leader-from-disk-latency-spikes}

Dieses Verhalten ist beabsichtigt: Die Datenträgerlatenz gehört zur Beurteilung der Funktionsfähigkeit des Leaders. Angenommen, der Cluster-Leader benötigt eine Minute, um eine Aktualisierung des Raft-Logs per fsync auf den Datenträger zu schreiben, während die Wahlzeitüberschreitung des etcd-Clusters eine Sekunde beträgt. Auch wenn der Leader Netzwerknachrichten innerhalb des Wahlintervalls verarbeiten kann, etwa Heartbeats senden, ist er praktisch nicht verfügbar: Er kann keine neuen Vorschläge festschreiben, weil er auf den langsamen Datenträger wartet. Verliert der Cluster wegen Datenträgerlatenzen häufig seinen Leader, versuchen, die Datenträgereinstellungen oder die Zeitparameter von etcd zu [optimieren][tuning].

### Was bedeutet die etcd-Warnung "request ignored (cluster ID mismatch)"? {#what-does-the-etcd-warning-request-ignored-cluster-id-mismatch-mean}

Jeder neue etcd-Cluster erzeugt aus der anfänglichen Clusterkonfiguration und einem vom Benutzer angegebenen eindeutigen Wert für `initial-cluster-token` eine neue Cluster-ID. Eindeutige Cluster-IDs schützen etcd vor Wechselwirkungen zwischen Clustern, die den Cluster beschädigen könnten.

Diese Warnung tritt üblicherweise auf, nachdem ein alter Cluster abgebaut wurde und einige seiner Peer-Adressen für einen neuen Cluster wiederverwendet werden. Läuft noch ein etcd-Prozess des alten Clusters, versucht er, den neuen Cluster zu kontaktieren. Dieser erkennt die abweichende Cluster-ID, ignoriert die Anfrage und gibt die Warnung aus. Häufig lässt sich die Warnung beseitigen, indem sichergestellt wird, dass verschiedene Cluster keine gemeinsamen Peer-Adressen haben.

### Was bedeutet "mvcc: database space exceeded" und wie lässt sich das beheben? {#what-does-mvcc-database-space-exceeded-mean-and-how-do-i-fix-it}

Das Datenmodell von etcd mit [Mehrversionen-Nebenläufigkeitskontrolle][api-mvcc] bewahrt einen exakten Verlauf des Schlüsselraums. Ohne regelmäßige Kompaktierung dieses Verlaufs, etwa durch Setzen von `--auto-compaction-mode` und `--auto-compaction-retention`, wird etcd seinen Speicherplatz irgendwann aufbrauchen. Bei knappem Speicherplatz löst etcd einen Speicherplatzquotenalarm aus, um den Cluster vor weiteren Schreibzugriffen zu schützen. Solange der Alarm aktiv ist, beantwortet etcd Schreibanfragen mit dem Fehler `mvcc: database space exceeded`.

So lässt sich der Speicherplatzquotenalarm beheben:

1. Den Verlauf von etcd [kompaktieren][maintenance-compact].
2. Jeden etcd-Endpunkt [defragmentieren][maintenance-defragment].
3. Den Alarm [deaktivieren][maintenance-disarm].

### Was bedeutet die etcd-Warnung "etcdserver/api/v3rpc: transport: http2Server.HandleStreams failed to read frame: read tcp 127.0.0.1:2379->127.0.0.1:43020: read: connection reset by peer"? {#what-does-the-etcd-warning-etcdserverapiv3rpc-transport-http2serverhandlestreams-failed-to-read-frame-read-tcp-1270012379-12700143020-read-connection-reset-by-peer-mean}

Dies ist eine gRPC-seitige Warnung, wenn ein Server ein TCP-RST-Flag empfängt, weil clientseitige Streams vorzeitig geschlossen wurden. Ein Client schließt beispielsweise seine Verbindung, bevor der gRPC-Server alle HTTP/2-Frames in der TCP-Warteschlange verarbeitet hat. Auf Serverseite können dabei Daten verloren gegangen sein; solange die Clientverbindung bereits geschlossen wurde, ist das jedoch unproblematisch.

Nur [alte gRPC-Versionen](https://github.com/grpc/grpc-go/issues/1362) protokollieren dies. etcd [>=v3.2.13 protokolliert es standardmäßig auf der Stufe DEBUG](https://github.com/etcd-io/etcd/pull/9080), sodass es nur mit aktivierter Option `--log-level=debug` sichtbar ist.

## Leistung {#performance}

### Wie sollte etcd einem Benchmark unterzogen werden? {#how-should-i-benchmark-etcd}

Das Werkzeug [benchmark] ausprobieren. Aktuelle [Benchmark-Ergebnisse][benchmark-result] stehen zum Vergleich bereit.

### Was bedeutet die etcd-Warnung "apply entries took too long"? {#what-does-the-etcd-warning-apply-entries-took-too-long-mean}

Nachdem die Mehrheit der etcd-Mitglieder dem Festschreiben einer Anfrage zugestimmt hat, wendet jeder etcd-Server die Anfrage auf seinen Datenspeicher an und speichert das Ergebnis dauerhaft auf dem Datenträger. Selbst mit einem langsamen mechanischen Datenträger oder einem virtualisierten Netzwerkdatenträger wie Amazons EBS oder Googles PD sollte das Anwenden einer Anfrage normalerweise weniger als 50 Millisekunden dauern. Übersteigt die durchschnittliche Anwendungsdauer 100 Millisekunden, warnt etcd, dass das Anwenden der Einträge zu lange dauert.

Meist wird dieses Problem durch einen langsamen Datenträger verursacht. Möglicherweise konkurrieren etcd und andere Anwendungen um Datenträgerzugriffe, oder der Datenträger ist schlicht zu langsam, etwa ein gemeinsam genutzter virtualisierter Datenträger. Um einen langsamen Datenträger als Ursache auszuschließen, [backend_commit_duration_seconds][backend_commit_metrics] überwachen (die p99-Dauer sollte unter 25ms liegen) und so prüfen, ob der Datenträger ausreichend schnell ist. Ist er zu langsam, lässt sich das Problem in der Regel durch einen dedizierten oder schnelleren Datenträger für etcd lösen.

Die zweithäufigste Ursache ist ein Mangel an CPU-Zeit. Zeigt die Überwachung der CPU-Nutzung des Rechners eine hohe Auslastung, reicht die Rechenkapazität für etcd möglicherweise nicht aus. In der Regel hilft es, etcd auf einen dedizierten Rechner zu verlagern, die Ressourcenisolierung der Prozesse mit cgroups zu verstärken oder dem etcd-Serverprozess mit renice eine höhere Priorität zu geben.

Aufwendige Benutzeranfragen, die auf zu viele Schlüssel zugreifen, etwa das Abrufen des gesamten Schlüsselraums, können ebenfalls lange Anwendungslatenzen verursachen. Zugriffe auf weniger als einige Hundert Schlüssel pro Anfrage sollten jedoch immer schnell sein.

Beseitigt keiner dieser Vorschläge die Warnungen, bitte [ein Issue erstellen][new_issue] und ausführliche Protokolle, Überwachungsdaten, Metriken sowie gegebenenfalls Informationen zur Arbeitslast beifügen.

### Was bedeutet die etcd-Warnung "failed to send out heartbeat on time"? {#what-does-the-etcd-warning-failed-to-send-out-heartbeat-on-time-mean}

etcd verwendet ein auf einem Leader basierendes Konsensprotokoll für konsistente Datenreplikation und Log-Ausführung. Die Clustermitglieder wählen einen einzigen Leader; alle anderen Mitglieder werden Follower. Der gewählte Leader muss regelmäßig Heartbeats an seine Follower senden, um seine Rolle beizubehalten. Erhalten Follower innerhalb eines Wahlintervalls keine Heartbeats, nehmen sie einen Leader-Ausfall an und lösen eine Wahl aus. Sendet ein noch laufender Leader seine Heartbeats nicht rechtzeitig, ist die Wahl unnötig und wird wahrscheinlich durch unzureichende Ressourcen ausgelöst. Um solche Funktionsstörungen zu erkennen, warnt etcd, wenn der Leader zwei Heartbeat-Intervalle auslässt, dass ein Heartbeat nicht rechtzeitig gesendet wurde.

Meist wird dieses Problem durch einen langsamen Datenträger verursacht. Bevor der Leader Heartbeats mit angehängten Metadaten sendet, muss er die Metadaten möglicherweise dauerhaft auf dem Datenträger speichern. Möglicherweise konkurrieren etcd und andere Anwendungen um Datenträgerzugriffe, oder der Datenträger ist schlicht zu langsam, etwa ein gemeinsam genutzter virtualisierter Datenträger. Um einen langsamen Datenträger als Ursache auszuschließen, [wal_fsync_duration_seconds][wal_fsync_duration_seconds] überwachen (die p99-Dauer sollte unter 10ms liegen) und so prüfen, ob der Datenträger ausreichend schnell ist. Ist er zu langsam, lässt sich das Problem in der Regel durch einen dedizierten oder schnelleren Datenträger für etcd lösen. Ob ein Datenträger schnell genug für etcd ist, lässt sich mit einem Benchmarkwerkzeug wie [fio][fio] prüfen. Ein Beispiel steht [hier][fio-blog-post].

Die zweithäufigste Ursache ist ein Mangel an CPU-Zeit. Zeigt die Überwachung der CPU-Nutzung des Rechners eine hohe Auslastung, reicht die Rechenkapazität für etcd möglicherweise nicht aus. In der Regel hilft es, etcd auf einen dedizierten Rechner zu verlagern, die Ressourcenisolierung der Prozesse mit cgroups zu verstärken oder dem etcd-Serverprozess mit renice eine höhere Priorität zu geben.

Auch ein langsames Netzwerk kann dieses Problem verursachen. Zeigen die Netzwerkmetriken zwischen den etcd-Rechnern lange Latenzen oder eine hohe Verlustrate, reicht die Netzwerkkapazität für etcd möglicherweise nicht aus. In der Regel hilft es, die etcd-Mitglieder in ein weniger ausgelastetes Netzwerk zu verlagern. Bei einem über mehrere Rechenzentren verteilten etcd-Cluster sind lange Latenzen zwischen den Mitgliedern jedoch zu erwarten. Für solche Bereitstellungen `heartbeat-interval` ungefähr auf die Umlaufzeit zwischen den Rechnern einstellen und `election-timeout` auf mindestens 5 * `heartbeat-interval` setzen. Einzelheiten enthält die [Dokumentation zur Optimierung][tuning].

Beseitigt keiner dieser Vorschläge die Warnungen, bitte [ein Issue erstellen][new_issue] und ausführliche Protokolle, Überwachungsdaten, Metriken sowie gegebenenfalls Informationen zur Arbeitslast beifügen.

### Was bedeutet die etcd-Warnung "snapshotting is taking more than x seconds to finish ..."? {#what-does-the-etcd-warning-snapshotting-is-taking-more-than-x-seconds-to-finish--mean}

etcd sendet einen Snapshot seines vollständigen Schlüssel-Wert-Speichers, um langsame Follower auf den aktuellen Stand zu bringen und [Backups][backup] zu erstellen. Langsame Snapshot-Übertragungen erhöhen die MTTR. Nimmt der Cluster Daten mit hohem Durchsatz auf, können langsame Follower in einen Livelock geraten: Sie benötigen bereits einen neuen Snapshot, bevor sie den vorherigen vollständig empfangen haben. Um langsame Snapshot-Übertragungen zu erkennen, warnt etcd, wenn das Senden eines Snapshots länger als dreißig Sekunden dauert und die für eine 1Gbps-Verbindung erwartete Übertragungszeit überschreitet.


[api-mvcc]: /de/etcd/learning/api/#revisions
[backend_commit_metrics]: /de/etcd/metrics/#disk
[backup]: /de/etcd/op-guide/recovery/#snapshotting-the-keyspace
[benchmark]: https://github.com/etcd-io/etcd/tree/main/tools/benchmark
[benchmark-result]: /de/etcd/op-guide/performance/
[chubby]: http://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf
[fio]: https://github.com/axboe/fio
[fio-blog-post]: https://web.archive.org/web/20240726111518/https://prog.world/is-storage-speed-suitable-for-etcd-ask-fio/
[hardware-setup]: /de/etcd/op-guide/hardware/
[maintenance-compact]:  /de/etcd/op-guide/maintenance/#history-compaction-v3-api-key-value-database
[maintenance-defragment]: /de/etcd/op-guide/maintenance/#defragmentation
[maintenance-disarm]: https://github.com/etcd-io/etcd/blob/main/etcdctl/README.md#alarm-disarm
[new_issue]: https://github.com/etcd-io/etcd/issues/new
[raft]: https://raft.github.io/raft.pdf
[runtime reconfiguration]: /de/etcd/op-guide/runtime-configuration/
[supported-platform]: /de/etcd/op-guide/supported-platform/
[tuning]: /de/etcd/tuning/
[wal_fsync_duration_seconds]: /de/etcd/metrics/#disk
