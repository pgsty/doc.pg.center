---
title: "Configuration Reference"
linkTitle: "Configuration"
weight: 50
description: "Complete pgBackRest configuration reference for all settings including archive, backup, repository, and cloud storage options."
icon: fa-solid fa-code
module: [PGBACKREST]
categories: [Reference]
---

--------

## Introduction

pgBackRest can be used entirely with command-line parameters but a configuration file is more practical for installations that are complex or set a lot of options. The default location for the configuration file is `/etc/pgbackrest/pgbackrest.conf`. If no file exists in that location then the old default of `/etc/pgbackrest.conf` will be checked.

The following option types are used:

**String**: A text string, commonly an identifier, password, etc.

Command line example: `--stanza=demo`<br/>Configuration file example: `repo1-cipher-pass=zWaf6XtpjIVZC5444yXB...`

**Path**: Used to uniquely identify a location in a directory structure. Paths must begin with /, double // is not allowed, and no ending / is expected.

Command line example: `--repo1-path=/var/lib/pgbackrest`<br/>Configuration file example: `repo1-path=/var/lib/pgbackrest`

**Boolean**: Enables or disables the option. Only y/n are valid argument values.

Command line examples: `--start-fast`, `--no-start-fast`, `--start-fast=y`, `--start-fast=n`<br/>Configuration file examples: `start-fast=y`, `start-fast=n`

**Integer**: Used for ports, retention/retry counts, parallel processes allowed, etc.

Command line example: `--compress-level=3`<br/>Configuration file example: `pg1-port=5432`

**Size**: Used for buffer sizes, disk usage, etc. Size can be specified in bytes (default) or KiB, MiB, GiB, TiB, or PiB where the multiplier is a power of 1024. For example, the case-insensitive value 5GiB (or 5GB, 5g) can be used instead of 5368709120. Fractional values such as 2.5GiB are not allowed, use 2560MiB instead.

Command line example: `--archive-get-queue-max=1GiB`<br/>Configuration file example: `buffer-size=2MiB`

**Time**: Time in seconds.

Command line example: `--io-timeout=90`<br/>Configuration file example: `db-timeout=600`

**List**: Option may be provided multiple times.

Command line example: `--db-exclude=db1 --db-exclude=db2 --db-exclude=db5`<br/>Configuration file example, each on its own line: `db-exclude=db1 db-exclude=db2 db-exclude=db5`

**Key/Value**: Option may be provided multiple times in the form `key=value`.

Command line example: `--tablespace-map=ts_01=/db/ts_01 --tablespace-map=ts_02=/db/ts_02`<br/>Configuration file example, each on its own line: `tablespace-map=ts_01=/db/ts_01 tablespace-map=ts_02=/db/ts_02`

--------

## Archive Options

The `archive` section defines options for the `archive-push` and `archive-get` commands.

### Asynchronous Archiving Option (`--archive-async`)

Push/get WAL segments asynchronously.

Enables asynchronous operation for the `archive-push` and `archive-get` commands.

Asynchronous operation is more efficient because it can reuse connections and take advantage of parallelism. See the `spool-path`, `archive-get-queue-max`, and `archive-push-queue-max` options for more information.

```text
default: n
example: archive-async=y
```

### Maximum Archive Get Queue Size Option (`--archive-get-queue-max`)

Maximum size of the pgBackRest archive-get queue.

Specifies the maximum size of the `archive-get` queue when `archive-async` is enabled. The queue is stored in the `spool-path` and is used to speed providing WAL to PostgreSQL.

```text
default: 128MiB
allowed: [0B, 4PiB]
example: archive-get-queue-max=1GiB
```

### Retry Missing WAL Segment Option (`--archive-missing-retry`)

Retry missing WAL segment

Retry a WAL segment that was previously reported as missing by the `archive-get` command when in asynchronous mode. This prevents notifications in the spool path from a prior restore from being used and possibly causing a recovery failure if consistency has not been reached.

Disabling this option allows PostgreSQL to more reliably recognize when the end of the WAL in the archive has been reached, which permits it to switch over to streaming from the primary. With retries enabled, a steady stream of WAL being archived will cause PostgreSQL to continue getting WAL from the archive rather than switch to streaming.

When disabling this option it is important to ensure that the spool path for the stanza is empty. The `restore` command does this automatically if the spool path is configured at restore time. Otherwise, it is up to the user to ensure the spool path is empty.

```text
default: y
example: archive-missing-retry=n
```

### Archive Push Batch Size Option (`--archive-push-batch-size`)

Maximum amount of WAL to push per asynchronous run.

In asynchronous mode the `archive-push` process pushes all the WAL segments that are ready in a single run. Since `archive-push-queue-max` is only checked at the start of each run, a run that processes a very large number of segments can let the queue grow well beyond the limit before it is rechecked.

This option limits the amount of WAL processed per run so the process exits and is spawned again by the next `archive-push`, which rechecks the queue. Lower values recheck the queue more often at the cost of spawning the asynchronous process more frequently. The value is rounded down to a whole number of WAL segments but at least one segment is always processed.

```text
default: 16GiB
allowed: [1MiB, 4PiB]
example: archive-push-batch-size=1GiB
```

### Maximum Archive Push Queue Size Option (`--archive-push-queue-max`)

Maximum size of the PostgreSQL archive queue.

After the limit is reached, the following will happen:

- pgBackRest will notify PostgreSQL that the WAL was successfully archived, then **DROP IT**.
- A warning will be output to the PostgreSQL log.

If this occurs then the archive log stream will be interrupted and PITR will not be possible past that point. A new backup will be required to regain full restore capability.

In asynchronous mode the entire queue will be dropped to prevent spurts of WAL getting through before the queue limit is exceeded again.

In asynchronous mode this limit is only checked at the start of each `archive-push` run, so the queue can grow beyond it within a single run. Reduce `archive-push-batch-size` to check the queue more frequently.

The purpose of this feature is to prevent the log volume from filling up at which point PostgreSQL will stop completely. Better to lose the backup than have PostgreSQL go down.

```text
allowed: [0B, 4PiB]
example: archive-push-queue-max=1TiB
```

Deprecated Name: archive-queue-max

### Archive Timeout Option (`--archive-timeout`)

Archive timeout.

Set maximum time, in seconds, to wait for each WAL segment to reach the pgBackRest archive repository. The timeout applies to the `check` and `backup` commands when waiting for WAL segments required for backup consistency to be archived.

```text
default: 1m
allowed: [100ms, 1d]
example: archive-timeout=30
```

--------

## Backup Options

The `backup` section defines settings related to backup.

### Backup Annotation Option (`--annotation`)

Annotate backup with user-defined key/value pairs.

Users can attach informative key/value pairs to the backup. This option may be used multiple times to attach multiple annotations.

Annotations are output by the `info` command text output when a backup is specified with `--set` and always appear in the JSON output.

```text
example: annotation=source="Sunday backup for website database"
```

### Check Archive Option (`--archive-check`)

Check that WAL segments are in the archive before backup completes.

Checks that all WAL segments required to make the backup consistent are present in the WAL archive. It's a good idea to leave this as the default unless you are using another method for archiving.

This option must be enabled if `archive-copy` is enabled.

```text
default: y
example: archive-check=n
```

### Copy Archive Option (`--archive-copy`)

Copy WAL segments needed for consistency to the backup.

This slightly paranoid option protects against corruption in the WAL segment archive by storing the WAL segments required for consistency directly in the backup. WAL segments are still stored in the archive so this option will use additional space.

It is best if the `archive-push` and `backup` commands have the same `compress-type` (e.g. `lz4`) when using this option. Otherwise, the WAL segments will need to be recompressed with the `compress-type` used by the backup, which can be fairly expensive depending on how much WAL was generated during the backup.

On restore, the WAL segments will be present in `pg_xlog/pg_wal` and PostgreSQL will use them in preference to calling the `restore_command`.

The `archive-check` option must be enabled if `archive-copy` is enabled.

```text
default: n
example: archive-copy=y
```

### Check Archive Mode Option (`--archive-mode-check`)

Check the PostgreSQL `archive_mode` setting.

Enabled by default, this option disallows PostgreSQL `archive_mode=always`.

