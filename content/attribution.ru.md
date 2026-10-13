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

pig.center повторно публикует документацию, написанную шестью исходными проектами. В конце каждой
страницы документации приведена строка атрибуции: из какой работы она получена, кому принадлежат
авторские права, по какой лицензии распространяется и в каком разделе этой страницы приведены
соответствующие сведения.

Эта страница служит единым реестром. Здесь указано, какие материалы были импортированы, когда и из
какой зафиксированной версии, по какой лицензии они распространяются и где хранится полное
уведомление исходного проекта.

> [!NOTE]
> Русская версия полностью охватывает Patroni, PgBouncer, pgBadger и etcd. Для pgBackRest,
> HAProxy и отдельных ещё не переведённых маршрутов ссылки открывают соответствующую английскую
> страницу.

> [!NOTE]
> pig.center — независимый проект документации сообщества. Он не связан ни с одним из перечисленных
> ниже проектов и с PostgreSQL Global Development Group, не одобрен ими и не является их официальным
> изданием.

## Сводка {#summary}

| Компонент | Исходная работа | Зафиксированная версия | Лицензия | Сохранённое уведомление |
|---|---|---|---|---|
| [Patroni](/ru/docs/patroni/) | [Документация Patroni](https://patroni.readthedocs.io/en/latest/) | v4.1.5 | [MIT](https://opensource.org/license/mit) | [Исходный `LICENSE`](https://github.com/patroni/patroni/blob/master/LICENSE) |
| [pgBackRest](/ru/docs/pgbackrest/) | [Документация pgBackRest](https://pgbackrest.org/) | v2.59.2 (английский / упрощённый китайский); v2.59.1 (другие переводы) | [MIT](https://opensource.org/license/mit) | [Исходный `LICENSE`](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE) |
| [PgBouncer](/ru/docs/pgbouncer/) | [Документация PgBouncer](https://www.pgbouncer.org/) | v1.26.0 (все шесть языков) | [ISC](https://opensource.org/license/isc-license-txt) | [Исходный `COPYRIGHT`](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT) |
| [pgBadger](/ru/docs/pgbadger/) | [Документация pgBadger](https://pgbadger.darold.net/) | v13.2, коммит `a1ad95a` | [PostgreSQL](https://opensource.org/license/postgresql) | [`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) |
| [HAProxy](/ru/docs/haproxy/) | [Руководства HAProxy 3.4](https://docs.haproxy.org/3.4/) | v3.4.4, коммит `7f03ae6` | [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) |
| [etcd](/ru/docs/etcd/) | [Документация etcd v3.7](https://etcd.io/docs/v3.7/) | v3.7, коммит `8245979` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [Исходный `LICENSE`](https://github.com/etcd-io/website/blob/main/LICENSE) |

Каждый сборник **адаптирован**, а не зеркально скопирован. Заголовки, якоря, перекрёстные ссылки,
сигнатуры кода, группировка страниц и навигация переработаны для этого издания; исходный текст при
этом сохранён. Строка атрибуции в конце страницы прямо указывает на адаптацию и содержит ссылку на
историю изменений просматриваемой страницы.

## Patroni {#patroni}

Импортировано 2026-08-15 из [документации Patroni](https://patroni.readthedocs.io/en/latest/)
версии **v4.1.5**; переводы на упрощённый китайский и русский языки поддерживаются параллельно.

Авторские права на Patroni принадлежат Compose, Zalando SE и Patroni Contributors
(copyright (c) 2025). Материалы распространяются по [лицензии MIT](https://opensource.org/license/mit).
Полный текст лицензии сохранён в [исходном проекте](https://github.com/patroni/patroni/blob/master/LICENSE).

## pgBackRest {#pgbackrest}

Импортировано 2026-08-15 с [сайта документации pgBackRest](https://pgbackrest.org/).
Английская версия и версия на упрощённом китайском обновлены 2026-10-04 до **v2.59.2**.
Другие существующие переводы остаются на **v2.59.1**; их последнее обновление выполнено 2026-08-30.
Русская версия pgBackRest пока не опубликована.

Авторские права на pgBackRest принадлежат The PostgreSQL Global Development Group и David Steele
(copyright (c) 2015-2026). Материалы распространяются по
[лицензии MIT](https://opensource.org/license/mit). Полный текст лицензии сохранён в
[исходном проекте](https://github.com/pgbackrest/pgbackrest/blob/main/LICENSE).

## PgBouncer {#pgbouncer}

Импортировано 2026-08-15 из [документации PgBouncer](https://www.pgbouncer.org/) версии
**v1.25.2**; перевод на упрощённый китайский язык подготовлен параллельно.

Английская версия и версия на упрощённом китайском обновлены 2026-10-04 до
[**v1.26.0**](https://github.com/pgbouncer/pgbouncer/releases/tag/pgbouncer_1_26_0)
на основе вычитанных руководств из `pigsty.io` и `pigsty.cc` соответственно.

2026-10-13 все шесть языковых версий были синхронизированы с актуальным английским
руководством для **v1.26.0**. Справочные описания сверены с реализацией выпуска;
локальные исправления устраняют фактические, орфографические и грамматические ошибки
исходной документации. Исходные диагностические сообщения сохранены дословно,
а каждый перевод прошёл постраничную проверку.

Авторские права на PgBouncer принадлежат Marko Kreen и Skype Technologies OÜ
(copyright (c) 2007-2009). Материалы распространяются по
[лицензии ISC](https://opensource.org/license/isc-license-txt). Полный текст лицензии сохранён в
[исходном проекте](https://github.com/pgbouncer/pgbouncer/blob/pgbouncer_1_26_0/COPYRIGHT).

## pgBadger {#pgbadger}

Импортировано 2026-08-15 с <https://pgbadger.darold.net/> и из репозитория
[`darold/pgbadger`](https://github.com/darold/pgbadger) на коммите
[`a1ad95a`](https://github.com/darold/pgbadger/commit/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae),
когда последней опубликованной версией была v13.2.

Авторские права на pgBadger принадлежат Gilles Darold (copyright (c) 2012-2026). Материалы
распространяются по [лицензии PostgreSQL](https://opensource.org/license/postgresql). Полный текст
лицензии размещён рядом с автономными примерами по адресу
[`/third_party/pgbadger/LICENSE`](/third_party/pgbadger/LICENSE) и в файле
`sources/pgbadger/upstream/LICENSE` репозитория сайта.

> [!IMPORTANT]
> pgBadger включает изменённый модуль `SQL::Beautify`, распространяемый по Artistic License 2.0;
> ресурсы создаваемых отчётов также содержат компоненты под лицензиями MIT, GPL-2.0 и SIL Open Font
> License 1.1. Полный перечень исходных ресурсов сохранён в файле
> [`/third_party/pgbadger/THIRD-PARTY-LICENSES`](/third_party/pgbadger/THIRD-PARTY-LICENSES).
> Опубликованные здесь [примеры отчётов](/ru/docs/pgbadger/sample-reports/) являются историческими
> сгенерированными материалами и сохраняют исходные встроенные уведомления.

## HAProxy {#haproxy}

Импортировано 2026-08-16 и обновлено 2026-08-30 из официального репозитория сопровождения HAProxy
3.4 на теге `v3.4.4`, коммите
[`7f03ae65c286`](https://git.haproxy.org/?p=haproxy-3.4.git;a=commit;h=7f03ae65c28605152c7a1a9ba7d9d0bcfb50f8b0).
Английский текст получен из полных руководств `doc/intro.txt`, `doc/configuration.txt` и
`doc/management.txt` — всего 40 128 строк — и реорганизован в 34 страницы для последовательного
чтения.

Авторские права на HAProxy принадлежат Willy Tarreau (copyright 2000-2026). Материалы
распространяются по [GNU General Public License version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
Собственное пояснение HAProxy к лицензии, исключение OpenSSL и полный текст GPLv2 опубликованы в
файлах [`/third_party/haproxy/LICENSE`](/third_party/haproxy/LICENSE) и
[`/third_party/haproxy/GPL-2.0`](/third_party/haproxy/GPL-2.0).

> [!WARNING]
> На страницы, производные от HAProxy, **не распространяется** лицензия CC BY 4.0 этого сайта.
> Они распространяются на условиях GPLv2 проекта HAProxy.

## etcd {#etcd}

Импортировано из официальной документации etcd v3.7 и обновлено 2026-08-30 до коммита
[`824597935df6`](https://github.com/etcd-io/website/commit/824597935df6e95992ef61c07e3222f4f796ca6c).
Зафиксированное дерево исходного кода находится в
[`content/en/docs/v3.7`](https://github.com/etcd-io/website/tree/824597935df6e95992ef61c07e3222f4f796ca6c/content/en/docs/v3.7).

Авторские права на документацию etcd принадлежат etcd Authors (copyright 2013-present). Её текст
распространяется по [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), а код и примеры кода —
по [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0). Полное уведомление сохранено в
[исходном проекте](https://github.com/etcd-io/website/blob/main/LICENSE).

## Этот сайт {#site}

Оригинальные материалы, написанные для pig.center, — обзорные страницы, полные версии на упрощённом
китайском и французском языках, опубликованные переводы на японский, немецкий и русский языки,
редакторские примечания и локализованные главные страницы — публикуются по
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
[репозиторий сайта](https://github.com/pgsty/pig.center/issues).
