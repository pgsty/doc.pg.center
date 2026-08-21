---
title: "pgBadger 13.2 Documentation"
linkTitle: pgBadger
weight: 40
description: "Fast PostgreSQL and PgBouncer log analysis with detailed, self-contained reports"
icon: fa-solid fa-otter
type: docs
sidebar_root_for: self
sidebar_root_link_self: true
module: [PGBADGER]
categories: [Concept]
aliases: [/docs/pgbadger/, /docs/pgbadger/documentation/]
upstream_source: pgbadger
upstream_link: "https://github.com/darold/pgbadger"
cascade:
  upstream_source: pgbadger
  type: docs
  module: [PGBADGER]
---

![pgBadger logo](/img/docs/pgbadger/logo.png "pgBadger")

**pgBadger** is a fast, standalone PostgreSQL log analyzer written in Perl. It reads PostgreSQL or PgBouncer logs and produces detailed HTML, text, binary, JSON, or raw CSV output. The HTML reports are self-contained, interactive, zoomable, and need only a web browser to view.

## Why pgBadger {#why-pgbadger}

pgBadger is designed for large logs and operational use:

- one Perl program, with no mandatory non-core Perl modules;
- automatic detection of `stderr`, `syslog`, `csvlog`, `jsonlog`, RDS, Cloud SQL, logplex, Redshift, and PgBouncer input;
- direct reading of local files, standard input, remote files over SSH, and HTTP, FTP, or SFTP URLs;
- gzip, bzip2, lz4, xz, zip, and zstd compressed input;
- parallel parsing of one large file or many smaller files;
- daily, weekly, and on-demand monthly incremental reports;
- filters by time, database, user, client, application, process, session, and query pattern.

## What the reports contain {#report-coverage}

The PostgreSQL report set covers:

- overall activity and query statistics;
- slow, frequent, time-consuming, waiting, and cancelled queries;
- temporary files, checkpoints, locks, sessions, and connections;
- autovacuum and autoanalyze activity by table;
- errors and events by severity and class;
- distributions by database, user, client, application, and statement type.

PgBouncer input adds throughput, average query duration, simultaneous sessions, connection and session distributions, reserved-pool usage, and frequent error/event reports.

## Documentation map {#documentation-map}

Read the manual in this order, or use the sidebar to jump directly to a task:

1. [Download and install](download/) pgBadger and its optional modules.
2. Review the complete [command-line reference](command-line/).
3. Configure [PostgreSQL logging](postgresql-logging/) with a parseable prefix.
4. Choose the right [parallel-processing](parallel-processing/) mode.
5. Build [incremental reports](incremental-reports/) safely.
6. Select an [output format](output-formats/) and inspect the [local examples](sample-reports/).
7. Follow [release history](releases/), [support](support/), and [licensing](license/).

## Upstream links {#upstream-links}

- [Project website](https://pgbadger.darold.net/)
- [Source code](https://github.com/darold/pgbadger)
- [Releases](https://github.com/darold/pgbadger/releases)
- [Issue tracker](https://github.com/darold/pgbadger/issues)
