---
title: "Referenz zur Konfiguration"
linkTitle: "Konfiguration"
weight: 50
description: "Vollständige pgBackRest-Konfigurationsreferenz mit allen Einstellungen, einschließlich Optionen für Archivierung, Backups, Repositorys und Cloud-Speicher."
icon: fa-solid fa-code
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/configuration.html"
---

--------

## Einführung {#introduction}

pgBackRest lässt sich vollständig über Befehlszeilenparameter steuern. Für komplexe Installationen oder viele Optionen ist jedoch eine Konfigurationsdatei praktischer. Ihr standardmäßiger Pfad ist `/etc/pgbackrest/pgbackrest.conf`. Existiert dort keine Datei, wird der frühere Standardpfad `/etc/pgbackrest.conf` geprüft.

Die folgenden Optionentypen werden verwendet:

**Zeichenfolge**: Text, häufig eine Kennung, ein Passwort oder Ähnliches.

Beispiel für die Befehlszeile: `--stanza=demo`<br/>Beispiel für die Konfigurationsdatei: `repo1-cipher-pass=zWaf6XtpjIVZC5444yXB...`

**Pfad**: Identifiziert einen Speicherort in einer Verzeichnisstruktur eindeutig. Pfade müssen mit / beginnen. Doppeltes // ist nicht erlaubt, und ein abschließendes / wird nicht erwartet.

Beispiel für die Befehlszeile: `--repo1-path=/var/lib/pgbackrest`<br/>Beispiel für die Konfigurationsdatei: `repo1-path=/var/lib/pgbackrest`

**Boolescher Wert**: Aktiviert oder deaktiviert die Option. Nur y/n sind als Argumentwerte zulässig.

Beispiele für die Befehlszeile: `--start-fast`, `--no-start-fast`, `--start-fast=y`, `--start-fast=n`<br/>Beispiele für die Konfigurationsdatei: `start-fast=y`, `start-fast=n`

**Ganzzahl**: Für Ports, Aufbewahrungsanzahlen, Wiederholungsversuche, die Anzahl zulässiger paralleler Prozesse und Ähnliches.

Beispiel für die Befehlszeile: `--compress-level=3`<br/>Beispiel für die Konfigurationsdatei: `pg1-port=5432`

**Größe**: Für Puffergrößen, Speicherplatzbedarf und Ähnliches. Größen können in Byte (Standard) oder in KiB, MiB, GiB, TiB oder PiB angegeben werden; der Multiplikator ist jeweils eine Potenz von 1024. Beispielsweise kann statt 5368709120 der Wert 5GiB (oder 5GB, 5g) verwendet werden, wobei Groß- und Kleinschreibung keine Rolle spielen. Bruchwerte wie 2.5GiB sind nicht zulässig; stattdessen 2560MiB verwenden.

Beispiel für die Befehlszeile: `--archive-get-queue-max=1GiB`<br/>Beispiel für die Konfigurationsdatei: `buffer-size=2MiB`

**Zeit**: Zeit in Sekunden.

Beispiel für die Befehlszeile: `--io-timeout=90`<br/>Beispiel für die Konfigurationsdatei: `db-timeout=600`

**Liste**: Die Option kann mehrfach angegeben werden.

Beispiel für die Befehlszeile: `--db-exclude=db1 --db-exclude=db2 --db-exclude=db5`

Beispiel für die Konfigurationsdatei, jeweils in einer eigenen Zeile:

```ini
db-exclude=db1
db-exclude=db2
db-exclude=db5
```

**Schlüssel/Wert**: Die Option kann mehrfach in der Form `key=value` angegeben werden.

Beispiel für die Befehlszeile: `--tablespace-map=ts_01=/db/ts_01 --tablespace-map=ts_02=/db/ts_02`

Beispiel für die Konfigurationsdatei, jeweils in einer eigenen Zeile:

```ini
tablespace-map=ts_01=/db/ts_01
tablespace-map=ts_02=/db/ts_02
```

--------

## Archivierungsoptionen {#archive-options}

Der Abschnitt `archive` definiert Optionen für die Befehle `archive-push` und `archive-get`.

### Option für asynchrone Archivierung (`--archive-async`) {#asynchronous-archiving-option---archive-async}

WAL-Segmente asynchron übertragen und abrufen.

Aktiviert den asynchronen Betrieb für die Befehle `archive-push` und `archive-get`.

Der asynchrone Betrieb ist effizienter, da er Verbindungen wiederverwenden und parallele Verarbeitung nutzen kann. Weitere Informationen bieten die Optionen `spool-path`, `archive-get-queue-max` und `archive-push-queue-max`.

```text
default: n
example: archive-async=y
```

### Option für die maximale Größe der Abrufwarteschlange (`--archive-get-queue-max`) {#maximum-archive-get-queue-size-option---archive-get-queue-max}

Maximale Größe der archive-get-Warteschlange von pgBackRest.

Legt die maximale Größe der `archive-get`-Warteschlange fest, wenn `archive-async` aktiviert ist. Die Warteschlange liegt im `spool-path` und beschleunigt die Bereitstellung von WAL für PostgreSQL.

```text
default: 128MiB
allowed: [0B, 4PiB]
example: archive-get-queue-max=1GiB
```

### Option zum erneuten Abruf fehlender WAL-Segmente (`--archive-missing-retry`) {#retry-missing-wal-segment-option---archive-missing-retry}

Abruf fehlender WAL-Segmente erneut versuchen

Ein WAL-Segment erneut abrufen, das der Befehl `archive-get` im asynchronen Modus zuvor als fehlend gemeldet hat. Dies verhindert, dass Meldungen einer früheren Wiederherstellung aus dem Spool-Pfad verwendet werden und möglicherweise die Recovery scheitern lassen, wenn noch kein konsistenter Zustand erreicht wurde.

Bei deaktivierter Option kann PostgreSQL zuverlässiger erkennen, wann das Ende des WAL im Archiv erreicht ist, und dann zum Streaming vom Primärserver wechseln. Bei aktivierten Wiederholungsversuchen führt ein stetiger Strom neu archivierter WAL-Segmente dazu, dass PostgreSQL weiterhin WAL aus dem Archiv abruft, statt zum Streaming zu wechseln.

Wird diese Option deaktiviert, muss sichergestellt werden, dass der Spool-Pfad der Stanza leer ist. Der Befehl `restore` erledigt dies automatisch, wenn der Spool-Pfad zum Zeitpunkt der Wiederherstellung konfiguriert ist. Andernfalls muss der Benutzer selbst dafür sorgen, dass der Spool-Pfad leer ist.

```text
default: y
example: archive-missing-retry=n
```

### Option für die Datenmenge pro Archivierungslauf (`--archive-push-batch-size`) {#archive-push-batch-size-option---archive-push-batch-size}

Maximale WAL-Menge, die pro asynchronem Lauf übertragen wird.

Im asynchronen Modus überträgt der Prozess `archive-push` alle bereitstehenden WAL-Segmente in einem Lauf. Da `archive-push-queue-max` nur zu Beginn jedes Laufs geprüft wird, kann die Warteschlange bei einem Lauf mit sehr vielen Segmenten weit über den Grenzwert hinaus wachsen, bevor sie erneut geprüft wird.

Diese Option begrenzt die pro Lauf verarbeitete WAL-Menge. Der Prozess beendet sich dadurch und wird beim nächsten `archive-push` neu gestartet, wobei die Warteschlange erneut geprüft wird. Kleinere Werte führen zu häufigeren Prüfungen, erfordern aber auch häufigere Starts des asynchronen Prozesses. Der Wert wird auf eine ganze Anzahl von WAL-Segmenten abgerundet; mindestens ein Segment wird jedoch immer verarbeitet.

```text
default: 16GiB
allowed: [1MiB, 4PiB]
example: archive-push-batch-size=1GiB
```

### Option für die maximale Größe der Archivierungswarteschlange (`--archive-push-queue-max`) {#maximum-archive-push-queue-size-option---archive-push-queue-max}

Maximale Größe der PostgreSQL-Archivierungswarteschlange.

Nach Erreichen des Grenzwerts geschieht Folgendes:

- pgBackRest meldet PostgreSQL, dass das WAL erfolgreich archiviert wurde, und wird es dann **VERWERFEN**.
- Eine Warnung wird in das PostgreSQL-Protokoll geschrieben.

Dadurch wird der Archivprotokollstrom unterbrochen, und PITR ist über diesen Punkt hinaus nicht mehr möglich. Ein neues Backup ist erforderlich, um die vollständige Wiederherstellbarkeit erneut herzustellen.

Im asynchronen Modus wird die gesamte Warteschlange verworfen. So wird verhindert, dass kurzzeitig wieder einzelne WAL-Segmente archiviert werden, bevor die Grenze erneut überschritten wird.

Im asynchronen Modus wird diese Grenze nur zu Beginn jedes `archive-push`-Laufs geprüft. Daher kann die Warteschlange innerhalb eines Laufs darüber hinaus wachsen. `archive-push-batch-size` verringern, um die Warteschlange häufiger zu prüfen.

Diese Funktion soll verhindern, dass das Volume mit den Protokolldateien voll wird, da PostgreSQL dann vollständig zum Stillstand kommt. Es ist besser, das Backup zu verlieren, als PostgreSQL ausfallen zu lassen.

```text
allowed: [0B, 4PiB]
example: archive-push-queue-max=1TiB
```

Veralteter Name: archive-queue-max

### Option für das Archivierungszeitlimit (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

Archivierungszeitlimit.

Maximale Wartezeit in Sekunden festlegen, bis ein einzelnes WAL-Segment das Archiv-Repository von pgBackRest erreicht. Dieses Zeitlimit gilt für die Befehle `check` und `backup`, wenn sie auf die Archivierung der WAL-Segmente warten, die für ein konsistentes Backup erforderlich sind.

```text
default: 1m
allowed: [100ms, 1d]
example: archive-timeout=30
```

--------

## Backup-Optionen {#backup-options}

Der Abschnitt `backup` definiert Einstellungen für Backups.

### Option für Backup-Anmerkungen (`--annotation`) {#backup-annotation-option---annotation}

Das Backup mit benutzerdefinierten Schlüssel/Wert-Paaren versehen.

Benutzer können dem Backup informative Schlüssel/Wert-Paare hinzufügen. Diese Option kann mehrfach verwendet werden, um mehrere Anmerkungen hinzuzufügen.

Anmerkungen erscheinen in der Textausgabe des Befehls `info`, wenn mit `--set` ein Backup angegeben wird. In der JSON-Ausgabe erscheinen sie immer.

```text
example: annotation=source="Sunday backup for website database"
```

### Option zur Archivprüfung (`--archive-check`) {#check-archive-option---archive-check}

Vor Abschluss des Backups prüfen, ob sich die WAL-Segmente im Archiv befinden.

Prüft, ob alle für ein konsistentes Backup erforderlichen WAL-Segmente im WAL-Archiv vorhanden sind. Es empfiehlt sich, die Standardeinstellung beizubehalten, sofern keine andere Archivierungsmethode verwendet wird.

Diese Option muss aktiviert sein, wenn `archive-copy` aktiviert ist.

```text
default: y
example: archive-check=n
```

### Option zum Kopieren des Archivs (`--archive-copy`) {#copy-archive-option---archive-copy}

Für die Konsistenz benötigte WAL-Segmente in das Backup kopieren.

Diese etwas übervorsichtige Option schützt vor beschädigten Daten im WAL-Segmentarchiv, indem sie die für die Konsistenz erforderlichen WAL-Segmente direkt im Backup speichert. Die WAL-Segmente bleiben zusätzlich im Archiv gespeichert, daher benötigt diese Option weiteren Speicherplatz.

Bei Verwendung dieser Option sollten die Befehle `archive-push` und `backup` möglichst denselben Wert für `compress-type` verwenden (z. B. `lz4`). Andernfalls müssen die WAL-Segmente mit dem für das Backup verwendeten `compress-type` neu komprimiert werden. Je nach der während des Backups erzeugten WAL-Menge kann dies recht aufwendig sein.

Bei der Wiederherstellung liegen die WAL-Segmente in `pg_xlog/pg_wal`. PostgreSQL bevorzugt diese Segmente gegenüber einem Aufruf von `restore_command`.

