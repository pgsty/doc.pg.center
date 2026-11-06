---
title: "gpbackup"
description: "创建供 `gprestore` 工具使用的 Apache Cloudberry 备份。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpbackup.md"
---

## 概要 {#synopsis}

```
gpbackup --dbname <database_name>
   [--backup-dir <directory>]
   [--compression-level <level>]
   [--compression-type <type>]
   [--copy-queue-size <int>
   [--data-only]
   [--debug]
   [--exclude-schema <schema_name> [--exclude-schema <schema_name> ...]]
   [--exclude-table <schema.table> [--exclude-table <schema.table> ...]]
   [--exclude-schema-file <file_name>]
   [--exclude-table-file <file_name>]
   [--include-schema <schema_name> [--include-schema <schema_name> ...]]
   [--include-table <schema.table> [--include-table <schema.table> ...]]
   [--include-schema-file <file_name>]
   [--include-table-file <file_name>]
   [--incremental [--from-timestamp <backup-timestamp>]]
   [--jobs <int>]
   [--leaf-partition-data]
   [--metadata-only]
   [--no-compression]
   [--plugin-config <config_file_location>]
   [--quiet]
   [--single-data-file]
   [--verbose]
   [--version]
   [--with-stats]
   [--without-globals]

gpbackup --help
```

## 说明 {#description}

`gpbackup` 工具将数据库内容备份为一组元数据文件和数据文件，之后可使用 `gprestore` 恢复数据库。备份数据库时，可以指定表级和模式级筛选选项，备份特定表。例如，可以组合模式级和表级选项，备份某个模式中除一个表以外的所有表。

默认情况下，`gpbackup` 备份指定数据库中的对象及 Apache Cloudberry 全局系统对象。使用 `--without-globals` 可省略全局对象。`gprestore` 默认不恢复全局对象；使用 `--with-globals` 可恢复它们。

对于物化视图，仅备份其定义，不备份数据。

默认情况下，`gpbackup` 将备份的对象元数据文件和 DDL 文件存储在 Apache Cloudberry Coordinator 数据目录中。Apache Cloudberry Segment 使用 `COPY ... ON SEGMENT` 命令，将待备份表的数据存储为压缩 CSV 数据文件，位于各 Segment 的数据目录中。

可以添加 `--backup-dir` 选项，将 Apache Cloudberry Coordinator 和 Segment 主机上的所有备份文件复制到绝对路径下，以供后续使用。还提供了其他选项，可筛选备份集以包含或排除特定表。

可以使用 `--incremental` 选项创建增量备份。当 AO 表或表分区中发生更改的数据总量相对于未更改数据较小时，增量备份效率较高。

使用默认 `--jobs` 选项（1 个作业）时，每次 `gpbackup` 操作在 Apache Cloudberry Coordinator 主机上使用单个事务。`COPY ... ON SEGMENT` 命令在各 Segment 主机上并行执行备份任务。备份过程会在每个待备份表上获取 `ACCESS SHARE` 锁。表加锁期间，数据库应处于静默状态。

备份操作完成后，`gpbackup` 返回状态码。

`gpexpand` 初始化新 Segment 时，不能运行 `gpbackup` 工具。扩容前创建的备份，在集群扩容完成后无法用 `gprestore` 恢复。

每个备份由格式为 `YYYYMMDDHHMMSS` 的时间戳标识，粒度为一秒。该时间戳也用于备份目录和备份锁文件。因此，不能在同一秒内启动多个 `gpbackup` 操作。如果同一秒内又启动另一次备份（例如，在脚本循环中运行 `gpbackup`，或并发运行多个 `gpbackup` 进程），后启动的备份会失败，并显示类似以下的错误：

```
[CRITICAL]:-A backup with timestamp 20260502005451 is already in progress. Wait 1 second and try the backup again.
```

为避免此错误，两次 `gpbackup` 操作之间至少等待一秒（例如在脚本命令之间添加 `sleep 1`），或在单次 `gpbackup` 操作中重复使用 `--include-schema`/`--include-table` 选项，或使用 `--include-schema-file`/`--include-table-file`，备份多个模式或表。

`gpbackup` 可以在备份操作完成后发送状态邮件通知。发送时机和收件人在配置文件中指定。

