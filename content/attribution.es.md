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

Los seis manuales de operaciones de esta edición incorporan los cambios de la versión inglesa. El 23 de noviembre de 2026 también se completaron las 117 tareas de traducción y revisión pendientes en los manuales de bases de datos en chino, y se añadió el texto que faltaba en cuatro páginas de sección de pgEdge.

| Componente | Obra original | Revisión fijada | Licencia | Aviso conservado |
|---|---|---|---|---|
| [Patroni](/es/patroni/) | [Documentación de Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [`LICENSE` original](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/es/pgbackrest/) | [Documentación de pgBackRest](https://pgbackrest.org/) | v2.60.1 | [MIT](https://opensource.org/license/mit) | [`LICENSE` original](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/es/pgbouncer/) | [Documentación de PgBouncer](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [`COPYRIGHT` original](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/es/pgbadger/) | [Documentación de pgBadger](https://pgbadger.darold.net/) | v13.3, commit `0514893` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/es/haproxy/) | [Manuales de HAProxy 3.4](https://docs.haproxy.org/3.4/) | v3.4.8 LTS | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/es/etcd/) | [Documentación de etcd v3.7](https://etcd.io/docs/v3.7/) | Documentación v3.7, commit `e60635a`; versión del software v3.7.4 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE` original](https://github.com/etcd-io/website/blob/main/LICENSE) |
{.wide .expand}

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

Importada el 2026-08-15 desde el [sitio de documentación de pgBackRest](https://pgbackrest.org/) y actualizada el 2026-11-21 a **v2.60.1**, etiqueta `release/2.60.1`, commit [`7aeba29`](https://github.com/pgbackrest/pgbackrest/commit/7aeba299c49abd768ca741506569007a5cab0870). Esta edición traducida está sincronizada con esa revisión.

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

Importada el 2026-08-15 desde <https://pgbadger.darold.net/> y [`darold/pgbadger`](https://github.com/darold/pgbadger), y actualizada el 2026-11-21 a la versión publicada **v13.3**, commit [`0514893`](https://github.com/darold/pgbadger/commit/0514893e97296695c77755fa36c59288c3afef3e). Esta edición traducida está sincronizada con esa revisión. Los extractos históricos del sitio web y los informes de ejemplo conservan sus propias fuentes.

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

Importada el 2026-08-16 y actualizada el 2026-11-21 a la versión oficial de HAProxy 3.4 [**v3.4.8 LTS**](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8). Los manuales completos `doc/intro.txt`, `doc/configuration.txt` y `doc/management.txt` se reorganizaron en 34 páginas de lectura. Las guías Starter y Management no cambian respecto a la instantánea anterior; los cambios del Manual de configuración están registrados en el diff de actualización e incluidos en esta edición traducida.

HAProxy tiene derechos de autor 2000-2026 de Willy Tarreau y se distribuye bajo la
[GNU General Public License versión 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
La explicación de licencia del propio HAProxy, su excepción OpenSSL y el texto completo de la
GPLv2 se publican como [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) y
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> Las páginas derivadas de HAProxy **no** están cubiertas por la licencia CC BY 4.0 de este
> sitio. Llevan los términos GPLv2 de HAProxy.

## etcd {#etcd}

Importada desde la documentación oficial de etcd v3.7 y actualizada el 2026-11-21 en el commit
[`e60635a46b57`](https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7).
El árbol fuente fijado es `content/en/docs/v3.7`.

Los ejemplos de instalación y el resumen de cambios corresponden a [etcd v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4), commit de publicación `2e8a5c99e4982c8d4c521be15364ea4c5c68a489`, compilado con Go 1.26.11. El changelog fijado por separado conserva el título «v3.7.4 (TBC)»; la etiqueta de versión confirma su publicación. La instantánea de documentación y la versión del software se registran por separado en `data/upstreams.yaml`, junto con las sumas de comprobación de las fuentes.

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
