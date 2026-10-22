---
title: "Форматы вывода"
linkTitle: "Форматы вывода"
weight: 70
description: "Выбор вывода HTML, текста, двоичных данных, JSON или необработанного CSV и объединение промежуточных файлов"
search_keywords: [--anonymize, --csv-separator, --dump-all-queries, --dump-raw-csv, --extension, --extra-files, --last-parsed, --normalized-only, --outfile, --prettify-json, --query-numbering, JSON::XS, all, anonymize, csv, csv-separator, dump, dump-all-queries, dump-raw-csv, extension, extra, extra-files, files, json, last, last-parsed, normalized, normalized-only, numbering, only, outfile, parsed, prettify, prettify-json, queries, query, query-numbering, raw, separator]
icon: fa-solid fa-file-export
module: [PGBADGER]
categories: [Справочник]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger выбирает формат вывода по расширению имени файла либо по параметру `-x` / `--extension`. Укажите `-o` / `--outfile` несколько раз, чтобы создать несколько форматов из одного результата разбора.

| Формат | Обычное расширение | Оптимальное применение |
|---|---|---|
| HTML | `.html` | интерактивный, удобный для чтения отчёт с диаграммами |
| Текст | `.txt` | просмотр в терминале и простое архивирование |
| Двоичный | `.bin` | объединяемая промежуточная статистика и пересборка отчётов |
| JSON | `.json` | интеграция с другим ПО; требует `JSON::XS` |
| Необработанный CSV | выбранный файл вывода | построчное извлечение с `--dump-raw-csv` |

## HTML и текст {#html-and-text}

По умолчанию результат записывается в `out.html`:

```console
$ pgbadger postgresql.log -o report.html
```

Обычно HTML включает сценарии, стили, шрифты и данные отчёта, необходимые для автономного просмотра. Параметр `-X` / `--extra-files` выносит общие JavaScript и CSS из инкрементальных отчётов; храните эти ресурсы рядом с деревом HTML.

Чтобы явно создать текстовый файл:

```console
$ pgbadger -x text -o report.txt postgresql.log
```

Укажите `-` вместо имени выходного файла, чтобы записать поддерживаемый формат в стандартный вывод.

## Двоичные промежуточные данные {#binary-format}

Двоичный вывод отделяет разбор от представления. Создавайте почасовые приращения из одного растущего суточного журнала:

```console
$ pgbadger --last-parsed .pgbadger_last_state \
    -o sunday/hour01.bin \
    /var/log/pgsql/postgresql-Sun.log
```

Объедините один или несколько двоичных файлов в новый отчёт:

```console
$ pgbadger -o sunday.html sunday/*.bin
```

Если сервер создаёт отдельный файл журнала каждый час, формируйте по одному двоичному файлу на каждую ротацию, а затем при необходимости пересобирайте накопительный HTML:

```console
$ pgbadger -o day1/hour01.bin postgresql-2026-08-15_01.log
$ pgbadger -o day1/hour02.bin postgresql-2026-08-15_02.log
$ pgbadger -o day1/hour03.bin postgresql-2026-08-15_03.log
$ pgbadger -o day1.html day1/*.bin
```

Храните вместе только двоичные файлы совместимых версий pgBadger. Перед обновлением каталога долгоживущих отчётов проверьте в примечаниях к выпуску совместимость инкрементального формата.

## JSON {#json-format}

Вывод JSON предназначен для программных потребителей, например конвейеров мониторинга и отчётности:

```console
$ pgbadger -o report.json postgresql.log
```

Сначала установите `JSON::XS`. Если размер файла и время создания вторичны, добавьте `--prettify-json` для удобства чтения.

## Необработанный и ориентированный на запросы экспорт {#raw-exports}

Справочник команд также описывает специализированные способы экспорта:

- `--dump-raw-csv` разбирает журнал и записывает построчный CSV без построения отчёта;
- `--csv-separator` меняет разделитель необработанного CSV; в 13.2 по умолчанию используется запятая;
- `--dump-all-queries` выводит каждый запрос после подстановки параметров привязки;
- `--normalized-only` записывает нормализованные запросы;
- `--query-numbering` нумерует текстовый вывод, ориентированный на запросы.

Эти режимы могут включать SQL приложения, идентификаторы, пользователей, адреса клиентов или литеральные значения. Проверяйте результат перед передачей другим и используйте `--anonymize`, если для предполагаемого анализа литералы не нужны.
