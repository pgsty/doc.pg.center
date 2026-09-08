---
title: "Загрузка и установка"
linkTitle: "Загрузка и установка"
weight: 20
description: "Официальные выпуски, пакеты, требования и установка из исходного кода"
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Tutorial]
aliases: [/pgbadger/download/]
upstream_link: "https://pgbadger.darold.net/#download"
upstream_name: "pgBadger website"
upstream_ref: "site snapshot of 2026-08-15"
---

## Выбор канала распространения {#distribution-channels}

| Канал | Для чего использовать | Где находится |
|---|---|---|
| Официальный выпуск | Архивы исходного кода и примечания к выпуску | [Выпуски GitHub](https://github.com/darold/pgbadger/releases) |
| Пакет RPM | Дистрибутивы Linux на базе RPM | [Репозиторий PostgreSQL Yum](https://yum.postgresql.org/packages/) |
| Пакет Debian/Ubuntu | Дистрибутивы Linux на базе APT | [Репозиторий PostgreSQL Apt](https://wiki.postgresql.org/wiki/Apt) |
| Разрабатываемый исходный код | Текущий код, ещё не вошедший в выпуск | [darold/pgbadger](https://github.com/darold/pgbadger) |

Снимок документации на этом сайте основан на дереве исходного кода версии 13.2. Перед загрузкой всегда проверяйте страницу выпусков: локальный снимок намеренно зафиксирован, тогда как исходный проект продолжает выпускать новые версии.

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

## Установка из официального архива {#install-from-tarball}

Загрузите архив выпуска, затем соберите и установите его стандартными средствами Perl:

```console
$ tar xzf pgbadger-13.2.tar.gz
$ cd pgbadger-13.2
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

## Установка разрабатываемой версии {#install-development-code}

```console
$ git clone https://github.com/darold/pgbadger.git
$ cd pgbadger
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Разрабатываемый код может содержать изменения, ещё не описанные в примечаниях к выпуску. Для воспроизводимой сборки производственного пакета предпочтительнее архив с тегом версии.

## Проверка установки {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Далее перейдите к [справочнику командной строки](/ru/docs/pgbadger/command-line/) и [настройке журналирования PostgreSQL](/ru/docs/pgbadger/postgresql-logging/).
