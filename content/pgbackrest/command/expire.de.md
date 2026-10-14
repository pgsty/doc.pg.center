---
title: "Befehl zum Entfernen abgelaufener Backups (expire)"
linkTitle: "expire"
weight: 60
description: "Referenz zu den Optionen und zum Verhalten des pgBackRest-Befehls `expire`."
icon: fa-solid fa-hourglass-end
module: [PGBACKREST]
categories: [Referenz]
upstream_link: "https://pgbackrest.org/command.html#command-expire"
---

pgBackRest rotiert vollständige Backups je nach Art der Aufbewahrung anhand einer Anzahl oder eines Zeitraums. Bei einer Anzahl richtet sich die Bereinigung danach, wie viele Backups aufbewahrt werden müssen, nicht nach ihrem Erstellungszeitpunkt. Differenzielle Backups werden anhand ihrer Anzahl aufbewahrt, aber immer entfernt, sobald das vollständige Backup entfernt wird, von dem sie abhängen. Inkrementelle Backups werden nie eigenständig anhand von Aufbewahrungsregeln entfernt, sondern immer zusammen mit dem zugehörigen vollständigen oder differenziellen Backup. Einzelheiten und Beispiele finden Sie unter [Aufbewahrung vollständiger Backups](/de/pgbackrest/user-guide/#full-backup-retention) und [Aufbewahrung differenzieller Backups](/de/pgbackrest/user-guide/#differential-backup-retention).

Archiviertes WAL bleibt standardmäßig für noch nicht entfernte Backups erhalten. Mit den retention-archive-Optionen lässt sich dies pro Repository ändern, was jedoch nicht empfohlen wird. Einzelheiten und Beispiele finden Sie unter [Archivaufbewahrung](/de/pgbackrest/user-guide/#archive-retention).

Der Befehl `expire` läuft automatisch nach jedem erfolgreichen Backup und kann auch vom Benutzer ausgeführt werden. Bei manueller Ausführung erfolgt die Bereinigung gemäß den Aufbewahrungseinstellungen jedes konfigurierten Repositorys. Mit `--repo` wird nur das angegebene Repository bereinigt. Der Benutzer kann die Bereinigung mit `--set` auf einen bestimmten Backup-Satz begrenzen. Ohne `--repo` werden dabei alle Repositorys durchsucht und alle passenden Backup-Sätze entfernt. Bei jeder Ausführung von `expire` werden außerdem die Regeln zur Archivaufbewahrung geprüft und angewendet.

## Befehlsoptionen {#command-options}

### Option zum Entfernen älterer Archivsegmente (`--archive-expire-before`) {#expire-archive-before-option---archive-expire-before}

WAL-Archiv vor dem angegebenen WAL-Segment entfernen.

WAL-Segmente vor dem angegebenen Segment entfernen, jedoch nur, wenn sie von keinem aufbewahrten Backup benötigt werden. Dies sind Segmente vor dem frühesten aufzubewahrenden Backup-Satz oder beliebige Segmente, wenn das Repository kein Backup enthält. Das angegebene Segment und alle nachfolgenden bleiben erhalten. Dies entspricht dem Wert, den PostgreSQL über `%r` an archive_cleanup_command übergibt.

Diese Option ist vor allem für reine Archiv-Repositorys ohne Backups vorgesehen. Sie kann auch Speicherplatz im WAL-Archiv für Segmente vor dem ersten Backup freigeben, wenn die Aufbewahrungsbedingungen für vollständige Backups noch nicht erfüllt sind und deshalb keine Archivbereinigung ausgelöst wird.

```yaml
example: --archive-expire-before=000000010000000000000010
```

### Option zum Entfernen des ältesten Backup-Satzes (`--oldest`) {#oldest-option---oldest}

Den ältesten entfernbaren Backup-Satz entfernen.

Entfernt den ältesten vollständigen Backup-Satz, der gelöscht werden kann, wobei mindestens ein neueres vollständiges Backup verbleibt. Dies entspricht einer manuellen Verringerung der Aufbewahrungsanzahl um eins, wird aber automatisch berechnet. Alle zugehörigen differenziellen und inkrementellen Backups werden ebenfalls entfernt.

Dabei wird auch die Archivaufbewahrung vorübergehend angepasst, damit WAL für die entfernten Backups im selben Lauf gelöscht werden kann.

Ist die Aufbewahrung vollständiger Backups zeitbasiert konfiguriert (mit `--repo-retention-full-type=time`), verwendet `--oldest` für diesen Lauf eine anzahlbasierte Bereinigung.

WARNUNG:

Diese Option kann nicht mit `--set` kombiniert werden.

```yaml
default: n
example: --oldest
```

### Option zur Auswahl des Backup-Satzes (`--set`) {#set-option---set}

Zu entfernender Backup-Satz.

Der angegebene Backup-Satz, also das angegebene Backup-Label und gegebenenfalls alle davon abhängigen Backups, wird unabhängig von den Aufbewahrungsregeln entfernt. Mindestens ein vollständiges Backup muss jedoch im Repository verbleiben.

WARNUNG:

Diese Option mit äußerster Vorsicht verwenden: Für den angegebenen Backup-Satz entfernt sie dauerhaft alle Backups sowie alle Archive, die nicht für die Konsistenz eines Backups erforderlich sind, aus dem pgBackRest-Repository. Dies kann PITR unmöglich machen. Sind `--repo-retention-full` und/oder `--repo-retention-archive` konfiguriert, wird empfohlen, diese Werte während einer solchen außerplanmäßigen Bereinigung auf den Höchstwert zu setzen, um unbeabsichtigtes Entfernen von Archiven zu verhindern.

```yaml
example: --set=20150131-153358F_20150131-153401I
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

### Option für einen Probelauf (`--dry-run`) {#dry-run-option---dry-run}

Einen Probelauf des Befehls ausführen.

Die Option `--dry-run` ist nur in der Befehlszeile verfügbar. Mit ihr lässt sich ermitteln, welche Änderungen der Befehl vornehmen würde, ohne diese tatsächlich auszuführen.

```yaml
default: n
example: --dry-run
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

### Option für den Sperrdateipfad (`--lock-path`) {#lock-path-option---lock-path}

Pfad zum Speichern der Sperrdateien.

In diesem Pfad erstellt pgBackRest Sperrdateien, um die gleichzeitige Ausführung miteinander in Konflikt stehender Operationen zu verhindern.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
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

## Repository-Optionen {#repository-options}

### Option zur Auswahl des Repositorys (`--repo`) {#set-repository-option---repo}

Repository festlegen.

Legt das Repository fest, auf das ein Befehl wirken soll.

Damit kann beispielsweise eine Wiederherstellung aus einem bestimmten Repository durchgeführt werden, anstatt pgBackRest die Auswahl zu überlassen.

```yaml
allowed: [1, 256]
example: --repo=1
```

### Option für den Azure-Container des Repositorys (`--repo-azure-container`) {#azure-repository-container-option---repo-azure-container}

Azure-Repository-Container.

Azure-Container, der das Repository speichert.

pgBackRest-Repositorys können mit `repo-path=/` im Stammverzeichnis des Containers gespeichert werden. Meist ist jedoch ein Präfix wie `/repo` sinnvoll, damit auch Protokolle und andere von Azure erzeugte Inhalte im Container gespeichert werden können.

```yaml
example: --repo1-azure-container=pg-backup
```

### Option für den Azure-Schlüsseltyp des Repositorys (`--repo-azure-key-type`) {#azure-repository-key-type-option---repo-azure-key-type}

Azure-Repository-Schlüsseltyp.

Folgende Typen werden für die Autorisierung unterstützt:

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

Folgende Typen werden für die Autorisierung unterstützt:

- `auto` - Autorisierung mithilfe des Dienstkontos der Instanz.
- `service` - Dienstkonto anhand eines lokal gespeicherten Schlüssels.
- `token` - Für lokale Tests, z. B. `fakegcs`.

Wenn `repo-gcs-key-type=service` ist, werden die Anmeldeinformationen erneut geladen, wenn das Authentifizierungstoken erneuert wird.

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

### Option für die Archivaufbewahrung (`--repo-retention-archive`) {#archive-retention-option---repo-retention-archive}

Anzahl der Backups, für die lückenloses WAL aufbewahrt wird.

> **HINWEIS:** WAL-Segmente, die für ein konsistentes Backup erforderlich sind, bleiben unabhängig von dieser Einstellung immer bis zum Entfernen des Backups erhalten.

Ist dieser Wert nicht gesetzt und ist `repo-retention-full-type` auf `count` gesetzt (Standardeinstellung), richtet sich die Archivbereinigung nach `repo-retention-full` beziehungsweise `repo-retention-diff`, wenn `repo-retention-archive-type` auf `full` beziehungsweise `diff` gesetzt ist. So wird WAL nur für bereits entfernte Backups gelöscht. Ist `repo-retention-full-type` auf `time` gesetzt, werden standardmäßig Archive entfernt, die älter sind als das älteste vollständige Backup, das nach Anwendung von `repo-retention-full` aufbewahrt wird.

Diese Option muss gesetzt sein, wenn `repo-retention-archive-type` auf `incr` gesetzt ist. Bei knappem Speicherplatz kann sie zusammen mit `repo-retention-archive-type` verwendet werden, um WAL-Segmente frühzeitig zu entfernen. Damit ist jedoch keine PITR mehr aus Backups möglich, deren WAL entfernt wurde. Dies wird daher **nicht** empfohlen.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-archive=2
```

Veralteter Name: retention-archive

### Option für den Typ der Archivaufbewahrung (`--repo-retention-archive-type`) {#archive-retention-type-option---repo-retention-archive-type}

Backup-Typ für die WAL-Aufbewahrung.

Bei `full` bewahrt pgBackRest Archivprotokolle für die durch `repo-retention-archive` festgelegte Anzahl vollständiger Backups auf. Bei `diff` (differenziell) werden sie für die durch `repo-retention-archive` festgelegte Anzahl vollständiger und differenzieller Backups aufbewahrt. War das letzte Backup vollständig, wird es für repo-retention also als differenzielles Backup gezählt. Bei `incr` (inkrementell) bewahrt pgBackRest Archivprotokolle für die durch `repo-retention-archive` festgelegte Anzahl vollständiger, differenzieller und inkrementeller Backups auf. Es wird empfohlen, die Standardeinstellung beizubehalten, bei der WAL nur zusammen mit vollständigen Backups entfernt wird.

```yaml
default: full
example: --repo1-retention-archive-type=diff
```

Veralteter Name: retention-archive-type

### Option für die Aufbewahrung differenzieller Backups (`--repo-retention-diff`) {#differential-retention-option---repo-retention-diff}

Anzahl der aufzubewahrenden differenziellen Backups.

Wird ein differenzielles Backup entfernt, werden auch alle zugehörigen inkrementellen Backups entfernt. Ohne Angabe bleiben alle differenziellen Backups erhalten, bis die vollständigen Backups entfernt werden, von denen sie abhängen.

Bei der Bereinigung zählen vollständige Backups zur Anzahl der differenziellen Backups. Dadurch müssen in den meisten Fällen etwas weniger differenzielle Backups aufbewahrt werden.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-diff=3
```

Veralteter Name: retention-diff

### Option für die Aufbewahrung vollständiger Backups (`--repo-retention-full`) {#full-retention-option---repo-retention-full}

Anzahl oder Aufbewahrungsdauer vollständiger Backups.

Wird ein vollständiges Backup entfernt, werden auch alle zugehörigen differenziellen und inkrementellen Backups entfernt. Ist diese Option nicht gesetzt, wird eine Warnung ausgegeben. Für eine unbegrenzte Aufbewahrung die Option auf den Höchstwert setzen.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-full=2
```

Veralteter Name: retention-full

### Option für die Art der Aufbewahrung vollständiger Backups (`--repo-retention-full-type`) {#full-retention-type-option---repo-retention-full-type}

Art der Aufbewahrung vollständiger Backups.

Bestimmt, ob `repo-retention-full` einen Zeitraum in Tagen oder die Anzahl der aufzubewahrenden vollständigen Backups angibt.

Bei `time` werden vollständige Backups, die älter als `repo-retention-full` sind, aus dem Repository entfernt, wenn mindestens ein weiteres Backup vorhanden ist, dessen Alter mindestens dem Wert von `repo-retention-full` entspricht. Steht beispielsweise `repo-retention-full` auf 30 Tage und gibt es 2 vollständige Backups, eines 25 Tage und eines 35 Tage alt, wird keines entfernt. Würde das 35 Tage alte Backup entfernt, bliebe nur das 25 Tage alte übrig. Dies würde die Aufbewahrungsregel von 30 Tagen verletzen: Es muss mindestens ein 30 Tage altes Backup vorhanden sein, bevor ein älteres entfernt werden kann. Archiviertes WAL, das älter als das älteste verbleibende vollständige Backup ist, wird automatisch entfernt, sofern `repo-retention-archive-type` und `repo-retention-archive` nicht ausdrücklich gesetzt sind.

Bei `count` werden vollständige Backups entfernt, die über die durch `repo-retention-full` festgelegte Anzahl hinausgehen. Steht beispielsweise `repo-retention-full` auf `4` und wird ein fünftes vollständiges Backup abgeschlossen, wird das älteste entfernt, sodass die Anzahl bei 4 bleibt.

Ein Backup muss erfolgreich abgeschlossen sein, bevor es für die Aufbewahrung zählt. Steht beispielsweise `repo-retention-full-type` auf `count` und `repo-retention-full` auf `2`, müssen 3 abgeschlossene vollständige Backups vorhanden sein, bevor das älteste entfernt wird.

```yaml
default: count
example: --repo1-retention-full-type=time
```

### Option für die Aufbewahrung des Backup-Verlaufs (`--repo-retention-history`) {#backup-history-retention-option---repo-retention-history}

Aufbewahrungsdauer der Manifeste im Backup-Verlauf in Tagen.

Nach Abschluss eines Backups wird eine Kopie seines Manifests im Pfad `backup.history` gespeichert. Standardmäßig werden diese Dateien nie entfernt, da sie für Auswertungen nützlich sind, etwa um das Wachstum von Backups und WAL im Zeitverlauf zu messen.

Mit `repo-retention-history` die Anzahl der Tage festlegen, für die Manifeste im Backup-Verlauf aufbewahrt werden. Noch nicht entfernte Backups bleiben stets im Verlauf erhalten. Mit `repo-retention-history=0` wird der Verlauf nur für solche Backups aufbewahrt.

Wird das Verlaufsmanifest eines vollständigen Backups entfernt, werden auch die Verlaufsmanifeste aller zugehörigen differenziellen und inkrementellen Backups entfernt.

```yaml
allowed: [0, 9999999]
example: --repo1-retention-history=365
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

Die folgenden Typen werden unterstützt:

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

Hash-Typ des SFTP-Hostschlüssels für das Repository. Legt den Hash-Typ fest, mit dem beim SSH-Verbindungsaufbau der Hashwert des Hostschlüssels des entfernten Systems berechnet wird. Neuere Versionen von `libssh2` unterstützen neben md5 und sha1 auch `sha256`.

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

### Option für symbolische Links im Repository (`--repo-symlink`) {#repository-symlink-option---repo-symlink}

Symbolische Links innerhalb des Repositorys erstellen.

Aktiviert das Erstellen der symbolischen Links für `latest` und Tablespaces. Diese Links sind vor allem nützlich, wenn Snapshots für eine Recovery direkt im Repository verwendet werden, was selten vorkommt.

Obwohl diese Funktion für die meisten Benutzer wahrscheinlich nicht nützlich ist, bleibt sie aus Kompatibilitätsgründen standardmäßig aktiviert. Bei POSIX-ähnlichen Speichern ohne Unterstützung für symbolische Links kann es jedoch sinnvoll sein, sie zu deaktivieren.

```yaml
default: y
example: --no-repo1-symlink
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

```yaml
default: posix
example: --repo1-type=cifs
```
