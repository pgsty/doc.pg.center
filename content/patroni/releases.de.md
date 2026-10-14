---
title: "Versionshinweise"
weight: 190
icon: fa-solid fa-scroll
description: "Chronologische Versionshinweise und Änderungshistorie von Patroni."
module: [PATRONI]
categories: [Referenz]
upstream_link: "https://patroni.readthedocs.io/en/latest/releases.html"
---

<a id="releases"></a>

--------

## Version 4.1.5 {#version-415}

Veröffentlicht am 2026-08-12

**Verbesserungen der Kompatibilität**

- Kompatibilität mit PostgreSQL 14.24, 15.19, 16.15, 17.11, 18.6 (Alexander Kukushkin)

  Die neue GUC `output_plugin_libraries` wurde hinzugefügt. Sie beschränkt die Ausgabe-Plugins für die logische Dekodierung.

**Verbesserungen**

- Verbindungsabbrüche der REST API auf Stufe `DEBUG` statt `WARNING` protokollieren (Kyle McLaren)

  Die üblichen Varianten von „Client hat die Verbindung während des Schreibens getrennt“ werden unterdrückt, ohne die Behandlung tatsächlicher Fehler zu beeinträchtigen, die nicht die Verbindung betreffen.

**Fehlerbehebungen**

- Ausrichtung bei der Validierung von `thread_stack_size` korrigieren (Sundong Kim)

  Der Wert `aligned` im Schemaeintrag für `thread_stack_size` wurde von `65535` auf `65536` korrigiert. Zuvor lehnte `patroni --validate-config` fast jeden realistischen Wert ab, einschließlich des Standardwerts `524288`, den der Daemon selbst anwendet.

- Bei der Validierung von `synchronous_mode` auch `'quorum'` und Zeichenketten mit booleschen Werten akzeptieren (Eray Araz)

  `patroni --validate-config` lehnte zuvor Werte für `synchronous_mode` wie `quorum` und boolesche Zeichenketten im PostgreSQL-Stil ab, die zur Laufzeit akzeptiert werden.

## Version 4.1.4 {#version-414}

Veröffentlicht am 2026-07-07

**Fehlerbehebungen**

- Die Umgebungsvariable `NOTIFY_SOCKET` vor Verwendung des Pakets `systemd` prüfen (Polina Bungina)

  Das Paket wird nur dann importiert und verwendet, wenn die Umgebungsvariable `NOTIFY_SOCKET` gesetzt ist. Dadurch wird die Ausnahme `FileNotFoundError: [Errno 2] No such file or directory` vermieden.

- Die Abfrage von `pg_replication_slots` vereinheitlichen (Polina Bungina)

  Eine fehlerhafte Behandlung der Werte `failover` und `synced` führte beim Entfernen fehlerhafter logischer Replikations-Slots zu `KeyError`-Ausnahmen.

- Versionsabhängige Authentifizierungsparameter bei der Konfigurationserzeugung berücksichtigen (Polina Bungina)

  Der Befehl `patroni --generate-config` entfernt anhand der über eine PostgreSQL-Verbindung ermittelten Version alle nicht anwendbaren Authentifizierungsparameter, die versehentlich aus der Umgebung übernommen wurden.

- `pg_rewind` behandeln, während eine PostgreSQL-Instanz als Standby startet (Alexander Kukushkin)

  Wenn eine PostgreSQL-Instanz läuft, aber noch keine Verbindungen annimmt, wird auf die Informationen von `pg_controldata` zurückgegriffen.

- Prometheus-Metriktyp für `patroni_postgres_timeline` korrigieren (Huseyin Demir)

  Die Metrik `patroni_postgres_timeline` wird als `gauge` statt als `counter` deklariert, da sie nicht immer monoton steigt (sie kann beispielsweise auf 0 zurückgesetzt werden, wenn eine PostgreSQL-Instanz nicht läuft).

- Watchdog erst stoppen, wenn alle Client-Backends vollständig beendet sind (Alexander Kukushkin)

  Wenn `primary_stop_timeout` kürzer als die minimale Watchdog-Zeitüberschreitung war und die Zeitüberschreitung beim Stoppen tatsächlich eintrat, deaktivierte Patroni zuvor den Watchdog, bevor alle Client-Backends beendet waren.

- Zeitüberschreitung einer Anweisung bei der Überwachungsabfrage behandeln (Alexander Kukushkin)

  Bei einer Zeitüberschreitung der Anweisung wird auf die zwischengespeicherte Rolle zurückgegriffen, um eine Herabstufung des Primärservers zu vermeiden. Außerdem wird `pg_stat_statements.track` für die Überwachungsabfrage zwingend auf `none` gesetzt, um aufwendige GC-Aufrufe von `pg_stat_statements` zu vermeiden.

- Von Patroni verwaltete Replikations-Slots mit `wal_status=lost` löschen (Alexander Kukushkin)

  Replikations-Slots mit `wal_status=lost` sind nicht mehr verwendbar. Patroni löscht solche Slots jetzt und erstellt sie bei Bedarf neu.

- Rollendarstellung im Validierungsfehler für patronictl-Mitglieder korrigieren (Polina Bungina)

  In der Ausnahmemeldung wird die korrekte Zeichenkettendarstellung verwendet. So werden fehlerhaft formatierte Meldungen wie `Error: No CtlPostgresqlRole.REPLICA among provided members` vermieden.

## Version 4.1.3 {#version-413}

Veröffentlicht am 2026-05-05

**Verbesserungen der Stabilität**

- Falsch bezeichneten etcd-Fehler korrekt behandeln (Ants Aasma)

  Aktuelle etcd-Versionen lösen den Fehler `Unknown` aus, wenn während der Aktualisierung der Lease der etcd-Leader verloren geht. Patroni überschreibt den gemeldeten Fehlercode jetzt mit `Unavailable`.

**Fehlerbehebungen**

- Version der ausführbaren Datei verwenden, wenn die Datei `PG_VERSION` fehlt (Polina Bungina)

  In manchen Fällen, etwa bei einem benutzerdefinierten Bootstrap, befindet sich die Datei `PG_VERSION` möglicherweise nicht im Datenverzeichnis. Patroni behandelte die Version in diesem Fall als 0.0, was in Teilen der versionsabhängigen Logik zu Problemen führte. Mit dieser Korrektur versucht Patroni in solchen Fällen, die Version über die ausführbare Datei zu ermitteln.

- Initialisierung der Protokollierung umstrukturieren, damit frühe Protokollmeldungen nicht verloren gehen (Alexander Kukushkin)

  `PatroniLogger` wird vor dem Laden von `Config` erstellt, um frühe Protokollmeldungen zu erfassen.

- `MONOTONIC_USEC` in die systemd-Benachrichtigung `RELOADING=1` aufnehmen (Alexander Kukushkin)

  systemd 257+ verlangt bei Diensten mit `Type=notify-reload` neben `RELOADING=1` auch `MONOTONIC_USEC`. Ohne diese Angabe bleibt `systemctl reload` unbegrenzt hängen.

**Verbesserungen**

- Crash-Recovery im Einzelbenutzermodus überspringen, wenn `backup_label` vorhanden ist (Vadim Ponomarev)

  Beim Start eines Replikats, das aus einem externen Backup wiederhergestellt wurde (ohne benutzerdefinierte Bootstrap-Methode), wird die Crash-Recovery im Einzelbenutzermodus übersprungen. PostgreSQL übernimmt sie stattdessen beim normalen Start.

- Bei Ausführung unter `systemd` ohne das Paket `python-systemd` warnen (Alexander Kukushkin)

  Statt beim Start „systemd integration is not supported“ zu protokollieren, wird auf `NOTIFY_SOCKET` geprüft. Eine Warnung erfolgt nur, wenn Patroni tatsächlich unter `systemd` läuft und das Paket `python-systemd` nicht installiert ist.

## Version 4.1.2 {#version-412}

Veröffentlicht am 2026-04-21

**Verbesserungen der Systemd-Unterstützung**

- Unterstützung für den systemd-Unit-Typ `notify-reload` hinzufügen (Ronan Dunklau)

  Durch die Benachrichtigungen `RELOADING=1` und `READY=1` an systemd kann `systemctl reload` warten, bis Patroni das Neuladen der Konfiguration tatsächlich verarbeitet hat.

- Beim Herunterfahren die Benachrichtigung `STOPPING=1` an systemd senden (Alexander Kukushkin)

  Patroni benachrichtigt systemd jetzt entsprechend dem systemd-notify-Protokoll korrekt darüber, dass es heruntergefahren wird.

- Benachrichtigungen von PostgreSQL an systemd verhindern (Alexander Kukushkin)

  `NotifyAccess=all` wurde aus der systemd-Unit-Beispieldatei entfernt. Beim Start von PostgreSQL wird `NOTIFY_SOCKET` aus der Umgebung gefiltert, damit PostgreSQL weder `READY=1` noch `STOPPING=1` an systemd sendet. Bei der Übernahme einer PostgreSQL-Instanz, die vor Patroni gestartet wurde und bereits `NOTIFY_SOCKET` besitzt, wird während des Herunterfahrens von PostgreSQL erneut `READY=1` gesendet, um dessen `STOPPING=1` entgegenzuwirken.

## Version 4.1.1 {#version-411}

Veröffentlicht am 2026-04-08

**Verbesserungen der Stabilität**

- Kompatibilität mit Änderungen an Threads in python 3.11+ (Alexander Kukushkin)

  Das Starten und Stoppen von Threads zur Laufzeit wird vermieden. Thread-Pools für die REST API und für die Ausführung asynchroner Aufgaben wurden eingeführt. Die globalen Einstellungen `thread_pool_size` und `restapi.thread_pool_size` sind konfigurierbar.

- Kompatibilität mit python 3.14 (Alexander Kukushkin)

  Tests werden mit python 3.14 ausgeführt und Kompatibilitätsprobleme behoben.

- Kompatibilität mit den etcd-Sicherheitskorrekturen in v3.6.9, v3.5.28 und v3.4.42 (Alexander Kukushkin)

  Diese etcd-Versionen behoben CVEs und änderten das Verhalten so, dass das Lesen der Clustertopologie und Lease-Keepalives ohne Authentifizierung nicht mehr zulässig sind. Patroni berücksichtigt dies jetzt durch Authentifizierung bei der Erkennung von Mitgliedern und bei Lease-Keepalives, erneute Authentifizierung bei Authentifizierungsfehlern sowie entsprechende Wiederholungen von Anfragen.

- Verbesserte Fehlerbehandlung für etcd3 (Alexander Kukushkin)

  Fehlerhafte JSON-Antworten werden behandelt, JSON-Fehler flexibler ausgewertet und interne etcd-Fehler besser gemeldet.

**Fehlerbehebungen**

- Leader-Aktualisierung bei vorübergehendem Kubernetes-Fehler `403` wiederholen (Sophia Ruan, Alexander Kukushkin)

  Wenn die Kubernetes-API vorübergehend `403 Permission Denied` zurückgibt (etwa bei vorübergehenden RBAC-Problemen), prüft Patroni jetzt, ob der aktuelle Knoten weiterhin Leader ist, und wiederholt die Leader-Aktualisierung innerhalb von `retry_timeout`, statt den Knoten sofort herabzustufen.

- Problem beim Umbenennen des Leader-Knotens im synchronen Modus während einer Pause beheben (Alexander Kukushkin)

  Der Schlüssel `/sync` wurde nach dem Umbenennen des Leader-Knotens mit einem Patroni-Neustart während einer Pause (ohne Postgres-Neustart) nicht aktualisiert. Dadurch konnte Patroni nach dem nächsten Neustart ohne Pause keine Hochstufung durchführen.

- `pg_rewind`-Prüfung auslösen, wenn derselbe Primärserver seine Timeline erhöht hat (Alexander Kukushkin)

  Eine solche Timeline-Erhöhung kann durch Crash-Recovery im Einzelbenutzermodus mit anschließender Hochstufung nach Übernahme des Leader-Schlüssels entstehen, während andere Replikatknoten vom DCS isoliert sind. In diesem Fall lösten die Replikatknoten den `pg_rewind`-Zustandsautomaten nicht aus, weil sich der Leader und damit `primary_conninfo` nicht geändert hatten.

- Superuser-Passwort beim Bootstrap mit `initdb` nur schreiben, wenn es nicht leer ist (Michael Banck)

  Das Schreiben eines leeren Passworts beim Bootstrap mit `initdb` führte zu Problemen.

- Fehler bei `failover_priority` mit `synchronous_mode=on` beheben (Alexander Kukushkin)

  Werte von `tag.failover_priority` wurden ignoriert, wenn `synchronous_node_count > 1` galt.

- Fehler beim Passwortvergleich in `primary_conninfo` beheben (Alexander Kukushkin)

  Ab PostgreSQL 10 verwendet Patroni in `primary_conninfo` eine Passwortdatei. Nach einer Änderung des Replikationspassworts in der YAML-Dateikonfiguration mit anschließendem Neuladen aktualisierte Patroni diese Passwortdatei nicht.

- Replikat mit dem Tag `nofailover` im Pause-Modus nicht neu starten (Alexander Kukushkin)

  Patroni startete zuvor ein manuell heruntergefahrenes PostgreSQL-Replikat im Pause-Modus, wenn dessen Tag `nofailover` auf `true` gesetzt war.

- `check_recovery_conf()` korrigieren, wenn PostgreSQL gerade startet (Alexander Kukushkin)

  Bei PostgreSQL v12 und neuer kann `pg_settings` nicht abgefragt werden, solange der Server noch startet und keine Verbindungen annimmt. Fehlende Recovery-Parameter werden jetzt beim Schreiben von `postgresql.conf` dem internen Zustand hinzugefügt. Außerdem wurde die Prüfung `Postgresql.is_starting()` in `Ha.is_healthiest_node()` wiederhergestellt.

- Benutzeroptionen im Dictionary-Format für `initdb`/`basebackup` validieren (m4rrypro)

  Wenn Optionen für `initdb` oder `basebackup` als Dictionary statt als Liste angegeben wurden, wurde die Validierung durch `option_is_allowed()` umgangen, wodurch gesperrte Optionen verwendet werden konnten.

- Serverseitige Komprimierung für die Option `basebackup` zulassen (m4rrypro)

  Die Option `compress` war für `basebackup` vollständig gesperrt. Seit PostgreSQL 15 ist serverseitige Komprimierung jedoch sinnvoll und funktioniert transparent mit dem Plain-Format. Clientseitige Komprimierung wird weiterhin abgelehnt.

- PostgreSQL-Konfiguration während eines benutzerdefinierten Bootstraps nicht neu laden (Alexander Kukushkin)

  Ein benutzerdefinierter Bootstrap kann komplex sein und PostgreSQL mehrfach starten und stoppen. Das Neuladen der PostgreSQL-Konfiguration während dieses Vorgangs konnte zu unerwartetem Verhalten führen.

- Prüfen, ob `postgresql.parameters` ein Dictionary ist (Alexander Kukushkin)

  Eine neue Konfiguration wird verworfen, wenn `postgresql.parameters` kein Dictionary ist.

## Version 4.1.0 {#version-410}

Veröffentlicht am 2025-09-23

**Neue Funktionen**

- Unterstützung für den systemd-Unit-Typ „notify“ hinzufügen (Ronan Dunklau)

  Ohne den Unit-Typ notify ist es möglich, Patroni zu starten und ihm unmittelbar über systemd ein SIGHUP-Signal zu senden. Dadurch wird Patroni beendet, bevor es seine Signal-Handler einrichten konnte.

- Informationen zu empfangener und wiedergegebener LSN sowie zum jeweiligen Rückstand in API und ctl bereitstellen (Polina Bungina)

  Der Patroni-REST-API-Endpunkt `/cluster` und der Befehl `patronictl list` liefern jetzt für jedes Replikatmitglied die empfangene LSN, die wiedergegebene LSN, den Empfangsrückstand und den Wiedergaberückstand.

