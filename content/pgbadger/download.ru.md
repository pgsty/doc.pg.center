---
title: "Загрузка и установка"
linkTitle: "Загрузка и установка"
weight: 20
description: "Официальные выпуски, пакеты, требования и установка из исходного кода"
search_keywords: [--content-size, --help, --robot, --version, --zcat, JSON::XS, Text::CSV_XS, content, content-size, help, robot, size, version, zcat, zstdcat]
icon: fa-solid fa-cloud-arrow-down
module: [PGBADGER]
categories: [Руководство]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

## Выбор канала распространения {#distribution-channels}

| Канал | Для чего использовать | Где находится |
|---|---|---|
| Официальный выпуск | Архивы исходного кода и примечания к выпуску | [Выпуски GitHub](https://github.com/darold/pgbadger/releases) |
| Пакет RPM | Дистрибутивы Linux на базе RPM | [Репозиторий PostgreSQL Yum](https://yum.postgresql.org/packages/) |
| Пакет Debian/Ubuntu | Дистрибутивы Linux на базе APT | [Репозиторий PostgreSQL Apt](https://wiki.postgresql.org/wiki/Apt) |
| Разрабатываемый исходный код | Текущий код, ещё не вошедший в выпуск | [darold/pgbadger](https://github.com/darold/pgbadger) |

Последняя стабильная версия, проверенная на 2026-10-23, — [pgBadger 13.2](https://github.com/darold/pgbadger/releases/tag/v13.2), выпущенная 2025-12-29. Приведённый ниже пример установки из архива выпуска устанавливает эту версию. Руководство также охватывает неопубликованный снимок разработки; чтобы воспроизвести его новое поведение, используйте приведённые ниже команды с переходом на фиксированный коммит.

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
$ git checkout --detach f373ac678c756f66a785c5ab4773d1f05f468d67
$ perl Makefile.PL
$ make
$ make test
$ sudo make install
```

Полученный код соответствует описанному здесь неопубликованному снимку разработки: [`f373ac6`](https://github.com/darold/pgbadger/commit/f373ac678c756f66a785c5ab4773d1f05f468d67), коммит от 2026-10-21 (UTC). Он новее стабильной версии 13.2 и не является новым стабильным выпуском. Разрабатываемый код может содержать изменения, ещё не описанные в примечаниях к выпуску; для сборки пакетов для производственной среды предпочтительнее архив с тегом версии.

## Проверка установки {#verify-installation}

```console
$ pgbadger --version
$ pgbadger --help
```

Далее перейдите к [справочнику командной строки](/ru/pgbadger/command-line/) и [настройке журналирования PostgreSQL](/ru/pgbadger/postgresql-logging/).
