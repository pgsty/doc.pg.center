---
title: "Patroni-Konfiguration"
weight: 30
icon: fa-solid fa-code
description: "Konfigurationsmodell, Vorrangregeln und Validierungswerkzeuge von Patroni."
sidebar_expanded: true
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/patroni_configuration.html"
---

<a id="config"></a>
Es gibt 3 Arten der Patroni-Konfiguration:

- Globale [dynamische Konfiguration](/de/patroni/config/dynamic#dynamic).  
  Diese Optionen werden im DCS (verteilter Konfigurationsspeicher) gespeichert und auf allen Clusterknoten angewendet. Die dynamische Konfiguration kann jederzeit mit dem Werkzeug [patronictl_edit_config](/de/patroni/patronictl#patronictl_edit_config) oder der [REST API](/de/patroni/rest_api#rest_api) von Patroni festgelegt werden. Gehören die geänderten Optionen nicht zur Startkonfiguration, werden sie asynchron (beim nächsten Aufwachen der Verarbeitungsschleife) auf jedem Knoten angewendet; dessen Konfiguration wird anschließend neu geladen. Erfordert ein Knoten einen Neustart, um die Konfiguration anzuwenden (wenn sich Werte von [PostgreSQL-Parametern](https://www.postgresql.org/docs/current/view-pg-settings.html) mit dem Kontext postmaster geändert haben), wird dies durch das spezielle Flag `pending_restart` im JSON members.data gekennzeichnet. Zusätzlich zeigt der Knotenstatus `"restart_pending": true` an.

- Lokale [Konfigurationsdatei](/de/patroni/config/yaml#yaml) (patroni.yml).  
  Diese Optionen werden in der Konfigurationsdatei definiert und haben Vorrang vor der dynamischen Konfiguration. `patroni.yml` kann zur Laufzeit geändert und neu geladen werden (ohne Patroni neu zu starten), indem SIGHUP an den Patroni-Prozess gesendet, die REST-API-Anfrage `POST /reload` gestellt oder [patronictl_reload](/de/patroni/patronictl#patronictl_reload) ausgeführt wird. Die lokale Konfiguration kann entweder aus einer einzelnen YAML-Datei oder einem Verzeichnis bestehen. Bei einem Verzeichnis werden alle darin enthaltenen YAML-Dateien nacheinander in sortierter Reihenfolge geladen. Ist ein Schlüssel in mehreren Dateien definiert, hat sein Vorkommen in der letzten Datei Vorrang.

- [Umgebungskonfiguration](/de/patroni/config/env#env).  
  Einige „lokale“ Konfigurationsparameter können über Umgebungsvariablen festgelegt oder überschrieben werden. Die Umgebungskonfiguration ist sehr nützlich in dynamischen Umgebungen, in denen einige Parameter nicht im Voraus bekannt sind (beispielsweise lässt sich beim Betrieb in `docker` die externe IP-Adresse nicht im Voraus kennen).

<a id="important_configuration_rules"></a>

--------

## Wichtige Regeln {#important-rules}

### Von Patroni gesteuerte PostgreSQL-Parameter {#postgresql-parameters-controlled-by-patroni}

Einige PostgreSQL-Parameter **müssen auf dem Primärserver und den Replikaten dieselben Werte haben**. Für diese Parameter **haben Werte aus den lokalen Patroni-Konfigurationsdateien oder aus Umgebungsvariablen keine Wirkung**. Um ihre Werte zu ändern oder festzulegen, muss die gemeinsame Konfiguration im DCS geändert werden. Die folgende Liste enthält diese Parameter mit ihren Standard- und Mindestwerten:

- **max_connections**: Standardwert 100, Mindestwert 25
- **max_locks_per_transaction**: Standardwert 64, Mindestwert 32
- **max_worker_processes**: Standardwert 8, Mindestwert 2
- **max_prepared_transactions**: Standardwert 0, Mindestwert 0
- **wal_level**: Standardwert hot_standby, zulässige Werte: hot_standby, replica, logical
- **track_commit_timestamp**: Standardwert off

Für die folgenden Parameter verlangt PostgreSQL keine gleichen Werte auf dem Primärserver und allen Replikaten. Da ein Replikat jedoch jederzeit zum Primärserver werden kann, sind unterschiedliche Werte kaum sinnvoll; daher **erlaubt Patroni das Festlegen ihrer Werte ausschließlich über die** [dynamische Konfiguration](/de/patroni/config/dynamic#dynamic).

- **max_wal_senders**: Standardwert 10, Mindestwert 3
- **max_replication_slots**: Standardwert 10, Mindestwert 4
- **wal_keep_segments**: Standardwert 8, Mindestwert 1
- **wal_keep_size**: Standardwert 128MB, Mindestwert 16MB
- **wal_log_hints**: on

Diese Parameter werden auf sinnvolle Werte beziehungsweise die Einhaltung eines Mindestwerts geprüft.

Patroni steuert außerdem einige weitere Postgres-Parameter:

- **listen_addresses** - wird aus `postgresql.listen` oder der Umgebungsvariablen `PATRONI_POSTGRESQL_LISTEN` gesetzt
- **port** - wird aus `postgresql.listen` oder der Umgebungsvariablen `PATRONI_POSTGRESQL_LISTEN` gesetzt
- **cluster_name** - wird aus `scope` oder der Umgebungsvariablen `PATRONI_SCOPE` gesetzt
- **hot_standby: on**

Zur Sicherheit werden die Parameter aus den obigen Listen in `postgresql.conf` geschrieben und als Argumentliste an `postgres` übergeben. Dadurch haben sie die höchste Priorität (ausgenommen `wal_keep_segments` und `wal_keep_size`), noch vor [ALTER SYSTEM](https://www.postgresql.org/docs/current/static/sql-altersystem.html).

Einige Parameter wie **postgresql.listen** und **postgresql.data_dir** **können nur lokal festgelegt werden**, also in der Patroni-[Konfigurationsdatei](/de/patroni/config/yaml#yaml) oder über eine [Konfigurationsvariable](/de/patroni/config/env#env). In den meisten Fällen überschreibt die lokale Konfiguration die dynamische Konfiguration.

Beim Anwenden lokaler oder dynamischer Konfigurationsoptionen werden folgende Schritte ausgeführt:

- Der Knoten prüft zunächst, ob eine Datei `postgresql.base.conf` vorhanden oder der Parameter `custom_conf` gesetzt ist.
- Ist `custom_conf` gesetzt, dient die dort angegebene Datei als Basiskonfiguration; `postgresql.base.conf` und `postgresql.conf` werden ignoriert.
- Ist `custom_conf` nicht gesetzt und existiert `postgresql.base.conf`, enthält diese Datei die umbenannte „ursprüngliche“ Konfiguration und dient als Basiskonfiguration.
- Ist weder `custom_conf` gesetzt noch `postgresql.base.conf` vorhanden, wird die ursprüngliche `postgresql.conf` in `postgresql.base.conf` umbenannt und als Basiskonfiguration verwendet.
- Die dynamischen Optionen werden (mit den obigen Ausnahmen) in `postgresql.conf` geschrieben. In `postgresql.conf` wird außerdem ein include für die Basiskonfiguration gesetzt (entweder `postgresql.base.conf` oder die Datei aus `custom_conf`). So lassen sich neue Optionen anwenden, ohne die Konfigurationsdatei erneut einzulesen, um das Vorhandensein des include zu prüfen.
- Einige Parameter, die für die Clusterverwaltung durch Patroni wesentlich sind, werden über die Befehlszeile überschrieben.
- Wird eine Option geändert, die einen Neustart erfordert (hierfür sollten der Kontext in pg_settings und die tatsächlichen Werte dieser Optionen betrachtet werden), wird auf diesem Knoten das Flag pending_restart gesetzt. Dieses Flag wird bei jedem Neustart zurückgesetzt.

Die Parameter werden in der folgenden Reihenfolge angewendet (Laufzeitparameter haben die höchste Priorität):

1.  Parameter aus der Datei `postgresql.base.conf` laden (oder aus einer `custom_conf`-Datei, falls gesetzt)
2.  Parameter aus der Datei `postgresql.conf` laden
3.  Parameter aus der Datei `postgresql.auto.conf` laden
4.  Laufzeitparameter über `-o --name=value`

Dies ermöglicht die Konfiguration aller Knoten (2) sowie eines bestimmten Knotens mit `ALTER SYSTEM` (3) und stellt sicher, dass für den Betrieb von Patroni wesentliche Parameter durchgesetzt werden (4). Zugleich bleibt Raum für Konfigurationswerkzeuge, die `postgresql.conf` direkt ohne Beteiligung von Patroni verwalten (1).

<a id="shared_memory_gucs"></a>

### PostgreSQL-Parameter mit Einfluss auf den gemeinsam genutzten Speicher {#postgresql-parameters-that-touch-shared-memory}

PostgreSQL hat einige Parameter, die die Größe des von ihnen verwendeten gemeinsam genutzten Speichers bestimmen:

- **max_connections**
- **max_prepared_transactions**
- **max_locks_per_transaction**
- **max_wal_senders**
- **max_worker_processes**

Änderungen dieser Parameter werden erst nach einem PostgreSQL-Neustart wirksam. Ihre Strukturen im gemeinsam genutzten Speicher dürfen auf den Standby-Knoten nicht kleiner sein als auf dem Primärserver.

Wie bereits erläutert, erlaubt Patroni Änderungen ihrer Werte nur über die [dynamische Konfiguration](/de/patroni/config/dynamic#dynamic). Dies umfasst üblicherweise:

1.  Änderungen mit [patronictl_edit_config](/de/patroni/patronictl#patronictl_edit_config) anwenden (oder über den REST-API-Endpunkt `/config`)
2.  Knoten mit [patronictl_restart](/de/patroni/patronictl#patronictl_restart) neu starten (oder über den REST-API-Endpunkt `/restart`)

**Hinweis:** PostgreSQL-Knoten sollten mit dem Befehl [patronictl_restart](/de/patroni/patronictl#patronictl_restart) oder über den REST-API-Endpunkt `/restart` neu gestartet werden. Der Versuch, PostgreSQL durch einen Neustart des Patroni-Daemons neu zu starten, etwa mit `systemctl restart patroni`, kann beim Neustart des Primärservers ein Failover im Cluster auslösen.

Da diese Einstellungen den gemeinsam genutzten Speicher steuern, ist beim Neustart der Knoten zusätzliche Sorgfalt erforderlich:

- Wenn der Wert einer dieser Einstellungen **erhöht** werden soll:

  > 1.  Zuerst alle Standbys neu starten
  > 2.  Danach den Primärserver neu starten

- Wenn der Wert einer dieser Einstellungen **verringert** werden soll:

  > 1.  Zuerst den Primärserver neu starten
  > 2.  Danach alle Standbys neu starten

**Hinweis:** Wenn nach einer **Verringerung** einer dieser Einstellungen alle Knoten auf einmal neu gestartet werden, ignoriert Patroni die Änderung und startet den Standby mit dem ursprünglichen Wert neu. Daher müssen die Standbys später erneut neu gestartet werden. So verhindert Patroni eine endlose Absturzschleife des Standbys: PostgreSQL beendet sich mit einer `FATAL`-Meldung, wenn einer dieser Parameter auf einen niedrigeren Wert gesetzt wird als den, den `pg_controldata` auf dem Standby-Knoten ausweist. Die Einstellung kann auf dem Standby also erst verringert werden, wenn dessen `pg_controldata` hinsichtlich dieser Änderungen auf dem Primärserver aktuell ist.

Weitere Informationen dazu enthält die [Administrationsübersicht von PostgreSQL](https://www.postgresql.org/docs/current/hot-standby.html#HOT-STANDBY-ADMIN).

### Patroni-Konfigurationsparameter {#patroni-configuration-parameters}

Auch die folgenden Patroni-Konfigurationsoptionen **können nur dynamisch geändert werden**:

- **ttl**: 30
- **loop_wait**: 10
- **retry_timeout**: 10
- **maximum_lag_on_failover**: 1048576
- **max_timelines_history**: 0
- **check_timeline**: false
- **postgresql.use_slots**: true

Bei einer Änderung dieser Optionen liest Patroni den entsprechenden Abschnitt der im DCS gespeicherten Konfiguration und ändert seine Laufzeitwerte.

Patroni-Knoten schreiben den Zustand der DCS-Optionen bei jeder Konfigurationsänderung in die Datei `patroni.dynamic.json` im Postgres-Datenverzeichnis. Nur der Leader darf diese Optionen aus der gespeicherten Datei wiederherstellen, wenn sie im DCS vollständig fehlen oder ungültig sind.

<a id="validate_generate_config"></a>

--------

## Konfiguration erzeugen und validieren {#configuration-generation-and-validation}

Patroni bietet Befehlszeilenschnittstellen zum Erzeugen und Validieren einer [lokalen Patroni-Konfiguration](/de/patroni/config/yaml#yaml). Mit dem ausführbaren Programm `patroni` lässt sich:

- Eine lokale Patroni-Beispielkonfiguration erstellen;
- Eine Patroni-Konfigurationsdatei für die lokal laufende PostgreSQL-Instanz erstellen (etwa als Vorbereitung für die [Patroni-Integration](/de/patroni/existing_data#existing_data));
- Eine angegebene Patroni-Konfigurationsdatei validieren.

<a id="generate_sample_config"></a>

### Patroni-Beispielkonfiguration {#sample-patroni-configuration}

```text
patroni --generate-sample-config [configfile]
```

#### Beschreibung {#description}

Erzeugt eine Patroni-Beispielkonfigurationsdatei im Format `yaml`. Parameterwerte werden über die [Umgebungskonfiguration](/de/patroni/config/env#env) festgelegt. Sind sie dort nicht gesetzt, werden die Standardwerte von Patroni verwendet oder die Zeichenfolge `#FIXME` für Werte, die der Benutzer später festlegen sollte.

Einige Standardwerte werden anhand der lokalen Umgebung bestimmt:

> - **postgresql.listen**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der Standardport `5432`.
> - **postgresql.connect_address**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der Standardport `5432`.
> - **postgresql.authentication.rewind**: wird nur definiert, wenn die PostgreSQL-Version anhand der Programmdatei ermittelt werden kann und mindestens 11 ist.
> - **restapi.listen**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der Standardport `8008`.
> - **restapi.connect_address**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der Standardport `8008`.

#### Parameter {#parameters}

`configfile` - vollständiger Pfad zur Konfigurationsdatei, in der das Ergebnis gespeichert wird. Fehlt die Angabe, wird das Ergebnis an `stdout` ausgegeben.

<a id="generate_config"></a>

### Patroni-Konfiguration für eine laufende Instanz {#patroni-configuration-for-a-running-instance}

```text
patroni --generate-config [--dsn DSN] [configfile]
```

#### Beschreibung {#description-1}

Erzeugt eine Patroni-Konfiguration im Format `yaml` für die lokal laufende PostgreSQL-Instanz. Für die Verbindung zu PostgreSQL wird entweder der angegebene DSN (hat Vorrang) oder die PostgreSQL-[Umgebungsvariablen](https://www.postgresql.org/docs/current/libpq-envars.html) verwendet. Ist kein Passwort angegeben, sollte es auf Aufforderung eingegeben werden.

Alle nicht internen GUCs der Quellinstanz von Postgres dienen als Quelle für die folgenden Patroni-Konfigurationsparameter, unabhängig davon, ob sie über eine Konfigurationsdatei, die postmaster-Befehlszeile oder Umgebungsvariablen gesetzt wurden:

> - **scope**: Wert des GUC `cluster_name`;
> - **postgresql.listen**: Werte der GUCs `listen_addresses` und `port`;
> - **postgresql.data_dir**: Wert des GUC `data_directory`;
> - **postgresql.parameters**: Werte der GUCs `archive_command`, `restore_command`, `archive_cleanup_command`, `recovery_end_command`, `ssl_passphrase_command`, `hba_file`, `ident_file`, `config_file`;
> - **bootstrap.dcs**: alle anderen ermittelten PostgreSQL-GUCs.

Wird `scope`, `postgresql.listen` oder `postgresql.data_dir` nicht aus den Postgres-GUCs gesetzt, wird der jeweilige Wert aus der [Umgebungskonfiguration](/de/patroni/config/env#env) verwendet.

Weitere Regeln zur Bestimmung der Werte:

> - **name**: Wert der Umgebungsvariablen `PATRONI_NAME`, falls gesetzt, andernfalls der Hostname des aktuellen Rechners.
> - **postgresql.bin_dir**: Pfad zu den Postgres-Programmdateien, ermittelt aus der laufenden Instanz.
> - **postgresql.connect_address**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der für die Verbindung zur Instanz verwendete Port oder der Wert des GUC `port`.
> - **postgresql.authentication.superuser**: die für die Verbindung zur Instanz verwendete Konfiguration;
> - **postgresql.pg_hba**: die aus der `hba_file` der Quellinstanz gelesenen Zeilen.
> - **postgresql.pg_ident**: die aus der `ident_file` der Quellinstanz gelesenen Zeilen.
> - **restapi.listen**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der Standardport `8008`.
> - **restapi.connect_address**: die von `getaddrinfo` aufgelöste IP-Adresse zum Hostnamen des aktuellen Rechners, den `gethostname` zurückgibt, und der Standardport `8008`.

Weitere über die [Umgebungskonfiguration](/de/patroni/config/env#env) definierte Parameter werden ebenfalls in die Konfiguration aufgenommen.

#### Parameter {#parameters-1}

`configfile`  
Vollständiger Pfad zur Konfigurationsdatei, in der das Ergebnis gespeichert wird. Fehlt die Angabe, wird das Ergebnis an `stdout` ausgegeben.

`dsn`  
Optionale DSN-Zeichenfolge für die lokale PostgreSQL-Instanz, aus der die GUC-Werte ermittelt werden sollen.

### Patroni-Konfiguration validieren {#validate-patroni-configuration}

```text
patroni --validate-config [configfile] [--ignore-listen-port | -i]
```

#### Beschreibung {#description-2}

Validiert die angegebene Patroni-Konfiguration und gibt Informationen zu fehlgeschlagenen Prüfungen aus.

#### Parameter {#parameters-2}

`configfile`  
Vollständiger Pfad zur zu prüfenden Konfigurationsdatei. Ist er nicht angegeben oder existiert die Datei nicht, wird versucht, die Konfiguration aus der Umgebungsvariablen `PATRONI_CONFIGURATION` oder, falls diese nicht gesetzt ist, aus den [Patroni-Umgebungsvariablen](/de/patroni/config/env#env) zu lesen.

`--ignore-listen-port | -i`  
Optionales Flag, um bei der Validierung von `configfile` Bindungsfehler für bereits belegte `listen`-Ports zu ignorieren.

`--print | -p`  
Optionales Flag, um die lokale Konfiguration (einschließlich der durch die Umgebungskonfiguration überschriebenen Werte) nach erfolgreicher Validierung auszugeben.
