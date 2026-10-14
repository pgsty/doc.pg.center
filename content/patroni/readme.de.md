---
title: "Einführung"
weight: 10
icon: fa-solid fa-circle-info
description: "Einführung in Patroni, Schnelleinstieg und grundlegende Hochverfügbarkeitskonzepte."
module: [PATRONI]
categories: [Konzept]
upstream_link: "https://patroni.readthedocs.io/en/latest/README.html"
---

<a id="readme"></a>
Patroni ist eine Vorlage für PostgreSQL-Lösungen zur Hochverfügbarkeit (HA) auf Basis von Python. Es entstand als Fork von [Governor](https://github.com/compose/governor), einem Projekt von Compose, und enthält zahlreiche neue Funktionen.

Weitere Hintergrundinformationen:

- [PostgreSQL-HA mit Kubernetes und Patroni](https://www.youtube.com/watch?v=iruaCgeG7qs), Vortrag von Josh Berkus auf der KubeCon 2016 (Video)
- [Beitrag im Zalando-Tech-Blog vom Februar 2016](https://engineering.zalando.com/posts/2016/02/zalandos-patroni-a-template-for-high-availability-postgresql.html)

--------

## Entwicklungsstand {#development-status}

Patroni wird aktiv weiterentwickelt und nimmt Beiträge entgegen. Weitere Einzelheiten stehen im Abschnitt [Mitwirken](/de/patroni/contributing_guidelines#contributing_guidelines) weiter unten.

Informationen zu neuen Versionen veröffentlichen wir [hier](/de/patroni/releases#releases).

--------

## Technische Voraussetzungen und Installation {#technical-requirementsinstallation}

Anleitungen zur Installation und zum Upgrade von Patroni auf verschiedenen Plattformen stehen [hier](/de/patroni/installation#installation).

<a id="running_configuring"></a>

--------

## Anzahl der PostgreSQL-Knoten planen {#planning-the-number-of-postgresql-nodes}

Patroni-/PostgreSQL-Knoten sind von den DCS-Knoten unabhängig (außer wenn Patroni RAFT selbst implementiert). Daher gibt es keine Mindestanzahl an Knoten. Ein Cluster aus einem Primärserver und einem Standby kann problemlos betrieben werden. Weitere Standby-Knoten können später hinzugefügt werden.

**Cluster mit 2 Knoten** (Primärserver + Standby) sind üblich und bieten automatisches Failover mit Hochverfügbarkeit. Während eines Failovers besteht vorübergehend keine Redundanz, bis der ausgefallene Knoten wieder beitritt.

**DCS-Anforderungen**: Der DCS (etcd, ZooKeeper, Consul) muss für zuverlässigen Konsens und Fehlertoleranz mit **3 oder 5 Knoten** betrieben werden. Ein einzelner DCS-Cluster kann Informationen für Hunderte oder Tausende Patroni-Cluster speichern, die unterschiedliche namespace/scope-Kombinationen verwenden.

--------

## Ausführen und Konfigurieren {#running-and-configuring}

Der folgende Abschnitt setzt voraus, dass das Patroni-Repository von <https://github.com/patroni/patroni> geklont wurde. Insbesondere werden die Beispielkonfigurationen `postgres0.yml` und `postgres1.yml` benötigt. Wurde Patroni mit pip installiert, können diese Dateien aus dem Git-Repository bezogen werden; `./patroni.py` ist dann unten durch den Befehl `patroni` zu ersetzen.

Die folgenden Befehle verwenden die etcd-v2-API und erfordern eine etcd-Version mit Unterstützung für `--enable-v2`, etwa etcd 3.5. Bei etcd 3.6 oder neuer stattdessen die `etcd3`-Konfiguration von Patroni verwenden, da [etcd 3.6 die Unterstützung der v2-API entfernt hat](https://etcd.io/docs/v3.6/upgrades/upgrade_3_6/).

Zum Einstieg die folgenden Befehle in verschiedenen Terminals ausführen:

    > etcd --data-dir=data/etcd --enable-v2=true
    > ./patroni.py postgres0.yml
    > ./patroni.py postgres1.yml

Daraufhin startet ein hochverfügbarer Cluster. Verschiedene Einstellungen in den YAML-Dateien ausprobieren, um ihre Auswirkungen auf das Clusterverhalten zu beobachten. Einzelne Komponenten beenden, um das Verhalten des Systems zu testen.

Weitere Dateien `postgres*.yml` hinzufügen, um einen noch größeren Cluster zu erstellen.

Patroni stellt eine [HAProxy](https://www.haproxy.org/)-Konfiguration bereit, die der Anwendung einen einzelnen Endpunkt für Verbindungen zum Cluster-Leader bietet. Zur Einrichtung folgende Befehle ausführen:

    > haproxy -f haproxy.cfg

    > psql --host 127.0.0.1 --port 5000 postgres

--------

## YAML-Konfiguration {#yaml-configuration}

Ausführliche Informationen zu den Einstellungen für etcd, Consul und ZooKeeper stehen [hier](/de/patroni/config/yaml#yaml). Ein Beispiel enthält [postgres0.yml](https://github.com/patroni/patroni/blob/master/postgres0.yml).

--------

## Konfiguration über Umgebungsvariablen {#environment-configuration}

Ausführliche Informationen zum Festlegen und Überschreiben von Einstellungen über Umgebungsvariablen stehen [hier](/de/patroni/config/env#env).

--------

## Replikationsmöglichkeiten {#replication-choices}

Patroni verwendet die Streaming-Replikation von Postgres, die standardmäßig asynchron arbeitet. In der asynchronen Replikationskonfiguration von Patroni lässt sich `maximum_lag_on_failover` setzen. Diese Einstellung verhindert die Hochstufung eines Followers bei einem Failover, wenn er mehr als die festgelegte Anzahl Bytes hinter dem Leader liegt. Ihr Wert sollte je nach geschäftlichen Anforderungen erhöht oder verringert werden. Für stärkere Garantien zur Dauerhaftigkeit kann auch synchrone Replikation verwendet werden. Einzelheiten stehen in der [Dokumentation zu Replikationsmodi](/de/patroni/replication_modes#replication_modes).

--------

## Anwendungen sollten keine Superuser verwenden {#applications-should-not-use-superusers}

Für Verbindungen aus Anwendungen immer einen Benutzer ohne Superuser-Rechte verwenden. Patroni benötigt Datenbankzugriff, um ordnungsgemäß zu funktionieren. Verwendet eine Anwendung einen Superuser, kann sie möglicherweise den gesamten Verbindungspool belegen, einschließlich der über `superuser_reserved_connections` für Superuser reservierten Verbindungen. Kann Patroni wegen eines vollen Verbindungspools nicht auf den Primärserver zugreifen, führt dies zu unerwünschtem Verhalten.

--------

## Die HA-Lösung testen {#testing-your-ha-solution}

Das Testen einer HA-Lösung ist zeitaufwendig und umfasst viele Einflussgrößen. Dies gilt besonders für eine plattformübergreifende Anwendung. Dafür wird ein geschulter Systemadministrator oder Berater benötigt. Die Dokumentation kann dies nicht im Detail abdecken.

Folgende Teile der Infrastruktur sollten auf jeden Fall getestet werden:

- Netzwerk (sowohl das dem System vorgelagerte Netzwerk als auch die NICs \[physisch oder virtuell\] selbst)
- Datenträger-IO
- Dateilimits (nofile unter Linux)
- RAM. Auch bei deaktiviertem oomkiller kann fehlender Arbeitsspeicher Probleme verursachen.
- CPU
- Ressourcenkonkurrenz bei der Virtualisierung (Überbelegung des Hypervisors)
- Sämtliche cgroup-Beschränkungen (wahrscheinlich im Zusammenhang mit den obigen Punkten)
- `kill -9` für einen beliebigen postgres-Prozess (außer postmaster!). Dies simuliert einen Segmentation Fault recht gut.

Ein postmaster-Prozess sollte dagegen nicht mit `kill -9` beendet werden, da das Beenden des Prozesses allein die zugrunde liegenden Bedingungen eines Ressourcenmangels oder anderer Infrastrukturfehler nicht nachbildet. Besteht die Sorge, dass die Infrastruktur unsicher ist und ein Angreifer `kill -9` ausführen könnte, kann kein HA-Verfahren das beheben. Der Angreifer würde den Prozess einfach erneut beenden oder auf andere Weise Schaden anrichten.
