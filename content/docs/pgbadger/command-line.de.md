---
title: "Befehlszeilenreferenz"
linkTitle: "Befehlszeile"
weight: 30
description: "Vollständige pgBadger-Befehlssyntax, Optionen, Remote-Eingabe, Rückgabecodes und Beispiele"
search_keywords: [--Jobs, --anonymize, --appname, --average, --begin, --charset, --command, --csv-separator, --day-report, --dbclient, --dbname, --dbuser, --disable-autovacuum, --disable-checkpoint, --disable-connection, --disable-error, --disable-hourly, --disable-lock, --disable-query, --disable-session, --disable-temporary, --disable-type, --dns-resolv, --dump-all-queries, --dump-raw-csv, --enable-checksum, --end, --exclude-appname, --exclude-client, --exclude-db, --exclude-file, --exclude-line, --exclude-query, --exclude-time, --exclude-user, --explain-url, --explode, --extension, --extra-files, --format, --help, --histo-average, --histogram-query, --histogram-session, --html-outdir, --ident, --include-file, --include-pid, --include-query, --include-session, --include-time, --incremental, --iso-week-number, --jobs, --journalctl, --keep-comments, --last-parsed, --log-duration, --log-timezone, --logfile-list, --maxlength, --month-report, --no-fork, --no-multiline, --no-prettify, --no-process-info, --no-progressbar, --no-week, --nocomment, --noexplain, --nograph, --noreport, --normalized-only, --outdir, --outfile, --pgbouncer-only, --pid-dir, --pid-file, --pie-limit, --prefix, --prettify-json, --query-numbering, --quiet, --rebuild, --remote-host, --retention, --sample, --select-only, --ssh-identity, --ssh-option, --ssh-port, --ssh-program, --ssh-sudo, --ssh-timeout, --ssh-user, --start-monday, --tempdir, --timezone, --title, --top, --verbose, --version, --watch-mode, --wide-char, --zcat, JSON::XS, Jobs, all, anonymize, appname, autovacuum, average, begin, char, charset, checkpoint, checksum, client, command, comments, connection, csv, csv-separator, csvlog, day, day-report, db, dbclient, dbname, dbuser, dir, disable, disable-autovacuum, disable-checkpoint, disable-connection, disable-error, disable-hourly, disable-lock, disable-query, disable-session, disable-temporary, disable-type, dns, dns-resolv, dump, dump-all-queries, dump-raw-csv, duration, enable, enable-checksum, end, error, exclude, exclude-appname, exclude-client, exclude-db, exclude-file, exclude-line, exclude-query, exclude-time, exclude-user, explain, explain-url, explode, extension, extra, extra-files, file, files, fork, format, help, histo, histo-average, histogram, histogram-query, histogram-session, host, hourly, html, html-outdir, ident, identity, include, include-file, include-pid, include-query, include-session, include-time, incremental, info, iso, iso-week-number, jobs, journalctl, json, jsonlog, keep, keep-comments, last, last-parsed, limit, line, list, lock, log, log-duration, log-timezone, log_duration, log_line_prefix, log_statement, logfile, logfile-list, logplex, maxlength, mode, monday, month, month-report, multiline, no, no-fork, no-multiline, no-prettify, no-process-info, no-progressbar, no-week, nocomment, noexplain, nograph, noreport, normalized, normalized-only, number, numbering, only, option, outdir, outfile, parsed, pgbouncer, pgbouncer-only, pid, pid-dir, pid-file, pie, pie-limit, port, prefix, prettify, prettify-json, process, program, progressbar, queries, query, query-numbering, quiet, raw, rebuild, redshift, remote, remote-host, report, resolv, retention, sample, select, select-only, separator, session, ssh, ssh-identity, ssh-option, ssh-port, ssh-program, ssh-sudo, ssh-timeout, ssh-user, start, start-monday, stderr, sudo, syslog, tempdir, temporary, time, timeout, timezone, title, top, type, url, user, verbose, version, watch, watch-mode, week, wide, wide-char, zcat]
search_boost: 8
icon: fa-solid fa-terminal
module: [PGBADGER]
categories: [Referenz]
aliases: [/pgbadger/command-line/]
upstream_link: "https://github.com/darold/pgbadger/tree/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