**注意**：此工具通过系统之间的安全 shell（SSH）连接执行任务。在大型 Apache Cloudberry 部署、云部署，或每台主机包含大量 Segment 的部署中，此工具可能超过主机对未认证连接设置的最大阈值。可以考虑更新 SSH 的 `MaxStartups` 和 `MaxSessions` 配置参数以提高此阈值。有关 SSH 配置选项的更多信息，请参阅 Linux 发行版的 SSH 文档。

## 选项 {#options}

**--dbname database_name：** 必需。指定要备份的数据库。

**--backup-dir directory：** 可选。将所有必需的备份文件（元数据文件和数据文件）复制到指定目录。directory 必须为绝对路径，不能是相对路径。如果未提供此选项，元数据文件将在 Apache Cloudberry Coordinator 主机的 $MASTER_DATA_DIRECTORY/backups/YYYYMMDD/YYYYMMDDhhmmss/ 目录中创建。Segment 主机会在 `<seg_dir>/backups/YYYYMMDD/YYYYMMDDhhmmss/` 目录中创建 CSV 数据文件。指定自定义备份目录时，文件会复制到该备份目录下采用这些路径的子目录中。

此选项不能与 `--plugin-config` 选项组合使用。

**--compression-level level：** 可选。指定压缩数据文件时使用的压缩级别（1 到 9）。默认为 1。注意，`gpbackup` 默认使用压缩。

**--compression-type type：** 可选。指定压缩数据文件时使用的压缩类型（`gzip` 或 `zstd`）。默认为 `gzip`。

