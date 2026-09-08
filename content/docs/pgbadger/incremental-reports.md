---
title: "Incremental Reports"
linkTitle: "Incremental Reports"
weight: 60
description: "Generate daily and weekly reports, control retention, rebuild output, and add monthly summaries"
icon: fa-solid fa-calendar-days
module: [PGBADGER]
categories: [Task]
aliases: [/pgbadger/incremental-reports/]
upstream_link: "https://github.com/darold/pgbadger/blob/a1ad95a035a0c2d246fe632eb1c361d4bde0ddae/README.md"
upstream_name: "pgBadger README.md"
---

Incremental mode stores parsed statistics in binary form, then builds one HTML report per day, a cumulative report per week, and a calendar-style index linking them together. It is intended for repeated processing of rotated logs without counting the same entries again.

## Build daily and weekly reports {#daily-and-weekly}

Run pgBadger after the daily log rotation and provide a persistent output directory:

```cron {title="crontab"}
0 4 * * * /usr/bin/pgbadger -I -q /var/log/postgresql/postgresql.log.1 -O /var/www/pg_reports/
```

`-I` enables incremental mode and `-O` selects the directory that holds the binary state, calendar index, and generated reports. pgBadger maintains its own incremental state in that directory, so `--last-parsed` is unnecessary unless you deliberately want the state file elsewhere.

Use a separate HTML directory while retaining binary state in the original directory:

```console
$ pgbadger -I -O /var/lib/pgbadger/data -H /var/www/pg_reports postgresql.log.1
```

Treat the binary files as source data for future rebuilds. Back them up or retain the original logs if report regeneration matters.

## Retention {#retention}

Keep only a chosen number of weeks:

```console
$ pgbadger --incremental --retention 8 \
    --outdir /var/www/pg_reports \
    /var/log/postgresql/postgresql.log.1
```

Older week and day directories are removed automatically. Test the policy on a non-production copy before enabling it around your only report history.

## Write shared assets separately {#shared-assets}

By default, HTML reports embed their JavaScript and CSS. In a directory containing many incremental reports, `-X` / `--extra-files` writes shared assets separately and reduces duplicated output:

```console
$ pgbadger -X -I -O /var/www/pg_reports postgresql.log.1
```

All reports and their versioned resource directory must be moved together.

## Rebuild existing reports {#rebuild}

After upgrading pgBadger or applying a report-generation fix, rebuild HTML from retained binary data:

```console
$ rm /var/www/pg_reports/*.js
$ rm /var/www/pg_reports/*.css
$ pgbadger -X -I -O /var/www/pg_reports --rebuild
```

Use `-E` / `--explode` again if the original reports were generated per database.

> Use the long option `--rebuild`. In the current command reference, `-R` means `--retention`; treating `-R` as a rebuild shortcut would apply the wrong option.

## Add a monthly report {#monthly-reports}

Daily and weekly reports are automatic. Monthly aggregation is explicit because it may be expensive for a large history:

```console
$ pgbadger -X --month-report 2026-07 /var/www/pg_reports/
```

The generated month is added to the calendar index. Re-running the command rebuilds that month from the available binary data. For per-database history, repeat `-E`:

```console
$ pgbadger -E -X --month-report 2026-07 /var/www/pg_reports/
```

The complete command reference also provides `--day-report YYYY-MM-DD`, `--no-week`, `--noreport`, `--start-monday`, and `--iso-week-number` for more specialized schedules.

Open the bundled [incremental-report example](/third_party/pgbadger/examples/report/index.html) to inspect the calendar, week links, and daily-report hierarchy without a network connection.

