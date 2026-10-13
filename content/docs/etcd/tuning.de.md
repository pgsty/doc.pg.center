---
title: "Optimierung"
weight: 1450
description: "Wann das Heartbeat-Intervall und die Wahlzeitüberschreitung angepasst werden sollten"
icon: fa-solid fa-sliders
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/tuning.md"
aliases: [/etcd/tuning/]
---

Die Standardeinstellungen von etcd sollten für Installationen in einem lokalen Netzwerk mit geringer durchschnittlicher Netzwerklatenz gut geeignet sein. Beim Einsatz von etcd über mehrere Rechenzentren oder Netzwerke mit hoher Latenz hinweg kann es jedoch nötig sein, das Heartbeat-Intervall und die Wahlzeitüberschreitung anzupassen.

Das Netzwerk ist nicht die einzige Latenzquelle. Langsame Datenträger auf Leader und Follower können jede Anfrage und Antwort beeinträchtigen. Jede dieser Zeitüberschreitungen bezieht sich auf die gesamte Zeit von der Anfrage bis zur erfolgreichen Antwort des anderen Rechners.

## Zeitparameter {#time-parameters}

Das zugrunde liegende verteilte Konsensprotokoll verwendet zwei getrennte Zeitparameter, damit Knoten die Leader-Rolle übergeben können, wenn ein Knoten blockiert oder offline geht. Der erste Parameter heißt *Heartbeat-Intervall*. Er legt fest, wie oft der Leader seinen Followern mitteilt, dass er weiterhin Leader ist.
Als bewährte Vorgehensweise sollte der Parameter ungefähr auf die Umlaufzeit zwischen den Mitgliedern gesetzt werden. Standardmäßig verwendet etcd ein Heartbeat-Intervall von `100ms`.

Der zweite Parameter heißt *Wahlzeitüberschreitung*. Er legt fest, wie lange ein Follower-Knoten ohne Heartbeat wartet, bevor er selbst versucht, Leader zu werden. Standardmäßig verwendet etcd eine Wahlzeitüberschreitung von `1000ms`.

Bei der Anpassung dieser Werte ist eine Abwägung nötig. Für das Heartbeat-Intervall wird ungefähr das Maximum der durchschnittlichen Umlaufzeiten (RTT) zwischen den Mitgliedern empfohlen, in der Regel bei etwa 0.5-1.5x der Umlaufzeit. Ist das Heartbeat-Intervall zu kurz, sendet etcd unnötige Nachrichten und beansprucht dadurch mehr CPU- und Netzwerkressourcen. Ein zu langes Heartbeat-Intervall führt dagegen zu einer langen Wahlzeitüberschreitung. Bei einer längeren Wahlzeitüberschreitung dauert es länger, den Ausfall eines Leaders zu erkennen. Am einfachsten lässt sich die Umlaufzeit (RTT) mit dem [PING-Werkzeug][ping] messen.

Die Wahlzeitüberschreitung sollte anhand des Heartbeat-Intervalls und der durchschnittlichen Umlaufzeit zwischen den Mitgliedern festgelegt werden. Sie muss mindestens das 10-Fache der Umlaufzeit betragen, um Schwankungen im Netzwerk zu berücksichtigen. Beträgt die Umlaufzeit zwischen den Mitgliedern beispielsweise 10ms, sollte die Wahlzeitüberschreitung mindestens 100ms betragen.

Die Obergrenze der Wahlzeitüberschreitung beträgt 50000ms (50s). Dieser Wert sollte nur bei einem weltweit verteilten etcd-Cluster verwendet werden. Auf dem US-Festland ist eine Umlaufzeit von 130ms realistisch, zwischen den USA und Japan etwa 350-400ms. Bei schwankender Netzwerkleistung oder regelmäßigen Paketverzögerungen bzw. -verlusten können mehrere Wiederholungen nötig sein, um ein Paket erfolgreich zu senden. Daher sind 5s eine sichere Obergrenze für die weltweite Umlaufzeit. Da die Wahlzeitüberschreitung eine Größenordnung über der Broadcast-Zeit liegen sollte, sind bei ~5s für einen weltweit verteilten Cluster 50 Sekunden ein angemessenes Maximum.

