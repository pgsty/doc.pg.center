---
title: "Eine eigenständige Instanz in einen Patroni-Cluster überführen"
linkTitle: "Bestehenden Cluster übernehmen"
weight: 140
icon: fa-solid fa-truck-moving
description: "Vorgehen zur Übernahme bestehender PostgreSQL-Daten in einen Patroni-Cluster."
module: [PATRONI]
categories: [Aufgabe]
aliases: [/patroni/existing_data/]
upstream_link: "https://patroni.readthedocs.io/en/latest/existing_data.html"
---

<a id="existing_data"></a>
Dieser Abschnitt beschreibt, wie eine eigenständige PostgreSQL-Instanz in einen Patroni-Cluster überführt wird.

Zur Bereitstellung eines Patroni-Clusters ohne bestehende PostgreSQL-Instanz siehe [Ausführen und Konfigurieren](/de/docs/patroni/readme#running_configuring).

--------

## Vorgehen {#procedure}

Nachfolgend stehen die Schritte zur Übernahme eines bestehenden Postgres-Clusters in die Verwaltung durch Patroni. Dabei wird vorausgesetzt, dass alle Knoten des bestehenden Clusters aktuell laufen und die Postgres-Konfiguration während der Migration *nicht* geändert werden soll. Die Schritte:

1.  Die Postgres-Benutzer wie im Abschnitt [authentication](/de/docs/patroni/config/yaml#postgresql_settings) der Patroni-Konfiguration beschrieben anlegen. Der folgende Codeblock enthält SQL-Beispiele zum Anlegen der Benutzer; Benutzernamen und Passwörter müssen an die eigene Umgebung angepasst werden. Sind die entsprechenden Benutzer bereits vorhanden, kann dieser Schritt entfallen.

    ``` sql
    -- Patroni superuser
    -- Replace PATRONI_SUPERUSER_USERNAME and PATRONI_SUPERUSER_PASSWORD accordingly
    CREATE USER PATRONI_SUPERUSER_USERNAME WITH SUPERUSER ENCRYPTED PASSWORD 'PATRONI_SUPERUSER_PASSWORD';

    -- Patroni replication user
    -- Replace PATRONI_REPLICATION_USERNAME and PATRONI_REPLICATION_PASSWORD accordingly
    CREATE USER PATRONI_REPLICATION_USERNAME WITH REPLICATION ENCRYPTED PASSWORD 'PATRONI_REPLICATION_PASSWORD';

    -- Patroni rewind user, if you intend to enable use_pg_rewind in your Patroni configuration
    -- Replace PATRONI_REWIND_USERNAME and PATRONI_REWIND_PASSWORD accordingly
    CREATE USER PATRONI_REWIND_USERNAME WITH ENCRYPTED PASSWORD 'PATRONI_REWIND_PASSWORD';
    GRANT EXECUTE ON function pg_catalog.pg_ls_dir(text, boolean, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_stat_file(text, boolean) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text) TO PATRONI_REWIND_USERNAME;
    GRANT EXECUTE ON function pg_catalog.pg_read_binary_file(text, bigint, bigint, boolean) TO PATRONI_REWIND_USERNAME;
    ```

2.  Die folgenden Schritte auf allen Postgres-Knoten ausführen. Zuerst alle Schritte auf einem Knoten abschließen, bevor mit dem nächsten fortgefahren wird. Mit dem Primärknoten beginnen, anschließend die einzelnen Standby-Knoten bearbeiten:

    1.  Wird Postgres über systemd betrieben, die systemd-Unit für Postgres deaktivieren. Dies ist erforderlich, weil Patroni das Starten und Stoppen des Postgres-Daemons übernimmt.
    2.  Eine YAML-Konfigurationsdatei für Patroni erstellen. Dafür können die [Werkzeuge zur Erzeugung und Validierung der Patroni-Konfiguration](/de/docs/patroni/config#validate_generate_config) verwendet werden.
        - **Hinweis (nur für den Primärknoten):** Werden Replikationsslots zur Replikation zwischen Clustermitgliedern verwendet, wird empfohlen, `use_slots` zu aktivieren und die bestehenden Replikationsslots über den Konfigurationseintrag `slots` als permanent zu konfigurieren. Bei aktiviertem `use_slots` erstellt Patroni automatisch Replikationsslots für die Replikation zwischen Mitgliedern und entfernt Slots, die es nicht erkennt. Permanente Slots sorgen hier dafür, dass die bestehenden Slots während der Migration zu Patroni erhalten bleiben. Einzelheiten stehen unter [Dynamische Konfiguration](/de/docs/patroni/config/dynamic#dynamic).
    3.  Patroni über die systemd-Service-Unit `patroni` starten. Es erkennt automatisch, dass Postgres bereits läuft, und beginnt mit der Überwachung der Instanz.

3.  Den Startvorgang von Postgres an Patroni übergeben. Dazu müssen die Clustermitglieder mit dem Befehl [patronictl restart cluster-name member-name](/de/docs/patroni/patronictl#patronictl_restart_parameters) neu gestartet werden. Für eine möglichst kurze Ausfallzeit kann dieser Schritt aufgeteilt werden:

    1.  Die Standby-Knoten sofort neu starten.
    2.  Den Neustart des Primärknotens für ein Wartungsfenster planen.

4.  Wurden in Schritt `2.2.` permanente Slots konfiguriert, sollten sie mit dem Befehl [patronictl edit-config cluster-name](/de/docs/patroni/patronictl#patronictl_edit_config_parameters) aus der Konfiguration `slots` entfernt werden, sobald die `restart_lsn` der von Patroni angelegten Slots die `restart_lsn` der ursprünglichen Slots für die jeweiligen Mitglieder eingeholt hat. Durch das Entfernen aus der Konfiguration `slots` kann Patroni die ursprünglichen Slots aus dem Cluster löschen, sobald sie nicht mehr benötigt werden. Die folgende Beispielabfrage zeigt die `restart_lsn` zweier Slots zum Vergleich:

    ``` sql
    -- Assume original_slot_for_member_x is the name of the slot in your original
    -- cluster for replicating changes to member X, and slot_for_member_x is the
    -- slot created by Patroni for that purpose. You need restart_lsn of
    -- slot_for_member_x to be >= restart_lsn of original_slot_for_member_x
    SELECT slot_name,
           restart_lsn
    FROM pg_replication_slots
    WHERE slot_name IN (
        'original_slot_for_member_x',
        'slot_for_member_x'
    )
    ```

<a id="major_upgrade"></a>

## Upgrade auf eine neue PostgreSQL-Hauptversion {#major-upgrade-of-postgresql-version}

Ein Upgrade auf eine neue Hauptversion mit `pg_upgrade` erfolgt nach folgendem Verfahren:

1.  Patroni stoppen.
2.  Die PostgreSQL-Binärdateien aktualisieren und [pg_upgrade](https://www.postgresql.org/docs/current/pgupgrade.html) auf dem Primärknoten ausführen.
3.  patroni.yml aktualisieren.
4.  Den initialize-Schlüssel aus dem DCS entfernen oder den vollständigen Clusterzustand im DCS löschen. Letzteres lässt sich mit [patronictl remove cluster-name](/de/docs/patroni/patronictl#patronictl_remove_parameters) erreichen. Dies ist nötig, weil der neue PostgreSQL-Cluster mit initdb initialisiert wird und dadurch eine neue PostgreSQL-Systemkennung erhält.
5.  Wurde der Clusterzustand im vorherigen Schritt gelöscht, kann patroni.dynamic.json aus dem alten in das neue Datenverzeichnis kopiert werden. So lassen sich einige zuvor gesetzte PostgreSQL-Parameter beibehalten.
6.  Patroni auf dem Primärknoten starten.
7.  Auf den Standby-Knoten die PostgreSQL-Binärdateien und patroni.yml aktualisieren sowie data_dir leeren.
8.  Patroni auf den Standby-Knoten starten und warten, bis die Replikation abgeschlossen ist.

PostgreSQL unterstützt die Ausführung von pg_upgrade auf Standby-Knoten nicht. Mit entsprechender Sachkenntnis kann anstelle des Leerens von data_dir auf den Standby-Knoten das unter <https://www.postgresql.org/docs/current/pgupgrade.html> beschriebene rsync-Verfahren versucht werden. Am sichersten ist es jedoch, die Daten von Patroni replizieren zu lassen.

--------

## Häufig gestellte Fragen {#faq}

- Beim Start meldet Patroni, dass es sich nicht an den PostgreSQL-Port binden kann.

  `listen_addresses` und `port` in `postgresql.conf` sowie `postgresql.listen` in `patroni.yml` überprüfen. Auch `pg_hba.conf` sollte diesen Zugriff erlauben.

- Nachdem Patroni zum Neustart des Knotens aufgefordert wurde, zeigt PostgreSQL die Fehlermeldung `could not open configuration file "/etc/postgresql/10/main/pg_hba.conf": No such file or directory` an.

  Je nach Verwaltung der PostgreSQL-Konfiguration kann dies verschiedene Ursachen haben. Wurde `postgresql.config_dir` angegeben, erzeugt Patroni die `pg_hba.conf` anhand der Einstellungen im Abschnitt [bootstrap](/de/docs/patroni/config/yaml#bootstrap_settings) nur bei der Initialisierung eines neuen Clusters. In diesem Szenario war `PGDATA` nicht leer, daher fand keine Initialisierung statt. Diese Datei muss bereits vorher vorhanden sein.
