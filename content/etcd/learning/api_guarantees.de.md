---
title: Garantien der etcd-API
weight: 2750
description: API-Garantien von etcd
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/api_guarantees.md"
---

etcd ist ein konsistenter und dauerhafter Schlüssel-Wert-Speicher.
Der Zugriff erfolgt über [gRPC-Dienste][gRPC Services].
etcd bietet die stärksten Konsistenz- und Dauerhaftigkeitsgarantien für ein verteiltes System.
Diese Spezifikation führt die API-Garantien von etcd auf.

### Betrachtete APIs {#apis-to-consider}

* KV-APIs
  * [Range](/de/etcd/learning/api/#range)
  * [RangeStream](/de/etcd/learning/api/#rangestream)
  * [Put](/de/etcd/learning/api/#put)
  * [Delete](/de/etcd/learning/api/#delete-range)
  * [Transaktion](/de/etcd/learning/api/#transaction)
* Watch-APIs
  * [Watch](/de/etcd/learning/api/#watch-api)
* Lease-APIs
  * [Grant](/de/etcd/learning/api/#obtaining-leases)
  * [Revoke]
  * [Keepalive](/de/etcd/learning/api/#keep-alives)

Die KV-API ermöglicht das direkte Lesen und Bearbeiten des Schlüssel-Wert-Speichers.
Mit der Watch-API lassen sich Änderungen am Schlüssel-Wert-Speicher abonnieren.
Mit der Lease-API lässt sich einem Schlüssel eine Lebensdauer zuweisen.

Die KV- und Watch-APIs erlauben den Zugriff nicht nur auf die neuesten Schlüsselversionen,
sondern auch auf frühere Versionen innerhalb eines zusammenhängenden Verlaufsfensters,
das durch eine Kompaktierungsoperation begrenzt wird.

Ein Aufruf der KV-API wirkt unmittelbar, während die Watch-API mit einer nicht begrenzten Verzögerung zurückkehrt.
In einem korrekt arbeitenden etcd-Cluster sollten Watch-Ereignisse etwa 10ms nach ihrem Auftreten sichtbar werden.
Es gibt jedoch keine Obergrenze; in gestörten Clustern kommen Ereignisse möglicherweise nie an.

## KV-APIs {#kv-apis}

etcd gewährleistet Dauerhaftigkeit und strikte Serialisierbarkeit für alle KV-API-Aufrufe.
Dies sind die stärksten Isolationsgarantien verteilter transaktionaler Datenbanksysteme.

### Dauerhaftigkeit {#durability}

Alle abgeschlossenen Operationen sind dauerhaft. Auch alle zugänglichen Daten sind dauerhaft gespeichert.
Ein Lesezugriff gibt niemals Daten zurück, die noch nicht dauerhaft gespeichert wurden.

### Strikte Serialisierbarkeit {#strict-serializability}

Operationen des KV-Dienstes sind atomar und erfolgen in einer totalen Ordnung, die ihrer Echtzeitreihenfolge entspricht.
Diese totale Ordnung ergibt sich aus der [Revision][revision].
Weitere Informationen zur [strikten Serialisierbarkeit][strict serializability].

Bei Transaktionen ohne verschachtelte TXNs entspricht die Ausführungsreihenfolge garantiert
jener in der Operationsliste. Dadurch sind die GET-Antworten innerhalb der Transaktion stabil.
Bei Transaktionen mit verschachtelten TXNs ist die Ausführungsreihenfolge nicht festgelegt.

Strikte Serialisierbarkeit impliziert weitere, schwächere Garantien, die möglicherweise leichter verständlich sind:

#### Atomarität {#atomicity}

Alle API-Anfragen sind atomar: Eine Operation wird entweder vollständig oder gar nicht abgeschlossen.
Bei Watch-Anfragen befinden sich alle von einer Operation erzeugten Ereignisse in einer Watch-Antwort.
Ein Watch beobachtet niemals nur einen Teil der Ereignisse einer einzelnen Operation.

#### Linearisierbarkeit {#linearizability}

Aus Sicht des Clients bietet Linearisierbarkeit nützliche Eigenschaften, die das Nachvollziehen des Verhaltens erleichtern.
Die folgende klare Beschreibung stammt aus der
[Originalveröffentlichung][linearizability]: `Linearisierbarkeit erweckt den Eindruck, dass jede von nebenläufigen Prozessen
ausgeführte Operation zu einem Zeitpunkt zwischen ihrem Aufruf und ihrer Antwort
augenblicklich wirksam wird.`

Angenommen, ein Client schließt einen Schreibvorgang zum Zeitpunkt 1 (*t1*) ab.
Ein Client, der zu *t2* mit *t2* > *t1* einen Lesevorgang startet, sollte einen Wert erhalten,
der mindestens so aktuell ist wie der zuvor zu *t1* abgeschlossene Schreibvorgang.
Der Lesevorgang wird möglicherweise aber erst zu *t3* abgeschlossen. Linearisierbarkeit garantiert,
dass er den neuesten Wert zu einem Zeitpunkt zwischen seinem Beginn zu *t2* und seinem Abschluss
zu *t3* zurückgibt. Er berücksichtigt alle vor seinem Beginn abgeschlossenen Schreibvorgänge.
Ein gleichzeitiger Schreibvorgang zwischen *t2* und *t3* kann berücksichtigt werden oder auch nicht;
der zurückgegebene Wert muss beim Abschluss des Lesevorgangs nicht der neueste sein.

etcd gewährleistet standardmäßig Linearisierbarkeit für alle anderen Operationen.
Sie hat jedoch ihren Preis, da linearisierte Anfragen den Raft-Konsensprozess durchlaufen müssen.
Für geringere Latenzen und höheren Durchsatz bei Leseanfragen können Clients deren Konsistenzmodus
auf `serializable` setzen. Dabei können gegenüber dem Quorum veraltete Daten gelesen werden,
doch der Leistungsnachteil linearisierter Zugriffe durch ihre Abhängigkeit vom laufenden Konsens entfällt.

## Watch-APIs {#watch-apis}

Watches bieten folgende Garantien für Ereignisse:
* Geordnet - Ereignisse sind nach Revision geordnet.
  Ein Ereignis erscheint niemals in einem Watch, wenn es zeitlich vor einem bereits ausgegebenen Ereignis liegt.
  Bei Transaktionen ohne verschachtelte TXNs entspricht die Reihenfolge der erzeugten Ereignisse garantiert
  der Reihenfolge in der Operationsliste. Bei Transaktionen mit verschachtelten TXNs ist sie nicht festgelegt.
* Eindeutig - Ein Ereignis erscheint niemals zweimal in einem Watch.
* Zuverlässig - Innerhalb des verfügbaren Verlaufsfensters geht niemals eine Teilfolge einer Ereignisfolge verloren.
  Sind Ereignisse zeitlich als a < b < c geordnet und empfängt der Watch a und c,
  empfängt er garantiert auch b, sofern b im verfügbaren Verlaufsfenster liegt.
* Atomar - Eine Ereignisliste umfasst garantiert vollständige Revisionen.
  Aktualisierungen mehrerer Schlüssel in derselben Revision werden nicht auf mehrere Ereignislisten aufgeteilt.
* Fortsetzbar - Ein unterbrochener Watch kann durch einen neuen Watch fortgesetzt werden,
  der nach der letzten vor der Unterbrechung in einem Watch-Ereignis empfangenen Revision beginnt,
  sofern diese Revision noch im Verlaufsfenster liegt.
* Mit Fortschrittsmarken - Fortschrittsbenachrichtigungen garantieren, dass alle Ereignisse bis zu einer Revision bereits ausgeliefert wurden.

etcd gewährleistet keine Linearisierbarkeit für Watch-Operationen. Von Benutzern wird erwartet,
die Revision von Watch-Ereignissen zu prüfen, um ihre korrekte Reihenfolge gegenüber anderen Operationen sicherzustellen.

## Lease-APIs {#lease-apis}

etcd bietet [einen Lease-Mechanismus][lease]. Der wichtigste Anwendungsfall einer Lease ist die
Implementierung verteilter Koordinationsmechanismen wie verteilter Sperren. Der Mechanismus selbst ist einfach:
Eine Lease kann mit der Grant-API erstellt, mit der Put-API einem Schlüssel zugeordnet und mit der Revoke-API
widerrufen werden. Sie läuft nach ihrer anhand der realen Uhrzeit gemessenen Lebensdauer (TTL) ab.
Um korrekte verteilte Koordinationsmechanismen zu implementieren, müssen Benutzer jedoch
[die wesentlichen Eigenschaften der APIs und ihrer Verwendung][why] kennen.

## etcd-spezifische Definitionen {#etcd-specific-definitions}

### Abgeschlossene Operation {#operation-completed}

Eine etcd-Operation gilt als abgeschlossen, wenn sie durch Konsens bestätigt und damit von der
Speicherengine von etcd „ausgeführt“, also dauerhaft gespeichert wurde. Der Client weiß, dass eine
Operation abgeschlossen ist, sobald er eine Antwort vom etcd-Server erhält. Bei einer Zeitüberschreitung
oder einer Netzwerkunterbrechung zwischen Client und etcd-Mitglied kann ihr Status für den Client jedoch
ungewiss sein. etcd kann Operationen auch während einer Leader-Wahl abbrechen. In diesem Fall sendet
etcd keine `abort`-Antworten auf ausstehende Client-Anfragen.

### Revision {#revision}

Einer etcd-Operation, die den Schlüssel-Wert-Speicher ändert, wird genau eine steigende Revision zugewiesen.
Eine Transaktionsoperation kann den Speicher mehrfach ändern, erhält aber nur eine Revision.
Das Revisionsattribut eines durch die Operation geänderten Schlüssel-Wert-Paars hat denselben Wert
wie die Revision der Operation. Die Revision kann als logische Uhr des Schlüssel-Wert-Speichers dienen.
Ein Paar mit einer größeren Revision wurde nach einem Paar mit einer kleineren Revision geändert.
Zwei Schlüssel-Wert-Paare mit derselben Revision wurden durch eine Operation „gleichzeitig“ geändert.

[grpc Services]: /de/etcd/learning/api/#grpc-services
[lease]: https://web.stanford.edu/class/cs240/readings/leases.pdf
[linearizability]: https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf
[serializable_isolation]: https://en.wikipedia.org/wiki/Isolation_(database_systems)#Serializable
[strict serializability]: http://jepsen.io/consistency/models/strict-serializable
[txn]: /de/etcd/learning/api/#transaction
[why]: /de/etcd/learning/why/#notes-on-the-usage-of-lock-and-lease
[revision]: #revision
