---
title: "Patroni 4.1.5 Dokumentation"
linkTitle: Patroni
weight: 10
icon: fa-solid fa-heart-pulse
description: "Überblick über die Patroni-Dokumentation zur Hochverfügbarkeit von PostgreSQL."
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PATRONI]
categories: [Konzept]
aliases: [/patroni/]
upstream_source: patroni
upstream_link: "https://patroni.readthedocs.io/en/latest/index.html"
cascade:
  upstream_source: patroni
  type: docs
  module: [PATRONI]
---

> [!WARNING]
> Betrieb von Patroni auf **Systemen mit begrenztem Arbeitsspeicher und Python 3.11+**

Wenn Sie Patroni auf einem System mit strengen Speichergrenzen betreiben, beispielsweise mit `vm.overcommit_memory=2` (für PostgreSQL empfohlen), und Python 3.11 oder neuer verwenden, kann unerwartetes Verhalten auftreten:

- Patroni scheint ordnungsgemäß zu funktionieren
- PostgreSQL läuft weiter
- Die **REST API von Patroni reagiert nicht mehr**
- Das Betriebssystem meldet, dass Patroni auf dem REST API-Port lauscht
- Die Patroni-Protokolle erscheinen normal; einmalig können jedoch folgende Meldungen auftreten: `Exception ignored in thread started by: <object repr() failed>`, `MemoryError`
- Die Kernel-Protokolle können Meldungen wie `not enough memory for the allocation` enthalten

Dieses Verhalten wird durch einen [Fehler in Python 3.11+](https://github.com/python/cpython/issues/140746) verursacht. Bei strengen Speichergrenzen kann der Start eines neuen Threads auf unbestimmte Zeit hängen bleiben, wenn nicht genügend freier Arbeitsspeicher verfügbar ist.

## Empfohlene Lösung {#recommended-solution}

Neuere Patroni-Versionen (4.1.1+, 4.0.8+) verringern die Auswirkungen dieses Problems, indem sie alle erforderlichen Threads früh beim Start erzeugen, bevor das System unter Speicherdruck gerät.

## Weitere Empfehlungen (Linux, glibc) {#additional-recommendations-linux-glibc}

Beim Betrieb mit `vm.overcommit_memory=2` (für PostgreSQL empfohlen) empfehlen wir außerdem, Patroni mit den folgenden Umgebungsvariablen zu starten:

- `MALLOC_ARENA_MAX=1` - verringert den von glibc für Anwendungen mit mehreren Threads reservierten virtuellen Speicher
- `PG_MALLOC_ARENA_MAX=` - setzt den Wert von `MALLOC_ARENA_MAX` für PostgreSQL-Prozesse zurück, die Patroni startet.

Zusätzlich können Sie folgende Patroni-Konfigurationsparameter anpassen:

- `thread_stack_size` - Stackgröße der von Patroni gestarteten Threads. Ein niedrigerer Wert verringert den Speicherbedarf des Patroni-Prozesses. Der von Patroni vorgegebene Standardwert ist `512kB`. Erhöhen Sie `thread_stack_size`, wenn Patroni aufgrund von Stackproblemen abstürzt; andernfalls reicht der Standardwert aus.
- `thread_pool_size` - Größe des Threadpools, den Patroni für asynchrone Aufgaben und die REST API-Kommunikation mit anderen Mitgliedern bei der Leader-Wahl oder bei Failsafe-Prüfungen verwendet. Der Standardwert ist `5` und reicht für Cluster mit drei Knoten aus.
- `restapi.thread_pool_size` - Größe des Threadpools zur Bearbeitung von REST API-Anfragen. Der Standardwert ist `5` und erlaubt bis zu fünf parallele REST API-Anfragen. Anfragen mit SQL-Abfragen werden jedoch praktisch nacheinander verarbeitet, da nur eine Datenbankverbindung verwendet wird. Eine Erhöhung dieses Wertes bringt daher üblicherweise keinen Vorteil.

--------

Patroni ist eine Vorlage für PostgreSQL-Lösungen zur Hochverfügbarkeit (HA) auf Basis von Python. Für eine möglichst breite Einsetzbarkeit unterstützt Patroni verschiedene verteilte Konfigurationsspeicher wie [ZooKeeper](https://zookeeper.apache.org/), [etcd](https://github.com/coreos/etcd), [Consul](https://github.com/hashicorp/consul) oder [Kubernetes](https://kubernetes.io). Datenbankentwickler, DBAs, DevOps-Fachleute und SREs, die PostgreSQL mit HA schnell in Rechenzentren oder anderswo bereitstellen möchten, finden darin hoffentlich ein hilfreiches Werkzeug.

Wir nennen Patroni eine „Vorlage“, weil es keineswegs ein universelles oder sofort einsatzbereites Replikationssystem ist. Es hat seine Besonderheiten und Einschränkungen. Setzen Sie es mit Bedacht ein. Es gibt viele Möglichkeiten, PostgreSQL hochverfügbar zu betreiben; eine Übersicht bietet die [PostgreSQL-Dokumentation](https://wiki.postgresql.org/wiki/Replication,_Clustering,_and_Connection_Pooling).

Derzeit unterstützte PostgreSQL-Versionen: 9.3 bis 18.

**Hinweis für Citus-Anwender**: Ab Version 3.0 integriert sich Patroni gut mit der Postgres-Datenbankerweiterung [Citus](https://github.com/citusdata/citus). Weitere Informationen zur gemeinsamen Nutzung der Patroni-Hochverfügbarkeit mit einem verteilten Citus-Cluster finden Sie auf der [Seite zur Citus-Unterstützung](/de/docs/patroni/citus#citus) in der Patroni-Dokumentation.

**Hinweis für Kubernetes-Anwender**: Patroni kann direkt auf Kubernetes laufen. Lesen Sie dazu das Kapitel [Kubernetes](/de/docs/patroni/kubernetes#kubernetes) der Patroni-Dokumentation.

<img src="/img/docs/patroni/patroni-logo.png" width="128" height="128" alt="Bild" />
