---
title: "PostgreSQL Logging Configuration"
linkTitle: "PostgreSQL Logging"
weight: 40
description: "Configure query logging, log_line_prefix, locale, and supporting statistics for pgBadger"
search_keywords: [--prefix, lc_messages, log_autovacuum_min_duration, log_checkpoints, log_connections, log_disconnections, log_duration, log_error_verbosity, log_line_prefix, log_lock_waits, log_min_duration_statement, log_statement, log_temp_files, prefix, stderr, syslog]
icon: fa-solid fa-database
module: [PGBADGER]
categories: [Task]
upstream_link: "https://github.com/darold/pgbadger/blob/f373ac678c756f66a785c5ab4773d1f05f468d67/README.md"
upstream_name: "pgBadger README.md"
---

pgBadger can only report information that PostgreSQL writes to the log. Start with a parseable prefix and a deliberate statement-logging policy, then add the operational events you want to analyze.

## Minimum query logging {#minimum-query-logging}

To include query text and duration, enable duration-based statement logging:

```postgresql
log_min_duration_statement = 0
```

`0` logs every completed statement. On a busy server, choose a higher threshold in milliseconds to control log volume. Measure the overhead and storage growth before enabling a low threshold in production.

If you only need duration and query counts, not the query text, use:

```postgresql
log_min_duration_statement = -1
log_duration = on
```

Prefer `log_min_duration_statement` when you need the slowest-query and total-query-time reports.

## Required prefix fields {#required-prefix-fields}

A custom `log_line_prefix` must include both:

- a time field: `%t`, `%m`, or `%n`;
- a process or session field: `%p` or `%c`.

A minimal `stderr` prefix is:

```postgresql
log_line_prefix = '%t [%p]: '
```

A more useful prefix records user, database, application, and client:

```postgresql
log_line_prefix = '%t [%p]: user=%u,db=%d,app=%a,client=%h '
```

The equivalent prefix for a syslog destination omits the timestamp and process fields already supplied by syslog:

```postgresql
log_line_prefix = 'user=%u,db=%d,app=%a,client=%h '
```

Another supported key order is:

```postgresql
log_line_prefix = '%t [%p]: db=%d,user=%u,app=%a,client=%h '
```

When your prefix is not one of pgBadger's recognized forms, pass the exact value with `--prefix`. Do not simplify or retype it differently from `postgresql.conf`.

## Recommended event settings {#recommended-event-settings}

Enable the event classes you want to appear in the report:

```postgresql
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_error_verbosity = default
```

These settings can produce substantial log traffic. In particular, `log_temp_files = 0` and `log_autovacuum_min_duration = 0` log every qualifying event; adjust them to match the workload and retention budget.

## Keep server messages in English {#message-locale}

The parser recognizes PostgreSQL server messages in English. Use either:

```postgresql
lc_messages = 'en_US.UTF-8'
```

or:

```postgresql
lc_messages = 'C'
```

Locales such as `fr_FR.UTF-8` are not supported by the upstream parser.

## Avoid conflicting statement settings {#statement-setting-conflicts}

Do not enable `log_min_duration_statement`, `log_duration`, and `log_statement = 'all'` together. The same execution can be logged more than once, which inflates pgBadger counters and greatly increases log volume.

| Goal | Recommended setting |
|---|---|
| Query text plus timing | `log_min_duration_statement = 0` or a chosen threshold |
| Duration and count only | `log_min_duration_statement = -1`, `log_duration = on` |
| Broad statement auditing | Treat `log_statement` as a separate logging policy; do not combine all three settings for pgBadger statistics |

After reloading PostgreSQL, inspect several real log entries before running a large analysis. Verify that the timestamp, process/session identifier, user, database, application, and client fields match the selected format.