Die Option `archive-check` muss aktiviert sein, wenn `archive-copy` aktiviert ist.

```text
default: n
example: archive-copy=y
```

### Option zur Prüfung des Archivierungsmodus (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

Die PostgreSQL-Einstellung `archive_mode` prüfen.

Diese standardmäßig aktivierte Option verbietet die PostgreSQL-Einstellung `archive_mode=always`.

Von einem Standby-Server übertragene WAL-Segmente können logisch mit denen des Primärservers übereinstimmen, aber andere Prüfsummen aufweisen. Zur Vermeidung von Konflikten wird empfohlen, die Archivierung aus mehreren Quellen zu unterbinden.

ACHTUNG:

Bei deaktivierter Option muss unbedingt sichergestellt werden, dass nur ein Archivierer mit dem Befehl `archive-push` in das Repository schreibt.

```text
default: y
example: archive-mode-check=n
```

### Option für Backups vom Standby (`--backup-standby`) {#backup-from-standby-option---backup-standby}

Backup vom Standby-Cluster erstellen.

Backups vom Standby aktivieren, um die Last auf dem Primärcluster zu verringern. Für diese Option müssen sowohl der Primär- als auch der Standby-Host konfiguriert sein.

Die folgenden Modi werden unterstützt:

- `y` - Für das Backup ist ein Standby erforderlich.
- `prefer` - Backup vom Standby erstellen, falls verfügbar, andernfalls vom Primärserver.
- `n` - Backup ausschließlich vom Primärserver erstellen.

```text
default: n
example: backup-standby=y
```

### Option für Seitenprüfsummen (`--checksum-page`) {#page-checksums-option---checksum-page}

Prüfsummen der Datenseiten validieren.

Weist pgBackRest an, beim Backup eines Clusters die Prüfsummen aller Datenseiten zu validieren. Diese Option wird automatisch aktiviert, wenn Datenseitenprüfsummen im Cluster aktiviert sind.

Fehler bei der Prüfsummenvalidierung brechen das Backup nicht ab. Stattdessen werden Warnungen ins Protokoll geschrieben und bei Standardeinstellungen auch auf der Konsole ausgegeben. Die Liste der ungültigen Seiten wird im Backup-Manifest gespeichert.

```text
example: checksum-page=n
```

### Option zum Ausschließen von Pfaden und Dateien (`--exclude`) {#pathfile-exclusions-option---exclude}

Pfade und Dateien vom Backup ausschließen.

Alle Ausschlüsse beziehen sich auf `$PGDATA`. Endet der Ausschluss mit /, werden nur Dateien im angegebenen Verzeichnis ausgeschlossen. Beispielsweise schließt `--exclude=junk/` alle Dateien im Verzeichnis `$PGDATA/junk` aus, nimmt aber das Verzeichnis selbst auf. Endet der Ausschluss nicht mit /, kann eine Datei entweder genau dem Ausschluss entsprechen oder dem Ausschluss mit angehängtem /. So schließt `--exclude=junk` das Verzeichnis `$PGDATA/junk` und alle darin enthaltenen Dateien aus.

**Diese Funktion mit Vorsicht verwenden: Wichtige Inhalte lassen sich leicht versehentlich ausschließen, wodurch das Backup inkonsistent wird. Testen Sie unbedingt Ihre Wiederherstellungen!**

Alle ausgeschlossenen Dateien werden zusammen mit der Ausschlussregel auf der Stufe `info` protokolliert. Prüfen Sie unbedingt die Liste, damit keine Dateien unerwartet ausgeschlossen werden.

HINWEIS:

Ausschlüsse werden bei Delta-Wiederherstellungen nicht berücksichtigt. Alle beim Backup ausgeschlossenen Dateien und Verzeichnisse werden bei einer Delta-Wiederherstellung *entfernt*.

Diese Option sollte nicht verwendet werden, um PostgreSQL-Protokolle vom Backup auszuschließen. Mit der PostgreSQL-Einstellung `log_directory` lassen sich Protokolle außerhalb des Verzeichnisses `PGDATA` ablegen. Dies hat den Vorteil, dass sie nach einer Wiederherstellung erhalten bleiben können.

In der Befehlszeile oder einer Konfigurationsdatei können mehrere Ausschlüsse angegeben werden.

```text
example: exclude=junk/
```

### Option zur automatischen Bereinigung (`--expire-auto`) {#expire-auto-option---expire-auto}

Nach einem erfolgreichen Backup automatisch den Befehl `expire` ausführen.

Diese Einstellung ist standardmäßig aktiviert. Beim Deaktivieren ist Vorsicht geboten: Alle Backups und Archive bleiben dann unbegrenzt erhalten, wodurch der Speicherplatz im Repository ausgehen kann. Um dies zu verhindern, muss der Befehl `expire` regelmäßig ausgeführt werden.

Wird `expire` nach einem erfolgreichen Backup automatisch ausgeführt, verwendet es die Konfiguration des Befehls `backup`. Optionen, die ausschließlich in einem Abschnitt für den Befehl `expire` stehen, etwa `[global:expire]`, werden daher nicht angewendet. Um eine eigene Konfiguration für `expire` anzuwenden, diese Option deaktivieren und den Befehl `expire` separat ausführen.

```text
default: y
example: expire-auto=y
```

### Option für den Schwellenwert zum Speichern des Manifests (`--manifest-save-threshold`) {#manifest-save-threshold-option---manifest-save-threshold}

Schwellenwert zum Speichern des Manifests während des Backups.

Legt fest, wie oft das Manifest während eines Backups gespeichert wird. Das Speichern ist wichtig, da das Manifest Prüfsummen enthält und eine effiziente Wiederaufnahme ermöglicht. Der tatsächlich verwendete Schwellenwert ist der größere Wert aus 1% der Backup-Größe und `manifest-save-threshold`.

```text
default: 1GiB
allowed: [1B, 1TiB]
example: manifest-save-threshold=8GiB
```

### Option zur Wiederaufnahme (`--resume`) {#resume-option---resume}

Die Wiederaufnahme eines fehlgeschlagenen Backups erlauben.

Legt fest, ob die Wiederaufnahme aktiviert ist. Sie kann die benötigte Zeit erheblich verkürzen, wenn zuvor ein Backup desselben Typs fehlgeschlagen ist. Sie erhöht jedoch die Komplexität. In Umgebungen, die diese Funktion nicht benötigen, kann es daher sinnvoll sein, sie zu deaktivieren.

```text
default: y
example: resume=n
```

### Option für einen schnellen Start (`--start-fast`) {#start-fast-option---start-fast}

Einen Checkpoint erzwingen, um das Backup schnell zu starten.

Erzwingt einen Checkpoint, indem dem Parameter `fast` der Backup-Startfunktion der Wert `y` übergeben wird, sodass das Backup sofort beginnt. Andernfalls beginnt es nach dem nächsten regulären Checkpoint.

```text
default: n
example: start-fast=y
```

--------

## Allgemeine Optionen {#general-options}

Der Abschnitt `general` definiert Optionen, die mehrere Befehle gemeinsam verwenden.

### Option zur Ausführung als root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Die Ausführung des Befehls als Benutzer root erlauben.

Standardmäßig darf nur der Befehl `restore` als Benutzer root ausgeführt werden, da er die Dateieigentümer sorgfältig verwaltet. Bei anderen Befehlen besteht das Risiko, dass Dateien entstehen, die root gehören, etwa im Repository. Diese sind für den PostgreSQL-Benutzer nicht zugänglich, sodass spätere Befehle fehlschlagen.

Diese Option aktivieren, um einen Befehl dennoch als root auszuführen. Es ist jedoch deutlich besser, pgBackRest als den Benutzer auszuführen, dem das Repository und der PostgreSQL-Cluster gehören.

```text
default: n
example: allow-root=y
```

### Option für die Puffergröße (`--buffer-size`) {#buffer-size-option---buffer-size}

Puffergröße für I/O-Operationen.

Puffergröße für Kopier-, Komprimierungs-, Verschlüsselungs- und andere Operationen. Die Anzahl der verwendeten Puffer hängt von den Optionen ab. Jede Operation kann zusätzlichen Speicher benötigen; beispielsweise kann die Komprimierung mit `gz` weitere 256KiB Speicher beanspruchen.

Zulässige Werte sind `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` und `16MiB`.

```text
default: 1MiB
example: buffer-size=2MiB
```

### Option für den pgBackRest-Befehl (`--cmd`) {#pgbackrest-command-option---cmd}

pgBackRest-Befehl.

pgBackRest kann eine Befehlszeichenfolge erzeugen, etwa wenn der Befehl `restore` die Einstellung restore_command erzeugt. Dafür wird der Befehl verwendet, mit dem der pgBackRest-Prozess gestartet wurde, sofern nicht die Option `cmd` angegeben ist.

ACHTUNG:

Das Einbetten des pgBackRest-Befehls in einen Wrapper kann unvorhersehbares Verhalten verursachen und wird nicht empfohlen.

```text
default: [path of executed pgbackrest binary]
example: cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### Option für den SSH-Client-Befehl (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

SSH-Client-Befehl.

Einen bestimmten SSH-Client-Befehl verwenden, wenn eine Alternative gewünscht wird oder der Befehl `ssh` nicht in $PATH liegt.

```text
default: ssh
example: cmd-ssh=/usr/bin/ssh
```

### Option zur Komprimierung (`--compress`) {#compress-option---compress}

Dateikomprimierung verwenden.

Die Backup-Dateien sind mit Komprimierungswerkzeugen für die Befehlszeile kompatibel.

Diese Option ist inzwischen veraltet. Stattdessen sollte `compress-type` verwendet werden.

```text
default: y
example: compress=n
```

### Option für die Komprimierungsstufe (`--compress-level`) {#compress-level-option---compress-level}

Komprimierungsstufe für Dateien.

Legt die Stufe für die Dateikomprimierung fest, wenn `compress-type` nicht `none` ist oder `compress=y` (veraltet) gilt.

```text
default (depending on compress-type):
    bz2 - 9
    gz - 6
    lz4 - 1
    zst - 3

allow range (depending on compress-type):
    bz2 - [1, 9]
    gz - [-1, 9]
    lz4 - [-5, 12]
    zst - [-7, 22]