## Aufruf und Optionen {#usage-and-options}

Aufruf: pgbadger [options] logfile [...]

```text
PostgreSQL-Protokollanalyse mit detaillierten Berichten und Diagrammen.
```

Argumente:

```text
logfile kann eine einzelne Protokolldatei, eine Dateiliste oder einen Shell-Befehl
bezeichnen, der eine Dateiliste zurückgibt. Für Protokollinhalte aus stdin verwenden
Sie - als Dateinamen. Eingaben aus stdin funktionieren nicht mit csvlog.
```

Optionen:

```text
-a | --average minutes : Anzahl der Minuten je Intervall für die
                         Durchschnittsdiagramme zu Abfragen und Verbindungen. Standard: 5 Minuten.
-A | --histo-average min: Anzahl der Minuten je Intervall für die
                         Abfragehistogramme. Standard: 60 Minuten.
-b | --begin datetime  : Startdatum/-zeit der im Protokoll zu analysierenden
                         Daten (Zeitstempel oder Uhrzeit).
-c | --dbclient host   : Nur Einträge des angegebenen Client-Hosts
                         auswerten.
-C | --nocomment       : Kommentare wie /* ... */ aus Abfragen entfernen.
-d | --dbname database : Nur Einträge der angegebenen Datenbank auswerten.
-D | --dns-resolv      : Client-IP-Adressen durch ihren DNS-Namen ersetzen.
                         Dies kann pgBadger erheblich verlangsamen.
-e | --end datetime    : Enddatum/-zeit der im Protokoll zu analysierenden
                         Daten (Zeitstempel oder Uhrzeit).
-E | --explode         : Den Hauptbericht in einen Bericht je Datenbank
                         aufteilen. Globale Informationen ohne Datenbankzuordnung werden dem Bericht
                         der Datenbank postgres hinzugefügt.
-f | --format logtype  : Mögliche Werte: syslog, syslog2, stderr, jsonlog,
                         csv, pgbouncer, logplex, rds und redshift. Verwenden, wenn pgBadger das
                         Protokollformat nicht erkennt.
-G | --nograph         : Diagramme in der HTML-Ausgabe deaktivieren.
                         Diagramme sind standardmäßig aktiviert.
-h | --help            : Diese Hilfe anzeigen und beenden.
-H | --html-outdir path: Verzeichnis für HTML-Berichte im inkrementellen
                         Modus. Binärdateien bleiben im mit -O, --outdir angegebenen Verzeichnis.
-i | --ident name      : Programmname als Syslog-Kennung. Standard:
                         postgres.
-I | --incremental     : Inkrementellen Modus verwenden; Tagesberichte
                         werden in separaten Verzeichnissen erzeugt. --outdir muss angegeben werden.
-j | --jobs number     : Anzahl gleichzeitig laufender Aufgaben für eine
                         einzelne Protokolldatei. Standardmäßig sowie bei csvlog wird nur eine
                         Aufgabe ausgeführt.
-J | --Jobs number     : Anzahl parallel zu analysierender Protokolldateien.
                         Standardmäßig wird jeweils eine Datei verarbeitet.
-l | --last-parsed file: Inkrementelle Analyse durch Speichern des zuletzt
                         analysierten Zeitpunkts und der letzten Zeile ermöglichen. Nützlich für
                         Fehler seit dem letzten Lauf oder Tagesberichte aus einem wöchentlich
                         rotierten Protokoll.
-L | --logfile-list file: Datei mit einer Liste der zu analysierenden
                         Protokolldateien.
-m | --maxlength size  : Maximale Abfragelänge; längere Abfragen werden
                         gekürzt. Standard: 100000.
-M | --no-multiline    : Mehrzeilige Anweisungen nicht sammeln, um störende
                         Inhalte zu vermeiden, insbesondere bei Fehlern, die sehr große Berichte
                         erzeugen.
-N | --appname name    : Nur Einträge des angegebenen Anwendungsnamens
                         auswerten.
-o | --outfile filename: Ausgabedateiname. Je nach Format standardmäßig
                         out.html, out.txt, out.bin oder out.json. Für mehrere Formate mehrfach
                         verwendbar. JSON erfordert das Perl-Modul JSON::XS. Für die Ausgabe auf
                         stdout den Dateinamen - verwenden.
-O | --outdir path     : Verzeichnis zum Speichern der Ausgabedateien.
-p | --prefix string   : Wert Ihres log_line_prefix aus postgresql.conf. Nur
                         verwenden, wenn Sie keines der dokumentierten Standardpräfixe nutzen, etwa
                         bei zusätzlichen Feldern für Client-IP oder Anwendung. MUSS Zeitfelder (%t,
                         %m oder %n) und Prozessfelder (%p oder %c) enthalten. Beispiele siehe
                         unten.
-P | --no-prettify     : Formatierung der SQL-Abfragen deaktivieren.
-q | --quiet           : Nichts auf stdout ausgeben, auch keinen
                         Fortschrittsbalken.
-Q | --query-numbering : Abfragen bei --dump-all-queries oder
                         --normalized-only nummerieren.
-r | --remote-host ip  : Host festlegen, auf dem cat für die entfernte
                         Protokolldatei ausgeführt wird, damit die Analyse lokal erfolgt.
-R | --retention N     : Anzahl aufzubewahrender Wochen im inkrementellen
                         Modus. Standard: 0, deaktiviert. Ältere Wochen- und Tagesverzeichnisse
                         werden automatisch aus dem Ausgabeverzeichnis entfernt.
-s | --sample number   : Anzahl aufzubewahrender Abfragebeispiele. Standard:
                         3.
-S | --select-only     : Nur SELECT-Abfragen auswerten.
-t | --top number      : Anzahl aufzubewahrender/anzuzeigender Abfragen.
                         Standard: 20.
-T | --title string    : Titel der HTML-Berichtsseite ändern.
-u | --dbuser username : Nur Einträge des angegebenen Benutzers auswerten.
-U | --exclude-user username : Einträge des angegebenen Benutzers aus dem
                         Bericht ausschließen. Mehrfach verwendbar.
-v | --verbose         : Ausführlichen Ausgabe- oder Debugmodus aktivieren.
                         Standardmäßig deaktiviert.
-V | --version         : pgBadger-Version anzeigen und beenden.
-w | --watch-mode      : Nur Fehler auswerten, ähnlich wie logwatch.
-W | --wide-char       : Abfragen in der HTML-Ausgabe als UTF8 kodieren, um
                         die Perl-Meldung "Wide character in print" zu vermeiden.
-x | --extension       : Ausgabeformat: text, html, bin oder json. Standard:
                         html.
-X | --extra-files     : Im inkrementellen Modus CSS und JS als separate
                         Dateien im Ausgabeverzeichnis schreiben.
-z | --zcat exec_path  : Vollständiger Pfad zum Programm zcat. Verwenden,
                         wenn zcat, bzcat oder unzip nicht im PATH liegt.
-Z | --timezone +/-XX  : Zeitzonenversatz gegenüber GMT in Stunden zum
                         Anpassen von Datum/Uhrzeit in JavaScript-Diagrammen. Ganzzahl, z. B. 2,
                         oder Gleitkommazahl, z. B. 2.5.
--anonymize            : Alle Literalwerte in Abfragen verschleiern, um
                         vertrauliche Daten zu verbergen.
--charset              : Zeichensatz der HTML-Ausgabe. Standard: utf-8.
--command CMD          : Befehl, der Protokolleinträge über stdin liefert.
                         pgBadger öffnet eine Pipe zu diesem Befehl und analysiert dessen Ausgabe.
--csv-separator        : CSV-Feldtrennzeichen festlegen. Standard: ,
--day-report YYYY-MM-DD: HTML-Bericht für den angegebenen Tag erzeugen.
                         Erfordert inkrementelle Ausgabeverzeichnisse und alle benötigten binären
                         Datendateien.
--disable-autovacuum   : Keinen Autovacuum-Bericht erzeugen.
--disable-checkpoint   : Keinen Bericht zu Checkpoints/Restartpoints
                         erzeugen.
--disable-connection   : Keinen Verbindungsbericht erzeugen.
--disable-error        : Keinen Fehlerbericht erzeugen.
--disable-hourly       : Keinen Stundenbericht erzeugen.
--disable-lock         : Keinen Sperrenbericht erzeugen.
--disable-query        : Keine Abfrageberichte erzeugen (langsamste,
                         häufigste, nach Benutzer, nach Datenbank usw.).
--disable-session      : Keinen Sitzungsbericht erzeugen.
--disable-temporary    : Keinen Bericht zu temporären Dateien erzeugen.
--disable-type         : Keinen Abfragebericht nach Typ, Datenbank oder
                         Benutzer erzeugen.
--dump-all-queries     : Alle Abfragen aus dem Protokoll ausgeben und dabei
                         Bind-Parameter an den jeweiligen Platzhalterpositionen ersetzen.
--dump-raw-csv         : Protokoll analysieren und Informationen im
                         CSV-Format ausgeben. Keine weitere Verarbeitung und kein Bericht.
--enable-checksum      : Unter jedem Abfragebericht eine md5-Prüfsumme
                         hinzufügen.
--exclude-appname name : Einträge der angegebenen Anwendung ausschließen, z.
                         B. "pg_dump". Mehrfach verwendbar.
--exclude-client name  : Einträge der angegebenen Client-IP ausschließen.
                         Mehrfach verwendbar.
--exclude-db name      : Einträge der angegebenen Datenbank ausschließen, z.
                         B. "postgres". Mehrfach verwendbar.
--exclude-file filename: Datei mit regulären Ausdrücken zum Ausschließen von
                         Abfragen. Ein Ausdruck je Zeile.
--exclude-line regex   : Alle Protokolleinträge ausschließen, die dem
                         regulären Ausdruck entsprechen. Mehrfach verwendbar.
--exclude-query regex  : Abfragen ausschließen, die dem regulären Ausdruck
                         entsprechen, z. B. "^(VACUUM|COMMIT)". Mehrfach verwendbar.
--exclude-time  regex  : Zeitstempel ausschließen, die dem regulären
                         Ausdruck entsprechen, z. B. "2013-04-12 .*". Mehrfach verwendbar.
--explain-url URL      : URL des grafischen EXPLAIN-Werkzeugs überschreiben.
                         Standard: https://explain.depesz.com/
--histogram-query VAL  : Benutzerdefinierte Klassengrenzen für das
                         Histogramm der Abfragedauer verwenden. Standardgrenzen in Millisekunden:
                         0,1,5,10,25,50,100,500,1000,10000
--histogram-session VAL: Benutzerdefinierte Klassengrenzen für das
                         Histogramm der Sitzungsdauer verwenden. Standardgrenzen in Millisekunden:
                         0,500,1000,30000,60000,600000,1800000,3600000,28800000
--include-file filename: Datei mit regulären Ausdrücken für die in den
                         Bericht aufzunehmenden Abfragen. Ein Ausdruck je Zeile.
--include-query regex  : Abfragen ausschließen, die dem regulären Ausdruck
                         nicht entsprechen. Mehrfach verwendbar, z. B. "(tbl1|tbl2)".
--include-pid PID      : Nur Ereignisse zur Sitzungs-PID (%p) auswerten.
                         Mehrfach verwendbar.
--include-session ID   : Nur Ereignisse zur Sitzungs-ID (%c) auswerten.
                         Mehrfach verwendbar.
--include-time  regex  : Nur Zeitstempel aufnehmen, die dem regulären
                         Ausdruck entsprechen, z. B. "2013-04-12 .*". Mehrfach verwendbar.
--iso-week-number      : Im inkrementellen Modus Wochen montags beginnen
                         lassen und nach ISO 8601 von 01 bis 53 nummerieren. Woche 1 ist die erste
                         mit mindestens 4 Tagen im neuen Jahr.
--keep-comments        : Kommentare in normalisierten Abfragen beibehalten,
                         um Abfragen mit derselben normalisierten Form unterscheiden zu können.
--journalctl command   : PostgreSQL-Protokolldatei durch einen Aufruf von
                         journalctl ersetzen, beispielsweise:
                         journalctl -u postgresql-9.5
--log-duration         : pgBadger zwingen, Einträge von log_duration = on
                         und log_statement = 'all' einander zuzuordnen.
--log-timezone +/-XX   : Zeitzonenversatz gegenüber GMT in Stunden zum
                         Anpassen von Datum/Uhrzeit im Protokoll vor der Analyse. Dies erschwert die
                         Suche nach Datum/Uhrzeit. Ganzzahl, z. B. 2, oder Gleitkommazahl, z. B.
                         2.5.
--month-report YYYY-MM : Kumulativen HTML-Bericht für den angegebenen Monat
                         erzeugen. Erfordert inkrementelle Ausgabeverzeichnisse und alle benötigten
                         binären Datendateien.
--noexplain            : Von auto_explain erzeugte Zeilen nicht verarbeiten.
--no-fork              : Zu Debugging-Zwecken keine Prozesse forken.
--no-process-info      : Änderung des Prozesstitels zur Kennzeichnung des
                         pgBadger-Prozesses deaktivieren; einige Systeme unterstützen dies nicht.
--no-progressbar       : Fortschrittsbalken deaktivieren.
--noreport             : Im inkrementellen Modus keine Berichte erzeugen.
--no-week              : Im inkrementellen Modus keine Wochenberichte
                         erzeugen, falls dies zu viel Zeit kostet.
--normalized-only      : Nur normalisierte Abfragen nach out.txt ausgeben.
--pgbouncer-only       : Im Kopfbereich nur PgBouncer-Menüs anzeigen.
--pid-dir path         : Verzeichnis für die PID-Datei. Standard: /tmp
--pid-file file        : Name der PID-Datei zur Steuerung gleichzeitiger
                         pgBadger-Ausführungen. Standard: pgbadger.pid
--pie-limit num        : Kreisdiagrammanteile unter num% zu einer Summe
                         zusammenfassen.
--prettify-json        : JSON-Ausgabe lesbar formatieren.
--rebuild              : Alle HTML-Berichte in inkrementellen
                         Ausgabeverzeichnissen mit binären Datendateien neu erstellen.
--start-monday         : Im inkrementellen Modus beginnen Wochen
                         standardmäßig sonntags. Mit dieser Option beginnen sie montags.
--tempdir DIR          : Verzeichnis für temporäre Dateien. Standard:
                         File::Spec->tmpdir() || '/tmp'
```

