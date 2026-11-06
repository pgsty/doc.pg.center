---
title: "gpsync"
description: "同时在多台主机之间复制文件。"
weight: 310
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpsync.md"
---

## 概要 {#synopsis}

```shell
gpsync { -f <hostfile_gpssh> | -h <hostname> [-h <hostname> ...] } 
      [-a][-J <character>] [-v] [[<user>@]<hostname>:]<file_to_copy> [...]
      [[<user>@]<hostname>:]<copy_to_path> 

gpsync -? 

gpsync --version
```

## 说明 {#description}

`gpsync` 工具通过远程同步，让你用一条命令将一个或多个文件从指定主机复制到其他指定主机。例如，可以同时将 Apache Cloudberry Coordinator 主机上的一个文件复制到所有 Segment 主机。

要指定参与远程同步会话的主机，可以使用 `-f` 选项指定包含主机名列表的文件，也可以在命令行上使用 `-h` 选项逐个指定主机名。至少必须指定一个主机名（`-h`）或一个主机文件（`-f`）。`-J` 选项允许指定一个字符，在 `copy from` 和 `copy to` 目标字符串中代替主机名。如果未指定 `-J`，默认替代字符为等号（`=`）。例如，以下命令将本地主机上的 `.bashrc` 复制到 `hostfile_gpssh` 中列出的所有主机的 `/home/gpadmin` 目录：

```shell
gpsync -f hostfile_gpssh .bashrc =:/home/gpadmin
```

如果未在主机列表中指定用户名，也未在文件路径中使用 user`@` 指定用户名，`gpsync` 将以当前登录用户的身份复制文件。可执行 `whoami` 命令确定当前登录用户。默认情况下，`gpsync` 登录远程主机后会进入会话用户的 `$HOME` 目录。为确保文件复制到远程主机上的正确位置，建议使用绝对路径。

使用 `gpsync` 前，参与远程同步会话的主机之间必须建立信任关系。如果尚未完成，可使用 `gpssh-exkeys` 工具更新已知主机文件，并在主机之间交换公钥。

## 选项 {#options}

**`-f hostfile_gpssh`**

指定一个文件的名称，其中列出参与此次远程同步会话的主机。主机文件每行一个主机，语法如下：

```shell
<hostname>
```

**`-h hostname`**

指定参与此次远程同步会话的单个主机名。可多次使用 `-h` 选项来指定多个主机名。

**`-a`**

以归档模式同步源目录和目标目录。

**`-J character`**

`-J` 选项允许指定一个字符，在 `copy from` 和 `copy to` 目标字符串中代替主机名。如果未指定 `-J`，默认替代字符为等号（`=`）。

**`-v (verbose mode)`**

可选。除远程同步命令的输出外，还报告额外消息。

**`file_to_copy`**

必需。要复制到其他主机（或文件位置）的文件名（或绝对路径）。文件可以位于本地主机上，也可以位于另一台指定的主机上。

**`copy_to_path`**

必需。指定主机上接收所复制文件的路径。如果未使用绝对路径，将相对于会话用户的 `$HOME` 复制文件。还可以使用等号“`=`”（或通过 `-J` 选项指定的其他字符）代替主机名。该字符将依次替换为所提供主机文件（`-f`）中或通过 `-h` 选项指定的各个主机名。

**`-? (help)`**

显示在线帮助。

**`--version`**

显示此工具的版本。

## 示例 {#examples}

将名为 `installer.tar` 的文件复制到 `hostfile_gpssh` 文件中列出的所有主机的 `/` 目录。

```shell
gpsync -f hostfile_gpssh installer.tar =:/
```

将名为 myfuncs.so 的文件复制到主机 `sdw1` 和 `sdw2` 上的指定位置：

```shell
gpsync -h sdw1 -h sdw2 myfuncs.so =:/usr/local/cloudberry/lib
```

## 另请参阅 {#see-also}

[gpssh](/cloudberry/reference/sys-utilities/gpssh/), [gpssh-exkeys](/cloudberry/reference/sys-utilities/gpssh-exkeys/)
