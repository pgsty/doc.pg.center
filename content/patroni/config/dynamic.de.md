---
title: "Dynamische Konfigurationseinstellungen"
linkTitle: "Dynamische Konfiguration"
weight: 10
icon: fa-solid fa-sliders
description: "Im DCS gespeicherte dynamische Konfigurationseinstellungen, die clusterweit angewendet werden."
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/dynamic_configuration.html"
---

<a id="dynamic"></a>
Die dynamische Konfiguration wird im DCS (verteilter Konfigurationsspeicher) gespeichert und auf allen Clusterknoten angewendet.

Zum Ändern der dynamischen Konfiguration kann entweder das Werkzeug [patronictl_edit_config](/de/patroni/patronictl#patronictl_edit_config) oder die [REST API](/de/patroni/rest_api#rest_api) von Patroni verwendet werden.

- **loop_wait**: Anzahl der Sekunden, die die Schleife schläft. Standardwert: 10, kleinster zulässiger Wert: 1
- **ttl**: TTL für den Erwerb der Leader-Sperre (in Sekunden). Sie entspricht der Zeitspanne bis zum Beginn eines automatischen Failovers. Standardwert: 30, kleinster zulässiger Wert: 20
- **retry_timeout**: Zeitüberschreitung für Wiederholungsversuche bei DCS- und PostgreSQL-Operationen (in Sekunden). Kürzer andauernde DCS- oder Netzwerkprobleme führen nicht dazu, dass Patroni den Leader herabstuft. Standardwert: 10, kleinster zulässiger Wert: 3

> [!WARNING]
> Beim Ändern von **loop_wait**, **retry_timeout** oder **ttl** muss folgende Regel eingehalten werden:
>
> ```python
> loop_wait + 2 * retry_timeout <= ttl
> ```

- **maximum_lag_on_failover**: maximaler Rückstand eines Followers in Bytes, mit dem er noch an der Leader-Wahl teilnehmen darf.
- **primary_race_backoff**: verschiebt die Leader-Wahl auf Standbys um `primary_race_backoff` Sekunden, wenn die WAL-Replikation vom Primärserver noch voranschreitet. Dies minimiert unnötige Failovers durch ein kurzzeitig nicht reagierendes Patroni. Standardwert: 0 (deaktiviert).
- **maximum_lag_on_syncnode**: maximaler Rückstand eines synchronen Followers in Bytes, bevor er als fehlerhafter Kandidat gilt und durch einen fehlerfreien asynchronen Follower ersetzt wird. Bei mehr als einem Follower verwendet Patroni die höchste Replikat-LSN, andernfalls die aktuelle WAL-LSN des Leaders. Der Standardwert ist -1. Bei einem Wert von 0 oder weniger tauscht Patroni einen fehlerhaften synchronen Follower nicht aus. Den Wert ausreichend hoch wählen, damit Patroni bei hohem Transaktionsaufkommen synchrone Follower nicht häufig austauscht.
- **max_timelines_history**: maximale Anzahl der im DCS gespeicherten Einträge des Timeline-Verlaufs. Standardwert: 0. Bei 0 wird der vollständige Verlauf im DCS gespeichert.
- **primary_start_timeout**: Zeit, die ein Primärserver zur Erholung von Fehlern erhält, bevor ein Failover ausgelöst wird (in Sekunden). Der Standardwert beträgt 300 Sekunden. Bei 0 erfolgt das Failover nach Möglichkeit sofort nach Erkennung eines Absturzes. Bei asynchroner Replikation kann ein Failover zum Verlust von Transaktionen führen. Im schlimmsten Fall beträgt die Failover-Zeit bei Ausfall des Primärservers: loop_wait + primary_start_timeout + loop_wait. Ist primary_start_timeout jedoch null, beträgt sie nur loop_wait. Den Wert entsprechend der Abwägung zwischen Dauerhaftigkeit und Verfügbarkeit festlegen.
- **primary_stop_timeout**: Anzahl der Sekunden, die Patroni beim Stoppen von Postgres warten darf; wirkt nur bei aktiviertem synchronous_mode. Ist der Wert auf \> 0 gesetzt und synchronous_mode aktiviert, sendet Patroni SIGKILL an den postmaster, wenn der Stoppvorgang länger als primary_stop_timeout dauert. Den Wert entsprechend der Abwägung zwischen Dauerhaftigkeit und Verfügbarkeit festlegen. Ist der Parameter nicht gesetzt oder auf \<= 0 gesetzt, wird primary_stop_timeout nicht angewendet.
- **synchronous_mode**: aktiviert den synchronen Replikationsmodus. Mögliche Werte: `off`, `on`, `quorum`. In diesem Modus verwaltet der Leader `synchronous_standby_names`; nur der zuletzt bekannte Leader oder eines der synchronen Replikate darf an der Leader-Wahl teilnehmen. Der synchrone Modus gewährleistet, dass erfolgreich festgeschriebene Transaktionen bei einem Failover nicht verloren gehen. Dafür entfällt die Schreibverfügbarkeit, wenn Patroni die Dauerhaftigkeit der Transaktionen nicht sicherstellen kann. Einzelheiten enthält die [Dokumentation der Replikationsmodi](/de/patroni/replication_modes#replication_modes).
- **synchronous_mode_strict**: verhindert das Deaktivieren der synchronen Replikation, wenn keine synchronen Replikate verfügbar sind, und blockiert dadurch alle Schreibzugriffe von Clients auf den Primärserver. Im prioritätsbasierten synchronen Modus (`synchronous_mode: on`) setzt Patroni 4.1.5 `synchronous_standby_names` auf `*`, wenn kein geeignetes synchrones Replikat verfügbar ist. Einzelheiten enthält die [Dokumentation der Replikationsmodi](/de/patroni/replication_modes#replication_modes).
- **synchronous_node_count**: bei aktiviertem [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) verwaltet Patroni mit diesem Parameter die genaue Anzahl synchroner Standby-Instanzen und passt beim Hinzukommen und Ausscheiden von Mitgliedern den Zustand im DCS und den PostgreSQL-Parameter `synchronous_standby_names` an. Ist der Wert höher als die Anzahl geeigneter Knoten, wird er automatisch angepasst. Standardwert: `1`.
- **failsafe_mode**: aktiviert den [DCS-Failsafe-Modus](/de/patroni/dcs_failsafe_mode#dcs_failsafe_mode). Standardwert: `false`.
- **postgresql**:
  - **use_pg_rewind**: bestimmt, ob pg_rewind verwendet wird. Standardwert: `false`. Der Cluster muss mit `data page checksums` (Option `--data-checksums` für `initdb`) initialisiert worden sein und/oder `wal_log_hints` muss auf `on` gesetzt sein, andernfalls funktioniert `pg_rewind` nicht.
  - **use_slots**: bestimmt, ob Replikationsslots verwendet werden. Standardwert unter PostgreSQL 9.4+: `true`.
  - **recovery_conf**: zusätzliche Konfigurationseinstellungen, die beim Konfigurieren eines Followers in recovery.conf geschrieben werden. Ab PostgreSQL 12 gibt es keine recovery.conf mehr; dieser Abschnitt kann dennoch weiter verwendet werden, da Patroni dies transparent handhabt.
  - **parameters**: Konfigurationsparameter (GUCs) für Postgres im Format `{max_connections: 100, wal_level: "replica", max_wal_senders: 10, wal_log_hints: "on"}`. Viele davon sind für die Replikation erforderlich.
  - **parameters_primary**: (optional) rollenspezifische Parameterüberschreibungen für primary. Diese Werte werden mit den grundlegenden **parameters** zusammengeführt und überschreiben sie.
  - **parameters_replica**: (optional) rollenspezifische Parameterüberschreibungen für replica. Diese Werte werden mit den grundlegenden **parameters** zusammengeführt und überschreiben sie.
  - **parameters_standby_leader**: (optional) rollenspezifische Parameterüberschreibungen für standby_leader. Diese Werte werden mit den grundlegenden **parameters** zusammengeführt und überschreiben sie.
  - **pg_hba**: Liste der Zeilen, aus denen Patroni `pg_hba.conf` erzeugt. Patroni ignoriert diesen Parameter, wenn der PostgreSQL-Parameter `hba_file` auf einen anderen Wert als den Standardwert gesetzt ist.
    - **- host all all 0.0.0.0/0 md5**
    - **- host replication replicator 127.0.0.1/32 md5**: Eine solche Zeile ist für die Replikation erforderlich.
  - **pg_hba_primary**: (optional) rollenspezifische pg_hba-Einträge für primary. Sie ersetzen **pg_hba** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_hba** verwendet.
  - **pg_hba_replica**: (optional) rollenspezifische pg_hba-Einträge für replica. Sie ersetzen **pg_hba** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_hba** verwendet.
  - **pg_hba_standby_leader**: (optional) rollenspezifische pg_hba-Einträge für standby_leader. Sie ersetzen **pg_hba** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_hba** verwendet.
  - **pg_ident**: Liste der Zeilen, aus denen Patroni `pg_ident.conf` erzeugt. Patroni ignoriert diesen Parameter, wenn der PostgreSQL-Parameter `ident_file` auf einen anderen Wert als den Standardwert gesetzt ist.
    - **- mapname1 systemname1 pguser1**
    - **- mapname1 systemname2 pguser2**
  - **pg_ident_primary**: (optional) rollenspezifische pg_ident-Einträge für primary. Sie ersetzen **pg_ident** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_ident** verwendet.
  - **pg_ident_replica**: (optional) rollenspezifische pg_ident-Einträge für replica. Sie ersetzen **pg_ident** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_ident** verwendet.
  - **pg_ident_standby_leader**: (optional) rollenspezifische pg_ident-Einträge für standby_leader. Sie ersetzen **pg_ident** vollständig (keine Zusammenführung). Sind sie nicht definiert, wird **pg_ident** verwendet.
- **standby_cluster**: ist dieser Abschnitt definiert, soll ein Standby-Cluster initialisiert werden.
  - **host**: Adresse des entfernten Knotens
  - **port**: Port des entfernten Knotens
  - **primary_slot_name**: auf dem entfernten Knoten für die Replikation zu verwendender Slot. Dieser Parameter ist optional; der Standardwert wird aus dem Instanznamen abgeleitet (siehe Funktion `slot_name_from_member_name`).
  - **create_replica_methods**: geordnete Liste der Methoden, mit denen ein Standby-Leader vom entfernten Primärserver initialisiert werden kann. Sie kann sich von der in [postgresql_settings](/de/patroni/config/yaml#postgresql_settings) definierten Liste unterscheiden.
  - **restore_command**: Befehl zur Wiederherstellung von WAL-Einträgen des entfernten Primärservers auf den Knoten eines Standby-Clusters. Er kann sich von der in [postgresql_settings](/de/patroni/config/yaml#postgresql_settings) definierten Liste unterscheiden.
  - **archive_cleanup_command**: Bereinigungsbefehl für den Standby-Leader
  - **recovery_min_apply_delay**: Wartezeit vor dem tatsächlichen Anwenden von WAL-Einträgen auf einem Standby-Leader
- **member_slots_ttl**: Aufbewahrungszeit physischer Replikationsslots für heruntergefahrene Replikate. Standardwert: `30min`. Bei `0` bleibt das bisherige Verhalten erhalten (der Slot wird sofort entfernt, wenn der Mitgliedsschlüssel im DCS abläuft). Die Funktion wird erst ab PostgreSQL 11 unterstützt.
- **slots**: definiert permanente Replikationsslots. Diese Slots bleiben bei einem Switchover/Failover erhalten. Nicht vorhandene permanente Slots werden von Patroni erstellt. Ab PostgreSQL 11 werden permanente physische Slots auf allen Knoten angelegt und ihre Position alle **loop_wait** Sekunden vorgerückt. Bei PostgreSQL-Versionen vor 11 werden permanente physische Replikationsslots nur auf dem aktuellen Primärserver verwaltet. Logische Slots werden mit einem Neustart vom Primärserver auf einen Standby kopiert; anschließend wird ihre Position bei Bedarf alle **loop_wait** Sekunden vorgerückt. Das Kopieren der Dateien logischer Slots erfolgt über eine `libpq`-Verbindung mit den Zugangsdaten für rewind oder den Superuser (siehe Abschnitt **postgresql.authentication**). Die Position eines logischen Slots auf dem Replikat kann immer etwas hinter der des bisherigen Primärservers liegen. Daher sollte die Anwendung darauf vorbereitet sein, dass einige Nachrichten nach einem Failover erneut empfangen werden können. Am einfachsten lässt sich dies durch Verfolgen von `confirmed_flush_lsn` handhaben. Permanente Replikationsslots erfordern, dass **postgresql.use_slots** auf `true` gesetzt ist. Sind permanente logische Replikationsslots definiert, aktiviert Patroni automatisch `hot_standby_feedback`. Da das Failover logischer Replikationsslots unter PostgreSQL 9.6 und älter unsicher ist und PostgreSQL 10 einige wichtige Funktionen fehlen, wird diese Funktion nur unter PostgreSQL 11+ unterstützt.
  - **my_slot_name**: Name des permanenten Replikationsslots. Entspricht der Name des permanenten Slots dem Namen des aktuellen Knotens, wird er auf diesem Knoten nicht erstellt. Wird ein permanenter physischer Replikationsslot hinzugefügt, dessen Name dem eines Patroni-Mitglieds entspricht, stellt Patroni sicher, dass der erstellte Slot auch dann nicht entfernt wird, wenn das zugehörige Mitglied nicht mehr reagiert. Normalerweise würde Patroni den Slot in dieser Situation entfernen. Das kann nützlich sein, etwa wenn die von Mitgliedern verwendeten Replikationsslots während vorübergehender Ausfälle erhalten bleiben sollen oder bestehende Mitglieder in einen neuen Patroni-Cluster übernommen werden (siehe [Eine eigenständige Instanz in einen Patroni-Cluster überführen](/de/patroni/existing_data#existing_data)). Betreiber sollten jedoch darauf achten, solche Namensüberschneidungen nicht im DCS zu belassen, wenn der Slot nicht mehr benötigt wird, da sie den normalen Betrieb von Patroni beeinflussen.
    - **type**: Slot-Typ. Möglich sind `physical` oder `logical`. Bei einem logischen Slot müssen zusätzlich `database` und `plugin` definiert werden. Bei einem physischen Slot kann optional `cluster_type` definiert werden.
    - **database**: Name der Datenbank, in der logische Slots erstellt werden sollen.
    - **plugin**: Name des Plugins für den logischen Slot.
    - **cluster_type**: Clustertyp (`primary` oder `standby`), auf dem der Slot ausschließlich erstellt werden soll. Andernfalls wird er nicht erstellt beziehungsweise ein bereits vorhandener Slot gelöscht.
- **ignore_slots**: Liste von Gruppen von Replikationsslot-Eigenschaften; Patroni soll Slots ignorieren, die diesen Eigenschaften entsprechen. Diese Konfiguration/Funktion ist nützlich, wenn einige Replikationsslots außerhalb von Patroni verwaltet werden. Jede passende Teilmenge von Eigenschaften führt dazu, dass ein Slot ignoriert wird.
  - **name**: Name des Replikationsslots.
  - **type**: Slot-Typ. Möglich sind `physical` oder `logical`. Bei einem logischen Slot können zusätzlich `database` und/oder `plugin` definiert werden.
  - **database**: Datenbankname (beim Abgleich eines `logical`-Slots).
  - **plugin**: Plugin für logische Dekodierung (beim Abgleich eines `logical`-Slots).

Hinweis: **slots** ist eine Hashmap, **ignore_slots** dagegen ein Array. Beispiel:

```yaml
slots:
  permanent_logical_slot_name:
    type: logical
    database: my_db
    plugin: test_decoding
  permanent_physical_slot_name:
    type: physical
  ...
ignore_slots:
  - name: ignored_logical_slot_name
    type: logical
    database: my_db
    plugin: test_decoding
  - name: ignored_physical_slot_name
    type: physical
  ...
```

Hinweis: Unter PostgreSQL v11 oder neuer verwaltet Patroni physische Replikationsslots auf allen Knoten, die potenziell Leader werden können. Replikatknoten halten dadurch WAL-Segmente vor, die andere Knoten möglicherweise benötigen. Ist ein Knoten nicht verfügbar und läuft sein Mitgliedsschlüssel im DCS ab, wird der zugehörige Replikationsslot nach `member_slots_ttl` entfernt (Standardwert `30min`). Die Aufbewahrungszeit kann je nach Bedarf erhöht oder verringert werden. Bei einer statischen Clustertopologie (feste Anzahl von Knoten, deren Namen sich nie ändern) können alternativ permanente physische Replikationsslots mit den Namen der Knoten konfiguriert werden. So werden Slots nicht entfernt und WAL-Dateien nicht wiederverwendet, während ein Replikat vorübergehend ausgefallen ist:

```yaml
slots:
  node_name1:
    type: physical
  node_name2:
    type: physical
  node_name3:
    type: physical
  ...
```

> [!WARNING]
> Permanente Replikationsslots werden nur von `primary`/`standby_leader` zu Replikatknoten synchronisiert. Anwendungen sollen sie daher ausschließlich auf dem Leader-Knoten verwenden. Ihre Verwendung auf Replikatknoten führt zu unbegrenztem Wachstum von `pg_wal` auf allen anderen Knoten des Clusters. Ausgenommen sind physische Slots, deren Namen den Patroni-Mitgliedsnamen entsprechen (von Patroni erstellt und verwaltet). Diese werden zwischen allen Knoten synchronisiert, da sie für die Replikation untereinander verwendet werden.

> [!WARNING]
> Das Tag `nostream` auf einem Standby deaktiviert das Kopieren und Synchronisieren permanenter logischer Replikationsslots auf dem Knoten selbst sowie auf all seinen etwaigen kaskadierenden Replikaten.
