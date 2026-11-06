---
title: "pg_checksums"
description: "启用、禁用或检查 Apache Cloudberry 集群中的数据校验和。"
weight: 320
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/pg-checksums.md"
---

## 概要 {#synopsis}

```shell
pg_checksums [<option> ...] [-D <datadir> | --pgdata=<datadir>]

pg_checksums -? | --help

pg_checksums -V | --version
```

## 说明 {#description}

`pg_checksums` 是标准 PostgreSQL 工具，可用于检查、启用或禁用 Apache Cloudberry 集群中的数据校验和。运行 `pg_checksums` 前，必须正常关闭服务器。验证校验和时，如果没有校验和错误，Apache Cloudberry 返回退出状态零；如果检测到至少一个校验和失败，则返回非零值。启用或禁用校验和时，如果操作失败，Cloudberry 返回非零退出状态。

验证校验和时，Apache Cloudberry 扫描集群中的每个文件。启用校验和时，会就地重写集群中的每个文件。禁用校验和仅更新 `pg_control` 文件。

## 选项 {#options}

可使用以下命令行选项：

**`-D datadir`**<br />
**`--pgdata=datadir`**

指定存储数据库集群的目录。

**`-c`**<br />
**`--check`**

检查校验和。未指定其他选项时，这是默认模式。

**`-d`**<br />
**`--disable`**

禁用校验和。

**`-e`**<br />
**`--enable`**

启用校验和。

**`-f fnode`**<br />
**`--filenode=fnode`**

仅验证 filenode 为 fnode 的关系中的校验和。

**`-N`**<br />
**`--no-sync`**

默认情况下，`pg_checksums` 等待所有文件安全写入磁盘。使用此选项后，`pg_checksums` 无需等待即可返回，速度更快，但随后发生的操作系统崩溃可能使更新后的数据目录损坏。与 `--check` 一起指定时，此选项无效。

> **注意**
> `-N/--nosync` 选项虽适用于测试，但请勿在生产环境中使用。

**`-P`**<br />
**`--progress`**

启用进度报告。开启后，会在检查或启用校验和时报告进度。

**`-v`**<br />
**`--verbose`**

指定详细模式，列出所有已检查的文件。

**`-V`**<br />
**`--version`**

打印 `pg_checksums` 版本并退出。

**`-?`**<br />
**`--help`**

显示 `pg_checksums` 命令行参数的帮助并退出。

## 环境变量 {#environment}

**`PGDATA`**

指定存储数据库集群的目录；可以通过 `pg_checksums` 命令的 `-D` 选项覆盖此设置。

**`PG_COLOR`**

指定是否在诊断消息中使用颜色。可选值为 `always`、`auto` 和 `never`。

## 注意事项 {#notes}

为大型集群启用校验和可能需要很长时间。为防止此操作期间丢失数据，不得启动集群，也不得启动其他会写入数据目录的程序。

如果 `pg_checksums` 在启用或禁用校验和时中止或被杀死，集群的数据校验和配置保持不变；可以重新运行 `pg_checksums` 执行同一操作。
