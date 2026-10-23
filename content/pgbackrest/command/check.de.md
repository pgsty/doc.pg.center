---
title: "Prüfbefehl (check)"
linkTitle: "check"
weight: 50
description: "Referenz zu den Optionen und zum Verhalten des pgBackRest-Befehls `check`."
icon: fa-solid fa-circle-check
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/command.html#command-check"
---

Der Befehl `check` prüft, ob pgBackRest und die Einstellung archive_command für Archivierung und Backups der angegebenen Stanza korrekt konfiguriert sind. Er versucht, alle Repositorys und Datenbanken zu prüfen, die für den Host konfiguriert sind, auf dem er läuft. Dabei erkennt er Fehlkonfigurationen, insbesondere bei der Archivierung, die zu unvollständigen Backups führen, weil erforderliche WAL-Segmente das Archiv nicht erreicht haben. Der Befehl kann auf dem PostgreSQL- oder dem Repository-Host ausgeführt werden. Auch die Ausführung auf dem Standby-Host ist möglich. Da dort jedoch `pg_switch_xlog()`/`pg_switch_wal()` nicht ausgeführt werden können, wird in diesem Fall nur die Repository-Konfiguration geprüft.

Um PostgreSQL zur Archivierung eines WAL-Segments zu zwingen, werden `pg_create_restore_point('pgBackRest Archive Check')` und `pg_switch_xlog()`/`pg_switch_wal()` aufgerufen.

## Befehlsoptionen {#command-options}

### Option zur Archivprüfung (`--archive-check`) {#check-archive-option---archive-check}

Vor Abschluss des Backups prüfen, ob sich die WAL-Segmente im Archiv befinden.

Prüft, ob alle für ein konsistentes Backup erforderlichen WAL-Segmente im WAL-Archiv vorhanden sind. Es empfiehlt sich, die Standardeinstellung beizubehalten, sofern keine andere Archivierungsmethode verwendet wird.

Diese Option muss aktiviert sein, wenn `archive-copy` aktiviert ist.

```yaml
default: y
example: --no-archive-check
```

### Option zur Prüfung des Archivierungsmodus (`--archive-mode-check`) {#check-archive-mode-option---archive-mode-check}

Die PostgreSQL-Einstellung `archive_mode` prüfen.

Diese standardmäßig aktivierte Option verbietet die PostgreSQL-Einstellung `archive_mode=always`.

Von einem Standby-Server übertragene WAL-Segmente können logisch mit denen des Primärservers übereinstimmen, aber andere Prüfsummen aufweisen. Zur Vermeidung von Konflikten wird empfohlen, die Archivierung aus mehreren Quellen zu unterbinden.

ACHTUNG:

Bei deaktivierter Option muss unbedingt sichergestellt werden, dass nur ein Archivierer mit dem Befehl `archive-push` in das Repository schreibt.

```yaml
default: y
example: --no-archive-mode-check
```

### Option für das Archivierungszeitlimit (`--archive-timeout`) {#archive-timeout-option---archive-timeout}

Archivierungszeitlimit.

Maximale Wartezeit in Sekunden festlegen, bis ein einzelnes WAL-Segment das Archiv-Repository von pgBackRest erreicht. Dieses Zeitlimit gilt für die Befehle `check` und `backup`, wenn sie auf die Archivierung der WAL-Segmente warten, die für ein konsistentes Backup erforderlich sind.

```yaml
default: 1m
allowed: [100ms, 1d]
example: --archive-timeout=30
```

### Option für Backups vom Standby (`--backup-standby`) {#backup-from-standby-option---backup-standby}

Backup vom Standby-Cluster erstellen.

Backups vom Standby aktivieren, um die Last auf dem Primärcluster zu verringern. Für diese Option müssen sowohl der Primär- als auch der Standby-Host konfiguriert sein.

Die folgenden Modi werden unterstützt:

- `y` - Für das Backup ist ein Standby erforderlich.
- `prefer` - Backup vom Standby erstellen, falls verfügbar, andernfalls vom Primärserver.
- `n` - Backup ausschließlich vom Primärserver erstellen.

```yaml
default: n
example: --backup-standby=y
```

## Allgemeine Optionen {#general-options}

### Option zur Ausführung als root (`--allow-root`) {#allow-run-as-root-option---allow-root}

Die Ausführung des Befehls als Benutzer root erlauben.

Standardmäßig darf nur der Befehl `restore` als Benutzer root ausgeführt werden, da er die Dateieigentümer sorgfältig verwaltet. Bei anderen Befehlen besteht das Risiko, dass Dateien entstehen, die root gehören, etwa im Repository. Diese sind für den PostgreSQL-Benutzer nicht zugänglich, sodass spätere Befehle fehlschlagen.

Diese Option aktivieren, um einen Befehl dennoch als root auszuführen. Es ist jedoch deutlich besser, pgBackRest als den Benutzer auszuführen, dem das Repository und der PostgreSQL-Cluster gehören.

```yaml
default: n
example: --allow-root
```

### Option für die Puffergröße (`--buffer-size`) {#buffer-size-option---buffer-size}

Puffergröße für I/O-Operationen.

Puffergröße für Kopier-, Komprimierungs-, Verschlüsselungs- und andere Operationen. Die Anzahl der verwendeten Puffer hängt von den Optionen ab. Jede Operation kann zusätzlichen Speicher benötigen; beispielsweise kann die Komprimierung mit `gz` weitere 256KiB Speicher beanspruchen.

