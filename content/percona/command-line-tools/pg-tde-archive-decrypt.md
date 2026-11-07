---
title: pg_tde_archive_decrypt
linkTitle: Archive WAL
description: Decrypt WAL while wrapping an archive command for tools that require plaintext WAL.
type: docs
translation_notice: false
upstream_link: https://github.com/percona/pg_tde/blob/1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39/documentation/docs/command-line-tools/pg-tde-archive-decrypt.md
upstream_name: percona/pg_tde documentation
upstream_copyright: Copyright © 2024–2025 Percona LLC and/or its affiliates
upstream_license: LicenseRef-pg-tde
upstream_notice: /percona/site/attribution/
upstream_ref: 1660e66a6a30d3b8a9020eef7d1fba51bf7e8e39
upstream_modified: true
weight: 720
upstream_source: percona
---

The `pg_tde_archive_decrypt` tool wraps an archive command and decrypts WAL files before archiving. It allows external tools to access unencrypted WAL data, which is required because WAL encryption keys in the two-key hierarchy are host-specific and may not be available on the replay host.

> [!TIP]
> For more information on the encryption architecture and key hierarchy, see [Architecture](/percona/architecture/overview/).

This tool is often used in conjunction with [pg_tde_restore_encrypt](/percona/command-line-tools/pg-tde-restore-encrypt/) to support WAL archive.

## How it works {#how-it-works}

1. Decrypts the WAL segment to a temporary file on a RAM disk (`/dev/shm`)
2. Replaces `%p` and `%f` in the archive command with the path and name of the decrypted file
3. Executes the archive command

> [!NOTE]
>
> To ensure security, encrypt the files stored in your WAL archive using tools like `PgBackRest`.

## Usage {#usage}

```bash
pg_tde_archive_decrypt [OPTION]
pg_tde_archive_decrypt DEST-NAME SOURCE-PATH ARCHIVE-COMMAND
```

## Parameter descriptions {#parameter-descriptions}

* `DEST-NAME`: name of the WAL file to send to the archive
* `SOURCE-PATH`: path to the original encrypted WAL file
* `ARCHIVE-COMMAND`: archive command to wrap. `%p` and `%f` are replaced with the decrypted WAL file path and WAL file name, respectively.

## Options {#options}

* `-V, --version`: show version information, then exit
* `-?, --help`: show help information, then exit

> [!NOTE]
>
> Any `%f` or `%p` parameter in `ARCHIVE-COMMAND` has to be escaped as `%%f` or `%%p` respectively if used as `archive_command` in `postgresql.conf`.

## Examples {#examples}

### Using `cp` {#using-cp}

```ini
archive_command='pg_tde_archive_decrypt %f %p "cp %%p /mnt/server/archivedir/%%f"'
```

### Using `PgBackRest` {#using-pgbackrest}

```ini
archive_command='pg_tde_archive_decrypt %f %p "pgbackrest --stanza=your_stanza archive-push %%p"'
```

> [!WARNING] Required configuration
>
> A deployment with WAL encryption is not supported unless `archive_command` uses `pg_tde_archive_decrypt` and `restore_command` uses [`pg_tde_restore_encrypt`](/percona/command-line-tools/pg-tde-restore-encrypt/).
>
> Disable the following pgBackRest features in the applicable pgBackRest configuration section:
>
> ```ini
> archive-async=n
> archive-header-check=n
> checksum-page=n
> ```