pgBadger kann eine entfernte Protokolldatei über eine passwortlose
SSH-Verbindung parsen. Verwenden Sie -r oder --remote-host, um die IP-Adresse
oder den Hostnamen des Zielsystems festzulegen. Weitere Optionen erlauben die
vollständige Steuerung der SSH-Verbindung.

```text
--ssh-identity file      Pfad zur zu verwendenden Identitätsdatei.
--ssh-option  options    Liste der -o-Optionen für die SSH-Verbindung. Stets
                         verwendete Optionen:
                         -o ConnectTimeout=$ssh_timeout
                         -o PreferredAuthentications=hostbased,publickey
--ssh-port port          SSH-Port für die Verbindung. Standard: 22.
--ssh-program ssh        Pfad zum SSH-Programm. Standard: ssh.
--ssh-timeout second     Zeitlimit bis zum Fehlschlagen der SSH-Verbindung.
                         Standard: 10 Sekunden.
--ssh-user username      Benutzername für die Verbindung. Standard: ausführender
                         Benutzer.
```

Die Option `--ssh-sudo` stellt den entfernten Befehlen zum Auflisten und Lesen der Protokolldateien `sudo` voran. Der entfernte SSH-Benutzer muss diese Befehle mit `sudo` ohne interaktive Rückfrage ausführen können.

