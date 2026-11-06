---
title: "gpaddmirrors"
description: "为最初仅配置主 Segment 实例、未启用镜像的 Apache Cloudberry 系统添加镜像 Segment。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpaddmirrors.md"
---

## 概要 {#synopsis}

```shell
gpaddmirrors [-p <port_offset>] [-m <datadir_config_file> [-a]] [-s] 
   [-d <coordinator_data_directory>] [-b <segment_batch_size>] [-B <batch_size>] [-l <logfile_directory>]
   [-v] [--hba-hostnames <boolean>] 

gpaddmirrors -i <mirror_config_file> [-a] [-d <coordinator_data_directory>]
   [-b <segment_batch_size>] [-B <batch_size>] [-l <logfile_directory>] [-v]

gpaddmirrors -o output_sample_mirror_config> [-s] [-m <datadir_config_file>]

gpaddmirrors -? 

gpaddmirrors --version
```

## 说明 {#description}

`gpaddmirrors` 工具为现有的 Apache Cloudberry 系统配置镜像 Segment 实例；该系统最初仅配置了主 Segment 实例。此工具会创建镜像实例，并开始主 Segment 与镜像 Segment 实例之间的在线复制。所有镜像与其主实例同步后，Apache Cloudberry 系统便实现完整的数据冗余。

> **重要** 在线复制过程中，Apache Cloudberry 应处于静默状态，不应运行工作负载或其他查询。

默认情况下，此工具会提示输入用于创建镜像 Segment 数据目录的文件系统位置。如果不希望看到提示，可以使用 `-m` 选项传入一个包含文件系统位置的文件。

镜像位置和端口必须与主 Segment 数据位置和端口不同。

此工具会使用预定义的命名约定，在指定位置为每个镜像 Segment 实例创建唯一的数据目录。为镜像 Segment 实例声明的文件系统位置数量必须与主 Segment 实例数量相同。如果希望在同一位置创建镜像数据目录，可以多次指定相同的目录名；也可以为每个镜像输入不同的数据位置。请输入绝对路径。例如：

```shell
Enter mirror segment data directory location 1 of 2 > /gpdb/mirror
Enter mirror segment data directory location 2 of 2 > /gpdb/mirror
```

或者

```shell
Enter mirror segment data directory location 1 of 2 > /gpdb/m1
Enter mirror segment data directory location 2 of 2 > /gpdb/m2
```

另一种方式是运行 `gpaddmirrors` 工具，并使用 `-i` 选项提供详细配置文件。如果希望将镜像 Segment 放在与主 Segment 完全不同的一组主机上，这种方式很有用。镜像配置文件的格式如下：

```shell
<contentID>|<address>|<port>|<data_dir>
```

其中，`<contentID>` 是 Segment 实例内容 ID，`<address>` 是 Segment 主机的主机名或 IP 地址，`<port>` 是通信端口，`<data_dir>` 是 Segment 实例数据目录。

例如：

```shell
0|sdw1-1|60000|/gpdata/m1/gp0
1|sdw1-1|60001|/gpdata/m2/gp1
```

`gp_segment_configuration` 系统目录表可以帮助你确定当前的主 Segment 配置，从而规划镜像 Segment 配置。例如，运行以下查询：

```sql
=# SELECT dbid, content, address as host_address, port, datadir 
   FROM gp_segment_configuration
   ORDER BY dbid;
```

如果要在备用镜像主机上创建镜像，新的镜像 Segment 主机必须预先安装 Apache Cloudberry 软件，并且配置必须与现有主 Segment 主机完全相同。

必须确保运行 `gpaddmirrors` 的用户（`gpadmin` 用户）具有写入指定数据目录位置的权限。运行 `gpaddmirrors` 前，可以在 Segment 主机上创建这些目录，并将其 `chown` 给适当的用户。

