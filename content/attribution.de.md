---
title: "Quellenangaben und Lizenzierung"
linkTitle: "Quellenangaben"
description: "Herkunft, Rechteinhaber und Lizenz jeder Seite sowie der Ablageort der vollständigen Lizenz- und Urheberrechtshinweise."
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

pgsql.cc veröffentlicht Dokumentationen von sechs Upstream-Projekten erneut. Jede
Dokumentationsseite endet mit einer einzeiligen Quellenangabe. Sie nennt das
Werk, auf dem die Seite basiert, dessen Urheberrechtsinhaber und Lizenz und
verweist auf den zugehörigen Abschnitt dieser Seite.

Diese Seite dient als entsprechendes Verzeichnis. Sie dokumentiert, welche
Inhalte wann aus welcher festgeschriebenen Revision unter welcher Lizenz
importiert wurden und wo der vollständige Upstream-Hinweis aufbewahrt wird.

> [!NOTE]
> Die deutsche Ausgabe enthält die vollständige pgBadger-Sammlung sowie bereits
> übersetzte Seiten aus Patroni, PgBouncer, HAProxy und etcd. Für pgBackRest und
> noch fehlende Einzelseiten führen die Links zur entsprechenden englischen Seite.

> [!NOTE]
> pgsql.cc ist ein unabhängiges Dokumentationsprojekt der Community. Es ist mit
> keinem der unten aufgeführten Projekte und auch nicht mit der PostgreSQL Global
> Development Group verbunden, wird von diesen nicht unterstützt und ist keine
> offizielle Veröffentlichung dieser Organisationen.

## Zusammenfassung {#summary}