Die zu parsende Protokolldatei lässt sich auch über eine URI angeben;
unterstützt werden http[s] und [s]ftp. pgBadger lädt die Datei mit dem
curl-Befehl herunter und parst sie bereits während des Downloads. Auch das
ssh-Protokoll wird unterstützt; dabei kommt wie beim Remote-Host der ssh-Befehl
zum Einsatz. Beispiele folgen weiter unten.

Rückgabecodes:

```text
0: Erfolg
1: Abbruch wegen eines Fehlers
2: Unterbrechung, beispielsweise durch Strg+C
3: PID-Datei existiert bereits oder kann nicht erstellt werden
4: keine Protokolldatei auf der Befehlszeile angegeben
```

Beispiele:

```text
pgbadger /var/log/postgresql.log
pgbadger /var/log/postgres.log.2.gz /var/log/postgres.log.1.gz /var/log/postgres.log
pgbadger /var/log/postgresql/postgresql-2012-05-*
pgbadger --exclude-query="^(COPY|COMMIT)" /var/log/postgresql.log
pgbadger -b "2012-06-25 10:56:11" -e "2012-06-25 10:59:11" /var/log/postgresql.log
cat /var/log/postgres.log | pgbadger -
# Logzeilenpräfix bei stderr-Ausgabe
pgbadger --prefix '%t [%p]: user=%u,db=%d,client=%h' /pglog/postgresql-2012-08-21*
pgbadger --prefix '%m %u@%d %p %r %a : ' /pglog/postgresql.log
# Logzeilenpräfix bei syslog-Ausgabe
pgbadger --prefix 'user=%u,db=%d,client=%h,appname=%a' /pglog/postgresql-2012-08-21*
# 8 CPUs zum schnelleren Analysieren einer Datei mit 10GB verwenden
pgbadger -j 8 /pglog/postgresql-10.1-main.log
```

