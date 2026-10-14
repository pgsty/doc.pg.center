---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "Befehlsreferenz zu Konfiguration, Syntax und Unterbefehlen von patronictl."
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/patronictl.html"
---

<a id="patronictl"></a>
Patroni bietet eine Befehlszeilenschnittstelle namens [patronictl](/de/patroni/patronictl#patronictl), die hauptsächlich mit der REST API von Patroni und dem DCS interagiert. Sie erleichtert die Durchführung von Vorgängen im Cluster und lässt sich sowohl manuell als auch in Skripten einfach verwenden.

<a id="patronictl_configuration"></a>

--------

## Konfiguration {#configuration}

[patronictl](/de/patroni/patronictl#patronictl) verwendet 3 Abschnitte der Konfiguration:

- **ctl**: Authentifizierung gegenüber der REST API von Patroni und Prüfung der Serveridentität. Weitere Einzelheiten finden sich unter [ctl-Einstellungen](/de/patroni/config/yaml#patronictl_settings);
- **restapi**: Authentifizierung gegenüber der REST API von Patroni und Prüfung der Serveridentität. Wird nur verwendet, wenn die `ctl`-Konfiguration nicht ausreicht. [patronictl](/de/patroni/patronictl#patronictl) verwendet hauptsächlich den Abschnitt `restapi.authentication` (wenn `ctl.authentication` fehlt) und die Einstellung `restapi.cafile` (wenn `ctl.cacert` fehlt). Weitere Einzelheiten finden sich unter [REST-API-Einstellungen](/de/patroni/config/yaml#restapi_settings);
- DCS (z. B. **etcd**): Verbindung und Authentifizierung gegenüber dem von Patroni verwendeten DCS.

Diese Konfigurationsoptionen können entweder aus Umgebungsvariablen oder aus einer Konfigurationsdatei stammen. Die obigen Abschnitte unter [Konfiguration über Umgebungsvariablen](/de/patroni/config/env#env) bzw. [YAML-Konfiguration](/de/patroni/config/yaml#yaml) erläutern, wie die Optionen über Umgebungsvariablen oder eine Konfigurationsdatei gesetzt werden können.

Die Verwendung von Umgebungsvariablen ist unkompliziert. Patronictl liest die Umgebungsvariablen und verwendet ihre Werte.

Bei Verwendung einer Konfigurationsdatei gibt es verschiedene Möglichkeiten, [patronictl](/de/patroni/patronictl#patronictl) die gewünschte Datei mitzuteilen. Standardmäßig versucht [patronictl](/de/patroni/patronictl#patronictl), eine Konfigurationsdatei namens `patronictl.yaml` zu laden. Je nach System wird sie unter einem der folgenden Pfade erwartet:

- Mac OS X: `~/Library/Application Support/patroni`
- Mac OS X (POSIX): `~/.patroni`
- Unix: `~/.config/patroni`
- Unix (POSIX): `~/.patroni`
- Windows (mit Roaming): `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (ohne Roaming): `C:\Users\<user>\AppData\Local\patroni`

Dieses Verhalten lässt sich auf folgende Weise überschreiben:

- Die Umgebungsvariable `PATRONICTL_CONFIG_FILE` auf den Pfad einer eigenen Konfigurationsdatei setzen;
- Dem Befehlszeilenargument `-c` / `--config-file` von [patronictl](/de/patroni/patronictl#patronictl) den Pfad einer eigenen Konfigurationsdatei übergeben.

> [!NOTE]
> Wenn [patronictl](/de/patroni/patronictl#patronictl) auf demselben Host wie der Daemon `patroni` ausgeführt wird, kann dieselbe Konfigurationsdatei verwendet werden, sofern sie alle von [patronictl](/de/patroni/patronictl#patronictl) benötigten Konfigurationsabschnitte enthält.

<a id="patronictl_usage"></a>

--------

## Verwendung {#usage}

[patronictl](/de/patroni/patronictl#patronictl) bietet mehrere praktische Operationen. Dieser Abschnitt beschreibt sie im Einzelnen.

Vor der Beschreibung der einzelnen Unterbefehle von [patronictl](/de/patroni/patronictl#patronictl) folgt eine Übersicht der Befehlszeilenargumente von [patronictl](/de/patroni/patronictl#patronictl) selbst:

`-c` / `--config-file`  
Wie bereits erläutert, wird damit der Pfad zu einer Konfigurationsdatei für [patronictl](/de/patroni/patronictl#patronictl) angegeben.

`-d` / `--dcs-url` / `--dcs`  
Eine Verbindungszeichenfolge für den von Patroni verwendeten DCS angeben.

Dieses Argument kann die DCS- und `namespace`-Einstellungen aus der Konfiguration von [patronictl](/de/patroni/patronictl#patronictl) überschreiben oder sie festlegen, falls sie dort fehlen.

Der Wert sollte das Format `DCS://HOST:PORT/NAMESPACE` haben, z. B. `etcd3://localhost:2379/service`, um eine Verbindung zu etcd v3 auf `localhost` herzustellen, wobei der Patroni-Cluster im Namensraum `service` gespeichert ist. Jeder im Argument fehlende Teil wird durch den Wert aus der Konfiguration oder den Standardwert ersetzt.

`-k` / `--insecure`  
Flag zum Überspringen der Prüfung des SSL-Zertifikats des REST-API-Servers.

Dies ist das Aufrufschema für einen Befehl von [patronictl](/de/patroni/patronictl#patronictl):

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> Für das Aufrufschema gilt folgende Syntax:
>
> - Optionen in eckigen Klammern sind optional;
> - Optionen in geschweiften Klammern bedeuten, dass eine Option aus der Menge gewählt wird;
> - Optionen mit `[, ... ]` können mehrfach angegeben werden;
> - Angaben in Großbuchstaben stehen für Literale, denen ein Wert zugewiesen werden sollte.
>
> Dieselbe Syntax wird in den folgenden Unterabschnitten bei der Beschreibung der Unterbefehle von [patronictl](/de/patroni/patronictl#patronictl) verwendet. Die dortigen Aufrufschemata der Unterbefehle ersetzen jeweils `SUBCOMMAND` im obigen Aufrufschema.

Die folgenden Unterabschnitte beschreiben alle von [patronictl](/de/patroni/patronictl#patronictl) implementierten Befehle. Für die Beispiele werden die Konfigurationsdateien aus dem GitHub-Repository von Patroni verwendet (`postgres0.yml`, `postgres1.yml` und `postgres2.yml`).

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster {#patronictl-demote-cluster}

<a id="patronictl_demote_cluster_synopsis"></a>

#### Aufrufschema {#synopsis}

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### Beschreibung {#description}

`patronictl demote-cluster` wandelt einen regulären Patroni-Cluster in einen [Standby-Cluster](/de/patroni/standby_cluster#standby_cluster) um.

Der Befehl ergänzt die dynamische Konfiguration um einen Abschnitt `standby_cluster`, der aus den angegebenen Verbindungsoptionen für den entfernten Primärserver erstellt wird. Anschließend wartet er, bis der Leader als Standby-Leader läuft. Vor der Konfigurationsänderung gibt er die aktuelle Cluster-Topologie aus. Eine Bestätigung fordert er an, sofern `--force` nicht verwendet wird.

Mindestens eine der Optionen `--host`, `--port` oder `--restore-command` muss angegeben werden.

<a id="patronictl_demote_cluster_parameters"></a>

#### Parameter {#parameters}

`CLUSTER_NAME`: Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--host`: Adresse des entfernten Knotens.

`--port`: Port des entfernten Knotens.

`--restore-command`: Befehl zur Wiederherstellung von WAL-Einträgen vom entfernten Primärserver.

`--primary-slot-name`: Name des Replikationsslots auf dem entfernten Knoten, der für die Replikation verwendet werden soll.

`--force`: Flag zum Überspringen der Bestätigungsabfragen beim Herabstufen des Clusters.

Nützlich für Skripte.

<a id="patronictl_demote_cluster_examples"></a>

#### Beispiele {#examples}

Den Cluster zu einem Standby-Cluster herabstufen, der einem entfernten Primärserver-Endpunkt folgt:

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn {#patronictl-dsn}

<a id="patronictl_dsn_synopsis"></a>

#### Aufrufschema {#synopsis-1}

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### Beschreibung {#description-1}

`patronictl dsn` ermittelt die Verbindungszeichenfolge für ein Mitglied des Patroni-Clusters.

Wenn mehrere Mitglieder den Parametern dieses Befehls entsprechen, wird eines davon ausgewählt, wobei der Primärserver Vorrang hat.

<a id="patronictl_dsn_parameters"></a>

#### Parameter {#parameters-1}

`CLUSTER_NAME`: Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`-r` / `--role`  
Ein Mitglied mit der angegebenen Rolle auswählen.

Die Rolle kann einen der folgenden Werte haben:

- `leader`: der Leader eines regulären Patroni-Clusters oder eines Patroni-Standby-Clusters; oder
- `primary`: der Leader eines regulären Patroni-Clusters; oder
- `standby-leader`: der Leader eines Patroni-Standby-Clusters; oder
- `replica`: ein Replikat eines Patroni-Clusters; oder
- `standby`: entspricht `replica`; oder
- `any`: beliebige Rolle. Entspricht dem Weglassen dieses Parameters; oder

`-m` / `--member`  
Ein Mitglied des Clusters mit dem angegebenen Namen auswählen.

`MEMBER_NAME` ist der Name des Mitglieds.

`--group`  
Ein Mitglied auswählen, das zur angegebenen Citus-Gruppe gehört.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

<a id="patronictl_dsn_examples"></a>

#### Beispiele {#examples-1}

DSN des Primärservers abrufen:

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

DSN des Knotens namens `postgresql1` abrufen:

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config {#patronictl-edit-config}

<a id="patronictl_edit_config_synopsis"></a>

#### Aufrufschema {#synopsis-2}

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### Beschreibung {#description-2}

`patronictl edit-config` ändert die dynamische Konfiguration des Clusters und aktualisiert damit den DCS.

> [!NOTE]
> Beim Aufruf über ein TTY versucht der Befehl, einen Diff der dynamischen Konfiguration mit einem Pager anzuzeigen. Standardmäßig versucht er, `less` oder `more` zu verwenden. Für einen anderen Pager die Umgebungsvariable `PAGER` auf das gewünschte Programm setzen.

<a id="patronictl_edit_config_parameters"></a>

#### Parameter {#parameters-2}

`CLUSTER_NAME`: Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Die dynamische Konfiguration der angegebenen Citus-Gruppe ändern.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `citus.group` zu lesen, sofern sie vorhanden ist.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-q` / `--quiet`  
Flag zum Überspringen der Anzeige des Konfigurations-Diffs.

`-s` / `--set`  
Eine bestimmte dynamische Konfigurationsoption auf den angegebenen Wert setzen.

`CONFIG` ist der Pfad der dynamischen Konfiguration im YAML-Baum, dessen Ebenen durch `.` verbunden sind.

`VALUE` ist der Wert für `CONFIG`. Bei `null` wird `CONFIG` aus der dynamischen Konfiguration entfernt.

`-p` / `--pg`  
Eine bestimmte dynamische Postgres-Konfigurationsoption auf den angegebenen Wert setzen.

Dies ist im Wesentlichen eine Kurzform für `-s` / `--set`, bei der `CONFIG` das Präfix `postgresql.parameters.` erhält.

`PG_CONFIG` ist der Name der zu setzenden Postgres-Konfigurationsoption.

`PG_VALUE` ist der Wert für `PG_CONFIG`. Bei `null` wird `PG_CONFIG` aus der dynamischen Konfiguration entfernt.

`--apply`  
Die dynamische Konfiguration aus der angegebenen Datei anwenden.

Dies entspricht der Angabe mehrerer Optionen `-s` / `--set`, einer für jede Konfigurationsoption aus `CONFIG_FILE`.

`CONFIG_FILE` ist der Pfad zu einer Datei mit der anzuwendenden dynamischen Konfiguration im YAML-Format. Zum Lesen aus `stdin` den Wert `-` verwenden.

`--replace`  
Die dynamische Konfiguration im DCS durch die dynamische Konfiguration aus der angegebenen Datei ersetzen.

`CONFIG_FILE` ist der Pfad zu einer Datei mit der neuen dynamischen Konfiguration im YAML-Format, die wirksam werden soll. Zum Lesen aus `stdin` den Wert `-` verwenden.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen beim Ändern der dynamischen Konfiguration.

Nützlich für Skripte.

<a id="patronictl_edit_config_examples"></a>

#### Beispiele {#examples-2}

Den Postgres-GUC `max_connections` ändern:

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

Die Einstellungen `loop_wait` und `ttl` ändern:

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

Die Einstellung `maximum_lag_on_failover` aus der dynamischen Konfiguration entfernen:

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

<a id="patronictl_failover"></a>

### patronictl failover {#patronictl-failover}

<a id="patronictl_failover_synopsis"></a>

#### Aufrufschema {#synopsis-3}

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_failover_description"></a>

#### Beschreibung {#description-3}

`patronictl failover` führt ein manuelles Failover im Cluster durch.

Der Befehl ist für nicht funktionsfähige Cluster vorgesehen, z. B. wenn:

- kein Leader vorhanden ist; oder
- in einem synchronen Cluster kein synchroner Standby verfügbar ist.

Er ermöglicht bei aktiviertem synchronem Modus auch ein Failover zu einem asynchronen Knoten.

> [!NOTE]
> `patronictl failover` kann auch in einem funktionsfähigen Cluster ausgeführt werden. Für diese Fälle wird jedoch `patronictl switchover` empfohlen.

> [!WARNING]
> Das Auslösen eines Failovers kann zu Datenverlust führen, je nachdem, wie aktuell das hochgestufte Replikat im Vergleich zum Primärserver ist.

<a id="patronictl_failover_parameters"></a>

#### Parameter {#parameters-3}

`CLUSTER_NAME`: Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Ein Failover in der angegebenen Citus-Gruppe durchführen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`--candidate`  
Der Knoten, der beim Failover hochgestuft werden soll.

`CANDIDATE_NAME` ist der Name des hochzustufenden Knotens.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen bei der Durchführung des Failovers.

Nützlich für Skripte.

<a id="patronictl_failover_examples"></a>

#### Beispiele {#examples-3}

Ein Failover zum Knoten `postgresql2` durchführen:

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_flush"></a>

### patronictl flush {#patronictl-flush}

<a id="patronictl_flush_synopsis"></a>

#### Aufrufschema {#synopsis-4}

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_flush_description"></a>

#### Beschreibung {#description-4}

`patronictl flush` verwirft geplante Ereignisse, sofern vorhanden.

<a id="patronictl_flush_parameters"></a>

#### Parameter {#parameters-4}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

`MEMBER_NAME`  
Geplante Ereignisse für die angegebenen Patroni-Mitglieder verwerfen.

Es können mehrere Mitglieder angegeben werden. Ohne Angabe von Mitgliedern werden alle berücksichtigt.

> [!NOTE]
> Wird nur beim Verwerfen geplanter Neustarts verwendet.

`restart`  
Geplante Neustarts verwerfen.

`switchover`  
Geplanten Switchover verwerfen.

`--group`  
Geplante Ereignisse der angegebenen Citus-Gruppe verwerfen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-r` / `--role`  
Geplante Ereignisse für Mitglieder mit der angegebenen Rolle verwerfen.

Die Rolle kann einen der folgenden Werte haben:

- `leader`: der Leader eines regulären Patroni-Clusters oder eines Patroni-Standby-Clusters; oder
- `primary`: der Leader eines regulären Patroni-Clusters; oder
- `standby-leader`: der Leader eines Patroni-Standby-Clusters; oder
- `replica`: ein Replikat eines Patroni-Clusters; oder
- `standby`: entspricht `replica`; oder
- `any`: beliebige Rolle. Entspricht dem Weglassen dieses Parameters.

> [!NOTE]
> Wird nur beim Verwerfen geplanter Neustarts verwendet.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen beim Verwerfen geplanter Ereignisse.

Nützlich für Skripte.

<a id="patronictl_flush_examples"></a>

#### Beispiele {#examples-4}

Einen geplanten Switchover verwerfen:

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

Den geplanten Neustart aller Standby-Knoten verwerfen:

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

Den geplanten Neustart der Knoten `postgresql0` und `postgresql1` verwerfen:

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_history"></a>

### patronictl history {#patronictl-history}

<a id="patronictl_history_synopsis"></a>

#### Aufrufschema {#synopsis-5}

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_history_description"></a>

#### Beschreibung {#description-5}

`patronictl history` zeigt die Historie der Failover- und Switchover-Ereignisse des Clusters, sofern vorhanden.

Die Ausgabe enthält folgende Informationen:

`TL`  
Postgres-Timeline, auf der das Ereignis auftrat.

`LSN`  
Postgres-LSN, an der das Ereignis auftrat.

`Reason`  
Grund aus der Postgres-Datei `.history`.

`Timestamp`  
Zeitpunkt des Ereignisses.

`New Leader`  
Patroni-Mitglied, das bei diesem Ereignis hochgestuft wurde.

<a id="patronictl_history_parameters"></a>

#### Parameter {#parameters-5}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Die Ereignishistorie der angegebenen Citus-Gruppe anzeigen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `citus.group` zu lesen, sofern sie vorhanden ist.

`-f` / `--format`  
Formatierung der Ereignisliste in der Ausgabe.

Das Format kann einen der folgenden Werte haben:

- `pretty`: gibt die Historie als formatierte Tabelle aus; oder
- `tsv`: gibt die Historie tabellarisch aus, mit durch `\t` getrennten Spalten; oder
- `json`: gibt die Historie im JSON-Format aus; oder
- `yaml`: gibt die Historie im YAML-Format aus.

Der Standardwert ist `pretty`.

<a id="patronictl_history_examples"></a>

#### Beispiele {#examples-5}

Die Ereignishistorie anzeigen:

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

Die Ereignishistorie im YAML-Format anzeigen:

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_list"></a>

### patronictl list {#patronictl-list}

<a id="patronictl_list_synopsis"></a>

#### Aufrufschema {#synopsis-6}

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_list_description"></a>

#### Beschreibung {#description-6}

`patronictl list` zeigt Informationen zum Patroni-Cluster und seinen Mitgliedern.

Die Ausgabe enthält folgende Informationen:

`Cluster`  
Name des Patroni-Clusters.

`Member`  
Name des Patroni-Mitglieds.

`Host`  
Host, auf dem sich das Mitglied befindet.

`Role`  
Aktuelle Rolle des Mitglieds.

Mögliche Werte sind:

- `Leader`: der aktuelle Leader eines regulären Patroni-Clusters; oder
- `Standby Leader`: der aktuelle Leader eines Patroni-Standby-Clusters; oder
- `Sync Standby`: ein synchroner Standby eines Patroni-Clusters mit aktiviertem synchronem Modus; oder
- `Replica`: ein regulärer Standby eines Patroni-Clusters.

`State`  
Aktueller Zustand von Postgres im Patroni-Mitglied.

Einige Beispiele für mögliche Zustände:

- `running`: wenn Postgres derzeit läuft;
- `streaming`: bei einem Replikat, wenn Postgres derzeit WAL per Streaming vom Primärserver empfängt;
- `in archive recovery`: bei einem Replikat, wenn Postgres derzeit WAL aus dem Archiv abruft;
- `stopped`: wenn Postgres heruntergefahren wurde;
- `crashed`: wenn Postgres abgestürzt ist.

`TL`  
Aktuelle Postgres-Timeline im Patroni-Mitglied.

`Receive LSN`  
Die letzte Write-Ahead-Log-Position, die das Mitglied per Streaming-Replikation empfangen und auf den Datenträger synchronisiert hat (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Replikationsrückstand zwischen der Position `Receive LSN` des Mitglieds und seiner Replikationsquelle in MB.

`Replay LSN`  
Die letzte Write-Ahead-Log-Position, die bei der Recovery des Mitglieds wiedergegeben wurde (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Replikationsrückstand zwischen der Position `Replay LSN` des Mitglieds und seiner Replikationsquelle in MB.

Darüber hinaus kann die Ausgabe folgende Informationen enthalten:

`System identifier`  
Postgres-Systemkennung.

> [!NOTE]
> Wird im Tabellenkopf angezeigt.
>
> Wird nur beim Ausgabeformat `pretty` angezeigt.

`Group`  
ID der Citus-Gruppe.

> [!NOTE]
> Wird im Tabellenkopf angezeigt.
>
> Wird nur bei einem Citus-Cluster angezeigt.

`Pending restart`  
`*` zeigt an, dass der Knoten einen Neustart benötigt, damit bestimmte Postgres-Konfigurationseinstellungen wirksam werden. Ein leerer Wert zeigt an, dass der Knoten keinen Neustart benötigt.

> [!NOTE]
> Wird als Attribut des Mitglieds angezeigt.
>
> Wird angezeigt, wenn:
>
> - die Ausgabe im Format `pretty` oder `tsv` erfolgt und die erweiterte Ausgabe aktiviert ist; oder
> - der Knoten einen Neustart benötigt.

`Scheduled restart`  
Zeitstempel des geplanten Neustarts der vom Patroni-Mitglied verwalteten Postgres-Instanz. Ein leerer Wert zeigt an, dass für das Mitglied kein Neustart geplant ist.

> [!NOTE]
> Wird als Attribut des Mitglieds angezeigt.
>
> Wird angezeigt, wenn:
>
> - die Ausgabe im Format `pretty` oder `tsv` erfolgt und die erweiterte Ausgabe aktiviert ist; oder
> - für den Knoten ein Neustart geplant ist.

`Tags`  
Enthält die für das Patroni-Mitglied gesetzten Tags. Ein leerer Wert zeigt an, dass entweder keine Tags konfiguriert wurden oder diese auf die Standardwerte gesetzt sind.

> [!NOTE]
> Wird als Attribut des Mitglieds angezeigt.
>
> Wird angezeigt, wenn:
>
> - die Ausgabe im Format `pretty` oder `tsv` erfolgt und die erweiterte Ausgabe aktiviert ist; oder
> - der Knoten benutzerdefinierte Tags oder Standard-Tags mit abweichenden Werten hat.

`Scheduled switchover`  
Zeitstempel des geplanten Switchovers für den Patroni-Cluster, sofern vorhanden.

> [!NOTE]
> Wird am Tabellenende angezeigt.
>
> Wird nur angezeigt, wenn ein Switchover geplant ist und das Ausgabeformat `pretty` verwendet wird.

`Maintenance mode`

> Ob die Cluster-Überwachung derzeit pausiert ist.
>
> > [!NOTE]
> > Wird am Tabellenende angezeigt.
> >
> > Wird nur angezeigt, wenn der Cluster pausiert ist und das Ausgabeformat `pretty` verwendet wird.

<a id="patronictl_list_parameters"></a>

#### Parameter {#parameters-6}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Informationen zu Mitgliedern der angegebenen Citus-Gruppe anzeigen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-e` / `--extended`  
Erweiterte Informationen anzeigen.

Die Attribute `Pending restart`, `Scheduled restart` und `Tags` auch dann anzeigen, wenn ihr Wert leer ist.

> [!NOTE]
> Gilt nur für die Ausgabeformate `pretty` und `tsv`.

`-t` / `--timestamp`  
Vor den Informationen zum Cluster und seinen Mitgliedern einen Zeitstempel ausgeben.

`-f` / `--format`  
Formatierung der Liste der Clustermitglieder in der Ausgabe.

Das Format kann einen der folgenden Werte haben:

- `pretty`: gibt die Clustermitglieder als formatierte Tabelle aus; oder
- `tsv`: gibt die Clustermitglieder tabellarisch aus, mit durch `\t` getrennten Spalten; oder
- `json`: gibt die Clustermitglieder im JSON-Format aus; oder
- `yaml`: gibt die Clustermitglieder im YAML-Format aus.

Der Standardwert ist `pretty`.

`-W`  
Informationen automatisch alle 2 Sekunden aktualisieren.

`-w` / `--watch`  
Informationen automatisch im angegebenen Intervall aktualisieren.

`TIME` ist das Aktualisierungsintervall in Sekunden.

<a id="patronictl_list_examples"></a>

#### Beispiele {#examples-6}

Informationen zum Cluster als formatierte Tabelle anzeigen:

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

Informationen zum Cluster als formatierte Tabelle mit erweiterten Spalten anzeigen:

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

Informationen zum Cluster im YAML-Format mit Ausführungszeitstempel anzeigen:

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_pause"></a>

### patronictl pause {#patronictl-pause}

<a id="patronictl_pause_synopsis"></a>

#### Aufrufschema {#synopsis-7}

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_pause_description"></a>

#### Beschreibung {#description-7}

`patronictl pause` versetzt den Patroni-Cluster vorübergehend in den Wartungsmodus und deaktiviert automatisches Failover.

<a id="patronictl_pause_parameters"></a>

#### Parameter {#parameters-7}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Die angegebene Citus-Gruppe pausieren.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `citus.group` zu lesen, sofern sie vorhanden ist.

`--wait`  
Warten, bis alle Patroni-Mitglieder pausiert sind, bevor die Kontrolle an den Aufrufer zurückgegeben wird.

<a id="patronictl_pause_examples"></a>

#### Beispiele {#examples-7}

Den Cluster in den Wartungsmodus versetzen und warten, bis alle Knoten pausiert sind:

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster {#patronictl-promote-cluster}

<a id="patronictl_promote_cluster_synopsis"></a>

#### Aufrufschema {#synopsis-8}

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### Beschreibung {#description-8}

`patronictl promote-cluster` wandelt einen Standby-Cluster in einen regulären Patroni-Cluster um.

Der Befehl entfernt den Abschnitt `standby_cluster` aus der dynamischen Konfiguration und wartet, bis der Leader als Primärserver läuft. Vor der Konfigurationsänderung gibt er die aktuelle Cluster-Topologie aus. Eine Bestätigung fordert er an, sofern `--force` nicht verwendet wird.

<a id="patronictl_promote_cluster_parameters"></a>

#### Parameter {#parameters-8}

`CLUSTER_NAME`: Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--force`: Flag zum Überspringen der Bestätigungsabfragen beim Hochstufen des Clusters.

Nützlich für Skripte.

<a id="patronictl_promote_cluster_examples"></a>

#### Beispiele {#examples-8}

Den Standby-Cluster hochstufen, sodass er als regulärer Patroni-Cluster läuft:

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_query"></a>

### patronictl query {#patronictl-query}

<a id="patronictl_query_synopsis"></a>

#### Aufrufschema {#synopsis-9}

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_query_description"></a>

#### Beschreibung {#description-9}

`patronictl query` führt einen SQL-Befehl oder ein Skript auf einem Mitglied des Patroni-Clusters aus.

<a id="patronictl_query_parameters"></a>

#### Parameter {#parameters-9}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Die angegebene Citus-Gruppe abfragen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-r` / `--role`  
Ein Mitglied mit der angegebenen Rolle auswählen.

Die Rolle kann einen der folgenden Werte haben:

- `leader`: der Leader eines regulären Patroni-Clusters oder eines Patroni-Standby-Clusters; oder
- `primary`: der Leader eines regulären Patroni-Clusters; oder
- `standby-leader`: der Leader eines Patroni-Standby-Clusters; oder
- `replica`: ein Replikat eines Patroni-Clusters; oder
- `standby`: entspricht `replica`; oder
- `any`: beliebige Rolle. Entspricht dem Weglassen dieses Parameters.

`-m` / `--member`  
Ein Mitglied mit dem angegebenen Namen auswählen.

`MEMBER_NAME` ist der Name des auszuwählenden Mitglieds.

`-d` / `--dbname`  
Datenbank, zu der eine Verbindung hergestellt und auf der die Abfrage ausgeführt wird.

`DBNAME` ist der Name der Datenbank. Ohne Angabe wird `USERNAME` verwendet.

`-U` / `--username`  
Benutzer für die Verbindung zur Datenbank.

`USERNAME` ist der Name des Benutzers. Ohne Angabe wird der Betriebssystembenutzer verwendet, der `patronictl query` ausführt.

`--password`  
Das Passwort des Benutzers abfragen, der die Verbindung herstellt.

Da Patroni `libpq` verwendet, kann alternativ eine Datei `~/.pgpass` erstellt oder die Umgebungsvariable `PGPASSWORD` gesetzt werden.

`--format`  
Formatierung der Abfrageausgabe.

Das Format kann einen der folgenden Werte haben:

- `pretty`: gibt das Abfrageergebnis als formatierte Tabelle aus; oder
- `tsv`: gibt das Abfrageergebnis tabellarisch aus, mit durch `\t` getrennten Spalten; oder
- `json`: gibt das Abfrageergebnis im JSON-Format aus; oder
- `yaml`: gibt das Abfrageergebnis im YAML-Format aus.

Der Standardwert ist `tsv`.

`-f` / `--file`  
Eine Datei als Quelle der auszuführenden Abfragebefehle verwenden.

`FILE_NAME` ist der Pfad zur Quelldatei.

`-c` / `--command`  
Den angegebenen SQL-Befehl als Abfrage ausführen.

`SQL_COMMAND` ist der auszuführende SQL-Befehl.

`--delimiter`  
Das Trennzeichen für die Ausgabe im Format `tsv`; ohne Angabe wird `\t` verwendet.

`-W`  
Die Abfrage automatisch alle 2 Sekunden erneut ausführen.

`-w` / `--watch`  
Die Abfrage automatisch im angegebenen Intervall erneut ausführen.

`TIME` ist das Intervall zwischen den Ausführungen in Sekunden.

<a id="patronictl_query_examples"></a>

#### Beispiele {#examples-9}

Einen SQL-Befehl als Benutzer `postgres` ausführen und dessen Passwort abfragen:

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

Einen SQL-Befehl als Benutzer `postgres` ausführen und das Passwort aus der Umgebungsvariable von `libpq` beziehen:

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

Einen SQL-Befehl alle 2 Sekunden ausführen und das Ergebnis im Format `pretty` ausgeben:

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

Einen SQL-Befehl auf der Datenbank `test` ausführen und das Ergebnis im YAML-Format ausgeben:

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

Einen SQL-Befehl auf dem Mitglied `postgresql2` ausführen:

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

Einen SQL-Befehl auf einem beliebigen Standby ausführen:

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_reinit"></a>

### patronictl reinit {#patronictl-reinit}

<a id="patronictl_reinit_synopsis"></a>

#### Aufrufschema {#synopsis-10}

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_reinit_description"></a>

#### Beschreibung {#description-10}

`patronictl reinit` erstellt eine Postgres-Standby-Instanz neu, die von einem Replikatmitglied des Patroni-Clusters verwaltet wird.

<a id="patronictl_reinit_parameters"></a>

#### Parameter {#parameters-10}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

`MEMBER_NAME`  
Name des Replikatmitglieds, dessen Postgres-Instanz neu erstellt werden soll.

Es können mehrere Replikatmitglieder angegeben werden. Ohne Angabe von Mitgliedern führt der Befehl keine Aktion aus.

`--group`  
Ein Replikatmitglied der angegebenen Citus-Gruppe neu erstellen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`--wait`  
Warten, bis die Neuinitialisierung der Postgres-Standby-Knoten abgeschlossen ist.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen beim Neuerstellen von Postgres-Standby-Instanzen.

Nützlich für Skripte.

`--from-leader`  
Flag zum direkten Beziehen des Basis-Backups vom Leader.

<a id="patronictl_reinit_examples"></a>

#### Beispiele {#examples-10}

Das Neuerstellen aller Replikatmitglieder des Patroni-Clusters anfordern und die Kontrolle sofort an den Aufrufer zurückgeben:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

Das Neuerstellen von `postgresql2` anfordern und auf den Abschluss warten:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

Das Neuerstellen von `postgresql2` anfordern und das Basis-Backup direkt vom Leader beziehen:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reload"></a>

### patronictl reload {#patronictl-reload}

<a id="patronictl_reload_synopsis"></a>

#### Aufrufschema {#synopsis-11}

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reload_description"></a>

#### Beschreibung {#description-11}

`patronictl reload` fordert ein Neuladen der lokalen Konfiguration für ein oder mehrere Patroni-Mitglieder an.

Dabei wird auf der verwalteten Postgres-Instanz auch `pg_ctl reload` ausgelöst, selbst wenn sich nichts geändert hat.

<a id="patronictl_reload_parameters"></a>

#### Parameter {#parameters-11}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

`MEMBER_NAME`  
Das Neuladen der lokalen Konfiguration für die angegebenen Patroni-Mitglieder anfordern.

Es können mehrere Mitglieder angegeben werden. Ohne Angabe von Mitgliedern werden alle berücksichtigt.

`--group`  
Ein Neuladen der Mitglieder der angegebenen Citus-Gruppe anfordern.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-r` / `--role`  
Mitglieder mit der angegebenen Rolle auswählen.

Die Rolle kann einen der folgenden Werte haben:

- `leader`: der Leader eines regulären Patroni-Clusters oder eines Patroni-Standby-Clusters; oder
- `primary`: der Leader eines regulären Patroni-Clusters; oder
- `standby-leader`: der Leader eines Patroni-Standby-Clusters; oder
- `replica`: ein Replikat eines Patroni-Clusters; oder
- `standby`: entspricht `replica`; oder
- `any`: beliebige Rolle. Entspricht dem Weglassen dieses Parameters.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen beim Anfordern eines Neuladens der lokalen Konfiguration.

Nützlich für Skripte.

<a id="patronictl_reload_examples"></a>

#### Beispiele {#examples-11}

Das Neuladen der lokalen Konfiguration aller Mitglieder des Patroni-Clusters anfordern:

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_remove"></a>

### patronictl remove {#patronictl-remove}

<a id="patronictl_remove_synopsis"></a>

#### Aufrufschema {#synopsis-12}

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_remove_description"></a>

#### Beschreibung {#description-12}

`patronictl remove` entfernt die Informationen zum Cluster aus dem DCS.

Dies ist ein interaktiver Vorgang.

> [!WARNING]
> Dieser Vorgang zerstört die Informationen zum Patroni-Cluster im DCS.

<a id="patronictl_remove_parameters"></a>

#### Parameter {#parameters-12}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

`--group`  
Die Informationen zum Patroni-Cluster entfernen, die zur angegebenen Citus-Gruppe gehören.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-f` / `--format`  
Formatierung der Mitgliederliste in der Ausgabe bei der Bestätigungsabfrage.

Das Format kann einen der folgenden Werte haben:

- `pretty`: gibt die Mitglieder als formatierte Tabelle aus; oder
- `tsv`: gibt die Mitglieder tabellarisch aus, mit durch `\t` getrennten Spalten; oder
- `json`: gibt die Mitglieder im JSON-Format aus; oder
- `yaml`: gibt die Mitglieder im YAML-Format aus.

Der Standardwert ist `pretty`.

<a id="patronictl_remove_examples"></a>

#### Beispiele {#examples-12}

Informationen zum Patroni-Cluster `batman` aus dem DCS entfernen:

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_restart"></a>

### patronictl restart {#patronictl-restart}

<a id="patronictl_restart_synopsis"></a>

#### Aufrufschema {#synopsis-13}

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_restart_description"></a>

#### Beschreibung {#description-13}

`patronictl restart` fordert einen Neustart der Postgres-Instanz an, die von einem Mitglied des Patroni-Clusters verwaltet wird.

Der Neustart kann sofort ausgeführt oder für später geplant werden.

<a id="patronictl_restart_parameters"></a>

#### Parameter {#parameters-13}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

`--group`  
Den zur angegebenen Citus-Gruppe gehörenden Patroni-Cluster neu starten.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-r` / `--role`  
Mitglieder mit der angegebenen Rolle auswählen.

Die Rolle kann einen der folgenden Werte haben:

- `leader`: der Leader eines regulären Patroni-Clusters oder eines Patroni-Standby-Clusters; oder
- `primary`: der Leader eines regulären Patroni-Clusters; oder
- `standby-leader`: der Leader eines Patroni-Standby-Clusters; oder
- `replica`: ein Replikat eines Patroni-Clusters; oder
- `standby`: entspricht `replica`; oder
- `any`: beliebige Rolle. Entspricht dem Weglassen dieses Parameters.

`--any`  
Einen einzelnen, zufällig ausgewählten Knoten aus denjenigen neu starten, die den angegebenen Filtern entsprechen.

`--pg-version`  
Nur Mitglieder auswählen, deren verwaltete Postgres-Instanz eine ältere als die angegebene Version hat.

`PG_VERSION` ist die zum Vergleich herangezogene Postgres-Version.

`--pending`  
Nur Mitglieder auswählen, die als `Pending restart` markiert sind.

`--timeout`: Den Neustart abbrechen, wenn er länger als die angegebene Wartezeit dauert, und ein Failover zu einem Replikat durchführen, wenn das Problem auf dem Primärserver auftritt.

`TIMEOUT` ist die Wartezeit in Sekunden, bevor der Neustart abgebrochen wird.

`--scheduled`  
Einen Neustart zum angegebenen Zeitpunkt planen.

`TIMESTAMP` ist der Zeitstempel, zu dem der Neustart erfolgen soll. Er ist in einem eindeutigen Format anzugeben, vorzugsweise mit Zeitzone. Mit dem Literal `now` kann der Neustart auch sofort ausgeführt werden.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen beim Anfordern von Neustarts.

Nützlich für Skripte.

<a id="patronictl_restart_examples"></a>

#### Beispiele {#examples-13}

Alle Mitglieder des Clusters sofort neu starten:

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

Ein zufällig ausgewähltes Mitglied des Clusters sofort neu starten:

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

Einen Neustart für `2023-09-13T18:00-03:00` planen:

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_resume"></a>

### patronictl resume {#patronictl-resume}

<a id="patronictl_resume_synopsis"></a>

#### Aufrufschema {#synopsis-14}

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_resume_description"></a>

#### Beschreibung {#description-14}

`patronictl resume` beendet den Wartungsmodus des Patroni-Clusters und aktiviert automatisches Failover wieder.

<a id="patronictl_resume_parameters"></a>

#### Parameter {#parameters-14}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Den Betrieb der angegebenen Citus-Gruppe fortsetzen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `citus.group` zu lesen, sofern sie vorhanden ist.

`--wait`  
Warten, bis die Pause für alle Patroni-Mitglieder aufgehoben ist, bevor die Kontrolle an den Aufrufer zurückgegeben wird.

<a id="patronictl_resume_examples"></a>

#### Beispiele {#examples-14}

Den Wartungsmodus des Clusters beenden:

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_show_config"></a>

### patronictl show-config {#patronictl-show-config}

<a id="patronictl_show_config_synopsis"></a>

#### Aufrufschema {#synopsis-15}

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_show_config_description"></a>

#### Beschreibung {#description-15}

`patronictl show-config` zeigt die im DCS gespeicherte dynamische Konfiguration des Clusters.

<a id="patronictl_show_config_parameters"></a>

#### Parameter {#parameters-15}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Die dynamische Konfiguration der angegebenen Citus-Gruppe anzeigen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `citus.group` zu lesen, sofern sie vorhanden ist.

<a id="patronictl_show_config_examples"></a>

#### Beispiele {#examples-15}

Die dynamische Konfiguration des Clusters `batman` anzeigen:

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_switchover"></a>

### patronictl switchover {#patronictl-switchover}

<a id="patronictl_switchover_synopsis"></a>

#### Aufrufschema {#synopsis-16}

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_switchover_description"></a>

#### Beschreibung {#description-16}

`patronictl switchover` führt einen Switchover im Cluster durch.

Der Befehl ist für funktionsfähige Cluster vorgesehen, z. B. wenn:

- ein Leader vorhanden ist;
- in einem synchronen Cluster synchrone Standbys verfügbar sind.

> [!NOTE]
> Bei einem nicht funktionsfähigen Cluster kommt stattdessen möglicherweise `patronictl failover` infrage.

<a id="patronictl_switchover_parameters"></a>

#### Parameter {#parameters-16}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Einen Switchover in der angegebenen Citus-Gruppe durchführen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`--leader` / `--primary`  
Den Leader angeben, der beim Switchover herabgestuft werden soll.

`LEADER_NAME` sollte mit dem Namen des aktuellen Leaders im Cluster übereinstimmen.

`--candidate`  
Der Knoten, der beim Switchover hochgestuft werden und die Rolle des Primärservers übernehmen soll.

`CANDIDATE_NAME` ist der Name des hochzustufenden Knotens.

`--scheduled`  
Einen Switchover zum angegebenen Zeitpunkt planen.

`TIMESTAMP` ist der Zeitstempel, zu dem der Switchover erfolgen soll. Er ist in einem eindeutigen Format anzugeben, vorzugsweise mit Zeitzone. Mit dem Literal `now` kann der Switchover auch sofort ausgeführt werden.

`--force`  
Flag zum Überspringen der Bestätigungsabfragen bei der Durchführung des Switchovers.

Nützlich für Skripte.

<a id="patronictl_switchover_examples"></a>

#### Beispiele {#examples-16}

Einen Switchover zum Knoten `postgresql2` durchführen:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

Einen Switchover zwischen `postgresql0` und `postgresql2` für `2023-09-13T18:00:00-03:00` planen:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_topology"></a>

### patronictl topology {#patronictl-topology}

<a id="patronictl_topology_synopsis"></a>

#### Aufrufschema {#synopsis-17}

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_topology_description"></a>

#### Beschreibung {#description-17}

`patronictl topology` zeigt Informationen zum Patroni-Cluster und seinen Mitgliedern als Baumansicht.

Die Ausgabe enthält folgende Informationen:

`Cluster`  
Name des Patroni-Clusters.

> [!NOTE]
> Wird im Tabellenkopf angezeigt.

`System identifier`  
Postgres-Systemkennung.

> [!NOTE]
> Wird im Tabellenkopf angezeigt.

`Member`  
Name des Patroni-Mitglieds.

> [!NOTE]
> Diese Spalte zeigt die Mitglieder als Baumansicht ihrer Replikationsverbindungen.

`Host`  
Host, auf dem sich das Mitglied befindet.

`Role`  
Aktuelle Rolle des Mitglieds.

Mögliche Werte sind:

- `Leader`: der aktuelle Leader eines regulären Patroni-Clusters; oder
- `Standby Leader`: der aktuelle Leader eines Patroni-Standby-Clusters; oder
- `Sync Standby`: ein synchroner Standby eines Patroni-Clusters mit aktiviertem synchronem Modus; oder
- `Replica`: ein regulärer Standby eines Patroni-Clusters.

`State`  
Aktueller Zustand von Postgres im Patroni-Mitglied.

Einige Beispiele für mögliche Zustände:

- `running`: wenn Postgres derzeit läuft;
- `streaming`: bei einem Replikat, wenn Postgres derzeit WAL per Streaming vom Primärserver empfängt;
- `in archive recovery`: bei einem Replikat, wenn Postgres derzeit WAL aus dem Archiv abruft;
- `stopped`: wenn Postgres heruntergefahren wurde;
- `crashed`: wenn Postgres abgestürzt ist.

`TL`  
Aktuelle Postgres-Timeline im Patroni-Mitglied.

`Receive LSN`  
Die letzte Write-Ahead-Log-Position, die das Mitglied per Streaming-Replikation empfangen und auf den Datenträger synchronisiert hat (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Replikationsrückstand zwischen der Position `Receive LSN` des Mitglieds und seiner Replikationsquelle in MB.

`Replay LSN`  
Die letzte Write-Ahead-Log-Position, die bei der Recovery des Mitglieds wiedergegeben wurde (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Replikationsrückstand zwischen der Position `Replay LSN` des Mitglieds und seiner Replikationsquelle in MB.

Darüber hinaus kann die Ausgabe folgende Informationen enthalten:

`Group`  
ID der Citus-Gruppe.

> [!NOTE]
> Wird im Tabellenkopf angezeigt.
>
> Wird nur bei einem Citus-Cluster angezeigt.

`Pending restart`  
`*` zeigt an, dass der Knoten einen Neustart benötigt, damit bestimmte Postgres-Konfigurationseinstellungen wirksam werden. Ein leerer Wert zeigt an, dass der Knoten keinen Neustart benötigt.

> [!NOTE]
> Wird als Attribut des Mitglieds angezeigt.
>
> Wird angezeigt, wenn der Knoten einen Neustart benötigt.

`Scheduled restart`  
Zeitstempel des geplanten Neustarts der vom Patroni-Mitglied verwalteten Postgres-Instanz. Ein leerer Wert zeigt an, dass für das Mitglied kein Neustart geplant ist.

> [!NOTE]
> Wird als Attribut des Mitglieds angezeigt.
>
> Wird angezeigt, wenn für den Knoten ein Neustart geplant ist.

`Tags`  
Enthält die für das Patroni-Mitglied gesetzten Tags. Ein leerer Wert zeigt an, dass entweder keine Tags konfiguriert wurden oder diese auf die Standardwerte gesetzt sind.

> [!NOTE]
> Wird als Attribut des Mitglieds angezeigt.
>
> Wird angezeigt, wenn der Knoten benutzerdefinierte Tags oder Standard-Tags mit abweichenden Werten hat.

`Scheduled switchover`  
Zeitstempel des geplanten Switchovers für den Patroni-Cluster, sofern vorhanden.

> [!NOTE]
> Wird am Tabellenende angezeigt.
>
> Wird nur angezeigt, wenn ein Switchover geplant ist.

`Maintenance mode`

> Ob die Cluster-Überwachung derzeit pausiert ist.
>
> > [!NOTE]
> > Wird am Tabellenende angezeigt.
> >
> > Wird nur angezeigt, wenn der Cluster pausiert ist.

<a id="patronictl_topology_parameters"></a>

#### Parameter {#parameters-17}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

Falls nicht angegeben, versucht [patronictl](/de/patroni/patronictl#patronictl), den Wert aus der Konfiguration `scope` zu lesen, sofern sie vorhanden ist.

`--group`  
Informationen zu Mitgliedern der angegebenen Citus-Gruppe anzeigen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

`-W`  
Informationen automatisch alle 2 Sekunden aktualisieren.

`-w` / `--watch`  
Informationen automatisch im angegebenen Intervall aktualisieren.

`TIME` ist das Aktualisierungsintervall in Sekunden.

<a id="patronictl_topology_examples"></a>

#### Beispiele {#examples-17}

Die Topologie des Clusters `batman` anzeigen – `postgresql1` und `postgresql2` replizieren von `postgresql0`:

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_version"></a>

### patronictl version {#patronictl-version}

<a id="patronictl_version_synopsis"></a>

#### Aufrufschema {#synopsis-18}

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_version_description"></a>

#### Beschreibung {#description-18}

`patronictl version` ermittelt die Version der Anwendung [patronictl](/de/patroni/patronictl#patronictl). Zusätzlich kann die Ausgabe Versionsinformationen zu Patroni-Clustern und ihren Mitgliedern enthalten.

<a id="patronictl_version_parameters"></a>

#### Parameter {#parameters-18}

`CLUSTER_NAME`  
Name des Patroni-Clusters.

`MEMBER_NAME`  
Name des Mitglieds des Patroni-Clusters.

`--group`  
Einen Patroni-Cluster mit der angegebenen Citus-Gruppe berücksichtigen.

`CITUS_GROUP` ist die ID der Citus-Gruppe.

<a id="patronictl_version_examples"></a>

#### Beispiele {#examples-18}

Nur die Version von [patronictl](/de/patroni/patronictl#patronictl) abrufen:

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

Die Version von [patronictl](/de/patroni/patronictl#patronictl) und aller Mitglieder des Clusters `batman` abrufen:

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

Die Version von [patronictl](/de/patroni/patronictl#patronictl) und der Mitglieder `postgresql1` und `postgresql2` des Clusters `batman` abrufen:

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
