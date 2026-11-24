---
title: "Атрибуция и лицензирование"
linkTitle: "Атрибуция"
description: "Источники всех страниц сайта, их правообладатели и лицензии, а также места хранения полных уведомлений."
icon: fa-solid fa-copyright
page_width: wide
type: docs
sidebar_enabled: false
breadcrumb: false
translation_notice: false
outputs: [HTML, markdown]
---

PG.CENTER повторно публикует документацию, написанную шестью исходными проектами. В конце каждой
страницы документации приведена строка атрибуции: из какой работы она получена, кому принадлежат
авторские права, по какой лицензии распространяется и в каком разделе этой страницы приведены
соответствующие сведения.

Эта страница служит единым реестром. Здесь указано, какие материалы были импортированы, когда и из
какой зафиксированной версии, по какой лицензии они распространяются и где хранится полное
уведомление исходного проекта.

> [!NOTE]
> PG.CENTER — независимый проект документации сообщества. Он не связан ни с одним из перечисленных
> ниже проектов и с PostgreSQL Global Development Group, не одобрен ими и не является их официальным
> изданием.

## Сводка {#summary}

В шести руководствах по эксплуатации учтены изменения английской версии. 23 ноября 2026 года сообщество также завершило перевод и сверку 117 страниц китайских руководств по базам данных и дополнило текст четырёх вводных страниц разделов pgEdge.

