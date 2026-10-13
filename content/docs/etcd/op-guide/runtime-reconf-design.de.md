---
title: "Entwurf der Laufzeitrekonfiguration"
weight: 4650
description: "Der Entwurf der etcd-Befehle zur Laufzeitrekonfiguration"
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/runtime-reconf-design.md"
aliases: [/etcd/op-guide/runtime-reconf-design/]
---

Die Laufzeitrekonfiguration gehört zu den schwierigsten und fehleranfälligsten Funktionen eines verteilten Systems, insbesondere eines konsensbasierten Systems wie etcd.

Im Folgenden wird erläutert, wie die Befehle zur Laufzeitrekonfiguration von etcd entworfen wurden und wie wir diese Probleme gelöst haben.

## Konfigurationsänderungen in zwei Phasen schützen den Cluster {#two-phase-config-changes-keep-the-cluster-safe}

In etcd muss jede Laufzeitrekonfiguration aus Sicherheitsgründen [zwei Phasen][add-member] durchlaufen. Um beispielsweise ein Mitglied hinzuzufügen, wird zunächst der Cluster über die neue Konfiguration informiert und anschließend das neue Mitglied gestartet.

Phase 1 – Den Cluster über die neue Konfiguration informieren

Um einem etcd-Cluster ein Mitglied hinzuzufügen, wird dies über einen API-Aufruf angefordert. Dies ist die einzige Möglichkeit, ein neues Mitglied zu einem bestehenden Cluster hinzuzufügen. Der API-Aufruf kehrt zurück, sobald sich der Cluster auf die Konfigurationsänderung geeinigt hat.

Phase 2 – Das neue Mitglied starten

Damit das neue etcd-Mitglied dem bestehenden Cluster beitritt, den korrekten Wert für `initial-cluster` angeben und `initial-cluster-state` auf `existing` setzen. Beim Start kontaktiert das Mitglied zunächst den bestehenden Cluster und prüft, ob dessen aktuelle Konfiguration mit der in `initial-cluster` angegebenen erwarteten Konfiguration übereinstimmt. Sobald das neue Mitglied erfolgreich gestartet ist, hat der Cluster die erwartete Konfiguration erreicht.

Die Aufteilung in zwei getrennte Phasen zwingt Benutzer dazu, Änderungen der Clustermitgliedschaft ausdrücklich vorzunehmen. Tatsächlich verschafft dies mehr Flexibilität und macht die Abläufe leichter nachvollziehbar. Wird beispielsweise versucht, ein neues Mitglied mit derselben ID wie ein bereits vorhandenes Mitglied hinzuzufügen, scheitert die Aktion sofort in der ersten Phase, ohne den laufenden Cluster zu beeinträchtigen. Ein ähnlicher Schutz verhindert, dass neue Mitglieder versehentlich hinzugefügt werden. Versucht ein neues etcd-Mitglied beizutreten, bevor der Cluster die Konfigurationsänderung angenommen hat, wird es vom Cluster nicht akzeptiert.

Ohne den ausdrücklichen Ablauf für Mitgliedschaftsänderungen wäre etcd anfällig für unerwartete Änderungen der Clustermitgliedschaft. Läuft etcd beispielsweise unter einem Init-System wie systemd, würde etcd nach der Entfernung über die Mitgliedschafts-API neu gestartet und beim Start erneut versuchen, dem Cluster beizutreten. Diese unerwartete Schleife würde sich jedes Mal wiederholen, wenn ein Mitglied über die API entfernt wird und systemd etcd nach einem Fehlschlag neu starten soll.

Wir gehen davon aus, dass die Laufzeitrekonfiguration nur selten erforderlich ist. Daher haben wir sie bewusst als ausdrücklichen, benutzergesteuerten Vorgang gestaltet, um die Konfigurationssicherheit zu gewährleisten und den Cluster unter klarer Kontrolle reibungslos zu betreiben.

## Dauerhafter Quorumverlust erfordert einen neuen Cluster {#permanent-loss-of-quorum-requires-new-cluster}

Verliert ein Cluster dauerhaft die Mehrheit seiner Mitglieder, muss ein neuer Cluster aus einem alten Datenverzeichnis gestartet werden, um den vorherigen Zustand wiederherzustellen.

Es wäre durchaus möglich, ausgefallene Mitglieder zwangsweise aus dem bestehenden Cluster zu entfernen und ihn so wiederherzustellen. Wir unterstützen dieses Verfahren jedoch nicht, da es die normale Commit-Phase des Konsensverfahrens umgeht und somit unsicher ist. Ist das zu entfernende Mitglied tatsächlich noch aktiv oder wird die Entfernung über verschiedene Mitglieder desselben Clusters erzwungen, entstehen voneinander abweichende Cluster mit derselben clusterID. Dies ist sehr gefährlich und im Nachhinein schwer zu untersuchen oder zu beheben.

Bei einer korrekten Installation ist die Wahrscheinlichkeit eines dauerhaften Mehrheitsverlusts sehr gering. Das Problem ist jedoch schwerwiegend genug, um besondere Vorsorge zu rechtfertigen. Wir empfehlen dringend, vor dem produktiven Einsatz von etcd die [Dokumentation zur Disaster Recovery][disaster-recovery] zu lesen und Vorkehrungen für einen dauerhaften Mehrheitsverlust zu treffen.

## Den öffentlichen Erkennungsdienst nicht für die Laufzeitrekonfiguration verwenden {#do-not-use-public-discovery-service-for-runtime-reconfiguration}

Der öffentliche Erkennungsdienst sollte nur zur Initialisierung eines Clusters verwendet werden. Um ein Mitglied zu einem bestehenden Cluster hinzuzufügen, die API zur Laufzeitrekonfiguration verwenden.

Der Erkennungsdienst ist für die Initialisierung eines etcd-Clusters in einer Cloud-Umgebung gedacht, wenn die IP-Adressen aller Mitglieder noch nicht bekannt sind. Nach erfolgreicher Initialisierung sind diese IP-Adressen bekannt. Technisch sollte der Erkennungsdienst dann nicht mehr benötigt werden.

Der öffentliche Erkennungsdienst scheint eine bequeme Möglichkeit zur Laufzeitrekonfiguration zu sein, da er bereits alle Informationen zur Clusterkonfiguration besitzt. Die Abhängigkeit von ihm bringt jedoch Probleme mit sich:

1. Sie schafft externe Abhängigkeiten über den gesamten Lebenszyklus des Clusters hinweg, nicht nur während der Initialisierung. Bei Netzwerkproblemen zwischen dem Cluster und dem öffentlichen Erkennungsdienst wird der Cluster beeinträchtigt.

2. Der öffentliche Erkennungsdienst muss über den gesamten Lebenszyklus des Clusters hinweg dessen korrekte Laufzeitkonfiguration abbilden. Er muss Sicherheitsmechanismen gegen unerwünschte Aktionen bereitstellen, was schwierig ist.

3. Der öffentliche Erkennungsdienst muss Zehntausende von Clusterkonfigurationen aufbewahren. Das Backend unseres öffentlichen Erkennungsdiensts ist für diese Arbeitslast nicht ausgelegt.

Wird ein Erkennungsdienst mit Unterstützung für Laufzeitrekonfiguration benötigt, ist ein eigener privater Dienst die beste Wahl.

[add-member]: /de/docs/etcd/op-guide/runtime-configuration/#add-a-new-member
[disaster-recovery]: /de/docs/etcd/op-guide/recovery/
