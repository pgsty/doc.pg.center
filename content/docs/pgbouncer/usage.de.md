---
title: "Verwendung: pgbouncer-Befehl"
linkTitle: "Verwendung"
weight: 30
description: "Verwendung von PgBouncer auf der Befehlszeile und in der Administrationskonsole"
icon: fa-solid fa-bell-concierge
module: [PGBOUNCER]
categories: [Aufgabe]
aliases: [/pgbouncer/usage/]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/doc/usage.md"
---

--------

## Zusammenfassung {#synopsis}

    pgbouncer [-d][-v][-u user] <pgbouncer.ini>
    pgbouncer -V|-h

Unter Windows stehen folgende Optionen zur Verfügung:

    pgbouncer.exe [-v][-u user] <pgbouncer.ini>
    pgbouncer.exe -V|-h

Zusätzliche Optionen zur Einrichtung eines Windows-Dienstes:

    pgbouncer.exe --regservice   <pgbouncer.ini>
    pgbouncer.exe --unregservice <pgbouncer.ini>

--------

## Beschreibung {#description}

**pgbouncer** ist ein PostgreSQL-Verbindungspooler. Jede Zielanwendung kann sich mit **pgbouncer** verbinden, als wäre PgBouncer ein PostgreSQL-Server. **pgbouncer** stellt dann eine Verbindung zum tatsächlichen Server her oder verwendet eine bereits vorhandene Verbindung wieder.

Das Ziel von **pgbouncer** ist es, die Auswirkungen auf die Leistung beim Öffnen neuer Verbindungen zu PostgreSQL zu reduzieren.

Um die Transaktionssemantik beim Pooling von Verbindungen nicht zu beeinträchtigen, unterstützt **pgbouncer** beim Wechsel der Verbindungen mehrere Pooling-Varianten:

Sitzungs-Pooling

:   Die am wenigsten restriktive Methode. Sobald ein Client eine Verbindung herstellt, wird ihm für die gesamte Verbindungsdauer eine Serververbindung zugewiesen. Trennt der Client die Verbindung, wird die Serververbindung wieder in den Pool zurückgegeben. Dies ist die Standardmethode.

Transaktions-Pooling

:   Eine Serververbindung wird einem Client nur für die Dauer einer Transaktion zugewiesen.
    Sobald PgBouncer erkennt, dass die Transaktion beendet ist, wird die Serververbindung wieder in den Pool zurückgegeben.

Statement-Pooling

:   Die restriktivste Methode. Die Serververbindung wird unmittelbar nach Abschluss einer Abfrage in den Pool zurückgegeben. Transaktionen mit mehreren Anweisungen sind in diesem Modus nicht zulässig, da sie sonst nicht funktionieren würden.

Die Administrationsoberfläche von **pgbouncer** umfasst einige zusätzliche `SHOW`-Befehle. Sie stehen bei einer Verbindung mit der speziellen „virtuellen“ Datenbank **pgbouncer** zur Verfügung.

