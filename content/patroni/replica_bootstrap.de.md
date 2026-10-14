---
title: "Replikaterstellung und Cluster-Initialisierung"
linkTitle: "Replikate initialisieren"
weight: 60
icon: fa-solid fa-boxes-stacked
description: "Replikaterstellung, Cluster-Initialisierung und benutzerdefinierte Erstellungsverfahren."
module: [PATRONI]
categories: [Aufgabe]
upstream_link: "https://patroni.readthedocs.io/en/latest/replica_bootstrap.html"
---

<a id="replica_imaging_and_bootstrap"></a>
Patroni ermöglicht es, die Erstellung neuer Replikate anzupassen. Ebenso lässt sich festlegen, wie ein neuer, leerer Cluster initialisiert wird. Die beiden Vorgänge sind klar voneinander getrennt: Patroni erstellt Replikate nur dann, wenn der Schlüssel `initialize` für den Cluster im DCS vorhanden ist. Fehlt der Schlüssel `initialize`, führt Patroni die Cluster-Initialisierung ausschließlich auf dem ersten Knoten aus, der die Sperre für diesen Schlüssel erlangt.

<a id="custom_bootstrap"></a>

--------

## Cluster-Initialisierung {#bootstrap}

PostgreSQL stellt den Befehl `initdb` zum Initialisieren eines neuen Clusters bereit; Patroni ruft ihn standardmäßig auf. In bestimmten Fällen, insbesondere beim Erstellen eines neuen Clusters als Kopie eines bestehenden, muss die eingebaute Methode durch eigene Aktionen ersetzt werden. Patroni kann benutzerdefinierte Skripte zur Cluster-Initialisierung ausführen und ihnen die erforderlichen Argumente wie Clustername und Pfad zum Datenverzeichnis übergeben. Dies wird im Abschnitt `bootstrap` der Patroni-Konfiguration festgelegt. Beispiel:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script> [param1 [, ...]]
        keep_existing_recovery_conf: False
        no_params: False
        recovery_conf:
            recovery_target_action: promote
            recovery_target_timeline: latest
            restore_command: <method_specific_restore_command>
```

Jede benutzerdefinierte Initialisierungsmethode muss über die Einstellung `method` benannt werden und im gleichnamigen Abschnitt einen `command` definieren. Die spezielle Methode `initdb` aktiviert das Standardverhalten; in diesem Fall kann der Parameter `method` vollständig entfallen. Für `command` kann ein absoluter Pfad, ein Pfad relativ zum Arbeitsverzeichnis von Patroni oder ein in `PATH` verfügbarer Befehlsname angegeben werden. Zusätzlich zu den festen Parametern aus den Konfigurationsdateien übergibt Patroni zwei clusterspezifische Parameter:

`--scope`  
Name des zu initialisierenden Clusters

`--datadir`  
Pfad zum Datenverzeichnis der zu initialisierenden Clusterinstanz

Die Übergabe dieser beiden zusätzlichen Optionen lässt sich deaktivieren, indem der spezielle Parameter `no_params` auf `True` gesetzt wird.

Gibt das Initialisierungsskript `0` zurück, versucht Patroni, die damit erstellte PostgreSQL-Instanz zu konfigurieren und zu starten. Schlägt ein Zwischenschritt fehl oder gibt das Skript einen Wert ungleich null zurück, betrachtet Patroni die Initialisierung als fehlgeschlagen, räumt auf und gibt die initialize-Sperre frei, damit ein anderer Knoten die Initialisierung versuchen kann.

Ist im selben Abschnitt wie die benutzerdefinierte Initialisierungsmethode ein Block `recovery_conf` definiert, erzeugt Patroni vor dem Start der neu initialisierten Instanz eine `recovery.conf` (oder setzt bei PostgreSQL \>= 12 die Recovery-Einstellungen in der Postgres-Konfiguration). Eine solche Recovery-Konfiguration sollte üblicherweise mindestens einen Parameter `recovery_target_*` enthalten und `recovery_target_action` auf `promote` setzen.

Ist `keep_existing_recovery_conf` definiert und auf `True` gesetzt, entfernt Patroni eine vorhandene Datei `recovery.conf` nicht (PostgreSQL \<= 11). Ebenso entfernt Patroni in diesem Fall weder eine vorhandene `recovery.signal` noch eine `standby.signal` und überschreibt auch die konfigurierten Recovery-Einstellungen nicht (PostgreSQL \>= 12). Dies ist bei der Initialisierung aus einem Backup mit Werkzeugen wie pgBackRest nützlich, die selbst die passende Recovery-Konfiguration erzeugen.

Alle weiteren Schlüssel-Wert-Paare in der Konfiguration der benutzerdefinierten Initialisierungsmethode werden außerdem als Argumente im Format `--name=value` an `command` übergeben. Beispiel:

```yaml
bootstrap:
    method: <custom_bootstrap_method_name>
    <custom_bootstrap_method_name>:
        command: <path_to_custom_bootstrap_script>
        arg1: value1
        arg2: value2
