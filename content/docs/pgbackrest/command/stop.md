---
title: "Stop Command (stop)"
linkTitle: "stop"
weight: 180
description: "Reference for pgBackRest `stop` command options and behavior."
icon: fa-solid fa-stop
module: [PGBACKREST]
categories: [Reference]
---

> Source: [pgBackRest Command Docs: stop](https://pgbackrest.org/command.html#command-stop)

Does not allow any new pgBackRest processes to run. By default running processes will be allowed to complete successfully. Use the `--force` option to terminate running processes.

pgBackRest processes will return an error if they are run after the stop command completes. See [Starting and Stopping](/docs/pgbackrest/user-guide/#starting-and-stopping) for more information and examples.

## Command Options

### Force Option (`--force`)

Force all pgBackRest processes to stop.

This option will send TERM signals to all running pgBackRest processes to effect a graceful but immediate shutdown. Note that this will also shutdown processes that were initiated on another system but have remotes running on the current system. For instance, if a backup was started on the backup server then running `stop --force` on the database server will shutdown the backup process on the backup server.

```yaml
default: n
example: --force
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

### Stanza Option (`--stanza`)

Defines the stanza.

A stanza is the configuration for a PostgreSQL database cluster that defines where it is located, how it will be backed up, archiving options, etc. Most db servers will only have one PostgreSQL database cluster and therefore one stanza, whereas backup servers will have a stanza for every database cluster that needs to be backed up.

It is tempting to name the stanza after the primary cluster but a better name describes the databases contained in the cluster. Because the stanza name will be used for the primary and all replicas it is more appropriate to choose a name that describes the actual function of the cluster, such as app or dw, rather than the local cluster name, such as main or prod.

```yaml
example: --stanza=main
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

### Log Timestamp Option (`--log-timestamp`)

Enable timestamp in logging.

Enables the timestamp in console and file logging. This option is disabled in special situations such as generating documentation.

```yaml
default: y
example: --no-log-timestamp
```