WAL segments pushed from a standby server might be logically the same as WAL segments pushed from the primary but have different checksums. Disabling archiving from multiple sources is recommended to avoid conflicts.

CAUTION:

If this option is disabled then it is critical to ensure that only one archiver is writing to the repository via the `archive-push` command.

```text
default: y
example: archive-mode-check=n
```

### Backup from Standby Option (`--backup-standby`)

Backup from the standby cluster.

Enable backup from standby to reduce load on the primary cluster. This option requires that both the primary and standby hosts be configured.

The following modes are supported:

- `y` - Standby is required for backup.
- `prefer` - Backup from standby if available otherwise backup from primary.
- `n` - Backup from primary only.

```text
default: n
example: backup-standby=y
```

### Page Checksums Option (`--checksum-page`)

Validate data page checksums.

Directs pgBackRest to validate all data page checksums while backing up a cluster. This option is automatically enabled when data page checksums are enabled on the cluster.

Failures in checksum validation will not abort a backup. Rather, warnings will be emitted in the log (and to the console with default settings) and the list of invalid pages will be stored in the backup manifest.

```text
example: checksum-page=n
```

### Path/File Exclusions Option (`--exclude`)

Exclude paths/files from the backup.

All exclusions are relative to `$PGDATA`. If the exclusion ends with / then only files in the specified directory will be excluded, e.g. `--exclude=junk/` will exclude all files in the `$PGDATA/junk` directory but include the directory itself. If the exclusion does not end with / then the file may match the exclusion exactly or match with / appended to the exclusion, e.g. `--exclude=junk` will exclude the `$PGDATA/junk` directory and all the files it contains.

**Be careful using this feature -- it is very easy to exclude something critical that will make the backup inconsistent. Be sure to test your restores!**

All excluded files will be logged at `info` level along with the exclusion rule. Be sure to audit the list of excluded files to ensure nothing unexpected is being excluded.

NOTE:

Exclusions are not honored on delta restores. Any files/directories that were excluded by the backup will be *removed* on delta restore.

This option should not be used to exclude PostgreSQL logs from a backup. Logs can be moved out of the `PGDATA` directory using the PostgreSQL `log_directory` setting, which has the benefit of allowing logs to be preserved after a restore.

Multiple exclusions may be specified on the command-line or in a configuration file.

```text
example: exclude=junk/
```

### Expire Auto Option (`--expire-auto`)

Automatically run the `expire` command after a successful backup.

The setting is enabled by default. Use caution when disabling this option as doing so will result in retaining all backups and archives indefinitely, which could cause your repository to run out of space. The `expire` command will need to be run regularly to prevent this from happening.

When `expire` is run automatically after a successful backup it uses the configuration of the `backup` command, so options set only in an `expire` command section (e.g. `[global:expire]`) are not applied. To apply `expire`-specific configuration, disable this option and run the `expire` command separately.

```text
default: y
example: expire-auto=y
```

### Manifest Save Threshold Option (`--manifest-save-threshold`)

Manifest save threshold during backup.

Defines how often the manifest will be saved during a backup. Saving the manifest is important because it stores the checksums and allows the resume function to work efficiently. The actual threshold used is 1% of the backup size or `manifest-save-threshold`, whichever is greater.

```text
default: 1GiB
allowed: [1B, 1TiB]
example: manifest-save-threshold=8GiB
```

### Resume Option (`--resume`)

Allow resume of failed backup.

Defines whether the resume feature is enabled. Resume can greatly reduce the amount of time required to run a backup after a previous backup of the same type has failed. It adds complexity, however, so it may be desirable to disable in environments that do not require the feature.

```text
default: y
example: resume=n
```

### Start Fast Option (`--start-fast`)

Force a checkpoint to start backup quickly.

Forces a checkpoint (by passing `y` to the `fast` parameter of the backup start function) so the backup begins immediately. Otherwise the backup will start after the next regular checkpoint.

```text
default: n
example: start-fast=y
```

--------

## General Options

The `general` section defines options that are common for many commands.

### Allow Run as Root Option (`--allow-root`)

Allow the command to run as the root user.

By default only the `restore` command may be run as the root user since it is designed to carefully manage file ownership. Running other commands as root risks creating files (e.g. in the repository) that are owned by root and therefore inaccessible to the PostgreSQL user, causing later commands to fail.

Enable this option to run a command as root anyway. However, it is far better to run pgBackRest as the user that owns the repository and PostgreSQL cluster.

```text
default: n
example: allow-root=y
```

### Buffer Size Option (`--buffer-size`)

Buffer size for I/O operations.

Buffer size used for copy, compress, encrypt, and other operations. The number of buffers used depends on options and each operation may use additional memory, e.g. `gz` compression may use an additional 256KiB of memory.

Allowed values are `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB`, and `16MiB`.

```text
default: 1MiB
example: buffer-size=2MiB
```

### pgBackRest Command Option (`--cmd`)

pgBackRest command.

pgBackRest may generate a command string, e.g. when the `restore` command generates the restore_command setting. The command used to run the pgBackRest process will be used in this case unless the `cmd` option is provided.

CAUTION:

Wrapping the pgBackRest command may cause unpredictable behavior and is not recommended.

```text
default: [path of executed pgbackrest binary]
example: cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### SSH Client Command Option (`--cmd-ssh`)

SSH client command.

Use a specific SSH client command when an alternate is desired or the `ssh` command is not in $PATH.

```text
default: ssh
example: cmd-ssh=/usr/bin/ssh
```

### Compress Option (`--compress`)

Use file compression.

Backup files are compatible with command-line compression tools.

This option is now deprecated. The `compress-type` option should be used instead.

```text
default: y
example: compress=n
```

### Compress Level Option (`--compress-level`)

File compression level.

Sets the level to be used for file compression when `compress-type` does not equal `none` or `compress=y` (deprecated).

```text
default (depending on compress-type):
    bz2 - 9
    gz - 6
    lz4 - 1
    zst - 3

allow range (depending on compress-type):
    bz2 - [1, 9]
    gz - [-1, 9]
    lz4 - [-5, 12]
    zst - [-7, 22]