| Komponente | Ursprungswerk | Festgeschriebener Stand | Lizenz | Hinterlegter Hinweis |
|---|---|---|---|---|
| [Patroni](/de/patroni/) | [Patroni-Dokumentation](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/de/pgbackrest/) | [pgBackRest-Dokumentation](https://pgbackrest.org/) | v2.59.1 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/de/pgbouncer/) | [PgBouncer-Dokumentation](https://www.pgbouncer.org/) | v1.25.2 | [ISC](https://opensource.org/license/isc-license-txt) | [Upstream `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/master/COPYRIGHT) |
| [pgBadger](/de/pgbadger/) | [pgBadger-Dokumentation](https://pgbadger.darold.net/) | v13.2, Commit `a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/de/haproxy/) | [HAProxy-3.4-Handbücher](https://docs.haproxy.org/3.4/) | v3.4.4, Commit `7f03ae6` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/de/etcd/) | [etcd-v3.7-Dokumentation](https://etcd.io/docs/v3.7/) | v3.7, Commit `8245979` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Upstream `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

Jede Sammlung ist **bearbeitet**, nicht gespiegelt. Überschriften, Anker,
Querverweise, Codesignaturen, Seitengruppierung und Navigation wurden für diese
Ausgabe überarbeitet; der Upstream-Wortlaut selbst bleibt erhalten. Die
Quellenangabe am Seitenende weist darauf hin und verlinkt den Änderungsverlauf
dieser Website für die gerade gelesene Seite.

## Patroni {#patroni}

Am 2026-08-15 aus der [Patroni-Dokumentation](https://patroni.readthedocs.io/en/latest/)
für **v4.1.5** importiert; parallel dazu wurde eine vereinfachte chinesische
Übersetzung erstellt.

Copyright (c) 2025 für Patroni: Compose, Zalando SE und Patroni Contributors.
Patroni wird unter der [MIT License](https://opensource.org/license/mit)
verbreitet. Der vollständige Lizenztext wird
[im Upstream-Projekt](https://github.com/patroni/patroni/blob/master/LICENSE)
aufbewahrt.

## pgBackRest {#pgbackrest}

Am 2026-08-15 importiert und am 2026-08-30 anhand der
[pgBackRest-Dokumentationswebsite](https://pgbackrest.org/) für **v2.59.1**
aktualisiert; die vollständigen Übersetzungen in vereinfachtem Chinesisch und
Französisch werden parallel gepflegt. Eine deutsche pgBackRest-Ausgabe liegt
derzeit noch nicht vor.

Copyright (c) 2015-2026 für pgBackRest: The PostgreSQL Global Development Group
und David Steele. pgBackRest wird unter der
[MIT License](https://opensource.org/license/mit) verbreitet. Der vollständige
Lizenztext wird
[im Upstream-Projekt](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)
aufbewahrt.

## PgBouncer {#pgbouncer}

Am 2026-08-15 aus der
[PgBouncer-Dokumentationswebsite](https://www.pgbouncer.org/) für **v1.25.2**
importiert; parallel dazu wurde eine vereinfachte chinesische Übersetzung
erstellt.

Copyright (c) 2007-2009 für PgBouncer: Marko Kreen und Skype Technologies OÜ.
PgBouncer wird unter der
[ISC License](https://opensource.org/license/isc-license-txt) verbreitet. Der
vollständige Lizenztext wird
[im Upstream-Projekt](https://github.com/pgbouncer/pgbouncer/blob/master/COPYRIGHT)
aufbewahrt.

## pgBadger {#pgbadger}

Am 2026-08-15 von <https://pgbadger.darold.net/> und aus
[`darold/pgbadger`](https://github.com/darold/pgbadger) beim Commit
[`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae)
importiert; die zu diesem Zeitpunkt neueste veröffentlichte Version war v13.2.

Copyright (c) 2012-2026 für pgBadger: Gilles Darold. pgBadger wird unter der
[PostgreSQL License](https://opensource.org/license/postgresql) verbreitet. Der
vollständige Lizenztext wird neben den Offline-Beispielen unter
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) sowie im
Site-Repository unter `sources/pgbadger/upstream/LICENSE` aufbewahrt.

> [!IMPORTANT]
> pgBadger bindet ein modifiziertes `SQL::Beautify`-Modul unter der Artistic License 2.0
> ein. Die Ressourcen der erzeugten Berichte enthalten außerdem
> Komponenten unter MIT, GPL-2.0 und SIL Open Font License 1.1. Die vollständige
> Upstream-Ressourcenübersicht wird unter
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES)
> aufbewahrt. Die hier veröffentlichten
> [Beispielberichte](/de/pgbadger/sample-reports/) sind historische erzeugte
> Artefakte und behalten ihre ursprünglichen eingebetteten Hinweise bei.

## HAProxy {#haproxy}

Am 2026-08-16 aus dem offiziellen Wartungsrepository von HAProxy 3.4 importiert
und am 2026-08-30 aktualisiert: Tag `v3.4.4`, Commit
[`7f03ae65c286`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0).
Der englische Text basiert auf den vollständigen Handbüchern `doc/intro.txt`,
`doc/configuration.txt` und `doc/management.txt` mit insgesamt 40,128 Zeilen,
die in 34 Leseseiten neu gegliedert wurden.

Copyright 2000-2026 für HAProxy: Willy Tarreau. HAProxy wird unter der
[GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
verbreitet. Die HAProxy-eigene Lizenzerläuterung, die OpenSSL-Ausnahme und der
vollständige GPLv2-Text werden unter
[`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) und
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0) veröffentlicht.

> [!WARNING]
> Die von HAProxy abgeleiteten Seiten fallen **nicht** unter die CC BY
> 4.0-Lizenz dieser Website. Für sie gelten die GPLv2-Bedingungen von HAProxy.

## etcd {#etcd}

Aus der offiziellen etcd-v3.7-Dokumentation importiert und am 2026-08-30 beim
Commit
[`824597935df6`](https://github.com/etcd-io/website/commit/824597935df6e95992ef61c07e3222f4f796ca6c)
aktualisiert. Der festgeschriebene Quellbaum ist
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7).

Copyright 2013–heute für die etcd-Dokumentation: etcd Authors. Ihr Fließtext
steht unter [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), Code und
Codebeispiele dagegen unter
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Der vollständige
Hinweis wird [im Upstream-Projekt](https://github.com/etcd-io/website/blob/main/LICENSE)
aufbewahrt.

## Diese Website {#site}

Die eigens für pgsql.cc verfassten Texte — Orientierungsseiten, die vollständigen
chinesischen und französischen Ausgaben, die bereits veröffentlichten japanischen,
deutschen und russischen Übersetzungen, redaktionelle Hinweise und die lokalisierten
Startseiten — werden unter
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) veröffentlicht, sofern
für eine Seite nicht stattdessen eine oben genannte Upstream-Lizenz gilt.


Der auf der Startseite gezeigte PostgreSQL-Elefant (Slonik) ist eine eigene
Marke des PostgreSQL-Projekts. Er stammt aus dem
[Website-Repository von postgresql.org](https://git.postgresql.org/gitweb/?p=pgweb.git)
und wird hier unverändert gemäß der
[Richtlinie zu Marken und Logos von PostgreSQL](https://www.postgresql.org/about/policies/trademarks/)
als Verweis auf PostgreSQL wiederveröffentlicht. Slonik ist eine Marke der
PostgreSQL Community Association of Canada; seine Verwendung hier bedeutet
keine Unterstützung oder Empfehlung.

Die Website wird mit [OINK](https://oink.pgsty.com/) v1.0.0 erstellt, einem unter
der [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
lizenzierten Hugo-Theme. Die Modulquellen enthalten eigene Hinweise zum
Upstream-Projekt und zu gebündelten Abhängigkeiten.

Korrekturen an den Quellenangaben auf dieser Seite sind über das
[Repository der Website](https://github.com/pgsty/pgsql.cc/issues) willkommen.
