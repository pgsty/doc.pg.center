---
title: "PgBouncer kompilieren und installieren"
linkTitle: "Installieren"
weight: 40
description: "Anleitung zum Kompilieren und Installieren von PgBouncer"
icon: fa-solid fa-cloud-arrow-down
module: [PGBOUNCER]
categories: [Tutorial]
upstream_link: "https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/README.md"
---

--------

## Kompilieren {#building}

PgBouncer kann entweder mit dem Autoconf-basierten Build-System oder mit dem
neueren, noch experimentellen Build-System [Meson] kompiliert werden.
Für produktive Builds und die Paketerstellung wird derzeit Autoconf empfohlen.
Voraussichtlich wird Meson in einer künftigen Version zum Standard und Autoconf
entfernt. Daher sind Tests des Meson-Builds und Berichte über Probleme sehr willkommen.
Für das Kompilieren werden einige Komponenten benötigt:

* [Libevent] 2.0+
* [pkg-config]
* [OpenSSL] 1.0.1+ für TLS-Unterstützung
* ein C-Compiler mit C11-Unterstützung
* (optional) [c-ares] als Alternative zu evdns von Libevent
* (optional) LDAP-Bibliotheken
* (optional) PAM-Bibliotheken

Der Meson-Build benötigt zusätzlich [Meson] 0.58+ und [Ninja], der
Autoconf-Build [GNU Make] 3.81+.

[Meson]: https://mesonbuild.com/
[Ninja]: https://ninja-build.org/
[GNU Make]: https://www.gnu.org/software/make/
[Libevent]: http://libevent.org/
[pkg-config]: https://www.freedesktop.org/wiki/Software/pkg-config/
[OpenSSL]: https://www.openssl.org/
[c-ares]: http://c-ares.haxx.se/

Wenn alle Abhängigkeiten installiert sind, mit Autoconf kompilieren:

    $ ./configure --prefix=/usr/local
    $ make
    $ make install

oder mit Meson (experimentell):

    $ meson setup build --prefix=/usr/local
    $ meson compile -C build
    $ meson install -C build

Wenn Sie PgBouncer direkt aus dem Git-Repository oder für Windows kompilieren, beachten Sie die entsprechenden Anleitungen weiter unten.

--------

## Unterstützung für DNS-Abfragen {#dns-lookup-support}

PgBouncer löst Hostnamen beim Verbindungsaufbau auf und nicht nur einmal beim Einlesen der Konfiguration. Dafür ist eine asynchrone DNS-Implementierung erforderlich. Die folgende Tabelle zeigt die unterstützten Backends und die Reihenfolge, in der sie geprüft werden:

| Backend                    | Parallel | EDNS0 (1) | /etc/hosts | SOA-Abfrage (2) | Hinweis                                  |
|----------------------------|----------|-----------|------------|------------------|------------------------------------------|
| c-ares                     | ja       | ja        | ja         | ja               | IPv6+CNAME in Versionen <=1.10 fehlerhaft |
| evdns, libevent 2.x        | ja       | nein      | ja         | nein             | erkennt Änderungen an /etc/hosts nicht   |
| getaddrinfo_a, glibc 2.9+  | ja       | ja (3)    | ja         | nein             | N/A (auf Systemen ohne glibc nicht verfügbar) |
| getaddrinfo, libc          | nein     | ja (3)    | ja         | nein             | erfordert pthreads                       |

1. EDNS0 ist erforderlich, wenn einem Hostnamen mehr als 8 Adressen zugeordnet sind.
2. Eine SOA-Abfrage ist erforderlich, um Hostnamen bei einer Änderung der Zonen-Seriennummer erneut zu prüfen.
3. Um EDNS0 zu aktivieren, fügen Sie `options edns0` zu `/etc/resolv.conf` hinzu.

c-ares ist die Implementierung mit dem größten Funktionsumfang und wird für die meisten Einsatzbereiche sowie für die Erstellung von Binärpaketen empfohlen (sofern eine ausreichend neue Version verfügbar ist). Das in Libevent integrierte evdns eignet sich unter Beachtung der genannten Einschränkungen ebenfalls für viele Einsatzbereiche. Die übrigen Backends sind inzwischen weitgehend veraltet und werden kaum noch getestet.

Standardmäßig wird c-ares verwendet, sofern es gefunden wird. Der Einsatz lässt
sich mit `-Dcares=enabled` (configure: `--with-cares`) erzwingen oder mit
`-Dcares=disabled` (configure: `--without-cares`) deaktivieren. Wenn c-ares nicht
verwendet wird (weil es nicht gefunden oder deaktiviert wurde), kommt Libevent
zum Einsatz. Mit `-Devdns=false` (configure: `--disable-evdns`) wird evdns von
Libevent deaktiviert und auf eine libc-basierte Implementierung zurückgegriffen.

