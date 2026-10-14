---
title: "Replikationsmodi"
weight: 70
icon: fa-solid fa-share-nodes
description: "Von Patroni verwaltete asynchrone und synchrone Replikationsmodi."
module: [PATRONI]
categories: [Konzept]
upstream_link: "https://patroni.readthedocs.io/en/latest/replication_modes.html"
---

<a id="replication_modes"></a>
Patroni verwendet die Streaming-Replikation von PostgreSQL. Weitere Informationen dazu stehen in der [Postgres-Dokumentation](http://www.postgresql.org/docs/current/static/warm-standby.html#STREAMING-REPLICATION). Standardmäßig konfiguriert Patroni PostgreSQL für asynchrone Replikation. Die Wahl des Replikationsverfahrens hängt von den geschäftlichen Anforderungen ab. Sowohl asynchrone als auch synchrone Replikation sowie andere HA-Lösungen sollten geprüft werden, um die passende Lösung zu bestimmen.

--------

## Dauerhaftigkeit im asynchronen Modus {#asynchronous-mode-durability}

Im asynchronen Modus darf der Cluster einige bereits festgeschriebene Transaktionen verlieren, um die Verfügbarkeit zu gewährleisten. Fällt der Primärserver aus oder wird er aus einem anderen Grund unerreichbar, stuft Patroni automatisch einen hinreichend funktionsfähigen Standby zum Primärserver hoch. Alle Transaktionen, die noch nicht auf diesen Standby repliziert wurden, verbleiben auf dem bisherigen Primärserver in einer „abgezweigten Zeitleiste“ und sind praktisch nicht wiederherstellbar[^1].

Die Menge der potenziell verlorenen Transaktionen wird durch den Parameter `maximum_lag_on_failover` gesteuert. Da die Position im Transaktionsprotokoll des Primärservers nicht in Echtzeit erfasst wird, ist der tatsächliche Datenverlust bei einem Failover im schlimmsten Fall auf `maximum_lag_on_failover` Bytes des Transaktionsprotokolls zuzüglich der in den letzten `ttl` Sekunden geschriebenen Daten begrenzt (im Durchschnitt `loop_wait`/2 Sekunden). Im normalen, stabilen Betrieb liegt die Replikationsverzögerung jedoch typischerweise deutlich unter einer Sekunde.

Standardmäßig berücksichtigt Patroni bei Leader-Wahlen nicht die aktuelle Zeitleiste der Replikate, was in manchen Fällen unerwünscht sein kann. Wird `check_timeline` auf `true` gesetzt, kann ein Knoten mit einer älteren Zeitleiste als der zuletzt bekannten Cluster-Zeitleiste oder mit einer nicht bestimmbaren Zeitleiste nicht neuer Leader werden.

--------

## Synchrone Replikation von PostgreSQL {#postgresql-synchronous-replication}

Die [synchrone Replikation](http://www.postgresql.org/docs/current/static/warm-standby.html#SYNCHRONOUS-REPLICATION) von Postgres kann mit Patroni verwendet werden. Sie gewährleistet die Konsistenz im Cluster, indem sie bestätigt, dass Schreibvorgänge auf einem Sekundärserver gespeichert wurden, bevor dem verbundenen Client Erfolg gemeldet wird. Der Preis dafür sind höhere Latenzen und ein geringerer Schreibdurchsatz. Dieser Durchsatz wird von der Netzwerkleistung beeinflusst.

In gehosteten Rechenzentrumsumgebungen (wie AWS, Rackspace oder jedem Netzwerk außerhalb der eigenen Kontrolle) erhöht synchrone Replikation die Schwankungen der Schreibleistung erheblich. Kann der Leader seine Follower nicht mehr erreichen, wird er faktisch schreibgeschützt.

Für einen einfachen Test der synchronen Replikation folgende Zeilen zum Abschnitt `parameters` der YAML-Konfigurationsdateien hinzufügen:

```yaml
synchronous_commit: "on"
synchronous_standby_names: "*"
```

Bei synchroner PostgreSQL-Replikation mindestens drei Postgres-Datenknoten verwenden, um die Schreibverfügbarkeit beim Ausfall eines Hosts zu gewährleisten.

Synchrone PostgreSQL-Replikation garantiert nicht unter allen Umständen, dass keine Transaktionen verloren gehen. Fallen der Primärserver und der derzeit als synchrones Replikat dienende Sekundärserver gleichzeitig aus, wird ein dritter Knoten hochgestuft, der möglicherweise nicht alle Transaktionen enthält.

<a id="synchronous_mode"></a>

--------

## Synchroner Modus {#synchronous-mode}

Darf eine Anwendung keine festgeschriebenen Transaktionen verlieren, kann der [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) von Patroni aktiviert werden. Bei aktiviertem [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) stuft Patroni einen Standby nur dann hoch, wenn sicher ist, dass er alle Transaktionen enthält, deren erfolgreiches Festschreiben dem Client möglicherweise bereits bestätigt wurde[^2]. Das bedeutet, dass das System für Schreibzugriffe unverfügbar sein kann, obwohl einige Server erreichbar sind. Systemadministratoren können weiterhin manuelle Failover-Befehle verwenden, um einen Standby hochzustufen, auch wenn dadurch Transaktionen verloren gehen.

Das Aktivieren von [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) garantiert nicht unter allen Umständen, dass Commits auf mehreren Knoten dauerhaft gespeichert werden. Ist kein geeigneter Standby verfügbar, nimmt der Primärserver weiterhin Schreibvorgänge an, garantiert aber deren Replikation nicht. Fällt der Primärserver in diesem Modus aus, wird kein Standby hochgestuft. Sobald der bisherige Primärhost zurückkehrt, wird er automatisch hochgestuft, sofern kein Systemadministrator ein manuelles Failover durchgeführt hat. Durch dieses Verhalten ist der synchrone Modus auch für Cluster mit 2 Knoten geeignet.

Ist [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) aktiviert, der strikte Modus deaktiviert und stürzt der einzige synchrone Standby ab, blockieren Commits, bis der nächste Patroni-Durchlauf den Primärserver in den Einzelbetrieb versetzt (Schreibverzögerung im schlimmsten Fall `ttl` Sekunden, im Durchschnitt `loop_wait`/2 Sekunden). Ein manuelles Herunterfahren oder Neustarten eines Standbys unterbricht die Commit-Verarbeitung nicht. Vor dem Herunterfahren von PostgreSQL signalisiert der Standby dem Primärserver, ihn von seiner Aufgabe als synchroner Standby zu entbinden.

Muss unbedingt gewährleistet sein, dass jeder Schreibvorgang auf mindestens zwei Knoten dauerhaft gespeichert wird, zusätzlich zu [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) die Option `synchronous_mode_strict` aktivieren. Dieser Parameter verhindert, dass Patroni die synchrone Replikation auf dem Primärserver deaktiviert, wenn keine Kandidaten für einen synchronen Standby verfügbar sind. Synchrone Commits blockieren, bis ein synchrones Replikat verfügbar ist; Transaktionen mit den `synchronous_commit`-Werten `off` oder `local` umgehen diese Wartezeit.

Im prioritätsbasierten synchronen Modus (`synchronous_mode: on`) setzt Patroni 4.1.5 bei aktiviertem striktem Modus `synchronous_standby_names` auf `*`, wenn kein geeigneter synchroner Standby verfügbar ist, und gibt die Warnung `"No standbys available!"` aus. Commits warten dadurch weiterhin auf einen synchronen Standby. Der Platzhalter beschränkt Bestätigungen nicht auf die zuvor in `/sync` gespeicherten Mitgliedsnamen.

Ist das Tag `nosync` auf true gesetzt, schließt Patroni den Standby von seiner Auswahl synchroner Standbys aus. Dies wird für Standbys mit langsamer Netzwerkverbindung empfohlen, die als synchrone Standbys die Leistung beeinträchtigen würden. Das Tag `nostream` auf true zu setzen, hat dieselbe Wirkung.

Der synchrone Modus lässt sich mit `patronictl edit-config` oder über die REST-Schnittstelle von Patroni ein- und ausschalten. Eine Anleitung steht unter [Dynamische Konfiguration](/de/patroni/config/dynamic#dynamic).

Hinweis: Aufgrund der Implementierung der synchronen Replikation in PostgreSQL können auch mit `synchronous_mode_strict` Transaktionen verloren gehen. Wird ein PostgreSQL-Backend abgebrochen, während es auf die Bestätigung der Replikation wartet (durch ein Abbruchpaket infolge einer clientseitigen Zeitüberschreitung oder durch einen Backend-Ausfall), werden die Transaktionsänderungen für andere Backends sichtbar. Diese Änderungen sind noch nicht repliziert und können bei der Hochstufung eines Standbys verloren gehen.

--------

## Synchroner Replikationsfaktor {#synchronous-replication-factor}

Mit dem Parameter `synchronous_node_count` verwaltet Patroni die Anzahl synchroner Standby-Datenbanken. Sein Standardwert ist `1`. Ist [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) auf `off` gesetzt, hat er keine Wirkung. Bei aktiviertem Modus steuert Patroni die genaue Anzahl synchroner Standby-Datenbanken anhand von `synchronous_node_count` und passt beim Hinzukommen und Ausscheiden von Mitgliedern sowohl den Zustand im DCS als auch `synchronous_standby_names` in PostgreSQL an. Sind weniger geeignete Knoten verfügbar, kann Patroni weniger synchrone Standbys als angefordert verwenden; im strikten Quorum-Modus warten Commits jedoch weiterhin auf die konfigurierte Anzahl von Standby-Bestätigungen.

--------

## Maximaler Rückstand eines synchronen Knotens {#maximum-lag-on-synchronous-node}

Standardmäßig hält Patroni an Knoten fest, die laut Sicht `pg_stat_replication` als `synchronous` gelten, selbst wenn andere Knoten weiter fortgeschritten sind. Dadurch wird die Anzahl der Änderungen an `synchronous_standby_names` minimiert. Dieses Verhalten lässt sich mit `maximum_lag_on_syncnode` ändern. Der Parameter steuert, wie weit ein Replikat zurückliegen darf, um noch als „synchron“ zu gelten.

Bei mehr als einem Standby verwendet Patroni die höchste Replikat-LSN, andernfalls die aktuelle WAL-LSN des Leaders. Der Standardwert ist `-1`; bei einem Wert von `0` oder weniger unternimmt Patroni nichts, um einen beeinträchtigten synchronen Standby auszutauschen. Den Wert ausreichend hoch wählen, damit Patroni synchrone Standbys bei hohem Transaktionsaufkommen nicht zu häufig austauscht.

--------

## Implementierung des synchronen Modus {#synchronous-mode-implementation}

Im synchronen Modus verwaltet Patroni den Synchronisationszustand im DCS (Schlüssel `/sync`). Er enthält den zuletzt bekannten Primärserver und die aktuellen synchronen Standby-Datenbanken. Für Aktualisierungen gelten strenge Reihenfolgevorgaben, um folgende Invarianten zu gewährleisten:

- Ein Knoten muss immer dann als letzter Leader gekennzeichnet sein, wenn er Schreibtransaktionen annehmen kann. Ein Absturz von Patroni oder ein nicht herunterfahrendes PostgreSQL kann diese Invariante verletzen.
- Solange ein Knoten im DCS-Schlüssel `/sync` als synchroner Standby veröffentlicht ist, muss er in PostgreSQL als synchroner Standby eingestellt sein.
- Ein Knoten, der weder Leader noch aktueller synchroner Standby ist, darf sich nicht automatisch hochstufen.

Bei einer nicht leeren Menge synchroner Standbys weist Patroni `synchronous_standby_names` einen oder mehrere synchrone Standby-Knoten gemäß `synchronous_node_count` zu.

Bei jedem Durchlauf der HA-Schleife bewertet Patroni die Auswahl der synchronen Standby-Knoten neu. Sind die aktuell aufgeführten synchronen Standby-Knoten verbunden und haben sie nicht darum gebeten, ihren synchronen Status aufzuheben, bleiben sie ausgewählt. Andernfalls werden die für synchrone Replikation verfügbaren Clustermitglieder ausgewählt, die bei der Replikation am weitesten fortgeschritten sind.

### Beispiel: {#example}

#### Schlüssel `/config` im DCS {#config-key-in-dcs}

```yaml
synchronous_mode: on
synchronous_node_count: 2
...
```

#### Schlüssel `/sync` im DCS {#sync-key-in-dcs}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2"
}
```

#### postgresql.conf {#postgresqlconf}

```ini
synchronous_standby_names = 'FIRST 2 (node1,node2)'
```

Im obigen Beispiel gelten nur `node1` und `node2` als nachweislich synchron. Nur sie dürfen automatisch hochgestuft werden, wenn der Primärserver (`node0`) ausfällt.

<a id="quorum_mode"></a>

--------

## Quorum-Commit-Modus {#quorum-commit-mode}

Ab PostgreSQL v10 unterstützt Patroni Quorum-basierte synchrone Replikation.

In diesem Modus verwaltet Patroni den Synchronisationszustand im DCS. Er enthält den zuletzt bekannten Primärserver, die für ein Quorum erforderliche Knotenzahl und die derzeit zur Quorum-Abstimmung berechtigten Knoten. Im stabilen Zustand stimmen der Leader und alle synchronen Standbys ab. Bei Aktualisierungen gelten strenge Reihenfolgevorgaben bezüglich Knotenhochstufung und `synchronous_standby_names`. So enthält zu jedem Zeitpunkt jede Teilmenge der Stimmberechtigten, die ein Quorum erreichen kann, mindestens einen Knoten mit dem letzten erfolgreichen Commit.

Bei jedem Durchlauf der HA-Schleife bewertet Patroni anhand der Knotenverfügbarkeit und der gewünschten Clusterkonfiguration die Auswahl synchroner Standbys sowie das Quorum neu. In PostgreSQL-Versionen nach 9.6 werden alle geeigneten Knoten als synchrone Standbys hinzugefügt, sobald ihre Replikation den Leader eingeholt hat.

Quorum-Commit hilft, die Latenzen im ungünstigsten Fall selbst im Normalbetrieb zu verringern, da andere Standbys eine höhere Replikationslatenz zu einem einzelnen Standby ausgleichen können.

Der Quorum-basierte synchrone Modus lässt sich aktivieren, indem [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) mit `patronictl edit-config` oder über die REST-Schnittstelle von Patroni auf `quorum` gesetzt wird. Eine Anleitung steht unter [Dynamische Konfiguration](/de/patroni/config/dynamic#dynamic).

Andere Parameter wie `synchronous_node_count`, `maximum_lag_on_syncnode` und `synchronous_mode_strict` funktionieren weiterhin wie bei `synchronous_mode=on`.

Ist im Quorum-Commit-Modus die Menge synchroner Standbys leer und erfordert der strikte Modus Bestätigungen von `N` Standbys, setzt Patroni 4.1.5 `synchronous_standby_names` auf `ANY N (*)`.

### Beispiel: {#example-1}

#### Schlüssel `/config` im DCS {#config-key-in-dcs-1}

```yaml
synchronous_mode: quorum
synchronous_node_count: 2
...
```

#### Schlüssel `/sync` im DCS {#sync-key-in-dcs-1}

```json
{
    "leader": "node0",
    "sync_standby": "node1,node2,node3",
    "quorum": 1
}
```

#### postgresql.conf {#postgresqlconf-1}

```ini
synchronous_standby_names = 'ANY 2 (node1,node2,node3)'
```

Fällt der Primärserver (`node0`) im obigen Beispiel aus, haben zwei der Knoten `node1`, `node2`, `node3` die letzte Transaktion empfangen; es ist jedoch unbekannt, welche. Um festzustellen, ob `node1` die letzte Transaktion empfangen hat, muss seine LSN mit der LSN **mindestens** eines Knotens (`quorum=1` im Schlüssel `/sync`) aus `node2` und `node3` verglichen werden. Liegt `node1` gegenüber mindestens einem von ihnen nicht zurück, lässt sich garantieren, dass bei der Hochstufung von `node1` kein für Benutzer sichtbarer Datenverlust auftritt.

[^1]: Die Daten sind noch vorhanden, ihre Wiederherstellung erfordert aber manuelle Arbeit durch Spezialisten für Datenrettung. Darf Patroni mit `use_pg_rewind` zurücksetzen, wird die abgezweigte Zeitleiste automatisch gelöscht, um den ausgefallenen Primärserver wieder in den Cluster aufzunehmen. Damit `use_pg_rewind` richtig funktioniert, muss der Cluster mit `data page checksums` (Option `--data-checksums` für `initdb`) initialisiert worden sein und/oder `wal_log_hints` muss auf `on` gesetzt sein.

[^2]: Clients können das Verhalten je Transaktion mit der PostgreSQL-Einstellung `synchronous_commit` ändern. Transaktionen mit den `synchronous_commit`-Werten `off` und `local` können bei einem Failover verloren gehen, werden aber nicht durch Replikationsverzögerungen blockiert.
