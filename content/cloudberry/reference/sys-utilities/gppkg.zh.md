---
title: "gppkg"
description: "Cloudberry 包管理器在整个集群中安装、升级、迁移和删除 `.gppkg` 格式的 Apache Cloudberry 扩展（如 PL/Java、PL/R、PostGIS 和 MADlib）及其依赖。"
weight: 210
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gppkg.md"
---

## 概要 {#synopsis}

```shell
gppkg <command> [<command_options> ...] 

gppkg <commmand> --h | --help

gppkg --version

gppkg -v | --verbose
```

## 说明 {#description}

Cloudberry 包管理器 `gppkg` 工具在集群的所有主机上安装 Apache Cloudberry 扩展及其依赖。在系统扩容和 Segment 恢复时，它还会自动在新主机上安装扩展。

`gppkg` 工具安装软件包时不要求 Apache Cloudberry 正在运行。

通过 Cloudberry 包管理器提供的数据库扩展和软件包示例：

- PL/Java
- PL/R
- PostGIS
- MADlib

## 命令 {#commands}

**`help`**

显示此命令的帮助。

**`install <package_name> [<command_options>]`**

在集群中安装或升级指定软件包。包括所有安装前／后步骤，以及安装所有依赖。

**`migrate --source <source_path> --destination <destination_path> [--pkglibs <pkglibs_path>] [<command_options>]`**

将所有软件包从 Apache Cloudberry 的一个次要版本迁移到另一个次要版本。选项 `--source <source_path>` 指定源 `$GPHOME` 的路径，选项 `--destination <destination_path>` 指定目标 `$GPHOME` 的路径。此外，选项 `--pkglibs <pkglibs_path>` 允许指定一个位置，用于存放适用于目标 Cloudberry 版本的新版软件包；`gppkg` 会自动升级这些软件包。

**`query [<package_name_string>] [<query_option>] [<command_options>]`**

显示集群中已安装扩展的信息。`<package_name_string>` 是指定包名的字符串。如果为空字符串，将匹配所有软件包。如果是单个词，将匹配名称中包含该词的所有软件包。使用 `–-exact` 可指定精确的包名。

|query_option|返回结果|
|-------------|-------|
|`--exact`|提供的 `<package_name_string>` 必须与包名完全匹配|
|`--detail`|提供软件包的详细信息|
|`--verify`|验证软件包安装|
|`--local`|不在集群级别查询|

**`remove <package_name> [<command_options>]`**

从集群中卸载指定软件包。

**`sync [<command_options>]`**

协调集群的软件包状态，使其与主节点的状态一致。安装／卸载失败或仅完成一部分后运行此选项，可以确保整个集群的软件包安装状态一致。

## 全局选项 {#global-options}

**`--cluster_info <cluster_info>`**

Apache Cloudberry 未运行时使用此选项。输入文件 `<cluster_info>` 包含数据库集群信息。可以运行以下命令生成该文件：

```shell
psql postgres -Xc 'select dbid, content, role, preferred_role, mode, status, hostname, address, port, datadir from gp_segment_configuration order by content, preferred_role desc;' | head -n-2 | tail -n+3 | tr -d " " > cluster_info
```

**`-a | --accept`**

不提示用户确认。

**`-d | --dryrun`**

模拟执行命令，不进行任何修改。

**`-f | --force`**

跳过所有要求检查，并覆盖现有文件。

**`-h | --help`**

显示在线帮助。

**`-V | --version`**

显示此工具的版本。

**`-v | --verbose`**

将日志级别设为 verbose。

## 示例 {#examples}

安装 Apache Cloudberry PL/Java 扩展：

```shell
gppkg install ./pljava-2.0.7-gp7-rhel8_x86_64.gppkg
```

查询集群中已安装的所有软件包：

```shell
gppkg query

Detecting network topology[=========================================] [OK] 
Detect result 
 3 unique hosts found 
DataSciencePython3.9 - 1.1.0 
```