> **注意** 此工具通过系统之间的安全 shell（SSH）连接执行任务。在大型 Apache Cloudberry 部署、云部署，或每台主机包含大量 Segment 的部署中，此工具可能超过主机对未认证连接设置的最大阈值。可以考虑更新 SSH `MaxStartups` 配置参数以提高此阈值。有关 SSH 配置选项的更多信息，请参阅 Linux 发行版的 SSH 文档。

## 选项 {#options}

**`-a (do not prompt)`**

以静默模式运行，不提示输入信息。使用此选项时必须通过 `-m` 或 `-i` 提供配置文件。

**`-b segment_batch_size`**

每台主机并行操作的最大 Segment 数量。有效值为 `1` 到 `128`。如果未指定，此工具会在每台主机上并行恢复最多 64 个 Segment。

**`-B batch_size`**

并行处理的主机数。如果未指定，此工具会并行处理最多 16 台主机。有效值为 `1` 到 `64`。

**`-d coordinator_data_directory`**

Coordinator 数据目录。如果未指定，将使用 `$COORDINATOR_DATA_DIRECTORY` 的值。

**`--hba-hostnames boolean`**

可选。控制此工具更新 `pg_hba.conf` 文件中可连接 Apache Cloudberry 的地址时使用 IP 地址还是主机名。设为 0（默认值）时，此工具使用 IP 地址更新文件；设为 1 时，使用主机名更新文件。为保持一致，应使用初始化 Apache Cloudberry 系统时为 `HBA_HOSTNAMES` 指定的相同值。

**`-i mirror_config_file`**

包含要创建的每个镜像 Segment 一行配置的文件。系统中的每个主 Segment 都必须对应列出一个镜像 Segment 实例。文件格式如下（与 `gp_segment_configuration` 目录表中的属性一致）：

```shell
<contentID>|<address>|<port>|<data_dir>
```

