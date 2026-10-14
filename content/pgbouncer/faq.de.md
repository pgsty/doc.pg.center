---
title: "Häufig gestellte Fragen"
linkTitle: "FAQ"
weight: 90
description: "Häufig gestellte Fragen zu PgBouncer"
icon: fa-solid fa-circle-question
module: [PGBOUNCER]
categories: [Referenz]
upstream_link: "https://www.pgbouncer.org/faq.html"
---

--------

## Wie stelle ich eine Verbindung zu PgBouncer her? {#how-to-connect-to-pgbouncer}

PgBouncer verhält sich wie ein PostgreSQL-Server. Richten Sie Ihren Client daher
einfach auf den PgBouncer-Port.

--------

## Wie lassen sich Abfragen auf mehrere Server verteilen? {#how-to-load-balance-queries-between-several-servers}

PgBouncer unterstützt eine durch Kommas getrennte Liste von Hosts in der
Datenbank-Verbindungszeichenfolge. Mit
[`load_balance_hosts=round-robin`](/de/pgbouncer/config/#load_balance_hosts)
werden neue Serververbindungen reihum auf diese Hosts verteilt. Beispiel:

```ini
[databases]
app = host=pg1,pg2 port=5432 dbname=app load_balance_hosts=round-robin
```

Auch externe Werkzeuge können verwendet werden:

1.  DNS-Round-Robin. Hinterlegen Sie mehrere IP-Adressen für einen DNS-Namen.
    PgBouncer führt nicht bei jeder neuen Verbindung eine DNS-Abfrage durch.
    Stattdessen speichert es alle IP-Adressen im Cache und verteilt die
    Verbindungen intern per Round-Robin. Hinweis: Sind einem Namen mehr als 8
    IP-Adressen zugeordnet, muss das DNS-Backend das EDNS0-Protokoll
    unterstützen. Einzelheiten finden sich unter
    [Unterstützung für DNS-Abfragen](/de/pgbouncer/install/#dns-lookup-support).

2.  Verwenden Sie einen Load-Balancer für TCP-Verbindungen. Sowohl
    [LVS](http://www.linuxvirtualserver.org/) als auch
    [HAProxy](https://www.haproxy.org/) scheinen dafür gut geeignet. Auf PgBouncer-Seite
    kann es sinnvoll sein, `server_lifetime` zu verkürzen und
    `server_round_robin` zu aktivieren: Standardmäßig werden inaktive
    Verbindungen nach dem LIFO-Prinzip wiederverwendet, was bei Lastverteilung
    ungünstig sein kann.

--------

## Wie lässt sich ein Failover durchführen? {#how-to-failover}

Bei einer durch Kommas getrennten Hostliste und
[`load_balance_hosts=disable`](/de/pgbouncer/config/#load_balance_hosts)
verwendet PgBouncer denselben Host weiter, bis ein Verbindungsversuch scheitert.
Dann versucht es den nächsten Host. Dabei werden die Rollen Primärserver und
Replikat nicht erkannt. Für ein Failover, das Änderungen an der
Datenbanktopologie folgt, sind externe Werkzeuge zu verwenden:

1. DNS-Neukonfiguration: Wenn die IP-Adresse geändert wird, auf die ein
   DNS-Name verweist, verbindet sich PgBouncer erneut mit dem neuen Server.
   Dieses Verhalten lässt sich über zwei Konfigurationsparameter steuern:
   `dns_max_ttl` legt die Gültigkeitsdauer eines Hostnamens fest;
   `dns_zone_check_period` bestimmt, wie häufig der SOA-Eintrag einer Zone auf
   Änderungen geprüft wird. Hat sich der SOA-Eintrag geändert, fragt PgBouncer
   alle Hostnamen dieser Zone erneut ab.

2. Tragen Sie einen neuen Host in die Konfiguration ein und lassen Sie PgBouncer
   sie neu laden: Senden Sie SIGHUP oder verwenden Sie den Befehl `RELOAD` in der
   Konsole. PgBouncer erkennt die geänderte Hostkonfiguration und verbindet sich
   mit dem neuen Server.

3. Verwenden Sie den Befehl `RECONNECT`. Er ist für Situationen vorgesehen, in
   denen sich keine der beiden vorherigen Optionen anwenden lässt, etwa wenn
   Sie den zuvor erwähnten HAProxy-Load-Balancer einsetzen, um Verbindungen
   hinter PgBouncer weiterzuleiten. `RECONNECT` öffnet einfach alle
   Serververbindungen neu.
   Führen Sie den Befehl aus, nachdem die andere Komponente ihre
   Routinginformationen geändert hat.

--------

## Wie lassen sich vorbereitete Anweisungen mit Sitzungs-Pooling verwenden? {#how-to-use-prepared-statements-with-session-pooling}

Im Sitzungs-Pooling muss die Abfrage zum Zurücksetzen alte vorbereitete Anweisungen
bereinigen. Hierzu kann `server_reset_query = DISCARD ALL;` oder zumindest
`DEALLOCATE ALL;` verwendet werden.

--------

## Wie lassen sich vorbereitete Anweisungen mit Transaktions-Pooling verwenden? {#how-to-use-prepared-statements-with-transaction-pooling}

Seit Version 1.21.0 kann PgBouncer vorbereitete Anweisungen im
Transaktions-Pooling nachverfolgen und sicherstellen, dass sie bei Bedarf auf
der zugeordneten Serververbindung vorbereitet werden. Um diese Funktion zu
aktivieren, muss `max_prepared_statements` auf einen von null verschiedenen
Wert gesetzt werden (der Standardwert ist 200). Weitere Einzelheiten finden Sie in der [Dokumentation zu
`max_prepared_statements`](/de/pgbouncer/config/#max_prepared_statements).

Je nach verwendeter Version kann PHP/PDO mit der Unterstützung vorbereiteter
Anweisungen durch PgBouncer inkompatibel sein ([#991]). PHP/PDO ist nur bei
Verwendung von [PHP 8.4+ **und** libpq 17][php-fix] kompatibel. Für
Installationen mit älteren Versionen empfiehlt sich daher ein Upgrade oder die
Deaktivierung vorbereiteter Anweisungen auf Clientseite.

[php-fix]: https://github.com/php/php-src/commit/f35ad560b468e3e0a6c289949ba9b19af4fa3e7b

[#991]: https://github.com/pgbouncer/pgbouncer/issues/991

### Vorbereitete Anweisungen in JDBC deaktivieren {#disabling-prepared-statements-in-jdbc}

Die richtige Vorgehensweise für JDBC besteht darin, den Parameter `prepareThreshold=0`
zur Verbindungszeichenfolge hinzuzufügen.

### Vorbereitete Anweisungen in PHP/PDO deaktivieren {#disabling-prepared-statements-in-phppdo}

Um serverseitig vorbereitete Anweisungen zu deaktivieren, muss das
PDO-Attribut `PDO::ATTR_EMULATE_PREPARES` auf `true` gesetzt werden, entweder beim
Verbindungsaufbau:

    $db = new PDO("dsn", "user", "pass", array(PDO::ATTR_EMULATE_PREPARES => true));

oder später:

    $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, true);

--------

## Wie aktualisiere ich PgBouncer, ohne Verbindungen zu unterbrechen? {#how-to-upgrade-pgbouncer-without-dropping-connections}

Sie können einen rollierenden Neustart nach dem Verfahren im [Dokumentationsabschnitt
zu `SHUTDOWN WAIT_FOR_CLIENTS`](/de/pgbouncer/usage/#shutdown-wait_for_clients)
durchführen.

--------

## Wie finde ich heraus, welcher Client welcher Serververbindung zugeordnet ist? {#how-to-know-which-client-is-on-which-server-connection}

Verwenden Sie die Befehle `SHOW CLIENTS` und `SHOW SERVERS` in der Konsole.

1.  Ordnen Sie mithilfe von `ptr` und `link` eine lokale Clientverbindung der
    Serververbindung zu.

2.  Identifizieren Sie die vom Client ausgehende TCP-Verbindung anhand von
    `addr` und `port` der Clientverbindung.

3.  Identifizieren Sie die zum Server führende TCP-Verbindung anhand von
    `local_addr` und `local_port`.

--------

## Soll PgBouncer auf dem Webserver oder dem Datenbankserver installiert werden? {#should-pgbouncer-be-installed-on-the-web-server-or-database-server}

Das hängt davon ab.

Eine Installation von PgBouncer auf dem Webserver ist sinnvoll, wenn
kurzlebige Verbindungen genutzt werden, weil sie die Latenz beim
Verbindungsaufbau minimiert. (TCP benötigt mehrere Paketumlaufzeiten, bevor
eine Verbindung nutzbar ist.) Eine Installation von PgBouncer auf dem
Datenbankserver eignet sich, wenn viele unterschiedliche Hosts (z. B.
Webserver) darauf zugreifen. Ihre Verbindungen können dann gemeinsam optimiert
werden.

PgBouncer kann sowohl auf dem Webserver als auch auf dem Datenbankserver
installiert werden. Nachteilig ist, dass jeder zusätzliche PgBouncer-Hop jeder
Abfrage eine geringe Latenz hinzufügt.

Letztlich müssen Sie testen, welches Modell Ihre Leistungsanforderungen am
besten erfüllt. Sie sollten außerdem berücksichtigen, wie sich die gewählte
PgBouncer-Position auf das Failover Ihrer Anwendungen auswirkt, wenn ein
Webserver beziehungsweise der Datenbankserver ausfällt.