example: compress-level=9
```

### Option für die Netzwerkkomprimierungsstufe (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Komprimierungsstufe für die Netzwerkübertragung.

Legt die Komprimierungsstufe für die Netzwerkübertragung fest, wenn `compress-type=none` gilt und der Befehl nicht auf demselben Host wie das Repository ausgeführt wird. Die Komprimierung verringert den Netzwerkverkehr. Wenn `compress-type` nicht `none` ist, wird `compress-level-network` ignoriert und stattdessen `compress-level` verwendet, damit die Datei nur einmal komprimiert wird.

```text
default: 1
allowed: [-5, 12]
example: compress-level-network=1
```

### Option für das Komprimierungsverfahren (`--compress-type`) {#compress-type-option---compress-type}

Komprimierungsverfahren für Dateien.

Die folgenden Komprimierungsverfahren werden unterstützt:

- `none` - Keine Komprimierung
- `bz2` - bzip2-Komprimierungsformat
- `gz` - gzip-Komprimierungsformat
- `lz4` - lz4-Komprimierungsformat (nicht auf allen Plattformen verfügbar)
- `zst` - Zstandard-Komprimierungsformat (nicht auf allen Plattformen verfügbar)

```text
default: gz
example: compress-type=none
```

### Option für das Datenbankzeitlimit (`--db-timeout`) {#database-timeout-option---db-timeout}

Zeitlimit für Datenbankabfragen.

Legt das Zeitlimit für Datenbankabfragen in Sekunden fest. Dazu gehören auch die Funktionen zum Starten und Stoppen des Backups, die jeweils viel Zeit benötigen können. Daher sollte das Zeitlimit hoch bleiben, sofern nicht bekannt ist, dass diese Funktionen schnell zurückkehren, etwa wenn `start-fast=y` gesetzt ist und bekannt ist, dass der Datenbankcluster während des Backups nur wenige WAL-Segmente erzeugt.

HINWEIS:

Der Wert von `db-timeout` muss kleiner sein als der von `protocol-timeout`.

```text
default: 30m
allowed: [100ms, 7d]
example: db-timeout=600
```

### Delta-Option (`--delta`) {#delta-option---delta}

Wiederherstellung oder Backup anhand von Prüfsummen durchführen.

Bei einer Wiederherstellung wird standardmäßig erwartet, dass die PostgreSQL-Daten- und Tablespace-Verzeichnisse vorhanden, aber leer sind. Diese Option führt eine Delta-Wiederherstellung anhand von Prüfsummen durch.

Bei einem Backup verwendet diese Option Prüfsummen anstelle von Zeitstempeln, um zu entscheiden, ob Dateien kopiert werden.

```text
default: n
example: delta=y
```

### Option für das I/O-Zeitlimit (`--io-timeout`) {#io-timeout-option---io-timeout}

I/O-Zeitlimit.

Zeitlimit in Sekunden für Verbindungen sowie Lese- und Schreiboperationen.

Die gesamte Lese- oder Schreiboperation muss nicht innerhalb dieses Zeitlimits abgeschlossen sein, aber es muss *irgendein* Fortschritt erzielt werden, selbst wenn es nur ein einziges Byte ist.

```text
default: 1m
allowed: [100ms, 1h]
example: io-timeout=120
```

### Option für den Sperrdateipfad (`--lock-path`) {#lock-path-option---lock-path}

Pfad zum Speichern der Sperrdateien.

In diesem Pfad erstellt pgBackRest Sperrdateien, um die gleichzeitige Ausführung miteinander in Konflikt stehender Operationen zu verhindern.

```text
default: /tmp/pgbackrest
example: lock-path=/backup/db/lock
```

### Option für eine neutrale umask (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Eine neutrale umask verwenden.

Setzt die umask auf 0000, damit die Zugriffsrechte im Repository sinnvoll gesetzt werden. Standardmäßig erhalten Verzeichnisse den Modus 0750 und Dateien den Modus 0640.

Um stattdessen die umask des ausführenden Benutzers zu verwenden, `neutral-umask=n` in der Konfigurationsdatei oder `--no-neutral-umask` in der Befehlszeile angeben.

```text
default: y
example: neutral-umask=n
```

### Option für die Prozesspriorität (`--priority`) {#set-process-priority-option---priority}

Prozesspriorität festlegen.

Legt fest, welche Priorität (also welcher nice-Wert) dem Prozess vom Kernel-Scheduler zugewiesen wird. Positive Werte verringern die Priorität, negative Werte erhöhen sie. In den meisten Fällen dürfen Prozesse ihre Priorität nicht erhöhen.

```text
allowed: [-20, 19]
example: priority=19
```

### Option für die maximale Prozessanzahl (`--process-max`) {#process-maximum-option---process-max}

Maximale Anzahl der Prozesse für Komprimierung und Übertragung.

Jeder Prozess führt Komprimierung und Übertragung aus, um den Befehl zu beschleunigen. `process-max` jedoch nicht so hoch setzen, dass die Datenbankleistung beeinträchtigt wird.

```text
default: 1
allowed: [1, 999]
example: process-max=4
```

### Option für das Protokollzeitlimit (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Protokollzeitlimit.

Legt in Sekunden fest, wie lange der lokale oder entfernte Prozess auf eine neue Nachricht auf der Protokollebene wartet. Dies verhindert, dass Prozesse unbegrenzt auf eine Nachricht warten.

HINWEIS:

Der Wert von `protocol-timeout` muss größer sein als der von `db-timeout`.

```text
default: 31m
allowed: [100ms, 7d]
example: protocol-timeout=630
```

### Option für Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Keep-alive aktivieren.

Aktiviert Keep-alive-Nachrichten auf Socket-Verbindungen.

```text
default: y
example: sck-keep-alive=n
```

### Option für den Spool-Pfad (`--spool-path`) {#spool-path-option---spool-path}

Pfad zum Speichern vorübergehend benötigter Daten.

In diesem Pfad werden Daten für die asynchronen Befehle `archive-push` und `archive-get` gespeichert.

Der asynchrone Befehl `archive-push` schreibt Bestätigungen in den Spool-Pfad, wenn WAL erfolgreich im Archiv gespeichert wurde, und Fehlermeldungen bei einem Fehlschlag. So kann der Vordergrundprozess PostgreSQL schnell benachrichtigen. Die Bestätigungsdateien sind sehr klein: bei Erfolg leer, bei Fehlern wenige hundert Byte groß.

Der asynchrone Befehl `archive-get` hält WAL im Spool-Pfad bereit, damit es auf Anfrage von PostgreSQL sehr schnell geliefert werden kann. Das Verschieben der Dateien zu PostgreSQL ist am effizientesten, wenn der Spool-Pfad auf demselben Dateisystem wie `pg_xlog`/`pg_wal` liegt. Es wird jedoch davon abgeraten, den Spool-Pfad *innerhalb* des Verzeichnisses `pg_xlog`/`pg_wal` anzulegen, da dies bei PostgreSQL-Werkzeugen wie `pg_rewind` Probleme verursachen kann.

Die Daten im Spool-Pfad sind nicht rein temporär, da sie einen Neustart überdauern können und sollten. Ihr Verlust ist jedoch kein Problem: Für `archive-push` prüft pgBackRest einfach jedes WAL-Segment erneut auf sichere Archivierung; für `archive-get` baut es die Warteschlange neu auf.

Der Spool-Pfad ist für ein lokales POSIX-kompatibles Dateisystem vorgesehen, nicht für ein entferntes Dateisystem wie NFS oder CIFS.

```text
default: /var/spool/pgbackrest
example: spool-path=/backup/db/spool
```

### Option für die Keep-alive-Anzahl (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Anzahl der Keep-alive-Nachrichten.

Legt fest, wie viele TCP-Keep-alive-Nachrichten verloren gehen dürfen, bevor die Verbindung als unterbrochen gilt.

Diese Option ist auf Systemen verfügbar, die die Socket-Option `TCP_KEEPCNT` unterstützen.

```text
allowed: [1, 32]
example: tcp-keep-alive-count=3
```

### Option für die Keep-alive-Leerlaufzeit (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Keep-alive-Leerlaufzeit.

Legt die Zeit ohne Netzwerkaktivität in Sekunden fest, nach der das Betriebssystem eine TCP-Keep-alive-Nachricht senden sollte.

Diese Option ist auf Systemen verfügbar, die die Socket-Option `TCP_KEEPIDLE` unterstützen.

```text
allowed: [1, 3600]
example: tcp-keep-alive-idle=60
```

### Option für das Keep-alive-Intervall (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Keep-alive-Intervall.

Legt die Zeit in Sekunden fest, nach der eine nicht bestätigte TCP-Keep-alive-Nachricht erneut gesendet werden sollte.

Diese Option ist auf Systemen verfügbar, die die Socket-Option `TCP_KEEPINTVL` unterstützen.

```text
allowed: [1, 900]
example: tcp-keep-alive-interval=30
```

### Option für TLSv1.2-Cipher-Suites (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Zulässige TLSv1.2-Cipher-Suites.

Alle TLS-Verbindungen zwischen pgBackRest-Client und -Server sind verschlüsselt. Standardmäßig sind auch Verbindungen zu Objektspeichern wie S3 verschlüsselt.

HINWEIS:

TLSv1.2 ist das absolute Mindestsicherheitsniveau für jede Transportverbindung.

Die akzeptierten Cipher-Suites können bei Bedarf angepasst werden. Das Beispiel ist eine sinnvolle Wahl, sofern keine besonderen Sicherheitsanforderungen bestehen. Ist die Option nicht gesetzt (Standardeinstellung), gilt die Vorgabe der zugrunde liegenden OpenSSL-Bibliothek.

```text
example: tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Option für TLSv1.3-Cipher-Suites (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Zulässige TLSv1.3-Cipher-Suites.

Alle TLS-Verbindungen zwischen pgBackRest-Client und -Server sind verschlüsselt. Standardmäßig sind auch Verbindungen zu Objektspeichern wie S3 verschlüsselt.

HINWEIS:

TLSv1.2 ist das absolute Mindestsicherheitsniveau für jede Transportverbindung.

Die akzeptierten Cipher-Suites können bei Bedarf angepasst werden. Ist die Option nicht gesetzt (Standardeinstellung), gilt die Vorgabe der zugrunde liegenden OpenSSL-Bibliothek.

```text
example: tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

--------

## Protokollierungsoptionen {#log-options}

Der Abschnitt `log` definiert Einstellungen für die Protokollierung.

ACHTUNG:

Die Protokollierung auf Trace-Stufe kann Geheimnisse wie Schlüssel und Passwörter offenlegen. Mit Vorsicht verwenden!

### Option für die Protokollierungsstufe der Konsole (`--log-level-console`) {#console-log-level-option---log-level-console}

Protokollierungsstufe für die Konsole.

Die folgenden Protokollierungsstufen werden unterstützt:

- `off` - Keine Protokollierung (nicht empfohlen)
- `error` - Nur Fehler protokollieren
- `warn` - Warnungen und Fehler protokollieren
- `info` - Informationen, Warnungen und Fehler protokollieren
- `detail` - Details, Informationen, Warnungen und Fehler protokollieren
- `debug` - Debug-Meldungen, Details, Informationen, Warnungen und Fehler protokollieren
- `trace` - Trace-Meldungen (sehr ausführliche Debug-Ausgaben), Debug-Meldungen, Informationen, Warnungen und Fehler protokollieren

```text
default: warn
example: log-level-console=error
```

### Option für die Protokollierungsstufe der Datei (`--log-level-file`) {#file-log-level-option---log-level-file}

Protokollierungsstufe für die Dateiausgabe.

Die folgenden Protokollierungsstufen werden unterstützt:

- `off` - Keine Protokollierung (nicht empfohlen)
- `error` - Nur Fehler protokollieren
- `warn` - Warnungen und Fehler protokollieren
- `info` - Informationen, Warnungen und Fehler protokollieren
- `detail` - Details, Informationen, Warnungen und Fehler protokollieren
- `debug` - Debug-Meldungen, Details, Informationen, Warnungen und Fehler protokollieren
- `trace` - Trace-Meldungen (sehr ausführliche Debug-Ausgaben), Debug-Meldungen, Informationen, Warnungen und Fehler protokollieren

```text
default: info
example: log-level-file=debug
```

### Option für die Protokollierungsstufe der Standardfehlerausgabe (`--log-level-stderr`) {#std-error-log-level-option---log-level-stderr}

Protokollierungsstufe für stderr.

Legt fest, welche Protokollierungsstufen an `stderr` statt an `stdout` ausgegeben werden (festgelegt durch `log-level-console`). Zeitstempel und Prozess werden nicht an `stderr` ausgegeben.

Die folgenden Protokollierungsstufen werden unterstützt:

- `off` - Keine Protokollierung (nicht empfohlen)
- `error` - Nur Fehler protokollieren
- `warn` - Warnungen und Fehler protokollieren
- `info` - Informationen, Warnungen und Fehler protokollieren
- `detail` - Details, Informationen, Warnungen und Fehler protokollieren
- `debug` - Debug-Meldungen, Details, Informationen, Warnungen und Fehler protokollieren
- `trace` - Trace-Meldungen (sehr ausführliche Debug-Ausgaben), Debug-Meldungen, Informationen, Warnungen und Fehler protokollieren

```text
default: off
example: log-level-stderr=error
```

### Option für den Protokollpfad (`--log-path`) {#log-path-option---log-path}

Pfad, an dem Protokolldateien gespeichert werden.

In diesem Pfad speichert pgBackRest seine Protokolldateien. Bei `log-level-file=off` ist kein Protokollpfad erforderlich.

```text
default: /var/log/pgbackrest
example: log-path=/backup/db/log
```

### Option für die Protokollierung von Unterprozessen (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Protokollierung in Unterprozessen aktivieren.

Aktiviert die Dateiprotokollierung für alle von diesem Prozess erzeugten Unterprozesse mit der durch `log-level-file` festgelegten Protokollierungsstufe.

```text
default: n
example: log-subprocess=y
```

### Option für Zeitstempel im Protokoll (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Zeitstempel in der Protokollierung aktivieren.

Aktiviert Zeitstempel in der Konsolen- und Dateiprotokollierung. Diese Option wird in besonderen Situationen deaktiviert, etwa beim Erzeugen der Dokumentation.

```text
default: y
example: log-timestamp=n
```

--------

## Optionen für Maintainer {#maintainer-options}

Maintainer-Optionen dienen der Unterstützung von PostgreSQL-Forks. Die richtigen Einstellungen sollten vom Maintainer des Forks ermittelt und anschließend dessen Benutzern mitgeteilt werden.

WARNUNG:

Unsachgemäße Verwendung dieser Optionen kann zu unerwartetem Verhalten oder Datenbeschädigungen führen.

Es liegt in der Verantwortung des Fork-Maintainers, pgBackRest mit den erforderlichen Optionen zu testen. pgBackRest garantiert keine Kompatibilität mit Forks.

### Option zur Prüfung der WAL-Header (`--archive-header-check`) {#check-wal-headers-option---archive-header-check}

PostgreSQL-Version und -ID in WAL-Headern prüfen.

Diese standardmäßig aktivierte Option prüft den WAL-Header anhand der PostgreSQL-Version und der Systemkennung. Dadurch wird sichergestellt, dass WAL in die richtige Stanza kopiert wird. Zusätzlich wird bereits `pg_control` mit der Stanza abgeglichen und geprüft, ob WAL aus demselben PostgreSQL-Datenverzeichnis kopiert wird, in dem sich `pg_control` befindet.

Das Deaktivieren dieser Prüfung ist daher relativ sicher, sollte aber nur bei Bedarf erfolgen, etwa wenn WAL verschlüsselt ist.

```text
default: y
example: archive-header-check=n
```

### Option zur Prüfung der Seitenheader (`--page-header-check`) {#page-header-check-option---page-header-check}

PostgreSQL-Seitenheader prüfen.

Diese standardmäßig aktivierte Option ergänzt Prüfungen der Seitenheader.

Das Deaktivieren dieser Option sollte vermieden werden, außer wenn es erforderlich ist, etwa bei verschlüsselten Seiten.

```text
default: y
example: page-header-check=n
```

### Option zum Erzwingen der PostgreSQL-Version (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

PostgreSQL-Version erzwingen.

Verwendet die angegebene PostgreSQL-Version statt der Version, die automatisch aus `pg_control` oder WAL-Headern ermittelt wird. Dies ist hauptsächlich für PostgreSQL-Forks oder Entwicklungsversionen hilfreich, deren Werte von denen der veröffentlichten Version abweichen. Die von PostgreSQL über `server_version_num` gemeldete Version muss mit der erzwungenen Version übereinstimmen.

WARNUNG:

Diese Option mit Vorsicht verwenden: `pg_control` und WAL-Header werden weiterhin im erwarteten Format der angegebenen Version gelesen, also im Format der offiziellen Open-Source-Version von PostgreSQL. Ändert der Fork oder die Entwicklungsversion das Format von Feldern, auf die pgBackRest angewiesen ist, führt dies zu unerwartetem Verhalten. Im Allgemeinen funktioniert diese Option nur dann wie erwartet, wenn der Fork alle eigenen Strukturfelder *nach* den standardmäßigen PostgreSQL-Feldern hinzufügt.

```text
example: pg-version-force=15
```

--------

## Repository-Optionen {#repository-options}

Der Abschnitt `repository` definiert Optionen zur Konfiguration des Repositorys.

**Indizierung**: Alle `repo-`-Optionen sind indiziert, damit mehrere Repositorys konfiguriert werden können. Ein einzelnes Repository wird beispielsweise mit `repo1-path`, `repo1-host` usw. konfiguriert. Sind mehrere Repositorys konfiguriert und wird bei einem Befehl kein `--repo` angegeben, werden sie in absteigender Priorität bearbeitet, etwa repo1 vor repo2.

Die Optionen `repo-retention-*` legen fest, wie lange Backups aufbewahrt werden. Eine Bereinigung erfolgt erst, wenn die Anzahl abgeschlossener Backups die zulässige Aufbewahrung überschreitet. Steht also `repo1-retention-full-type` auf `count` (Standard) und `repo1-retention-full` auf 2, müssen 3 abgeschlossene Backups vorhanden sein, bevor das älteste entfernt wird. Steht `repo1-retention-full-type` auf `time`, gibt `repo1-retention-full` Tage an. Daher müssen vollständige Backups für mindestens diesen Zeitraum vorliegen, bevor eine Bereinigung erfolgen kann. Sorgen Sie stets für genügend Platz für die Aufbewahrungsanzahl + 1 Backups.

### Option für das Azure-Konto des Repositorys (`--repo-azure-account`) {#azure-repository-account-option---repo-azure-account}

Azure-Konto des Repositorys.

Azure-Konto, in dem das Repository gespeichert wird.

```text
example: repo1-azure-account=pg-backup
```

### Option für den Azure-Container des Repositorys (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Azure-Repository-Container.

Azure-Container, der das Repository speichert.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Containers gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von Azure erzeugte Inhalte im Container gespeichert werden können.

```text
example: repo1-azure-container=pg-backup
```

### Option für den Azure-Endpunkt des Repositorys (`--repo-azure-endpoint`) {#azure-repository-endpoint-option---repo-azure-endpoint}

Azure-Endpunkt des Repositorys.

Endpunkt für die Verbindung zum Blob-Dienst. Der Standardwert ist im Allgemeinen korrekt, sofern nicht Azure Government verwendet wird.

Für angepasste Konfigurationen oder Tests können die Optionen `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` und `repo-storage-verify-tls` hilfreich sein.

```text
default: blob.core.windows.net
example: repo1-azure-endpoint=blob.core.usgovcloudapi.net
```

### Option für den Azure-Schlüssel des Repositorys (`--repo-azure-key`) {#azure-repository-key-option---repo-azure-key}

Azure-Schlüssel des Repositorys.

Je nach `repo-azure-key-type` ein gemeinsamer Schlüssel oder eine Signatur für gemeinsamen Zugriff.

```text
example: repo1-azure-key=T+9+aov82qNhrcXSNGZCzm9mjd4d75/oxxOr6r1JVpgTLA==
```

### Option für den Azure-Schlüsseltyp des Repositorys (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Azure-Repository-Schlüsseltyp.

Folgende Typen werden für die Autorisierung unterstützt:

- `shared` - Gemeinsamer Schlüssel
- `sas` - Signatur für gemeinsamen Zugriff
- `auto` - Automatische Autorisierung mit verwalteten Azure-Identitäten

```text
default: shared
example: repo1-azure-key-type=sas
```

### Option für den Azure-URI-Stil des Repositorys (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Azure-URI-Stil.

Folgende URI-Stile werden unterstützt:

- `host` - Verbindung zum `account.endpoint`-Host herstellen.
- `path` - Verbindung zum `endpoint`-Host herstellen und den Kontonamen vor die URIs stellen.

```text
default: host
example: repo1-azure-uri-style=path
```

### Option für inkrementelle Backups auf Blockebene (`--repo-block`) {#block-incremental-backup-option---repo-block}

Inkrementelle Backups auf Blockebene aktivieren.

Inkrementelle Backups auf Blockebene ermöglichen feinere Abstufungen, indem Dateien in Blöcke aufgeteilt werden, die sich unabhängig voneinander sichern lassen. Dies spart Speicherplatz im Repository und kann Delta-Wiederherstellungen beschleunigen, da einzelne Blöcke abgerufen werden können, ohne die gesamte Datei aus dem Repository zu lesen.

HINWEIS:

`repo-bundle` muss aktiviert sein, bevor `repo-block` aktiviert werden kann.

Die Blockgröße einer Datei wird anhand ihrer Größe und ihres Alters bestimmt. Ältere oder größere Dateien erhalten im Allgemeinen größere Blöcke. Ist eine Datei alt genug, wird sie nicht inkrementell auf Blockebene gesichert.

Inkrementelle Backups auf Blockebene sind am effizientesten, wenn sie für alle Backup-Typen einschließlich vollständiger Backups aktiviert sind. Das vollständige Backup wird dadurch etwas größer. Spätere differenzielle und inkrementelle Backups können aber die dabei erzeugten Blockzuordnungen nutzen, um Speicherplatz zu sparen.

```text
default: n
example: repo1-block=y
```

### Option für Dateibündel im Repository (`--repo-bundle`) {#repository-bundles-option---repo-bundle}

Dateien im Repository bündeln.

Kleinere Dateien bündeln, also zusammenfassen, um die Gesamtzahl der ins Repository geschriebenen Dateien zu verringern. Weniger Dateien zu schreiben ist im Allgemeinen effizienter, insbesondere bei Objektspeichern wie S3. Außerdem werden leere Dateien nur im Manifest erfasst und ansonsten nicht gespeichert, was Zeit und Speicherplatz spart.

```text
default: n
example: repo1-bundle=y
```

### Option für die Dateigrößengrenze beim Bündeln (`--repo-bundle-limit`) {#repository-bundle-limit-option---repo-bundle-limit}

Grenzwert für Dateibündel.

Größenlimit für Dateien, die in Bündel aufgenommen werden. Größere Dateien werden separat gespeichert.

Gebündelte Dateien können bei der Wiederaufnahme eines Backups nicht wiederverwendet werden. Diese Option bestimmt daher, welche Dateien sich wiederverwenden lassen: Höhere Werte führen zu weniger wiederverwendbaren Dateien.

```text
default: 2MiB
allowed: [8KiB, 1PiB]
example: repo1-bundle-limit=10MiB
```

### Option für die Bündelgröße im Repository (`--repo-bundle-size`) {#repository-bundle-size-option---repo-bundle-size}

Zielgröße für Dateibündel.

Legt die angestrebte Gesamtgröße der Dateien in einem Bündel fest. Die unkomprimierte Bündelgröße kann bis zu `repo-bundle-size` + `repo-bundle-limit` betragen. Deshalb diese Option nicht auf die maximal zulässige Dateigröße des Dateisystems setzen.

Im Allgemeinen sollte diese Option nicht zu hoch gesetzt werden, da bei Wiederholungsversuchen das gesamte Bündel erneut verarbeitet werden muss.

```text
default: 20MiB
allowed: [1MiB, 1PiB]
example: repo1-bundle-size=10MiB
```

### Option für die Verschlüsselungspassphrase des Repositorys (`--repo-cipher-pass`) {#repository-cipher-passphrase-option---repo-cipher-pass}

Verschlüsselungspassphrase des Repositorys.

Passphrase zum Verschlüsseln und Entschlüsseln von Dateien im Repository.

HINWEIS:

Ohne die Option `stanza` liest der Befehl `info` Verschlüsselungseinstellungen nur aus dem Abschnitt `global`. Sind diese Einstellungen pro Stanza konfiguriert, `info` mit der Option `stanza` ausführen, um eine verschlüsselte Stanza zu lesen.

```text
example: repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
```

### Option für den Verschlüsselungstyp des Repositorys (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Verfahren zur Verschlüsselung des Repositorys.

Folgende Verschlüsselungstypen werden unterstützt:

- `none` - Das Repository ist nicht verschlüsselt
- `aes-256-cbc` - Advanced Encryption Standard mit Schlüssellänge von 256 Bit

Beachten Sie, dass die Verschlüsselung immer clientseitig durchgeführt wird, selbst wenn der Repository-Typ (z. B. S3) Verschlüsselung unterstützt.

```text
default: none
example: repo1-cipher-type=aes-256-cbc
```

### Option für den GCS-Bucket des Repositorys (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

GCS-Bucket des Repositorys.

GCS-Bucket, in dem das Repository gespeichert wird.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Buckets gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von GCS erzeugte Inhalte im Bucket gespeichert werden können.

```text
example: repo1-gcs-bucket=/pg-backup
```

### Option für den GCS-Endpunkt des Repositorys (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

GCS-Repository-Endpunkt.

Endpunkt, der zum Verbinden mit dem Speicherdienst verwendet wird. Kann aktualisiert werden, um einen lokalen GCS-Server oder einen alternativen Endpunkt zu verwenden.

```text
default: storage.googleapis.com
example: repo1-gcs-endpoint=localhost
```

### Option für den GCS-Schlüssel des Repositorys (`--repo-gcs-key`) {#gcs-repository-key-option---repo-gcs-key}

GCS-Schlüssel des Repositorys.

Je nach `repo-gcs-key-type` ein Token oder eine Dienstschlüsseldatei.

```text
example: repo1-gcs-key=/etc/pgbackrest/gcs-key.json
```

### Option für den GCS-Schlüsseltyp des Repositorys (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

GCS-Repository-Schlüsseltyp.

Folgende Typen werden für die Autorisierung unterstützt:

- `auto` - Autorisierung mithilfe des Dienstkontos der Instanz.
- `service` - Dienstkonto anhand eines lokal gespeicherten Schlüssels.
- `token` - Für lokale Tests, z. B. `fakegcs`.

Wenn `repo-gcs-key-type=service` ist, werden die Anmeldeinformationen erneut geladen, wenn das Authentifizierungstoken erneuert wird.

```text
default: service
example: repo1-gcs-key-type=auto
```

### Option für die GCS-Projekt-ID des Repositorys (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

GCS-Projekt-ID.

GCS-Projekt-ID, die zur Bestimmung der Abrechnung von Anfragen verwendet wird.

```text
example: repo1-gcs-user-project=my-project
```

### Option für Hardlinks im Repository (`--repo-hardlink`) {#repository-hardlink-option---repo-hardlink}

Dateien zwischen Backups im Repository durch Hardlinks verbinden.

Aktiviert Hardlinks von Dateien in differenziellen und inkrementellen Backups auf die zugehörigen vollständigen Backups. Auf Dateisystemebene wirkt dadurch jedes Backup wie ein vollständiges Backup. Vorsicht: Änderungen an Dateien mit Hardlinks können alle Backups des Satzes betreffen.

```text
default: n
example: repo1-hardlink=y
```

Veralteter Name: hardlink

### Option für den Repository-Host (`--repo-host`) {#repository-host-option---repo-host}

Repository-Host bei entfernter Ausführung.

Für Backups und Archivierung auf einem lokal eingehängten Dateisystem ist diese Einstellung nicht erforderlich.

```text
example: repo1-host=repo1.domain.com
```

Veralteter Name: backup-host

### Option für die CA-Datei des Repository-Hosts (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Datei mit den Zertifizierungsstellen für den Repository-Host.

Für Verbindungen zum Repository-Host eine andere als die systemweite CA-Datei verwenden.

```text
example: repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option für den CA-Pfad des Repository-Hosts (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Pfad mit den Zertifizierungsstellen für den Repository-Host.

Für Verbindungen zum Repository-Host einen anderen als den systemweiten CA-Pfad verwenden.

```text
example: repo1-host-ca-path=/etc/pki/tls/certs
```

### Option für die Zertifikatdatei des Repository-Hosts (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Zertifikatdatei für den Repository-Host.

Wird an den Repository-Host gesendet, um die Client-Identität zu bestätigen.

```text
example: repo1-host-cert-file=/path/to/client.crt
```

### Option für den Befehl auf dem Repository-Host (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

pgBackRest-Befehl auf dem Repository-Host.

Erforderlich nur, wenn der Pfad zum pgBackRest-Befehl auf dem lokalen und dem Repository-Host unterschiedlich ist. Wenn nicht definiert, wird der Repository-Host-Befehl auf den gleichen Wert wie der lokale Befehl gesetzt.

```text
default: [path of executed pgbackrest binary]
example: repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Veralteter Name: backup-cmd

### Option für die Konfiguration des Repository-Hosts (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

pgBackRest-Konfigurationsdatei auf dem Repository-Host.

Legt den Speicherort der Konfigurationsdatei auf dem Repository-Host fest. Dies ist nur erforderlich, wenn sich die Repository-Host-Konfigurationsdatei an einem anderen Ort befindet als die lokale Konfigurationsdatei.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Veralteter Name: backup-config

### Option für zusätzliche Konfigurationsdateien auf dem Repository-Host (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Pfad zu zusätzlichen pgBackRest-Konfigurationsdateien auf dem Repository-Host.

Legt den Pfad für zusätzliche Konfigurationsdateien auf dem Repository-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem Repository-Host vom entsprechenden lokalen Pfad abweicht.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Option für den Konfigurationspfad des Repository-Hosts (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

pgBackRest-Konfigurationspfad auf dem Repository-Host.

Legt den Konfigurationspfad auf dem Repository-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem Repository-Host vom lokalen Konfigurationspfad abweicht.

```text
default: CFGOPTDEF_CONFIG_PATH
example: repo1-host-config-path=/conf/pgbackrest
```

### Option für die Schlüsseldatei des Repository-Hosts (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Schlüsseldatei für den Repository-Host.

Weist nach, dass das Client-Zertifikat von seinem Eigentümer gesendet wurde.

```text
example: repo1-host-key-file=/path/to/client.key
```

### Option für den Port des Repository-Hosts (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Port des Repository-Hosts, wenn `repo-host` gesetzt ist.

Mit dieser Option einen anderen als den Standardport für das Protokoll des Repository-Hosts angeben.

HINWEIS:

Bei `repo-host-type=ssh` gibt es keinen Standardwert für `repo-host-port`. In diesem Fall wird der Port verwendet, der für den durch `cmd-ssh` angegebenen Befehl konfiguriert ist.

```text
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: repo1-host-port=25
```

Veralteter Name: backup-ssh-port

### Option für den Protokolltyp des Repository-Hosts (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Protokolltyp für den Repository-Host.

Die folgenden Protokolltypen werden unterstützt:

- `ssh` - Secure Shell.
- `tls` - pgBackRest-TLS-Server.

```text
default: ssh
example: repo1-host-type=tls
```

### Option für den Benutzer auf dem Repository-Host (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Benutzer auf dem Repository-Host, wenn `repo-host` gesetzt ist.

Legt den Benutzer für Operationen auf dem Repository-Host fest. Vorzugsweise ist dies nicht `postgres`, sondern ein anderer Benutzer wie `pgbackrest`. Läuft PostgreSQL auf dem Repository-Host, kann der Benutzer `postgres` der Gruppe `pgbackrest` hinzugefügt werden. So erhält er Leserechte für das Repository, ohne dessen Inhalt versehentlich beschädigen zu können.

```text
default: pgbackrest
example: repo1-host-user=repo-user
```

Veralteter Name: backup-user

### Option für den Repository-Pfad (`--repo-path`) {#repository-path-option---repo-path}

Pfad zum Speichern von Backups und Archiv.

Im Repository speichert pgBackRest Backups und archiviert WAL-Segmente.

Der benötigte Speicherplatz lässt sich im Voraus oft schwer abschätzen. Am besten erstellen Sie einige Backups, erfassen die Größe verschiedener Backup-Typen (full/incr/diff) und messen die täglich erzeugte WAL-Menge. So erhalten Sie einen ungefähren Überblick über den Platzbedarf. Dieser wird sich im Laufe der Zeit mit der Entwicklung der Datenbank wahrscheinlich ändern.

```text
default: /var/lib/pgbackrest
example: repo1-path=/backup/db/backrest
```

### Option für die Archivaufbewahrung (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

Anzahl der Backups, für die lückenloses WAL aufbewahrt wird.

HINWEIS:

WAL-Segmente, die für ein konsistentes Backup erforderlich sind, bleiben unabhängig von dieser Einstellung immer bis zum Entfernen des Backups erhalten.

Ist dieser Wert nicht gesetzt und ist `repo-retention-full-type` auf `count` gesetzt (Standardeinstellung), richtet sich die Archivbereinigung nach `repo-retention-full` beziehungsweise `repo-retention-diff`, wenn `repo-retention-archive-type` auf `full` beziehungsweise `diff` gesetzt ist. So wird WAL nur für bereits entfernte Backups gelöscht. Ist `repo-retention-full-type` auf `time` gesetzt, werden standardmäßig Archive entfernt, die älter sind als das älteste vollständige Backup, das nach Anwendung von `repo-retention-full` aufbewahrt wird.

Diese Option muss gesetzt sein, wenn `repo-retention-archive-type` auf `incr` gesetzt ist. Bei knappem Speicherplatz kann sie zusammen mit `repo-retention-archive-type` verwendet werden, um WAL-Segmente frühzeitig zu entfernen. Damit ist jedoch keine PITR mehr aus Backups möglich, deren WAL entfernt wurde. Dies wird daher **nicht** empfohlen.

```text
allowed: [1, 9999999]
example: repo1-retention-archive=2
```

Veralteter Name: retention-archive

### Option für den Typ der Archivaufbewahrung (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

Backup-Typ für die WAL-Aufbewahrung.

Bei `full` bewahrt pgBackRest Archivprotokolle für die durch `repo-retention-archive` festgelegte Anzahl vollständiger Backups auf. Bei `diff` (differenziell) werden sie für die durch `repo-retention-archive` festgelegte Anzahl vollständiger und differenzieller Backups aufbewahrt. War das letzte Backup vollständig, wird es für repo-retention also als differenzielles Backup gezählt. Bei `incr` (inkrementell) bewahrt pgBackRest Archivprotokolle für die durch `repo-retention-archive` festgelegte Anzahl vollständiger, differenzieller und inkrementeller Backups auf. Es wird empfohlen, die Standardeinstellung beizubehalten, bei der WAL nur zusammen mit vollständigen Backups entfernt wird.

```text
default: full
example: repo1-retention-archive-type=diff
```

Veralteter Name: retention-archive-type

### Option für die Aufbewahrung differenzieller Backups (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

Anzahl der aufzubewahrenden differenziellen Backups.

Wird ein differenzielles Backup entfernt, werden auch alle zugehörigen inkrementellen Backups entfernt. Ohne Angabe bleiben alle differenziellen Backups erhalten, bis die vollständigen Backups entfernt werden, von denen sie abhängen.

Bei der Bereinigung zählen vollständige Backups zur Anzahl der differenziellen Backups. Dadurch müssen in den meisten Fällen etwas weniger differenzielle Backups aufbewahrt werden.

```text
allowed: [1, 9999999]
example: repo1-retention-diff=3
```

Veralteter Name: retention-diff

### Option für die Aufbewahrung vollständiger Backups (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

Anzahl oder Aufbewahrungsdauer vollständiger Backups.

Wird ein vollständiges Backup entfernt, werden auch alle zugehörigen differenziellen und inkrementellen Backups entfernt. Ist diese Option nicht gesetzt, wird eine Warnung ausgegeben. Für eine unbegrenzte Aufbewahrung die Option auf den Höchstwert setzen.

```text
allowed: [1, 9999999]
example: repo1-retention-full=2
```

Veralteter Name: retention-full

### Option für die Art der Aufbewahrung vollständiger Backups (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

Art der Aufbewahrung vollständiger Backups.

Bestimmt, ob `repo-retention-full` einen Zeitraum in Tagen oder die Anzahl der aufzubewahrenden vollständigen Backups angibt.

Bei `time` werden vollständige Backups, die älter als `repo-retention-full` sind, aus dem Repository entfernt, wenn mindestens ein weiteres Backup vorhanden ist, dessen Alter mindestens dem Wert von `repo-retention-full` entspricht. Steht beispielsweise `repo-retention-full` auf 30 Tage und gibt es 2 vollständige Backups, eines 25 Tage und eines 35 Tage alt, wird keines entfernt. Würde das 35 Tage alte Backup entfernt, bliebe nur das 25 Tage alte übrig. Dies würde die Aufbewahrungsregel von 30 Tagen verletzen: Es muss mindestens ein 30 Tage altes Backup vorhanden sein, bevor ein älteres entfernt werden kann. Archiviertes WAL, das älter als das älteste verbleibende vollständige Backup ist, wird automatisch entfernt, sofern `repo-retention-archive-type` und `repo-retention-archive` nicht ausdrücklich gesetzt sind.

Bei `count` werden vollständige Backups entfernt, die über die durch `repo-retention-full` festgelegte Anzahl hinausgehen. Steht beispielsweise `repo-retention-full` auf `4` und wird ein fünftes vollständiges Backup abgeschlossen, wird das älteste entfernt, sodass die Anzahl bei 4 bleibt.

Ein Backup muss erfolgreich abgeschlossen sein, bevor es für die Aufbewahrung zählt. Steht beispielsweise `repo-retention-full-type` auf `count` und `repo-retention-full` auf `2`, müssen 3 abgeschlossene vollständige Backups vorhanden sein, bevor das älteste entfernt wird.

```text
default: count
example: repo1-retention-full-type=time
```

### Option für die Aufbewahrung des Backup-Verlaufs (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

Aufbewahrungsdauer der Manifeste im Backup-Verlauf in Tagen.

Nach Abschluss eines Backups wird eine Kopie seines Manifests im Pfad `backup.history` gespeichert. Standardmäßig werden diese Dateien nie entfernt, da sie für Auswertungen nützlich sind, etwa um das Wachstum von Backups und WAL im Zeitverlauf zu messen.

Mit `repo-retention-history` die Anzahl der Tage festlegen, für die Manifeste im Backup-Verlauf aufbewahrt werden. Noch nicht entfernte Backups bleiben stets im Verlauf erhalten. Mit `repo-retention-history=0` wird der Verlauf nur für solche Backups aufbewahrt.

Wird das Verlaufsmanifest eines vollständigen Backups entfernt, werden auch die Verlaufsmanifeste aller zugehörigen differenziellen und inkrementellen Backups entfernt.

```text
allowed: [0, 9999999]
example: repo1-retention-history=365
```

### Option für den S3-Bucket des Repositorys (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

S3-Bucket des Repositorys.

S3-Bucket, in dem das Repository gespeichert wird.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Buckets gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von AWS erzeugte Inhalte im Bucket gespeichert werden können.

```text
example: repo1-s3-bucket=pg-backup
```

### Option für den S3-Endpunkt des Repositorys (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

S3-Endpunkt des Repositorys.

Der AWS-Endpunkt sollte für die ausgewählte Region gültig sein.

Für angepasste Konfigurationen oder Tests können die Optionen `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` und `repo-storage-verify-tls` hilfreich sein.

```text
example: repo1-s3-endpoint=s3.amazonaws.com
```

### Option für den S3-Zugriffsschlüssel des Repositorys (`--repo-s3-key`) {#s3-repository-access-key-option---repo-s3-key}

S3-Zugriffsschlüssel des Repositorys.

AWS-Schlüssel für den Zugriff auf diesen Bucket.

```text
example: repo1-s3-key=AKIAIOSFODNN7EXAMPLE
```

### Option für den geheimen S3-Zugriffsschlüssel des Repositorys (`--repo-s3-key-secret`) {#s3-repository-secret-access-key-option---repo-s3-key-secret}

Geheimer S3-Zugriffsschlüssel des Repositorys.

Geheimer AWS-Schlüssel für den Zugriff auf diesen Bucket.

```text
example: repo1-s3-key-secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Option für den S3-Schlüsseltyp des Repositorys (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

S3-Schlüsseltyp des Repositorys.

Die folgenden Typen werden unterstützt:

- `shared` - Gemeinsame Schlüssel
- `auto` - Temporäre Anmeldeinformationen automatisch abrufen
- `web-id` - Anmeldeinformationen für eine Web-Identität automatisch abrufen
- `pod-id` - Anmeldeinformationen für eine EKS-Pod-Identität automatisch abrufen
- `process` - Anmeldeinformationen durch Ausführen eines Prozesses abrufen

```text
default: shared
example: repo1-s3-key-type=auto
```

### Option für die KMS-Schlüssel-ID des S3-Repositorys (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

KMS-Schlüssel für das S3-Repository.

Aktiviert die serverseitige S3-Verschlüsselung mit dem angegebenen Schlüssel des AWS Key Management Service.

```text
example: repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Option für den S3-Authentifizierungsprozess (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Befehl für den S3-Authentifizierungsprozess.

Befehl mit optionalen Argumenten zum Abrufen temporärer S3-Anmeldeinformationen. Der erste Listeneintrag ist der Befehl; die übrigen Einträge werden als Parameter übergeben.

Der Prozess muss JSON mit den Feldern `AccessKeyId`, `SecretAccessKey`, `SessionToken` und `Expiration` ausgeben. Die Anmeldeinformationen werden vor ihrem Ablauf automatisch erneuert. Einzelheiten zum Format finden Sie unter [Anmeldeinformationen aus einem Prozess](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output).

```text
example: repo1-s3-process-cmd=/usr/local/bin/get-credentials
example: repo1-s3-process-cmd=--role
example: repo1-s3-process-cmd=my-role
```

### Option für die S3-Region des Repositorys (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

S3-Region des Repositorys.

AWS-Region, in der der Bucket erstellt wurde.

```text
example: repo1-s3-region=us-east-1
```

### Option für die Kostenübernahme durch den S3-Anforderer (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Kostenübernahme durch den Anforderer beim S3-Repository.

Aktiviert die S3-Kostenübernahme durch den Anforderer.

```text
default: n
example: repo1-s3-requester-pays=n
```

### Option für die S3-Rolle des Repositorys (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

S3-Rolle des Repositorys.

Name der AWS-Rolle (nicht der vollständige ARN) zum Abrufen temporärer Anmeldeinformationen bei `repo-s3-key-type=auto`.

```text
example: repo1-s3-role=authrole
```

### Option für den S3-Dienst des Repositorys (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

S3-Signaturdienst.

Der bei der SigV4-Authentifizierung verwendete S3-Signaturdienst. Für standardmäßige S3-Endpunkte ist der Standardwert `s3`. Bei einem S3-Outposts-Endpunkt auf `s3-outposts` setzen.

```text
default: s3
example: repo1-s3-service=s3-outposts
```

### Option für den S3-SSE-Kundenschlüssel des Repositorys (`--repo-s3-sse-customer-key`) {#s3-repository-sse-customer-key-option---repo-s3-sse-customer-key}

S3-SSE-Kundenschlüssel des Repositorys.

Aktiviert die serverseitige S3-Verschlüsselung mit dem angegebenen Kundenschlüssel.

```text
example: repo1-s3-sse-customer-key=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Option für den STS-Endpunkt des S3-Repositorys (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

STS-Endpunkt des S3-Repositorys.

STS-Endpunkt zum Abrufen temporärer Anmeldeinformationen, wenn `repo-s3-key-type=web-id` konfiguriert ist. Einen regionalen Endpunkt wie `sts.us-east-1.amazonaws.com` angeben, um regionales STS zu verwenden. Dies kann für GovCloud, Regionen in China oder zur Verringerung der Latenz erforderlich sein.

```text
default: sts.amazonaws.com
example: repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Option für das S3-Sicherheitstoken des Repositorys (`--repo-s3-token`) {#s3-repository-security-token-option---repo-s3-token}

S3-Sicherheitstoken des Repositorys.

AWS-Sicherheitstoken für die Verwendung mit temporären Anmeldeinformationen.

```text
example: repo1-s3-token=AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22 ...
```

### Option für den S3-URI-Stil des Repositorys (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

S3-URI-Stil.

Folgende URI-Stile werden unterstützt:

- `host` - Mit dem Host `bucket.endpoint` verbinden.
- `path` - Mit dem Host `endpoint` verbinden und den Bucket den URIs voranstellen.

```text
default: host
example: repo1-s3-uri-style=path
```

### Option für den SFTP-Host des Repositorys (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

SFTP-Host des Repositorys.

SFTP-Host, auf dem sich das Repository befindet.

```text
example: repo1-sftp-host=sftprepo.domain
```

### Option für den Fingerabdruck des SFTP-Hosts (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Fingerabdruck des SFTP-Hosts des Repositorys.

Die Erzeugung des Fingerabdrucks für den SFTP-Host des Repositorys sollte `repo-sftp-host-key-hash-type` entsprechen. Den Fingerabdruck mit `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b` erzeugen. Die SSH-Hostschlüssel befinden sich normalerweise im Verzeichnis `/etc/ssh`.

```text
example: repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Option für die SFTP-Hostschlüsselprüfung (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Art der SFTP-Hostschlüsselprüfung.

Die folgenden Arten der SFTP-Hostschlüsselprüfung werden unterstützt:

- `strict` - pgBackRest fügt niemals automatisch Hostschlüssel zur Datei ~/.ssh/known_hosts hinzu und verweigert Verbindungen zu Hosts, deren Hostschlüssel geändert wurde oder in den Dateien mit bekannten Hosts fehlt. Bei dieser Option muss der Benutzer alle neuen Hosts manuell hinzufügen.
- `accept-new` - pgBackRest fügt neue Hostschlüssel automatisch zur Datei mit bekannten Hosts des Benutzers hinzu, lässt aber keine Verbindungen zu Hosts mit geändertem Hostschlüssel zu.
- `fingerprint` - pgBackRest prüft den Hostschlüssel anhand des mit `repo-sftp-host-fingerprint` angegebenen Fingerabdrucks.
- `none` - Es wird keine Hostschlüsselprüfung durchgeführt.

```text
default: strict
example: repo1-sftp-host-key-check-type=accept-new
```

### Option für den Hash-Typ des SFTP-Hostschlüssels (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Hash-Typ des SFTP-Hostschlüssels für das Repository.

Hash-Typ des SFTP-Hostschlüssels für das Repository. Legt den Hash-Typ fest, mit dem beim SSH-Verbindungsaufbau der Hashwert des Hostschlüssels des entfernten Systems berechnet wird. Neuere Versionen von `libssh2` unterstützen neben md5 und sha1 auch `sha256`.

```text
example: repo1-sftp-host-key-hash-type=sha256
```

### Option für den Port des SFTP-Hosts (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Port des SFTP-Hosts für das Repository.

Port des SFTP-Hosts für das Repository.

```text
default: 22
allowed: [1, 65535]
example: repo1-sftp-host-port=22
```

### Option für den Benutzer auf dem SFTP-Host (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Benutzer auf dem SFTP-Host für das Repository.

Benutzer auf dem Host, auf dem das Repository gespeichert wird.

```text
example: repo1-sftp-host-user=pg-backup
```

### Option für die Datei bekannter SFTP-Hosts (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Datei mit bekannten SFTP-Hosts.

Datei mit bekannten Hosts, in der bei der Authentifizierung nach einem passenden SFTP-Host gesucht wird. Ohne Angabe durchsucht pgBackRest standardmäßig `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` und `/etc/ssh/ssh_known_hosts2`. Sind ein oder mehrere Dateipfade konfiguriert, durchsucht pgBackRest diese nach einem passenden Eintrag. Dateipfade müssen vollständig sein oder mit einer Tilde beginnen. Die Option `repo-sftp-known-host` kann mehrfach angegeben werden, um mehrere Dateien mit bekannten Hosts zu durchsuchen. Für die Prüfung anhand dieser Dateien darf `repo-sftp-host-fingerprint` nicht angegeben sein. Siehe auch die Option `repo-sftp-host-check-type`.

```text
example: repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Option für die private SFTP-Schlüsseldatei (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Datei mit dem privaten SFTP-Schlüssel.

Datei mit dem privaten SFTP-Schlüssel zur Authentifizierung.

```text
example: repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Option für die Passphrase des privaten SFTP-Schlüssels (`--repo-sftp-private-key-passphrase`) {#sftp-repository-private-key-passphrase-option---repo-sftp-private-key-passphrase}

Passphrase für den privaten SFTP-Schlüssel.

Passphrase für den Zugriff auf den privaten Schlüssel. Sie kann beim Erstellen eines öffentlichen/privaten SSH-Schlüsselpaars optional vergeben werden.

```text
example: repo1-sftp-private-key-passphrase=BeSureToGenerateAndUseASecurePassphrase
```

### Option für die öffentliche SFTP-Schlüsseldatei (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Datei mit dem öffentlichen SFTP-Schlüssel.

Datei mit dem öffentlichen SFTP-Schlüssel zur Authentifizierung. Bei einer gegen OpenSSL kompilierten Version optional, bei einer gegen eine andere Bibliothek kompilierten Version erforderlich.

```text
example: repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Option für die CA-Datei des Repository-Speichers (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

CA-Datei für den Repository-Speicher.

Für Zertifikate des Speicherdienstes (z. B. S3 oder Azure) eine andere als die systemweite CA-Datei verwenden.

```text
example: repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Veraltete Namen: repo-azure-ca-file, repo-s3-ca-file

### Option für den TLS-CA-Pfad des Repository-Speichers (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

CA-Pfad für den Repository-Speicher.

Für Zertifikate des Speicherdienstes (z. B. S3 oder Azure) einen anderen als den systemweiten CA-Pfad verwenden.

```text
example: repo1-storage-ca-path=/etc/pki/tls/certs
```

Veraltete Namen: repo-azure-ca-path, repo-s3-ca-path

### Option für den Host des Repository-Speichers (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Host des Repository-Speichers.

Mit einem anderen Host als dem Endpunkt des Speicherdienstes (z. B. S3 oder Azure) verbinden. Dies wird üblicherweise für Tests verwendet.

```text
example: repo1-storage-host=127.0.0.1
```

Veraltete Namen: repo-azure-host, repo-s3-host

### Option für den Port des Repository-Speichers (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Port des Repository-Speichers.

Port für Verbindungen zum Endpunkt des Speicherdienstes (z. B. S3 oder Azure) oder zum angegebenen Host.

```text
default: 443
allowed: [1, 65535]
example: repo1-storage-port=9000
```

Veraltete Namen: repo-azure-port, repo-s3-port

### Option für Tags im Repository-Speicher (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Tags für den Repository-Speicher.

Tags angeben, die Objekten hinzugefügt werden, wenn das Repository ein Objektspeicher wie S3 ist. Die Option kann wiederholt werden, um mehrere Tags hinzuzufügen.

pgBackRest bietet keine Möglichkeit, diese Tags zu ändern. Deshalb sollten sie vor dem Ausführen von `stanza-create` korrekt gesetzt werden, damit die Tags im gesamten Repository einheitlich sind.

```text
example: repo1-storage-tag=key1=value1
```

### Option für die Upload-Blockgröße des Repository-Speichers (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Blockgröße für Uploads in den Repository-Speicher.

Objektspeicher wie S3 erlauben das Hochladen von Dateien in Blöcken, wenn die Datei zu groß für den Arbeitsspeicher ist. Auch wenn die Datei in den Arbeitsspeicher passt, ist es speichereffizienter, den für Uploads verwendeten Speicher zu begrenzen.

Eine größere Blockgröße verbessert im Allgemeinen die Leistung, da sie die Anzahl der Upload-Anfragen verringert und es ermöglicht, mehr Dateien jeweils in einer einzelnen Anfrage statt in Blöcken hochzuladen. Nachteilig ist der höhere Speicherverbrauch. Da für jeden Prozess ein eigener Blockpuffer zugewiesen werden muss, erhöhen größere Werte für `process-max` den gesamten Speicherverbrauch zusätzlich.

Die zulässigen Blockgrößen unterscheiden sich je nach Speichertyp und Plattform. Beispielsweise beträgt die Mindestblockgröße bei AWS S3 5MiB. Auch die Bezeichnung variiert: Bei der Suche nach Mindest- und Höchstwerten für AWS S3 nach „part size“, für GCS nach „chunk size“ und für Azure nach „block size“ suchen.

Ist eine Datei größer als 1GiB (die maximale Dateigröße, die PostgreSQL standardmäßig erzeugt), wird die Blockgröße schrittweise bis zum zulässigen Maximum erhöht, um den Datei-Upload abzuschließen.

```text
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: repo1-storage-upload-chunk-size=16MiB
```

### Option zur Zertifikatprüfung des Repository-Speichers (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Zertifikatprüfung für den Repository-Speicher.

Mit dieser Option lässt sich die Prüfung des TLS-Serverzertifikats des Speicherdienstes (z. B. S3 oder Azure) aktivieren oder deaktivieren. Die Prüfung sollte nur für Tests oder andere Situationen mit selbstsignierten Zertifikaten deaktiviert werden.

```text
default: y
example: repo1-storage-verify-tls=n
```

Veraltete Namen: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Option für symbolische Links im Repository (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

Symbolische Links innerhalb des Repositorys erstellen.

Aktiviert das Erstellen der symbolischen Links für `latest` und Tablespaces. Diese Links sind vor allem nützlich, wenn Snapshots für eine Recovery direkt im Repository verwendet werden, was selten vorkommt.

Obwohl diese Funktion für die meisten Benutzer wahrscheinlich nicht nützlich ist, bleibt sie aus Kompatibilitätsgründen standardmäßig aktiviert. Bei POSIX-ähnlichen Speichern ohne Unterstützung für symbolische Links kann es jedoch sinnvoll sein, sie zu deaktivieren.

```text
default: y
example: repo1-symlink=n
```

### Option für den Zielzeitpunkt des Repositorys (`--repo-target-time`) {#target-time-for-repository-option---repo-target-time}

Zielzeitpunkt für das Repository.

Der Zielzeitpunkt legt fest, welchen Stand des Repositorys Befehle auf versioniertem Speicher lesen. So lässt sich das Repository zu einem früheren Zeitpunkt lesen, um Daten wiederherzustellen, die versehentlich durch Benutzer oder durch Schadsoftware gelöscht oder beschädigt wurden.

S3, GCS und Azure unterstützen versionierten Speicher, aktivieren ihn aber im Allgemeinen nicht standardmäßig. Neben der Versionierung kann es sinnvoll sein, bei S3 die Objektsperre und bei GCS oder Azure das vorläufige Löschen zu aktivieren.

Wenn `repo-target-time` angegeben wird, muss auch die Option `repo` angegeben werden. Wahrscheinlich unterstützen nicht alle Repository-Typen die Versionierung. Im Allgemeinen ist es sinnvoll, für die Wiederherstellung ein einzelnes Repository auszuwählen.

Beim Vergleich werden Speicherzeitstempel berücksichtigt, die <= dem angegebenen Zeitstempel sind. Enthaltene Millisekunden werden abgeschnitten.

```text
example: repo-target-time=2024-08-08 12:12:12+00
```

### Option für den Repository-Typ (`--repo-type`) {#repository-type-option---repo-type}

Art des für das Repository verwendeten Speichers.

Die folgenden Repository-Typen werden unterstützt:

- `azure` - Azure Blob Storage Service
- `cifs` - Wie `posix`, deaktiviert jedoch Links und fsync für Verzeichnisse
- `gcs` - Google Cloud Storage
- `posix` - POSIX-konforme Dateisysteme
- `s3` - AWS Simple Storage Service
- `sftp` - Secure File Transfer Protocol

Wird ein NFS-Mount als `posix`-Repository verwendet, gelten für pgBackRest dieselben Regeln wie in der PostgreSQL-Dokumentation beschrieben: [Erstellen eines Datenbankclusters – Dateisysteme](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```text
default: posix
example: repo1-type=cifs
```

--------

## Wiederherstellungsoptionen {#restore-options}

Der Abschnitt `restore` definiert Einstellungen zur Wiederherstellung von Backups.

### Option für den Archivierungsmodus (`--archive-mode`) {#archive-mode-option---archive-mode}

Archivierung auf dem wiederhergestellten Cluster beibehalten oder deaktivieren.

Mit dieser Option lässt sich die Archivierung auf einem wiederhergestellten Cluster beibehalten oder deaktivieren. Dies ist nützlich, wenn der Cluster für bestimmte Arbeiten zum Primärserver hochgestuft werden muss, aber nicht dauerhaft der neue Primärserver werden soll. In diesem Fall ist es nicht ratsam, WAL aus diesem Cluster ins Repository zu übertragen.

Die folgenden Modi werden unterstützt:

- `off` - Archivierung durch Setzen von `archive_mode=off` deaktivieren.
- `preserve` - Die aktuelle Einstellung von `archive_mode` beibehalten.

**HINWEIS**: Diese Option ist unter PostgreSQL < 12 nicht verfügbar.

```text
default: preserve
example: archive-mode=off
```

### Option zum Ausschließen von Datenbanken (`--db-exclude`) {#exclude-database-option---db-exclude}

Wiederherstellung unter Ausschluss der angegebenen Datenbanken.

Ausgeschlossene Datenbanken werden als Sparse-Dateien mit Nullinhalt wiederhergestellt. Dies spart Platz und ermöglicht PostgreSQL dennoch die Recovery. Danach sind diese Datenbanken nicht zugänglich, können aber mit `drop database` entfernt werden. Die Option `--db-exclude` kann mehrfach angegeben werden, um mehrere Datenbanken auszuschließen.

In Kombination mit `--db-include` gilt `--db-exclude` nur für die standardmäßigen Systemdatenbanken `template0`, `template1` und `postgres`.

```text
example: db-exclude=db_main
```

### Option zur Auswahl von Datenbanken (`--db-include`) {#include-database-option---db-include}

Nur die angegebenen Datenbanken wiederherstellen.

Mit dieser Funktion lassen sich gezielt ausgewählte Datenbanken wiederherstellen. Nicht ausdrücklich ausgewählte Datenbanken werden als Sparse-Dateien mit Nullinhalt wiederhergestellt. Dies spart Platz und ermöglicht PostgreSQL dennoch die Recovery. Danach sind die nicht ausgewählten Datenbanken nicht zugänglich, können aber mit `drop database` entfernt werden.

HINWEIS:

Die integrierten Datenbanken `template0`, `template1` und `postgres` werden immer wiederhergestellt, sofern sie nicht ausdrücklich ausgeschlossen sind.

Die Option `--db-include` kann mehrfach angegeben werden, um mehrere Datenbanken auszuwählen.

Weitere Informationen und Einschränkungen finden Sie unter [Ausgewählte Datenbanken wiederherstellen](/de/pgbackrest/user-guide/#restore-selected-databases).

```text
example: db-include=db_main
```

### Option zur Wiederherstellung aller symbolischen Links (`--link-all`) {#link-all-option---link-all}

Alle symbolischen Links wiederherstellen.

Standardmäßig werden symbolisch verlinkte Verzeichnisse und Dateien als normale Verzeichnisse und Dateien in $PGDATA wiederhergestellt. Auf einem anderen System als dem Ursprungssystem des Backups ist es möglicherweise nicht sicher, symbolische Links mit ihren ursprünglichen Zielen wiederherzustellen. Diese Option stellt alle symbolischen Links genau so wieder her, wie sie auf dem Ursprungssystem des Backups vorhanden waren.

```text
default: n
example: link-all=y
```

### Option zur Zuordnung von Linkzielen (`--link-map`) {#link-map-option---link-map}

Das Ziel eines symbolischen Links ändern.

Ermöglicht es, die Zieldatei oder den Zielpfad eines symbolischen Links bei der Wiederherstellung zu ändern. Dies ist bei Systemen hilfreich, deren Speicheraufteilung vom Ursprungssystem des Backups abweicht.

```text
example: link-map=pg_xlog=/data/xlog
```

### Recovery-Option (`--recovery-option`) {#recovery-option---recovery-option}

Eine Option in `postgresql.auto.conf` oder `recovery.conf` setzen.

Einzelheiten zu den Optionen von `postgresql.auto.conf` oder `recovery.conf` finden Sie unter [Serverkonfiguration](https://www.postgresql.org/docs/current/runtime-config.html). Wählen Sie dort unbedingt Ihre PostgreSQL-Version aus. Diese Option kann mehrfach verwendet werden.

Für PostgreSQL >= 12 werden die Optionen in `postgresql.auto.conf` geschrieben, für alle anderen Versionen in `recovery.conf`.

HINWEIS:

`restore_command` wird automatisch erzeugt, kann aber mit dieser Option überschrieben werden. Einen eigenen `restore_command` mit Vorsicht angeben, da pgBackRest dafür ausgelegt ist, dies selbst zu übernehmen. Optionen für das Recovery-Ziel wie recovery_target_name und recovery_target_time werden automatisch von pgBackRest erzeugt und sollten nicht mit dieser Option gesetzt werden.

Da pgBackRest PostgreSQL nach dem Schreiben von `postgresql.auto.conf` oder `recovery.conf` nicht startet, lassen sich `postgresql.auto.conf` oder `recovery.conf` vor einem manuellen Neustart jederzeit bearbeiten und prüfen.

```text
example: recovery-option=primary_conninfo=db.mydomain.com
```

### Option zur Tablespace-Zuordnung (`--tablespace-map`) {#tablespace-map-option---tablespace-map}

Einen Tablespace im angegebenen Verzeichnis wiederherstellen.

Verschiebt einen Tablespace bei der Wiederherstellung an einen neuen Speicherort. Dies ist nützlich, wenn sich die Tablespace-Pfade auf einem Replikat unterscheiden oder ein aktualisiertes System andere Einhängepunkte verwendet.

Die Speicherorte von Tablespaces werden nicht in pg_tablespace gespeichert. Deshalb können Tablespaces ohne Folgen verschoben werden. Ein Verschieben in `data_directory` wird jedoch nicht empfohlen und kann Probleme verursachen. Weitere hilfreiche Informationen zum Verschieben von Tablespaces bietet http://www.databasesoup.com/2013/11/moving-tablespaces.html.

```text
example: tablespace-map=ts_01=/db/ts_01
```

### Option zur Zuordnung aller Tablespaces (`--tablespace-map-all`) {#map-all-tablespaces-option---tablespace-map-all}

Alle Tablespaces im angegebenen Verzeichnis wiederherstellen.

Tablespaces werden standardmäßig an ihren ursprünglichen Speicherorten wiederhergestellt. Dies lässt sich mit `tablespace-map` für jeden Tablespace ändern. Manchmal ist es jedoch sinnvoller, alle Tablespaces auf einmal einem neuen Verzeichnis zuzuordnen. Dies ist besonders für Entwicklungs- oder Staging-Systeme nützlich, deren Speicheraufteilung vom Ursprungssystem des Backups abweichen kann.

Der angegebene Pfad dient als übergeordnetes Verzeichnis, unter dem alle Tablespaces des Backups erstellt werden.

ACHTUNG:

Tablespaces, die nach Beginn des Backups erstellt wurden, werden nicht neu zugeordnet. Ist eine Tablespace-Zuordnung erforderlich, nach dem Erstellen eines Tablespaces ein neues Backup erstellen.

```text
example: tablespace-map-all=/data/tablespace
```

--------

## Serveroptionen {#server-options}

Der Abschnitt `server` definiert Optionen zur Konfiguration des TLS-Servers.

### Option für die TLS-Serveradresse (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

TLS-Serveradresse.

IP-Adresse, an der der Server auf Client-Anfragen wartet.

```text
default: localhost
example: tls-server-address=*
```

### Option für berechtigte TLS-Clients (`--tls-server-auth`) {#tls-server-authorized-clients-option---tls-server-auth}

Für den TLS-Server berechtigte Clients.

Der Server autorisiert Clients, indem er ihr Zertifikat prüft und dessen CN (Common Name) mit einer Liste vergleicht, die auf dem Server mit der Option `tls-server-auth` konfiguriert ist.

Ein Client-CN kann für beliebig viele Stanzas berechtigt werden, indem der Option `tls-server-auth` eine durch Kommas getrennte Liste übergeben wird. Mit `tls-server-auth=client-cn=*` gilt die Berechtigung für alle Stanzas. Im Client-CN dürfen keine Platzhalter angegeben werden.

```text
example: tls-server-auth=client-cn=stanza1,stanza2
```

### Option für die Zertifizierungsstellen des TLS-Servers (`--tls-server-ca-file`) {#tls-server-certificate-authorities-option---tls-server-ca-file}

Zertifizierungsstellen des TLS-Servers.

Prüft, ob Client-Zertifikate von einer vertrauenswürdigen Zertifizierungsstelle signiert sind.

```text
example: tls-server-ca-file=/path/to/server.ca
```

### Option für das TLS-Serverzertifikat (`--tls-server-cert-file`) {#tls-server-certificate-option---tls-server-cert-file}

Datei mit dem TLS-Serverzertifikat.

Wird an den Client gesendet, um die Identität des Servers nachzuweisen.

```text
example: tls-server-cert-file=/path/to/server.crt
```

### Option für den TLS-Serverschlüssel (`--tls-server-key-file`) {#tls-server-key-option---tls-server-key-file}

Datei mit dem TLS-Serverschlüssel.

Weist nach, dass das Serverzertifikat von seinem Eigentümer gesendet wurde.

```text
example: tls-server-key-file=/path/to/server.key
```

### Option für den TLS-Serverport (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

TLS-Serverport.

Port, an dem der Server auf Client-Anfragen wartet.

```text
default: 8432
allowed: [1, 65535]
example: tls-server-port=8000
```

--------

## Stanza-Optionen {#stanza-options}

Eine Stanza definiert die Backup-Konfiguration für einen bestimmten PostgreSQL-Datenbankcluster. Der Stanza-Abschnitt muss den Pfad des Datenbankclusters sowie bei einem entfernten Cluster Host und Benutzer festlegen. Außerdem können alle globalen Konfigurationsabschnitte überschrieben werden, um Stanza-spezifische Einstellungen zu definieren.

**Indizierung**: Alle `pg-`-Optionen sind indiziert, damit mehrere PostgreSQL-Hosts konfiguriert werden können. Ein einzelner Primärserver wird beispielsweise mit `pg1-path`, `pg1-port` usw. konfiguriert. Wenn ein Standby konfiguriert wird, indizieren Sie die `pg-`-Optionen auf dem Repository-Host als `pg2-` (z. B. pg2-host, pg2-path usw.).

### Option für die PostgreSQL-Datenbank (`--pg-database`) {#postgresql-database-option---pg-database}

PostgreSQL-Datenbank.

Name der Datenbank für Verbindungen zu PostgreSQL. Meist ist der Standardwert die beste Wahl, doch manche Installationen enthalten diese Datenbank möglicherweise nicht.

Aus Kompatibilitätsgründen wird die Umgebungsvariable `PGDATABASE` ignoriert.

```text
default: postgres
example: pg1-database=backupdb
```

### Option für den PostgreSQL-Host (`--pg-host`) {#postgresql-host-option---pg-host}

PostgreSQL-Host für die Ausführung auf einem entfernten System.

Für Backups, bei denen PostgreSQL-Host und Repository-Host unterschiedliche Systeme sind.

```text
example: pg1-host=db.domain.com
```

Veralteter Name: db-host

### Option für die CA-Datei des PostgreSQL-Hosts (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

Datei mit den Zertifizierungsstellen für den PostgreSQL-Host.

Für Verbindungen zum PostgreSQL-Host eine andere als die systemweite CA-Datei verwenden.

```text
example: pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option für den CA-Pfad des PostgreSQL-Hosts (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

Pfad mit den Zertifizierungsstellen für den PostgreSQL-Host.

Für Verbindungen zum PostgreSQL-Host einen anderen als den systemweiten CA-Pfad verwenden.

```text
example: pg1-host-ca-path=/etc/pki/tls/certs
```

### Option für die Zertifikatdatei des PostgreSQL-Hosts (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

Zertifikatdatei für den PostgreSQL-Host.

Wird an den PostgreSQL-Host gesendet, um die Identität des Clients nachzuweisen.

```text
example: pg1-host-cert-file=/path/to/client.crt
```

### Option für den Befehl auf dem PostgreSQL-Host (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

pgBackRest-Befehl auf dem PostgreSQL-Host.

Nur erforderlich, wenn der Pfad zum pgBackRest-Befehl auf dem lokalen und dem PostgreSQL-Host unterschiedlich ist. Ohne Angabe wird auf dem PostgreSQL-Host derselbe Befehl wie lokal verwendet.

```text
default: [path of executed pgbackrest binary]
example: pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Veralteter Name: db-cmd

### Option für die Konfiguration des PostgreSQL-Hosts (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

pgBackRest-Konfigurationsdatei auf dem Datenbank-Host.

Legt den Speicherort der Konfigurationsdatei auf dem PostgreSQL-Host fest. Dies ist nur erforderlich, wenn die Datei dort an einem anderen Ort liegt als die lokale Konfigurationsdatei.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Veralteter Name: db-config

### Option für zusätzliche Konfigurationsdateien auf dem PostgreSQL-Host (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

Pfad zu zusätzlichen pgBackRest-Konfigurationsdateien auf dem Datenbank-Host.

Legt den Pfad für zusätzliche Konfigurationsdateien auf dem PostgreSQL-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem PostgreSQL-Host vom entsprechenden lokalen Pfad abweicht.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Option für den Konfigurationspfad des PostgreSQL-Hosts (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

pgBackRest-Konfigurationspfad auf dem Datenbank-Host.

Legt den Konfigurationspfad auf dem PostgreSQL-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem PostgreSQL-Host vom lokalen Konfigurationspfad abweicht.

```text
default: CFGOPTDEF_CONFIG_PATH
example: pg1-host-config-path=/conf/pgbackrest
```

### Option für die Schlüsseldatei des PostgreSQL-Hosts (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

Schlüsseldatei für den PostgreSQL-Host.

Weist nach, dass das Client-Zertifikat von seinem Eigentümer gesendet wurde.

```text
example: pg1-host-key-file=/path/to/client.key
```

### Option für den Port des PostgreSQL-Hosts (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

Port des PostgreSQL-Hosts, wenn `pg-host` gesetzt ist.

Mit dieser Option einen anderen als den Standardport für das Protokoll des PostgreSQL-Hosts angeben.

HINWEIS:

Bei `pg-host-type=ssh` gibt es keinen Standardwert für `pg-host-port`. In diesem Fall wird der Port verwendet, der für den durch `cmd-ssh` angegebenen Befehl konfiguriert ist.

```text
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: pg1-host-port=25
```

Veralteter Name: db-ssh-port

### Option für den Protokolltyp des PostgreSQL-Hosts (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

Protokolltyp für den PostgreSQL-Host.

Die folgenden Protokolltypen werden unterstützt:

- `ssh` - Secure Shell.
- `tls` - pgBackRest-TLS-Server.

```text
default: ssh
example: pg1-host-type=tls
```

### Option für den Benutzer auf dem PostgreSQL-Host (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

Anmeldebenutzer auf dem PostgreSQL-Host, wenn `pg-host` gesetzt ist.

Unter diesem Benutzer läuft auch der entfernte pgBackRest-Prozess, und er baut die Verbindungen zu PostgreSQL auf. Damit dies korrekt funktioniert, sollte er Eigentümer des PostgreSQL-Datenbankclusters sein. Üblicherweise ist dies `postgres`, der Standardwert.

```text
default: postgres
example: pg1-host-user=db_owner
```

Veralteter Name: db-user

### Option für den PostgreSQL-Pfad (`--pg-path`) {#postgresql-path-option---pg-path}

PostgreSQL-Datenverzeichnis.

Dieser Pfad sollte dem von PostgreSQL gemeldeten `data_directory` entsprechen. Obwohl sich der Wert an verschiedenen Stellen auslesen lässt, ist eine ausdrückliche Angabe ratsam, falls diese Quellen bei einer Wiederherstellung oder einem Offline-Backup nicht verfügbar sind.

Bei jedem Online-Backup wird `pg-path` mit dem von PostgreSQL gemeldeten Wert verglichen. Die Option sollte daher immer aktuell sein.

```text
example: pg1-path=/data/db
```

Veralteter Name: db-path

### Option für den PostgreSQL-Port (`--pg-port`) {#postgresql-port-option---pg-port}

PostgreSQL-Port.

Port, auf dem PostgreSQL läuft. Dieser muss normalerweise nicht angegeben werden, da die meisten PostgreSQL-Cluster den Standardport verwenden.

```text
default: 5432
allowed: [0, 65535]
example: pg1-port=6543
```

Veralteter Name: db-port

### Option für den PostgreSQL-Socket-Pfad (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

Pfad zum PostgreSQL-Unix-Socket.

Das beim Start von PostgreSQL angegebene Unix-Socket-Verzeichnis. pgBackRest sucht automatisch am üblichen Speicherort des Betriebssystems. Diese Einstellung ist daher normalerweise nur erforderlich, wenn das Socket-Verzeichnis ausdrücklich über `unix_socket_directories` in `postgresql.conf` geändert wurde.

```text
example: pg1-socket-path=/var/run/postgresql
```

Veralteter Name: db-socket-path

### Option für den PostgreSQL-Datenbankbenutzer (`--pg-user`) {#postgresql-database-user-option---pg-user}

PostgreSQL-Datenbankbenutzer.

Datenbankbenutzername für Verbindungen zu PostgreSQL. Ohne Angabe verbindet sich pgBackRest mit dem lokalen Betriebssystembenutzer oder mit `PGUSER`.

```text
example: pg1-user=backupuser
```
