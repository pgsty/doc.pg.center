---
title: "Fehler melden"
weight: 1400
description: "Fehlerberichte für das etcd-Projekt erstellen"
icon: fa-solid fa-bug
categories: [Aufgabe]
upstream_link: "https://github.com/etcd-io/website/blob/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7/reporting_bugs.md"
---

Fehler in einem Teil des etcd-Projekts oder in seiner Dokumentation bitte durch [Erstellen eines Issues][etcd-issue] melden. Wir nehmen Fehler und Mängel sehr ernst und halten kein Problem für zu klein. Vor dem Erstellen eines Fehlerberichts bitte prüfen, ob dasselbe Problem bereits gemeldet wurde.

Damit Fehlerberichte präzise und leicht verständlich sind, sollten sie möglichst folgende Eigenschaften haben:

- Konkret. Möglichst viele Einzelheiten angeben: Version, Umgebung, Konfiguration usw. Bei Fehlern im Betrieb des etcd-Servers bitte das etcd-Protokoll beifügen (besonders wichtig ist das Startprotokoll mit der etcd-Konfiguration).

- Reproduzierbar. Die Schritte zum Reproduzieren des Problems angeben. Wir wissen, dass sich manche Probleme nur schwer reproduzieren lassen; in solchen Fällen bitte die Schritte angeben, die zum Problem führen könnten. Wenn möglich, dem Fehlerbericht das betroffene etcd-Datenverzeichnis und den Stacktrace beifügen.

- Isoliert. Den Fehler möglichst mit einem Minimum an Abhängigkeiten isolieren und reproduzieren. Zu viele Abhängigkeiten in einem Fehlerbericht verlangsamen die Behebung erheblich. Die Fehlersuche in externen Systemen, die etcd verwenden, liegt außerhalb unseres Zuständigkeitsbereichs. Wir geben aber gern Hinweise zur weiteren Suche oder helfen bei der Verwendung von etcd selbst.

- Einmalig. Keine bereits vorhandenen Fehlerberichte duplizieren.

- Abgegrenzt. Pro Bericht nur einen Fehler melden. Keinen weiteren Fehler an einen bestehenden Bericht anhängen.

Vor dem Erstellen eines Fehlerberichts kann es hilfreich sein, [Elika Etemads Artikel über gute Fehlerberichte][filing-good-bugs] zu lesen.

Zur Eingrenzung eines Fehlers fragen wir möglicherweise nach weiteren Informationen. Doppelte Fehlerberichte werden geschlossen.

## Häufig gestellte Fragen {#frequently-asked-questions}

### Einen Stacktrace abrufen {#how-to-get-a-stack-trace}

``` bash
$ kill -QUIT $PID
```

### Die etcd-Version abrufen {#how-to-get-etcd-version}

``` bash
$ etcd --version
```

### etcd-Konfiguration und Protokoll beim Betrieb als systemd-Dienst ‘etcd2.service’ abrufen {#how-to-get-etcd-configuration-and-log-when-it-runs-as-systemd-service-etcd2service}

``` bash
$ sudo systemctl cat etcd2
$ sudo journalctl -u etcd2
```

Aufgrund eines Fehlers in systemd kann journald die letzten Protokollzeilen verlieren, wenn seine Prozesse enden. Wenn journalctl meldet, dass etcd ohne eine fatal- oder panic-Meldung beendet wurde, mit `sudo journalctl -f -t etcd2` versuchen, das vollständige Protokoll abzurufen.

[etcd-issue]: https://github.com/etcd-io/etcd/issues/new
[filing-good-bugs]: http://fantasai.inkedblade.net/style/talks/filing-good-bugs/