Heartbeat-Intervall und Wahlzeitüberschreitung sollten für alle Mitglieder eines Clusters gleich sein. Unterschiedliche Werte für etcd-Mitglieder können die Stabilität des Clusters beeinträchtigen.

Die Standardwerte lassen sich auf der Befehlszeile überschreiben:

```sh
# Command line arguments:
$ etcd --heartbeat-interval=100 --election-timeout=500

# Environment variables:
$ ETCD_HEARTBEAT_INTERVAL=100 ETCD_ELECTION_TIMEOUT=500 etcd
```

Die Werte werden in Millisekunden angegeben.

## Snapshots {#snapshots}

etcd hängt alle Schlüsseländerungen an eine Protokolldatei an. Dieses Protokoll wächst unbegrenzt und enthält den vollständigen linearen Verlauf aller Änderungen an den Schlüsseln. Für wenig genutzte Cluster eignet sich ein vollständiger Verlauf gut; stark genutzte Cluster müssten jedoch ein großes Protokoll mitführen.

Um ein riesiges Protokoll zu vermeiden, erstellt etcd regelmäßig Snapshots. Sie ermöglichen die Kompaktierung des Protokolls: Der aktuelle Systemzustand wird gespeichert, alte Protokolle werden entfernt.

### Snapshots optimieren {#snapshot-tuning}

Raft-Snapshots werden nach einer konfigurierten Anzahl angewendeter Einträge erstellt; etcd 3.7 verwendet das V2-Backend nicht mehr. Standardmäßig erfolgt dies nach jeweils 10,000 Änderungen. Wenn der Arbeitsspeicher- und Datenträgerverbrauch von etcd zu hoch ist, versuchen, den Snapshot-Schwellenwert mit folgender Befehlszeilenoption zu senken:

```sh
# Command line arguments:
$ etcd --snapshot-count=5000

# Environment variables:
$ ETCD_SNAPSHOT_COUNT=5000 etcd
```

## Datenträger {#disk}

Ein etcd-Cluster reagiert sehr empfindlich auf Datenträgerlatenzen. Da etcd Vorschläge dauerhaft in seinem Protokoll speichern muss, können Datenträgerzugriffe anderer Prozesse lange `fsync`-Latenzen verursachen. Dadurch kann etcd Heartbeats verpassen, was zu Zeitüberschreitungen bei Anfragen und zum vorübergehenden Verlust des Leaders führt. Mit hoher Priorität für Datenträgerzugriffe kann ein etcd-Server unter Umständen stabil neben diesen Prozessen laufen.

Unter Linux lässt sich die Priorität der Datenträgerzugriffe von etcd mit `ionice` konfigurieren:

```sh
# best effort, highest priority
$ sudo ionice -c2 -n0 -p `pgrep etcd`
```

## Netzwerk {#network}

Wenn der etcd-Leader viele gleichzeitige Clientanfragen bedient, kann eine Netzwerküberlastung die Verarbeitung von Peer-Anfragen der Follower verzögern. Dies äußert sich auf den Follower-Knoten in Fehlermeldungen zum Sendepuffer:

```
dropped MsgProp to 247ae21ff9436b2d since streamMsg's sending buffer is full
dropped MsgAppResp to 247ae21ff9436b2d since streamMsg's sending buffer is full
```

Diese Fehler lassen sich möglicherweise beheben, indem der Peer-Verkehr von etcd gegenüber dem Clientverkehr priorisiert wird. Unter Linux kann der Peer-Verkehr mit dem Mechanismus zur Verkehrssteuerung priorisiert werden:

```
tc qdisc add dev eth0 root handle 1: prio bands 3
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dport 2380 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip sport 2379 0xffff flowid 1:1
tc filter add dev eth0 parent 1: protocol ip prio 2 u32 match ip dport 2379 0xffff flowid 1:1
```

[ping]: https://en.wikipedia.org/wiki/Ping_(networking_utility)


Zum Aufheben von `tc` Folgendes ausführen:

```
tc qdisc del dev eth0 root
```

## CPU {#cpu}

Da etcd sehr empfindlich auf Latenz reagiert, lässt sich die Leistung unter Linux weiter optimieren, indem der CPU-Governor auf den Modus performance oder conservative gesetzt wird.

Unter Linux lässt sich der CPU-Governor auf den Modus performance setzen:
```
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```
