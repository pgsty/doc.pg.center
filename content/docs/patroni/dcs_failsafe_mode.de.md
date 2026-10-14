---
title: "DCS-Failsafe-Modus"
weight: 110
icon: fa-solid fa-shield-halved
description: "Verhalten, Voraussetzungen und betriebliche Einschränkungen des DCS-Failsafe-Modus."
module: [PATRONI]
categories: [Konzept]
aliases: [/patroni/dcs_failsafe_mode/]
upstream_link: "https://patroni.readthedocs.io/en/latest/dcs_failsafe_mode.html"
---

<a id="dcs_failsafe_mode"></a>

--------

## Das Problem {#the-problem}

Patroni stützt sich bei der Leader-Wahl und der Erkennung von Netzwerkpartitionen stark auf den verteilten Konfigurationsspeicher (DCS). Ein Knoten darf Postgres also nur dann als Primärserver betreiben, wenn er die Leader-Sperre im DCS aktualisieren kann. Schlägt diese Aktualisierung fehl, wird Postgres sofort herabgestuft und schreibgeschützt gestartet. Wie wahrscheinlich dieses „Problem“ auftritt, hängt vom verwendeten DCS ab. Bei etcd, das ausschließlich für Patroni genutzt wird, ist die Wahrscheinlichkeit beispielsweise nahezu null; bei der K8s-API (mit etcd als Speicher) kann es häufiger auftreten.

--------

## Gründe für die aktuelle Implementierung {#reasons-for-the-current-implementation}

Eine Aktualisierung der Leader-Sperre kann hauptsächlich aus zwei Gründen fehlschlagen:

1.  Netzwerkpartitionierung
2.  Ausfall des DCS

Im Allgemeinen kann ein einzelner Knoten diese beiden Fälle nicht unterscheiden. Deshalb nimmt Patroni den schlimmsten Fall an: eine Netzwerkpartitionierung. Bei einem partitionierten Netzwerk können andere Knoten des Patroni-Clusters die Leader-Sperre erfolgreich übernehmen und Postgres zum Primärserver hochstufen. Um Split-Brain zu vermeiden, wird der bisherige Primärserver herabgestuft, bevor die Leader-Sperre abläuft.

--------

## DCS-Failsafe-Modus {#dcs-failsafe-mode}

Dafür wird die neue spezielle Option `failsafe_mode` eingeführt. Sie kann nur über die globale [dynamische Konfiguration](/de/docs/patroni/config/dynamic#dynamic) aktiviert werden, die im DCS-Schlüssel `/config` gespeichert ist. Wenn der Failsafe-Modus aktiviert ist und die Aktualisierung der Leader-Sperre im DCS aus einem anderen Grund als einer Abweichung bei Version, Wert oder Index fehlschlägt, kann Postgres weiter als Primärserver laufen, sofern es alle bekannten Clustermitglieder über die REST-API von Patroni erreichen kann.

--------

## Implementierungsdetails {#low-level-implementation-details}

- Im DCS wird ein neuer, dauerhafter Schlüssel namens `/failsafe` eingeführt.
- Der Schlüssel `/failsafe` enthält alle zu einem bestimmten Zeitpunkt bekannten Mitglieder des jeweiligen Patroni-Clusters.
- Der aktuelle Leader verwaltet den Schlüssel `/failsafe`.
- Ein Mitglied darf nur dann an der Leader-Wahl teilnehmen und neuer Leader werden, wenn es im Schlüssel `/failsafe` enthalten ist.
- Besteht der Cluster aus einem einzigen Knoten, enthält der Schlüssel `/failsafe` ein einziges Mitglied.
- Bei einem DCS-Ausfall kontaktiert der bestehende Primärserver alle im Schlüssel `/failsafe` aufgeführten Mitglieder über die REST-API `POST /failsafe`. Er kann weiter als Primärserver laufen, wenn alle Replikate dies bestätigen.
- Antwortet eines der Mitglieder nicht, wird der Primärserver herabgestuft.
- Replikate werten eingehende REST-API-Anfragen an `POST /failsafe` als Zeichen dafür, dass der Primärserver noch aktiv ist. Diese Information wird für `ttl` Sekunden zwischengespeichert.

--------

## Häufig gestellte Fragen {#faq}

- Warum MUSS der aktuelle Primärserver ALLE anderen Mitglieder erreichen? Können wir uns hier nicht auf ein Quorum verlassen?

  Das ist eine gute Frage! Das Problem ist, dass DCS und Patroni unterschiedliche Sichtweisen auf das Quorum haben können. DCS-Knoten müssen gleichmäßig über die Verfügbarkeitszonen verteilt sein; für Patroni gibt es keine solche Regel und vor allem keinen Mechanismus, um sie einzuführen und durchzusetzen. Befindet sich die Mehrheit der Patroni-Knoten einschließlich des Primärservers im unterlegenen Teil des partitionierten Netzwerks und die Minderheit im siegreichen Teil, muss der Primärserver herabgestuft werden. Nur durch die Prüfung ALLER anderen Mitglieder lässt sich diese Situation erkennen.

- Was geschieht, wenn ein Knoten oder Pod beendet wird, während der DCS ausgefallen ist?

  Ist der DCS nicht erreichbar, wird in jedem Durchlauf der Heartbeat-Schleife (alle `loop_wait` Sekunden) geprüft, ob ALLE anderen Clustermitglieder erreichbar sind. Wird ein Pod oder Knoten beendet, schlägt diese Prüfung fehl und Postgres wird in den schreibgeschützten Zustand herabgestuft. Es kehrt erst dann zum normalen Betrieb zurück, wenn der DCS wiederhergestellt ist.

- Was geschieht, wenn alle Mitglieder des Patroni-Clusters verloren gehen, während der DCS ausgefallen ist?

  Patroni kann so konfiguriert werden, dass es ein neues Replikat aus einem Backup erstellt, auch wenn der Cluster keinen Leader hat. Ist das neue Mitglied jedoch nicht im Schlüssel `/failsafe` enthalten, kann es weder die Leader-Sperre übernehmen noch hochgestuft werden.

- Was geschieht, wenn der Primärserver den Zugriff auf den DCS verliert, die Replikate aber nicht?

  Der Primärserver führt den Failsafe-Code aus und kontaktiert alle bekannten Replikate. Diese werten die Information als Zeichen dafür, dass der Primärserver aktiv ist, und starten auch dann keine Leader-Wahl, wenn die Leader-Sperre im DCS abgelaufen ist.

- Wie wird der Failsafe-Modus aktiviert?

  Vor der Aktivierung von `failsafe_mode` sicherstellen, dass die Patroni-Version auf allen Mitgliedern aktuell ist. Anschließend kann entweder die [REST-API](/de/docs/patroni/rest_api#rest_api) `PATCH /config` oder [patronictl edit-config -s failsafe_mode=true](/de/docs/patroni/patronictl#patronictl_edit_config_parameters) verwendet werden.
