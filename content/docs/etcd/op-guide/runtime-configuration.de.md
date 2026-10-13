---
title: "Laufzeitrekonfiguration"
weight: 4700
description: "Unterstützung für schrittweise Laufzeitrekonfiguration in etcd"
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-configuration.md"
aliases: [/etcd/op-guide/runtime-configuration/]
---

etcd unterstützt die schrittweise Laufzeitrekonfiguration, mit der die Mitgliedschaft im Cluster während des Betriebs geändert werden kann.

Rekonfigurationsanfragen können nur verarbeitet werden, wenn die Mehrheit der Clustermitglieder funktioniert. Für den produktiven Betrieb wird **dringend empfohlen**, stets mehr als zwei Mitglieder zu verwenden. Das Entfernen eines Mitglieds aus einem Cluster mit zwei Mitgliedern ist unsicher, da auch dessen Mehrheit aus zwei Mitgliedern besteht. Tritt während der Entfernung ein Fehler auf, kann der Cluster möglicherweise nicht mehr weiterarbeiten und einen [Neustart nach einem Mehrheitsausfall][majority failure] benötigen.

Weitere Informationen zum Entwurf der Laufzeitrekonfiguration bietet das [Dokument zur Laufzeitrekonfiguration][runtime-reconf].

## Anwendungsfälle für die Rekonfiguration {#reconfiguration-use-cases}

Dieser Abschnitt beschreibt einige häufige Gründe für die Rekonfiguration eines Clusters. Meist bestehen die erforderlichen Schritte aus Kombinationen des Hinzufügens und Entfernens von Mitgliedern. Diese werden weiter unten unter [Operationen zur Clusterrekonfiguration][cluster-reconf] erläutert.

### Mehrere Rechner austauschen oder aufrüsten {#cycle-or-upgrade-multiple-machines}

Müssen mehrere Clustermitglieder wegen geplanter Wartungsarbeiten umziehen (Hardwareaufrüstung, Netzwerkunterbrechungen usw.), wird empfohlen, die Mitglieder nacheinander zu ändern.

Der Leader kann sicher entfernt werden; während der anschließenden Wahl gibt es jedoch eine kurze Ausfallzeit. Enthält der Cluster mehr als 50MB v2-Daten, wird empfohlen, [das Datenverzeichnis des Mitglieds zu migrieren][member migration].

### Clustergröße ändern {#change-the-cluster-size}

Eine Vergrößerung des Clusters kann die [Fehlertoleranz][fault tolerance table] und die Leseleistung verbessern. Da Clients von jedem Mitglied lesen können, erhöht eine größere Mitgliederzahl den gesamten Durchsatz serialisierbarer Lesezugriffe.

Eine Verkleinerung des Clusters kann die Schreibleistung verbessern, verringert aber seine Ausfallsicherheit. Schreiboperationen werden auf eine Mehrheit der Clustermitglieder repliziert, bevor sie als festgeschrieben gelten. Eine Verkleinerung senkt die erforderliche Mehrheit, sodass jede Schreiboperation schneller festgeschrieben wird.

### Einen ausgefallenen Rechner ersetzen {#replace-a-failed-machine}

Fällt ein Rechner durch einen Hardwaredefekt, ein beschädigtes Datenverzeichnis oder einen anderen schwerwiegenden Fehler aus, sollte er so schnell wie möglich ersetzt werden. Ausgefallene, aber noch nicht entfernte Rechner wirken sich ungünstig auf das Quorum aus und verringern die Toleranz gegenüber einem weiteren Ausfall.

Um den Rechner zu ersetzen, zunächst nach der Anleitung [das Mitglied aus dem Cluster entfernen][remove member] und anschließend [ein neues Mitglied hinzufügen][add member]. Enthält der Cluster mehr als 50MB, wird empfohlen, [das Datenverzeichnis des ausgefallenen Mitglieds zu migrieren][member migration], sofern es noch zugänglich ist.

### Cluster nach einem Mehrheitsausfall neu starten {#restart-cluster-from-majority-failure}

Geht die Mehrheit des Clusters verloren oder haben sich die IP-Adressen aller Knoten geändert, ist für eine sichere Wiederherstellung ein manueller Eingriff erforderlich. Die grundlegenden Schritte umfassen das [Erstellen eines neuen Clusters mit den alten Daten][disaster recovery], das Erzwingen eines einzelnen Mitglieds als Leader und schließlich das schrittweise [Hinzufügen neuer Mitglieder][add member] zu diesem Cluster über die Laufzeitkonfiguration.

### Cluster nach einem Minderheitsausfall wiederherstellen {#recover-cluster-from-minority-failure}

