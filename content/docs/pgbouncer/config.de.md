---
title: "Konfiguration: pgbouncer.ini"
linkTitle: "Konfiguration"
weight: 20
description: "Referenz zur PgBouncer-Konfigurationsdatei (pgbouncer.ini)"
icon: fa-solid fa-code
module: [PGBOUNCER]
categories: [Referenz]
aliases: [/pgbouncer/config/]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/doc/config.md"
---

--------

## Beschreibung {#description}

Die Konfigurationsdatei verwendet das „ini“-Format. Abschnittsnamen stehen zwischen `[` und `]`. Zeilen, die mit `;` oder `#` beginnen, werden als Kommentare betrachtet und ignoriert. Treten die Zeichen `;` und `#` später in einer Zeile auf, haben sie keine besondere Bedeutung.

--------

## Allgemeine Einstellungen {#generic-settings}

### logfile {#logfile}

Gibt die Protokolldatei an. Für den Daemon-Betrieb (`-d`) muss entweder diese Einstellung oder `syslog` gesetzt sein.

Die Protokolldatei bleibt geöffnet. Nach einer Rotation sollte daher `kill -HUP` oder in der Konsole `RELOAD;` ausgeführt werden. Unter Windows muss der Dienst gestoppt und wieder gestartet werden.

Das Setzen von `logfile` allein schaltet die Protokollierung auf stderr nicht ab. Dazu dient die Befehlszeilenoption `-q` oder `-d`.

Standard: nicht gesetzt

### pidfile {#pidfile}

Gibt die PID-Datei an. Ohne gesetztes `pidfile` ist der Daemon-Betrieb (`-d`) nicht zulässig.

Standard: nicht gesetzt

### listen_addr {#listen_addr}

Gibt eine durch Kommas getrennte Liste von Adressen an, an denen auf TCP-Verbindungen gewartet wird. Mit `*` kann auf allen Adressen gewartet werden. Ist die Einstellung nicht gesetzt, werden nur Verbindungen über Unix-Sockets angenommen.

Adressen können numerisch (IPv4/IPv6) oder als Name angegeben werden.

Standard: nicht gesetzt

### listen_port {#listen_port}

Port, an dem auf Verbindungen gewartet wird. Gilt sowohl für TCP als auch für Unix-Sockets.

Standard: 6432

### unix_socket_dir {#unix_socket_dir}

Gibt das Verzeichnis für Unix-Sockets an. Gilt sowohl für den lauschenden Socket als auch für Serververbindungen. Bei einer leeren Zeichenfolge sind Unix-Sockets deaktiviert. Ein mit `@` beginnender Wert legt fest, dass ein Unix-Socket im abstrakten Namensraum erstellt werden soll (derzeit unter Linux und Windows unterstützt).

Standard: `/tmp` (unter Windows leer)

### unix_socket_mode {#unix_socket_mode}

Dateisystemmodus für Unix-Sockets. Wird für Sockets im abstrakten Namensraum ignoriert. Unter Windows nicht unterstützt.

Standard: 0777

### unix_socket_group {#unix_socket_group}

Gruppenname für Unix-Sockets. Wird für Sockets im abstrakten Namensraum ignoriert. Unter Windows nicht unterstützt.

Standard: nicht gesetzt

### user {#user}

Falls gesetzt, gibt diese Einstellung den Unix-Benutzer an, zu dem nach dem Start gewechselt wird. Funktioniert nur, wenn PgBouncer als root gestartet wird oder bereits unter dem angegebenen Benutzer läuft. Unter Windows nicht unterstützt.

Standard: nicht gesetzt

### pool_mode {#pool_mode}

Legt fest, wann eine Serververbindung von anderen Clients wiederverwendet werden kann.

- **`session`**: Die Serververbindung wird an den Pool zurückgegeben, nachdem der Client die Verbindung getrennt hat. Standard.
- **`transaction`**: Die Serververbindung wird nach Abschluss der Transaktion an den Pool zurückgegeben.
- **`statement`**: Die Serververbindung wird nach Abschluss der Abfrage an den Pool zurückgegeben. Transaktionen über mehrere Anweisungen sind in diesem Modus nicht zulässig.

### max_client_conn {#max_client_conn}

Maximal zulässige Anzahl von Clientverbindungen.

Wird diese Einstellung erhöht, müssen möglicherweise auch die Grenzen für Dateideskriptoren im Betriebssystem erhöht werden. Die Anzahl der potenziell verwendeten Dateideskriptoren liegt über `max_client_conn`. Verbindet sich jeder Benutzer unter seinem eigenen Benutzernamen mit dem Server, beträgt das theoretische Maximum:

```text
max_client_conn + (max pool_size * total databases * total users)
```

Wird in der Verbindungszeichenfolge ein Datenbankbenutzer angegeben (alle Benutzer verbinden sich unter demselben Benutzernamen), beträgt das theoretische Maximum:

```text
max_client_conn + (max pool_size * total databases)
```

Das theoretische Maximum sollte nie erreicht werden, sofern nicht gezielt eine spezielle Last dafür erzeugt wird. Dennoch sollte die Grenze für Dateideskriptoren ausreichend hoch angesetzt werden.

Suchen Sie in der Handbuchseite Ihrer bevorzugten Shell nach `ulimit`. Hinweis: `ulimit` gilt nicht in einer Windows-Umgebung.

Standard: 100

### default_pool_size {#default_pool_size}

Maximal zulässige Anzahl von Serververbindungen pro Benutzer/Datenbank-Paar. Kann durch `pool_size` in der datenbank- und benutzerspezifischen Konfiguration überschrieben werden; dieser Standardwert wird verwendet, wenn für eine bestimmte Datenbank oder einen bestimmten Benutzer kein eigener Wert für `pool_size` angegeben ist.

Standard: 20

### min_pool_size {#min_pool_size}

Fügt dem Pool weitere Serververbindungen hinzu, wenn ihre Anzahl unter diesem Wert liegt. Verbessert das Verhalten, wenn nach einer Phase völliger Inaktivität plötzlich wieder die normale Last einsetzt. Der Wert wird effektiv auf die Poolgröße begrenzt.

Wird nur für Pools durchgesetzt, für die mindestens eine der folgenden Bedingungen zutrifft:

* Im Eintrag des Pools im Abschnitt `[databases]` ist für den Schlüssel `user` ein Wert gesetzt (ein sogenannter erzwungener Benutzer).
* Mindestens ein Client ist mit dem Pool verbunden.

Standard: 0 (deaktiviert)

### reserve_pool_size {#reserve_pool_size}

Anzahl zusätzlicher Verbindungen, die für einen Pool zugelassen werden (siehe `reserve_pool_timeout`). 0 deaktiviert diese Funktion.

Standard: 0 (deaktiviert)

### reserve_pool_timeout {#reserve_pool_timeout}

Wurde ein Client innerhalb dieser Zeit nicht bedient, werden zusätzliche Verbindungen aus dem Reservepool verwendet. 0 deaktiviert diese Funktion. [Sekunden]

Standard: 5.0

### max_db_connections {#max_db_connections}

Lässt pro Datenbank höchstens diese Anzahl von Serververbindungen zu (unabhängig vom Benutzer). Maßgeblich ist die PgBouncer-Datenbank, mit der sich der Client verbunden hat, nicht die PostgreSQL-Datenbank der ausgehenden Verbindung.

Kann auch pro Datenbank im Abschnitt `[databases]` gesetzt werden.

Ist die Grenze erreicht, ermöglicht das Schließen einer Clientverbindung zu einem Pool nicht sofort eine neue Serververbindung für einen anderen Pool, da die Serververbindung des ersten Pools noch geöffnet ist. Sobald diese Serververbindung geschlossen wird (wegen Überschreitung der Leerlaufzeit), wird unmittelbar eine neue Serververbindung für den wartenden Pool geöffnet.

Standard: 0 (unbegrenzt)

### max_db_client_connections {#max_db_client_connections}

Lässt pro Datenbank höchstens diese Anzahl von Clientverbindungen zu PgBouncer zu (unabhängig vom Benutzer). Maßgeblich ist die PgBouncer-Datenbank, mit der sich der Client verbunden hat, nicht die PostgreSQL-Datenbank der ausgehenden Verbindung.

Dieser Wert sollte mindestens so groß wie max_db_connections sein. Die Differenz zwischen den beiden Werten lässt sich als Anzahl der Verbindungen zu einer bestimmten Datenbank verstehen, die in der Warteschlange auf den Abschluss aktiver Verbindungen warten können.

Kann auch pro Datenbank im Abschnitt `[databases]` gesetzt werden.

Standard: 0 (unbegrenzt)

### max_user_connections {#max_user_connections}

Lässt pro Benutzer höchstens diese Anzahl von Serververbindungen zu (unabhängig von der Datenbank). Maßgeblich ist der dem Pool zugeordnete PgBouncer-Benutzer: entweder der für die Serververbindung angegebene Benutzer oder, falls keiner angegeben ist, der Benutzer, als der sich der Client verbunden hat.

Kann auch pro Benutzer im Abschnitt `[users]` gesetzt werden.

Ist die Grenze erreicht, ermöglicht das Schließen einer Clientverbindung zu einem Pool nicht sofort eine neue Serververbindung für einen anderen Pool, da die Serververbindung des ersten Pools noch geöffnet ist. Sobald diese Serververbindung geschlossen wird (wegen Überschreitung der Leerlaufzeit), wird unmittelbar eine neue Serververbindung für den wartenden Pool geöffnet.

Standard: 0 (unbegrenzt)

### max_user_client_connections {#max_user_client_connections}

Lässt pro Benutzer höchstens diese Anzahl von Clientverbindungen zu (unabhängig von der Datenbank). Dieser Wert sollte größer als max_user_connections sein. Die Differenz zwischen max_user_connections und max_user_client_connections lässt sich als maximale Größe der Warteschlange für den Benutzer verstehen.

Kann auch pro Benutzer im Abschnitt `[users]` gesetzt werden.

Standard: 0 (unbegrenzt)

### server_round_robin {#server_round_robin}

Standardmäßig verwendet PgBouncer Serververbindungen nach dem LIFO-Prinzip (zuletzt hinein, zuerst heraus) wieder, sodass wenige Verbindungen den Großteil der Last tragen. Dies bietet die beste Leistung, wenn eine Datenbank von einem einzelnen Server bedient wird. Steht hinter einer Datenbankadresse jedoch ein Round-Robin-System (TCP, DNS oder eine Hostliste), ist es besser, wenn PgBouncer Verbindungen ebenfalls nach diesem Verfahren nutzt und so die Last gleichmäßig verteilt.

Standard: 0

### track_extra_parameters {#track_extra_parameters}

Standardmäßig verfolgt PgBouncer alle Parameter, die Postgres an den Client meldet und die der Client ändern kann:

- `application_name`
- `client_encoding`
- `DateStyle`
- `default_transaction_read_only`
- `IntervalStyle`
- `scram_iterations` (seit PostgreSQL-Version 16)
- `search_path` (seit PostgreSQL-Version 18)
- `session_authorization`
- `standard_conforming_strings`
- `TimeZone`

Weitere zu verfolgende Parameter können hier angegeben werden. PgBouncer weiß dann, dass sie im Variablencache des Clients verwaltet und auf dem Server wiederhergestellt werden sollen, sobald der Client aktiv wird.

Mehrere Werte werden als durch Kommas getrennte Liste angegeben (z. B. `some_extension.setting, other_extension.setting`).

Hinweis: Die meisten Parameter lassen sich auf diese Weise nicht vollständig verfolgen. PgBouncer erfährt nur bei Parametern, die Postgres an den Client meldet, von Änderungen durch `SET`. Postgres stellt [eine offizielle Liste der an den Client gemeldeten Parameter](https://www.postgresql.org/docs/current/protocol-flow.html#PROTOCOL-ASYNC) bereit. Postgres-Erweiterungen können diese Liste jedoch ändern: Sie können eigene Parameter hinzufügen und melden sowie die Meldung bereits vorhandener Parameter veranlassen, die Postgres selbst nicht meldet. Insbesondere bewirkt Citus 12.0+, dass Postgres auch `search_path` meldet. Auch einige der standardmäßig verfolgten Parameter werden erst von neueren Postgres-Versionen gemeldet: `default_transaction_read_only` seit Postgres 14, `scram_iterations` seit Postgres 16 und `search_path` seit Postgres 18.

Bei einem verfolgten Parameter, den Postgres nicht meldet (z. B. `search_path` in Postgres-Versionen vor 18), kennt PgBouncer nur den Wert, den ein Client in seinem Startpaket (oder im Startparameter `options`) angegeben hat. Dieser Wert wird auf die Serververbindung angewendet, sobald der Client aktiv wird. Für Clients, die ihn nicht angegeben haben, wird der Parameter auf seinen Standardwert zurückgesetzt. Änderungen durch `SET` nach dem Verbindungsaufbau werden bei solchen Parametern nicht verfolgt und wirken sich daher auf andere Clients aus, die dieselbe Serververbindung nutzen, sofern nicht `server_reset_query_always` verwendet wird.

Das Postgres-Protokoll erlaubt Parametereinstellungen sowohl direkt als Parameter im Startpaket als auch innerhalb des [Startpaketparameters `options`][options-startup]. `track_extra_parameters` unterstützt Parameter, die auf beide Arten angegeben werden. `options` selbst kann jedoch nicht in `track_extra_parameters` aufgenommen werden, sondern nur die in `options` enthaltenen Parameter.

Standard: leer

### ignore_startup_parameters {#ignore_startup_parameters}

Standardmäßig lässt PgBouncer in Startpaketen nur Parameter zu, die es verfolgen kann (die Liste steht unter `track_extra_parameters`). Alle anderen Parameter lösen einen Fehler aus. Weitere zulässige Parameter können hier angegeben werden. PgBouncer weiß dann, dass sie vom Administrator behandelt werden und ignoriert werden können.

Mehrere Werte werden als durch Kommas getrennte Liste angegeben (z. B. `options,extra_float_digits`).

Das Postgres-Protokoll erlaubt Parametereinstellungen sowohl direkt als Parameter im Startpaket als auch innerhalb des [Startpaketparameters `options`][options-startup]. `ignore_startup_parameters` unterstützt Parameter, die auf beide Arten angegeben werden. Auch `options` selbst kann in `ignore_startup_parameters` aufgenommen werden; dann werden alle unbekannten Parameter innerhalb von `options` ignoriert.

[options-startup]: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNECT-OPTIONS

Standard: leer

### peer_id {#peer_id}

Peer-ID, die diesen PgBouncer-Prozess innerhalb einer Gruppe miteinander verbundener PgBouncer-Prozesse identifiziert. Der Wert von `peer_id` sollte innerhalb einer solchen Gruppe eindeutig sein. Bei 0 ist PgBouncer-Peering deaktiviert. Weitere Informationen enthält die Dokumentation zum Abschnitt `[peers]`. Der Höchstwert für `peer_id` ist 16383.

Standard: 0

### disable_pqexec {#disable_pqexec}

Deaktiviert das Protokoll Simple Query (PQexec). Anders als das Protokoll Extended Query erlaubt Simple Query mehrere Abfragen in einem Paket, was bestimmte Arten von SQL-Injection-Angriffen ermöglicht. Die Deaktivierung kann die Sicherheit erhöhen. Das bedeutet allerdings, dass nur Clients weiter funktionieren, die ausschließlich das Protokoll Extended Query verwenden.

Standard: 0

### application_name_add_host {#application_name_add_host}

Fügt die Hostadresse und den Port des Clients zu dem Anwendungsnamen hinzu, der beim Verbindungsaufbau gesetzt wird. Dies hilft, die Herkunft problematischer Abfragen usw. zu ermitteln. Die Logik greift nur beim Verbindungsaufbau. Wird `application_name` später mit `SET` geändert, passt PgBouncer den Wert nicht erneut an.

Standard: 0

### conffile {#conffile}

Zeigt den Pfad der aktuellen Konfigurationsdatei an. Wird er geändert, verwendet PgBouncer beim nächsten `RELOAD` / `SIGHUP` eine andere Konfigurationsdatei.

Standard: Datei aus der Befehlszeile

### service_name {#service_name}

Wird bei der Registrierung eines win32-Dienstes verwendet.

Standard: `pgbouncer`

### job_name {#job_name}

Alias für `service_name`.

### stats_period {#stats_period}

Legt fest, wie oft die in verschiedenen `SHOW`-Befehlen angezeigten Durchschnittswerte aktualisiert und wie oft aggregierte Statistiken ins Protokoll geschrieben werden (siehe jedoch `log_stats`). [Sekunden]

Standard: 60

### max_prepared_statements {#max_prepared_statements}

Bei einem Wert ungleich null verfolgt PgBouncer im Transaktions- und Statement-Pooling die vom Client gesendeten Befehle für benannte vorbereitete Anweisungen auf Protokollebene. PgBouncer stellt sicher, dass jede von einem Client vorbereitete Anweisung auf der zugehörigen Serververbindung verfügbar ist, auch wenn die Anweisung ursprünglich auf einer anderen Serververbindung vorbereitet wurde.

PgBouncer untersucht intern alle Abfragen, die Clients als vorbereitete Anweisung senden, und weist jeder eindeutigen Abfragezeichenfolge einen internen Namen im Format `PGBOUNCER_{unique_id}` zu. Wird dieselbe Abfragezeichenfolge mehrfach vorbereitet (möglicherweise von unterschiedlichen Clients), teilen sich diese Abfragen denselben internen Namen. PgBouncer bereitet die Anweisung auf dem eigentlichen PostgreSQL-Server ausschließlich unter dem internen Namen vor (also nicht unter dem vom Client angegebenen Namen). PgBouncer merkt sich den Namen, den der Client jeder vorbereiteten Anweisung gegeben hat. Vor der Weiterleitung an den Server schreibt es dann jeden Befehl, der eine vorbereitete Anweisung verwendet, um: Der clientseitige Name wird durch den internen Namen ersetzt (z. B. `my_prepared_statement` durch `PGBOUNCER_123`). Wichtiger noch: Ist die vom Client auszuführende Anweisung auf dem Server noch nicht vorbereitet (z. B. weil dem Client inzwischen ein anderer Server zugewiesen wurde als beim Vorbereiten), bereitet PgBouncer sie transparent vor der Ausführung vor.

Hinweis: Diese Nachverfolgung und Umschreibung von Befehlen für vorbereitete Anweisungen funktioniert nicht für entsprechende SQL-Befehle. `PREPARE`, `EXECUTE` und `DEALLOCATE` werden daher direkt an Postgres weitergeleitet. Ausgenommen sind die Befehle `DEALLOCATE ALL` und `DISCARD ALL`: Sie funktionieren wie erwartet und löschen die vorbereiteten Anweisungen, die PgBouncer für den Client verfolgt hat, der den Befehl sendet.

Der konkrete Wert dieser Einstellung steuert die Anzahl vorbereiteter Anweisungen, die in einem LRU-Cache auf einer einzelnen Serververbindung aktiv gehalten werden. Bei 0 ist die Unterstützung vorbereiteter Anweisungen für Transaktions- und Statement-Pooling deaktiviert. Für die beste Leistung sollte dieser Wert größer sein als die Anzahl der in der Anwendung häufig verwendeten vorbereiteten Anweisungen. Je höher der Wert, desto größer ist der Speicherbedarf jeder PgBouncer-Verbindung auf dem PostgreSQL-Server, da mehr Abfragen auf diesen Verbindungen vorbereitet bleiben. Auch der Speicherbedarf von PgBouncer selbst steigt, da es nun Abfragezeichenfolgen verwalten muss.

Die Auswirkungen auf den Speicherbedarf von PgBouncer sind jedoch nicht sehr groß:
- Jede eindeutige Abfrage wird einmal in einem globalen Abfragecache gespeichert.
- Jede Clientverbindung hält einen Puffer vor, mit dem Pakete umgeschrieben werden. Dieser ist höchstens 4-mal so groß wie `pkt_buf`. Diese Grenze wird allerdings oft nicht erreicht; sie tritt nur auf, wenn die Abfragen in den vorbereiteten Anweisungen zwischen 2- und 4-mal so groß wie `pkt_buf` sind.

Als Beispielszenario seien folgende Bedingungen angenommen:
- Es gibt 1000 aktive Clients.
- Die Clients bereiten 200 eindeutige Abfragen vor.
- Die durchschnittliche Größe einer Abfrage beträgt 5kB.
- Der Parameter `pkt_buf` ist auf den Standardwert 4096 (4kB) gesetzt.

Dann benötigt PgBouncer höchstens folgende Speichermenge für diese vorbereiteten Anweisungen:

```text
200 x 5kB + 1000 x 4 x 4kB = ~17MB of memory.
```

Die Nachverfolgung vorbereiteter Anweisungen benötigt nicht nur Speicher, sondern erhöht auch die CPU-Auslastung, da PgBouncer die Abfragen untersuchen und umschreiben muss. Mehrere PgBouncer-Instanzen können am selben Port lauschen, um mehr als einen Prozessorkern für die Verarbeitung zu nutzen. Einzelheiten enthält [die Dokumentation zur Option `so_reuseport`](#so_reuseport).

Vorbereitete Anweisungen bieten natürlich auch Leistungsvorteile. Wie bei einer direkten Verbindung zu PostgreSQL verringert das Vorbereiten einer häufig ausgeführten Abfrage den gesamten Aufwand für Parsing und Planung. Die Art, wie PgBouncer vorbereitete Anweisungen verfolgt, ist für die Leistung besonders vorteilhaft, wenn mehrere Clients dieselben Abfragen vorbereiten: Clientverbindungen verwenden eine vorbereitete Anweisung auf einer Serververbindung automatisch wieder, selbst wenn ein anderer Client sie vorbereitet hat. Bei einer `pool_size` von 20 und 100 Clients, die alle exakt dieselbe Abfrage vorbereiten, wird die Abfrage auf dem PostgreSQL-Server beispielsweise nur 20-mal vorbereitet (und damit geparst).

Die Wiederverwendung vorbereiteter Anweisungen hat einen Nachteil. Ändern sich die Rückgabe- oder Argumenttypen einer vorbereiteten Anweisung zwischen Ausführungen, gibt PostgreSQL derzeit einen Fehler wie den folgenden aus:

```text
ERROR:  cached plan must not change result type
```

Solche Fehler lassen sich vermeiden, indem sichergestellt wird, dass mehrere Clients bei exakt derselben Abfragezeichenfolge in einer vorbereiteten Anweisung keine unterschiedlichen Argument- oder Ergebnistypen erwarten. Eine der häufigsten Situationen, in denen dieses Problem auftritt, ist eine DDL-Migration, bei der einer vorhandenen Tabelle eine Spalte hinzugefügt oder ein Spaltentyp geändert wird. In diesen Fällen kann nach der Migration `RECONNECT` in der PgBouncer-Administrationskonsole ausgeführt werden, um ein erneutes Vorbereiten der Abfrage zu erzwingen und den Fehler zu beheben.

Standard: 200

### scram_iterations {#scram_iterations}

Anzahl der Recheniterationen beim Hashen eines Passworts mit SCRAM-SHA-256. Eine höhere Iterationszahl schützt gespeicherte Passwörter zusätzlich vor Brute-Force-Angriffen, verlangsamt jedoch die Authentifizierung.

Standard: 4096

--------

## Authentifizierungseinstellungen {#authentication-settings}

PgBouncer führt die Clientauthentifizierung selbst durch und hat eine eigene Benutzerdatenbank. Die folgenden Einstellungen steuern dieses Verhalten.

### auth_type {#auth_type}

Art der Benutzerauthentifizierung.

- **`cert`**: Der Client muss sich über TLS mit einem gültigen Clientzertifikat verbinden. Der Benutzername wird dann dem Feld CommonName des Zertifikats entnommen.
- **`md5`**: Verwendet eine MD5-basierte Passwortprüfung. Dies ist die Standardmethode zur Authentifizierung. `auth_file` kann sowohl MD5-gehashte Passwörter als auch Klartextpasswörter enthalten. Ist `md5` konfiguriert und für einen Benutzer ein SCRAM-Secret hinterlegt, wird stattdessen automatisch SCRAM-Authentifizierung verwendet.
- **`scram-sha-256`**: Verwendet die Passwortprüfung mit SCRAM-SHA-256. `auth_file` muss SCRAM-Secrets oder Klartextpasswörter enthalten.
- **`plain`**: Das Passwort wird im Klartext über die Verbindung gesendet. Veraltet.
- **`trust`**: Es findet keine Authentifizierung statt. Der Benutzername muss dennoch in `auth_file` vorhanden sein.
- **`any`**: Wie die Methode `trust`, jedoch wird der angegebene Benutzername ignoriert. Alle Datenbanken müssen so konfiguriert sein, dass die Anmeldung als bestimmter Benutzer erfolgt. Außerdem erlaubt die Konsolendatenbank jedem Benutzer die Anmeldung als Statistikbenutzer; in `admin_users` aufgeführte Benutzer erhalten Administratorrechte.
- **`hba`**: Die tatsächliche Authentifizierungsmethode wird aus `auth_hba_file` geladen. Dies ermöglicht unterschiedliche Methoden für verschiedene Zugriffswege, etwa: Verbindungen über Unix-Sockets verwenden `peer`-Authentifizierung, Verbindungen über TCP müssen TLS verwenden.
- **`ldap`**: Benutzer werden wie in PostgreSQL über einen LDAP-Server authentifiziert (Einzelheiten unter <https://www.postgresql.org/docs/current/auth-ldap.html>). Die LDAP-Verbindungsoptionen werden mit der Einstellung `auth_ldap_options` oder alternativ in `auth_hba_file` konfiguriert.
- **`pam`**: Verwendet PAM zur Benutzerauthentifizierung; `auth_file` wird ignoriert. Diese Methode ist nicht mit Datenbanken kompatibel, die die Option `auth_user` verwenden. Der an PAM gemeldete Dienstname lautet "pgbouncer". `pam` wird in der HBA-Konfigurationsdatei nicht unterstützt.

### auth_hba_file {#auth_hba_file}

HBA-Konfigurationsdatei, die verwendet wird, wenn `auth_type` auf `hba` gesetzt ist. Einzelheiten enthält der Abschnitt [HBA-Dateiformat](#hba-file-format) weiter unten.

Standard: nicht gesetzt

### auth_ident_file {#auth_ident_file}

Datei mit Identitätszuordnungen, die verwendet wird, wenn `auth_type` auf `hba` gesetzt ist und eine Benutzerzuordnung definiert werden soll. Einzelheiten enthält der Abschnitt [Format der Ident-Zuordnungsdatei](#ident-map-file-format) weiter unten.

Standard: nicht gesetzt

### auth_file {#auth_file}

Name der Datei, aus der Benutzernamen und Passwörter geladen werden. Einzelheiten enthält der Abschnitt [Format der Authentifizierungsdatei](#authentication-file-format) weiter unten.

Die meisten Authentifizierungsmethoden (siehe oben) erfordern, dass entweder `auth_file` oder `auth_user` gesetzt ist; andernfalls wären keine Benutzer definiert.

Standard: nicht gesetzt

### auth_user {#auth_user}

Ist `auth_user` gesetzt, wird jeder nicht in `auth_file` aufgeführte Benutzer mithilfe von `auth_query` unter Verwendung von `auth_user` aus `pg_authid` in der Datenbank abgefragt. Das Passwort für `auth_user` wird aus `auth_file` entnommen. (Benötigt `auth_user` kein Passwort, muss der Benutzer nicht in `auth_file` definiert sein.)

Der direkte Zugriff auf `pg_authid` erfordert Administratorrechte. Vorzuziehen ist stattdessen ein Benutzer ohne Superuser-Rechte, der eine SECURITY DEFINER-Funktion aufruft.

Standard: nicht gesetzt

### auth_query {#auth_query}

Abfrage zum Laden des Benutzerpassworts aus der Datenbank.

Der direkte Zugriff auf `pg_authid` erfordert Administratorrechte. Vorzuziehen ist stattdessen ein Benutzer ohne Superuser-Rechte, der eine SECURITY DEFINER-Funktion aufruft.

Die Abfrage wird in der Zieldatenbank ausgeführt. Wird eine Funktion verwendet, muss sie daher in jeder Datenbank installiert sein.

Die Abfrage muss zwei Spalten zurückgeben: den Benutzernamen und das Passwort (geeignet verschlüsselt/gehasht). Um einen nicht vorhandenen Benutzer zu melden, entweder keine Zeilen oder eine Zeile mit einem Nullwert für den Benutzer zurückgeben. (Die nachfolgende Standardabfrage gibt für einen nicht vorhandenen Benutzer keine Zeilen zurück. Die Variante mit dem Nullwert ist nützlich, wenn die Abfrage eine Funktion mit einem Datensatz als Rückgabewert aufruft, wie im Beispiel unter [Beispiele](#examples) weiter unten.) Ein Nullwert in der Passwortspalte bedeutet, dass der Benutzer existiert, aber kein Passwort für ihn verfügbar ist; somit wird kein vom Client angebotenes Passwort akzeptiert.

Standard: `SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END FROM pg_authid WHERE rolname=$1 AND rolcanlogin`

### auth_dbname {#auth_dbname}

Name einer Datenbank im Abschnitt `[databases]`, die für die Authentifizierung verwendet werden soll. Diese Option kann global gesetzt oder durch Angabe dieses Parameters in der Verbindungszeichenfolge überschrieben werden.

### auth_ldap_options {#auth_ldap_options}

LDAP-Verbindungsoptionen, die verwendet werden, wenn `auth_type` auf `ldap` gesetzt ist. (Wird nicht verwendet, wenn die Authentifizierung über `auth_hba_file` konfiguriert ist.) Beispiel:

```ini
auth_ldap_options = ldapurl="ldap://127.0.0.1:12345/dc=example,dc=net?uid?sub"
```

--------

## Protokollierungseinstellungen {#log-settings}

### syslog {#syslog}

Schaltet syslog ein oder aus. Unter Windows wird stattdessen das Ereignisprotokoll verwendet.

Standard: 0

### syslog_ident {#syslog_ident}

Name, unter dem Meldungen an syslog gesendet werden.

Standard: `pgbouncer` (Programmname)

### syslog_facility {#syslog_facility}

Facility, unter der Meldungen an syslog gesendet werden. Mögliche Werte: `auth`, `authpriv`, `daemon`, `user`, `local0-7`.

Standard: `daemon`

### log_connections {#log_connections}

Protokolliert erfolgreiche Anmeldungen.

Standard: 1

### log_disconnections {#log_disconnections}

Protokolliert Verbindungstrennungen mit Angabe des Grundes.

Standard: 1

### log_pooler_errors {#log_pooler_errors}

Protokolliert Fehlermeldungen, die der Pooler an Clients sendet.

Standard: 1

### log_stats {#log_stats}

Schreibt im Abstand von `stats_period` aggregierte Statistiken ins Protokoll. Kann deaktiviert werden, wenn externe Überwachungswerkzeuge dieselben Daten über `SHOW`-Befehle abrufen.

Standard: 1

### verbose {#verbose}

Erhöht den Detailgrad der Ausgabe. Entspricht dem Schalter `-v` in der Befehlszeile. Beispielsweise entspricht `-v -v` in der Befehlszeile der Einstellung `verbose=2`. 3 ist der höchste derzeit unterstützte Detailgrad.

Standard: 0

--------

## Zugriffskontrolle für die Konsole {#console-access-control}

### admin_users {#admin_users}

Durch Kommas getrennte Liste von Datenbankbenutzern, die sich mit der Konsole verbinden und alle Befehle ausführen dürfen. Auch bei `auth_type=any` bestimmt diese Liste, wer Administratorrechte erhält; andere Benutzer können sich als Statistikbenutzer anmelden. Siehe die [Prüfungen des Konsolenzugriffs in 1.26.0](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/src/admin.c#L1572-L1609).

Standard: leer

### stats_users {#stats_users}

Durch Kommas getrennte Liste von Datenbankbenutzern, die sich mit der Konsole verbinden und dort lesende Abfragen ausführen dürfen, also alle `SHOW`-Befehle.

Standard: leer

--------

## Verbindungsprüfungen und Zeitüberschreitungen {#connection-sanity-checks-timeouts}

### server_reset_query {#server_reset_query}

Abfrage, die beim Freigeben einer Serververbindung an den Server gesendet wird, bevor die Verbindung anderen Clients zur Verfügung steht. Zu diesem Zeitpunkt läuft keine Transaktion; der Wert sollte daher weder `ABORT` noch `ROLLBACK` enthalten.

Die Abfrage soll alle Änderungen an der Datenbanksitzung bereinigen, damit der nächste Client die Verbindung in einem klar definierten Zustand erhält. Der Standardwert `DISCARD ALL` bereinigt alles, lässt dem nächsten Client jedoch keinen zuvor zwischengespeicherten Zustand. Eine weniger umfassende Abfrage ist möglich, z. B. `DEALLOCATE ALL`, um nur vorbereitete Anweisungen zu entfernen, sofern die Anwendung auch dann korrekt funktioniert, wenn Teile des Zustands erhalten bleiben.

Beim Transaktions-Pooling wird `server_reset_query` nicht verwendet, da Clients in diesem Modus keine sitzungsbezogenen Funktionen verwenden dürfen: Jede Transaktion läuft über eine andere Verbindung und erhält damit einen anderen Sitzungszustand.

Standard: `DISCARD ALL`

### server_reset_query_always {#server_reset_query_always}

Legt fest, ob `server_reset_query` in allen Pooling-Modi ausgeführt werden soll. Ist die Einstellung deaktiviert (Standard), wird `server_reset_query` nur in Pools mit Sitzungs-Pooling ausgeführt. Verbindungen im Transaktions-Pooling sollten keine Rücksetzabfrage benötigen.

Diese Einstellung dient als Behelf für fehlerhafte Konfigurationen, in denen Anwendungen sitzungsbezogene Funktionen über einen PgBouncer mit Transaktions-Pooling nutzen. Sie ersetzt nicht deterministische Fehler durch deterministische Fehler: Clients verlieren ihren Zustand immer nach jeder Transaktion.

Standard: 0

### server_check_delay {#server_check_delay}

Zeitraum, in dem freigegebene Verbindungen für die sofortige Wiederverwendung bereitgehalten werden, ohne `server_check_query` auf ihnen auszuführen. Bei 0 wird die Prüfung immer ausgeführt.

Standard: 30.0

### server_check_query {#server_check_query}

Einfache Abfrage ohne Wirkung, mit der geprüft wird, ob die Serververbindung noch besteht.

Bei einer leeren Zeichenfolge ist die Verbindungsprüfung deaktiviert.

Bei `<empty>` wird eine leere Abfrage als Verbindungsprüfung gesendet.

Standard: `<empty>`

### server_fast_close {#server_fast_close}

Trennt eine Serververbindung im Sitzungs-Pooling sofort oder nach Abschluss der aktuellen Transaktion, wenn sie sich im Zustand "close_needed" befindet (gesetzt durch `RECONNECT`, ein `RELOAD` mit geänderten Verbindungseinstellungen oder eine DNS-Änderung), statt bis zum Ende der Sitzung zu warten. Im Statement- oder Transaktions-Pooling hat dies keine Wirkung, da es dort dem Standardverhalten entspricht.

Wird aufgrund dieser Einstellung eine Serververbindung vor Ende der Clientsitzung geschlossen, wird auch die Clientverbindung geschlossen. So bemerkt der Client, dass die Sitzung unterbrochen wurde.

Bei Sitzungs-Pooling mit lang laufenden Sitzungen lässt diese Einstellung Änderungen an der Verbindungskonfiguration schneller wirksam werden. Der Nachteil ist, dass Konfigurationsänderungen Clientsitzungen unterbrechen können; Clientanwendungen benötigen daher Logik zum erneuten Verbinden und Wiederherstellen des Sitzungszustands. Es gehen jedoch keine Transaktionen verloren, da laufende Transaktionen nicht unterbrochen werden, sondern nur inaktive Sitzungen.

Standard: 0

### server_lifetime {#server_lifetime}

Der Pooler schließt eine ungenutzte Serververbindung (die derzeit keiner Clientverbindung zugeordnet ist), wenn sie länger als diese Zeit besteht. Bei 0 wird die Verbindung nur einmal verwendet und dann geschlossen. [Sekunden]

Kann auch pro Datenbank im Abschnitt `[databases]` gesetzt werden.

Standard: 3600.0

### server_idle_timeout {#server_idle_timeout}

Ist eine Serververbindung länger als diese Anzahl von Sekunden inaktiv, wird sie geschlossen. Bei 0 ist diese Zeitüberschreitung deaktiviert. [Sekunden]

Standard: 600.0

### server_connect_timeout {#server_connect_timeout}

Werden Verbindungsaufbau und Anmeldung nicht innerhalb dieser Zeit abgeschlossen, wird die Verbindung geschlossen. [Sekunden]

Standard: 15.0

### server_login_retry {#server_login_retry}

Scheitert die Anmeldung am Server wegen eines Verbindungs- oder Authentifizierungsfehlers, wartet der Pooler diese Zeit, bevor er erneut versucht, sich zu verbinden. Während dieser Wartezeit erhalten neue Clients, die sich mit dem betroffenen Server verbinden wollen, sofort einen Fehler, ohne dass ein weiterer Verbindungsversuch erfolgt. [Sekunden]

Dieses Verhalten verhindert, dass Clients unnötig in einer Warteschlange auf eine verfügbare Serververbindung warten, wenn der Server nicht funktioniert. Es bedeutet jedoch auch, dass nach einer vorübergehenden Störung, etwa bei einem Neustart oder einer fehlerhaften Konfiguration, mindestens diese Zeit verstreicht, bevor der Pooler einen neuen Verbindungsversuch in Betracht zieht. Geplante Ereignisse wie Neustarts sollten normalerweise mit dem Befehl `PAUSE` gesteuert werden, um dies zu vermeiden.

Standard: 15.0

### client_login_timeout {#client_login_timeout}

Baut ein Client eine Verbindung auf, meldet sich aber nicht innerhalb dieser Zeit erfolgreich an, wird seine Verbindung getrennt. [Sekunden]

Standard: 60.0

### autodb_idle_timeout {#autodb_idle_timeout}

Werden die automatisch (über `*`) erstellten Datenbankpools diese Anzahl von Sekunden nicht verwendet, werden sie freigegeben. Der Nachteil ist, dass dabei auch ihre Statistiken verloren gehen. [Sekunden]

Standard: 3600.0

### pool_idle_timeout {#pool_idle_timeout}

Hat ein Pool (ein bestimmtes Datenbank/Benutzer-Paar) während dieser Anzahl von Sekunden weder Client- noch Serververbindungen, wird er freigegeben. Dies ähnelt `autodb_idle_timeout`, gibt jedoch einzelne Pools statt ganzer automatisch erstellter Datenbanken frei. Anders als `server_idle_timeout` (das inaktive Serververbindungen schließt, den Pool aber beibehält) gibt diese Einstellung den gesamten Pool frei, und zwar erst, wenn er vollständig leer ist.

Wie bei `autodb_idle_timeout` gehen dabei die Statistiken des freigegebenen Pools verloren. Da die datenbankbezogenen Gesamtwerte in `SHOW STATS` die Summe über die derzeit vorhandenen Pools darstellen, verringern sie sich beim Freigeben eines Pools. Überwachungssysteme können dies als Zurücksetzen eines Zählers fehlinterpretieren. Deshalb ist diese Einstellung standardmäßig deaktiviert. 0 deaktiviert sie. [Sekunden]

Standard: 0 (deaktiviert)

### dns_max_ttl {#dns_max_ttl}

Zeitraum, für den DNS-Abfragen zwischengespeichert werden können. Die tatsächliche DNS-TTL wird ignoriert. [Sekunden]

Standard: 15.0

### dns_nxdomain_ttl {#dns_nxdomain_ttl}

Zeitraum, für den DNS-Fehler und DNS-Abfragen mit NXDOMAIN zwischengespeichert werden können. [Sekunden]

Standard: 15.0

### dns_zone_check_period {#dns_zone_check_period}

Intervall für die Prüfung, ob sich die Seriennummer einer Zone geändert hat.

PgBouncer kann DNS-Zonen aus Hostnamen ermitteln (alles nach dem ersten Punkt) und dann regelmäßig prüfen, ob sich die Seriennummer der Zone ändert. Erkennt es Änderungen, werden alle Hostnamen dieser Zone erneut aufgelöst. Ändert sich die IP-Adresse eines Hosts, werden dessen Verbindungen für ungültig erklärt.

Funktioniert nur mit dem c-ares-Backend (`configure`-Option `--with-cares`).

Standard: 0.0 (deaktiviert)

### resolv_conf {#resolv_conf}

Pfad einer eigenen `resolv.conf`-Datei. Damit lassen sich eigene DNS-Server und gegebenenfalls weitere Optionen zur Namensauflösung unabhängig von der globalen Betriebssystemkonfiguration angeben.

Erfordert das evdns-Backend (>= 2.0.3) oder das c-ares-Backend (>= 1.15.0).

Die Datei wird von der DNS-Backend-Bibliothek ausgewertet, nicht von PgBouncer. Einzelheiten zur zulässigen Syntax und zu den Direktiven stehen daher in der Dokumentation der Bibliothek.

Standard: leer (Betriebssystemvorgaben verwenden)

### query_wait_notify {#query_wait_notify}

Zeit, die ein Client in der Warteschlange verbringt, bevor PgBouncer eine Benachrichtigung sendet, dass der Client in die Warteschlange eingereiht wird. [Sekunden]

Der Wert 0 deaktiviert diese Benachrichtigung.

Standard: 5

### login_notify_message {#login_notify_message}

Begrüßungsmeldung, die nach erfolgreicher Anmeldung an den Client gesendet wird. Damit kann sichergestellt werden, dass Clients erkennen, dass sie sich mit pgbouncer und nicht direkt mit postgres verbinden.

Standard: leer (keine Begrüßungsmeldung)

--------

## TLS-Einstellungen {#tls-settings}

Wird der Inhalt einer Zertifikats- oder Schlüsseldatei geändert, ohne den Dateinamen in der Konfiguration anzupassen, wird der neue Inhalt nach einem RELOAD für neue Verbindungen verwendet. Bestehende Verbindungen werden jedoch nicht geschlossen. Müssen aus Sicherheitsgründen alle Verbindungen so schnell wie möglich (ASAP) die neuen Dateien verwenden, empfiehlt sich ein RECONNECT nach dem RELOAD.

Jede Änderung einer TLS-Einstellung löst aus Sicherheitsgründen automatisch ein RECONNECT aus.

### client_tls_sslmode {#client_tls_sslmode}

TLS-Modus für Verbindungen von Clients. TLS-Verbindungen sind standardmäßig deaktiviert. Bei Aktivierung müssen auch `client_tls_key_file` und `client_tls_cert_file` konfiguriert werden, um den Schlüssel und das Zertifikat festzulegen, mit denen PgBouncer Clientverbindungen annimmt. Das gebräuchlichste von PgBouncer unterstützte Zertifikatsdateiformat ist PEM.

- **`disable`**: Unverschlüsseltes TCP. Eine TLS-Anforderung des Clients wird ignoriert. Standard.
- **`allow`**: Fordert der Client TLS an, wird es verwendet. Andernfalls wird unverschlüsseltes TCP verwendet. Legt der Client ein Clientzertifikat vor, wird es nicht geprüft.
- **`prefer`**: Wie `allow`.
- **`require`**: Der Client muss TLS verwenden. Andernfalls wird die Clientverbindung abgelehnt. Legt der Client ein Clientzertifikat vor, wird es nicht geprüft.
- **`verify-ca`**: Der Client muss TLS mit einem gültigen Clientzertifikat verwenden.
- **`verify-full`**: Wie `verify-ca`.

### client_tls_key_file {#client_tls_key_file}

Privater Schlüssel, mit dem PgBouncer Clientverbindungen annimmt.

Standard: nicht gesetzt

### client_tls_cert_file {#client_tls_cert_file}

Zertifikat für den privaten Schlüssel. Clients können es prüfen.

Standard: nicht gesetzt

### client_tls_ca_file {#client_tls_ca_file}

Datei mit Stammzertifikaten zur Prüfung von Clientzertifikaten.

Standard: nicht gesetzt

### client_tls_protocols {#client_tls_protocols}

Zulässige TLS-Protokollversionen. Mögliche Werte: `tlsv1.0`, `tlsv1.1`, `tlsv1.2`, `tlsv1.3`. Kurzformen: `all` (tlsv1.0,tlsv1.1,tlsv1.2,tlsv1.3), `secure` (tlsv1.2,tlsv1.3).

Standard: `secure`

### client_tls_ciphers {#client_tls_ciphers}

Zulässige TLS-Chiffren in OpenSSL-Syntax. Kurzformen:

- `default`/`secure`/`fast`/`normal` (alle verwenden die systemweiten OpenSSL-Vorgaben)
- `all` (aktiviert alle Chiffren, nicht empfohlen)

Betrifft nur Verbindungen mit TLS-Version 1.2 und niedriger. Für Version 1.3 siehe `client_tls13_ciphers` weiter unten.

Standard: `default`

### client_tls13_ciphers {#client_tls13_ciphers}

Zulässige Chiffren für TLS v1.3. Ist der Wert leer, wird der Wert von `client_tls_ciphers` verwendet. Mögliche Werte:

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`
- `TLS_AES_128_CCM_SHA256`

Betrifft nur Verbindungen mit TLS-Version 1.3 und höher. Für Version 1.2 und niedriger siehe `client_tls_ciphers`.

Standard: `<empty>`

### client_tls_ecdhcurve {#client_tls_ecdhcurve}

Name der elliptischen Kurve für den ECDH-Schlüsselaustausch.

Mögliche Werte: `none` (DH ist deaktiviert), `auto` (256-Bit-ECDH), Kurvenname

Standard: `auto`

### client_tls_dheparams {#client_tls_dheparams}

Art des DHE-Schlüsselaustauschs.

Mögliche Werte: `none` (DH ist deaktiviert), `auto` (2048-Bit-DH), `legacy` (1024-Bit-DH)

Standard: `auto`

### server_tls_sslmode {#server_tls_sslmode}

TLS-Modus für Verbindungen zu PostgreSQL-Servern. Der Standardmodus ist `prefer`.

- **`disable`**: Unverschlüsseltes TCP. TLS wird beim Server gar nicht angefordert.
- **`allow`**: Verhält sich wie `prefer`: Zuerst wird TLS angefordert. Lehnt der Server TLS ab, wird auf unverschlüsseltes TCP zurückgegriffen. Das Serverzertifikat wird nicht geprüft.
- **`prefer`**: Bei PostgreSQL wird immer zuerst eine TLS-Verbindung angefordert. Wird sie abgelehnt, wird die Verbindung über unverschlüsseltes TCP aufgebaut. Das Serverzertifikat wird nicht geprüft. Standard.
- **`require`**: Die Verbindung muss TLS verwenden. Lehnt der Server dies ab, wird kein unverschlüsseltes TCP versucht. Das Serverzertifikat wird nicht geprüft.
- **`verify-ca`**: Die Verbindung muss TLS verwenden und das Serverzertifikat muss gemäß `server_tls_ca_file` gültig sein. Der Serverhostname wird nicht mit dem Zertifikat abgeglichen.
- **`verify-full`**: Die Verbindung muss TLS verwenden und das Serverzertifikat muss gemäß `server_tls_ca_file` gültig sein. Der Serverhostname muss mit den Zertifikatsangaben übereinstimmen.

### server_tls_ca_file {#server_tls_ca_file}

Datei mit Stammzertifikaten zur Prüfung von PostgreSQL-Serverzertifikaten.

Standard: nicht gesetzt

### server_tls_key_file {#server_tls_key_file}

Privater Schlüssel, mit dem sich PgBouncer gegenüber dem PostgreSQL-Server authentifiziert.

Standard: nicht gesetzt

### server_tls_cert_file {#server_tls_cert_file}

Zertifikat für den privaten Schlüssel. Der PostgreSQL-Server kann es prüfen.

Standard: nicht gesetzt

### server_tls_protocols {#server_tls_protocols}

Zulässige TLS-Protokollversionen. Mögliche Werte: `tlsv1.0`, `tlsv1.1`, `tlsv1.2`, `tlsv1.3`. Kurzformen: `all` (tlsv1.0,tlsv1.1,tlsv1.2,tlsv1.3), `secure` (tlsv1.2,tlsv1.3), `legacy` (all).

Standard: `secure`

### server_tls_ciphers {#server_tls_ciphers}

Zulässige TLS-Chiffren in OpenSSL-Syntax. Kurzformen:

- `default`/`secure`/`fast`/`normal` (alle verwenden die systemweiten OpenSSL-Vorgaben)
- `all` (aktiviert alle Chiffren, nicht empfohlen)

Betrifft nur Verbindungen mit TLS-Version 1.2 und niedriger. Für Version 1.3 siehe `server_tls13_ciphers` weiter unten.

Standard: `default`

### server_tls13_ciphers {#server_tls13_ciphers}

Zulässige Chiffren für TLS v1.3. Ist der Wert leer, wird der Wert von `server_tls_ciphers` verwendet. Mögliche Werte:

- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`
- `TLS_AES_128_CCM_SHA256`

Betrifft nur Verbindungen mit TLS-Version 1.3 und höher. Für Version 1.2 und niedriger siehe `server_tls_ciphers`.

Standard: `<empty>`

--------

## Gefährliche Zeitüberschreitungen {#dangerous-timeouts}

Das Setzen der folgenden Zeitüberschreitungen kann unerwartete Fehler verursachen.

### query_timeout {#query_timeout}

Abfragen, die länger als diese Zeit laufen, werden abgebrochen. Diese Einstellung sollte nur zusammen mit einem etwas kürzeren serverseitigen `statement_timeout` verwendet werden, damit sie nur bei Netzwerkproblemen greift. [Sekunden]

Standard: 0.0 (deaktiviert)

### query_wait_timeout {#query_wait_timeout}

Maximal zulässige Wartezeit von Abfragen auf ihre Ausführung. Wird die Abfrage innerhalb dieser Zeit keinem Server zugewiesen, wird die Clientverbindung getrennt. 0 deaktiviert diese Zeitüberschreitung. Bei Deaktivierung bleiben Clients unbegrenzt in der Warteschlange. [Sekunden]

Diese Einstellung verhindert, dass nicht reagierende Server Verbindungen blockieren. Sie hilft auch, wenn der Server ausgefallen ist oder Verbindungen aus irgendeinem Grund ablehnt.

Diese Einstellung kann auch pro Datenbank und pro Benutzer konfiguriert werden. Die Rangfolge lautet: Benutzer, dann Datenbank, dann global. Eine explizite 0 auf der ausgewählten Ebene deaktiviert diese Zeitüberschreitung. Siehe den [Code zur Auswahl der Zeitüberschreitung in 1.26.0](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/src/janitor.c#L328-L336).

Standard: 120.0

### cancel_wait_timeout {#cancel_wait_timeout}

Maximal zulässige Wartezeit von Abbruchanfragen auf ihre Ausführung. Wird die Abbruchanfrage innerhalb dieser Zeit keinem Server zugewiesen, wird die Clientverbindung getrennt. 0 deaktiviert diese Zeitüberschreitung. Bei Deaktivierung bleiben Abbruchanfragen unbegrenzt in der Warteschlange. [Sekunden]

Diese Einstellung verhindert, dass ein Client blockiert, wenn eine Abbruchanfrage wegen eines ausgefallenen Servers nicht weitergeleitet werden kann.

Standard: 10.0

### client_idle_timeout {#client_idle_timeout}

Clientverbindungen, die länger als diese Anzahl von Sekunden inaktiv sind, werden geschlossen. Dieser Wert sollte größer als die clientseitigen Einstellungen zur Verbindungslebensdauer sein und nur für Netzwerkprobleme verwendet werden. [Sekunden]

Standard: 0.0 (deaktiviert)

### idle_transaction_timeout {#idle_transaction_timeout}

Befindet sich ein Client länger als diese Zeit im Zustand "idle in transaction", wird seine Verbindung getrennt. [Sekunden]

Standard: 0.0 (deaktiviert)

### transaction_timeout {#transaction_timeout}

Befindet sich ein Client länger als diese Zeit im Zustand "in transaction", wird seine Verbindung getrennt. [Sekunden]

Standard: 0.0 (deaktiviert)

--------

## Systemnahe Netzwerkeinstellungen {#low-level-network-settings}

### pkt_buf {#pkt_buf}

Interne Puffergröße für Pakete. Beeinflusst die Größe der gesendeten TCP-Pakete und den allgemeinen Speicherbedarf. Tatsächliche libpq-Pakete können größer sein; der Wert muss daher nicht groß angesetzt werden.

Standard: 4096

### max_packet_size {#max_packet_size}

Maximale Größe von PostgreSQL-Paketen, die PgBouncer durchlässt. Ein Paket enthält entweder eine Abfrage oder eine Zeile einer Ergebnismenge. Die vollständige Ergebnismenge kann größer sein.

Standard: 2147483647

### listen_backlog {#listen_backlog}

Backlog-Argument für `listen(2)`. Bestimmt, wie viele neue, noch nicht beantwortete Verbindungsversuche in der Warteschlange gehalten werden. Ist die Warteschlange voll, werden weitere neue Verbindungen verworfen.

Standard: 128

### sbuf_loopcnt {#sbuf_loopcnt}

Anzahl der Verarbeitungsschritte für Daten auf einer Verbindung, bevor zur nächsten übergegangen wird. Ohne diese Grenze kann eine Verbindung mit einer großen Ergebnismenge PgBouncer lange blockieren. Ein Durchlauf verarbeitet eine Datenmenge der Größe `pkt_buf`. 0 bedeutet keine Begrenzung.

Standard: 5

### so_reuseport {#so_reuseport}

Legt fest, ob die Socket-Option `SO_REUSEPORT` für lauschende TCP-Sockets gesetzt wird. Auf manchen Betriebssystemen ermöglicht dies, mehrere PgBouncer-Instanzen auf demselben Host am selben Port lauschen zu lassen, wobei der Kernel die Verbindungen automatisch verteilt. Mit dieser Option kann PgBouncer mehr CPU-Kerne nutzen. (PgBouncer arbeitet mit einem einzelnen Thread und verwendet einen CPU-Kern pro Instanz.)

Das genaue Verhalten hängt vom Betriebssystemkernel ab. Zum Zeitpunkt der Erstellung dieser Dokumentation hat die Einstellung auf (hinreichend aktuellen Versionen von) Linux, DragonFlyBSD und FreeBSD die gewünschte Wirkung. (Unter FreeBSD wird stattdessen die Socket-Option `SO_REUSEPORT_LB` angewendet.) Einige andere Betriebssysteme unterstützen die Socket-Option, ohne dass sie die gewünschte Wirkung hat: Mehrere Prozesse können sich an denselben Port binden, aber nur einer erhält die Verbindungen. Einzelheiten stehen in der Dokumentation zu `setsockopt()` des Betriebssystems.

Auf Systemen, die diese Socket-Option überhaupt nicht unterstützen, führt die Aktivierung dieser Einstellung zu einem Fehler.

Jede PgBouncer-Instanz auf demselben Host benötigt mindestens unterschiedliche Werte für `unix_socket_dir` und `pidfile` sowie für `logfile`, falls verwendet. Bei Nutzung dieser Option ist es außerdem nicht mehr möglich, sich über TCP/IP mit einer bestimmten PgBouncer-Instanz zu verbinden. Dies kann Auswirkungen auf die Überwachung und die Erfassung von Metriken haben.

Damit Abfrageabbrüche weiterhin funktionieren, sollte PgBouncer-Peering zwischen den verschiedenen PgBouncer-Prozessen eingerichtet werden. Einzelheiten stehen in der Dokumentation zur Konfigurationsoption `peer_id` und zum Konfigurationsabschnitt `peers`. Der Beispielabschnitt dieser Dokumentation enthält außerdem ein Beispiel mit Peering und `so_reuseport`.

Standard: 0

### tcp_defer_accept {#tcp_defer_accept}

Setzt die Socket-Option `TCP_DEFER_ACCEPT`; Einzelheiten unter `man 7 tcp`. (Dies ist eine boolesche Option: 1 bedeutet aktiviert. Der bei Aktivierung tatsächlich gesetzte Wert ist derzeit fest auf 45 Sekunden codiert.)

Wird derzeit nur unter Linux unterstützt.

Standard: 1 unter Linux, sonst 0

### tcp_socket_buffer {#tcp_socket_buffer}

Standard: nicht gesetzt

### tcp_keepalive {#tcp_keepalive}

Aktiviert grundlegendes Keepalive mit den Betriebssystemvorgaben.

Unter Linux lauten die Systemvorgaben `tcp_keepidle=7200`, `tcp_keepintvl=75`, `tcp_keepcnt=9`. Auf anderen Betriebssystemen sind sie wahrscheinlich ähnlich.

Standard: 1

### tcp_keepcnt {#tcp_keepcnt}

Standard: nicht gesetzt

### tcp_keepidle {#tcp_keepidle}

Standard: nicht gesetzt

### tcp_keepintvl {#tcp_keepintvl}

Standard: nicht gesetzt

### tcp_user_timeout {#tcp_user_timeout}

Setzt die Socket-Option `TCP_USER_TIMEOUT`. Sie gibt die maximale Zeit in Millisekunden an, während der gesendete Daten unbestätigt bleiben dürfen, bevor die TCP-Verbindung zwangsweise geschlossen wird. Bei 0 wird die Betriebssystemvorgabe verwendet.

Wird derzeit nur unter Linux unterstützt.

Standard: 0

--------

## Abschnitt [databases] {#section-databases}

Der Abschnitt `[databases]` definiert die Namen der Datenbanken, mit denen sich PgBouncer-Clients verbinden können, und legt fest, wohin diese Verbindungen weitergeleitet werden. Der Abschnitt enthält Zeilen im Format key=value wie

```ini
dbname = connection string
```

Dabei wird der Schlüssel als Datenbankname und der Wert als Verbindungszeichenfolge interpretiert. Diese besteht aus key=value-Paaren mit den nachfolgend beschriebenen Verbindungsparametern (ähnlich wie bei libpq, allerdings wird libpq selbst nicht verwendet und der verfügbare Funktionsumfang unterscheidet sich). Beispiel:

```ini
foodb = host=host1.example.com port=5432
bardb = host=localhost dbname=bazdb
```

Der Datenbankname kann die Zeichen `_0-9A-Za-z` ohne Anführungszeichen enthalten. Namen mit anderen Zeichen müssen nach den üblichen SQL-Regeln für Bezeichner in doppelte Anführungszeichen gesetzt werden; ein einzelnes doppeltes Anführungszeichen wird dabei als `""` geschrieben.

Der Datenbankname `pgbouncer` ist für die Administrationskonsole reserviert und kann hier nicht als Schlüssel verwendet werden.

`*` dient als Fallback-Datenbank: Existiert der genaue Name nicht, wird ihr Wert als Verbindungszeichenfolge für die angeforderte Datenbank verwendet. Gibt es beispielsweise den Eintrag (und keine anderen vorrangigen Einträge)

```ini
* = host=foo
```

verhält sich eine Verbindung zu PgBouncer mit Angabe der Datenbank `bar` effektiv so, als existiere der Eintrag

```ini
bar = host=foo dbname=bar
```

(da der Standardwert für `dbname` der clientseitige Datenbankname ist; siehe unten).

Solche automatisch erstellten Datenbankeinträge werden bereinigt, wenn sie länger als die durch `autodb_idle_timeout` festgelegte Zeit inaktiv bleiben.

### dbname {#dbname}

Name der Zieldatenbank.

Standard: identisch mit dem clientseitigen Datenbanknamen

### host {#host}

Hostname oder IP-Adresse des Verbindungsziels. Hostnamen werden beim Verbindungsaufbau aufgelöst; das Ergebnis wird gemäß dem Parameter `dns_max_ttl` zwischengespeichert. Ändert sich die Auflösung eines Hostnamens, werden bestehende Serververbindungen bei ihrer Freigabe (entsprechend dem Pooling-Modus) automatisch geschlossen, und neue Serververbindungen verwenden sofort das neue Ergebnis. Liefert DNS mehrere Ergebnisse, werden sie im Round-Robin-Verfahren verwendet.

Beginnt der Wert mit `/`, wird ein Unix-Socket im Dateisystem-Namensraum verwendet. Beginnt er mit `@`, wird ein Unix-Socket im abstrakten Namensraum verwendet.

Eine durch Kommas getrennte Liste von Hostnamen oder Adressen ist möglich. In diesem Fall werden Verbindungen im Round-Robin-Verfahren aufgebaut. (Enthält eine Hostliste Hostnamen, die ihrerseits per DNS zu mehreren Adressen aufgelöst werden, arbeiten die Round-Robin-Verfahren unabhängig voneinander. Dieses Verhalten ist implementierungsabhängig und kann sich ändern.) In einer Liste müssen alle Hosts jederzeit verfügbar sein: Es gibt keine Mechanismen, um nicht erreichbare Hosts zu überspringen, nur verfügbare Hosts aus einer Liste auszuwählen oder Ähnliches. (Dies unterscheidet sich von der Bedeutung einer Hostliste in libpq.) Außerdem betrifft dies nur die Auswahl der Ziele neuer Verbindungen. Zur Zuweisung von Clients an bereits bestehende Serververbindungen siehe auch `server_round_robin`.

Beispiele:

```text
host=localhost
host=127.0.0.1
host=2001:0db8:85a3:0000:0000:8a2e:0370:7334
host=/var/run/postgresql
host=192.168.0.1,192.168.0.2,192.168.0.3
```

Standard: nicht gesetzt, das heißt, es wird ein Unix-Socket verwendet

### port {#port}

Standard: 5432

### user {#user-1}

Ist `user=` gesetzt, werden alle Verbindungen zur Zieldatenbank unter dem angegebenen Benutzer hergestellt. Für diese Datenbank gibt es somit nur einen Pool.

Andernfalls meldet sich PgBouncer mit dem Benutzernamen des Clients an der Zieldatenbank an, sodass es pro Benutzer einen Pool gibt.

### password {#password}

Ist hier kein Passwort angegeben, wird für den oben angegebenen Benutzer das Passwort aus `auth_file` verwendet. Dynamische Verfahren zur Passwortermittlung wie `auth_query` werden derzeit nicht unterstützt.

### auth_user {#auth_user-1}

Überschreibt die globale Einstellung `auth_user`, falls angegeben.

### auth_query {#auth_query-1}

Überschreibt die globale Einstellung `auth_query`, falls angegeben. Die gesamte SQL-Anweisung muss in einfache Anführungszeichen gesetzt werden.

### auth_dbname {#auth_dbname-1}

Überschreibt die globale Einstellung `auth_dbname`, falls angegeben.

### pool_size {#pool_size}

Legt die maximale Größe der Pools für diese Datenbank fest. Falls nicht gesetzt, wird `default_pool_size` verwendet.

### min_pool_size {#min_pool_size-1}

Legt die minimale Poolgröße für diese Datenbank fest. Falls nicht gesetzt, wird der globale Wert von `min_pool_size` verwendet.

Wird nur durchgesetzt, wenn mindestens eine der folgenden Bedingungen zutrifft:

* In diesem Eintrag im Abschnitt `[databases]` ist für den Schlüssel `user` ein Wert gesetzt (ein sogenannter erzwungener Benutzer).
* Mindestens ein Client ist mit dem Pool verbunden.

### reserve_pool_size {#reserve_pool_size-1}

Legt die Anzahl zusätzlicher Verbindungen für diese Datenbank fest. Falls nicht gesetzt, wird der globale Wert von `reserve_pool_size` verwendet. Aus Gründen der Abwärtskompatibilität ist `reserve_pool` ein Alias für diese Option.

### connect_query {#connect_query}

Abfrage, die nach dem Verbindungsaufbau ausgeführt wird, bevor ein Client die Verbindung verwenden darf. Fehler der Abfrage werden protokolliert, ansonsten jedoch ignoriert.

### pool_mode {#pool_mode-1}

Legt den Pooling-Modus für diese Datenbank fest. Falls nicht gesetzt, wird der Standardwert von `pool_mode` verwendet.

### query_wait_timeout {#query_wait_timeout-1}

Maximal zulässige Wartezeit von Abfragen auf ihre Ausführung. 0 deaktiviert diese Zeitüberschreitung. Wird diese Einstellung weggelassen, wird der jeweils geltende Standardwert übernommen. [Sekunden]

Weitere Einzelheiten enthält die Beschreibung der globalen Einstellung `query_wait_timeout`.

Ein benutzerspezifischer Wert für `query_wait_timeout` überschreibt diese Datenbankeinstellung. Ist keiner von beiden gesetzt, wird der globale Wert von `query_wait_timeout` verwendet.

### load_balance_hosts {#load_balance_hosts}

Ist in `host` eine durch Kommas getrennte Liste angegeben, steuert `load_balance_hosts`, welcher Eintrag für eine neue Verbindung ausgewählt wird.

Hinweis: Diese Einstellung steuert derzeit nur die Lastverteilung bei mehreren Hosts in der Verbindungszeichenfolge, nicht jedoch bei einem einzelnen Host, dessen DNS-Eintrag auf mehrere IP-Adressen verweist. Diese Funktion fehlt noch; in einer zukünftigen Version könnte diese Einstellung daher beide Arten der Lastverteilung steuern.

- **`round-robin`**: Ein neuer Verbindungsversuch wählt den nächsten Hosteintrag in der Liste.
- **`disable`**: Neue Verbindungen verwenden weiterhin denselben Hosteintrag, bis eine Verbindung fehlschlägt. Danach wird der nächste Hosteintrag ausgewählt.

Es wird empfohlen, `server_login_retry` unter den Standardwert zu setzen, um bei mehreren verfügbaren Hosts schnelle Wiederholungsversuche zu ermöglichen.

Standard: `round-robin`

### max_db_connections {#max_db_connections-1}

Konfiguriert eine datenbankweite Höchstzahl von Serververbindungen (alle Pools innerhalb der Datenbank haben also zusammen höchstens diese Anzahl von Serververbindungen).

### max_db_client_connections {#max_db_client_connections-1}

Konfiguriert eine datenbankweite Höchstzahl von Clientverbindungen. Sollte zusammen mit `max_client_conn` verwendet werden, um die Anzahl der Verbindungen zu begrenzen, die PgBouncer annehmen darf.

### server_lifetime {#server_lifetime-1}

Konfiguriert `server_lifetime` pro Datenbank. Falls nicht gesetzt, verwendet die Datenbank den instanzweit konfigurierten Wert von `server_lifetime`.

### client_encoding {#client_encoding}

Fordert einen bestimmten Wert für `client_encoding` vom Server an.

### datestyle {#datestyle}

Fordert einen bestimmten Wert für `datestyle` vom Server an.

### timezone {#timezone}

Fordert einen bestimmten Wert für `timezone` vom Server an.

--------

## Abschnitt [users] {#section-users}

Dieser Abschnitt enthält Zeilen im Format key=value wie

```ini
user1 = settings
```

Dabei wird der Schlüssel als Benutzername und der Wert als Liste von key=value-Paaren mit benutzerspezifischen Konfigurationseinstellungen interpretiert. Beispiel:

```ini
user1 = pool_mode=session
```

Hier sind nur wenige Einstellungen verfügbar.

Ist `auth_file` konfiguriert und ein Benutzer zwar in diesem Abschnitt definiert, aber nicht in `auth_file` aufgeführt, versucht PgBouncer bei gesetztem `auth_user`, mit `auth_query` ein Passwort für diesen Benutzer zu ermitteln. Ist `auth_user` nicht gesetzt, verhält sich PgBouncer so, als existiere der Benutzer, und gibt keine Meldungen "no such user" an den Client zurück; es akzeptiert jedoch auch kein angegebenes Passwort.

### pool_size {#pool_size-1}

Legt die maximale Poolgröße für alle Verbindungen dieses Benutzers fest. Falls nicht gesetzt, wird die Datenbankeinstellung oder `default_pool_size` verwendet.

### reserve_pool_size {#reserve_pool_size-2}

Legt die Anzahl zusätzlicher Verbindungen fest, die für einen Pool dieses Benutzers zugelassen werden. Falls nicht gesetzt, wird die Datenbankkonfiguration oder der globale Wert von `reserve_pool_size` verwendet.

### pool_mode {#pool_mode-2}

Legt den Pooling-Modus für alle Verbindungen dieses Benutzers fest. Falls nicht gesetzt, wird die Datenbankeinstellung oder der Standardwert von `pool_mode` verwendet.

### max_user_connections {#max_user_connections-1}

Konfiguriert eine benutzerbezogene Höchstzahl von Serververbindungen (alle Pools dieses Benutzers haben also zusammen höchstens diese Anzahl von Serververbindungen).

### query_timeout {#query_timeout-1}

Legt die maximale Laufzeit einer Benutzerabfrage in Sekunden fest. Falls gesetzt, überschreibt diese Zeitüberschreitung den oben beschriebenen serverweiten Wert von `query_timeout`.

### query_wait_timeout {#query_wait_timeout-2}

Maximal zulässige Wartezeit von Abfragen auf ihre Ausführung. 0 deaktiviert diese Zeitüberschreitung. Wird diese Einstellung weggelassen, wird der jeweils geltende Standardwert übernommen. [Sekunden]

Weitere Einzelheiten enthält die Beschreibung der globalen Einstellung `query_wait_timeout`.

Diese Einstellung überschreibt sowohl den datenbankspezifischen als auch den globalen Wert von `query_wait_timeout`. Falls nicht gesetzt, wird die Datenbankeinstellung verwendet; fehlt auch diese, gilt der globale Wert.

### idle_transaction_timeout {#idle_transaction_timeout-1}

Legt die maximale Zeit in Sekunden fest, während der ein Benutzer eine inaktive Transaktion offen halten kann. Falls gesetzt, überschreibt diese Zeitüberschreitung den oben beschriebenen serverweiten Wert von `idle_transaction_timeout`.

### transaction_timeout {#transaction_timeout-1}

Legt die maximale Zeit in Sekunden fest, während der ein Benutzer eine Transaktion offen halten kann. Falls gesetzt, überschreibt diese Zeitüberschreitung den oben beschriebenen serverweiten Wert von `transaction_timeout`.

### client_idle_timeout {#client_idle_timeout-1}

Legt die maximale Zeit in Sekunden fest, während der ein Client untätig mit der PgBouncer-Instanz verbunden bleiben darf. Falls gesetzt, überschreibt diese Zeitüberschreitung den oben beschriebenen serverweiten Wert von `client_idle_timeout`.

Diese Zeitüberschreitung kann gefährlich sein.

### max_user_client_connections {#max_user_client_connections-1}

Konfiguriert eine benutzerbezogene Höchstzahl von Clientverbindungen. Dies ist das benutzerspezifische Gegenstück zur Einstellung `max_client_conn`.

--------

## Abschnitt [peers] {#section-peers}

Der Abschnitt `[peers]` definiert die Peers, an die PgBouncer Abbruchanfragen weiterleiten kann, sowie die Ziele für diese Anfragen.

PgBouncer-Prozesse können durch einen Wert für `peer_id` und einen Abschnitt `[peers]` in der Konfiguration aller beteiligten PgBouncer-Prozesse zu einer Peer-Gruppe verbunden werden. Sie können Abbruchanfragen dann an den Prozess weiterleiten, der die abzubrechende Abfrage empfangen hat. Dies ist erforderlich, damit Abbrüche funktionieren, wenn mehrere PgBouncer-Prozesse (möglicherweise auf verschiedenen Servern) hinter demselben TCP-Load-Balancer stehen. Abbruchanfragen werden über andere TCP-Verbindungen gesendet als die abzubrechende Abfrage. Ein TCP-Load-Balancer kann die Verbindung einer Abbruchanfrage daher an einen anderen als den vorgesehenen Prozess senden. Durch das Peering erreichen diese Anfragen schließlich den richtigen Prozess. Eine ausführlichere Erklärung bietet diese [Aufzeichnung eines Konferenzvortrags][cancel-problem-video].

[cancel-problem-video]: https://www.youtube.com/watch?v=X-nCHcZ6vQU

Der Abschnitt enthält Zeilen im Format key=value wie

```ini
peer_id = connection string
```

Dabei wird der Schlüssel als `peer_id` und der Wert als Verbindungszeichenfolge interpretiert. Diese besteht aus key=value-Paaren mit den nachfolgend beschriebenen Verbindungsparametern (ähnlich wie bei libpq, allerdings wird libpq selbst nicht verwendet und der verfügbare Funktionsumfang unterscheidet sich). Beispiel:

```ini
1 = host=host1.example.com
2 = host=/tmp/pgbouncer-2  port=5555
```

Hinweis 1: Damit Peering funktioniert, muss die `peer_id` jedes PgBouncer-Prozesses innerhalb der Peer-Gruppe eindeutig sein. Der Abschnitt `[peers]` sollte Einträge für jede dieser Peer-IDs enthalten. Ein Beispiel steht im Beispielabschnitt dieser Dokumentation. Der Abschnitt `[peers]` **darf** die `peer_id` des PgBouncer-Prozesses enthalten, für den die Konfiguration bestimmt ist, muss es aber nicht. Ein solcher Eintrag wird ignoriert, ist jedoch zur Vereinfachung der Konfigurationsverwaltung erlaubt: So kann in mehreren Konfigurationen exakt derselbe Abschnitt `[peers]` verwendet werden.

Hinweis 2: Peering zwischen unterschiedlichen Versionen wird unterstützt, solange alle Peers auf derselben Seite der Versionsgrenze v1.21.0 liegen. In v1.21.0 wurde die Codierung der Abbruch-Tokens so geändert, dass sie nicht mehr mit Tokens früherer Versionen kompatibel sind.

### host {#host-1}

Hostname oder IP-Adresse des Verbindungsziels. Hostnamen werden beim Verbindungsaufbau aufgelöst; das Ergebnis wird gemäß dem Parameter `dns_max_ttl` zwischengespeichert. Liefert DNS mehrere Ergebnisse, werden sie im Round-Robin-Verfahren verwendet. Grundsätzlich wird jedoch von Hostnamen abgeraten, die zu mehreren IP-Adressen aufgelöst werden: Die Abbruchanfrage könnte dann weiterhin an den falschen Knoten weitergeleitet werden und müsste erneut weitergeleitet werden (was höchstens dreimal zulässig ist).

Beginnt der Wert mit `/`, wird ein Unix-Socket im Dateisystem-Namensraum verwendet. Beginnt er mit `@`, wird ein Unix-Socket im abstrakten Namensraum verwendet.

Beispiele:

```text
host=localhost
host=127.0.0.1
host=2001:0db8:85a3:0000:0000:8a2e:0370:7334
host=/var/run/pgbouncer-1
```

### port {#port-1}

Standard: 6432

### pool_size {#pool_size-2}

Legt die maximale Anzahl von Abbruchanfragen fest, die gleichzeitig zum Peer unterwegs sein können. Abbruchanfragen treffen häufig schubweise ein, etwa wenn der dahinterliegende Postgres-Server langsam oder ausgefallen ist. Deshalb ist es wichtig, `pool_size` nicht so niedrig zu setzen, dass diese Spitzen nicht bewältigt werden können.

Falls nicht gesetzt, wird `default_pool_size` verwendet.

--------

## Include-Direktive {#include-directive}

Die PgBouncer-Konfigurationsdatei kann Include-Direktiven enthalten, die eine weitere einzulesende und zu verarbeitende Konfigurationsdatei angeben. So lässt sich die Konfiguration auf physisch getrennte Dateien aufteilen. Include-Direktiven haben folgende Form:

```ini
%include filename
```

Ist der Dateiname kein absoluter Pfad, wird er relativ zum aktuellen Arbeitsverzeichnis interpretiert.

--------

## Format der Authentifizierungsdatei {#authentication-file-format}

Dieser Abschnitt beschreibt das Format der mit `auth_file` angegebenen Datei. Es handelt sich um eine Textdatei im folgenden Format:

```text
"username1" "password" ...
"username2" "md5abcdef012342345" ...
"username2" "SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>"
```

Es sollten mindestens 2 Felder vorhanden sein, die von doppelten Anführungszeichen umgeben sind. Das erste Feld ist der Benutzername; das zweite enthält ein Klartextpasswort, ein MD5-gehashtes Passwort oder ein SCRAM-Secret. PgBouncer ignoriert den Rest der Zeile. Doppelte Anführungszeichen in einem Feldwert können durch zwei aufeinanderfolgende doppelte Anführungszeichen maskiert werden.

PostgreSQL-Format für MD5-gehashte Passwörter:

```text
"md5" + md5(password + username)
```

Der Benutzer `admin` mit dem Passwort `1234` hat somit das MD5-gehashte Passwort `md545f2603610af569b6155c45067268c6b`.

PostgreSQL-Format für SCRAM-Secrets:

```text
SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>
```

Einzelheiten stehen in der PostgreSQL-Dokumentation und in RFC 5803.

Die in der Authentifizierungsdatei gespeicherten Passwörter oder Secrets dienen zwei Zwecken. Erstens werden sie zur Prüfung der Passwörter eingehender Clientverbindungen verwendet, wenn eine passwortbasierte Authentifizierungsmethode konfiguriert ist. Zweitens dienen sie als Passwörter für ausgehende Verbindungen zum Backend-Server, wenn dieser passwortbasierte Authentifizierung verlangt (sofern das Passwort nicht direkt in der Verbindungszeichenfolge der Datenbank angegeben ist).

### Einschränkungen {#limitations}

Ist das Passwort im Klartext gespeichert, kann es für jede passwortbasierte Authentifizierung des Backend-Servers verwendet werden: Klartext, MD5 oder SCRAM (Einzelheiten unter <https://www.postgresql.org/docs/current/auth-password.html>).

MD5-gehashte Passwörter können verwendet werden, wenn der Backend-Server MD5-Authentifizierung nutzt (oder einzelne Benutzer MD5-gehashte Passwörter haben).

SCRAM-Secrets können nur zur Anmeldung an einem Server verwendet werden, wenn auch die Clientauthentifizierung SCRAM nutzt, die PgBouncer-Datenbankdefinition keinen Benutzernamen angibt und die SCRAM-Secrets in PgBouncer und auf dem PostgreSQL-Server identisch sind (gleicher Salt und gleiche Iterationszahl, nicht nur dasselbe Passwort). Dies folgt aus einer grundlegenden Sicherheitseigenschaft von SCRAM: Aus dem gespeicherten SCRAM-Secret allein lassen sich keine Anmeldedaten ableiten.

Die Authentifizierungsdatei kann von Hand erstellt werden; sinnvoll ist auch die Erzeugung aus einer anderen Liste von Benutzern und Passwörtern. `./etc/mkauth.py` enthält ein Beispielskript, das die Authentifizierungsdatei aus der Systemtabelle `pg_authid` erzeugt. Alternativ kann `auth_query` statt `auth_file` verwendet werden, um keine separate Authentifizierungsdatei pflegen zu müssen.

### Hinweis zu verwalteten Servern {#note-on-managed-servers}

Ist der Backend-Server für SCRAM-Passwortauthentifizierung konfiguriert, kann sich PgBouncer nur erfolgreich authentifizieren, wenn es entweder a) das Benutzerpasswort im Klartext oder b) das zugehörige SCRAM-Secret kennt.

Einige Cloud-Anbieter (z. B. AWS RDS) verbieten den Zugriff auf sensible PostgreSQL-Systemtabellen zum Abrufen von Passwörtern. Selbst für den Benutzer mit den höchsten Rechten (z. B. ein Mitglied von `rds_superuser`) liefert `select * from pg_authid` die Meldung `ERROR: permission denied for table pg_authid`. Dies ist ein bekanntes Verhalten ([Blogbeitrag](https://aws.amazon.com/blogs/database/best-practices-for-migrating-postgresql-databases-to-amazon-rds-and-amazon-aurora/)).

Ein bereits auf einem verwalteten Server gespeichertes SCRAM-Secret lässt sich daher nicht abrufen. Das erschwert die Konfiguration von PgBouncer mit demselben SCRAM-Secret. Mit dem folgenden Vorgehen kann dennoch auf beiden Seiten dasselbe SCRAM-Secret konfiguriert und verwendet werden:

Ein SCRAM-Secret für ein beliebiges Passwort mit einem Werkzeug erzeugen, das das Secret ausgeben kann. Beispielsweise gibt `psql --echo-hidden` mit dem Befehl `\password` das SCRAM-Secret in der Konsole aus, bevor es an den Server gesendet wird.

```bash
$ psql --echo-hidden <connection_string>
postgres=# \password <role_name>
Enter new password for user "<role_name>":
Enter it again:
********* QUERY **********
ALTER USER <role_name> PASSWORD 'SCRAM-SHA-256$<iterations>:<salt>$<storedkey>:<serverkey>'
**************************
```

Das SCRAM-Secret aus QUERY notieren und in der Datei `userlist.txt` von PgBouncer setzen.

Wurde ein anderes Werkzeug als `psql --echo-hidden` verwendet, muss das SCRAM-Secret auch auf dem Server gesetzt werden (dazu kann `ALTER ROLE <role_name> PASSWORD '<scram_secret>'` verwendet werden).

--------

## HBA-Dateiformat {#hba-file-format}

Der Pfad der HBA-Datei wird mit `auth_hba_file` angegeben. Sie wird nur verwendet, wenn `auth_type` auf `hba` gesetzt ist.

Die Datei folgt dem Format der PostgreSQL-Datei `pg_hba.conf` (siehe <https://www.postgresql.org/docs/current/auth-pg-hba-conf.html>).

* Unterstützte Datensatztypen: `local`, `host`, `hostssl`, `hostnossl`.
* Datenbankfeld: Unterstützt `all`, `replication`, `sameuser`, `@file` und mehrere Namen. Nicht unterstützt: `samerole`, `samegroup`.
* Benutzernamensfeld: Unterstützt `all`, `@file` und mehrere Namen. Nicht unterstützt: `+groupname`.
* Adressfeld: Unterstützt `all`, IPv4 und IPv6. Nicht unterstützt: `samehost`, `samenet`, DNS-Namen und Domainpräfixe.
* Feld für die Authentifizierungsmethode: Unterstützt nur die Methoden, die PgBouncers `auth_type` unterstützt, sowie `peer` und `reject`, jedoch nicht `any` und `pam`, die nur global funktionieren.
* Der Parameter zur Benutzernamenszuordnung (`map=`) wird unterstützt, wenn `auth_type` auf `cert` oder `peer` gesetzt ist.

--------

## Format der Ident-Zuordnungsdatei {#ident-map-file-format}

Der Pfad der Ident-Zuordnungsdatei wird mit `auth_ident_file` angegeben. Sie wird nur geladen, wenn `auth_type` auf `hba` gesetzt ist.

Das Dateiformat ist eine vereinfachte Variante der PostgreSQL-Datei für Ident-Zuordnungen (siehe <https://www.postgresql.org/docs/current/auth-username-maps.html>).

* Es werden nur Zeilen der Form `map-name system-username database-username` unterstützt.
* Das Einbinden von Dateien/Verzeichnissen wird nicht unterstützt.
* Feld System-username: Nicht unterstützt: reguläre Ausdrücke.
* Feld Database-username: Unterstützt `all` oder einen einzelnen Postgres-Benutzernamen. Nicht unterstützt: `+groupname` und reguläre Ausdrücke.

--------

## Beispiele {#examples}

Kleines Konfigurationsbeispiel:

```ini
[databases]
template1 = host=localhost dbname=template1 auth_user=someuser

[pgbouncer]
pool_mode = session
listen_port = 6432
listen_addr = localhost
auth_type = md5
auth_file = users.txt
logfile = pgbouncer.log
pidfile = pgbouncer.pid
admin_users = someuser
stats_users = stat_collector
```

Datenbankbeispiele:

```ini
[databases]

; foodb over Unix socket
foodb =

; redirect bardb to bazdb on localhost
bardb = host=localhost dbname=bazdb

; access to destination database will go with single user
forcedb = host=localhost port=300 user=baz password=foo client_encoding=UNICODE datestyle=ISO
```

Beispiel einer sicheren Funktion für `auth_query`:

```sql
CREATE OR REPLACE FUNCTION pgbouncer.user_lookup(in i_username text, out uname text, out phash text)
RETURNS record AS $$
BEGIN
    SELECT rolname, CASE WHEN rolvaliduntil < now() THEN NULL ELSE rolpassword END
    FROM pg_authid
    WHERE rolname=i_username AND rolcanlogin
    INTO uname, phash;
    RETURN;
END;
$$ LANGUAGE plpgsql
   SECURITY DEFINER
   -- Set a secure search_path: trusted schema(s), then 'pg_temp'.
   SET search_path = pg_catalog, pg_temp;
REVOKE ALL ON FUNCTION pgbouncer.user_lookup(text) FROM public, pgbouncer;
GRANT EXECUTE ON FUNCTION pgbouncer.user_lookup(text) TO pgbouncer;
```

Beispielkonfigurationen für 2 per Peering verbundene PgBouncer-Prozesse, die mit `so_reuseport` mehrere Prozessorkerne nutzen. Die Konfiguration des ersten Prozesses:

```ini
[databases]
postgres = host=localhost dbname=postgres

[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2

[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
unix_socket_dir=/tmp/pgbouncer1
peer_id=1
```

Die Konfiguration des zweiten Prozesses:

```ini
[databases]
postgres = host=localhost dbname=postgres

[peers]
1 = host=/tmp/pgbouncer1
2 = host=/tmp/pgbouncer2

[pgbouncer]
listen_addr=127.0.0.1
auth_file=auth_file.conf
so_reuseport=1
; only unix_socket_dir and peer_id are different
unix_socket_dir=/tmp/pgbouncer2
peer_id=2
```

--------

## Siehe auch {#see-also}

pgbouncer(1) - Handbuchseite zur allgemeinen Verwendung und zu Konsolenbefehlen

<https://www.pgbouncer.org/>