Verwenden Sie die URI-Schreibweise für entfernte Protokolldateien:

```text
pgbadger http://172.12.110.1//var/log/postgresql/postgresql-10.1-main.log
pgbadger ftp://username@172.12.110.14/postgresql-10.1-main.log
pgbadger ssh://username@172.12.110.14:2222//var/log/postgresql/postgresql-10.1-main.log*
```

Sie können eine lokale PostgreSQL-Protokolldatei gemeinsam mit einer
entfernten PgBouncer-Protokolldatei parsen:

```text
pgbadger /var/log/postgresql/postgresql-10.1-main.log ssh://username@172.12.110.14/pgbouncer.log
```

Wöchentliche Fehlerberichte per Cron-Job:

```text
30 23 * * 1 /usr/bin/pgbadger -q -w /var/log/postgresql.log -o /var/reports/pg_errors.html
```

Einen wöchentlichen Bericht mit inkrementeller Verarbeitung erzeugen:

```text
0 4 * * 1 /usr/bin/pgbadger -q `find /var/log/ -mtime -7 -name "postgresql.log*"` -o /var/reports/pg_errors-`date +\%F`.html -l /var/reports/pgbadger_incremental_file.dat
```

Das setzt voraus, dass sowohl Ihre Protokolldatei als auch der HTML-Bericht
wöchentlich rotiert werden.