Zulässige Werte sind `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB` und `16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### Option für den SSH-Client-Befehl (`--cmd-ssh`) {#ssh-client-command-option---cmd-ssh}

SSH-Client-Befehl.

Einen bestimmten SSH-Client-Befehl verwenden, wenn eine Alternative gewünscht wird oder der Befehl `ssh` nicht in $PATH liegt.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### Option für die Netzwerkkomprimierungsstufe (`--compress-level-network`) {#network-compress-level-option---compress-level-network}

Komprimierungsstufe für die Netzwerkübertragung.

Legt die Komprimierungsstufe für die Netzwerkübertragung fest, wenn `compress-type=none` gilt und der Befehl nicht auf demselben Host wie das Repository ausgeführt wird. Die Komprimierung verringert den Netzwerkverkehr. Wenn `compress-type` nicht `none` ist, wird `compress-level-network` ignoriert und stattdessen `compress-level` verwendet, damit die Datei nur einmal komprimiert wird.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### Option für die Konfigurationsdatei (`--config`) {#config-option---config}

pgBackRest-Konfigurationsdatei.

Mit dieser Option eine andere als die standardmäßige Konfigurationsdatei angeben.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### Option für den Pfad zusätzlicher Konfigurationsdateien (`--config-include-path`) {#config-include-path-option---config-include-path}

Pfad zu zusätzlichen pgBackRest-Konfigurationsdateien.

Konfigurationsdateien mit der Endung `.conf` am angegebenen Speicherort werden mit der pgBackRest-Konfigurationsdatei zu einer einzigen Konfigurationsdatei zusammengefügt.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### Option für den Konfigurationspfad (`--config-path`) {#config-path-option---config-path}

Basispfad der pgBackRest-Konfigurationsdateien.

Diese Einstellung überschreibt den standardmäßigen Basispfad der Optionen `--config` und `--config-include-path`, sofern diese nicht ausdrücklich in der Befehlszeile gesetzt werden.

Wird beispielsweise nur `--config-path=/conf/pgbackrest` angegeben, erhält `--config` den Standardwert `/conf/pgbackrest/pgbackrest.conf` und `--config-include-path` den Standardwert `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### Option für das Datenbankzeitlimit (`--db-timeout`) {#database-timeout-option---db-timeout}

Zeitlimit für Datenbankabfragen.

Legt das Zeitlimit für Datenbankabfragen in Sekunden fest. Dazu gehören auch die Funktionen zum Starten und Stoppen des Backups, die jeweils viel Zeit benötigen können. Daher sollte das Zeitlimit hoch bleiben, sofern nicht bekannt ist, dass diese Funktionen schnell zurückkehren, etwa wenn `start-fast=y` gesetzt ist und bekannt ist, dass der Datenbankcluster während des Backups nur wenige WAL-Segmente erzeugt.

> **HINWEIS:** Der Wert von `db-timeout` muss kleiner sein als der von `protocol-timeout`.

```yaml
default: 30m
allowed: [100ms, 7d]
example: --db-timeout=600
```

### Option für das I/O-Zeitlimit (`--io-timeout`) {#io-timeout-option---io-timeout}

I/O-Zeitlimit.

Zeitlimit in Sekunden für Verbindungen sowie Lese- und Schreiboperationen.

