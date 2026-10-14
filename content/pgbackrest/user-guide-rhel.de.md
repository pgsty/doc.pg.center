---
title: "Benutzerhandbuch (RHEL)"
linkTitle: "Benutzerhandbuch (EL)"
weight: 30
description: "Schrittweise Anleitung zur Einrichtung und Verwendung von pgBackRest auf RHEL-, Rocky- und AlmaLinux-Systemen."
icon: fa-brands fa-redhat
module: [PGBACKREST]
categories: [Tutorial]
upstream_link: "https://pgbackrest.org/user-guide-rhel.html"
---

--------

## Einführung {#introduction}

Dieses Benutzerhandbuch sollte von Anfang bis Ende der Reihe nach durchgearbeitet werden, da jeder Abschnitt auf dem vorherigen aufbaut. Beispielsweise setzt der Abschnitt [Wiederherstellung](#restore-1) die Einrichtung aus dem Abschnitt [Schnellstart](#quick-start) voraus. Sobald pgBackRest eingerichtet ist und läuft, können einzelne Abschnitte gezielt aufgerufen werden. Beim ersten Durcharbeiten wird jedoch empfohlen, die Reihenfolge des Benutzerhandbuchs einzuhalten.

Die Beispiele in diesem Handbuch beziehen sich auf RHEL und PostgreSQL 14, sollten sich aber ohne großen Aufwand auf andere Unix-Distributionen und PostgreSQL-Versionen übertragen lassen. Nur die Befehle zum Erstellen, Starten, Stoppen und Löschen von PostgreSQL-Clustern sind betriebssystemspezifisch. Die pgBackRest-Befehle sind auf allen Unix-Systemen gleich, auch wenn der Speicherort der ausführbaren Datei abweichen kann. pgBackRest soll sich über PostgreSQL-Versionen hinweg einheitlich verhalten. Dennoch gibt es zwischen den PostgreSQL-Versionen kleinere Unterschiede, die in einigen Beispielen dieses Handbuchs sichtbar werden können, etwa bei PostgreSQL-Pfad- und Dateinamen sowie Einstellungen.

Informationen zur Konfiguration und die Dokumentation von PostgreSQL sind im PostgreSQL-[Handbuch](http://www.postgresql.org/docs/14/static/index.html) zu finden.

Dieses Benutzerhandbuch verwendet einen etwas ungewöhnlichen Ansatz zur Dokumentation: Beim Erstellen der Dokumentation aus der XML-Quelle wird jeder Befehl auf einer virtuellen Maschine ausgeführt. Dadurch lässt sich mit hoher Zuverlässigkeit davon ausgehen, dass die Befehle in der angegebenen Reihenfolge korrekt funktionieren. Wo sinnvoll, wird die Ausgabe erfasst und unter dem Befehl angezeigt. Fehlende Ausgaben wurden als nicht relevant eingestuft oder weggelassen, weil sie vom beschriebenen Ablauf ablenken würden.

Alle Befehle sind für die Ausführung durch einen unprivilegierten Benutzer vorgesehen, der sudo-Rechte für die Benutzer `root` und `postgres` besitzt. Sie können auch unverändert direkt unter dem jeweiligen Benutzer ausgeführt werden; in diesem Fall können die vorangestellten `sudo`-Befehle entfallen.

--------

## Konzepte {#concepts}

Die folgenden Begriffe werden in ihrer Bedeutung für pgBackRest, PostgreSQL und dieses Benutzerhandbuch definiert.

### Backup {#backup}

Ein Backup ist eine konsistente Kopie eines Datenbankclusters. Es kann wiederhergestellt werden, um den Betrieb nach einem Hardwareausfall wieder aufzunehmen, eine Point-in-Time-Recovery durchzuführen oder einen neuen Standby in Betrieb zu nehmen.

**Vollständiges Backup**: pgBackRest kopiert den gesamten Inhalt des Datenbankclusters in das Backup. Das erste Backup eines Datenbankclusters ist immer ein vollständiges Backup. pgBackRest kann ein vollständiges Backup jederzeit direkt wiederherstellen. Für seine Konsistenz ist es auf keine Dateien außerhalb dieses vollständigen Backups angewiesen.

**Differenzielles Backup**: pgBackRest kopiert nur die Dateien des Datenbankclusters, die sich seit dem letzten vollständigen Backup geändert haben. Bei der Wiederherstellung eines differenziellen Backups kopiert pgBackRest alle Dateien aus dem gewählten differenziellen Backup und die zugehörigen unveränderten Dateien aus dem vorherigen vollständigen Backup. Ein differenzielles Backup benötigt weniger Speicherplatz als ein vollständiges Backup. Für seine Wiederherstellung müssen jedoch sowohl das differenzielle als auch das vollständige Backup gültig sein.

**Inkrementelles Backup**: pgBackRest kopiert nur die Dateien des Datenbankclusters, die sich seit dem letzten Backup geändert haben. Dieses kann ein anderes inkrementelles, ein differenzielles oder ein vollständiges Backup sein. Da ein inkrementelles Backup nur die seit dem vorherigen Backup geänderten Dateien enthält, ist es in der Regel deutlich kleiner als ein vollständiges oder differenzielles Backup. Wie beim differenziellen Backup müssen für die Wiederherstellung eines inkrementellen Backups auch andere Backups gültig sein. Da es nur die seit dem letzten Backup geänderten Dateien enthält, müssen alle vorherigen inkrementellen Backups bis zum vorherigen differenziellen Backup sowie dieses differenzielle und das vorherige vollständige Backup gültig sein. Gibt es kein differenzielles Backup, müssen alle vorherigen inkrementellen Backups bis zum vorherigen vollständigen Backup sowie das vollständige Backup selbst gültig sein; ein vollständiges Backup muss vorhanden sein.

### Wiederherstellung {#restore}

Bei einer Wiederherstellung wird ein Backup auf ein System kopiert, auf dem es als aktiver Datenbankcluster gestartet wird. Für eine korrekte Wiederherstellung werden die Backup-Dateien und ein oder mehrere WAL-Segmente benötigt.

### Write-Ahead-Log (WAL) {#write-ahead-log-wal}

Mit dem WAL stellt PostgreSQL sicher, dass keine durch Commit bestätigten Änderungen verloren gehen. Transaktionen werden sequenziell in das WAL geschrieben. Eine Transaktion gilt als bestätigt, sobald diese Schreibvorgänge dauerhaft auf dem Datenträger gespeichert sind. Anschließend schreibt ein Hintergrundprozess die Änderungen in die eigentlichen Dateien des Datenbankclusters, die auch als Heap bezeichnet werden. Nach einem Absturz wird das WAL erneut angewendet, um die Datenbank in einen konsistenten Zustand zu bringen.

Das WAL ist konzeptionell unendlich, wird in der Praxis jedoch in einzelne 16MB-Dateien, sogenannte Segmente, unterteilt. WAL-Segmente folgen der Namenskonvention `0000000100000A1E000000FE`: Die ersten 8 Hexadezimalziffern stehen für die Timeline, die folgenden 16 Ziffern für die logische Sequenznummer (LSN).

### Verschlüsselung {#encryption}

Bei der Verschlüsselung werden Daten in ein Format umgewandelt, das ohne das passende Passwort, auch Passphrase genannt, nicht lesbar ist.

pgBackRest verschlüsselt das Repository basierend auf einem vom Benutzer bereitgestellten Passwort, wodurch ein unbefugter Zugriff auf die im Repository gespeicherten Daten verhindert wird.

--------

## Upgrade von pgBackRest {#upgrading-pgbackrest}


### Upgrade von pgBackRest von v2.x auf v2.y {#upgrading-pgbackrest-from-v2x-to-v2y}

Ein Upgrade von v2.x auf v2.y ist unkompliziert. Das Repository-Format hat sich nicht geändert, sodass bei den meisten Installationen lediglich die Binärdateien der neuen Version installiert werden müssen. Ein Downgrade ist ebenfalls möglich, solange keine neuen Funktionen verwendet wurden, die die ältere Version nicht unterstützt.

WICHTIG:

Die pgBackRest-Versionen auf dem lokalen und dem entfernten Host müssen exakt übereinstimmen und sollten daher gemeinsam aktualisiert werden. Bei einer Abweichung funktionieren WAL-Archivierung und Backups erst wieder, wenn die Versionen übereinstimmen. In diesem Fall wird folgender Fehler gemeldet: `[ProtocolError] expected value '2.x' for greeting key 'version' but got '2.y'`.

--------

## Kompilierung {#build}

Die Installation von pgBackRest aus einem Paket ist der Kompilierung aus dem Quellcode vorzuziehen. Weitere Informationen zu Paketen stehen unter [Installation](#installation).

Für die Kompilierung aus dem Quellcode empfiehlt sich ein eigener Build-Host, statt direkt in der Produktionsumgebung zu kompilieren. Viele der dafür benötigten Werkzeuge sollten grundsätzlich nicht in der Produktionsumgebung installiert werden. pgBackRest besteht aus einer einzigen ausführbaren Datei, die nach der Kompilierung leicht auf einen neuen Host kopiert werden kann.

build **⇒** Version `2.59.3` von pgBackRest unter `/build` herunterladen

```bash
mkdir -p /build
curl -fsSL \
       https://github.com/pgbackrest/pgbackrest/releases/download/release%2F2.59.3/pgbackrest-2.59.3.tar.gz | \
       tar zx -C /build
```

build **⇒** Build-Abhängigkeiten installieren

```bash
sudo yum install meson gcc postgresql14-devel openssl-devel libxml2-devel \
       lz4-devel libzstd-devel bzip2-devel libssh2-devel systemd-devel
```

build **⇒** pgBackRest konfigurieren und kompilieren

```bash
meson setup /build/pgbackrest /build/pgbackrest-2.59.3
ninja -C /build/pgbackrest
```

build **⇒** Optional Smoke-Tests ausführen, um die korrekte Kompilierung von pgBackRest zu prüfen

```bash
meson test -C /build/pgbackrest --suite smoke
```

```text
ninja: Entering directory `/build/pgbackrest'
ninja: no work to do.
1/1 smoke OK               10.32s

Ok:                 1
       [filtered 6 lines of output]
```

--------

## Installation {#installation}

Ein neuer Host namens pg-primary wird für den Demo-Cluster und die Ausführung der pgBackRest-Beispiele eingerichtet.

Die Installation von pgBackRest aus einem Paket ist der Kompilierung aus dem Quellcode vorzuziehen. Bei einer Paketinstallation sind die übrigen Anweisungen in diesem Abschnitt normalerweise nicht erforderlich. Es kann jedoch vorkommen, dass ein Paket eines der Verzeichnisse nicht anlegt oder falsche Berechtigungen vergibt. In diesem Fall kann es erforderlich sein, Verzeichnisse manuell anzulegen oder Berechtigungen anzupassen.

RHEL-Pakete für pgBackRest sind unter [yum.postgresql.org](http://yum.postgresql.org) verfügbar.

Falls für Ihre Distribution oder Version keine Pakete bereitstehen, können Sie pgBackRest [aus dem Quellcode kompilieren](#build) und anschließend wie hier gezeigt manuell installieren.

pg-primary **⇒** Abhängigkeiten installieren

```bash
sudo yum install postgresql-libs libssh2
```

pg-primary **⇒** pgBackRest-Binärdatei vom Build-Host kopieren

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest benötigt Protokoll- und Konfigurationsverzeichnisse sowie eine Konfigurationsdatei.

pg-primary **⇒** pgBackRest-Konfigurationsdatei und Verzeichnisse erstellen

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

pgBackRest sollte nun ordnungsgemäß installiert sein, aber es ist ratsam, dies zu überprüfen. Falls Abhängigkeiten vergessen wurden, erhalten Sie einen Fehler, wenn Sie pgBackRest über die Befehlszeile ausführen.

pg-primary **⇒** Sicherstellen, dass die Installation erfolgreich war

```bash
sudo -u postgres pgbackrest
```

```text
pgBackRest 2.59.3 - General help

Usage:
    pgbackrest [options] [command]

Commands:
    annotate        add or modify backup annotation
    archive-get     get a WAL segment from the archive
    archive-push    push a WAL segment to the archive
    backup          backup a database cluster
    check           check the configuration
    expire          expire backups that exceed retention
    help            get help
    info            retrieve information about backups
    repo-get        get a file from a repository
    repo-ls         list files in a repository
    restore         restore a database cluster
    server          pgBackRest server
    server-ping     ping pgBackRest server
    stanza-create   create the required stanza data
    stanza-delete   delete a stanza
    stanza-upgrade  upgrade a stanza
    start           allow pgBackRest processes to run
    stop            stop pgBackRest processes from running
    verify          verify contents of a repository
    version         get version

Use 'pgbackrest help [command]' for more information.
```

--------

## Schnellstart {#quick-start}

Der Schnellstart-Abschnitt behandelt die grundlegende Konfiguration von pgBackRest und PostgreSQL und führt die Befehle `backup`, `restore` und `info` ein.

### Demo-Cluster einrichten {#setup-demo-cluster}

Das Erstellen des Demo-Clusters ist optional, wird jedoch insbesondere neuen Benutzern dringend empfohlen, da die Beispielbefehle im Benutzerhandbuch auf ihn verweisen. Die Beispiele setzen voraus, dass der Demo-Cluster auf dem Standardport 5432 läuft. Der Cluster wird erst in einem späteren Abschnitt gestartet, da zuvor noch einige Einstellungen vorgenommen werden müssen.

pg-primary **⇒** Demo-Cluster erstellen

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

RHEL nimmt standardmäßig den Wochentag in den Namen der Protokolldatei auf. Da dies das Benutzerhandbuch etwas komplizierter macht, wird log_filename auf einen konstanten Wert gesetzt.

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** log_filename setzen

```ini
log_filename = 'postgresql.log'
```

### Cluster-Stanza konfigurieren {#configure-cluster-stanza}

Eine Stanza ist die Konfiguration für einen PostgreSQL-Datenbankcluster. Sie legt unter anderem seinen Speicherort, die Durchführung von Backups und die Archivierungsoptionen fest. Die meisten Datenbankserver betreiben nur einen PostgreSQL-Datenbankcluster und haben daher eine Stanza. Backup-Server haben dagegen für jeden zu sichernden Datenbankcluster eine Stanza.

Es liegt nahe, die Stanza nach dem Primärcluster zu benennen. Besser ist jedoch ein Name, der die im Cluster enthaltenen Datenbanken beschreibt. Da der Name der Stanza für den Primärserver und alle Replikate verwendet wird, sollte er die tatsächliche Funktion des Clusters beschreiben, etwa app oder dw, statt den lokalen Clusternamen wie main oder prod zu übernehmen.

Der Name „demo“ beschreibt den Zweck dieses Clusters treffend und eignet sich daher auch als Name der Stanza.

pgBackRest muss den Speicherort des Basisdatenverzeichnisses des PostgreSQL-Clusters kennen. Der Pfad kann direkt von PostgreSQL abgefragt werden, doch bei einer Recovery steht der PostgreSQL-Prozess nicht zur Verfügung. Während eines Backups wird der für pgBackRest angegebene Wert mit dem von PostgreSQL verwendeten Pfad verglichen. Beide müssen übereinstimmen, andernfalls meldet das Backup einen Fehler. Sicherstellen, dass `pg-path` exakt dem von PostgreSQL gemeldeten data_directory entspricht.

RHEL speichert Cluster standardmäßig unter `/var/lib/pgsql/[version]/data`, sodass sich der richtige Pfad zum Datenverzeichnis leicht bestimmen lässt.

Beim Erstellen der Datei `/etc/pgbackrest/pgbackrest.conf` muss dem Datenbankeigentümer, normalerweise `postgres`, Leseberechtigung erteilt werden.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Datenverzeichnis des PostgreSQL-Clusters konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data
```

Die Konfigurationsdateien von pgBackRest folgen einer Konvention ähnlich dem INI-Format von Windows. Abschnitte werden durch Text in eckigen Klammern gekennzeichnet und enthalten Schlüssel-Wert-Paare. Zeilen, die mit `#` beginnen, werden ignoriert und können als Kommentare verwendet werden. Kommentare nach einem Wert in derselben Zeile werden jedoch nicht unterstützt. Anführungszeichen werden nicht unterstützt; Leerraum am Anfang und Ende von Schlüsseln und Werten wird entfernt. Mehrfach vorkommende Abschnitte werden zusammengeführt.

Die Konfigurationsdateien von pgBackRest können auf mehrere Arten geladen werden:

- `config` und `config-include-path` haben ihre Standardwerte: Die Standardkonfigurationsdatei wird geladen, sofern sie existiert. Vorhandene `*.conf`-Dateien im standardmäßigen Konfigurations-Include-Pfad werden angehängt.
- Die Option `config` ist angegeben: Nur die angegebene Konfigurationsdatei wird geladen; sie muss existieren.
- `config-include-path` ist angegeben: Die `*.conf`-Dateien im Konfigurations-Include-Pfad werden geladen; der Pfad muss existieren. Die Standardkonfigurationsdatei wird geladen, sofern sie existiert. Sollen nur die Dateien im angegebenen Konfigurations-Include-Pfad geladen werden, kann zusätzlich die Option `--no-config` übergeben werden.
- `config` und `config-include-path` sind angegeben: Die Konfigurationsdatei wird anhand der benutzerdefinierten Werte geladen und die `*.conf`-Dateien im Konfigurations-Include-Pfad werden angehängt. Die Dateien müssen existieren.
- `config-path` ist angegeben: Diese Einstellung überschreibt den Basispfad des Standardspeicherorts der Konfigurationsdatei und/oder den Basispfad der Standardeinstellung von config-include-path, sofern die Option config und/oder config-include-path nicht ausdrücklich gesetzt ist.

Die Dateien werden so zusammengefügt, als wären sie eine einzige große Datei; jede Datei muss jedoch für sich gültig sein. Das bedeutet, dass Abschnitte in jeder Datei angegeben werden müssen, in der sie zum Speichern eines Schlüssel-Wert-Paars benötigt werden. Die Reihenfolge ist unerheblich, doch es gilt eine Rangfolge der Abschnitte. Die Priorität ist, von der höchsten zur niedrigsten:

- [*stanza*:*command*]
- [*stanza*]
- [global:*command*]
- [global]

HINWEIS:

`--config`, `--config-include-path` und `--config-path` sind ausschließlich über die Befehlszeile verfügbare Optionen.

pgBackRest kann auch über Umgebungsvariablen konfiguriert werden, wie im folgenden Beispiel gezeigt. Diese Variablen gelten für Befehle wie [backup](/de/pgbackrest/command/backup/), [restore](/de/pgbackrest/command/restore/) und [archive-push](/de/pgbackrest/command/archive-push/).

pg-primary **⇒** `log-path` über die Umgebung konfigurieren

```bash
sudo -u postgres bash -c ' \
       export PGBACKREST_LOG_PATH=/path/set/by/env && \
       pgbackrest --log-level-console=error help backup log-path'
```

```text
pgBackRest 2.59.3 - 'backup' command - 'log-path' option help

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that
if log-level-file=off then no log path is required.

current: /path/set/by/env
default: /var/log/pgbackrest
```

### Repository erstellen {#create-the-repository}

Im Repository speichert pgBackRest Backups und archiviert WAL-Segmente.

Der benötigte Speicherplatz lässt sich im Voraus möglicherweise nur schwer abschätzen. Am besten werden einige Backups erstellt und die Größe der verschiedenen Backup-Typen (full/incr/diff) sowie die täglich erzeugte WAL-Menge erfasst. Das liefert eine grobe Vorstellung vom Speicherbedarf. Dieser wird sich allerdings im Laufe der Zeit mit der Entwicklung der Datenbank wahrscheinlich ändern.

Für diese Demonstration wird das Repository auf demselben Host wie der PostgreSQL-Server gespeichert. Dies ist die einfachste Konfiguration und eignet sich für Fälle, in denen der Datenbankhost mit herkömmlicher Backup-Software gesichert wird.

pg-primary **⇒** pgBackRest-Repository erstellen

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown postgres:postgres /var/lib/pgbackrest
```

Der Repository-Pfad muss konfiguriert werden, damit pgBackRest das Repository finden kann.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Pfad zum pgBackRest-Repository konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest
```

Es können auch mehrere Repositorys konfiguriert werden. Einzelheiten stehen unter [Mehrere Repositorys](#multiple-repositories).

### Archivierung konfigurieren {#configure-archiving}

Für das Backup eines laufenden PostgreSQL-Clusters muss die WAL-Archivierung aktiviert sein. Mit `%p` gibt PostgreSQL den Speicherort des zu archivierenden WAL-Segments an. Während des Backups wird *mindestens* ein WAL-Segment erzeugt, auch wenn keine ausdrücklichen Schreibzugriffe auf den Cluster erfolgen.

pg-primary:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** Archivierungseinstellungen konfigurieren

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

Nach diesen Änderungen muss der PostgreSQL-Cluster neu gestartet werden, bevor ein Backup durchgeführt wird.

pg-primary **⇒** Demo-Cluster neu starten

```bash
sudo systemctl restart postgresql-14.service
```

Die Einstellung `hot_standby` ist standardmäßig aktiviert und sollte auf jedem Cluster aktiviert bleiben. Jeder Cluster kann später als Standby wiederhergestellt werden, beispielsweise ein Primärserver, der nach einem Failover als Standby neu aufgebaut wird. Ohne diese Einstellung akzeptiert ein Standby keine schreibgeschützten Verbindungen.

Wenn zu erwarten ist, dass ein zu archivierendes WAL-Segment mehr als 60 Sekunden, den Standardwert, benötigt, um das pgBackRest-Repository zu erreichen, sollte die pgBackRest-Option `archive-timeout` erhöht werden. Diese Option ist nicht mit der PostgreSQL-Option archive_timeout identisch. Letztere erzwingt einen WAL-Segmentwechsel und ist bei Datenbanken mit längeren Phasen ohne Aktivität nützlich. Weitere Informationen zur PostgreSQL-Option archive_timeout stehen unter [Write-Ahead-Log](https://www.postgresql.org/docs/current/static/runtime-config-wal.html) in der PostgreSQL-Dokumentation.

Für den Befehl `archive-push` können eigene Optionen konfiguriert werden. Beispielsweise lässt sich eine niedrigere Komprimierungsstufe festlegen, um die Archivierung zu beschleunigen, ohne die Komprimierung für Backups zu beeinflussen.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `archive-push` für eine niedrigere Komprimierungsstufe konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest



[global:archive-push]

compress-level=3
```

Diese Art der Konfiguration kann für jeden Befehl verwendet werden und sich auch auf eine bestimmte Stanza beziehen, beispielsweise `demo:archive-push`.

### Aufbewahrung konfigurieren {#configure-retention}

pgBackRest entfernt Backups anhand der Aufbewahrungsoptionen.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Aufbewahrung auf 2 vollständige Backups festlegen

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

Weitere Informationen zur Aufbewahrung stehen im Abschnitt [Aufbewahrung](#retention).

### Repository-Verschlüsselung konfigurieren {#configure-repository-encryption}

Zur Demonstration der Verschlüsselung werden für das Repository ein Verschlüsselungstyp und ein Schlüssel konfiguriert. Die Verschlüsselung erfolgt immer auf der Clientseite, auch wenn der Repository-Typ, beispielsweise S3 oder ein anderer Objektspeicher, Verschlüsselung unterstützt.

Für den Schlüssel ist eine lange, zufällige Passphrase wichtig. Sie lässt sich beispielsweise mit folgendem Befehl erzeugen: `openssl rand -base64 48`.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Verschlüsselung des pgBackRest-Repositorys konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2



[global:archive-push]

compress-level=3
```

HINWEIS:

Die Verschlüsselungseinstellungen werden oben im Abschnitt `[global]` abgelegt, damit der Befehl `info` alle Stanzas lesen kann. Ohne die Option `stanza` liest `info` Verschlüsselungseinstellungen ausschließlich aus dem Abschnitt `[global]`. Werden die Verschlüsselungseinstellungen pro Stanza konfiguriert, ist daher die Option `stanza` erforderlich, um eine verschlüsselte Stanza zu lesen.

Nachdem das Repository konfiguriert und die Stanza erstellt und geprüft wurde, können die Verschlüsselungseinstellungen des Repositorys nicht mehr geändert werden.

### Stanza erstellen {#create-the-stanza}

Zum Initialisieren der Stanza muss der Befehl `stanza-create` ausgeführt werden. Es wird empfohlen, nach `stanza-create` den Befehl `check` auszuführen, um sicherzustellen, dass Archivierung und Backups korrekt konfiguriert sind.

pg-primary **⇒** Stanza erstellen und Konfiguration prüfen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=1200-90682d35 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create command end: completed successfully
```

### Konfiguration prüfen {#check-the-configuration}

Der Befehl `check` prüft, ob pgBackRest und die Einstellung archive_command für Archivierung und Backups der angegebenen Stanza korrekt konfiguriert sind. Er versucht, alle Repositorys und Datenbanken zu prüfen, die für den Host konfiguriert sind, auf dem er ausgeführt wird. Er erkennt Fehlkonfigurationen, insbesondere bei der Archivierung, die zu unvollständigen Backups führen, weil erforderliche WAL-Segmente das Archiv nicht erreicht haben. Der Befehl kann auf dem PostgreSQL- oder dem Repository-Host ausgeführt werden. Er kann auch auf dem Standby-Host ausgeführt werden. Da `pg_switch_xlog()`/`pg_switch_wal()` auf dem Standby jedoch nicht ausgeführt werden können, prüft er dort nur die Repository-Konfiguration.

Dabei werden `pg_create_restore_point('pgBackRest Archive Check')` und `pg_switch_xlog()`/`pg_switch_wal()` aufgerufen, um PostgreSQL zur Archivierung eines WAL-Segments zu veranlassen.

pg-primary **⇒** Konfiguration prüfen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1233-340209f5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000100000000/000000010000000000000001-dac4045f133f7305d6342d81e428e60050928bc4.gz' on repo1
P00   INFO: check command end: completed successfully
```

### Leistungsoptimierung {#performance-tuning}

pgBackRest bietet mehrere Leistungsoptionen, die standardmäßig deaktiviert sind, um die Abwärtskompatibilität des Repositorys zu wahren. Beim Erstellen eines neuen Repositorys werden die folgenden Optionen jedoch empfohlen. Sie können auch mit einem vorhandenen Repository verwendet werden, allerdings können ältere pgBackRest-Versionen das Repository dann nicht mehr lesen. Diese Inkompatibilität hängt davon ab, wann die jeweilige Funktion eingeführt wurde, wie in der folgenden Liste angegeben.

- `compress-type` - legt den Komprimierungsalgorithmus für die Befehle `backup` und `archive-push` fest. Der Standardwert ist `gz` (Gzip), empfohlen wird jedoch `zst` (Zstandard), da es deutlich schneller ist und eine ähnliche Komprimierung wie `gz` bietet. Die Option `compress-type` unterstützt `zst` seit [v2.27](/de/pgbackrest/release/#v227-release-notes). Weitere Einzelheiten stehen unter [Komprimierungstyp](/de/pgbackrest/configuration/#compress-type-option---compress-type).
- `repo-bundle` - fasst beim Backup kleine Dateien zusammen, um Speicherplatz zu sparen und die Befehle `backup` und `restore` zu beschleunigen, insbesondere bei Objektspeichern wie S3. Die Option `repo-bundle` wurde in [v2.39](/de/pgbackrest/release/#v239-release-notes) eingeführt. Weitere Einzelheiten stehen unter [Dateibündelung](#file-bundling).
- `repo-block` - speichert bei einem `diff`/`incr`-`backup` nur die geänderten Teile einer Datei statt der gesamten Datei. Das spart Speicherplatz und beschleunigt das `backup`. Die Option `repo-block` wurde in [v2.46](/de/pgbackrest/release/#v246-release-notes) eingeführt, empfohlen wird jedoch mindestens [v2.52.1](/de/pgbackrest/release/#v2521-release-notes). Weitere Einzelheiten stehen unter [Inkrementelle Backups auf Blockebene](#block-incremental).

Weitere Leistungsoptionen sind standardmäßig deaktiviert, weil sie zusätzliche Konfiguration erfordern oder weil der Standardwert sicher, aber nicht optimal ist. Diese Optionen stehen in allen v2-Versionen von pgBackRest zur Verfügung.

- `process-max` - legt fest, wie viele Prozesse für Befehle verwendet werden. Der Standardwert ist 1 und fast nie angemessen. Jeder Befehl verwendet `process-max` anders; Einzelheiten zur Verwendung stehen daher in der jeweiligen Befehlsdokumentation.
- `archive-async` - archiviert WAL-Dateien stapelweise im Repository und erhöht dadurch die Archivierungsgeschwindigkeit erheblich. Die Option ist standardmäßig deaktiviert, da ein Spool-Pfad angelegt werden muss. Weitere Einzelheiten stehen unter [Asynchrone Archivierung](#asynchronous-archiving).
- `backup-standby` - führt das Backup auf einem Standby statt auf dem Primärserver durch, um dessen Last zu verringern. Die Option ist standardmäßig deaktiviert, da sie zusätzliche Konfiguration und mindestens einen Standby-Host erfordert. Weitere Einzelheiten stehen unter [Backup von einem Standby](#backup-from-a-standby).

### Backup durchführen {#perform-a-backup}

Standardmäßig wartet pgBackRest vor dem Beginn eines Backups auf den nächsten regulär geplanten Checkpoint. Je nach den PostgreSQL-Einstellungen checkpoint_timeout und checkpoint_segments kann es recht lange dauern, bis ein Checkpoint abgeschlossen ist und das Backup beginnen kann. Im Allgemeinen empfiehlt sich `start-fast=y`, damit das Backup sofort beginnt. Dadurch wird ein Checkpoint erzwungen. Da Backups normalerweise einmal täglich durchgeführt werden, sollte ein zusätzlicher Checkpoint die Leistung jedoch nicht spürbar beeinflussen. Bei sehr stark ausgelasteten Clustern kann es dagegen besser sein, `--start-fast` bei Bedarf über die Befehlszeile zu übergeben.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Schnellen Backup-Start konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Für ein Backup des PostgreSQL-Clusters pgBackRest mit dem Befehl `backup` ausführen.

pg-primary **⇒** Backup des Demo-Clusters erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 000000010000000000000002, lsn = 0/2000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000002:000000010000000000000003
P00   INFO: new backup label = 20261002-185647F
P00   INFO: full backup size = 25.2MB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1327-e87cfc24 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

Standardmäßig versucht pgBackRest, ein inkrementelles Backup durchzuführen. Ein inkrementelles Backup muss jedoch auf einem vollständigen Backup basieren. Da noch keines vorhanden war, hat pgBackRest stattdessen ein vollständiges Backup erstellt.

Mit der Option `type` lässt sich ein vollständiges oder differenzielles Backup angeben.

pg-primary **⇒** Differenzielles Backup des Demo-Clusters erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 7 lines of output]
P00   INFO: check archive for segment(s) 000000010000000000000004:000000010000000000000005
P00   INFO: new backup label = 20261002-185647F_20261002-185651D
P00   INFO: diff backup size = 9.2KB, file total = 951
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=1398-36e29fed --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-full=2 --stanza=demo
```

Diesmal gab es keine Warnung, da bereits ein vollständiges Backup vorhanden war. Inkrementelle Backups können auf einem vollständigen *oder* differenziellen Backup basieren; differenzielle Backups müssen hingegen auf einem vollständigen Backup basieren. Ein vollständiges Backup lässt sich mit dem Befehl `backup` und der Option `--type=full` durchführen.

Bei einem Online-Backup wartet pgBackRest, bis die für die Konsistenz des Backups erforderlichen WAL-Segmente archiviert wurden. Diese Wartezeit wird durch die pgBackRest-Option `archive-timeout` bestimmt, deren Standardwert 60 Sekunden beträgt. Wenn die Archivierung eines einzelnen Segments bekanntermaßen länger dauert, sollte dieser Wert erhöht werden.

### Backups planen {#schedule-a-backup}

Backups können mit Werkzeugen wie cron geplant werden.

Im folgenden Beispiel werden zwei cron-Jobs eingerichtet: Vollständige Backups laufen sonntags um 6:30 Uhr morgens, differenzielle Backups montags bis samstags ebenfalls um 6:30 Uhr morgens. Wird diese crontab erstmals mitten in der Woche installiert, führt pgBackRest beim ersten Aufruf des differenziellen Jobs ein vollständiges Backup aus. Am folgenden Tag wird dann ein differenzielles Backup erstellt.

```bash
#m h   dom mon dow   command
30 06  *   *   0     pgbackrest --type=full --stanza=demo backup
30 06  *   *   1-6   pgbackrest --type=diff --stanza=demo backup
```

Nach dem Einrichten des Backup-Zeitplans ist es wichtig, auch die Aufbewahrung passend zu konfigurieren, damit Backups regelmäßig entfernt werden; siehe [Aufbewahrung](#retention).

### Backup-Informationen {#backup-information}

Mit dem Befehl `info` lassen sich Informationen über Backups abrufen.

pg-primary **⇒** Informationen zum Demo-Cluster abrufen

```bash
sudo -u postgres pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000010000000000000001/000000010000000000000005

        full backup: 20261002-185647F
            timestamp start/stop: 2026-10-02 18:56:47+00 / 2026-10-02 18:56:50+00
            wal start/stop: 000000010000000000000002 / 000000010000000000000003
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup set size: 3.2MB, backup size: 3.2MB

        diff backup: 20261002-185647F_20261002-185651D
            timestamp start/stop: 2026-10-02 18:56:51+00 / 2026-10-02 18:56:52+00
            wal start/stop: 000000010000000000000004 / 000000010000000000000005
            database size: 25.2MB, database backup size: 9.2KB
            repo1: backup set size: 3.2MB, backup size: 864B
            backup reference total: 1 full
```

Der Befehl `info` arbeitet mit einer einzelnen Stanza oder allen Stanzas. Die standardmäßige Textausgabe bietet eine für Menschen lesbare Übersicht der Backups für die angeforderten Stanzas. Dieses Format kann sich mit jeder Version ändern.

Für maschinenlesbare Ausgabe `--output=json` verwenden. Die JSON-Ausgabe enthält wesentlich mehr Informationen als die Textausgabe und bleibt stabil, sofern kein Fehler gefunden wird.

Um die Ausführung zu beschleunigen, kann die Ausgabe mit `--detail-level=progress` auf Fortschrittsinformationen beschränkt werden. Dabei werden alle Prüfungen außer der Verfügbarkeit der Stanza übersprungen.

Jede Stanza hat einen eigenen Abschnitt. Mit der Option `--stanza` lässt sich die Ausgabe auf eine einzelne Stanza beschränken. Der '`status`' gibt einen kurzen Überblick über den Zustand der Stanza. Bei '`ok`' funktioniert pgBackRest normal. Bei mehreren Repositorys bedeutet der Status '`mixed`', dass die Stanza in mindestens einem Repository nicht fehlerfrei ist; in diesem Fall wird ihr Zustand für jedes Repository einzeln angegeben. Tritt in einem Repository ein Fehler auf, der keinem bekannten Fehlercode entspricht, wird der Fehlercode '`other`' verwendet und der Fehler vollständig beschrieben. '`wal archive min/max`' zeigt das kleinste und das größte derzeit im Archiv gespeicherte WAL-Segment. Bei mehreren Repositorys bezieht sich diese Angabe auf alle Repositorys, sofern die Option `--repo` nicht gesetzt ist. Durch Regeln zur Archivaufbewahrung oder aus anderen Gründen können Lücken vorhanden sein.

Wenn einer dieser Befehle gerade auf dem Host läuft, erscheinen die Meldungen '`backup/expire running`' und/oder '`restore running`' neben der '`status`'-Angabe. Die Textausgabe enthält außerdem den Fortschritt pro Repository; in der JSON-Ausgabe wird ein '`repo`'-Array eingefügt.

Die Backups werden vom ältesten zum neuesten angezeigt. Das älteste Backup ist *immer* ein vollständiges Backup, gekennzeichnet durch ein `F` am Ende der Bezeichnung. Das neueste Backup kann vollständig, differenziell mit der Endung `D` oder inkrementell mit der Endung `I` sein.

'`timestamp start/stop`' gibt den Zeitraum an, in dem das Backup ausgeführt wurde. Mit '`timestamp stop`' lässt sich bestimmen, welches Backup für eine Point-in-Time-Recovery verwendet werden soll. Weitere Informationen zur Point-in-Time-Recovery stehen im Abschnitt [Point-in-Time-Recovery](#point-in-time-recovery).

'`wal start/stop`' gibt den WAL-Bereich an, der benötigt wird, um die Datenbank bei der Wiederherstellung konsistent zu machen. Der Befehl `backup` stellt vor seinem Abschluss sicher, dass dieser WAL-Bereich im Archiv vorhanden ist.

'`database size`' ist die gesamte unkomprimierte Größe der Datenbank. '`database backup size`' bezeichnet dagegen die tatsächlich zu sichernde Datenmenge in der Datenbank. Bei vollständigen Backups stimmen beide Werte überein.

'`repo`' gibt an, in welchem Repository sich das Backup befindet. '`backup set size`' umfasst alle Dateien dieses Backups sowie aller referenzierten Backups im Repository, die benötigt werden, um die Datenbank aus diesem Backup wiederherzustellen. '`backup size`' umfasst dagegen nur die Dateien dieses Backups. Bei vollständigen Backups stimmen auch diese Werte überein. Wenn in pgBackRest die Komprimierung aktiviert ist, geben die Repository-Größen die komprimierten Dateigrößen an.

'`backup reference total`' fasst die Liste der weiteren Backups zusammen, die zur Wiederherstellung dieses Backups benötigt werden. Mit der Option `--set` lässt sich die vollständige Referenzliste anzeigen.

### Backup wiederherstellen {#restore-a-backup}

Backups können vor verschiedenen Ausfallszenarien schützen, insbesondere Hardwareausfällen und Datenbeschädigungen. Am einfachsten lässt sich eine Datenbeschädigung simulieren, indem eine wichtige Datei des PostgreSQL-Clusters entfernt wird.

pg-primary **⇒** Demo-Cluster stoppen und die Datei `pg_control` löschen

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres rm /var/lib/pgsql/14/data/global/pg_control
```

Beim Starten des Clusters ohne diese wichtige Datei tritt ein Fehler auf.

pg-primary **⇒** Start des beschädigten Demo-Clusters versuchen

```bash
sudo systemctl start postgresql-14.service
sudo systemctl status postgresql-14.service
```

```text
postgresql-14.service - PostgreSQL 14 database server
    Loaded: loaded (/usr/lib/systemd/system/postgresql-14.service, disabled)
    Active: failed (failed)
```

Zur Wiederherstellung eines Backups des PostgreSQL-Clusters pgBackRest mit dem Befehl `restore` ausführen. Der Cluster muss gestoppt sein, was hier bereits der Fall ist, und alle Dateien müssen aus dem PostgreSQL-Datenverzeichnis entfernt werden.

pg-primary **⇒** Alte Dateien aus dem Demo-Cluster entfernen

```bash
sudo -u postgres find /var/lib/pgsql/14/data -mindepth 1 -delete
```

pg-primary **⇒** Demo-Cluster wiederherstellen und PostgreSQL starten

```bash
sudo -u postgres pgbackrest --stanza=demo restore
sudo systemctl start postgresql-14.service
```

Diesmal wurde der Cluster erfolgreich gestartet, da die Wiederherstellung die fehlende Datei `pg_control` ersetzt hat.

Weitere Informationen zum Befehl `restore` stehen im Abschnitt [Wiederherstellung](#restore-1).

--------

## Überwachung {#monitoring}

Die Überwachung ist ein wichtiger Bestandteil jedes Produktionssystems. Es stehen zahlreiche Werkzeuge zur Verfügung, und mit etwas Aufwand lässt sich pgBackRest mit jedem davon überwachen.

pgBackRest kann Informationen über das Repository im JSON-Format ausgeben. Dazu gehören eine Liste aller Backups jeder Stanza und Informationen zum WAL-Archiv.

### In PostgreSQL {#in-postgresql}

Mit dem PostgreSQL-Befehl `COPY` lassen sich pgBackRest-Informationen in eine Tabelle laden. Das folgende Beispiel kapselt diese Logik in einer Funktion, mit der Abfragen in Echtzeit durchgeführt werden können.

pg-primary **⇒** pgBackRest-Informationsfunktion für PostgreSQL laden

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

```text
-- An example of monitoring pgBackRest from within PostgreSQL
--
-- Use copy to export data from the pgBackRest info command into the jsonb
-- type so it can be queried directly by PostgreSQL.

-- Create monitor schema
create schema monitor;

-- Get pgBackRest info in JSON format
create function monitor.pgbackrest_info()
    returns jsonb AS $$
declare
    data jsonb;
begin
    -- Create a temp table to hold the JSON data
    create temp table temp_pgbackrest_data (data text);

    -- Copy data into the table directly from the pgBackRest info command
    copy temp_pgbackrest_data (data)
        from program
            'pgbackrest --output=json info' (format text);

    select replace(temp_pgbackrest_data.data, E'\n', '\n')::jsonb
      into data
      from temp_pgbackrest_data;

    drop table temp_pgbackrest_data;

    return data;
end $$ language plpgsql;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-info.sql
```

Mit der Funktion `monitor.pgbackrest_info()` lassen sich nun der Zeitpunkt des letzten erfolgreichen Backups und das archivierte WAL einer Stanza ermitteln.

pg-primary **⇒** Zeitpunkt des letzten erfolgreichen Backups und archiviertes WAL abfragen

```bash
sudo -u postgres cat \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
-- Get last successful backup for each stanza
--
-- Requires the monitor.pgbackrest_info function.
with stanza as
(
    select data->'name' as name,
           data->'backup'->(
               jsonb_array_length(data->'backup') - 1) as last_backup,
           data->'archive'->(
               jsonb_array_length(data->'archive') - 1) as current_archive
      from jsonb_array_elements(monitor.pgbackrest_info()) as data
)
select name,
       to_timestamp(
           (last_backup->'timestamp'->>'stop')::numeric) as last_successful_backup,
       current_archive->>'max' as last_archived_wal
  from stanza;
```

```bash
sudo -u postgres psql -f \
       /var/lib/pgsql/pgbackrest/doc/example/pgsql-pgbackrest-query.sql
```

```text
  name  | last_successful_backup |    last_archived_wal
--------+------------------------+--------------------------
 "demo" | 2026-10-02 18:56:52+00 | 000000010000000000000005
(1 row)
```

--------

## Backup {#backup-1}

Wenn mehrere Repositorys konfiguriert sind, erstellt pgBackRest das Backup im Repository mit der höchsten Priorität, beispielsweise `repo1`, sofern die Option `--repo` nicht angegeben ist.

pgBackRest hat keine integrierte Zeitplanung. Daher empfiehlt es sich, pgBackRest über cron oder einen anderen Mechanismus zur Zeitplanung auszuführen.

Weitere Einzelheiten und Beispiele stehen unter [Backup durchführen](#perform-a-backup).

### Dateibündelung {#file-bundling}

Das Bündeln von Dateien im Repository spart Zeit beim Backup und etwas Speicherplatz im Repository. Besonders deutlich ist dies bei Repositorys auf Objektspeichern wie S3 oder auf Dateisystemen mit großen Blockgrößen. Auf Objektspeichern dauert das Erstellen einer einzelnen Datei länger, und die Speicherung sehr kleiner Dateien kann genauso viel kosten wie die größerer Dateien.

Die Dateibündelung wird mit der Option `repo-bundle` aktiviert.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-bundle` konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Ein vollständiges Backup ohne Dateibündelung enthält 1000+ Dateien im Backup-Pfad. Mit Bündelung wird die Gesamtzahl der Dateien erheblich reduziert. Außerdem werden leere Dateien nur im Manifest erfasst und ansonsten nicht gespeichert, während bei einem normalen Backup jede leere Datei einzeln gespeichert wird.

pg-primary **⇒** Vollständiges Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full backup
```

pg-primary **⇒** Gesamtzahl der Dateien prüfen

```bash
sudo -u postgres find /var/lib/pgbackrest/backup/demo/latest/ -type f | wc -l
```

```text
5
```

Zur Optimierung können die Optionen `repo-bundle-size` und `repo-bundle-limit` verwendet werden. Die Standardwerte sollten jedoch in den meisten Fällen optimal sein.

Dateibündelung ist im Allgemeinen effizienter, erschwert jedoch das manuelle Abrufen von Dateien aus dem Repository. Für deduplizierten Speicher ist sie möglicherweise nicht ideal, da jedes vollständige Backup die Dateien in den Bündeln anders anordnet. Bei Dateibündeln ist außerdem keine Fortsetzung nach einer Unterbrechung möglich. Daher sollte `repo-bundle-limit` nicht zu hoch eingestellt werden.

### Inkrementelle Backups auf Blockebene {#block-incremental}

Inkrementelle Backups auf Blockebene sparen Speicherplatz, indem sie nur die seit dem vorherigen Backup geänderten Teile einer Datei statt der gesamten Datei speichern.

Die Funktion für inkrementelle Backups auf Blockebene wird mit der Option `repo-block` aktiviert und funktioniert am besten, wenn sie für alle Backup-Typen aktiviert ist. Auch die Dateibündelung muss aktiviert sein.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-block` konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

### Backup-Annotationen {#backup-annotations}

Benutzer können einem Backup informative Schlüssel-Wert-Paare hinzufügen. Diese Option kann mehrfach verwendet werden, um mehrere Annotationen anzufügen.

pg-primary **⇒** Vollständiges Backup mit Annotationen durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --annotation=source="demo backup" \
       --annotation=key=value --type=full backup
```

Annotationen erscheinen in der Textausgabe des Befehls `info`, wenn mit `--set` ein Backup angegeben wird. In der JSON-Ausgabe erscheinen sie immer.

pg-primary **⇒** Informationen zum Demo-Cluster abrufen

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                key: value
                source: demo backup
```

Annotationen, die mit dem Befehl `backup` hinzugefügt wurden, können anschließend mit dem Befehl `annotate` ergänzt, geändert oder entfernt werden.

pg-primary **⇒** Backup-Annotationen ändern

```bash
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F \
       --annotation=key= --annotation=new_key=new_value annotate
sudo -u postgres pgbackrest --stanza=demo --set=20261002-185708F info
```

```text
stanza: demo
    status: ok
    cipher: aes-256-cbc

    db (current)
        wal archive min/max (14): 000000020000000000000007/000000020000000000000009

        full backup: 20261002-185708F
            timestamp start/stop: 2026-10-02 18:57:08+00 / 2026-10-02 18:57:09+00
            wal start/stop: 000000020000000000000008 / 000000020000000000000009
            lsn start/stop: 0/8000028 / 0/9000050
            database size: 25.2MB, database backup size: 25.2MB
            repo1: backup size: 3.2MB
            database list: postgres (13755)
            annotation(s)
                new_key: new_value
                source: demo backup
```

--------

## Aufbewahrung {#retention}

Im Allgemeinen empfiehlt es sich, möglichst viele Backups aufzubewahren, um ein größeres Zeitfenster für die [Point-in-Time-Recovery](#point-in-time-recovery) zu erhalten. Dabei müssen jedoch auch praktische Einschränkungen wie der verfügbare Speicherplatz berücksichtigt werden. Aufbewahrungsoptionen entfernen ältere Backups, sobald sie nicht mehr benötigt werden.

pgBackRest rotiert vollständige Backups anhand des Aufbewahrungstyps, der eine Anzahl oder einen Zeitraum festlegen kann. Bei einer Anzahl hängt das Entfernen nicht vom Erstellungszeitpunkt der Backups ab, sondern davon, wie viele aufbewahrt werden müssen. Differenzielle Backups werden nach Anzahl aufbewahrt, jedoch immer entfernt, wenn das vollständige Backup entfernt wird, von dem sie abhängen. Inkrementelle Backups werden durch die Aufbewahrungsregeln nie eigenständig entfernt, sondern immer zusammen mit dem zugehörigen vollständigen oder differenziellen Backup. Einzelheiten und Beispiele stehen unter [Aufbewahrung vollständiger Backups](#full-backup-retention) und [Aufbewahrung differenzieller Backups](#differential-backup-retention).

Archiviertes WAL wird standardmäßig für alle noch nicht entfernten Backups aufbewahrt. Diese Regel kann pro Repository mit den Optionen retention-archive geändert werden, was jedoch nicht empfohlen wird. Einzelheiten und Beispiele stehen unter [Archivaufbewahrung](#archive-retention).

Der Befehl `expire` wird nach jedem erfolgreichen Backup automatisch ausgeführt und kann auch vom Benutzer aufgerufen werden. Bei einem manuellen Aufruf erfolgt das Entfernen gemäß den Aufbewahrungseinstellungen jedes konfigurierten Repositorys. Wenn die Option `--repo` angegeben ist, wird nur das angegebene Repository bereinigt. Der Benutzer kann das Entfernen mit der Option `--set` auch auf einen bestimmten Backup-Satz beschränken. Sofern `--repo` nicht angegeben ist, werden alle Repositorys durchsucht und alle dem angegebenen Satz entsprechenden Backups entfernt. Die Regeln zur Archivaufbewahrung werden bei jedem Aufruf von `expire` geprüft und angewendet.

### Aufbewahrung vollständiger Backups {#full-backup-retention}

`repo1-retention-full-type` bestimmt, ob die Option `repo1-retention-full` als Anzahl aufzubewahrender vollständiger Backups oder als Anzahl von Tagen ihrer Aufbewahrung interpretiert wird. Neue Backups müssen abgeschlossen sein, bevor Backups entfernt werden. Bei `repo1-retention-full-type=count` und `repo1-retention-full=2` sind daher drei vollständige Backups gespeichert, bevor das älteste entfernt wird. Bei `repo1-retention-full-type=time` und `repo1-retention-full=20` muss ein vollständiges Backup vorhanden sein, das mindestens 20 Tage alt ist, bevor Backups entfernt werden können.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-retention-full` konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Für Backups gilt `repo1-retention-full=2`. Derzeit gibt es jedoch nur ein vollständiges Backup, sodass beim nächsten vollständigen Backup noch keines entfernt wird.

pg-primary **⇒** Vollständiges Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=detail backup
```

```text
       [filtered 963 lines of output]
P00   INFO: repo1: remove expired backup 20261002-185706F
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185708F, start = 000000020000000000000008
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000007, stop = 000000020000000000000007
P00   INFO: expire command end: completed successfully
```

Archivdaten werden hingegen *entfernt*, da WAL-Segmente vor dem ältesten Backup erzeugt wurden. Diese sind für eine Recovery nicht nutzbar. Nur WAL-Segmente, die nach einem Backup erzeugt wurden, können für dessen Recovery verwendet werden.

pg-primary **⇒** Vollständiges Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=full \
       --log-level-console=info backup
```

```text
       [filtered 11 lines of output]
P00   INFO: repo1: expire full backup 20261002-185708F
P00   INFO: repo1: remove expired backup 20261002-185708F
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000008, stop = 000000020000000000000009
P00   INFO: expire command end: completed successfully
```

Das vollständige Backup `20261002-185647F` wird entfernt. Die Archivaufbewahrung richtet sich nun nach `20261002-185711F`, dem jetzt ältesten vollständigen Backup.

### Aufbewahrung differenzieller Backups {#differential-backup-retention}

`repo1-retention-diff` auf die benötigte Anzahl differenzieller Backups setzen. Differenzielle Backups hängen nur vom vorherigen vollständigen Backup ab. Daher lässt sich ein fortlaufend erneuerter Satz differenzieller Backups für den letzten Tag oder länger erstellen. Dies ermöglicht schnelle Wiederherstellungen auf kürzlich vergangene Zeitpunkte und verringert gleichzeitig den gesamten Speicherbedarf.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-retention-diff` konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=1

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

Für Backups gilt `repo1-retention-diff=1`, sodass zwei differenzielle Backups durchgeführt werden müssen, bevor eines entfernt wird. Zusätzlich wird ein inkrementelles Backup erstellt, um dessen Entfernung zu demonstrieren. Diese hängt hier von der Entfernung des differenziellen Backups ab.

pg-primary **⇒** Differenzielle und inkrementelle Backups durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff backup
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Ein weiteres differenzielles Backup entfernt nun das vorherige differenzielle und das inkrementelle Backup, sodass nur ein differenzielles Backup übrig bleibt.

pg-primary **⇒** Differenzielles Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 10 lines of output]
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=2641-6abf9293 --log-level-console=info --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-diff=1 --repo1-retention-full=2 --stanza=demo
P00   INFO: repo1: expire diff backup set 20261002-185713F_20261002-185715D, 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185716I
P00   INFO: repo1: remove expired backup 20261002-185713F_20261002-185715D
P00   INFO: expire command end: completed successfully
```

### Archivaufbewahrung {#archive-retention}

pgBackRest entfernt archivierte WAL-Segmente automatisch beim Entfernen von Backups. Standardmäßig wird WAL für vollständige Backups anhand der Option `repo1-retention-full` entfernt. Um Speicherplatz zu sparen, kann es dennoch sinnvoll sein, Archivdaten früher zu entfernen. Für die differenzielle Archivaufbewahrung werden vollständige Backups wie differenzielle Backups behandelt.

Beim Entfernen von Archivdaten werden niemals WAL-Segmente entfernt, die für die Konsistenz eines Backups erforderlich sind. Point-in-Time-Recovery (PITR) funktioniert jedoch nur mit einem lückenlosen WAL-Strom. Daher ist Vorsicht geboten, wenn Archivdaten außerhalb der normalen Backup-Bereinigung besonders früh entfernt werden. Um zu ermitteln, was entfernt würde, ohne tatsächlich etwas zu entfernen, kann dem Befehl `expire` auf der Befehlszeile die Option `dry-run` übergeben werden.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-retention-diff` konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

start-fast=y



[global:archive-push]

compress-level=3
```

pg-primary **⇒** Differenzielles Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=diff \
       --log-level-console=info backup
```

```text
       [filtered 6 lines of output]
P00   INFO: backup stop archive = 000000020000000000000017, lsn = 0/17000050
P00   INFO: check archive for segment(s) 000000020000000000000016:000000020000000000000017
P00   INFO: new backup label = 20261002-185713F_20261002-185719D
P00   INFO: diff backup size = 11.5KB, file total = 951
P00   INFO: backup command end: completed successfully
       [filtered 2 lines of output]
```

pg-primary **⇒** Archiv bereinigen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=detail \
       --repo1-retention-archive-type=diff --repo1-retention-archive=1 expire
```

```text
P00   INFO: expire command begin 2.59.3: --exec-id=2877-3548ad61 --log-level-console=detail --no-log-timestamp --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo1-retention-archive=1 --repo1-retention-archive-type=diff --repo1-retention-diff=2 --repo1-retention-full=2 --stanza=demo
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185711F, start = 00000002000000000000000A, stop = 00000002000000000000000B
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F, start = 00000002000000000000000C, stop = 00000002000000000000000D
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185717D, start = 000000020000000000000012, stop = 000000020000000000000013
P00 DETAIL: repo1: 14-1 archive retention on backup 20261002-185713F_20261002-185719D, start = 000000020000000000000016
P00   INFO: repo1: 14-1 remove archive, start = 00000002000000000000000E, stop = 000000020000000000000011
P00   INFO: repo1: 14-1 remove archive, start = 000000020000000000000014, stop = 000000020000000000000015
P00   INFO: expire command end: completed successfully
```

Zum differenziellen Backup `20261002-185713F_20261002-185717D` gehören archivierte WAL-Segmente, die aufbewahrt werden müssen, um die älteren Backups konsistent zu machen, auch wenn diese mit PITR nicht weiter vorwärts abgespielt werden können. WAL-Segmente, die nach `20261002-185713F_20261002-185717D`, aber vor `20261002-185713F_20261002-185719D` erzeugt wurden, werden entfernt. WAL-Segmente nach dem neuen Backup `20261002-185713F_20261002-185719D` bleiben erhalten und können für PITR verwendet werden.

Da vollständige Backups für die differenzielle Archivaufbewahrung als differenzielle Backups gelten, bleibt bei einem nun mit denselben Einstellungen durchgeführten vollständigen Backup nur dessen Archiv für PITR erhalten.

--------

## Wiederherstellung {#restore-1}

Der Befehl restore wählt standardmäßig automatisch das neueste Backup aus dem ersten Repository aus, in dem Backups vorhanden sind; siehe [Schnellstart – Backup wiederherstellen](#restore-a-backup). Die Prüfreihenfolge der Repositorys wird durch `pgbackrest.conf` bestimmt; beispielsweise wird repo1 vor repo2 geprüft. Mit der Option `--repo`, etwa `--repo=1`, lässt sich ein bestimmtes Repository auswählen. Wenn ein anderes als das neueste Backup gewünscht ist, kann die Option `--set` angegeben werden.

Bei PITR mit `--type=time` oder `--type=lsn` muss die Zielzeit bzw. die Ziel-LSN mit der Option `--target` angegeben werden. Ohne `--set` werden die konfigurierten Repositorys der Reihe nach nach einem Backup durchsucht, dessen Endzeit vor der Zielzeit liegt bzw. dessen End-LSN kleiner oder gleich der Ziel-LSN ist. Wird kein passendes Backup gefunden, meldet pgBackRest sowohl bei `--type=time` als auch bei `--type=lsn` einen Fehler; es fällt nicht auf das neueste Backup zurück. Bei anderen PITR-Typen, z. B. `xid`, muss die Option `--set` angegeben werden, wenn das Ziel vor dem neuesten Backup liegt. Weitere Informationen und Beispiele finden Sie unter [Point-in-Time-Recovery](#point-in-time-recovery).

Replikations-Slots werden gemäß der Empfehlung von PostgreSQL nicht eingeschlossen. Weitere Informationen stehen unter [Backup des Datenverzeichnisses](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-LOWLEVEL-BASE-BACKUP-DATA) in der PostgreSQL-Dokumentation.

Die folgenden Abschnitte stellen weitere Funktionen des Befehls `restore` vor.

### Dateieigentümer {#file-ownership}

Wird `restore` unter einem anderen Benutzer als root ausgeführt, was der übliche Fall ist, gehören alle wiederhergestellten Dateien dem Benutzer und der Gruppe, unter denen pgBackRest ausgeführt wird. Gehören vorhandene Dateien einem anderen Benutzer oder einer anderen Gruppe, tritt ein Fehler auf, wenn der Eigentümer nicht auf den ausführenden Benutzer beziehungsweise die ausführende Gruppe geändert werden kann. In diesem Fall muss ein privilegierter Benutzer die Dateieigentümer anpassen, bevor die Wiederherstellung erneut versucht werden kann.

Wird `restore` als Benutzer `root` ausgeführt, versucht pgBackRest, die beim Backup im Manifest gespeicherten Eigentümer wiederherzustellen. Das Manifest speichert nur die **Namen** von Benutzern und Gruppen. Damit dies funktioniert, müssen auf dem Wiederherstellungshost dieselben Namen existieren. Wird ein Benutzer- oder Gruppenname lokal nicht gefunden, wird der Benutzer beziehungsweise die Gruppe des PostgreSQL-Datenverzeichnisses verwendet. Lässt sich auch dessen Benutzer oder Gruppe keinem Namen zuordnen, wird letztlich `root` verwendet.

### Delta-Option {#delta-option}

Unter [Backup wiederherstellen](#restore-a-backup) im [Schnellstart](#quick-start) musste das Datenbankcluster-Verzeichnis vor der Ausführung von `restore` geleert werden. Mit der Option `delta` ermittelt pgBackRest automatisch, welche Dateien in diesem Verzeichnis erhalten bleiben können und welche aus dem Backup wiederhergestellt werden müssen. Außerdem *entfernt* es Dateien, die nicht im Backup-Manifest stehen, und beseitigt so abweichende Änderungen. Dazu wird für jede Datei im Datenbankcluster-Verzeichnis ein kryptografischer [SHA-1](https://en.wikipedia.org/wiki/SHA-1)-Hash berechnet. Stimmt der `SHA-1`-Hash nicht mit dem im Backup gespeicherten Hash überein, wird die Datei wiederhergestellt. In Verbindung mit der Option `process-max` ist dieses Verfahren sehr effizient. Da der PostgreSQL-Server während der Wiederherstellung gestoppt ist, können mehr Prozesse verwendet werden als während eines Backups bei laufendem PostgreSQL-Server sinnvoll wären.

pg-primary **⇒** Demo-Cluster stoppen und Delta-Wiederherstellung durchführen

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --log-level-console=detail restore
```

```text
       [filtered 2 lines of output]
P00 DETAIL: check '/var/lib/pgsql/14/data' exists
P00 DETAIL: remove 'global/pg_control' so cluster will not start if restore does not complete
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/backup_label.old'
P00 DETAIL: remove invalid file '/var/lib/pgsql/14/data/base/13755/pg_internal.init'
       [filtered 996 lines of output]
```

pg-primary **⇒** PostgreSQL neu starten

```bash
sudo systemctl start postgresql-14.service
```

### Ausgewählte Datenbanken wiederherstellen {#restore-selected-databases}

In manchen Fällen sollen gezielt einzelne Datenbanken aus einem Cluster-Backup wiederhergestellt werden. Gründe dafür können die Leistung sein oder der Wunsch, ausgewählte Datenbanken auf einen Rechner zu verschieben, dessen Speicherplatz für die Wiederherstellung des gesamten Cluster-Backups nicht ausreicht.

Zur Demonstration werden zwei Datenbanken erstellt: test1 und test2.

pg-primary **⇒** Zwei Testdatenbanken erstellen

```bash
sudo -u postgres psql -c "create database test1;"
```

```text
CREATE DATABASE
```

```bash
sudo -u postgres psql -c "create database test2;"
```

```text
CREATE DATABASE
```

Jede Testdatenbank wird mit Tabellen und Daten gefüllt, um zu zeigen, dass die Recovery bei einer selektiven Wiederherstellung funktioniert.

pg-primary **⇒** In jeder Datenbank eine Testtabelle erstellen

```bash
sudo -u postgres psql -c "create table test1_table (id int); \
       insert into test1_table (id) values (1);" test1
```

```text
CREATE TABLE
INSERT 0 1
```

```bash
sudo -u postgres psql -c "create table test2_table (id int); \
       insert into test2_table (id) values (2);" test2
```

```text
CREATE TABLE
INSERT 0 1
```

Ein neues Backup wird durchgeführt, damit pgBackRest die neuen Datenbanken kennt.

pg-primary **⇒** Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
```

Ein wesentlicher Grund für die selektive Wiederherstellung ist die Einsparung von Speicherplatz. Hier wird die Größe der Datenbank test1 angezeigt, um sie nach der selektiven Wiederherstellung mit deren Speicherbelegung vergleichen zu können.

pg-primary **⇒** Speicherbelegung der Datenbank test1 anzeigen

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.4M	/var/lib/pgsql/14/data/base/32768
```

Ist die wiederherzustellende Datenbank nicht bekannt, lassen sich mit der Option `set` des Befehls `info` die im Backup-Satz enthaltenen Datenbanken ermitteln.

pg-primary **⇒** Datenbankliste des Backups anzeigen

```bash
sudo -u postgres pgbackrest --stanza=demo \
       --set=20261002-185713F_20261002-185728I info
```

```text
       [filtered 12 lines of output]
            repo1: backup size: 2.1MB
            backup reference list: 20261002-185713F, 20261002-185713F_20261002-185719D
            database list: postgres (13755), test1 (32768), test2 (32769)
```

Den Cluster stoppen und nur die Datenbank test2 wiederherstellen. Die eingebauten Datenbanken `template0`, `template1` und `postgres` werden immer wiederhergestellt.

WARNUNG:

Ohne `--type=immediate` kann die Recovery mit einem Fehler abbrechen. Sobald Konsistenz erreicht ist, meldet PostgreSQL mit Nullen gefüllte Seiten als Fehler, auch bei einem Schreibvorgang für eine vollständige Seite. Für PostgreSQL ≥ 13 kann die Einstellung ignore_invalid_pages verwendet werden, um ungültige Seiten zu ignorieren. In diesem Fall ist es wichtig, die Protokolle nach der Recovery zu prüfen, um sicherzustellen, dass in den ausgewählten Datenbanken keine ungültigen Seiten gemeldet wurden.

pg-primary **⇒** Aus dem letzten Backup nur die Datenbank test2 wiederherstellen

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --db-include=test2 --type=immediate --target-action=promote restore
sudo systemctl start postgresql-14.service
```

Nach Abschluss der Recovery enthält die Datenbank test2 alle zuvor erstellten Tabellen und Daten.

pg-primary **⇒** Erfolgreiche Recovery der Datenbank test2 zeigen

```bash
sudo -u postgres psql -c "select * from test2_table;" test2
```

```text
 id
----
  2
(1 row)
```

Trotz erfolgreicher Recovery ist die Datenbank test1 nicht zugänglich. Sie wurde vollständig als mit Nullen gefüllte Sparse-Dateien wiederhergestellt. PostgreSQL kann WAL erfolgreich auf diese Dateien anwenden. Die Datenbank als Ganzes ist jedoch ungültig, da wichtige Dateien keine Daten enthalten. Dies ist beabsichtigt: Es verhindert die versehentliche Verwendung einer Datenbank, die möglicherweise nur unvollständige, während der WAL-Wiedergabe angewendete Daten enthält.

pg-primary **⇒** Verbindungsversuch mit der Datenbank test1 führt zu einem Fehler

```bash
sudo -u postgres psql -c "select * from test1_table;" test1
```

```text
psql: error: connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: FATAL:  relation mapping file "base/32768/pg_filenode.map" contains invalid data
```

Da die Datenbank test1 als mit Nullen gefüllte Sparse-Dateien wiederhergestellt wird, benötigt sie nur so viel Speicherplatz wie die während der Recovery geschriebene WAL-Menge. Die während eines Backups erzeugte und bei der Recovery angewendete WAL-Menge kann beträchtlich sein, macht aber in der Regel nur einen kleinen Teil der gesamten Datenbankgröße aus. Das gilt insbesondere für große Datenbanken, bei denen diese Funktion am ehesten nützlich ist.

Die Datenbank test1 belegt bei der selektiven Wiederherstellung deutlich weniger Speicherplatz, als sie bei einer vollständigen Wiederherstellung benötigt hätte.

pg-primary **⇒** Speicherbelegung der Datenbank test1 nach der Recovery anzeigen

```bash
sudo -u postgres du -sh /var/lib/pgsql/14/data/base/32768
```

```text
8.0K	/var/lib/pgsql/14/data/base/32768
```

Die einzige mögliche Aktion für die ungültige Datenbank test1 ist nun `drop database`. pgBackRest löscht die Datenbank nicht automatisch, da dies erst nach Abschluss der Recovery und bei zugänglichem Cluster möglich ist.

pg-primary **⇒** Datenbank test1 löschen

```bash
sudo -u postgres psql -c "drop database test1;"
```

```text
DROP DATABASE
```

Nach dem Löschen der ungültigen Datenbank test1 bleiben nur test2 und die eingebauten Datenbanken übrig.

pg-primary **⇒** Verbleibende Datenbanken auflisten

```bash
sudo -u postgres psql -c "select oid, datname from pg_database order by oid;"
```

```text
  oid  |  datname
-------+-----------
     1 | template1
 13754 | template0
 13755 | postgres
 32769 | test2
(4 rows)
```

--------

## Point-in-Time-Recovery {#point-in-time-recovery}

Unter [Backup wiederherstellen](#restore-a-backup) im [Schnellstart](#quick-start) wurde die standardmäßige Recovery durchgeführt, die den WAL-Strom bis zu seinem Ende wiedergibt. Bei einem Hardwareausfall ist dies normalerweise die beste Wahl. Bei Datenbeschädigungen, ob durch technische Fehler oder menschliches Handeln verursacht, ist dagegen häufig eine Point-in-Time-Recovery (PITR) geeigneter.

Point-in-Time-Recovery (PITR) ermöglicht es, das WAL ausgehend von einem Backup bis zu einer bestimmten LSN, einem Zeitpunkt, einer Transaktions-ID oder einem Recovery-Punkt wiederzugeben. Für übliche Recovery-Szenarien ist die zeitbasierte Recovery wohl am nützlichsten. Ein typischer Fall ist die Wiederherstellung einer versehentlich gelöschten Tabelle oder versehentlich gelöschter Daten. Da die Recovery einer gelöschten Tabelle anschaulicher ist, wird sie hier als Beispiel verwendet. Gelöschte Daten würden jedoch genauso wiederhergestellt.

pg-primary **⇒** Tabelle mit sehr wichtigen Daten erstellen

```bash
sudo -u postgres psql -c "begin; \
       create table important_table (message text); \
       insert into important_table values ('Important Data'); \
       commit; \
       select * from important_table;"
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Es ist wichtig, die Zeit so anzugeben, wie PostgreSQL sie erfasst, und den Zeitzonenversatz einzubeziehen. Das verringert das Risiko unbeabsichtigter Zeitzonenumrechnungen und eines unerwarteten Recovery-Ergebnisses.

pg-primary **⇒** Zeit von PostgreSQL abrufen

```bash
sudo -u postgres psql -Atc "select current_timestamp"
```

```text
2026-10-02 18:57:39.575732+00
```

Nachdem der Zeitpunkt festgehalten wurde, wird die Tabelle gelöscht. In der Praxis ist es wesentlich schwieriger als in diesem Beispiel, den genauen Zeitpunkt der Löschung zu ermitteln. Er lässt sich möglicherweise nicht exakt feststellen, doch eine Untersuchung der verfügbaren Spuren sollte eine gute Annäherung ermöglichen.

pg-primary **⇒** Wichtige Tabelle löschen

```bash
sudo -u postgres psql -c "begin; \
       drop table important_table; \
       commit; \
       select * from important_table;"
```

```text
BEGIN
DROP TABLE
COMMITERROR:  relation "important_table" does not exist
LINE 1: ...le important_table;     commit;     select * from important_...
                                                             ^
```

Wird für die Wiederherstellung das falsche Backup gewählt, schlägt die Recovery bis zur gewünschten Zielzeit fehl. Zur Demonstration wird ein neues inkrementelles Backup durchgeführt, in dem `important_table` nicht existiert.

pg-primary **⇒** Inkrementelles Backup durchführen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=incr backup
sudo -u postgres pgbackrest info
```

```text
       [filtered 38 lines of output]
            backup reference total: 1 full, 1 diff

        incr backup: 20261002-185713F_20261002-185741I
            timestamp start/stop: 2026-10-02 18:57:41+00 / 2026-10-02 18:57:42+00
            wal start/stop: 00000004000000000000001A / 00000004000000000000001A
       [filtered 2 lines of output]
```

Aus diesem Backup lässt sich die verlorene Tabelle nicht wiederherstellen, da PostgreSQL nur vorwärts und nicht rückwärts wiedergeben kann.

pg-primary **⇒** Recovery aus einem ungeeigneten Backup versuchen

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta \
       --set=20261002-185713F_20261002-185741I --target-timeline=current \
       --type=time "--target=2026-10-02 18:57:39.575732+00" --target-action=promote restore
sudo systemctl start postgresql-14.service
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 11 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  redo done at 0/1A000100 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.01 s
FATAL:  recovery ended before configured recovery target was reached
LOG:  startup process (PID 4045) exited with exit code 1
LOG:  terminating any other active server processes
LOG:  database system is shut down
```

Zuverlässig ist es, pgBackRest automatisch ein Backup auswählen zu lassen, das eine Recovery bis zur Zielzeit ermöglicht, also ein Backup, das vor dem angegebenen Zeitpunkt endete.

HINWEIS:

Beim Wiederherstellungstyp `xid` oder `name` kann pgBackRest das Backup nicht automatisch auswählen.

pg-primary **⇒** Demo-Cluster auf `2026-10-02 18:57:39.575732+00` wiederherstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --delta \
       --type=time "--target=2026-10-02 18:57:39.575732+00" \
       --target-action=promote restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
       [filtered 9 lines of output]
# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
recovery_target_time = '2026-10-02 18:57:39.575732+00'
recovery_target_action = 'promote'
```

pgBackRest hat die Recovery-Einstellungen in `postgresql.auto.conf` geschrieben, sodass PostgreSQL sofort gestartet werden kann. Mit `%f` gibt PostgreSQL das benötigte WAL-Segment an, mit `%p` den Speicherort, an den es kopiert werden soll. Sobald PostgreSQL die Recovery abgeschlossen hat, existiert die Tabelle wieder und kann abgefragt werden.

pg-primary **⇒** PostgreSQL starten und prüfen, ob die wichtige Tabelle existiert

```bash
sudo systemctl start postgresql-14.service
sudo -u postgres psql -c "select * from important_table"
```

```text
    message
----------------
 Important Data
(1 row)
```

Auch das PostgreSQL-Protokoll enthält wertvolle Informationen. Es nennt den Zeitpunkt und die Transaktion, bei der die Recovery gestoppt wurde, sowie den Zeitpunkt der zuletzt angewendeten Transaktion.

pg-primary **⇒** PostgreSQL-Protokollausgabe untersuchen

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 5 lines of output]
LOG:  database system was interrupted; last known up at 2026-10-02 18:57:28 UTC
LOG:  restored log file "00000004.history" from archive
LOG:  starting point-in-time recovery to 2026-10-02 18:57:39.575732+00
LOG:  restored log file "00000004.history" from archive
LOG:  restored log file "000000040000000000000019" from archive
       [filtered 2 lines of output]
LOG:  consistent recovery state reached at 0/19000100
LOG:  database system is ready to accept read-only connections
LOG:  recovery stopping before commit of transaction 743, time 2026-10-02 18:57:40.904112+00
LOG:  redo done at 0/1901E6C0 system usage: CPU: user: 0.00 s, system: 0.00 s, elapsed: 0.00 s
LOG:  last completed transaction was at log time 2026-10-02 18:57:38.228184+00
LOG:  selected new timeline ID: 5
LOG:  archive recovery complete
LOG:  database system is ready to accept connections
```

--------

## Stanza löschen {#delete-a-stanza}

Der Befehl `stanza-delete` entfernt die zu einer Stanza gehörenden Daten aus dem Repository.

WARNUNG:

Diesen Befehl mit Vorsicht verwenden: Er entfernt dauerhaft alle Backups und Archive der angegebenen Stanza aus dem pgBackRest-Repository.

Zum Löschen einer Stanza:

- Den PostgreSQL-Cluster stoppen, der zur Stanza gehört, oder diese Vorgabe mit --force übergehen.
- Den Befehl `stop` auf dem Host ausführen, auf dem `stanza-delete` ausgeführt werden soll.
- Den Befehl `stanza-delete` ausführen.

Nach dem erfolgreichen Abschluss des Befehls ist der Benutzer dafür verantwortlich, die Stanza aus allen pgBackRest-Konfigurationsdateien und/oder Umgebungsvariablen zu entfernen.

Eine Stanza kann jeweils nur aus einem Repository gelöscht werden. Zum Löschen aus mehreren Repositorys den Befehl `stanza-delete` für jedes Repository wiederholen und dabei die Option `--repo` angeben.

pg-primary **⇒** Zu entfernenden PostgreSQL-Cluster stoppen

```bash
sudo systemctl stop postgresql-14.service
```

pg-primary **⇒** pgBackRest für die Stanza stoppen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stop
```

```text
P00   INFO: stop command begin 2.59.3: --exec-id=4396-32c67a63 --log-level-console=info --no-log-timestamp --stanza=demo
P00   INFO: stop command end: completed successfully
```

pg-primary **⇒** Stanza aus einem Repository löschen

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=1 \
       --log-level-console=info stanza-delete
```

```text
P00   INFO: stanza-delete command begin 2.59.3: --exec-id=4428-6f4dadb2 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=1 --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --stanza=demo
P00   INFO: stanza-delete command end: completed successfully
```

--------

## Mehrere Repositorys {#multiple-repositories}

Es können mehrere Repositorys konfiguriert werden, wie unter [S3-Unterstützung](#s3-compatible-object-store-support) gezeigt. Ein möglicher Vorteil ist die Kombination eines lokalen Repositorys für schnelle Wiederherstellungen mit einem entfernten Repository für Redundanz.

Einige Befehle, etwa [`stanza-create`](/de/pgbackrest/command/stanza-create/)/[`stanza-upgrade`](/de/pgbackrest/command/stanza-upgrade/), arbeiten automatisch mit allen konfigurierten Repositorys. Andere, etwa [`stanza-delete`](/de/pgbackrest/command/stanza-delete/), erfordern die Angabe eines Repositorys über die Option `repo`.

Ist nur `repo1` konfiguriert, wird die Option `repo` zur Wahrung der Abwärtskompatibilität nicht benötigt. Ist dagegen ein einzelnes Repository beispielsweise als `repo2` konfiguriert, *ist* die Option `repo` erforderlich. Dadurch wird verhindert, dass Befehle nicht mehr funktionieren, wenn später ein weiteres Repository hinzukommt.

Der Befehl `archive-push` überträgt WAL immer in das Archiv aller konfigurierten Repositorys. Ist ein Repository nicht erreichbar, wird WAL weiterhin an die anderen Repositorys übertragen. Damit dies wirksam funktioniert, muss jedoch `archive-async=y` aktiviert sein; andernfalls können die anderen Repositorys dem nicht erreichbaren Repository nur um ein WAL-Segment voraus sein. Kann WAL in keines der Repositorys übertragen werden, entfernt PostgreSQL es nicht aus dem Verzeichnis `pg_wal`. Dadurch kann der Speicherplatz des Volumes erschöpft werden.

Backups müssen für jedes Repository einzeln geplant werden. Häufig ist das erwünscht, da sich Backup-Typen und Aufbewahrung je nach Repository unterscheiden. Ebenso muss bei Wiederherstellungen ein Repository angegeben werden. Im Allgemeinen empfiehlt sich dafür ein Repository mit geringer Latenz und niedrigen Kosten, auch wenn die Recovery dadurch länger dauert. Welches Repository am effizientesten ist, lässt sich nur durch Wiederherstellungstests ermitteln.

--------

## Unterstützung für Azure-kompatible Objektspeicher {#azure-compatible-object-store-support}

pgBackRest unterstützt Repositorys in Azure-kompatiblen Objektspeichern. Der Container für das Repository muss vorab erstellt werden; pgBackRest legt ihn nicht automatisch an. Das Repository kann im Stammverzeichnis des Containers (`/`) liegen. Meist empfiehlt sich jedoch ein Unterpfad, damit Objektspeicherprotokolle oder andere Daten ohne Konflikte im selben Container gespeichert werden können.

WARNUNG:

„Hierarchischer Namespace“ nicht aktivieren, da dies bei expire zu Fehlern führt.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Azure konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

start-fast=y



[global:archive-push]

compress-level=3
```

Shared Access Signatures können verwendet werden, indem die Option `repo2-azure-key-type` auf `sas` und `repo2-azure-key` auf das Shared-Access-Signature-Token gesetzt wird.

Die Befehle werden genauso ausgeführt, als läge das Repository auf einem lokalen Datenträger.

pg-primary **⇒** Stanza erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=4635-4a99c6c0 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo2-type=azure --stanza=demo
P00   INFO: stanza-create for stanza 'demo' on repo1
P00   INFO: stanza-create for stanza 'demo' on repo2
P00   INFO: stanza-create command end: completed successfully
```

Da das Erstellen von Dateien in Azure relativ langsam ist, verbessert die Aktivierung der [Dateibündelung](#file-bundling) die Leistung von `backup`/`restore`.

pg-primary **⇒** Backup des Demo-Clusters erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=2 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001B, lsn = 0/1B000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001B:00000005000000000000001B
P00   INFO: new backup label = 20261002-185802F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=4667-a84748a5 --log-level-console=info --no-log-timestamp --repo=2 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo2-type=azure --stanza=demo
```

--------

## Unterstützung für S3-kompatible Objektspeicher {#s3-compatible-object-store-support}

pgBackRest unterstützt Repositorys in S3-kompatiblen Objektspeichern. Der Bucket für das Repository muss vorab erstellt werden; pgBackRest legt ihn nicht automatisch an. Das Repository kann im Stammverzeichnis des Buckets (`/`) liegen. Meist empfiehlt sich jedoch ein Unterpfad, damit Objektspeicherprotokolle oder andere Daten ohne Konflikte im selben Bucket gespeichert werden können.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** S3 konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

start-fast=y



[global:archive-push]

compress-level=3
```

HINWEIS:

Region und Endpunkt müssen entsprechend dem Standort des Buckets konfiguriert werden. Die hier angegebenen Werte gelten für die Region `us-east-1`.

Für die Ausführung von pgBackRest sollte eine Rolle erstellt werden, und die Bucket-Berechtigungen sollten möglichst restriktiv gesetzt werden. Ist die Rolle einer AWS-Instanz zugeordnet, ruft pgBackRest bei `repo3-s3-key-type=auto` automatisch temporäre Zugangsdaten ab. Schlüssel müssen dann nicht ausdrücklich in `/etc/pgbackrest/pgbackrest.conf` angegeben werden.

Diese Amazon-S3-Beispielrichtlinie beschränkt alle Lese- und Schreibzugriffe auf den Bucket und den Repository-Pfad.

```text
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:prefix": [
                        "",
                        "demo-repo"
                    ],
                    "s3:delimiter": [
                        "/"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket"
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "demo-repo/*"
                    ]
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectTagging",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::demo-bucket/demo-repo/*"
            ]
        }
    ]
}
```

Die Befehle werden genauso ausgeführt, als läge das Repository auf einem lokalen Datenträger.

pg-primary **⇒** Stanza erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 4 lines of output]
P00   INFO: stanza 'demo' already exists on repo2 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo3
P00   INFO: stanza-create command end: completed successfully
```

Da das Erstellen von Dateien in S3 relativ langsam ist, verbessert die Aktivierung der [Dateibündelung](#file-bundling) die Leistung von `backup`/`restore`.

pg-primary **⇒** Backup des Demo-Clusters erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo --start-fast
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001D, lsn = 0/1D000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001D:00000005000000000000001D
P00   INFO: new backup label = 20261002-185820F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5060-13323a52 --log-level-console=info --no-log-timestamp --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo2-type=azure --repo3-type=s3 --stanza=demo
```

--------

## SFTP-Unterstützung {#sftp-support}

pgBackRest unterstützt Repositorys auf SFTP-Hosts. SFTP-Dateiübertragungen sind relativ langsam. Daher profitieren Befehle von einer Erhöhung von `process-max`, um die Dateiübertragungen zu parallelisieren.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** SFTP konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

start-fast=y



[global:archive-push]

compress-level=3
```

Bei der Verwendung von SFTP ist `repo4-sftp-public-key-file` optional, wenn libssh2 gegen OpenSSH kompiliert wurde.

pg-primary **⇒** SSH-Schlüsselpaar für SFTP-Backups erzeugen

```bash
sudo -u postgres mkdir -m 750 -p /var/lib/pgsql/.ssh
sudo -u postgres ssh-keygen -f /var/lib/pgsql/.ssh/id_rsa_sftp \
       -t rsa -b 4096 -N "" -m PEM
```

sftp-server **⇒** Öffentlichen SFTP-Backup-Schlüssel von pg-primary nach sftp-server kopieren

```bash
sudo -u pgbackrest mkdir -m 750 -p /home/pgbackrest/.ssh
(sudo ssh root@pg-primary cat /var/lib/pgsql/.ssh/id_rsa_sftp.pub) | \
       sudo -u pgbackrest tee -a /home/pgbackrest/.ssh/authorized_keys
```

Die Befehle werden genauso ausgeführt, als läge das Repository auf einem lokalen Datenträger.

pg-primary **⇒** Fingerprint von sftp-server zur Datei known_hosts hinzufügen, da `repo4-sftp-host-key-check-type` standardmäßig "strict" verwendet

```bash
ssh-keyscan -H sftp-server >> /var/lib/pgsql/.ssh/known_hosts 2>/dev/null
```

pg-primary **⇒** Stanza erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info stanza-create
```

```text
       [filtered 6 lines of output]
P00   INFO: stanza 'demo' already exists on repo3 and is valid
P00   INFO: stanza-create for stanza 'demo' on repo4
P00   INFO: stanza-create command end: completed successfully
```

pg-primary **⇒** Backup des Demo-Clusters erstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=4 \
       --log-level-console=info backup
```

```text
P00   INFO: backup command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-block --repo1-bundle --repo4-bundle --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo --start-fast
P00   WARN: option 'repo4-retention-full' is not set for 'repo4-retention-full-type=count', the repository may run out of space
            HINT: to retain full backups indefinitely (without warning), set option 'repo4-retention-full' to the maximum.
P00   WARN: no prior backup exists, incr backup has been changed to full
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000005000000000000001E, lsn = 0/1E000028
       [filtered 3 lines of output]
P00   INFO: check archive for segment(s) 00000005000000000000001E:00000005000000000000001F
P00   INFO: new backup label = 20261002-185837F
P00   INFO: full backup size = 33.5MB, file total = 1249
P00   INFO: backup command end: completed successfully
P00   INFO: expire command begin 2.59.3: --exec-id=5361-dd15b633 --log-level-console=info --no-log-timestamp --repo=4 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo1-retention-diff=2 --repo1-retention-full=2 --repo2-retention-full=4 --repo3-retention-full=4 --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --stanza=demo
P00   INFO: expire command end: completed successfully
```

--------

## Unterstützung für GCS-kompatible Objektspeicher {#gcs-compatible-object-store-support}

pgBackRest unterstützt Repositorys in GCS-kompatiblen Objektspeichern. Der Bucket für das Repository muss vorab erstellt werden; pgBackRest legt ihn nicht automatisch an. Das Repository kann im Stammverzeichnis des Buckets (`/`) liegen. Meist empfiehlt sich jedoch ein Unterpfad, damit Objektspeicherprotokolle oder andere Daten ohne Konflikte im selben Bucket gespeichert werden können.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** GCS konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=4

repo1-block=y

repo1-bundle=y

repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO

repo1-cipher-type=aes-256-cbc

repo1-path=/var/lib/pgbackrest

repo1-retention-diff=2

repo1-retention-full=2

repo2-azure-account=pgbackrest

repo2-azure-container=demo-container

repo2-azure-key=YXpLZXk=

repo2-path=/demo-repo

repo2-retention-full=4

repo2-type=azure

repo3-path=/demo-repo

repo3-retention-full=4

repo3-s3-bucket=demo-bucket

repo3-s3-endpoint=s3.us-east-1.amazonaws.com

repo3-s3-key=accessKey1

repo3-s3-key-secret=verySecretKey1

repo3-s3-region=us-east-1

repo3-type=s3

repo4-bundle=y

repo4-path=/demo-repo

repo4-sftp-host=sftp-server

repo4-sftp-host-key-hash-type=sha1

repo4-sftp-host-user=pgbackrest

repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp

repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub

repo4-type=sftp

repo5-gcs-bucket=demo-bucket

repo5-gcs-key=/etc/pgbackrest/gcs-key.json

repo5-path=/demo-repo

repo5-type=gcs

start-fast=y



[global:archive-push]

compress-level=3
```

Bei der Ausführung in GCE `repo5-gcs-key-type=auto` setzen, um sich automatisch über das Dienstkonto der Instanz zu authentifizieren.

Die Befehle werden genauso ausgeführt, als läge das Repository auf einem lokalen Datenträger.

Da das Erstellen von Dateien in GCS relativ langsam ist, verbessert die Aktivierung der [Dateibündelung](#file-bundling) die Leistung von `backup`/`restore`.

--------

## Zielzeit für ein Repository {#target-time-for-repository}

Die Zielzeit legt den Zeitpunkt fest, auf dessen Stand Befehle ein Repository auf versioniertem Speicher lesen. So kann ein Befehl das Repository in seinem damaligen Zustand lesen, um Daten wiederherzustellen, die durch ein Benutzerversehen oder Schadsoftware gelöscht oder beschädigt wurden.

Versionierter Speicher wird von S3, GCS und Azure unterstützt, ist jedoch im Allgemeinen nicht standardmäßig aktiviert. Zusätzlich zur Versionierung kann es sinnvoll sein, für S3 die Objektsperre und für GCS oder Azure das vorläufige Löschen (Soft Delete) zu aktivieren.

Wenn die Option `repo-target-time` angegeben wird, muss auch die Option `repo` angegeben werden. Voraussichtlich werden nicht alle Repository-Typen Versionierung unterstützen. Außerdem ist es im Allgemeinen sinnvoll, für die Recovery gezielt ein einzelnes Repository auszuwählen.

Der Speicherzeitstempel wird darauf geprüft, ob er <= dem angegebenen Zeitstempel ist. Enthält der angegebene Zeitstempel Millisekunden, werden sie abgeschnitten.

Zur Demonstration dieser Funktion wird die Stanza `demo` im S3-Repository gelöscht.

pg-primary **⇒** Stanza im S3-Repository löschen

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo stop
sudo -u postgres pgbackrest --stanza=demo --repo=3 stanza-delete
```

Nach dem Löschen der Stanza zeigt der Befehl `info` das Repository in einem Fehlerzustand an.

pg-primary **⇒** Fehler bei info

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 info
```

```text
stanza: demo
    status: error (missing stanza path)
```

Da der Speicher versioniert ist, lässt sich das Repository jedoch zu einem Zeitpunkt vor dem Löschen der Stanza betrachten. Je nach Situation kann es schwierig sein, die Zielzeit zu ermitteln. Hier lässt sich der Löschzeitpunkt der Stanza anhand des Löschzeitpunkts von `backup.info` bestimmen.

pg-primary **⇒** Versionen von `backup.info` im Bucket auflisten

```bash
key=demo-repo/backup/demo/backup.info; \
       aws s3api list-object-versions --bucket demo-bucket \
       --prefix $key --output table \
       --query "sort_by([Versions[?Key=='$key'].{Action:'PUT', \
       Modified:LastModified,Object:Key}, \
       DeleteMarkers[?Key=='$key'].{Action:'DELETE', \
       Modified:LastModified,Object:Key}][],&Modified)"
```

```text
-------------------------------------------------------------------------------------
|                                ListObjectVersions                                 |
+--------+------------------------------------+-------------------------------------+
| Action |             Modified               |               Object                |
+--------+------------------------------------+-------------------------------------+
|  PUT   |  2026-10-02T18:58:20.631000+00:00  |  demo-repo/backup/demo/backup.info  |
|  PUT   |  2026-10-02T18:58:33.900000+00:00  |  demo-repo/backup/demo/backup.info  |
|  DELETE|  2026-10-02T18:58:45.634000+00:00  |  demo-repo/backup/demo/backup.info  |
+--------+------------------------------------+-------------------------------------+
```

Der Befehl `info` kann nun mit einer Zielzeit ausgeführt werden, die das Repository vor dem Löschen zeigt.

pg-primary **⇒** Info mit Zielzeit

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 \
       --repo-target-time="2026-10-02 18:58:34+00" info
```

```text
       [filtered 5 lines of output]
        wal archive min/max (14): 00000005000000000000001C/00000005000000000000001D

        full backup: 20261002-185820F
            timestamp start/stop: 2026-10-02 18:58:20+00 / 2026-10-02 18:58:33+00
            wal start/stop: 00000005000000000000001D / 00000005000000000000001D
            repo3: backup set size: 4.2MB, backup size: 4.2MB
```

Wenn der Befehl `info` das benötigte Backup anzeigt, kann es mit derselben Zielzeit wiederhergestellt werden.

pg-primary **⇒** Wiederherstellung mit Zielzeit

```bash
sudo -u postgres pgbackrest --stanza=demo --repo=3 --delta \
       --repo-target-time="2026-10-02 18:58:34+00" --log-level-console=info restore
```

```text
P00   INFO: restore command begin 2.59.3: --delta --exec-id=5686-f718513c --log-level-console=info --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=4 --repo=3 --repo2-azure-account=<redacted> --repo2-azure-container=demo-container --repo2-azure-key=<redacted> --repo1-cipher-pass=<redacted> --repo1-cipher-type=aes-256-cbc --repo5-gcs-bucket=demo-bucket --repo5-gcs-key=<redacted> --repo1-path=/var/lib/pgbackrest --repo2-path=/demo-repo --repo3-path=/demo-repo --repo4-path=/demo-repo --repo5-path=/demo-repo --repo3-s3-bucket=demo-bucket --repo3-s3-endpoint=s3.us-east-1.amazonaws.com --repo3-s3-key=<redacted> --repo3-s3-key-secret=<redacted> --repo3-s3-region=us-east-1 --repo4-sftp-host=sftp-server --repo4-sftp-host-key-hash-type=sha1 --repo4-sftp-host-user=pgbackrest --repo4-sftp-private-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp --repo4-sftp-public-key-file=/var/lib/pgsql/.ssh/id_rsa_sftp.pub --repo-target-time="2026-10-02 18:58:34+00" --repo2-type=azure --repo3-type=s3 --repo4-type=sftp --repo5-type=gcs --stanza=demo
P00   INFO: repo3: restore backup set 20261002-185820F, recovery will start at 2026-10-02 18:58:20
P00   INFO: remove invalid files/links/paths from '/var/lib/pgsql/14/data'
P00   INFO: write updated /var/lib/pgsql/14/data/postgresql.auto.conf
       [filtered 2 lines of output]
```

```bash
sudo systemctl start postgresql-14.service
```

--------

## Dedizierter Repository-Host {#dedicated-repository-host}

Die unter [Schnellstart](#quick-start) beschriebene Konfiguration eignet sich für einfache Installationen. In Unternehmensumgebungen ist dagegen ein dedizierter Repository-Host üblich, auf dem Backups und WAL-Archivdateien gespeichert werden. Dadurch sind Backups und WAL-Archiv vom Datenbankserver getrennt, sodass Ausfälle des Datenbankhosts geringere Auswirkungen haben. Zusätzlich empfiehlt es sich weiterhin, den Repository-Host mit herkömmlicher Backup-Software zu sichern.

Auf PostgreSQL-Hosts muss `pg1-path` auf den lokalen PostgreSQL-Cluster verweisen, und `pg1-host` sollte nicht konfiguriert sein. Auf einem Repository-Host muss in der pgBackRest-Konfigurationsdatei die Option `pg-host` für die Verbindung zum Primärserver und zu gegebenenfalls vorhandenen Standby-Hosts konfiguriert sein. Nur die pgBackRest-Konfiguration des Repository-Hosts sollte mehr als einen PostgreSQL-Host kennen. Die Reihenfolge spielt keine Rolle: Beispielsweise können pg1-path/pg1-host und pg2-path/pg2-host jeweils Primärserver oder Standby bezeichnen.

### Installation {#installation-1}

Ein neuer Host namens repository wird zum Speichern der Cluster-Backups eingerichtet.

HINWEIS:

Die auf dem Repository-Host installierte pgBackRest-Version muss exakt mit der Version auf dem PostgreSQL-Host übereinstimmen.

Der Benutzer `pgbackrest` wird als Eigentümer des pgBackRest-Repositorys angelegt. Jeder Benutzer kann Eigentümer des Repositorys sein. Zur Vermeidung von Verwechslungen empfiehlt es sich jedoch, nicht den Benutzer `postgres` zu verwenden, falls dieser existiert.

HINWEIS:

Bei der Installation von pgBackRest aus einem Paket wird möglicherweise eine logrotate-Konfiguration wie `/etc/logrotate.d/pgbackrest` bereitgestellt, die die Protokolle über die Direktive `su` unter einem bestimmten Benutzer rotiert, beispielsweise `su postgres postgres`. Da die Dateien in `/var/log/pgbackrest` dem Benutzer gehören, der pgBackRest ausführt, hier `pgbackrest`, muss die Direktive `su` auf diesen Benutzer angepasst werden. Andernfalls schlägt logrotate mit einem Berechtigungsfehler fehl.

repository **⇒** Benutzer `pgbackrest` erstellen

```bash
sudo groupadd pgbackrest
sudo adduser -gpgbackrest -n pgbackrest
```

Die Installation von pgBackRest aus einem Paket ist der Kompilierung aus dem Quellcode vorzuziehen. Bei einer Paketinstallation sind die übrigen Anweisungen in diesem Abschnitt normalerweise nicht erforderlich. Es kann jedoch vorkommen, dass ein Paket eines der Verzeichnisse nicht anlegt oder falsche Berechtigungen vergibt. In diesem Fall kann es erforderlich sein, Verzeichnisse manuell anzulegen oder Berechtigungen anzupassen.

RHEL-Pakete für pgBackRest sind unter [yum.postgresql.org](http://yum.postgresql.org) verfügbar.

Falls für Ihre Distribution oder Version keine Pakete bereitstehen, können Sie pgBackRest [aus dem Quellcode kompilieren](#build) und anschließend wie hier gezeigt manuell installieren.

repository **⇒** Abhängigkeiten installieren

```bash
sudo yum install postgresql-libs libssh2
```

repository **⇒** pgBackRest-Binärdatei vom Build-Host kopieren

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest benötigt Protokoll- und Konfigurationsverzeichnisse sowie eine Konfigurationsdatei.

repository **⇒** pgBackRest-Konfigurationsdatei und Verzeichnisse erstellen

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown pgbackrest:pgbackrest /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown pgbackrest:pgbackrest /etc/pgbackrest/pgbackrest.conf
```

repository **⇒** pgBackRest-Repository erstellen

```bash
sudo mkdir -p /var/lib/pgbackrest
sudo chmod 750 /var/lib/pgbackrest
sudo chown pgbackrest:pgbackrest /var/lib/pgbackrest
```

### Konfiguration {#configuration}

pgBackRest kann TLS mit Clientzertifikaten für die Kommunikation zwischen Hosts verwenden. Alternativ ist SSH möglich; siehe [SSH einrichten](/de/pgbackrest/user-guide/#setup-passwordless-ssh).

pgBackRest erwartet, dass Client- und Serverzertifikate genauso wie für PostgreSQL erstellt werden. Eine ausführliche Anleitung zum Erstellen von Zertifikaten steht unter [Sichere TCP/IP-Verbindungen mit TLS](https://www.postgresql.org/docs/current/ssl-tcp.html).

Auf dem Repository-Host müssen Hostname und Benutzer von pg-primary sowie der Datenbankpfad konfiguriert werden. Der Primärserver wird als `pg1` konfiguriert, damit später ein Standby hinzugefügt werden kann.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-host`/`pg1-host-user` und `pg1-path` konfigurieren

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Auf dem Datenbankhost müssen Hostname und Benutzer des Repository-Hosts konfiguriert werden. Der Standardwert der Option `repo1-host-user` ist `pgbackrest`. Wenn der Benutzer `postgres` auf dem Repository-Host Wiederherstellungen durchführt, empfiehlt es sich, dem Benutzer `postgres` nicht zusätzlich die Durchführung von Backups zu erlauben. Der Benutzer `postgres` kann das Repository jedoch direkt lesen, wenn er derselben Gruppe wie `pgbackrest` angehört.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `repo1-host`/`repo1-host-user` konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Die PostgreSQL-Konfiguration ist im Abschnitt [Archivierung konfigurieren](#configure-archiving) beschrieben.

Die Befehle werden genauso ausgeführt wie bei einer Konfiguration mit einem einzelnen Host. Einige Befehle, etwa `backup` und `expire`, laufen jedoch auf dem Repository-Host statt auf dem Datenbankhost.

### TLS-Server einrichten {#setup-tls-server}

Der pgBackRest-TLS-Server muss auf jedem Host konfiguriert und gestartet werden.

repository **⇒** pgBackRest-Server einrichten

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=pgbackrest
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

pg-primary **⇒** pgBackRest-Server einrichten

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### Stanza erstellen und prüfen {#create-and-check-stanza}

Die Stanza im neuen Repository erstellen.

repository **⇒** Stanza erstellen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo stanza-create
```

Die Konfiguration sowohl auf dem Datenbankhost als auch auf dem Repository-Host prüfen. Weitere Informationen zum Befehl `check` stehen unter [Konfiguration prüfen](#check-the-configuration).

pg-primary **⇒** Konfiguration prüfen

```bash
sudo -u postgres pgbackrest --stanza=demo check
```

repository **⇒** Konfiguration prüfen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

### Backup durchführen {#perform-a-backup-1}

Für ein Backup des PostgreSQL-Clusters pgBackRest mit dem Befehl `backup` auf dem Repository-Host ausführen.

repository **⇒** Backup des Demo-Clusters erstellen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: no prior backup exists, incr backup has been changed to full
```

Da auf dem Repository-Host ein neues Repository erstellt wurde, erschien die Warnung, dass das inkrementelle Backup in ein vollständiges Backup umgewandelt wurde.

### Backup wiederherstellen {#restore-a-backup-1}

Zur Wiederherstellung des PostgreSQL-Clusters pgBackRest mit dem Befehl `restore` auf dem Datenbankhost ausführen.

pg-primary **⇒** Demo-Cluster stoppen, wiederherstellen und PostgreSQL neu starten

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta restore
sudo systemctl start postgresql-14.service
```

--------

## Paralleles Backup / parallele Wiederherstellung {#parallel-backup--restore}

pgBackRest bietet parallele Verarbeitung, um die Leistung von Komprimierung und Übertragung zu verbessern. Die Anzahl der dafür verwendeten Prozesse wird mit der Option `--process-max` festgelegt.

Für den Befehl `backup` empfiehlt es sich normalerweise, höchstens 25% der verfügbaren CPUs zu verwenden. Backups müssen nicht besonders schnell laufen, solange sie regelmäßig durchgeführt werden. Der Backup-Prozess sollte die Datenbankleistung möglichst nicht beeinträchtigen.

Der Befehl restore kann und sollte alle verfügbaren CPUs verwenden, da der PostgreSQL-Cluster während einer Wiederherstellung gestoppt ist und auf dem Host normalerweise keine anderen wichtigen Arbeiten stattfinden. Enthält der Host mehrere Cluster, sollte dies bei der Festlegung der Parallelität der Wiederherstellung berücksichtigt werden.

repository **⇒** Backup mit einem einzelnen Prozess durchführen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** pgBackRest für mehrere `backup`-Prozesse konfigurieren

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository **⇒** Backup mit mehreren Prozessen durchführen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

repository **⇒** Backup-Informationen zum Demo-Cluster abrufen

```bash
sudo -u pgbackrest pgbackrest info
```

```text
stanza: demo
    status: ok
    cipher: none

    db (current)
        wal archive min/max (14): 000000070000000000000023/000000070000000000000025

        full backup: 20261002-185937F
            timestamp start/stop: 2026-10-02 18:59:37+00 / 2026-10-02 18:59:40+00
            wal start/stop: 000000070000000000000023 / 000000070000000000000023
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB

        full backup: 20261002-185941F
            timestamp start/stop: 2026-10-02 18:59:41+00 / 2026-10-02 18:59:43+00
            wal start/stop: 000000070000000000000024 / 000000070000000000000025
            database size: 33.5MB, database backup size: 33.5MB
            repo1: backup set size: 4.2MB, backup size: 4.2MB
```

Durch die Verwendung mehrerer Prozesse sollte das letzte Backup schneller sein. Bei sehr kleinen Backups ist der Unterschied möglicherweise kaum erkennbar. Mit zunehmender Datenbankgröße steigt jedoch auch die Zeitersparnis.

--------

## Starten und Stoppen {#starting-and-stopping}

Wird ein Standby zu Testzwecken hochgestuft oder ein Testcluster aus einem Produktionsbackup wiederhergestellt, empfiehlt es sich, Schreibzugriffe dieser Cluster auf pgBackRest-Repositorys zu verhindern. Dies ist mit dem Befehl `stop` möglich.

Die schreibenden Befehle, die `stop` blockiert, sind `archive-push`, `backup`, `expire`, `stanza-create` und `stanza-upgrade`. `stanza-delete` ist eine Ausnahme von dieser Regel; weitere Einzelheiten stehen unter [Stanza löschen](#delete-a-stanza).

pg-primary **⇒** Schreibende pgBackRest-Befehle stoppen

```bash
sudo -u postgres pgbackrest stop
```

Neue schreibende pgBackRest-Befehle werden nicht mehr ausgeführt.

repository **⇒** Backup versuchen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for all stanzas
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

Mit der Option `--force` werden bereits laufende schreibende pgBackRest-Befehle beendet. Das schließt asynchrones archive-get ein, das jedoch erneut läuft, wenn PostgreSQL es benötigt. Ist pgBackRest bereits gestoppt, erzeugt ein erneutes Stoppen eine Warnung.

pg-primary **⇒** pgBackRest-Dienste erneut stoppen

```bash
sudo -u postgres pgbackrest stop
```

```text
P00   WARN: stop file already exists for all stanzas
```

Mit dem Befehl `start` werden schreibende pgBackRest-Befehle wieder zugelassen. Schreibende Befehle, die vor dem Stoppen liefen, starten nicht automatisch erneut; sie dürfen jetzt jedoch wieder gestartet werden.

pg-primary **⇒** Schreibende pgBackRest-Befehle starten

```bash
sudo -u postgres pgbackrest start
```

pgBackRest kann auch für eine einzelne Stanza gestoppt werden.

pg-primary **⇒** Schreibende pgBackRest-Befehle für die Stanza `demo` stoppen

```bash
sudo -u postgres pgbackrest --stanza=demo stop
```

Neue schreibende pgBackRest-Befehle für die angegebene Stanza werden nicht mehr ausgeführt.

repository **⇒** Backup versuchen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo backup
```

```text
P00   WARN: unable to check pg1: [StopError] raised from remote-0 tls protocol on 'pg-primary': stop file exists for stanza demo
P00  ERROR: [056]: unable to find primary cluster - cannot proceed
            HINT: are all available clusters in recovery?
```

Auch beim Starten schreibender pgBackRest-Befehle für eine einzelne Stanza muss diese angegeben werden.

pg-primary **⇒** Schreibende pgBackRest-Befehle für die Stanza `demo` starten

```bash
sudo -u postgres pgbackrest --stanza=demo start
```

--------

## Replikation {#replication}

Durch Replikation lassen sich mehrere Kopien eines PostgreSQL-Clusters, sogenannte Standbys, von einem einzigen Primärserver erstellen. Standbys dienen zur Verteilung von Lesezugriffen und bieten Redundanz, falls der primäre Host ausfällt.

### Installation {#installation-2}

Ein neuer Host namens pg-standby wird für den Betrieb des Standbys eingerichtet.

Die Installation von pgBackRest aus einem Paket ist der Kompilierung aus dem Quellcode vorzuziehen. Bei einer Paketinstallation sind die übrigen Anweisungen in diesem Abschnitt normalerweise nicht erforderlich. Es kann jedoch vorkommen, dass ein Paket eines der Verzeichnisse nicht anlegt oder falsche Berechtigungen vergibt. In diesem Fall kann es erforderlich sein, Verzeichnisse manuell anzulegen oder Berechtigungen anzupassen.

RHEL-Pakete für pgBackRest sind unter [yum.postgresql.org](http://yum.postgresql.org) verfügbar.

Falls für Ihre Distribution oder Version keine Pakete bereitstehen, können Sie pgBackRest [aus dem Quellcode kompilieren](#build) und anschließend wie hier gezeigt manuell installieren.

pg-standby **⇒** Abhängigkeiten installieren

```bash
sudo yum install postgresql-libs libssh2
```

pg-standby **⇒** pgBackRest-Binärdatei vom Build-Host kopieren

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest benötigt Protokoll- und Konfigurationsverzeichnisse sowie eine Konfigurationsdatei.

pg-standby **⇒** pgBackRest-Konfigurationsdatei und Verzeichnisse erstellen

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Hot Standby {#hot-standby}

Ein Hot Standby repliziert über das WAL-Archiv und erlaubt schreibgeschützte Abfragen.

Die pgBackRest-Konfiguration ist der von pg-primary sehr ähnlich. Es wird jedoch der Recovery-Typ `standby` verwendet, damit der Cluster nach Erreichen des Endes des WAL-Stroms im Recovery-Modus bleibt.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** pgBackRest auf dem Standby konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-standby **⇒** pgBackRest-Server einrichten

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

Den Pfad erstellen, in dem PostgreSQL wiederhergestellt werden soll.

pg-standby **⇒** PostgreSQL-Pfad erstellen

```bash
sudo -u postgres mkdir -p -m 700 /var/lib/pgsql/14/data
```

Nun kann der Standby mit dem Befehl `restore` erstellt werden.

WICHTIG:

Soll der Cluster hochgestuft werden, ohne zum neuen Primärserver zu werden, beispielsweise für Berichte oder Tests, die Archivierung mit `--archive-mode=off` oder archive_mode=off in `postgresql.conf` deaktivieren. Andernfalls kann WAL im Repository landen, das Wiederherstellungen erschwert.

pg-standby **⇒** Demo-Standby-Cluster wiederherstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:04
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

Diese Konfiguration gilt für den Fall, dass der Standby zum Primärserver hochgestuft wird.

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** PostgreSQL konfigurieren

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** PostgreSQL starten

```bash
sudo systemctl start postgresql-14.service
```

Das PostgreSQL-Protokoll liefert wertvolle Informationen zur Recovery. Besonders zu beachten ist, dass der Cluster in den Standby-Modus gewechselt ist und schreibgeschützte Verbindungen annehmen kann.

pg-standby **⇒** PostgreSQL-Protokollausgabe auf Erfolgsmeldungen prüfen

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 4 lines of output]
LOG:  listening on Unix socket "/tmp/.s.PGSQL.5432"
LOG:  database system was interrupted; last known up at 2026-10-02 18:59:41 UTC
LOG:  entering standby mode
LOG:  restored log file "00000007.history" from archive
LOG:  restored log file "000000070000000000000024" from archive
       [filtered 3 lines of output]
```

Eine einfache Prüfung der Replikationskonfiguration besteht darin, auf pg-primary eine Tabelle zu erstellen.

pg-primary **⇒** Neue Tabelle auf dem Primärserver erstellen

```bash
sudo -u postgres psql -c " \
       begin; \
       create table replicated_table (message text); \
       insert into replicated_table values ('Important Data'); \
       commit; \
       select * from replicated_table";
```

```text
       [filtered 4 lines of output]
    message
----------------
 Important Data
(1 row)
```

Anschließend dieselbe Tabelle auf pg-standby abfragen.

pg-standby **⇒** Neue Tabelle auf dem Standby abfragen

```bash
sudo -u postgres psql -c "select * from replicated_table;"
```

```text
ERROR:  relation "replicated_table" does not exist
LINE 1: select * from replicated_table;
                      ^
```

Was ist schiefgegangen? Da PostgreSQL WAL-Segmente für die Replikation aus dem Archiv abruft, werden Änderungen auf dem Standby erst sichtbar, wenn pg-primary das WAL-Segment mit diesen Änderungen in das Archiv übertragen hat.

Dies lässt sich manuell durch einen Aufruf von `pg_switch_wal()` auslösen. Dadurch wird das aktuelle WAL-Segment ins Archiv übertragen und ein neues WAL-Segment für weitere Änderungen erstellt.

pg-primary **⇒** `pg_switch_wal()` aufrufen

```bash
sudo -u postgres psql -c "select *, current_timestamp from pg_switch_wal()";
```

```text
 pg_switch_wal |       current_timestamp
---------------+-------------------------------
 0/2601E7C0    | 2026-10-02 19:00:10.880013+00
(1 row)
```

Nach einer kurzen Verzögerung erscheint die Tabelle nun auf pg-standby.

pg-standby **⇒** Die neue Tabelle existiert jetzt auf dem Standby; möglicherweise sind einige Versuche nötig

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from replicated_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:11.954843+00
(1 row)
```

Die Standby-Konfiguration auf Zugriff zum Repository prüfen.

pg-standby **⇒** Konfiguration prüfen

```bash
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1250-e6a5e2d8 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 (standby)
P00   INFO: switch wal not performed because this is a standby
P00   INFO: check command end: completed successfully
```

### Streaming-Replikation {#streaming-replication}

Streaming-Replikation verlässt sich nicht allein auf das WAL-Archiv, sondern stellt eine direkte Verbindung zum Primärserver her und wendet Änderungen an, sobald sie dort vorgenommen werden. Dadurch ist die Verzögerung zwischen Primärserver und Standby deutlich geringer.

Streaming-Replikation erfordert einen Benutzer mit Replikationsberechtigung.

pg-primary **⇒** Replikationsbenutzer erstellen

```bash
sudo -u postgres psql -c " \
       create user replicator password 'jw8s0F4' replication";
```

```text
CREATE ROLE
```

Die Datei `pg_hba.conf` muss angepasst werden, damit der Standby eine Verbindung als Replikationsbenutzer herstellen darf. Die folgende IP-Adresse durch die tatsächliche IP-Adresse von pg-standby ersetzen. Nach der Änderung von `pg_hba.conf` muss die Konfiguration neu geladen werden.

pg-primary **⇒** Eintrag in `pg_hba.conf` für den Replikationsbenutzer erstellen

```bash
sudo -u postgres sh -c 'echo \
       "host    replication     replicator      172.17.0.8/32           md5" \
       >> /var/lib/pgsql/14/data/pg_hba.conf'
sudo systemctl reload postgresql-14.service
```

Der Standby muss wissen, wie er den Primärserver erreicht. Daher wird die Einstellung primary_conninfo in pgBackRest konfiguriert.

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** primary_conninfo setzen

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Ein Passwort kann in der Einstellung primary_conninfo angegeben werden. Eine Datei `.pgpass` ist jedoch flexibler und sicherer.

pg-standby **⇒** Replikationspasswort in der Datei `.pgpass` konfigurieren.

```bash
sudo -u postgres sh -c 'echo \
       "172.17.0.6:*:replication:replicator:jw8s0F4" \
       >> /var/lib/pgsql/.pgpass'
sudo -u postgres chmod 600 /var/lib/pgsql/.pgpass
```

Nun kann der Standby mit dem Befehl `restore` erstellt werden.

pg-standby **⇒** PostgreSQL stoppen und Demo-Standby-Cluster wiederherstellen

```bash
sudo systemctl stop postgresql-14.service
sudo -u postgres pgbackrest --stanza=demo --delta --type=standby restore
sudo -u postgres cat /var/lib/pgsql/14/data/postgresql.auto.conf
```

```text
# Do not edit this file manually!
# It will be overwritten by the ALTER SYSTEM command.

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:00
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:22
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:57:47
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_time = '2026-10-02 18:57:39.575732+00'
# Removed by pgBackRest restore on 2026-10-02 18:58:52 # recovery_target_action = 'promote'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:58:52
restore_command = 'pgbackrest --repo=3 --repo-target-time="2026-10-02 18:58:34+00" --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 18:59:32
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'

# Recovery settings generated by pgBackRest restore on 2026-10-02 19:00:18
primary_conninfo = 'host=172.17.0.6 port=5432 user=replicator'
restore_command = 'pgbackrest --stanza=demo archive-get %f "%p"'
```

HINWEIS:

Die Einstellung primary_conninfo wurde in die Datei `postgresql.auto.conf` geschrieben, da sie als `recovery-option` in `pgbackrest.conf` konfiguriert war. Falls gewünscht, kann mit `restore` die Option `--type=preserve` verwendet werden, um die vorhandene Datei `postgresql.auto.conf` beizubehalten.

RHEL speichert die Datei `postgresql.conf` standardmäßig im PostgreSQL-Datenverzeichnis. Daher wurde die Änderung an `postgresql.conf` bei der letzten Wiederherstellung überschrieben, und die Einstellung hot_standby muss erneut aktiviert werden. Alternativ kann die Datei `postgresql.conf` an einem anderen Ort gespeichert oder hot_standby auf dem Host pg-primary aktiviert werden, wo die Einstellung ignoriert wird.

pg-standby:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** hot_standby aktivieren

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

hot_standby = on

log_filename = 'postgresql.log'
```

pg-standby **⇒** PostgreSQL starten

```bash
sudo systemctl start postgresql-14.service
```

Das PostgreSQL-Protokoll bestätigt den Start der Streaming-Replikation.

pg-standby **⇒** PostgreSQL-Protokollausgabe auf Erfolgsmeldungen prüfen

```bash
sudo -u postgres cat /var/lib/pgsql/14/data/log/postgresql.log
```

```text
       [filtered 12 lines of output]
LOG:  database system is ready to accept read-only connections
LOG:  restored log file "000000070000000000000026" from archive
LOG:  started streaming WAL from primary at 0/27000000 on timeline 7
```

Wenn nun auf pg-primary eine Tabelle erstellt wird, erscheint sie schnell auf pg-standby, ohne dass `pg_switch_wal()` aufgerufen werden muss.

pg-primary **⇒** Neue Tabelle auf dem Primärserver erstellen

```bash
sudo -u postgres psql -c " \
       begin; \
       create table stream_table (message text); \
       insert into stream_table values ('Important Data'); \
       commit; \
       select *, current_timestamp from stream_table";
```

```text
       [filtered 4 lines of output]
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.428653+00
(1 row)
```

pg-standby **⇒** Tabelle auf dem Standby abfragen

```bash
sudo -u postgres psql -c " \
       select *, current_timestamp from stream_table"
```

```text
    message     |       current_timestamp
----------------+-------------------------------
 Important Data | 2026-10-02 19:00:24.605628+00
(1 row)
```

--------

## Mehrere Stanzas {#multiple-stanzas}

pgBackRest unterstützt mehrere Stanzas. Am häufigsten wird dabei ein Repository-Host von mehreren Stanzas gemeinsam genutzt.

### Installation {#installation-3}

Ein neuer Host namens pg-alt wird für den Betrieb des neuen Primärservers eingerichtet.

Die Installation von pgBackRest aus einem Paket ist der Kompilierung aus dem Quellcode vorzuziehen. Bei einer Paketinstallation sind die übrigen Anweisungen in diesem Abschnitt normalerweise nicht erforderlich. Es kann jedoch vorkommen, dass ein Paket eines der Verzeichnisse nicht anlegt oder falsche Berechtigungen vergibt. In diesem Fall kann es erforderlich sein, Verzeichnisse manuell anzulegen oder Berechtigungen anzupassen.

RHEL-Pakete für pgBackRest sind unter [yum.postgresql.org](http://yum.postgresql.org) verfügbar.

Falls für Ihre Distribution oder Version keine Pakete bereitstehen, können Sie pgBackRest [aus dem Quellcode kompilieren](#build) und anschließend wie hier gezeigt manuell installieren.

pg-alt **⇒** Abhängigkeiten installieren

```bash
sudo yum install postgresql-libs libssh2
```

pg-alt **⇒** pgBackRest-Binärdatei vom Build-Host kopieren

```bash
sudo scp build:/build/pgbackrest/src/pgbackrest /usr/bin
sudo chmod 755 /usr/bin/pgbackrest
```

pgBackRest benötigt Protokoll- und Konfigurationsverzeichnisse sowie eine Konfigurationsdatei.

pg-alt **⇒** pgBackRest-Konfigurationsdatei und Verzeichnisse erstellen

```bash
sudo mkdir -p -m 770 /var/log/pgbackrest
sudo chown postgres:postgres /var/log/pgbackrest
sudo mkdir -p /etc/pgbackrest
sudo mkdir -p /etc/pgbackrest/conf.d
sudo touch /etc/pgbackrest/pgbackrest.conf
sudo chmod 640 /etc/pgbackrest/pgbackrest.conf
sudo chown postgres:postgres /etc/pgbackrest/pgbackrest.conf
```

### Konfiguration {#configuration-1}

Die pgBackRest-Konfiguration ist nahezu identisch mit der von pg-primary. Es wird jedoch die Stanza `demo-alt` verwendet, damit Backups und Archiv an einem getrennten Ort gespeichert werden.

pg-alt:`/etc/pgbackrest/pgbackrest.conf` **⇒** pgBackRest auf dem neuen Primärserver konfigurieren

```ini
[demo-alt]

pg1-path=/var/lib/pgsql/14/data



[global]

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

tls-server-address=*

tls-server-auth=pgbackrest-client=demo-alt

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-host`/`pg1-host-user` und `pg1-path` konfigurieren

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-alt **⇒** pgBackRest-Server einrichten

```bash
sudo cat /etc/systemd/system/pgbackrest.service
```

```text
[Unit]
Description=pgBackRest Server
After=network.target
StartLimitIntervalSec=0

[Service]
Type=notify
Restart=always
RestartSec=1
User=postgres
ExecStart=/usr/bin/pgbackrest server
ExecStartPost=/bin/sleep 3
ExecStartPost=/bin/bash -c "[ ! -z $MAINPID ]"
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pgbackrest
sudo systemctl start pgbackrest
```

### Demo-Cluster einrichten {#setup-demo-cluster-1}

pg-alt **⇒** Demo-Cluster erstellen

```bash
sudo -u postgres /usr/pgsql-14/bin/initdb \
       -D /var/lib/pgsql/14/data -k -A peer
```

pg-alt:`/var/lib/pgsql/14/data/postgresql.conf` **⇒** PostgreSQL-Einstellungen konfigurieren

```ini
archive_command = 'pgbackrest --stanza=demo-alt archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

pg-alt **⇒** Demo-Cluster starten

```bash
sudo systemctl restart postgresql-14.service
```

### Stanza erstellen und Konfiguration prüfen {#create-the-stanza-and-check-configuration}

Zum Initialisieren der Stanza muss der Befehl `stanza-create` ausgeführt werden. Es wird empfohlen, nach `stanza-create` den Befehl `check` auszuführen, um sicherzustellen, dass Archivierung und Backups korrekt konfiguriert sind.

pg-alt **⇒** Stanza erstellen und Konfiguration prüfen

```bash
sudo -u postgres pgbackrest --stanza=demo-alt --log-level-console=info stanza-create
```

```text
P00   INFO: stanza-create command begin 2.59.3: --exec-id=929-571b66d7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo-alt
P00   INFO: stanza-create for stanza 'demo-alt' on repo1
P00   INFO: stanza-create command end: completed successfully
```

```bash
sudo -u postgres pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=962-2cadc106 --log-level-console=info --log-level-file=detail --no-log-timestamp --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000001 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000001-5cb25be2e89d0324cc2a94cbc964295204118888.gz' on repo1
P00   INFO: check command end: completed successfully
```

Wird der Befehl `check` auf dem Repository-Host ausgeführt, werden alle Stanzas geprüft.

repository **⇒** Konfiguration aller Stanzas prüfen

```bash
sudo -u pgbackrest pgbackrest --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=1384-3bcda35c --log-level-console=info --no-log-timestamp --repo1-path=/var/lib/pgbackrest
P00   INFO: check stanza 'demo'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000070000000000000027 successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/000000070000000000000027-b36b790bcf0b1a9f54bc84458117feb77853d452.gz' on repo1
P00   INFO: check stanza 'demo-alt'
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 000000010000000000000002 successfully archived to '/var/lib/pgbackrest/archive/demo-alt/14-1/0000000100000000/000000010000000000000002-c303ffb17f8a111070459593520aa35640317a38.gz' on repo1
P00   INFO: check command end: completed successfully
```

--------

## Asynchrone Archivierung {#asynchronous-archiving}

Asynchrone Archivierung wird mit der Option `archive-async` aktiviert. Diese aktiviert den asynchronen Betrieb sowohl für `archive-push` als auch für `archive-get`.

Ein Spool-Pfad ist erforderlich. Die Befehle speichern dort vorübergehende Daten, arbeiten jedoch recht unterschiedlich. Daher wird die Verwendung des Spool-Pfads in den jeweiligen Abschnitten ausführlich beschrieben.

pg-primary **⇒** Spool-Verzeichnis erstellen

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

pg-standby **⇒** Spool-Verzeichnis erstellen

```bash
sudo mkdir -p -m 750 /var/spool/pgbackrest
sudo chown postgres:postgres /var/spool/pgbackrest
```

Der Spool-Pfad muss konfiguriert und die asynchrone Archivierung aktiviert werden. Schon die asynchrone Archivierung allein bringt Vorteile, weil sie die Zahl der Verbindungen zu entferntem Speicher verringert. Mit `process-max` kann die Leistung durch Parallelisierung der Vorgänge erheblich gesteigert werden. `process-max` darf dabei nicht so hoch gesetzt werden, dass der normale Datenbankbetrieb beeinträchtigt wird.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** Spool-Pfad und asynchrone Archivierung konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** Spool-Pfad und asynchrone Archivierung konfigurieren

```ini
[demo]

pg1-path=/var/lib/pgsql/14/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

HINWEIS:

`process-max` wird in Befehlsabschnitten konfiguriert, damit die Option nicht von backup und restore verwendet wird. Dies ermöglicht auch unterschiedliche Werte für `archive-push` und `archive-get`.

Zur Demonstration wird die Streaming-Replikation unterbrochen, um PostgreSQL zum Abruf von WAL über restore_command zu zwingen.

pg-primary **⇒** Streaming-Replikation durch Änderung des Replikationspassworts unterbrechen

```bash
sudo -u postgres psql -c "alter user replicator password 'bogus'"
```

```text
ALTER ROLE
```

pg-standby **⇒** Standby neu starten, um die Verbindung zu unterbrechen

```bash
sudo systemctl restart postgresql-14.service
```

### Archivübertragung {#archive-push}

Der asynchrone Befehl `archive-push` lagert die WAL-Archivierung in einen oder mehrere separate Prozesse aus, um den Durchsatz zu erhöhen. Er schaut gewissermaßen voraus und ermittelt, welche weiteren WAL-Segmente neben der aktuellen Anfrage von PostgreSQL über `archive_command` zur Archivierung bereitstehen. WAL-Segmente werden direkt aus dem Verzeichnis `pg_xlog`/`pg_wal` ins Archiv übertragen. `archive_command` meldet erst dann Erfolg, wenn das WAL-Segment sicher im Archiv gespeichert ist.

Der Spool-Pfad enthält den aktuellen Status der WAL-Archivierung. Die dort geschriebenen Statusdateien sind normalerweise leer und sollten nur minimalen Speicherplatz, höchstens einige MB, und sehr wenig IO beanspruchen. Alle Informationen in diesem Verzeichnis können neu erstellt werden. Bei einem Umzug des Clusters auf neue Hardware muss das Spool-Verzeichnis daher nicht aufbewahrt werden.

WICHTIG:

In der ursprünglichen Implementierung der asynchronen Archivierung wurden WAL-Segmente vor der Komprimierung und Übertragung in das Spool-Verzeichnis kopiert. Die neue Implementierung kopiert WAL direkt aus dem Verzeichnis `pg_xlog`. Wurde asynchrone Archivierung in v1.12 oder früher verwendet, vor dem Upgrade die Versionshinweise zu v1.13 sorgfältig lesen.

Mit der Datei `[stanza]-archive-push-async.log` lässt sich die Aktivität des asynchronen Prozesses überwachen. Ein guter Test ist die Übertragung mehrerer WAL-Segmente kurz hintereinander.

pg-primary **⇒** Parallele asynchrone Archivierung testen

```bash
sudo -u postgres psql -c " \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal(); \
       select pg_create_restore_point('test async push'); select pg_switch_wal();"
sudo -u postgres pgbackrest --stanza=demo --log-level-console=info check
```

```text
P00   INFO: check command begin 2.59.3: --exec-id=6864-e51531e7 --log-level-console=info --log-level-file=detail --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: check repo1 configuration (primary)
P00   INFO: check repo1 archive for WAL (primary)
P00   INFO: WAL segment 00000007000000000000002D successfully archived to '/var/lib/pgbackrest/archive/demo/14-1/0000000700000000/00000007000000000000002D-7addc4d9a1861c1b8b68300ea3a7db01fbe08ae2.gz' on repo1
P00   INFO: check command end: completed successfully
```

Die Protokolldatei enthält nun parallele, asynchrone Aktivitäten.

pg-primary **⇒** Ergebnisse im Protokoll prüfen

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-push-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6828-6cf1b924 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 1 WAL file(s) to archive: 000000070000000000000028
P01 DETAIL: pushed WAL file '000000070000000000000028' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully

-------------------PROCESS START-------------------
P00   INFO: archive-push:async command begin 2.59.3: [/var/lib/pgsql/14/data/pg_wal] --archive-async --exec-id=6866-2a936d60 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: push 5 WAL file(s) to archive: 000000070000000000000029...00000007000000000000002D
P02 DETAIL: pushed WAL file '00000007000000000000002A' to the archive
P01 DETAIL: pushed WAL file '000000070000000000000029' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002C' to the archive
P02 DETAIL: pushed WAL file '00000007000000000000002B' to the archive
P01 DETAIL: pushed WAL file '00000007000000000000002D' to the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
P00   INFO: archive-push:async command end: completed successfully
```

### Archivabruf {#archive-get}

Der asynchrone Befehl `archive-get` hält eine lokale WAL-Warteschlange vor, um den Durchsatz zu erhöhen. Fehlt ein WAL-Segment in der Warteschlange, wird es zusammen mit genügend nachfolgenden WAL-Segmenten zum Füllen der Warteschlange aus dem Repository abgerufen. Deren maximale Größe wird durch `archive-get-queue-max` festgelegt. Sobald die Warteschlange weniger als halb voll ist, wird weiteres WAL zum Auffüllen abgerufen.

Der asynchrone Betrieb ist besonders nützlich in Umgebungen, die viel WAL erzeugen oder eine Verbindung mit hoher Latenz zum Repository-Speicher haben, etwa zu S3 oder anderen Objektspeichern. Bei hoher Verbindungslatenz kann es sinnvoll sein, `process-max` zu erhöhen.

Mit der Datei `[stanza]-archive-get-async.log` lässt sich die Aktivität des asynchronen Prozesses überwachen.

pg-standby **⇒** Ergebnisse im Protokoll prüfen

```bash
sudo -u postgres cat /var/log/pgbackrest/demo-archive-get-async.log
```

```text
-------------------PROCESS START-------------------
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000024, 000000070000000000000025, 000000070000000000000026, 000000070000000000000027, 000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B] --archive-async --exec-id=1919-a90112cb --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000024...00000007000000000000002B
P01 DETAIL: found 000000070000000000000024 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000025 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000027 in the repo1: 14-1 archive
P01 DETAIL: found 000000070000000000000026 in the repo1: 14-1 archive
P00 DETAIL: unable to find 000000070000000000000028 in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 31 lines of output]
P00   INFO: archive-get:async command begin 2.59.3: [000000070000000000000028, 000000070000000000000029, 00000007000000000000002A, 00000007000000000000002B, 00000007000000000000002C, 00000007000000000000002D, 00000007000000000000002E, 00000007000000000000002F] --archive-async --exec-id=1976-2ef79408 --log-level-console=off --log-level-file=detail --log-level-stderr=off --no-log-timestamp --pg1-path=/var/lib/pgsql/14/data --process-max=2 --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --spool-path=/var/spool/pgbackrest --stanza=demo
P00   INFO: get 8 WAL file(s) from archive: 000000070000000000000028...00000007000000000000002F
P01 DETAIL: found 000000070000000000000028 in the repo1: 14-1 archive
P02 DETAIL: found 000000070000000000000029 in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002A in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002B in the repo1: 14-1 archive
P02 DETAIL: found 00000007000000000000002D in the repo1: 14-1 archive
P01 DETAIL: found 00000007000000000000002C in the repo1: 14-1 archive
P00 DETAIL: unable to find 00000007000000000000002E in the archive
P00 DETAIL: statistics: {"socket.client":{"total":1},"socket.session":{"total":1},"tls.client":{"total":1},"tls.session":{"total":1}}
       [filtered 14 lines of output]
```

pg-primary **⇒** Streaming-Replikation durch Änderung des Replikationspassworts reparieren

```bash
sudo -u postgres psql -c "alter user replicator password 'jw8s0F4'"
```

```text
ALTER ROLE
```

--------

## Backup von einem Standby {#backup-from-a-standby}

pgBackRest kann Backups auf einem Standby statt auf dem Primärserver durchführen. Dazu muss der Host pg-standby konfiguriert und die Option `backup-standby` aktiviert sein. Sind mehrere Standbys konfiguriert, wird der erste gefundene laufende Standby für das Backup verwendet.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg2-host`/`pg2-host-user` und `pg2-path` konfigurieren

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/14/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

Für das Backup werden sowohl die Datenbank auf dem Primärserver als auch die auf dem Standby benötigt. Der weitaus größte Teil der Dateien wird jedoch vom Standby kopiert, um den Primärserver zu entlasten. Die Datenbankhosts können in beliebiger Reihenfolge konfiguriert werden. pgBackRest erkennt automatisch, welcher Host der Primärserver und welcher der Standby ist.

repository **⇒** Backup des Demo-Clusters von pg2 erstellen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --log-level-console=detail backup
```

```text
       [filtered 2 lines of output]
P00   INFO: execute backup start: backup begins after the requested immediate checkpoint completes
P00   INFO: backup start archive = 00000007000000000000002F, lsn = 0/2F000028
P00   INFO: wait for replay on the standby to reach 0/2F000028
P00   INFO: replay on the standby reached 0/2F000028
P00   INFO: check archive for prior segment 00000007000000000000002E
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/log/postgresql.log (10.9KB, 0.42%) checksum dbfa988289c2ff32dcd198f19455165722870b43
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/global/pg_control (8KB, 0.73%) checksum 0a793efbb7bb2e255bbb2bfac8f612bc943c7f31
P01 DETAIL: backup file pg-primary:/var/lib/pgsql/14/data/pg_hba.conf (4.5KB, 0.90%) checksum cfa97af1dab1b130f0a921fa2d10d76fe0c5f630
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/current_logfiles (26B, 0.91%) checksum 78a9f5c10960f0d91fcd313937469824861795a2
P01 DETAIL: match file from prior backup pg-primary:/var/lib/pgsql/14/data/pg_logical/replorigin_checkpoint (8B, 0.91%) checksum 347fc8f2df71bd4436e38bd1516ccd7ea0d46532
       [filtered 1263 lines of output]
```

Dieses inkrementelle Backup zeigt, dass die meisten Dateien vom Host pg-standby und nur wenige vom Host pg-primary kopiert werden.

pgBackRest erstellt auf dem Standby ein Backup, das mit einem auf dem Primärserver durchgeführten Backup identisch ist. Dazu startet und beendet es das Backup auf dem Host pg-primary, kopiert die replizierten Dateien vom Host pg-standby und anschließend die wenigen übrigen Dateien von pg-primary. Damit enthält das Backup auch Protokolle und Statistiken der primären Datenbank.

--------

## Upgrade von PostgreSQL {#upgrading-postgresql}

Unmittelbar nach dem Upgrade von PostgreSQL auf eine neuere Hauptversion muss `pg-path` in allen pgBackRest-Konfigurationen auf den neuen Datenbankspeicherort gesetzt und der Befehl `stanza-upgrade` ausgeführt werden. Sind auf dem Host mehrere Repositorys konfiguriert, wird die Stanza in jedem davon aktualisiert. Ist die Datenbank offline, die Option `--no-online` verwenden.

Die folgenden Anweisungen sind keine umfassende Anleitung zum Upgrade von PostgreSQL. Sie skizzieren den allgemeinen Ablauf für ein Upgrade von Primärserver und Standby, um die zur Neukonfiguration von pgBackRest erforderlichen Schritte zu zeigen. Vor dem Upgrade wird ein Backup empfohlen.

pg-primary **⇒** Alten Cluster stoppen

```bash
sudo systemctl stop postgresql-14.service
```

Den alten Cluster auf dem Standby stoppen, da er aus dem gerade aktualisierten Cluster wiederhergestellt wird.

pg-standby **⇒** Alten Cluster stoppen

```bash
sudo systemctl stop postgresql-14.service
```

Den neuen Cluster erstellen und das Upgrade durchführen.

pg-primary **⇒** Neuen Cluster erstellen und Upgrade durchführen

```bash
sudo -u postgres /usr/pgsql-15/bin/initdb \
       -D /var/lib/pgsql/15/data -k -A peer
sudo -u postgres sh -c 'cd /var/lib/pgsql && \
       /usr/pgsql-15/bin/pg_upgrade \
       --old-bindir=/usr/pgsql-14/bin \
       --new-bindir=/usr/pgsql-15/bin \
       --old-datadir=/var/lib/pgsql/14/data \
       --new-datadir=/var/lib/pgsql/15/data \
       --old-options=" -c config_file=/var/lib/pgsql/14/data/postgresql.conf" \
       --new-options=" -c config_file=/var/lib/pgsql/15/data/postgresql.conf"'
```

```text
       [filtered 41 lines of output]
Checking for extension updates                              ok
Upgrade Complete
----------------
Optimizer statistics are not transferred by pg_upgrade.
       [filtered 4 lines of output]
```

Die Einstellungen und den Port des neuen Clusters konfigurieren.

pg-primary:`/var/lib/pgsql/15/data/postgresql.conf` **⇒** PostgreSQL konfigurieren

```ini
archive_command = 'pgbackrest --stanza=demo archive-push %p'

archive_mode = on

log_filename = 'postgresql.log'
```

Die pgBackRest-Konfiguration auf allen Systemen so anpassen, dass sie auf den neuen Cluster verweist.

pg-primary:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-path` aktualisieren

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

pg-standby:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg-path` aktualisieren

```ini
[demo]

pg1-path=/var/lib/pgsql/15/data

recovery-option=primary_conninfo=host=172.17.0.6 port=5432 user=replicator



[global]

archive-async=y

log-level-file=detail

repo1-host=repository

repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt

repo1-host-cert-file=/etc/pgbackrest/cert/client.crt

repo1-host-key-file=/etc/pgbackrest/cert/client.key

repo1-host-type=tls

spool-path=/var/spool/pgbackrest

tls-server-address=*

tls-server-auth=pgbackrest-client=demo

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key



[global:archive-get]

process-max=2



[global:archive-push]

process-max=2
```

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** `pg1-path` und `pg2-path` aktualisieren und Backup vom Standby deaktivieren

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=n

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```

pg-primary **⇒** hba-Konfiguration kopieren

```bash
sudo cp /var/lib/pgsql/14/data/pg_hba.conf \
       /var/lib/pgsql/15/data/pg_hba.conf
```

Vor dem Start des neuen Clusters muss der Befehl `stanza-upgrade` ausgeführt werden.

pg-primary **⇒** Stanza aktualisieren

```bash
sudo -u postgres pgbackrest --stanza=demo --no-online \
       --log-level-console=info stanza-upgrade
```

```text
P00   INFO: stanza-upgrade command begin 2.59.3: --exec-id=7454-62cfb155 --log-level-console=info --log-level-file=detail --no-log-timestamp --no-online --pg1-path=/var/lib/pgsql/15/data --repo1-host=repository --repo1-host-ca-file=/etc/pgbackrest/cert/ca.crt --repo1-host-cert-file=/etc/pgbackrest/cert/client.crt --repo1-host-key-file=/etc/pgbackrest/cert/client.key --repo1-host-type=tls --stanza=demo
P00   INFO: stanza-upgrade for stanza 'demo' on repo1
P00   INFO: stanza-upgrade command end: completed successfully
```

Den neuen Cluster starten und den Erfolg der Installation prüfen.

pg-primary **⇒** Neuen Cluster starten

```bash
sudo systemctl start postgresql-15.service
```

Die Konfiguration mit dem Befehl `check` testen.

pg-primary **⇒** Konfiguration prüfen

```bash
sudo systemctl status postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

Den alten Cluster entfernen.

pg-primary **⇒** Alten Cluster entfernen

```bash
sudo rm -rf /var/lib/pgsql/14/data
```

Die neuen PostgreSQL-Binärdateien auf dem Standby installieren und den Cluster erstellen.

pg-standby **⇒** Alten Cluster entfernen und neuen Cluster erstellen

```bash
sudo rm -rf /var/lib/pgsql/14/data
sudo -u postgres mkdir -p -m 700 /usr/pgsql-15/bin
```

`check` auf dem Repository-Host ausführen. Die Warnung zum nicht verfügbaren Standby ist zu erwarten, da der Standby-Cluster gestoppt ist. Die Ausführung zeigt, dass der Repository-Server den Standby kennt und für den Primärserver korrekt konfiguriert ist.

repository **⇒** Konfiguration prüfen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo check
```

```text
P00   WARN: unable to check pg2: [DbConnectError] raised from remote-0 tls protocol on 'pg-standby': unable to connect to 'dbname='postgres' port=5432': connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
                Is the server running locally and accepting connections on that socket?
```

Ein vollständiges Backup des neuen Clusters durchführen und anschließend den Standby daraus wiederherstellen. Wird `incr` oder `diff` angefordert, wird der Backup-Typ automatisch auf `full` geändert.

repository **⇒** Vollständiges Backup durchführen

```bash
sudo -u pgbackrest pgbackrest --stanza=demo --type=full backup
```

pg-standby **⇒** Demo-Standby-Cluster wiederherstellen

```bash
sudo -u postgres pgbackrest --stanza=demo --type=standby restore
```

pg-standby **⇒** PostgreSQL starten und pgBackRest-Konfiguration prüfen

```bash
sudo systemctl start postgresql-15.service
sudo -u postgres pgbackrest --stanza=demo check
```

Nach der Wiederherstellung des Standbys kann das Backup vom Standby aktiviert werden.

repository:`/etc/pgbackrest/pgbackrest.conf` **⇒** Backup vom Standby wieder aktivieren

```ini
[demo]

pg1-host=pg-primary

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/15/data

pg2-host=pg-standby

pg2-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg2-host-cert-file=/etc/pgbackrest/cert/client.crt

pg2-host-key-file=/etc/pgbackrest/cert/client.key

pg2-host-type=tls

pg2-path=/var/lib/pgsql/15/data



[demo-alt]

pg1-host=pg-alt

pg1-host-ca-file=/etc/pgbackrest/cert/ca.crt

pg1-host-cert-file=/etc/pgbackrest/cert/client.crt

pg1-host-key-file=/etc/pgbackrest/cert/client.key

pg1-host-type=tls

pg1-path=/var/lib/pgsql/14/data



[global]

backup-standby=y

process-max=3

repo1-path=/var/lib/pgbackrest

repo1-retention-full=2

start-fast=y

tls-server-address=*

tls-server-auth=pgbackrest-client=*

tls-server-ca-file=/etc/pgbackrest/cert/ca.crt

tls-server-cert-file=/etc/pgbackrest/cert/server.crt

tls-server-key-file=/etc/pgbackrest/cert/server.key
```