**注意：** 要使用 `zstd` 压缩类型，必须将 [Zstandard](http://facebook.github.io/zstd/) 安装在 gpadmin 用户可访问的 `$PATH` 中。

**--copy-queue-size int：** 可选。指定使用 `--single-data-file` 选项备份时，`gpbackup` 应加入队列的 `COPY` 命令数量。此选项通过减少初始化 `COPY` 命令所耗费的时间来优化备份性能。如果未将此选项设为 2 或更大，`gpbackup` 每次只将 1 条 `COPY` 命令加入队列。

**注意：** 此选项必须与 `--single-data-file` 选项一起使用，不能与 `--jobs` 选项一起使用。**--data-only：** 可选。仅将表数据备份到 CSV 文件，不备份重建表及其他数据库对象所需的元数据文件。

**--debug：** 可选。在操作期间显示详细调试消息。

**--exclude-schema schema_name：** 可选。指定要从备份中排除的数据库模式。可以多次指定此选项以排除多个模式。此选项不能与 `--include-schema`、`--include-schema-file` 或 `--include-table` 等表筛选选项组合使用。

**--exclude-schema-file file_name：** 可选。指定一个文本文件，其中列出要从备份中排除的模式。文件每行必须定义一个模式，文件末尾不能有多余行。如果模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。此选项不能与 `--include-schema`、`--include-schema-file` 或 `--include-table` 等表筛选选项组合使用。

**--exclude-table schema.table：** 可选。指定要从备份中排除的表，必须采用 `<schema-name>.<table-name>` 格式。如果表名或模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。可以多次指定此选项。此选项不能与 `--exclude-schema`、`--exclude-schema-file` 或 `--include-table` 等其他表筛选选项组合使用。

如果指定叶分区名，`gpbackup` 会忽略这些分区名，不会排除该叶分区。

**--exclude-table-file file_name：** 可选。指定一个文本文件，其中列出要从备份中排除的表。文件每行必须以 `<schema-name>.<table-name>` 格式定义一个表，文件末尾不能有多余行。如果表名或模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。此选项不能与 `--exclude-schema`、`--exclude-schema-file` 或 `--include-table` 等其他表筛选选项组合使用。

如果在 `--exclude-table-file` 使用的文件中指定叶分区名，`gpbackup` 会忽略这些分区名，不会排除这些叶分区。

**--include-schema schema_name：** 可选。指定要纳入备份的数据库模式。可以多次指定此选项以包含多个模式。如果指定此选项，后续 `--include-schema` 选项未包含的模式都将从备份集中省略。此选项不能与 `--exclude-schema`、`--exclude-schema-file`、`--exclude-schema-file`、`--include-table` 或 `--include-table-file` 选项组合使用。

**--include-schema-file file_name：** 可选。指定一个文本文件，其中列出要备份的模式。文件每行必须定义一个模式，文件末尾不能有多余行。如果模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。

**--include-table schema.table：** 可选。指定要纳入备份的表，必须采用 `<schema-name>.<table-name>` 格式。

可以多次指定此选项。此选项不能与 `--include-schema` 等模式筛选选项，或 `--exclude-table-file` 等其他表筛选选项组合使用。

也可以指定序列、视图或物化视图的限定名称。

指定此选项后，工具不会自动备份依赖对象，必须显式指定所需的依赖对象。例如，备份视图或物化视图时，还必须备份其使用的表。备份使用序列的表时，还必须备份该序列。

也可以用表的叶分区名代替表名，配合 `--leaf-partition-data` 选项，使备份仅包含特定叶分区。备份叶分区时，会同时备份该叶分区的数据和分区表的元数据。

**--include-table-file file_name：** 可选。指定一个文本文件，其中列出要纳入备份的表。文件每行必须以 `<schema-name>.<table-name>` 格式定义一个表，文件末尾不能有多余行。

未在此文件中列出的表都会从备份集中省略。此选项不能与 `--include-schema` 等模式筛选选项，或 `--exclude-table-file` 等其他表筛选选项组合使用。

也可以指定序列、视图或物化视图的限定名称。

指定此选项后，工具不会自动备份依赖对象，必须显式指定所需的依赖对象。例如，备份视图或物化视图时，还必须指定其使用的表。指定使用序列的表时，还必须指定该序列。

也可以用表的叶分区名代替表名，配合 `--leaf-partition-data` 选项，使备份仅包含特定叶分区。备份叶分区时，会同时备份该叶分区的数据和分区表的元数据。

**--incremental：** 指定此选项，将增量备份添加到增量备份集中。备份集由一个完整备份及一个或多个增量备份组成。集合中的备份必须使用一致的备份选项创建，以确保该备份集可用于恢复操作。

默认情况下，`gpbackup` 尝试查找使用一致选项的最新现有备份。如果该备份是完整备份，工具会创建备份集；如果是增量备份，则将本次备份添加到现有备份集中。此次增量备份会成为备份集中最新的备份。可以指定 `--from-timestamp` 覆盖默认行为。

**--from-timestamp backup-timestamp**：可选。指定某个备份的时间戳。指定备份的选项必须与正在创建的增量备份一致。如果指定的是完整备份，工具会创建备份集；如果指定的是增量备份，则将此次增量备份添加到现有备份集中。

必须同时指定 `--leaf-partition-data`。此选项不能与 `--data-only` 或 `--metadata-only` 组合使用。

如果无法将备份添加到现有增量备份集，或无法使用该备份创建备份集，工具不会创建备份，并会返回错误。

**--jobs int：** 可选。指定备份表时并行运行的作业数。默认情况下，`gpbackup` 使用 1 个作业（数据库连接）。增大此值可以提高数据备份速度。运行多个作业时，每个作业在独立事务中备份表。**重要：** 如果指定的值大于 1，在工具获取待备份表的锁时，数据库应处于静默状态。如果无法获取某个待备份表的锁，工具会退出。

此选项不能与 `--metadata-only`、`--single-data-file` 或 `--plugin-config` 选项组合使用。

**注意**：使用 `--jobs` 标志时，某种潜在死锁情况可能在日志中生成 `WARNING` 消息。在备份元数据阶段，主工作进程获取备份集中所有表的 Access Share 锁。在备份数据阶段，会根据 `--jobs` 标志的值创建额外工作进程，尝试在其备份的表上获取额外的 Access Share 锁。如果在元数据备份与数据备份之间，第三方进程（执行 `TRUNCATE`、`DROP`、`ALTER` 等操作）尝试访问相同表并获取 Exclusive 锁，工作线程会识别潜在死锁，将该表的备份任务交给主工作进程（它已持有该表的 Access Share 锁）。此时会记录类似以下的警告：`[WARNING]:-Worker 5 could not acquire AccessShareLock for table public.foo.`

**--leaf-partition-data**：可选。对于分区表，为每个叶分区创建一个数据文件，而不是按默认行为为整个表创建一个数据文件。使用此选项后，还可以通过 `--include-table`、`--include-table-file`、`--exclude-table` 和 `--exclude-table-file` 选项指定要纳入备份或从备份中排除的单个叶分区。**--metadata-only：** 可选。仅创建重建数据库对象所需的元数据文件（DDL），不备份实际表数据。

**--no-compression：** 可选。不压缩表数据 CSV 文件。

**--plugin-config config-file_location：** 指定 `gpbackup` 插件配置文件的位置。该文件是 YAML 格式的文本文件，包含 `gpbackup` 在备份操作中使用的插件应用程序的配置信息。

备份数据库时如果指定了 `--plugin-config` 选项，从该备份恢复数据库时也必须指定此选项，并提供对应插件应用程序的配置信息。

此选项不能与 `--backup-dir` 选项组合使用。

**--quiet**：可选。不输出除警告和错误外的所有日志消息。

**--single-data-file**：可选。为每台 Segment 主机上备份的所有表创建单个数据文件。默认情况下，每次 `gpbackup` 为 Segment 上备份的每个表创建一个压缩 CSV 文件。注意：如果使用 `--single-data-file` 选项将表备份合并为每个 Segment 一个文件，则不能将 `gprestore` 的 `--jobs` 选项设为大于 1 的值来执行并行恢复。

**--verbose**：可选。打印详细日志消息。

**--version**：可选。打印版本号并退出。

**--with-stats**：可选。在备份集中包含查询计划统计信息。

**--without-globals**：可选。备份时省略 Apache Cloudberry 全局系统对象。

**--help：** 显示在线帮助。

## 返回码 {#return-codes}

`gpbackup` 完成后会返回以下代码之一。

-   0 -- 备份顺利完成。
-   1 -- 备份完成，但有非致命错误。更多信息请查看日志文件。
-   2 -- 备份因致命错误而失败。更多信息请查看日志文件。

## 模式名和表名 {#schema-and-table-names}

使用 `--include-table` 或 `--include-table-file` 选项筛选备份时，模式名或表名可以包含大写字符、空格（ ）、换行符（\n）、制表符（\t）或以下特殊字符：

`~ # $ % ^ & * ( ) _ - + [ ] { } > < \ | ; : / ? ! , " '`

例如：

```
public.foo"bar
public.foo bar
public.foo\nbar
```

**注意**：`--include-table` 和 `--include-table-file` 选项不支持包含句点（`.`）或已求值换行符的模式名或表名。

表名包含特殊字符时，必须用单引号括起名称：

```
gpbackup --dbname test --include-table 'my#1schema'.'my_$42_Table'
```

表名包含单引号时，请转义每个引号，或将表名括在双引号中。例如：

```

gpbackup --dbname test --include-table public.'foo\'bar'
gpbackup --dbname test --include-table public."foo'bar"
```

使用 `--include-table-file` 选项时，文本文件中的表名不需要单引号。例如，文本文件的内容可以类似于：

```
my#1schema.my_$42_Table
my#1schema.my_$590_Table
```

## 示例 {#examples}

备份“demo”数据库中的所有模式和表，包括 Apache Cloudberry 全局系统对象统计信息：

```
$ gpbackup --dbname demo
```

备份“demo”数据库中除“twitter”模式以外的所有模式和表：

```
$ gpbackup --dbname demo --exclude-schema twitter
```

仅备份“demo”数据库中的“twitter”模式：

```
$ gpbackup --dbname demo --include-schema twitter
```

备份“demo”数据库中的所有模式和表，包括 Apache Cloudberry 全局系统对象及查询统计信息，并将所有备份文件复制到 /home/gpadmin/backup 目录：

```
$ gpbackup --dbname demo --with-stats --backup-dir /home/gpadmin/backup
```

以下示例组合使用 `--include-schema` 和 `--exclude-table`，备份某个模式中除一个表以外的内容。

```
$ gpbackup --dbname demo --include-schema mydata --exclude-table mydata.addresses
```

不能将 `--exclude-schema` 选项与 `--include-table` 等表筛选选项一起使用。

## 另请参阅 {#see-also}

[gprestore](/cloudberry/reference/sys-utilities/gprestore/)
