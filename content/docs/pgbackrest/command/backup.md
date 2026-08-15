---
title: "Backup Command (backup)"
linkTitle: "backup"
weight: 40
description: "Reference for pgBackRest `backup` command options and behavior."
icon: fa-solid fa-box-archive
module: [PGBACKREST]
categories: [Reference]
---

> Source: [pgBackRest Command Docs: backup](https://pgbackrest.org/command.html#command-backup)

When multiple repositories are configured, pgBackRest will backup to the highest priority repository (e.g. `repo1`) unless the `--repo` option is specified.

pgBackRest does not have a built-in scheduler so it's best to run it from cron or some other scheduling mechanism.

See [Perform a Backup](/docs/pgbackrest/user-guide/#perform-a-backup) for more details and examples.

## Command Options

### Backup Annotation Option (`--annotation`)

Annotate backup with user-defined key/value pairs.

Users can attach informative key/value pairs to the backup. This option may be used multiple times to attach multiple annotations.

Annotations are output by the `info` command text output when a backup is specified with `--set` and always appear in the JSON output.

```yaml
example: --annotation=source="Sunday backup for website database"
```

### Check Archive Option (`--archive-check`)

Check that WAL segments are in the archive before backup completes.

Checks that all WAL segments required to make the backup consistent are present in the WAL archive. It's a good idea to leave this as the default unless you are using another method for archiving.

This option must be enabled if `archive-copy` is enabled.

```yaml
default: y
example: --no-archive-check
```

### Copy Archive Option (`--archive-copy`)

Copy WAL segments needed for consistency to the backup.

This slightly paranoid option protects against corruption in the WAL segment archive by storing the WAL segments required for consistency directly in the backup. WAL segments are still stored in the archive so this option will use additional space.

It is best if the `archive-push` and `backup` commands have the same `compress-type` (e.g. `lz4`) when using this option. Otherwise, the WAL segments will need to be recompressed with the `compress-type` used by the backup, which can be fairly expensive depending on how much WAL was generated during the backup.

On restore, the WAL segments will be present in `pg_xlog/pg_wal` and PostgreSQL will use them in preference to calling the `restore_command`.

The `archive-check` option must be enabled if `archive-copy` is enabled.

```yaml
default: n
example: --archive-copy
```

### Check Archive Mode Option (`--archive-mode-check`)

Check the PostgreSQL `archive_mode` setting.

Enabled by default, this option disallows PostgreSQL `archive_mode=always`.

WAL segments pushed from a standby server might be logically the same as WAL segments pushed from the primary but have different checksums. Disabling archiving from multiple sources is recommended to avoid conflicts.

CAUTION:

If this option is disabled then it is critical to ensure that only one archiver is writing to the repository via the `archive-push` command.

```yaml
default: y
example: --no-archive-mode-check
```

### Archive Timeout Option (`--archive-timeout`)

Archive timeout.

Set maximum time, in seconds, to wait for each WAL segment to reach the pgBackRest archive repository. The timeout applies to the `check` and `backup` commands when waiting for WAL segments required for backup consistency to be archived.

```yaml
default: 1m
allowed: [100ms, 1d]
example: --archive-timeout=30
```

### Backup from Standby Option (`--backup-standby`)

Backup from the standby cluster.

Enable backup from standby to reduce load on the primary cluster. This option requires that both the primary and standby hosts be configured.

The following modes are supported:

- `y` - Standby is required for backup.
- `prefer` - Backup from standby if available otherwise backup from primary.
- `n` - Backup from primary only.

```yaml
default: n
example: --backup-standby=y
```

### Page Checksums Option (`--checksum-page`)

Validate data page checksums.

Directs pgBackRest to validate all data page checksums while backing up a cluster. This option is automatically enabled when data page checksums are enabled on the cluster.

Failures in checksum validation will not abort a backup. Rather, warnings will be emitted in the log (and to the console with default settings) and the list of invalid pages will be stored in the backup manifest.

```yaml
example: --no-checksum-page
```

### Path/File Exclusions Option (`--exclude`)

Exclude paths/files from the backup.

All exclusions are relative to `$PGDATA`. If the exclusion ends with / then only files in the specified directory will be excluded, e.g. `--exclude=junk/` will exclude all files in the `$PGDATA/junk` directory but include the directory itself. If the exclusion does not end with / then the file may match the exclusion exactly or match with / appended to the exclusion, e.g. `--exclude=junk` will exclude the `$PGDATA/junk` directory and all the files it contains.

**Be careful using this feature -- it is very easy to exclude something critical that will make the backup inconsistent. Be sure to test your restores!**

All excluded files will be logged at `info` level along with the exclusion rule. Be sure to audit the list of excluded files to ensure nothing unexpected is being excluded.

> **NOTE:** Exclusions are not honored on delta restores. Any files/directories that were excluded by the backup will be *removed* on delta restore.

This option should not be used to exclude PostgreSQL logs from a backup. Logs can be moved out of the `PGDATA` directory using the PostgreSQL `log_directory` setting, which has the benefit of allowing logs to be preserved after a restore.

Multiple exclusions may be specified on the command-line or in a configuration file.

```yaml
example: --exclude=junk/
```

### Expire Auto Option (`--expire-auto`)

Automatically run the `expire` command after a successful backup.

The setting is enabled by default. Use caution when disabling this option as doing so will result in retaining all backups and archives indefinitely, which could cause your repository to run out of space. The `expire` command will need to be run regularly to prevent this from happening.

When `expire` is run automatically after a successful backup it uses the configuration of the `backup` command, so options set only in an `expire` command section (e.g. `[global:expire]`) are not applied. To apply `expire`-specific configuration, disable this option and run the `expire` command separately.

```yaml
default: y
example: --expire-auto
```

### Force Option (`--force`)

Force an offline backup.

When used with `--no-start-stop` a backup will be run even if pgBackRest thinks that PostgreSQL is running. **This option should be used with extreme care as it will likely result in a bad backup.**

There are some scenarios where a backup might still be desirable under these conditions. For example, if a server crashes and the database cluster volume can only be mounted read-only, it would be a good idea to take a backup even if `postmaster.pid` is present. In this case it would be better to revert to the prior backup and replay WAL, but possibly there is a very important transaction in a WAL segment that did not get archived.

```yaml
default: n
example: --force
```

### Manifest Save Threshold Option (`--manifest-save-threshold`)

Manifest save threshold during backup.

Defines how often the manifest will be saved during a backup. Saving the manifest is important because it stores the checksums and allows the resume function to work efficiently. The actual threshold used is 1% of the backup size or `manifest-save-threshold`, whichever is greater.

```yaml
default: 1GiB
allowed: [1B, 1TiB]
example: --manifest-save-threshold=8GiB
```

### Online Option (`--online`)

Perform an online backup.

Specifying --no-online prevents pgBackRest from running the backup start/stop functions on the database cluster. In order for this to work PostgreSQL should be shut down and pgBackRest will generate an error if it is not.

The purpose of this option is to allow offline backups. The `pg_xlog`/`pg_wal` directory is copied as-is and `archive-check` is automatically disabled for the backup.

```yaml
default: y
example: --no-online
```

### Resume Option (`--resume`)

Allow resume of failed backup.

Defines whether the resume feature is enabled. Resume can greatly reduce the amount of time required to run a backup after a previous backup of the same type has failed. It adds complexity, however, so it may be desirable to disable in environments that do not require the feature.

```yaml
default: y
example: --no-resume
```

### Start Fast Option (`--start-fast`)

Force a checkpoint to start backup quickly.

Forces a checkpoint (by passing `y` to the `fast` parameter of the backup start function) so the backup begins immediately. Otherwise the backup will start after the next regular checkpoint.

```yaml
default: n
example: --start-fast
```

### Type Option (`--type`)

Backup type.

The following backup types are supported:

- `full` - all database cluster files will be copied and there will be no dependencies on previous backups.
- `incr` - incremental from the last successful backup.
- `diff` - like an incremental backup but always based on the last full backup.

```yaml
default: incr
example: --type=full
```

## General Options

### Allow Run as Root Option (`--allow-root`)

Allow the command to run as the root user.

By default only the `restore` command may be run as the root user since it is designed to carefully manage file ownership. Running other commands as root risks creating files (e.g. in the repository) that are owned by root and therefore inaccessible to the PostgreSQL user, causing later commands to fail.

Enable this option to run a command as root anyway. However, it is far better to run pgBackRest as the user that owns the repository and PostgreSQL cluster.

```yaml
default: n
example: --allow-root
```

### Buffer Size Option (`--buffer-size`)

Buffer size for I/O operations.

Buffer size used for copy, compress, encrypt, and other operations. The number of buffers used depends on options and each operation may use additional memory, e.g. `gz` compression may use an additional 256KiB of memory.

Allowed values are `16KiB`, `32KiB`, `64KiB`, `128KiB`, `256KiB`, `512KiB`, `1MiB`, `2MiB`, `4MiB`, `8MiB`, and `16MiB`.

```yaml
default: 1MiB
example: --buffer-size=2MiB
```

### pgBackRest Command Option (`--cmd`)

pgBackRest command.

pgBackRest may generate a command string, e.g. when the `restore` command generates the restore_command setting. The command used to run the pgBackRest process will be used in this case unless the `cmd` option is provided.

CAUTION:

Wrapping the pgBackRest command may cause unpredictable behavior and is not recommended.

```yaml
default: [path of executed pgbackrest binary]
example: --cmd=/var/lib/pgsql/bin/pgbackrest_wrapper.sh
```

### SSH Client Command Option (`--cmd-ssh`)

SSH client command.

Use a specific SSH client command when an alternate is desired or the `ssh` command is not in $PATH.

```yaml
default: ssh
example: --cmd-ssh=/usr/bin/ssh
```

### Compress Option (`--compress`)

Use file compression.

Backup files are compatible with command-line compression tools.

This option is now deprecated. The `compress-type` option should be used instead.

```yaml
default: y
example: --no-compress
```

### Compress Level Option (`--compress-level`)

File compression level.

Sets the level to be used for file compression when `compress-type` does not equal `none` or `compress=y` (deprecated).

```yaml
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

example: --compress-level=9
```

### Network Compress Level Option (`--compress-level-network`)

Network compression level.

Sets the network compression level when `compress-type=none` and the command is not run on the same host as the repository. Compression is used to reduce network traffic. When `compress-type` does not equal `none` the `compress-level-network` setting is ignored and `compress-level` is used instead so that the file is only compressed once.

```yaml
default: 1
allowed: [-5, 12]
example: --compress-level-network=1
```

### Compress Type Option (`--compress-type`)

File compression type.

The following compression types are supported:

- `none` - no compression
- `bz2` - bzip2 compression format
- `gz` - gzip compression format
- `lz4` - lz4 compression format (not available on all platforms)
- `zst` - Zstandard compression format (not available on all platforms)

```yaml
default: gz
example: --compress-type=none
```

### Config Option (`--config`)

pgBackRest configuration file.

Use this option to specify a different configuration file than the default.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --config=/conf/pgbackrest/pgbackrest.conf
```

### Config Include Path Option (`--config-include-path`)

Path to additional pgBackRest configuration files.

Configuration files existing in the specified location with extension `.conf` will be concatenated with the pgBackRest configuration file, resulting in one configuration file.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --config-include-path=/conf/pgbackrest/conf.d
```

### Config Path Option (`--config-path`)

Base path of pgBackRest configuration files.

This setting is used to override the default base path setting for the `--config` and `--config-include-path` options unless they are explicitly set on the command-line.

For example, passing only `--config-path=/conf/pgbackrest` results in the `--config` default being set to `/conf/pgbackrest/pgbackrest.conf` and the `--config-include-path` default being set to `/conf/pgbackrest/conf.d`.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --config-path=/conf/pgbackrest
```

### Database Timeout Option (`--db-timeout`)

Database query timeout.

Sets the timeout, in seconds, for queries against the database. This includes the backup start/stop functions which can each take a substantial amount of time. Because of this the timeout should be kept high unless you know that these functions will return quickly (i.e. if you have set `start-fast=y` and you know that the database cluster will not generate many WAL segments during the backup).

> **NOTE:** The `db-timeout` option must be less than the `protocol-timeout` option.

```yaml
default: 30m
allowed: [100ms, 7d]
example: --db-timeout=600
```

### Delta Option (`--delta`)

Restore or backup using checksums.

During a restore, by default the PostgreSQL data and tablespace directories are expected to be present but empty. This option performs a delta restore using checksums.

During a backup, this option will use checksums instead of the timestamps to determine if files will be copied.

```yaml
default: n
example: --delta
```

### I/O Timeout Option (`--io-timeout`)

I/O timeout.

Timeout, in seconds, used for connections and read/write operations.

Note that the entire read/write operation does not need to complete within this timeout but *some* progress must be made, even if it is only a single byte.

```yaml
default: 1m
allowed: [100ms, 1h]
example: --io-timeout=120
```

### Lock Path Option (`--lock-path`)

Path where lock files are stored.

The lock path provides a location for pgBackRest to create lock files to prevent conflicting operations from being run concurrently.

```yaml
default: /tmp/pgbackrest
example: --lock-path=/backup/db/lock
```

### Neutral Umask Option (`--neutral-umask`)

Use a neutral umask.

Sets the umask to 0000 so modes in the repository are created in a sensible way. The default directory mode is 0750 and default file mode is 0640.

To use the executing user's umask instead specify `neutral-umask=n` in the config file or `--no-neutral-umask` on the command line.

```yaml
default: y
example: --no-neutral-umask
```

### Set Process Priority Option (`--priority`)

Set process priority.

Defines how much priority (i.e. niceness) will be given to the process by the kernel scheduler. Positive values decrease priority and negative values increase priority. In most case processes do not have permission to increase their priority.

```yaml
allowed: [-20, 19]
example: --priority=19
```

### Process Maximum Option (`--process-max`)

Max processes to use for compress/transfer.

Each process will perform compression and transfer to make the command run faster, but don't set `process-max` so high that it impacts database performance.

```yaml
default: 1
allowed: [1, 999]
example: --process-max=4
```

### Protocol Timeout Option (`--protocol-timeout`)

Protocol timeout.

Sets the timeout, in seconds, that the local or remote process will wait for a new message to be received on the protocol layer. This prevents processes from waiting indefinitely for a message.

> **NOTE:** The `protocol-timeout` option must be greater than the `db-timeout` option.

```yaml
default: 31m
allowed: [100ms, 7d]
example: --protocol-timeout=630
```

### Keep Alive Option (`--sck-keep-alive`)

Keep-alive enable.

Enables keep-alive messages on socket connections.

```yaml
default: y
example: --no-sck-keep-alive
```

### Stanza Option (`--stanza`)

Defines the stanza.

A stanza is the configuration for a PostgreSQL database cluster that defines where it is located, how it will be backed up, archiving options, etc. Most db servers will only have one PostgreSQL database cluster and therefore one stanza, whereas backup servers will have a stanza for every database cluster that needs to be backed up.

It is tempting to name the stanza after the primary cluster but a better name describes the databases contained in the cluster. Because the stanza name will be used for the primary and all replicas it is more appropriate to choose a name that describes the actual function of the cluster, such as app or dw, rather than the local cluster name, such as main or prod.

```yaml
example: --stanza=main
```

### Keep Alive Count Option (`--tcp-keep-alive-count`)

Keep-alive count.

Specifies the number of TCP keep-alive messages that can be lost before the connection is considered dead.

This option is available on systems that support the `TCP_KEEPCNT` socket option.

```yaml
allowed: [1, 32]
example: --tcp-keep-alive-count=3
```

### Keep Alive Idle Option (`--tcp-keep-alive-idle`)

Keep-alive idle time.

Specifies the amount of time (in seconds) with no network activity after which the operating system should send a TCP keep-alive message.

This option is available on systems that support the `TCP_KEEPIDLE` socket option.

```yaml
allowed: [1, 3600]
example: --tcp-keep-alive-idle=60
```

### Keep Alive Interval Option (`--tcp-keep-alive-interval`)

Keep-alive interval time.

Specifies the amount of time (in seconds) after which a TCP keep-alive message that has not been acknowledged should be retransmitted.

This option is available on systems that support the `TCP_KEEPINTVL` socket option.

```yaml
allowed: [1, 900]
example: --tcp-keep-alive-interval=30
```

### TLSv1.2 cipher suites Option (`--tls-cipher-12`)

Allowed TLSv1.2 cipher suites.

All TLS connections between the pgBackRest client and server are encrypted. By default, connections to objects stores (e.g. S3) are also encrypted.

> **NOTE:** The absolute minimum security level for any transport connection is TLSv1.2.

The accepted cipher suites can be adjusted if need arises. The example is reasonable choice unless you have specific security requirements. If unset (the default), the default of the underlying OpenSSL library applies.

```yaml
example: --tls-cipher-12=HIGH:MEDIUM:+3DES:!aNULL
```

### TLSv1.3 cipher suites Option (`--tls-cipher-13`)

Allowed TLSv1.3 cipher suites.

All TLS connections between the pgBackRest client and server are encrypted. By default, connections to objects stores (e.g. S3) are also encrypted.

> **NOTE:** The absolute minimum security level for any transport connection is TLSv1.2.

The accepted cipher suites can be adjusted if need arises. If unset (the default), the default of the underlying OpenSSL library applies.

```yaml
example: --tls-cipher-13=TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

## Log Options

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

```yaml
default: warn
example: --log-level-console=error
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

```yaml
default: info
example: --log-level-file=debug
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

```yaml
default: off
example: --log-level-stderr=error
```

### Log Path Option (`--log-path`)

Path where log files are stored.

The log path provides a location for pgBackRest to store log files. Note that if `log-level-file=off` then no log path is required.

```yaml
default: /var/log/pgbackrest
example: --log-path=/backup/db/log
```

### Log Subprocesses Option (`--log-subprocess`)

Enable logging in subprocesses.

Enable file logging for any subprocesses created by this process using the log level specified by `log-level-file`.

```yaml
default: n
example: --log-subprocess
```

### Log Timestamp Option (`--log-timestamp`)

Enable timestamp in logging.

Enables the timestamp in console and file logging. This option is disabled in special situations such as generating documentation.

```yaml
default: y
example: --no-log-timestamp
```

## Maintainer Options

### Page Header Check Option (`--page-header-check`)

Check PostgreSQL page headers.

Enabled by default, this option adds page header checks.

Disabling this option should be avoided except when necessary, e.g. if pages are encrypted.

```yaml
default: y
example: --no-page-header-check
```

### Force PostgreSQL Version Option (`--pg-version-force`)

Force PostgreSQL version.

The specified PostgreSQL version will be used instead of the version automatically detected by reading `pg_control` or WAL headers. This is mainly useful for PostgreSQL forks or development versions where those values are different from the release version. The version reported by PostgreSQL via `server_version_num` must match the forced version.

WARNING:

Be cautious when using this option because `pg_control` and WAL headers will still be read with the expected format for the specified version, i.e. the format from the official open-source version of PostgreSQL. If the fork or development version changes the format of the fields that pgBackRest depends on it will lead to unexpected behavior. In general, this option will only work as expected if the fork adds all custom struct members *after* the standard PostgreSQL members.

```yaml
example: --pg-version-force=15
```

## Repository Options

### Set Repository Option (`--repo`)

Set repository.

Set the repository for a command to operate on.

For example, this option may be used to perform a restore from a specific repository, rather than letting pgBackRest choose.

```yaml
allowed: [1, 256]
example: --repo=1
```

### Azure Repository Container Option (`--repo-azure-container`)

Azure repository container.

Azure container used to store the repository.

pgBackRest repositories can be stored in the container root by setting `repo-path=/` but it is usually best to specify a prefix, such as `/repo`, so logs and other Azure-generated content can also be stored in the container.

```yaml
example: --repo1-azure-container=pg-backup
```

### Azure Repository Key Type Option (`--repo-azure-key-type`)

Azure repository key type.

The following types are supported for authorization:

- `shared` - Shared key
- `sas` - Shared access signature
- `auto` - Automatically authorize using Azure managed identities

```yaml
default: shared
example: --repo1-azure-key-type=sas
```

### Azure Repository URI Style Option (`--repo-azure-uri-style`)

Azure URI Style.

The following URI styles are supported:

- `host` - Connect to `account.endpoint` host.
- `path` - Connect to `endpoint` host and prepend account to URIs.

```yaml
default: host
example: --repo1-azure-uri-style=path
```

### Block Incremental Backup Option (`--repo-block`)

Enable block incremental backup.

Block incremental allows for more granular backups by splitting files into blocks that can be backed up independently. This saves space in the repository and can improve delta restore performance because individual blocks can be fetched without reading the entire file from the repository.

> **NOTE:** The `repo-bundle` option must be enabled before `repo-block` can be enabled.

The block size for a file is determined based on the file size and age. Generally, older/larger files will get larger block sizes. If a file is old enough, it will not be backed up using block incremental.

Block incremental is most efficient when enabled for all backup types, including full. This makes the full a bit larger but subsequent differential and incremental backups can make use of the block maps generated by the full backup to save space.

```yaml
default: n
example: --repo1-block
```

### Repository Bundles Option (`--repo-bundle`)

Bundle files in repository.

Bundle (combine) smaller files to reduce the total number of files written to the repository. Writing fewer files is generally more efficient, especially on object stores such as S3. In addition, zero-length files are not stored (except in the manifest), which saves time and space.

```yaml
default: n
example: --repo1-bundle
```

### Repository Bundle Limit Option (`--repo-bundle-limit`)

Limit for file bundles.

Size limit for files that will be included in bundles. Files larger than this size will be stored separately.

Bundled files cannot be reused when a backup is resumed, so this option controls the files that can be resumed, i.e. higher values result in fewer resumable files.

```yaml
default: 2MiB
allowed: [8KiB, 1PiB]
example: --repo1-bundle-limit=10MiB
```

### Repository Bundle Size Option (`--repo-bundle-size`)

Target size for file bundles.

Defines the target size for files that will be added to a single bundle. The uncompressed bundle size may be as large as `repo-bundle-size` + `repo-bundle-limit`, so do not set this option to the maximum size that your file system allows.

In general, it is not a good idea to set this option too high because retries will need to redo the entire bundle.

```yaml
default: 20MiB
allowed: [1MiB, 1PiB]
example: --repo1-bundle-size=10MiB
```

### Repository Cipher Type Option (`--repo-cipher-type`)

Cipher used to encrypt the repository.

The following cipher types are supported:

- `none` - The repository is not encrypted
- `aes-256-cbc` - Advanced Encryption Standard with 256 bit key length

Note that encryption is always performed client-side even if the repository type (e.g. S3) supports encryption.

```yaml
default: none
example: --repo1-cipher-type=aes-256-cbc
```

### GCS Repository Bucket Option (`--repo-gcs-bucket`)

GCS repository bucket.

GCS bucket used to store the repository.

pgBackRest repositories can be stored in the bucket root by setting `repo-path=/` but it is usually best to specify a prefix, such as `/repo`, so logs and other GCS-generated content can also be stored in the bucket.

```yaml
example: --repo1-gcs-bucket=/pg-backup
```

### GCS Repository Endpoint Option (`--repo-gcs-endpoint`)

GCS repository endpoint.

Endpoint used to connect to the storage service. May be updated to use a local GCS server or alternate endpoint.

```yaml
default: storage.googleapis.com
example: --repo1-gcs-endpoint=localhost
```

### GCS Repository Key Type Option (`--repo-gcs-key-type`)

GCS repository key type.

The following types are supported for authorization:

- `auto` - Authorize using the instance service account.
- `service` - Service account from locally stored key.
- `token` - For local testing, e.g. `fakegcs`.

When `repo-gcs-key-type=service` the credentials will be reloaded when the authentication token is renewed.

```yaml
default: service
example: --repo1-gcs-key-type=auto
```

### GCS Repository Project ID Option (`--repo-gcs-user-project`)

GCS project ID.

GCS project ID used to determine request billing.

```yaml
example: --repo1-gcs-user-project=my-project
```

### Repository Hardlink Option (`--repo-hardlink`)

Hardlink files between backups in the repository.

Enable hard-linking of files in differential and incremental backups to their full backups. This gives the appearance that each backup is a full backup at the file-system level. Be careful, though, because modifying files that are hard-linked can affect all the backups in the set.

```yaml
default: n
example: --repo1-hardlink
```

Deprecated Name: hardlink

### Repository Host Option (`--repo-host`)

Repository host when operating remotely.

When backing up and archiving to a locally mounted filesystem this setting is not required.

```yaml
example: --repo1-host=repo1.domain.com
```

Deprecated Name: backup-host

### Repository Host Certificate Authority File Option (`--repo-host-ca-file`)

Repository host certificate authority file.

Use a CA file other than the system default for connecting to the repository host.

```yaml
example: --repo1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### Repository Host Certificate Authority Path Option (`--repo-host-ca-path`)

Repository host certificate authority path.

Use a CA path other than the system default for connecting to the repository host.

```yaml
example: --repo1-host-ca-path=/etc/pki/tls/certs
```

### Repository Host Certificate File Option (`--repo-host-cert-file`)

Repository host certificate file.

Sent to repository host to prove client identity.

```yaml
example: --repo1-host-cert-file=/path/to/client.crt
```

### Repository Host Command Option (`--repo-host-cmd`)

Repository host pgBackRest command.

Required only if the path to the pgBackRest command is different on the local and repository hosts. If not defined, the repository host command will be set the same as the local command.

```yaml
default: [path of executed pgbackrest binary]
example: --repo1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Deprecated Name: backup-cmd

### Repository Host Configuration Option (`--repo-host-config`)

pgBackRest repository host configuration file.

Sets the location of the configuration file on the repository host. This is only required if the repository host configuration file is in a different location than the local configuration file.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --repo1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Deprecated Name: backup-config

### Repository Host Configuration Include Path Option (`--repo-host-config-include-path`)

pgBackRest repository host configuration include path.

Sets the location of the configuration include path on the repository host. This is only required if the repository host configuration include path is in a different location than the local configuration include path.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --repo1-host-config-include-path=/conf/pgbackrest/conf.d
```

### Repository Host Configuration Path Option (`--repo-host-config-path`)

pgBackRest repository host configuration path.

Sets the location of the configuration path on the repository host. This is only required if the repository host configuration path is in a different location than the local configuration path.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --repo1-host-config-path=/conf/pgbackrest
```

### Repository Host Key File Option (`--repo-host-key-file`)

Repository host key file.

Proves client certificate was sent by owner.

```yaml
example: --repo1-host-key-file=/path/to/client.key
```

### Repository Host Port Option (`--repo-host-port`)

Repository host port when `repo-host` is set.

Use this option to specify a non-default port for the repository host protocol.

> **NOTE:** When `repo-host-type=ssh` there is no default for `repo-host-port`. In this case the port will be whatever is configured for the command specified by `cmd-ssh`.

```yaml
default (depending on repo-host-type):
    tls - 8432

allowed: [0, 65535]
example: --repo1-host-port=25
```

Deprecated Name: backup-ssh-port

### Repository Host Protocol Type Option (`--repo-host-type`)

Repository host protocol type.

The following protocol types are supported:

- `ssh` - Secure Shell.
- `tls` - pgBackRest TLS server.

```yaml
default: ssh
example: --repo1-host-type=tls
```

### Repository Host User Option (`--repo-host-user`)

Repository host user when `repo-host` is set.

Defines the user that will be used for operations on the repository host. Preferably this is not the `postgres` user but rather some other user like `pgbackrest`. If PostgreSQL runs on the repository host the `postgres` user can be placed in the `pgbackrest` group so it has read permissions on the repository without being able to damage the contents accidentally.

```yaml
default: pgbackrest
example: --repo1-host-user=repo-user
```

Deprecated Name: backup-user

### Repository Path Option (`--repo-path`)

Path where backups and archive are stored.

The repository is where pgBackRest stores backups and archives WAL segments.

It may be difficult to estimate in advance how much space you'll need. The best thing to do is take some backups then record the size of different types of backups (full/incr/diff) and measure the amount of WAL generated per day. This will give you a general idea of how much space you'll need, though of course requirements will likely change over time as your database evolves.

```yaml
default: /var/lib/pgbackrest
example: --repo1-path=/backup/db/backrest
```

### Archive Retention Option (`--repo-retention-archive`)

Number of backups worth of continuous WAL to retain.

> **NOTE:** WAL segments required to make a backup consistent are always retained until the backup is expired regardless of how this option is configured.

If this value is not set and `repo-retention-full-type` is `count` (default), then the archive to expire will default to the `repo-retention-full` (or `repo-retention-diff`) value corresponding to the `repo-retention-archive-type` if set to `full` (or `diff`). This will ensure that WAL is only expired for backups that are already expired. If `repo-retention-full-type` is `time`, then this value will default to removing archives that are earlier than the oldest full backup retained after satisfying the `repo-retention-full` setting.

This option must be set if `repo-retention-archive-type` is set to `incr`. If disk space is at a premium, then this setting, in conjunction with `repo-retention-archive-type`, can be used to aggressively expire WAL segments. However, doing so negates the ability to perform PITR from the backups with expired WAL and is therefore **not** recommended.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-archive=2
```

Deprecated Name: retention-archive

### Archive Retention Type Option (`--repo-retention-archive-type`)

Backup type for WAL retention.

If set to `full` pgBackRest will keep archive logs for the number of full backups defined by `repo-retention-archive`. If set to `diff` (differential) pgBackRest will keep archive logs for the number of full and differential backups defined by `repo-retention-archive`, meaning if the last backup taken was a full backup, it will be counted as a differential for the purpose of repo-retention. If set to `incr` (incremental) pgBackRest will keep archive logs for the number of full, differential, and incremental backups defined by `repo-retention-archive`. It is recommended that this setting not be changed from the default which will only expire WAL in conjunction with expiring full backups.

```yaml
default: full
example: --repo1-retention-archive-type=diff
```

Deprecated Name: retention-archive-type

### Differential Retention Option (`--repo-retention-diff`)

Number of differential backups to retain.

When a differential backup expires, all incremental backups associated with the differential backup will also expire. When not defined all differential backups will be kept until the full backups they depend on expire.

Note that full backups are included in the count of differential backups for the purpose of expiration. This slightly reduces the number of differential backups that need to be retained in most cases.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-diff=3
```

Deprecated Name: retention-diff

### Full Retention Option (`--repo-retention-full`)

Full backup retention count/time.

When a full backup expires, all differential and incremental backups associated with the full backup will also expire. When the option is not defined a warning will be issued. If indefinite retention is desired then set the option to the max value.

```yaml
allowed: [1, 9999999]
example: --repo1-retention-full=2
```

Deprecated Name: retention-full

### Full Retention Type Option (`--repo-retention-full-type`)

Retention type for full backups.

Determines whether the `repo-retention-full` setting represents a time period (days) or count of full backups to keep.

If set to `time` then full backups older than `repo-retention-full` will be removed from the repository if there is at least one other backup that is equal to or greater than the `repo-retention-full` setting. For example, if `repo-retention-full` is 30 (days) and there are 2 full backups: one 25 days old and one 35 days old, no full backups will be expired because expiring the 35 day old backup would leave only the 25 day old backup, which would violate the 30 day retention policy of having at least one backup 30 days old before an older one can be expired. Archived WAL older than the oldest full backup remaining will be automatically expired unless `repo-retention-archive-type` and `repo-retention-archive` are explicitly set.

If set to `count` then full backups that exceed `repo-retention-full` will be expired. For example, if `repo-retention-full` is `4` and a fifth full backup is completed, then the oldest full backup will be expired to keep the count at 4.

Note that a backup must be successfully completed before it will be considered for retention. For example, if `repo-retention-full-type` is `count` and `repo-retention-full` is `2`, then there must be 3 complete full backups before the oldest will be expired.

```yaml
default: count
example: --repo1-retention-full-type=time
```

### Backup History Retention Option (`--repo-retention-history`)

Days of backup history manifests to retain.

A copy of the backup manifest is stored in the `backup.history` path when a backup completes. By default these files are never expired since they are useful for data mining, e.g. measuring backup and WAL growth over time.

Set `repo-retention-history` to define the number of days of backup history manifests to retain. Unexpired backups are always kept in the backup history. Specify `repo-retention-history=0` to retain the backup history only for unexpired backups.

When a full backup history manifest is expired, all differential and incremental backup history manifests associated with the full backup also expire.

```yaml
allowed: [0, 9999999]
example: --repo1-retention-history=365
```

### S3 Repository Bucket Option (`--repo-s3-bucket`)

S3 repository bucket.

S3 bucket used to store the repository.

pgBackRest repositories can be stored in the bucket root by setting `repo-path=/` but it is usually best to specify a prefix, such as `/repo`, so logs and other AWS generated content can also be stored in the bucket.

```yaml
example: --repo1-s3-bucket=pg-backup
```

### S3 Repository Endpoint Option (`--repo-s3-endpoint`)

S3 repository endpoint.

The AWS endpoint should be valid for the selected region.

For custom/test configurations the `repo-storage-ca-file`, `repo-storage-ca-path`, `repo-storage-host`, `repo-storage-port`, and `repo-storage-verify-tls` options may be useful.

```yaml
example: --repo1-s3-endpoint=s3.amazonaws.com
```

### S3 Repository Key Type Option (`--repo-s3-key-type`)

S3 repository key type.

The following types are supported:

- `shared` - Shared keys
- `auto` - Automatically retrieve temporary credentials
- `web-id` - Automatically retrieve web identity credentials
- `pod-id` - Automatically retrieve EKS pod identity credentials
- `process` - Retrieve credentials by executing a process

```yaml
default: shared
example: --repo1-s3-key-type=auto
```

### S3 Repository KMS Key ID Option (`--repo-s3-kms-key-id`)

S3 repository KMS key.

Enables S3 server-side encryption using the specified AWS key management service key.

```yaml
example: --repo1-s3-kms-key-id=bceb4f13-6939-4be3-910d-df54dee817b7
```

### S3 Authentication Process Command Option (`--repo-s3-process-cmd`)

S3 authentication process command.

Command (and optional arguments) to execute for retrieving temporary S3 credentials. The first list entry is the command and the remaining entries are passed as parameters.

The process must output JSON containing `AccessKeyId`, `SecretAccessKey`, `SessionToken`, and `Expiration` fields. Credentials will be automatically refreshed before the expiration time. See [Process Credential Provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html#feature-process-credentials-output) for format details.

```yaml
example: --repo1-s3-process-cmd=/usr/local/bin/get-credentials --repo1-s3-process-cmd=--role --repo1-s3-process-cmd=my-role
```

### S3 Repository Region Option (`--repo-s3-region`)

S3 repository region.

The AWS region where the bucket was created.

```yaml
example: --repo1-s3-region=us-east-1
```

### S3 Repository Requestor Pays Option (`--repo-s3-requester-pays`)

S3 repository requester pays.

Enables S3 requester pays.

```yaml
default: n
example: --no-repo1-s3-requester-pays
```

### S3 Repository Role Option (`--repo-s3-role`)

S3 repository role.

The AWS role name (not the full ARN) used to retrieve temporary credentials when `repo-s3-key-type=auto`.

```yaml
example: --repo1-s3-role=authrole
```

### S3 Repository Service Option (`--repo-s3-service`)

S3 signing service.

The S3 signing service used in SigV4 authentication. Defaults to `s3` for standard S3 endpoints. Set to `s3-outposts` when using an S3 Outposts endpoint.

```yaml
default: s3
example: --repo1-s3-service=s3-outposts
```

### S3 Repository STS Endpoint Option (`--repo-s3-sts-host`)

S3 repository STS endpoint.

The STS endpoint used to retrieve temporary credentials when `repo-s3-key-type=web-id` is configured. Set to a regional endpoint (e.g. `sts.us-east-1.amazonaws.com`) to use regional STS, which may be required for GovCloud, China regions, or to reduce latency.

```yaml
default: sts.amazonaws.com
example: --repo1-s3-sts-host=sts.us-east-1.amazonaws.com
```

### S3 Repository URI Style Option (`--repo-s3-uri-style`)

S3 URI Style.

The following URI styles are supported:

- `host` - Connect to `bucket.endpoint` host.
- `path` - Connect to `endpoint` host and prepend bucket to URIs.

```yaml
default: host
example: --repo1-s3-uri-style=path
```

### SFTP Repository Host Option (`--repo-sftp-host`)

SFTP repository host.

The SFTP host containing the repository.

```yaml
example: --repo1-sftp-host=sftprepo.domain
```

### SFTP Repository Host Fingerprint Option (`--repo-sftp-host-fingerprint`)

SFTP repository host fingerprint.

SFTP repository host fingerprint generation should match the `repo-sftp-host-key-hash-type`. Generate the fingerprint via `awk '{print $2}' ssh_host_xxx_key.pub | base64 -d | (md5sum or sha1sum) -b`. The ssh host keys are normally found in the `/etc/ssh` directory.

```yaml
example: --repo1-sftp-host-fingerprint=f84e172dfead7aeeeae6c1fdfb5aa8cf
```

### SFTP Host Key Check Type Option (`--repo-sftp-host-key-check-type`)

SFTP host key check type.

The following SFTP host key check types are supported:

- `strict` - pgBackRest will never automatically add host keys to the ~/.ssh/known_hosts file, and refuses to connect to hosts whose host key has changed or is not found in the known hosts files. This option forces the user to manually add all new hosts.
- `accept-new` - pgBackRest will automatically add new host keys to the user's known hosts file, but will not permit connections to hosts with changed host keys.
- `fingerprint` - pgBackRest will check the host key against the fingerprint specified by the `repo-sftp-host-fingerprint` option.
- `none` - no host key checking will be performed.

```yaml
default: strict
example: --repo1-sftp-host-key-check-type=accept-new
```

### SFTP Repository Host Key Hash Type Option (`--repo-sftp-host-key-hash-type`)

SFTP repository host key hash type.

SFTP repository host key hash type. Declares the hash type to be used to compute the digest of the remote system's host key on SSH startup. Newer versions of `libssh2` support `sha256` in addition to md5 and sha1.

```yaml
example: --repo1-sftp-host-key-hash-type=sha256
```

### SFTP Repository Host Port Option (`--repo-sftp-host-port`)

SFTP repository host port.

SFTP repository host port.

```yaml
default: 22
allowed: [1, 65535]
example: --repo1-sftp-host-port=22
```

### SFTP Repository Host User Option (`--repo-sftp-host-user`)

SFTP repository host user.

User on the host used to store the repository.

```yaml
example: --repo1-sftp-host-user=pg-backup
```

### SFTP Known Hosts File Option (`--repo-sftp-known-host`)

SFTP known hosts file.

A known hosts file to search for an SFTP host match during authentication. When unspecified, pgBackRest will default to searching `~/.ssh/known_hosts`, `~/.ssh/known_hosts2`, `/etc/ssh/ssh_known_hosts`, and `/etc/ssh/ssh_known_hosts2`. If configured with one or more file paths, pgBackRest will search those for a match. File paths must be full or leading tilde paths. The `repo-sftp-known-host` option can be passed multiple times to specify more than one known hosts file to search. To utilize known hosts file checking `repo-sftp-host-fingerprint` must not be specified. See also `repo-sftp-host-check-type` option.

```yaml
example: --repo1-sftp-known-host=/home/postgres/.ssh/known_hosts
```

### SFTP Repository Private Key File Option (`--repo-sftp-private-key-file`)

SFTP private key file.

SFTP private key file used for authentication.

```yaml
example: --repo1-sftp-private-key-file=~/.ssh/id_ed25519
```

### SFTP Repository Public Key File Option (`--repo-sftp-public-key-file`)

SFTP public key file.

SFTP public key file used for authentication. Optional if compiled against OpenSSL, required if compiled against a different library.

```yaml
example: --repo1-sftp-public-key-file=~/.ssh/id_ed25519.pub
```

### Repository Storage CA File Option (`--repo-storage-ca-file`)

Repository storage CA file.

Use a CA file other than the system default for storage (e.g. S3, Azure) certificates.

```yaml
example: --repo1-storage-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

Deprecated Names: repo-azure-ca-file, repo-s3-ca-file

### Repository Storage TLS CA Path Option (`--repo-storage-ca-path`)

Repository storage CA path.

Use a CA path other than the system default for storage (e.g. S3, Azure) certificates.

```yaml
example: --repo1-storage-ca-path=/etc/pki/tls/certs
```

Deprecated Names: repo-azure-ca-path, repo-s3-ca-path

### Repository Storage Host Option (`--repo-storage-host`)

Repository storage host.

Connect to a host other than the storage (e.g. S3, Azure) endpoint. This is typically used for testing.

```yaml
example: --repo1-storage-host=127.0.0.1
```

Deprecated Names: repo-azure-host, repo-s3-host

### Repository Storage Port Option (`--repo-storage-port`)

Repository storage port.

Port to use when connecting to the storage (e.g. S3, Azure) endpoint (or host if specified).

```yaml
default: 443
allowed: [1, 65535]
example: --repo1-storage-port=9000
```

Deprecated Names: repo-azure-port, repo-s3-port

### Repository Storage Tag Option (`--repo-storage-tag`)

Repository storage tag(s).

Specify tags that will be added to objects when the repository is an object store (e.g. S3). The option can be repeated to add multiple tags.

There is no provision in pgBackRest to modify these tags so be sure to set them correctly before running `stanza-create` to ensure uniform tags across the entire repository.

```yaml
example: --repo1-storage-tag=key1=value1
```

### Repository Storage Upload Chunk Size Option (`--repo-storage-upload-chunk-size`)

Repository storage upload chunk size.

Object stores such as S3 allow files to be uploaded in chunks when the file is too large to be stored in memory. Even if the file can be stored in memory, it is more memory efficient to limit the amount of memory used for uploads.

A larger chunk size will generally lead to better performance because it will minimize upload requests and allow more files to be uploaded in a single request rather than in chunks. The disadvantage is that memory usage will be higher and because the chunk buffer must be allocated per process, larger `process-max` values will lead to more memory being consumed overall.

Note that valid chunk sizes vary by storage type and by platform. For example, AWS S3 has a minimum chunk size of 5MiB. Terminology for chunk size varies by storage type, so when searching min/max values use "part size" for AWS S3, "chunk size" for GCS, and "block size" for Azure.

If a file is larger than 1GiB (the maximum size PostgreSQL will create by default) then the chunk size will be increased incrementally up to the maximum allowed in order to complete the file upload.

```yaml
default (depending on repo-type):
    azure - 4MiB
    gcs - 4MiB
    s3 - 5MiB

allow range (depending on repo-type):
    azure - [4MiB, 1GiB]
    gcs - [4MiB, 1GiB]
    s3 - [5MiB, 1GiB]

example: --repo1-storage-upload-chunk-size=16MiB
```

### Repository Storage Certificate Verify Option (`--repo-storage-verify-tls`)

Repository storage certificate verify.

This option provides the ability to enable/disable verification of the storage (e.g. S3, Azure) server TLS certificate. Disabling should only be used for testing or other scenarios where a certificate has been self-signed.

```yaml
default: y
example: --no-repo1-storage-verify-tls
```

Deprecated Names: repo-azure-verify-tls, repo-s3-verify-ssl, repo-s3-verify-tls

### Repository Symlink Option (`--repo-symlink`)

Create symlinks within the repository.

Enable creation of the `latest` and tablespace symlinks. These symlinks are most useful when using snapshots to do in-place recovery in the repository, which is an uncommon use case.

While this feature is likely not useful for the vast majority of users it remains on by default for legacy purposes. However, it may be useful to disable symlinks for Posix-like storage that does not support them.

```yaml
default: y
example: --no-repo1-symlink
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

```yaml
default: posix
example: --repo1-type=cifs
```

## Stanza Options

### PostgreSQL Database Option (`--pg-database`)

PostgreSQL database.

The database name used when connecting to PostgreSQL. The default is usually best but some installations may not contain this database.

Note that for legacy reasons the setting of the `PGDATABASE` environment variable will be ignored.

```yaml
default: postgres
example: --pg1-database=backupdb
```

### PostgreSQL Host Option (`--pg-host`)

PostgreSQL host for operating remotely.

Used for backups where the PostgreSQL host is different from the repository host.

```yaml
example: --pg1-host=db.domain.com
```

Deprecated Name: db-host

### PostgreSQL Host Certificate Authority File Option (`--pg-host-ca-file`)

PostgreSQL host certificate authority file.

Use a CA file other than the system default for connecting to the PostgreSQL host.

```yaml
example: --pg1-host-ca-file=/etc/pki/tls/certs/ca-bundle.crt
```

### PostgreSQL Host Certificate Authority Path Option (`--pg-host-ca-path`)

PostgreSQL host certificate authority path.

Use a CA path other than the system default for connecting to the PostgreSQL host.

```yaml
example: --pg1-host-ca-path=/etc/pki/tls/certs
```

### PostgreSQL Host Certificate File Option (`--pg-host-cert-file`)

PostgreSQL host certificate file.

Sent to PostgreSQL host to prove client identity.

```yaml
example: --pg1-host-cert-file=/path/to/client.crt
```

### PostgreSQL Host Command Option (`--pg-host-cmd`)

PostgreSQL host pgBackRest command.

Required only if the path to the pgBackRest command is different on the local and PostgreSQL hosts. If not defined, the PostgreSQL host command will be set the same as the local command.

```yaml
default: [path of executed pgbackrest binary]
example: --pg1-host-cmd=/usr/lib/backrest/bin/pgbackrest
```

Deprecated Name: db-cmd

### PostgreSQL Host Configuration Option (`--pg-host-config`)

pgBackRest database host configuration file.

Sets the location of the configuration file on the PostgreSQL host. This is only required if the PostgreSQL host configuration file is in a different location than the local configuration file.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_FILE
example: --pg1-host-config=/conf/pgbackrest/pgbackrest.conf
```

Deprecated Name: db-config

### PostgreSQL Host Configuration Include Path Option (`--pg-host-config-include-path`)

pgBackRest database host configuration include path.

Sets the location of the configuration include path on the PostgreSQL host. This is only required if the PostgreSQL host configuration include path is in a different location than the local configuration include path.

```yaml
default: CFGOPTDEF_CONFIG_PATH "/" PROJECT_CONFIG_INCLUDE_PATH
example: --pg1-host-config-include-path=/conf/pgbackrest/conf.d
```

### PostgreSQL Host Configuration Path Option (`--pg-host-config-path`)

pgBackRest database host configuration path.

Sets the location of the configuration path on the PostgreSQL host. This is only required if the PostgreSQL host configuration path is in a different location than the local configuration path.

```yaml
default: CFGOPTDEF_CONFIG_PATH
example: --pg1-host-config-path=/conf/pgbackrest
```

### PostgreSQL Host Key File Option (`--pg-host-key-file`)

PostgreSQL host key file.

Proves client certificate was sent by owner.

```yaml
example: --pg1-host-key-file=/path/to/client.key
```

### PostgreSQL Host Port Option (`--pg-host-port`)

PostgreSQL host port when `pg-host` is set.

Use this option to specify a non-default port for the PostgreSQL host protocol.

> **NOTE:** When `pg-host-type=ssh` there is no default for `pg-host-port`. In this case the port will be whatever is configured for the command specified by `cmd-ssh`.

```yaml
default (depending on pg-host-type):
    tls - 8432

allowed: [0, 65535]
example: --pg1-host-port=25
```

Deprecated Name: db-ssh-port

### PostgreSQL Host Protocol Type Option (`--pg-host-type`)

PostgreSQL host protocol type.

The following protocol types are supported:

- `ssh` - Secure Shell.
- `tls` - pgBackRest TLS server.

```yaml
default: ssh
example: --pg1-host-type=tls
```

### PostgreSQL Host User Option (`--pg-host-user`)

PostgreSQL host logon user when `pg-host` is set.

This user will also own the remote pgBackRest process and will initiate connections to PostgreSQL. For this to work correctly the user should be the PostgreSQL database cluster owner which is generally `postgres`, the default.

```yaml
default: postgres
example: --pg1-host-user=db_owner
```

Deprecated Name: db-user

### PostgreSQL Path Option (`--pg-path`)

PostgreSQL data directory.

This should be the same as the `data_directory` reported by PostgreSQL. Even though this value can be read from various places, it is prudent to set it in case those resources are not available during a restore or offline backup scenario.

The `pg-path` option is tested against the value reported by PostgreSQL on every online backup so it should always be current.

```yaml
example: --pg1-path=/data/db
```

Deprecated Name: db-path

### PostgreSQL Port Option (`--pg-port`)

PostgreSQL port.

Port that PostgreSQL is running on. This usually does not need to be specified as most PostgreSQL clusters run on the default port.

```yaml
default: 5432
allowed: [0, 65535]
example: --pg1-port=6543
```

Deprecated Name: db-port

### PostgreSQL Socket Path Option (`--pg-socket-path`)

PostgreSQL unix socket path.

The unix socket directory that was specified when PostgreSQL was started. pgBackRest will automatically look in the standard location for your OS so there is usually no need to specify this setting unless the socket directory was explicitly modified with the `unix_socket_directories` setting in `postgresql.conf`.

```yaml
example: --pg1-socket-path=/var/run/postgresql
```

Deprecated Name: db-socket-path

### PostgreSQL Database User Option (`--pg-user`)

PostgreSQL database user.

The database user name used when connecting to PostgreSQL. If not specified pgBackRest will connect with the local OS user or `PGUSER`.

```yaml
example: --pg1-user=backupuser
```
