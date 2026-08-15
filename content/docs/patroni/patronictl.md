---
title: "patronictl"
weight: 50
icon: fa-solid fa-terminal
description: "Command reference for patronictl configuration, syntax, and subcommands."
module: [PATRONI]
categories: [Reference]
---

> Source: https://patroni.readthedocs.io/en/latest/patronictl.html

<a id="patronictl_version_description"></a>
<a id="patronictl_version_parameters"></a>
<a id="patronictl_version_examples"></a>
<a id="patronictl"></a>
Patroni has a command-line interface named [patronictl](/docs/patroni/patronictl#patronictl), which is used basically to interact with Patroni's REST API and with the DCS. It is intended to make it easier to perform operations in the cluster, and can easily be used by humans or scripts.

<a id="patronictl_configuration"></a>

--------

## Configuration

[patronictl](/docs/patroni/patronictl#patronictl) uses 3 sections of the configuration:

- **ctl**: how to authenticate against the Patroni REST API, and how to validate the server identity. Refer to [ctl settings](/docs/patroni/config/yaml#patronictl_settings) for more details;
- **restapi**: how to authenticate against the Patroni REST API, and how to validate the server identity. Only used if `ctl` configuration is not enough. [patronictl](/docs/patroni/patronictl#patronictl) is mainly interested in `restapi.authentication` section (in case `ctl.authentication` is missing) and `restapi.cafile` setting (in case `ctl.cacert` is missing). Refer to [REST API settings](/docs/patroni/config/yaml#restapi_settings) for more details;
- DCS (e.g. **etcd**): how to contact and authenticate against the DCS used by Patroni.

Those configuration options can come either from environment variables or from a configuration file. Look for the above sections in [Environment Configuration Settings](/docs/patroni/config/env#env) or [YAML Configuration Settings](/docs/patroni/config/yaml#yaml) to understand how you can set the options for them through environment variables or through a configuration file.

If you opt for using environment variables, it's a straight forward approach. Patronictl will read the environment variables and use their values.

If you opt for using a configuration file, you have different ways to inform [patronictl](/docs/patroni/patronictl#patronictl) about the file to be used. By default [patronictl](/docs/patroni/patronictl#patronictl) will attempt to load a configuration file named `patronictl.yaml`, which is expected to be found under either of these paths, according to your system:

- Mac OS X: `~/Library/Application Support/patroni`
- Mac OS X (POSIX): `~/.patroni`
- Unix: `~/.config/patroni`
- Unix (POSIX): `~/.patroni`
- Windows (roaming): `C:\Users\<user>\AppData\Roaming\patroni`
- Windows (not roaming): `C:\Users\<user>\AppData\Local\patroni`

You can override that behavior either by:

- Setting the environment variable `PATRONICTL_CONFIG_FILE` with the path to a custom configuration file;
- Using the `-c` / `--config-file` command-line argument of [patronictl](/docs/patroni/patronictl#patronictl) with the path to a custom configuration file.

> [!NOTE]
> If you are running [patronictl](/docs/patroni/patronictl#patronictl) in the same host as `patroni` daemon is running, you may just use the same configuration file if it contains all the configuration sections required by [patronictl](/docs/patroni/patronictl#patronictl).

<a id="patronictl_usage"></a>

--------

## Usage

[patronictl](/docs/patroni/patronictl#patronictl) exposes several handy operations. This section is intended to describe each of them.

Before jumping into each of the sub-commands of [patronictl](/docs/patroni/patronictl#patronictl), be aware that [patronictl](/docs/patroni/patronictl#patronictl) itself has the following command-line arguments:

`-c` / `--config-file`  
As explained before, used to provide a path to a configuration file for [patronictl](/docs/patroni/patronictl#patronictl).

`-d` / `--dcs-url` / `--dcs`  
Provide a connection string to the DCS used by Patroni.

This argument can be used either to override the DCS and `namespace` settings from the [patronictl](/docs/patroni/patronictl#patronictl) configuration, or to define it if it's missing in the configuration.

The value should be in the format `DCS://HOST:PORT/NAMESPACE`, e.g. `etcd3://localhost:2379/service` to connect to etcd v3 running on `localhost` with Patroni cluster stored under `service` namespace. Any part that is missing in the argument value will be replaced with the value present in the configuration or with its default.

`-k` / `--insecure`  
Flag to bypass validation of REST API server SSL certificate.

This is the synopsis for running a command from the [patronictl](/docs/patroni/patronictl#patronictl):

```text
patronictl [ { -c | --config-file } CONFIG_FILE ]
  [ { -d | --dcs-url | --dcs } DCS_URL ] 
  [ { -k | --insecure } ]
  SUBCOMMAND
```

> [!NOTE]
> This is the syntax for the synopsis:
>
> - Options between square brackets are optional;
> - Options between curly brackets represent a "choose one of set" operation;
> - Options with `[, ... ]` can be specified multiple times;
> - Things written in uppercase represent a literal that should be given a value to.
>
> We will use this same syntax when describing [patronictl](/docs/patroni/patronictl#patronictl) sub-commands in the following sub-sections. Also, when describing sub-commands in the following sub-sections, the commands' synopsis should be seen as a replacement for the `SUBCOMMAND` in the above synopsis.

In the following sub-sections you can find a description of each command implemented by [patronictl](/docs/patroni/patronictl#patronictl). For sake of example, we will use the configuration files present in the GitHub repository of Patroni (files `postgres0.yml`, `postgres1.yml` and `postgres2.yml`).

<a id="patronictl_demote_cluster"></a>

### patronictl demote-cluster

<a id="patronictl_demote_cluster_synopsis"></a>

#### Synopsis

```text
demote-cluster
  [ CLUSTER_NAME ]
  [ --host HOST ]
  [ --port PORT ]
  [ --restore-command RESTORE_COMMAND ]
  [ --primary-slot-name PRIMARY_SLOT_NAME ]
  [ --force ]
```

<a id="patronictl_demote_cluster_description"></a>

#### Description

`patronictl demote-cluster` converts a regular Patroni cluster into a [standby cluster](/docs/patroni/standby_cluster#standby_cluster).

The command patches the dynamic configuration with a `standby_cluster` section built from the provided remote primary connection options, then waits until the leader is running as a standby leader. It prints the current cluster topology before changing the configuration and asks for confirmation unless `--force` is used.

At least one of `--host`, `--port` or `--restore-command` must be specified.

<a id="patronictl_demote_cluster_parameters"></a>

#### Parameters

`CLUSTER_NAME`: Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--host`: Address of the remote node.

`--port`: Port of the remote node.

`--restore-command`: Command to restore WAL records from the remote primary.

`--primary-slot-name`: Name of the replication slot on the remote node to use for replication.

`--force`: Flag to skip confirmation prompts when demoting the cluster.

Useful for scripts.

<a id="patronictl_demote_cluster_examples"></a>

#### Examples

Demote the cluster to a standby cluster that follows a remote primary endpoint:

```bash
$ patronictl -c postgres0.yml demote-cluster batman --host 192.0.2.10 --port 5432 --primary-slot-name batman --force
```

<a id="patronictl_dsn"></a>

### patronictl dsn

<a id="patronictl_dsn_synopsis"></a>

#### Synopsis

```text
dsn
  [ CLUSTER_NAME ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_dsn_description"></a>

#### Description

`patronictl dsn` gets the connection string for one member of the Patroni cluster.

If multiple members match the parameters of this command, one of them will be chosen, prioritizing the primary node.

<a id="patronictl_dsn_parameters"></a>

#### Parameters

`CLUSTER_NAME`: Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`-r` / `--role`  
Choose a member that has the given role.

Role can be one of:

- `leader`: the leader of either a regular Patroni cluster or a standby Patroni cluster; or
- `primary`: the leader of a regular Patroni cluster; or
- `standby-leader`: the leader of a standby Patroni cluster; or
- `replica`: a replica of a Patroni cluster; or
- `standby`: same as `replica`; or
- `any`: any role. Same as omitting this parameter; or

`-m` / `--member`  
Choose a member of the cluster with the given name.

`MEMBER_NAME` is the name of the member.

`--group`  
Choose a member that is part of the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

<a id="patronictl_dsn_examples"></a>

#### Examples

Get DSN of the primary node:

``` bash
$ patronictl -c postgres0.yml dsn batman -r primary
host=127.0.0.1 port=5432
```

Get DSN of the node named `postgresql1`:

``` bash
$ patronictl -c postgres0.yml dsn batman --member postgresql1
host=127.0.0.1 port=5433
```

<a id="patronictl_edit_config"></a>

### patronictl edit-config

<a id="patronictl_edit_config_synopsis"></a>

#### Synopsis

```text
edit-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -q | --quiet } ]
  [ { -s | --set } CONFIG="VALUE" [, ... ] ]
  [ { -p | --pg } PG_CONFIG="PG_VALUE" [, ... ] ]
  [ { --apply | --replace } CONFIG_FILE ]
  [ --force ]
```

<a id="patronictl_edit_config_description"></a>

#### Description

`patronictl edit-config` changes the dynamic configuration of the cluster and updates the DCS with that.

> [!NOTE]
> When invoked through a TTY the command attempts to show a diff of the dynamic configuration through a pager. By default, it attempts to use either `less` or `more`. If you want a different pager, set the `PAGER` environment variable with the desired one.

<a id="patronictl_edit_config_parameters"></a>

#### Parameters

`CLUSTER_NAME`: Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Change dynamic configuration of the given Citus group.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `citus.group` configuration, if it exists.

`CITUS_GROUP` is the ID of the Citus group.

`-q` / `--quiet`  
Flag to skip showing the configuration diff.

`-s` / `--set`  
Set a given dynamic configuration option with a given value.

`CONFIG` is the name of the dynamic configuration path in the YAML tree, with levels joined by `.` .

`VALUE` is the value for `CONFIG`. If it is `null`, then `CONFIG` will be removed from the dynamic configuration.

`-p` / `--pg`  
Set a given dynamic Postgres configuration option with the given value.

It is essentially a shorthand for `--s` / `--set` with `CONFIG` prepended with `postgresql.parameters.`.

`PG_CONFIG` is the name of the Postgres configuration to be set.

`PG_VALUE` is the value for `PG_CONFIG`. If it is `null`, then `PG_CONFIG` will be removed from the dynamic configuration.

`--apply`  
Apply dynamic configuration from the given file.

It is similar to specifying multiple `-s` / `--set` options, one for each configuration from `CONFIG_FILE`.

`CONFIG_FILE` is the path to a file containing the dynamic configuration to be applied, in YAML format. Use `-` if you want to read from `stdin`.

`--replace`  
Replace the dynamic configuration in the DCS with the dynamic configuration specified in the given file.

`CONFIG_FILE` is the path to a file containing the new dynamic configuration to take effect, in YAML format. Use `-` if you want to read from `stdin`.

`--force`  
Flag to skip confirmation prompts when changing the dynamic configuration.

Useful for scripts.

<a id="patronictl_edit_config_examples"></a>

#### Examples

Change `max_connections` Postgres GUC:

``` diff
patronictl -c postgres0.yml edit-config batman --pg max_connections="150" --force
---
+++
@@ -1,6 +1,8 @@
loop_wait: 10
maximum_lag_on_failover: 1048576
postgresql:
+  parameters:
+    max_connections: 150
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5

Configuration changed
```

Change `loop_wait` and `ttl` settings:

``` diff
patronictl -c postgres0.yml edit-config batman --set loop_wait="15" --set ttl="45" --force
---
+++
@@ -1,4 +1,4 @@
-loop_wait: 10
+loop_wait: 15
maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
@@ -6,4 +6,4 @@
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
-ttl: 30
+ttl: 45

Configuration changed
```

Remove `maximum_lag_on_failover` setting from dynamic configuration:

``` diff
patronictl -c postgres0.yml edit-config batman --set maximum_lag_on_failover="null" --force
---
+++
@@ -1,5 +1,4 @@
loop_wait: 10
-maximum_lag_on_failover: 1048576
postgresql:
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5

Configuration changed
```

### patronictl failover

#### Synopsis

```text
failover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

#### Description

`patronictl failover` performs a manual failover in the cluster.

It is designed to be used when the cluster is not healthy, e.g.:

- There is no leader; or
- There is no synchronous standby available in a synchronous cluster.

It also allows to fail over to an asynchronous node if synchronous mode is enabled.

> [!NOTE]
> Nothing prevents you from running `patronictl failover` in a healthy cluster. However, we recommend using `patronictl switchover` in those cases.

> [!WARNING]
> Triggering a failover can cause data loss depending on how up-to-date the promoted replica is in comparison to the primary.

<a id="patronictl_failover"></a>

#### Parameters

`CLUSTER_NAME`: Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Perform a failover in the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`--candidate`  
The node to be promoted on failover.

`CANDIDATE_NAME` is the name of the node to be promoted.

`--force`  
Flag to skip confirmation prompts when performing the failover.

Useful for scripts.

<a id="patronictl_failover_synopsis"></a>

#### Examples

Fail over to node `postgresql2`:

``` bash
$ patronictl -c postgres0.yml failover batman --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  3 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  3 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-12 11:52:27.50978 Successfully failed over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  3 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  3 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

<a id="patronictl_failover_description"></a>

### patronictl flush

<a id="patronictl_failover_parameters"></a>

#### Synopsis

```text
flush
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  { restart | switchover }
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_failover_examples"></a>

#### Description

`patronictl flush` discards scheduled events, if any.

<a id="patronictl_flush"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

`MEMBER_NAME`  
Discard scheduled events for the given Patroni member(s).

Multiple members can be specified. If no members are specified, all of them are considered.

> [!NOTE]
> Only used if discarding scheduled restart events.

`restart`  
Discard scheduled restart events.

`switchover`  
Discard scheduled switchover event.

`--group`  
Discard scheduled events from the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-r` / `--role`  
Discard scheduled events for members that have the given role.

Role can be one of:

- `leader`: the leader of either a regular Patroni cluster or a standby Patroni cluster; or
- `primary`: the leader of a regular Patroni cluster; or
- `standby-leader`: the leader of a standby Patroni cluster; or
- `replica`: a replica of a Patroni cluster; or
- `standby`: same as `replica`; or
- `any`: any role. Same as omitting this parameter.

> [!NOTE]
> Only used if discarding scheduled restart events.

`--force`  
Flag to skip confirmation prompts when performing the flush.

Useful for scripts.

<a id="patronictl_flush_synopsis"></a>

#### Examples

Discard a scheduled switchover event:

``` bash
$ patronictl -c postgres0.yml flush batman switchover --force
Success: scheduled switchover deleted
```

Discard scheduled restart of all standby nodes:

``` bash
$ patronictl -c postgres0.yml flush batman restart -r replica --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql1
Success: flush scheduled restart for member postgresql2
```

Discard scheduled restart of nodes `postgresql0` and `postgresql1`:

``` bash
$ patronictl -c postgres0.yml flush batman postgresql0 postgresql1 restart --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+---------------------------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Scheduled restart         |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     | 2025-03-23T18:00:00-03:00 |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/4000400 |   0 |  0/4000400 |   0 | 2025-03-23T18:00:00-03:00 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+---------------------------+
Success: flush scheduled restart for member postgresql0
Success: flush scheduled restart for member postgresql1
```

<a id="patronictl_flush_description"></a>

### patronictl history

<a id="patronictl_flush_parameters"></a>

#### Synopsis

```text
history
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_flush_examples"></a>

#### Description

`patronictl history` shows a history of failover and switchover events from the cluster, if any.

The following information is included in the output:

`TL`  
Postgres timeline at which the event occurred.

`LSN`  
Postgres LSN at which the event occurred.

`Reason`  
Reason fetched from the Postgres `.history` file.

`Timestamp`  
Time when the event occurred.

`New Leader`  
Patroni member that has been promoted during the event.

<a id="patronictl_history"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Show history of events from the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `citus.group` configuration, if it exists.

`-f` / `--format`  
How to format the list of events in the output.

Format can be one of:

- `pretty`: prints history as a pretty table; or
- `tsv`: prints history as tabular information, with columns delimited by `\t`; or
- `json`: prints history in JSON format; or
- `yaml`: prints history in YAML format.

The default is `pretty`.

`--force`  
Flag to skip confirmation prompts when performing the flush.

Useful for scripts.

<a id="patronictl_history_synopsis"></a>

#### Examples

Show the history of events:

``` bash
$ patronictl -c postgres0.yml history batman
+----+----------+------------------------------+----------------------------------+-------------+
| TL |      LSN | Reason                       | Timestamp                        | New Leader  |
+----+----------+------------------------------+----------------------------------+-------------+
|  1 | 24392648 | no recovery target specified | 2023-09-11T22:11:27.125527+00:00 | postgresql0 |
|  2 | 50331864 | no recovery target specified | 2023-09-12T11:34:03.148097+00:00 | postgresql0 |
|  3 | 83886704 | no recovery target specified | 2023-09-12T11:52:26.948134+00:00 | postgresql2 |
|  4 | 83887280 | no recovery target specified | 2023-09-12T11:53:09.620136+00:00 | postgresql0 |
+----+----------+------------------------------+----------------------------------+-------------+
```

Show the history of events in YAML format:

``` bash
$ patronictl -c postgres0.yml history batman -f yaml
- LSN: 24392648
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 1
  Timestamp: '2023-09-11T22:11:27.125527+00:00'
- LSN: 50331864
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 2
  Timestamp: '2023-09-12T11:34:03.148097+00:00'
- LSN: 83886704
  New Leader: postgresql2
  Reason: no recovery target specified
  TL: 3
  Timestamp: '2023-09-12T11:52:26.948134+00:00'
- LSN: 83887280
  New Leader: postgresql0
  Reason: no recovery target specified
  TL: 4
  Timestamp: '2023-09-12T11:53:09.620136+00:00'
```

<a id="patronictl_history_description"></a>

### patronictl list

<a id="patronictl_history_parameters"></a>

#### Synopsis

```text
list
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -e | --extended } ]
  [ { -t | --timestamp } ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_history_examples"></a>

#### Description

`patronictl list` shows information about Patroni cluster and its members.

The following information is included in the output:

`Cluster`  
Name of the Patroni cluster.

`Member`  
Name of the Patroni member.

`Host`  
Host where the member is located.

`Role`  
Current role of the member.

Can be one among:

- `Leader`: the current leader of a regular Patroni cluster; or
- `Standby Leader`: the current leader of a Patroni standby cluster; or
- `Sync Standby`: a synchronous standby of a Patroni cluster with synchronous mode enabled; or
- `Replica`: a regular standby of a Patroni cluster.

`State`  
Current state of Postgres in the Patroni member.

Some examples among the possible states:

- `running`: if Postgres is currently up and running;
- `streaming`: if a replica and Postgres is currently streaming WALs from the primary node;
- `in archive recovery`: if a replica and Postgres is currently fetching WALs from the archive;
- `stopped`: if Postgres had been shut down;
- `crashed`: if Postgres has crashed.

`TL`  
Current Postgres timeline in the Patroni member.

`Receive LSN`  
The last write-ahead log location received and synced to disk by streaming replication of the member (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Replication lag between the `Receive LSN` position of the member and its upstream in MB.

`Replay LSN`  
The last write-ahead log location replayed during recovery of the member (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Replication lag between the `Replay LSN` position of the member and its upstream in MB.

Besides that, the following information may be included in the output:

`System identifier`  
Postgres system identifier.

> [!NOTE]
> Shown in the table header.
>
> Only shown if output format is `pretty`.

`Group`  
Citus group ID.

> [!NOTE]
> Shown in the table header.
>
> Only shown if a Citus cluster.

`Pending restart`  
`*` indicates that the node needs a restart for some Postgres configuration to take effect. An empty value indicates the node does not require a restart.

> [!NOTE]
> Shown as a member attribute.
>
> Shown if:
>
> - Printing in `pretty` or `tsv` format and with extended output enabled; or
> - If node requires a restart.

`Scheduled restart`  
Timestamp at which a restart has been scheduled for the Postgres instance managed by the Patroni member. An empty value indicates there is no scheduled restart for the member.

> [!NOTE]
> Shown as a member attribute.
>
> Shown if:
>
> - Printing in `pretty` or `tsv` format and with extended output enabled; or
> - If node has a scheduled restart.

`Tags`  
Contains tags set for the Patroni member. An empty value indicates that either no tags have been configured, or that they have been configured with default values.

> [!NOTE]
> Shown as a member attribute.
>
> Shown if:
>
> - Printing in `pretty` or `tsv` format and with extended output enabled; or
> - If node has any custom tags, or any default tags with non-default values.

`Scheduled switchover`  
Timestamp at which a switchover has been scheduled for the Patroni cluster, if any.

> [!NOTE]
> Shown in the table footer.
>
> Only shown if there is a scheduled switchover, and output format is `pretty`.

`Maintenance mode`

> If the cluster monitoring is currently paused.
>
> > [!NOTE]
> > Shown in the table footer.
> >
> > Only shown if the cluster is paused, and output format is `pretty`.

<a id="patronictl_list"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Show information about members from the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-e` / `--extended`  
Show extended information.

Force showing `Pending restart`, `Scheduled restart` and `Tags` attributes, even if their value is empty.

> [!NOTE]
> Only applies to `pretty` and `tsv` output formats.

`-t` / `--timestamp`  
Print timestamp before printing information about the cluster and its members.

`-f` / `--format`  
How to format the list of events in the output.

Format can be one of:

- `pretty`: prints history as a pretty table; or
- `tsv`: prints history as tabular information, with columns delimited by `\t`; or
- `json`: prints history in JSON format; or
- `yaml`: prints history in YAML format.

The default is `pretty`.

`-W`  
Automatically refresh information every 2 seconds.

`-w` / `--watch`  
Automatically refresh information at the specified interval.

`TIME` is the interval between refreshes, in seconds.

<a id="patronictl_list_synopsis"></a>

#### Examples

Show information about the cluster in pretty format:

``` bash
$ patronictl -c postgres0.yml list batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

Show information about the cluster in pretty format with extended columns:

``` bash
$ patronictl -c postgres0.yml list batman -e
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag | Pending restart | Pending restart reason | Scheduled restart | Tags |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |                 |                        |                   |      |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |                 |                        |                   |      |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+-----------------+------------------------+-------------------+------+
```

Show information about the cluster in YAML format, with timestamp of execution:

``` bash
$ patronictl -c postgres0.yml list batman -f yaml -t
2023-09-12 13:30:48
- Cluster: batman
  Host: 127.0.0.1:5432
  Member: postgresql0
  Role: Leader
  State: running
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5433
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql1
  Role: Replica
  State: streaming
  TL: 5
- Cluster: batman
  Host: 127.0.0.1:5434
  Receive LSN: 0/40004E8
  Receive Lag: 0
  Replay LSN: 0/40004E8
  Replay Lag: 0
  Member: postgresql2
  Role: Replica
  State: streaming
  TL: 5
```

<a id="patronictl_list_description"></a>

### patronictl pause

<a id="patronictl_list_parameters"></a>

#### Synopsis

```text
pause
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_list_examples"></a>

#### Description

`patronictl pause` temporarily puts the Patroni cluster in maintenance mode and disables automatic failover.

<a id="patronictl_pause"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Pause the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `citus.group` configuration, if it exists.

`--wait`  
Wait until all Patroni members are paused before returning control to the caller.

<a id="patronictl_pause_synopsis"></a>

#### Examples

Put the cluster in maintenance mode, and wait until all nodes have been paused:

``` bash
$ patronictl -c postgres0.yml pause batman --wait
'pause' request sent, waiting until it is recognized by all nodes
Success: cluster management is paused
```

<a id="patronictl_promote_cluster"></a>

### patronictl promote-cluster

<a id="patronictl_promote_cluster_synopsis"></a>

#### Synopsis

```text
promote-cluster
  [ CLUSTER_NAME ]
  [ --force ]
```

<a id="patronictl_promote_cluster_description"></a>

#### Description

`patronictl promote-cluster` converts a standby cluster into a regular Patroni cluster.

The command removes the `standby_cluster` section from the dynamic configuration and waits until the leader is running as the primary. It prints the current cluster topology before changing the configuration and asks for confirmation unless `--force` is used.

<a id="patronictl_promote_cluster_parameters"></a>

#### Parameters

`CLUSTER_NAME`: Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--force`: Flag to skip confirmation prompts when promoting the cluster.

Useful for scripts.

<a id="patronictl_promote_cluster_examples"></a>

#### Examples

Promote the standby cluster to run as a regular Patroni cluster:

```bash
$ patronictl -c postgres0.yml promote-cluster batman --force
```

<a id="patronictl_pause_description"></a>

### patronictl query

<a id="patronictl_pause_parameters"></a>

#### Synopsis

```text
query
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { { -r | --role } { leader | primary | standby-leader | replica | standby | any } | { -m | --member } MEMBER_NAME } ]
  [ { -d | --dbname } DBNAME ]
  [ { -U | --username } USERNAME ]
  [ --password ]
  [ --format { pretty | tsv | json | yaml } ]
  [ { { -f | --file } FILE_NAME | { -c | --command } SQL_COMMAND } ]
  [ --delimiter ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_pause_examples"></a>

#### Description

`patronictl query` executes a SQL command or script against a member of the Patroni cluster.

<a id="patronictl_query"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Query the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-r` / `--role`  
Choose a member that has the given role.

Role can be one of:

- `leader`: the leader of either a regular Patroni cluster or a standby Patroni cluster; or
- `primary`: the leader of a regular Patroni cluster; or
- `standby-leader`: the leader of a standby Patroni cluster; or
- `replica`: a replica of a Patroni cluster; or
- `standby`: same as `replica`; or
- `any`: any role. Same as omitting this parameter.

`-m` / `--member`  
Choose a member that has the given name.

`MEMBER_NAME` is the name of the member to be picked.

`-d` / `--dbname`  
Database to connect and run the query.

`DBNAME` is the name of the database. If not given, defaults to `USERNAME`.

`-U` / `--username`  
User to connect to the database.

`USERNAME` name of the user. If not given, defaults to the operating system user running `patronictl query`.

`--password`  
Prompt for the password of the connecting user.

As Patroni uses `libpq`, alternatively you can create a `~/.pgpass` file or set the `PGPASSWORD` environment variable.

`--format`  
How to format the output of the query.

Format can be one of:

- `pretty`: prints query output as a pretty table; or
- `tsv`: prints query output as tabular information, with columns delimited by `\t`; or
- `json`: prints query output in JSON format; or
- `yaml`: prints query output in YAML format.

The default is `tsv`.

`-f` / `--file`  
Use a file as source of commands to run queries.

`FILE_NAME` is the path to the source file.

`-c` / `--command`  
Run the given SQL command in the query.

`SQL_COMMAND` is the SQL command to be executed.

`--delimiter`  
The delimiter when printing information in `tsv` format, or `\t` if omitted.

`-W`  
Automatically re-run the query every 2 seconds.

`-w` / `--watch`  
Automatically re-run the query at the specified interval.

`TIME` is the interval between re-runs, in seconds.

<a id="patronictl_query_synopsis"></a>

#### Examples

Run a SQL command as `postgres` user, and ask for its password:

``` bash
$ patronictl -c postgres0.yml query batman -U postgres --password -c "SELECT now()"
Password:
now
2023-09-12 18:10:53.228084+00:00
```

Run a SQL command as `postgres` user, and take password from `libpq` environment variable:

``` bash
$ PGPASSWORD=patroni patronictl -c postgres0.yml query batman -U postgres -c "SELECT now()"
now
2023-09-12 18:11:37.639500+00:00
```

Run a SQL command and print in `pretty` format every 2 seconds:

``` bash
$ patronictl -c postgres0.yml query batman -c "SELECT now()" --format pretty -W
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:16.716235+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:18.732645+00:00 |
+----------------------------------+
+----------------------------------+
| now                              |
+----------------------------------+
| 2023-09-12 18:12:20.750573+00:00 |
+----------------------------------+
```

Run a SQL command on database `test` and print the output in YAML format:

``` bash
$ patronictl -c postgres0.yml query batman -d test -c "SELECT now() AS column_1, 'test' AS column_2" --format yaml
- column_1: 2023-09-12 18:14:22.052060+00:00
  column_2: test
```

Run a SQL command on member `postgresql2`:

``` bash
$ patronictl -c postgres0.yml query batman -m postgresql2 -c "SHOW port"
port
5434
```

Run a SQL command on any of the standbys:

``` bash
$ patronictl -c postgres0.yml query batman -r replica -c "SHOW port"
port
5433
```

<a id="patronictl_query_description"></a>

### patronictl reinit

<a id="patronictl_query_parameters"></a>

#### Synopsis

```text
reinit
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ --wait ]
  [ --force ]
  [ --from-leader ]
```

<a id="patronictl_query_examples"></a>

#### Description

`patronictl reinit` rebuilds a Postgres standby instance managed by a replica member of the Patroni cluster.

<a id="patronictl_reinit"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

`MEMBER_NAME`  
Name of the replica member for which the Postgres instance will be rebuilt.

Multiple replica members can be specified. If no members are specified, the command does nothing.

`--group`  
Rebuild a replica member of the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`--wait`  
Wait until the reinitialization of the Postgres standby node(s) is finished.

`--force`  
Flag to skip confirmation prompts when rebuilding Postgres standby instances.

`--from-leader`  
Flag to get basebackup from leader directly.

Useful for scripts.

<a id="patronictl_reinit_synopsis"></a>

#### Examples

Request a rebuild of all replica members of the Patroni cluster and immediately return control to the caller:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql1 postgresql2 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql1
Success: reinitialize for member postgresql2
```

Request a rebuild of `postgresql2` and wait for it to complete:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --wait --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
Waiting for reinitialize to complete on: postgresql2
Reinitialize is completed on: postgresql2
```

Request a rebuild of `postgresql2` and get basebackup from leader directly:

``` bash
$ patronictl -c postgres0.yml reinit batman postgresql2 --from-leader
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: reinitialize for member postgresql2
```

<a id="patronictl_reinit_description"></a>

### patronictl reload

<a id="patronictl_reinit_parameters"></a>

#### Synopsis

```text
reload
  CLUSTER_NAME
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --force ]
```

<a id="patronictl_reinit_examples"></a>

#### Description

`patronictl reload` requests a reload of local configuration for one or more Patroni members.

It also triggers `pg_ctl reload` on the managed Postgres instance, even if nothing has changed.

<a id="patronictl_reload"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

`MEMBER_NAME`  
Request a reload of local configuration for the given Patroni member(s).

Multiple members can be specified. If no members are specified, all of them are considered.

`--group`  
Request a reload of members of the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-r` / `--role`  
Select members that have the given role.

Role can be one of:

- `leader`: the leader of either a regular Patroni cluster or a standby Patroni cluster; or
- `primary`: the leader of a regular Patroni cluster; or
- `standby-leader`: the leader of a standby Patroni cluster; or
- `replica`: a replica of a Patroni cluster; or
- `standby`: same as `replica`; or
- `any`: any role. Same as omitting this parameter.

`--force`  
Flag to skip confirmation prompts when requesting a reload of the local configuration.

Useful for scripts.

<a id="patronictl_reload_synopsis"></a>

#### Examples

Request a reload of the local configuration of all members of the Patroni cluster:

``` bash
$ patronictl -c postgres0.yml reload batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Reload request received for member postgresql0 and will be processed within 10 seconds
Reload request received for member postgresql1 and will be processed within 10 seconds
Reload request received for member postgresql2 and will be processed within 10 seconds
```

<a id="patronictl_reload_description"></a>

### patronictl remove

<a id="patronictl_reload_parameters"></a>

#### Synopsis

```text
remove
  CLUSTER_NAME
  [ --group CITUS_GROUP ]
  [ { -f | --format } { pretty | tsv | json | yaml } ]
```

<a id="patronictl_reload_examples"></a>

#### Description

`patronictl remove` removes information of the cluster from the DCS.

It is an interactive action.

> [!WARNING]
> This operation will destroy the information of the Patroni cluster from the DCS.

<a id="patronictl_remove"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

`--group`  
Remove information about the Patroni cluster related with the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-f` / `--format`  
How to format the list of members in the output when prompting for confirmation.

Format can be one of:

- `pretty`: prints members as a pretty table; or
- `tsv`: prints members as tabular information, with columns delimited by `\t`; or
- `json`: prints members in JSON format; or
- `yaml`: prints members in YAML format.

The default is `pretty`.

<a id="patronictl_remove_synopsis"></a>

#### Examples

Remove information about Patroni cluster `batman` from the DCS:

``` bash
$ patronictl -c postgres0.yml remove batman
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  5 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  5 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Please confirm the cluster name to remove: batman
You are about to remove all information in DCS for batman, please type: "Yes I am aware": Yes I am aware
This cluster currently is healthy. Please specify the leader name to continue: postgresql0
```

<a id="patronictl_remove_description"></a>

### patronictl restart

<a id="patronictl_remove_parameters"></a>

#### Synopsis

```text
restart
  CLUSTER_NAME
  [ MEMBER_NAME [, ...] ]
  [ --group CITUS_GROUP ]
  [ { -r | --role } { leader | primary | standby-leader | replica | standby | any } ]
  [ --any ]
  [ --pg-version PG_VERSION ]
  [ --pending ]
  [ --timeout TIMEOUT ]
  [ --scheduled TIMESTAMP ]
  [ --force ]
```

<a id="patronictl_remove_examples"></a>

#### Description

`patronictl restart` requests a restart of the Postgres instance managed by a member of the Patroni cluster.

The restart can be performed immediately or scheduled for later.

<a id="patronictl_restart"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

`--group`  
Restart the Patroni cluster related with the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-r` / `--role`  
Choose members that have the given role.

Role can be one of:

- `leader`: the leader of either a regular Patroni cluster or a standby Patroni cluster; or
- `primary`: the leader of a regular Patroni cluster; or
- `standby-leader`: the leader of a standby Patroni cluster; or
- `replica`: a replica of a Patroni cluster; or
- `standby`: same as `replica`; or
- `any`: any role. Same as omitting this parameter.

`--any`  
Restart a single random node among the ones which match the given filters.

`--pg-version`  
Select only members which version of the managed Postgres instance is older than the given version.

`PG_VERSION` is the Postgres version to be compared.

`--pending`  
Select only members which are flagged as `Pending restart`.

`--timeout`: Abort the restart if it takes more than the specified timeout, and fail over to a replica if the issue is on the primary.

`TIMEOUT` is the amount of seconds to wait before aborting the restart.

`--scheduled`  
Schedule a restart to occur at the given timestamp.

`TIMESTAMP` is the timestamp when the restart should occur. Specify it in unambiguous format, preferably with time zone. You can also use the literal `now` for the restart to be executed immediately.

`--force`  
Flag to skip confirmation prompts when requesting the restart operations.

Useful for scripts.

<a id="patronictl_restart_synopsis"></a>

#### Examples

Restart all members of the cluster immediately:

``` bash
$ patronictl -c postgres0.yml restart batman --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql0
Success: restart on member postgresql1
Success: restart on member postgresql2
```

Restart a random member of the cluster immediately:

``` bash
$ patronictl -c postgres0.yml restart batman --any --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart on member postgresql1
```

Schedule a restart to occur at `2023-09-13T18:00-03:00`:

``` bash
$ patronictl -c postgres0.yml restart batman --scheduled 2023-09-13T18:00-03:00 --force
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Success: restart scheduled on member postgresql0
Success: restart scheduled on member postgresql1
Success: restart scheduled on member postgresql2
```

<a id="patronictl_restart_description"></a>

### patronictl resume

<a id="patronictl_restart_parameters"></a>

#### Synopsis

```text
resume
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ --wait ]
```

<a id="patronictl_restart_examples"></a>

#### Description

`patronictl resume` takes the Patroni cluster out of maintenance mode and re-enables automatic failover.

<a id="patronictl_resume"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Resume the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `citus.group` configuration, if it exists.

`--wait`  
Wait until all Patroni members are unpaused before returning control to the caller.

<a id="patronictl_resume_synopsis"></a>

#### Examples

Put the cluster out of maintenance mode:

``` bash
$ patronictl -c postgres0.yml resume batman --wait
'resume' request sent, waiting until it is recognized by all nodes
Success: cluster management is resumed
```

<a id="patronictl_resume_description"></a>

### patronictl show-config

<a id="patronictl_resume_parameters"></a>

#### Synopsis

```text
show-config
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_resume_examples"></a>

#### Description

`patronictl show-config` shows the dynamic configuration of the cluster that is stored in the DCS.

<a id="patronictl_show_config"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Show dynamic configuration of the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `citus.group` configuration, if it exists.

<a id="patronictl_show_config_synopsis"></a>

#### Examples

Show dynamic configuration of cluster `batman`:

``` bash
$ patronictl -c postgres0.yml show-config batman
loop_wait: 10
postgresql:
  parameters:
    max_connections: 250
  pg_hba:
  - host replication replicator 127.0.0.1/32 md5
  - host all all 0.0.0.0/0 md5
  use_pg_rewind: true
retry_timeout: 10
ttl: 30
```

<a id="patronictl_show_config_description"></a>

### patronictl switchover

<a id="patronictl_show_config_parameters"></a>

#### Synopsis

```text
switchover
  [ CLUSTER_NAME ]
  [ --group CITUS_GROUP ]
  [ { --leader | --primary } LEADER_NAME ]
  --candidate CANDIDATE_NAME
  [ --force ]
```

<a id="patronictl_show_config_examples"></a>

#### Description

`patronictl switchover` performs a switchover in the cluster.

It is designed to be used when the cluster is healthy, e.g.:

- There is a leader;
- There are synchronous standbys available in a synchronous cluster.

> [!NOTE]
> If your cluster is unhealthy you might be interested in `patronictl failover` instead.

<a id="patronictl_switchover"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Perform a switchover in the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`--leader` / `--primary`  
Indicate who is the leader to be demoted at switchover time.

`LEADER_NAME` should match the name of the current leader in the cluster.

`--candidate`  
The node to be promoted on switchover, and take the primary role.

`CANDIDATE_NAME` is the name of the node to be promoted.

`--scheduled`  
Schedule a switchover to occur at the given timestamp.

`TIMESTAMP` is the timestamp when the switchover should occur. Specify it in unambiguous format, preferably with time zone. You can also use the literal `now` for the switchover to be executed immediately.

`--force`  
Flag to skip confirmation prompts when performing the switchover.

Useful for scripts.

<a id="patronictl_switchover_synopsis"></a>

#### Examples

Switch over with node `postgresql2`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  6 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  6 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:15:23.07497 Successfully switched over to "postgresql2"
+ Cluster: batman (7277694203142172922) -+---------+----+-------------+---------+------------+---------+
| Member      | Host           | Role    | State   | TL | Receive LSN |     Lag | Replay LSN |     Lag |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
| postgresql0 | 127.0.0.1:5432 | Replica | stopped |    |     unknown | unknown |    unknown | unknown |
| postgresql1 | 127.0.0.1:5433 | Replica | running |  6 |   0/4000188 |       0 |  0/4000188 |       0 |
| postgresql2 | 127.0.0.1:5434 | Leader  | running |  6 |             |         |            |         |
+-------------+----------------+---------+---------+----+-------------+---------+------------+---------+
```

Schedule a switchover between `postgresql0` and `postgresql2` to occur at `2023-09-13T18:00:00-03:00`:

``` bash
$ patronictl -c postgres0.yml switchover batman --leader postgresql0 --candidate postgresql2 --scheduled 2023-09-13T18:00-03:00 --force
Current cluster topology
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
2023-09-13 14:18:11.20661 Switchover scheduled
+ Cluster: batman (7277694203142172922) -+-----------+----+-------------+-----+------------+-----+
| Member      | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0 | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+-------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
Switchover scheduled at: 2023-09-13T18:00:00-03:00
                    from: postgresql0
                    to: postgresql2
```

<a id="patronictl_switchover_description"></a>

### patronictl topology

<a id="patronictl_switchover_parameters"></a>

#### Synopsis

```text
topology
  [ CLUSTER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
  [ { -W | { -w | --watch } TIME } ]
```

<a id="patronictl_switchover_examples"></a>

#### Description

`patronictl topology` shows information about the Patroni cluster and its members with a tree view approach.

The following information is included in the output:

`Cluster`  
Name of the Patroni cluster.

> [!NOTE]
> Shown in the table header.

`System identifier`  
Postgres system identifier.

> [!NOTE]
> Shown in the table header.

`Member`  
Name of the Patroni member.

> [!NOTE]
> Information in this column is shown as a tree view of members in terms of replication connections.

`Host`  
Host where the member is located.

`Role`  
Current role of the member.

Can be one among:

- `Leader`: the current leader of a regular Patroni cluster; or
- `Standby Leader`: the current leader of a Patroni standby cluster; or
- `Sync Standby`: a synchronous standby of a Patroni cluster with synchronous mode enabled; or
- `Replica`: a regular standby of a Patroni cluster.

`State`  
Current state of Postgres in the Patroni member.

Some examples among the possible states:

- `running`: if Postgres is currently up and running;
- `streaming`: if a replica and Postgres is currently streaming WALs from the primary node;
- `in archive recovery`: if a replica and Postgres is currently fetching WALs from the archive;
- `stopped`: if Postgres had been shut down;
- `crashed`: if Postgres has crashed.

`TL`  
Current Postgres timeline in the Patroni member.

`Receive LSN`  
The last write-ahead log location received and synced to disk by streaming replication of the member (`pg_catalog.pg_last_(xlog|wal)_receive_(location|lsn)()`).

`Receive Lag`  
Replication lag between the `Receive LSN` position of the member and its upstream in MB.

`Replay LSN`  
The last write-ahead log location replayed during recovery of the member (`pg_catalog.pg_last_(xlog|wal)_replay_(location|lsn)()`).

`Replay Lag`  
Replication lag between the `Replay LSN` position of the member and its upstream in MB.

Besides that, the following information may be included in the output:

`Group`  
Citus group ID.

> [!NOTE]
> Shown in the table header.
>
> Only shown if a Citus cluster.

`Pending restart`  
`*` indicates the node needs a restart for some Postgres configuration to take effect. An empty value indicates the node does not require a restart.

> [!NOTE]
> Shown as a member attribute.
>
> Shown if node requires a restart.

`Scheduled restart`  
Timestamp at which a restart has been scheduled for the Postgres instance managed by the Patroni member. An empty value indicates there is no scheduled restart for the member.

> [!NOTE]
> Shown as a member attribute.
>
> Shown if node has a scheduled restart.

`Tags`  
Contains tags set for the Patroni member. An empty value indicates that either no tags have been configured, or that they have been configured with default values.

> [!NOTE]
> Shown as a member attribute.
>
> Shown if node has any custom tags, or any default tags with non-default values.

`Scheduled switchover`  
Timestamp at which a switchover has been scheduled for the Patroni cluster, if any.

> [!NOTE]
> Shown in the table footer.
>
> Only shown if there is a scheduled switchover.

`Maintenance mode`

> If the cluster monitoring is currently paused.
>
> > [!NOTE]
> > Shown in the table footer.
> >
> > Only shown if the cluster is paused.

<a id="patronictl_topology"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

If not given, [patronictl](/docs/patroni/patronictl#patronictl) will attempt to fetch that from the `scope` configuration, if it exists.

`--group`  
Show information about members from the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

`-W`  
Automatically refresh information every 2 seconds.

`-w` / `--watch`  
Automatically refresh information at the specified interval.

`TIME` is the interval between refreshes, in seconds.

<a id="patronictl_topology_synopsis"></a>

#### Examples

Show topology of the cluster `batman` -- `postgresql1` and `postgresql2` are replicating from `postgresql0`:

``` bash
$ patronictl -c postgres0.yml topology batman
+ Cluster: batman (7277694203142172922) ---+-----------+----+-------------+-----+------------+-----+
| Member        | Host           | Role    | State     | TL | Receive LSN | Lag | Replay LSN | Lag |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
| postgresql0   | 127.0.0.1:5432 | Leader  | running   |  8 |             |     |            |     |
| + postgresql1 | 127.0.0.1:5433 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
| + postgresql2 | 127.0.0.1:5434 | Replica | streaming |  8 |   0/40004E8 |   0 |  0/40004E8 |   0 |
+---------------+----------------+---------+-----------+----+-------------+-----+------------+-----+
```

<a id="patronictl_topology_description"></a>

### patronictl version

<a id="patronictl_topology_parameters"></a>

#### Synopsis

```text
version
  [ CLUSTER_NAME [, ... ] ]
  [ MEMBER_NAME [, ... ] ]
  [ --group CITUS_GROUP ]
```

<a id="patronictl_topology_examples"></a>

#### Description

`patronictl version` gets the version of [patronictl](/docs/patroni/patronictl#patronictl) application. Besides that it may also include version information about Patroni clusters and their members.

<a id="patronictl_version"></a>

#### Parameters

`CLUSTER_NAME`  
Name of the Patroni cluster.

`MEMBER_NAME`  
Name of the member of the Patroni cluster.

`--group`  
Consider a Patroni cluster with the given Citus group.

`CITUS_GROUP` is the ID of the Citus group.

<a id="patronictl_version_synopsis"></a>

#### Examples

Get version of [patronictl](/docs/patroni/patronictl#patronictl) only:

``` bash
$ patronictl -c postgres0.yml version
patronictl version 4.0.0
```

Get version of [patronictl](/docs/patroni/patronictl#patronictl) and of all members of cluster `batman`:

``` bash
$ patronictl -c postgres0.yml version batman
patronictl version 4.0.0

postgresql0: Patroni 4.0.0 PostgreSQL 16.4
postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```

Get version of [patronictl](/docs/patroni/patronictl#patronictl) and of members `postgresql1` and `postgresql2` of cluster `batman`:

``` bash
$ patronictl -c postgres0.yml version batman postgresql1 postgresql2
patronictl version 4.0.0

postgresql1: Patroni 4.0.0 PostgreSQL 16.4
postgresql2: Patroni 4.0.0 PostgreSQL 16.4
```
