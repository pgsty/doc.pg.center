---
title: "Download und Installation"
linkTitle: "Download & Installation"
weight: 20
description: "Offizielle Releases, Pakete, Anforderungen und Installation aus dem Quellcode"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutorial]
upstream_link: "https://github.com/darold/pgbadger/blob/0514893e97296695c77755fa36c59288c3afef3e/README.md"
upstream_name: "pgBadger README.md"
---

## Verteilungskanal auswählen {#distribution-channels}

| Kanal | Verwendungszweck | Bezugsquelle |
|---|---|---|
| Offizielles Release | Quellcode-Tarballs und Versionshinweise | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPM-Paket | RPM-basierte Linux-Distributionen | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Debian/Ubuntu-Paket | APT-basierte Linux-Distributionen | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| Entwicklungsquelle | Aktueller, noch nicht veröffentlichter Code | [darold/pgbadger](https://github.com/darold/pgbadger) |
{.wide .expand}

Die am 2026-11-21 überprüfte neueste stabile Version ist [pgBadger 13.3](https://github.com/darold/pgbadger/releases/tag/v13.3), veröffentlicht am 2026-11-03. Sowohl das folgende Beispiel mit dem Release-Archiv als auch der unten fixierte Checkout installieren diese dokumentierte Version.

## Anforderungen {#requirements}

Für HTML-Berichte benötigen Sie lediglich:

- eine aktuelle Perl-Installation;
- einen Webbrowser zur Darstellung der eingebetteten JavaScript-Diagramme.

Für optionale Funktionen benötigen Sie die folgenden Abhängigkeiten:

| Funktion | Abhängigkeit |
|---|---|
| PostgreSQL-Protokolle im CSV-Format analysieren | `Text::CSV_XS` |
| JSON-Ausgaben erzeugen | `JSON::XS` |
| Lesen von Eingabedateien mit der Endung `.gz`, `.bz2`, `.lz4`, `.xz`, `.zip` oder `.zst` | das jeweils passende Hilfsprogramm `zcat`, `bzcat`, `lz4cat`, `xz`, `unzip` oder `zstdcat` |

Installieren Sie die JSON-Unterstützung unter Debian oder Ubuntu:

```console
$ sudo apt-get install libjson-xs-perl
```

Auf einem RPM-basierten System:

```console
$ sudo yum install perl-JSON-XS
```

Verwenden Sie `--zcat`, um den Pfad zum Dekomprimierungsprogramm zu überschreiben. Wenn Sie einen benutzerdefinierten Befehl angeben, können Sie innerhalb desselben Aufrufs keine unterschiedlichen Komprimierungsformate mischen.

Das Hilfsprogramm `xz` muss `--robot` unterstützen, damit pgBadger die Archivmetadaten lesen kann. Komprimieren Sie lz4-Protokolle mit `--content-size`, damit pgBadger ihre unkomprimierte Größe bestimmen kann.

## Aus einem offiziellen Tarball installieren {#install-from-tarball}

Laden Sie ein Release-Archiv herunter, bauen Sie es anschließend mit den Standardwerkzeugen von Perl und installieren Sie es:

```console
$ tar xzf pgbadger-13.3.tar.gz
$ cd pgbadger-13.3
$ perl Makefile.PL
$ make
$ sudo make install
```

Das standardmäßige `site`-Layout installiert das Programm als `/usr/local/bin/pgbadger` und die Handbuchseite als `/usr/local/share/man/man1/pgbadger.1`.

Für eine distributionskonforme Installation unter `/usr` erzeugen Sie das Makefile mit:

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

`INSTALLDIRS=perl` ist ein weiteres vom Originalprojekt unterstütztes Layout. Prüfen Sie die erzeugten Pfade, bevor Sie die Software auf einem verwalteten System installieren.

## Aus der fixierten Quelle installieren {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ git checkout --detach 0514893e97296695c77755fa36c59288c3afef3e
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Dieser Checkout entspricht der [dokumentierten Version v13.3](https://github.com/darold/pgbadger/releases/tag/v13.3), fixiert auf `0514893e97296695c77755fa36c59288c3afef3e`.

## Installation überprüfen {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Fahren Sie mit der [Befehlszeilenreferenz](/de/pgbadger/command-line/) und der [Konfiguration der PostgreSQL-Protokollierung](/de/pgbadger/postgresql-logging/) fort.
