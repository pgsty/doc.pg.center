---
title: "gpssh-exkeys"
description: "在主机之间交换 SSH 公钥。"
weight: 260
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpssh-exkeys.md"
---

## 概要 {#synopsis}

```shell
gpssh-exkeys -f <hostfile_exkeys> | -h <hostname> [-h <hostname> ...]

gpssh-exkeys -e <hostfile_exkeys> -x <hostfile_gpexpand>

gpssh-exkeys -? 

gpssh-exkeys --version
```

## 说明 {#description}

`gpssh-exkeys` 工具在指定的主机名（或主机地址）之间交换 SSH 密钥，使 Cloudberry 主机和网络接口之间可以建立无需提示输入密码的 SSH 连接。此工具既用于为 Apache Cloudberry 系统初次配置免密 SSH 访问，也用于在 Apache Cloudberry 系统扩容时为新增主机配置免密 SSH 访问。

密钥以当前登录用户的身份交换。应在 Coordinator 主机上以 `gpadmin` 用户（指定为 Apache Cloudberry 安装所有者的用户）运行此工具。Apache Cloudberry 管理工具要求在系统的所有主机上创建 `gpadmin` 用户，且这些工具必须能够以该用户身份连接所有主机，而无需提示输入密码。

也可以使用 `gpssh-exkeys` 为其他用户启用免密 SSH，例如 `root`。

`gpssh-exkeys` 工具有以下前提条件：

- 用户必须在 Apache Cloudberry 集群的 Coordinator、Standby Coordinator 及每台 Segment 主机上都拥有账户。
- 用户必须在 Coordinator 主机上安装有 `id_rsa` SSH 密钥对。
- 用户必须能够从 Coordinator 主机通过 SSH 连接到所有其他主机，而无需输入密码。（这称为“1-*n* 免密 SSH”。）

可以使用 `ssh-copy-id` 命令，将用户的公钥添加到每台主机的 `authorized_keys` 文件中，从而启用 1-*n* 免密 SSH。`gpssh-exkeys` 工具启用的是“*n*-*n* 免密 SSH”，允许用户从集群中的任意主机通过 SSH 连接到其他任意主机，而无需输入密码。

要指定参与 SSH 密钥交换的主机，可以使用 `-f` 选项指定包含主机名列表的文件（推荐），也可以在命令行上使用 `-h` 选项逐个指定主机名。至少必须指定一个主机名（`-h`）或一个主机文件（`-f`）。注意，默认情况下，本地主机也参与密钥交换。

要指定添加到现有 Apache Cloudberry 系统中的扩容主机，请使用 `-e` 和 `-x` 选项。`-e` 选项指定一个文件，其中列出系统中已交换 SSH 密钥的现有主机。`-x` 选项指定一个文件，其中列出需要参与 SSH 密钥交换的新主机。

`gpssh-exkeys` 工具按以下步骤交换密钥：

- 将用户的公钥添加到当前主机上该用户自己的 `authorized_keys` 文件中。
- 使用通过 `-h`、`-f`、`-e` 和 `-x` 选项指定的各主机的主机密钥，更新当前用户的 `known_hosts` 文件。
- 使用 `ssh` 连接到各主机，获取用户的 `authorized_keys`、`known_hosts` 和 `id_rsa.pub` 文件。
- 将从各主机获取的 `id_rsa.pub` 文件中的密钥添加到当前用户的 `authorized_keys` 文件中。
- 使用新的主机信息（如有）更新所有主机上的 `authorized_keys`、`known_hosts` 和 `id_rsa.pub` 文件。

## 选项 {#options}

**`-e hostfile_exkeys`**

系统扩容时，指定一个文件的名称和位置，其中包含当前 Cloudberry 系统各主机（Coordinator、Standby Coordinator 和 Segment）已配置的全部主机名和主机地址（接口名），每行一个名称，不得有空行或多余空格。此文件中指定的主机不能再出现在 `-x` 所用的主机文件中。

**`-f hostfile_exkeys`**

指定一个文件的名称和位置，其中包含 Cloudberry 系统各主机（Coordinator、Standby Coordinator 和 Segment）已配置的全部主机名和主机地址（接口名），每行一个名称，不得有空行或多余空格。

**`-h hostname`**

指定参与 SSH 密钥交换的单个主机名（或主机地址）。可多次使用 `-h` 选项来指定多个主机名和主机地址。

**`--version`**

显示此工具的版本。

**`-x hostfile_gpexpand`**

系统扩容时，指定一个文件的名称和位置，其中包含将要添加到 Cloudberry 系统的各新 Segment 主机已配置的全部主机名和主机地址（接口名），每行一个名称，不得有空行或多余空格。此文件中指定的主机不能再出现在 `-e` 所用的主机文件中。

**`-? (help)`**

显示在线帮助。

## 示例 {#examples}

在文件 `hostfile_exkeys` 中列出的所有主机名和地址之间交换 SSH 密钥：

```shell
$ gpssh-exkeys -f hostfile_exkeys
```

在主机 `sdw1`、`sdw2` 和 `sdw3` 之间交换 SSH 密钥：

```shell
$ gpssh-exkeys -h sdw1 -h sdw2 -h sdw3
```

在系统扩容过程中，在现有主机 `sdw1`、`sdw2`、`sdw3` 与新主机 `sdw4`、`sdw5` 之间交换 SSH 密钥：

```shell
$ cat hostfile_exkeys

cdw
cdw-1
cdw-2
scdw
scdw-1
scdw-2
sdw1
sdw1-1
sdw1-2
sdw2
sdw2-1
sdw2-2
sdw3
sdw3-1
sdw3-2
$ cat hostfile_gpexpand
sdw4
sdw4-1
sdw4-2
sdw5
sdw5-1
sdw5-2

$ gpssh-exkeys -e hostfile_exkeys -x hostfile_gpexpand
```

## 另请参阅 {#see-also}

[gpssh](/cloudberry/reference/sys-utilities/gpssh/), [gpsync](/cloudberry/reference/sys-utilities/gpsync/)