Die gesamte Lese- oder Schreiboperation muss nicht innerhalb dieses Zeitlimits abgeschlossen sein, aber es muss *irgendein* Fortschritt erzielt werden, selbst wenn es nur ein einziges Byte ist.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Option für eine neutrale umask (`--neutral-umask`) {#neutral-umask-option---neutral-umask}

Eine neutrale umask verwenden.

Setzt die umask auf 0000, damit die Zugriffsrechte im Repository sinnvoll gesetzt werden. Standardmäßig erhalten Verzeichnisse den Modus 0750 und Dateien den Modus 0640.

Um stattdessen die umask des ausführenden Benutzers zu verwenden, `neutral-umask=n` in der Konfigurationsdatei oder `--no-neutral-umask` in der Befehlszeile angeben.

```yaml
default: y
example: --no-neutral-umask
```

### Option für die Prozesspriorität (`--priority`) {#set-process-priority-option---priority}

Prozesspriorität festlegen.

Legt fest, welche Priorität (also welcher nice-Wert) dem Prozess vom Kernel-Scheduler zugewiesen wird. Positive Werte verringern die Priorität, negative Werte erhöhen sie. In den meisten Fällen dürfen Prozesse ihre Priorität nicht erhöhen.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### Option für das Protokollzeitlimit (`--protocol-timeout`) {#protocol-timeout-option---protocol-timeout}

Protokollzeitlimit.

Legt in Sekunden fest, wie lange der lokale oder entfernte Prozess auf eine neue Nachricht auf der Protokollebene wartet. Dies verhindert, dass Prozesse unbegrenzt auf eine Nachricht warten.

> **HINWEIS:** Der Wert von `protocol-timeout` muss größer sein als der von `db-timeout`.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### Option für Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Keep-alive aktivieren.

Aktiviert Keep-alive-Nachrichten auf Socket-Verbindungen.

```yaml
default: y
example: --no-sck-keep-alive
```

### Option für die Stanza (`--stanza`) {#stanza-option---stanza}

Definiert die Stanza.

Eine Stanza ist die Konfiguration eines PostgreSQL-Datenbankclusters. Sie legt unter anderem dessen Speicherort, das Backup-Verfahren und die Archivierungsoptionen fest. Die meisten Datenbankserver haben nur einen PostgreSQL-Datenbankcluster und daher nur eine Stanza. Backup-Server haben dagegen für jeden zu sichernden Datenbankcluster eine Stanza.

Es liegt nahe, die Stanza nach dem Primärcluster zu benennen. Ein besserer Name beschreibt jedoch die im Cluster enthaltenen Datenbanken. Da der Stanza-Name für den Primärserver und alle Replikate verwendet wird, sollte er die tatsächliche Funktion des Clusters beschreiben, etwa app oder dw, statt den lokalen Clusternamen wie main oder prod zu übernehmen.

```yaml
example: --stanza=main
```

### Option für die Keep-alive-Anzahl (`--tcp-keep-alive-count`) {#keep-alive-count-option---tcp-keep-alive-count}

Anzahl der Keep-alive-Nachrichten.

Legt fest, wie viele TCP-Keep-alive-Nachrichten verloren gehen dürfen, bevor die Verbindung als unterbrochen gilt.

Diese Option ist auf Systemen verfügbar, die die Socket-Option `TCP_KEEPCNT` unterstützen.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### Option für die Keep-alive-Leerlaufzeit (`--tcp-keep-alive-idle`) {#keep-alive-idle-option---tcp-keep-alive-idle}

Keep-alive-Leerlaufzeit.

Legt die Zeit ohne Netzwerkaktivität in Sekunden fest, nach der das Betriebssystem eine TCP-Keep-alive-Nachricht senden sollte.

Diese Option ist auf Systemen verfügbar, die die Socket-Option `TCP_KEEPIDLE` unterstützen.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### Option für das Keep-alive-Intervall (`--tcp-keep-alive-interval`) {#keep-alive-interval-option---tcp-keep-alive-interval}

Keep-alive-Intervall.

Legt die Zeit in Sekunden fest, nach der eine nicht bestätigte TCP-Keep-alive-Nachricht erneut gesendet werden sollte.

Diese Option ist auf Systemen verfügbar, die die Socket-Option `TCP_KEEPINTVL` unterstützen.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### Option für TLSv1.2-Cipher-Suites (`--tls-cipher-12`) {#tlsv12-cipher-suites-option---tls-cipher-12}

Zulässige TLSv1.2-Cipher-Suites.

Alle TLS-Verbindungen zwischen pgBackRest-Client und -Server sind verschlüsselt. Standardmäßig sind auch Verbindungen zu Objektspeichern wie S3 verschlüsselt.

> **HINWEIS:** TLSv1.2 ist das absolute Mindestsicherheitsniveau für jede Transportverbindung.

Die akzeptierten Cipher-Suites können bei Bedarf angepasst werden. Das Beispiel ist eine sinnvolle Wahl, sofern keine besonderen Sicherheitsanforderungen bestehen. Ist die Option nicht gesetzt (Standardeinstellung), gilt die Vorgabe der zugrunde liegenden OpenSSL-Bibliothek.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### Option für TLSv1.3-Cipher-Suites (`--tls-cipher-13`) {#tlsv13-cipher-suites-option---tls-cipher-13}

Zulässige TLSv1.3-Cipher-Suites.

Alle TLS-Verbindungen zwischen pgBackRest-Client und -Server sind verschlüsselt. Standardmäßig sind auch Verbindungen zu Objektspeichern wie S3 verschlüsselt.

> **HINWEIS:** TLSv1.2 ist das absolute Mindestsicherheitsniveau für jede Transportverbindung.

Die akzeptierten Cipher-Suites können bei Bedarf angepasst werden. Ist die Option nicht gesetzt (Standardeinstellung), gilt die Vorgabe der zugrunde liegenden OpenSSL-Bibliothek.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## Protokollierungsoptionen {#log-options}

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

```yaml
default: warn
example: --log-level-console=error
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

```yaml
default: info
example: --log-level-file=debug
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

```yaml
default: off
example: --log-level-stderr=error
```

### Option für den Protokollpfad (`--log-path`) {#log-path-option---log-path}

Pfad, an dem Protokolldateien gespeichert werden.

In diesem Pfad speichert pgBackRest seine Protokolldateien. Bei `log-level-file=off` ist kein Protokollpfad erforderlich.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### Option für die Protokollierung von Unterprozessen (`--log-subprocess`) {#log-subprocesses-option---log-subprocess}

Protokollierung in Unterprozessen aktivieren.

Aktiviert die Dateiprotokollierung für alle von diesem Prozess erzeugten Unterprozesse mit der durch `log-level-file` festgelegten Protokollierungsstufe.

```yaml
default: n
example: --log-subprocess
```

### Option für Zeitstempel im Protokoll (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Zeitstempel in der Protokollierung aktivieren.

Aktiviert Zeitstempel in der Konsolen- und Dateiprotokollierung. Diese Option wird in besonderen Situationen deaktiviert, etwa beim Erzeugen der Dokumentation.

```yaml
default: y
example: --no-log-timestamp
```

## Optionen für Maintainer {#maintainer-options}

### Option zum Erzwingen der PostgreSQL-Version (`--pg-version-force`) {#force-postgresql-version-option---pg-version-force}

PostgreSQL-Version erzwingen.

Verwendet die angegebene PostgreSQL-Version statt der Version, die automatisch aus `pg_control` oder WAL-Headern ermittelt wird. Dies ist hauptsächlich für PostgreSQL-Forks oder Entwicklungsversionen hilfreich, deren Werte von denen der veröffentlichten Version abweichen. Die von PostgreSQL über `server_version_num` gemeldete Version muss mit der erzwungenen Version übereinstimmen.

WARNUNG:

Diese Option mit Vorsicht verwenden: `pg_control` und WAL-Header werden weiterhin im erwarteten Format der angegebenen Version gelesen, also im Format der offiziellen Open-Source-Version von PostgreSQL. Ändert der Fork oder die Entwicklungsversion das Format von Feldern, auf die pgBackRest angewiesen ist, führt dies zu unerwartetem Verhalten. Im Allgemeinen funktioniert diese Option nur dann wie erwartet, wenn der Fork alle eigenen Strukturfelder *nach* den standardmäßigen PostgreSQL-Feldern hinzufügt.

```yaml
example: --pg-version-force=15
```

## Repository-Optionen {#repository-options}

### Option für den Azure-Container des Repositorys (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Azure-Repository-Container.

Azure-Container, der das Repository speichert.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Containers gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von Azure erzeugte Inhalte im Container gespeichert werden können.

```yaml
example: --repo1-azure-container=pg-backup
```

### Option für den Azure-Schlüsseltyp des Repositorys (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Azure-Repository-Schlüsseltyp.

Die folgenden Autorisierungsarten werden unterstützt:

- `shared` - Gemeinsamer Schlüssel
- `sas` - Signatur für gemeinsamen Zugriff
- `auto` - Automatische Autorisierung mit verwalteten Azure-Identitäten

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### Option für den Azure-URI-Stil des Repositorys (`--repo-azure-uri-style`) {#azure-repository-uri-style-option---repo-azure-uri-style}

Azure-URI-Stil.

Folgende URI-Stile werden unterstützt:

- `host` - Verbindung zum `account.endpoint`-Host herstellen.
- `path` - Verbindung zum `endpoint`-Host herstellen und den Kontonamen vor die URIs stellen.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### Option für den Verschlüsselungstyp des Repositorys (`--repo-cipher-type`) {#repository-cipher-type-option---repo-cipher-type}

Verfahren zur Verschlüsselung des Repositorys.

Folgende Verschlüsselungstypen werden unterstützt:

- `none` - Das Repository ist nicht verschlüsselt
- `aes-256-cbc` - Advanced Encryption Standard mit Schlüssellänge von 256 Bit

Beachten Sie, dass die Verschlüsselung immer clientseitig durchgeführt wird, selbst wenn der Repository-Typ (z. B. S3) Verschlüsselung unterstützt.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### Option für den GCS-Bucket des Repositorys (`--repo-gcs-bucket`) {#gcs-repository-bucket-option---repo-gcs-bucket}

GCS-Bucket des Repositorys.

GCS-Bucket, in dem das Repository gespeichert wird.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Buckets gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von GCS erzeugte Inhalte im Bucket gespeichert werden können.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### Option für den GCS-Endpunkt des Repositorys (`--repo-gcs-endpoint`) {#gcs-repository-endpoint-option---repo-gcs-endpoint}

GCS-Repository-Endpunkt.

Endpunkt, der zum Verbinden mit dem Speicherdienst verwendet wird. Kann aktualisiert werden, um einen lokalen GCS-Server oder einen alternativen Endpunkt zu verwenden.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### Option für den GCS-Schlüsseltyp des Repositorys (`--repo-gcs-key-type`) {#gcs-repository-key-type-option---repo-gcs-key-type}

GCS-Repository-Schlüsseltyp.

Die folgenden Autorisierungsarten werden unterstützt:

- `auto` - Autorisierung mithilfe des Dienstkontos der Instanz.
- `service` - Dienstkonto anhand eines lokal gespeicherten Schlüssels.
- `token` - Für lokale Tests, z. B. `fakegcs`.
- `web-id` - Autorisierung über Workload Identity Federation.

Wenn `repo-gcs-key-type=service` ist, werden die Anmeldeinformationen erneut geladen, wenn das Authentifizierungstoken erneuert wird.

Bei `repo-gcs-key-type=web-id` muss `repo-gcs-key` eine Datei mit Anmeldedaten für ein externes Konto angeben. Das Web-Identity-Token wird bei der Erneuerung des Authentifizierungstokens neu geladen.

`service_account_impersonation_url` wird nicht unterstützt. Nur `credential_source.file` wird unterstützt; wenn `credential_source.format` angegeben ist, muss der Typ `text` sein.

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### Option für die GCS-Projekt-ID des Repositorys (`--repo-gcs-user-project`) {#gcs-repository-project-id-option---repo-gcs-user-project}

GCS-Projekt-ID.

GCS-Projekt-ID, die zur Bestimmung der Abrechnung von Anfragen verwendet wird.

```yaml
example: --repo1-gcs-user-project=my-project
```

### Option für den Repository-Host (`--repo-host`) {#repository-host-option---repo-host}

Repository-Host bei entfernter Ausführung.

Für Backups und Archivierung auf einem lokal eingehängten Dateisystem ist diese Einstellung nicht erforderlich.

```yaml
example: --repo1-host=repo1.domain.com
```

Veralteter Name: backup-host

### Option für die CA-Datei des Repository-Hosts (`--repo-host-ca-file`) {#repository-host-certificate-authority-file-option---repo-host-ca-file}

Datei mit den Zertifizierungsstellen für den Repository-Host.

Für Verbindungen zum Repository-Host eine andere als die systemweite CA-Datei verwenden.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option für den CA-Pfad des Repository-Hosts (`--repo-host-ca-path`) {#repository-host-certificate-authority-path-option---repo-host-ca-path}

Pfad mit den Zertifizierungsstellen für den Repository-Host.

Für Verbindungen zum Repository-Host einen anderen als den systemweiten CA-Pfad verwenden.

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### Option für die Zertifikatdatei des Repository-Hosts (`--repo-host-cert-file`) {#repository-host-certificate-file-option---repo-host-cert-file}

Zertifikatdatei für den Repository-Host.

Wird an den Repository-Host gesendet, um die Client-Identität zu bestätigen.

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### Option für den Befehl auf dem Repository-Host (`--repo-host-cmd`) {#repository-host-command-option---repo-host-cmd}

pgBackRest-Befehl auf dem Repository-Host.

Erforderlich nur, wenn der Pfad zum pgBackRest-Befehl auf dem lokalen und dem Repository-Host unterschiedlich ist. Wenn nicht definiert, wird der Repository-Host-Befehl auf den gleichen Wert wie der lokale Befehl gesetzt.

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Veralteter Name: backup-cmd

### Option für die Konfiguration des Repository-Hosts (`--repo-host-config`) {#repository-host-configuration-option---repo-host-config}

pgBackRest-Konfigurationsdatei auf dem Repository-Host.

Legt den Speicherort der Konfigurationsdatei auf dem Repository-Host fest. Dies ist nur erforderlich, wenn sich die Repository-Host-Konfigurationsdatei an einem anderen Ort befindet als die lokale Konfigurationsdatei.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Veralteter Name: backup-config

### Option für zusätzliche Konfigurationsdateien auf dem Repository-Host (`--repo-host-config-include-path`) {#repository-host-configuration-include-path-option---repo-host-config-include-path}

Pfad zu zusätzlichen pgBackRest-Konfigurationsdateien auf dem Repository-Host.

Legt den Pfad für zusätzliche Konfigurationsdateien auf dem Repository-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem Repository-Host vom entsprechenden lokalen Pfad abweicht.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Option für den Konfigurationspfad des Repository-Hosts (`--repo-host-config-path`) {#repository-host-configuration-path-option---repo-host-config-path}

pgBackRest-Konfigurationspfad auf dem Repository-Host.

Legt den Konfigurationspfad auf dem Repository-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem Repository-Host vom lokalen Konfigurationspfad abweicht.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### Option für die Schlüsseldatei des Repository-Hosts (`--repo-host-key-file`) {#repository-host-key-file-option---repo-host-key-file}

Schlüsseldatei für den Repository-Host.

Weist nach, dass das Client-Zertifikat von seinem Eigentümer gesendet wurde.

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### Option für den Port des Repository-Hosts (`--repo-host-port`) {#repository-host-port-option---repo-host-port}

Port des Repository-Hosts, wenn `repo-host` gesetzt ist.

Mit dieser Option einen anderen als den Standardport für das Protokoll des Repository-Hosts angeben.

> **HINWEIS:** Bei `repo-host-type=ssh` gibt es keinen Standardwert für `repo-host-port`. In diesem Fall wird der Port verwendet, der für den durch `cmd-ssh` angegebenen Befehl konfiguriert ist.

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

Veralteter Name: backup-ssh-port

### Option für den Protokolltyp des Repository-Hosts (`--repo-host-type`) {#repository-host-protocol-type-option---repo-host-type}

Protokolltyp für den Repository-Host.

Die folgenden Protokolltypen werden unterstützt:

- `ssh` - Secure Shell.
- `tls` - pgBackRest-TLS-Server.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### Option für den Benutzer auf dem Repository-Host (`--repo-host-user`) {#repository-host-user-option---repo-host-user}

Benutzer auf dem Repository-Host, wenn `repo-host` gesetzt ist.

Legt den Benutzer für Operationen auf dem Repository-Host fest. Vorzugsweise ist dies nicht `postgres`, sondern ein anderer Benutzer wie `pgbackrest`. Läuft PostgreSQL auf dem Repository-Host, kann der Benutzer `postgres` der Gruppe `pgbackrest` hinzugefügt werden. So erhält er Leserechte für das Repository, ohne dessen Inhalt versehentlich beschädigen zu können.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

Veralteter Name: backup-user

### Option für den Repository-Pfad (`--repo-path`) {#repository-path-option---repo-path}

Pfad zum Speichern von Backups und Archiv.

Im Repository speichert pgBackRest Backups und archiviert WAL-Segmente.

Der benötigte Speicherplatz lässt sich im Voraus oft schwer abschätzen. Am besten erstellen Sie einige Backups, erfassen die Größe verschiedener Backup-Typen (full/incr/diff) und messen die täglich erzeugte WAL-Menge. So erhalten Sie einen ungefähren Überblick über den Platzbedarf. Dieser wird sich im Laufe der Zeit mit der Entwicklung der Datenbank wahrscheinlich ändern.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### Option für den S3-Bucket des Repositorys (`--repo-s3-bucket`) {#s3-repository-bucket-option---repo-s3-bucket}

S3-Bucket des Repositorys.

S3-Bucket, in dem das Repository gespeichert wird.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Buckets gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von AWS erzeugte Inhalte im Bucket gespeichert werden können.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### Option für den S3-Endpunkt des Repositorys (`--repo-s3-endpoint`) {#s3-repository-endpoint-option---repo-s3-endpoint}

S3-Endpunkt des Repositorys.

Der AWS-Endpunkt sollte für die ausgewählte Region gültig sein.

Für angepasste Konfigurationen oder Tests können die Optionen `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port` und `repo-storage-verify-tls` hilfreich sein.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### Option für den S3-Schlüsseltyp des Repositorys (`--repo-s3-key-type`) {#s3-repository-key-type-option---repo-s3-key-type}

S3-Schlüsseltyp des Repositorys.

Die folgenden Autorisierungsarten werden unterstützt:

- `shared` - Gemeinsame Schlüssel
- `auto` - Temporäre Anmeldeinformationen automatisch abrufen
- `web-id` - Anmeldeinformationen für eine Web-Identität automatisch abrufen
- `pod-id` - Anmeldeinformationen für eine EKS-Pod-Identität automatisch abrufen
- `process` - Anmeldeinformationen durch Ausführen eines Prozesses abrufen

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### Option für die KMS-Schlüssel-ID des S3-Repositorys (`--repo-s3-kms-key-id`) {#s3-repository-kms-key-id-option---repo-s3-kms-key-id}

KMS-Schlüssel für das S3-Repository.

Aktiviert die serverseitige S3-Verschlüsselung mit dem angegebenen Schlüssel des AWS Key Management Service.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### Option für den S3-Authentifizierungsprozess (`--repo-s3-process-cmd`) {#s3-authentication-process-command-option---repo-s3-process-cmd}

Befehl für den S3-Authentifizierungsprozess.

Befehl mit optionalen Argumenten zum Abrufen temporärer S3-Anmeldeinformationen. Der erste Listeneintrag ist der Befehl; die übrigen Einträge werden als Parameter übergeben.

Der Prozess muss JSON mit den Feldern `AccessKeyId`, `SecretAccessKey`, `SessionToken` und `Expiration` ausgeben. Die Anmeldeinformationen werden vor ihrem Ablauf automatisch erneuert. Einzelheiten zum Format finden Sie unter [Anmeldeinformationen aus einem Prozess](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output).

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### Option für die S3-Region des Repositorys (`--repo-s3-region`) {#s3-repository-region-option---repo-s3-region}

S3-Region des Repositorys.

AWS-Region, in der der Bucket erstellt wurde.

```yaml
example: --repo1-s3-region=us-east-1
```

### Option für die Kostenübernahme durch den S3-Anforderer (`--repo-s3-requester-pays`) {#s3-repository-requestor-pays-option---repo-s3-requester-pays}

Kostenübernahme durch den Anforderer beim S3-Repository.

Aktiviert die S3-Kostenübernahme durch den Anforderer.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### Option für die S3-Rolle des Repositorys (`--repo-s3-role`) {#s3-repository-role-option---repo-s3-role}

S3-Rolle des Repositorys.

Name der AWS-Rolle (nicht der vollständige ARN) zum Abrufen temporärer Anmeldeinformationen bei `repo-s3-key-type=auto`.

```yaml
example: --repo1-s3-role=authrole
```

### Option für den S3-Dienst des Repositorys (`--repo-s3-service`) {#s3-repository-service-option---repo-s3-service}

S3-Signaturdienst.

Der bei der SigV4-Authentifizierung verwendete S3-Signaturdienst. Für standardmäßige S3-Endpunkte ist der Standardwert `s3`. Bei einem S3-Outposts-Endpunkt auf `s3-outposts` setzen.

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### Option für den STS-Endpunkt des S3-Repositorys (`--repo-s3-sts-host`) {#s3-repository-sts-endpoint-option---repo-s3-sts-host}

STS-Endpunkt des S3-Repositorys.

STS-Endpunkt zum Abrufen temporärer Anmeldeinformationen, wenn `repo-s3-key-type=web-id` konfiguriert ist. Einen regionalen Endpunkt wie `sts.us-east-1.amazonaws.com` angeben, um regionales STS zu verwenden. Dies kann für GovCloud, Regionen in China oder zur Verringerung der Latenz erforderlich sein.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### Option für den S3-URI-Stil des Repositorys (`--repo-s3-uri-style`) {#s3-repository-uri-style-option---repo-s3-uri-style}

S3-URI-Stil.

Folgende URI-Stile werden unterstützt:

- `host` - Mit dem Host `bucket.endpoint` verbinden.
- `path` - Mit dem Host `endpoint` verbinden und den Bucket den URIs voranstellen.

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### Option für den SFTP-Host des Repositorys (`--repo-sftp-host`) {#sftp-repository-host-option---repo-sftp-host}

SFTP-Host des Repositorys.

SFTP-Host, auf dem sich das Repository befindet.

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### Option für den Fingerabdruck des SFTP-Hosts (`--repo-sftp-host-fingerprint`) {#sftp-repository-host-fingerprint-option---repo-sftp-host-fingerprint}

Fingerabdruck des SFTP-Hosts des Repositorys.

Die Erzeugung des Fingerabdrucks für den SFTP-Host des Repositorys sollte `repo-sftp-host-key-hash-type` entsprechen. Den Fingerabdruck mit `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b` erzeugen. Die SSH-Hostschlüssel befinden sich normalerweise im Verzeichnis `/etc/ssh`.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### Option für die SFTP-Hostschlüsselprüfung (`--repo-sftp-host-key-check-type`) {#sftp-host-key-check-type-option---repo-sftp-host-key-check-type}

Art der SFTP-Hostschlüsselprüfung.

Die folgenden Arten der SFTP-Hostschlüsselprüfung werden unterstützt:

- `strict` - pgBackRest fügt niemals automatisch Hostschlüssel zur Datei ~/.ssh/known_hosts hinzu und verweigert Verbindungen zu Hosts, deren Hostschlüssel geändert wurde oder in den Dateien mit bekannten Hosts fehlt. Bei dieser Option muss der Benutzer alle neuen Hosts manuell hinzufügen.
- `accept-new` - pgBackRest fügt neue Hostschlüssel automatisch zur Datei mit bekannten Hosts des Benutzers hinzu, lässt aber keine Verbindungen zu Hosts mit geändertem Hostschlüssel zu.
- `fingerprint` - pgBackRest prüft den Hostschlüssel anhand des mit `repo-sftp-host-fingerprint` angegebenen Fingerabdrucks.
- `none` - Es wird keine Hostschlüsselprüfung durchgeführt.

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### Option für den Hash-Typ des SFTP-Hostschlüssels (`--repo-sftp-host-key-hash-type`) {#sftp-repository-host-key-hash-type-option---repo-sftp-host-key-hash-type}

Hash-Typ des SFTP-Hostschlüssels für das Repository.

Legt den Hash-Typ fest, mit dem beim SSH-Verbindungsaufbau der Hashwert des Hostschlüssels des entfernten Systems berechnet wird. Zulässige Werte sind `md5`, `sha1` und `sha256`, wobei `sha256` nur von neueren Versionen von `libssh2` unterstützt wird.

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### Option für den Port des SFTP-Hosts (`--repo-sftp-host-port`) {#sftp-repository-host-port-option---repo-sftp-host-port}

Port des SFTP-Hosts für das Repository.

Port des SFTP-Hosts für das Repository.

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### Option für den Benutzer auf dem SFTP-Host (`--repo-sftp-host-user`) {#sftp-repository-host-user-option---repo-sftp-host-user}

Benutzer auf dem SFTP-Host für das Repository.

Benutzer auf dem Host, auf dem das Repository gespeichert wird.

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### Option für die Datei bekannter SFTP-Hosts (`--repo-sftp-known-host`) {#sftp-known-hosts-file-option---repo-sftp-known-host}

Datei mit bekannten SFTP-Hosts.

Datei mit bekannten Hosts, in der bei der Authentifizierung nach einem passenden SFTP-Host gesucht wird. Ohne Angabe durchsucht pgBackRest standardmäßig `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts` und `/etc/ssh/ssh_known_hosts2`. Sind ein oder mehrere Dateipfade konfiguriert, durchsucht pgBackRest diese nach einem passenden Eintrag. Dateipfade müssen vollständig sein oder mit einer Tilde beginnen. Die Option `repo-sftp-known-host` kann mehrfach angegeben werden, um mehrere Dateien mit bekannten Hosts zu durchsuchen. Für die Prüfung anhand dieser Dateien darf `repo-sftp-host-fingerprint` nicht angegeben sein. Siehe auch die Option `repo-sftp-host-check-type`.

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### Option für die private SFTP-Schlüsseldatei (`--repo-sftp-private-key-file`) {#sftp-repository-private-key-file-option---repo-sftp-private-key-file}

Datei mit dem privaten SFTP-Schlüssel.

Datei mit dem privaten SFTP-Schlüssel zur Authentifizierung.

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### Option für die öffentliche SFTP-Schlüsseldatei (`--repo-sftp-public-key-file`) {#sftp-repository-public-key-file-option---repo-sftp-public-key-file}

Datei mit dem öffentlichen SFTP-Schlüssel.

Datei mit dem öffentlichen SFTP-Schlüssel zur Authentifizierung. Bei einer gegen OpenSSL kompilierten Version optional, bei einer gegen eine andere Bibliothek kompilierten Version erforderlich.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Option für die CA-Datei des Repository-Speichers (`--repo-storage-ca-file`) {#repository-storage-ca-file-option---repo-storage-ca-file}

CA-Datei für den Repository-Speicher.

Für Zertifikate des Speicherdienstes (z. B. S3 oder Azure) eine andere als die systemweite CA-Datei verwenden.

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Veraltete Namen: repo-azure-ca-file, repo-s3-ca-file

### Option für den TLS-CA-Pfad des Repository-Speichers (`--repo-storage-ca-path`) {#repository-storage-tls-ca-path-option---repo-storage-ca-path}

CA-Pfad für den Repository-Speicher.

Für Zertifikate des Speicherdienstes (z. B. S3 oder Azure) einen anderen als den systemweiten CA-Pfad verwenden.

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

Veraltete Namen: repo-azure-ca-path, repo-s3-ca-path

### Option für den Host des Repository-Speichers (`--repo-storage-host`) {#repository-storage-host-option---repo-storage-host}

Host des Repository-Speichers.

Mit einem anderen Host als dem Endpunkt des Speicherdienstes (z. B. S3 oder Azure) verbinden. Dies wird üblicherweise für Tests verwendet.

```yaml
example: --repo1-storage-host=127.0.0.1
```

Veraltete Namen: repo-azure-host, repo-s3-host

### Option für den Port des Repository-Speichers (`--repo-storage-port`) {#repository-storage-port-option---repo-storage-port}

Port des Repository-Speichers.

Port für Verbindungen zum Endpunkt des Speicherdienstes (z. B. S3 oder Azure) oder zum angegebenen Host.

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

Veraltete Namen: repo-azure-port, repo-s3-port

### Option für das Vorabladen aus dem Repository-Speicher (`--repo-storage-prefetch`) {#repository-storage-prefetch-option---repo-storage-prefetch}

Vorabladen aus dem Repository-Speicher.

Bestimmt die Anzahl der vorab gesendeten Anfragen beim Lesen aus Objektspeichern wie S3. Dies ist keine echte Nebenläufigkeit, verringert aber die Latenz beim Senden der Anfragen.

Die Anzahl offener Anfragen pro Lesevorgang ist um eins höher als der Vorabladewert, da die erste Leseanfrage nicht vorab gesendet werden kann.

```yaml
default: 3
allowed: [0, 1024]
example: --repo1-storage-prefetch=7
```

### Option zum Überlesen im Repository-Speicher (`--repo-storage-read-over`) {#repository-storage-read-over-option---repo-storage-read-over}

Überlesen im Repository-Speicher.

Bündel können Daten enthalten, die bei der Wiederherstellung nicht benötigt werden, etwa bereits vorhandene Dateien. Diese Option überspringt unnötige Daten durch fortgesetztes Lesen, ohne eine neue Leseanfrage an den Objektspeicher zu senden. Das ist in der Regel schneller, da eine neue Leseanfrage eine höhere Latenz verursacht als das Fortsetzen eines laufenden Lesevorgangs. Für die meisten Speicherklassen ist es auch kostengünstiger.

```yaml
default: 64KiB
allowed: [0B, 1MiB]
example: --repo1-storage-read-over=128KiB
```

### Option für Tags im Repository-Speicher (`--repo-storage-tag`) {#repository-storage-tag-option---repo-storage-tag}

Tags für den Repository-Speicher.

Tags angeben, die Objekten hinzugefügt werden, wenn das Repository ein Objektspeicher wie S3 ist. Die Option kann wiederholt werden, um mehrere Tags hinzuzufügen.

pgBackRest bietet keine Möglichkeit, diese Tags zu ändern. Deshalb sollten sie vor dem Ausführen von `stanza-create` korrekt gesetzt werden, damit die Tags im gesamten Repository einheitlich sind.

```yaml
example: --repo1-storage-tag=key1=value1
```

### Option für die Upload-Blockgröße des Repository-Speichers (`--repo-storage-upload-chunk-size`) {#repository-storage-upload-chunk-size-option---repo-storage-upload-chunk-size}

Blockgröße für Uploads in den Repository-Speicher.

Objektspeicher wie S3 erlauben das Hochladen von Dateien in Blöcken, wenn die Datei zu groß für den Arbeitsspeicher ist. Auch wenn die Datei in den Arbeitsspeicher passt, ist es speichereffizienter, den für Uploads verwendeten Speicher zu begrenzen.

Eine größere Blockgröße verbessert im Allgemeinen die Leistung, da sie die Anzahl der Upload-Anfragen verringert und es ermöglicht, mehr Dateien jeweils in einer einzelnen Anfrage statt in Blöcken hochzuladen. Nachteilig ist der höhere Speicherverbrauch. Da für jeden Prozess ein eigener Blockpuffer zugewiesen werden muss, erhöhen größere Werte für `process-max` den gesamten Speicherverbrauch zusätzlich.

Die zulässigen Blockgrößen unterscheiden sich je nach Speichertyp und Plattform. Beispielsweise beträgt die Mindestblockgröße bei AWS S3 5MiB. Auch die Bezeichnung variiert: Bei der Suche nach Mindest- und Höchstwerten für AWS S3 nach „part size“, für GCS nach „chunk size“ und für Azure nach „block size“ suchen.

Ist eine Datei größer als 1GiB (die maximale Dateigröße, die PostgreSQL standardmäßig erzeugt), wird die Blockgröße schrittweise bis zum zulässigen Maximum erhöht, um den Datei-Upload abzuschließen.

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### Option zur Zertifikatprüfung des Repository-Speichers (`--repo-storage-verify-tls`) {#repository-storage-certificate-verify-option---repo-storage-verify-tls}

Zertifikatprüfung für den Repository-Speicher.

Mit dieser Option lässt sich die Prüfung des TLS-Serverzertifikats des Speicherdienstes (z. B. S3 oder Azure) aktivieren oder deaktivieren. Die Prüfung sollte nur für Tests oder andere Situationen mit selbstsignierten Zertifikaten deaktiviert werden.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

Veraltete Namen: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

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

```yaml
default: posix
example: --repo1-type=cifs
```

## Stanza-Optionen {#stanza-options}

### Option für die PostgreSQL-Datenbank (`--pg-database`) {#postgresql-database-option---pg-database}

PostgreSQL-Datenbank.

Name der Datenbank für Verbindungen zu PostgreSQL. Meist ist der Standardwert die beste Wahl, doch manche Installationen enthalten diese Datenbank möglicherweise nicht.

Aus Kompatibilitätsgründen wird die Umgebungsvariable `PGDATABASE` ignoriert.

```yaml
default: postgres
example: --pg1-database=backupdb
```

### Option für den PostgreSQL-Host (`--pg-host`) {#postgresql-host-option---pg-host}

PostgreSQL-Host für die Ausführung auf einem entfernten System.

Für Backups, bei denen PostgreSQL-Host und Repository-Host unterschiedliche Systeme sind.

```yaml
example: --pg1-host=db.domain.com
```

Veralteter Name: db-host

### Option für die CA-Datei des PostgreSQL-Hosts (`--pg-host-ca-file`) {#postgresql-host-certificate-authority-file-option---pg-host-ca-file}

Datei mit den Zertifizierungsstellen für den PostgreSQL-Host.

Für Verbindungen zum PostgreSQL-Host eine andere als die systemweite CA-Datei verwenden.

```yaml
example: --pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Option für den CA-Pfad des PostgreSQL-Hosts (`--pg-host-ca-path`) {#postgresql-host-certificate-authority-path-option---pg-host-ca-path}

Pfad mit den Zertifizierungsstellen für den PostgreSQL-Host.

Für Verbindungen zum PostgreSQL-Host einen anderen als den systemweiten CA-Pfad verwenden.

```yaml
example: --pg1-host-ca-path=/etc/pki/tls/certs
```

### Option für die Zertifikatdatei des PostgreSQL-Hosts (`--pg-host-cert-file`) {#postgresql-host-certificate-file-option---pg-host-cert-file}

Zertifikatdatei für den PostgreSQL-Host.

Wird an den PostgreSQL-Host gesendet, um die Identität des Clients nachzuweisen.

```yaml
example: --pg1-host-cert-file=/path/to/client.crt
```

### Option für den Befehl auf dem PostgreSQL-Host (`--pg-host-cmd`) {#postgresql-host-command-option---pg-host-cmd}

pgBackRest-Befehl auf dem PostgreSQL-Host.

Nur erforderlich, wenn der Pfad zum pgBackRest-Befehl auf dem lokalen und dem PostgreSQL-Host unterschiedlich ist. Ohne Angabe wird auf dem PostgreSQL-Host derselbe Befehl wie lokal verwendet.

```yaml
default: [path of executed pgbackrest binary]
example: --pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Veralteter Name: db-cmd

### Option für die Konfiguration des PostgreSQL-Hosts (`--pg-host-config`) {#postgresql-host-configuration-option---pg-host-config}

pgBackRest-Konfigurationsdatei auf dem Datenbank-Host.

Legt den Speicherort der Konfigurationsdatei auf dem PostgreSQL-Host fest. Dies ist nur erforderlich, wenn die Datei dort an einem anderen Ort liegt als die lokale Konfigurationsdatei.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Veralteter Name: db-config

### Option für zusätzliche Konfigurationsdateien auf dem PostgreSQL-Host (`--pg-host-config-include-path`) {#postgresql-host-configuration-include-path-option---pg-host-config-include-path}

Pfad zu zusätzlichen pgBackRest-Konfigurationsdateien auf dem Datenbank-Host.

Legt den Pfad für zusätzliche Konfigurationsdateien auf dem PostgreSQL-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem PostgreSQL-Host vom entsprechenden lokalen Pfad abweicht.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Option für den Konfigurationspfad des PostgreSQL-Hosts (`--pg-host-config-path`) {#postgresql-host-configuration-path-option---pg-host-config-path}

pgBackRest-Konfigurationspfad auf dem Datenbank-Host.

Legt den Konfigurationspfad auf dem PostgreSQL-Host fest. Dies ist nur erforderlich, wenn dieser Pfad auf dem PostgreSQL-Host vom lokalen Konfigurationspfad abweicht.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --pg1-host-config-path=/conf/pgbackrest
```

### Option für die Schlüsseldatei des PostgreSQL-Hosts (`--pg-host-key-file`) {#postgresql-host-key-file-option---pg-host-key-file}

Schlüsseldatei für den PostgreSQL-Host.

Weist nach, dass das Client-Zertifikat von seinem Eigentümer gesendet wurde.

```yaml
example: --pg1-host-key-file=/path/to/client.key
```

### Option für den Port des PostgreSQL-Hosts (`--pg-host-port`) {#postgresql-host-port-option---pg-host-port}

Port des PostgreSQL-Hosts, wenn `pg-host` gesetzt ist.

Mit dieser Option einen anderen als den Standardport für das Protokoll des PostgreSQL-Hosts angeben.

> **HINWEIS:** Bei `pg-host-type=ssh` gibt es keinen Standardwert für `pg-host-port`. In diesem Fall wird der Port verwendet, der für den durch `cmd-ssh` angegebenen Befehl konfiguriert ist.

```yaml
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: --pg1-host-port=25
```

Veralteter Name: db-ssh-port

### Option für den Protokolltyp des PostgreSQL-Hosts (`--pg-host-type`) {#postgresql-host-protocol-type-option---pg-host-type}

Protokolltyp für den PostgreSQL-Host.

Die folgenden Protokolltypen werden unterstützt:

- `ssh` - Secure Shell.
- `tls` - pgBackRest-TLS-Server.

```yaml
default: ssh
example: --pg1-host-type=tls
```

### Option für den Benutzer auf dem PostgreSQL-Host (`--pg-host-user`) {#postgresql-host-user-option---pg-host-user}

Anmeldebenutzer auf dem PostgreSQL-Host, wenn `pg-host` gesetzt ist.

Unter diesem Benutzer läuft auch der entfernte pgBackRest-Prozess, und er baut die Verbindungen zu PostgreSQL auf. Damit dies korrekt funktioniert, sollte er Eigentümer des PostgreSQL-Datenbankclusters sein. Üblicherweise ist dies `postgres`, der Standardwert.

```yaml
default: postgres
example: --pg1-host-user=db_owner
```

Veralteter Name: db-user

### Option für den PostgreSQL-Pfad (`--pg-path`) {#postgresql-path-option---pg-path}

PostgreSQL-Datenverzeichnis.

Dieser Pfad sollte dem von PostgreSQL gemeldeten `data_directory` entsprechen. Obwohl sich der Wert an verschiedenen Stellen auslesen lässt, ist eine ausdrückliche Angabe ratsam, falls diese Quellen bei einer Wiederherstellung oder einem Offline-Backup nicht verfügbar sind.

Bei jedem Online-Backup wird `pg-path` mit dem von PostgreSQL gemeldeten Wert verglichen. Die Option sollte daher immer aktuell sein.

```yaml
example: --pg1-path=/data/db
```

Veralteter Name: db-path

### Option für den PostgreSQL-Port (`--pg-port`) {#postgresql-port-option---pg-port}

PostgreSQL-Port.

Port, auf dem PostgreSQL läuft. Dieser muss normalerweise nicht angegeben werden, da die meisten PostgreSQL-Cluster den Standardport verwenden.

```yaml
default: 5432
allowed: [0, 65535]
example: --pg1-port=6543
```

Veralteter Name: db-port

### Option für den PostgreSQL-Socket-Pfad (`--pg-socket-path`) {#postgresql-socket-path-option---pg-socket-path}

Pfad zum PostgreSQL-Unix-Socket.

Das beim Start von PostgreSQL angegebene Unix-Socket-Verzeichnis. pgBackRest sucht automatisch am üblichen Speicherort des Betriebssystems. Diese Einstellung ist daher normalerweise nur erforderlich, wenn das Socket-Verzeichnis ausdrücklich über `unix_socket_directories` in `postgresql.conf` geändert wurde.

```yaml
example: --pg1-socket-path=/var/run/postgresql
```

Veralteter Name: db-socket-path

### Option für den PostgreSQL-Datenbankbenutzer (`--pg-user`) {#postgresql-database-user-option---pg-user}

PostgreSQL-Datenbankbenutzer.

Datenbankbenutzername für Verbindungen zu PostgreSQL. Ohne Angabe verbindet sich pgBackRest mit dem lokalen Betriebssystembenutzer oder mit `PGUSER`.

```yaml
example: --pg1-user=backupuser
```