example: compress-level=9
```

### Network Compress Level Option (`--compress-level-network`)

Network compression level.

Sets the network compression level when `compress-type=none` and the command is not run on the same host as the repository. Compression is used to reduce network traffic. When `compress-type` does not equal `none` the `compress-level-network` setting is ignored and `compress-level` is used instead so that the file is only compressed once.

```text
default: 1
allowed: [-5, 12]
example: compress-level-network=1
```

### Compress Type Option (`--compress-type`)

File compression type.

The following compression types are supported:

- `none` - no compression
- `bz2` - bzip2 compression format
- `gz` - gzip compression format
- `lz4` - lz4 compression format (not available on all platforms)
- `zst` - Zstandard compression format (not available on all platforms)

```text
default: gz
example: compress-type=none
```

### Database Timeout Option (`--db-timeout`)

Database query timeout.

Sets the timeout, in seconds, for queries against the database. This includes the backup start/stop functions which can each take a substantial amount of time. Because of this the timeout should be kept high unless you know that these functions will return quickly (i.e. if you have set `start-fast=y` and you know that the database cluster will not generate many WAL segments during the backup).

NOTE:

The `db-timeout` option must be less than the `protocol-timeout` option.

```text
default: 30m
allowed: [100ms, 7d]
example: db-timeout=600
```

### Delta Option (`--delta`)

Restore or backup using checksums.

During a restore, by default the PostgreSQL data and tablespace directories are expected to be present but empty. This option performs a delta restore using checksums.

During a backup, this option will use checksums instead of the timestamps to determine if files will be copied.

```text
default: n
example: delta=y
```

### I/O Timeout Option (`--io-timeout`)

I/O timeout.

Timeout, in seconds, used for connections and read/write operations.

Note that the entire read/write operation does not need to complete within this timeout but *some* progress must be made, even if it is only a single byte.

```text
default: 1m
allowed: [100ms, 1h]
example: io-timeout=120
```

### Lock Path Option (`--lock-path`)

Path where lock files are stored.

The lock path provides a location for pgBackRest to create lock files to prevent conflicting operations from being run concurrently.

```text
default: /tmp/pgbackrest
example: lock-path=/backup/db/lock
```

### Neutral Umask Option (`--neutral-umask`)

Use a neutral umask.

Sets the umask to 0000 so modes in the repository are created in a sensible way. The default directory mode is 0750 and default file mode is 0640.

To use the executing user's umask instead specify `neutral-umask=n` in the config file or `--no-neutral-umask` on the command line.

```text
default: y
example: neutral-umask=n
```

### Set Process Priority Option (`--priority`)

Set process priority.

Defines how much priority (i.e. niceness) will be given to the process by the kernel scheduler. Positive values decrease priority and negative values increase priority. In most case processes do not have permission to increase their priority.

```text
allowed: [-20, 19]
example: priority=19
```

### Process Maximum Option (`--process-max`)

Max processes to use for compress/transfer.

Each process will perform compression and transfer to make the command run faster, but don't set `process-max` so high that it impacts database performance.

```text
default: 1
allowed: [1, 999]
example: process-max=4
```

### Protocol Timeout Option (`--protocol-timeout`)

Protocol timeout.

Sets the timeout, in seconds, that the local or remote process will wait for a new message to be received on the protocol layer. This prevents processes from waiting indefinitely for a message.

NOTE:

The `protocol-timeout` option must be greater than the `db-timeout` option.

```text
default: 31m
allowed: [100ms, 7d]
example: protocol-timeout=630
```

### Keep Alive Option (`--sck-keep-alive`)

Keep-alive enable.

Enables keep-alive messages on socket connections.

```text
default: y
example: sck-keep-alive=n
```

### Spool Path Option (`--spool-path`)

Path where transient data is stored.

This path is used to store data for the asynchronous `archive-push` and `archive-get` command.

The asynchronous `archive-push` command writes acknowledgements into the spool path when it has successfully stored WAL in the archive (and errors on failure) so the foreground process can quickly notify PostgreSQL. Acknowledgement files are very small (zero on success and a few hundred bytes on error).

The asynchronous `archive-get` command queues WAL in the spool path so it can be provided very quickly when PostgreSQL requests it. Moving files to PostgreSQL is most efficient when the spool path is on the same filesystem as `pg_xlog`/`pg_wal`. However, it is not recommended to place the spool path *within* the `pg_xlog`/`pg_wal` directory as this may cause issues for PostgreSQL utilities such as `pg_rewind`.

The data stored in the spool path is not strictly temporary since it can and should survive a reboot. However, loss of the data in the spool path is not a problem. pgBackRest will simply recheck each WAL segment to ensure it is safely archived for `archive-push` and rebuild the queue for `archive-get`.

The spool path is intended to be located on a local Posix-compatible filesystem, not a remote filesystem such as NFS or CIFS.

```text
default: /var/spool/pgbackrest
example: spool-path=/backup/db/spool
```

### Keep Alive Count Option (`--tcp-keep-alive-count`)

Keep-alive count.

Specifies the number of TCP keep-alive messages that can be lost before the connection is considered dead.

This option is available on systems that support the `TCP_KEEPCNT` socket option.

```text
allowed: [1, 32]
example: tcp-keep-alive-count=3
```

### Keep Alive Idle Option (`--tcp-keep-alive-idle`)

Keep-alive idle time.

Specifies the amount of time (in seconds) with no network activity after which the operating system should send a TCP keep-alive message.

This option is available on systems that support the `TCP_KEEPIDLE` socket option.

```text
allowed: [1, 3600]
example: tcp-keep-alive-idle=60
```

### Keep Alive Interval Option (`--tcp-keep-alive-interval`)

Keep-alive interval time.

Specifies the amount of time (in seconds) after which a TCP keep-alive message that has not been acknowledged should be retransmitted.

This option is available on systems that support the `TCP_KEEPINTVL` socket option.

```text
allowed: [1, 900]
example: tcp-keep-alive-interval=30
```

### TLSv1.2 cipher suites Option (`--tls-cipher-12`)

Allowed TLSv1.2 cipher suites.

All TLS connections between the pgBackRest client and server are encrypted. By default, connections to objects stores (e.g. S3) are also encrypted.

NOTE:

The absolute minimum security level for any transport connection is TLSv1.2.

The accepted cipher suites can be adjusted if need arises. The example is reasonable choice unless you have specific security requirements. If unset (the default), the default of the underlying OpenSSL library applies.

```text
example: tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### TLSv1.3 cipher suites Option (`--tls-cipher-13`)

Allowed TLSv1.3 cipher suites.

All TLS connections between the pgBackRest client and server are encrypted. By default, connections to objects stores (e.g. S3) are also encrypted.

NOTE:

The absolute minimum security level for any transport connection is TLSv1.2.

The accepted cipher suites can be adjusted if need arises. If unset (the default), the default of the underlying OpenSSL library applies.

