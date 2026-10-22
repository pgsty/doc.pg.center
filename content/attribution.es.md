---
title: "Atribución y licencias"
linkTitle: "Atribución"
description: "De dónde procede cada página de este sitio, quién posee sus derechos, qué licencia lleva y dónde se conserva el aviso completo."
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

PG.CENTER republica documentación escrita por seis proyectos originales. Cada página de
documentación lleva al final una línea de crédito que indica la obra de la que deriva, su titular
de derechos, su licencia y un enlace a la sección de esta página que la cubre.

Esta página es ese registro. Establece qué se importó, cuándo, desde qué revisión fijada, bajo
qué licencia y dónde se conserva el aviso original completo.

> [!NOTE]
> PG.CENTER es un proyecto de documentación comunitario e independiente. No está afiliado a
> ninguno de los proyectos siguientes ni cuenta con su respaldo, ni es una publicación oficial
> de ellos, ni del PostgreSQL Global Development Group.

## Resumen {#summary}

| Componente | Obra original | Revisión fijada | Licencia | Aviso conservado |
|---|---|---|---|---|
| [Patroni](/es/patroni/) | [Documentación de Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [`LICENSE` original](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/es/pgbackrest/) | [Documentación de pgBackRest](https://pgbackrest.org/) | v2.60.0 | [MIT](https://opensource.org/license/mit) | [`LICENSE` original](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/es/pgbouncer/) | [Documentación de PgBouncer](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [`COPYRIGHT` original](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/es/pgbadger/) | [Documentación de pgBadger](https://pgbadger.darold.net/) | v13.2, instantánea de desarrollo, commit `f373ac6` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/es/haproxy/) | [Manuales de HAProxy 3.4](https://docs.haproxy.org/3.4/) | 3.4.7-57; estable v3.4.7, commit `0faeaed` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/es/etcd/) | [Documentación de etcd v3.7](https://etcd.io/docs/v3.7/) | v3.7, commit `d20f8ae` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE` original](https://github.com/etcd-io/website/blob/main/LICENSE) |

Cada colección está **adaptada**, no replicada. Los títulos, anclas, enlaces cruzados, firmas de
código, agrupación de páginas y navegación se reelaboraron para esta edición; la prosa original
se conserva. El crédito al final de la página así lo indica y enlaza con el historial de cambios
de este sitio para la página que estás leyendo.

## Patroni {#patroni}

Importada el 2026-08-15 desde la [documentación de Patroni](https://patroni.readthedocs.io/en/latest/)
para **v4.1.5**.

Patroni tiene derechos de autor (c) 2025 de Compose, Zalando SE, Patroni Contributors, y se
distribuye bajo la [Licencia MIT](https://opensource.org/license/mit). El texto completo de la
licencia se conserva [en el proyecto original](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Importada el 2026-08-15 desde el [sitio de documentación de pgBackRest](https://pgbackrest.org/) y actualizada el 2026-10-23 a **v2.60.0**, etiqueta `release/2.60.0`, commit [`2e1c4f2`](https://github.com/pgbackrest/pgbackrest/commit/2e1c4f2ba727c45a0a23d4b326905088dc15b1a1).

pgBackRest tiene derechos de autor (c) 2015-2026 de The PostgreSQL Global Development Group y
David Steele, y se distribuye bajo la [Licencia MIT](https://opensource.org/license/mit). El
texto completo de la licencia se conserva
[en el proyecto original](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Importada el 2026-08-15 desde el [sitio de documentación de PgBouncer](https://www.pgbouncer.org/)
para **v1.25.2** y actualizada el 2026-10-23 a
[**v1.26.1**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_1).

PgBouncer tiene derechos de autor (c) 2007-2009 de Marko Kreen, Skype Technologies OÜ, y se
distribuye bajo la [Licencia ISC](https://opensource.org/license/isc-license-txt). El texto
completo de la licencia se conserva
[en el proyecto original](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT).

## pgBadger {#pgbadger}

Importada el 2026-08-15 desde <https://pgbadger.darold.net/> y [`darold/pgbadger`](https://github.com/darold/pgbadger), y actualizada el 2026-10-23 al commit [`f373ac6`](https://github.com/darold/pgbadger/commit/f373ac678c756f66a785c5ab4773d1f05f468d67).
Es una instantánea de la documentación de desarrollo posterior a la última versión publicada, v13.2; no es una nueva versión estable. Los extractos históricos del sitio web y los informes de ejemplo conservan sus propias fuentes.

pgBadger tiene derechos de autor (c) 2012-2026 de Gilles Darold y se distribuye bajo la
[Licencia PostgreSQL](https://opensource.org/license/postgresql). El texto completo de la
licencia se conserva junto a los ejemplos sin conexión como
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) y en
`static/third_party/pgbadger/LICENSE` en el repositorio del sitio.

> [!IMPORTANT]
> pgBadger incluye un módulo `SQL::Beautify` modificado bajo la Artistic License 2.0, y los
> recursos de los informes que genera incluyen componentes MIT, GPL-2.0 y SIL Open Font License
> 1.1. El inventario completo de recursos originales se conserva como
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> Los [informes de ejemplo](/es/pgbadger/sample-reports/) publicados aquí son artefactos
> históricos ya generados y conservan sus avisos originales incrustados.

## HAProxy {#haproxy}

Importada el 2026-08-16, actualizada el 2026-08-30 y revisada el 2026-10-23 con la instantánea
oficial de mantenimiento en inglés de HAProxy 3.4 `3.4.7-57`, commit
[`0faeaeda6cdb`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=0faeaeda6cdbb65c0e0cedb9a20489581bd7d4c3).
La última versión estable es `3.4.7` (etiqueta `v3.4.7`); la instantánea de documentación
incluye cambios de la rama de mantenimiento posteriores a esa versión.
La prosa en inglés procede de los manuales completos `doc/intro.txt`, `doc/configuration.txt` y
`doc/management.txt` — 40,246 líneas en total — reorganizados en 34 páginas de lectura.

HAProxy tiene derechos de autor 2000-2026 de Willy Tarreau y se distribuye bajo la
[GNU General Public License versión 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
La explicación de licencia del propio HAProxy, su excepción OpenSSL y el texto completo de la
GPLv2 se publican como [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) y
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> Las páginas derivadas de HAProxy **no** están cubiertas por la licencia CC BY 4.0 de este
> sitio. Llevan los términos GPLv2 de HAProxy.

## etcd {#etcd}

Importada desde la documentación oficial de etcd v3.7 y actualizada el 2026-10-13 en el commit
[`d20f8ae346da`](https://github.com/etcd-io/website/commit/d20f8ae346da60ab6eb6f24f200753b328aa9fcc).
El árbol fuente fijado es
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/d20f8ae346da60ab6eb6f24f200753b328aa9fcc/content/en/docs/v3.7).

La documentación de etcd tiene derechos de autor 2013-actualidad de los autores de etcd. Su
prosa está licenciada bajo [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), mientras
que el código y los ejemplos de código están licenciados bajo
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). El aviso completo se conserva
[en el proyecto original](https://github.com/etcd-io/website/blob/main/LICENSE).

## Este sitio {#site}

El texto original escrito para PG.CENTER se publica bajo
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), salvo donde una licencia original de
las anteriores se aplique a la página en su lugar.

El elefante de PostgreSQL (Slonik) que aparece en la página de inicio es la propia marca del
proyecto PostgreSQL, tomada del
[repositorio del sitio postgresql.org](https://git.postgresql.org/gitweb/?p=pgweb.git)
y republicada aquí sin modificaciones bajo
[la política de marcas y logotipos de PostgreSQL](https://www.postgresql.org/about/policies/trademarks/)
como referencia a PostgreSQL. Es una marca de PostgreSQL Community Association of Canada y su
uso aquí no implica respaldo alguno.

El sitio está construido con [OINK](https://oink.pgsty.com/) v1.2.0, un tema de Hugo licenciado
bajo la [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), que incluye sus
propios avisos de origen y de dependencias incluidas en el código fuente del módulo.

Las correcciones a cualquier atribución de esta página son bienvenidas a través del
[repositorio del sitio](https://github.com/pgsty/doc.pg.center/issues).
