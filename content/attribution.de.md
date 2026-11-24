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

PG.CENTER veröffentlicht Dokumentationen von sechs Upstream-Projekten erneut. Jede
Dokumentationsseite endet mit einer einzeiligen Quellenangabe. Sie nennt das
Werk, auf dem die Seite basiert, dessen Urheberrechtsinhaber und Lizenz und
verweist auf den zugehörigen Abschnitt dieser Seite.

Diese Seite dient als entsprechendes Verzeichnis. Sie dokumentiert, welche
Inhalte wann aus welcher festgeschriebenen Revision unter welcher Lizenz
importiert wurden und wo der vollständige Upstream-Hinweis aufbewahrt wird.

> [!NOTE]
> PG.CENTER ist ein unabhängiges Dokumentationsprojekt der Community. Es ist mit
> keinem der unten aufgeführten Projekte und auch nicht mit der PostgreSQL Global
> Development Group verbunden, wird von diesen nicht unterstützt und ist keine
> offizielle Veröffentlichung dieser Organisationen.

## Zusammenfassung {#summary}

Die sechs Betriebshandbücher folgen in dieser Ausgabe dem englischen Stand. Am 23. November 2026 wurden außerdem 117 offene Übersetzungs- und Prüfaufgaben für die chinesischen Datenbankhandbücher abgeschlossen und vier chinesische pgEdge-Kapiteleinstiege vervollständigt.