```text
example: tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

--------

## Log Options

The `log` section defines logging-related settings.

CAUTION:

Trace-level logging may expose secrets such as keys and passwords. Use with caution!

### Console Log Level Option (`--log-level-console`)

Level for console logging.

The following log levels are supported:

- `off` - No logging at all (not recommended)
- `error` - Log only errors
- `warn` - Log warnings and errors
- `info` - Log info, warnings, and errors
- `detail` - Log detail, info, warnings, and errors
- `debug` - Log debug, detail, info, warnings, and errors
- `trace` - Log trace (very verbose debugging), debug, info, warnings, and errors

```text
default: warn
example: log-level-console=error
```

### File Log Level Option (`--log-level-file`)

Level for file logging.

The following log levels are supported:

- `off` - No logging at all (not recommended)
- `error` - Log only errors
- `warn` - Log warnings and errors
- `info` - Log info, warnings, and errors
- `detail` - Log detail, info, warnings, and errors
- `debug` - Log debug, detail, info, warnings, and errors
- `trace` - Log trace (very verbose debugging), debug, info, warnings, and errors

```text
default: info
example: log-level-file=debug
```

### Std Error Log Level Option (`--log-level-stderr`)

Level for stderr logging.

Specifies which log levels will output to `stderr` rather than `stdout` (specified by `log-level-console`). The timestamp and process will not be output to `stderr`.

The following log levels are supported:

- `off` - No logging at all (not recommended)
- `error` - Log only errors
- `warn` - Log warnings and errors
- `info` - Log info, warnings, and errors
- `detail` - Log detail, info, warnings, and errors
- `debug` - Log debug, detail, info, warnings, and errors
- `trace` - Log trace (very verbose debugging), debug, info, warnings, and errors

```text
default: off
example: log-level-stderr=error
```

### Log Path Option (`--log-path`)

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that if `log-level-file=off` then no log path is required.

```text
default: /var/log/pgbackrest
example: log-path=/backup/db/log
```

### Log Subprocesses Option (`--log-subprocess`)

Enable logging in subprocesses.

Enable file logging for any subprocesses created by this process using the log level specified by `log-level-file`.

```text
default: n
example: log-subprocess=y
```

### Log Timestamp Option (`--log-timestamp`)

Enable timestamp in logging.

Enables the timestamp in console and file logging. This option is disabled in special situations such as generating documentation.

```text
default: y
example: log-timestamp=n
```

--------

## Maintainer Options

Maintainer options are intended to support PostgreSQL forks. The proper settings should be determined by the fork maintainer and then communicated to users of the fork.

WARNING:

Improper use of these options may lead to unexpected behavior or data corruption.

It is the responsibility of the fork maintainer to test pgBackRest with the required options. pgBackRest does not guarantee compatibility with any fork.

### Check WAL Headers Option (`--archive-header-check`)

Check PostgreSQL version/id in WAL headers.

Enabled by default, this option checks the WAL header against the PostgreSQL version and system identifier to ensure that the WAL is being copied to the correct stanza. This is in addition to checking `pg_control` against the stanza and verifying that WAL is being copied from the same PostgreSQL data directory where `pg_control` is located.

Therefore, disabling this check is fairly safe but should only be done when needed, e.g. if the WAL is encrypted.

```text
default: y
example: archive-header-check=n
```

### Page Header Check Option (`--page-header-check`)

Check PostgreSQL page headers.

Enabled by default, this option adds page header checks.

Disabling this option should be avoided except when necessary, e.g. if pages are encrypted.

```text
default: y
example: page-header-check=n
```

### Force PostgreSQL Version Option (`--pg-version-force`)

Force PostgreSQL version.

The specified PostgreSQL version will be used instead of the version automatically detected by reading `pg_control` or WAL headers. This is mainly useful for PostgreSQL forks or development versions where those values are different from the release version. The version reported by PostgreSQL via `server_version_num` must match the forced version.

WARNING:

Be cautious when using this option because `pg_control` and WAL headers will still be read with the expected format for the specified version, i.e. the format from the official open-source version of PostgreSQL. If the fork or development version changes the format of the fields that pgBackRest depends on it will lead to unexpected behavior. In general, this option will only work as expected if the fork adds all custom struct members *after* the standard PostgreSQL members.

```text
example: pg-version-force=15
```

--------

## Repository Options

The `repository` section defines options used to configure the repository.

**Indexing**: All `repo-` options are indexed to allow for configuring multiple repositories. For example, a single repository is configured with the `repo1-path`, `repo1-host`, etc. options. If there is more than one repository configured and the `--repo` option is not specified for a command, the repositories will be acted upon in highest priority order (e.g. repo1 then repo2).

The `repo-retention-*` options define how long backups will be retained. Expiration only occurs when the count of complete backups exceeds the allowed retention. In other words, if `repo1-retention-full-type` is set to `count` (default) and `repo1-retention-full` is set to 2, then there must be 3 complete backups before the oldest will be expired. If `repo1-retention-full-type` is set to `time` then `repo1-retention-full` represents days so there must be at least that many days worth of full backups before expiration can occur. Make sure you always have enough space for retention + 1 backups.

### Azure Repository Account Option (`--repo-azure-account`)

Azure repository account.

Azure account used to store the repository.

```text
example: repo1-azure-account=pg-backup
```

### Azure Repository Container Option (`--repo-azure-container`)

Azure repository container.

Azure container used to store the repository.

pgBackRest repositories can be stored in the container root by setting `repo-path=/` but it is usually best to specify a prefix, such as `/repo`, so logs and other Azure-generated content can also be stored in the container.

```text
example: repo1-azure-container=pg-backup
```

### Azure Repository Endpoint Option (`--repo-azure-endpoint`)

Azure repository endpoint.

Endpoint used to connect to the blob service. The default is generally correct unless using Azure Government.

For custom/test configurations the `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port`, and `repo-storage-verify-tls` options may be useful.

```text
default: blob.core.windows.net
example: repo1-azure-endpoint=blob.core.usgovcloudapi.net
```

### Azure Repository Key Option (`--repo-azure-key`)

Azure repository key.

A shared key or shared access signature depending on the `repo-azure-key-type` option.

```text
example: repo1-azure-key=T+9+aov82qNhrcXSNGZCzm9mjd4d75/oxxOr6r1JVpgTLA==
```

### Azure Repository Key Type Option (`--repo-azure-key-type`)

Azure repository key type.

The following types are supported for authorization:

- `shared` - Shared key
- `sas` - Shared access signature
- `auto` - Automatically authorize using Azure managed identities

```text
default: shared
example: repo1-azure-key-type=sas
```

### Azure Repository URI Style Option (`--repo-azure-uri-style`)

Azure URI Style.

The following URI styles are supported:

- `host` - Connect to `account.endpoint` host.
- `path` - Connect to `endpoint` host and prepend account to URIs.

```text
default: host
example: repo1-azure-uri-style=path
```

### Block Incremental Backup Option (`--repo-block`)

Enable block incremental backup.

Block incremental allows for more granular backups by splitting files into blocks that can be backed up independently. This saves space in the repository and can improve delta restore performance because individual blocks can be fetched without reading the entire file from the repository.

NOTE:

The `repo-bundle` option must be enabled before `repo-block` can be enabled.

The block size for a file is determined based on the file size and age. Generally, older/larger files will get larger block sizes. If a file is old enough, it will not be backed up using block incremental.

Block incremental is most efficient when enabled for all backup types, including full. This makes the full a bit larger but subsequent differential and incremental backups can make use of the block maps generated by the full backup to save space.

```text
default: n
example: repo1-block=y
```

### Repository Bundles Option (`--repo-bundle`)

Bundle files in repository.

Bundle (combine) smaller files to reduce the total number of files written to the repository. Writing fewer files is generally more efficient, especially on object stores such as S3. In addition, zero-length files are not stored (except in the manifest), which saves time and space.

```text
default: n
example: repo1-bundle=y
```

### Repository Bundle Limit Option (`--repo-bundle-limit`)

Limit for file bundles.

Size limit for files that will be included in bundles. Files larger than this size will be stored separately.

Bundled files cannot be reused when a backup is resumed, so this option controls the files that can be resumed, i.e. higher values result in fewer resumable files.

```text
default: 2MiB
allowed: [8KiB, 1PiB]
example: repo1-bundle-limit=10MiB
```

### Repository Bundle Size Option (`--repo-bundle-size`)

Target size for file bundles.

Defines the target size for files that will be added to a single bundle. The uncompressed bundle size may be as large as `repo-bundle-size` + `repo-bundle-limit`, so do not set this option to the maximum size that your file system allows.

In general, it is not a good idea to set this option too high because retries will need to redo the entire bundle.

```text
default: 20MiB
allowed: [1MiB, 1PiB]
example: repo1-bundle-size=10MiB
```

### Repository Cipher Passphrase Option (`--repo-cipher-pass`)

Repository cipher passphrase.

Passphrase used to encrypt/decrypt files of the repository.

NOTE:

When run without the `stanza` option the `info` command reads encryption settings only from the `global` section. If encryption settings are configured per stanza, run the `info` command with the `stanza` option to read an encrypted stanza.

```text
example: repo1-cipher-pass=zWaf6XtpjIVZC5444yXB+cgFDFl7MxGlgkZSaoPvTGirhPygu4jOKOXf9LO4vjfO
```

### Repository Cipher Type Option (`--repo-cipher-type`)

Cipher used to encrypt the repository.

The following cipher types are supported:

- `none` - The repository is not encrypted
- `aes-256-cbc` - Advanced Encryption Standard with 256 bit key length

Note that encryption is always performed client-side even if the repository type (e.g. S3) supports encryption.

```text
default: none
example: repo1-cipher-type=aes-256-cbc
```

### GCS Repository Bucket Option (`--repo-gcs-bucket`)

GCS repository bucket.

GCS bucket used to store the repository.

pgBackRest repositories can be stored in the bucket root by setting `repo-path=/` but it is usually best to specify a prefix, such as `/repo`, so logs and other GCS-generated content can also be stored in the bucket.

```text
example: repo1-gcs-bucket=/pg-backup
```

### GCS Repository Endpoint Option (`--repo-gcs-endpoint`)

GCS repository endpoint.

Endpoint used to connect to the storage service. May be updated to use a local GCS server or alternate endpoint.

```text
default: storage.googleapis.com
example: repo1-gcs-endpoint=localhost
```

### GCS Repository Key Option (`--repo-gcs-key`)

GCS repository key.

A token or service key file depending on the `repo-gcs-key-type` option.

```text
example: repo1-gcs-key=/etc/pgbackrest/gcs-key.json
```

### GCS Repository Key Type Option (`--repo-gcs-key-type`)

GCS repository key type.

The following types are supported for authorization:

- `auto` - Authorize using the instance service account.
- `service` - Service account from locally stored key.
- `token` - For local testing, e.g. `fakegcs`.

When `repo-gcs-key-type=service` the credentials will be reloaded when the authentication token is renewed.

```text
default: service
example: repo1-gcs-key-type=auto
```

### GCS Repository Project ID Option (`--repo-gcs-user-project`)

GCS project ID.

GCS project ID used to determine request billing.

```text
example: repo1-gcs-user-project=my-project
```

### Repository Hardlink Option (`--repo-hardlink`)

Hardlink files between backups in the repository.

Enable hard-linking of files in differential and incremental backups to their full backups. This gives the appearance that each backup is a full backup at the file-system level. Be careful, though, because modifying files that are hard-linked can affect all the backups in the set.

```text
default: n
example: repo1-hardlink=y
```

Deprecated Name: hardlink

### Repository Host Option (`--repo-host`)

Repository host when operating remotely.

When backing up and archiving to a locally mounted filesystem this setting is not required.

```text
example: repo1-host=repo1.domain.com
```

Deprecated Name: backup-host

### Repository Host Certificate Authority File Option (`--repo-host-ca-file`)

Repository host certificate authority file.

Use a CA file other than the system default for connecting to the repository host.

```text
example: repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Repository Host Certificate Authority Path Option (`--repo-host-ca-path`)