Eine bessere Alternative sind die automatisch erzeugten inkrementellen
Berichte:

```text
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Dieser Aufruf erzeugt jeweils einen Bericht pro Tag und pro Woche.

Im inkrementellen Modus können Sie außerdem festlegen, wie viele Berichtswochen
aufbewahrt werden:

```text
/usr/bin/pgbadger --retention 2 -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Wenn pg_dump jeden Tag um 23:00 und 13:00 jeweils eine halbe Stunde läuft,
können Sie diese Zeiträume wie folgt aus dem Bericht ausschließen:

```text
pgbadger --exclude-time "2013-09-.* (23|13):.*" postgresql.log
```

Dieser Ausdruck schließt jede passende Stunde vollständig aus, einschließlich der Zeit außerhalb der halbstündigen Sicherung. Schränken Sie das Minutenmuster ein, wenn nur das Sicherungsintervall ausgeschlossen werden soll.

Dies hilft zu vermeiden, dass die von pg_dump erzeugten COPY-Anweisungen am
Anfang der Liste der langsamsten Abfragen stehen. Alternativ können Sie das
Problem einfacher mit --exclude-appname "pg_dump" lösen.

Auch die Ausgabe von journalctl lässt sich wie eine Protokolldatei parsen:

```text
pgbadger --journalctl 'journalctl -u postgresql-9.5'
```