```

Dadurch wird der konfigurierte `command` zusätzlich mit den Befehlszeilenargumenten `--arg1=value1 --arg2=value2` aufgerufen.

> [!NOTE]
> Initialisierungsmethoden werden weder verkettet, noch wird bei einem Fehlschlag der gewählten Methode auf die Standardmethode zurückgegriffen.

Ein neuer Patroni-Cluster lässt sich beispielsweise mit folgender Konfiguration aus einem Barman-Backup initialisieren:

```yaml
bootstrap:
    method: barman
    barman:
        keep_existing_recovery_conf: true
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
```

> [!NOTE]
> `patroni_barman recover` setzt voraus, dass auf dem Barman-Host sowohl Barman als auch `pg-backup-api` konfiguriert sind, damit `barman recover` über die Backup-API aus der Ferne ausgeführt werden kann. Das obige Beispiel verwendet nur einen Teil der verfügbaren Parameter. Weitere Informationen liefert `patroni_barman recover --help`.

<a id="custom_replica_creation"></a>

--------

## Replikate erstellen {#building-replicas}

Patroni verwendet das bewährte `pg_basebackup`, um neue Replikate zu erstellen. Dafür ist eine laufende PostgreSQL-Quellinstanz erforderlich; eine eingebaute Bereinigung veralteter Backup-Dateien ist nicht vorhanden. Manche Anwender bevorzugen andere Backup-Lösungen wie `WAL-E`, `pgBackRest`, `Barman` oder eigene Skripte. Um all diese Fälle abzudecken, unterstützt Patroni benutzerdefinierte Skripte zum Klonen eines neuen Replikats. Sie werden im Konfigurationsblock `postgresql` eingerichtet:

```yaml
postgresql:
    create_replica_methods:
        - <method name>
    <method name>:
        command: <command name>
        keep_data: True
        no_params: True
        no_leader: 1
```

Beispiel: wal_e

```yaml
postgresql:
    create_replica_methods:
        - wal_e
        - basebackup
    wal_e:
        command: patroni_wale_restore
        no_leader: 1
        envdir: '{{WALE_ENV_DIR}}'
        use_iam: 1
    basebackup:
        max-rate: '100M'
```

Beispiel: pgbackrest

```yaml
postgresql:
    create_replica_methods:
        - pgbackrest
        - basebackup
    pgbackrest:
        command: /usr/bin/pgbackrest --stanza=<scope> --delta restore
        keep_data: True
        no_params: True
    basebackup:
        max-rate: '100M'
```

Beispiel: Barman

```yaml
postgresql:
    create_replica_methods:
        - barman
        - basebackup
    barman:
        command: patroni_barman --api-url https://barman-host:7480 recover
        barman-server: my_server
        ssh-command: ssh postgres@patroni-host
    basebackup:
        max-rate: '100M'
