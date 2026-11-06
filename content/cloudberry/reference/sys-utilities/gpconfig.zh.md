---
title: "gpconfig"
description: "设置 Apache Cloudberry 系统中所有 Segment 的服务器配置参数。"
weight: 90
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpconfig.md"
---

## 概要 {#synopsis}

```shell
gpconfig -c <param_name> -v <value> [-m <coordinator_value> | --coordinatoronly]
       | -r <param_name> [--coordinatoronly]
       | -l
       [--skipvalidation] [--verbose] [--debug]

gpconfig -s <param_name> [--file | --file-compare] [--verbose] [--debug]

gpconfig --help
```

## 说明 {#description}

`gpconfig` 工具可用于设置、取消设置或查看 Apache Cloudberry 系统中所有实例（Coordinator、Segment 和镜像）的 `postgresql.conf` 文件中的配置参数。设置参数时，如有需要，还可以为 Coordinator 指定不同的值。例如，`max_connections` 等参数在 Coordinator 上需要采用与 Segment 不同的设置。如果要设置或取消设置全局参数或仅适用于 Coordinator 的参数，请使用 `--coordinatoronly` 选项。

> **注意** 对于 vartype 为 `string` 的配置参数，不得向 `gpconfig -c` 传入用单引号括起的值。

`gpconfig` 只能管理某些参数。例如，不能用它设置 `port` 等必须在每个 Segment 实例上各不相同的参数。使用 `-l`（列表）选项可查看 `gpconfig` 支持的完整配置参数列表。

`gpconfig` 在 Segment 的 `postgresql.conf` 文件中设置配置参数时，新设置总是出现在文件末尾。使用 `gpconfig` 删除配置参数设置时，`gpconfig` 会在所有 Segment 的 `postgresql.conf` 文件中将该参数注释掉，从而恢复系统默认设置。例如，如果先用 `gpconfig` 删除（注释掉）某个参数，之后又将其添加回来（设置新值），就会有两处该参数：一处被注释掉，另一处已启用并插入到 `postgresql.conf` 文件末尾。

设置参数后，必须重启 Apache Cloudberry 系统或重新加载 `postgresql.conf` 文件，更改才会生效。需要重启还是重新加载，取决于具体参数。

要显示整个系统中某个参数当前设置的值，请使用 `-s` 选项。

`gpconfig` 使用以下环境变量连接 Apache Cloudberry Coordinator 实例并获取系统配置信息：

- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

## 选项 {#options}

**`-c | --change param_name`**

通过在 `postgresql.conf` 文件末尾添加新设置来更改配置参数。

**`-v | --value value`**

通过 `-c` 选项指定的配置参数所使用的值。默认情况下，此值应用于所有 Segment、其镜像、Coordinator 和 Standby Coordinator。

此工具向 `postgresql.conf` 文件添加设置时，会正确地为值添加引号。

要将值设为空字符串，请输入空单引号（`''`）。

**`-m | --coordinatorvalue coordinator_value`**

通过 `-c` 选项指定的配置参数在 Coordinator 上使用的值。如果指定，此值仅应用于 Coordinator 和 Standby Coordinator。此选项只能与 `-v` 一起使用。

**`--coordinatoronly`**

指定后，`gpconfig` 仅编辑 Coordinator 的 `postgresql.conf` 文件。

**`-r | --remove param_name`**

通过将 `postgresql.conf` 文件中的条目注释掉来删除配置参数设置。

**`-l | --list`**

列出 `gpconfig` 工具支持的所有配置参数。

**`-s | --show param_name`**

显示 Apache Cloudberry 系统中所有实例（Coordinator 和 Segment）使用的某个配置参数的值。如果各实例的参数值不同，此工具会显示错误消息。使用 `-s` 选项运行 `gpconfig` 时，会直接从数据库读取参数值，而不是从 `postgresql.conf` 文件读取。如果使用 `gpconfig` 为所有 Segment 设置配置参数，随后运行 `gpconfig -s` 验证更改，可能仍会看到原来的（旧）值。必须重新加载配置文件（`gpstop -u`）或重启系统（`gpstop -r`），更改才会生效。

**`--file`**

显示 Apache Cloudberry 系统中所有实例（Coordinator 和 Segment）的 `postgresql.conf` 文件中某个配置参数的值。如果各实例的参数值不同，此工具会显示消息。必须与 `-s` 选项一起指定。

例如，通过 `ALTER ROLE` 命令将某个用户的配置参数 `statement_mem` 设为 64MB，而 `postgresql.conf` 文件中的值为 128MB。运行命令 `gpconfig -s statement_mem --file` 会显示 128MB。该用户运行命令 `gpconfig -s statement_mem` 则显示 64MB。

不能与 `--file-compare` 选项一起使用。

**`--file-compare`**

将某个配置参数当前在 Apache Cloudberry 中的值与各主机（Coordinator 和 Segment）上 `postgresql.conf` 文件中的值进行比较。`postgresql.conf files` 中的值表示 Apache Cloudberry 重启时使用的值。

如果值不同，此工具会显示所有主机上的值。如果所有主机的值相同，则显示汇总报告。

不能与 `--file` 选项一起使用。

**`--skipvalidation`**

覆盖 `gpconfig` 的系统验证检查，允许操作任何服务器配置参数，包括隐藏参数，以及无法通过 `gpconfig` 更改的受限参数。与 `-l` 选项（列表）一起使用时，会显示受限参数列表。

> **小心** 使用此选项设置配置参数时务必极其谨慎。

**`--verbose`**

在执行 `gpconfig` 命令期间显示额外的日志信息。

**`--debug`**

将日志输出设为 debug 级别。

**`-? | -h | --help`**

显示在线帮助。

## 示例 {#examples}

将所有 Segment 的 `max_connections` 设为 100，将 Coordinator 的值设为 10：

```shell
gpconfig -c max_connections -v 100 -m 10
```

以下示例展示了因 bash shell 字符串处理规则而需要采用的语法。

```shell
gpconfig -c search_path -v '"\$user",public'
gpconfig -c dynamic_library_path -v '\$libdir'
```

配置参数会添加到 `postgresql.conf` 文件中。

```shell
search_path='"$user",public'
dynamic_library_path='$libdir'
```

注释掉所有 `default_statistics_target` 配置参数条目，恢复系统默认值：

```shell
gpconfig -r default_statistics_target
```

列出 `gpconfig` 支持的所有配置参数：

```shell
gpconfig -l
```

显示整个系统中某个配置参数的值：

```shell
gpconfig -s max_connections
```

## 另请参阅 {#see-also}

[gpstop](/cloudberry/reference/sys-utilities/gpstop/)