Repository host certificate authority path.

Use a CA path other than the system default for connecting to the repository host.

```text
example: repo1-host-ca-path=/etc/pki/tls/certs
```

### Repository Host Certificate File Option (`--repo-host-cert-file`)

Repository host certificate file.

Sent to repository host to prove client identity.

```text
example: repo1-host-cert-file=/path/to/client.crt
```

### Repository Host Command Option (`--repo-host-cmd`)

Repository host pgBackRest command.

Required only if the path to the pgBackRest command is different on the local and repository hosts. If not defined, the repository host command will be set the same as the local command.

```text
default: [path of executed pgbackrest binary]
example: repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Deprecated Name: backup-cmd

### Repository Host Configuration Option (`--repo-host-config`)

pgBackRest repository host configuration file.

Sets the location of the configuration file on the repository host. This is only required if the repository host configuration file is in a different location than the local configuration file.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Deprecated Name: backup-config

### Repository Host Configuration Include Path Option (`--repo-host-config-include-path`)

pgBackRest repository host configuration include path.

Sets the location of the configuration include path on the repository host. This is only required if the repository host configuration include path is in a different location than the local configuration include path.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Repository Host Configuration Path Option (`--repo-host-config-path`)

pgBackRest repository host configuration path.

Sets the location of the configuration path on the repository host. This is only required if the repository host configuration path is in a different location than the local configuration path.

```text
default: CFGOPTDEF_CONFIG_PATH
example: repo1-host-config-path=/conf/pgbackrest
```

### Repository Host Key File Option (`--repo-host-key-file`)

Repository host key file.

Proves client certificate was sent by owner.

```text
example: repo1-host-key-file=/path/to/client.key
```

### Repository Host Port Option (`--repo-host-port`)

Repository host port when `repo-host` is set.

Use this option to specify a non-default port for the repository host protocol.

NOTE:

When `repo-host-type=ssh` there is no default for `repo-host-port`. In this case the port will be whatever is configured for the command specified by `cmd-ssh`.

```text
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: repo1-host-port=25
```

Deprecated Name: backup-ssh-port

### Repository Host Protocol Type Option (`--repo-host-type`)

Repository host protocol type.

The following protocol types are supported:

- `ssh` - Secure Shell.
- `tls` - pgBackRest TLS server.

```text
default: ssh
example: repo1-host-type=tls
```

### Repository Host User Option (`--repo-host-user`)

Repository host user when `repo-host` is set.

Defines the user that will be used for operations on the repository host. Preferably this is not the `postgres` user but rather some other user like `pgbackrest`. If PostgreSQL runs on the repository host the `postgres` user can be placed in the `pgbackrest` group so it has read permissions on the repository without being able to damage the contents accidentally.

```text
default: pgbackrest
example: repo1-host-user=repo-user
```

Deprecated Name: backup-user

### Repository Path Option (`--repo-path`)

Path where backups and archive are stored.

The repository is where pgBackRest stores backups and archives WAL segments.

It may be difficult to estimate in advance how much space you'll need. The best thing to do is take some backups then record the size of different types of backups (full/incr/diff) and measure the amount of WAL generated per day. This will give you a general idea of how much space you'll need, though of course requirements will likely change over time as your database evolves.

```text
default: /var/lib/pgbackrest
example: repo1-path=/backup/db/backrest
```

### Archive Retention Option (`--repo-retention-archive`)

Number of backups worth of continuous WAL to retain.

NOTE:

WAL segments required to make a backup consistent are always retained until the backup is expired regardless of how this option is configured.

If this value is not set and `repo-retention-full-type` is `count` (default), then the archive to expire will default to the `repo-retention-full` (or `repo-retention-diff`) value corresponding to the `repo-retention-archive-type` if set to `full` (or `diff`). This will ensure that WAL is only expired for backups that are already expired. If `repo-retention-full-type` is `time`, then this value will default to removing archives that are earlier than the oldest full backup retained after satisfying the `repo-retention-full` setting.

This option must be set if `repo-retention-archive-type` is set to `incr`. If disk space is at a premium, then this setting, in conjunction with `repo-retention-archive-type`, can be used to aggressively expire WAL segments. However, doing so negates the ability to perform PITR from the backups with expired WAL and is therefore **not** recommended.

```text
allowed: [1, 9999999]
example: repo1-retention-archive=2
```

Deprecated Name: retention-archive

### Archive Retention Type Option (`--repo-retention-archive-type`)

Backup type for WAL retention.

If set to `full` pgBackRest will keep archive logs for the number of full backups defined by `repo-retention-archive`. If set to `diff` (differential) pgBackRest will keep archive logs for the number of full and differential backups defined by `repo-retention-archive`, meaning if the last backup taken was a full backup, it will be counted as a differential for the purpose of repo-retention. If set to `incr` (incremental) pgBackRest will keep archive logs for the number of full, differential, and incremental backups defined by `repo-retention-archive`. It is recommended that this setting not be changed from the default which will only expire WAL in conjunction with expiring full backups.

```text
default: full
example: repo1-retention-archive-type=diff
```

Deprecated Name: retention-archive-type

### Differential Retention Option (`--repo-retention-diff`)

Number of differential backups to retain.

When a differential backup expires, all incremental backups associated with the differential backup will also expire. When not defined all differential backups will be kept until the full backups they depend on expire.

Note that full backups are included in the count of differential backups for the purpose of expiration. This slightly reduces the number of differential backups that need to be retained in most cases.

```text
allowed: [1, 9999999]
example: repo1-retention-diff=3
```

Deprecated Name: retention-diff

### Full Retention Option (`--repo-retention-full`)

Full backup retention count/time.

When a full backup expires, all differential and incremental backups associated with the full backup will also expire. When the option is not defined a warning will be issued. If indefinite retention is desired then set the option to the max value.

```text
allowed: [1, 9999999]
example: repo1-retention-full=2
```

Deprecated Name: retention-full

### Full Retention Type Option (`--repo-retention-full-type`)

Retention type for full backups.

Determines whether the `repo-retention-full` setting represents a time period (days) or count of full backups to keep.

If set to `time` then full backups older than `repo-retention-full` will be removed from the repository if there is at least one other backup that is equal to or greater than the `repo-retention-full` setting. For example, if `repo-retention-full` is 30 (days) and there are 2 full backups: one 25 days old and one 35 days old, no full backups will be expired because expiring the 35 day old backup would leave only the 25 day old backup, which would violate the 30 day retention policy of having at least one backup 30 days old before an older one can be expired. Archived WAL older than the oldest full backup remaining will be automatically expired unless `repo-retention-archive-type` and `repo-retention-archive` are explicitly set.

If set to `count` then full backups that exceed `repo-retention-full` will be expired. For example, if `repo-retention-full` is `4` and a fifth full backup is completed, then the oldest full backup will be expired to keep the count at 4.

Note that a backup must be successfully completed before it will be considered for retention. For example, if `repo-retention-full-type` is `count` and `repo-retention-full` is `2`, then there must be 3 complete full backups before the oldest will be expired.

```text
default: count
example: repo1-retention-full-type=time
```

### Backup History Retention Option (`--repo-retention-history`)

Days of backup history manifests to retain.

A copy of the backup manifest is stored in the `backup.history` path when a backup completes. By default these files are never expired since they are useful for data mining, e.g. measuring backup and WAL growth over time.

Set `repo-retention-history` to define the number of days of backup history manifests to retain. Unexpired backups are always kept in the backup history. Specify `repo-retention-history=0` to retain the backup history only for unexpired backups.

When a full backup history manifest is expired, all differential and incremental backup history manifests associated with the full backup also expire.

```text
allowed: [0, 9999999]
example: repo1-retention-history=365
```

### S3 Repository Bucket Option (`--repo-s3-bucket`)

S3 repository bucket.

S3 bucket used to store the repository.

pgBackRest repositories can be stored in the bucket root by setting `repo-path=/` but it is usually best to specify a prefix, such as `/repo`, so logs and other AWS generated content can also be stored in the bucket.

```text
example: repo1-s3-bucket=pg-backup
```

### S3 Repository Endpoint Option (`--repo-s3-endpoint`)

S3 repository endpoint.

The AWS endpoint should be valid for the selected region.

For custom/test configurations the `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port`, and `repo-storage-verify-tls` options may be useful.

```text
example: repo1-s3-endpoint=s3.amazonaws.com
```

### S3 Repository Access Key Option (`--repo-s3-key`)

S3 repository access key.

AWS key used to access this bucket.

```text
example: repo1-s3-key=AKIAIOSFODNN7EXAMPLE
```

### S3 Repository Secret Access Key Option (`--repo-s3-key-secret`)

S3 repository secret access key.

AWS secret key used to access this bucket.

```text
example: repo1-s3-key-secret=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### S3 Repository Key Type Option (`--repo-s3-key-type`)

