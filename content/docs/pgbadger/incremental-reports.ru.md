---
title: "Инкрементальные отчёты"
linkTitle: "Инкрементальные отчёты"
weight: 60
description: "Создание ежедневных и еженедельных отчётов, управление хранением, пересборка вывода и добавление месячных сводок"
search_keywords: [--day-report, --explode, --extra-files, --incremental, --iso-week-number, --last-parsed, --month-report, --no-week, --noreport, --outdir, --rebuild, --retention, --start-monday, day, day-report, explode, extra, extra-files, files, incremental, iso, iso-week-number, last, last-parsed, monday, month, month-report, no, no-week, noreport, number, outdir, parsed, rebuild, report, retention, start, start-monday, week]
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [Задача]
aliases: [/pgbadger/incremental-reports/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

Инкрементальный режим сохраняет разобранную статистику в двоичном виде, а затем строит по одному HTML-отчёту на день, накопительный отчёт на неделю и связывающий их календарный индекс. Он предназначен для регулярной обработки ротируемых журналов без повторного учёта одних и тех же записей.

## Создание ежедневных и еженедельных отчётов {#daily-and-weekly}

Запускайте pgBadger после ежедневной ротации журнала и укажите постоянный каталог вывода:

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

Параметр `-I` включает инкрементальный режим, а `-O` выбирает каталог для двоичного состояния, календарного индекса и сгенерированных отчётов. pgBadger самостоятельно ведёт инкрементальное состояние в этом каталоге, поэтому `--last-parsed` не нужен, если только вы намеренно не хотите хранить файл состояния в другом месте.

Чтобы выводить HTML в отдельный каталог, сохраняя двоичное состояние в исходном каталоге, используйте:

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

Считайте двоичные файлы исходными данными для будущих пересборок. Создавайте их резервные копии или сохраняйте исходные журналы, если возможность повторного создания отчётов важна.

## Срок хранения {#retention}

Оставляйте только выбранное число недель:

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

Каталоги старых недель и дней удаляются автоматически. Прежде чем применять политику к единственной истории отчётов, проверьте её на непроизводственной копии.

## Раздельная запись общих ресурсов {#shared-assets}

По умолчанию HTML-отчёты включают JavaScript и CSS внутрь файла. В каталоге с большим числом инкрементальных отчётов параметр `-X` / `--extra-files` записывает общие ресурсы отдельно и уменьшает дублирование в выводе:

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

Все отчёты и каталог ресурсов соответствующей версии необходимо перемещать вместе.

## Пересборка существующих отчётов {#rebuild}

После обновления pgBadger или исправления генератора отчётов пересоберите HTML из сохранённых двоичных данных:

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

Если исходные отчёты создавались отдельно по базам данных, снова укажите `-E` / `--explode`.

> Используйте длинный параметр `--rebuild`. В текущем справочнике команд `-R` означает `--retention`; если принять `-R` за сокращение для пересборки, будет применён неверный параметр.

## Добавление месячного отчёта {#monthly-reports}

Ежедневные и еженедельные отчёты создаются автоматически. Месячное агрегирование запускается явно, поскольку для большой истории оно может быть ресурсоёмким:

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

Созданный месяц добавляется в календарный индекс. Повторный запуск команды пересобирает отчёт за этот месяц из доступных двоичных данных. Для истории по отдельным базам данных снова укажите `-E`:

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

Полный справочник команд также описывает `--day-report YYYY-MM-DD`, `--no-week`, `--noreport`, `--start-monday` и `--iso-week-number` для более специализированных расписаний.

Откройте включённый [пример инкрементального отчёта](/third_party/pgbadger/examples/report/index.html), чтобы без подключения к сети изучить календарь, ссылки на недели и иерархию ежедневных отчётов.
