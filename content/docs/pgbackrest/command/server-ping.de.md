---
title: "Server-Ping-Befehl (server-ping)"
linkTitle: "server-ping"
weight: 130
description: "Referenz zu den Optionen und zum Verhalten des pgBackRest-Befehls `server-ping`."
icon: fa-solid fa-heart-pulse
module: [PGBACKREST]
categories: [Referenz]
aliases: [/pgbackrest/command/server-ping/]
upstream_link: "https://pgbackrest.org/command.html#command-server-ping"
---

Einen pgBackRest-TLS-Server mit einem Ping darauf prüfen, ob er Verbindungen annimmt. Dabei wird nur geprüft, ob der Server reagiert; eine Authentifizierung findet nicht statt.

Wird in der Befehlszeile kein Host angegeben, wird die Option `tls-server-host` verwendet.

## Befehlsoptionen {#command-options}

### Option für die TLS-Serveradresse (`--tls-server-address`) {#tls-server-address-option---tls-server-address}

TLS-Serveradresse.

IP-Adresse, an der der Server auf Client-Anfragen wartet.

```yaml
default: localhost
example: --tls-server-address=*
```

### Option für den TLS-Serverport (`--tls-server-port`) {#tls-server-port-option---tls-server-port}

TLS-Serverport.

Port, an dem der Server auf Client-Anfragen wartet.

```yaml
default: 8432
allowed: [1, 65535]
example: --tls-server-port=8000
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

### Option für das I/O-Zeitlimit (`--io-timeout`) {#io-timeout-option---io-timeout}

I/O-Zeitlimit.

Zeitlimit in Sekunden für Verbindungen sowie Lese- und Schreiboperationen.

Die gesamte Lese- oder Schreiboperation muss nicht innerhalb dieses Zeitlimits abgeschlossen sein, aber es muss *irgendein* Fortschritt erzielt werden, selbst wenn es nur ein einziges Byte ist.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Option für die Prozesspriorität (`--priority`) {#set-process-priority-option---priority}

Prozesspriorität festlegen.

Legt fest, welche Priorität (also welcher nice-Wert) dem Prozess vom Kernel-Scheduler zugewiesen wird. Positive Werte verringern die Priorität, negative Werte erhöhen sie. In den meisten Fällen dürfen Prozesse ihre Priorität nicht erhöhen.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### Option für Keep-alive (`--sck-keep-alive`) {#keep-alive-option---sck-keep-alive}

Keep-alive aktivieren.

Aktiviert Keep-alive-Nachrichten auf Socket-Verbindungen.

```yaml
default: y
example: --no-sck-keep-alive
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

### Option für Zeitstempel im Protokoll (`--log-timestamp`) {#log-timestamp-option---log-timestamp}

Zeitstempel in der Protokollierung aktivieren.

Aktiviert Zeitstempel in der Konsolen- und Dateiprotokollierung. Diese Option wird in besonderen Situationen deaktiviert, etwa beim Erzeugen der Dokumentation.

```yaml
default: y
example: --no-log-timestamp
```