S3 repository key type.

The following types are supported:

- `shared` - Shared keys
- `auto` - Automatically retrieve temporary credentials
- `web-id` - Automatically retrieve web identity credentials
- `pod-id` - Automatically retrieve EKS pod identity credentials
- `process` - Retrieve credentials by executing a process

```text
default: shared
example: repo1-s3-key-type=auto
```

### S3 Repository KMS Key ID Option (`--repo-s3-kms-key-id`)

S3 repository KMS key.

Enables S3 server-side encryption using the specified AWS key management service key.

```text
example: repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### S3 Authentication Process Command Option (`--repo-s3-process-cmd`)

S3 authentication process command.

Command (and optional arguments) to execute for retrieving temporary S3 credentials. The first list entry is the command and the remaining entries are passed as parameters.

The process must output JSON containing `AccessKeyId`, `SecretAccessKey`, `SessionToken`, and `Expiration` fields. Credentials will be automatically refreshed before the expiration time. See [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) for format details.

```text
example: repo1-s3-process-cmd=/usr/local/bin/get-credentials
example: repo1-s3-process-cmd=--role
example: repo1-s3-process-cmd=my-role
```

### S3 Repository Region Option (`--repo-s3-region`)

S3 repository region.

The AWS region where the bucket was created.

```text
example: repo1-s3-region=us-east-1
```

### S3 Repository Requestor Pays Option (`--repo-s3-requester-pays`)

S3 repository requester pays.

Enables S3 requester pays.

```text
default: n
example: repo1-s3-requester-pays=n
```

### S3 Repository Role Option (`--repo-s3-role`)

S3 repository role.

The AWS role name (not the full ARN) used to retrieve temporary credentials when `repo-s3-key-type=auto`.

```text
example: repo1-s3-role=authrole
```

### S3 Repository Service Option (`--repo-s3-service`)

S3 signing service.

The S3 signing service used in SigV4 authentication. Defaults to `s3` for standard S3 endpoints. Set to `s3-outposts` when using an S3 Outposts endpoint.

```text
default: s3
example: repo1-s3-service=s3-outposts
```

### S3 Repository SSE Customer Key Option (`--repo-s3-sse-customer-key`)

S3 repository SSE customer key.

Enables S3 server-side encryption using the specified customer key.

```text
example: repo1-s3-sse-customer-key=bceb4f13-6939-4be3-910d-df54dee817b7
```

### S3 Repository STS Endpoint Option (`--repo-s3-sts-host`)

S3 repository STS endpoint.

The STS endpoint used to retrieve temporary credentials when `repo-s3-key-type=web-id` is configured. Set to a regional endpoint (e.g. `sts.us-east-1.amazonaws.com`) to use regional STS, which may be required for GovCloud, China regions, or to reduce latency.

```text
default: sts.amazonaws.com
example: repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### S3 Repository Security Token Option (`--repo-s3-token`)

S3 repository security token.

AWS security token used with temporary credentials.

```text
example: repo1-s3-token=AQoDYXdzEPT//////////wEXAMPLEtc764bNrC9SAPBSM22 ...
```

### S3 Repository URI Style Option (`--repo-s3-uri-style`)

S3 URI Style.

The following URI styles are supported:

- `host` - Connect to `bucket.endpoint` host.
- `path` - Connect to `endpoint` host and prepend bucket to URIs.

```text
default: host
example: repo1-s3-uri-style=path
```

### SFTP Repository Host Option (`--repo-sftp-host`)

SFTP repository host.

The SFTP host containing the repository.

```text
example: repo1-sftp-host=sftprepo.domain
```

### SFTP Repository Host Fingerprint Option (`--repo-sftp-host-fingerprint`)

SFTP repository host fingerprint.

SFTP repository host fingerprint generation should match the `repo-sftp-host-key-hash-type`. Generate the fingerprint via `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. The ssh host keys are normally found in the `/etc/ssh` directory.

```text
example: repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### SFTP Host Key Check Type Option (`--repo-sftp-host-key-check-type`)

SFTP host key check type.

The following SFTP host key check types are supported:

- `strict` - pgBackRest will never automatically add host keys to the ~/.ssh/known_hosts file, and refuses to connect to hosts whose host key has changed or is not found in the known hosts files. This option forces the user to manually add all new hosts.
- `accept-new` - pgBackRest will automatically add new host keys to the user's known hosts file, but will not permit connections to hosts with changed host keys.
- `fingerprint` - pgBackRest will check the host key against the fingerprint specified by the `repo-sftp-host-fingerprint` option.
- `none` - no host key checking will be performed.

```text
default: strict
example: repo1-sftp-host-key-check-type=accept-new
```

### SFTP Repository Host Key Hash Type Option (`--repo-sftp-host-key-hash-type`)

SFTP repository host key hash type.

SFTP repository host key hash type. Declares the hash type to be used to compute the digest of the remote system's host key on SSH startup. Newer versions of `libssh2` support `sha256` in addition to md5 and sha1.

```text
example: repo1-sftp-host-key-hash-type=sha256
```

### SFTP Repository Host Port Option (`--repo-sftp-host-port`)

SFTP repository host port.

SFTP repository host port.

```text
default: 22
allowed: [1, 65535]
example: repo1-sftp-host-port=22
```

### SFTP Repository Host User Option (`--repo-sftp-host-user`)

SFTP repository host user.

User on the host used to store the repository.

```text
example: repo1-sftp-host-user=pg-backup
```

### SFTP Known Hosts File Option (`--repo-sftp-known-host`)

SFTP known hosts file.

A known hosts file to search for an SFTP host match during authentication. When unspecified, pgBackRest will default to searching `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts`, and `/etc/ssh/ssh_known_hosts2`. If configured with one or more file paths, pgBackRest will search those for a match. File paths must be full or leading tilde paths. The `repo-sftp-known-host` option can be passed multiple times to specify more than one known hosts file to search. To utilize known hosts file checking `repo-sftp-host-fingerprint` must not be specified. See also `repo-sftp-host-check-type` option.

```text
example: repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### SFTP Repository Private Key File Option (`--repo-sftp-private-key-file`)

SFTP private key file.

SFTP private key file used for authentication.

```text
example: repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### SFTP Repository Private Key Passphrase Option (`--repo-sftp-private-key-passphrase`)

SFTP private key passphrase.

Passphrase used to access the private key. This is an optional feature when creating an SSH public/private key pair.

```text
example: repo1-sftp-private-key-passphrase=BeSureToGenerateAndUseASecurePassphrase
```

### SFTP Repository Public Key File Option (`--repo-sftp-public-key-file`)

SFTP public key file.

SFTP public key file used for authentication. Optional if compiled against OpenSSL, required if compiled against a different library.

```text
example: repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Repository Storage CA File Option (`--repo-storage-ca-file`)

Repository storage CA file.

Use a CA file other than the system default for storage (e.g. S3, Azure) certificates.

```text
example: repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Deprecated Names: repo-azure-ca-file, repo-s3-ca-file

### Repository Storage TLS CA Path Option (`--repo-storage-ca-path`)

