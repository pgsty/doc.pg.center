---
title: "Download und Installation"
linkTitle: "Download & Installation"
weight: 20
description: "Offizielle Releases, Pakete, Anforderungen und Installation aus dem Quellcode"
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutorial]
aliases: [/docs/pgbadger/download/]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## Verteilungskanal auswählen {#distribution-channels}

| Kanal | Verwendungszweck | Bezugsquelle |
|---|---|---|
| Offizielles Release | Quellcode-Tarballs und Versionshinweise | [GitHub Releases](https://github.com/darold/pgbadger/releases) |
| RPM-Paket | RPM-basierte Linux-Distributionen | [PostgreSQL Yum Repository](https://yum.postgresql.org/packages/) |
| Debian/Ubuntu-Paket | APT-basierte Linux-Distributionen | [PostgreSQL Apt Repository](https://wiki.postgresql.org/wiki/Apt) |
| Entwicklungsquelle | Aktueller, noch nicht veröffentlichter Code | [darold/pgbadger](https://github.com/darold/pgbadger) |

Der Dokumentations-Snapshot auf dieser Website basiert auf dem Quellcode der Version 13.2. Prüfen Sie vor dem Herunterladen stets die Releaseseite: Der lokale Snapshot ist bewusst fixiert, während das Originalprojekt weiterhin neue Versionen veröffentlicht.

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

## Aus einem offiziellen Tarball installieren {#install-from-tarball}

Laden Sie ein Release-Archiv herunter, bauen Sie es anschließend mit den Standardwerkzeugen von Perl und installieren Sie es:

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
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

## Entwicklungsstand installieren {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Der Entwicklungsstand kann Änderungen enthalten, die noch nicht in den Versionshinweisen dokumentiert sind. Verwenden Sie für reproduzierbare Produktionspakete vorzugsweise ein mit einem Versions-Tag versehenes Archiv.

## Installation überprüfen {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Fahren Sie mit der [Befehlszeilenreferenz](command-line/) und der [Konfiguration der PostgreSQL-Protokollierung](postgresql-logging/) fort.
