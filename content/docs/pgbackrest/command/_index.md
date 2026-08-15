---
title: "Command Reference"
linkTitle: "Commands"
weight: 40
description: "pgBackRest command reference with all options for backup, restore, archive, and management operations."
icon: fa-solid fa-terminal
sidebar_expanded: true
module: [PGBACKREST]
categories: [Reference]
---

> Source: <https://pgbackrest.org/command.html>

## Introduction

Commands are used to execute the various pgBackRest functions. Here the command options are listed exhaustively, that is, each option applicable to a command is listed with that command even if it applies to one or more other commands. This includes all the options that may also be configured in `pgbackrest.conf`.

Non-boolean options configured in `pgbackrest.conf` can be reset to default on the command-line by using the `reset-` prefix. This feature may be used to restore a backup directly on a repository host. Normally, pgBackRest will error because it can see that the database host is remote and restores cannot be done remotely. By adding `--reset-pg1-host` on the command-line, pgBackRest will ignore the remote database host and restore locally. It may be necessary to pass a new `--pg1-path` to force the restore to happen in a specific path, i.e. not the path used on the database host.

The `no-` prefix may be used to set a boolean option to false on the command-line.

Any option may be set in an environment variable using the `PGBACKREST_` prefix and the option name in all caps replacing `-` with `_`, e.g. `pg1-path` becomes `PGBACKREST_PG1_PATH` and `stanza` becomes `PGBACKREST_STANZA`. Boolean options are represented as they would be in a configuration file, e.g. `PGBACKREST_COMPRESS="n"`, and `reset-*` variants are not allowed. Options that can be specified multiple times on the command-line or in a config file can be represented by separating the values with colons, e.g. `PGBACKREST_DB_INCLUDE="db1:db2"`.

Command-line options override environment options which override config file options.

See [Configuration Introduction](/docs/pgbackrest/configuration/#introduction) for information on option types

## Commands

| Command                                                          | Summary                                                                                 |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [**`annotate`**](/docs/pgbackrest/command/annotate/)             | Add, modify, or remove backup annotations after the backup is created.                  |
| [**`archive-get`**](/docs/pgbackrest/command/archive-get/)       | Fetch archived WAL segments for restore, PITR, or replica recovery.                     |
| [**`archive-push`**](/docs/pgbackrest/command/archive-push/)     | Accept WAL segments from PostgreSQL and push them to configured repositories.           |
| [**`backup`**](/docs/pgbackrest/command/backup/)                 | Create backups to the target repository (defaults to highest priority repository).      |
| [**`check`**](/docs/pgbackrest/command/check/)                   | Validate stanza backup/archive configuration and WAL archiving health.                  |
| [**`expire`**](/docs/pgbackrest/command/expire/)                 | Expire backups and archived WAL based on configured retention policies.                 |
| [**`help`**](/docs/pgbackrest/command/help/)                     | Show command and option help at general, command, or option level.                      |
| [**`info`**](/docs/pgbackrest/command/info/)                     | Display stanza and backup status/metadata in text or JSON format.                       |
| [**`repo-get`**](/docs/pgbackrest/command/repo-get/)             | Read repository files (like `cat`) for administration, investigation, and testing.      |
| [**`repo-ls`**](/docs/pgbackrest/command/repo-ls/)               | List repository files/paths (like `ls`) for administration, investigation, and testing. |
| [**`restore`**](/docs/pgbackrest/command/restore/)               | Restore from backup (latest by default) with optional point-in-time recovery.           |
| [**`server`**](/docs/pgbackrest/command/server/)                 | Run the pgBackRest TLS server for remote host access without SSH.                       |
| [**`server-ping`**](/docs/pgbackrest/command/server-ping/)       | Ping a pgBackRest TLS server to verify it is accepting connections.                     |
| [**`stanza-create`**](/docs/pgbackrest/command/stanza-create/)   | Create stanza metadata in all configured repositories.                                  |
| [**`stanza-delete`**](/docs/pgbackrest/command/stanza-delete/)   | Permanently remove all backups and archives for a stanza.                               |
| [**`stanza-upgrade`**](/docs/pgbackrest/command/stanza-upgrade/) | Upgrade stanza metadata after a PostgreSQL major version upgrade.                       |
| [**`start`**](/docs/pgbackrest/command/start/)                   | Re-allow pgBackRest processes to run after a previous `stop`.                           |
| [**`stop`**](/docs/pgbackrest/command/stop/)                     | Prevent new pgBackRest processes and optionally force-stop running ones.                |
| [**`verify`**](/docs/pgbackrest/command/verify/)                 | Verify that backup and archive data in the repository is valid.                         |
| [**`version`**](/docs/pgbackrest/command/version/)               | Display the installed pgBackRest version.                                               |
{.full-width}