| Komponente | Ursprungswerk | Festgeschriebener Stand | Lizenz | Hinterlegter Hinweis |
|---|---|---|---|---|
| [Patroni](/de/patroni/) | [Patroni-Dokumentation](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/de/pgbackrest/) | [pgBackRest-Dokumentation](https://pgbackrest.org/) | v2.60.1 | [MIT](https://opensource.org/license/mit) | [Upstream `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/de/pgbouncer/) | [PgBouncer-Dokumentation](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [Upstream `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/de/pgbadger/) | [pgBadger-Dokumentation](https://pgbadger.darold.net/) | v13.3, Commit `0514893` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/de/haproxy/) | [HAProxy-3.4-Handbücher](https://docs.haproxy.org/3.4/) | v3.4.8 LTS | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/de/etcd/) | [etcd-v3.7-Dokumentation](https://etcd.io/docs/v3.7/) | Dokumentation v3.7, Commit `e60635a`; Softwareversion v3.7.4 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Upstream `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |
{.wide .expand}

Jede Sammlung ist **bearbeitet**, nicht gespiegelt. Überschriften, Anker,
Querverweise, Codesignaturen, Seitengruppierung und Navigation wurden für diese
Ausgabe überarbeitet; der Upstream-Wortlaut selbst bleibt erhalten. Die
Quellenangabe am Seitenende weist darauf hin und verlinkt den Änderungsverlauf
dieser Website für die gerade gelesene Seite.

## Patroni {#patroni}

Am 2026-08-15 aus der [Patroni-Dokumentation](https://patroni.readthedocs.io/en/latest/)
für **v4.1.5** importiert.

Copyright (c) 2025 für Patroni: Compose, Zalando SE und Patroni Contributors.
Patroni wird unter der [MIT License](https://opensource.org/license/mit)
verbreitet. Der vollständige Lizenztext wird
[im Upstream-Projekt](https://github.com/patroni/patroni/blob/master/LICENSE)
aufbewahrt.

## pgBackRest {#pgbackrest}

Am 2026-08-15 von der [pgBackRest-Dokumentationswebsite](https://pgbackrest.org/) importiert und am 2026-11-21 auf **v2.60.1**, Tag `release/2.60.1`, Commit [`7aeba29`](https://github.com/pgbackrest/pgbackrest/commit/7aeba299c49abd768ca741506569007a5cab0870) aktualisiert. Diese übersetzte Ausgabe ist auf diesen Stand abgeglichen.

Copyright (c) 2015-2026 für pgBackRest: The PostgreSQL Global Development Group
und David Steele. pgBackRest wird unter der
[MIT License](https://opensource.org/license/mit) verbreitet. Der vollständige
Lizenztext wird
[im Upstream-Projekt](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE)
aufbewahrt.

## PgBouncer {#pgbouncer}

Am 2026-08-15 von der [PgBouncer-Dokumentationswebsite](https://www.pgbouncer.org/)
für **v1.25.2** importiert und am 2026-10-23 auf
[**v1.26.1**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_1) aktualisiert.

Copyright (c) 2007-2009 für PgBouncer: Marko Kreen und Skype Technologies OÜ.
PgBouncer wird unter der
[ISC License](https://opensource.org/license/isc-license-txt) verbreitet. Der
vollständige Lizenztext wird
[im Upstream-Projekt](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT)
aufbewahrt.

## pgBadger {#pgbadger}

Am 2026-08-15 von <https://pgbadger.darold.net/> und aus [`darold/pgbadger`](https://github.com/darold/pgbadger) importiert und am 2026-11-21 auf die veröffentlichte Version **v13.3**, Commit [`0514893`](https://github.com/darold/pgbadger/commit/0514893e97296695c77755fa36c59288c3afef3e), aktualisiert. Diese übersetzte Ausgabe ist auf diesen Stand abgeglichen. Historische Website-Auszüge und Beispielberichte behalten ihre eigenen Quellen.

Copyright (c) 2012-2026 für pgBadger: Gilles Darold. pgBadger wird unter der
[PostgreSQL License](https://opensource.org/license/postgresql) verbreitet. Der
vollständige Lizenztext wird neben den Offline-Beispielen unter
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) sowie im
Site-Repository unter `static/third_party/pgbadger/LICENSE` aufbewahrt.

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

Am 2026-08-16 importiert und am 2026-11-21 auf die offizielle HAProxy-3.4-Version [**v3.4.8 LTS**](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8) aktualisiert. Die vollständigen Handbücher `doc/intro.txt`, `doc/configuration.txt` und `doc/management.txt` wurden in 34 Leseseiten neu gegliedert. Starter- und Management-Handbuch sind gegenüber dem vorherigen Stand unverändert; die Änderungen des Configuration-Handbuchs sind im Update-Diff erfasst und in dieser übersetzten Ausgabe enthalten.

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

Aus der offiziellen etcd-v3.7-Dokumentation importiert und am 2026-11-21 beim
Commit [`e60635a46b57`](https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7)
aktualisiert. Der festgeschriebene Quellbaum ist `content/en/docs/v3.7`.

Installationsbeispiele und Versionszusammenfassung zielen auf [etcd v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4), Release-Commit `2e8a5c99e4982c8d4c521be15364ea4c5c68a489`, gebaut mit Go 1.26.11. Das separat fixierte Changelog behält die Überschrift „v3.7.4 (TBC)“; der Release-Tag bestätigt die Veröffentlichung. Dokumentationsstand und Softwareversion sind in `data/upstreams.yaml` zusammen mit den Prüfsummen der Quellen getrennt erfasst.

Copyright 2013–heute für die etcd-Dokumentation: etcd Authors. Ihr Fließtext
steht unter [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), Code und
Codebeispiele dagegen unter
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Der vollständige
Hinweis wird [im Upstream-Projekt](https://github.com/etcd-io/website/blob/main/LICENSE)
aufbewahrt.

## Diese Website {#site}

Die eigens für PG.CENTER verfassten Texte werden unter
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

Die Website wird mit [OINK](https://oink.pgsty.com/) v1.2.0 erstellt, einem unter
der [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
lizenzierten Hugo-Theme. Die Modulquellen enthalten eigene Hinweise zum
Upstream-Projekt und zu gebündelten Abhängigkeiten.

Korrekturen an den Quellenangaben auf dieser Seite sind über das
[Repository der Website](https://github.com/pgsty/doc.pg.center/issues) willkommen.