oder, weniger elegant, von einem entfernten Host aus:

```text
pgbadger -r 192.168.1.159 --journalctl 'journalctl -u postgresql-9.5'
```

Dabei müssen Sie auf der Befehlszeile keine Protokolldatei angeben. Weitere
PostgreSQL-Protokolldateien können Sie wie gewohnt hinzufügen.

Um anschließend alle inkrementellen HTML-Berichte neu aufzubauen, gehen Sie wie
folgt vor:

```text
rm /path/to/reports/*.js
rm /path/to/reports/*.css
pgbadger -X -I -O /path/to/reports/ --rebuild
```

Dieser Aufruf aktualisiert zugleich alle Ressourcendateien (JS und CSS).
Verwenden Sie -E oder --explode, wenn die Berichte mit dieser Option erstellt
wurden.

pgBadger unterstützt außerdem Heroku-PostgreSQL-Protokolle im Logplex-Format:

```text
heroku logs -p postgres | pgbadger -f logplex -o heroku.html -
```

Damit wird das Heroku-PostgreSQL-Protokoll über stdin an pgBadger
weitergeleitet.

pgBadger kann RDS- und CloudWatch-Protokolle von PostgreSQL automatisch anhand
des RDS-Formats erkennen:

```text
pgbadger -f rds -o rds_out.html rds.log
```

Ein CloudSQL-PostgreSQL-Protokoll ist im Wesentlichen ein normales
PostgreSQL-Protokoll, das in JSON gekapselt ist. pgBadger erkennt es
automatisch; falls Sie das Protokollformat dennoch erzwingen müssen, verwenden
Sie `jsonlog`.

```text
pgbadger -f jsonlog -o cloudsql_out.html cloudsql.log
```

Dasselbe gilt für die jsonlog-Erweiterung: Das JSON-Format unterscheidet sich,
doch pgBadger kann beide Formate parsen.

pgBadger unterstützt außerdem Protokolle, die der CloudNativePG-Operator für
PostgreSQL auf Kubernetes erzeugt:

```text
pgbadger -f jsonlog -o cnpg_out.html cnpg.log
```

Um einen kumulierten Monatsbericht zu erstellen, verwenden Sie folgenden
Befehl:

```text
pgbadger --month-report 2019-05 /path/to/incremental/reports/
```

Dadurch wird in der Kalenderansicht der inkrementellen Berichte beim Monatsnamen
ein Link eingefügt, über den Sie den Bericht für Mai 2019 öffnen können.
Verwenden Sie -E oder --explode, wenn die Berichte mit dieser Option erstellt
wurden.
