---
title: "gpssh"
description: "同时提供对多台主机的 SSH 访问。"
weight: 270
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpssh.md"
---

## 概要 {#synopsis}

```shell
gpssh { -f <hostfile_gpssh> | - h <hostname> [-h <hostname> ...] } [-s] [-e]
      [-d <seconds>] [-t <multiplier>] [-v]
      [<bash_command>]

gpssh -? 

gpssh --version
```

## 说明 {#description}

`gpssh` 工具使用 SSH（安全 shell），让你可以同时在多台主机上运行 bash shell 命令。可以在命令行上指定并运行单个命令，也可以省略命令，进入交互式命令行会话。

要指定参与 SSH 会话的主机，可以使用 `-f` 选项指定包含主机名列表的文件，也可以在命令行上使用 `-h` 选项逐个指定主机名。至少必须指定一个主机名（`-h`）或一个主机文件（`-f`）。注意，默认情况下，会话中***不***包含当前主机；要包含本地主机，必须在参与会话的主机列表中显式列出它。

使用 `gpssh` 前，参与 SSH 会话的主机之间必须建立信任关系。如果尚未完成，可使用 `gpssh-exkeys` 工具更新已知主机文件，并在主机之间交换公钥。

如果未在命令行上指定命令，`gpssh` 将进入交互模式。在 `gpssh` 命令提示符（`=>`）下，可以像在普通 bash 终端命令行中一样输入命令，该命令将在参与会话的所有主机上运行。要结束交互式会话，请按键盘上的 `CTRL`+`D`，或输入 `exit` 或 `quit`。

如果未在主机文件中指定用户名，`gpssh` 将以当前登录用户的身份运行命令。可执行 `whoami` 命令确定当前登录用户。默认情况下，`gpssh` 登录远程主机后会进入会话用户的 `$HOME` 目录。为确保命令在所有远程主机上正确运行，应始终输入绝对路径。

如果使用 `gpssh` 时遇到网络超时问题，可使用 `-d` 和 `-t` 选项，或在 `gpssh.conf` 文件中设置参数，控制 `gpssh` 验证初始 `ssh` 连接时使用的时间设置。有关配置文件的信息，请参阅 [gpssh 配置文件](#gpssh-configuration-file)。

## 选项 {#options}

**`bash_command`**

要在参与此次会话的所有主机上运行的 bash shell 命令（可用引号括起）。如果未指定，`gpssh` 将启动交互式会话。

**`-d (delay) seconds`**

可选。指定 `gpssh` 与 `ssh` 开始交互时的等待时间，单位为秒。默认值为 `0.05`。此选项覆盖 `gpssh.conf` 配置文件中指定的 `delaybeforesend` 值。

增大此值可能导致 `gpssh` 启动时等待较长时间。

**`-e (echo)`**

可选。在非交互模式下运行时，回显传给各主机的命令及其输出。

**`-f hostfile_gpssh`**

指定一个文件的名称，其中列出参与此次 SSH 会话的主机。主机文件每行一个主机。

**`-h hostname`**

指定参与此次 SSH 会话的单个主机名。可多次使用 `-h` 选项来指定多个主机名。

**`-s`**

可选。如果指定此选项，`gpssh` 会先加载 `$GPHOME` 环境变量所指定目录中的 `greenplum_path.sh` 文件，再在目标主机上运行命令。

此选项适用于交互模式和单命令模式。

**`-t multiplier`**

可选。一个大于 0（零）的十进制数，作为 `gpssh` 验证 `ssh` 提示符时所用超时值的倍数。默认值为 `1`。此选项覆盖 `gpssh.conf` 配置文件中指定的 `prompt_validation_timeout` 值。

增大此值对 `gpssh` 启动的影响较小。

**`-v (verbose mode)`**

可选。在非交互模式下运行时，除命令输出外，还报告额外消息。

**`--version`**

显示此工具的版本。

**`-? (help)`**

显示在线帮助。

## gpssh 配置文件 {#gpssh-configuration-file}

`gpssh.conf` 文件中的参数用于调整 `gpssh` 验证初始 `ssh` 连接时的时间设置。这些参数影响 `gpssh` 会话通过 `ssh` 运行命令之前的网络连接。文件位置由环境变量 `COORDINATOR_DATA_DIRECTORY` 指定。如果未定义该环境变量，或 `gpssh.conf` 文件不存在，`gpssh` 将使用默认值或通过 `-d` 和 `-t` 选项设置的值。

`gpssh.conf` 是一个文本文件，由 `[gpssh]` 节及其参数组成。一行中的 `#`（井号）表示注释的开始。以下是 `gpssh.conf` 文件示例。

```conf
[gpssh]
delaybeforesend = 0.05
prompt_validation_timeout = 1.0
sync_retries = 5
```

以下是 `gpssh.conf` 的参数。

**`delaybeforesend = seconds`**

指定 `gpssh` 与 `ssh` 开始交互时的等待时间，单位为秒。默认值为 0.05。增大此值可能导致 `gpssh` 启动时等待较长时间。`-d` 选项覆盖此参数。

**`prompt_validation_timeout = multiplier`**

一个大于 0（零）的十进制数，作为 `gpssh` 验证 `ssh` 提示符时所用超时值的倍数。增大此值对 `gpssh` 启动的影响较小。默认值为 `1`。`-t` 选项覆盖此参数。

**`sync_retries = attempts`**

一个非负整数，指定 `gpssh` 尝试连接远程 Apache Cloudberry 主机的最大次数。默认值为 3。如果值为 0，首次连接尝试失败时，`gpssh` 就会返回错误。增加尝试次数也会延长重试间隔。此参数无法通过命令行选项配置。

`-t` 选项也会影响重试间隔。

增大此值可以应对网络性能较差或 Segment 主机性能问题，例如 CPU 或 I/O 负载较重的情况。不过，无法建立连接时，增大此值也会延长返回错误前的等待时间。

## 示例 {#examples}

与文件 `hostfile_gpssh` 中列出的所有主机启动交互式组 SSH 会话：

```shell
$ gpssh -f hostfile_gpssh
```

在 `gpssh` 交互式命令提示符下，在参与此次会话的所有主机上运行 shell 命令。

```shell
=> ls -a /data/primary/*
```

退出交互式会话：

```shell
=> exit
=> quit
```

与主机 `sdw1` 和 `sdw2` 启动非交互式组 SSH 会话，并将名为 `command_file`、包含多条命令的文件传给 `gpssh`：

```shell
$ gpssh -h sdw1 -h sdw2 -v -e < command_file
```

在非交互模式下，在主机 `sdw2` 和 `localhost` 上运行单个命令：

```shell
$ gpssh -h sdw2 -h localhost -v -e 'ls -a /data/primary/*'
$ gpssh -h sdw2 -h localhost -v -e 'echo $GPHOME'
$ gpssh -h sdw2 -h localhost -v -e 'ls -1 | wc -l'
```

## 另请参阅 {#see-also}

[gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/), [gpsync](/cloudberry/reference/sys-utilities/gpsync/)
