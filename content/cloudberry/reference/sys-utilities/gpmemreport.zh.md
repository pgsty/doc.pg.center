---
title: "gpmemreport"
description: "使用 gpmemreport 将 gpmemwatcher 输出转换为可读报告，并选择报告时间范围。"
weight: 180
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpmemreport.md"
---

解析 [gpmemwatcher](/cloudberry/reference/sys-utilities/gpmemwatcher/) 工具创建的输出，并生成可读格式的输出文件。

## 概要 {#synopsis}

```
gpmemreport [<GZIP_FILE>] [[-s <START>] | [--start= <START>]] [[-e <END>] | [--end= <END>]] 
        
gpmemreport --version

gpmemreport -h | --help 
```

## 说明 {#description}

`gpmemreport` 工具用于解析 [gpmemwatcher](/cloudberry/reference/sys-utilities/gpmemwatcher/) 工具创建的输出文件。

对 `gpmemwatcher` 生成的 `.gz` 文件运行 `gpmemreport` 时，会生成一系列文件。每个文件对应 `gpmemwatcher` 在 60 秒内收集的数据，并已转换为可读格式。

## 选项 {#options}

**`-s | --start start_time`**

指定报告时段的起始时间。时间戳格式必须为 `'%Y-%m-%d %H:%M:%S'`。

**`-e | --end end_time`**

指定报告时段的结束时间。时间戳格式必须为 `'%Y-%m-%d %H:%M:%S'`。

**`--version`**

显示此工具的版本。

**`-h | --help`**

显示在线帮助。

## 示例 {#examples}

**示例 1：提取 `gpmemwatcher` 为 Cloudberry Coordinator 生成的所有文件**

找到 `gpmemwatcher` 的输出 `.gz` 文件，并对其运行 `gpmemreport`：

```shell
$ gpmemreport cdw.ps.out.gz

>>>21:11:19:15:37:18<<<

>>>21:11:19:15:38:18<<<

>>>21:11:19:15:39:18<<<
```

检查当前目录下是否列出了生成的文件：

```shell
$ ls -thrl

-rw-rw-r--. 1 gpadmin gpadmin 1.2K Nov 19 15:50 20211119-153718
-rw-rw-r--. 1 gpadmin gpadmin 1.2K Nov 19 15:50 20211119-153818
-rw-rw-r--. 1 gpadmin gpadmin 1.2K Nov 19 15:50 20211119-153918
```

**示例 2：提取 `gpmemwatcher` 为 Cloudberry Coordinator 生成的、某个时间戳之后的文件**

找到 `gpmemwatcher` 的输出 `.gz` 文件，并对其运行 `gpmemreport`，指定起始时间为 `2021-11-19 15:38:00`：

```shell
$ gpmemreport cdw.ps.out.gz --start='2021-11-19 15:38:00'

>>>21:11:19:15:37:18<<<

>>>21:11:19:15:38:18<<<

>>>21:11:19:15:39:18<<<
```

检查当前目录下是否仅列出了所选时间戳对应的文件：

```shell
$ ls -thrl

-rw-rw-r--. 1 gpadmin gpadmin 1.2K Nov 19 15:50 20211119-153818
-rw-rw-r--. 1 gpadmin gpadmin 1.2K Nov 19 15:50 20211119-153918
```

## 另请参阅 {#see-also}

[gpmemwatcher](/cloudberry/reference/sys-utilities/gpmemwatcher/)