Geht ein einzelnes Mitglied verloren, entspricht dies dem Ersetzen eines ausgefallenen Rechners. Die Schritte stehen unter [Einen ausgefallenen Rechner ersetzen](/de/docs/etcd/op-guide/runtime-configuration/#replace-a-failed-machine).

## Operationen zur Clusterrekonfiguration {#cluster-reconfiguration-operations}

Für diese Anwendungsfälle lassen sich die jeweils erforderlichen Operationen wie folgt beschreiben.

Vor jeder Änderung muss eine einfache Mehrheit (ein Quorum) der etcd-Mitglieder verfügbar sein. Im Wesentlichen gilt dieselbe Anforderung für jede Art von Schreibzugriff auf etcd.

Alle Änderungen am Cluster müssen nacheinander erfolgen:

* Zum Aktualisieren der peerURLs eines einzelnen Mitglieds eine Aktualisierungsoperation ausführen
* Zum Ersetzen eines einzelnen intakten Mitglieds das alte Mitglied entfernen und danach ein neues hinzufügen
* Für eine Erweiterung von 3 auf 5 Mitglieder zwei Hinzufügeoperationen ausführen
* Für eine Verkleinerung von 5 auf 3 zwei Entfernungsoperationen ausführen

Alle Beispiele verwenden das mit etcd gelieferte Befehlszeilenwerkzeug `etcdctl`. Um die Mitgliedschaft ohne `etcdctl` zu ändern, die [v3-gRPC-Mitglieder-API][member-api-grpc] verwenden.

### Ein Mitglied aktualisieren {#update-a-member}

#### Bekannt gegebene Client-URLs aktualisieren {#update-advertise-client-urls}

Um die bekannt gegebenen Client-URLs eines Mitglieds zu aktualisieren, dieses einfach mit der aktualisierten Option `--advertise-client-urls` oder Umgebungsvariablen `ETCD_ADVERTISE_CLIENT_URLS` neu starten. Das neu gestartete Mitglied veröffentlicht die aktualisierten URLs selbst. Eine falsch aktualisierte Client-URL beeinträchtigt den Zustand des etcd-Clusters nicht.

#### Bekannt gegebene Peer-URLs aktualisieren {#update-advertise-peer-urls}

Um die bekannt gegebenen Peer-URLs eines Mitglieds zu aktualisieren, sie zunächst ausdrücklich mit dem member-Befehl ändern und anschließend das Mitglied neu starten. Dieser zusätzliche Schritt ist erforderlich, da Peer-URL-Änderungen die clusterweite Konfiguration ändern und den Zustand des etcd-Clusters beeinflussen können.

Zum Aktualisieren der bekannt gegebenen Peer-URLs zunächst die ID des Zielmitglieds ermitteln. Alle Mitglieder mit `etcdctl` auflisten:

```sh
$ etcdctl member list
6e3bd23ae5f1eae0: name=node2 peerURLs=http://localhost:23802 clientURLs=http://127.0.0.1:23792
924e2e83e93f2560: name=node3 peerURLs=http://localhost:23803 clientURLs=http://127.0.0.1:23793
a8266ecf031671f3: name=node1 peerURLs=http://localhost:23801 clientURLs=http://127.0.0.1:23791
```

In diesem Beispiel wird `update` auf die Mitglieds-ID a8266ecf031671f3 angewendet und deren peerURLs-Wert in `http://10.0.1.10:2380` geändert:

```sh
$ etcdctl member update a8266ecf031671f3 --peer-urls=http://10.0.1.10:2380
Updated member with ID a8266ecf031671f3 in cluster
```

### Ein Mitglied entfernen {#remove-a-member}

Angenommen, die ID des zu entfernenden Mitglieds ist a8266ecf031671f3. Das Mitglied mit dem Befehl `remove` entfernen:

```sh
$ etcdctl member remove a8266ecf031671f3
Removed member a8266ecf031671f3 from cluster
```

Das Zielmitglied beendet sich daraufhin selbst und protokolliert seine Entfernung:

```
etcd: this member has been permanently removed from the cluster. Exiting.
```

Der Leader kann sicher entfernt werden, allerdings ist der Cluster während der Wahl eines neuen Leaders inaktiv. Diese Dauer entspricht normalerweise dem Wahlzeitlimit zuzüglich des Abstimmungsvorgangs.

### Ein neues Mitglied hinzufügen {#add-a-new-member}

Das Hinzufügen eines Mitglieds erfolgt in zwei Schritten:

 * Das neue Mitglied über die [v3-gRPC-Mitglieder-API][member-api-grpc] oder den Befehl `etcdctl member add` zum Cluster hinzufügen.
 * Das neue Mitglied mit der neuen Clusterkonfiguration starten, einschließlich der aktualisierten Mitgliederliste (vorhandene Mitglieder + neues Mitglied).

`etcdctl` fügt ein neues Mitglied hinzu, indem dessen [Name][conf-name] und [bekannt gegebene Peer-URLs][conf-adv-peer] angegeben werden:

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380
added member 9bf1b35fc7761a23 to cluster

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

`etcdctl` hat den Cluster über das neue Mitglied informiert und die für dessen erfolgreichen Start benötigten Umgebungsvariablen ausgegeben. Nun den neuen etcd-Prozess mit den passenden Optionen für das neue Mitglied starten:

```sh
$ export ETCD_NAME="infra3"
$ export ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
$ export ETCD_INITIAL_CLUSTER_STATE=existing
$ etcd --listen-client-urls http://10.0.1.13:2379 --advertise-client-urls http://10.0.1.13:2379 --listen-peer-urls http://10.0.1.13:2380 --initial-advertise-peer-urls http://10.0.1.13:2380 --data-dir %data_dir%
```

Das neue Mitglied läuft als Teil des Clusters und beginnt sofort, zum übrigen Cluster aufzuschließen.

Beim Hinzufügen mehrerer Mitglieder empfiehlt es sich, jeweils ein einzelnes Mitglied zu konfigurieren und seinen korrekten Start zu prüfen, bevor weitere Mitglieder hinzukommen. Wird einem Cluster mit 1 Knoten ein neues Mitglied hinzugefügt, kann der Cluster erst weiterarbeiten, sobald dieses gestartet ist, da er für den Konsens nun zwei Mitglieder als Mehrheit benötigt. Dieses Verhalten tritt nur zwischen der Meldung des neuen Mitglieds durch `etcdctl member add` und dem erfolgreichen Verbindungsaufbau des neuen zum bestehenden Mitglied auf.

#### Ein neues Mitglied als Learner hinzufügen {#add-a-new-member-as-learner}

Seit v3.4 unterstützt etcd das Hinzufügen eines neuen Mitglieds als Learner, also als nicht stimmberechtigtes Mitglied.
Die Gründe und der Entwurf sind im [Entwurfsdokument][design-learner] beschrieben.
Um das Hinzufügen sicherer zu machen und die dabei entstehenden Clusterunterbrechungen zu verkürzen,
empfiehlt es sich, das neue Mitglied zunächst als Learner hinzuzufügen, bis es aufgeholt hat.
Dies lässt sich als Ablauf in drei Schritten beschreiben:

 * Das neue Mitglied über die [gRPC-Mitglieder-API][member-api-grpc] oder den Befehl `etcdctl member add --learner` als Learner hinzufügen.

 * Das neue Mitglied mit der neuen Clusterkonfiguration starten, einschließlich der aktualisierten Mitgliederliste (vorhandene Mitglieder + neues Mitglied).
 Dieser Schritt ist genau derselbe wie zuvor.

 * Den neu hinzugefügten Learner über die [gRPC-Mitglieder-API][member-api-grpc] oder den Befehl `etcdctl member promote` zu einem stimmberechtigten Mitglied befördern.
 Der etcd-Server prüft die Beförderungsanfrage, um die Betriebssicherheit zu gewährleisten.
 Erst wenn sein Raft-Log zum Log des Leaders aufgeholt hat, kann der Learner zum stimmberechtigten Mitglied befördert werden.
 Hat ein Learner-Mitglied noch nicht zum Raft-Log des Leaders aufgeholt, schlägt die Beförderungsanfrage fehl
 (Einzelheiten stehen im Abschnitt [Fehlerfälle bei der Beförderung eines Mitglieds][error cases when promoting a member]).
 In diesem Fall sollte gewartet und die Anfrage später wiederholt werden.

In v3.4 begrenzt der etcd-Server die Zahl der Learner im Cluster auf einen. Dadurch soll vor allem die zusätzliche Last begrenzt werden,
die dem Leader durch die Übertragung von Daten an den Learner entsteht.

Mit `etcdctl member add` und der Option `--learner` ein neues Mitglied als Learner zum Cluster hinzufügen.

```sh
$ etcdctl member add infra3 --peer-urls=http://10.0.1.13:2380 --learner
Member 9bf1b35fc7761a23 added to cluster a7ef944b95711739

ETCD_NAME="infra3"
ETCD_INITIAL_CLUSTER="infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra3=http://10.0.1.13:2380"
ETCD_INITIAL_CLUSTER_STATE=existing
```

Nachdem der neue etcd-Prozess für das hinzugefügte Learner-Mitglied gestartet wurde, den Learner mit `etcdctl member promote` zu einem stimmberechtigten Mitglied befördern.
```
$ etcdctl member promote 9bf1b35fc7761a23
Member 9e29bbaa45d74461 promoted in cluster a7ef944b95711739
```

#### Fehlerfälle beim Hinzufügen von Mitgliedern {#error-cases-when-adding-members}

Im folgenden Fall fehlt ein neuer Host in der Liste der aufgeführten Knoten. Handelt es sich um einen neuen Cluster, muss der Knoten zur Liste der anfänglichen Clustermitglieder hinzugefügt werden.

```sh
$ etcd --name infra3 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: the member count is unequal
exit 1
```

In diesem fehlgeschlagenen Beispiel startet das Mitglied mit einer Adresse (10.0.1.14:2380), die von der registrierten Peer-Adresse (10.0.1.13:2380) abweicht:

```sh
$ etcd --name infra4 \
  --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380,infra4=http://10.0.1.14:2380 \
  --initial-cluster-state existing
etcdserver: assign ids error: unmatched member while checking PeerURLs
exit 1
```

Startet etcd mit dem Datenverzeichnis eines entfernten Mitglieds, beendet es sich automatisch, sobald es sich mit einem aktiven Clustermitglied verbindet:

```sh
$ etcd
etcd: this member has been permanently removed from the cluster. Exiting.
exit 1
```

#### Fehlerfälle beim Hinzufügen eines Learner-Mitglieds {#error-cases-when-adding-a-learner-member}

Ein Learner kann nicht hinzugefügt werden, wenn der Cluster bereits 1 Learner enthält (v3.4).
```
$ etcdctl member add infra4 --peer-urls=http://10.0.1.14:2380 --learner
Error: etcdserver: too many learner members in cluster
```

#### Fehlerfälle bei der Beförderung eines Learner-Mitglieds {#error-cases-when-promoting-a-learner-member}

Ein Learner kann nur zu einem stimmberechtigten Mitglied befördert werden, wenn er mit dem Leader synchron ist.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member which is in sync with leader
```

Die Beförderung eines Mitglieds, das kein Learner ist, schlägt fehl.
```
$ etcdctl member promote 9bf1b35fc7761a23
Error: etcdserver: can only promote a learner member
```

Die Beförderung eines Mitglieds, das im Cluster nicht existiert, schlägt fehl.
```
$ etcdctl member promote 12345abcde
Error: etcdserver: member not found
```


### Strenge Rekonfigurationsprüfung (`-strict-reconfig-check`) {#strict-reconfiguration-check-mode--strict-reconfig-check}

Wie oben beschrieben, empfiehlt es sich, neue Mitglieder einzeln zu konfigurieren und ihren korrekten Start zu prüfen, bevor weitere hinzukommen. Dieses schrittweise Vorgehen ist sehr wichtig: Ist ein neues Mitglied falsch konfiguriert, etwa mit falschen Peer-URLs, kann der Cluster sein Quorum verlieren. Der Quorumverlust entsteht, weil das neue Mitglied bei der Quorumberechnung mitgezählt wird, selbst wenn die übrigen Mitglieder es nicht erreichen können. Auch Verbindungsprobleme oder betriebliche Probleme können zum Quorumverlust führen.

Um dieses Problem zu vermeiden, bietet etcd die Option `-strict-reconfig-check`. Wird sie an etcd übergeben, lehnt etcd Rekonfigurationsanfragen ab, wenn die Anzahl gestarteter Mitglieder nach der Änderung kleiner als das Quorum des neu konfigurierten Clusters wäre.

Diese Option ist standardmäßig aktiviert.

[add member]: #add-a-new-member
[cluster-reconf]: #cluster-reconfiguration-operations
[conf-adv-peer]: /de/docs/etcd/op-guide/configuration#clustering
[conf-name]: /de/docs/etcd/op-guide/configuration#member
[design-learner]: /de/docs/etcd/learning/design-learner
[disaster recovery]: /de/docs/etcd/op-guide/recovery
[error cases when promoting a member]: #error-cases-when-promoting-a-learner-member
[fault tolerance table]: https://etcd.io/docs/v2.3/admin_guide/#fault-tolerance-table
[majority failure]: #restart-cluster-from-majority-failure
[member migration]: https://etcd.io/docs/v2.3/admin_guide/#member-migration
[member-api]: https://etcd.io/docs/v2.3/members_api/
[member-api-grpc]: /de/docs/etcd/dev-guide/api_reference_v3/
[remove member]: #remove-a-member
[runtime-reconf]: /de/docs/etcd/op-guide/runtime-reconf-design/