Seit Version 1.26.0 sendet PgBouncer bei der Anmeldung die `ParameterStatus`-Werte `pgbouncer.version`, `pgbouncer.pool_mode` und `pgbouncer.max_prepared_statements` an Clients. Treiber können anhand dieser Werte PgBouncer erkennen und ihr Verhalten anpassen. Die optionale Einstellung [`login_notify_message`](/de/docs/pgbouncer/config/#login_notify_message) sendet nach erfolgreicher Anmeldung eine Begrüßungsmeldung vom Typ NOTICE.

--------

## Schnellstart {#quick-start}

Die grundlegende Einrichtung und Verwendung erfolgen wie folgt:

1. Erstellen Sie eine Datei namens pgbouncer.ini. Weitere Informationen finden Sie in **pgbouncer(5)**. Ein einfaches Beispiel:

        [databases]
        template1 = host=localhost port=5432 dbname=template1

        [pgbouncer]
        listen_port = 6432
        listen_addr = localhost
        auth_type = md5
        auth_file = userlist.txt
        logfile = pgbouncer.log
        pidfile = pgbouncer.pid
        admin_users = someuser

2. Erstellen Sie eine Datei mit dem Namen `userlist.txt`, die die Benutzer enthält, die sich anmelden dürfen:

        "someuser" "same_password_as_in_server"

3. Starten Sie **pgbouncer**:

        $ pgbouncer -d pgbouncer.ini

4. Lassen Sie Ihre Anwendung (oder den **psql**-Client) eine Verbindung mit **pgbouncer** statt direkt mit dem PostgreSQL-Server herstellen:

        $ psql -p 6432 -U someuser template1

5. Verwalten Sie **pgbouncer**, indem Sie sich mit der speziellen Administrationsdatenbank **pgbouncer** verbinden und zunächst den Befehl `SHOW HELP;` ausführen:

        $ psql -p 6432 -U someuser pgbouncer
        pgbouncer=# SHOW HELP;
        NOTICE:  Console usage
        DETAIL:
          SHOW [HELP|CONFIG|DATABASES|POOLS|CLIENTS|SERVERS|SOCKETS|LISTS|VERSION|...]
          SET key = arg
          RELOAD
          PAUSE
          RESUME
          SHUTDOWN
          [...]

6. Wenn Sie pgbouncer.ini geändert haben, können Sie die Datei mit folgendem Befehl neu laden:

        pgbouncer=# RELOAD;

--------

## Befehlszeilenoptionen {#command-line-switches}

`-d`, `--daemon`
:   Im Hintergrund ausführen. Ohne diese Option wird der Prozess im Vordergrund ausgeführt.

    Im Daemon-Modus müssen sowohl `pidfile` als auch `logfile` oder `syslog`
    festgelegt sein. Nach dem Wechsel in den Hintergrund werden keine
    Protokollmeldungen mehr auf stderr ausgegeben.

    Hinweis: Funktioniert nicht unter Windows; dort muss **pgbouncer** als Dienst ausgeführt werden.

`-u` _USERNAME_, `--user=` _USERNAME_
:   Beim Start zum angegebenen Benutzer wechseln.

`-v`, `--verbose`
:   Ausführlichkeit erhöhen. Kann mehrfach angegeben werden.

`-q`, `--quiet`
:   Keine Protokollausgabe auf stderr. Dies beeinflusst nicht die Ausführlichkeit der Protokollierung,
    sondern nur die Verwendung von stderr.
    Für den Einsatz in init.d-Skripten vorgesehen.

`-V`, `--version`
:   Version anzeigen.

`-h`, `--help`
:   Kurzhilfe anzeigen.

`--regservice`
:   Win32: PgBouncer als Windows-Dienst registrieren. Der Wert des Konfigurationsparameters **service_name** wird als Registrierungsname verwendet.

`--unregservice`
:   Win32: Registrierung des Windows-Dienstes aufheben.

--------

## Admin-Konsole {#admin-console}

Die Konsole ist über eine normale Verbindung zur Datenbank **pgbouncer** erreichbar:

    $ psql -p 6432 pgbouncer

Nur Benutzer, die in den Konfigurationsparametern **admin_users** oder **stats_users** aufgeführt sind, dürfen sich an der Konsole anmelden. (Bei `auth_type=any` ist dagegen jeder Benutzer als stats_user zugelassen.)

Zusätzlich darf sich der Benutzer **pgbouncer** ohne Passwort anmelden, sofern die Anmeldung über einen Unix-Socket erfolgt und der Client dieselbe Unix-Benutzer-ID (UID) wie der laufende Prozess besitzt.

Die Admin-Konsole unterstützt derzeit nur das einfache Abfrageprotokoll. Einige Treiber verwenden für alle Befehle das erweiterte Abfrageprotokoll und können daher nicht mit der Admin-Konsole verwendet werden.

### Anzeigebefehle {#show-commands}

Die **SHOW**-Befehle geben Informationen aus. Jeder Befehl wird nachfolgend beschrieben.

#### SHOW STATS {#show-stats}

Zeigt Statistiken an. Die Gesamtwerte in diesem und verwandten Befehlen beziehen sich auf den Zeitraum seit dem Prozessstart; die Durchschnittswerte werden nach jedem `stats_period`-Intervall aktualisiert.

database
:   Statistiken werden pro Datenbank angezeigt.

total_xact_count
:   Gesamtanzahl der von **pgbouncer** gepoolten SQL-Transaktionen.

total_query_count
:   Gesamtanzahl der von **pgbouncer** gepoolten SQL-Befehle.

total_server_assignment_count
:   Gesamtzahl der Zuweisungen eines Servers an einen Client.

total_received
:   Gesamtvolumen des von **pgbouncer** empfangenen Netzwerkverkehrs in Byte.

total_sent
:   Gesamtvolumen des von **pgbouncer** gesendeten Netzwerkverkehrs in Byte.

total_xact_time
:   Gesamtzahl der Mikrosekunden, die **pgbouncer** während einer Transaktion mit PostgreSQL verbunden war – entweder im Leerlauf innerhalb der Transaktion oder bei der Ausführung von Abfragen.

total_query_time
:   Gesamtzahl der Mikrosekunden, die **pgbouncer** aktiv mit PostgreSQL verbunden war und Abfragen ausführte.

total_wait_time
:   Gesamte Wartezeit der Clients auf einen Server in Mikrosekunden. Sie wird aktualisiert, wenn einer Clientverbindung eine Backendverbindung zugewiesen wird.

total_client_parse_count
:   Gesamtzahl der von Clients erstellten vorbereiteten Anweisungen. Nur bei der Nachverfolgung benannter vorbereiteter Anweisungen relevant, siehe `max_prepared_statements`.

total_server_parse_count
:   Gesamtzahl der von **pgbouncer** auf einem Server erstellten vorbereiteten Anweisungen. Nur bei der Nachverfolgung benannter vorbereiteter Anweisungen relevant, siehe `max_prepared_statements`.

total_bind_count
:   Gesamtzahl der vorbereiteten Anweisungen, die von Clients zur Ausführung bereitgestellt und von **pgbouncer** an PostgreSQL weitergeleitet wurden. Nur bei der Nachverfolgung benannter vorbereiteter Anweisungen relevant, siehe `max_prepared_statements`.

total_client_login_count
:   Gesamtzahl erfolgreicher Clientanmeldungen.

avg_xact_count
:   Durchschnittliche Anzahl von Transaktionen pro Sekunde im letzten Statistikzeitraum.

avg_query_count
:   Durchschnittliche Anzahl von Abfragen pro Sekunde im letzten Statistikzeitraum.

avg_server_assignment_count
:   Durchschnittliche Anzahl der Zuweisungen eines Servers an einen Client pro Sekunde im letzten Statistikzeitraum.

avg_recv
:   Durchschnittlich pro Sekunde empfangene Byte (von Clients).

avg_sent
:   Durchschnittlich pro Sekunde gesendete Byte (an Clients).

avg_xact_time
:   Durchschnittliche Transaktionsdauer in Mikrosekunden.

avg_query_time
:   Durchschnittliche Abfragezeit in Mikrosekunden.

avg_wait_time
:   Wartezeit der Clients auf einen Server in Mikrosekunden (Durchschnitt der Wartezeiten für Clients, die während des aktuellen `stats_period` einem Backend zugewiesen wurden).

avg_client_parse_count
:   Durchschnittliche Zahl der von Clients pro Sekunde erstellten vorbereiteten Anweisungen. Nur bei der Nachverfolgung benannter vorbereiteter Anweisungen relevant, siehe `max_prepared_statements`.

avg_server_parse_count
:   Durchschnittliche Zahl der von **pgbouncer** pro Sekunde auf einem Server erstellten vorbereiteten Anweisungen. Nur bei der Nachverfolgung benannter vorbereiteter Anweisungen relevant, siehe `max_prepared_statements`.

avg_bind_count
:   Durchschnittliche Zahl der vorbereiteten Anweisungen, die pro Sekunde von Clients zur Ausführung bereitgestellt und von **pgbouncer** an PostgreSQL weitergeleitet wurden. Nur bei der Nachverfolgung benannter vorbereiteter Anweisungen relevant, siehe `max_prepared_statements`.

avg_client_login_count
:   Durchschnittliche Anzahl erfolgreicher Clientanmeldungen pro Sekunde.

#### SHOW STATS_TOTALS {#show-stats_totals}

Zeigt die kumulierten Statistiken pro Datenbank, die den **total_**-Feldern von **SHOW STATS** entsprechen. Die ausgegebenen Spaltennamen tragen kein Präfix **total_**: Die Spalte **total_query_count** heißt hier beispielsweise **query_count**.

#### SHOW STATS_AVERAGES {#show-stats_averages}

Teilmenge von **SHOW STATS** mit den Durchschnittswerten (**avg_**).

#### SHOW TOTALS {#show-totals}

Wie **SHOW STATS**, jedoch über alle Datenbanken aggregiert.

#### SHOW SERVERS {#show-servers}

type
:   S für Server.

user
:   Benutzername, mit dem **pgbouncer** die Verbindung zum Server herstellt.

database
:   Datenbankname.

replication
:   Gibt an, ob die Serververbindung Replikation nutzt. Kann **none**, **logical** oder **physical** sein.

state
:   Zustand der PgBouncer-Serververbindung, einer der folgenden: **active**, **idle**, **used**, **tested**, **new**, **active_cancel**, **being_canceled**.

addr
:   IP-Adresse des PostgreSQL-Servers.

port
:   Port des PostgreSQL-Servers.

local_addr
:   Verbindungsstartadresse auf dem lokalen Computer.

local_port
:   Verbindungsstartport auf dem lokalen Computer.

connect_time
:   Zeitpunkt des Verbindungsaufbaus.

request_time
:   Zeitpunkt der letzten Anfrage.

wait
:   Nicht für Serververbindungen verwendet.

wait_us
:   Nicht für Serververbindungen verwendet.

close_needed
:   1, wenn die Verbindung so schnell wie möglich geschlossen wird,
    weil das Neuladen einer Konfigurationsdatei oder eine DNS-Aktualisierung die
    Verbindungsinformationen geändert hat oder **RECONNECT** ausgeführt wurde.

ptr
:   Adresse des internen Objekts für diese Verbindung.

link
:   Adresse der Clientverbindung, mit der der Server verknüpft ist.

remote_pid
:   PID des Backend-Serverprozesses. Wurde die Verbindung über einen Unix-Socket hergestellt
    und unterstützt das Betriebssystem das Abrufen von Prozess-ID-Informationen, ist dies die
    Betriebssystem-PID. Andernfalls wird der Wert aus dem vom Server gesendeten Abbruchpaket entnommen;
    bei einem PostgreSQL-Server sollte dies die PID sein, bei einer anderen PgBouncer-Instanz ist es eine Zufallszahl.

tls
:   Eine Zeichenkette mit TLS-Verbindungsinformationen oder leer, wenn TLS nicht verwendet wird.

application_name
:   Ein String, der den `application_name` auf der verknüpften Clientverbindung enthält,
    oder leer, wenn dieser nicht gesetzt ist oder keine verknüpfte Verbindung besteht.

prepared_statements
:  Die Anzahl der auf dem Server vorbereiteten Anweisungen. Diese Zahl ist durch die Einstellung `max_prepared_statements` begrenzt.

id
:   Eindeutige ID für den Server.

#### SHOW CLIENTS {#show-clients}

type
:   C für Client.

user
:   Benutzername der Clientverbindung.

database
:   Datenbankname.

replication
:   Gibt an, ob die Clientverbindung Replikation nutzt. Kann **none**, **logical** oder **physical** sein.

state
:   Zustand der Clientverbindung, einer der Werte **active** (Clientverbindungen, die mit Serververbindungen verknüpft sind),
    **idle** (Clientverbindungen ohne ausstehende Abfragen), **waiting**,
    **active_cancel_req** oder **waiting_cancel_req**.

addr
:   IP-Adresse des Clients.

port
:   Quellport des Clients.

local_addr
:   Lokale Endadresse der Verbindung.

local_port
:   Lokaler Endport der Verbindung.

connect_time
:   Zeitstempel des Verbindungsaufbaus.

request_time
:   Zeitstempel der letzten Clientanfrage.

wait
:   Aktuelle Wartezeit in Sekunden.

wait_us
:   Mikrosekundenanteil der aktuellen Wartezeit.

close_needed
:   Nicht für Clients verwendet.

ptr
:   Adresse des internen Objekts für diese Verbindung.

link
:   Adresse der Serververbindung, der der Client zugeordnet ist.

remote_pid
:   Prozess-ID, falls der Client über einen Unix-Socket verbunden ist
    und das Betriebssystem die ID abrufen kann.

tls
:   Ein String mit TLS-Verbindungsinformationen oder leer, falls TLS nicht verwendet wird.

application_name
:   Ein String, der den `application_name` enthält, der vom Client
    für diese Verbindung festgelegt wurde, oder leer, falls kein solcher Wert gesetzt wurde.

prepared_statements
:  Anzahl der vom Client vorbereiteten Anweisungen.

id
:   Eindeutige ID für den Client.

#### SHOW POOLS {#show-pools}

Für jede Kombination aus Datenbank und Benutzer wird ein neuer Pool-Eintrag erstellt.

database
:   Datenbankname.

user
:   Benutzername.

cl_active
:   Clientverbindungen, die entweder Serververbindungen zugeordnet sind oder sich im Leerlauf befinden, ohne dass Abfragen zur Verarbeitung anstehen.

cl_waiting
:   Clientverbindungen, die Abfragen gesendet, aber noch keine Serververbindung erhalten haben.

cl_active_cancel_req
:   Clientverbindungen, die Abfrageabbrüche an den Server weitergeleitet haben und auf dessen Antwort warten.

cl_waiting_cancel_req
:   Clientverbindungen, die noch keine Abbruchanfragen an den Server weitergeleitet haben.

sv_active
:   Serververbindungen, die mit einem Client verbunden sind.

sv_active_cancel
:   Serververbindungen, die derzeit eine Abbruchanfrage weiterleiten.

sv_being_canceled
:   Serververbindungen, die normalerweise in den Leerlauf wechseln könnten, damit jedoch warten, bis alle noch laufenden Anforderungen zum Abbruch einer Abfrage auf diesem Server abgeschlossen sind.

sv_idle
:   Serververbindungen, die ungenutzt sind und sofort für Clientanfragen verwendet werden können.

sv_used
:   Serververbindungen, die länger als `server_check_delay` inaktiv waren, sodass `server_check_query` ausgeführt werden muss, bevor sie erneut verwendet werden können.

sv_tested
:   Serververbindungen, die derzeit entweder `server_reset_query` oder `server_check_query` ausführen.

sv_login
:   Serververbindungen, die gerade angemeldet werden.

maxwait
:   Bisherige Wartezeit des ersten (ältesten) Clients in der Warteschlange in Sekunden.
    Steigt dieser Wert, verarbeitet der aktuelle Serverpool die Anfragen nicht schnell genug.
    Ursache kann ein überlasteter Server oder eine zu kleine **pool_size**-Einstellung sein.

maxwait_us
:   Mikrosekundenanteil der maximalen Wartezeit.

pool_mode
:   Der verwendete Pool-Modus.

load_balance_hosts
:   Die verwendete load_balance_hosts-Einstellung, wenn der Host des Pools eine kommagetrennte Liste enthält.

#### SHOW PEER_POOLS {#show-peer_pools}

Für jeden konfigurierten Peer wird ein neuer peer_pool-Eintrag erstellt.

peer_id
:   ID des konfigurierten Peer-Eintrags.

cl_active_cancel_req
:   Clientverbindungen, die Abfrageabbrüche an den Server weitergeleitet haben und auf dessen Antwort warten.

cl_waiting_cancel_req
:   Clientverbindungen, die Abbruchanfragen noch nicht an den Server weitergeleitet haben.

sv_active_cancel
:   Serververbindungen, die derzeit eine Abbruchanfrage weiterleiten.

sv_login
:   Serververbindungen, deren Anmeldung gerade läuft.

#### SHOW LISTS {#show-lists}

Zeigt die folgenden internen Listen und ihre Elementanzahl an. Jede Liste steht in einer eigenen Zeile mit den Spalten **list** und **items**:

databases
:   Anzahl der Datenbanken.

users
:   Anzahl der Benutzer.

peers
:   Anzahl der konfigurierten Peers.

pools
:   Anzahl der Pools.

peer_pools
:   Anzahl der Peer-Pools.

free_clients
:   Anzahl freier Clients. Diese Clients sind getrennt, PgBouncer behält jedoch den für sie reservierten Speicher bei, um ihn für künftige Clients wiederzuverwenden und neue Speicherzuweisungen zu vermeiden.

used_clients
:   Anzahl genutzter Clients.

login_clients
:   Anzahl der Clients im **login**-Zustand.

free_servers
:   Anzahl freier Server. Diese Server sind getrennt, PgBouncer behält jedoch den für sie reservierten Speicher bei, um ihn für künftige Server wiederzuverwenden und neue Speicherzuweisungen zu vermeiden.

used_servers
:   Anzahl genutzter Server.

dns_names
:   Anzahl der DNS-Namen im Cache.

dns_zones
:   Anzahl der DNS-Zonen im Cache.

dns_queries
:   Anzahl der laufenden DNS-Abfragen.

dns_pending
:   Nicht verwendet.

#### SHOW USERS {#show-users}

name
:   Der Benutzername.

pool_size
:   Benutzerspezifische Überschreibung von pool_size oder eine leere Zeichenfolge, falls nicht gesetzt.

reserve_pool_size
:   Benutzerspezifische Überschreibung von reserve_pool_size oder eine leere Zeichenfolge, falls nicht gesetzt.

pool_mode
:   Benutzerspezifische Überschreibung von pool_mode oder NULL, falls nicht gesetzt.

max_user_connections
:   Benutzerspezifische Einstellung max_user_connections. Ist sie für diesen Benutzer nicht gesetzt, wird der Standardwert angezeigt.

current_connections
:   Aktuelle Anzahl der Serververbindungen, die dieser Benutzer zu allen Servern geöffnet hat.

max_user_client_connections
:   Benutzerspezifische Einstellung max_user_client_connections. Ist sie für diesen Benutzer nicht gesetzt, wird der Standardwert angezeigt.

current_client_connections
:   Aktuelle Anzahl der Clientverbindungen, die dieser Benutzer zu PgBouncer geöffnet hat.

#### SHOW DATABASES {#show-databases}

name
:   Name des konfigurierten Datenbankeintrags.

host
:   Host, zu dem PgBouncer eine Verbindung herstellt.

port
:   Port, zu dem PgBouncer eine Verbindung herstellt.

database
:   Tatsächlicher Name der Datenbank, zu der PgBouncer eine Verbindung herstellt.

force_user
:   Ist ein Benutzer Teil der Verbindungszeichenfolge, wird für die Verbindung zwischen PgBouncer und PostgreSQL unabhängig vom Clientbenutzer dieser angegebene Benutzer erzwungen.

pool_size
:   Maximale Anzahl an Serververbindungen.

min_pool_size
:   Minimale Anzahl an Serververbindungen.

reserve_pool_size
:   Maximale Anzahl zusätzlicher Verbindungen für diese Datenbank.

server_lifetime
:   Maximale Lebensdauer einer Serververbindung für diese Datenbank.

pool_mode
:   Datenbankspezifische Überschreibung von pool_mode oder NULL, wenn stattdessen der Standardwert verwendet wird.

load_balance_hosts
:   Datenbankspezifische load_balance_hosts-Einstellung, falls der Host eine kommagetrennte Liste enthält.

max_connections
:   Maximale Anzahl zulässiger Serververbindungen für diese Datenbank, wie durch **max_db_connections** global oder pro Datenbank festgelegt.

current_connections
:   Aktuelle Anzahl der Serververbindungen für diese Datenbank.

max_client_connections
:   Maximale Anzahl zulässiger Clientverbindungen für diese Datenbank. Maßgeblich ist die datenbankspezifische Einstellung max_db_client_connections oder, falls nicht gesetzt, deren globaler Standardwert.

current_client_connections
:   Aktuelle Anzahl der Clientverbindungen für diese Datenbank.

paused
:   1, wenn diese Datenbank derzeit pausiert ist, sonst 0.

disabled
:   1, wenn diese Datenbank derzeit deaktiviert ist, sonst 0.

#### SHOW PEERS {#show-peers}

peer_id
:   ID des konfigurierten Peer-Eintrags.

host
:   Host, zu dem PgBouncer eine Verbindung herstellt.

port
:   Port, zu dem PgBouncer eine Verbindung herstellt.

pool_size
:   Maximale Anzahl der Serververbindungen, die zu diesem Peer hergestellt werden können.

#### SHOW SOCKETS, SHOW ACTIVE_SOCKETS {#show-sockets-show-active_sockets}

Zeigt systemnahe Informationen über alle oder nur die aktiven Sockets an. Dazu gehören die unter **SHOW CLIENTS** und **SHOW SERVERS** angezeigten Informationen sowie weitere systemnahe Angaben.

#### SHOW CONFIG {#show-config}

Zeigt die aktuellen Konfigurationseinstellungen mit einer Einstellung pro Zeile und den folgenden Spalten:

key
:   Name der Konfigurationsvariable.

value
:   Konfigurationswert.

default
:   Standardwert der Konfiguration.

changeable
:   Gibt mit **yes** oder **no** an, ob die Variable zur Laufzeit geändert werden kann.
    Wenn **no**, kann die Variable nur beim Start geändert werden. Verwenden Sie **SET**, um eine Variable zur Laufzeit zu ändern.

#### SHOW MEM {#show-mem}

Zeigt systemnahe Informationen über die aktuellen Größen verschiedener interner Speicherreservierungen an. Diese Angaben können sich ändern.

#### SHOW DNS_HOSTS {#show-dns_hosts}

Zeigt Hostnamen im DNS-Cache an.

hostname
:   Hostname.

ttl
:   Sekunden bis zur nächsten Abfrage.

addrs
:   Kommagetrennte Liste von Adressen.

#### SHOW DNS_ZONES {#show-dns_zones}

Zeigt DNS-Zonen im Cache an.

zonename
:   Zonenname.

serial
:   Aktuelle Seriennummer.

count
:   Anzahl von Hostnamen, die dieser Zone zugeordnet sind.

#### SHOW VERSION {#show-version}

Zeigt die PgBouncer-Version als Zeichenkette an.

#### SHOW STATE {#show-state}

Zeigt die Zustandseinstellungen von PgBouncer an. Mögliche Zustände sind active und paused.

### Befehle zur Prozesskontrolle {#process-controlling-commands}

#### PAUSE [db] {#pause-db}

PgBouncer versucht, alle Serververbindungen zu trennen. Jede Verbindung wird erst getrennt, nachdem sie entsprechend dem Pooling-Modus des Serverpools freigegeben wurde (beim Transaktions-Pooling muss die Transaktion abgeschlossen sein, beim Statement-Pooling die Anweisung und beim Sitzungs-Pooling muss der Client die Verbindung trennen).
Der Befehl kehrt erst zurück, nachdem alle Serververbindungen getrennt wurden.
Für Datenbankneustarts vorgesehen.

Wird ein Datenbankname angegeben, wird nur diese Datenbank pausiert.

Neue Clientverbindungen zu einer pausierten Datenbank warten, bis **RESUME** aufgerufen wird.

#### DISABLE db {#disable-db}

Weist alle neuen Clientverbindungen zur angegebenen Datenbank ab.

#### ENABLE db {#enable-db}

Ermöglicht nach einem vorherigen **DISABLE**-Befehl wieder neue Clientverbindungen.

#### RECONNECT [db] {#reconnect-db}

Schließt jede offene Serververbindung für die angegebene Datenbank oder für alle Datenbanken, sobald sie entsprechend dem Pooling-Modus freigegeben wird, selbst wenn ihre Lebensdauer noch nicht abgelaufen ist. Neue Serververbindungen können sofort hergestellt werden und verbinden sich bei Bedarf gemäß den Einstellungen der Poolgröße.

Dieser Befehl ist nützlich, wenn sich die Einrichtung der Serververbindung geändert hat, etwa für einen schrittweisen Wechsel zu einem neuen Server. Er muss *nicht* ausgeführt werden, wenn die Verbindungszeichenfolge in pgbouncer.ini geändert und neu geladen wurde (siehe **RELOAD**) oder wenn sich die DNS-Auflösung geändert hat; in diesen Fällen wird ein gleichwertiger Befehl automatisch ausgeführt. Er ist nur erforderlich, wenn eine dem PgBouncer nachgelagerte Komponente die Verbindungen weiterleitet.

Nach Ausführung dieses Befehls kann es längere Zeit dauern, bis alle Serververbindungen zum neuen Ziel führen; einige können noch das alte Ziel verwenden. Dies ist voraussichtlich nur beim Umschalten von schreibgeschütztem Datenverkehr zwischen schreibgeschützten Replikaten oder zwischen Knoten einer Multimaster-Replikation sinnvoll. Müssen alle Verbindungen gleichzeitig umgeschaltet werden, wird stattdessen **PAUSE** empfohlen. Sollen Serververbindungen ohne Wartezeit geschlossen werden, etwa bei einem Notfall-Failover statt eines schrittweisen Switchovers, kommt auch **KILL** infrage.

#### KILL [db] {#kill-db}

Trennt sofort alle Client- und Serververbindungen für die angegebene Datenbank oder für alle Datenbanken mit Ausnahme der Administrationsdatenbank.

Neue Clientverbindungen zu einer Datenbank, für die KILL ausgeführt wurde, warten, bis **RESUME** aufgerufen wird.

#### KILL_CLIENT id {#kill_client-id}

Trennt sofort die angegebene Clientverbindung sowie alle Serververbindungen des betreffenden Clients. Der Client, dessen Verbindung getrennt werden soll, wird durch den `id`-Wert identifiziert, der mit dem Befehl `SHOW CLIENTS` ermittelt werden kann.

Ein Beispielbefehl sieht etwa so aus: `KILL_CLIENT 1234`.

#### RESUME [db] {#resume-db}

Nimmt den Betrieb nach einem vorherigen **KILL**- oder **PAUSE**-Befehl wieder auf.

#### SHUTDOWN {#shutdown}

Der PgBouncer-Prozess wird beendet.

#### SHUTDOWN WAIT_FOR_SERVERS {#shutdown-wait_for_servers}

Nimmt keine neuen Verbindungen mehr an und fährt herunter, nachdem alle Serververbindungen freigegeben wurden.
Dies entspricht im Wesentlichen der Ausführung von **PAUSE** und **SHUTDOWN**. Zusätzlich werden bereits während des Wartens auf **PAUSE** keine neuen Verbindungen mehr angenommen und Clients, die auf eine Serververbindung warten, sofort getrennt. Beachten Sie, dass Unix-Sockets während des Herunterfahrens geöffnet bleiben, aber nur Verbindungen zur PgBouncer-Administrationskonsole annehmen.

#### SHUTDOWN WAIT_FOR_CLIENTS {#shutdown-wait_for_clients}

Nimmt keine neuen Verbindungen mehr an und beendet den Prozess, sobald alle vorhandenen Clients ihre Verbindung getrennt haben. Beachten Sie, dass Unix-Sockets während des Herunterfahrens geöffnet bleiben, aber nur Verbindungen zur PgBouncer-Administrationskonsole annehmen. Mit diesem Befehl lässt sich nach dem folgenden Verfahren ein rollierender Neustart zweier PgBouncer-Prozesse ohne Ausfallzeit durchführen:

1. Lassen Sie zwei oder mehr PgBouncer-Prozesse mit `so_reuseport` auf demselben Port laufen ([Peering konfigurieren](/de/docs/pgbouncer/config/#section-peers) wird empfohlen, ist aber nicht erforderlich). Für einen Neustart ohne Ausfallzeit werden diese Prozesse nacheinander neu gestartet. So können die übrigen weiterhin Verbindungen annehmen, während jeweils ein Prozess neu startet.
2. Wählen Sie den zuerst neu zu startenden Prozess; nennen wir ihn A.
3. Führen Sie für Prozess A `SHUTDOWN WAIT_FOR_CLIENTS` aus (oder senden Sie ihm `SIGTERM`).
4. Veranlassen Sie alle Clients, ihre Verbindung neu herzustellen. Warten Sie dazu etwa, bis der clientseitige Pooler aufgrund seines `server_idle_timeout` (oder einer ähnlichen Konfiguration) Neuverbindungen auslöst. Wird kein clientseitiger Pooler verwendet, können stattdessen die Clients neu gestartet werden. Sobald alle Clients wieder verbunden sind, beendet sich Prozess A automatisch, da keine Clients mehr mit ihm verbunden sind.
5. Starten Sie Prozess A erneut.
6. Wiederholen Sie die Schritte 3, 4 und 5 nacheinander für jeden verbleibenden Prozess, bis alle Prozesse neu gestartet wurden.

#### RELOAD {#reload}

Der PgBouncer-Prozess lädt seine Konfigurationsdateien neu und aktualisiert änderbare Einstellungen. Dazu gehören die Hauptkonfigurationsdatei sowie die Dateien, die durch die Einstellungen `auth_file` und `auth_hba_file` angegeben sind.

PgBouncer erkennt, wenn das Neuladen einer Konfigurationsdatei die Verbindungsparameter einer Datenbankdefinition ändert. Eine vorhandene Serververbindung zum alten Ziel wird bei ihrer nächsten Freigabe entsprechend dem Pooling-Modus geschlossen; neue Serververbindungen verwenden sofort die aktualisierten Verbindungsparameter.

#### WAIT_CLOSE [db] {#wait_close-db}

Wartet, bis alle Serververbindungen der angegebenen Datenbank oder aller Datenbanken den Zustand "close_needed" verlassen haben (siehe **SHOW SERVERS**). Der Befehl kann nach **RECONNECT** oder **RELOAD** aufgerufen werden, um zu warten, bis die jeweilige Konfigurationsänderung vollständig aktiviert ist, beispielsweise in Switchover-Skripten.

### Weitere Befehle {#other-commands}

#### SET key = arg {#set-key--arg}

Ändert eine Konfigurationseinstellung (siehe auch **SHOW CONFIG**). Zum Beispiel:

    SET log_connections = 1;
    SET server_check_query = 'select 2';

(Beachten Sie, dass dieser Befehl in der PgBouncer-Administrationskonsole ausgeführt wird und
PgBouncer-Einstellungen setzt. Ein in einer anderen Datenbank ausgeführter **SET**-Befehl wird
wie jeder andere SQL-Befehl an das PostgreSQL-Backend weitergeleitet.)

### Signale {#signals}

SIGHUP
:   Konfiguration neu laden. Entspricht dem Befehl **RELOAD** an der Konsole.

SIGTERM
:   Besonders sicheres Herunterfahren. Wartet, bis alle vorhandenen Clients ihre Verbindung getrennt haben, nimmt jedoch keine neuen Verbindungen an. Dies entspricht **SHUTDOWN WAIT_FOR_CLIENTS** an der Konsole. Wird dieses Signal empfangen, während bereits ein Herunterfahren läuft, wird statt des „besonders sicheren Herunterfahrens“ ein „sofortiges Herunterfahren“ ausgelöst. In PgBouncer-Versionen vor 1.23.0 löste dieses Signal ein „sofortiges Herunterfahren“ aus.

SIGINT
:   Sicheres Herunterfahren. Entspricht **SHUTDOWN WAIT_FOR_SERVERS** an der Konsole. Wird dieses Signal empfangen, während bereits ein Herunterfahren läuft, wird statt des „sicheren Herunterfahrens“ ein „sofortiges Herunterfahren“ ausgelöst.

SIGQUIT
:   Sofortiges Herunterfahren. Entspricht **SHUTDOWN** an der Konsole.

SIGUSR1
:   Entspricht **PAUSE** an der Konsole.

SIGUSR2
:   Entspricht **RESUME** an der Konsole.

### Libevent-Einstellungen {#libevent-settings}

Aus der Libevent-Dokumentation:

> Es ist möglich, die Unterstützung für epoll, kqueue, devpoll, poll oder select zu deaktivieren, indem die Umgebungsvariable EVENT_NOEPOLL, EVENT_NOKQUEUE, EVENT_NODEVPOLL, EVENT_NOPOLL oder EVENT_NOSELECT jeweils gesetzt wird.
>
> Durch Setzen der Umgebungsvariablen EVENT_SHOW_METHOD zeigt libevent die verwendete Kernel-Benachrichtigungsmethode an.

--------

## Siehe auch {#see-also}

pgbouncer(5) – Handbuchseite mit Beschreibungen der Konfigurationseinstellungen

<https://www.pgbouncer.org/>
