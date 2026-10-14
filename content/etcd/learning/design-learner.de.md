---
title: Design der Learner in etcd
weight: 2375
description: Häufige Schwierigkeiten bei der Neukonfiguration der Clustermitgliedschaft entschärfen
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/learning/design-learner.md"
---

Learner in etcd {#etcd-learner}
============

*Gyuho Lee (github.com/gyuho, Amazon Web Services, Inc.), Joe Betz (github.com/jpbetz, Google Inc.)*


Hintergrund {#background}
==========

Die Neukonfiguration der Clustermitgliedschaft zählt zu den größten Herausforderungen im Betrieb. Im Folgenden werden häufige Schwierigkeiten betrachtet.

### 1. Ein neues Clustermitglied überlastet den Leader {#1-new-cluster-member-overloads-leader}
Ein neu beigetretenes etcd-Mitglied startet ohne Daten und fordert daher zusätzliche Aktualisierungen vom Leader an, bis es dessen Logstand erreicht hat. Dadurch kann das Netzwerk des Leaders leichter überlastet werden, sodass seine Heartbeats an Follower blockiert oder verworfen werden. In diesem Fall kann bei einem Follower das Wahlzeitlimit ablaufen und eine neue Leader-Wahl auslösen. Ein Cluster mit einem neuen Mitglied ist somit anfälliger für Leader-Wahlen. Sowohl die Wahl als auch die anschließende Übertragung der Aktualisierungen an das neue Mitglied können Zeiträume verursachen, in denen der Cluster nicht verfügbar ist (siehe *Abbildung 1*).

![server-learner-figure-01](/etcd/learning/img/server-learner-figure-01.png)

### 2. Szenarien mit Netzwerkpartitionen {#2-network-partitions-scenarios}
Was passiert bei einer Netzwerkpartition? Das hängt von der Partition des Leaders ab. Verfügt der Leader weiterhin über ein aktives Quorum, arbeitet der Cluster weiter (siehe *Abbildung 2*).

![server-learner-figure-02](/etcd/learning/img/server-learner-figure-02.png)

#### 2.1 Isolation des Leaders {#21-leader-isolation}
Was passiert, wenn der Leader vom Rest des Clusters isoliert wird? Der Leader überwacht den Fortschritt jedes Followers. Verliert er die Verbindung zum Quorum, kehrt er in die Follower-Rolle zurück. Dies beeinträchtigt die Clusterverfügbarkeit (siehe *Abbildung 3*).

![server-learner-figure-03](/etcd/learning/img/server-learner-figure-03.png)

Wird einem Cluster mit 3 Knoten ein neuer Knoten hinzugefügt, steigt die Clustergröße auf 4 und die Quorumgröße auf 3. Was passiert, wenn nach dem Beitritt eines neuen Knotens eine Netzwerkpartition auftritt? Das hängt davon ab, in welcher Partition sich das neue Mitglied anschließend befindet.

#### 2.2 Clusteraufteilung 3+1 {#22-cluster-split-31}
Befindet sich der neue Knoten in derselben Partition wie der Leader, verfügt dieser weiterhin über ein aktives Quorum von 3. Es findet keine Leader-Wahl statt, und die Clusterverfügbarkeit bleibt unbeeinträchtigt (siehe *Abbildung 4*).

![server-learner-figure-04](/etcd/learning/img/server-learner-figure-04.png)

#### 2.3 Clusteraufteilung 2+2 {#23-cluster-split-22}
Wird der Cluster in 2 und 2 Knoten aufgeteilt, erreicht keine Partition das Quorum von 3. In diesem Fall findet eine Leader-Wahl statt (siehe *Abbildung 5*).

![server-learner-figure-05](/etcd/learning/img/server-learner-figure-05.png)

#### 2.4 Quorum verloren {#24-quorum-lost}
Was passiert, wenn zuerst eine Netzwerkpartition auftritt und danach ein neues Mitglied hinzugefügt wird? In einem partitionierten Cluster mit 3 Knoten ist bereits ein Follower abgetrennt. Wird ein neues Mitglied hinzugefügt, steigt das Quorum von 2 auf 3. Der Cluster hat nun nur 2 aktive von 4 Knoten, verliert dadurch sein Quorum und beginnt eine neue Leader-Wahl (siehe *Abbildung 6*).

![server-learner-figure-06](/etcd/learning/img/server-learner-figure-06.png)

Da das Hinzufügen eines Mitglieds die Quorumgröße ändern kann, wird beim Ersetzen eines nicht funktionsfähigen Knotens stets empfohlen, zuerst „member remove“ auszuführen.

Das Hinzufügen eines neuen Mitglieds zu einem Cluster mit 1 Knoten erhöht die Quorumgröße auf 2. Sobald der bisherige Leader feststellt, dass das Quorum nicht aktiv ist, löst dies unmittelbar eine Leader-Wahl aus. Der Grund: „member add“ ist ein Vorgang mit 2 Schritten, bei dem der Benutzer zuerst den Befehl „member add“ ausführen und anschließend den Prozess des neuen Knotens starten muss (siehe *Abbildung 7*).

![server-learner-figure-07](/etcd/learning/img/server-learner-figure-07.png)

### 3. Fehlkonfigurationen des Clusters {#3-cluster-misconfigurations}
Noch problematischer ist ein falsch konfiguriertes hinzugefügtes Mitglied. Die Neukonfiguration der Mitgliedschaft besteht aus zwei Schritten: „etcdctl member add“ und dem Start eines etcd-Serverprozesses mit der angegebenen Peer-URL. Der Befehl „member add“ wird also unabhängig von der URL angewendet, selbst wenn diese ungültig ist. Werden im ersten Schritt ungültige URLs verwendet, kann der zweite Schritt den neuen etcd-Prozess nicht einmal starten. Sobald der Cluster sein Quorum verliert, lässt sich die Mitgliedschaftsänderung nicht mehr rückgängig machen (siehe *Abbildung 8*).

![server-learner-figure-08](/etcd/learning/img/server-learner-figure-08.png)

Dasselbe gilt für einen Cluster mit mehreren Knoten. Beispielsweise hat der Cluster zwei nicht verfügbare Mitglieder, eines ausgefallen und eines falsch konfiguriert, sowie zwei aktive Mitglieder. Er benötigt nun aber mindestens 3 Stimmen, um die Clustermitgliedschaft zu ändern (siehe *Abbildung 9*).

![server-learner-figure-09](/etcd/learning/img/server-learner-figure-09.png)

Wie gezeigt, kann eine einfache Fehlkonfiguration den gesamten Cluster funktionsunfähig machen. In diesem Fall muss ein Betreiber den Cluster manuell mit der Option `etcd --force-new-cluster` neu erstellen. Da etcd für Kubernetes zu einem betriebskritischen Dienst geworden ist, können selbst kürzeste Ausfälle erhebliche Auswirkungen auf Benutzer haben. Wie lassen sich solche etcd-Operationen vereinfachen? Besonders entscheidend für die Clusterverfügbarkeit ist die Leader-Wahl: Lässt sich die Neukonfiguration der Mitgliedschaft weniger störend gestalten, indem die Quorumgröße unverändert bleibt? Kann ein neuer Knoten zunächst inaktiv bleiben und nur die nötigsten Aktualisierungen vom Leader anfordern, bis er aufgeholt hat? Lassen sich Fehlkonfigurationen der Mitgliedschaft immer rückgängig machen und sicherer behandeln, sodass ein falscher Befehl zum Hinzufügen eines Mitglieds niemals den Cluster ausfallen lässt? Sollte ein Benutzer beim Hinzufügen eines Mitglieds die Netzwerktopologie berücksichtigen müssen? Kann die API zum Hinzufügen von Mitgliedern unabhängig von der Lage der Knoten und bestehenden Netzwerkpartitionen funktionieren?

Raft-Learner {#raft-learner}
============

Um die im vorigen Abschnitt beschriebenen Verfügbarkeitslücken zu verringern, führt [Raft §4.2.1](https://github.com/ongardie/dissertation/blob/master/stanford.pdf) den neuen Knotenzustand „Learner“ ein. Ein solcher Knoten tritt dem Cluster als **nicht stimmberechtigtes Mitglied** bei, bis er den Logstand des Leaders erreicht hat.

Funktionen in v3.4 {#features-in-v34}
----------------

Ein Betreiber sollte möglichst wenig Aufwand haben, um einen neuen Learner-Knoten hinzuzufügen. Der Befehl `member add --learner` fügt einen Learner hinzu, der als nicht stimmberechtigtes Mitglied beitritt, aber dennoch alle Daten vom Leader empfängt (siehe *Abbildung 10*).

![server-learner-figure-10](/etcd/learning/img/server-learner-figure-10.png)

Hat ein Learner den Fortschritt des Leaders eingeholt, kann er über die API `member promote` zu einem stimmberechtigten Mitglied hochgestuft werden und zählt dann zum Quorum (siehe *Abbildung 11*).

![server-learner-figure-11](/etcd/learning/img/server-learner-figure-11.png)

Der etcd-Server validiert die Hochstufungsanfrage, um einen sicheren Betrieb zu gewährleisten. Erst wenn sein Log den Stand des Leaders erreicht hat, kann ein Learner zu einem stimmberechtigten Mitglied hochgestuft werden (siehe *Abbildung 12*).

![server-learner-figure-12](/etcd/learning/img/server-learner-figure-12.png)

Bis zur Hochstufung dient ein Learner nur als Standby-Knoten: Die Führungsrolle kann ihm nicht übertragen werden. Ein Learner lehnt Lese- und Schreibanfragen von Clients ab; der Client-Load-Balancer sollte keine Anfragen an ihn weiterleiten. Daher muss ein Learner keine Read-Index-Anfragen an den Leader senden. Diese Einschränkung vereinfacht die erste Learner-Implementierung in v3.4 (siehe *Abbildung 13*).

![server-learner-figure-13](/etcd/learning/img/server-learner-figure-13.png)

Außerdem begrenzt etcd die Gesamtzahl der Learner in einem Cluster, um eine Überlastung des Leaders durch Logreplikation zu vermeiden. Ein Learner stuft sich niemals selbst hoch. etcd liefert Statusinformationen über Learner und Sicherheitsprüfungen; die endgültige Entscheidung über eine Hochstufung muss jedoch der Clusterbetreiber treffen.

Vorgeschlagene Funktionen für künftige Versionen {#proposed-features-for-future-releases}
----------------

*Learner als einzigen Anfangszustand und Standard festlegen*: Wird der Anfangszustand neuer Mitglieder auf Learner gesetzt, erhöht dies die Sicherheit der Mitgliedschaftsneukonfiguration erheblich, da Learner die Quorumgröße nicht verändern. Fehlkonfigurationen lassen sich dann immer rückgängig machen, ohne das Quorum zu verlieren.

*Die Hochstufung zum stimmberechtigten Mitglied vollständig automatisieren*: Sobald ein Learner den Logstand des Leaders erreicht hat, kann der Cluster ihn automatisch hochstufen. Der Benutzer legt bestimmte von etcd benötigte Schwellenwerte fest. Sind die Anforderungen erfüllt, stuft sich der Learner selbst zu einem stimmberechtigten Mitglied hoch. Aus Benutzersicht würde „member add“ wie bisher funktionieren, aber dank der Learner-Funktion mehr Sicherheit bieten.

*Learner als Standby-Knoten für Failover verwenden*: Ein Learner tritt als Standby-Knoten bei und wird automatisch hochgestuft, wenn die Clusterverfügbarkeit beeinträchtigt ist.

*Learner nur für Lesezugriffe verwenden*: Ein Learner kann als ausschließlich lesender Knoten dienen, der nie hochgestuft wird. In einem Modus mit schwacher Konsistenz empfängt er nur Daten vom Leader und verarbeitet keine Schreibvorgänge. Lokale Lesezugriffe ohne Konsensaufwand würden die Last des Leaders erheblich verringern, können aber veraltete Daten liefern. In einem Modus mit starker Konsistenz fordert der Learner einen Leseindex vom Leader an, um die neuesten Daten bereitzustellen, lehnt Schreibvorgänge aber weiterhin ab.

Learner und Mirror Maker im Vergleich {#learner-vs-mirror-maker}
========================

etcd implementiert „mirror maker“ mit der Watch-API, um Schlüsselerstellungen und -aktualisierungen fortlaufend an einen separaten Cluster weiterzuleiten. Nach Abschluss der anfänglichen Synchronisierung verursacht die Spiegelung gewöhnlich nur geringe zusätzliche Latenz. Learner und Spiegelung überschneiden sich darin, dass beide vorhandene Daten für reine Lesezugriffe replizieren können. Die Spiegelung garantiert jedoch keine Linearisierbarkeit. Bei Netzwerkunterbrechungen können frühere Schlüssel-Wert-Paare bereits verworfen worden sein, und von Clients wird erwartet, die Watch-Antworten auf korrekte Reihenfolge zu prüfen. Eine Spiegelung bietet daher keine Reihenfolgegarantie. Spiegelung eignet sich für minimale Latenz, etwa zwischen Rechenzentren, auf Kosten der Konsistenz. Learner eignen sich, um alle historischen Daten und deren Reihenfolge zu erhalten.

Anhang: Learner-Implementierung in v3.4 {#appendix-learner-implementation-in-v34}
========================================

*Den Knotentyp "Learner" in der API "MemberAdd" verfügbar machen.*

Der etcd-Client ergänzt die API „MemberAdd“ um eine Option für Learner-Knoten. Der Server-Handler von etcd wendet einen Mitgliedschaftsänderungseintrag vom Typ `pb.ConfChangeAddLearnerNode` an. Nach Anwendung des Befehls tritt ein Server mit der Option `etcd --initial-cluster-state=existing` dem Cluster bei. Dieser Learner-Knoten ist weder stimmberechtigt noch zählt er zum Quorum.

Der etcd-Server darf die Führungsrolle keinem Learner übertragen, da dieser noch zurückliegen kann und nicht zum Quorum zählt. Der etcd-Server begrenzt die Anzahl der Learner pro Cluster auf einen: Je mehr Learner vorhanden sind, desto mehr Daten muss der Leader verteilen. Clients können mit einem Learner-Knoten kommunizieren, dieser lehnt jedoch alle Anfragen außer serialisierbaren Lesezugriffen und der API für den Mitgliedsstatus ab. Das vereinfacht die erste Implementierung. Künftig kann ein Learner zu einem ausschließlich lesenden Server erweitert werden, der Clusterdaten fortlaufend spiegelt. Der Client-Load-Balancer muss eine Hilfsfunktion bereitstellen, um den Endpunkt eines Learner-Knotens auszuschließen. Andernfalls können Anfragen an den Learner fehlschlagen. Der Client-Aufruf zur Mitgliedersynchronisierung sollte den Knotentyp Learner berücksichtigen, ebenso der Aufruf zur Aktualisierung der Client-Endpunkte.

Die Antworten von `MemberList` und `MemberStatus` sollten angeben, welcher Knoten ein Learner ist.

*Die API "MemberPromote" hinzufügen.*

Raft-intern stuft ein zweiter `MemberAdd`-Aufruf für den Learner-Knoten diesen zu einem stimmberechtigten Mitglied hoch. Der Leader verwaltet den Fortschritt jedes Followers und Learners. Hat der Learner die Verarbeitung seiner Snapshot-Nachricht noch nicht abgeschlossen, wird die Hochstufungsanfrage abgelehnt. Sie wird genau dann angenommen, wenn der Learner-Knoten funktionsfähig ist und mit dem Leader synchron ist oder die Differenz innerhalb des Schwellenwerts liegt. Beispielsweise muss die Zahl der an den Learner zu replizierenden Einträge unter 1/10 der Snapshot-Anzahl liegen; damit ist es weniger wahrscheinlich, dass der Leader selbst nach der Hochstufung einen Snapshot an den Learner senden müsste. Diese gesamte Logik ist im Paket `etcdserver` fest codiert und nicht konfigurierbar.

Referenzen {#reference}
=========

- Ursprüngliches GitHub-Issue: [etcd#9161](https://github.com/etcd-io/etcd/issues/9161)
- Anwendungsfall: [etcd#3715](https://github.com/etcd-io/etcd/issues/3715)
- Anwendungsfall: [etcd#8888](https://github.com/etcd-io/etcd/issues/8888)
- Anwendungsfall: [etcd#10114](https://github.com/etcd-io/etcd/issues/10114)
