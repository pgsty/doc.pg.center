---
title: "Документация pgBadger 13.3"
linkTitle: pgBadger
weight: 40
description: "Быстрый анализ журналов PostgreSQL и PgBouncer с подробными автономными отчётами"
search_keywords: [csvlog, jsonlog, logplex, stderr, syslog]
icon: fa-solid fa-otter
type: docs
outputs: [HTML, RSS, print, markdown, LLMSFULL]
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [Концепция]
aliases: [/pgbadger/documentation/]
upstream_source: pgbadger-20261121
upstream_ref: "v13.3"
upstream_link: "https://github.com/darold/pgbadger/tree/0514893e97296695c77755fa36c59288c3afef3e"
cascade:
  upstream_source: pgbadger-20261121
  upstream_ref: "v13.3"
  type: docs
  module: [PGBADGER]
---

Это руководство охватывает [pgBadger 13.3](https://github.com/darold/pgbadger/releases/tag/v13.3), выпущенный 3 ноября 2026 г. Выпуск включает удалённую фильтрацию в режиме наблюдения, кодирование каталогов отчётов по базам данных, прокручиваемые легенды графиков и исправления из [примечаний к версии 13.3](/ru/pgbadger/releases/13/#v13-3).

![Логотип pgBadger](/img/pgbadger/logo.png "pgBadger")

**pgBadger** — быстрый автономный анализатор журналов PostgreSQL, написанный на Perl. Он читает журналы PostgreSQL или PgBouncer и формирует подробные результаты в HTML, текстовом, двоичном, JSON-формате либо в виде необработанного CSV. HTML-отчёты автономны, интерактивны, поддерживают масштабирование, и для их просмотра нужен только веб-браузер.

## Зачем нужен pgBadger {#why-pgbadger}

pgBadger рассчитан на большие журналы и повседневную эксплуатацию:

- одна программа на Perl, не требующая обязательных модулей за пределами базовой поставки Perl;
- автоматическое определение форматов ввода `stderr`, `syslog`, `csvlog`, `jsonlog`, RDS, Cloud SQL, logplex, Redshift и PgBouncer;
- непосредственное чтение локальных файлов, стандартного ввода, удалённых файлов по SSH, а также URL с HTTP, FTP или SFTP;
- поддержка сжатых входных данных gzip, bzip2, lz4, xz, zip и zstd;
- параллельный разбор одного большого файла или множества небольших файлов;
- ежедневные, еженедельные и создаваемые по запросу ежемесячные инкрементальные отчёты;
- фильтрация по времени, базе данных, пользователю, клиенту, приложению, процессу, сеансу и шаблону запроса.

## Что содержат отчёты {#report-coverage}

Набор отчётов PostgreSQL охватывает:

- общую активность и статистику запросов;
- медленные, частые, наиболее затратные по времени, ожидающие и отменённые запросы;
- временные файлы, контрольные точки, блокировки, сеансы и соединения;
- активность autovacuum и autoanalyze по таблицам;
- ошибки и события по уровню важности и классу;
- распределения по базе данных, пользователю, клиенту, приложению и типу оператора.

Для входных данных PgBouncer дополнительно отображаются пропускная способность, средняя длительность запросов, число одновременных сеансов, распределения соединений и сеансов, использование резервного пула, а также отчёты о частых ошибках и событиях.

## Структура документации {#documentation-map}

Читайте руководство в следующем порядке или сразу переходите к нужной задаче через боковую панель:

1. [Загрузите и установите](/ru/pgbadger/download/) pgBadger и его необязательные модули.
2. Ознакомьтесь с полным [справочником командной строки](/ru/pgbadger/command-line/).
3. Настройте [журналирование PostgreSQL](/ru/pgbadger/postgresql-logging/) с префиксом, пригодным для разбора.
4. Выберите подходящий режим [параллельной обработки](/ru/pgbadger/parallel-processing/).
5. Безопасно создавайте [инкрементальные отчёты](/ru/pgbadger/incremental-reports/).
6. Выберите [формат вывода](/ru/pgbadger/output-formats/) и изучите [локальные примеры](/ru/pgbadger/sample-reports/).
7. Следите за [историей выпусков](/ru/pgbadger/releases/), обращайтесь за [поддержкой](/ru/pgbadger/support/) и изучите [лицензию](/ru/pgbadger/license/).

## Ссылки на исходный проект {#upstream-links}

- [Сайт проекта](https://pgbadger.darold.net/)
- [Исходный код](https://github.com/darold/pgbadger)
- [Выпуски](https://github.com/darold/pgbadger/releases)
- [Трекер задач](https://github.com/darold/pgbadger/issues)
