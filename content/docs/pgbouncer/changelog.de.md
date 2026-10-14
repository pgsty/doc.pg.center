---
title: "Änderungsprotokoll"
weight: 70
description: "Versionsgeschichte und Versionshinweise zu PgBouncer"
icon: fa-solid fa-scroll
module: [PGBOUNCER]
categories: [Referenz]
aliases: [/pgbouncer/changelog/]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/NEWS.md"
---

--------

## PgBouncer 1.26.x {#pgbouncer-126x}

**2026-09-23  -  PgBouncer 1.26.0  -  „Alle bisherigen search_path ignorieren“**

- Sicherheit
    * CVE-2026-19888 behoben: PgBouncer vor 1.26.0 prüfte nicht, ob die SCRAM-Nachricht client-final-message eine Nonce enthielt. Ein nicht authentifizierter Angreifer konnte PgBouncer aus der Ferne zum Absturz bringen, indem er eine client-final-message ohne Nonce sendete. Dies gilt auch für nicht existierende Benutzer, da PgBouncer für diese einen SCRAM-Austausch simuliert. Dieser Fehler bestand seit der Einführung der SCRAM-Unterstützung in PgBouncer 1.11.0.
    * CVE-2026-6668 behoben: Ein Ganzzahlüberlauf in der Logik zur Vergrößerung des Paketpuffers konnte PgBouncer vor 1.26.0 in einer Endlosschleife hängen lassen. Dazu musste eine große Datenmenge in einen einzelnen Paketpuffer gesendet werden. Dies ist ohne vorherige Authentifizierung möglich, wenn `max_packet_size` seinen Standardwert behält. Da PgBouncer nur einen Thread verwendet, konnte es bis zum Beenden des Prozesses keine Clients mehr bedienen.
    * CVE-2026-6669 behoben: PgBouncer vor 1.26.0 begrenzte die von einem Server akzeptierte SCRAM-Iterationszahl nicht. Ein böswilliger oder kompromittierter PostgreSQL-Server konnte PgBouncer dadurch bei einer einzigen Anmeldung zu unbegrenzt viel Rechenarbeit veranlassen. Währenddessen konnte PgBouncer keine anderen Clients und Datenbanken bedienen. Die Iterationszahl darf jetzt höchstens 1000000 betragen.
