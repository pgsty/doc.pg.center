---
title: "gpcheckcat"
description: "`gpcheckcat` 工具检查 Apache Cloudberry 目录表是否存在不一致。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpcheckcat.md"
---

此工具位于 `$GPHOME/bin/lib`。

## 概要 {#synopsis}

```shell
gpcheckcat [ <options<] [ <dbname>] 

  Options:
     -g <dir>
     -p <port>
     -s <test_name | 'test_name1, test_name2 [, ...]'>  
     -P <password>
     -U <user_name>
     -S {none | only}
     -O
     -R <test_name | 'test_name1, test_name2 [, ...]'>
     -C <catalog_name>
     -B <parallel_processes>
     -v
     -A
     -x "<parameter_name>=<value>"

gpcheckcat  -l 

gpcheckcat -? | --help 
```

## 说明 {#description}

`gpcheckcat` 工具运行多项测试，检查数据库目录是否存在不一致。其中一些测试不能与其他工作负载语句并发运行，否则结果将不可用。运行 `gpcheckcat` 时，应将数据库重启为受限模式；否则，`gpcheckcat` 可能会报告正在进行的数据库操作造成的不一致，而不是实际的不一致数量。如果运行 `gpcheckcat` 时未停止数据库活动，请使用 `-O` 选项运行。

> **注意** 每次运行此工具时，它都会检查并删除指定数据库中孤立的临时数据库模式（没有会话 ID 的临时模式）。此工具会在命令行显示孤立临时模式检查的结果，也会记录这些结果。

目录不一致是 Apache Cloudberry 系统表之间发生的不一致。一般来说，有三种不一致：

- Segment 级别系统表中的不一致。例如，包含表数据的系统表与包含列数据的系统表之间不一致。又如，本应唯一的列在系统表中包含重复项。

- 各 Segment 上同一个系统表之间的不一致。例如，一个系统表在某个 Segment 上缺少一行，而其他 Segment 上有这一行。再如，某行特定列的数据值在不同 Segment 上不同，例如表所有者或表访问权限。
- 目录表与文件系统之间的不一致。例如，数据库目录中存在某个文件，但 pg_class 表中没有对应条目。

## 选项 {#options}

**`-A`**

对 Apache Cloudberry 安装中的所有数据库运行 `gpcheckcat`。

**`-B <parallel_processes>`**

并行运行的进程数。

`gpcheckcat` 工具会尝试确定要使用的并发进程数（批次大小）。此工具假定每个进程至少可以使用 20MB 缓冲区。并行进程的最大数量是 Apache Cloudberry Segment 实例数。开始检查目录时，此工具会显示所使用的并行进程数。

> **注意** 如果返回的错误数量超过缓冲区大小，此工具可能耗尽内存。如果发生内存不足错误，可以使用 `-B` 选项降低批次大小。例如，如果工具显示批次大小为 936 后耗尽内存，可以指定 `-B 468`，以并行运行 468 个进程。

**`-C catalog_table`**

对指定目录表运行交叉一致性、外键和 ACL 测试。

**`-g data_directory`**

生成用于修复目录不一致的 SQL 脚本。脚本放置在 data_directory 中。

**`-l`**

列出 `gpcheckcat` 测试。

**`-O`**

仅运行可以在在线（非受限）模式下运行的 `gpcheckcat` 测试。

**`-p port`**

此选项指定 Apache Cloudberry 使用的端口。

**`-P password`**

连接 Apache Cloudberry 的用户密码。

**`-R test_name | 'test_name1,test_name2 [, ...]'`**

指定要运行的一个或多个测试。多个测试必须以引号括起，并以逗号分隔测试名称。

有些测试只能在 Apache Cloudberry 处于受限模式时运行。

可执行的测试如下：

`acl` - 访问控制权限交叉一致性检查

`aoseg_table` - 检查 Segment 实例上的垂直分区信息（vpinfo）是否与 `pg_attribute` 一致（仅检查数据库中的 AO 列存表）

`duplicate` - 检查重复条目

`foreign_key` - 检查外键

`inconsistent` - 检查 Coordinator 与 Segment 不一致的交叉一致性

`missing_extraneous` - 检查缺失或多余条目的交叉一致性

`owner` - 检查与 Coordinator 数据库不一致的表所有权

`orphaned_toast_tables` - 检查孤立的 TOAST 表。

> **注意** TOAST 表可能因多种原因变成孤立表，此时无法生成修复脚本，必须手动修改目录。一种情况是 *pg_class* 中的 `reltoastrelid` 条目指向错误的 TOAST 表（TOAST 表不匹配）。另一种情况是 *pg_class* 中的 `reltoastrelid` 和 `pg_depend` 条目都缺失（双重孤立 TOAST 表）。如果需要手动修改目录，`gpcheckcat` 会显示可用于更新目录的详细步骤。

`part_integrity` - 检查 *pg_partition* 分支完整性、带 OID 的分区以及分区分布策略

`unique_index_violation` - 检查具有唯一索引约束的列中是否存在重复条目

`dependency` - 检查对不存在对象的依赖（仅限受限模式）

`distribution_policy` - 检查随机分布表上的约束（仅限受限模式）

`namespace` - 检查缺少模式定义的模式（仅限受限模式）

`pgclass` - 检查没有任何对应 *pg_attribute* 条目的 *pg_class* 条目（仅限受限模式）

**``-s `test_name | 'test_name1, test_name2 [, ...]'``**

指定要跳过的一个或多个测试。多个测试必须以引号括起，并以逗号分隔测试名称。

**`-S {none | only}`**

指定此选项，控制对 Apache Cloudberry 安装中所有数据库共享的目录表（如 *pg_database*）的测试。

`none` 值禁用共享目录表测试。`only` 值仅测试共享目录表。

**`-U user_name`**

连接 Apache Cloudberry 的用户。

**`-? | --help`**

显示在线帮助。

**`-v (verbose)`**

显示所执行测试的详细信息。

**`-x "<parameter_name>=<value>"`**

在会话级别设置服务器配置参数，例如 `log_min_messages`。要设置多个配置参数，请多次使用 `-x` 选项。

## 注意事项 {#notes}

此工具会在输出的多个位置以各种非标准格式显示缺少属性的表。输出信息显示后，还会以 `<database>. <schema>. <table>. <segment_id>` 格式显示缺少属性的表汇总列表。

如果 `gpcheckcat` 检测到不一致的 OID（对象 ID）信息，会生成一个或多个包含 SQL 查询的验证文件。可以运行其中的 SQL 查询，查看 OID 不一致的详细信息并调查原因。文件生成在运行 `gpcheckcat` 的目录中。

文件格式如下：

```shell
gpcheckcat.verify.dbname.catalog_table_name.test_name.TIMESTAMP.sql
```

以下是 `gpcheckcat` 检测到数据库 `mydb` 的目录表 *pg_type* 中存在不一致的 OID（对象 ID）信息时创建的验证文件名示例：

```shell
gpcheckcat.verify.mydb.pg_type.missing_extraneous.20150420102715.sql
```

以下是验证文件中的查询示例：

```sql
SELECT *
  FROM (
       SELECT relname, oid FROM pg_class WHERE reltype 
         IN (1305822,1301043,1301069,1301095)
       UNION ALL
       SELECT relname, oid FROM gp_dist_random('pg_class') WHERE reltype 
         IN (1305822,1301043,1301069,1301095)
       ) alltyprelids
  GROUP BY relname, oid ORDER BY count(*) desc ;
```