其中，`<contentID>` 是 Segment 实例内容 ID，`<address>` 是 Segment 主机的主机名或 IP 地址，`<port>` 是通信端口，`<data_dir>` 是 Segment 实例数据目录。有关使用主机名或 IP 地址的信息，请参阅[使用主机名或 IP 地址指定主机](#specify-hosts-using-hostnames-or-ip-addresses)。另请参阅[使用具有多个 NIC 的主机系统](#use-host-systems-with-multiple-nics)。

**`-l logfile_directory`**

写入日志文件的目录。默认为 `~/gpAdminLogs`。

**`-m datadir_config_file`**

包含文件系统位置列表的配置文件，镜像数据目录将在这些位置创建。如果未提供，此工具会提示输入位置。文件中的每一行指定一个镜像数据目录位置。例如：

```shell
/gpdata/m1
/gpdata/m2
/gpdata/m3
/gpdata/m4
```

**`-o output_sample_mirror_config`**

如果不确定如何布局 `-i` 选项使用的镜像配置文件，可以使用此选项运行 `gpaddmirrors`，根据主 Segment 配置生成示例镜像配置文件。除非通过 `-m` 在文件中提供镜像 Segment 数据目录位置，否则工具会提示输入这些位置。随后可以编辑此文件，必要时将主机名改为备用镜像主机。

**`-p port_offset`**

可选。此数值用于计算镜像 Segment 使用的数据库端口。默认偏移量为 1000。镜像端口按以下方式分配：

```shell
primary_port + offset = mirror_database_port
```

例如，如果主 Segment 端口为 50001，则其镜像默认使用 51001 数据库端口。

**`-s (spread mirrors)`**

将镜像 Segment 分散到可用主机上。默认情况下，会将一组镜像 Segment 分组到与其主 Segment 集不同的备用主机上。分散模式会将每个镜像放置在 Apache Cloudberry 阵列中的不同主机上。只有阵列中的主机数量足够时才允许分散（主机数大于每台主机上的 Segment 实例数）。

**`-v (verbose)`**

将日志输出级别设为 verbose。

**`--version (show utility version)`**

显示此工具的版本。

**`-? (help)`**

显示在线帮助。

## 使用主机名或 IP 地址指定主机 {#specify-hosts-using-hostnames-or-ip-addresses}

使用 `gpaddmirrors` 的 `-i` 选项指定镜像配置时，可以为 `<address>` 值指定主机名或 IP 地址。

- 如果指定主机名，为安全起见，应在本地完成主机名到 IP 地址的解析。例如，应使用本地 `/etc/hosts` 文件中的条目将主机名映射到 IP 地址。不应通过公共 DNS 服务器等外部服务解析主机名到 IP 地址的映射。更改主机名到不同 IP 地址的映射前，必须停止 Cloudberry 系统。
- 如果指定 IP 地址，初始配置后不应更改该地址。启用 Segment 镜像后，如果 IP 地址与配置值不同，主 Segment 到镜像 Segment 的复制将失败。因此，除非有特定要求使用 IP 地址，否则使用 `-i` 选项启用镜像时应使用主机名。

启用会向 Cloudberry 系统添加主机的镜像配置时，`gpaddmirrors` 会将镜像 Segment 实例信息填入 `gp_segment_configuration` 目录表。Apache Cloudberry 使用 `gp_segment_configuration` 目录表的 address 值查找主机系统，以进行 Coordinator 与 Segment 实例之间、以及 Segment 实例之间的 Cloudberry Interconnect（内部）通信和其他内部通信。

## 使用具有多个 NIC 的主机系统 {#use-host-systems-with-multiple-nics}

如果主机系统配置了多个 NIC，可以初始化 Apache Cloudberry 系统，让每个 NIC 都作为 Cloudberry 主机系统使用。必须确保主机系统配置了足够的资源，以支持要添加到主机上的所有 Segment 实例。此外，如果启用 Segment 镜像，必须确保 Cloudberry 系统配置支持主机系统发生故障时的故障切换。

例如，以下是简单 Cloudberry 系统的 Segment 实例配置。Segment 主机 `gp7c` 配置了两个 NIC：`gp7c-1` 和 `gp7c-2`；Apache Cloudberry 系统使用 `gp7c-1` 承载 Coordinator Segment，使用 `gp7c-2` 承载 Segment 实例。

```sql
select content, role, port, hostname, address from gp_segment_configuration ;

 content | role | port  | hostname | address
---------+------+-------+----------+----------
      -1 | p    |  5432 | gp7c     | gp7c-1
       0 | p    | 40000 | gp7c     | gp7c-2
       0 | m    | 50000 | gp7s     | gp7s
       1 | p    | 40000 | gp7s     | gp7s
       1 | m    | 50000 | gp7c     | gp7c-2
(5 rows) 
```

## 示例 {#examples}

使用与主数据相同的一组主机，为现有 Apache Cloudberry 系统添加镜像。将当前主 Segment 端口号加 100，计算镜像数据库端口：

```shell
$ gpaddmirrors -p 100
```

使用 `-o` 生成示例镜像配置文件，供 `gpaddmirrors -i` 使用：

```shell
$ gpaddmirrors -o /home/gpadmin/sample_mirror_config
```

使用与主数据不同的一组主机，为现有 Apache Cloudberry 系统添加镜像：

```shell
$ gpaddmirrors -i mirror_config_file
```

其中 `mirror_config_file` 内容大致如下：

```shell
0|sdw1-1|52001|/gpdata/m1/gp0
1|sdw1-2|52002|/gpdata/m2/gp1
2|sdw2-1|52001|/gpdata/m1/gp2
3|sdw2-2|52002|/gpdata/m2/gp3
```

## 另请参阅 {#see-also}

[gpinitsystem](/cloudberry/reference/sys-utilities/gpinitsystem/), [gpinitstandby](/cloudberry/reference/sys-utilities/gpinitstandby/), [gpactivatestandby](/cloudberry/reference/sys-utilities/gpactivatestandby/)
