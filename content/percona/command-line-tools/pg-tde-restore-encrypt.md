---
title: pg_tde_restore_encrypt
linkTitle: Restore WAL
description: Wrap a restore command and encrypt the retrieved WAL before PostgreSQL reads it.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-restore-encrypt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 730
upstream_source: percona
---

> [!NOTE] Editorial correction
> The placeholder descriptions now match the tool’s built-in help. See [site errata](/percona/site/errata/).

The `pg_tde_restore_encrypt` tool wraps a normal restore command from the WAL archive and writes them to disk in a format compatible with `pg_tde`.

> [!NOTE]
>
> This command is often use together with [pg_tde_archive_decrypt](/percona/command-line-tools/pg-tde-archive-decrypt/).

## How it works {#how-it-works}

1. Replaces `%f` and `%p` in the restore command with the WAL file name and temporary file path (in `/dev/shm`)
2. Runs the restore command to fetch the unencrypted WAL from the archive and write it to the temp file
3. Encrypts the temp file and writes it to the destination path in PostgreSQL’s data directory

## Usage {#usage}

```bash
pg_tde_restore_encrypt [OPTION]
pg_tde_restore_encrypt SOURCE-NAME DEST-PATH RESTORE-COMMAND
```

## Parameter descriptions {#parameter-descriptions}

* `SOURCE-NAME`: name of the WAL file to retrieve from the archive
* `DEST-PATH`: path where the encrypted WAL file should be written
* `RESTORE-COMMAND`: restore command to wrap; `%f` and `%p` are replaced with the WAL file name and path to write the unencrypted WAL, respectively

## Options {#options}

* `-V, --version`: show version information, then exit
* `-?, --help`: show help information, then exit

> [!NOTE]
>
> Any `%f` or `%p` parameter in `RESTORE-COMMAND` has to be escaped as `%%f` or `%%p` respectively if used as `restore_command` in `postgresql.conf`.

## Examples {#examples}

### Using `cp` {#using-cp}

```ini
restore_command='pg_tde_restore_encrypt %f %p "cp /mnt/server/archivedir/%%f %%p"'
```

### Using `PgBackRest` {#using-pgbackrest}

```ini
restore_command='pg_tde_restore_encrypt %f %p "pgbackrest --stanza=your_stanza archive-get %%f \"%%p\""'
```

> [!WARNING] Required configuration
>
> A deployment with WAL encryption is not supported unless `archive_command` uses [`pg_tde_archive_decrypt`](/percona/command-line-tools/pg-tde-archive-decrypt/) and `restore_command` uses `pg_tde_restore_encrypt`.
>
> Disable the following pgBackRest features in the applicable pgBackRest configuration section:
>
> ```ini
> archive-async=n
> archive-header-check=n
> checksum-page=n
> ```
