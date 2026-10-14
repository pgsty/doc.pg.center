---
title: "Standby-Cluster"
weight: 80
icon: fa-solid fa-clone
description: "Einrichtung und Verhalten eines Standby-Clusters sowie Replikation von einem entfernten Primärserver."
module: [PATRONI]
categories: [Aufgabe]
upstream_link: "https://patroni.readthedocs.io/en/latest/standby_cluster.html"
---

<a id="standby_cluster"></a>
Patroni unterstützt mit der Funktion „Standby-Cluster“ auch kaskadierende Replikation in ein entferntes Rechenzentrum (eine Region). Ein solcher Cluster besteht aus:

- einem „Standby-Leader“, der sich weitgehend wie ein normaler Cluster-Leader verhält, aber von einem entfernten Knoten repliziert.
- kaskadierenden Replikaten, die vom Standby-Leader replizieren.

Der Standby-Leader hält und aktualisiert eine Leader-Sperre im DCS. Läuft diese Sperre ab, wählen die kaskadierenden Replikate einen anderen Leader aus den Standbys.

Zwischen dem Standby-Cluster und dem Primärcluster, von dem er repliziert, besteht keine weitere Beziehung. Insbesondere dürfen sie nicht denselben DCS-Scope verwenden, wenn sie denselben DCS nutzen. Außer den Replikationsinformationen wissen sie nichts voneinander. Der Standby-Cluster erscheint außerdem nicht in der Ausgabe von [patronictl_list](/de/patroni/patronictl#patronictl_list) oder [patronictl_topology](/de/patroni/patronictl#patronictl_topology) auf dem Primärcluster.

Für mehr Flexibilität lassen sich die Methoden zur Erstellung eines Replikats und zur Wiederherstellung von WAL-Einträgen im „Standby-Modus“ über den Schlüssel [create_replica_methods](/de/patroni/replica_bootstrap#custom_replica_creation) im Abschnitt [standby_cluster](/de/patroni/standby_cluster#standby_cluster) festlegen. Davon getrennt ist die Replikaterstellung, wenn der Cluster abgekoppelt ist und als normaler Cluster arbeitet: Sie wird durch `create_replica_methods` im Abschnitt `postgresql` gesteuert. Sowohl die „Standby“- als auch die „normalen“ `create_replica_methods` verweisen auf Schlüssel im Abschnitt `postgresql`.

Zur Konfiguration eines solchen Clusters muss in der Patroni-Konfiguration der Abschnitt [standby_cluster](/de/patroni/standby_cluster#standby_cluster) angegeben werden:

```yaml
bootstrap:
    dcs:
        standby_cluster:
            host: 1.2.3.4
            port: 5432
            primary_slot_name: patroni
            create_replica_methods:
            - basebackup
```

Diese Optionen werden nur einmal während der Cluster-Initialisierung angewendet. Danach können sie ausschließlich über den DCS geändert werden.

Patroni erwartet `postgresql.conf` oder `postgresql.conf.backup` im PGDATA des entfernten Primärservers und startet nicht, wenn diese Datei nach einem Basisbackup fehlt. Liegt die `postgresql.conf` des entfernten Primärservers an einem anderen Ort, muss sie eigenständig nach PGDATA kopiert werden.

Werden Replikationsslots im Standby-Cluster verwendet, muss der entsprechende Replikationsslot auch im Primärcluster angelegt werden. Die Implementierung des Standby-Clusters erledigt dies nicht automatisch. Mit der Funktion für permanente Replikationsslots von Patroni kann im Primärcluster ein Replikationsslot verwaltet werden, dessen Name `primary_slot_name` entspricht – oder dessen Standardwert, falls `primary_slot_name` nicht angegeben ist.

Bietet der entfernte Standort keinen einzelnen Endpunkt für die Verbindung zum Primärserver, können alle Hosts des Quellclusters im Abschnitt `standby_cluster.host` aufgelistet werden. Enthält `standby_cluster.host` mehrere durch Kommas getrennte Hosts, führt Patroni Folgendes aus:

- Es ergänzt `primary_conninfo` auf dem Standby-Leader um `target_session_attrs=read-write`.
- Es verwendet `target_session_attrs=read-write`, wenn geprüft wird, ob `pg_rewind` erforderlich ist, oder wenn `pg_rewind` auf allen Knoten des Standby-Clusters ausgeführt wird.
- Damit `pg_rewind` erfolgreich funktioniert, muss der Cluster mit `data page checksums` (Option `--data-checksums` für `initdb`) initialisiert worden sein und/oder `wal_log_hints` muss auf `on` gesetzt sein. Andernfalls funktioniert `pg_rewind` nicht ordnungsgemäß.

Ein Standby-Cluster kann auch von einem anderen Standby-Cluster oder einem Standby-Mitglied des Primärclusters replizieren. Dafür muss im Abschnitt `standby_cluster.host` genau ein Host angegeben werden. Dabei ist jedoch zu beachten, dass `pg_rewind` in diesem Fall auf dem Standby-Cluster fehlschlägt.

> [!WARNING]
> Mitgliedsnamen (das Feld `name` in der Patroni-Konfiguration jedes Knotens) müssen im Primärcluster und in allen mit ihm verbundenen Standby-Clustern eindeutig sein.
>
> Patroni setzt `synchronous_standby_names` auf dem Primärserver anhand der Mitgliedsnamen. Diese werden zugleich als `application_name` der jeweiligen Replikationsverbindung in `pg_stat_replication` verwendet. Hat ein Knoten eines Standby-Clusters denselben Namen wie ein Mitglied des Primärclusters, sieht PostgreSQL zwei Verbindungen mit identischen `application_name`-Werten. Durch diese Mehrdeutigkeit kann PostgreSQL die Anforderung an synchrone Replikation mit der Verbindung des Standby-Clusters statt mit der des vorgesehenen Primärcluster-Mitglieds erfüllen. PostgreSQL bestätigt Transaktionen dadurch vorzeitig als synchron festgeschrieben, obwohl sie auf dem richtigen Standby noch nicht dauerhaft gespeichert sind.
>
> Dieser Fehler bleibt unbemerkt: Die Replikation läuft weiter und es werden keine Fehler protokolliert, doch der Cluster arbeitet faktisch ohne gültigen synchronen Standby. Fällt der Primärserver aus, droht Datenverlust.