- Saubere Herabstufung zu einem Standby-Cluster sicherstellen (Polina Bungina)

  Das Hinzufügen des Abschnitts [standby_cluster](/de/patroni/standby_cluster#standby_cluster) in der dynamischen Konfiguration führt zu einer sauberen Herabstufung des Clusters.

- Die Befehle `patronictl demote-cluster` und `promote-cluster` implementieren (Polina Bungina)

  Die neuen Befehle zur Herabstufung und Hochstufung eines Clusters übernehmen sowohl die Bearbeitung der dynamischen Konfiguration als auch die Prüfung des Ergebnisstatus.

- Tag `sync_priority` implementieren (Polina Bungina)

  Dieser Parameter steuert die Priorität eines Mitglieds bei der Auswahl synchroner Replikate, wenn [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) auf `on` gesetzt ist.

- Option `--print` für `--validate-config` implementieren (Polina Bungina)

  Nach erfolgreicher Validierung wird die lokale Konfiguration ausgegeben, einschließlich der durch Umgebungsvariablen überschriebenen Einstellungen.

- `kubernetes.bootstrap_labels` implementieren (Polina Bungina)

  Mit dieser Funktion können Labels definiert werden, die dem Pod eines Mitglieds in den Zuständen `initializing new cluster`, `running custom bootstrap script`, `starting after custom bootstrap` oder `creating replica` zugewiesen werden.

- Konfigurationsoption zur Unterdrückung doppelter Heartbeat-Protokollmeldungen hinzufügen (Michael Morris)

  Ist die Option auf `true` gesetzt, werden aufeinanderfolgende identische Heartbeat-Protokollmeldungen nicht ausgegeben.

- Optionales Attribut `cluster_type` für permanente Replikations-Slots hinzufügen (Michael Banck)

  Damit lässt sich festlegen, ob ein bestimmter permanenter Replikations-Slot immer oder nur auf einem Primär- beziehungsweise Standby-Cluster erstellt werden soll.

- HTTP-Server-Header konfigurierbar machen (David Grierson)

  Der Konfigurationsparameter `restapi.server_tokens` wurde eingeführt. Er ermöglicht es, die im HTTP-Server-Header offengelegten Informationen einzuschränken.

- Readiness-Prüfungen der API für die Replikation auf Replikatmitgliedern implementieren (Ants Aasma)

  Die bisherige Implementierung betrachtete Replikate als bereit, sobald PostgreSQL gestartet war. Mit dieser Änderung gilt ein Replikat-Pod erst dann als bereit, wenn PostgreSQL repliziert und nicht zu weit hinter dem Leader zurückliegt.

**Verbesserungen**

- Protokollstufe für Fehler bei der Watchdog-Konfiguration senken (Ants Aasma)

  Die Protokollzeile `Could not activate Linux watchdog device` wird auf der Debug-Stufe ausgegeben, sofern der Watchdog nicht im Modus `required` konfiguriert ist. Zuvor wurde sie auf der Info-Stufe ausgegeben.

- `written_lsn` und `latest_end_lsn` aus `pg_stat_wal_receiver` nutzen (Alexander Kukushkin)

  `written_lsn`, die tatsächliche Schreib-LSN, wird jetzt dem von `pg_last_wal_receive_lsn()` gelieferten Wert vorgezogen, der tatsächlich die Flush-LSN ist. `latest_end_lsn` verweist auf die auf dem Quellhost dauerhaft auf den Datenträger geschriebene WAL-Position. Bei einem Primärserver ermöglicht dies eine genauere Berechnung des Wiedergaberückstands, da die im DCS gespeicherten Werte nur alle `loop_wait` Sekunden aktualisiert werden.

- Interaktionen mit Slots vermeiden, die mit der Option `failover=true` erstellt wurden (Alexander Kukushkin)

  Diese Änderung ist erforderlich, damit die Funktion für logische Failover-Slots vollständig funktioniert.

- PostgreSQL-Zustand zum REST-API-Endpunkt `/metrics` hinzufügen (Ivan Filianin)

  Informationen zum Zustand der PostgreSQL-Instanz sind jetzt in der Ausgabe des REST-API-Endpunkts `/metrics` im Prometheus-Format verfügbar.

--------

## Version 4.0.7 {#version-407}

Veröffentlicht am 2025-09-22

**Neue Funktionen**

- Unterstützung für PostgreSQL 18 RC1 hinzufügen (Alexander Kukushkin)

  Die Validierungsregeln für GUCs wurden erweitert. Patroni behandelt den neuen Hintergrund-Worker für I/O jetzt korrekt.

**Fehlerbehebungen**

- Mögliches Problem bei der Auflösung von localhost zu IPv6 unter Windows beheben (András Váczi)

  Bei der Konfiguration von `listen_addresses` in PostgreSQL beschränken `0.0.0.0` oder `127.0.0.1` die Adressen, auf denen PostgreSQL lauscht auf IPv4 und schließen IPv6 aus. Auf typischen Windows-Systemen wird `localhost` jedoch häufig standardmäßig zur IPv6-Adresse `::1` aufgelöst. Um Kompatibilität sicherzustellen, konfiguriert Patroni PostgreSQL auf Windows-Systemen jetzt so, dass es auf `127.0.0.1` statt auf `localhost` lauscht.

- Globale Konfiguration nur zurückgeben, wenn der Schlüssel `/config` im DCS vorhanden ist (Alexander Kukushkin)

  Die Patroni-REST-API gab eine leere Konfiguration zurück, statt einen Fehler auszulösen, wenn der Schlüssel `/config` im DCS fehlte.

- Fehler beheben, durch den bei nicht verfügbarem etcd der Failsafe-Modus nicht ausgelöst wurde (Alexander Kukushkin)

  Patroni behandelte `etcd3`-Ausnahmen nicht immer korrekt, weshalb der Failsafe-Modus nicht ausgelöst wurde.

- Deadlock durch erneuten Eintritt in einen Signal-Handler beheben (Waynerv)

  Bei Patroni in einem Docker-Container mit `PID=1` kam es in bestimmten Fällen nach dem Empfang von `SIGCHLD` zu einem Deadlock.

- Einen (permanenten) physischen Slot neu erstellen, wenn er kein WAL reserviert (Israel Barth Rubio)

  Permanente physische Replikations-Slots, die außerhalb der Verwaltung durch Patroni ohne WAL-Reservierung erstellt wurden, verursachten den Fehler `replication slot cannot be advanced`. Um dies zu vermeiden, erstellt Patroni solche Slots jetzt neu.

- Watch-Abbruchmeldungen in `etcd3` korrekt behandeln (Alexander Kukushkin)

  Wenn `etcd3` eine Abbruchmeldung an den Watch-Kanal sendet, wird die Verbindung nicht geschlossen. Dadurch verwendet Patroni veraltete Daten. Patroni löst dies jetzt, indem es die Schleife zum Lesen der in Blöcken übertragenen Antwort abbricht und die Verbindung auf seiner Seite schließt.

- Mit `pyopenssl` umschlossene `HTTPConnection`-Sockets behandeln (Alexander Kukushkin)

  Patroni verwendete die durch `python-etcd` erzwungenen `pyopenssl`-Schnittstellen nicht korrekt.

**Verbesserungen der Dokumentation**

- Hinweise zu Clustern mit 2 Knoten verbessern (Nikolay Samokhvalov)

  Das Verhalten beim Failover und die Anforderungen an den DCS wurden präzisiert.

--------

## Version 4.0.6 {#version-406}

Veröffentlicht am 2025-06-06

**Fehlerbehebungen**

- Fehler beim Failover von einem Leader mit höherer Priorität beheben (Alexander Kukushkin)

  Patroni ignoriert den früheren Leader mit höherer Priorität, wenn dieser dieselbe `LSN` wie der aktuelle Knoten meldet.

- Berechtigungen für außerhalb von `PGDATA` erstellte Dateien `postgresql.conf` korrigieren (Michael Banck)

  Beim Erstellen der Datei `postgresql.conf` außerhalb des Verzeichnisses `PGDATA` wird der systemweite umask-Wert berücksichtigt.

- Fehler beim Switchover mit `synchronous_mode=quorum` beheben (Alexander Kukushkin)

  Wenn ein Kandidat angegeben ist, werden die Quorum-Anforderungen nicht geprüft.

- Veraltete etcd-Knoten durch Vergleich der Cluster-Amtszeit ignorieren (Alexander Kukushkin)

  Der zuletzt bekannte Wert von „raft_term“ des etcd-Clusters wird gespeichert und beim Ausführen von Client-Anfragen mit dem von einem etcd-Knoten gemeldeten Wert von „raft_term“ verglichen.

- PostgreSQL-Konfigurationsdateien bei `SIGHUP` aktualisieren (Alexander Kukushkin)

  Zuvor ersetzte Patroni PostgreSQL-Konfigurationsdateien nur, wenn eine Änderung an der globalen oder lokalen Konfiguration erkannt wurde.

- Von `etcd3` ausgelöste Ausnahme `Unavailable` korrekt behandeln (Alexander Kukushkin)

  Patroni wiederholte solche Anfragen zuvor auf demselben `etcd3`-Knoten. Der Wechsel zu einem anderen Knoten ist jedoch die bessere Strategie.

- Lease-Behandlung von `etcd3` verbessern (Alexander Kukushkin)

  Patroni erneuert die `etcd3`-Lease mindestens einmal pro HA-Schleifendurchlauf.

- Bei Statuscode 409 während des Versuchs, den Leader-Lock zu erwerben, die Annotationen erneut prüfen (Alexander Kukushkin)

  Dasselbe Verhalten wie beim Lesen des Leader-Objekts in Patroni-Version 4.0.3 wurde implementiert.

- `replay_lsn` beim Vorrücken von Slots berücksichtigen (Polina Bungina)

  Slots auf Replikaten werden nicht über `replay_lsn` hinaus vorgerückt. Außerdem wird der Slot bis zur Position `replay_lsn` vorgerückt, wenn diese bereits größer als die `confirmed_flush_lsn` dieses Slots auf dem Replikat ist, das Replikat aber die tatsächliche `LSN`, an der sich der Slot auf dem Primärserver befindet, noch nicht wiedergegeben hat.

- Ausführung von `CHECKPOINT` nach einer Hochstufung sicherstellen (Alexander Kukushkin)

  Es konnte vorkommen, dass die Checkpoint-Aufgabe beim Herabstufen nicht zurückgesetzt wurde, weil `CHECKPOINT` noch nicht abgeschlossen war. Dadurch wurde beim Auslösen der nächsten Hochstufung ein veraltetes `result` verwendet.

- Gleichzeitige „offline“-Herabstufungen vermeiden (Alexander Kukushkin)

  Bei langsamem Herunterfahren konnte die nächste Heartbeat-Schleife erneut die Methode zur DCS-Fehlerbehandlung aufrufen. Dies führte zur Warnung `AsyncExecutor is busy, demoting from the main thread` und zu einem erneuten Start der Offline-Herabstufung.

- Wert von `data_dir` vor dem Umbenennen des Datenverzeichnisses nach fehlgeschlagener Initialisierung normalisieren (Waynerv)

  Ein abschließender Schrägstrich im Parameterwert `data_dir` unterbricht dadurch nicht mehr das Umbenennen nach einer fehlgeschlagenen Initialisierung.

- Prüfen, ob `synchronous_standby_names` den erwarteten Wert enthält (Alexander Kukushkin)

  Der Zustandsautomat für synchrone Replikation ohne Quorum prüfte zuvor den tatsächlichen Wert von `synchronous_standby_names` nicht. Dies führte dazu, dass ein veralteter Wert von `synchronous_standby_names` verwendet wurde, wenn `pg_stat_replication` eine Teilmenge von `synchronous_standby_names` war.

--------

## Version 4.0.5 {#version-405}

Veröffentlicht am 2025-02-20

**Verbesserungen der Stabilität**

- Kompatibilität mit `python-json-logger>=3.1` (Alexander Kukushkin)

  Die durch Verwendung der alten API erzeugten Warnungen wurden beseitigt.

- Kompatibilität mit Python 3.13 (Alexander Kukushkin)

  Tests werden mit Python 3.13 ausgeführt.

- Kompatibilität mit `pyinstaller>=4.4` (Joe Jensen)

  Wenn das Attribut `toc` von `pyinstaller` fehlt, wird auf das standardmäßige `iter_modules` zurückgegriffen.

- Probleme bei der Unterstützung von PostgreSQL 9.5 behoben (Alexander Kukushkin)

  - Das Ausgabeformat von `pg_rewind` wird korrekt behandelt.
  - Es wird berücksichtigt, dass das Format von `synchronous_standby_names` keine Angabe von „num“ unterstützt.

- Kompatibilität mit den neuesten Änderungen in `urlparse` (Alexander Kukushkin)

  `urlparse` akzeptiert keine URLs mit mehreren Hosts und den Zeichen `[]` mehr. Um das Problem zu umgehen, werden nach Möglichkeit die nativen Wrapper von `PQconninfoParse()` aus `libpq` verwendet. Die eigene Implementierung wird nur noch für ältere `psycopg2`-Versionen genutzt, die gegen eine veraltete `libpq`-Version gelinkt sind.

**Fehlerbehebungen**

- Bei der Neustartbestätigung nur die tatsächlich neu zu startenden Mitglieder angezeigt (András Váczi)

  Zuvor listete die Bestätigung bei `patronictl restart <clustername> --pending` alle Mitglieder auf, unabhängig davon, ob bei ihnen ein Neustart ausstand.

- Lang laufende Aufgaben beim Stoppen von Patroni abgebrochen und Datenverzeichnis bei fehlgeschlagenem Replikat-Bootstrap entfernt (Alexander Kukushkin)

  Zuvor konnte Patroni während eines Replikat-Bootstraps stoppen, während `pg_basebackup` / `wal-g` / `pgBackRest` / `barman` oder ähnliche Programme weiterliefen.

- Clusternamen mit Schrägstrich in `patronictl edit-config` korrekt behandelt (Antoni Mur)

  Ein Schrägstrich in `cluster_name` wird durch einen Unterstrich ersetzt.

- Zu frühes Löschen physischer Slots vermieden (Alexander Kukushkin)

  Nach einem Failover wird das Entfernen physischer Replikationsslots mit `xmin` aufgeschoben: auf dem neuen Primärserver bis zu dessen Hochstufung, auf Replikaten bis ein Leader im Cluster vorhanden ist.

- Alle von subprocess in `controldata()` ausgelösten Ausnahmen behandelt (Alexander Kukushkin)

  Patroni behandelte nicht alle Ausnahmen korrekt, die beim Aufruf des Werkzeugs `pg_controldata` auftreten können.

- Fehler behoben, durch den der Slot für einen früheren Leader beim Failover nicht erhalten blieb (Alexander Kukushkin)

  Patroni verlässt sich nicht mehr fälschlich auf die Anwesenheit von Mitgliedern im DCS, während beim Failover der Schlüssel `/member` des früheren Leaders genau zur selben Zeit abläuft.

- Mehrere Fehler im Quorum-Zustandsautomaten behoben (Alexander Kukushkin)

  - Bei der Prüfung, ob funktionsfähige Knoten für die Leader-Wahl vorhanden sind, müssen vor der Herabstufung die Quorum-Anforderungen berücksichtigt werden. Andernfalls kann der frühere Leader in Recovery gelangen und nur von asynchronen Knoten umgeben sein.
  - `QuorumStateResolver` behandelte den Fall nicht korrekt, dass ein Replikatknoten schnell beitrat und sich wieder trennte.

**Verbesserungen**

- Fehlermeldung für eine leere Konfigurationsdatei oder einen Inhalt, der kein Dictionary ist, verbessert (Julian)

  Bei der Prüfung, ob die Patroni-Konfigurationsdatei ein gültiges `Mapping`-Objekt enthält, wird eine aussagekräftigere Ausnahme ausgelöst.

--------

## Version 4.0.4 {#version-404}

Veröffentlicht am 2024-11-22

**Verbesserungen der Stabilität**

- Kompatibilität mit dem Modul `py-consul` hinzugefügt (Alexander Kukushkin)

  Das Modul `python-consul` wird seit Langem nicht mehr gepflegt; `py-consul` ist der offizielle Ersatz. Die Rückwärtskompatibilität mit python-consul bleibt erhalten.

- Kompatibilität mit dem Modul `prettytable>=3.12.0` hinzugefügt (Alexander Kukushkin)

  Warnungen zu veralteten Funktionen wurden behoben.

- Kompatibilität mit dem Modul `ydiff==1.4.2` (Alexander Kukushkin)

  Kompatibilitätsprobleme mit der neuesten Version wurden behoben, die Version in `requirements.txt` eingeschränkt und ein Kompatibilitätstest für die neueste Version eingeführt.

**Fehlerbehebungen**

- Callback `on_role_change` nach fehlgeschlagener Recovery des Primärservers ausgeführt (Polina Bungina, Alexander Kukushkin)

  `on_role_change` wird zusätzlich für einen Primärserver aufgerufen, der nach einem Absturz nicht starten konnte. Dadurch steigt die Wahrscheinlichkeit, dass der Callback ausgeführt wird, auch wenn der anschließende Start als Replikat fehlschlägt.

- Thread-Leck in `patronictl list -W` behoben (Alexander Kukushkin)

  Das DCS-Instanzobjekt wird zwischengespeichert, um das Thread-Leck zu vermeiden.

- Nur unterstützte Parameter in die Verbindungszeichenkette geschrieben (Alexander Kukushkin)

  Patroni übergab zuvor in neueren Versionen eingeführte Parameter in der Verbindungszeichenkette, was zu Verbindungsfehlern führte.

--------

## Version 4.0.3 {#version-403}

Veröffentlicht am 2024-10-18

**Fehlerbehebungen**

- `pgaudit` bei der Benutzererstellung deaktiviert, damit Passwörter nicht offengelegt werden (kviset)

  Bei aktivierter Erweiterung `pgaudit` protokollierte Patroni bei der Erstellung die Passwörter für `superuser`, `replication` und `rewind`.

- Problem bei gemischten Installationen mit Primärserver vor Patroni v4 und Replikaten mit v4+ behoben (Alexander Kukushkin)

  Wenn auf dem Leader eine Patroni-Version vor 4.0.0 läuft, wird `xlog_location` aus dem Schlüssel `/members` verwendet, statt die Slot-Position eines Mitglieds aus `/status` zu lesen. Das bisherige Verhalten führte zur Ansammlung von WAL auf Replikaten.

- Gültige PostgreSQL-GUCs ohne Patroni-Validator nicht ignoriert (Polina Bungina)

  Wenn eine GUC keinen Patroni-Validator besitzt, aber tatsächlich gültig ist, wird sie weiterhin anhand von `postgres --describe-config` geprüft.

**Verbesserungen**

- Bei Statuscode 409 beim Lesen des Leader-Objekts in K8s die Annotationen erneut geprüft (Alexander Kukushkin)

  Eine zusätzliche Aktualisierung wird vermieden, wenn Patroni die `PATCH`-Anfrage abgebrochen hat, diese das Ziel aber erfolgreich aktualisiert hat.

- Clientseitige Verbindungsoption `sslnegotiation` unterstützt (Alexander Kukushkin)

  `sslnegotiation` wurde der endgültigen PostgreSQL-Version 17 hinzugefügt.

--------

## Version 4.0.2 {#version-402}

Veröffentlicht am 2024-09-17

**Fehlerbehebungen**

- Ausnahmen beim Auffinden von Dateien zur Konfigurationsvalidierung behandelt (Alexander Kukushkin)

  Verzeichnisse werden übersprungen, wenn Patroni keine ausreichenden Berechtigungen zum Auflisten besitzt.

- Inaktive physische Hot-Replikationsslots halten kein `xmin` mehr fest (Alexander Kukushkin, Polina Bungina)

  Seit Version 3.2.0 erstellt Patroni auf Replikaten physische Replikationsslots für alle Mitglieder und rückt sie regelmäßig mit `pg_replication_slot_advance()` vor. Ist jedoch aus irgendeinem Grund `hot_standby_feedback` aktiviert und wird der Primärserver zum Replikat herabgestuft, wird der `NOT NULL`-Wert von `xmin` der nun inaktiven Slots an den neuen Primärserver zurückgemeldet. Dadurch rückt der `xmin`-Horizont nicht vor und vacuum kann tote Tupel nicht entfernen. Mit dieser Korrektur erstellt Patroni physische Replikationsslots neu, die inaktiv sein sollten, aber einen `NOT NULL`-Wert für `xmin` besitzen.

- Unbehandelten `DCSError` während der Startphase behoben (Waynerv)

  Vor der Prüfung auf Eindeutigkeit des Knotennamens wird die Verbindung zum DCS sichergestellt.

- GUCs aus `CMDLINE_OPTIONS` beim Abfragen von `pg_settings` ausdrücklich eingeschlossen (Alexander Kukushkin)

  Wenn Patroni einen laufenden Standby übernimmt, werden alle GUCs wiederhergestellt, die als Befehlszeilenparameter an postmaster übergeben werden. Dies ergänzt die Fehlerbehebung aus Patroni 3.2.2.

- Fehler in der Anführungszeichenlogik von `synchronous_standby_names` behoben (Alexander Kukushkin)

  Laut PostgreSQL-Dokumentation müssen die Schlüsselwörter `ANY` und `FIRST` in doppelte Anführungszeichen gesetzt werden. Patroni tat dies zuvor nicht.

- Überschreitung des Wertebereichs für Verbindungs-Keepalives behoben (hadizamani021)

  Der anhand von `ttl` berechnete Wert der Option `keepalive` überschreitet nicht mehr den für die aktuelle Plattform zulässigen Höchstwert.

--------

## Version 4.0.1 {#version-401}

Veröffentlicht am 2024-08-30

**Fehlerbehebung**

- Patroni erstellte unnötige Replikationsslots für sich selbst (Alexander Kukushkin)

  Dies geschah, wenn `name` Großbuchstaben oder Sonderzeichen enthielt.

--------

## Version 4.0.0 {#version-400}

Veröffentlicht am 2024-08-29

> [!WARNING]
> - Diese Version schließt die Ablösung des Begriffs „master“ durch „primary“ ab. Damit sind einige inkompatible Änderungen verbunden; lesen Sie die Versionshinweise sorgfältig. Das Upgrade auf Patroni 4+ funktioniert nur zuverlässig, wenn Patroni 3.1.0 oder neuer verwendet wird. Ein direktes Upgrade von einer älteren Version auf 4+ ist möglich, kann aber zu unerwartetem Verhalten führen, wenn der Primärserver ausfällt, während die übrigen Knoten andere Patroni-Versionen ausführen.

**Inkompatible Änderungen**

- Beim Entfernen des nicht inklusiven Begriffs „master“ aus dem Patroni-Code wurden folgende inkompatible Änderungen eingeführt:
  - Auf Kubernetes setzt Patroni das Label `role` standardmäßig auf `primary`. Um das bisherige Verhalten beizubehalten und Ausfallzeiten oder langwierige, komplexe Migrationen zu vermeiden, können die Parameter `kubernetes.leader_label_value` und `kubernetes.standby_leader_label_value` auf `master` gesetzt werden. Weitere Informationen finden sich [hier](/de/patroni/kubernetes#kubernetes_role_values).
  - Die Patroni-Rolle wird als `primary` statt als `master` in den DCS geschrieben.
  - Die von der Patroni-REST-API zurückgegebene Rolle wurde von `master` in `primary` geändert.
  - Die Patroni-REST-API akzeptiert `role=master` in Anfragen an die Endpunkte `/switchover`, `/failover` und `/restart` nicht mehr.
  - Der REST-API-Endpunkt `/metrics` meldet die Metrik `patroni_master` nicht mehr.
  - [patronictl](/de/patroni/patronictl#patronictl) akzeptiert die Option `--master` für keinen Befehl mehr. Stattdessen sollten `--leader` oder `--primary` verwendet werden.
  - Die Option `no_master` in der deklarativen Konfiguration benutzerdefinierter Methoden zur Replikaterstellung wird nicht mehr als besondere Option behandelt; verwenden Sie stattdessen `no_leader`.
  - Das Skript `patroni_wale_restore` akzeptiert die Option `--no_master` nicht mehr.
  - Das Skript `patroni_barman` akzeptiert die Option `--role=master` nicht mehr.
  - Allen Callback-Skripten wird bei der Ausführung die Option `role=primary` statt `role=master` übergeben.
- `patronictl failover` akzeptiert die seit Patroni 3.2.0 veraltete Option `--leader` nicht mehr.
- Die seit Patroni 3.2.0 veraltete Funktion zur Benutzererstellung im Konfigurationsabschnitt `bootstrap.users` wurde entfernt.

**Neue Funktionen**

- Quorumbasiertes Failover (Ants Aasma, Alexander Kukushkin)

  Diese Funktion implementiert quorumbasierte synchrone Replikation, die ab PostgreSQL v10 verfügbar ist. Sie hilft, selbst im Normalbetrieb die maximal auftretenden Latenzen zu verringern, weil eine höhere Replikationslatenz zu einem Standby durch andere Standbys ausgeglichen werden kann. Patroni implementiert zusätzliche Schutzmaßnahmen gegen jeden für Benutzer sichtbaren Datenverlust, indem es den Failover-Kandidaten anhand der zuletzt empfangenen Transaktion auswählt.

- Citus-Sekundärknoten in `pg_dist_node` registriert (Alexander Kukushkin)

  Patroni verwaltet jetzt in `pg_dist_node` die Liste der Knoten mit `role==replica`, `state==running` und ohne den [Tag](/de/patroni/config/yaml#tags_settings) `noloadbalance`.

- Aufbewahrungsdauer der Replikationsslots von Mitgliedern konfigurierbar gemacht (Alexander Kukushkin)

  Der globale Konfigurationsparameter `member_slots_ttl` wird unterstützt. Er steuert, wie lange die Replikationsslots eines Mitglieds erhalten bleiben sollen, wenn dessen Mitgliedsschlüssel fehlt.

- Berechtigungen für von Patroni erstellte Protokolldateien konfigurierbar gemacht (Alexander Kukushkin)

  Für von Patroni erstellte Protokolldateien können bestimmte Berechtigungen festgelegt werden. Ohne Angabe werden die Berechtigungen anhand des aktuellen Werts von `umask` gesetzt.

- Kompatibilität mit PostgreSQL 17 beta3 (Alexander Kukushkin)

  Die Validierungsregeln für GUCs wurden erweitert. Patroni behandelt beim Herunterfahren alle neuen Hilfs-Backends und setzt `dbname` in `primary_conninfo`, da dies für die Synchronisierung logischer Replikationsslots erforderlich ist.

- Option `--ignore-listen-port` für die Validierung der Patroni-Konfiguration implementiert (Sahil Naphade)

  Bei der Ausführung von `patroni --validate-config` können bereits belegte Ports ignoriert werden.

**Verbesserungen**

- `wal_log_hints` konfigurierbar gemacht (Paul_Kim)

  Damit lässt sich der Mehraufwand durch aktiviertes `wal_log_hints` vermeiden, wenn `use_pg_rewind` auf `off` gesetzt ist.

- Befehl `pg_basebackup` auf Stufe `DEBUG` protokolliert (Waynerv)

  Dies erleichtert die Diagnose fehlgeschlagener Initialisierungen.

**Fehlerbehebungen**

- Permanente Slots für kaskadierende Knoten im Failsafe-Modus vorgerückt (Alexander Kukushkin)

  Bei aktiviertem Failsafe-Modus werden die Slots kaskadierender Replikate auf dem Primärserver korrekt vorgerückt. Dazu wird die Antwort der Replikate auf die REST-API-Anfrage `POST /failsafe` um deren `xlog_location` ergänzt.

- Auswahl des aktuellen Knotens als synchronen Knoten verhindert (Alexander Kukushkin)

  Es kann „etwas“ vom aktuellen Primärserver streamen, dessen `application_name` dem Namen des Primärservers entspricht. Patroni behandelte diese Situation nicht korrekt. Dadurch konnte der Primärserver als synchroner Knoten deklariert werden, was anschließend Switchovers blockierte.

- `restapi.allowlist_include_members` bei POST /failsafe ignoriert (Alexander Kukushkin)

- Validierung von GUCs verbessert (Polina Bungina)

  Wegen der zusätzlichen Validierung durch `postgres --describe-config` konnten GUCs, die dort nicht aufgeführt waren, zuvor nicht über die Patroni-Konfiguration gesetzt werden. Diese Einschränkung wurde entfernt.

- Bei erkannten Unix-Sockets eine Zeile mit `localhost` zur Datei `.pgpass` hinzugefügt (Alexander Kukushkin)

  Patroni ergänzt `.pgpass` um eine weitere Zeile, wenn der angegebene Parameter `host` mit `/` beginnt. Damit wird der Sonderfall abgedeckt, dass `host` dem Pfad des standardmäßigen Socket-Verzeichnisses entspricht.

- Probleme bei der Protokollierung behoben (Waynerv)

  In den Protokollen der Failsafe-Behandlung wurde die korrekte Anfrage-URL festgelegt und die Reihenfolge der Zeitstempel im Protokoll der postmaster-Prüfung korrigiert.

--------

## Version 3.3.2 {#version-332}

Veröffentlicht am 2024-07-11

**Fehlerbehebungen**

- Natives synchrones Replikationsverhalten von Postgres korrigiert (Israel Barth Rubio)

  Seit Einführung von [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) in Patroni funktionierte die native synchrone Replikation von Postgres nicht. Mit dieser Korrektur setzt Patroni `synchronous_standby_names` auf den vom Benutzer konfigurierten Wert, sofern ein solcher vorhanden ist, wenn [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) deaktiviert ist.

- Ungültigwerden logischer Slots auf einem Standby behandelt (Polina Bungina)

  Seit PG16 können logische Replikationsslots auf einem Standby aufgrund des Horizonts ungültig werden. Patroni erzwingt jetzt das Kopieren, also die Neuerstellung, ungültiger Slots.

- Race Condition beim Vorrücken und Kopieren logischer Slots behoben (Alexander Kukushkin)

  Aufgrund dieses Fehlers konnte ein ungültiger logischer Replikationsslot mehrfach mit einem PostgreSQL-Neustart kopiert werden.

--------

## Version 3.3.1 {#version-331}

Veröffentlicht am 2024-06-17

**Verbesserungen der Stabilität**

- Kompatibilität mit Python 3.12 (Alexander Kukushkin)

  Ein neues Attribut von `logging.LogRecord` wird berücksichtigt.

**Fehlerbehebungen**

- Endlose Rekursion bei der Verarbeitung von `replicatefrom`-Tags behoben (Alexander Kukushkin)

  Im Zuge dieser Korrektur wurden außerdem die Prüfung `is_physical_slot()` verbessert und die Dokumentation angepasst.

- Falsche Rollenmeldungen in Standby-Clustern behoben (Alexander Kukushkin)

  `synchronous_standby_names` und synchrone Replikation funktionieren nur auf einem tatsächlichen Primärserver. Bei kaskadierender Replikation werden sie von Postgres schlicht ignoriert. Vor dieser Korrektur meldeten `patronictl list` und `GET /cluster` manche Knoten fälschlich als synchron.

- Verfügbarkeit der GUC `allow_in_place_tablespaces` korrigiert (Polina Bungina)

  `allow_in_place_tablespaces` wurde nicht nur PostgreSQL 15 hinzugefügt, sondern auch auf PostgreSQL 10-14 zurückportiert.

--------

## Version 3.3.0 {#version-330}

Veröffentlicht am 2024-04-04

> [!WARNING]
> Alle älteren Patroni-Versionen sind mit `ydiff>=1.3` inkompatibel.
>
> Folgende Möglichkeiten stehen zur „Behebung“ des Problems zur Verfügung:
>
> 1.  Patroni auf die neueste Version aktualisieren
> 2.  Nach der Installation von Patroni `ydiff<1.3` installieren
> 3.  Das Modul `cdiff` installieren

**Neue Funktionen**

- Übergabe von `auth_data` an den Zookeeper-Client ermöglicht (Aras Mumcuyan)

  Damit können die für die Verbindung zu verwendenden Authentifizierungsdaten angegeben werden.

- Contrib-Skript für die Integration von `Barman` hinzugefügt (Israel Barth Rubio)

  Die Anwendung `patroni_barman` ermöglicht die entfernte Ausführung von `Barman`-Operationen. Sie kann als benutzerdefinierte Bootstrap- oder Replikaterstellungsmethode oder als Callback `on_role_change` verwendet werden. Weitere Informationen finden sich [hier](/de/patroni/tools_integration#tools_integration).

- Protokollformat `JSON` unterstützt (alisalemmi)

  Neben `plain`, dem Standard, unterstützt Patroni jetzt das Protokollformat `json`. Dafür muss die Bibliothek `python-json-logger>=2.0.2` installiert sein.

- Informationen zu `pending_restart_reason` angezeigt (Polina Bungina)

  Erweiterte Informationen zu den PostgreSQL-Parametern werden bereitgestellt, die das Setzen des Kennzeichens `pending_restart` verursacht haben. Sowohl `patronictl list` als auch der REST-API-Endpunkt `/patroni` zeigen jetzt die Parameternamen und deren Unterschiede als `pending_restart_reason` an.

- Tag `nostream` implementiert (Grigory Smolkin)

  Wenn `nostream` auf `true` gesetzt ist, verwendet der Knoten nicht das Replikationsprotokoll zum Streamen von WAL, sondern die Archiv-Recovery, sofern `restore_command` konfiguriert ist. Außerdem werden das Kopieren und Synchronisieren permanenter logischer Replikationsslots auf dem Knoten selbst und allen seinen kaskadierenden Replikaten deaktiviert.

**Verbesserungen**

- Validierung des Abschnitts `log` implementiert (Alexander Kukushkin)

  Bisher prüfte der Validator nicht, ob die angegebene Protokollierungskonfiguration korrekt war.

- Protokollierung von Änderungen an PostgreSQL-Parametern verbessert (Polina Bungina)

  Alte Werte werden in ein menschenlesbares Format umgewandelt und Abweichungen zwischen `pg_controldata` und der globalen Patroni-Konfiguration protokolliert.

**Fehlerbehebungen**

- Nicht zulässige Optionen von `pg_basebackup` korrekt herausgefiltert (Israel Barth Rubio)

  Aufgrund eines Fehlers filterte Patroni unzulässige Optionen für die Replikat-Bootstrap-Methode `basebackup` nicht korrekt heraus, wenn sie im Format `- setting: value` angegeben wurden.

- Behandlung von `etcd3`-Authentifizierungsfehlern korrigiert (Alexander Kukushkin)

  Bei einem `etcd3`-Authentifizierungsfehler wird immer ein Wiederholungsversuch durchgeführt, sofern die Authentifizierung nicht unmittelbar vor Ausführung der Anfrage erfolgte. Außerdem werden Watcher bei erneuter Authentifizierung nicht neu gestartet.

- Logik zum Auffinden von Validierungsdateien verbessert (Waynerv)

  Nach Möglichkeit wird die Bibliothek `importlib` verwendet, um Dateien mit verfügbaren Konfigurationsparametern zu finden, ab Python 3.9+. Diese Implementierung ist stabiler und beeinträchtigt keine Patroni-Distributionen auf Basis von `zip`-Archiven.

- `target_session_attrs` nur bei mehreren Hosts im Abschnitt [standby_cluster](/de/patroni/standby_cluster#standby_cluster) verwendet (Alexander Kukushkin)

  `target_session_attrs=read-write` wird auf dem Standby-Leader nur noch dann zu `primary_conninfo` hinzugefügt, wenn `standby_cluster.host` mehrere durch Kommas getrennte Hosts enthält.

- Kompatibilitätscode für Version 1.3+ der Bibliothek `ydiff` hinzugefügt (Alexander Kukushkin)

  Patroni nutzt Teile der nicht öffentlichen API von `ydiff`, da dieses eigentlich als Terminalwerkzeug und nicht als Python-Modul gedacht ist. Die API-Änderung in 1.3 machte ältere Patroni-Versionen leider funktionsunfähig.

--------

## Version 3.2.2 {#version-322}

Veröffentlicht am 2024-01-17

**Fehlerbehebungen**

- Wiederherstellung des initialize-Schlüssels durch ein Replikat nach dem Löschen des DCS verhindert (Alexander Kukushkin)

  Dies geschah in der Methode, in der Patroni einen eigenständigen PG-Cluster übernehmen sollte.

- Konsistentes Lesen beim Abruf eines gerade aktualisierten sync-Schlüssels aus Consul verwendet (Alexander Kukushkin)

  Consul bietet keine Schnittstelle, um `ModifyIndex` für einen gerade aktualisierten Schlüssel sofort zu ermitteln. Daher ist ein ausdrücklicher Lesevorgang erforderlich. Weil veraltete Leseergebnisse standardmäßig erlaubt sind, wurde dabei manchmal eine veraltete Schlüsselversion abgerufen.

- Postgres-Konfiguration wird neu geladen, wenn ein Parameter, der einen Neustart erfordert, auf seinen ursprünglichen Wert zurückgesetzt wurde (Polina Bungina)

  Zuvor aktualisierte Patroni die Konfiguration nicht, sondern setzte lediglich `pending_restart` zurück.

- Fälschlich invertierte Logik der Bestätigungsabfrage beim Failover zu einem asynchronen Kandidaten im synchronen Modus korrigiert (Polina Bungina)

  Das Problem bestand nur in [patronictl](/de/patroni/patronictl#patronictl).

- Leader von Failover-Kandidaten in [patronictl](/de/patroni/patronictl#patronictl) ausgeschlossen (Polina Bungina)

  In einem funktionsfähigen Cluster hat ein Failover zum vorhandenen Leader keine Wirkung.

- Citus-Datenbank und -Erweiterung idempotent erstellt (Alexander Kukushkin, Zhao Junwang)

  Dadurch können sie im Skript `post_bootstrap` erstellt werden, wenn weitere Abhängigkeiten zur Citus-Datenbank hinzugefügt werden müssen.

- Widersprüchlichen Tag `nofailover` nicht herausgefiltert (Polina Bungina)

  Die auf einem Knoten gesetzte Konfiguration `{nofailover: false, failover_priority: 0}` hinderte ihn an der Teilnahme an der Leader-Wahl. Er sollte jedoch teilnehmen dürfen, da der Tag `nofailover` Vorrang haben sollte.

- Problem mit durch PyInstaller eingefrorenen Anwendungen behoben (Sophia Ruan)

  `freeze_support()` wurde nach `argparse` aufgerufen, weshalb Patroni Postgres nicht starten konnte.

- Fehler im Konfigurationsgenerator für [patronictl](/de/patroni/patronictl#patronictl) und [Citus](/de/patroni/citus#citus) behoben (Israel Barth Rubio)

  Der Fehler verhinderte, dass über Umgebungsvariablen gesetzte Konfigurationsparameter für [patronictl](/de/patroni/patronictl#patronictl) und [Citus](/de/patroni/citus#citus) in die erzeugte Konfiguration geschrieben wurden.

- Recovery-GUCs und einige von Patroni verwaltete Parameter bei der Übernahme eines laufenden Standbys wiederhergestellt (Alexander Kukushkin)

  Ab Postgres v12 konnte Patroni Postgres nicht neu starten und meldete einen fehlenden `port` in einer internen Struktur.

- Korrekturen am Kennzeichen `pending_restart` (Polina Bungina)

  `pending_restart` wird während eines benutzerdefinierten Bootstraps mit `recovery_target_action = promote` nicht bereitgestellt. Dasselbe gilt, wenn jemand `hot_standby` oder `wal_log_hints` etwa über `ALTER SYSTEM` geändert hat.

--------

## Version 3.2.1 {#version-321}

Veröffentlicht am 2023-11-30

**Fehlerbehebungen**

- Zulässige Werte des Arguments `--format` in [patronictl](/de/patroni/patronictl#patronictl) begrenzt (Alexander Kukushkin)

  Zuvor wurden beliebige Zeichenketten akzeptiert und bei einem unbekannten Wert keine Ausgabe erzeugt.

- Vor Freigabe des Leader-Schlüssels wird geprüft, ob Replikatknoten beim Herunterfahren die Checkpoint-LSN erhalten haben (Alexander Kukushkin)

  Zuvor wurde in manchen Fällen die LSN des SWITCH-Eintrags verwendet, auf den bei aktiviertem Archivmodus ein CHECKPOINT folgt. Dadurch musste der frühere Primärserver manchmal `pg_rewind` ausführen; Datenverlust entstand dabei jedoch nicht.

- Bei der Prüfung auf Eindeutigkeit des Knotennamens eine tatsächliche HTTP-Anfrage ausgeführt (Alexander Kukushkin)

  Beim Betrieb von Patroni in Containern kann der Datenverkehr über `docker-proxy` geleitet werden, das auf dem Port lauscht und eingehende Verbindungen annimmt. Dies führte zu falsch positiven Ergebnissen.

- Citus-Unterstützung mit etcd v2 korrigiert (Alexander Kukushkin)

  Patroni konnte mit etcd v2 keinen neuen Citus-Cluster bereitstellen.

- Verhalten von `pg_rewind` mit Postgres v16+ korrigiert (Alexander Kukushkin)

  In v16 änderte sich das Format der Fehlermeldung von `pg_waldump`, sodass Patroni `pg_rewind` auch dann aufrief, wenn dies nicht erforderlich war.

- Fehler beim benutzerdefinierten Bootstrap behoben (Alexander Kukushkin)

  Patroni wandte das Argument `--command`, das selbst der Bootstrap-Befehl ist, fälschlich an.

- Problem mit REST-API-Endpunkten für Health Checks behoben (Sophia Ruan)

  Nach einem Postgres-Neustart konnte der Zustand von Postgres als `unknown` zurückgegeben werden, weil Verbindungen nicht korrekt geschlossen worden waren.

- Ausgabe von `postgres --describe-config` zwischengespeichert (Waynerv)

  Sie dient dazu, die für die Validierung der PostgreSQL-Konfiguration verfügbaren GUCs zu ermitteln. Eine Änderung dieser Liste während der Patroni-Laufzeit wird nicht erwartet.

--------

## Version 3.2.0 {#version-320}

Veröffentlicht am 2023-10-25

**Hinweis auf veraltete Funktionen**

- Die Unterstützung für `bootstrap.users` wird in Version 4.0.0 entfernt. Falls nach der Bereitstellung eines neuen Clusters Benutzer erstellt werden müssen, verwenden Sie dazu den Hook `bootstrap.post_bootstrap`.

**Inkompatible Änderungen**

- Regel `loop_wait + 2*retry_timeout <= ttl` erzwungen und kleinste mögliche Werte fest vorgegeben (Alexander Kukushkin)

  Mindestwerte: `loop_wait=2`, `retry_timeout=3`, `ttl=20`. Kleinere Werte oder Werte, die die Regel verletzen, werden angepasst; eine Warnung wird in den Patroni-Protokollen ausgegeben.

**Neue Funktionen**

- Failover-Priorität (Mark Pekala)

  Mit `tags.failover_priority` kann ein Knoten jetzt bei der Leader-Wahl bevorzugt werden. Weitere Einzelheiten enthält die Dokumentation zu Tags (ref tags).

- `patroni --generate-config [--dsn DSN]` und `patroni --generate-sample-config` implementiert (Polina Bungina)

  Damit kann eine Konfigurationsdatei für einen laufenden PostgreSQL-Cluster oder eine Beispielkonfiguration für einen neuen Patroni-Cluster erzeugt werden.

- Eigene Verbindung zu Postgres für die Patroni-REST-API verwendet (Alexander Kukushkin)

  Dies hilft, eine Blockierung der Heartbeat-Hauptschleife bei hoher Systemlast zu vermeiden.

- Einige Endpunkte um den `name` des Knotens ergänzt (sskserk)

  Beim Überwachungsendpunkt wird `name` neben `scope` hinzugefügt; beim Metrikendpunkt wird `name` in die Tags aufgenommen.

- Failover und Switchover strikt unterschieden (Polina Bungina)

  Protokollmeldungen werden präziser und ein Failover zu einem asynchronen Knoten in einem funktionsfähigen synchronen Cluster wird ermöglicht.

- Verhalten permanenter physischer Replikationsslots an permanente logische Slots angeglichen (Alexander Kukushkin)

  Permanente physische Replikationsslots werden auf allen Knoten erstellt, die Leader werden dürfen. Auf Standby-Knoten wird `restart_lsn` der Slots mit `pg_replication_slot_advance()` vorgerückt.

- Angabe des Namespace über das Argument `--dcs` in [patronictl](/de/patroni/patronictl#patronictl) ermöglicht (Israel Barth Rubio)

  Dies kann nützlich sein, wenn [patronictl](/de/patroni/patronictl#patronictl) ohne Konfigurationsdatei verwendet wird.

- Zusätzliche Parameter in der Konfiguration benutzerdefinierter Bootstraps unterstützt (Israel Barth Rubio)

  Zuvor konnten benutzerdefinierte Argumente nur an `command` angehängt werden; jetzt lassen sie sich als Mapping angeben.

**Verbesserungen**

- GUC `citus.local_hostname` wird auf denselben Wert gesetzt, den Patroni für die Verbindung zu Postgres verwendet (Alexander Kukushkin)

  In manchen Fällen benötigt Citus eine Verbindung zum lokalen Postgres. Standardmäßig wird dafür `localhost` verwendet, das jedoch nicht immer verfügbar ist.

**Fehlerbehebungen**

- Einstellung [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) in einem Standby-Cluster ignoriert (Polina Bungina)

  Postgres unterstützt keine kaskadierende synchrone Replikation. Die Berücksichtigung von [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) führte daher zum Fehlschlagen eines Switchovers im Standby-Cluster.

- SIGCHLD für den Callback `on_reload` behandelt (Alexander Kukushkin)

  Andernfalls entsteht ein Zombie-Prozess, der erst bei der nächsten Ausführung von `on_reload` aufgeräumt wird.

- Fehler `AuthOldRevision` bei der Arbeit mit etcd v3 behandelt (Alexander Kukushkin, Kenny Do)

  Der Fehler wird ausgelöst, wenn etcd JWT verwendet und die Benutzerdatenbank in etcd aktualisiert wird.

--------

## Version 3.1.2 {#version-312}

Veröffentlicht am 2023-09-26

**Fehlerbehebungen**

- Fehler bei Prüfungen von `wal_keep_size` behoben (Alexander Kukushkin)

  Die GUC `wal_keep_size` besitzt normalerweise eine Einheit; Patroni konnte ihren Wert nicht in `int` umwandeln. Dadurch wurde anschließend der Wert von `bootstrap.dcs` nicht in den Schlüssel `/config` geschrieben.

- Inkonsistenzen zwischen dem Schlüssel `/sync` und `synchronous_standby_names` erkannt und behoben (Alexander Kukushkin)

  Normalerweise aktualisiert Patroni `/sync` und `synchronous_standby_names` in einer genau festgelegten Reihenfolge. Bei einem Fehler oder wenn jemand `synchronous_standby_names` manuell zurücksetzte, geriet Patroni jedoch in einen inkonsistenten Zustand. Dadurch konnte ein Failover zu einem asynchronen Knoten erfolgen.

- GUC-Werte bei der Übernahme eines laufenden Postgres gelesen (Alexander Kukushkin)

  Bei einem Neustart im [Pause-Modus](/de/patroni/pause#pause) entfernte Patroni die GUC `synchronous_standby_names` aus `postgresql.conf`. Um dieses und ähnliche Probleme zu vermeiden, liest Patroni den GUC-Wert, wenn es einen bereits laufenden Postgres übernimmt.

- Störende Warnungen bei der Prüfung auf Eindeutigkeit des Knotens unterdrückt (Alexander Kukushkin)

  Bei einem schnellen Patroni-Neustart erzeugt `urllib3` Meldungen der Stufe `WARNING`.

--------

## Version 3.1.1 {#version-311}

Veröffentlicht am 2023-09-20

**Fehlerbehebungen**

- Failsafe-Zustand bei der Hochstufung zurückgesetzt (ChenChangAo)

  Erfolgte ein Switchover oder Failover kurz nach Aktivierung des Failsafe-Modus, stufte sich der neu hochgestufte Primärserver selbst herab, sobald Failsafe wieder inaktiv wurde.

- Nutzlose Warnungen in [patronictl](/de/patroni/patronictl#patronictl) unterdrückt (Alexander Kukushkin)

  Wenn [patronictl](/de/patroni/patronictl#patronictl) dieselbe Datei patroni.yaml wie Patroni verwendet und auf das Verzeichnis `PGDATA` zugreifen kann, wurden möglicherweise störende Warnungen zu falschen Werten in der globalen Konfiguration angezeigt.

- Synchronen Modus in einem Sonderfall ausdrücklich aktiviert (Alexander Kukushkin)

  Wenn keine Replikate vom Primärserver streamten, wurde der synchrone Modus tatsächlich nie aktiviert.

- Fehler bei der Validierung ganzzahliger Werte von `0` behoben (Israel Barth Rubio)

  Meist verursachte dies keine Probleme, sondern nur Warnungen.

- Keine logischen Slots für Standby-Cluster zurückgegeben (Alexander Kukushkin)

  Patroni kann in einem Standby-Cluster keine logischen Replikationsslots erstellen. Daher sollten sie ignoriert werden, wenn sie in der globalen Konfiguration definiert sind.

- Anzeige des Docstrings in der Ausgabe von `patronictl --help` vermieden (Israel Barth Rubio)

  Das Modul `click` benötigt dafür einen besonderen Hinweis.

- Fehler bei `kubernetes.standby_leader_label_value` behoben (Alexander Kukushkin)

  Diese Funktion hatte tatsächlich nie funktioniert.

- Systemkennung des Clusters wieder in der Ausgabe von `patronictl list` angezeigt (Polina Bungina)

  Das Problem entstand bei der Implementierung der Citus-Unterstützung. Dort muss die Kennung ausgeblendet werden, da sie für den Coordinator und alle Worker unterschiedlich ist.

- Methode `write_leader_optime` in der Kubernetes-Implementierung überschrieben (Alexander Kukushkin)

  Die Methode soll die LSN beim Herunterfahren in das Endpoint- oder ConfigMap-Objekt des Leaders schreiben, wenn kein funktionsfähiges Replikat als neuer Primärserver zur Verfügung steht.

- Gestopptes Postgres wird während einer Pause nicht gestartet (Alexander Kukushkin)

  Aufgrund einer Race Condition nahm Patroni fälschlich an, der Standby müsse neu gestartet werden, weil sich Recovery-Parameter wie `primary_conninfo` geändert hätten.

- Fehler im Befehl `patronictl query` behoben (Israel Barth Rubio)

  Der Befehl funktionierte nicht, wenn nur `-m` oder keines der Argumente `-r` und `-m` angegeben wurde.

- Ganzzahlige Parameter auf der Befehlszeile zum Start von postgres korrekt behandelt (Polina Bungina)

  Wurden Werte als Zeichenketten angegeben und nicht in Ganzzahlen umgewandelt, wurde `max_prepared_transactions` für Citus-Cluster anhand von `max_connections` falsch berechnet.

- Bei der Entscheidung über `pg_rewind` nicht auf `pg_stat_wal_receiver` vertraut (Alexander Kukushkin)

  Der von `pg_stat_wal_receiver` gemeldete Wert `received_tli` konnte der tatsächlich wiedergegebenen Timeline voraus sein. Dagegen ist die von `IDENTIFY_SYSTEM` über die Replikationsverbindung gemeldete Timeline immer korrekt.

--------

## Version 3.1.0 {#version-310}

Veröffentlicht am 2023-08-03

**Inkompatible Änderungen**

- Bedeutung von `restapi.keyfile` und `restapi.certfile` geändert (Alexander Kukushkin)

  Zuvor verwendete Patroni `restapi.keyfile` und `restapi.certfile` ersatzweise als Client-Zertifikate, wenn die entsprechenden Konfigurationsparameter im Abschnitt `ctl` fehlten.

> [!WARNING]
> Wenn die Prüfung von Client-Zertifikaten aktiviert ist (`restapi.verify_client` ist auf `required` gesetzt), **müssen** außerdem **gültige Client-Zertifikate** in `ctl.certfile`, `ctl.keyfile` und `ctl.keyfile_password` angegeben werden. Ohne diese Angaben funktioniert Patroni nicht korrekt.

**Neue Funktionen**

- Rollenlabel von Pods konfigurierbar gemacht (Waynerv)

  Die Werte können über `kubernetes.leader_label_value`, `kubernetes.follower_label_value` und `kubernetes.standby_leader_label_value` angepasst werden. Diese Funktion wird beim Wechsel von der Rolle `master` zu `primary` sehr nützlich sein. Weitere Informationen zur Funktion und den Migrationsschritten finden sich [hier](/de/patroni/kubernetes#kubernetes_role_values).

**Verbesserungen**

- Verschiedene Verbesserungen an `patroni --validate-config` (Alexander Kukushkin)

  Die Parametervalidierung für verschiedene DCS sowie die Abschnitte `bootstrap.dcs`, `ctl`, `restapi` und [watchdog](/de/patroni/watchdog#watchdog) wurde verbessert.

- Postgres wird außerhalb der Recovery gestartet, wenn es während der Recovery bei laufendem Patroni abgestürzt ist (Alexander Kukushkin)

  Dies kann die Recovery-Zeit verkürzen und hilft, unnötige Timeline-Erhöhungen zu vermeiden.

- Unnötige Aktualisierungen des Schlüssels `/status` vermieden (Alexander Kukushkin)

  Wenn keine permanenten logischen Slots vorhanden waren, aktualisierte Patroni `/status` bei jedem Heartbeat-Schleifendurchlauf, selbst wenn sich die LSN auf dem Primärserver nicht weiterbewegt hatte.

- Verhindert, dass ein Primärserver mit veraltetem Zustand die Leader-Wahl gewinnt (Alexander Kukushkin)

  Wenn Patroni wegen Ressourcenmangels längere Zeit nicht reagiert hat, prüft es vor dem Erwerb der Leader-Sperre zusätzlich, ob auf keinem anderen Knoten Postgres hochgestuft wurde.

- Validierung bestimmter PostgreSQL-Parameter sichtbar gemacht (Alexander Kukushkin, Feike Steenbergen)

  Wenn die Validierung von `max_connections`, `max_wal_senders`, `max_prepared_transactions`, `max_locks_per_transaction`, `max_replication_slots` oder `max_worker_processes` fehlschlug, verwendete Patroni einen geeigneten Standardwert. Zusätzlich wird jetzt eine Warnung ausgegeben.

- Berechtigungen für in `PGDATA` erstellte Dateien und Verzeichnisse gesetzt (Alexander Kukushkin)

  Alle von Patroni erstellten Dateien hatten nur Lese- und Schreibberechtigungen für den Eigentümer. Dadurch funktionierten Backup-Werkzeuge nicht, die unter einem anderen Benutzer laufen und Gruppenleserechte benötigen. Patroni berücksichtigt jetzt die Berechtigungen von `PGDATA` und setzt die Berechtigungen aller innerhalb von `PGDATA` erstellten Dateien und Verzeichnisse korrekt.

**Fehlerbehebungen**

- `archive_command` über eine Shell ausgeführt (Waynerv)

  Patroni kann vor einer Crash-Recovery im Einzelbenutzermodus oder vor `pg_rewind` einige WAL-Segmente archivieren. Enthielt archive_command Shell-Operatoren wie `&&`, funktionierte dies mit Patroni nicht.

- Prüfungen beim Herunterfahren während eines Switchovers korrigiert (Polina Bungina)

  Es konnte vorkommen, dass der angegebene Kandidat noch streamte und den Shutdown-Checkpoint noch nicht erhalten hatte, der Leader-Schlüssel aber entfernt wurde, weil andere Knoten funktionsfähig waren.

- Prüfung auf Primärserver korrigiert (Alexander Kukushkin)

  Während der Leader-Wahl konnten Replikate nicht erkennen, dass Postgres auf dem alten Leader weiterhin als Primärserver lief.

- `patronictl list` korrigiert (Alexander Kukushkin)

  Das Feld für den Clusternamen fehlte in den Ausgabeformaten `tsv`, `json` und `yaml`.

- Verhalten von `pg_rewind` nach einer Pause korrigiert (Alexander Kukushkin)

  Unter bestimmten Bedingungen konnte Patroni nach dem Verlassen des Wartungsmodus den fälschlich als Primärserver laufenden Knoten nicht mit `pg_rewind` wieder in den Cluster eingliedern.

- Fehler in der etcd-v3-Implementierung behoben (Alexander Kukushkin)

  Der interne KV-Cache wird ungültig gemacht, wenn eine Schlüsselaktualisierung mit dem Feld `create_revision`/`mod_revision` aufgrund einer Revisionsabweichung fehlschlägt.

- Verhalten von Replikaten in einem pausierten Standby-Cluster korrigiert (Alexander Kukushkin)

  Wenn der Leader-Schlüssel abläuft, folgen Replikate im Standby-Cluster nicht dem entfernten Knoten, sondern behalten `primary_conninfo` unverändert bei.

--------

## Version 3.0.4 {#version-304}

Veröffentlicht am 2023-07-13

**Neue Funktionen**

- Replikationsstatus von Standby-Knoten sichtbar gemacht (Alexander Kukushkin)

  Für PostgreSQL 9.6+ meldet Patroni den Replikationszustand als `streaming`, wenn der Standby von einem anderen Knoten streamt. Besteht keine Replikationsverbindung und ist `restore_command` gesetzt, wird `in archive recovery` gemeldet. Der Zustand ist in den Schlüsseln `member` im DCS, in der REST API und in der Ausgabe von `patronictl list` sichtbar.

**Verbesserungen**

- Fehlermeldungen mit etcd v3 verbessert (Alexander Kukushkin)

  War ein etcd-v3-Cluster nicht erreichbar, meldete Patroni, dass es auf die Endpunkte `/v2` nicht zugreifen könne.

- Nach Möglichkeit Quorum-Lesezugriffe in [patronictl](/de/patroni/patronictl#patronictl) verwendet (Alexander Kukushkin)

  etcd- oder Consul-Cluster konnten nur noch lesbar sein, während aus Sicht von [patronictl](/de/patroni/patronictl#patronictl) alles in Ordnung war. Jetzt schlägt der Zugriff mit einer Fehlermeldung fehl.

- Split-Brain durch doppelte Namen in der Konfiguration verhindert (Mark Pekala)

  Beim Start prüft Patroni, ob im DCS ein Knoten mit demselben Namen registriert ist, und versucht, dessen REST API abzufragen. Ist diese erreichbar, beendet sich Patroni mit einem Fehler. Dies schützt vor menschlichen Fehlern.

- Postgres wird außerhalb der Recovery gestartet, wenn es bei laufendem Patroni abgestürzt ist (Alexander Kukushkin)

  Dies kann die Recovery-Zeit verkürzen und hilft, unnötige Timeline-Erhöhungen zu vermeiden.

**Fehlerbehebungen**

- SSL-Zertifikate der REST API wurden bei Empfang von SIGHUP nicht neu geladen (Israel Barth Rubio)

  Die Regression wurde in 3.0.3 eingeführt.

- Validierung ganzzahliger GUCs für Parameter wie `max_connections` korrigiert (Feike Steenbergen)

  Patroni akzeptierte numerische Werte in Anführungszeichen nicht. Die Regression wurde in 3.0.3 eingeführt.

- Problem mit [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) behoben (Alexander Kukushkin)

  `txid_current()` wird mit `synchronous_commit=off` ausgeführt, damit es bei aktiviertem `synchronous_mode_strict` nicht versehentlich auf fehlende synchrone Standbys wartet.

--------

## Version 3.0.3 {#version-303}

Veröffentlicht am 2023-06-22

**Neue Funktionen**

- Kompatibilität mit PostgreSQL 16 beta1 (Alexander Kukushkin)

  Die Validierungsregeln für GUCs wurden erweitert.

- Validator für PostgreSQL-GUCs erweiterbar gemacht (Israel Barth Rubio)

  Validierungsregeln werden aus YAML-Dateien im Verzeichnis `patroni/postgresql/available_parameters/` geladen. Die Dateien werden alphabetisch sortiert und nacheinander angewendet. Damit sind benutzerdefinierte Validatoren für von der Standarddistribution abweichende Postgres-Distributionen möglich.

- Option `restapi.request_queue_size` hinzugefügt (Andrey Zhidenkov, Aleksei Sukhov)

  Sie legt die Größe der Anfragewarteschlange für den von der Patroni-REST-API verwendeten TCP-Socket fest. Ist die Warteschlange voll, erhalten weitere Anfragen den Fehler "Connection denied". Der Standardwert ist 5.

- `initdb` beim Bootstrap eines neuen Clusters direkt aufgerufen (Matt Baker)

  Zuvor wurde es über `pg_ctl` aufgerufen, was eine besondere Behandlung der Anführungszeichen für die an `initdb` übergebenen Parameter erforderte.

- Hook vor dem Stoppen hinzugefügt (Le Duane)

  Der Hook kann über `postgresql.before_stop` konfiguriert werden und wird unmittelbar vor `pg_ctl stop` ausgeführt. Sein Exit-Code beeinflusst den Vorgang des Herunterfahrens nicht.

- Benutzerdefinierte Namen für Postgres-Programme unterstützt (Israel Barth Rubio, Polina Bungina)

  In einer benutzerdefinierten Postgres-Distribution können die Programme unter anderen Namen als in der Community-Distribution kompiliert sein. Benutzerdefinierte Programmnamen lassen sich über `postgresql.bin_name.*` und die Umgebungsvariablen `PATRONI_POSTGRESQL_BIN_*` konfigurieren.

**Verbesserungen**

- Verschiedene Verbesserungen an `patroni --validate-config` (Polina Bungina)

  - `bootstrap.initdb` ist nun optional. Es ist nur für neue Cluster erforderlich, doch `patroni --validate-config` beanstandete bisher sein Fehlen in der Konfiguration.
  - Bei leerem oder nicht gesetztem `postgresql.bin_dir` wird kein Fehler ausgelöst. Stattdessen wird zunächst im standardmäßigen PATH nach Postgres-Programmen gesucht.
  - Der Abschnitt `postgresql.authentication.rewind` ist nun optional. Fehlt er, verwendet Patroni den Superuser.

- Fehlermeldungen in [patronictl](/de/patroni/patronictl#patronictl) verbessert (Israel Barth Rubio)

  Das Symbol `\n` wurde wörtlich statt als tatsächlicher Zeilenumbruch dargestellt.

**Fehlerbehebungen**

- Problem in der Citus-Unterstützung behoben (Alexander Kukushkin)

  Wenn während eines Switchovers der REST-API-Aufruf vom hochgestuften Worker zum Coordinator fehlschlug, blieb die betreffende Citus-Gruppe auf unbestimmte Zeit blockiert.

- `etcd3`-URL in der Option `--dcs-url` von [patronictl](/de/patroni/patronictl#patronictl) zugelassen (Israel Barth Rubio)

  Der Versuch, über die Option `--dcs-url` von [patronictl](/de/patroni/patronictl#patronictl) eine `etcd3`-URL zu übergeben, führte zu einer Ausnahme.

--------

## Version 3.0.2 {#version-302}

Veröffentlicht am 2023-03-24

> [!WARNING]
> Version 3.0.2 stellt die Unterstützung für Python-Versionen vor 3.6 ein.

**Neue Funktionen**

- Status synchroner Standby-Replikate zum Endpunkt `/metrics` hinzugefügt (Thomas von Dein, Alexander Kukushkin)

  Zuvor wurden nur `primary`/`standby_leader`/`replica` gemeldet.

- Benutzerfreundliche Behandlung von `PAGER` in [patronictl](/de/patroni/patronictl#patronictl) (Israel Barth Rubio)

  Der Pager kann über die Umgebungsvariable `PAGER` konfiguriert werden, die die Standardprogramme `less` und `more` überschreibt.

- HTTP-Statuscodes für wiederholbare K8s-Anfragen konfigurierbar gemacht (Alexander Kukushkin)

  Auf manchen verwalteten Plattformen kann der Statuscode `401 Unauthorized` auftreten; das Problem behebt sich bisweilen nach einigen Wiederholungsversuchen.

**Verbesserungen**

- `hot_standby` wird während eines benutzerdefinierten Bootstraps nur auf `off` gesetzt, wenn `recovery_target_action` auf `promote` gesetzt ist (Alexander Kukushkin)

  Dies war erforderlich, damit `recovery_target_action=pause` korrekt funktioniert.

- Verhindert, dass der Callback `on_reload` andere Callbacks beendet (Alexander Kukushkin)

  `on_start`/`on_stop`/`on_role_change` dienen üblicherweise zum Hinzufügen und Entfernen einer virtuellen IP. `on_reload` sollte diese nicht beeinträchtigen.

- AWS-Callback-Beispielskript auf `IMDSFetcher` umgestellt (Polina Bungina)

  `IMDSv2` benötigt ein Token; `IMDSFetcher` kümmert sich transparent darum.

**Fehlerbehebungen**

- `patronictl switchover` für einen Citus-Cluster auf Kubernetes korrigiert (Lukáš Lalinský)

  Der Befehl funktionierte für andere Namespaces als `default` nicht.

- Bei unbekannter Hauptversion wird nicht in `PGDATA` geschrieben (Alexander Kukushkin)

  War `PGDATA` unmittelbar nach dem Start leer, etwa weil es noch nicht eingehängt war, nahm Patroni eine falsche PostgreSQL-Version an und erstellte fälschlich `recovery.conf`, selbst wenn die tatsächliche Hauptversion v10+ war.

- Fehler bei Citus-Metadaten nach einem Coordinator-Failover behoben (Alexander Kukushkin)

  Der Aufruf von `citus_set_coordinator_host()` löst keine Metadatensynchronisierung aus, sodass die Änderung auf Worker-Knoten nicht sichtbar war. Das Problem wird durch den Wechsel zu `citus_update_node()` behoben.

- Bei „Ausfall“ aller etcd-Knoten auf die Hosts aus der Konfigurationsdatei zurückgegriffen (Alexander Kukushkin)

  Die Topologie des etcd-Clusters kann sich im Laufe der Zeit ändern; Patroni versucht, ihr zu folgen. Sind irgendwann alle Knoten nicht mehr erreichbar, verwendet Patroni bei erneuten Verbindungsversuchen eine Kombination der Knoten aus der Konfiguration und der zuletzt bekannten Topologie.

--------

## Version 3.0.1 {#version-301}

Veröffentlicht am 2023-02-16

**Fehlerbehebungen**

- Korrekter Rollenname wird an ein Callback-Skript `on_role_change` übergeben. (Alexander Kukushkin, Polina Bungina)

  Patroni übergab bei der Hochstufung fälschlich die Rolle `promoted` an ein Callback-Skript `on_role_change`. Der übergebene Rollenname wurde wieder auf `master` geändert. Diese Regression wurde in 3.0.0 eingeführt.

--------

## Version 3.0.0 {#version-300}

Veröffentlicht am 2023-01-30

Diese Version ergänzt die Integration mit [Citus](https://www.citusdata.com) und ermöglicht es, vorübergehende DCS-Ausfälle ohne Herabstufung des Primärservers zu überstehen.

> [!WARNING]
> - Version 3.0.0 ist die letzte Version mit Unterstützung für Python 2.7. Die nächste Version wird Python-Versionen vor 3.7 nicht mehr unterstützen.
>
> - Die RAFT-Unterstützung ist veraltet. Sie wird nach besten Kräften weiter gepflegt, es wird jedoch weder eine Garantie noch Verantwortung für mögliche Probleme übernommen.
> - Diese Version ist der erste Schritt zur Ablösung von „master“ durch „primary“. Ein zuverlässiges Upgrade auf die nächste Hauptversion ist nur von mindestens Version 3.0.0 aus möglich.

**Neue Funktionen**

- DCS-Failsafe-Modus (Alexander Kukushkin, Polina Bungina)

  Wenn diese Funktion aktiviert ist, kann ein Patroni-Cluster vorübergehende DCS-Ausfälle überstehen. Weitere Einzelheiten enthält die [Dokumentation](/de/patroni/dcs_failsafe_mode#dcs_failsafe_mode).

- Citus-Unterstützung (Alexander Kukushkin, Polina Bungina, Jelte Fennema)

  Patroni ermöglicht die einfache Bereitstellung und Verwaltung von [Citus](https://www.citusdata.com)-Clustern mit HA. Weitere Informationen finden sich [hier](/de/patroni/citus#citus).

**Verbesserungen**

- Wiederkehrende Fehler beim Löschen unbekannter, aber aktiver Replikationsslots unterdrückt (Michael Banck)

  Patroni schreibt diese Protokollmeldungen weiterhin, jedoch nur auf Stufe DEBUG.

- Nur eine Überwachungsabfrage pro HA-Schleifendurchlauf ausgeführt (Alexander Kukushkin)

  Bei aktivierter synchroner Replikation war dies bisher nicht der Fall.

- Nur das zuletzt fehlgeschlagene Datenverzeichnis wird behalten (William Albertus Dembo)

  Nach einem fehlgeschlagenen Bootstrap benannte Patroni das Verzeichnis \$PGDATA bisher mit einem Zeitstempelsuffix um. Jetzt lautet das Suffix `.failed`. Existiert ein solches Verzeichnis bereits, wird es vor dem Umbenennen entfernt.

- Prüfung synchroner Replikationsverbindungen verbessert (Alexander Kukushkin)

  Wird ein neuer Host zu `synchronous_standby_names` hinzugefügt, wird er im DCS erst dann als synchron eingetragen, wenn er neben `pg_stat_replication.sync_state = 'sync'` auch zum Primärserver aufgeholt hat.

**Entfernte Funktionen**

- `patronictl scaffold` entfernt (Alexander Kukushkin)

  Sein einziger Zweck war eine behelfsmäßige Möglichkeit, Standby-Cluster zu betreiben.

--------

## Version 2.1.7 {#version-217}

Veröffentlicht am 2023-01-04

**Fehlerbehebungen**

- Kleine Inkompatibilitäten mit älteren Python-Modulen behoben (Alexander Kukushkin)

  Sie verhinderten das Bauen oder Ausführen von Patroni unter Debian buster/Ubuntu bionic.

--------

## Version 2.1.6 {#version-216}

Veröffentlicht am 2022-12-30

**Verbesserungen**

- Störende Ausnahmen beim Schließen von SSL-Sockets behoben (Alexander Kukushkin)

  HAProxy schließt Verbindungen, sobald es den HTTP-Statuscode empfangen hat. Dadurch blieb Patroni keine Zeit, die SSL-Verbindung ordnungsgemäß zu schließen.

- Beispiel-Dockerfile für arm64 angepasst (Polina Bungina)

  Die expliziten Angaben `amd64` und `x86_64` wurden entfernt; `libnss_files.so.*` wird nicht entfernt.

**Sicherheitsverbesserungen**

- `search_path=pg_catalog` für Verbindungen außerhalb des Replikationsprotokolls erzwungen (Alexander Kukushkin)

  Da Patroni stark auf Superuser-Verbindungen angewiesen ist, soll es vor möglichen Angriffen über benutzerdefinierte Funktionen und/oder Operatoren im Schema `public` geschützt werden, die denselben Namen und dieselbe Signatur wie entsprechende Objekte in `pg_catalog` haben. Dazu wird `search_path=pg_catalog` für alle von Patroni erstellten Verbindungen außer Replikationsverbindungen erzwungen.

- Aufzeichnung von Passwörtern in `pg_stat_statements` verhindert (Feike Steenbergen)

  Dazu wird beim Anlegen von Benutzern `pg_stat_statements.track_utility=off` gesetzt.

**Fehlerbehebungen**

- `proxy_address` als optional deklariert (Denis Laxalde)

  Die Option ist tatsächlich nicht erforderlich.

- Verhalten der Option insecure verbessert (Alexander Kukushkin)

  Die Option `insecure` von ctl funktionierte nicht richtig, wenn für REST-API-Anfragen Clientzertifikate verwendet wurden.

- Watchdog-Konfiguration beim Bootstrap eines neuen Clusters aus `bootstrap.dcs` übernommen (Matt Baker)

  Bisher konfigurierte Patroni den Watchdog beim Bootstrap eines neuen Clusters zunächst mit Standardwerten, statt die zum Bootstrap des DCS verwendete Konfiguration zu übernehmen.

- Behandlung von Dateiendungen bei der Suche nach ausführbaren Dateien unter WIN32 korrigiert (Martín Marqués)

  `.exe` wird nur angehängt, wenn der Dateiname noch keine Endung hat.

- Einstellung der Consul-TTL korrigiert (Alexander Kukushkin)

  Beim Setzen des Werts im HTTPClient wurde `ttl/2.0` verwendet, in der Eigenschaft der Klasse jedoch vergessen, den aktuellen Wert mit 2 zu multiplizieren. Dadurch war die Consul-TTL um den Faktor zwei falsch.

**Entfernte Funktionen**

- `patronictl configure` entfernt (Polina Bungina)

  Eine separate Erstellung der [patronictl](/de/patroni/patronictl#patronictl)-Konfiguration ist nicht mehr nötig.

--------

## Version 2.1.5 {#version-215}

Veröffentlicht am 2022-11-28

Diese Version verbessert die Kompatibilität mit PostgreSQL 15 und erklärt die Unterstützung für etcd v3 für produktionsreif. Patroni auf Raft bleibt im Beta-Stadium.

**Neue Funktionen**

- `patroni --validate-config` verbessert (Denis Laxalde)

  Bei ungültiger Konfiguration erfolgt der Abbruch mit Code 1; Fehler werden auf stderr ausgegeben.

- Replikationsslots werden im pausierten Modus nicht entfernt (Alexander Kukushkin)

  Patroni erstellt oder entfernt physische Replikationsslots automatisch, wenn Mitglieder dem Cluster beitreten oder ihn verlassen. Im pausierten Modus werden Slots nicht mehr entfernt.

- Anfragemethode `HEAD` für Überwachungsendpunkte unterstützt (Robert Cutajar)

  Wird sie anstelle von `GET` verwendet, gibt Patroni nur den HTTP-Statuscode zurück.

- behave-Tests unter Windows unterstützt (Alexander Kukushkin)

  Der neue REST-API-Endpunkt `POST /sigterm` ermöglicht es, ein geordnetes Herunterfahren von Patroni (`SIGTERM`) unter Windows nachzubilden.

- `postgresql.proxy_address` eingeführt (Alexander Kukushkin)

  Der Wert wird als `proxy_url` in den Mitgliedsschlüssel im DCS geschrieben und kann zur Diensterkennung verwendet werden.

**Stabilitätsverbesserungen**

- `pg_replication_slot_advance()` wird aus einem Thread aufgerufen (Alexander Kukushkin)

  Auf stark ausgelasteten Clustern mit vielen logischen Replikationsslots beeinträchtigte der Aufruf von `pg_replication_slot_advance()` die HA-Hauptschleife und konnte zum Ablauf des Mitgliedsschlüssels führen.

- Möglicherweise fehlende WAL-Dateien werden vor dem Aufruf von `pg_rewind` auf dem alten Primärserver archiviert (Polina Bungina)

  War der Primärserver nach einem Absturz längere Zeit ausgefallen, konnten einige WAL-Dateien sowohl im Archiv als auch auf dem neuen Primärserver fehlen. `pg_rewind` konnte diese Dateien vom alten Primärserver entfernen, sodass dieser nicht mehr als Standby gestartet werden konnte. Das Archivieren von WAL-Dateien im Zustand `ready` verringert dieses Risiko und verbessert die kontinuierliche Archivierung insgesamt.

- Fehler `403` beim Versuch, einen Kubernetes-Service anzulegen, werden ignoriert (Nick Hudson, Polina Bungina)

  Erfolglose Versuche, den möglicherweise bereits vorhandenen Service anzulegen, überfluteten die Patroni-Protokolle.

- Liveness-Prüfung verbessert (Alexander Kukushkin)

  Die Liveness-Prüfung schlägt fehl, wenn die Heartbeat-Schleife auf dem Primärserver länger als `ttl` oder auf einem Replikat länger als `2*ttl` läuft. Dadurch kann sie unter Kubernetes als Alternative zum [Watchdog](/de/patroni/watchdog#watchdog) verwendet werden.

- Bei einem Switchover versucht nur ein synchroner Knoten, die Sperre zu übernehmen (Alexander Kukushkin, Polina Bungina)

  Zuvor bestand eine geringe Chance, dass ein asynchrones Mitglied auf dem aktuellen Stand Leader wurde, wenn ein manuelles Switchover ohne Zielangabe ausgeführt wurde.

- Klonen während des Cluster-Bootstraps verhindert (Ants Aasma)

  Eine Methode zur Replikaterstellung, die keinen Leader benötigt, darf während des laufenden Cluster-Bootstraps nicht gestartet werden.

- Kompatibilität mit kazoo-2.9.0 (Alexander Kukushkin)

  Je nach Python-Version kann `SequentialThreadingHandler.select()` die Ausnahmen `TypeError` und `IOError` auslösen, wenn `select()` auf einem geschlossenen Socket aufgerufen wird.

- SSL-Verbindung wird vor dem Socket ausdrücklich geschlossen (Alexander Kukushkin)

  Ohne diesen Schritt kam es mit OpenSSL 3.0 zu Fehlern `unexpected eof while reading`.

- Kompatibilität mit `prettytable>=2.2.0` (Alexander Kukushkin)

  Durch interne API-Änderungen wurde die Überschrift mit dem Clusternamen in der falschen Zeile angezeigt.

**Fehlerbehebungen**

- Abgelaufene Token bei etcd lease_grant behandelt (monsterxx03)

  Bei einem Fehler wird ein neues Token geholt und die Anfrage wiederholt.

- Fehler im Endpunkt `GET /read-only-sync` behoben (Alexander Kukushkin)

  Er wurde in der vorherigen Version eingeführt und hatte tatsächlich nie funktioniert.

- Verschwundener Speicher des Datenverzeichnisses behandelt (Alexander Kukushkin)

  Patroni prüft regelmäßig, ob PGDATA vorhanden und nicht leer ist. Bei Speicherproblemen löst `os.listdir()` jedoch `OSError` aus, wodurch die Heartbeat-Schleife unterbrochen wurde.

- `master_stop_timeout` beim Warten auf das Ende von Benutzer-Backends angewendet (Alexander Kukushkin)

  Ein vermeintliches Benutzer-Backend kann tatsächlich ein Hintergrundprozess sein, etwa der Citus Maintenance Daemon, der sich nicht beendet.

- `*:<port>` für `postgresql.listen` zugelassen (Denis Laxalde)

  `patroni --validate-config` meldete diesen Wert als ungültig.

- Zeitüberschreitungen in Raft korrigiert (Alexander Kukushkin)

  Beim Start versuchen Patroni oder patronictl, die Raft-Clustertopologie von bekannten Mitgliedern abzurufen. Diese Aufrufe erfolgten ohne geeignete Zeitbegrenzung.

- Consul-Service nach einer Tokenänderung zwingend aktualisiert (John A. Lotoski)

  Ohne die Aktualisierung entstanden Fehler wie "rpc error making call: rpc error making call: ACL not found".

--------

## Version 2.1.4 {#version-214}

Veröffentlicht am 2022-06-01

**Neue Funktionen**

- Verhalten von `pg_rewind` auf typischen Debian-/Ubuntu-Systemen verbessert (Gunnar "Nick" Bluth)

  Bei Postgres-Installationen mit `postgresql.conf` außerhalb des Datenverzeichnisses (z. B. Ubuntu-/Debian-Pakete) kann `pg_rewind --restore-target-wal` den Wert von `restore_command` nicht ermitteln.

- `TLSServerName` für Consul-Service-Prüfungen einstellbar (Michael Gmelin)

  Dies ist nützlich, wenn Prüfungen über IP-Adressen erfolgen und der Consul-`node_name` kein FQDN ist.

- Unterstützung für `ppc64le` im Watchdog hinzugefügt (Jean-Michel Scheiwiler)

  Außerdem wurde die Watchdog-Unterstützung auf einigen Nicht-x86-Plattformen korrigiert.

- Callback aws.py von `boto` auf `boto3` umgestellt (Alexander Kukushkin)

> `boto` 2.x wird seit 2018 nicht mehr gepflegt und funktioniert mit Python 3.9 nicht.

- Service-Account-Token unter K8s regelmäßig erneuert (Haitao Li)

  Seit Kubernetes v1.21 laufen Service-Account-Token nach 1 Stunde ab.

- Überwachungsendpunkt `/read-only-sync` hinzugefügt (Dennis4b)

  Er ähnelt `/read-only`, berücksichtigt aber nur synchrone Replikate.

**Stabilitätsverbesserungen**

- Logische Replikationsslots werden bei abweichender Konfiguration der logischen Dekodierung nicht auf Replikate kopiert (Alexander Kukushkin)

  Ein Replikat kopiert einen logischen Replikationsslot nicht mehr vom Primärserver, wenn dieser nicht zu den Konfigurationsoptionen `plugin` oder `database` passt. Zuvor erfolgte diese Prüfung erst, nachdem das Replikat den Slot kopiert hatte und damit gestartet war. Dies führte zu unnötigen, wiederholten Neustarts.

- Recovery-Konfigurationsparameter für PostgreSQL v12+ gesondert behandelt (Alexander Kukushkin)

  Beim Start als Replikat sollte Patroni `postgresql.conf` aktualisieren und einen Neustart bzw. ein Neuladen ausführen können, wenn sich die Leader-Adresse geändert hat. Dazu werden die aktuellen Parameterwerte zwischengespeichert, statt sie aus `pg_settings` abzufragen.

- IPv6-Adressen in `postgresql.listen` besser behandelt (Alexander Kukushkin)

  Da `listen` einen Port enthält, werden IPv6-Adressen häufig in eckige Klammern gesetzt. Diese wurden bei mehreren IP-Adressen in der Liste nicht korrekt entfernt.

- Zugangsdaten von `replication` für die Divergenzprüfung nur unter PostgreSQL v10 und älter verwendet (Alexander Kukushkin)

  Ist `rewind` aktiviert, verwendet Patroni auf neueren Postgres-Versionen wieder entweder `superuser`- oder `rewind`-Zugangsdaten.

**Fehlerbehebungen**

- Fehlenden Import von `dateutil.parser` ergänzt (Wesley Mendes)

  Die Tests schlugen nur deshalb nicht fehl, weil das Modul auch aus anderen Modulen importiert wurde.

- Sichergestellt, dass die Annotation `optime` eine Zeichenfolge ist (Sebastian Hasler)

  In bestimmten Fällen versuchte Patroni, sie als Zahl zu übergeben.

- Fehlgeschlagene Versuche mit `pg_rewind` besser behandelt (Alexander Kukushkin)

  Wird der Primärserver während `pg_rewind` unerreichbar, bleibt `$PGDATA` in einem beschädigten Zustand zurück. Anschließend entfernt Patroni das Datenverzeichnis, auch wenn die Konfiguration dies nicht erlaubt.

- Annotationen `slots` werden bei noch nicht bereitem PostgreSQL nicht aus der Leader-`ConfigMap` bzw. dem Leader-`Endpoint` entfernt (Alexander Kukushkin)

  Wird kein Wert für `slots` übergeben, behält die Annotation ihren aktuellen Wert.

- Nebenläufigkeitsproblem mit K8s-API-Watchern behandelt (Alexander Kukushkin)

  Unter bestimmten, unbekannten Bedingungen können Watcher veralten, wodurch `attempt_to_acquire_leader()` mit HTTP-Statuscode 409 fehlschlagen kann. In diesem Fall werden die Watcher-Verbindungen zurückgesetzt und neu aufgebaut.

--------

## Version 2.1.3 {#version-213}

Veröffentlicht am 2022-02-18

**Neue Funktionen**

- Verschlüsselte TLS-Schlüssel für [patronictl](/de/patroni/patronictl#patronictl) unterstützt (Alexander Kukushkin)

  Die Konfiguration erfolgt über `ctl.keyfile_password` oder die Umgebungsvariable `PATRONI_CTL_KEYFILE_PASSWORD`.

- Weitere Metriken zum Endpunkt /metrics hinzugefügt (Alexandre Pereira)

  Konkret sind dies `patroni_pending_restart` und `patroni_is_paused`.

- Mehrere Hosts in der Standby-Cluster-Konfiguration zugelassen (Michael Banck)

  Repliziert der Standby-Cluster von einem Patroni-Cluster, kann clientseitiges Failover nützlich sein, das `libpq` seit PostgreSQL v10 unterstützt. Dazu setzen `primary_conninfo` auf dem Standby-Leader und `pg_rewind` die Option `target_session_attrs=read-write` in der Verbindungszeichenfolge. Die Datei `pgpass` wird mit mehreren Zeilen erzeugt, einer pro Host. Statt `CHECKPOINT` auf den Knoten des Primärclusters aufzurufen, wartet der Standby-Cluster darauf, dass `pg_control` aktualisiert wird.

**Stabilitätsverbesserungen**

- Kompatibilität mit älterem `psycopg2` (Alexander Kukushkin)

  Beispielsweise enthält das über Ubuntu-18.04-Pakete installierte `psycopg2` die Ausnahme `UndefinedFile` noch nicht.

- `etcd3`-Watcher wird neu gestartet, wenn kein etcd-Knoten antwortet (Alexander Kukushkin)

  Solange der Watcher aktiv ist, liefert `get_cluster()` weiterhin veraltete Informationen, selbst wenn alle etcd-Knoten ausfallen.

- Leader-Sperre im pausierten Standby-Cluster wird nicht entfernt (Alexander Kukushkin)

  Zuvor wurde die Sperre nur von einem als Primärserver laufenden Knoten aufrechterhalten, nicht von einem Standby-Leader.

**Fehlerbehebungen**

- Fehler beim Bootstrap des Standby-Leaders behoben (Alexander Kukushkin)

  Patroni betrachtete den Bootstrap als fehlgeschlagen, wenn Postgres nach 60 Sekunden noch keine Verbindungen annahm. Der Fehler wurde mit Version 2.1.2 eingeführt.

- Fehler beim Failover auf einen kaskadierenden Standby behoben (Alexander Kukushkin)

  Bei der Ermittlung der auf einem kaskadierenden Standby anzulegenden Slots wurde nicht berücksichtigt, dass der Leader fehlen könnte.

- Kleine Probleme im Validator für die Postgres-Konfiguration behoben (Alexander Kukushkin)

  Die Validierung von Ganzzahlparametern, die mit PostgreSQL v14 eingeführt wurden, schlug fehl, weil ihre Minimal- und Maximalwerte in validator.py in Anführungszeichen standen.

- Replikationszugangsdaten bei der Prüfung des Leader-Status verwendet (Alexander Kukushkin)

  Es kann vorkommen, dass `remove_data_directory_on_diverged_timelines` gesetzt ist, aber keine `rewind_credentials` definiert sind und Superuser-Zugriff zwischen den Knoten nicht erlaubt ist.

- Fehler "port in use" beim Austausch des REST-API-Zertifikats behoben (Ants Aasma)

  Beim Zertifikatswechsel bestand eine Race Condition mit gleichzeitig laufenden API-Anfragen. War während des Austauschs eine Anfrage aktiv, schlug der Austausch mit einem Portbelegungsfehler fehl, und Patroni blieb ohne aktiven API-Server hängen.

- Fehler beim Cluster-Bootstrap mit `%` im Passwort behoben (Bastien Wirtz)

  Die Bootstrap-Methode führt den `DO`-Block mit korrekt in Anführungszeichen gesetzten Parametern aus. Die Methode `cursor.execute()` kam jedoch mit einer übergebenen leeren Parameterliste nicht zurecht.

- Ausnahme "AttributeError: no attribute 'leader'" behoben (Hrvoje Milković)

  Sie konnte auftreten, wenn der synchrone Modus aktiviert und der Inhalt des DCS gelöscht worden war.

- Fehler bei der Prüfung auf divergierende Zeitleisten behoben (Alexander Kukushkin)

  Patroni nahm fälschlich an, dass die Zeitleisten auseinanderliefen. Für pg_rewind war dies unproblematisch. War pg_rewind jedoch nicht erlaubt und `remove_data_directory_on_diverged_timelines` gesetzt, wurde der bisherige Leader dadurch neu initialisiert.

--------

## Version 2.1.2 {#version-212}

Veröffentlicht am 2021-12-03

**Neue Funktionen**

- Kompatibilität mit `psycopg>=3.0` (Alexander Kukushkin)

  Standardmäßig wird `psycopg2` bevorzugt. `psycopg>=3.0` wird nur verwendet, wenn `psycopg2` fehlt oder zu alt ist.

- Feld `dcs_last_seen` zur REST-API hinzugefügt (Michael Banck)

  Das Feld enthält den letzten Zeitpunkt, zu dem ein Clustermitglied erfolgreich mit dem DCS kommuniziert hat, als Unix-Epoch-Zeit. Dies hilft, Netzwerkpartitionen zu erkennen und/oder zu analysieren.

- Leader-Sperre wird freigegeben, wenn `pg_controldata` "shut down" meldet (Alexander Kukushkin)

  Um langsame Switchover- oder Herunterfahrvorgänge bei langsamem oder fehlschlagendem `archive_command` zu beheben, entfernt Patroni den Leader-Schlüssel, sobald `pg_controldata` PGDATA als sauber `shut down` meldet und geprüft wurde, dass mindestens ein Replikat alle Änderungen empfangen hat. Erfüllt kein Replikat diese Bedingung, wird der Leader-Schlüssel nicht entfernt; das bisherige Verhalten bleibt bestehen und Patroni aktualisiert die Sperre weiterhin.

- Verbindungsparameter `sslcrldir` unterstützt (Kostiantyn Nemchenko)

  Der neue Verbindungsparameter wurde mit PostgreSQL v14 eingeführt.

- ACLs für ZNodes in ZooKeeper konfigurierbar (Alwyn Davis)

  Die neue Konfigurationsoption `zookeeper.set_acls` veranlasst Kazoo, auf jeden angelegten ZNode eine Standard-ACL anzuwenden.

**Stabilitätsverbesserungen**

- Nächster Wiederherstellungsversuch bis zum nächsten HA-Durchlauf verzögert (Alexander Kukushkin)

  War Postgres beispielsweise wegen eines vollen Datenträgers abgestürzt und konnte deshalb nicht starten, versuchte Patroni die Wiederherstellung zu häufig und überflutete die Protokolle.

- Protokolleintrag vor der möglicherweise länger dauernden Herabstufung hinzugefügt (Michael Banck)

  Eine Herabstufung kann einige Zeit dauern; anhand der Protokolle war nicht unbedingt erkennbar, was gerade geschah.

- Statusmeldungen "I am" verbessert (Michael Banck)

  `no action. I am a secondary ({0})` gegenüber `no action. I am ({0}), a secondary`

- `wal_keep_segments` bei der Umrechnung in `wal_keep_size` in eine Ganzzahl umgewandelt (Jorge Solórzano)

  `wal_keep_segments` kann in der globalen [dynamischen Konfiguration](/de/patroni/config/dynamic#dynamic) als Zeichenfolge angegeben werden. Wegen der dynamischen Typisierung von Python wurde dann einfach die Zeichenfolge vervielfacht. Beispiel: `wal_keep_segments: "100"` wurde in `100100100100100100100100100100100100100100100100MB` umgewandelt.

- Bei aktivierter synchroner Replikation Switchover nur auf synchrone Knoten zugelassen (Alexander Kukushkin)

  Außerdem tritt der Knoten bei der Leader-Wahl nur gegen bekannte synchrone Knoten an.

- Zwischengespeicherte Rolle als Rückfallwert bei langsamem Postgres verwendet (Alexander Kukushkin)

  In Extremfällen kann Postgres so langsam sein, dass die normale Überwachungsabfrage nicht innerhalb weniger Sekunden endet. Eine nicht korrekt behandelte Ausnahme durch `statement_timeout` konnte dazu führen, dass Postgres beim Ablauf des Leader-Schlüssels oder einer fehlgeschlagenen Aktualisierung nicht rechtzeitig herabgestuft wurde. Bei einer solchen Ausnahme verwendet Patroni die zwischengespeicherte `role`, um festzustellen, ob Postgres als Primärserver läuft.

- Unnötige Aktualisierungen des Mitglieds-ZNodes vermieden (Alexander Kukushkin)

  Wenn sich keine Werte in den Mitgliedsdaten geändert haben, sollte keine Aktualisierung erfolgen.

- Checkpoint nach der Hochstufung optimiert (Alexander Kukushkin)

  `CHECKPOINT` wird vermieden, wenn die neueste Zeitleiste bereits in `pg_control` gespeichert ist. Dadurch entfällt ein unnötiger `CHECKPOINT` unmittelbar nach der Initialisierung eines neuen Clusters mit `initdb`.

- Mitglieder ohne `nofailover` bei der Wahl synchroner Knoten bevorzugt (Alexander Kukushkin)

  Zuvor wurden synchrone Knoten allein anhand des Replikationsrückstands gewählt. Ein Knoten mit dem Tag `nofailover` hatte daher dieselbe Chance wie jeder andere Knoten, synchron zu werden. Dieses Verhalten war verwirrend und gefährlich, weil beim Ausfall des Primärservers kein automatisches Failover möglich war.

- Doppelte Hosts aus dem etcd-Machine-Cache entfernt (Michael Banck)

  Die veröffentlichten Client-URLs im etcd-Cluster können falsch konfiguriert sein. In diesem Fall ist das Entfernen von Duplikaten in Patroni eine einfache Verbesserung.

**Fehlerbehebungen**

- Temporäre Replikationsslots bei der Slot-Verwaltung übersprungen (Alexander Kukushkin)

  Seit v10 erstellt `pg_basebackup` einen temporären Replikationsslot für das WAL-Streaming. Patroni versuchte, ihn zu löschen, weil der Slotname unbekannt erschien. Zur Behebung werden bei der Abfrage der Sicht `pg_replication_slots` alle temporären Slots übersprungen.

- Zeitüberschreitungen bei `pg_replication_slot_advance()` verhindert (Alexander Kukushkin)

  Patroni verwendete hier den Standardwert von `statement_timeout`. Schlug der Aufruf einmal fehl, war es sehr wahrscheinlich, dass er sich nicht mehr erholte, was zu einem wachsenden `pg_wal` und zu Bloat in `pg_catalog` führte.

- `/status` wurde bei einer Herabstufung nicht aktualisiert (Alexander Kukushkin)

  Nach der Herabstufung von PostgreSQL aktualisiert der alte Leader die letzte LSN im DCS. Mit `2.1.0` wurde der neue Schlüssel `/status` eingeführt, die optime wurde jedoch weiterhin nach `/optime/leader` geschrieben.

- DCS-Ausnahmen bei der Herabstufung behandelt (Alexander Kukushkin)

  Während der Herabstufung des Primärservers wegen einer fehlgeschlagenen Aktualisierung der Leader-Sperre kann der DCS vollständig ausfallen und `get_cluster()` eine Ausnahme auslösen. Ohne korrekte Behandlung blieb Postgres gestoppt, bis der DCS wieder verfügbar war.

- `use_unix_socket_repl` funktionierte in einigen Fällen nicht (Alexander Kukushkin)

  Insbesondere betraf dies Fälle ohne gesetztes `postgresql.unix_socket_directories`. Patroni sollte dann den Standardwert von `libpq` verwenden.

- Mehrere Probleme mit der REST-API von Patroni behoben (Alexander Kukushkin)

  `clusters_unlocked` war manchmal nicht definiert, wodurch Ausnahmen im Endpunkt `GET /metrics` entstanden. Außerdem nahm die Fehlerbehandlung an, dass das Tupel `connect_address` stets zwei Elemente enthält; bei IPv6 können es tatsächlich mehr sein.

- Vor der Entscheidung über einen Rewind das Ende der Recovery des neu hochgestuften Knotens abgewartet (Alexander Kukushkin)

  Bis zur tatsächlichen Hochstufung und Erstellung der neuen Zeitleiste kann einige Zeit vergehen. Ohne diese Wartezeit konnten Replikate fälschlich folgern, dass kein Rewind nötig sei.

- Fehlende Zeitleisten in der History-Datei bei der Rewind-Entscheidung behandelt (Alexander Kukushkin)

  Fehlte die aktuelle Zeitleiste eines Replikats in der History-Datei des Primärservers, nahm das Replikat fälschlich an, dass kein Rewind nötig sei.

--------

## Version 2.1.1 {#version-211}

Veröffentlicht am 2021-08-19

**Neue Funktionen**

- Unterstützung für ETCD-SRV-Namenssuffixe (David Pavlicek)

  etcd kann mehrere etcd-Cluster unter derselben Domain unterscheiden; dies wird nun auch von Patroni unterstützt.

- Verlauf um den neuen Leader ergänzt (huiyalin525)

  Die Ausgabe von `patronictl history` erhält dafür eine neue Spalte.

- CA-Bündel für die Kubernetes-Konfiguration innerhalb des Clusters konfigurierbar (Aron Parsons)

  Standardmäßig verwendet Patroni `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`. Die neue Funktion erlaubt die Angabe eines eigenen `kubernetes.cacert`.

- Dynamisches Registrieren und Abmelden als Consul-Service sowie Ändern von Tags unterstützt (Tommy Li)

  Zuvor war dafür ein Patroni-Neustart erforderlich.

**Fehlerbehebungen**

- Unnötiges Neuladen der REST-API vermieden (Alexander Kukushkin)

  Die vorherige Version führte das Neuladen von REST-API-Zertifikaten ein, wenn diese auf dem Datenträger geändert wurden. Leider wurde unmittelbar nach dem Start bedingungslos neu geladen.

- Clustermitglieder werden bei gesetztem `etcd.use_proxies` nicht aufgelöst (Alexander Kukushkin)

  Beim Start prüft Patroni den Zustand des etcd-Clusters, indem es die Mitgliederliste abfragt. Zusätzlich versuchte es, deren Hostnamen aufzulösen. Dies ist bei etcd-Zugriffen über einen Proxy unnötig und erzeugte überflüssige Warnungen.

- Zeilen mit NULL-Werten in `pg_stat_replication` übersprungen (Alexander Kukushkin)

  Offenbar kann die Sicht `pg_stat_replication` NULL-Werte in `replay_lsn`, `flush_lsn` oder `write_lsn` enthalten, selbst wenn `state = 'streaming'` gilt.

--------

## Version 2.1.0 {#version-210}

Veröffentlicht am 2021-07-06

Diese Version ergänzt die Kompatibilität mit PostgreSQL v14, erhält logische Replikationsslots über Failover/Switchover hinweg, unterstützt eine Allowlist für die REST-API und reduziert die Protokollausgabe auf eine Zeile pro Heartbeat.

**Neue Funktionen**

- Kompatibilität mit PostgreSQL v14 (Alexander Kukushkin)

  Die WAL-Wiedergabe wird fortgesetzt, wenn Patroni selbst nicht im „Pause“-Modus ist. Sie kann durch die Änderung bestimmter Parameter auf dem Primärserver, etwa `max_connections`, „pausiert“ sein.

- Failover für logische Slots (Alexander Kukushkin)

  Logische Replikationsslots bleiben unter PostgreSQL v11+ über Failover/Switchover hinweg erhalten. Der Slot wird mit einem Neustart vom Primärserver auf das Replikat kopiert und später mit [pg_replication_slot_advance()](https://www.postgresql.org/docs/11/functions-admin.html#id-1.5.8.31.8.5.2.2.8.1.1) vorgerückt. Dadurch ist der Slot schon vor dem Failover vorhanden und es sollten keine Ereignisse verloren gehen. Einige Ereignisse können jedoch mehrfach zugestellt werden.

- Allowlist für die REST-API von Patroni implementiert (Alexander Kukushkin)

  Ist sie konfiguriert, dürfen nur IP-Adressen, die den Regeln entsprechen, unsichere Endpunkte aufrufen. Zusätzlich lassen sich die IP-Adressen der Clustermitglieder automatisch in die Liste aufnehmen.

- Replikationsverbindungen über Unix-Sockets unterstützt (Mohamad El-Rifai)

  Zuvor verwendete Patroni für Replikationsverbindungen stets TCP, was bei der SSL-Prüfung Probleme verursachen konnte. Unix-Sockets ermöglichen es, den Replikationsbenutzer von der SSL-Prüfung auszunehmen.

- Health Checks anhand benutzerdefinierter Tags (Arman Jafari Tehrani)

  Neben den [vordefinierten Tags:](/de/patroni/config/yaml#tags_settings) können beliebig viele eigene Tags angegeben werden. Sie erscheinen in `patronictl list` und in der REST-API und lassen sich nun auch in Health Checks verwenden.

- Prometheus-Endpunkt `/metrics` hinzugefügt (Mark Mercado, Michael Banck)

  Der Endpunkt stellt dieselben Metriken wie `/patroni` bereit.

- Patroni-Protokolle weniger ausführlich (Alexander Kukushkin)

  Im Normalbetrieb wird pro Durchlauf der HA-Schleife nur eine Zeile geschrieben.

**Inkompatible Änderungen**

- Die bisherige Funktion `permanent logical replication slots` funktioniert unter PostgreSQL v10 und älter nicht mehr (Alexander Kukushkin)

  Die Strategie, logische Slots erst nach der Hochstufung anzulegen, kann nicht garantieren, dass keine logischen Ereignisse verloren gehen, und wird daher deaktiviert.

- Der Endpunkt `/leader` liefert immer 200, wenn der Knoten die Sperre hält (Alexander Kukushkin)

  Beim Hochstufen eines Standby-Clusters müssen bisher die Health Checks des Load-Balancers angepasst werden. Dies ist umständlich und wird leicht vergessen. Deshalb wird das Verhalten des Health-Check-Endpunkts `/leader` geändert: Er gibt 200 zurück, unabhängig davon, ob der Cluster normal oder ein [standby_cluster](/de/patroni/standby_cluster#standby_cluster) ist.

**Verbesserungen der Raft-Unterstützung**

- Zuverlässige Verschlüsselung des Raft-Datenverkehrs (Alexander Kukushkin)

  Durch verschiedene Probleme in `PySyncObj` war die Verschlüsselungsunterstützung sehr instabil.

- DNS-Probleme in der Raft-Implementierung behandelt (Alexander Kukushkin)

  Wurden `self_addr` und/oder `partner_addrs` über DNS-Namen statt IP-Adressen konfiguriert, löste `PySyncObj` sie praktisch nur einmal beim Erstellen des Objekts auf. Dies verursachte Probleme, wenn derselbe Knoten mit einer anderen IP-Adresse zurückkehrte.

**Stabilitätsverbesserungen**

- Kompatibilität mit `psycopg2-2.9+` (Alexander Kukushkin)

  In `psycopg2` wird `autocommit = True` im Block `with connection` ignoriert, wodurch Verbindungen über das Replikationsprotokoll fehlschlagen.

- Übermäßig häufige HA-Durchläufe mit ZooKeeper behoben (Alexander Kukushkin)

  Aktualisierungen von Mitglieds-ZNodes lösten eine Kettenreaktion aus, sodass die HA-Schleifen mehrfach direkt hintereinander liefen.

- REST-API-Zertifikat wird nach Änderung auf dem Datenträger neu geladen (Michael Todorovic)

  Wurde die Zertifikatsdatei direkt ersetzt, führte Patroni kein Neuladen aus.

- Kein pgpass-Verzeichnis bei Kerberos-Authentifizierung angelegt (Kostiantyn Nemchenko)

  Kerberos- und Passwortauthentifizierung schließen sich gegenseitig aus.

- Kleine Probleme beim benutzerdefinierten Cluster-Bootstrap behoben (Alexander Kukushkin)

  Postgres wird nur für eine PITR mit `hot_standby=off` gestartet und nach deren Abschluss neu gestartet.

**Fehlerbehebungen**

- Kompatibilität mit `kazoo-2.7+` (Alexander Kukushkin)

  Da Patroni Wiederholungsversuche selbst verwaltet, ist es auf das frühere Verhalten von `kazoo` angewiesen, Anfragen an einen ZooKeeper-Cluster sofort zu verwerfen, wenn keine Verbindungen verfügbar sind.

- Version des etcd-v3-Clusters wird bei bekannter Proxy-Verbindung ausdrücklich abgefragt (Alexander Kukushkin)

  Patroni greift über gRPC-gateway auf etcd-v3-Cluster zu. Je nach Clusterversion müssen unterschiedliche Endpunkte (`/v3`, `/v3beta` oder `/v3alpha`) verwendet werden. Die Version wurde bisher nur zusammen mit der Clustertopologie ermittelt, was bei Proxy-Verbindungen nie geschah.

--------

## Version 2.0.2 {#version-202}

Veröffentlicht am 2021-02-22

**Neue Funktionen**

- Extern verwaltete Replikationsslots können ignoriert werden (James Coleman)

  Patroni versucht, ihm unbekannte Replikationsslots zu entfernen. Es gibt jedoch Fälle, in denen Slots extern verwaltet werden sollten. Nun lässt sich konfigurieren, welche Slots nicht entfernt werden sollen.

- Einschränkung der Cipher Suites für die REST-API unterstützt (Gunnar "Nick" Bluth)

  Die Konfiguration erfolgt über `restapi.ciphers` oder die Umgebungsvariable `PATRONI_RESTAPI_CIPHERS`.

- Verschlüsselte TLS-Schlüssel für die REST-API unterstützt (Jonathan S. Katz)

  Die Konfiguration erfolgt über `restapi.keyfile_password` oder die Umgebungsvariable `PATRONI_RESTAPI_KEYFILE_PASSWORD`.

- REST-API-Zugangsdaten in konstanter Zeit verglichen (Alex Brasetvik)

  `hmac.compare_digest()` ersetzt `==`, das für Timing-Angriffe anfällig ist.

- Synchrone Knoten anhand des Replikationsrückstands gewählt (Krishna Sarabu)

  Überschreitet der Replikationsrückstand eines synchronen Knotens den konfigurierten Schwellwert, kann dieser auf asynchron umgestellt und/oder durch einen anderen Knoten ersetzt werden. Das Verhalten wird mit `maximum_lag_on_syncnode` gesteuert.

**Stabilitätsverbesserungen**

- Postgres wird beim benutzerdefinierten Bootstrap mit `hot_standby = off` gestartet (Igor Yanchenko)

  Bei einem benutzerdefinierten Bootstrap stellt Patroni das Basisbackup wieder her, startet Postgres und wartet auf das Ende der Recovery. Einige PostgreSQL-Parameter dürfen auf einem Standby nicht kleiner sein als auf dem Primärserver. Ist der aus WAL wiederhergestellte neue Wert höher als der konfigurierte, bricht Postgres mit PANIC ab. Um dies zu vermeiden, erfolgt die benutzerdefinierte Initialisierung ohne `hot_standby`-Modus.

- Warnung bei nicht funktionsfähigem erforderlichem Watchdog hinzugefügt (Nicolas Thauvin)

  Ist das Watchdog-Gerät im Modus required nicht beschreibbar oder fehlt es, kann das Mitglied nicht hochgestuft werden. Eine neue Warnung zeigt, wo nach der Fehlkonfiguration gesucht werden sollte.

- Ausführlichere Meldungen bei Recovery im Einzelbenutzermodus (Alexander Kukushkin)

  Erkennt Patroni, dass PostgreSQL nicht sauber heruntergefahren wurde, führt es in bestimmten Fällen eine Crash-Recovery aus, indem es Postgres im Einzelbenutzermodus startet. Schlug diese Recovery etwa wegen fehlenden Speicherplatzes fehl, wurden die Fehler bisher verschluckt.

- Kompatibilität mit dem Modul `python-consul2` ergänzt (Alexander Kukushkin, Wilfried Roset)

  Das bewährte `python-consul` wird seit einigen Jahren nicht mehr gepflegt. Deshalb entstand ein Fork mit neuen Funktionen und Fehlerbehebungen.

- `bypass_api_service` wird bei [patronictl](/de/patroni/patronictl#patronictl) nicht verwendet (Alexander Kukushkin)

  Läuft ein K8s-Pod in einem anderen Namespace als `default`, hat er nicht unbedingt genügend Berechtigungen, um den Endpunkt [kubernetes](/de/patroni/kubernetes#kubernetes) abzufragen. In diesem Fall gibt Patroni eine Warnung aus und ignoriert `bypass_api_service`. Bei [patronictl](/de/patroni/patronictl#patronictl) war diese Warnung störend.

- `raft.data_dir` wird erstellt, falls es fehlt, oder auf Schreibbarkeit geprüft (Mark Mercado)

  Dies verbessert Benutzerfreundlichkeit und Bedienbarkeit.

**Fehlerbehebungen**

- Neustart oder Hochstufung wird bei Verlust der Leader-Sperre im pausierten Modus nicht unterbrochen (Alexander Kukushkin)

  Im pausierten Modus darf Postgres ohne Sperre als Primärserver laufen.

- Problem mit `shutdown_request()` in der REST-API behoben (Nicolas Limage)

  Um SSL-Verbindungen besser zu behandeln und den Handshake bis zum Threadstart zu verzögern, überschreibt Patroni einige Methoden von `HTTPServer`. `shutdown_request()` war dabei vergessen worden.

- Wartezeit bei Verwendung von ZooKeeper korrigiert (Alexander Kukushkin)

  Zwischen den Ausführungen des HA-Codes konnte Patroni bis zu doppelt so lange wie vorgesehen schlafen.

- Ungültige `os.symlink()`-Aufrufe beim Verschieben des Datenverzeichnisses nach fehlgeschlagenem Bootstrap korrigiert (Andrew L'Ecuyer)

  Bei fehlgeschlagenem Bootstrap benennt Patroni Datenverzeichnis, pg_wal und alle Tablespaces um. Danach werden die symbolischen Links aktualisiert, damit das Dateisystem konsistent bleibt. Deren Erstellung schlug fehl, weil `src` und `dst` vertauscht waren.

- Fehler in post_bootstrap() behoben (Alexander Kukushkin)

  War kein Superuser-Passwort konfiguriert, konnte Patroni das Skript `post_init` nicht aufrufen, wodurch der gesamte Bootstrap fehlschlug.

- Problem mit pg_rewind im Standby-Cluster behoben (Alexander Kukushkin)

  Wenn der Superuser-Name von `postgres` abwich, schlug `pg_rewind` im Standby-Cluster fehl, weil die Verbindungszeichenfolge keinen Datenbanknamen enthielt.

- Abbruch nur bei ausdrücklich fehlgeschlagener Authentifizierung mit etcd v3 (Alexander Kukushkin)

  Beim Start ermittelt Patroni die Topologie des etcd-Clusters und authentifiziert sich bei Bedarf. War einer der etcd-Server unerreichbar, versuchte Patroni die Authentifizierung auf diesem Server und brach ab, statt es beim nächsten Knoten erneut zu versuchen.

- Leere Rückgabe von psutil cmdline() behandelt (Alexander Kukushkin)

  Zombie-Prozesse sind weiterhin Kindprozesse des postmaster, besitzen aber kein cmdline().

- Umgebungsvariable `PATRONI_KUBERNETES_USE_ENDPOINTS` als booleschen Wert behandelt (Alexander Kukushkin)

  Ohne diese Behandlung ließ sich `kubernetes.use_endpoints` nicht über die Umgebung deaktivieren.

- Fehler bei gleichzeitigen Endpoint-Aktualisierungen besser behandelt (Alexander Kukushkin)

  Patroni fragt das aktuelle Endpoint-Objekt ausdrücklich ab, prüft, ob der aktuelle Pod weiterhin die Leader-Sperre hält, und wiederholt die Aktualisierung.

--------

## Version 2.0.1 {#version-201}

Veröffentlicht am 2020-10-01

**Neue Funktionen**

- `more` als Pager in `patronictl edit-config` verwendet, wenn `less` fehlt (Pavel Golub)

  Unter Windows ist dies `more.com`. Außerdem wurde in `requirements.txt` `cdiff` durch `ydiff` ersetzt; [patronictl](/de/patroni/patronictl#patronictl) unterstützt aus Kompatibilitätsgründen weiterhin beide.

- `bind_addr` und `password` für `raft` unterstützt (Alexander Kukushkin)

  `raft.bind_addr` kann beim Betrieb hinter NAT nützlich sein. `raft.password` aktiviert die Verschlüsselung des Datenverkehrs und erfordert das Modul `cryptography`.

- Verbindungsparameter `sslpassword` unterstützt (Kostiantyn Nemchenko)

  Dieser Parameter wurde mit PostgreSQL 13 eingeführt.

**Stabilitätsverbesserungen**

- Verhalten im pausierten Modus geändert (Alexander Kukushkin)

  1.  Patroni ruft die Methode `bootstrap` nicht auf, wenn das Verzeichnis `PGDATA` fehlt oder leer ist.
  2.  Patroni beendet sich bei abweichender sysid im pausierten Modus nicht, sondern protokolliert nur eine Warnung.
  3.  Im pausierten Modus versucht ein Knoten nicht, den Leader-Schlüssel zu übernehmen, wenn Postgres außerhalb der Recovery läuft und Schreibzugriffe annimmt, die sysid aber nicht zum initialize-Schlüssel passt.

- `master_start_timeout` bei der Crash-Recovery angewendet (Alexander Kukushkin)

  Stürzt Postgres auf dem Leader-Knoten ab, führt Patroni eine Crash-Recovery durch, indem es Postgres im Einzelbenutzermodus startet. Währenddessen wird die Leader-Sperre aktualisiert. Ist die Crash-Recovery nach `master_start_timeout` Sekunden nicht beendet, bricht Patroni sie zwangsweise ab und gibt die Leader-Sperre frei.

- Extra `secure` aus den `urllib3`-Abhängigkeiten entfernt (Alexander Kukushkin)

  Der einzige Grund für die ursprüngliche Aufnahme war die Abhängigkeit von `ipaddress` für Python 2.7.

**Fehlerbehebungen**

- Fehler in `Kubernetes.update_leader()` behoben (Alexander Kukushkin)

  Eine unbehandelte Ausnahme verhinderte die Herabstufung des Primärservers, wenn die Aktualisierung des Leader-Objekts fehlschlug.

- Hängendes [patronictl](/de/patroni/patronictl#patronictl) bei Verwendung von RAFT behoben (Alexander Kukushkin)

  Wird [patronictl](/de/patroni/patronictl#patronictl) mit der Patroni-Konfiguration verwendet, sollte `self_addr` zu `partner_addrs` hinzugefügt werden.

- Fehler in `get_guc_value()` behoben (Alexander Kukushkin)

  Patroni konnte unter PostgreSQL 12 den Wert von `restore_command` nicht ermitteln, sodass das Nachladen fehlender WAL-Dateien für `pg_rewind` nicht funktionierte.

--------

## Version 2.0.0 {#version-200}

Veröffentlicht am 2020-09-02

Diese Version verbessert die Kompatibilität mit PostgreSQL 13, unterstützt mehrere synchrone Standbys, verbessert den Umgang mit `pg_rewind` erheblich, ergänzt etcd v3 sowie Patroni auf reinem RAFT (ohne etcd, Consul oder ZooKeeper) und ermöglicht den optionalen Aufruf des Fencing-Skripts `pre_promote`.

**Unterstützung für PostgreSQL 13**

- Kein Aufruf von `on_reload` bei der Hochstufung zum `standby_leader` unter PostgreSQL 13+ (Alexander Kukushkin)

  Bei der Hochstufung zum `standby_leader` wird `primary_conninfo` geändert, die Rolle aktualisiert und Postgres neu geladen. Da sich `on_role_change` und `on_reload` praktisch doppeln, ruft Patroni nur `on_role_change` auf.

- Verbindungsparameter `gssencmode` und `channel_binding` unterstützt (Alexander Kukushkin)

  PostgreSQL 12 führte `gssencmode` und PostgreSQL 13 `channel_binding` ein. Diese Verbindungsparameter können nun verwendet werden, wenn sie im Abschnitt `postgresql.authentication` definiert sind.

- Umbenennung von `wal_keep_segments` in `wal_keep_size` berücksichtigt (Alexander Kukushkin)

  Bei einer Fehlkonfiguration (`wal_keep_segments` unter 13 oder `wal_keep_size` unter älteren Versionen) passt Patroni die Konfiguration automatisch an.

- `pg_rewind` unter 13 nach Möglichkeit mit `--restore-target-wal` verwendet (Alexander Kukushkin)

  Unter PostgreSQL 13 prüft Patroni, ob `restore_command` konfiguriert ist, und weist `pg_rewind` an, es zu verwenden.

**Neue Funktionen**

- \[BETA\] Patroni auf reinem RAFT unterstützt (Alexander Kukushkin)

  Dies ermöglicht den Betrieb von Patroni ohne Abhängigkeiten von Drittanbietern wie etcd, Consul oder ZooKeeper. Für HA werden entweder drei Patroni-Knoten oder zwei Patroni-Knoten und ein Knoten mit `patroni_raft_controller` benötigt. Weitere Informationen stehen in der [Dokumentation](/de/patroni/config/yaml#raft_settings).

- \[BETA\] etcd-v3-Protokoll über gRPC-gateway unterstützt (Alexander Kukushkin)

  etcd 3.0 erschien vor mehr als vier Jahren; in etcd 3.4 ist v2 standardmäßig deaktiviert. Da v2 möglicherweise vollständig aus etcd entfernt wird, wurde die Unterstützung für etcd v3 in Patroni implementiert. Zur Verwendung muss in der Patroni-Konfigurationsdatei ausdrücklich der Abschnitt `etcd3` angelegt werden.

- Mehrere synchrone Standbys unterstützt (Krishna Sarabu)

  Damit kann ein Cluster mit mehr als einem synchronen Replikat betrieben werden. Die maximale Zahl synchroner Replikate steuert der neue Parameter `synchronous_node_count`. Sein Standardwert ist 1; bei [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) gleich `off` hat er keine Wirkung.

- Optionaler Aufruf des Skripts `pre_promote` hinzugefügt (Sergey Dudoladov)

  Anders als Callbacks wird `pre_promote` synchron nach dem Erlangen der Leader-Sperre, aber vor der Hochstufung von Postgres aufgerufen. Schlägt das Skript fehl oder endet es mit einem Rückgabecode ungleich null, gibt der aktuelle Knoten die Leader-Sperre frei.

- Konfigurationsverzeichnisse unterstützt (Floris van Nee)

  YAML-Dateien im Verzeichnis werden in alphabetischer Reihenfolge geladen und angewendet.

- Erweiterte Validierung von PostgreSQL-Parametern (Alexander Kukushkin)

  Unterstützt die aktuelle PostgreSQL-Version einen Parameter nicht oder ist sein Wert falsch, entfernt Patroni den Parameter vollständig oder versucht, den Wert zu korrigieren.

- Hauptthread nach Abschluss des erzwungenen Checkpoints nach einer Hochstufung aufgeweckt (Alexander Kukushkin)

  Replikate warten auf die Checkpoint-Anzeige im Mitgliedsschlüssel des Leaders im DCS. Dieser Schlüssel wird normalerweise nur einmal pro HA-Durchlauf aktualisiert. Ohne das Aufwecken des Hauptthreads müssten Replikate bis zu `loop_wait` Sekunden länger als nötig warten.

- Sicht `pg_stat_wal_receiver` unter 9.6+ verwendet (Alexander Kukushkin)

  Die Sicht enthält aktuelle Werte für `primary_conninfo` und `primary_slot_name`, während der Inhalt von `recovery.conf` veraltet sein kann.

- IPv6-Adressen in der Patroni-Konfigurationsdatei besser behandelt (Mateusz Kowalski)

  IPv6-Adressen sollen in eckigen Klammern stehen; Patroni erwartete sie jedoch ohne Klammern. Nun werden beide Formate unterstützt.

- Consul-Konfigurationsparameter `service_tags` hinzugefügt (Robert Edström)

  Er eignet sich zur dynamischen Diensterkennung, etwa durch Load-Balancer.

- SSL-Unterstützung für ZooKeeper implementiert (Kostiantyn Nemchenko)

  Dafür ist `kazoo>=2.6.0` erforderlich.

- Option `no_params` für benutzerdefinierte Bootstrap-Methoden implementiert (Kostiantyn Nemchenko)

  Damit können `wal-g`, `pgBackRest` und andere Backup-Werkzeuge ohne umschließende Shellskripte aufgerufen werden.

- WAL und Tablespaces nach fehlgeschlagener Initialisierung verschoben (Feike Steenbergen)

  Bei `reinit` entfernte Patroni bereits neben `PGDATA` auch das über einen symbolischen Link eingebundene WAL-Verzeichnis und die Tablespaces. Nun führt `move_data_directory()` einen ähnlichen Vorgang aus: WAL-Verzeichnis und Tablespaces werden umbenannt und die symbolischen Links in PGDATA aktualisiert.

**Verbesserungen der pg_rewind-Unterstützung**

- Prüfung auf divergierende Zeitleisten verbessert (Alexander Kukushkin)

  Ein Rewind ist nicht nötig, wenn die auf dem Replikat wiedergegebene Position nicht über den Umschaltpunkt hinausgeht oder das Ende des Checkpoint-Eintrags auf dem bisherigen Primärserver dem Umschaltpunkt entspricht. Um das Ende des Checkpoint-Eintrags zu ermitteln, wird `pg_waldump` verwendet und dessen Ausgabe ausgewertet.

- Das Nachladen fehlender WAL-Dateien wird versucht, wenn `pg_rewind` sie meldet (Alexander Kukushkin)

  Ein von `pg_rewind` benötigtes WAL-Segment kann bereits aus `pg_wal` verschwunden sein. Dann kann `pg_rewind` die Checkpoint-Position vor dem Divergenzpunkt nicht finden. Seit PostgreSQL 13 kann `pg_rewind` fehlende WAL-Dateien über `restore_command` nachladen. Bei älteren PostgreSQL-Versionen wertet Patroni die Fehler eines fehlgeschlagenen Rewind-Versuchs aus und versucht selbst, die fehlende WAL-Datei über `restore_command` abzurufen.

- Neue Zeitleisten im Standby-Cluster erkannt und bei Bedarf Rewind oder Neuinitialisierung ausgelöst (Alexander Kukushkin)

  Der [standby_cluster](/de/patroni/standby_cluster#standby_cluster) ist vom Primärcluster entkoppelt und erfährt daher nicht sofort von Leader-Wahlen und Zeitleistenwechseln. Um sie zu erkennen, prüft der `standby_leader` regelmäßig, ob neue History-Dateien in `pg_wal` vorhanden sind.

- Ausgabe des Verlaufsprotokolls gekürzt und übersichtlicher gestaltet (Alexander Kukushkin)

  Bei der Prüfung, ob `pg_rewind` erforderlich ist, kann Patroni die History-Datei des Primärservers protokollieren. Diese wächst mit jedem Failover/Switchover und belegt schließlich zu viele Zeilen, die überwiegend wenig hilfreich sind. Statt der Rohdaten zeigt Patroni nur noch 3 Zeilen vor und 2 Zeilen nach der aktuellen Replikat-Zeitleiste an.

**Verbesserungen unter K8s**

- Python-Modul [kubernetes](/de/patroni/kubernetes#kubernetes) entfernt (Alexander Kukushkin)

  Der offizielle Python-Client für Kubernetes enthält viel automatisch generierten Code und ist daher sehr umfangreich. Patroni verwendet nur einen kleinen Teil der K8s-API-Endpunkte, deren Unterstützung sich leicht direkt implementieren ließ.

- Umgehen des Service [kubernetes](/de/patroni/kubernetes#kubernetes) ermöglicht (Alexander Kukushkin)

  Unter K8s kommuniziert Patroni normalerweise über den Service [kubernetes](/de/patroni/kubernetes#kubernetes) mit der K8s-API. Dessen Adresse steht in `KUBERNETES_SERVICE_HOST`. Wie andere Services wird auch [kubernetes](/de/patroni/kubernetes#kubernetes) von `kube-proxy` behandelt, das je nach Konfiguration ein Userspace-Programm oder `iptables` zur Weiterleitung verwendet. Die direkte Verbindung zu den K8s-Master-Knoten ohne diese Zwischenkomponente ermöglicht eine bessere Wiederholungsstrategie und verringert das Risiko, dass Postgres bei Upgrades der K8s-Master-Knoten herabgestuft wird.

- HA-Schleifen aller Pods eines Patroni-Clusters synchronisiert (Alexander Kukushkin)

  Ohne dies verlängerte sich die Fehlererkennungszeit von `ttl` auf `ttl + loop_wait`.

- `references` und `nodename` in den Adressen der Subsets unter K8s ausgefüllt (Alexander Kukushkin)

  Einige Load-Balancer sind auf diese Angaben angewiesen.

- Mögliche Race Conditions in `update_leader()` behoben (Alexander Kukushkin)

  Gleichzeitige Aktualisierungen der Leader-ConfigMap oder des Leader-Endpoints außerhalb von Patroni können `update_leader()` scheitern lassen. In diesem Fall prüft Patroni erneut, ob der aktuelle Knoten die Leader-Sperre noch besitzt, und wiederholt die Aktualisierung.

- Patchen nicht vorhandener Konfiguration ausdrücklich verboten (Alexander Kukushkin)

  Bei anderen DCS als [kubernetes](/de/patroni/kubernetes#kubernetes) schlägt ein PATCH-Aufruf mit einer Ausnahme fehl, weil `cluster.config` den Wert `None` hat. Unter Kubernetes wurde stattdessen die Konfigurationsannotation angelegt. Dadurch konnte nach Abschluss der Initialisierung die Bootstrap-Konfiguration nicht geschrieben werden.

- Fehler im [pausierten Modus](/de/patroni/pause#pause) behoben (Alexander Kukushkin)

  Fehlte der Leader-Schlüssel, entfernten Replikate `primary_conninfo` und starteten Postgres neu, obwohl sie nichts tun sollten.

**Verbesserungen der REST-API**

- TLS-Handshake bis zum Start des Arbeitsthreads verzögert (Alexander Kukushkin, Ben Harris)

  Fand der TLS-Handshake im API-Thread statt und sendete der Client keine Daten, wurde dieser Thread blockiert (DoS-Risiko).

- `basic-auth` in der REST-API unabhängig vom Clientzertifikat geprüft (Alexander Kukushkin)

  Bisher wurde nur das Clientzertifikat geprüft. Beide Prüfungen unabhängig auszuführen, ist ein berechtigter Anwendungsfall.

- Doppeltes `CRLF` nach den HTTP-Headern einer `OPTIONS`-Anfrage geschrieben (Sergey Burladyan)

  HAProxy kam mit einem einzelnen `CRLF` zurecht, während der Consul-Health-Check eine unterbrochene Verbindung und ein unerwartetes EOF meldete.

- `GET /cluster` zeigte veraltete Mitgliedsinformationen für ZooKeeper (Alexander Kukushkin)

  Der Endpunkt verwendete die interne Clustersicht von Patroni. Für Patroni selbst war dies unproblematisch; nach außen müssen jedoch aktuelle Informationen angezeigt werden, insbesondere zum Replikationsrückstand.

- Health Checks für Standby-Cluster korrigiert (Alexander Kukushkin)

  `GET /standby-leader` antwortete für einen Primärserver und `GET /master` für einen `standby_leader` fälschlich mit 200.

- `DELETE /switchover` implementiert (Alexander Kukushkin)

  Der REST-API-Aufruf löscht ein geplantes Switchover.

- Endpunkte `/readiness` und `/liveness` erstellt (Alexander Kukushkin)

  Sie können nützlich sein, um beeinträchtigte Pods aus den Subset-Adressen zu entfernen, wenn der K8s-Service mit Label-Selektoren verwendet wird.

- REST-API-Health-Checks `GET /replica` und `GET /async` erweitert (Krishna Sarabu, Alexander Kukushkin)

  Die Prüfungen unterstützen nun das optionale Schlüsselwort `?lag=<max-lag>` und antworten nur dann mit 200, wenn der Rückstand kleiner als der angegebene Wert ist. Dabei ist zu beachten, dass die WAL-Position des Leaders nur alle `loop_wait` Sekunden aktualisiert wird!

- Benutzerdefinierte HTTP-Header in REST-API-Antworten unterstützt (Yogesh Sharma)

  Dies kann bei Anfragen aus einem Browser nützlich sein.

**Verbesserungen in patronictl**

- Kein Aufruf eines nicht vorhandenen Leaders durch `patronictl pause` (Alexander Kukushkin)

  Beim Pausieren eines Clusters ohne Leader unter K8s warnte [patronictl](/de/patroni/patronictl#patronictl), dass das Mitglied "None" nicht erreichbar sei.

- Fehlendes `conn_url` eines Mitglieds behandelt (Alexander Kukushkin)

  Unter K8s kann ein Pod die erforderlichen Annotationen noch nicht besitzen, weil Patroni noch nicht läuft. Dies ließ [patronictl](/de/patroni/patronictl#patronictl) fehlschlagen.

- Ausgabe der Clustertopologie als ASCII-Darstellung hinzugefügt (Maxim Fedotov, Alexander Kukushkin)

  Dies gibt einen hilfreichen Überblick über Cluster mit kaskadierender Replikation.

- `patronictl flush switchover` implementiert (Alexander Kukushkin)

  Bisher konnte `patronictl flush` nur geplante Neustarts abbrechen.

**Fehlerbehebungen**

- Attributfehler beim Cluster-Bootstrap mit vorhandenem PGDATA (Krishna Sarabu)

  Beim Anlegen oder Aktualisieren von `/history` griff Patroni auf ein Objekt `ClusterConfig` zu, das im DCS noch nicht angelegt war.

- Ausnahmebehandlung für Consul verbessert (Alexander Kukushkin)

  Eine unbehandelte Ausnahme in `touch_member()` ließ den gesamten Patroni-Prozess abstürzen.

- `synchronous_commit=local` für das Skript `post_init` erzwungen (Alexander Kukushkin)

  Beim Anlegen der Benutzer (`replication`, `rewind`) tat Patroni dies bereits; bei `post_init` war es übersehen worden. Setzte das Skript den Wert nicht selbst, konnte die Initialisierung im [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) nicht abgeschlossen werden.

- `maxsize` im Consul-Pool-Manager erhöht (ponvenkates)

  Der Standardwert `size=1` erzeugte einige Warnungen.

- Patroni meldete Postgres fälschlich als laufend (Alexander Kukushkin)

  Der Zustand wurde beispielsweise nicht aktualisiert, wenn Postgres wegen eines vollen Datenträgers abstürzte.

- `*` statt fehlender oder leerer Werte in `pgpass` geschrieben (Alexander Kukushkin)

  War etwa `standby_cluster.port` nicht angegeben, wurde die Datei `pgpass` fehlerhaft erzeugt.

- Erstellung eines physischen Replikationsslots für den Leader mit Sonderzeichen im Namen übersprungen (Krishna Sarabu)

  Bei definierten `slots` schien Patroni für den Leader einen ungenutzten Slot anzulegen, wenn dessen Name Sonderzeichen wie '-' enthielt, etwa "abc-us-1".

- Entfernen einer nicht vorhandenen `pg_hba.conf` beim benutzerdefinierten Bootstrap vermieden (Krishna Sarabu)

  Patroni schlug fehl, wenn `pg_hba.conf` nach dem benutzerdefinierten Bootstrap außerhalb von `pgdata` lag.

--------

## Version 1.6.5 {#version-165}

Veröffentlicht am 2020-08-23

**Neue Funktionen**

- Zeitüberschreitung beim Stoppen des Primärservers (Krishna Sarabu)

  Anzahl der Sekunden, die Patroni beim Stoppen von Postgres warten darf. Wirkt nur bei aktiviertem [synchronous_mode](/de/patroni/replication_modes#synchronous_mode). Ist der Wert größer als 0 und [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) aktiviert, sendet Patroni `SIGKILL` an den Postmaster, wenn das Stoppen länger als der mit `master_stop_timeout` festgelegte Wert dauert. Der Wert ist entsprechend der gewünschten Abwägung zwischen Dauerhaftigkeit und Verfügbarkeit zu wählen. Ist der Parameter nicht gesetzt oder nicht positiv, hat `master_stop_timeout` keine Wirkung.

- Keinen permanenten physischen Slot mit dem Namen des Primärservers erstellen (Alexander Kukushkin)

  Ein häufiges Problem ist, dass der Primärserver WAL-Segmente wiederverwendet, während das Replikat ausgefallen ist. Für statische Cluster mit einer festen Anzahl von Knoten und unveränderlichen Namen gibt es nun eine gute Lösung: Die Namen aller Knoten unter `slots` aufführen. Dann entfernt der Primärserver den Slot nicht, wenn der Knoten ausgefallen ist (also nicht im DCS registriert ist).

- Erster Entwurf einer Konfigurationsvalidierung (Igor Yanchenko)

  Mit `patroni --validate-config patroni.yaml` lässt sich die Patroni-Konfiguration validieren.

- Maximale Länge der Timeline-Historie konfigurierbar machen (Krishna Sarabu)

  Patroni schreibt die Historie von Failover und Switchover in den Schlüssel `/history` im DCS. Mit der Zeit wird dieser Schlüssel groß, obwohl meist nur die letzten Zeilen von Interesse sind. Mit `max_timelines_history` lässt sich die maximale Anzahl der im DCS gespeicherten Einträge der Timeline-Historie festlegen.

- Kompatibilität mit Kazoo 2.7.0 (Danyal Prout)

  Die Signaturen einiger nicht öffentlicher Methoden von Kazoo wurden geändert, auf die Patroni angewiesen war.

**Verbesserungen in patronictl**

- Tags der Mitglieder anzeigen (Kostiantyn Nemchenko, Alexander Kukushkin)

  Tags werden für jeden Knoten einzeln konfiguriert. Bisher gab es keine einfache Möglichkeit, sich einen Überblick darüber zu verschaffen.

- Ausgabe der Mitglieder verbessern (Alexander Kukushkin)

  Der redundante Cluster-Name wird nur noch im Tabellenkopf angezeigt, nicht mehr in jeder Zeile.

``` bash
$ patronictl list
+ Cluster: batman (6813309862653668387) +---------+----+-----------+---------------------+
|    Member   |      Host      |  Role  |  State  | TL | Lag in MB | Tags                |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql0 | 127.0.0.1:5432 | Leader | running |  3 |           | clonefrom: true     |
|             |                |        |         |    |           | noloadbalance: true |
|             |                |        |         |    |           | nosync: true        |
+-------------+----------------+--------+---------+----+-----------+---------------------+
| postgresql1 | 127.0.0.1:5433 |        | running |  3 |       0.0 |                     |
+-------------+----------------+--------+---------+----+-----------+---------------------+
```

- Mit Fehler abbrechen, wenn eine ausdrücklich angegebene Konfigurationsdatei nicht gefunden wird (Kaarel Moppel)

  Zuvor gab [patronictl](/de/patroni/patronictl#patronictl) lediglich eine `DEBUG`-Meldung aus.

- Fehler in patronictl durch nicht initialisierten K8s-Pod beheben (Alexander Kukushkin)

  Patroni ist unter K8s auf bestimmte Pod-Annotationen angewiesen. Wenn einer der Patroni-Pods startet oder stoppt, liegt noch keine gültige Annotation vor, und [patronictl](/de/patroni/patronictl#patronictl) brach mit einer Ausnahme ab.

**Stabilitätsverbesserungen**

- Nach fehlgeschlagenem LIST-Aufruf an den K8s-API-Server 1 Sekunde warten (Alexander Kukushkin)

  Dies verhindert vor allem eine Flut von Protokollmeldungen, hilft aber auch dabei, dem Hauptthread weiterhin Rechenzeit zu ermöglichen.

- Anfrage wiederholen, wenn die K8s-API den HTTP-Header `retry-after` zurückgibt (Alexander Kukushkin)

  Bei Überlastung durch Anfragen kann der K8s-API-Server um einen erneuten Versuch bitten.

- `KUBERNETES_`-Umgebungsvariablen aus der Umgebung des Postmasters entfernen (Feike Steenbergen)

  PostgreSQL benötigt die Umgebungsvariablen `KUBERNETES_` nicht. Sind sie für den Postmaster verfügbar, können jedoch auch Backends und reguläre Datenbankbenutzer darauf zugreifen, etwa über pl/perl.

- Tablespaces bei der Neuinitialisierung bereinigen (Krishna Sarabu)

  Bei der Neuinitialisierung entfernte Patroni nur `PGDATA` und ließ benutzerdefinierte Tablespace-Verzeichnisse bestehen. Dadurch geriet Patroni in eine Schleife wiederholter Neuinitialisierungen. Bisher ließ sich das Problem mit einem Skript für einen [benutzerdefinierten Bootstrap](/de/patroni/replica_bootstrap#custom_bootstrap) umgehen.

- Nach der Hochstufung ausdrücklich `CHECKPOINT` ausführen (Alexander Kukushkin)

  Dadurch verkürzt sich die Zeit, bis der neue Primärserver für `pg_rewind` verwendbar ist.

- etcd-Mitglieder gezielt aktualisieren (Alexander Kukushkin)

  Schlägt eine Anfrage bei allen Mitgliedern des etcd-Clusters fehl, prüft Patroni vor dem nächsten Versuch erneut die `A`- oder `SRV`-Einträge auf Änderungen der IPs/Hosts.

- Fehlende Werte aus `pg_controldata` überspringen (Feike Steenbergen)

  Werte fehlen, wenn ausführbare Dateien einer Version verwendet werden, die nicht zu PGDATA passt. Patroni versucht dennoch, Postgres zu starten. Postgres meldet dann die abweichende Hauptversion und bricht mit einem Fehler ab.

**Fehlerbehebungen**

- SSL-Prüfung für Consul bei Bedarf deaktivieren (Julien Riou)

  Ab einer bestimmten Version von `urllib3` muss `cert_reqs` ausdrücklich auf `ssl.CERT_NONE` gesetzt werden, um die SSL-Prüfung tatsächlich zu deaktivieren.

- Nicht in jedem Durchlauf der HA-Schleife eine Replikationsverbindung öffnen (Alexander Kukushkin)

  Diese Regression wurde in 1.6.4 eingeführt.

- Callback `on_role_change` auf einem ausgefallenen Primärserver aufrufen (Alexander Kukushkin)

  Unter bestimmten Umständen konnte die virtuelle IP am alten Primärserver verbleiben. Diese Regression wurde in 1.4.5 eingeführt.

- Rewind-Zustand zurücksetzen, wenn Postgres nach erfolgreichem pg_rewind gestartet wurde (Alexander Kukushkin)

  Aufgrund dieses Fehlers startete Patroni im Pausenmodus ein manuell heruntergefahrenes Postgres wieder.

- Bei der Prüfung von `recovery.conf` den Wert von `recovery_min_apply_delay` in `ms` umrechnen

  War `recovery_min_apply_delay` unter einer PostgreSQL-Version vor 12 konfiguriert, startete Patroni das Replikat endlos neu.

- Kompatibilität mit PyInstaller (Alexander Kukushkin)

  PyInstaller bündelt Python-Anwendungen zu eigenständig ausführbaren Dateien. Die Kompatibilität ging beim Wechsel von `fork` zu `spawn` für `multiprocessing` verloren.

--------

## Version 1.6.4 {#version-164}

Veröffentlicht am 2020-01-27

**Neue Funktionen**

- Option `--wait` für `patronictl reinit` implementieren (Igor Yanchenko)

  Mit der Option `--wait` wartet Patronictl auf den Abschluss von `reinit`.

- Weitere Verbesserungen der Windows-Unterstützung (Igor Yanchenko, Alexander Kukushkin)

  1.  Alle für Integrationstests verwendeten Shell-Skripte wurden in Python neu geschrieben.
  2.  Auf Nicht-POSIX-Systemen wird Postgres mit `pg_ctl kill` gestoppt.
  3.  Es wird nicht versucht, Unix-Domain-Sockets zu verwenden.

**Stabilitätsverbesserungen**

- Sicherstellen, dass `unix_socket_directories` und `stats_temp_directory` existieren (Igor Yanchenko)

  Beim Start von Patroni und Postgres wird geprüft, ob `unix_socket_directories` und `stats_temp_directory` existieren, andernfalls wird versucht, sie anzulegen. Schlägt das Anlegen fehl, beendet sich Patroni.

- Sicherstellen, dass `postgresql.pgpass` an einem Ort liegt, auf den Patroni Schreibzugriff hat (Igor Yanchenko)

  Ohne Schreibzugriff beendet sich Patroni mit einer Ausnahme.

- Consul-Prüfung `serfHealth` standardmäßig deaktivieren (Kostiantyn Nemchenko)

  Selbst bei kleinen Netzwerkproblemen führt eine fehlgeschlagene `serfHealth`-Prüfung dazu, dass alle dem Knoten zugeordneten Sessions ungültig werden. Dadurch geht der Leader-Schlüssel deutlich vor Ablauf von `ttl` verloren, was unerwünschte Neustarts von Replikaten und möglicherweise eine Herabstufung des Primärservers verursacht.

- TCP-Keepalives für Verbindungen zur K8s-API konfigurieren (Alexander Kukushkin)

  Werden nach TTL Sekunden keine Daten vom Socket empfangen, kann die Verbindung als unterbrochen gelten.

- Protokollierung von Passwörtern bei der Benutzererstellung vermeiden (Alexander Kukushkin)

  Wird das Passwort zurückgewiesen oder ist die Protokollierung ausführlich beziehungsweise gar nicht konfiguriert, kann das Passwort in den Postgres-Protokollen landen. Um dies zu vermeiden, setzt Patroni `log_statement`, `log_min_duration_statement` und `log_min_error_statement` vor dem Versuch, einen Benutzer zu erstellen oder zu aktualisieren, auf sichere Werte.

**Fehlerbehebungen**

- Auf kaskadierenden Replikaten `restore_command` aus der Konfiguration [standby_cluster](/de/patroni/standby_cluster#standby_cluster) verwenden (Alexander Kukushkin)

  Der `standby_leader` tat dies bereits seit Einführung der Funktion. Geschieht dies nicht auch auf Replikaten, können sie möglicherweise nicht zum Standby-Leader aufholen.

- Vom Standby-Cluster gemeldete Timeline aktualisieren (Alexander Kukushkin)

  Bei einem Timeline-Wechsel replizierte der Standby-Cluster korrekt vom Primärserver, aber [patronictl](/de/patroni/patronictl#patronictl) meldete die alte Timeline.

- Bestimmte Recovery-Parameter in custom_conf zulassen (Alexander Kukushkin)

  Bei der Validierung der Recovery-Parameter auf einem Replikat überspringt Patroni `archive_cleanup_command`, `promote_trigger_file`, `recovery_end_command`, `recovery_min_apply_delay` und `restore_command`, wenn sie nicht in der Patroni-Konfiguration, sondern in anderen Dateien als `postgresql.auto.conf` oder `postgresql.conf` festgelegt sind.

- Behandlung von PostgreSQL-Parametern mit Punkt im Namen verbessern (Alexander Kukushkin)

  Solche Parameter können von Erweiterungen definiert werden, wobei die Einheit nicht unbedingt eine Zeichenkette ist. Eine Wertänderung kann einen Neustart erfordern, etwa bei `pg_stat_statements.max`.

- Ausnahmebehandlung beim Herunterfahren verbessern (Alexander Kukushkin)

  Beim Herunterfahren versucht Patroni, seinen Status im DCS zu aktualisieren. Ist der DCS nicht erreichbar, kann eine Ausnahme auftreten. Die fehlende Ausnahmebehandlung verhinderte das Beenden des Protokollierungsthreads.

--------

## Version 1.6.3 {#version-163}

Veröffentlicht am 2019-12-05

**Fehlerbehebungen**

- Passwort bei der Ausführung von `pg_rewind` nicht offenlegen (Alexander Kukushkin)

  Der Fehler wurde mit [\#1301](https://github.com/patroni/patroni/pull/1301) eingeführt.

- Verbindungsparameter aus `postgresql.authentication` auf `pg_basebackup` und benutzerdefinierte Methoden zur Replikaterstellung anwenden (Alexander Kukushkin)

  Diese verwendeten eine URL-artige Verbindungszeichenfolge, weshalb die Parameter nie angewendet wurden.

--------

## Version 1.6.2 {#version-162}

Veröffentlicht am 2019-12-05

**Neue Funktionen**

- `patroni --version` implementieren (Igor Yanchenko)

  Der Befehl gibt die aktuelle Patroni-Version aus und beendet sich.

- HTTP-Header `user-agent` für alle HTTP-Anfragen setzen (Alexander Kukushkin)

  Patroni kommuniziert über HTTP mit den APIs von Consul, etcd und Kubernetes. Ein gezielt zusammengesetzter `user-agent` (z. B. `Patroni/1.6.2 Python/3.6.8 Linux`) kann bei der Fehlersuche und Überwachung hilfreich sein.

- Protokollstufe für Ausnahme-Tracebacks konfigurierbar machen (Igor Yanchenko)

  Bei `log.traceback_level=DEBUG` werden Tracebacks nur angezeigt, wenn `log.level=DEBUG` gesetzt ist. Das Standardverhalten bleibt unverändert.

**Stabilitätsverbesserungen**

- Beim Suchen des in der Konfigurationsdatei benötigten Moduls nicht alle DCS-Module importieren (Alexander Kukushkin)

  Wird beispielsweise nur Zookeeper benötigt, müssen die Module für etcd, Consul und Kubernetes nicht importiert werden. Das reduziert den Speicherverbrauch und vermeidet die INFO-Meldungen `Failed to import smth`.

- Python-Modul `requests` aus den expliziten Abhängigkeiten entfernen (Alexander Kukushkin)

  Es wurde für keine kritische Funktion verwendet, verursachte aber bei neuen Versionen von `urllib3` zahlreiche Probleme.

- Behandlung von `etcd.hosts` als kommagetrennter Zeichenkette statt YAML-Array verbessern (Igor Yanchenko)

  Zuvor führte das Format `host1:port1, host2:port2` (mit Leerzeichen nach dem Komma) zu einem Fehler.

**Verbesserungen der Bedienbarkeit**

- In [patronictl](/de/patroni/patronictl#patronictl) keine Auswahl aus einer leeren Mitgliederliste verlangen (Igor Yanchenko)

  Bei einem falschen Cluster-Namen wird eine Ausnahme ausgelöst, statt zur Auswahl eines Mitglieds aus einer leeren Liste aufzufordern.

- Aussagekräftigere Fehlermeldung, wenn sich die REST API nicht an eine Adresse binden kann (Igor Yanchenko)

  Für unerfahrene Nutzer kann die Ursache anhand eines Python-Stacktraces schwer zu erkennen sein.

**Fehlerbehebungen**

- Berechnung von `wal_buffers` korrigieren (Alexander Kukushkin)

  In PostgreSQL 11 wurde die Basiseinheit von Blöcken mit 8 kB auf Bytes geändert.

- `passfile` in `primary_conninfo` nur unter PostgreSQL 10+ verwenden (Alexander Kukushkin)

  Bei älteren Versionen ist die Funktion von `passfile` nur gewährleistet, wenn die neueste Version von `libpq` installiert ist.

--------

## Version 1.6.1 {#version-161}

Veröffentlicht am 2019-11-15

**Neue Funktionen**

- Umgebungsvariable `PATRONICTL_CONFIG_FILE` hinzufügen (msvechla)

  Damit lässt sich das Argument `--config-file` für [patronictl](/de/patroni/patronictl#patronictl) über die Umgebung konfigurieren.

- `patronictl history` implementieren (Alexander Kukushkin)

  Der Befehl zeigt die Historie von Failover und Switchover.

- Bei `pg_rewind` den Wert `-c statement_timeout=0` in `PGOPTIONS` übergeben (Alexander Kukushkin)

  Dadurch wird verhindert, dass eine von pg_rewind ausgeführte Anweisung abgebrochen wird, weil `statement_timeout` auf dem Server sehr niedrig eingestellt ist.

- Niedrigere Werte für die PostgreSQL-Konfiguration zulassen (Soulou)

  Patroni ließ für einige PostgreSQL-Konfigurationsparameter keine Werte unterhalb fest programmierter Grenzen zu. Die zulässigen Mindestwerte wurden gesenkt; die Standardwerte bleiben unverändert.

- Zertifikatsbasierte Authentifizierung ermöglichen (Jonathan S. Katz)

  Diese Funktion ermöglicht zertifikatsbasierte Authentifizierung für Superuser-, Replikations- und Rewind-Konten. Außerdem kann der gewünschte `sslmode` für die Verbindung festgelegt werden.

- In `primary_conninfo` anstelle des Passworts `passfile` verwenden (Alexander Kukushkin)

  Dadurch müssen für postgresql.conf keine Berechtigungen von `600` gesetzt werden.

- `pg_ctl reload` unabhängig von Konfigurationsänderungen ausführen (Alexander Kukushkin)

  Manche Konfigurationsdateien werden möglicherweise nicht von Patroni verwaltet. Beim Neuladen über die REST API oder durch Senden von SIGHUP an den Patroni-Prozess wird üblicherweise erwartet, dass auch Postgres neu geladen wird. Zuvor geschah dies nicht, wenn der Abschnitt `postgresql` der Patroni-Konfiguration unverändert war.

- Alle Recovery-Parameter vergleichen, nicht nur `primary_conninfo` (Alexander Kukushkin)

  Zuvor prüfte die Methode `check_recovery_conf()` nur Änderungen an `primary_conninfo` und berücksichtigte keine anderen Recovery-Parameter.

- Einige Recovery-Parameter ohne Neustart anwenden können (Alexander Kukushkin)

  Ab PostgreSQL 12 lassen sich folgende Recovery-Parameter ohne Neustart ändern: `archive_cleanup_command`, `promote_trigger_file`, `recovery_end_command` und `recovery_min_apply_delay`. Diese Liste wird in künftigen Postgres-Versionen erweitert, und Patroni wird dies automatisch unterstützen.

- Änderung von `use_slots` im laufenden Betrieb ermöglichen (Alexander Kukushkin)

  Zuvor mussten dafür Patroni neu gestartet und Slots manuell entfernt werden.

- Beim Start von Postgres nur Umgebungsvariablen mit dem Präfix `PATRONI_` entfernen (Cody Coons)

  Dadurch werden zahlreiche Probleme beim Einsatz verschiedener Foreign Data Wrappers gelöst.

**Stabilitätsverbesserungen**

- Bei der Arbeit mit der K8s-API LIST + WATCH verwenden (Alexander Kukushkin)

  Dadurch lassen sich Objektänderungen (Pods, Endpoints/ConfigMaps) effizient empfangen, und die K8s-Masterknoten werden weniger belastet.

- Ablauf verbessern, wenn PGDATA beim Bootstrap nicht leer ist (Alexander Kukushkin)

  Laut dem Quellcode von `initdb` kann PGDATA als leer gelten, wenn es lediglich `lost+found` und `.dotfiles` enthält. Patroni verhält sich nun ebenso. Ist `PGDATA` nicht leer und aus Sicht von `pg_controldata` zugleich ungültig, meldet Patroni einen Fehler und beendet sich.

- Aufwendigen Aufruf von `os.listdir()` in jedem HA-Schleifendurchlauf vermeiden (Alexander Kukushkin)

  Unter hoher IO-Last kann `os.listdir()` mehrere Sekunden oder sogar Minuten benötigen und die HA-Schleife von Patroni erheblich beeinträchtigen. Wegen ausbleibender Aktualisierungen kann dadurch sogar der Leader-Schlüssel aus dem DCS verschwinden. Eine bessere und weniger aufwendige Prüfung, ob PGDATA nicht leer ist, besteht darin, das Vorhandensein der Datei `global/pg_control` in PGDATA zu prüfen. Dies wird nun verwendet.

- Verbesserungen an der Protokollierungsinfrastruktur (Alexander Kukushkin)

  Zuvor konnten beim Herunterfahren die letzten Protokollzeilen verloren gehen, weil der Protokollierungsthread ein `daemon`-Thread war.

- Unter Python 3.4+ die Multiprocessing-Startmethode `spawn` verwenden (Maciej Kowalczyk)

  In Python besteht ein bekanntes [Problem](https://bugs.python.org/issue6721) beim Zusammenspiel von Threads und Multiprocessing. Der Wechsel von der Standardmethode `fork` zu `spawn` wird als Umgehung empfohlen. Andernfalls kann der Prozess zum Starten des Postmasters hängen bleiben, und Patroni meldet endlos `INFO: restarting after failure in progress`, obwohl Postgres tatsächlich läuft.

**Verbesserungen der REST API**

- Prüfung von Client-Zertifikaten in der REST API ermöglichen (Alexander Kukushkin)

  Bei `verify_client` mit dem Wert `required` prüft Patroni Client-Zertifikate für alle REST-API-Aufrufe. Bei `optional` werden Client-Zertifikate für alle unsicheren REST-API-Endpunkte geprüft.

- Bei der Health-Check-Anfrage `GET /replica` den Antwortcode 503 zurückgeben, wenn Postgres nicht läuft (Alexander Anikin)

  Postgres kann längere Zeit in der Recovery verbringen, bevor es Client-Verbindungen annimmt.

- Endpunkte `/history` und `/cluster` implementieren (Alexander Kukushkin)

  Der Endpunkt `/history` zeigt den Inhalt des Schlüssels `history` im DCS. Der Endpunkt `/cluster` zeigt alle Cluster-Mitglieder und Betriebsinformationen, etwa ausstehende oder geplante Neustarts beziehungsweise Switchover.

**Verbesserungen der etcd-Unterstützung**

- Bei internem etcd-RAFT-Fehler erneut versuchen (Alexander Kukushkin)

  Beim Herunterfahren sendet ein etcd-Knoten `response code=300, data='etcdserver: server stopped'`. Dies führte dazu, dass Patroni den Primärserver herabstufte.

- Wiederholungsversuche für etcd-Anfragen nicht zu früh aufgeben (Alexander Kukushkin)

  Bei Netzwerkproblemen hatte Patroni die Liste der etcd-Knoten schnell ausgeschöpft und gab auf, ohne die gesamte Zeit `retry_timeout` zu nutzen. Dies konnte zur Herabstufung des Primärservers führen.

**Fehlerbehebungen**

- `synchronous_commit` beim Erteilen von Ausführungsrechten an den Benutzer für `pg_rewind` deaktivieren (kremius)

  Beim Bootstrap mit `synchronous_mode_strict: true` wartete die Anweisung `GRANT EXECUTE` unbegrenzt, da keine synchronen Standby-Knoten verfügbar waren.

- Speicherleck unter Python 3.7 beheben (Alexander Kukushkin)

  Patroni verwendet `ThreadingMixIn` zur Verarbeitung von REST-API-Anfragen. Seit Python 3.7 sind die für jede Anfrage erzeugten Threads standardmäßig keine Daemon-Threads.

- Race Conditions bei asynchronen Aktionen beheben (Alexander Kukushkin)

  Es konnte vorkommen, dass `patronictl reinit --force` durch den Versuch überschrieben wurde, ein gestopptes Postgres wiederherzustellen. Dadurch versuchte Patroni, Postgres zu starten, während das Basis-Backup noch lief.

- Race Condition in der Methode `postmaster_start_time()` beheben (Alexander Kukushkin)

  Wird die Methode aus dem REST-API-Thread ausgeführt, muss ein separates Cursor-Objekt erstellt werden.

- Fehler bei der Hochstufung synchroner Standbys mit Großbuchstaben im Namen beheben (Alexander Kukushkin)

  Der Name wurde in Kleinbuchstaben umgewandelt, weil Postgres beim Vergleich von `application_name` mit dem Wert in `synchronous_standby_names` ebenso vorging.

- Vor dem Start eines neuen Callbacks alle Kindprozesse zusammen mit dem Callback-Prozess beenden (Alexander Kukushkin)

  Andernfalls lassen sich Callbacks in Bash nur schwer implementieren, und es können schließlich zwei Callbacks gleichzeitig laufen.

- Problem mit 'start failed' beheben (Alexander Kukushkin)

  Unter bestimmten Bedingungen konnte der Postgres-Zustand auf 'start failed' gesetzt werden, obwohl Postgres lief.

--------

## Version 1.6.0 {#version-160}

Veröffentlicht am 2019-08-05

Diese Version ergänzt die Kompatibilität mit PostgreSQL 12, ermöglicht pg_rewind ohne Superuser unter PostgreSQL 11 und neuer und aktiviert die IPv6-Unterstützung.

**Neue Funktionen**

- Psycopg2 aus den Abhängigkeiten entfernen; separate Installation erforderlich (Alexander Kukushkin)

  Ab 2.8.0 wurde `psycopg2` in zwei Pakete aufgeteilt: `psycopg2` und `psycopg2-binary`. Beide konnten gleichzeitig an derselben Stelle im Dateisystem installiert werden. Um Abhängigkeitsprobleme zu verringern, bleibt die Installationsmethode den Nutzern überlassen. Die verfügbaren Möglichkeiten beschreibt die [Dokumentation](/de/patroni/installation#psycopg2_install_options).

- Kompatibilität mit PostgreSQL 12 (Alexander Kukushkin)

  Ab PostgreSQL 12 gibt es keine `recovery.conf` mehr; alle bisherigen Recovery-Parameter wurden in [GUCs](https://www.enterprisedb.com/blog/what-guc-variable) umgewandelt. Zum Schutz vor `ALTER SYSTEM SET primary_conninfo` und ähnlichen Änderungen analysiert Patroni `postgresql.auto.conf` und entfernt daraus alle Standby- und Recovery-Parameter. Die Patroni-Konfiguration bleibt abwärtskompatibel: Obwohl `restore_command` nun ein GUC ist, kann es weiterhin im Abschnitt `postgresql.recovery_conf.restore_command` angegeben werden. Patroni schreibt es für PostgreSQL 12 in `postgresql.conf`.

- `pg_rewind` ohne Superuser unter PostgreSQL 11 und neuer ermöglichen (Alexander Kukushkin)

  Für diese Funktion müssen `username` und `password` im Abschnitt `postgresql.authentication.rewind` der Patroni-Konfigurationsdatei festgelegt werden. Bei einem bestehenden Cluster muss der Benutzer manuell erstellt und für einige Funktionen die Berechtigung `GRANT EXECUTE` erteilt werden. Weitere Einzelheiten finden sich in der PostgreSQL-[Dokumentation](https://www.postgresql.org/docs/11/app-pgrewind.html#id-1.9.5.8.8).

- Tatsächliche und gewünschte Werte von `primary_conninfo` auf Replikaten gezielt vergleichen (Alexander Kukushkin)

  Dies kann einen Neustart des Replikats vermeiden, wenn ein bestehender Primärserver-/Standby-Cluster auf die Verwaltung durch Patroni umgestellt wird.

- IPv6-Unterstützung (Alexander Kukushkin)

  Es gab zwei wesentliche Probleme: Der REST-API-Dienst von Patroni lauschte nur auf `0.0.0.0`, und IPv6-Adressen in `api_url` und `conn_url` wurden nicht korrekt in eckige Klammern gesetzt.

- Kerberos-Unterstützung (Ajith Vilas, Alexander Kukushkin)

  Damit kann zwischen Postgres-Knoten Kerberos-Authentifizierung verwendet werden, anstatt Passwörter in der Patroni-Konfigurationsdatei festzulegen.

- `pg_ident.conf` verwalten (Alexander Kukushkin)

  Diese Funktion arbeitet ähnlich wie `pg_hba.conf`: Ist `postgresql.pg_ident` in der Konfigurationsdatei oder im DCS definiert, schreibt Patroni dessen Wert in `pg_ident.conf`. Ist jedoch `postgresql.parameters.ident_file` definiert, geht Patroni davon aus, dass `pg_ident` extern verwaltet wird, und aktualisiert die Datei nicht.

**Verbesserungen der REST API**

- Endpunkt `/health` hinzufügen (Wilfried Roset)

  Er gibt nur dann den HTTP-Statuscode 200 zurück, wenn PostgreSQL läuft.

- Endpunkte `/read-only` und `/read-write` hinzufügen (Julien Riou)

  Der Endpunkt `/read-only` verteilt Lesezugriffe auf Replikate und den Primärserver. Der Endpunkt `/read-write` ist ein Alias für `/primary`, `/leader` und `/master`.

- REST-API-Socket mit `SSLContext` umschließen (Julien Riou)

  `ssl.wrap_socket()` ist veraltet und ließ weiterhin Protokolle wie TLS 1.1 zu, die demnächst ebenfalls veraltet sein würden.

**Verbesserungen der Protokollierung**

- Zweistufige Protokollierung (Alexander Kukushkin)

  Alle Protokollmeldungen werden zunächst in eine Warteschlange im Arbeitsspeicher geschrieben und später asynchron aus einem separaten Thread nach stderr oder in eine Datei ausgegeben. Die maximale Größe der Warteschlange ist begrenzt und konfigurierbar. Wird die Grenze erreicht, gehen Protokollmeldungen verloren. Dies ist weiterhin besser, als die HA-Schleife zu blockieren.

- Debug-Protokollierung für API-Aufrufe mit GET/OPTIONS einschließlich Latenz aktivieren (Jan Tomsa)

  Dies erleichtert die Fehlersuche bei Health Checks durch HAProxy, Consul oder andere Werkzeuge, die den Primärserver beziehungsweise die Replikate ermitteln.

- In Retry abgefangene Ausnahmen protokollieren (Daniel Kucera)

  Sobald die maximale Anzahl von Versuchen oder die Wartezeit erreicht ist, wird die letzte Ausnahme protokolliert. Dies soll die Fehlersuche bei gestörter Kommunikation mit dem DCS erleichtern.

**Verbesserungen in patronictl**

- Dialoge für geplante Switchover und Neustarts verbessern (Rafia Sabih)

  Zuvor berücksichtigten die Dialoge geplante Aktionen nicht und waren dadurch irreführend.

- Existenz der Konfigurationsdatei prüfen (Wilfried Roset)

  Wenn die angegebene Datei nicht existiert, wird dies ausdrücklich gemeldet, statt es stillschweigend zu ignorieren und damit Missverständnisse zu begünstigen.

- Ersatzwert für `EDITOR` hinzufügen (Wilfried Roset)

  War die Umgebungsvariable `EDITOR` nicht definiert, brach `patronictl edit-config` mit `PatroniCtlException` ab. Die neue Strategie versucht zunächst `editor`, dann `vi`, das auf den meisten Systemen verfügbar sein sollte.

**Verbesserungen der Consul-Unterstützung**

- Konsistenzmodus für Consul konfigurierbar machen (Jan Tomsa)

  Weitere Informationen zum Konsistenzmodus finden sich [hier](https://www.consul.io/api/features/consistency.html).

- Consul-Konfiguration bei SIGHUP neu laden (Cameron Daniel Kucera, Alexander Kukushkin)

  Dies ist besonders nützlich, wenn der Wert von `token` geändert wird.

**Fehlerbehebungen**

- Sonderfall bei Switchover/Failover beheben (Sharoon Thomas)

  Die Variable `scheduled_at` kann undefiniert sein, wenn die REST API nicht erreichbar ist und stattdessen der DCS verwendet wird.

- Bei benutzerdefiniertem Bootstrap trust für localhost in `pg_hba.conf` freigeben (Alexander Kukushkin)

  Zuvor war dies nur für unix_socket freigegeben, was zahlreiche Fehler verursachte: `FATAL:  no pg_hba.conf entry for replication connection from host "127.0.0.1", user "replicator"`

- Synchronen Knoten auch dann als funktionsfähig einstufen, wenn der bisherige Leader weiter fortgeschritten ist (Alexander Kukushkin)

  Verliert der Primärserver den Zugriff auf den DCS, startet er Postgres im schreibgeschützten Modus neu. Andere Knoten können den alten Primärserver jedoch möglicherweise weiterhin über die REST API erreichen. In diesem Fall wurde der synchrone Standby nicht hochgestuft, weil der alte Primärserver eine weiter fortgeschrittene WAL-Position meldete.

- Fehlerbehebungen für Standby-Cluster (Alexander Kukushkin)

  Der Bootstrap eines Replikats in einem Standby-Cluster bei nicht erreichbarem standby_leader wird ermöglicht. Hinzu kommen einige kleinere Korrekturen.

--------

## Version 1.5.6 {#version-156}

Veröffentlicht am 2019-08-03

**Neue Funktionen**

- Zugriff auf einen etcd-Cluster über mehrere Proxys unterstützen (Alexander Kukushkin)

  Ein etcd-Cluster ist möglicherweise nur über mehrere Proxys und nicht direkt erreichbar. In diesem Fall ermittelt Patroni die etcd-Topologie nicht, sondern verwendet die Proxy-Hosts reihum. Das Verhalten wird über `etcd.use_proxies` gesteuert.

- Callback-Verhalten bei Rollenänderung eines Knotens ändern (Alexander Kukushkin)

  Wechselt die Rolle von `master` oder `standby_leader` zu `replica` oder von `replica` zu `standby_leader`, wird statt `on_restart` nun der Callback `on_role_change` aufgerufen.

- Startverfahren für Postgres ändern (Alexander Kukushkin)

  Statt sich selbst auszuführen, wird `multiprocessing.Process` verwendet. Die Postmaster-PID wird über `multiprocessing.Pipe` an den Patroni-Prozess übertragen. Zuvor wurden Pipes verwendet, wodurch stdin beim Postmaster-Prozess geschlossen blieb.

**Fehlerbehebungen**

- Von der REST API zurückgegebene Rolle des Standby-Leaders korrigieren (Alexander Kukushkin)

  Fälschlicherweise wurde `replica` statt `standby_leader` zurückgegeben.

- Auf das Ende eines Callbacks warten, wenn er nicht beendet werden kann (Julien Tachoires)

  Patroni hat nicht genügend Rechte, um ein unter `sudo` laufendes Callback-Skript zu beenden. Dadurch wurde der neue Callback verworfen. Kann das laufende Skript nicht beendet werden, wartet Patroni nun auf dessen Abschluss und führt anschließend den nächsten Callback aus.

- Sperrdauer der Methode dcs.get_cluster verkürzen (Alexander Kukushkin)

  Weil die Sperre gehalten wurde, beeinträchtigte ein langsamer DCS die REST-API-Health-Checks und führte zu Fehlalarmen.

- Bereinigung von PGDATA verbessern, wenn `pg_wal`/`pg_xlog` ein symbolischer Link ist (Julien Tachoires)

  In diesem Fall entfernt Patroni Dateien ausdrücklich aus dem Zielverzeichnis.

- Unnötige Verwendung von os.path.relpath entfernen (Ants Aasma)

  Die Funktion muss das Arbeitsverzeichnis auflösen können. Dies schlägt fehl, wenn Patroni in einem Verzeichnis gestartet wird, das später aus dem Dateisystem entfernt wird.

- Bei der Kommunikation mit etcd keine SSL-Version erzwingen (Alexander Kukushkin)

  Aus unbekanntem Grund basiert python3-etcd unter Debian und Ubuntu nicht auf der neuesten Paketversion und erzwingt deshalb TLSv1, das von etcd v3 nicht unterstützt wird. Dieses Problem wurde auf Patroni-Seite behoben.

--------

## Version 1.5.5 {#version-155}

Veröffentlicht am 2019-02-15

Diese Version ermöglicht die automatische Neuinitialisierung des bisherigen Primärservers, verbessert die Ausgabe von patronictl list und behebt mehrere Fehler.

**Neue Funktionen**

- Umgebungsvariablen `PATRONI_ETCD_PROTOCOL`, `PATRONI_ETCD_USERNAME` und `PATRONI_ETCD_PASSWORD` unterstützen (Étienne M)

  Zuvor konnten diese Werte nur in der Konfigurationsdatei oder als Teil von `PATRONI_ETCD_URL` festgelegt werden, was nicht immer praktisch ist.

- Automatische Neuinitialisierung des bisherigen Primärservers ermöglichen (Alexander Kukushkin)

  Ist pg_rewind deaktiviert oder nicht verwendbar, kann der bisherige Primärserver aufgrund auseinanderlaufender Timelines möglicherweise nicht als neues Replikat starten. In diesem Fall hilft nur, das Datenverzeichnis zu löschen und die Instanz neu zu initialisieren. Dieses Verhalten lässt sich mit `postgresql.remove_data_directory_on_diverged_timelines` ändern. Ist die Option gesetzt, löscht Patroni das Datenverzeichnis und initialisiert den bisherigen Primärserver automatisch neu.

- Timeline-Informationen in patronictl list anzeigen (Alexander Kukushkin)

  Dies erleichtert das Erkennen veralteter Replikate. Außerdem enthält `Host` den Zusatz ':{port}', wenn der Port vom Standardwert abweicht oder mehrere Mitglieder auf demselben Host laufen.

- Einen Headless Service für den Endpoint \$SCOPE-config erstellen (Alexander Kukushkin)

  Der Endpoint „config“ enthält die clusterweite Patroni- und Postgres-Konfiguration, die History-Datei und vor allem den Schlüssel `initialize`. Beim Neustart oder Upgrade eines Kubernetes-Masterknotens werden Endpoints ohne zugehörige Services entfernt. Der Headless Service verhindert dies.

**Fehlerbehebungen**

- Lesezeitlimit für die blockierende Leader-Watch-Abfrage anpassen (Alexander Kukushkin)

  Laut Consul-Dokumentation wird das tatsächliche Antwortzeitlimit um eine kleine zufällige Wartezeit erhöht, die zur angegebenen maximalen Wartezeit addiert wird. Dadurch werden die Aufwachzeitpunkte gleichzeitiger Anfragen verteilt. Dadurch verlängert sich die maximale Dauer um bis zu `wait / 16`. Hier wird `wait / 15` oder 1 Sekunde addiert, je nachdem, welcher Wert größer ist.

- Bei Verbindungen zu Postgres über das Replikationsprotokoll immer replication=1 verwenden (Alexander Kukushkin)

  Ab Postgres 10 akzeptiert eine Zeile mit database=replication in pg_hba.conf keine Verbindungen mit dem Parameter replication=database.

- Für einen Standby-Cluster mit ausschließlicher WAL-Nutzung kein primary_conninfo in recovery.conf schreiben (Alexander Kukushkin)

  Obwohl in der Konfiguration [standby_cluster](/de/patroni/standby_cluster#standby_cluster) weder `host` noch `port` definiert war, schrieb Patroni `primary_conninfo` in `recovery.conf`. Dies ist nutzlos und verursachte zahlreiche Fehler.

--------

## Version 1.5.4 {#version-154}

Veröffentlicht am 2019-01-15

Diese Version führt eine flexible Protokollierung ein und behebt mehrere Fehler.

**Neue Funktionen**

- Verbesserungen an der Protokollierungsinfrastruktur (Alexander Kukushkin, Lucas Capistrant, Alexander Anikin)

  Die Protokollierung lässt sich nun sowohl über Umgebungsvariablen als auch über die Patroni-Konfigurationsdatei konfigurieren. Damit kann die Konfiguration im laufenden Betrieb geändert werden: durch Aktualisieren der Datei und anschließendes Neuladen oder Senden von SIGHUP an den Patroni-Prozess. Standardmäßig schreibt Patroni Protokolle nach stderr. Nun können sie auch direkt in eine Datei geschrieben und beim Erreichen einer bestimmten Größe rotiert werden. Außerdem werden ein eigenes Datumsformat und die gezielte Einstellung der Protokollstufe für jedes Python-Modul unterstützt.

- Berücksichtigung der aktuellen Timeline bei der Leader-Wahl ermöglichen (Alexander Kukushkin)

  Ein Knoten konnte sich als den am besten geeigneten einstufen, obwohl er sich nicht auf der zuletzt bekannten Timeline befand. Um seine Hochstufung in solchen Fällen zu verhindern, kann `check_timeline` auf `true` gesetzt werden. Das Standardverhalten bleibt unverändert.

- Anforderungen an Superuser-Zugangsdaten lockern

  Libpq kann Verbindungen ohne ausdrückliche Angabe von Benutzername oder Passwort öffnen. Je nach Situation verwendet es die Datei pgpass oder die Authentifizierungsmethode trust in pg_hba.conf. Da pg_rewind ebenfalls libpq verwendet, gilt dort dasselbe Verhalten.

- Consul-Service-Registrierung und Prüfintervall über Umgebungsvariablen konfigurierbar machen (Alexander Kukushkin)

  Die Service-Registrierung in Consul wurde in 1.5.0 eingeführt, ließ sich bisher aber nur über patroni.yaml aktivieren.

**Stabilitätsverbesserungen**

- Bei benutzerdefiniertem Bootstrap archive_mode auf off setzen (Alexander Kukushkin)

  WAL- und History-Dateien sollen erst archiviert werden, wenn der Cluster vollständig funktionsfähig ist. Dies ist besonders hilfreich, wenn der benutzerdefinierte Bootstrap pg_upgrade verwendet.

- Beim Laden der globalen Konfiguration während des Starts fünf Sekunden zwischen Versuchen warten (Alexander Kukushkin)

  So wird der DCS beim Start von Patroni nicht durch ständige Anfragen belastet.

- Anzahl der Fehlermeldungen beim Herunterfahren verringern (Alexander Kukushkin)

  Sie waren harmlos, aber lästig und teilweise beunruhigend.

- Lese- und Schreibrechte für recovery.conf bereits beim Erstellen ausdrücklich absichern (Lucas Capistrant)

  Nur der Benutzer patroni/postgres soll diese Datei lesen können, da sie den Replikationsbenutzernamen und das Passwort enthält.

- Ausnahmen von HTTPServer an die Protokollierung weiterleiten (Julien Riou)

  Standardmäßig wurden diese Ausnahmen auf der Standardausgabe protokolliert und störten dadurch die regulären Protokolle.

**Fehlerbehebungen**

- Umleitung von stderr nach stdout beim pg_ctl-Prozess entfernen (Cody Coons)

  Durch das Erben von stderr vom Patroni-Hauptprozess werden alle Postgres-Protokolle zusammen mit allen Patroni-Protokollen sichtbar. Dies ist in Containern sehr nützlich, da beide mit Standardwerkzeugen wie docker logs oder kubectl erfasst werden können. Außerdem behebt die Änderung einen Fehler, bei dem Patroni die Postmaster-PID nicht ermitteln konnte, wenn Postgres Warnungen nach stderr schrieb.

- Zeitlimit zum Deregistrieren der Consul-Service-Prüfung im Go-Zeitformat angeben (Pavel Kirillov)

  Ohne ausdrückliche Zeiteinheit schlug die Registrierung fehl.

- Prüfungen der Konfiguration von standby_cluster lockern (Dmitry Dolgov, Alexander Kukushkin)

  Bisher wurden nur Zeichenketten als gültige Werte akzeptiert. Daher konnte port nicht als Ganzzahl und create_replica_methods nicht als Liste angegeben werden.

--------

## Version 1.5.3 {#version-153}

Veröffentlicht am 2018-12-03

Version mit Kompatibilitätsverbesserungen und Fehlerbehebungen.

- Stabilität bei der Verwendung von Python 3 mit Zookeeper verbessern (Alexander Kukushkin)

  Eine Änderung von `loop_wait` führte dazu, dass Patroni die Verbindung zu Zookeeper trennte und nicht erneut herstellte.

- Kompatibilität mit Postgres 9.3 wiederherstellen (Alexander Kukushkin)

  Beim Öffnen einer Replikationsverbindung sollte replication=1 angegeben werden, da 9.3 replication='database' nicht versteht.

- Consul-Session mindestens einmal pro HA-Schleifendurchlauf erneuern und Behandlung von Session-Ausnahmen verbessern (Alexander Kukushkin)

  Ein Neustart des lokalen Consul-Agenten macht alle dem Knoten zugeordneten Sessions ungültig. Eine verspätete Erneuerung und unzureichende Behandlung von Session-Fehlern führten zur Herabstufung des Primärservers.

--------

## Version 1.5.2 {#version-152}

Veröffentlicht am 2018-11-26

Version mit Kompatibilitätsverbesserungen und Fehlerbehebungen.

- Kompatibilität mit kazoo-2.6.0 (Alexander Kukushkin)

  Um angemessene Zeitlimits für Anfragen sicherzustellen, definiert Patroni die Methode create_connection des Moduls python-kazoo neu. Die neueste Kazoo-Version änderte den Aufruf von create_connection geringfügig.

- Absturz von Patroni beim Verlust des Leaders im Consul-Cluster beheben (Alexander Kukushkin)

  Ursache war eine fehlerhafte Implementierung der Methode touch_member: Sie sollte einen booleschen Wert zurückgeben und keine Ausnahmen auslösen.

--------

## Version 1.5.1 {#version-151}

Veröffentlicht am 2018-11-01

Diese Version unterstützt permanente Replikationsslots sowie pgBackRest und behebt mehrere Fehler.

**Neue Funktionen**

- Permanente Replikationsslots (Alexander Kukushkin)

  Permanente Replikationsslots bleiben bei Failover und Switchover erhalten. Patroni erstellt die konfigurierten Slots auf dem neuen Primärserver unmittelbar nach der Hochstufung. Die Slots lassen sich mit `patronictl edit-config` konfigurieren. Die anfängliche Konfiguration kann auch unter [bootstrap.dcs](/de/patroni/config/yaml#yaml) erfolgen.

- pgBackRest-Unterstützung hinzufügen (Yogesh Sharma)

  pgBackRest kann in ein bestehendes Verzeichnis \$PGDATA wiederherstellen. Dabei werden seit dem letzten Backup unveränderte Dateien übersprungen, was die Wiederherstellung beschleunigt. Zur Unterstützung dieser Funktion wurde der Parameter `keep_data` eingeführt. Weitere Beispiele enthält der Abschnitt [Methode zur Replikaterstellung](/de/patroni/replica_bootstrap#custom_replica_creation).

**Fehlerbehebungen**

- Fehlerbehebungen im Ablauf für Standby-Cluster (Alexander Kukushkin)

  Weitere Einzelheiten finden sich unter <https://github.com/patroni/patroni/pull/823>.

- REST-API-Health-Check bei pausierter Cluster-Verwaltung und nicht erreichbarem DCS korrigieren (Alexander Kukushkin)

  Diese Regression wurde mit <https://github.com/patroni/patroni/commit/90cf930036a9d5249265af15d2b787ec7517cf57> eingeführt.

--------

## Version 1.5.0 {#version-150}

Veröffentlicht am 2018-09-20

Diese Version ermöglicht den Betrieb eines Patroni-HA-Clusters im Standby-Modus, führt experimentelle Windows-Unterstützung ein und bietet einen neuen Konfigurationsparameter zur Registrierung des PostgreSQL-Dienstes in Consul.

**Neue Funktionen**

- Standby-Cluster (Dmitry Dolgov)

  Ein oder mehrere Patroni-Knoten können einen Standby-Cluster bilden, der neben dem Primärcluster läuft, etwa in einem anderen Rechenzentrum. Er besteht aus Standbys, die vom Primärserver des Primärclusters replizieren. Alle PostgreSQL-Knoten im Standby-Cluster sind Replikate. Eines davon wählt sich selbst für die direkte Replikation vom entfernten Primärserver aus; die anderen replizieren kaskadierend von diesem Replikat. Eine ausführlichere Beschreibung und Konfigurationsbeispiele finden sich [hier](/de/patroni/standby_cluster#standby_cluster).

- Dienste in Consul registrieren (Pavel Kirillov, Alexander Kukushkin)

  Ist `register_service` in der Consul-[Konfiguration](/de/patroni/config/yaml#consul_settings) aktiviert, registriert der Knoten einen Dienst mit dem Namen `scope` und dem Tag `master`, `replica` oder `standby-leader`.

- Experimentelle Windows-Unterstützung (Pavel Golub)

  Patroni kann nun unter Windows ausgeführt werden. Diese Unterstützung ist jedoch neu und wurde noch nicht so ausgiebig in der Praxis getestet wie die Linux-Variante. Rückmeldungen sind willkommen!

**Verbesserungen in patronictl**

- Flag patronictl -k/--insecure und Unterstützung für restapi-Zertifikate hinzufügen (Wilfried Roset)

  War die REST API durch selbstsignierte Zertifikate geschützt, schlug deren Prüfung durch [patronictl](/de/patroni/patronictl#patronictl) bisher fehl. Es gab keine Möglichkeit, die Prüfung zu deaktivieren. Nun kann [patronictl](/de/patroni/patronictl#patronictl) so konfiguriert werden, dass es die Zertifikatsprüfung vollständig überspringt. Alternativ können CA- und Client-Zertifikate im Konfigurationsabschnitt [ctl:](/de/patroni/config/yaml#patronictl_settings) angegeben werden.

- Mitglieder mit nofailover-Tag aus der Ausgabe von patronictl switchover/failover ausschließen (Alexander Anikin)

  Zuvor wurden diese Mitglieder bei interaktivem Switchover oder Failover über patronictl fälschlicherweise als Kandidaten vorgeschlagen.

**Stabilitätsverbesserungen**

- Ausgabezeilen von pg_controldata ohne Schlüssel-Wert-Paar nicht auswerten (Alexander Anikin)

  Unter bestimmten Umständen gibt pg_controldata Zeilen ohne Doppelpunkt aus. Dadurch entstand beim Auswerten der pg_controldata-Ausgabe ein Fehler im Patroni-Code, der das eigentliche Problem verdeckte. Solche Zeilen stammen häufig aus einer Warnung, die pg_controldata vor der regulären Ausgabe anzeigt, etwa wenn die Hauptversion der ausführbaren Datei nicht mit der des PostgreSQL-Datenverzeichnisses übereinstimmt.

- Mitgliedsnamen in Fehlermeldungen während der Leader-Wahl aufnehmen (Jan Mussler)

  Während der Leader-Wahl verbindet sich Patroni mit allen bekannten Cluster-Mitgliedern und fragt ihren Status ab. Dieser wird einschließlich des Mitgliedsnamens im Patroni-Protokoll festgehalten. War ein Mitglied nicht erreichbar, enthielt die Fehlermeldung bisher nur die URL, jedoch nicht seinen Namen.

- WAL-Position unmittelbar beim Erstellen des Replikationsslots reservieren (Alexander Kukushkin)

  Seit 9.6 bietet die Funktion `pg_create_physical_replication_slot` den zusätzlichen booleschen Parameter `immediately_reserve`. Bei `false`, dem Standardwert, reserviert der Slot die WAL-Position erst mit der ersten Client-Verbindung. Zwischen seiner Erstellung und der ersten Verbindung können deshalb vom Client benötigte Segmente verloren gehen.

- Fehler bei strikt synchroner Replikation beheben (Alexander Kukushkin)

  Bei `synchronous_mode_strict: true` trägt Patroni in manchen Fällen `*` in `synchronous_standby_names` ein. Dadurch wechselt der Synchronisationszustand der meisten Replikationsverbindungen zu `potential`. Bisher konnte Patroni dann keinen synchronen Kandidaten auswählen, da es nur Verbindungen im Zustand `async` berücksichtigte.

--------

## Version 1.4.6 {#version-146}

Veröffentlicht am 2018-08-14

**Fehlerbehebungen und Stabilitätsverbesserungen**

Diese Version behebt einen kritischen Fehler, bei dem der Patroni-API-Endpunkt /master für einen Knoten, der kein Primärserver war, 200 zurückgab. Es handelte sich um einen Meldefehler und nicht um einen tatsächlichen Split Brain. Unter bestimmten Umständen konnten Clients jedoch an einen schreibgeschützten Knoten weitergeleitet werden.

- Status is_leader beim Herabstufen zurücksetzen (Alexander Kukushkin, Oleksii Kliukin)

  Sicherstellen, dass ein herabgestuftes Cluster-Mitglied bei einem Aufruf der API /master nicht mehr mit Code 200 antwortet.

- Neues Feld „cluster_unlocked“ zur API-Ausgabe hinzufügen (Dmitry Dolgov)

  Das Feld zeigt an, ob im Cluster ein Primärserver läuft. Es kann verwendet werden, wenn sich außer einem einzelnen Replikat kein anderer Knoten abfragen lässt.

--------

## Version 1.4.5 {#version-145}

Veröffentlicht am 2018-08-03

**Neue Funktionen**

- Protokollierung beim Anwenden einer neuen Postgres-Konfiguration verbessern (Don Seiler)

  Patroni protokolliert die Namen und Werte geänderter Parameter.

- Kompatibilität mit Python 3.7 (Christoph Berg)

  async ist in python3.7 ein reserviertes Schlüsselwort.

- Beim Herunterfahren eines Mitglieds dessen Zustand im DCS auf "stopped" setzen (Tony Sorrentino)

  Dadurch zeigt der Befehl "patronictl list" den Zustand des Mitglieds als "stopped" an.

- Protokollmeldung verbessern, wenn eine veraltete postmaster.pid zu einem laufenden Prozess passt (Ants Aasma)

  Die bisherige Meldung war äußerst verwirrend.

- Funktion patronictl reload implementieren (Don Seiler)

  Zuvor ließ sich die Konfiguration nur durch einen REST-API-Aufruf oder durch Senden von SIGHUP an den Patroni-Prozess neu laden.

- Beim Start als Replikat einige Parameter aus controldata übernehmen und anwenden (Alexander Kukushkin)

  Der Wert von `max_connections` und einigen weiteren Parametern in der globalen Konfiguration kann niedriger sein als der tatsächlich vom Primärserver verwendete Wert. Dann kann das Replikat nicht starten und sollte manuell korrigiert werden. Patroni übernimmt dies nun: Es liest den Wert aus `pg_controldata`, wendet ihn an, startet Postgres und setzt das Flag `pending_restart`.

- Beim Start von Postgres LD_LIBRARY_PATH verwenden, sofern gesetzt (Chris Fraser)

  Beim Start von Postgres reichte Patroni die Umgebungsvariablen PATH, LC_ALL und LANG weiter, sofern sie gesetzt waren. Nun geschieht dies auch mit LD_LIBRARY_PATH. Dies sollte helfen, wenn PostgreSQL an einem nicht standardmäßigen Ort installiert wurde.

- create_replica_method in create_replica_methods umbenennen (Dmitry Dolgov)

  Der neue Name verdeutlicht, dass es sich um ein Array handelt. Der alte Name bleibt aus Gründen der Abwärtskompatibilität unterstützt.

**Fehlerbehebungen und Stabilitätsverbesserungen**

- Bedingung für den Start eines Replikats nach pg_rewind im Pausenmodus korrigieren (Oleksii Kliukin)

  Ein Replikat, das pg_rewind bereits ausgeführt hat, wird nicht erneut gestartet.

- Beim Health Check des Primärservers nur dann 200 zurückgeben, wenn update_lock erfolgreich war (Alexander Kukushkin)

  So wird verhindert, dass sich der bisherige, herabgestufte Primärserver bei einer Netzwerkpartition des DCS weiterhin als Primärserver meldet.

- Kompatibilität mit dem neuen Consul-Modul korrigieren (Alexander Kukushkin)

  Seit v1.1.0 verwendet python-consul eine geänderte interne API und übergibt Abfrageparameter als `list` statt als `dict`.

- Ausnahmen aus dem REST-API-Thread von Patroni beim Herunterfahren abfangen (Alexander Kukushkin)

  Aufgrund dieser nicht abgefangenen Ausnahmen lief PostgreSQL beim Herunterfahren weiter.

- Crash-Recovery nur ausführen, wenn Postgres als Primärserver läuft (Alexander Kukushkin)

  `pg_controldata` muss 'in production', 'shutting down' oder 'in crash recovery' melden. In allen anderen Fällen ist keine Crash-Recovery erforderlich.

- Behandlung von Konfigurationsfehlern verbessern (Henning Jacobs, Alexander Kukushkin)

  Viele Parameter, einschließlich `restapi.listen`, lassen sich im laufenden Betrieb ändern, indem die Patroni-Konfigurationsdatei aktualisiert und SIGHUP an den Patroni-Prozess gesendet wird. Diese Korrektur beseitigt schwer verständliche Ausnahmen aus dem Thread 'restapi', wenn Parameter ungültige Werte erhalten.

--------

## Version 1.4.4 {#version-144}

Veröffentlicht am 2018-05-22

**Verbesserungen der Stabilität**

- Race Condition in poll_failover_result beheben (Alexander Kukushkin)

  Sie wirkte sich weder auf Failover noch auf Switchover direkt aus. In seltenen Fällen wurde der Erfolg jedoch zu früh gemeldet, sobald der frühere Leader den Lock freigab. Dadurch entstand die Meldung 'Failed over to "None"' statt 'Failed over to "desired-node"'.

- Groß- und Kleinschreibung bei Postgres-Parameternamen ignorieren (Alexander Kukushkin)

  Die meisten Postgres-Parameter haben Namen in snake_case. Es gibt jedoch drei Ausnahmen: DateStyle, IntervalStyle und TimeZone. Postgres akzeptiert diese Parameter auch mit anderer Groß- und Kleinschreibung (etwa timezone = 'some/tzn'). Patroni konnte solche abweichend geschriebenen Parameternamen dagegen nicht in pg_settings finden und ignorierte sie deshalb.

- Start beim Anhängen an laufendes postgres abbrechen, wenn der Cluster nicht initialisiert ist (Alexander Kukushkin)

  Patroni kann sich an eine bereits laufende Postgres-Instanz anhängen. Dabei muss Patroni unbedingt zuerst auf dem Primärserver gestartet werden, bevor die Replikate an der Reihe sind.

- Verhalten von patronictl scaffold korrigieren (Alexander Kukushkin)

  An `touch_member` wird ein dict-Objekt statt einer JSON-kodierten Zeichenkette übergeben; die DCS-Implementierung übernimmt die Kodierung.

- Primärserver bei fehlgeschlagener Aktualisierung des Leader-Schlüssels während einer Pause nicht herabstufen (Alexander Kukushkin)

  Während Wartungsarbeiten kann ein DCS Schreibanfragen ablehnen, während er Leseanfragen weiterhin beantwortet. In diesem Fall versetzte Patroni den Postgres-Primärserver zuvor in einen schreibgeschützten Modus, nachdem die Aktualisierung des Leader-Locks im DCS fehlgeschlagen war.

- Replikations-Slots synchronisieren, wenn Patroni einen neuen postmaster-Prozess erkennt (Alexander Kukushkin)

  Nach einem Postgres-Neustart muss Patroni sicherstellen, dass die Liste der Replikations-Slots seinen Erwartungen entspricht.

- Nach Beendigung einer Pause sysid prüfen und Replikations-Slots synchronisieren (Alexander Kukushkin)

  Im Modus `maintenance` kann das Datenverzeichnis vollständig neu geschrieben worden sein. Daher muss geprüft werden, ob `Database system identifier` weiterhin zum Cluster gehört und die Replikations-Slots dem von Patroni erwarteten Zustand entsprechen.

- Mögliches Startproblem bei gestopptem Postgres mit vorhandener postmaster-Lock-Datei im Datenverzeichnis beheben (Alexander Kukushkin)

  Die Wiederverwendung der PID aus der postmaster-Lock-Datei wird erkannt. Dieses Problem tritt eher auf, wenn Patroni und Postgres in einem Docker-Container laufen.

- Schutz vor versehentlichem Löschen der DCS-Inhalte verbessern (Alexander Kukushkin)

  Patroni enthält umfangreiche Logik, um in diesem Fall ein Failover zu verhindern, und kann außerdem alle Schlüssel wiederherstellen. Bis zu dieser Änderung schaltete das versehentliche Löschen des Schlüssels /config jedoch den Pause-Modus für 1 Durchlauf der HA-Schleife aus.

- Bei ungültiger System-ID nicht beenden (Oleksii Kliukin)

  Patroni wird nicht beendet, wenn die System-ID des Clusters leer ist oder die Validierung nicht besteht. In diesem Fall muss der Cluster höchstwahrscheinlich neu initialisiert werden; darauf wird in der Ergebnismeldung hingewiesen. Patroni wird nicht beendet, da andernfalls keine Neuinitialisierung möglich wäre.

**Kompatibilität mit Kubernetes 1.10+**

- Prüfung auf leere subsets hinzufügen (Cody Coons)

  Seit Kubernetes 1.10.0+ wird `Endpoints.subsets` als `None` statt als `[]` zurückgegeben.

**Verbesserungen beim Bootstrap**

- Löschen von recovery.conf optional machen (Brad Nicholson)

  Wenn `bootstrap.<custom_bootstrap_method_name>.keep_existing_recovery_conf` definiert und auf `True` gesetzt ist, entfernt Patroni die vorhandene Datei `recovery.conf` nicht. Dies ist beim Bootstrap aus einem Backup mit Werkzeugen wie pgBackRest nützlich, die eine passende `recovery.conf` erzeugen.

- Optionen für die integrierte basebackup-Methode zulassen (Oleksii Kliukin)

  Der integrierten basebackup-Methode können jetzt Optionen übergeben werden, indem der Abschnitt `basebackup` in der Konfiguration definiert wird, ähnlich wie bei benutzerdefinierten Methoden zur Replikaterstellung. Der Unterschied liegt im akzeptierten Format des Abschnitts `basebackup`: Da pg_basebackup sowohl Optionen mit `--key=value` als auch mit `--key` akzeptiert, kann der Abschnitt entweder ein Dictionary mit Schlüssel-Wert-Paaren oder eine Liste aus Dictionaries mit jeweils einem Eintrag beziehungsweise aus einzelnen Schlüsseln für Optionen ohne Wert enthalten. Weitere Beispiele enthält der Abschnitt [Methode zur Replikaterstellung](/de/patroni/replica_bootstrap#custom_replica_creation).

--------

## Version 1.4.3 {#version-143}

Veröffentlicht am 2018-03-05

**Verbesserungen der Protokollierung**

- Protokollstufe über Umgebungsvariablen konfigurierbar machen (Andy Newton, Keyvan Hedayati)

  `PATRONI_LOGLEVEL` legt die allgemeine Protokollstufe fest. `PATRONI_REQUESTS_LOGLEVEL` legt die Protokollstufe für alle HTTP-Anfragen fest, etwa Aufrufe der Kubernetes-API. Die Namen der möglichen Protokollstufen stehen in [Dokumentation zur Python-Protokollierung](https://docs.python.org/3.6/library/logging.html#levels).

**Verbesserungen der Stabilität und Fehlerbehebungen**

- etcd-Clustertopologie nach einer Watch-Zeitüberschreitung nicht erneut ermitteln (Alexander Kukushkin)

  War nur ein Host in der etcd-Konfiguration angegeben und genau dieser nicht erreichbar, begann Patroni mit der Ermittlung der Clustertopologie, ohne jemals erfolgreich zu sein. Stattdessen sollte es lediglich zum nächsten verfügbaren Knoten wechseln.

- Inhalt von bootstrap.pg_hba nach einem benutzerdefinierten Bootstrap in eine pg_hba.conf schreiben (Alexander Kukushkin)

  Das Verhalten entspricht jetzt dem üblichen Bootstrap mit `initdb`.

- Einzelbenutzermodus wartete auf Benutzereingaben und wurde nie beendet (Alexander Kukushkin)

  Die Regression wurde in <https://github.com/patroni/patroni/pull/576> eingeführt.

--------

## Version 1.4.2 {#version-142}

Veröffentlicht am 2018-01-30

**Verbesserungen in patronictl**

- Geplantes Failover in geplantes Switchover umbenennen (Alexander Kukushkin)

  Failover und Switchover wurden in Version 1.4 getrennt. `patronictl list` meldete jedoch weiterhin `Scheduled failover` statt `Scheduled switchover`.

- Informationen zu ausstehenden Neustarts anzeigen (Alexander Kukushkin)

  Manche Konfigurationsänderungen erfordern einen Postgres-Neustart. Patroni gab darauf bereits in der REST API und beim Schreiben des Knotenstatus in den DCS einen Hinweis, dieser ließ sich jedoch nicht einfach anzeigen.

- show-config mit cluster_name aus der Konfigurationsdatei nutzbar machen (Alexander Kukushkin)

  Dies funktioniert ähnlich wie bei `patronictl edit-config`.

**Verbesserungen der Stabilität**

- Aufruf von pg_controldata während des Bootstraps vermeiden (Alexander Kukushkin)

  Während initdb oder eines benutzerdefinierten Bootstraps gibt es ein Zeitfenster, in dem pgdata nicht leer ist, pg_control aber noch nicht geschrieben wurde. Ein Aufruf von pg_controldata schlug dann mit Fehlermeldungen fehl.

- Von psutil ausgelöste Ausnahmen behandeln (Alexander Kukushkin)

  cmdline wird bei jedem Aufruf der Methode `cmdline()` gelesen und ausgewertet. Wenn der untersuchte Prozess inzwischen beendet wurde, wird `NoSuchProcess` ausgelöst.

**Verbesserungen der Kubernetes-Unterstützung**

- Fehler der k8s-API nicht unterdrücken (Alexander Kukushkin)

  Ein Aufruf der Kubernetes-API kann aus verschiedenen Gründen fehlschlagen. In manchen Fällen sollte der Aufruf wiederholt werden, in anderen sollten die Fehlermeldung und der Stacktrace der Ausnahme protokolliert werden. Diese Änderung hilft bei der Diagnose von Kubernetes-Berechtigungsproblemen.

- Kubernetes-Beispiel-Dockerfile auf Installation von Patroni aus dem master-Branch umstellen (Maciej Szulik)

  Zuvor wurde der inzwischen veraltete Branch `feature/k8s` verwendet.

- Passende RBAC-Konfiguration für Patroni auf k8s hinzufügen (Maciej Szulik)

  Ein Service Account für die Pods des Clusters, eine Rolle mit ausschließlich den notwendigen Berechtigungen und ein RoleBinding zur Verknüpfung von Service Account und Rolle wurden hinzugefügt.

--------

## Version 1.4.1 {#version-141}

Veröffentlicht am 2018-01-17

**Korrekturen in patronictl**

- Aktuellen Leader nicht in der vorgeschlagenen Liste der Failover-Ziele anzeigen. (Alexander Kukushkin)

  patronictl failover kann auch dann funktionieren, wenn der Cluster einen Leader hat. Dieser sollte aus der Liste der möglichen Failover-Ziele ausgeschlossen werden.

- patronictl switchover mit der alten Patroni-API kompatibel machen (Alexander Kukushkin)

  Schlägt der REST-API-Aufruf POST /switchover mit Statuscode 501 fehl, wird er erneut ausgeführt, diesmal jedoch am Endpunkt /failover.

--------

## Version 1.4 {#version-14}

Veröffentlicht am 2018-01-10

Diese Version unterstützt Kubernetes als DCS. Damit kann Patroni als Cloud-nativer Agent in Kubernetes ohne zusätzliche Bereitstellung von etcd, Zookeeper oder Consul laufen.

**Upgrade-Hinweis**

Bei der Installation von Patroni über pip werden Abhängigkeiten wie Bibliotheken für etcd, Zookeeper, Consul oder Kubernetes sowie Unterstützung für AWS nicht mehr automatisch installiert. Um sie zu aktivieren, müssen sie im Befehl pip install ausdrücklich aufgeführt werden, beispielsweise mit `pip install 'patroni[etcd,kubernetes]'`.

**Kubernetes-Unterstützung**

Ein Kubernetes-basierter DCS wurde implementiert. Die Metadaten der Endpoints speichern die Konfiguration und den Leader-Schlüssel. Das Metadatenfeld in den Pod-Definitionen speichert die mitgliederbezogenen Daten. Neben Endpoints unterstützt Patroni auch ConfigMaps. Weitere Informationen zu dieser Funktion finden sich im [Kubernetes-Kapitel der Dokumentation](/de/patroni/kubernetes#kubernetes).

**Verbesserungen der Stabilität**

- postmaster-Prozess in ein eigenes Objekt auslagern (Ants Aasma)

  Dieses Objekt identifiziert einen laufenden postmaster-Prozess anhand von PID und Startzeit. Es vereinfacht das Erkennen und Beheben von Situationen, in denen der postmaster ohne Wissen von Patroni neu gestartet wurde oder das Postgres-Verzeichnis aus dem Dateisystem verschwunden ist.

- Anzahl der von Patroni pro HA-Schleifendurchlauf ausgeführten SELECTs minimieren (Alexander Kukushkin)

  Bei jedem HA-Schleifendurchlauf benötigt Patroni den Recovery-Status und die absolute WAL-Position. Dazu führt Patroni jetzt nur ein SELECT aus, statt zwei auf dem Replikat und drei auf dem Primärserver.

- Leader-Schlüssel beim Herunterfahren nur entfernen, wenn der Lock gehalten wird (Ants Aasma)

  Das bedingungslose Entfernen erzeugte unnötige und irreführende Ausnahmen.

**Verbesserungen in patronictl**

- Befehl version zu patronictl hinzufügen (Ants Aasma)

  Er zeigt die installierte Patroni-Version an. Wird der Clustername angegeben, zeigt er außerdem die Versionen laufender Patroni-Instanzen.

- Angabe des Arguments cluster_name für einige patronictl-Befehle optional machen (Alexander Kukushkin, Ants Aasma)

  Dies funktioniert, wenn patronictl eine gewöhnliche Patroni-Konfigurationsdatei mit definiertem `scope` verwendet.

- Informationen zu geplantem Switchover und Wartungsmodus anzeigen (Alexander Kukushkin)

  Zuvor waren diese Informationen nur über Patroni-Protokolle oder direkt aus dem DCS verfügbar.

- `patronictl reinit` verbessern (Alexander Kukushkin)

  `patronictl reinit` weigerte sich manchmal fortzufahren, wenn Patroni mit anderen Aktionen beschäftigt war, insbesondere mit dem Versuch, postgres zu starten. [patronictl](/de/patroni/patronictl#patronictl) bot keine Befehle zum Abbrechen solcher lang laufenden Aktionen. Die einzige, gefährliche Umgehung bestand im manuellen Löschen eines Datenverzeichnisses. Die neue Implementierung von `reinit` bricht andere lang laufende Aktionen zwangsweise ab, bevor sie mit der Neuinitialisierung fortfährt.

- Option `--wait` in `patronictl pause` und `patronictl resume` implementieren (Alexander Kukushkin)

  Damit wartet [patronictl](/de/patroni/patronictl#patronictl), bis alle Knoten im Cluster die angeforderte Aktion bestätigt haben. Dazu wird der Schalter [pause](/de/patroni/pause#pause) für jeden Knoten im DCS und über die REST API bereitgestellt.

- `patronictl failover` in `patronictl switchover` umbenennen (Alexander Kukushkin)

  Das bisherige `failover` konnte tatsächlich nur ein Switchover durchführen und verweigerte die Ausführung in einem Cluster ohne Leader.

- Verhalten von `patronictl failover` ändern (Alexander Kukushkin)

  Der Befehl funktioniert auch ohne Leader. In diesem Fall muss jedoch ausdrücklich angegeben werden, welcher Knoten neuer Leader werden soll.

**Informationen zu Timeline und Historie bereitstellen**

- Aktuelle Timeline im DCS und über die API bereitstellen (Alexander Kukushkin)

  Für jedes Clustermitglied werden Informationen zur aktuellen Timeline gespeichert. Diese Informationen sind über die API zugänglich und werden im DCS gespeichert.

- Historie der Hochstufungen im DCS-Schlüssel /history speichern (Alexander Kukushkin)

  Zusätzlich wird die um den Zeitpunkt der jeweiligen Hochstufung ergänzte Timeline-Historie im DCS-Schlüssel /history gespeichert und bei jeder Hochstufung aktualisiert.

**Endpunkte zur Abfrage synchroner und asynchroner Replikate hinzufügen**

- Neue Endpunkte /sync und /async hinzufügen (Alexander Kukushkin, Oleksii Kliukin)

> Diese Endpunkte, auch als /synchronous und /asynchronous verfügbar, geben 200 ausschließlich für synchrone beziehungsweise asynchrone Replikate zurück. Mit `noloadbalance` markierte Replikate sind ausgeschlossen.

**Mehrere Hosts für etcd zulassen**

- Neuen Parameter `hosts` zur etcd-Konfiguration hinzufügen (Alexander Kukushkin)

  Dieser Parameter sollte die anfängliche Hostliste enthalten, anhand derer die laufenden Mitglieder des etcd-Clusters ermittelt und in eine Liste aufgenommen werden. Wird diese Liste ermittelter Hosts während des Betriebs aus irgendeinem Grund ausgeschöpft, sodass kein Host daraus mehr verfügbar ist, greift Patroni wieder auf die anfängliche Liste im Parameter `hosts` zurück.

--------

## Version 1.3.6 {#version-136}

Veröffentlicht am 2017-11-10

**Verbesserungen der Stabilität**

- Beim Prüfen, ob postgres läuft, die Startzeit des Prozesses verifizieren. (Ants Aasma)

  Nach einem Absturz, der postmaster.pid nicht entfernt, kann ein neuer Prozess dieselbe PID erhalten. Dadurch liefert is_running() fälschlich ein positives Ergebnis, was zu verschiedenen Fehlverhalten führt.

- PostgreSQL vor dem Bootstrap herunterfahren, wenn das Datenverzeichnis verloren gegangen ist (ainlolcat)

  Wird das Datenverzeichnis auf dem Primärserver zwangsweise entfernt, kann der Postgres-Prozess noch eine Zeit lang weiterlaufen. Dadurch kann er das anstelle des früheren Primärservers erstellte Replikat am Starten oder Replizieren hindern. Mit dieser Korrektur speichert Patroni die PID und Startzeit des postmaster zwischen und kann den alten postmaster beenden, wenn dieser nach dem Entfernen seines Datenverzeichnisses noch läuft.

- Nach dem Ausfall des Postgres-Primärservers Crash-Recovery im Einzelbenutzermodus durchführen (Alexander Kukushkin)

  Wurde postgres nicht sauber heruntergefahren, ist ein sofortiger Start als Standby unsicher und `pg_rewind` kann nicht ausgeführt werden. Die Crash-Recovery im Einzelbenutzermodus wird nur durchgeführt, wenn `pg_rewind` aktiviert ist oder derzeit kein Primärserver vorhanden ist.

**Verbesserungen für Consul**

- Angabe einer Rechenzentrumskonfiguration für Consul ermöglichen (Vilius Okockis, Alexander Kukushkin)

  Zuvor kommunizierte Patroni immer mit dem Rechenzentrum des Hosts, auf dem es lief.

- Token immer im HTTP-Header X-Consul-Token senden (Alexander Kukushkin)

  Wenn `consul.token` in der Patroni-Konfiguration definiert ist, wird es immer im HTTP-Header 'X-Consul-Token' gesendet. Das Modul python-consul versucht, mit der Consul-REST-API übereinzustimmen. Diese akzeptiert bei der [Session-API](https://www.consul.io/api/session.html) kein Token als Abfrageparameter, der Header 'X-Consul-Token' funktioniert jedoch weiterhin.

- Session-TTL anpassen, wenn der angegebene Wert unter dem kleinstmöglichen liegt (Stas Fomin, Alexander Kukushkin)

  Die in der Patroni-Konfiguration angegebene TTL kann unter dem von Consul unterstützten Mindestwert liegen. Dann kann der Consul-Agent keine neue Session erstellen. Ohne Session kann Patroni keine Member- und Leader-Schlüssel im Consul-KV-Speicher erstellen, wodurch der Cluster nicht ordnungsgemäß funktioniert.

**Weitere Verbesserungen**

- Benutzerdefiniertes Protokollformat über die Umgebungsvariable `PATRONI_LOGFORMAT` definieren (Stas Fomin)

  Zeitstempel und ähnliche Felder in Patroni-Protokollen können deaktiviert werden, wenn sie bereits durch die Systemprotokollierung hinzugefügt werden, üblicherweise bei der Ausführung von Patroni als Dienst.

--------

## Version 1.3.5 {#version-135}

Veröffentlicht am 2017-10-12

**Fehlerbehebung**

- Rolle auf 'uninitialized' setzen, wenn das Datenverzeichnis entfernt wurde (Alexander Kukushkin)

  Lief der Knoten als Primärserver, verhinderte dies ein Failover.

**Verbesserung der Stabilität**

- Nach einem erfolglosen Versuch, postgres zu starten, versuchen, postmaster im Einzelbenutzermodus auszuführen (Alexander Kukushkin)

  Dieses Problem tritt üblicherweise auf, wenn ein als Primärserver laufender Knoten beendet wurde und die Timelines auseinanderliefen. Ist in `recovery.conf` ein `restore_command` definiert, bricht postgres den Start mit hoher Wahrscheinlichkeit ab und lässt controldata unverändert. Dadurch kann `pg_rewind`, das ein sauberes Herunterfahren voraussetzt, nicht verwendet werden.

**Verbesserungen für Consul**

- Angabe von Health Checks beim Erstellen einer Session ermöglichen (Alexander Kukushkin)

  Ohne Angabe verwendet Consul „serfHealth“. Einerseits ermöglicht dies das schnelle Erkennen eines isolierten Primärservers; andererseits kann Patroni dadurch kurze Netzwerkverzögerungen nicht tolerieren.

**Fehlerbehebung**

- Watchdog unter Python 3 korrigieren (Ants Aasma)

  Die Schnittstelle des Aufrufs ioctl() wurde falsch verstanden. Bei mutable=False gibt fcntl.ioctl() tatsächlich den arg-Puffer zurück. Unter Python2 funktionierte dies zufällig, weil ein Vergleich von int und str keinen Fehler auslöste. Fehler werden tatsächlich durch Auslösen von IOError unter Python2 und OSError unter Python3 gemeldet.

--------

## Version 1.3.4 {#version-134}

Veröffentlicht am 2017-09-08

**Verschiedene Verbesserungen für Consul**

- Consul-Token als Header übergeben (Andrew Colin Kissa)

  Header sind jetzt der bevorzugte Weg, um das Token an die Consul-[API](https://www.consul.io/api/index.html#authentication) zu übergeben.

- Erweiterte Konfiguration für Consul (Alexander Kukushkin)

  `scheme`, `token` sowie Client- und CA-Zertifikate können angegeben werden; siehe [Details](/de/patroni/config/yaml#consul_settings).

- Kompatibilität mit python-consul-0.7.1 und neuer (Alexander Kukushkin)

  Das neue Modul python-consul hat die Signatur einiger Methoden geändert.

- Die Meldung "Could not take out TTL lock" wurde nie protokolliert (Alexander Kukushkin)

  Dies ist kein kritischer Fehler, aber fehlende geeignete Protokollierung erschwert die Untersuchung von Problemen.

**synchronous_standby_names mit quote_ident in Anführungszeichen setzen**

- Beim Schreiben von `synchronous_standby_names` in `postgresql.conf` muss der Wert in Anführungszeichen gesetzt werden (Alexander Kukushkin)

  Geschieht dies nicht korrekt, deaktiviert PostgreSQL effektiv die synchrone Replikation und arbeitet weiter.

**Verschiedene Fehlerbehebungen im Pause-Zustand, überwiegend im Zusammenhang mit dem Watchdog** (Alexander Kukushkin)

- Keine Keepalives senden, wenn der Watchdog nicht aktiv ist
- Aktivierung des Watchdogs im Pause-Modus vermeiden
- Korrekten Postgres-Zustand im Pause-Modus setzen
- Keine Abfragen über die API ausführen, wenn postgres gestoppt ist

--------

## Version 1.3.3 {#version-133}

Veröffentlicht am 2017-08-04

**Fehlerbehebungen**

- Die synchrone Replikation wurde kurz nach der Hochstufung deaktiviert, auch wenn synchronous_mode_strict eingeschaltet war (Alexander Kukushkin)
- Leere Datei `pg_ident.conf` erstellen, wenn sie nach der Wiederherstellung aus dem Backup fehlt (Alexander Kukushkin)
- Zugriff in `pg_hba.conf` auf alle Datenbanken öffnen, nicht nur auf postgres (Franco Bellagamba)

--------

## Version 1.3.2 {#version-132}

Veröffentlicht am 2017-07-31

**Fehlerbehebung**

- patronictl edit-config funktionierte mit ZooKeeper nicht (Alexander Kukushkin)

--------

## Version 1.3.1 {#version-131}

Veröffentlicht am 2017-07-28

**Fehlerbehebung**

- Failover über die API war aufgrund einer Änderung in `_MemberStatus` defekt (Alexander Kukushkin)

--------

## Version 1.3 {#version-13}

Veröffentlicht am 2017-07-27

Version 1.3 ermöglicht benutzerdefinierten Bootstrap, verbessert die Unterstützung für pg_rewind erheblich, erweitert den synchronen Modus, ergänzt patronictl um die Bearbeitung der Konfiguration und implementiert Watchdog-Unterstützung unter Linux. Außerdem ist dies die erste Version, die mit PostgreSQL 10 korrekt funktioniert.

**Upgrade-Hinweis**

Es sind keine Kompatibilitätsprobleme mit der neuen Patroni-Version bekannt. Die Konfiguration aus Version 1.2 sollte unverändert funktionieren. Für das Upgrade können neue Pakete installiert und Patroni anschließend neu gestartet werden, was einen PostgreSQL-Neustart verursacht. Alternativ kann Patroni zunächst in den [Pause-Modus](/de/patroni/pause#pause) versetzt, dann auf allen Knoten des Clusters neu gestartet und der Pause-Modus zum Schluss beendet werden. Patroni versucht im Pause-Modus nicht, PostgreSQL zu stoppen oder zu starten.

**Benutzerdefinierter Bootstrap**

- Ablauf des Cluster-Bootstraps konfigurierbar machen (Alexander Kukushkin)

  Bei der Initialisierung des allerersten Knotens im Cluster können benutzerdefinierte Bootstrap-Skripte statt `initdb` verwendet werden. Der Bootstrap-Befehl erhält den Clusternamen und den Pfad zum Datenverzeichnis. Der resultierende Cluster kann für Recovery konfiguriert werden, sodass ein Bootstrap aus einem Backup mit Point-in-Time-Recovery möglich ist. Eine ausführlichere Beschreibung dieser Funktion enthält die [Dokumentationsseite](/de/patroni/replica_bootstrap#custom_bootstrap).

**Intelligentere pg_rewind-Unterstützung**

- Anhand der Timeline-Unterschiede zum aktuellen Primärserver entscheiden, ob pg_rewind ausgeführt werden muss (Alexander Kukushkin)

  Zuvor hatte Patroni feste Bedingungen zum Auslösen von pg_rewind: beim Start eines früheren Primärservers, bei einem Switchover zum festgelegten Knoten für jeden anderen Knoten im Cluster oder wenn ein Replikat mit dem Tag nofailover vorhanden war. Allen diesen Fällen ist gemeinsam, dass ein Replikat dem neuen Primärserver voraus sein kann. In manchen Fällen tat pg_rewind nichts, in anderen wurde es trotz Notwendigkeit nicht ausgeführt. Statt sich auf diese begrenzte Regelliste zu verlassen, vergleicht Patroni jetzt die WAL-Positionen von Primärserver und Replikat über das Streaming-Replikationsprotokoll, um zuverlässig zu entscheiden, ob das Replikat einen Rewind benötigt.

**Strikter synchroner Replikationsmodus**

- Unterstützung für synchrone Replikation um einen strikten Modus erweitern (James Sewell, Alexander Kukushkin)

  Wenn [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) aktiviert ist und keine Replikate mit dem Primärserver verbunden sind, deaktiviert Patroni normalerweise die synchrone Replikation, damit der Primärserver für Schreibzugriffe verfügbar bleibt. Die Option `synchronous_mode_strict` ändert dies: Ist sie gesetzt, deaktiviert Patroni die synchrone Replikation bei fehlenden Replikaten nicht und blockiert damit alle Clients, die Daten auf den Primärserver schreiben. Zusätzlich zur Garantie des synchronen Modus, Datenverlust durch automatisches Failover zu verhindern, stellt der strikte Modus sicher, dass jeder Schreibvorgang dauerhaft auf zwei Knoten gespeichert wird oder ganz unterbleibt, wenn der Cluster nur einen Knoten enthält.

**Konfigurationsbearbeitung mit patronictl**

- Bearbeitung der Konfiguration zu patronictl hinzufügen (Ants Aasma, Alexander Kukushkin)

  patronictl kann die im DCS gespeicherte dynamische Clusterkonfiguration bearbeiten. Unterstützt werden die Angabe von Parametern und Werten über die Befehlszeile, der Aufruf von \$EDITOR und die Übernahme einer Konfiguration aus einer YAML-Datei.

**Linux-Watchdog-Unterstützung**

- Watchdog-Unterstützung für Linux implementieren (Ants Aasma)

  Der Linux-Software-Watchdog wird unterstützt, um einen Knoten neu zu starten, auf dem Patroni nicht läuft oder nicht reagiert, beispielsweise wegen hoher Last. Der Linux-Software-Watchdog startet den nicht reagierenden Knoten neu. Im Abschnitt watchdog der Patroni-Konfiguration können das zu verwendende Watchdog-Gerät, standardmäßig `/dev/watchdog`, und der Modus on, automatic oder off konfiguriert werden. Weitere Informationen enthält die [Watchdog-Dokumentation](/de/patroni/watchdog#watchdog).

**Unterstützung für PostgreSQL 10 hinzufügen**

- Patroni ist mit allen bisher veröffentlichten Betaversionen von PostgreSQL 10 kompatibel. Auch für die endgültige Veröffentlichung von PostgreSQL 10 wird Kompatibilität erwartet.

**Kleinere Verbesserungen im Zusammenhang mit PostgreSQL**

- pg_hba.conf über die Patroni-Konfigurationsdatei oder die dynamische Konfiguration im DCS definieren (Alexander Kukushkin)

  Der Inhalt von `pg_hba.conf` kann im Unterabschnitt `pg_hba` des Konfigurationsabschnitts `postgresql` definiert werden. Dies vereinfacht die Verwaltung von `pg_hba.conf` auf mehreren Knoten, da sie nur einmal im DCS definiert werden muss, statt sich auf jedem Knoten anzumelden, sie manuell zu ändern und die Konfiguration neu zu laden.

  Wenn der Abschnitt definiert ist, ersetzt sein Inhalt die aktuelle `pg_hba.conf` vollständig. Patroni ignoriert ihn, wenn der PostgreSQL-Parameter `hba_file` gesetzt ist.

- Verbindung zum lokalen PostgreSQL-Cluster über einen UNIX-Socket unterstützen (Alexander Kukushkin)

  Die Option `use_unix_socket` wurde zum Abschnitt `postgresql` der Patroni-Konfiguration hinzugefügt. Wenn sie auf true gesetzt ist und die PostgreSQL-Option `unix_socket_directories` nicht leer ist, verwendet Patroni deren ersten Wert zur Verbindung mit dem lokalen PostgreSQL-Cluster. Ist `unix_socket_directories` nicht definiert, nimmt Patroni den Standardwert an und lässt den Parameter `host` in der PostgreSQL-Verbindungszeichenkette vollständig weg.

- Änderung der Superuser- und Replikationszugangsdaten beim Neuladen unterstützen (Alexander Kukushkin)

- Speichern von Konfigurationsdateien außerhalb des PostgreSQL-Datenverzeichnisses unterstützen (@jouir)

  Die neue Konfigurationsdirektive `config_dir` wurde zum Abschnitt `postgresql` hinzugefügt. Sie verweist standardmäßig auf das Datenverzeichnis und muss für Patroni beschreibbar sein.

**Fehlerbehebungen und Verbesserungen der Stabilität**

- Ausnahmen EtcdEventIndexCleared und EtcdWatcherCleared behandeln (Alexander Kukushkin)

  Wenn etcd einen Watch-Vorgang beendet, wird durch Vermeidung nutzloser Wiederholungen eine schnellere Wiederherstellung erreicht.

- Endlose Fehlerschleifen bei etcd-Ausfällen beseitigen und übermäßige Protokollausgaben reduzieren (Ants Aasma)

  Beim zweiten und jedem weiteren etcd-Verbindungsfehler werden sofortige Wiederholungen und die Ausgabe von Stacktraces im Protokoll vermieden.

- Locale-Variablen beim Forken von PostgreSQL-Prozessen exportieren (Oleksii Kliukin)

  Dies vermeidet den schwerwiegenden Fehler `postmaster became multithreaded during startup` bei nicht englischen Locales und einem mit NLS gebauten PostgreSQL.

- Zusätzliche Prüfungen beim Löschen des Replikations-Slots (Alexander Kukushkin)

  In manchen Fällen hindert der WAL-Sender Patroni daran, den Replikations-Slot zu löschen.

- Namen von Replikations-Slots gemäß den PostgreSQL-Namensregeln auf 63 (NAMEDATALEN - 1) Zeichen kürzen (Nick Scott)

- Race Condition beheben, durch die Patroni zusätzliche Verbindungen zum PostgreSQL-Cluster öffnete (Alexander Kukushkin)

- Leader-Schlüssel freigeben, wenn der Knoten mit leerem Datenverzeichnis neu startet (Alex Kerney)

- Asynchronen Executor beim Bootstrap ohne Leader als beschäftigt markieren (Alexander Kukushkin)

  Andernfalls konnten Fehler auftreten, die besagten, der Knoten gehöre zu einem anderen Cluster. Denn Patroni setzte den normalen Betrieb fort, während eine Bootstrap-Methode ausgeführt wurde, die keinen Leader im Cluster benötigt.

- WAL-E-Methode zur Replikaterstellung verbessern (Joar Wandborg, Alexander Kukushkin).

  - Beim Auswerten des WAL-E-Basisbackups csv.DictReader verwenden und ISO-Datumsangaben akzeptieren, bei denen Datum und Uhrzeit durch ein Leerzeichen getrennt sind.
  - Abruf der aktuellen WAL-Position vom Replikat unterstützen, um die wiederherzustellende WAL-Menge abzuschätzen. Zuvor rief der Code Systeminformationsfunktionen auf, die nur auf dem Primärserver verfügbar waren.

--------

## Version 1.2 {#version-12}

Veröffentlicht am 2016-12-13

Diese Version verbessert die Handhabung synchroner Replikation erheblich, macht den Startvorgang und Failover zuverlässiger, unterstützt PostgreSQL 9.6 und behebt zahlreiche Fehler. Außerdem wurde die Dokumentation einschließlich dieser Versionshinweise nach [https://patroni.readthedocs.io](https://patroni.readthedocs.io) verlagert.

**Synchrone Replikation**

- Unterstützung für synchrone Replikation hinzufügen. (Ants Aasma)

  Die neue Konfigurationsvariable [synchronous_mode](/de/patroni/replication_modes#synchronous_mode) wurde hinzugefügt. Wenn sie aktiviert ist, verwaltet Patroni `synchronous_standby_names`, um die synchrone Replikation zu aktivieren, sobald funktionsfähige Standbys verfügbar sind. Im synchronen Modus führt Patroni ein automatisches Failover nur zu einem Standby durch, der zum Zeitpunkt des Primärserver-Ausfalls synchron repliziert hat. Dadurch geht in diesem Fall keine für Benutzer sichtbare Transaktion verloren. Eine ausführliche Beschreibung und Implementierungsdetails enthält die [Funktionsdokumentation](/de/patroni/replication_modes#synchronous_mode).

**Verbesserungen der Zuverlässigkeit**

- Die im Schlüssel `leader optime` gespeicherte Leader-Position nicht aktualisieren, wenn PostgreSQL nicht zu 100% funktionsfähig ist. Sofort herabstufen, wenn die Aktualisierung des Leader-Schlüssels fehlschlägt. (Alexander Kukushkin)

- Nicht funktionsfähige Knoten aus der Liste möglicher Quellen zum Klonen neuer Replikate ausschließen. (Alexander Kukushkin)

- Wiederholungs- und Zeitüberschreitungsstrategie für Consul ähnlich wie für etcd implementieren. (Alexander Kukushkin)

- `--dcs` und `--config-file` auf alle Optionen in [patronictl](/de/patroni/patronictl#patronictl) anwenden. (Alexander Kukushkin)

- Alle Postgres-Parameter in postgresql.conf schreiben. (Alexander Kukushkin)

  Dadurch kann das von Patroni konfigurierte PostgreSQL allein mit `pg_ctl` gestartet werden.

- Ausnahmen vermeiden, wenn die Konfiguration keine Benutzer enthält. (Kirill Pushkin)

- Pausieren eines nicht funktionsfähigen Clusters zulassen. Vor dieser Korrektur brach [patronictl](/de/patroni/patronictl#patronictl) ab, wenn der Knoten, auf dem die Pause ausgeführt werden sollte, nicht funktionsfähig war. (Alexander Kukushkin)

- Watch-Funktion für den Leader verbessern. (Alexander Kukushkin)

  Zuvor beobachteten Replikate immer den Leader-Schlüssel und warteten, bis die Wartezeit ablief oder sich der Leader-Schlüssel änderte. Mit dieser Änderung beobachten sie ihn nur, wenn PostgreSQL auf dem Replikat im Zustand `running` ist, und nicht, wenn PostgreSQL gestoppt ist, startet oder neu gestartet wird.

- Race Conditions bei der Behandlung von SIGCHLD als PID 1 vermeiden. (Alexander Kukushkin)

  In Docker-Containern konnte zuvor eine Race Condition auftreten, weil derselbe Prozess in Patroni sowohl neue Prozesse erzeugte als auch deren SIGCHLD behandelte. Diese Änderung verwendet fork/execs für Patroni und überlässt dem ursprünglichen Prozess mit PID 1 die Behandlung der Signale von Kindprozessen.

- WAL-E-Wiederherstellung korrigieren. (Oleksii Kliukin)

  Zuvor verwendete die WAL-E-Wiederherstellung den Schalter `no_master`, um den Primärserver überhaupt nicht zu konsultieren. Dadurch bevorzugte Patroni immer die Wiederherstellung aus WAL gegenüber `pg_basebackup`. Diese Änderung stellt die ursprüngliche Bedeutung von `no_master` wieder her: Die WAL-E-Wiederherstellung von Patroni kann auch dann als Replikationsmethode gewählt werden, wenn der Primärserver nicht läuft. Letzteres wird anhand der an die Methode übergebenen Verbindungszeichenkette geprüft. Außerdem wird der Wiederholungsmechanismus robuster und weitere kleinere Probleme werden behandelt.

- Asynchronen Cache für DNS-Auflösung implementieren. (Alexander Kukushkin)

  Dadurch werden Fehler vermieden, wenn DNS vorübergehend nicht verfügbar ist, etwa aufgrund übermäßigen eingehenden Datenverkehrs auf dem Knoten.

- Startzustand und Zeitüberschreitung für den Primärserver-Start implementieren. (Ants Aasma, Alexander Kukushkin)

  Zuvor wartete `pg_ctl` bis zu einer Zeitüberschreitung und fuhr anschließend fort, als würde PostgreSQL laufen. Dadurch wurde PostgreSQL in Listen als laufend angezeigt, obwohl dies nicht zutraf. Eine Race Condition konnte zu einem Failover, einer Crash-Recovery oder einer durch Failover unterbrochenen Crash-Recovery mit ausgelassenem Rewind führen. Diese Änderung ergänzt den Parameter `master_start_timeout` und den neuen Zustand `starting` für die HA-Hauptschleife. Wenn `master_start_timeout` auf 0 gesetzt ist, erfolgt nach einem Primärserver-Absturz sofort ein Failover, sobald ein geeigneter Kandidat vorhanden ist. Andernfalls wartet Patroni nach dem Versuch, PostgreSQL auf dem Primärserver zu starten, für die Dauer der Zeitüberschreitung und führt anschließend nach Möglichkeit ein Failover durch. Manuelle Failover-Anfragen werden bei einem Primärserver-Absturz auch vor Ablauf der Zeitüberschreitung berücksichtigt.

  Der Parameter `timeout` wurde zum API-Endpunkt `restart` und zu [patronictl](/de/patroni/patronictl#patronictl) hinzugefügt. Ist er gesetzt und dauert ein Neustart länger als die angegebene Zeit, gilt PostgreSQL als nicht funktionsfähig und die anderen Knoten dürfen den Leader-Lock übernehmen.

- Verhalten von `pg_rewind` im Pause-Modus korrigieren. (Ants Aasma)

  Ein unnötiger Neustart im Pause-Modus wird vermieden, wenn Patroni einen Rewind für erforderlich hält, dieser aber nicht möglich ist, etwa weil `pg_rewind` fehlt. Wenn im für `pg_rewind` relevanten Abschnitt der Patroni-Konfiguration die Authentifizierung für `superuser` fehlt, wird auf die Standardwerte von `libpq` für `superuser` zurückgegriffen, standardmäßig den Betriebssystembenutzer.

- Ausführung von Callbacks serialisieren. Vor Ausführung eines neuen Callbacks den vorherigen desselben Typs beenden. Erzeugung von Zombie-Prozessen beim Ausführen von Callbacks beheben. (Alexander Kukushkin)

- Hochstufung eines früheren Primärservers vermeiden, wenn der Leader-Schlüssel im DCS gesetzt ist, seine Aktualisierung jedoch fehlschlägt. (Alexander Kukushkin)

  Dadurch wird verhindert, dass ein aktueller Primärserver seine Rolle beibehält, wenn er zusammen mit einer Minderheit der Knoten in etcd oder einem anderen DCS isoliert ist, der „inkonsistente Lesezugriffe“ erlaubt.

**Verschiedenes**

- Konfigurationsoption `post_init` für den Bootstrap hinzufügen. (Alejandro Martínez)

  Patroni ruft das als Argument dieser Option angegebene Skript unmittelbar nach `initdb` und dem Start von PostgreSQL für einen neuen Cluster auf. Das Skript erhält eine Verbindungs-URL mit `superuser`. Wenn ein Passwort angegeben ist, setzt Patroni `PGPASSFILE` auf die Datei `.pgpass`, die das Passwort enthält. Schlägt das Skript fehl, schlägt auch die Patroni-Initialisierung fehl. Dies ist nützlich, um Benutzer hinzuzufügen oder Erweiterungen im neuen Cluster zu erstellen.

- Unterstützung für PostgreSQL 9.6 implementieren. (Alexander Kukushkin)

  `wal_level = replica` wird als Synonym für `hot_standby` verwendet, sodass beim Wechsel zwischen beiden kein pending_restart-Schalter gesetzt wird. (Alexander Kukushkin)

**Verbesserungen der Dokumentation**

- [Ablaufdiagramm der Patroni-Hauptschleife](https://raw.githubusercontent.com/patroni/patroni/master/docs/ha_loop_diagram.png) hinzufügen. (Alejandro Martínez, Alexander Kukushkin)

- README um das Helm-Chart und Links zu den Versionshinweisen ergänzen. (Lauri Apple)

- Patroni-Dokumentation zu `Read the Docs` verlagern. Die aktuelle Dokumentation ist unter [https://patroni.readthedocs.io](https://patroni.readthedocs.io) verfügbar. (Oleksii Kliukin)

  Dadurch lässt sich die Dokumentation auf verschiedenen Geräten einschließlich Smartphones einfach lesen und durchsuchen.

- Paket auf semantische Versionierung umstellen. (Oleksii Kliukin)

  Patroni folgt dem Versionsschema major.minor.patch, damit kleine, aber kritische Fehlerbehebungen keine neue Minor-Version erfordern. Versionshinweise werden nur für die Minor-Version veröffentlicht und enthalten alle Patches.

--------

## Version 1.1 {#version-11}

Veröffentlicht am 2016-09-07

Diese Version verbessert die Verwaltung von Patroni-Clustern durch den Pause-Modus und die Wartung durch geplante und bedingte Neustarts. Sie macht die Interaktion von Patroni mit etcd oder Zookeeper robuster und erweitert patronictl erheblich.

**Upgrade-Hinweis**

Beim Upgrade von Versionen unter 1.0 sind die Hinweise zu Änderungen an Zugangsdaten und Konfigurationsformat in den Versionshinweisen zu 1.0 zu beachten.

**Pause-Modus**

- Pause-Modus einführen, um Patroni vorübergehend von der Verwaltung einer PostgreSQL-Instanz zu entkoppeln (Murat Kabilov, Alexander Kukushkin, Oleksii Kliukin).

  Zuvor musste Patroni mit SIGKILL beendet werden, um es zu stoppen, ohne PostgreSQL zu beenden. Der neue Pause-Modus entkoppelt Patroni clusterweit von PostgreSQL, ohne Patroni zu beenden. Er ähnelt dem Wartungsmodus von Pacemaker. Patroni aktualisiert weiterhin die Member- und Leader-Schlüssel im DCS, startet und stoppt den PostgreSQL-Server dabei aber nicht und führt auch keine Neustarts durch. Es gibt einige Ausnahmen: Manuelle Failover, Neuinitialisierungen und Neustarts bleiben beispielsweise erlaubt. Eine [ausführliche Beschreibung dieser Funktion](/de/patroni/pause#pause) ist verfügbar.

Außerdem unterstützt patronictl die neuen Befehle [pause](/de/patroni/pause#pause) und `resume`, um den Pause-Modus ein- und auszuschalten.

**Geplante und bedingte Neustarts**

- Bedingungen zum API-Befehl restart hinzufügen (Oleksii Kliukin)

  Diese Änderung erweitert Patroni-Neustarts um Bedingungen, die vor dem Neustart geprüft werden können. Dazu gehören Neustarts abhängig von der PostgreSQL-Rolle als Primärserver oder Replikat, die Prüfung der PostgreSQL-Versionsnummer und Neustarts nur dann, wenn sie zum Anwenden von Konfigurationsänderungen erforderlich sind.

- Geplante Neustarts hinzufügen (Oleksii Kliukin)

  Neustarts können jetzt für einen späteren Zeitpunkt geplant werden. Pro Knoten wird nur ein geplanter Neustart unterstützt. Er kann gelöscht werden, wenn er nicht mehr benötigt wird. Geplante und bedingte Neustarts können kombiniert werden. So lassen sich beispielsweise PostgreSQL-Minor-Upgrades nachts ausführen und nur Instanzen mit veralteter Minor-Version neu starten, ohne Postgres-spezifische Logik in Administrationsskripte aufzunehmen.

- Unterstützung für bedingte und geplante Neustarts zu patronictl hinzufügen (Murat Kabilov).

  patronictl restart unterstützt mehrere neue Optionen. Außerdem gibt es den Befehl patronictl flush zum Löschen geplanter Aktionen.

**Robuste DCS-Interaktion**

- Kazoo-Zeitüberschreitungen abhängig von loop_wait setzen (Alexander Kukushkin)

  Ursprünglich wurden ping_timeout und connect_timeout aus der ausgehandelten Session-Zeitüberschreitung berechnet. Patronis loop_wait wurde nicht berücksichtigt. Dadurch konnte ein einzelner Wiederholungsversuch länger als die Session-Zeitüberschreitung dauern, sodass Patroni den Lock freigeben und sich herabstufen musste.

  Diese Änderung setzt die Ping- und Verbindungszeitüberschreitung auf die Hälfte von loop_wait. Dadurch werden Verbindungsprobleme schneller erkannt und es bleibt genug Zeit für einen erneuten Verbindungsversuch, bevor der Lock verloren geht.

- etcd-Topologie erst nach erfolgreicher ursprünglicher Anfrage aktualisieren (Alexander Kukushkin)

  Die Aktualisierung der dem Client bekannten etcd-Topologie wird bis nach der ursprünglichen Anfrage aufgeschoben. Beim Abruf der Clustertopologie werden die Zeitüberschreitungen für Wiederholungen abhängig von der bekannten Anzahl der Knoten im etcd-Cluster festgelegt. Dadurch zieht der Client das Ergebnis der Anfrage einer aktuellen Knotenliste vor.

  Beide Änderungen machen Patroni-Verbindungen zum DCS bei Netzwerkproblemen robuster.

**Patronictl, Überwachung und Konfiguration**

- Informationen über streamende Replikate über die API zurückgeben (Feike Steenbergen)

  Zuvor gab es keinen zuverlässigen Weg, Patroni nach PostgreSQL-Instanzen zu fragen, die keine Änderungen streamen, beispielsweise wegen Verbindungsproblemen. Diese Änderung stellt den Inhalt von pg_stat_replication über den Endpunkt /patroni bereit.

- Befehl patronictl scaffold hinzufügen (Oleksii Kliukin)

  Ein Befehl zum Erstellen einer Clusterstruktur in etcd wurde hinzugefügt. Der Cluster wird mit benutzerdefinierter sysid und benutzerdefiniertem Leader erstellt; sowohl Leader- als auch Member-Schlüssel werden dauerhaft angelegt. Dies ist für sogenannte Konfigurationen ohne Primärserver nützlich, bei denen ein nur aus Replikaten bestehender Patroni-Cluster von einem externen Primärserver repliziert, der Patroni nicht kennt. Anschließend kann der Leader-Schlüssel entfernt werden, wodurch einer der Patroni-Knoten hochgestuft und der ursprüngliche Primärserver durch einen Patroni-basierten HA-Cluster ersetzt wird.

- Konfigurationsoption `bin_dir` zur Angabe der PostgreSQL-Programme hinzufügen (Ants Aasma)

  Auf Linux-Distributionen, die die gleichzeitige Installation mehrerer PostgreSQL-Versionen unterstützen, ist die ausdrückliche Angabe des Verzeichnisses der PostgreSQL-Programme nützlich.

- Überschreiben des Konfigurationsdateipfads mit `custom_conf` ermöglichen (Alejandro Martínez)

  Benutzerdefinierte Pfade zu Konfigurationsdateien, die Patroni nicht verwaltet, sind möglich; siehe [Details](/de/patroni/config/yaml#postgresql_settings).

**Fehlerbehebungen und Codeverbesserungen**

- Patroni mit dem neuen Versionsschema ab PostgreSQL 10 kompatibel machen (Feike Steenbergen)

  Patroni versteht bei bedingten Neustarts anhand der PostgreSQL-Version auch 2-stellige Versionsnummern.

- pkgutil zum Auffinden von DCS-Modulen verwenden (Alexander Kukushkin)

  Statt Verzeichnisse manuell zu durchlaufen, wird das dafür vorgesehene Python-Modul zum Auffinden von DCS-Modulen verwendet.

- Beim Start von Patroni immer den Callback on_start aufrufen (Alexander Kukushkin)

  Zuvor rief Patroni beim Anhängen an einen bereits laufenden Knoten mit korrekter Rolle keinen Callback auf. Da Callbacks häufig zum Weiterleiten von Client-Verbindungen dienen, konnte der laufende Knoten dadurch im Verbindungsschema unregistriert bleiben. Mit dieser Korrektur ruft Patroni on_start auch dann auf, wenn es sich an einen bereits laufenden Knoten anhängt.

- Aktive Replikations-Slots nicht löschen (Murat Kabilov, Oleksii Kliukin)

  Aktive physische Replikations-Slots auf dem Primärserver werden nicht gelöscht; PostgreSQL kann solche Slots ohnehin nicht löschen. Diese Änderung ermöglicht Replikate und Verbraucher auf dem Primärserver, die nicht von Patroni verwaltet werden.

- Patroni-Verbindungen beim Start einer PostgreSQL-Instanz schließen (Alexander Kukushkin)

  Patroni schließt beim Start eines PostgreSQL-Knotens zwingend alle bisherigen Verbindungen. Dadurch wird vermieden, dass alte Verbindungen wiederverwendet werden, nachdem postmaster mit SIGKILL beendet wurde.

- Ungültige Zeichen beim Ableiten von Slot-Namen aus Mitgliedsnamen ersetzen (Ants Aasma)

  Standby-Namen, die nicht den Namensregeln für Slots entsprechen, führen nicht mehr zum Fehlschlagen der Slot-Erstellung und des Standby-Starts. Bindestriche in Slot-Namen werden durch Unterstriche ersetzt, alle anderen in Slot-Namen unzulässigen Zeichen durch ihre Unicode-Codepoints.

--------

## Version 1.0 {#version-10}

Veröffentlicht am 2016-07-05

Diese Version führt die globale dynamische Konfiguration ein, mit der PostgreSQL- und Patroni-Konfigurationsparameter für den gesamten HA-Cluster dynamisch geändert werden können. Außerdem enthält sie zahlreiche Fehlerbehebungen.

**Upgrade-Hinweis**

Beim Upgrade von v0.90 oder früher müssen stets alle Replikate vor dem Primärserver aktualisiert werden. Da Replikationszugangsdaten nicht mehr im DCS gespeichert werden, kann sich ein altes Replikat nicht mit dem neuen Primärserver verbinden.

**Dynamische Konfiguration**

- Dynamische globale Konfiguration implementieren (Alexander Kukushkin)

  Der neue REST-API-Endpunkt /config stellt PostgreSQL- und Patroni-Konfigurationsparameter bereit, die global für den gesamten HA-Cluster, also Primärserver und alle Replikate, gesetzt werden sollten. Diese Parameter werden im DCS gespeichert und können in vielen Fällen ohne Unterbrechung von PostgreSQL oder Patroni angewendet werden. Wenn bestimmte Werte einen PostgreSQL-Neustart erfordern, setzt Patroni den besonderen, über die API sichtbaren Schalter „pending restart“. In diesem Fall sollte der Neustart manuell über die API ausgelöst werden.

  SIGHUP an Patroni oder eine POST-Anfrage an /reload veranlasst Patroni, die Konfigurationsdatei erneut einzulesen.

  Welche Parameter geändert werden können und in welcher Reihenfolge verschiedene Konfigurationsquellen verarbeitet werden, beschreibt die [Patroni-Konfiguration](/de/patroni/config#config).

  Das Format der Konfigurationsdatei *hat sich* seit v0.90 *geändert*. Patroni ist weiterhin mit alten Konfigurationsdateien kompatibel. Um die Bootstrap-Parameter zu nutzen, müssen sie jedoch angepasst werden. Es wird empfohlen, die Dateien anhand der [Dokumentation zur dynamischen Konfiguration](/de/patroni/config/dynamic#dynamic) zu aktualisieren.

**Flexiblere Konfiguration**\*

- PostgreSQL-Konfiguration und Namen der Datenbank, mit der Patroni sich verbindet, konfigurierbar machen (Misja Hoebe)

  Die Konfigurationsparameter `database` und `config_base_name` wurden eingeführt. Dies ermöglicht unter anderem den Betrieb von Patroni mit PipelineDB und anderen PostgreSQL-Forks.

- Einstellung einiger Patroni-Konfigurationsparameter über die Umgebung ermöglichen (Alexander Kukushkin)

  Dazu gehören Scope, Knotenname, Namespace und Geheimnisse. Dies erleichtert den Betrieb von Patroni in einer dynamischen Umgebung wie Kubernetes. Weitere Einzelheiten enthält die Übersicht der [unterstützten Umgebungsvariablen](/de/patroni/config/env#env).

- Integrierten Patroni-Docker-Container zur Nutzung der umgebungsbasierten Konfiguration aktualisieren (Feike Steenbergen).

- Zookeeper-Unterstützung zum Patroni-Docker-Image hinzufügen (Alexander Kukushkin)

- Konfigurationsoptionen für Zookeeper und Exhibitor trennen (Alexander Kukushkin)

- Patroni-Code zum Einlesen der Konfiguration in patronictl wiederverwenden (Alexander Kukushkin)

  Dadurch kann patronictl die umgebungsbasierte Konfiguration nutzen.

- Anwendungsnamen in primary_conninfo auf den Knotennamen setzen (Alexander Kukushkin)

  Dies vereinfacht die Identifizierung und Konfiguration synchroner Replikation für einen bestimmten Knoten.

**Verbesserungen der Stabilität, Sicherheit und Bedienbarkeit**

- sysid zurücksetzen und pg_controldata während der Wiederherstellung eines Backups nicht aufrufen (Alexander Kukushkin)

  Diese Änderung reduziert die überflüssigen Meldungen der Patroni-API-Health-Checks während der langwierigen Initialisierung eines Knotens aus einem Backup.

- Mehrere Sonderfälle von pg_rewind beheben (Alexander Kukushkin)

  pg_rewind wird nicht ausgeführt, wenn der Quellcluster kein Primärserver ist.

  Außerdem wird das Datenverzeichnis nach einem fehlgeschlagenen Rewind nicht entfernt, sofern nicht der neue Parameter *remove_data_directory_on_rewind_failure* auf true gesetzt ist. Standardmäßig ist er false.

- Passwörter aus der Replikations-Verbindungszeichenkette im DCS entfernen (Alexander Kukushkin)

  Zuvor verwendete Patroni immer die Replikationszugangsdaten aus der Postgres-URL im DCS. Jetzt werden die Zugangsdaten aus der Patroni-Konfiguration übernommen. Die Geheimnisse, also Replikationsbenutzername und -passwort, sind nicht mehr im DCS offengelegt.

- Asynchrone Abläufe rund um den Aufruf demote korrigieren (Alexander Kukushkin)

  Die Herabstufung läuft jetzt vollständig asynchron, ohne Interaktionen mit dem DCS zu blockieren.

- patronictl den Authorization-Header immer senden lassen, wenn er konfiguriert ist (Alexander Kukushkin)

  Dadurch kann patronictl „geschützte“ Anfragen wie Neustart oder Neuinitialisierung senden, wenn Patroni dafür eine Autorisierung verlangt.

- Ausnahme SystemExit korrekt behandeln (Alexander Kukushkin)

  Dadurch werden Probleme vermieden, bei denen Patroni nach Empfang von SIGTERM nicht ordnungsgemäß beendet wurde.

- HAProxy-Beispielvorlagen für confd (Alexander Kukushkin)

  Mit confd wird aus dem Patroni-Zustand im DCS eine HAProxy-Konfiguration erzeugt und dynamisch angepasst.

- Dokumentation verbessern und umstrukturieren, damit sie für neue Benutzer leichter zugänglich ist (Lauri Apple)

- API muss während pg_ctl stop role=master melden (Alexander Kukushkin)

  Dadurch werden Callback-Aufrufe zuverlässiger, insbesondere beim Stoppen des Clusters. Außerdem wurde die Option `pg_ctl_timeout` eingeführt, um die Zeitüberschreitung für Start-, Stopp- und Neustartaufrufe über `pg_ctl` festzulegen.

- Wiederholungslogik in etcd korrigieren (Alexander Kukushkin)

  Wiederholungen werden vorhersehbarer und robuster.

- Zookeeper-Code gegen kurze Netzwerkunterbrechungen robuster machen (Alexander Kukushkin)

  Kürzere Verbindungszeitüberschreitungen ermöglichen häufigere Verbindungsversuche zu Zookeeper.

--------

## Version 0.90 {#version-090}

Veröffentlicht am 2016-04-27

Diese Version unterstützt Consul, ergänzt den Tag *noloadbalance*, ändert das Verhalten des Tags *clonefrom* und verbessert die Handhabung von *pg_rewind* sowie das Steuerungsprogramm *patronictl*.

**Consul-Unterstützung**

- Consul-Unterstützung implementieren (Alexander Kukushkin)

  Patroni kann neben etcd und Zookeeper auch Consul verwenden. Die Verbindungsparameter können in der YAML-Datei konfiguriert werden.

**Neue und verbesserte Tags**

- Tag *noloadbalance* implementieren (Alexander Kukushkin)

  Mit diesem Tag meldet Patroni dem Load-Balancer stets, dass das Replikat nicht verfügbar ist.

- Implementierung des Tags *clonefrom* ändern (Alexander Kukushkin)

  Zuvor musste bei *clonefrom* ein Knotenname angegeben werden, wodurch ein markiertes Replikat zwingend von diesem Knoten geklont wurde. Die neue Implementierung macht *clonefrom* zu einem booleschen Tag: Ist er auf true gesetzt, wird das Replikat zum möglichen Klon-Ursprung für andere Replikate. Gibt es mehrere Kandidaten, wählt das Replikat zufällig einen davon aus.

**Verbesserungen der Stabilität und Sicherheit**

- Zahlreiche Verbesserungen der Zuverlässigkeit (Alexander Kukushkin)

  Überflüssige Fehlermeldungen werden entfernt, die Stabilität des Failovers verbessert und Sonderfälle beim Lesen aus dem DCS, Herunterfahren, Herabstufen und erneuten Eingliedern des früheren Leaders behandelt.

- Systemskript verbessern, damit beim Stoppen keine Kindprozesse von Patroni beendet werden (Jan Keirse, Alexander Kukushkin)

  Zuvor sendete *systemd* beim Stoppen von Patroni auch ein Signal an PostgreSQL. Da Patroni selbst ebenfalls versuchte, PostgreSQL zu stoppen, wurden zwei verschiedene Anfragen zum Herunterfahren gesendet: zuerst smart, dann fast. Dadurch trennten sich Replikate zu früh und ein früherer Primärserver konnte nach der Herabstufung nicht wieder beitreten. Die Korrektur stammt von Jan, die vorausgehende Untersuchung von Alexander.

- Fälle beseitigen, in denen der frühere Primärserver vor dem erneuten Beitritt als Replikat pg_rewind nicht aufrufen konnte (Oleksii Kliukin)

  Zuvor wurde *pg_rewind* nur nach einem Absturz des früheren Primärservers aufgerufen. Jetzt wird pg_rewind für den früheren Primärserver immer ausgeführt, sofern pg_rewind auf dem System vorhanden ist. Damit wird der Fall behoben, dass der Primärserver heruntergefahren wird, bevor die Replikate die letzten Änderungen erhalten haben, etwa beim Herunterfahren im Modus „smart“.

- Zahlreiche Verbesserungen an Unit- und Akzeptanztests, insbesondere Unterstützung für Zookeeper und Consul (Alexander Kukushkin).

- Travis CI beschleunigen und Unterstützung für Tests mit Zookeeper (Exhibitor) und Consul implementieren (Alexander Kukushkin)

  Sowohl Unit- als auch Akzeptanztests werden bei jedem Commit oder Pull Request automatisch mit etcd, Zookeeper und Consul ausgeführt.

- Umgebungsvariablen vor dem Aufruf von PostgreSQL-Befehlen aus Patroni bereinigen (Feike Steenbergen)

  Dadurch wird verhindert, dass über eine Verbindung zum von Patroni verwalteten PostgreSQL-Cluster Systemumgebungsvariablen ausgelesen werden können.

**Änderungen an Konfiguration und Steuerung**

- Konfiguration von patronictl und Patroni vereinheitlichen (Feike Steenbergen)

  patronictl kann dieselbe Konfigurationsdatei wie Patroni selbst verwenden.

- Einlesen der Konfiguration aus Umgebungsvariablen durch Patroni ermöglichen (Oleksii Kliukin)

  Dies vereinfacht die automatische Erzeugung einer Patroni-Konfiguration oder das Zusammenführen einer Konfiguration aus verschiedenen Quellen.

- Datenbanksystemkennung in die von der API zurückgegebenen Informationen aufnehmen (Feike Steenbergen)

- *delete_cluster* für alle verfügbaren DCS implementieren (Alexander Kukushkin)

  Dadurch unterstützt patronictl neben etcd auch andere DCS.

--------

## Version 0.80 {#version-080}

Veröffentlicht am 2016-03-14

Diese Version unterstützt *kaskadierende Replikation* und vereinfacht die Patroni-Verwaltung durch *geplante Failover*. Für die Migration auf diese Version können ältere Patroni-Versionen, insbesondere 0.78, zusammen mit ihr verwendet werden. Die Funktionen für geplante Failover und kaskadierende Replikation funktionieren jedoch nur mit Patroni 0.80 und neuer.

**Kaskadierende Replikation**

> - Unterstützung für die Tags *replicatefrom* und *clonefrom* auf Patroni-Knoten hinzufügen (Oleksii Kliukin).
>
> Mit dem Tag *replicatefrom* kann ein Replikat einen beliebigen Knoten als Quelle verwenden; dies muss nicht der Primärserver sein. *clonefrom* bietet dasselbe für das anfängliche Backup. Zusammen ermöglichen sie die vollständige Unterstützung kaskadierender Replikation in Patroni.

- Ausführung von Replikationsmethoden zur Initialisierung eines Replikats auch ohne aktive Replikationsverbindung unterstützen (Oleksii Kliukin).

> Dies ist nützlich, um Replikate aus auf S3 oder FTP gespeicherten Snapshots zu erstellen. Eine Replikationsmethode, die keine aktive Replikationsverbindung benötigt, sollte *no_master: true* in der YAML-Konfiguration angeben. Besteht eine Replikationsverbindung, werden diese Skripte weiterhin der Reihe nach aufgerufen.

**Verbesserungen in Patronictl, API und DCS**

- Geplante Failover implementieren (Feike Steenbergen).

  Mit patronictl oder API-Aufrufen können Failover für einen bestimmten zukünftigen Zeitpunkt geplant werden.

- Unterstützung für die Parameter *dbuser* und *password* in patronictl hinzufügen (Feike Steenbergen).

- PostgreSQL-Version zur Ausgabe des Health Checks hinzufügen (Feike Steenbergen).

- Zookeeper-Unterstützung in patronictl verbessern (Oleksandr Shulgin)

- Auf python-etcd 0.4.3 migrieren (Alexander Kukushkin)

**Konfiguration**

- Beispielskript zur Systemkonfiguration für Patroni hinzufügen (Jan Keirse).
- Fehler beheben, durch den Patroni bei DB-Verbindungen den in der Konfigurationsdatei angegebenen Superuser-Namen ignorierte (Alexander Kukushkin).
- Behandlung von CTRL-C korrigieren, indem für den von Patroni gestarteten postmaster eine eigene Session-ID und Prozessgruppe erstellt wird (Alexander Kukushkin).

**Tests**

- Akzeptanztests mit *behave* hinzufügen, um reale Patroni-Betriebsszenarien zu prüfen (Alexander Kukushkin, Oleksii Kliukin).

  Die Tests können manuell mit dem Befehl *behave* gestartet werden. Sie werden außerdem automatisch bei Pull Requests und nach Commits ausgeführt.

  Versionshinweise zu einigen älteren Versionen finden sich auf der [GitHub-Seite des Projekts](https://github.com/patroni/patroni/releases).
