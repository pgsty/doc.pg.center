---
title: "gpmemwatcher"
description: "跟踪 Apache Cloudberry 集群中各进程的内存使用情况。"
weight: 190
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpmemwatcher.md"
---

## 概要 {#synopsis}

```shell
gpmemwatcher [-f | --host_file <hostfile>]   
        
gpmemwatcher --stop [-f | --host_file <hostfile>]  

gpmemwatcher --version

gpmemwatcher -h | --help
```

## 说明 {#description}

`gpmemwatcher` 工具是运行在 Apache Cloudberry 集群所有服务器上的守护进程。它每 60 秒收集一次 `ps` 命令的输出，以跟踪各进程的内存使用情况。此进程开销很低，仅占用 4 MB 内存。在 24 小时内约生成 30 MB 数据。

如果 Apache Cloudberry 报告 `Out of memory` 错误，导致 Segment 停机或查询失败，可以使用此工具。通过 `gpmemwatcher` 收集 Apache Cloudberry 集群中一台或多台服务器的内存使用信息，再使用 [gpmemreport](/cloudberry/reference/sys-utilities/gpmemreport/) 分析收集的文件。

## 选项 {#options}

**`-f | --host_file hostfile`**

指定 hostfile 输入文件，其中列出应收集内存使用信息的主机。文件必须包含主机名，以及各主机上都已存在的工作目录。例如：

```shell
cdw:/home/gpadmin/gpmemwatcher_dir/working
sdw1:/home/gpadmin/gpmemwatcher_dir/working
sdw2:/home/gpadmin/gpmemwatcher_dir/working
sdw3:/home/gpadmin/gpmemwatcher_dir/working
sdw4:/home/gpadmin/gpmemwatcher_dir/working
```

**`--stop`**

停止所有 `gpmemwatcher` 进程，在当前目录生成 `.gz` 数据文件，并删除所有主机上的全部工作文件。

**`--version`**

显示此工具的版本。

**`-h | --help`**

显示在线帮助。

## 示例 {#examples}

**示例 1：指定要收集信息的主机列表并启动工具**

创建文件 `/home/gpadmin/hostmap.txt`，包含以下内容：

```shell
cdw:/home/gpadmin/gpmemwatcher_dir/working
sdw1:/home/gpadmin/gpmemwatcher_dir/working
sdw2:/home/gpadmin/gpmemwatcher_dir/working
sdw3:/home/gpadmin/gpmemwatcher_dir/working
sdw4:/home/gpadmin/gpmemwatcher_dir/working
```

确保路径 `/home/gpadmin/gpmemwatcher_dir/working` 在所有主机上都存在。

启动工具：

```shell
$ gpmemwatcher -f /home/gpadmin/hostmap.txt
```

**示例 2：停止工具并将结果转储到 `.gz` 文件**

停止在示例 1 中启动的工具：

```shell
$ gpmemwatcher -f /home/gpadmin/hostmap.txt --stop
```

结果 `.gz` 文件将转储到运行此命令的目录中：

```shell
$ [gpadmin@gpdb-m]$ ls -thrl

-rw-rw-r--. 1 gpadmin gpadmin 2.8K Nov 19 15:17 cdw.ps.out.gz
-rw-rw-r--. 1 gpadmin gpadmin 2.8K Nov 19 15:17 sdw1.ps.out.gz
-rw-rw-r--. 1 gpadmin gpadmin 2.8K Nov 19 15:17 sdw2.ps.out.gz
-rw-rw-r--. 1 gpadmin gpadmin 2.8K Nov 19 15:17 sdw3.ps.out.gz
-rw-rw-r--. 1 gpadmin gpadmin 2.8K Nov 19 15:17 sdw4.ps.out.gz
```

## 另请参阅 {#see-also}

[gpmemreport](/cloudberry/reference/sys-utilities/gpmemreport/)