Repository storage CA path.

Use a CA path other than the system default for storage (e.g. S3, Azure) certificates.

```text
example: repo1-storage-ca-path=/etc/pki/tls/certs
```

Deprecated Names: repo-azure-ca-path, repo-s3-ca-path

### Repository Storage Host Option (`--repo-storage-host`)

Repository storage host.

Connect to a host other than the storage (e.g. S3, Azure) endpoint. This is typically used for testing.

```text
example: repo1-storage-host=127.0.0.1
```

Deprecated Names: repo-azure-host, repo-s3-host

### Repository Storage Port Option (`--repo-storage-port`)

Repository storage port.

Port to use when connecting to the storage (e.g. S3, Azure) endpoint (or host if specified).

```text
default: 443
allowed: [1, 65535]
example: repo1-storage-port=9000
```

Deprecated Names: repo-azure-port, repo-s3-port

### Repository Storage Tag Option (`--repo-storage-tag`)

Repository storage tag(s).

Specify tags that will be added to objects when the repository is an object store (e.g. S3). The option can be repeated to add multiple tags.

There is no provision in pgBackRest to modify these tags so be sure to set them correctly before running `stanza-create` to ensure uniform tags across the entire repository.

```text
example: repo1-storage-tag=key1=value1
```

### Repository Storage Upload Chunk Size Option (`--repo-storage-upload-chunk-size`)

Repository storage upload chunk size.

Object stores such as S3 allow files to be uploaded in chunks when the file is too large to be stored in memory. Even if the file can be stored in memory, it is more memory efficient to limit the amount of memory used for uploads.

A larger chunk size will generally lead to better performance because it will minimize upload requests and allow more files to be uploaded in a single request rather than in chunks. The disadvantage is that memory usage will be higher and because the chunk buffer must be allocated per process, larger `process-max` values will lead to more memory being consumed overall.

Note that valid chunk sizes vary by storage type and by platform. For example, AWS S3 has a minimum chunk size of 5MiB. Terminology for chunk size varies by storage type, so when searching min/max values use "part size" for AWS S3, "chunk size" for GCS, and "block size" for Azure.

If a file is larger than 1GiB (the maximum size PostgreSQL will create by default) then the chunk size will be increased incrementally up to the maximum allowed in order to complete the file upload.

```text
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: repo1-storage-upload-chunk-size=16MiB
```

### Repository Storage Certificate Verify Option (`--repo-storage-verify-tls`)

Repository storage certificate verify.

This option provides the ability to enable/disable verification of the storage (e.g. S3, Azure) server TLS certificate. Disabling should only be used for testing or other scenarios where a certificate has been self-signed.

```text
default: y
example: repo1-storage-verify-tls=n
```

Deprecated Names: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Repository Symlink Option (`--repo-symlink`)

Create symlinks within the repository.

Enable creation of the `latest` and tablespace symlinks. These symlinks are most useful when using snapshots to do in-place recovery in the repository, which is an uncommon use case.

While this feature is likely not useful for the vast majority of users it remains on by default for legacy purposes. However, it may be useful to disable symlinks for Posix-like storage that does not support them.

```text
default: y
example: repo1-symlink=n
```

### Target Time for Repository Option (`--repo-target-time`)

Target time for repository.

The target time defines the time that commands use to read a repository on versioned storage. This allows the command to read the repository as it was at a point-in-time in order to recover data that has been deleted or corrupted by user accident or malware.

Versioned storage is supported by S3, GCS, and Azure but is generally not enabled by default. In addition to enabling versioning, it may be useful to enable object locking for S3 and soft delete for GCS or Azure.

When the `repo-target-time` option is specified then the `repo` option must also be provided. It is likely that not all repository types will support versioning and in general it makes sense to target a single repository for recovery.

Note that comparisons to the storage timestamp are <= the timestamp provided and milliseconds are truncated from the timestamp when provided.

```text
example: repo-target-time=2024-08-08 12:12:12+00
```

### Repository Type Option (`--repo-type`)

Type of storage used for the repository.

The following repository types are supported:

- `azure` - Azure Blob Storage Service
- `cifs` - Like `posix`, but disables links and directory fsyncs
- `gcs` - Google Cloud Storage
- `posix` - Posix-compliant file systems
- `s3` - AWS Simple Storage Service
- `sftp` - Secure File Transfer Protocol

When an NFS mount is used as a `posix` repository, the same rules apply to pgBackRest as described in the PostgreSQL documentation: [Creating a Database Cluster - File Systems](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).

```text
default: posix
example: repo1-type=cifs
```

--------

## Restore Options

The `restore` section defines settings used for restoring backups.

### Archive Mode Option (`--archive-mode`)

Preserve or disable archiving on restored cluster.

This option allows archiving to be preserved or disabled on a restored cluster. This is useful when the cluster must be promoted to do some work but is not intended to become the new primary. In this case it is not a good idea to push WAL from the cluster into the repository.

The following modes are supported:

- `off` - disable archiving by setting `archive_mode=off`.
- `preserve` - preserve current `archive_mode` setting.

**NOTE**: This option is not available on PostgreSQL < 12.

```text
default: preserve
example: archive-mode=off
```

### Exclude Database Option (`--db-exclude`)

Restore excluding the specified databases.

Databases excluded will be restored as sparse, zeroed files to save space but still allow PostgreSQL to perform recovery. After recovery, those databases will not be accessible but can be removed with the `drop database` command. The `--db-exclude` option can be passed multiple times to specify more than one database to exclude.

When used in combination with the `--db-include` option, `--db-exclude` will only apply to standard system databases (`template0`, `template1`, and `postgres`).

```text
example: db-exclude=db_main
```

### Include Database Option (`--db-include`)

Restore only specified databases.

This feature allows only selected databases to be restored. Databases not specifically included will be restored as sparse, zeroed files to save space but still allow PostgreSQL to perform recovery. After recovery, the databases that were not included will not be accessible but can be removed with the `drop database` command.

NOTE:

built-in databases (`template0`, `template1`, and `postgres`) are always restored unless specifically excluded.

The `--db-include` option can be passed multiple times to specify more than one database to include.

