---
title: "Ausfallarten"
weight: 4250
description: "Arten von Ausfällen und ihre Tolerierung durch etcd"
categories: [Konzept]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/op-guide/failures.md"
aliases: [/etcd/op-guide/failures/]
---

In großen Rechnerinstallationen treten häufig Ausfälle auf. Ein Rechner fällt aus, wenn seine Hardware oder Software nicht ordnungsgemäß funktioniert. Bei Stromausfällen oder Netzwerkproblemen können mehrere Rechner gleichzeitig ausfallen. Auch mehrere Ausfallarten können zugleich auftreten; es ist nahezu unmöglich, alle denkbaren Ausfallszenarien aufzuzählen.

Dieser Abschnitt ordnet Ausfälle nach Arten ein und erläutert, wie etcd sie toleriert. Die meisten, wenn nicht alle Benutzer können einen konkreten Ausfall einer dieser Arten zuordnen. Um auf seltene oder [nicht behebbare Ausfälle][unrecoverable] vorbereitet zu sein, stets [Backups][backup] des etcd-Clusters erstellen.

## Ausfall einer Minderheit der Follower {#minor-followers-failure}

Wenn Follower ausfallen, aber weniger als die Hälfte aller Clustermitglieder ausgefallen ist und der Leader weiterhin verfügbar bleibt, kann der etcd-Cluster weiterhin Anfragen annehmen und ohne größere Beeinträchtigung weiterarbeiten. Beispielsweise beeinträchtigt der Ausfall von zwei Followern den Betrieb eines etcd-Clusters mit fünf Mitgliedern nicht. Clients verlieren jedoch die Verbindung zu den ausgefallenen Mitgliedern. Clientbibliotheken sollten solche Unterbrechungen bei Leseanfragen vor Benutzern verbergen, indem sie automatisch Verbindungen zu anderen Mitgliedern herstellen. Betreiber sollten damit rechnen, dass diese neuen Verbindungen die Systemlast auf den anderen Mitgliedern erhöhen.

## Ausfall des Leaders {#leader-failure}

Wenn ein Leader ausfällt, wählt der etcd-Cluster automatisch einen neuen Leader. Diese Wahl erfolgt nicht unmittelbar nach dem Ausfall. Sie dauert ungefähr so lange wie das Wahlzeitlimit, da die Ausfallerkennung auf Zeitüberschreitungen beruht.

Während der Leaderwahl kann der Cluster keine Schreiboperationen verarbeiten. Schreibanfragen, die während der Wahl eingehen, werden zur Verarbeitung in eine Warteschlange gestellt, bis ein neuer Leader gewählt ist.

Schreiboperationen, die bereits an den alten Leader gesendet, aber noch nicht festgeschrieben wurden, können verloren gehen. Der neue Leader kann alle nicht festgeschriebenen Einträge des vorherigen Leaders überschreiben. Aus Benutzersicht können einige Schreibanfragen nach der Wahl eines neuen Leaders mit einer Zeitüberschreitung enden. Bereits festgeschriebene Schreiboperationen gehen jedoch niemals verloren.

Der neue Leader verlängert automatisch die Zeitlimits aller Leases. Dieser Mechanismus stellt sicher, dass eine Lease nicht vor Ablauf ihrer gewährten TTL verfällt, selbst wenn sie vom alten Leader gewährt wurde.

## Ausfall einer Mehrheit {#majority-failure}

Wenn die Mehrheit der Clustermitglieder ausfällt, fällt der etcd-Cluster aus und kann keine weiteren Schreiboperationen annehmen.

Der etcd-Cluster kann sich erst von einem Mehrheitsausfall erholen, wenn die Mehrheit der Mitglieder wieder verfügbar ist. Kann eine Mehrheit der Mitglieder nicht wieder online gehen, muss der Betreiber eine [Disaster Recovery][unrecoverable] einleiten, um den Cluster wiederherzustellen.

Sobald eine Mehrheit der Mitglieder wieder funktioniert, wählt der etcd-Cluster automatisch einen neuen Leader und kehrt in einen intakten Zustand zurück. Der neue Leader verlängert automatisch die Zeitlimits aller Leases. Dieser Mechanismus stellt sicher, dass keine Lease wegen serverseitiger Nichtverfügbarkeit abläuft.

## Netzwerkpartition {#network-partition}

Eine Netzwerkpartition ähnelt dem Ausfall einer Minderheit der Follower oder dem Ausfall des Leaders. Sie teilt den etcd-Cluster in zwei Teile: einen mit einer Mehrheit und einen mit einer Minderheit der Mitglieder. Die Mehrheitsseite bildet den verfügbaren Cluster; die Minderheitsseite ist nicht verfügbar. In etcd gibt es kein „Split Brain“, da Clustermitglieder ausdrücklich hinzugefügt oder entfernt werden und jede solche Änderung von der aktuellen Mehrheit der Mitglieder genehmigt wird.

Befindet sich der Leader auf der Mehrheitsseite, entspricht der Ausfall aus Sicht der Mehrheit dem Ausfall einer Minderheit der Follower. Befindet er sich auf der Minderheitsseite, entspricht dies einem Leaderausfall. Der Leader auf der Minderheitsseite tritt zurück, und die Mehrheitsseite wählt einen neuen Leader.

Sobald die Netzwerkpartition aufgehoben ist, erkennt die Minderheitsseite automatisch den Leader der Mehrheitsseite an und stellt ihren Zustand wieder her.

## Ausfall während der Initialisierung {#failure-during-bootstrapping}

Die Initialisierung eines Clusters ist nur erfolgreich, wenn alle erforderlichen Mitglieder erfolgreich starten. Tritt während der Initialisierung ein Fehler auf, die Datenverzeichnisse aller Mitglieder entfernen und den Cluster mit einem neuen cluster-token oder einem neuen Discovery-Token erneut initialisieren.

Natürlich lässt sich ein während der Initialisierung ausgefallener Cluster ebenso wie ein laufender Cluster wiederherstellen. Da aber keine Daten wiederherzustellen sind, kostet seine Wiederherstellung fast immer mehr Zeit und Ressourcen als die Initialisierung eines neuen Clusters.

[backup]: /de/docs/etcd/op-guide/maintenance/#snapshot-backup
[unrecoverable]: /de/docs/etcd/op-guide/recovery/
