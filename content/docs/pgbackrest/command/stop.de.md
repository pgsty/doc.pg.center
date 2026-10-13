---
title: "Stoppbefehl (stop)"
linkTitle: "stop"
weight: 180
description: "Referenz zu den Optionen und zum Verhalten des pgBackRest-Befehls `stop`."
icon: fa-solid fa-stop
module: [PGBACKREST]
categories: [Referenz]
aliases: [/pgbackrest/command/stop/]
upstream_link: "https://pgbackrest.org/command.html#command-stop"
---

Verhindert die Ausführung neuer pgBackRest-Prozesse. Standardmäßig dürfen laufende Prozesse erfolgreich abgeschlossen werden. Mit der Option `--force` werden laufende Prozesse beendet.

pgBackRest-Prozesse geben einen Fehler zurück, wenn sie nach Abschluss des Stoppbefehls ausgeführt werden. Weitere Informationen und Beispiele finden Sie unter [Starten und Stoppen](/de/docs/pgbackrest/user-guide/#starting-and-stopping).

## Befehlsoptionen {#command-options}

### Option zum Erzwingen (`--force`) {#force-option---force}

Das Stoppen aller pgBackRest-Prozesse erzwingen.

Diese Option sendet TERM-Signale an alle laufenden pgBackRest-Prozesse, um ein geordnetes, aber sofortiges Herunterfahren auszulösen. Sie beendet auch Prozesse, die auf einem anderen System gestartet wurden, deren entfernte Teilprozesse aber auf dem aktuellen System laufen. Wurde beispielsweise ein Backup auf dem Backup-Server gestartet, beendet `stop --force` auf dem Datenbankserver auch den Backup-Prozess auf dem Backup-Server.

```yaml
default: n
example: --force
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

### Option für die Stanza (`--stanza`) {#stanza-option---stanza}

Definiert die Stanza.

Eine Stanza ist die Konfiguration eines PostgreSQL-Datenbankclusters. Sie legt unter anderem dessen Speicherort, das Backup-Verfahren und die Archivierungsoptionen fest. Die meisten Datenbankserver haben nur einen PostgreSQL-Datenbankcluster und daher nur eine Stanza. Backup-Server haben dagegen für jeden zu sichernden Datenbankcluster eine Stanza.

Es liegt nahe, die Stanza nach dem Primärcluster zu benennen. Ein besserer Name beschreibt jedoch die im Cluster enthaltenen Datenbanken. Da der Stanza-Name für den Primärserver und alle Replikate verwendet wird, sollte er die tatsächliche Funktion des Clusters beschreiben, etwa app oder dw, statt den lokalen Clusternamen wie main oder prod zu übernehmen.

```yaml
example: --stanza=main
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