```

> [!NOTE]
> `patroni_barman recover` setzt voraus, dass auf dem Barman-Host sowohl Barman als auch `pg-backup-api` konfiguriert sind, damit `barman recover` über die Backup-API aus der Ferne ausgeführt werden kann. Das obige Beispiel verwendet nur einen Teil der verfügbaren Parameter. Weitere Informationen liefert `patroni_barman recover --help`.

`create_replica_methods` legt die verfügbaren Methoden zur Replikaterstellung und ihre Ausführungsreihenfolge fest. Patroni beendet die Versuche bei der ersten Methode, die 0 zurückgibt. Für jede Methode sollte ein eigener Abschnitt in der Konfigurationsdatei den auszuführenden Befehl und alle zu übergebenden benutzerdefinierten Parameter aufführen. Sämtliche Parameter werden im Format `--name=value` übergeben. Zusätzlich zu den benutzerdefinierten Parametern übergibt Patroni einige clusterspezifische:

`--scope`  
Cluster, zu dem dieses Replikat gehört

`--datadir`  
Pfad zum Datenverzeichnis des Replikats

`--role`  
Immer 'replica'

`--connstring`  
Verbindungszeichenfolge zum Clustermitglied, von dem geklont werden soll (Primärserver oder anderes Replikat). Der Benutzer in der Verbindungszeichenfolge kann SQL-Befehle und Befehle des Replikationsprotokolls ausführen.

Ist der spezielle Parameter `no_leader` aktiviert, darf Patroni die Methode zur Replikaterstellung auch dann aufrufen, wenn weder ein Leader noch Replikate laufen. In diesem Fall wird eine leere Verbindungszeichenfolge übergeben. Dies ist nützlich, um einen zuvor laufenden Cluster aus einem Binärbackup wiederherzustellen.

Ist der spezielle Parameter `keep_data` aktiviert, leert Patroni das PGDATA-Verzeichnis vor dem Aufruf der Wiederherstellung nicht.

Ist der spezielle Parameter `no_params` aktiviert, werden dem benutzerdefinierten Befehl keine clusterspezifischen Parameter automatisch hinzugefügt. Benutzerdefinierte Parameter werden weiterhin übergeben.

Die Methode `basebackup` ist ein Sonderfall: Sie wird verwendet, wenn `create_replica_methods` leer ist, kann aber auch ausdrücklich in `create_replica_methods` aufgeführt werden. Diese Methode initialisiert ein neues Replikat mit `pg_basebackup`. Das Basisbackup wird vom Leader bezogen, es sei denn, es gibt Replikate mit dem Tag `clonefrom`; dann dient eines dieser Replikate als Quelle für pg_basebackup. Die Methode funktioniert ohne Konfiguration, es kann jedoch ein Konfigurationsabschnitt `basebackup` angegeben werden. Es gelten dieselben Regeln wie für die Konfiguration anderer Methoden: Dort sollten nur lange Optionen (mit --) angegeben werden. Patroni akzeptiert weder das Überschreiben der Verbindungseinstellungen noch Optionen für Backups im tar-Format oder mit clientseitiger Komprimierung. Ab PostgreSQL 15 wird serverseitige Komprimierung mit `compress: server-gzip` oder `compress: server-zstd` unterstützt. Patroni filtert von ihm selbst gesteuerte Optionen und andere Komprimierungseinstellungen als serverseitige Komprimierung heraus, führt aber keine vollständige Validierung aller Optionsnamen und -werte durch. Werden symbolische Links für das WAL-Verzeichnis verwendet, muss der Benutzer außerdem den richtigen Pfad für `--waldir` als Option angeben, damit der symbolische Link nach dem Aufbau oder der Neuinitialisierung des Replikats erhalten bleibt. Diese Option wird allerdings erst seit v10 unterstützt.

Die basebackup-Parameter können entweder als Zuordnung (Schlüssel-Wert-Paare) oder als Liste angegeben werden. Jedes Listenelement kann ein Schlüssel-Wert-Paar oder ein einzelner Schlüssel sein (für Optionen ohne Wert, etwa `--verbose`). Die folgenden 2 Beispiele zeigen beide Formen:

```yaml
postgresql:
    basebackup:
        max-rate: '100M'
        checkpoint: 'fast'
```

und

```yaml
postgresql:
    basebackup:
        - verbose
        - max-rate: '100M'
        - waldir: /pg-wal-mount/external-waldir
```

Schlagen alle Methoden zur Replikaterstellung fehl, versucht Patroni im nächsten Durchlauf der Ereignisschleife erneut alle Methoden der Reihe nach.