| Компонент | Исходная работа | Зафиксированная версия | Лицензия | Сохранённое уведомление |
|---|---|---|---|---|
| [Patroni](/ru/patroni/) | [Документация Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Исходный `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/ru/pgbackrest/) | [Документация pgBackRest](https://pgbackrest.org/) | v2.60.1 | [MIT](https://opensource.org/license/mit) | [Исходный `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/ru/pgbouncer/) | [Документация PgBouncer](https://www.pgbouncer.org/) | v1.26.1 | [ISC](https://opensource.org/license/isc-license-txt) | [Исходный `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT) |
| [pgBadger](/ru/pgbadger/) | [Документация pgBadger](https://pgbadger.darold.net/) | v13.3, коммит `0514893` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/ru/haproxy/) | [Руководства HAProxy 3.4](https://docs.haproxy.org/3.4/) | v3.4.8 LTS | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/ru/etcd/) | [Документация etcd v3.7](https://etcd.io/docs/v3.7/) | Документация v3.7, коммит `e60635a`; выпуск ПО v3.7.4 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Исходный `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |
{.wide .expand}

Каждый сборник **адаптирован**, а не зеркально скопирован. Заголовки, якоря, перекрёстные ссылки,
сигнатуры кода, группировка страниц и навигация переработаны для этого издания; исходный текст при
этом сохранён. Строка атрибуции в конце страницы прямо указывает на адаптацию и содержит ссылку на
историю изменений просматриваемой страницы.

## Patroni {#patroni}

Импортировано 2026-08-15 из [документации Patroni](https://patroni.readthedocs.io/en/latest/)
версии **v4.1.5**.

Авторские права на Patroni принадлежат Compose, Zalando SE и Patroni Contributors
(copyright (c) 2025). Материалы распространяются по [лицензии MIT](https://opensource.org/license/mit).
Полный текст лицензии сохранён в [исходном проекте](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Импортировано 2026-08-15 с [сайта документации pgBackRest](https://pgbackrest.org/) и обновлено 2026-11-21 до **v2.60.1**, тег `release/2.60.1`, коммит [`7aeba29`](https://github.com/pgbackrest/pgbackrest/commit/7aeba299c49abd768ca741506569007a5cab0870). Этот перевод синхронизирован с указанной ревизией.

Авторские права на pgBackRest принадлежат The PostgreSQL Global Development Group и David Steele
(copyright (c) 2015-2026). Материалы распространяются по
[лицензии MIT](https://opensource.org/license/mit). Полный текст лицензии сохранён в
[исходном проекте](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Импортировано 2026-08-15 из [документации PgBouncer](https://www.pgbouncer.org/) версии
**v1.25.2** и обновлено 2026-10-23 до
[**v1.26.1**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_1).

Авторские права на PgBouncer принадлежат Marko Kreen и Skype Technologies OÜ
(copyright (c) 2007-2009). Материалы распространяются по
[лицензии ISC](https://opensource.org/license/isc-license-txt). Полный текст лицензии сохранён в
[исходном проекте](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_1/COPYRIGHT).

## pgBadger {#pgbadger}

Импортировано 2026-08-15 с <https://pgbadger.darold.net/> и из [`darold/pgbadger`](https://github.com/darold/pgbadger), обновлено 2026-11-21 до опубликованного выпуска **v13.3**, коммит [`0514893`](https://github.com/darold/pgbadger/commit/0514893e97296695c77755fa36c59288c3afef3e). Этот перевод синхронизирован с указанной ревизией. Исторические выдержки с сайта и примеры отчётов сохраняют собственные источники.

Авторские права на pgBadger принадлежат Gilles Darold (copyright (c) 2012-2026). Материалы
распространяются по [лицензии PostgreSQL](https://opensource.org/license/postgresql). Полный текст
лицензии размещён рядом с автономными примерами по адресу
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) и в файле
`static/third_party/pgbadger/LICENSE` репозитория сайта.

> [!IMPORTANT]
> pgBadger включает изменённый модуль `SQL::Beautify`, распространяемый по Artistic License 2.0;
> ресурсы создаваемых отчётов также содержат компоненты под лицензиями MIT, GPL-2.0 и SIL Open Font
> License 1.1. Полный перечень исходных ресурсов сохранён в файле
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> Опубликованные здесь [примеры отчётов](/ru/pgbadger/sample-reports/) являются историческими
> сгенерированными материалами и сохраняют исходные встроенные уведомления.

## HAProxy {#haproxy}

Импортировано 2026-08-16 и обновлено 2026-11-21 до официальной версии HAProxy 3.4 [**v3.4.8 LTS**](https://git.haproxy.org/?p=haproxy-3.4.git;a=tag;h=v3.4.8). Полные руководства `doc/intro.txt`, `doc/configuration.txt` и `doc/management.txt` реорганизованы в 34 страницы для чтения. Руководства Starter и Management не изменились по сравнению с предыдущим снимком; изменения Configuration Manual зафиксированы в diff обновления и включены в этот перевод.

Авторские права на HAProxy принадлежат Willy Tarreau (copyright 2000-2026). Материалы
распространяются по [GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
Собственное пояснение HAProxy к лицензии, исключение OpenSSL и полный текст GPLv2 опубликованы в
файлах [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) и
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> На страницы, производные от HAProxy, **не распространяется** лицензия CC BY 4.0 этого сайта.
> Они распространяются на условиях GPLv2 проекта HAProxy.

## etcd {#etcd}

Импортировано из официальной документации etcd v3.7 и обновлено 2026-11-21 до коммита
[`e60635a46b57`](https://github.com/etcd-io/website/tree/e60635a46b57b7d74ca80c52c59aa0d37bed01a8/content/en/docs/v3.7).
Зафиксированное дерево исходного кода находится в `content/en/docs/v3.7`.

Примеры установки и сводка изменений соответствуют [etcd v3.7.4](https://github.com/etcd-io/etcd/releases/tag/v3.7.4), коммит выпуска `2e8a5c99e4982c8d4c521be15364ea4c5c68a489`, собранному с Go 1.26.11. Отдельно зафиксированный changelog сохраняет заголовок «v3.7.4 (TBC)»; тег выпуска подтверждает публикацию. Снимок документации и выпуск ПО зафиксированы отдельно в `data/upstreams.yaml` вместе с контрольными суммами исходных файлов.

Авторские права на документацию etcd принадлежат etcd Authors (copyright 2013-present). Её текст
распространяется по [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), а код и примеры кода —
по [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Полное уведомление сохранено в
[исходном проекте](https://github.com/etcd-io/website/blob/main/LICENSE).

## Этот сайт {#site}

Оригинальные материалы, написанные для PG.CENTER, публикуются по
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), кроме страниц, к которым применима одна
из указанных выше исходных лицензий.

Слон PostgreSQL (Slonik) на главной странице является собственным знаком проекта PostgreSQL. Он
взят из [репозитория сайта postgresql.org](https://git.postgresql.org/gitweb/?p=pgweb.git) и повторно
опубликован здесь без изменений в соответствии с
[политикой товарных знаков и логотипов PostgreSQL](https://www.postgresql.org/about/policies/trademarks/)
как обозначение PostgreSQL. Знак принадлежит PostgreSQL Community Association of Canada; его
использование здесь не означает одобрения проекта.

Сайт построен на [OINK](https://oink.pgsty.com/) v1.2.0 — теме Hugo, распространяемой по
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Её собственные уведомления об
исходных материалах и встроенных зависимостях входят в исходный код модуля.

Сообщить об ошибке в сведениях об атрибуции можно через
[репозиторий сайта](https://github.com/pgsty/doc.pg.center/issues).
