---
title: "Загрузка и установка"
linkTitle: "Загрузка и установка"
weight: 20
description: "Официальные выпуски, пакеты, требования и установка из исходного кода"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Руководство]
upstream_link: "https://github.com/darold/pgbadger/blob/0514893e97296695c77755fa36c59288c3afef3e/README.md"
upstream_name: "pgBadger README.md"
---

## Выбор канала распространения {#distribution-channels}

| Канал | Для чего использовать | Где находится |
|---|---|---|
| Официальный выпуск | Архивы исходного кода и примечания к выпуску | [Выпуски GitHub](https://github.com/darold/pgbadger/releases) |
| Пакет RPM | Дистрибутивы Linux на базе RPM | [Репозиторий PostgreSQL Yum](https://yum.postgresql.org/packages/) |
| Пакет Debian/Ubuntu | Дистрибутивы Linux на базе APT | [Репозиторий PostgreSQL Apt](https://wiki.postgresql.org/wiki/Apt) |
| Разрабатываемый исходный код | Текущий код, ещё не вошедший в выпуск | [darold/pgbadger](https://github.com/darold/pgbadger) |
{.wide .expand}

Последняя стабильная версия, проверенная 2026-11-21, — [pgBadger 13.3](https://github.com/darold/pgbadger/releases/tag/v13.3), выпущенная 2026-11-03. Как пример установки из архива выпуска, так и закреплённая ниже копия устанавливают эту документированную версию.

## Требования {#requirements}

Для создания HTML-отчётов нужны только:

- современная поставка Perl;
- веб-браузер для отображения встроенных диаграмм JavaScript.

Для необязательных возможностей требуются следующие зависимости:

| Возможность | Зависимость |
|---|---|
| Разбор CSV-журналов PostgreSQL | `Text::CSV_XS` |
| Запись вывода JSON | `JSON::XS` |
| Чтение входных файлов `.gz`, `.bz2`, `.lz4`, `.xz`, `.zip` или `.zst` | соответствующая утилита `zcat`, `bzcat`, `lz4cat`, `xz`, `unzip` или `zstdcat` |

Установите поддержку JSON в Debian или Ubuntu:

```console
$ sudo apt-get install libjson-xs-perl
```

В системе на базе RPM:

```console
$ sudo yum install perl-JSON-XS
```

Параметр `--zcat` позволяет переопределить путь к программе распаковки. Если указать одну пользовательскую команду, смешивать разные форматы сжатия в одном запуске будет нельзя.

Утилита `xz` должна поддерживать `--robot`, чтобы pgBadger мог читать метаданные архива. Сжимайте журналы lz4 с параметром `--content-size`, чтобы pgBadger мог определить их несжатый размер.

## Установка из официального архива {#install-from-tarball}

Загрузите архив выпуска, затем соберите и установите его стандартными средствами Perl:

```console
$ tar xzf pgbadger-13.3.tar.gz
$ cd pgbadger-13.3
$ perl Makefile.PL
$ make
$ sudo make install
```

Стандартная схема `site` устанавливает программу как `/usr/local/bin/pgbadger`, а страницу руководства — как `/usr/local/share/man/man1/pgbadger.1`.

Для установки в стиле системного дистрибутива под `/usr` создайте Makefile следующим образом:

```console
$ perl Makefile.PL INSTALLDIRS=vendor
$ make
$ sudo make install
```

Исходный проект также поддерживает схему `INSTALLDIRS=perl`. Перед установкой в управляемую систему проверьте сгенерированные пути.

## Установка из закреплённого исходного кода {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ git checkout --detach 0514893e97296695c77755fa36c59288c3afef3e
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Эта копия соответствует [документированному выпуску v13.3](https://github.com/darold/pgbadger/releases/tag/v13.3) и закреплена на `0514893e97296695c77755fa36c59288c3afef3e`.

## Проверка установки {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Далее перейдите к [справочнику командной строки](/ru/pgbadger/command-line/) и [настройке журналирования PostgreSQL](/ru/pgbadger/postgresql-logging/).
