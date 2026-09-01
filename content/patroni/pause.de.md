---
title: "Pausen/fortsetzen-Modus für den_Cluster"
linkTitle: "Pausieren/Wiederherstellen des Clusters"
weight: 100
icon: fa-solid fa-stopwatch
description: "Verhaltensweisen der Anhalten und Wiederherstellen im Patroni-Clustermanagement."
module: [PATRONI]
categories: [Aufgabe]
aliases: [/docs/patroni/pause/]
upstream_link: "https://patroni.readthedocs.io/en/latest/pause.html"
---

<a id="pause"></a>

--------

## Das Ziel {#the-goal}
Unter bestimmten Umständen muss Patroni vorübergehend die Verwaltung des Clusters aufgeben, während der Clusterstatus in DCS erhalten bleibt. Mögliche Anwendungsfälle sind ungewöhnliche Aktivitäten im Cluster, wie z. B. größere Versions-Upgrades oder die Wiederherstellung von Daten. Während dieser Aktivitäten werden die Knoten oft gestartet und gestoppt, aus Gründen, die Patroni nicht kennt. Einige Knoten können sogar vorübergehend als primäre Knoten fungieren, was die Annahme verletzt, dass nur ein primärer Knoten aktiv ist. Daher muss Patroni in der Lage sein, sich vom laufenden Cluster zu trennen und eine ähnliche Funktion wie der Wartigungsmodus in Pacemaker zu implementieren.

--------

## Die Implementierung {#the-implementation}
Wenn Patroni im angehaltenen Modus läuft, ändert es den Zustand von PostgreSQL nicht, außer in folgenden Fällen:

- Für jeden Knoten wird der Member-Schlüssel in DCS mit den aktuellen Informationen über den Cluster aktualisiert. Dadurch führt Patroni dazu, nur Leseabfragen auf einem Member-Knoten auszuführen, wenn dieser ausgeführt wird.
- Für den primären Postgres-Server mit dem Leader-Lock aktualisiert Patroni den Lock. Wenn der Knoten mit dem Leader-Lock nicht mehr der primäre Server ist (d. h. er wird manuell abgewickelt), gibt Patroni den Lock frei, anstatt den Knoten wieder aufzuwerten.
- Manuelle, nicht geplante Neustarts, manuelle, nicht geplante Failover/Umschaltung und Reinitialisierung sind erlaubt. Geplante Aktionen sind nicht erlaubt. Eine manuelle Umschaltung ist nur dann erlaubt, wenn der zu schaltende Knoten angegeben ist.
- Wenn Patroni "parallele" primäre Server erkennt, gibt es eine Warnmeldung aus, aber es wird der primäre Server ohne Leader-Lock nicht abgewickelt.
- Wenn kein Leader-Lock im Cluster vorhanden ist, erhält der laufende Primär den Lock. Wenn es mehr als einen Primär-Knoten gibt, gewinnt der erste Primär, der den Lock erhält. Wenn es keine Primär-Knoten gibt, versucht Patroni, keine Replik zu befördern. Es gibt eine Ausnahme: Wenn kein Leader-Lock vorhanden ist, weil der alte Primär sich manuell befördert hat, kann nur der im Anforderung zur Beförderung genannte Knoten den Leader-Lock erhalten. Wenn der neue Leader-Lock gewährt wird (d. h. nach manueller Beförderung einer Replik), stellt Patroni sicher, dass die Replik, die zuvor vom vorherigen Leader verwendet wurden, auf den neuen umgeschaltet werden.
- Wenn Postgres gestoppt wird, versucht Patroni, es nicht zu starten. Wenn Patroni gestoppt wird, versucht es nicht, die Postgres-Instanz zu stoppen, die es verwaltet.
- Patroni versucht nicht, Replikations-Slots zu entfernen, die nicht den anderen Cluster-Mitgliedern entsprechen oder nicht in der Konfiguration der permanenten Slots aufgeführt sind.

--------

## Benutzerhandbuch {#user-guide}
[patronictl](/de/patroni/patronictl#patronictl) unterstützt die Befehle [pause](/de/patroni/patronictl#patronictl_pause) und [resume](/de/patroni/patronictl#patronictl_resume).

Es ist auch möglich, eine Anfrage an den Schlüssel `{namespace}/{cluster}/config` mit dem Wert `{"pause": true/false/null}` auszugeben, die den Typ `PATCH` hat.