--------

## Optionale Funktionen {#optional-features}

Meson erkennt die Unterstützung für PAM, LDAP und systemd automatisch: Die
Optionen `-Dpam`, `-Dldap` und `-Dsystemd` haben den Standardwert `auto`.
Die jeweilige Funktion wird also eingebaut, wenn ihre Bibliotheken vorhanden
sind. Mit `-D<feature>=enabled` lässt sich eine Funktion ausdrücklich aktivieren,
mit `-D<feature>=disabled` deaktivieren. Der Autoconf-Build erkennt diese
Funktionen nicht automatisch; sie müssen ausdrücklich mit `--with-pam`,
`--with-ldap` oder `--with-systemd` aktiviert werden.

--------

## PAM-Authentifizierung {#pam-authentication}

Nach dem Kompilieren mit PAM-Unterstützung steht der neue globale Authentifizierungstyp `pam` zur Verfügung, mit dem Benutzer über PAM authentifiziert werden können.

--------

## LDAP-Authentifizierung {#ldap-authentication}

Nach dem Kompilieren mit LDAP-Unterstützung steht der neue globale Authentifizierungstyp `ldap` zur Verfügung, mit dem Benutzer über LDAP authentifiziert werden können.

--------

## systemd-Integration {#systemd-integration}

Die systemd-Unterstützung ermöglicht die Verwendung von `Type=notify` (oder `Type=notify-reload` mit systemd 253 oder neuer) sowie die Socket-Aktivierung. Beispiele finden sich in `etc/pgbouncer.service` und `etc/pgbouncer.socket`.

--------

## Aus dem Git-Repository kompilieren {#building-from-git}

Beim Autoconf-Build müssen die Header- und Konfigurationsdateien generiert
werden, bevor `configure` ausgeführt werden kann:

	$ git clone --branch pgbouncer_1_26_1 https://github.com/pgbouncer/pgbouncer.git
	$ cd pgbouncer
	$ ./autogen.sh
	$ ./configure
	$ make
	$ make install

Standardmäßig werden alle Dateien unter `/usr/local` installiert. Sie können für `configure` eine oder mehrere Befehlszeilenoptionen angeben. Führen Sie `./configure --help` aus, um die verfügbaren Optionen und die Umgebungsvariablen aufzulisten, mit denen sich die Konfiguration anpassen lässt.

Zusätzlich erforderliche Pakete für den Autoconf-Build aus Git: autoconf,
automake, libtool, pandoc

Mit Meson lässt sich direkt aus einem Checkout kompilieren;
zum Erstellen der Handbuchseiten wird pandoc benötigt:

	$ meson setup build
	$ meson compile -C build
	$ meson install -C build

Mit `meson configure build` lassen sich die verfügbaren `-D`-Optionen auflisten.

--------

## Tests {#testing}

Weitere Informationen zum Ausführen der Tests finden Sie in der Datei [`README.md` im Testverzeichnis][1].

[1]: https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/test/README.md

--------

## Kompilieren unter Windows {#building-on-windows}

Die einzige unterstützte Build-Umgebung unter Windows ist MinGW. Cygwin und Visual $ANYTHING werden nicht unterstützt.

Zum Kompilieren unter MinGW den üblichen Autoconf-Build ausführen:

	$ ./configure
	$ make

oder den experimentellen Meson-Build:

	$ meson setup build
	$ meson compile -C build

Für eine Cross-Kompilierung von Unix aus mit Autoconf:

	$ ./configure --host=i586-mingw32msvc

Die LDAP-Kompilierungsoption wird unter Windows derzeit nicht unterstützt.

--------

## Betrieb unter Windows {#running-on-windows}

Der Aufruf über die Befehlszeile erfolgt wie üblich. Die Schalter `-d` (Daemon-Modus) und `-u` (Benutzerwechsel) funktionieren jedoch nicht.

Wenn Sie PgBouncer als Windows-Dienst ausführen möchten, legen Sie mit dem Parameter `service_name` einen Namen für den Dienst fest. Danach:

	$ pgbouncer -regservice config.ini

Zum Deinstallieren des Dienstes:

	$ pgbouncer -unregservice config.ini

Um das Windows-Ereignisprotokoll zu nutzen, setzen Sie `syslog = 1` in der Konfigurationsdatei.
Zuvor müssen Sie `pgbevent.dll` registrieren:

	$ regsvr32 pgbevent.dll

Um die Registrierung aufzuheben, führen Sie folgenden Befehl aus:

	$ regsvr32 /u pgbevent.dll