- Funktionen
    * Alle Parameter, die PostgreSQL standardmäßig meldet, werden nachverfolgt. Insbesondere werden damit `search_path` (ab PostgreSQL 18) und `default_transaction_read_only` (ab PostgreSQL 14) jetzt standardmäßig nachverfolgt. Bisher beeinflusste ein Client, der im Transaktions-Pooling-Modus `SET search_path` oder `SET default_transaction_read_only = true` ausführte, andere Clients, die später dieselbe Serververbindung verwendeten. ([#1580], [#1573])
    * Die Einstellung `pool_idle_timeout` zum Entfernen längere Zeit ungenutzter Pools hinzugefügt. Dies ist bei Konfigurationen mit vielen verschiedenen Benutzern nützlich, die sich selten verbinden. Ohne diese Einstellung wächst die Anzahl der Pools in solchen Konfigurationen unbegrenzt. Die Einstellung ist standardmäßig deaktiviert, da beim Entfernen eines Pools auch dessen Statistiken verloren gehen. ([#1491])
    * `query_wait_timeout` kann pro Benutzer und pro Datenbank konfiguriert werden. ([#1449])
    * Die Statistik `client_login_count` zu `SHOW STATS` hinzugefügt. Sie zählt erfolgreiche Client-Anmeldungen und ermöglicht es, Clients zu erkennen, die ständig Verbindungen auf- und abbauen. ([#1457])
    * Bei der Anmeldung werden PgBouncer-spezifische `ParameterStatus`-Nachrichten an Clients gesendet: `pgbouncer.version`, `pgbouncer.pool_mode` und `pgbouncer.max_prepared_statements`. Damit können Clients und Treiber erkennen, dass sie über PgBouncer verbunden sind, und ihr Verhalten entsprechend anpassen. ([#1490])
    * Die Einstellung `login_notify_message` hinzugefügt. Ist sie gesetzt, wird ihr Wert nach der Anmeldung als NOTICE-Nachricht an Clients gesendet. Damit lässt sich Clients deutlich machen, dass sie über PgBouncer und nicht direkt mit PostgreSQL verbunden sind. ([#1488])
    * Unterstützung für das Bauen von PgBouncer mit meson hinzugefügt, einschließlich eines Windows-Builds mit der UCRT64-Umgebung. Builds mit Autoconf werden weiterhin unterstützt. ([#1524], [#1426], [#1568], [#1585], [#1602], [#1607])
    * Ein Logo hinzugefügt. ([#1609])
- Änderungen
    * Die veraltete Funktion für Online-Neustarts (`-R`, auch als Übernahme bezeichnet) entfernt, zusammen mit den Verwaltungsbefehlen `SHOW FDS` und `SUSPEND`, die nur zu ihrer Unterstützung vorhanden waren. Verwenden Sie stattdessen [rollierende Neustarts mit `so_reuseport`][rolling-restart-docs]. ([#1581])
    * Die maximale Passwortlänge auf 65535 Bytes erhöht, entsprechend libpq. ([#1310], [#1520])
    * Ein von `auth_query` zurückgegebener Benutzername `NULL` wird genauso behandelt wie ein Ergebnis ohne Zeilen und nicht mehr als Fehler. ([#1569])
    * `SET extra_float_digits` wird in der Verwaltungsdatenbank akzeptiert. Neuere PostgreSQL-JDBC-Treiber senden diesen Befehl beim Verbindungsaufbau. ([#1550])
    * `mkauth.py` kann durch Angabe von `-` als Ausgabedatei nach stdout schreiben. ([#1514])
    * Bei Builds mit OpenSSL 3 werden bei einem unerwarteten EOF von Clients keine störenden Fehlermeldungen mehr protokolliert. ([#1507])
    * Bei Builds mit OpenSSL 3 enthalten TLS-Fehlermeldungen den zugrunde liegenden Systemfehler. ([#1492])
    * Ein C11-Compiler ist erforderlich. ([#1417])
    * Es wird protokolliert, welches Limit das Verdrängen einer Serververbindung ausgelöst hat. Der Trennungsgrund lautet jetzt `evicted for max_db_connections`, `evicted for pool_size` oder `evicted for max_user_connections` statt lediglich `evicted`. ([#1597])
- Fehlerbehebungen
    * Behoben, dass verspätete `COPY`-Nachrichten im Transaktions-Pooling-Modus den Pool erschöpften. Dadurch funktioniert `COPY` in diesem Modus auch außerhalb einer expliziten Transaktion. ([#1471])
    * Fehler bei der LDAP-Authentifizierung mit langen DNs durch Erhöhen der maximalen Länge von LDAP-URLs behoben. ([#1497])
    * Behoben, dass die SCRAM-Durchleitung zwischengespeicherte Anmeldedaten eines erzwungenen Benutzers beschädigte. Dadurch schlugen Serveranmeldungen fehl, weil der eigentliche Server den SCRAM-Nachweis zurückwies. ([#1612])
    * Behoben, dass die SCRAM-Durchleitung mit gespeicherten SCRAM-Secrets nach dem erneuten Verbindungsaufbau zum Server mit dem Fehler "password is SCRAM secret but client authentication did not provide SCRAM keys" fehlschlug. ([#1504], Fehler in 1.25.1 eingeführt)
    * Einen Absturz durch Zugriff auf bereits freigegebenen Speicher behoben, wenn ein Replikationsclient die Verbindung trennt, während die Anmeldung seiner Serververbindung noch läuft. ([#1577])
    * Das Verdrängen ungenutzter Serververbindungen für Replikationsclients bei vollem Pool korrigiert. Bisher konnte ein einzelner Replikationsclient alle ungenutzten Server im Pool statt nur eines verdrängen. Enthielt der Pool aufgrund des Reservepools oder von Abbruchanfragen mehr Server als `pool_size`, wurde hingegen überhaupt keiner verdrängt. ([#1597])
    * Hängende TLS-Verbindungen behoben, wenn ein Paket über die Grenze des Paketpuffers hinausreicht, etwa bei `SET application_name` mit einem langen Wert. ([#1531])
    * Behoben, dass Antworten auf vorbereitete Anweisungen in falscher Reihenfolge gesendet wurden, wenn ein Stapel `Parse`- und `Close`-Nachrichten ohne dazwischenliegendes `Sync` mischte. ([#1555])
    * Fehlerhaftes Verhalten bei Parametern behoben, die in `track_extra_parameters` aufgeführt sind, vom Server aber nicht gemeldet werden, wenn ein Client sie in seinem Startpaket setzt. ([#1576])
    * Anmeldefehler behoben, wenn der Server seine Anmeldepakete auf mehrere TCP-Pakete verteilt, etwa wenn sich ein weiterer Proxy zwischen PgBouncer und PostgreSQL befindet. ([#1446])
    * Behoben, dass `query_timeout` Verbindungen schloss, obwohl keine Abfrage lief. ([#1395])
    * Das doppelte Senden einer `NegotiateProtocolVersion`-Nachricht behoben, wenn nicht sofort ein Server verfügbar war. ([#1460])
    * Behoben, dass die Spalte `pool_size` in `SHOW USERS` für Benutzer einen Wert anzeigte, für die keiner konfiguriert war. ([#1489])
    * Die Fehlermeldung für den Verwaltungsbefehl `ENABLE` korrigiert. ([#1308])
    * Die Kompilierung mit künftigen OpenSSL-Versionen korrigiert, die `struct asn1_string_st` zu einem opaken Typ machen. ([#1440])
    * Verhindert, dass der Compiler das Löschen sensibler kryptografischer Daten vom Stack wegoptimiert. ([#1508])
    * Das Linken von `pgbevent.dll` mit clang unter Windows korrigiert. ([#1571])
    * Pfade von Dateien auf der obersten Ebene des Release-Tarballs korrigiert, die als `pgbouncer-X.Y.Z/./configure` statt als `pgbouncer-X.Y.Z/configure` gespeichert waren. ([#1549])
    * Ein Speicherleck beim Lesen von `track_extra_parameters` aus der Konfiguration behoben. ([#1510])
    * Ein Speicherleck für jedes Startpaket behoben, das einen Protokollerweiterungsparameter (Präfix `_pq_.`) enthielt. Es konnte von nicht authentifizierten Clients ausgelöst werden. ([#1540])

[rolling-restart-docs]: /de/docs/pgbouncer/usage/#shutdown-wait_for_clients
[#1308]: https://github.com/pgbouncer/pgbouncer/pull/1308
[#1310]: https://github.com/pgbouncer/pgbouncer/pull/1310
[#1395]: https://github.com/pgbouncer/pgbouncer/pull/1395
[#1417]: https://github.com/pgbouncer/pgbouncer/pull/1417
[#1426]: https://github.com/pgbouncer/pgbouncer/pull/1426
[#1440]: https://github.com/pgbouncer/pgbouncer/pull/1440
[#1446]: https://github.com/pgbouncer/pgbouncer/pull/1446
[#1449]: https://github.com/pgbouncer/pgbouncer/pull/1449
[#1457]: https://github.com/pgbouncer/pgbouncer/pull/1457
[#1460]: https://github.com/pgbouncer/pgbouncer/pull/1460
[#1471]: https://github.com/pgbouncer/pgbouncer/pull/1471
[#1488]: https://github.com/pgbouncer/pgbouncer/pull/1488
[#1489]: https://github.com/pgbouncer/pgbouncer/pull/1489
[#1490]: https://github.com/pgbouncer/pgbouncer/pull/1490
[#1491]: https://github.com/pgbouncer/pgbouncer/pull/1491
[#1492]: https://github.com/pgbouncer/pgbouncer/pull/1492
[#1497]: https://github.com/pgbouncer/pgbouncer/pull/1497
[#1504]: https://github.com/pgbouncer/pgbouncer/pull/1504
[#1507]: https://github.com/pgbouncer/pgbouncer/pull/1507
[#1508]: https://github.com/pgbouncer/pgbouncer/pull/1508
[#1510]: https://github.com/pgbouncer/pgbouncer/pull/1510
[#1514]: https://github.com/pgbouncer/pgbouncer/pull/1514
[#1520]: https://github.com/pgbouncer/pgbouncer/pull/1520
[#1524]: https://github.com/pgbouncer/pgbouncer/pull/1524
[#1531]: https://github.com/pgbouncer/pgbouncer/pull/1531
[#1540]: https://github.com/pgbouncer/pgbouncer/pull/1540
[#1549]: https://github.com/pgbouncer/pgbouncer/pull/1549
[#1550]: https://github.com/pgbouncer/pgbouncer/pull/1550
[#1555]: https://github.com/pgbouncer/pgbouncer/pull/1555
[#1568]: https://github.com/pgbouncer/pgbouncer/pull/1568
[#1569]: https://github.com/pgbouncer/pgbouncer/pull/1569
[#1571]: https://github.com/pgbouncer/pgbouncer/pull/1571
[#1573]: https://github.com/pgbouncer/pgbouncer/pull/1573
[#1576]: https://github.com/pgbouncer/pgbouncer/pull/1576
[#1577]: https://github.com/pgbouncer/pgbouncer/pull/1577
[#1580]: https://github.com/pgbouncer/pgbouncer/pull/1580
[#1581]: https://github.com/pgbouncer/pgbouncer/pull/1581
[#1585]: https://github.com/pgbouncer/pgbouncer/pull/1585
[#1597]: https://github.com/pgbouncer/pgbouncer/pull/1597
[#1602]: https://github.com/pgbouncer/pgbouncer/pull/1602
[#1607]: https://github.com/pgbouncer/pgbouncer/pull/1607
[#1609]: https://github.com/pgbouncer/pgbouncer/pull/1609
[#1612]: https://github.com/pgbouncer/pgbouncer/pull/1612

--------

## PgBouncer 1.25.x {#pgbouncer-125x}

**2026-05-08  -  PgBouncer 1.25.2  -  „Eine menschliche Note und eine neue Wendung im Titelrennen voller Ungewissheiten“**

- Sicherheit
  * CVE-2026-6664 behoben: Ein Ganzzahlüberlauf beim Parsen von Netzwerkpaketen in PgBouncer vor 1.25.2 umgeht eine Bereichsprüfung und kann zu einem Absturz führen. Ein nicht authentifizierter Angreifer kann PgBouncer aus der Ferne mit einem fehlerhaften SCRAM-Authentifizierungspaket zum Absturz bringen.
  * CVE-2026-6665 behoben: Der SCRAM-Code in PgBouncer vor 1.25.2 prüfte beim Erstellen des Inhalts der SCRAM-Nachricht client-final-message den Rückgabewert von `strlcat()` nicht korrekt. Ein böswilliges Backend, das eine SCRAM-Nachricht server-final-message mit einer langen Nonce sendet, kann einen Stack-Überlauf auslösen.
  * CVE-2026-6666 behoben: Eine mögliche Nullzeigerreferenz in PgBouncer vor 1.25.2 konnte zu einem Absturz führen, wenn ein Server eine Fehlerantwort ohne SQLSTATE-Feld sendet.
  * CVE-2026-6667 behoben: PgBouncer vor 1.25.2 führte für den Verwaltungsbefehl `KILL_CLIENT` keine angemessene Berechtigungsprüfung durch. Alle Benutzer mit Zugriff auf die Verwaltungskonsole, der selbst eine Berechtigung erfordert, konnten diesen Befehl ausführen. Er sollte nur Benutzern erlaubt sein, die im Parameter `admin_users` aufgeführt sind.

- Fehlerbehebungen
  * Die Dokumentation des Parameters `default_pool_size` präzisiert.
  * Die Dokumentation zu `client_tls13_ciphers` und `server_tls13_ciphers` korrigiert.

**2025-12-03  -  PgBouncer 1.25.1  -  „Vor Weihnachten noch etliche Fehler beheben“**

- Sicherheit
  * CVE-2025-12819 behoben: Vor dieser Version konnte ein nicht authentifizierter Angreifer während der Authentifizierung beliebiges SQL ausführen, indem er in der StartupMessage einen bösartigen search_path-Parameter übergab. Systeme, bei denen ALLE folgenden Konfigurationen vorliegen, sind betroffen:

    1. `track_extra_parameters` enthält search_path (keine Standardkonfiguration; vermutlich nur bei Konfigurationen mit Citus oder PostgreSQL 18 eingestellt)
    2. `auth_user` ist auf eine nicht leere Zeichenkette gesetzt (keine Standardkonfiguration)
    3. `auth_query` ist ohne vollständig qualifizierte Objektnamen konfiguriert (Standardkonfiguration; der Operator < ist nicht mit einem Schema qualifiziert)

- Fehlerbehebungen
    - Fehler bei der Ad-hoc-SCRAM-Authentifizierung nach erneutem Verbindungsaufbau zum Server behoben ([#1432], in 1.25.0 eingeführt)
    - Fehlende Typdefinitionen für ungewöhnliche Architekturen ohne SIMD-Unterstützung hinzugefügt ([#1414], in 1.25.0 eingeführt)
    - Störende Warnmeldung entfernt, wenn der Client die Verbindung schließt, bevor er Daten sendet ([#1420], in 1.25.0 eingeführt)
    - Eine mögliche Dereferenzierung eines NULL-Zeigers verhindert ([#1423], in 1.25.0 eingeführt)
    - Ein mögliches Speicherleck behoben ([#1422], in 1.25.0 eingeführt)
    - Das Parsen von SCRAM-Servernachrichten korrigiert ([#1431], in 1.25.0 eingeführt)

[#1414]: https://github.com/pgbouncer/pgbouncer/pull/1414
[#1420]: https://github.com/pgbouncer/pgbouncer/pull/1420
[#1422]: https://github.com/pgbouncer/pgbouncer/pull/1422
[#1423]: https://github.com/pgbouncer/pgbouncer/pull/1423
[#1431]: https://github.com/pgbouncer/pgbouncer/pull/1431
[#1432]: https://github.com/pgbouncer/pgbouncer/pull/1432

**2025-11-09  -  PgBouncer 1.25.0  -  „Die Version mit LDAP-Unterstützung“**

- Funktionen
    * LDAP-Authentifizierung hinzugefügt! Sie lässt sich über eine HBA-Datei oder `auth_ldap_options` konfigurieren. ([#731])
    * Unterstützung für direkte TLS-Verbindungen auf der Clientseite hinzugefügt. Dadurch können Clients den schnelleren TLS-Verbindungsaufbau verwenden, der in PostgreSQL 17 eingeführt wurde. PgBouncer kann sich mit diesem schnelleren Verfahren (noch) nicht mit PostgreSQL-Servern verbinden. ([#1359])
    * Den Zustand idle zu `SHOW CLIENTS` hinzugefügt. ([#1191])
    * Die Einstellung `transaction_timeout` hinzugefügt, sowohl global als auch auf Benutzerebene. ([#1242])
    * Eine NOTICE-Nachricht wird an einen Client gesendet, wenn er länger als 5 Sekunden in der Warteschlange steht, ohne eine Verbindung zu erhalten. Mit `query_wait_notify` lässt sich diese Dauer ändern oder die Benachrichtigung deaktivieren. ([#1264])
    * Die Einstellung `scram_iterations` hinzugefügt, damit Betreiber zwischen Sicherheit und Authentifizierungsgeschwindigkeit abwägen können ([#1339])
    * `client_tls13_ciphers` und `server_tls13_ciphers` zur Auswahl der zu aktivierenden TLSv1.3-Cipher-Suites hinzugefügt. ([#1352])
- Änderungen
    * Die Leistung der Ad-hoc-SCRAM-Authentifizierung erheblich verbessert. ([#1338])
    * `KILL` kann ohne Angabe einer Datenbank ausgeführt werden. Dies bedeutet jetzt, dass `KILL` für alle Datenbanken ausgeführt wird. ([#1317])
    * Die Health-Check-Abfrage sendet standardmäßig eine leere Abfrage statt `SELECT 1`. ([#1233])
    * Die vollständige PAM-Warteschlange wird als Warnung protokolliert. Dadurch lässt sich die Ursache der hierdurch verlangsamten Abfragen leichter ermitteln. ([#1297])
    * Der Befehl `RELOAD` meldet jetzt alle beim Neuladen aufgetretenen Fehler. ([#1231])
    * Während des Herunterfahrens bleibt der PgBouncer-Unix-Socket für Verwaltungsverbindungen zugänglich. So können Betreiber leichter ermitteln, warum ein PgBouncer-Prozess nicht herunterfährt, und/oder für festhängende Verbindungen manuell `KILL_CLIENT` ausführen. ([#1305])
    * `mkauth.py` so geändert, dass kein veraltetes drittes Feld mehr hinzugefügt wird ([#1365])
    * Die `FATAL`-Meldungen in den Funktionen `disconnect_client` und `disconnect_server` verbessert. ([#1382])
    * Die veraltete OpenSSL-Funktion `EVP_PKEY_get0_EC_KEY` wird nicht mehr verwendet. Sie konnte bei bestimmten FIPS-Implementierungen Probleme verursachen. ([#1384])
- Fehlerbehebungen
    * Einen Absturz bei langen Passwörtern (1024 Zeichen oder mehr) behoben. ([#1215])
    * Verbindungen mit mehreren Hosts bei Verwendung von `server_tls_sslmode=verify-full` korrigiert. ([#1303])
    * Einen seltenen `FATAL`-Fehler beim Weiterleiten von Abbruchanfragen behoben. ([#1383])
    * Die Sortierung der Parameter in `SHOW CONFIG` korrigiert. ([#1403])
    * Das Parsen des Startpakets robuster gemacht. ([#1407])

[#731]: https://github.com/pgbouncer/pgbouncer/pull/731
[#1191]: https://github.com/pgbouncer/pgbouncer/pull/1191
[#1215]: https://github.com/pgbouncer/pgbouncer/pull/1215
[#1231]: https://github.com/pgbouncer/pgbouncer/pull/1231
[#1233]: https://github.com/pgbouncer/pgbouncer/pull/1233
[#1242]: https://github.com/pgbouncer/pgbouncer/pull/1242
[#1264]: https://github.com/pgbouncer/pgbouncer/pull/1264
[#1297]: https://github.com/pgbouncer/pgbouncer/pull/1297
[#1303]: https://github.com/pgbouncer/pgbouncer/pull/1303
[#1305]: https://github.com/pgbouncer/pgbouncer/pull/1305
[#1317]: https://github.com/pgbouncer/pgbouncer/pull/1317
[#1338]: https://github.com/pgbouncer/pgbouncer/pull/1338
[#1339]: https://github.com/pgbouncer/pgbouncer/pull/1339
[#1352]: https://github.com/pgbouncer/pgbouncer/pull/1352
[#1359]: https://github.com/pgbouncer/pgbouncer/pull/1359
[#1365]: https://github.com/pgbouncer/pgbouncer/pull/1365
[#1382]: https://github.com/pgbouncer/pgbouncer/pull/1382
[#1383]: https://github.com/pgbouncer/pgbouncer/pull/1383
[#1384]: https://github.com/pgbouncer/pgbouncer/pull/1384
[#1403]: https://github.com/pgbouncer/pgbouncer/pull/1403
[#1407]: https://github.com/pgbouncer/pgbouncer/pull/1407

--------

## PgBouncer 1.24.x {#pgbouncer-124x}

**2025-04-16  -  PgBouncer 1.24.1  -  „CVE-2025-2291 VALID UNTIL gestern“**

- Sicherheit
  * CVE-2025-2291 behoben: Bisher berücksichtigte PgBouncer beim Abrufen von Passwort-Hashes mit auth_query nicht den Wert VALID
    UNTIL eines Benutzerpassworts. Wurde PgBouncer als transparenter Proxy vor
    Postgres eingesetzt, konnte es daher bereits abgelaufene Passwörter akzeptieren.
    Zur Behebung wurden die standardmäßige auth_query und die Beispiele für
    benutzerdefinierte auth_query-Funktionen in der Dokumentation so geändert,
    dass sie VALID UNTIL berücksichtigen. Wenn Sie eine benutzerdefinierte
    auth_query verwenden, sollten Sie diese entsprechend aktualisieren. Bei Verwendung
    der standardmäßigen auth_query können Sie entweder auf PgBouncer 1.24.1 aktualisieren
    oder die Konfiguration einer älteren PgBouncer-Version so ändern, dass sie
    die neue standardmäßige auth_query verwendet.

- Fehlerbehebungen
  * Die PAM-Unterstützung repariert, indem die Unterstützung für `pam`-Authentifizierung in HBA-Dateien zurückgenommen wurde. ([#1291]) (Fehler in 1.24.0 eingeführt)
  * Einen Fehler beim Verringern des Zählers für Benutzerverbindungen behoben. Diese Korrektur war im Tag 1.24.0 auf GitHub enthalten, fehlte aber im Release-Tarball. ([#1238]) (Fehler in 1.24.0 eingeführt)
  * `test_load_balance_hosts.py` zum Tarball hinzugefügt. ([#1282])
  * Probleme in Tests behoben, damit Debian-Paketbetreuer sie ausführen können. ([#1266], [#1250])

- Dokumentation
  * Das Beispiel für `auth_query` aktualisiert, sodass es einen sicheren `search_path` setzt. ([#1245])

[#1238]: https://github.com/pgbouncer/pgbouncer/pull/1238
[#1291]: https://github.com/pgbouncer/pgbouncer/pull/1291
[#1282]: https://github.com/pgbouncer/pgbouncer/pull/1282
[#1266]: https://github.com/pgbouncer/pgbouncer/pull/1266
[#1250]: https://github.com/pgbouncer/pgbouncer/pull/1250
[#1245]: https://github.com/pgbouncer/pgbouncer/pull/1245

**2025-01-10  -  PgBouncer 1.24.0  -  „Neues Jahr, neuer Türsteher“**

- Funktionen
  * Unterstützung für `Type=notify-reload` für systemd hinzugefügt. Dies erfordert systemd
    ab Version 253. ([#1148])
  * Den Befehl `KILL_CLIENT` zur Verwaltungskonsole hinzugefügt. Damit lässt sich eine
    Clientverbindung zwangsweise beenden. ([#1147])
  * Die Einstellung `max_user_client_connections` hinzugefügt, sowohl global als auch auf Benutzerebene. ([#1137])
  * Die Einstellung `max_db_client_connections` hinzugefügt, sowohl global als auch auf Datenbankebene. ([#1138])
  * Den Zähler `current_client_connections` zur Ausgabe von `SHOW USERS` und `SHOW DATABASES` hinzugefügt. ([#1137], [#1138])
  * Den Parameter `load_balance_hosts` hinzugefügt, mit dem sich festlegen lässt, dass **keine** Lastverteilung zwischen Hosts erfolgt. ([#736])
  * Nutzungszähler für vorbereitete Anweisungen in `SHOW STATS` verfügbar gemacht. ([#1192])
  * Die Einstellung `client_idle_timeout` hinzugefügt. ([#1189])
  * `query_timeout` und `reserve_pool_size` auf Benutzerebene hinzugefügt. ([#1180], [#1228])
  * Unterstützung für `pam`-Authentifizierung in HBA-Dateien aktiviert. ([#326])

- Änderungen
  * Verbindungen werden bei RELOAD nicht erneuert, wenn die TLS-Konfiguration unverändert ist.
    Bisher wurden bei RELOAD alle vorhandenen TLS-Verbindungen erneuert, was zu einem
    vorübergehenden, aber erheblichen Leistungseinbruch führen konnte. Dies geschieht jetzt
    nur noch, wenn sich die TLS-Einstellungen tatsächlich ändern. ([#1157])
  * Die Unterstützung vorbereiteter Anweisungen ist standardmäßig aktiviert;
    `max_prepared_statements` ist jetzt standardmäßig auf 200 gesetzt. Diese Änderung
    der Standardwerte sollte nur Clients betreffen, die tatsächlich vorbereitete Anweisungen
    verwenden. Wenn Sie vorbereitete Anweisungen verwenden, empfiehlt es sich, die
    Einschränkungen dieser Unterstützung in [unserer Dokumentation][prepared-docs]
    zu lesen. ([#1144])
  * Sockets, Clients und Server lassen sich in der Verwaltungsausgabe jetzt anhand einer
    eindeutigen ID identifizieren. Bisher dienten dazu ihre Zeiger, die nach dem Trennen
    der Verbindung jedoch häufig für neue Clients wiederverwendet wurden. ([#1172])
  * Klarere Fehlermeldung für eine leere PID-Datei. ([#1195])
  * Bei einem Fehlschlag von `server_login_retry` wird der ursprüngliche Fehler an den Client zurückgegeben. ([#1152])
  * Bei einem Fehler in `auth_query` wird der ursprüngliche Serverfehler protokolliert. ([#1187])
  * Der Wert 0 für `default_pool_size` bedeutet unbegrenzte Größe. ([#1227])
  * Die Datenbankeinstellung `reserve_pool` in `reserve_pool_size` umbenannt.
    Der bisherige Name bleibt als Alias für den neuen Namen erhalten.
    ([#1232])

- Fehlerbehebungen
  * Verschiedene unwahrscheinliche Fehlerfälle, etwa OOM-Fehler, werden besser behandelt.
    Sie konnten zuvor Abstürze oder Speicherlecks verursachen. ([#1108], [#1101], [#1099], [#1169], [#1202])
  * Den Standardwert für `server_tls_sslmode` in der Beispielkonfiguration korrigiert. ([#1133])
  * Den Hinweis auf einen ungültigen Alias für `server_tls_protocols` aus der Dokumentation entfernt. ([#1155])
  * Einen Fehler bei gleichzeitiger Verwendung von `auth_query` und Replikationsverbindungen behoben.
    Er führte in solchen Konfigurationen zu Verbindungsfehlern. ([#1166])
  * Abbruchanfragen von Clients werden ignoriert, während PgBouncer Servereinstellungen konfiguriert. ([#298])

[prepared-docs]: /de/docs/pgbouncer/config/#max_prepared_statements

[#1148]: https://github.com/pgbouncer/pgbouncer/pull/1148
[#1147]: https://github.com/pgbouncer/pgbouncer/pull/1147
[#1137]: https://github.com/pgbouncer/pgbouncer/pull/1137
[#1138]: https://github.com/pgbouncer/pgbouncer/pull/1138
[#736]: https://github.com/pgbouncer/pgbouncer/pull/736
[#1192]: https://github.com/pgbouncer/pgbouncer/pull/1192
[#1189]: https://github.com/pgbouncer/pgbouncer/pull/1189
[#1180]: https://github.com/pgbouncer/pgbouncer/pull/1180
[#1228]: https://github.com/pgbouncer/pgbouncer/pull/1228
[#326]: https://github.com/pgbouncer/pgbouncer/pull/326
[#1157]: https://github.com/pgbouncer/pgbouncer/pull/1157
[#1144]: https://github.com/pgbouncer/pgbouncer/pull/1144
[#1172]: https://github.com/pgbouncer/pgbouncer/pull/1172
[#1195]: https://github.com/pgbouncer/pgbouncer/pull/1195
[#1152]: https://github.com/pgbouncer/pgbouncer/pull/1152
[#1187]: https://github.com/pgbouncer/pgbouncer/pull/1187
[#1227]: https://github.com/pgbouncer/pgbouncer/pull/1227
[#1232]: https://github.com/pgbouncer/pgbouncer/pull/1232
[#1108]: https://github.com/pgbouncer/pgbouncer/pull/1108
[#1101]: https://github.com/pgbouncer/pgbouncer/pull/1101
[#1099]: https://github.com/pgbouncer/pgbouncer/pull/1099
[#1169]: https://github.com/pgbouncer/pgbouncer/pull/1169
[#1202]: https://github.com/pgbouncer/pgbouncer/pull/1202
[#1133]: https://github.com/pgbouncer/pgbouncer/pull/1133
[#1155]: https://github.com/pgbouncer/pgbouncer/pull/1155
[#1166]: https://github.com/pgbouncer/pgbouncer/pull/1166
[#298]: https://github.com/pgbouncer/pgbouncer/pull/298

--------

## PgBouncer 1.23.x {#pgbouncer-123x}

**2024-08-02  -  PgBouncer 1.23.1  -  „Alles wieder in Ordnung“**

- Fehlerbehebungen
  * Einen möglichen Speicherzugriffsfehler nach dem Neuladen der PgBouncer-Konfiguration
    behoben. ([#1105]) (Fehler in 1.23.0 eingeführt)
  * Alle bekannten Abstürze in put_in_order behoben. ([#1120])
    (neue Abstürze wurden in 1.23.0 eingeführt)
  * Fehlende, für Tests benötigte Dateien zum Release-Tarball hinzugefügt.
    ([#1124]) (die Dateien fehlten seit 1.23.0)

[#1120]: https://github.com/pgbouncer/pgbouncer/pull/1120
[#1105]: https://github.com/pgbouncer/pgbouncer/pull/1105
[#1124]: https://github.com/pgbouncer/pgbouncer/pull/1124

**2024-07-03  -  PgBouncer 1.23.0  -  „Auf zu neuen Anfängen“**

- Funktionen
  * Unterstützung für rollierende Neustarts hinzugefügt. SIGTERM fährt den PgBouncer-Prozess
    nicht mehr sofort herunter. Stattdessen erfolgt jetzt ein „besonders sicheres Herunterfahren“:
    Vor dem Herunterfahren wird gewartet, bis alle Clients ihre Verbindung getrennt haben.
    Das neue SIGTERM-Verhalten ermöglicht rollierende Neustarts mehrerer PgBouncer-Prozesse
    hinter einem Load-Balancer oder mehrerer Prozesse, die mit `so_reuseport` am selben Port lauschen.
    Dies ist eine **kleine inkompatible Änderung**. Wenn Sie sich in Ihrer Dockerfile- oder
    Systemd-Service-Datei auf das bisherige SIGTERM-Verhalten verlassen haben, sollten Sie jetzt SIGQUIT verwenden.
    ([#902])
  * Unterstützung für Benutzernamenzuordnungen bei den Authentifizierungsmethoden `cert` und `peer`
    hinzugefügt. Diese Funktion bietet die Flexibilität, dass der die Verbindung aufbauende
    Benutzer nicht dem Datenbankbenutzer entsprechen muss. Benutzernamenzuordnungen in PgBouncer
    funktionieren sehr ähnlich wie in Postgres, mit den in der Dokumentation aufgeführten Ausnahmen.
    ([#996])
  * Unterstützung für Replikationsverbindungen über PgBouncer hinzugefügt. ([#876])

- Änderungen
  * Die Verbindungsliste in der Ausgabe von `SHOW USERS` verbessert. ([#1040])
  * `pool_size` kann pro Benutzer konfiguriert werden. ([#1049])
  * `server_lifetime` kann pro Datenbank konfiguriert werden. ([#1057])
  * Unterstützung für die Auflistung dynamisch erzeugter Benutzer in der Ausgabe von `SHOW USERS` hinzugefügt. ([#1052])
  * Unterstützung für den Adresstyp `all` in der hba-Konfiguration hinzugefügt. ([#1078])
  * Unterstützung für automatische Neustarts bei Verwendung von systemd hinzugefügt. ([#1080])
  * Die erforderliche Mindestversion von c-ares auf 1.9.0 erhöht ([#1076])

- Fehlerbehebungen
  * Probleme bei der Verarbeitung großer und unvollständiger Startpakete behoben. ([#1058])
  * Unterstützung für das Format `--config=value` im Startparameter options hinzugefügt. ([#1064])
  * Die Berechnung der Metrik `avg_wait_time` korrigiert. ([#727])
  * Unterstützung für das Aushandeln der Postgres-Protokollversion mit dem Client hinzugefügt. ([#1007])
  * Die Erfassung einer ausstehenden Anfrage für `auth_query` hinzugefügt. ([#1034])
  * Mehrere Verbesserungen an Dokumentation und CI.

[#996]: https://github.com/pgbouncer/pgbouncer/pull/996
[#1040]: https://github.com/pgbouncer/pgbouncer/pull/1040
[#1049]: https://github.com/pgbouncer/pgbouncer/pull/1049
[#1057]: https://github.com/pgbouncer/pgbouncer/pull/1057
[#1052]: https://github.com/pgbouncer/pgbouncer/pull/1052
[#1058]: https://github.com/pgbouncer/pgbouncer/pull/1058
[#1007]: https://github.com/pgbouncer/pgbouncer/pull/1007
[#876]: https://github.com/pgbouncer/pgbouncer/pull/876
[#902]: https://github.com/pgbouncer/pgbouncer/pull/902
[#1064]: https://github.com/pgbouncer/pgbouncer/pull/1064
[#1078]: https://github.com/pgbouncer/pgbouncer/pull/1078
[#1080]: https://github.com/pgbouncer/pgbouncer/pull/1080
[#727]: https://github.com/pgbouncer/pgbouncer/pull/727
[#1076]: https://github.com/pgbouncer/pgbouncer/pull/1076
[#1034]: https://github.com/pgbouncer/pgbouncer/pull/1034

--------

## PgBouncer 1.22.x {#pgbouncer-122x}

**2024-03-04  -  PgBouncer 1.22.1  -  „Sommer in Bangalore“**

- Fehlerbehebungen
  * Probleme behoben, die von manchen Clients durch `COPY FROM STDIN`-Abfragen verursacht wurden.
    Solche Abfragen konnten Speicherlecks, Leistungseinbußen und Fehlverhalten bei vorbereiteten
    Anweisungen verursachen. ([#1025])
    (Fehler in 1.21.0 eingeführt)
  * Fehlende Tests zum Release-Tarball hinzugefügt ([#1026])
    (die Tests fehlten seit 1.19.0 & 1.21.0)

[#1025]: https://github.com/pgbouncer/pgbouncer/pull/1025
[#1026]: https://github.com/pgbouncer/pgbouncer/pull/1026

**2024-01-31  -  PgBouncer 1.22.0  -  „DEALLOCATE ALL“**

- Funktionen
  * Unterstützung für `DEALLOCATE ALL` und `DISCARD ALL` hinzugefügt, wenn
    `max_prepared_statements` auf einen Wert ungleich null gesetzt ist (normales `DEALLOCATE`
    wird weiterhin nicht unterstützt) ([#972])
  * `auth_query` kann pro Datenbank konfiguriert werden ([#979])

- Änderungen
  * Die Einstellungen in der empfohlenen systemd-Unit-Datei verbessert ([#983])
  * Die Fail-Fast-Logik behandelt alle Szenarien, in denen keine funktionierenden Verbindungen
    zur Datenbank mehr bestehen und keine hergestellt werden können ([#998])
  * Mehrere Verbesserungen an der Dokumentation

- Fehlerbehebungen
  * Ein Problem in PG14+ behoben, bei dem PgBouncer für jede Transaktion `SET DateStyle='ISO'`
    sendete ([#879])
  * Die Behandlung eines leeren `application_name` korrigiert ([#999])
  * Das Bauen unter Windows mit OpenSSL 3.2.0 korrigiert ([#1009])

[#972]: https://github.com/pgbouncer/pgbouncer/pull/972
[#979]: https://github.com/pgbouncer/pgbouncer/pull/979
[#983]: https://github.com/pgbouncer/pgbouncer/pull/983
[#998]: https://github.com/pgbouncer/pgbouncer/pull/998
[#879]: https://github.com/pgbouncer/pgbouncer/pull/879
[#999]: https://github.com/pgbouncer/pgbouncer/pull/999
[#1009]: https://github.com/pgbouncer/pgbouncer/pull/1009

--------

## PgBouncer 1.21.x {#pgbouncer-121x}

**2023-10-16  -  PgBouncer 1.21.0  -  „Die Version mit vorbereiteten Anweisungen“**

- Funktionen
  * Unterstützung für benannte vorbereitete Anweisungen auf Protokollebene hinzugefügt!
    Dies ist vermutlich eine der am häufigsten gewünschten PgBouncer-Funktionen.
    Vorbereitete Anweisungen zusammen mit PgBouncer können die CPU-Last des Systems
    erheblich senken, sowohl auf der PgBouncer- als auch auf der PostgreSQL-Seite.
    In synthetischen Benchmarks erhöhte diese Funktion den Abfragedurchsatz je nach
    Arbeitslast um 15% bis 250%. Um die neue Funktion zu nutzen, müssen Sie die neue
    Einstellung `max_prepared_statements` auf einen Wert ungleich null setzen.
    Der genaue Wert hängt von der Arbeitslast ab, aber 100 dürfte angemessen sein.
    Einzelheiten zu Funktionsweise, Einschränkungen und Optimierung des Werts enthält
    [die Dokumentation zu
    `max_prepared_statements`](/de/docs/pgbouncer/config/#max_prepared_statements).
    Anschließend müssen Sie sicherstellen, dass Ihre Clientbibliothek tatsächlich
    vorbereitete Anweisungen verwendet. Wie dies geschieht, unterscheidet sich je nach Client;
    Sie sollten daher die Dokumentation des verwendeten Clients heranziehen. Die Funktion
    wurde vor der Veröffentlichung sehr gründlich getestet. Aufgrund ihrer Komplexität
    können jedoch durchaus noch Leistungsprobleme oder Fehler vorhanden sein.
    Bitte melden Sie solche Probleme, wenn Sie sie entdecken. ([#845])

- Änderungen
  * Die Sicherheit der OpenSSL-Einstellungen verbessert; die verwendeten Standardwerte waren SEHR veraltet.
    Ab dieser Version entsprechen die Standardwerte den OpenSSL-Standardwerten des Systems,
    auf dem PgBouncer läuft. ([#948] & [libusual/#41])
  * PgBouncer verwendet jetzt nach Möglichkeit OpenSSL zur Berechnung von MD5-Hashes.
    Dies ist für einen FIPS-konformen Einsatz von PgBouncer erforderlich. ([#949])
  * `min_pool_size` wird bei Pools mit einem erzwungenen Benutzer auch dann eingehalten,
    wenn keine Clients mit PgBouncer verbunden sind ([#947])
  * Die Kodierung von `peer_id` im Abbruch-Token durch PgBouncer wurde geändert.
    Deshalb funktioniert das Peering zwischen unterschiedlichen PgBouncer-Versionen nicht,
    wenn sie nicht alle auf derselben Seite der Versionsgrenze v1.21.0 liegen.
    ([#945])

- Fehlerbehebungen
  * Den Absturz mit der Fehlermeldung "FATAL in function client\_proto(): bad
    client state: 6/7" behoben ([#928]) (Fehler in 1.18.0 eingeführt)
  * Den Absturz mit der Fehlermeldung "FATAL in function server\_proto(): server in
    bad state: 11" behoben ([#927]) (Fehler in 1.18.0 eingeführt)
  * Die Protokollierungsstufe für das Senden von Abbruchanfragen verringert ([#903])
  * Das slog-Protokollpräfix für Peers korrigiert ([#922])
  * Tippfehler in der Dokumentation korrigiert ([#932])
  * Von der statischen Analyse erkannte Fehler behoben ([#943])
  * Bei vorübergehenden FATAL-Fehlern während der Anmeldung werden nicht alle wartenden Clients beendet ([#946])
  * Eine automatisch erzeugte Datenbank wird verwendet, wenn die Datenbank in `auth_dbname` nicht explizit konfiguriert ist
    ([#921])

- Bereinigungen
  * Die Unterstützung für udns entfernt ([#938])

[#845]: https://github.com/pgbouncer/pgbouncer/pull/845
[#948]: https://github.com/pgbouncer/pgbouncer/pull/948
[#949]: https://github.com/pgbouncer/pgbouncer/pull/949
[#947]: https://github.com/pgbouncer/pgbouncer/pull/947
[#945]: https://github.com/pgbouncer/pgbouncer/pull/945
[#903]: https://github.com/pgbouncer/pgbouncer/pull/903
[#922]: https://github.com/pgbouncer/pgbouncer/pull/922
[#932]: https://github.com/pgbouncer/pgbouncer/pull/932
[#928]: https://github.com/pgbouncer/pgbouncer/pull/928
[#927]: https://github.com/pgbouncer/pgbouncer/pull/927
[#943]: https://github.com/pgbouncer/pgbouncer/pull/943
[#946]: https://github.com/pgbouncer/pgbouncer/pull/946
[#921]: https://github.com/pgbouncer/pgbouncer/pull/921
[#938]: https://github.com/pgbouncer/pgbouncer/pull/938
[libusual/#41]: https://github.com/libusual/libusual/pull/41

--------

## PgBouncer 1.20.x {#pgbouncer-120x}

**2023-08-09  -  PgBouncer 1.20.1  -  „Optionale Optionen“**

- Fehlerbehebungen
  * Eine Regression behoben, bei der das Eintragen von `options` in `ignore_startup_parameters`
    nicht mehr dazu führte, dass unbekannte Parameter im Startparameter `options` ignoriert wurden.
    ([#908]) (Regression in 1.20.0 eingeführt)
  * Einen verwirrenden Tippfehler in der Dokumentation korrigiert ([#917])

[#908]: https://github.com/pgbouncer/pgbouncer/pull/908
[#917]: https://github.com/pgbouncer/pgbouncer/pull/917

**2023-07-20  -  PgBouncer 1.20.0  -  „Hier gehört ein lustiger Name hin“**

- Abkündigungen
  * Die Option für Online-Neustarts gilt jetzt als veraltet. Diese Funktion wurde in den letzten
    Jahren kaum gepflegt. Sie hat mehrere bekannte Probleme, und neu hinzugefügte Funktionen
    unterstützen sie häufig nicht. Heute wird für Online-Neustarts die Verwendung der Funktionen
    `so_reuseport` und `peers` empfohlen. Damit können mehrere unterschiedliche PgBouncer-Prozesse
    am selben Port laufen. Indem Sie diese Prozesse nacheinander neu starten, können Sie
    sicherstellen, dass immer ein PgBouncer-Prozess am gewünschten Port lauscht. ([#894])

- Funktionen
  * `track_extra_parameters` eingeführt, um im Transaktions-Pooling-Modus weitere Parameter
    nachverfolgen zu können. Bisher verfolgte PgBouncer nur `application_name`, `DateStyle`,
    `TimeZone` und `standard_conforming_strings`. Jetzt wird auch `IntervalStyle` standardmäßig
    nachverfolgt. Durch Ändern von `track_extra_parameters` lassen sich weitere Einstellungen
    nachverfolgen, jedoch nur [solche, die PostgreSQL an den Client zurückmeldet][guc_report].
    Bei Verwendung von Citus 12.0+ sorgt Citus dafür, dass PostgreSQL auch `search_path` an den
    Client zurückmeldet. Wenn Sie Citus verwenden, können Sie deshalb `search_path` zur
    Einstellung `track_extra_parameters` hinzufügen.
    ([#867])
  * SQLSTATE wird während der Authentifizierung weitergeleitet. Dadurch lässt sich erkennen,
    ob eine Datenbank nicht existiert, wie es Npgsql (ein .NET-Datenprovider für PostgreSQL)
    tut. ([#814])
  * Den Standardwert von `server_tls_sslmode` auf `prefer` geändert. ([#866])
  * Unterstützung für den Startparameter `options` hinzugefügt. Dies ermöglicht die Verwendung
    [der Umgebungsvariable `PGOPTIONS`, die `psql` und `libpq` unterstützen][pgoptions].
    Mit dieser Variable lassen sich beliebige PostgreSQL-Parameter beim Start setzen.
    Dies funktioniert nur für PostgreSQL-Parameter, die PgBouncer über
    `track_extra_parameters` nachverfolgt. ([#878])

- Fehlerbehebungen
  * Kein Absturz mehr, wenn die Verwaltungsdatenbank `pgbouncer` als auth_dbname verwendet wird.
    Dies wird weiterhin nicht unterstützt, führt jetzt aber zu einer klaren Fehlermeldung statt zu einem Absturz.
    ([#817])
  * Den Namen von `peer_cache` in `SHOW MEM` korrigiert. Bisher wurde er fälschlich als
    `db_cache` angezeigt. ([#864])
  * Die Verwechslung von src/dst im Protokoll korrigiert. PgBouncer protokollierte eine Quell-IP,
    obwohl die Ziel-IP gemeint war. ([#880])
  * Verwaltungsverbindungen über Unix-Sockets werden nur protokolliert, wenn `log_connections`
    auf `1` gesetzt ist. ([#883])

[guc_report]: https://www.postgresql.org/docs/15/protocol-flow.html#PROTOCOL-ASYNC
[pgoptions]: https://www.postgresql.org/docs/current/config-setting.html#id-1.6.7.4.5
[#867]: https://github.com/pgbouncer/pgbouncer/pull/867
[#814]: https://github.com/pgbouncer/pgbouncer/pull/814
[#866]: https://github.com/pgbouncer/pgbouncer/pull/866
[#878]: https://github.com/pgbouncer/pgbouncer/pull/878
[#817]: https://github.com/pgbouncer/pgbouncer/pull/817
[#864]: https://github.com/pgbouncer/pgbouncer/pull/864
[#880]: https://github.com/pgbouncer/pgbouncer/pull/880
[#883]: https://github.com/pgbouncer/pgbouncer/pull/883
[#894]: https://github.com/pgbouncer/pgbouncer/pull/894

--------

## PgBouncer 1.19.x {#pgbouncer-119x}

**2023-05-31  -  PgBouncer 1.19.1  -  „Sonniger Frühling“**

Dies ist eine Wartungsversion, die einige kürzlich eingeführte Fehler behebt:

- Fehlerbehebungen
  * Behoben: FATAL in function disconnect_client(): bad client state: 0 ([#846])
    (Fehler in 1.18.0 eingeführt)
  * Behoben: FATAL in function server_proto(): server in bad state: 14 ([#849])
    (Fehler in 1.18.0 eingeführt)
  * Für die Ausführung der Python-Tests erforderliche Dateien zum Release-Tarball hinzugefügt ([#852])
    (neue Tests in 1.19.0 eingeführt)

[#846]: https://github.com/pgbouncer/pgbouncer/pull/846
[#849]: https://github.com/pgbouncer/pgbouncer/pull/849
[#852]: https://github.com/pgbouncer/pgbouncer/pull/852

**2023-05-04  -  PgBouncer 1.19.0  -  „Auf die altmodische Art, von Menschen gemacht“**

- Funktionen
  * Die Option `auth_dbname` hinzugefügt. Sie legt fest, in welcher Datenbank
    `auth_query` ausgeführt wird. ([#764])
  * Den Befehl `SHOW STATE` hinzugefügt. Er zeigt an, ob PgBouncer aktiv,
    pausiert oder angehalten ist. ([#528])
  * Unterstützung für Peering zwischen PgBouncer-Prozessen hinzugefügt. Damit lässt sich
    PgBouncer so konfigurieren, dass Abbruchanfragen auch dann weiter funktionieren,
    wenn sich mehrere unterschiedliche PgBouncer-Prozesse hinter einem einzigen
    Load-Balancer befinden. ([#666])
  * Eine eigene Einstellung `cancel_wait_timeout` hinzugefügt. Sie bestimmt,
    nach welcher Zeit das Weiterleiten einer Abbruchanfrage aufgegeben wird.
    Der Standardwert beträgt 10 Sekunden. ([#833])
  * Neues Testframework ([#792])

- Fehlerbehebungen
  * Ein mögliches Speicherleck bei fehlgeschlagenem TLS-Handshake behoben. ([#796])
  * Genauere Fehlermeldungen für nicht unterstützte Befehlszeilenoptionen unter Windows.
    ([#620])
  * Den Aufruf von `disconnect_server` für einen Server im Zustand `BEING_CANCELED`
    korrigiert. ([#815]) (in 1.18.0 eingeführt)
  * Beim Empfang von `SIGTERM` wird PgBouncer nicht mit einem Status ungleich null beendet.
    ([#834])
  * Der Start wird mit einem Fehler abgebrochen, wenn ein Socket in `unix_socket_dir`
    nicht erstellt werden konnte. ([#830])
  * Der Start wird mit einem Fehler abgebrochen, wenn an keiner der Adressen in
    `listen_addr` gelauscht werden konnte. ([#838])
  * Beim Fehlschlagen von `sbuf_connect` werden mehr Warnungen mit zusätzlichen Informationen
    ausgegeben. Dies ist besonders hilfreich, wenn das Erstellen von Unix-Sockets fehlschlägt.
    ([#837])

- Bereinigungen
  * Verschiedene CI-Aktualisierungen für bessere Leistung
  * AppVeyor entfernt

[#528]: https://github.com/pgbouncer/pgbouncer/issues/528
[#620]: https://github.com/pgbouncer/pgbouncer/pull/620
[#666]: https://github.com/pgbouncer/pgbouncer/pull/666
[#764]: https://github.com/pgbouncer/pgbouncer/pull/764
[#792]: https://github.com/pgbouncer/pgbouncer/pull/792
[#796]: https://github.com/pgbouncer/pgbouncer/pull/796
[#815]: https://github.com/pgbouncer/pgbouncer/pull/815
[#830]: https://github.com/pgbouncer/pgbouncer/pull/830
[#833]: https://github.com/pgbouncer/pgbouncer/pull/833
[#834]: https://github.com/pgbouncer/pgbouncer/pull/834
[#837]: https://github.com/pgbouncer/pgbouncer/pull/837
[#838]: https://github.com/pgbouncer/pgbouncer/pull/838

--------

## PgBouncer 1.18.x {#pgbouncer-118x}

**2022-12-12  -  PgBouncer 1.18.0  -  „Kein echtes Rätsel“**

- Funktionen
  * `application_name` zur Ausgabe von `SHOW CLIENTS`/`SERVERS`/`SOCKETS`
    hinzugefügt ([#449](https://github.com/pgbouncer/pgbouncer/pull/449))
  * Informationen über Abbruchanfragen zur Ausgabe von `SHOW CLIENTS`/`SERVERS`/`POOLS` hinzugefügt
    ([#782](https://github.com/pgbouncer/pgbouncer/pull/782))

- Fehlerbehebungen
  * Die Operation `sbuf_send_pending` schlägt fehl, wenn der Ziel-Socket geschlossen ist
    ([#652](https://github.com/pgbouncer/pgbouncer/pull/652))
  * Einige mögliche Abstürze behoben
    ([#700](https://github.com/pgbouncer/pgbouncer/pull/700),
    [#730](https://github.com/pgbouncer/pgbouncer/pull/730))
  * Einen Überlauffehler bei der Funktion für kommagetrennte Hostlisten behoben,
    der die Verbindung auf einen Unix-Socket umleitete
    ([#747](https://github.com/pgbouncer/pgbouncer/pull/747))
  * Verbindungen werden nicht verdrängt, um `min_pool_size` zu erreichen
    ([#648](https://github.com/pgbouncer/pgbouncer/pull/648))
  * `SHOW HELP` mit PostgreSQL 15 korrigiert
    ([#769](https://github.com/pgbouncer/pgbouncer/issues/769))
  * Eine Race Condition bei der Verarbeitung von Abbruchanfragen für Abfragen behoben.
    Eine Abbruchanfrage für einen Client konnte die Abfrage eines anderen Clients abbrechen.
    Dies konnte geschehen, wenn PgBouncer die Abbruchanfrage erst erhielt, nachdem
    die eigentlich abzubrechende Abfrage bereits von selbst abgeschlossen war.
    ([#717](https://github.com/pgbouncer/pgbouncer/pull/717))

- Bereinigungen
  * Verschiedene CI-Aktualisierungen

--------

## PgBouncer 1.17.x {#pgbouncer-117x}

**2022-03-23  -  PgBouncer 1.17.0  -  „Eine Grenze wurde gezogen“**

- Funktionen
  * Eine Datenbankdefinition kann eine kommagetrennte Hostliste angeben.
    Die Verbindungen zu den Hosts werden im Round-Robin-Verfahren hergestellt.
  * Beim Verbinden mit einer nicht existierenden Datenbank wird der Fehler ("no such
    database") jetzt erst nach der Authentifizierung gemeldet. Dies verhindert,
    dass nicht authentifizierte Clients auskundschaften können, welche Datenbanken existieren.
    (Dies ähnelt der Änderung in Version 1.15.0, fehlende Benutzer erst nach der
    Authentifizierung zu melden.)
  * Fehler beim Trennen einer Serververbindung werden vor der Anmeldung nicht an den Client gesendet.
    Sie könnten einem noch nicht angemeldeten Client Informationen offenlegen, die nicht
    uneingeschränkt öffentlich sind, etwa Konfigurationsdetails.
  * Die maximale Passwortlänge erneut erhöht. Offenbar reichte die letzte Erhöhung
    nicht lange genug aus.
  * Das automatische Neuladen von `auth_file` entfernt. `auth_file` wird jetzt nur noch
    beim Neuladen der Konfigurationsdatei erneut gelesen, nicht mehr automatisch bei jeder Änderung.
  * Der Windows-Build enthält jetzt eine Ressourcendatei mit Versionsinformationen.
  * Die in der CI erstellten Windows-Builds sind jetzt statisch gelinkt und können daher
    ohne weitere Abhängigkeiten direkt verwendet werden.

- Fehlerbehebungen
  * Die Unterstützung für OpenSSL 3 korrigiert. Frühere Versionen stürzten ab.
  * Die Fail-Fast-Logik wird beim Verbindungsaufbau nicht angewendet. Dies ist Teil der oben
    genannten Änderung, Serverfehler nicht vor der Authentifizierung zu melden. Es behebt
    außerdem einen besonderen Fall bei der SCRAM-Durchleitung: Der clientseitige
    Authentifizierungsaustausch muss zugelassen werden, damit die serverseitige Verbindung
    durch erneute Authentifizierung repariert werden kann. Der Fail-Fast-Mechanismus greift
    weiterhin unmittelbar nach der Authentifizierung, sodass das tatsächlich beobachtete
    Verhalten in den meisten Fällen gleich bleibt.
  * `auth_type` in der Beispielkonfiguration `pgbouncer.ini` auf `md5` geändert, entsprechend
    dem eingebauten Standardwert. Manche setzen diese Datei als Standardkonfiguration ein;
    prüfen Sie daher, ob die geänderte Konfiguration für Ihren Einsatz weiterhin sinnvoll ist.
  * Einen Absturz beim Beenden von Builds mit aktivierten Assertions behoben.
  * Dokumentation und Verhalten von `tcp_defer_accept` verbessert. Die Angaben zum Standardwert
    waren falsch und irreführend. In manchen Fällen zeigte "show config" den falschen Wert.
    Ist die Option gesetzt, wird aber nicht unterstützt, wird jetzt außerdem ein Fehler
    ausgegeben, statt sie zu ignorieren; dies entspricht der Behandlung anderer
    plattformspezifischer Socket-Optionen.
  * Den Build mit c-ares unter Windows korrigiert. Unter Windows ist jetzt c-ares >=1.18.0 erforderlich.

- Bereinigungen
  * Die meisten Warnungen zu veralteten Funktionen von Autoconf >=2.70 beseitigt.
    Ältere Autoconf-Versionen werden weiterhin unterstützt.
  * Den Einsatz von Cirrus CI auf weitere Plattformen ausgeweitet.
  * Die Unterstützung für Travis CI entfernt.
  * Die Suchorte für die standardmäßige Root-CA-Datei aktualisiert, um weitere Plattformen
    wie Fedora/RHEL/CentOS abzudecken.
  * Alle Python-Skripte verwenden jetzt standardmäßig `python3`.
    Die Kompatibilität mit Python 2 wird nicht mehr gepflegt.
  * Die Skripte der Testsuite verwenden `command -v` statt des veralteten `which`.
  * Mehrere Fehlermeldungen umformuliert, damit deutlicher wird, auf welchen Befehl oder
    welche Konfigurationseinstellung sie sich beziehen.
  * Die Skripte der Testsuite benötigen GNU sed nicht mehr.
  * `make check` funktioniert jetzt unter Windows (die SSL-Testsuite allerdings noch nicht).
  * Dokumentiert, dass die Verwaltungskonsole nur das einfache Abfrageprotokoll unterstützt,
    und diesbezügliche Fehlermeldungen verbessert.

--------

## PgBouncer 1.16.x {#pgbouncer-116x}

**2021-11-11  -  PgBouncer 1.16.1  -  „Tiefgang auf dem Prüfstand gegen stille Effizienz“**

Dies ist eine Wartungsversion mit einer Sicherheitskorrektur.

* PgBouncer weist in seiner Rolle als Server zusätzliche Daten nach einem
  SSL- oder GSS-Verschlüsselungs-Handshake zurück.

  Ein Man-in-the-Middle-Angreifer, der Daten in die TCP-Verbindung einschleusen kann,
  konnte Klartextdaten am Anfang einer vermeintlich durch Verschlüsselung geschützten
  Datenbanksitzung platzieren. Dies ließ sich zum Senden gefälschter SQL-Befehle an den
  Server missbrauchen, allerdings nur, wenn PgBouncer keine Authentifizierungsdaten verlangte.
  (Eine PgBouncer-Konfiguration mit SSL-Zertifikatsauthentifizierung könnte tatsächlich
  darauf verzichten.) (CVE-2021-3935)

**2021-08-09  -  PgBouncer 1.16.0  -  „Einen Jaguar abgewehrt“**

- Funktionen
  * Das Neuladen von TLS-Einstellungen im laufenden Betrieb wird unterstützt. Beim Neuladen der
    Konfigurationsdatei werden geänderte TLS-Einstellungen automatisch wirksam.
  * Unterstützung für abstrakte Unix-Domain-Sockets hinzugefügt. Stellen Sie einem
    Unix-Domain-Socket-Pfad `@` voran, um einen Socket im abstrakten Namensraum zu verwenden.
    Dies entspricht der zugehörigen Funktion von PostgreSQL 14.
  * Die maximale Länge von Passwörtern und Benutzernamen wurde auf 996 bzw. 128 erhöht.
    Verschiedene Cloud-Dienste erfordern dies.
  * Die Mindestgröße des Pools kann jetzt pro Datenbank festgelegt werden, ebenso wie
    die reguläre Poolgröße und die Größe des Reservepools.
  * Die Anzahl ausstehender Abbruchanfragen für Abfragen wird in `SHOW
    POOLS` angezeigt.

- Fehlerbehebungen
  * Beim Parsen der Konfiguration werden Fehler jetzt an vielen Stellen strenger behandelt.
    Wo früher möglicherweise ein Fehler protokolliert und die Verarbeitung fortgesetzt wurde,
    führen solche Konfigurationsfehler jetzt zu einem fehlgeschlagenen Start. So hätte es
    schon immer sein sollen, doch einige Codestellen setzten dies nicht korrekt um.
    Manche Benutzer könnten feststellen, dass ihre Konfigurationen schon immer fehlerhaft
    waren und nun nicht mehr funktionieren.
  * Die Verarbeitung von Abbruchanfragen für Abfragen korrigiert. Unter bestimmten Umständen
    schienen Abbruchanfragen lange festzuhängen. Dies sollte nicht mehr vorkommen.
    Tatsächlich können Abbruchanfragen jetzt bis zum Doppelten der Poolgröße reichen,
    sodass sie wirklich nicht mehr festhängen sollten.
    ([#542](https://github.com/pgbouncer/pgbouncer/pull/542),
    [#543](https://github.com/pgbouncer/pgbouncer/pull/543))
  * Die gemischte Verwendung von md5 und scram über hba korrigiert.
  * Den Build mit c-ares unter Windows korrigiert.
  * Die gefürchteten Meldungen "FIXME: query end, but query_start == 0" beseitigt.
    Ihre Ursache ist jetzt bekannt; sie sollten nicht mehr auftreten.
    ([#565](https://github.com/pgbouncer/pgbouncer/pull/565))
  * Das Neuladen von `default_pool_size`, `min_pool_size` und `reserve_pool_size`
    korrigiert. Bisher funktionierte das Neuladen dieser Einstellungen nicht.

- Bereinigungen
  * Cirrus CI wird jetzt statt Travis CI
    [verwendet](https://cirrus-ci.com/github/pgbouncer/pgbouncer).
  * Wie üblich wurden viele Tests hinzugefügt.
  * Die Protokollmeldung "unclean server" etwas präzisiert. Sie lautet jetzt
    "client disconnect while server was not ready" oder
    "client disconnect before everything was sent to the server". Erstere kann auftreten,
    wenn die Clientverbindung geschlossen wird, während auf dem Server ein Transaktionsblock
    offen ist. Dies hatte einige Benutzer verwirrt.
  * "pgbouncer" kann nicht mehr als Datenbankname verwendet werden. Dieser Name ist für
    die Verwaltungskonsole reserviert; seine Verwendung als regulärer Datenbankname
    hatte nie wirklich korrekt funktioniert. Sie ist jetzt ausdrücklich untersagt.
  * Fehler, die vor dem Schließen der Verbindung an Clients gesendet werden, werden jetzt
    als FATAL statt nur als ERROR gekennzeichnet. Einige Clients reagierten andernfalls
    verwirrt. ([#564](https://github.com/pgbouncer/pgbouncer/pull/564))
  * Compilerwarnungen mit GCC 11 beseitigt.
    ([#623](https://github.com/pgbouncer/pgbouncer/issues/623))

--------

## PgBouncer 1.15.x {#pgbouncer-115x}

**2020-11-19  -  PgBouncer 1.15.0  -  „Ich hab noch einen Koffer in Berlin“**

- Funktionen
  * Die Meldung von Authentifizierungsfehlern verbessert. Die an Clients gesendeten
    Fehlermeldungen besagen jetzt nur noch, dass die Authentifizierung fehlgeschlagen ist,
    ohne weitere Einzelheiten. Details stehen im PgBouncer-Protokoll. Auch wenn der
    angeforderte Benutzer nicht existiert, wird die Authentifizierung vollständig
    durchgeführt und endet mit derselben allgemeinen Fehlermeldung. All dies verhindert,
    dass Clients die PgBouncer-Instanz nach Benutzernamen und anderen Informationen
    zur Authentifizierung auskundschaften. Das Verhalten ähnelt dem von PostgreSQL.
  * Nichts protokollieren, wenn ein Client die Verbindung sofort wieder trennt.
    Dies vermeidet unnötige Protokolleinträge, wenn Überwachungssysteme lediglich
    eine TCP/IP-Verbindung öffnen und ohne Senden von Daten wieder trennen.
  * Das systemd-Journal zur Protokollierung verwenden, wenn es im Einsatz ist.
    Wird erkannt, dass stderr ins systemd-Journal geleitet wird, werden die nativen
    systemd-Funktionen zur Protokollausgabe verwendet. Dies vermeidet doppelte
    Zeitstempel und Prozess-IDs und macht das Protokoll übersichtlicher. Außerdem
    werden Metadaten wie der Schweregrad ergänzt, sodass die Meldungen nützliche
    Metadaten enthalten, wenn das Journal an syslog weitergeleitet wird.
  * Ein Teil der Testsuite kann jetzt unter Windows ausgeführt werden.
  * `SHOW CONFIG` zeigt jetzt auch die Standardwerte der Einstellungen an.

- Fehlerbehebungen
  * Die Option `so_reuseport` unter FreeBSD korrigiert. Der ursprüngliche Code in
    PgBouncer 1.12.0 funktionierte unter FreeBSD tatsächlich nicht.
    ([#504](https://github.com/pgbouncer/pgbouncer/pull/504))
  * Die Kompilierung auf Systemen mit älteren systemd-Versionen repariert.
    Sie war in 1.14.0 beschädigt worden.
    ([#505](https://github.com/pgbouncer/pgbouncer/issues/505))
  * Das Makefile-Ziel zum Erstellen von ZIP-Paketen mit Windows-Binärdateien repariert.
  * Lange Befehlszeilenoptionen funktionieren jetzt auch unter Windows.
  * Das Verhalten der globalen Einstellung `auth_user` korrigiert. Das alte Verhalten
    war verwirrend und fehleranfällig, weil es von der Reihenfolge in der
    Konfigurationsdatei abhing. Dies ist nicht mehr der Fall.
    ([#391](https://github.com/pgbouncer/pgbouncer/issues/391),
    [#393](https://github.com/pgbouncer/pgbouncer/issues/393))

- Bereinigungen
  * Stabilität und Portierbarkeit der Tests verbessert.
  * Den Autoconf-bezogenen Code modernisiert.
  * Compilerwarnungen zu veralteten Funktionen von OpenSSL 3.0.0 deaktiviert.

--------

## PgBouncer 1.14.x {#pgbouncer-114x}

**2020-06-11  -  PgBouncer 1.14.0  -  „Die wiedergefundene Magie“**

- Funktionen
  * SCRAM-Authentifizierungsdurchleitung hinzugefügt. Damit lassen sich verschlüsselte
    SCRAM-Secrets in PgBouncer (aus `userlist.txt` oder `auth_query`) für die Anmeldung
    bei Servern verwenden.
  * Unterstützung für systemd-Socket-Aktivierung hinzugefügt. Dies ist besonders nützlich,
    um systemd auf Systemen mit eingeschränktem Zugriff auf `/var/run/postgresql`
    die Erstellung der Unix-Domain-Sockets zu überlassen.
  * Unterstützung für Unix-Domain-Sockets unter Windows hinzugefügt.

- Bereinigungen
  * Eine alternative, kleinere Beispielkonfiguration `pgbouncer-minimal.ini`
    für Tests oder den Einsatz hinzugefügt.

--------

## PgBouncer 1.13.x {#pgbouncer-113x}

**2020-04-27  -  PgBouncer 1.13.0  -  „Mein Lieblingsspiel“**

- Funktionen
  * Die Konfigurationseinstellung `tcp_user_timeout` zum Setzen der entsprechenden
    Socket-Option hinzugefügt.
  * `client_tls_protocols` und `server_tls_protocols` haben jetzt den Standardwert
    `secure`. Damit sind nur TLS 1.2 und TLS 1.3 aktiviert. Ältere Versionen werden
    weiterhin unterstützt, sind lediglich nicht standardmäßig eingeschaltet.
  * Unterstützung für systemd-Dienstbenachrichtigungen hinzugefügt. Damit lassen sich
    derzeit Service-Units mit `Type=notify` verwenden. Eine weitergehende Integration
    ist für zukünftige Versionen geplant.

- Fehlerbehebungen
  * Mehrzeilige Protokollmeldungen korrigiert
    ([libusual #24](https://github.com/libusual/libusual/pull/24))
  * Von `auth_query` zurückgegebene Nullwerte für Benutzernamen korrekt behandeln
    ([#340](https://github.com/pgbouncer/pgbouncer/pull/340))

- Bereinigungen
  * Die Dateien zur Debian-Paketerstellung unter `debian` entfernt.
    Es wird empfohlen, die Pakete von https://apt.postgresql.org/ zu verwenden.
  * Zahlreiche Korrekturen und Verbesserungen in der Testsuite
  * Die Tests versuchen standardmäßig nicht mehr, sudo zu verwenden. Dies kann
    jetzt durch Setzen der Umgebungsvariable `USE_SUDO` explizit aktiviert werden.
  * Die Nutzung der libevent-API wurde auf Schnittstellen im Stil von Version 2
    umgestellt; die veralteten Schnittstellen von Version 1 werden nicht mehr verwendet.

--------

## PgBouncer 1.12.x {#pgbouncer-112x}

**2019-10-17  -  PgBouncer 1.12.0  -  „Es geht ums Lernen und Besserwerden“**

Diese Version enthält zahlreiche kleinere Erweiterungen und Fehlerbehebungen.

- Funktionen
  * Eine Einstellung zum Aktivieren der Socket-Option `SO_REUSEPORT` hinzugefügt.
    Auf manchen Betriebssystemen ermöglicht dies, mehrere PgBouncer-Instanzen auf
    demselben Host am selben Port lauschen zu lassen, wobei der Kernel die
    Verbindungen automatisch verteilt.
  * Eine Einstellung für die Verwendung einer vom Betriebssystem getrennten
    `resolv.conf`-Datei hinzugefügt. Damit lassen sich eigene DNS-Server und
    gegebenenfalls weitere DNS-Optionen festlegen.
  * Die Ausgabe von `SHOW VERSION` wird als normale Ergebniszeile statt als
    NOTICE-Nachricht gesendet. Das erleichtert die Verarbeitung und entspricht
    dem Verhalten anderer `SHOW`-Befehle.

- Fehlerbehebungen
  * Statistikspalten werden als `numeric` statt als `bigint` gesendet. Dies verhindert
    Fehler in einigen Clientbibliotheken bei Werten, die den Wertebereich von
    `bigint` überschreiten.
    ([#360](https://github.com/pgbouncer/pgbouncer/pull/360),
    [#401](https://github.com/pgbouncer/pgbouncer/pull/401))
  * Ein Problem behoben, bei dem PAM-Benutzer ihr Passwort verloren.
    ([#285](https://github.com/pgbouncer/pgbouncer/issues/285))
  * Clients mit aktiviertem SCRAM Channel Binding werden akzeptiert. Bisher schlug
    die Verbindung mit PgBouncer in bestimmten Situationen fehl, wenn der Client
    Channel Binding unterstützte (also PostgreSQL 11+). PgBouncer unterstützt
    Channel Binding nicht. Diese Änderung korrigiert lediglich die Unterstützung
    für Clients, die es anbieten.
  * Die Kompilierung mit neueren Versionen von musl-libc (verwendet von Alpine Linux)
    korrigiert.

- Bereinigungen
  * Das Ziel `make check` hinzugefügt. Damit lassen sich alle Tests mit einem
    einzigen Befehl ausführen.
  * Verweise auf das PostgreSQL-Wiki entfernt. Alle Informationen stehen jetzt
    entweder in der PgBouncer-Dokumentation oder auf der Website.
  * Die Unterstützung für Libevent 1.x entfernt. Libevent 2.x ist jetzt erforderlich.
    Libevent wird jetzt über pkg-config erkannt.
  * Compilerwarnungen unter macOS und Windows beseitigt. Der Build auf diesen
    Plattformen sollte jetzt ohne Warnungen erfolgen.
  * Einige Warnungen von LLVM scan-build beseitigt.

--------

## PgBouncer 1.11.x {#pgbouncer-111x}

**2019-08-27  -  PgBouncer 1.11.0  -  „Instinkt für Großes“**

- Funktionen
  * Unterstützung für SCRAM-Authentifizierung für Clients und Server hinzugefügt.
    Der neue Authentifizierungstyp `scram-sha-256` wurde ergänzt.
  * `auth_type=password` wird bei einem gespeicherten md5-Passwort so behandelt,
    wie es ein PostgreSQL-Server tun würde.
    ([#129](https://github.com/pgbouncer/pgbouncer/pull/129))
  * Die Option `log_stats` hinzugefügt, um die Ausgabe von Statistiken ins Protokoll
    zu deaktivieren. ([#287](https://github.com/pgbouncer/pgbouncer/pull/287))
  * Die Zeitzone zu Protokollzeitstempeln hinzugefügt.
  * Die PID im Protokollpräfix in [eckige Klammern] setzen.
- Fehlerbehebungen
  * Den OpenSSL-Test in configure bei neueren OpenSSL-Versionen mit `-Werror` korrigiert.
  * Die Berechnung der Wartezeit mit `auth_user` korrigiert. Sie führte entweder
    zu einem Absturz oder meldete unsinnige Werte für die Wartezeit.
    ([#393](https://github.com/pgbouncer/pgbouncer/pull/393))
  * Das in PostgreSQL 12 hinzugefügte Paket GSSENCRequest verarbeiten. Es bewirkt
    derzeit nichts, verhindert aber verwirrende Fehlermeldungen zu "bad packet header".
- Bereinigungen
  * Viele Verbesserungen in der Testsuite und mehrere neue Tests
  * Mehrere Compilerwarnungen unter Windows beseitigt.
  * Die Dokumentation des Abschnitts `[users]` erweitert und diesen zur
    Beispielkonfiguration hinzugefügt.
    ([#330](https://github.com/pgbouncer/pgbouncer/pull/330))

--------

## PgBouncer 1.10.x {#pgbouncer-110x}

**2019-07-01  -  PgBouncer 1.10.0  -  „Angst vor der Welt“**

- Funktionen
  * Unterstützung für das Aktivieren und Deaktivieren von TLS 1.3 hinzugefügt.
    TLS 1.3 wurde abhängig von der OpenSSL-Bibliothek bereits unterstützt, wird
    jetzt aber auch von den Konfigurationseinstellungen zur Auswahl der
    TLS-Protokollversionen unterstützt.
- Fehlerbehebungen
  * Die Unterstützung für TLS 1.3 korrigiert. Sie funktionierte mit OpenSSL 1.1.1
    und 1.1.1a nicht, wohl aber mit früheren und späteren Versionen.
  * Einen seltenen Absturz in `SHOW FDS` behoben
    ([#311](https://github.com/pgbouncer/pgbouncer/issues/311)).
  * Ein Problem behoben, das bei vielen eintreffenden Abbruchanfragen zu einem
    längeren Ausfall führen konnte
    ([#329](https://github.com/pgbouncer/pgbouncer/issues/329)).
  * "unexpected response from login query" nach dem Neuladen von Postgres vermieden
    ([#220](https://github.com/pgbouncer/pgbouncer/issues/220)).
  * Die Berechnung von `idle_transaction_timeout` korrigiert
    ([#125](https://github.com/pgbouncer/pgbouncer/issues/125)). Der Fehler führte
    in bestimmten Situationen zu vorzeitigen Zeitüberschreitungen.
- Bereinigungen
  * Verschiedene Protokoll- und Fehlermeldungen präzisiert.
  * Von Coverity erkannte Probleme behoben; keines hatte in der Praxis erhebliche Auswirkungen.
  * Alle Testskripte verbessert und dokumentiert.
  * Weitere SHOW-Befehle zur Dokumentation hinzugefügt.
  * Die Dokumentation von rst auf Markdown umgestellt.
  * Alle Python-Skripte im Quellbaum sind jetzt mit Python 3 kompatibel.

--------

## PgBouncer 1.9.x {#pgbouncer-19x}

**2018-08-13  -  PgBouncer 1.9.0  -  „Überleben im Chaos“**

- Funktionen
  * Befehl RECONNECT
  * Befehl WAIT_CLOSE
  * Schnelles Schließen: Ein Server im Sitzungs-Pooling-Modus wird sofort getrennt,
    wenn er sich im Modus "close_needed" (erneuter Verbindungsaufbau) befindet.
  * Die Spalte close_needed zu SHOW SERVERS hinzugefügt
- Fehlerbehebungen
  * Doppelte Speicherfreigabe in parse_filename vermieden
  * Dereferenzierung eines NULL-Zeigers in parse_line vermieden
- Bereinigungen
  * mkauth.py auf Python 3 portiert
  * Die Dokumentation der Signale verbessert
  * Die Dokumentation zum Schnelleinstieg verbessert
  * Den Befehl SET dokumentiert
  * Die Liste benötigter Software korrigiert
  * Warnungen zu -Wimplicit-fallthrough beseitigt
  * Fehlende Dokumentation für verschiedene SHOW-Felder ergänzt
  * Das Verhalten beim erneuten Verbindungsaufbau nach Neuladen und DNS-Änderungen dokumentiert
  * Dokumentiert, dass auf KILL anschließend RESUME folgen muss
  * Die Dokumentation von server_lifetime präzisiert
  * Tippfehler und Groß-/Kleinschreibung in Meldungen und Dokumentation korrigiert
  * Den psql-Aufruf in Tests korrigiert
  * Verschiedene weitere Verbesserungen am Testaufbau

--------

## PgBouncer 1.8.x {#pgbouncer-18x}

**2017-12-20  -  PgBouncer 1.8.1  -  „Beim Bodenkampf aufs Zuschlagen setzen“**

- Fehlerbehebungen
  * Die Datei `include/pam.h` in den Distributions-Tarball aufgenommen. Ihr Fehlen
    hatte jeglichen Build aus dem Tarball von 1.8 verhindert.

**2017-12-19  -  PgBouncer 1.8  -  „Sicher am Steuer“**

- Funktionen
  * PAM-Authentifizierung unterstützt. (Mit `--with-pam` aktivieren.)
  * Die Felder `paused` und `disabled` zur Ausgabe von `SHOW DATABASES` hinzugefügt.
  * Das Feld `maxwait_us` zur Ausgabe von `SHOW POOLS` hinzugefügt.
  * Die Felder `wait` und `wait_us` zur Ausgabe der `SHOW`-Befehle hinzugefügt.
  * Die neuen Befehle `SHOW STATS_TOTALS` und `SHOW STATS_AVERAGES` hinzugefügt.
  * Abfragen und Transaktionen werden in `SHOW STATS` getrennt erfasst.
    Die Felder `total_requests`, `avg_req` und `avg_query` wurden durch neue Felder ersetzt.
  * `wait_time` zu `SHOW STATS` hinzugefügt.
- Fehlerbehebungen
  * Die aktualisierte libusual unterstützt OpenSSL 1.1.
  * Es wird nicht versucht, TLS auf Unix-Sockets zu verwenden.
  * Beim Parsen von `pg_hba.conf` wird nach fehlerhaften Zeilen weitergearbeitet, statt die gesamte Datei zurückzuweisen.
    ([#118](https://github.com/pgbouncer/pgbouncer/issues/118))
  * Mehrere weitere Korrekturen beim Parsen von hba.
  * Eine Race Condition beim Abbrechen einer Abfrage behoben.
    ([#141](https://github.com/pgbouncer/pgbouncer/issues/141))
- Bereinigungen
  * Die Einstellung `auth_user` ist jetzt auch global zulässig, nicht nur pro Datenbank.
    ([#142](https://github.com/pgbouncer/pgbouncer/issues/142))
  * Die Client- und Serverkodierung der Konsole auf `UTF8` setzen.

--------

## PgBouncer 1.7.x {#pgbouncer-17x}

**2016-02-26  -  PgBouncer 1.7.2  -  „Endlich abgehoben“**

- Fehlerbehebungen
  * Absturz beim Entfernen einer veralteten PID-Datei behoben. Das Problem wurde in 1.7.1 eingeführt.
  * Speicherbereinigung deaktiviert: Sie verhindert die Übernahme und ist
    für produktive Lasten nicht sinnvoll. Das Problem wurde in 1.7.1 eingeführt.
  * Nach der Übernahme warten, bis die PID-Datei entfernt wurde, bevor der Start fortgesetzt wird.
    Das durch die Speicherbereinigung verlangsamte Herunterfahren legte eine bestehende Race Condition offen.
    ([#113](https://github.com/pgbouncer/pgbouncer/issues/113))
- Bereinigungen
  * Builds durch Entfernen der DBGVER-Verarbeitung reproduzierbar gemacht.
    ([#112](https://github.com/pgbouncer/pgbouncer/issues/112))
  * Antimake: Dateiliste aus $(wildcard) sortieren; neuere gmake-Versionen
    sortieren sie nicht mehr.
    ([#111](https://github.com/pgbouncer/pgbouncer/issues/111))
  * libssl-Version im Protokoll anzeigen.
  * deb: Vollständige Härtung aktivieren.

**2016-02-18  -  PgBouncer 1.7.1  -  „An fünf Freunde weiterleiten, sonst ...“**

WARNUNG: Seit Version 1.7 wird `server_reset_query` nicht ausgeführt, wenn sich
die Datenbank im Transaktions-Pooling-Modus befindet. Offenbar wurde dies in
der Ankündigung zu 1.7 nicht deutlich genug hervorgehoben. Falls Anwendungen
darauf angewiesen sind, mit `server_reset_query_always` das bisherige Verhalten wiederherstellen.

Die Arbeit an dieser Version bestand ansonsten hauptsächlich darin, ein
vermeintliches TLS-Speicherleck aufzuspüren, das sich als nicht existent erwies.
Stattdessen benötigt der libssl-Build in Debian/wheezy 600k zusätzlichen Speicher
pro Verbindung (ohne Speicherleck) statt der erwarteten 20-30k.
Darauf sollte bei der Verwendung von TLS geachtet werden.

- Fehlerbehebungen
  * TLS: sslmode "disabled" in "disable" umbenannt, da PostgreSQL
    diese Bezeichnung verwendet.
  * TLS: `client_tls_sslmode=verify-ca/-full` weist jetzt
    Verbindungen ohne Clientzertifikat ab.
    ([#104](https://github.com/pgbouncer/pgbouncer/issues/104))
  * TLS: `client_tls_sslmode=allow/require` validiert ein
    Clientzertifikat, wenn eines gesendet wird. Zuvor blieb die
    Zertifikatsvalidierung unkonfiguriert, sodass Verbindungen mit Clientzertifikat fehlschlugen.
    ([#105](https://github.com/pgbouncer/pgbouncer/issues/105))
  * Speicherleck beim Freigeben einer Datenbank behoben.
  * Mögliches Speicherleck in tls_handshake() behoben.
  * EOF-Behandlung in tls_handshake() korrigiert.
  * Zu kleinen memset-Bereich in der Kompatibilitätsimplementierung von asn1_time_parse korrigiert.
  * Build ohne TLS (`--without-openssl`) korrigiert.
    ([#101](https://github.com/pgbouncer/pgbouncer/issues/101))
  * Verschiedene Probleme beim Windows-Build behoben.
    ([#100](https://github.com/pgbouncer/pgbouncer/issues/100))
- Bereinigungen
  * TLS: SSL_MODE_RELEASE_BUFFERS verwenden, um den Speicherverbrauch
    inaktiver Verbindungen zu verringern.
  * Zugewiesenen Speicher beim Beenden freigeben. Dies erleichtert den Einsatz von Werkzeugen zur Suche nach Speicherlecks.
  * Dokumentation zu `server_reset_query` verbessert.
    ([#110](https://github.com/pgbouncer/pgbouncer/issues/110))
  * TLS-Optionen zur Beispielkonfiguration hinzugefügt.

**2015-12-18  -  PgBouncer 1.7  -  „Die Farben variieren nach der Auferstehung“**

- Funktionen
  * TLS-Verbindungen unterstützen. OpenSSL/LibreSSL dient
    als Backend-Implementierung.
  * Authentifizierung über TLS-Clientzertifikate unterstützen.
  * "peer"-Authentifizierung über Unix-Sockets unterstützen.
  * Eine Datei für die hostbasierte Zugriffskontrolle unterstützen, wie
    [pg_hba.conf](http://www.postgresql.org/docs/9.4/static/auth-pg-hba-conf.html)
    in PostgreSQL. Damit lassen sich TLS für Netzwerkverbindungen und "peer"-
    Authentifizierung für lokale Verbindungen konfigurieren.
- Bereinigungen
  * `query_wait_timeout` standardmäßig auf 120s setzen. Der bisherige Standardwert
    (0) führt zu unbegrenztem Warten in der Warteschlange, was nicht sinnvoll ist.
    Das bedeutet: Hat ein Client eine ausstehende Abfrage und wurde ihm noch
    keine Serververbindung zugewiesen, wird die Clientverbindung
    getrennt.
  * `server_reset_query_always` standardmäßig deaktivieren. Die Abfrage zum
    Zurücksetzen wird jetzt nur in Pools mit Sitzungs-Pooling verwendet.
  * pkt_buf auf 4096 Byte erhöhen. Dies verbessert die Leistung mit TLS.
    Das Verhalten hängt wahrscheinlich von der Last ab, die Änderung sollte
    jedoch unbedenklich sein, da die Paketpuffer seit v1.2 von den Verbindungen
    getrennt sind und erst bei Bedarf aus einem Pool bezogen werden.
  * Pipelining durch Zählen der erwarteten ReadyForQuery-Pakete unterstützen.
    Dadurch wird verhindert, dass der Server zu früh freigegeben wird. Behebt
    [#52](https://github.com/pgbouncer/pgbouncer/issues/52).
  * sbuf_loopcnt-Logik verbessert: Der Socket wird garantiert erneut
    verarbeitet, auch wenn kein Socket-Ereignis vorliegt.
    Dies ist für TLS erforderlich, da es eigene Puffer verwendet.
  * Systemtests für aktuelle BSD- und MacOS-Versionen angepasst.
    (Eric Radman)
  * **crypt**-Authentifizierung entfernt. Sie ist veraltet und wird
    seit PostgreSQL 8.4 nicht mehr unterstützt.
  * Die einfache configure-Option "--with-cares" korrigiert: Ohne Argument
    funktionierte sie nicht.

--------

## PgBouncer 1.6.x {#pgbouncer-16x}

**2015-09-03  -  PgBouncer 1.6.1  -  „Das Studiopublikum stimmt zu“**

- Funktionen
  * Neue Einstellung: `server_reset_query_always`. Wenn sie gesetzt ist,
    wird `server_reset_query` für Pools ohne Sitzungs-Pooling deaktiviert.
    PgBouncer führt pool_mode pro Pool ein, doch Sitzungs-Pooling
    und Transaktions-Pooling sollten nicht dieselbe Abfrage zum Zurücksetzen verwenden.
    Tatsächlich sollte Transaktions-Pooling überhaupt keine solche Abfrage verwenden.

    In 1.6.x ist die Einstellung aktiviert, in 1.7 wird sie jedoch deaktiviert.

- Fehlerbehebungen
  * [SICHERHEIT] Ungültige Zuweisung von `auth_user` entfernt. (#69)
    Wenn `auth_user` gesetzt ist und der Client einen nicht vorhandenen
    Benutzernamen angibt, meldet sich der Client als `auth_user` an. Das ist problematisch.

    [CVE-2015-6817](https://access.redhat.com/security/cve/cve-2015-6817)

  * NoticeResponse in handle_auth_response überspringen. Andernfalls
    führen ausführliche Protokollierungsstufen auf dem Server zu Anmeldefehlern.

  * Konsole: `auth_user` belegen, wenn auth_type=any gesetzt ist. Andernfalls
    kann die Protokollierung abstürzen (#67).

  * Verschiedene Portabilitätskorrekturen (OpenBSD, Solaris, OSX).

**2015-08-01  -  PgBouncer 1.6  -  „Zombies der Zukunft“**

- Funktionen

  * Den Passwort-Hash des Benutzers aus einer PostgreSQL-Datenbank laden.
    Neue Parameter:

    auth_user
        Benutzer, mit dem die Verbindung zur selben Datenbank hergestellt und die Benutzerinformation abgefragt wird.
        Kann auch pro Datenbank gesetzt werden.

    auth_query
        SQL-Abfrage, die als auth_user ausgeführt wird.
        Standardwert: "SELECT usename, passwd FROM pg_shadow WHERE usename=$1"

    (Cody Cutrer)

  * Der Pooling-Modus lässt sich sowohl pro Datenbank als auch pro Benutzer konfigurieren.
    (Cody Cutrer)

  * Verbindungsgrenzen pro Datenbank und pro Benutzer: max_db_connections und
    max_user_connections.
    (Cody Cutrer / Pavel Stehule)

  * DISABLE/ENABLE-Befehle hinzugefügt, um neue Verbindungen zu verhindern.
    (William Grant)

  * Neues DNS-Backend: c-ares. Es ist das einzige DNS-Backend, das alle
    relevanten Funktionen unterstützt: /etc/hosts mit Aktualisierung, SOA-Abfragen,
    große Antworten (über TCP/EDNS+UDP), IPv6. Es ist jetzt das bevorzugte
    Backend und wird künftig wahrscheinlich das **einzige** Backend sein,
    da die Unterstützung einer Vielzahl unzureichender Bibliotheken nicht sinnvoll ist.

    Problem: c-ares-Versionen <= 1.10 enthalten einen Fehler, durch den die CNAME-Unterstützung
    bei aktiviertem IPv6 nicht funktioniert. (Im Upstream behoben.) Als Übergangslösung
    wird c-ares <= 1.10 nur mit IPv4 verwendet. PgBouncer wird die anderen Backends
    daher erst entfernen, wenn c-ares >1.10 (noch nicht veröffentlicht) einige Zeit verfügbar ist ...

  * remote_pid in SHOW CLIENTS/SERVERS anzeigen. Verfügbar für Clients mit
    Verbindungen über Unix-Sockets sowie für Serververbindungen über TCP und Unix-Sockets.
    Bei TCP-Servern wird die PID aus dem Abbruchschlüssel entnommen.

  * Eigenen Konfigurationsparameter (dns_nxdomain_ttl) zur Steuerung
    der negativen DNS-Zwischenspeicherung hinzugefügt.
    (Cody Cutrer)

  * IP-Adresse und Port des Clienthosts zu application_name hinzufügen.
    Dies wird durch den Konfigurationsparameter application_name_add_host
    aktiviert, dessen Standardwert 'off' ist.
    (Andrew Dunstan)

  * Konfigurationsdateien unterstützen die Direktive '%include FILENAME', mit der
    sich die Konfiguration auf mehrere Dateien aufteilen lässt.
    (Andrew Dunstan)

- Bereinigungen

  * Protokoll: IPv6-Adressen in [] einschließen.
  * Protokoll: Beim Verbindungsaufbau zum Server lokale IP-Adresse und Port anzeigen.
  * win32: Für lange Argumente den GNU-Stil verwenden: --foo
  * Ziffern in Hostnamen zulassen; immer versuchen, mit inet_pton zu parsen.
  * deallocate_all() in den FAQ korrigiert.
  * Falsches Schlüsselwort in der Beispielkonfiguration korrigiert.
    (Magnus Hagander)
  * Kommentare (mit ';') in Authentifizierungsdateien zulassen.
    (Guillaume Aubert)
  * Rechtschreibfehler in Protokollmeldungen und Kommentaren korrigiert.
    (Dmitriy Olshevskiy)

- Fehlerbehebungen

  * Aufbau neuer Verbindungen während der Wartung korrigiert.
    (Cody Cutrer)
  * Authentifizierungsdatei beim Start nicht zweimal laden.
    (Cody Cutrer)
  * Korrekte Invalidierung automatisch erzeugter Datenbanken.
  * IPv6: IPV6_V6ONLY am lauschenden Socket setzen.
  * win32: SO_REUSEADDR am lauschenden Socket nicht setzen.
  * memcpy für IPv6-Adressen korrigiert.
  * Abbruch wartender Clients korrigiert.
    (Mathieu Fenniak)
  * Kleinen Fehler behoben: Das Ergebnis von calloc muss geprüft werden.
    (Heikki Linnakangas)
  * Zeilenumbruch am Ende der PID-Datei hinzugefügt.
    (Peter Eisentraut)
  * Keine neuen Serververbindungen zulassen, wenn PAUSE <db> ausgeführt wurde.
    (Petr Jelinek)
  * 'bad packet' bei der Anmeldung behoben, wenn der Header verzögert eintrifft.
    (Michał Trojnara, Marko Kreen)
  * Von Coverity erkannte Fehler behoben.
    (Euler Taveira)
  * server_idle_timeout deaktivieren, wenn die Serveranzahl unter min_pool fällt (#60).
    (Marko Kreen)

--------

## PgBouncer 1.5.x {#pgbouncer-15x}

**2015-04-09  -  PgBouncer 1.5.5  -  „Totstellen, um zu gewinnen“**

- Fehlerbehebungen
  * Aus der Ferne auslösbaren Absturz behoben: Eine ungültige Paketreihenfolge führt
    zum Zugriff auf einen NULL-Zeiger. Nicht ausnutzbar, nur DoS.

**2012-11-28  -  PgBouncer 1.5.4  -  „Keine Lecks, Töpfchentraining erfolgreich“**

- Fehlerbehebungen
  * DNS: Speicherleck im getaddrinfo_a()-Backend behoben.
  * DNS: Speicherleck im udns-Backend behoben.
  * DNS: Statistikberechnung korrigiert.
  * DNS: Verarbeitung von Fehlermeldungen für getaddrinfo_a() verbessert.
  * win32-Kompilierung korrigiert.
  * Prüfung der Compiler-Unterstützung für Abhängigkeiten in configure korrigiert.
  * Einige Dokumentationsfehler korrigiert.

**2012-09-12  -  PgBouncer 1.5.3  -  „Quantentoaster“**

- Kritische Fehlerbehebung

  * Zu lange Datenbanknamen können zu einem Absturz führen, der sich
    bei aktivierten automatisch erzeugten Datenbanken aus der Ferne auslösen lässt.

    Die ursprünglichen Prüfungen gingen davon aus, dass alle Namen aus
    Konfigurationsdateien stammen; daher war die Verwendung von fatal() unproblematisch.
    Sind automatisch erzeugte Datenbanken jedoch aktiviert
    - durch '*' im Abschnitt [databases] -, kann der Datenbankname aus dem Netzwerk
    stammen, was ein Beenden aus der Ferne ermöglicht.

    [CVE-2012-4575](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-4575)

- Kleinere Funktionen

  * max_packet_size: Konfigurationsparameter zur Einstellung der maximalen
    Paketgröße, die weitergeleitet werden darf. Der Standardwert bleibt unverändert:
    (2G-1), kann jetzt jedoch verkleinert werden.
  * Wenn sich ein Paketheader nicht parsen lässt, diesen im Protokoll und in
    der Fehlermeldung hexadezimal anzeigen.

- Fehlerbehebungen

  * AntiMake verwendete $(relpath) und $(abspath) zur Bearbeitung von Pfadnamen.
    Dadurch schlug der Build jedoch fehl, wenn der Pfad des Quellbaums
    symbolische Links enthielt. Der Code arbeitet jetzt ausschließlich mit einfachen Zeichenketten.
  * Konsole: Mit SET können jetzt leere Zeichenketten als Werte gesetzt werden.
  * config.txt: Darauf hinweisen, dass alle Zeitüberschreitungen als Gleitkommazahlen
    angegeben werden können. Diese wenig bekannte Funktion wurde in 1.4 eingeführt.

**2012-05-29  -  PgBouncer 1.5.2  -  „Nicht kauen, nur schlucken“**

- Fehlerbehebungen
  * Durch einen Fehler wurde reserve_pool_timeout in Mikrosekunden statt
    Sekunden interpretiert. Dadurch wurde der Reservepool praktisch sofort aktiviert,
    sobald der Pool voll war. Jetzt wird der Wert wie vorgesehen als Sekunden interpretiert.
    (Von Keyur Govande bemerkt)

**2012-04-17  -  PgBouncer 1.5.1  -  „Abbrechen, wiederholen, ignorieren?“**

- Funktionen
  * Parameter zur Einstellung der Berechtigungen für den Unix-Socket:
    unix_socket_mode=0777, unix_socket_group=''.
- Fehlerbehebungen
  * Leere Zeichenketten als serverseitige Variablenwerte zulassen. Dies ist
    erforderlich, damit "application_name" korrekt funktioniert, da es der
    einzige Parameter ohne serverseitigen Standardwert ist.
  * Bei geänderter Verbindungszeichenfolge die Aktualisierung der Serverparameter erzwingen.
    Zuvor verwendete PgBouncer die alten Parameter weiter, was
    bei einem PostgreSQL-Upgrade zu Problemen führt.
  * Bei geänderter Verbindungszeichenfolge einer automatisch erzeugten Datenbank alte Verbindungen trennen.
  * cf_setint: strtol() statt atoi() zum Parsen ganzzahliger Konfigurationsparameter
    verwenden. Damit sind hexadezimale und oktale Werte sowie eine bessere Fehlererkennung möglich.
  * sigqueue() verwenden, um das Vorhandensein von union sigval zu erkennen.
    Dies korrigiert die Kompilierung unter HPUX.
  * Den Befehl 'git' aus dem Makefile entfernen, da er bei Builds aus einem
    einfachen Tarball zufällige Fehler verursacht.
  * Parameter stats_period dokumentieren. Er steuert das Intervall für
    die Statistikausgabe.
  * Asciidoc >= 8.4 voraussetzen; die Dokumentation scheint nicht mehr mit
    früheren Versionen kompatibel zu sein.
  * Bei EINTR von close() keinen erneuten Versuch mehr unternehmen.

**2012-01-05  -  PgBouncer 1.5  -  „Seit 2007 zufriedene Clients durchschleusen“**

Wenn hinter einem DNS-Namen mehr als 8 IP-Adressen verwendet werden, muss
die Abfrage jetzt über das EDNS0-Protokoll erfolgen. Nur die Backends
getaddrinfo_a()/getaddrinfo() und UDNS unterstützen es, libevent 1.x/2.x nicht.
Zur Aktivierung für libc 'options edns0' zu /etc/resolv.conf hinzufügen.

Zum Kompilieren wird GNU Make 3.81+ benötigt.

- Funktionen
  * Änderungen an DNS-Antworten erkennen und Verbindungen zu IP-Adressen
    invalidieren, die in der neuesten Antwort nicht mehr enthalten sind.
    (Petr Jelinek)
  * Hostnamen anhand der Seriennummer der DNS-Zone invalidieren. Wenn
    dns_zone_check_period gesetzt ist, werden die SOA-Einträge aller DNS-Zonen
    abgefragt. Hat sich die Seriennummer geändert, werden alle Hostnamen
    abgefragt. Dies ist für eine deterministische Invalidierung von Verbindungen
    erforderlich, da eine Invalidierung bei der Namensauflösung nutzlos ist,
    wenn keine Namensauflösung stattfindet.
    Funktioniert nur mit dem neuen UDNS-Backend.
  * Neue Befehle SHOW DNS_HOSTS und SHOW DNS_ZONES zum Untersuchen des DNS-Caches.
  * Neuer Parameter: min_pool_size verhindert, dass bei fehlender Last
    alle Verbindungen getrennt werden.
    (Filip Rembiałkowski)
  * idle_in_transaction_timeout: Transaktion beenden, wenn sie zu lange im Leerlauf ist.
    Standardmäßig nicht gesetzt.
  * Neues libudns-Backend für DNS-Abfragen. Bietet mehr Funktionen als evdns.
    Mit --with-udns aktivieren. Unterstützt IPv6 noch nicht.
  * KILL-Befehl zum sofortigen Trennen aller Verbindungen einer Datenbank.
    (Michael Tharp)
  * Wechsel zum Antimake-Build-System für übersichtlichere Makefiles.
    Zum Kompilieren wird jetzt GNU Make 3.81+ benötigt.
- Fehlerbehebungen
  * DNS funktioniert jetzt mit IPv6-Hostnamen.
  * Verbindungszustand nicht ändern, wenn NOTIFY vom Server eintrifft.
  * Verschiedene Dokumentationsfehler korrigiert.
    (Dan McGee)
  * Konsole: Bezeichner in "" einschließen können. Ursprünglich gab es keine
    Befehle mit Datenbanknamen als Argument, sodass kein Quoting benötigt wurde.
  * Konsole: Im regulären Ausdruck für Wörter auch Ziffern am Wortanfang zulassen.
    Ein strikter Parser würde die Verarbeitung hier zu komplex machen.
  * Pausierte automatisch erzeugte Datenbanken nicht verfallen lassen.
    (Michael Tharp)
  * Automatisch erzeugte Datenbanken bei PAUSE nach Bedarf anlegen.
    (Michael Tharp)
  * Falsche Protokollmeldung des Befehls RESUME korrigiert.
    (Peter Eisentraut)
  * Enthält die Datenbank-Verbindungszeichenfolge user= ohne password=,
    wird das Passwort aus userlist übernommen.
  * '*' im Übernahmecode korrekt parsen.
  * autogen.sh: Mit älteren autoconf-/automake-Versionen funktionieren.
  * Absturz beim Betrieb als Dienst unter win32 behoben, der durch ein fehlerhaftes
    basename() der mingw/msvc-Laufzeit verursacht wurde. Jetzt wird immer die Kompatibilitätsimplementierung von basename() verwendet.

--------

## PgBouncer 1.4.x {#pgbouncer-14x}

**2011-06-16  -  PgBouncer 1.4.2  -  „Algorithmus für den Erstschlag“**

Betroffene Betriebssysteme: \*BSD, Solaris, Win32.

- Portabilitätskorrekturen
  * CFLAGS an den Linker übergeben. Dies ist bei der pthread-basierten
    Ersatzimplementierung von getaddrinfo_a() erforderlich.
  * lib/find_modules.sh: split() durch index()+substr() ersetzen.
    Dadurch sollte es mit älteren AWKs funktionieren.
  * <usual/endian.h>: htoX/Xtoh-Definitionen des Systems ignorieren.
    Möglicherweise ist nur ein Teil der Makros definiert.
  * <usual/signal.h>: Kompatibilitätsimplementierungen von sigval und sigevent trennen.
  * <usual/socket.h>: <sys/uio.h> einbinden, um iovec zu erhalten.
  * <usual/time.h>: Automatische Funktionserkennung unter win32 verbessern.
  * <usual/base_win32.h>: Doppelte Deklaration von sigval/sigevent entfernen.

**2011-04-01  -  PgBouncer 1.4.1  -  „Alles war nur gespielt“**

- Funktionen

  * Lauschen und Verbindungsaufbau auf IPv6-Adressen unterstützen.
    (Hannu Krosing)
  * Mehrere Listen-Adressen in 'listen_addr'. Für jede wird getaddrinfo()
    aufgerufen, sodass auch Namen verwendet werden können.
  * Konsole: PgBouncer-Version als 'server_version' an den Client senden.

- Wichtige Fehlerbehebungen

  * getaddrinfo_a() unter glibc < 2.9 deaktivieren, da es mit älteren Versionen abstürzt.

    Insbesondere betroffene Betriebssysteme: RHEL/CentOS 5.x (glibc 2.5), Ubuntu 8.04 (glibc 2.7).
    Ebenfalls betroffen ist Debian/lenny (glibc 2.7), dessen getaddrinfo_a() zwar nicht abstürzt,
    für das es aber keine zuverlässige Erkennungsmöglichkeit gibt.

    Auf solchen Betriebssystemen bitte libevent 2.x verwenden; die Ersatzimplementierung
    von getaddrinfo_a() ist nicht für Produktionssysteme vorgesehen. Im neuen Abschnitt
    zur Unterstützung für DNS-Abfragen in README wird erläutert, wie das DNS-Backend ausgewählt wird.

    (Hubert Depesz Lubaczewski, Dominique Hermsdorff, David Sommerseth)

  * Bei Verwendung von libevent 2.x standardmäßig --enable-evdns aktivieren.

  * tcp_keepalive standardmäßig aktivieren, wie es auch PostgreSQL tut.
    (Hubert Depesz Lubaczewski)

  * server_reset_query standardmäßig auf DISCARD ALL setzen, um von Anfang an
    mit PostgreSQL kompatibel zu sein.

  * win32: Abstürze bei Unix-Socket-Adressen mit NULL behoben.
    (Hiroshi Saito)

  * Bereinigung automatisch erzeugter Datenbanken korrigiert: Der alte Code verwechselte
    Datenbanken und Pools. Sobald ein leerer Pool gefunden wurde, wurde die Datenbank
    als 'idle' markiert. Dadurch konnte später eine Datenbank mit aktiven Benutzern beendet werden.

    Gemeldet von: Hubert Depesz Lubaczewski

- Fehlerbehebungen

  * Kompatibilitätsimplementierung von getaddrinfo_a() durch einen einzelnen
    parallelen Thread für Namensabfragen nicht blockierend gemacht.
  * Kompilierung mit pthread aktivieren, wenn die Kompatibilitätsimplementierung von getaddrinfo_a verwendet wird.
  * release_server setzte bei einer Trennung aufgrund der Lebensdauer ->last_lifetime_disconnect nicht.
    (Emmanuel Courreges)
  * win32: Authentifizierungsdateien mit DOS-Zeilenenden korrigiert. load_file()
    berücksichtigte nicht, dass die Datei beim Laden schrumpft.
    (Rich Schaaf)
  * <usual/endian.h>: autoconf-Erkennung für enc/dec-Funktionen hinzufügen,
    um Konflikte unter BSD zu vermeiden.
    (James Pye)
  * Nicht abstürzen, wenn die Konfigurationsdatei nicht vorhanden ist.
    (Lou Picciano)
  * Bei fehlgeschlagener DNS-Abfrage mit sehr ausführlicher Protokollierung (-v -v) nicht abstürzen.
    (Hubert Depesz Lubaczewski, Dominique Hermsdorff)
  * In find_modules.sh Backticks statt $(cmd) verwenden, um die Portabilität zu verbessern.
    (Lou Picciano)
  * In find_modules.sh 'awk' statt 'sed' verwenden, um die Portabilität zu verbessern.
    (Giorgio Valoti)
  * Informationen zum aktiven asynchronen DNS-Backend beim Start protokollieren.
  * --disable-evdns korrigiert, sodass es 'no' statt 'yes' bedeutet.
  * In der Dokumentation erwähnen, dass -R unix_socket_dir voraussetzt.
  * server_reset_query in faq.txt erläutern.
  * Verloren gegangenen memset im Slab-Allokator wiederhergestellt.
  * Verschiedene kleinere Portabilitätskorrekturen in libusual.

**2011-01-11  -  PgBouncer 1.4  -  „Blutiger Code“**

- Funktionen

  * Asynchrone DNS-Abfragen: Hostnamen werden jetzt beim Verbindungsaufbau
    statt beim Neuladen aufgelöst; die Zwischenspeicherung ist konfigurierbar.
    (Siehe Parameter dns_max_ttl.)

    Standardmäßig wird getaddrinfo_a() (glibc) als Backend verwendet.
    Ist es nicht vorhanden, wird getaddrinfo_a() durch blockierendes(!) getaddrinfo() emuliert.

    Mit dem Argument --enable-evdns für configure wird evdns von libevent
    als Backend verwendet. Es ist nicht standardmäßig aktiviert, da libevent 1.3/1.4
    eine fehlerhafte Implementierung enthält. Nur evdns in libevent 2.0 scheint in Ordnung zu sein.

  * Neue Konfigurationsvariable: syslog_ident zur Einstellung des syslog-Namens.

  * Korrekte Unterstützung des Startparameters `application_name`.

  * Lange Befehlszeilenoptionen (Guillaume Lelarge)

  * Portabilitätskorrekturen für Solaris (Hubert Depesz Lubaczewski)

  * Neue Konfigurationsvariable: disable_pqexec. Damit lässt sich in Umgebungen
    mit sehr hohen Sicherheitsanforderungen das Simple Query Protocol deaktivieren.
    Dies erfordert Anwendungen, die ausschließlich das Extended Query Protocol verwenden.

  * PostgreSQL-Kompatibilität: Ist der Datenbankname im Startpaket leer,
    den Benutzernamen als Datenbanknamen verwenden.

- Fehlerbehebungen

  * Bei den Serverparametern DateStyle und TimeZone muss die Groß-/Kleinschreibung exakt stimmen.
  * Konsole: Serverparameter datetime, timezone und stdstr an den Client senden.

- Interne Bereinigungen

  * Bibliothek libusual für systemnahe Hilfsfunktionen verwenden.
  * Feste Längenbegrenzung für Serverparameter entfernen.

--------

## PgBouncer 1.3.x {#pgbouncer-13x}

**2010-09-09  -  PgBouncer 1.3.4  -  „Der Bouncer hat immer recht“**

- Fehlerbehebungen
  * Fail-Fast-Logik bereits beim Verbindungsaufbau anwenden.
    Bei einem Serverfehler erhalten Clients den Fehler somit schon beim Verbindungsaufbau.
  * Automatisch erzeugte Datenbanken beim Neuladen nicht zur Prüfung markieren.
    Andernfalls werden sie beendet, da sie nicht in der Konfiguration stehen.
  * Parameter application_name standardmäßig ignorieren. Dadurch müssen
    PostgreSQL-9.0-Benutzer ihn nicht selbst in ignore_startup_parameters=
    aufnehmen.
  * Quoting in pg_auth korrigiert. '\' wird dort nicht verwendet.
  * Bessere Fehlerausgabe auf der Konsole; eingehende Abfrage dem Benutzer anzeigen.
  * Betriebssysteme (OpenBSD) unterstützen, bei denen tv_sec nicht vom Typ time_t ist.
  * Übermäßig viele Warnungen mit gcc 4.5 vermeiden.

**2010-05-10  -  PgBouncer 1.3.3  -  „NSFW“**

- Verbesserungen
  * Argument von listen(2) mit listen_backlog konfigurierbar machen.
    Dies ist auf Betriebssystemen nützlich, bei denen das zulässige Systemmaximum konfigurierbar ist.
  * Meldungen beim Trennen verbessern, damit sie den Benutzernamen oder Datenbanknamen
    nennen, der zum Fehlschlagen der Anmeldung geführt hat.
- Fehlerbehebungen
  * Die Logik für erneute Verbindungsversuche im Fail-Fast-Verfahren umgestellt.
    Die bisherige Logik war bei dauerhaft fehlerhaften Datenbanken oder Benutzern störend,
    da sie selbst dann neue Versuche unternahm, wenn sich keine Clients anmelden wollten.
  * Protokollierungsfunktionen behalten den bisherigen errno-Wert bei.
    Andernfalls kann sich PgBouncer bei höheren Protokollierungsstufen und Protokollierungsproblemen unerwartet verhalten.
  * Verschiedene Puffer für den Verbindungsstart vergrößert, um die umfangreicheren
    Startmeldungen von EDB verarbeiten zu können.
  * Startanfrage des V2-Protokolls erkennen und einen klaren Grund für die Trennung angeben.

**2010-03-15  -  PgBouncer 1.3.2  -  „Bumerangkugel“**

- Fehlerbehebungen

  * Neue Konfigurationsvariable 'query_wait_timeout'. Erhält der Client innerhalb
    dieser Anzahl von Sekunden keine Serververbindung, wird seine Verbindung getrennt.

  * Ist keine Serververbindung im Pool vorhanden und schlug der letzte Verbindungsversuch fehl,
    Clientverbindungen nicht warten lassen, sondern sofort einen Fehler senden.

    Zusammen mit der vorherigen Korrektur verhindert dies unnötige Wartezeiten
    bei ausgefallenen Datenbanken.

  * libevent-Zustand in sbuf.c nachverfolgen, um doppelte event_del()-Aufrufe zu vermeiden.
    Obwohl dies normalerweise unbedenklich ist, scheint es nicht zu 100% zu funktionieren.
    Jetzt sollte jederzeit bekannt sein, ob der Aufruf bereits erfolgt ist.

  * Wartung während SUSPEND deaktivieren. Andernfalls könnte die alte PgBouncer-Instanz
    bei kurzen Zeitüberschreitungen nach der Übergabe noch einige Verbindungen schließen.

  * client_login_timeout auf Clients anwenden, die auf das Begrüßungspaket
    warten (erste Serververbindung). Andernfalls können sie unbegrenzt warten,
    sofern query_timeout nicht gesetzt ist.

  * win32: Schalter -U/-P zu -regservice hinzufügen, damit das Konto für
    die Ausführung des Dienstes gewählt werden kann. Die bisherige automatische Auswahl
    zwischen Local Service und Local System war nicht zuverlässig genug.

  * Konsole: \0 am Ende von Textspalten entfernen. Dies war schwer zu erkennen,
    da C-Clients damit zurechtkamen.

  * Dokumentation verbessert. (Greg Sabino Mullane)

  * Einige Protokollmeldungen zur Anmeldung präzisiert.

  * Protokollierungsstufe für vom Pooler gesendete Fehler (meist beim Trennen)
    von INFO auf WARNING ändern, da sie auf Probleme hinweisen.

  * Protokollmeldung für query_timeout in "query timeout" ändern.

**2009-07-06  -  PgBouncer 1.3.1  -  „Jetzt vollständig konform mit den NSA-Überwachungsanforderungen“**

- Fehlerbehebungen
  * Problem mit sbuf_loopcnt behoben, das Verbindungen blockieren konnte.
    Lag die Länge einer Abfrage oder eines Ergebnisses nahe einem Vielfachen von
    (pktlen*sbuf_loopcnt) [standardmäßig 10k], konnte die Verbindung auf weitere
    Daten warten, die nicht mehr eintreffen würden.
  * Datenbank-Neukonfiguration sofort wirksam machen. Bisher konnten alte
    Verbindungen nach SIGHUP wiederverwendet werden.
  * SHOW DATABASES korrigiert, das durch das Hinzufügen einer Spalte nicht mehr funktionierte.
  * Bei "auth_type=any" war der Konsolenzugriff deaktiviert, da PgBouncer den Benutzernamen verwarf.
    Korrektur: Bei "auth_type=any" jeden Benutzer als Administrator zur Konsole zulassen.
  * Fehlerhaftes CUSTOM_ALIGN-Makro korrigiert. Glücklicherweise wird es nicht verwendet,
    wenn das Betriebssystem bereits ALIGN definiert; daher scheint der Fehler praktisch nicht aufgetreten zu sein.
  * win32: WSAStartup() immer aufrufen, nicht nur im Daemon-Modus,
    da beim Parsen der Konfiguration Hostnamen aufgelöst werden sollen.
  * win32: Den Namen der Konfigurationsdatei in der Befehlszeile des Dienstes
    in Anführungszeichen einschließen, um Leerzeichen in Pfaden zu ermöglichen.
    Der Pfad der ausführbaren Datei scheint dies aufgrund einer win32-Besonderheit nicht zu benötigen.
  * STATS zur Ausgabe von SHOW HELP hinzufügen.
  * doc/usage.txt: Die Zeiteinheiten in Konsolenergebnissen sind
    Mikrosekunden, nicht Millisekunden.

**2009-02-18  -  PgBouncer 1.3 -  „Neue Abschlusstechnik Ki-Smash“**

- Funktionen

  * IANA hat Port 6432 als offiziellen Port für PgBouncer zugewiesen.
    Daher wurde die Standardportnummer auf 6432 geändert. Für bestehende
    Einzelanwender ist keine Änderung erforderlich. Bei der Verteilung
    von PgBouncer-Paketen bitte den Paketstandard auf den offiziellen
    Port ändern.

  * Dynamisches Anlegen von Datenbanken (David Galoyan)

    Jetzt lässt sich eine Datenbank mit dem Namen "*" definieren.
    Ihre Verbindungszeichenfolge wird dann für alle nicht definierten Datenbanken
    verwendet. Dies ist hauptsächlich für Test- und Entwicklungsumgebungen nützlich.

  * Windows-Unterstützung (Hiroshi Saito)

    PgBouncer läuft jetzt unter Windows 2000+. Der Aufruf über die Befehlszeile
    bleibt unverändert, allerdings sind weder der Daemon-Modus noch ein Online-Neustart möglich.
    Für den Betrieb als Dienst den Parameter service_name in der Konfiguration festlegen. Danach:

        > pgbouncer.exe config.ini -regservice
        > net start SERVICE_NAME

    Zum Beenden und Aufheben der Registrierung:

        > net stop SERVICE_NAME
        > pgbouncer.exe config.ini -unregservice

    Für das Windows-Ereignisprotokoll muss zunächst die Ereignis-DLL registriert werden:

        > regsvr32 pgbevent.dll

    Anschließend kann "syslog = 1" in der Konfiguration gesetzt werden.

- Kleinere Funktionen

  * Datenbanknamen in der Konfigurationsdatei können jetzt mit dem üblichen
    SQL-Quoting für Bezeichner angegeben werden, um Sonderzeichen in Datenbanknamen zuzulassen.

  * Neue Einstellungen: 'reserve_pool_size' und 'reserve_pool_timeout'.
    Wenn Clients im Pool länger als 'reserve_pool_timeout' Sekunden gewartet haben,
    legt 'reserve_pool_size' fest, wie viele Verbindungen zum Pool hinzugefügt
    werden können. Der Wert kann mit der Verbindungsvariable 'reserve_pool'
    auch pro Pool gesetzt werden.

  * Neue Einstellung 'sbuf_loopcnt', um die für einen Socket aufgewendete Zeit zu begrenzen.

    Unter bestimmten Bedingungen, etwa auf einem SMP-Server mit lokalem PostgreSQL
    und schnellem Netzwerk, kann PgBouncer die recv()->send()-Schleife oft
    durchlaufen, ohne auf einer Seite zu blockieren. Dadurch warten jedoch
    andere Verbindungen lange. Für eine fairere Verarbeitung die Anzahl der
    recv()->send()-Durchläufe für einen Socket begrenzen. Wird die Grenze erreicht,
    mit der Verarbeitung anderer Sockets fortfahren. Die Verarbeitung dieses Sockets
    wird in der nächsten Ereignisschleife fortgesetzt.

    Dank an Alexander Schöcke für den Bericht und die Tests.

  * crypt()-Authentifizierung ist jetzt optional, da sie aus PostgreSQL entfernt wurde.
    Falls das Betriebssystem sie nicht bereitstellt, funktioniert PgBouncer auch ohne sie.

  * Millisekunden zu Zeitstempeln im Protokoll hinzufügen.

  * Alte MD5-Implementierung durch eine kompaktere ersetzen.

  * ISC-Lizenz um die Klarstellung der FSF ergänzen.

- Fehlerbehebungen

  * Meldet event_del() einen Fehler, die Bereinigung einfach fortsetzen.
    Zuvor versuchte PgBouncer den Aufruf erneut, falls ENOMEM die Ursache war.
    Dies führte jedoch zu endlos wiederholten Protokollmeldungen;
    offenbar kommt libevent damit nicht zurecht.

    Weshalb event_del() beim ersten Aufruf einen Fehler meldet, ist weiterhin unklar.

  * --enable-debug legt jetzt lediglich fest, ob Debug-Informationen aus der Binärdatei entfernt werden.
    Die Option beeinflusst -fomit-frame-pointer nicht mehr, da dies gefährlich ist.

  * Reihenfolge der Include-Dateien korrigiert, da andernfalls System-Includes
    vor den internen eingebunden werden konnten. Dies war bei der neuen Datei md5.h ein Problem.

  * Datei COPYRIGHT in .tgz aufnehmen ...

--------

## PgBouncer 1.2.x {#pgbouncer-12x}

**2008-08-08  -  PgBouncer 1.2.3  -  „Sorgfältig ausgewählte Bytes“**

- Fehlerbehebungen
  * Nicht funktionierenden SO_ACCEPTFILTER-Code für BSDs deaktiviert.
  * Beispieldatei etc/userlist.txt in tgz aufnehmen.
  * Bei rekursiven Aufrufen '$(MAKE)' statt 'make' verwenden. (Jørgen Austvik)
  * _GNU_SOURCE definieren, da glibc sonst unbrauchbar ist.
  * libevent 1.1 den Linktest bestehen lassen, damit später "1.3b+ needed" gemeldet werden kann.
  * Veraltete PID-Datei erkennen und entfernen.

Dank an Devrim GÜNDÜZ und Bjoern Metzdorf für Problemberichte und Tests.

**2008-08-06  -  PgBouncer 1.2.2  -  „Spuckbeutel inbegriffen“**

- Fehlerbehebungen
  * 'drop_on_error' entfernt; es war keine gute Idee. Die Einstellung wurde als
    Übergangslösung für das fehlerhafte Verhalten des Plancaches in PostgreSQL eingeführt,
    kann jedoch im üblichen Fall, dass bestimmte Abfragen immer einen Fehler zurückgeben, Schäden verursachen.

**2008-08-04  -  PgBouncer 1.2.1  -  „Wasserdicht“**

- Funktionen
  * Neuer Parameter 'drop_on_error': Wenn der Server einen Fehler meldet, wird die Verbindung
    nicht wiederverwendet, sondern getrennt, sobald der Client sie nicht mehr benötigt.
    Dies ist zum Aktualisieren des Plancaches erforderlich. Die automatische Aktualisierung funktioniert auch in 8.3 nicht.
    Der Standardwert ist 1.
- Fehlerbehebungen
  * SHOW SOCKETS/CLIENTS/SERVERS: Nicht abstürzen, wenn ein Socket keinen Puffer hat.
  * Endlosschleife bei SUSPEND behoben, wenn suspend_timeout ausgelöst wird.
- Kleinere Bereinigungen
  * <sys/uio.h> für 'struct iovec' verwenden.
  * Herunterfahren (durch SIGINT) bei RESUME/SIGUSR2 abbrechen,
    da es sonst beim nächsten PAUSE ausgelöst würde.
  * Korrekte Protokollmeldung, wenn ein Konsolenvorgang abgebrochen wird.

**2008-07-29  -  PgBouncer 1.2  -  „Gewöhnliche Zauberflöte“**

PgBouncer 1.2 benötigt jetzt libevent-Version 1.3b oder neuer.
Ältere libevent-Versionen stürzen mit dem neuen Neustartcode ab.

- Funktionen

  * Befehlszeilenoption (-u) und Konfigurationsparameter (user=) für den
    Benutzerwechsel beim Start. Außerdem verweigert PgBouncer jetzt die Ausführung als root.

    (Jacob Coby)

  * Aussagekräftigere Hilfeausgabe (-h). (Jacob Coby)

  * Neue Datenbankoption: connect_query ermöglicht eine Abfrage auf neuen
    Verbindungen, bevor diese verwendet werden.

    (Teodor Sigaev)

  * Neue Konfigurationsvariable 'ignore_startup_parameters', mit der zusätzliche
    Parameter im Startpaket zugelassen und ignoriert werden können. Standardmäßig
    sind nur 'database' und 'user' zulässig; alle anderen führen zu einem Fehler.
    Dies ist erforderlich, um übermäßig eifriges JDBC zu tolerieren, das
    'extra_float_digits=2' bedingungslos im Startpaket setzen möchte.

  * Protokollierung über syslog: neue Parameter syslog=0/1 und
    syslog_facility=daemon/user/local0.

  * Weniger riskanter Online-Neustart (-R)

    - Laden der FD vor fork ausführen, damit die Ausgabe auf der Konsole erfolgt und der Vorgang mit ^C abgebrochen werden kann.

    - SHUTDOWN nach fork belassen, damit ^C unbedenklich ist.

    - Ein connect() auf den Unix-Socket prüft, ob dort ein Prozess lauscht.
      Jetzt kann -R auch verwendet werden, wenn zuvor kein Prozess lief.
      Läuft bereits ein Prozess, wird aber -R nicht verwendet, schlägt der Start fehl.

  * Neue Konsolenbefehle:

    - SHOW TOTALS zeigt die Statistikzusammenfassung wie im Protokoll sowie den Speicherverbrauch.

    - SHOW ACTIVE_SOCKETS: Wie show sockets, jedoch auf aktive Sockets beschränkt.

- Weniger sichtbare Funktionen

  * suspend_timeout: Blockierte Verbindungen und langwierige Anmeldungen abbrechen.
    Dies erhöht die Sicherheit bei Neustarts.

  * Clients benachrichtigen, wenn die entfernte Datenbank bei der Anmeldung einen Fehler meldet.

  * Eine Datenbank aus der Konfiguration zu entfernen und neu zu laden funktioniert:
    Alle Verbindungen werden getrennt und die Datenbank wird entfernt.

  * Bei den Konsolenbefehlen SHOW/SET einige Parameter nachbilden, um PostgreSQL ähnlicher zu sein.
    Dies war erforderlich, damit psycopg eine Verbindung zur Konsole herstellen kann.
    (client_encoding/default_transaction_isolation/datestyle/timezone)

  * Mit server_lifetime=0 die Serververbindung sofort nach der ersten Verwendung
    trennen. Zuvor bewirkte "0", dass PgBouncer das Alter des Servers ignorierte.
    Da dieses Verhalten nicht dokumentiert war, sollte niemand
    darauf angewiesen sein.

  * Interne Verbesserungen:

    - Paketpuffer werden erst bei Bedarf zugewiesen und wiederverwendet.
      Dies sollte den Speicherverbrauch erheblich senken. Damit wird es auch praktikabel,
      bei vielen Verbindungen große pktbuf zu verwenden.

    - Zahlreiche Verbesserungen bei der Fehlerbehandlung. PgBouncer sollte
      OOM-Situationen jetzt geordnet bewältigen.

    - Slab-Allokator für die Speicherverwaltung verwenden.

    - Zahlreiche Codebereinigungen.

- Fehlerbehebungen

  * Bisher wurde pro Ereignisschleife nur ein accept() ausgeführt. Bei vielen
    Verbindungsversuchen konnte sich dadurch ein Rückstau aufbauen.
    Jetzt werden vom lauschenden Socket immer alle ausstehenden Verbindungen angenommen,
    was das Problem beheben sollte.
  * EINTR von connect() behandeln.
  * configure.ac mit autoconf 2.59 kompatibel machen.
  * Kompatibilitätskorrekturen für Solaris (Magne Mæhre)

--------

## PgBouncer 1.1.x {#pgbouncer-11x}

**2007-12-10  -  PgBouncer 1.1.2  -  „Der Hammer“**

- Funktionen
  * Verbindungstrennungen aufgrund von server_lifetime erfolgen jetzt im Abstand
    von (server_lifetime / pool_size) Sekunden. Dadurch löst PgBouncer
    keine Flut von Neuverbindungen aus.
- Fehlerbehebungen
  * Probleme beim Online-Upgrade von 1.0 -> 1.1:
    - 1.0 verfolgt Serverparameter nicht nach, sodass sie NULL bleiben.
      1.1 rechnete damit jedoch nicht und stürzte ab.
    - Sind Serverparameter unbekannt, aber entsprechende Clientparameter gesetzt,
      ein SET dafür ausführen, statt einen Fehler zu melden.
  * Vorübergehende Debug-Anweisungen entfernt, die versehentlich auf Stufe INFO
    im Code verblieben waren und die Protokolle füllten.
  * debian/changelog repariert.
- Bereinigung
  * Felder von struct SBuf für eine bessere Ausrichtung des Puffers neu anordnen.

**2007-10-26  -  PgBouncer 1.1.1  -  „Breakdance-Biene“**

- Fehlerbehebungen
  * Der Cache für Serverparameter konnte uninitialisiert bleiben, wodurch
    unnötige SET-Anweisungen ausgeführt wurden. Dies führte unter 8.1 zu Problemen,
    da standard_conforming_strings dort nicht verändert werden darf.
    (Dank an Dimitri Fontaine für Bericht und Tests.)
  * Einige Dokumentationsfehler korrigiert.
  * doc/fixman.py in .tgz aufnehmen.

**2007-10-09  -  PgBouncer 1.1  -  „Werkzeugkasten mit verrücktem Hut“**

- Funktionen

  * Folgende Serverparameter nachverfolgen:

        client_encoding  datestyle, timezone, standard_conforming_strings

  * Erweiterungen der Datenbank-Verbindungszeichenfolge:

    - Hostnamen in host= akzeptieren.
    - Benutzerdefinierten Unix-Socket-Pfad in host= akzeptieren.
    - Werte in Anführungszeichen akzeptieren: password=' asd''foo'

  * Neue Konfigurationsvariable: server_reset_query wird unmittelbar nach der Freigabe gesendet.
  * Neue Konfigurationsvariable: server_round_robin zum Umschalten zwischen LIFO und RR.
  * Ein Abbruchpaket für eine inaktive Verbindung trennt diese nicht mehr.
  * Abbruch mit ^C aus psql funktioniert für SUSPEND / PAUSE.
  * FD-Grenzen beim Start ausgeben.
  * Beim Suspendieren möglichst schnell eine Paketgrenze erreichen.
  * 'timezone' zu den Datenbankparametern hinzufügen.
  * Dateideskriptor der Protokolldatei dauerhaft offen halten. Er wird bei SIGHUP / RELOAD erneut geöffnet.
  * Informationen zum lokalen Verbindungsendpunkt in SHOW SERVERS/CLIENTS/SOCKETS.

- Codebereinigung

  * Mehr Debug-Protokollmeldungen enthalten Socket-Informationen.
  * Magische Zahlen entfernt und Fehlermeldungen bereinigt. (David Fetter)
  * Wrapper-Struktur für Informationen zum aktuellen Paket. Dies verringert die Komplexität erheblich.

- Fehlerbehebungen

  * Ungültige Paketheader besser erkennen.
  * Die Prüfung auf Änderungen an auth_file war fehlerhaft, wodurch
    PgBouncer die Datei zu häufig neu lud.

--------

## PgBouncer 1.0.x {#pgbouncer-10x}

**2007-06-18  -  PgBouncer 1.0.8  -  „Jutsu der untoten Schaufel“**

- Fehlerbehebungen
  * Absturz bei der Verarbeitung von Abbruchpaketen behoben. (^C aus psql)
- Funktionen
  * PAUSE <db>; RESUME <db>; funktioniert jetzt.
  * Parsing der Konsolenbefehle bereinigt.
  * Aufwendige Assertion-Prüfung auf Listenzugehörigkeit deaktiviert.

**2007-04-19  -  PgBouncer 1.0.7  -  „Mit Vitamin A-Z“**

- Fehlerbehebungen
  * Mehrere Fehler-/Hinweispakete, zwischen denen send() blockierte,
    lösten eine Assertion aus. Durch vollständiges Entfernen der Flush-Logik behoben.
    Da PgBouncer selbst nichts aktiv puffert, ist sie nicht erforderlich.
    Sie stammte noch aus der Zeit, als die Pufferung mit MSG_MORE
    in den Kernel verlagert wurde.
  * Außerdem vermeiden, die recv()-Logik aufzurufen, wenn das Senden nicht mehr blockiert.
  * Der Listensuchcode für admin_users und stats_users behandelte
    Teiltreffer falsch. Dies wurde korrigiert.
  * Ermittlung der UID des Unix-Socket-Peers auf getpeereid() vereinheitlicht.

**2007-04-12  -  PgBouncer 1.0.6  -  „Tägliche Dosis“**

- Fehlerbehebungen
  * Die Korrektur zur Deaktivierung der Wartung während der Übernahme konnte
    die Wartung vollständig deaktivieren. Dies wurde behoben.
  * Kompilierung unter FreeBSD korrigiert: <sys/ucred.h> benötigt dort <sys/param.h>.
    Dank an Robert Gogolok für den Bericht.

**2007-04-11  -  PgBouncer 1.0.5  -  „Genug für heute“**

- Fehlerbehebungen
  * Fehler beim Online-Neustart behoben:
    - ->ready für inaktive Server setzen.
    - Veralteten Code aus use_client_socket() entfernen.
    - Wartung während der Übernahme deaktivieren.

**2007-04-11  -  PgBouncer 1.0.4  -  „Der letzte ‚letzte‘ Fehler“**

- Fehlerbehebungen
  * Ein Hinweis von einem inaktiven Server markierte diesen als nicht bereinigt.
    release_server() rechnete damit nicht. Das Problem wurde durch
    Verwerfen behoben.

**2007-04-11  -  PgBouncer 1.0.3  -  „Furchtloser Fork“**

- Fehlerbehebungen
  * Im Anmeldepfad fehlte teilweise die Fehlerbehandlung, sodass eine dort
    abbrechende Verbindung Assertions auslösen konnte.
  * Assertions in sbuf.c bereinigt, um Probleme früher zu erkennen.
  * Core-Dump erzeugen, wenn Assert() auslöst.

- Neuerungen
  * Neue Konfigurationsvariablen: log_connections, log_disconnections,
    log_pooler_errors zum Ein- und Ausschalten ausführlicher Protokollausgaben.
  * Konfigurationsvariable: client_login_timeout zum Trennen nicht mehr reagierender
    Verbindungen während der Anmeldung, die SUSPEND und damit den Online-Neustart blockieren könnten.

**2007-03-28  -  PgBouncer 1.0.2  -  „Überschalllöffel“**

- Fehlerbehebungen
  * libevent kann innerhalb derselben Schleife ein bereits gelöschtes Ereignis melden.
    Die Wiederverwendung des Sockets für einen Schleifendurchlauf verhindern.
  * release_server() aus disconnect_client() prüfte nicht,
    ob das Paket tatsächlich gesendet worden war.

**2007-03-15  -  PgBouncer 1.0.1  -  „Außerirdische Technologie“**

- Fehlerbehebungen
  * Die gemischte Verwendung zwischengespeicherter und nicht zwischengespeicherter Zeitwerte
    sowie ein vorzeichenloser usec_t-typedef führten zu unbegründeten query_timeout-Fehlern.
  * Seltenen Fall behoben, bei dem ein Socket nach dem Aufwecken aus dem Warten auf das Senden blockiert bleiben konnte.
  * Fairere Warteschlangen für Serververbindungen. Zuvor konnte eine neue Abfrage
    vor einer älteren eine Serververbindung erhalten.
  * Freigabe des Servers verzögern, bis garantiert alles gesendet wurde.

- Funktionen
  * Befehl SHOW SOCKETS für detaillierte Zustandsinformationen.
  * PgSocket-Zeiger ins Protokoll aufnehmen, um einzelne Verbindungen leichter nachzuverfolgen.
  * In der Konsole SELECT anstelle von SHOW zulassen.
  * Verschiedene Codebereinigungen.

**2007-03-13  -  PgBouncer 1.0  -  „Getunter BMW“**

- Erste öffentliche Version.