See [Restore Selected Databases](/docs/pgbackrest/user-guide/#restore-selected-databases) for additional information and caveats.

```text
example: db-include=db_main
```

### Link All Option (`--link-all`)

Restore all symlinks.

By default symlinked directories and files are restored as normal directories and files in $PGDATA. This is because it may not be safe to restore symlinks to their original destinations on a system other than where the original backup was performed. This option restores all the symlinks just as they were on the original system where the backup was performed.

```text
default: n
example: link-all=y
```

### Link Map Option (`--link-map`)

Modify the destination of a symlink.

Allows the destination file or path of a symlink to be changed on restore. This is useful for restoring to systems that have a different storage layout than the original system where the backup was generated.

```text
example: link-map=pg_xlog=/data/xlog
```

### Recovery Option (`--recovery-option`)

Set an option in `postgresql.auto.conf` or `recovery.conf`.

See [Server Configuration](https://www.postgresql.org/docs/current/runtime-config.html) for details on `postgresql.auto.conf` or `recovery.conf` options (be sure to select your PostgreSQL version). This option can be used multiple times.

For PostgreSQL >= 12, options will be written into `postgresql.auto.conf`. For all other versions, options will be written into `recovery.conf`.

NOTE:

The `restore_command` option will be automatically generated but can be overridden with this option. Be careful about specifying your own `restore_command` as pgBackRest is designed to handle this for you. Target Recovery options (recovery_target_name, recovery_target_time, etc.) are generated automatically by pgBackRest and should not be set with this option.

Since pgBackRest does not start PostgreSQL after writing the `postgresql.auto.conf` or `recovery.conf` file, it is always possible to edit/check `postgresql.auto.conf` or `recovery.conf` before manually restarting.

```text
example: recovery-option=primary_conninfo=db.mydomain.com
```

### Tablespace Map Option (`--tablespace-map`)

Restore a tablespace into the specified directory.

Moves a tablespace to a new location during the restore. This is useful when tablespace locations are not the same on a replica, or an upgraded system has different mount points.

Tablespace locations are not stored in pg_tablespace so moving tablespaces can be done with impunity. However, moving a tablespace to the `data_directory` is not recommended and may cause problems. For more information on moving tablespaces http://www.databasesoup.com/2013/11/moving-tablespaces.html is a good resource.

```text
example: tablespace-map=ts_01=/db/ts_01
```

### Map All Tablespaces Option (`--tablespace-map-all`)

Restore all tablespaces into the specified directory.

Tablespaces are restored into their original locations by default. This behavior can be modified for each tablespace with the `tablespace-map` option, but it is sometimes preferable to remap all tablespaces to a new directory all at once. This is particularly useful for development or staging systems that may not have the same storage layout as the original system where the backup was generated.

The path specified will be the parent path used to create all the tablespaces in the backup.

CAUTION:

Tablespaces created after the backup started will not be mapped. Make a new backup after a tablespace is created if tablespace mapping is required.

```text
example: tablespace-map-all=/data/tablespace
```

--------

## Server Options

The `server` section defines options used for configuring the TLS server.

### TLS Server Address Option (`--tls-server-address`)

TLS server address.

IP address the server will listen on for client requests.

```text
default: localhost
example: tls-server-address=*
```

### TLS Server Authorized Clients Option (`--tls-server-auth`)

TLS server authorized clients.

Clients are authorized on the server by verifying their certificate and checking their certificate CN (Common Name) against a list on the server configured with the `tls-server-auth` option.

A client CN can be authorized for as many stanzas as needed by providing a comma-separated list to the `tls-server-auth` option or for all stanzas by specifying `tls-server-auth=client-cn=*`. Wildcards may not be specified for the client CN.

```text
example: tls-server-auth=client-cn=stanza1,stanza2
```

### TLS Server Certificate Authorities Option (`--tls-server-ca-file`)

TLS server certificate authorities.

Checks that client certificates are signed by a trusted certificate authority.

```text
example: tls-server-ca-file=/path/to/server.ca
```

### TLS Server Certificate Option (`--tls-server-cert-file`)

TLS server certificate file.

Sent to the client to show the server identity.

```text
example: tls-server-cert-file=/path/to/server.crt
```

### TLS Server Key Option (`--tls-server-key-file`)

TLS server key file.

Proves server certificate was sent by the owner.

```text
example: tls-server-key-file=/path/to/server.key
```

### TLS Server Port Option (`--tls-server-port`)

TLS server port.

Port the server will listen on for client requests.

```text
default: 8432
allowed: [1, 65535]
example: tls-server-port=8000
```

--------

## Stanza Options

A stanza defines the backup configuration for a specific PostgreSQL database cluster. The stanza section must define the database cluster path and host/user if the database cluster is remote. Also, any global configuration sections can be overridden to define stanza-specific settings.

**Indexing**: All `pg-` options are indexed to allow for configuring multiple PostgreSQL hosts. For example, a single primary is configured with the `pg1-path`, `pg1-port`, etc. options. If a standby is configured then index the `pg-` options on the repository host as `pg2-` (e.g. pg2-host, pg2-path, etc).

### PostgreSQL Database Option (`--pg-database`)

PostgreSQL database.

The database name used when connecting to PostgreSQL. The default is usually best but some installations may not contain this database.

Note that for legacy reasons the setting of the `PGDATABASE` environment variable will be ignored.

```text
default: postgres
example: pg1-database=backupdb
```

### PostgreSQL Host Option (`--pg-host`)

PostgreSQL host for operating remotely.

Used for backups where the PostgreSQL host is different from the repository host.

```text
example: pg1-host=db.domain.com
```

Deprecated Name: db-host

### PostgreSQL Host Certificate Authority File Option (`--pg-host-ca-file`)

PostgreSQL host certificate authority file.

Use a CA file other than the system default for connecting to the PostgreSQL host.

```text
example: pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### PostgreSQL Host Certificate Authority Path Option (`--pg-host-ca-path`)

PostgreSQL host certificate authority path.

Use a CA path other than the system default for connecting to the PostgreSQL host.

```text
example: pg1-host-ca-path=/etc/pki/tls/certs
```

### PostgreSQL Host Certificate File Option (`--pg-host-cert-file`)

PostgreSQL host certificate file.

Sent to PostgreSQL host to prove client identity.

```text
example: pg1-host-cert-file=/path/to/client.crt
```

### PostgreSQL Host Command Option (`--pg-host-cmd`)

PostgreSQL host pgBackRest command.

Required only if the path to the pgBackRest command is different on the local and PostgreSQL hosts. If not defined, the PostgreSQL host command will be set the same as the local command.

```text
default: [path of executed pgbackrest binary]
example: pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Deprecated Name: db-cmd

### PostgreSQL Host Configuration Option (`--pg-host-config`)

pgBackRest database host configuration file.

Sets the location of the configuration file on the PostgreSQL host. This is only required if the PostgreSQL host configuration file is in a different location than the local configuration file.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Deprecated Name: db-config

### PostgreSQL Host Configuration Include Path Option (`--pg-host-config-include-path`)

pgBackRest database host configuration include path.

Sets the location of the configuration include path on the PostgreSQL host. This is only required if the PostgreSQL host configuration include path is in a different location than the local configuration include path.

```text
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### PostgreSQL Host Configuration Path Option (`--pg-host-config-path`)

pgBackRest database host configuration path.

Sets the location of the configuration path on the PostgreSQL host. This is only required if the PostgreSQL host configuration path is in a different location than the local configuration path.

```text
default: CFGOPTDEF_CONFIG_PATH
example: pg1-host-config-path=/conf/pgbackrest
```

### PostgreSQL Host Key File Option (`--pg-host-key-file`)

PostgreSQL host key file.

Proves client certificate was sent by owner.

```text
example: pg1-host-key-file=/path/to/client.key
```

### PostgreSQL Host Port Option (`--pg-host-port`)

PostgreSQL host port when `pg-host` is set.

Use this option to specify a non-default port for the PostgreSQL host protocol.

NOTE:

When `pg-host-type=ssh` there is no default for `pg-host-port`. In this case the port will be whatever is configured for the command specified by `cmd-ssh`.

```text
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: pg1-host-port=25
```

Deprecated Name: db-ssh-port

### PostgreSQL Host Protocol Type Option (`--pg-host-type`)

PostgreSQL host protocol type.

The following protocol types are supported:

- `ssh` - Secure Shell.
- `tls` - pgBackRest TLS server.

```text
default: ssh
example: pg1-host-type=tls
```

### PostgreSQL Host User Option (`--pg-host-user`)

PostgreSQL host logon user when `pg-host` is set.

This user will also own the remote pgBackRest process and will initiate connections to PostgreSQL. For this to work correctly the user should be the PostgreSQL database cluster owner which is generally `postgres`, the default.

```text
default: postgres
example: pg1-host-user=db_owner
```

Deprecated Name: db-user

### PostgreSQL Path Option (`--pg-path`)

PostgreSQL data directory.

This should be the same as the `data_directory` reported by PostgreSQL. Even though this value can be read from various places, it is prudent to set it in case those resources are not available during a restore or offline backup scenario.

The `pg-path` option is tested against the value reported by PostgreSQL on every online backup so it should always be current.

```text
example: pg1-path=/data/db
```

Deprecated Name: db-path

### PostgreSQL Port Option (`--pg-port`)

PostgreSQL port.

Port that PostgreSQL is running on. This usually does not need to be specified as most PostgreSQL clusters run on the default port.

```text
default: 5432
allowed: [0, 65535]
example: pg1-port=6543
```

Deprecated Name: db-port

### PostgreSQL Socket Path Option (`--pg-socket-path`)

PostgreSQL unix socket path.

The unix socket directory that was specified when PostgreSQL was started. pgBackRest will automatically look in the standard location for your OS so there is usually no need to specify this setting unless the socket directory was explicitly modified with the `unix_socket_directories` setting in `postgresql.conf`.

```text
example: pg1-socket-path=/var/run/postgresql
```

Deprecated Name: db-socket-path

### PostgreSQL Database User Option (`--pg-user`)

PostgreSQL database user.

The database user name used when connecting to PostgreSQL. If not specified pgBackRest will connect with the local OS user or `PGUSER`.

```text
example: pg1-user=backupuser
```
