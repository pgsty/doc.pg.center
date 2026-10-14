---
title: "Cluster-Verwaltung pausieren und fortsetzen"
linkTitle: "Cluster pausieren/fortsetzen"
weight: 100
icon: fa-solid fa-stopwatch
description: "Verhalten beim Pausieren und Fortsetzen der Patroni-Cluster-Verwaltung."
module: [PATRONI]
categories: [Aufgabe]
upstream_link: "https://patroni.readthedocs.io/en/latest/pause.html"
---

<a id="pause"></a>

--------

## Ziel {#the-goal}

Unter bestimmten Umständen muss Patroni die Verwaltung des Clusters vorübergehend aussetzen, den Clusterzustand aber weiterhin im DCS speichern. Mögliche Anwendungsfälle sind seltene Eingriffe wie Hauptversionsupgrades oder die Wiederherstellung nach Datenbeschädigungen. Dabei werden Knoten häufig aus Gründen gestartet und gestoppt, die Patroni nicht kennt. Einige Knoten werden möglicherweise sogar vorübergehend hochgestuft, wodurch die Annahme verletzt wird, dass nur ein Primärserver läuft. Patroni muss sich daher vom laufenden Cluster „abkoppeln“ können und eine Entsprechung zum Wartungsmodus von Pacemaker bereitstellen.

--------

## Implementierung {#the-implementation}

Im pausierten Modus ändert Patroni den Zustand von PostgreSQL nicht, mit folgenden Ausnahmen:

- Für jeden Knoten wird der Mitgliedsschlüssel im DCS mit den aktuellen Clusterinformationen aktualisiert. Dazu führt Patroni auf einem laufenden Mitgliedsknoten schreibgeschützte Abfragen aus.
- Für den Postgres-Primärserver mit der Leader-Sperre aktualisiert Patroni diese Sperre. Ist der Knoten mit der Leader-Sperre kein Primärserver mehr (d. h. nach einer manuellen Herabstufung), gibt Patroni die Sperre frei, statt den Knoten wieder hochzustufen.
- Manuelle, nicht zeitgesteuerte Neustarts, Failover/Switchover und Neuinitialisierungen sind erlaubt. Zeitgesteuerte Aktionen sind nicht erlaubt. Ein manuelles Switchover ist nur erlaubt, wenn der Zielknoten angegeben wird.
- Erkennt Patroni „parallele“ Primärserver, gibt es eine Warnung aus, stuft den Primärserver ohne Leader-Sperre jedoch nicht herab.
- Gibt es im Cluster keine Leader-Sperre, erlangt der laufende Primärserver die Sperre. Gibt es mehrere Primärserver, gewinnt der erste, der die Sperre erlangt. Gibt es überhaupt keinen Primärserver, versucht Patroni nicht, Replikate hochzustufen. Von dieser Regel gibt es eine Ausnahme: Fehlt die Leader-Sperre, weil sich der bisherige Primärserver infolge einer manuellen Hochstufung selbst herabgestuft hat, darf nur der in der Hochstufungsanfrage genannte Kandidat die Leader-Sperre übernehmen. Wird die neue Leader-Sperre vergeben (d. h. nach der manuellen Hochstufung eines Replikats), stellt Patroni sicher, dass Replikate, die zuvor vom bisherigen Leader gestreamt haben, auf den neuen wechseln.
- Ist Postgres gestoppt, versucht Patroni nicht, es zu starten. Wird Patroni gestoppt, versucht es nicht, die von ihm verwaltete Postgres-Instanz zu stoppen.
- Patroni versucht nicht, Replikationsslots zu entfernen, die weder ein anderes Clustermitglied repräsentieren noch in der Konfiguration der permanenten Slots aufgeführt sind.

--------

## Benutzerhandbuch {#user-guide}

[patronictl](/de/patroni/patronictl#patronictl) unterstützt die Befehle [pause](/de/patroni/patronictl#patronictl_pause) und [resume](/de/patroni/patronictl#patronictl_resume).

Es kann auch eine `PATCH /config`-Anfrage mit `{"pause": true/false/null}` an die REST-API von Patroni gesendet werden, um den Schlüssel `{namespace}/{cluster}/config` im DCS zu aktualisieren.
