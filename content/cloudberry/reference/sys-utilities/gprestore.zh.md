---
title: "gprestore"
description: "恢复使用 `gpbackup` 工具创建的 Apache Cloudberry 备份。"
weight: 220
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gprestore.md"
---

默认情况下，`gprestore` 使用 Apache Cloudberry Coordinator 主机数据目录中的备份元数据文件和 DDL 文件，表数据则以 CSV 数据文件形式存储在各 Segment 主机本地。

## 概要 {#synopsis}

```
gprestore --timestamp <YYYYMMDDHHMMSS>
   [--backup-dir <directory>]
   [--copy-queue-size <int>
   [--create-db]
   [--debug]
   [--exclude-schema <schema_name> [--exclude-schema <schema_name> ...]]
   [--exclude-table <schema.table> [--exclude-table <schema.table> ...]]
   [--exclude-table-file <file_name>]
   [--exclude-schema-file <file_name>]
   [--include-schema <schema_name> [--include-schema <schema_name> ...]]
   [--include-table <schema.table> [--include-table <schema.table> ...]]
   [--include-schema-file <file_name>]
   [--include-table-file <file_name>]
   [--truncate-table]
   [--redirect-schema <schema_name>]
   [--resize-cluster]
   [--data-only | --metadata-only]
   [--incremental]
   [--jobs <int>]
   [--on-error-continue]
   [--plugin-config <config_file_location>]
   [--quiet]
   [--redirect-db <database_name>]
   [--verbose]
   [--version]
   [--with-globals]
   [--with-stats]
   [--run-analyze]

gprestore --help
```

## 说明 {#description}

使用 `gprestore` 从备份集恢复时，必须通过 `--timestamp` 选项指定待恢复备份集的确切时间戳值（`YYYYMMDDHHMMSS`）。如果先前指定了自定义 `--backup-dir` 来集中存放备份文件，请在运行 `gprestore` 时指定相同的 `--backup-dir` 选项，以定位这些文件。

如果指定的是增量备份，需要完整的一组备份文件（一个完整备份及所有必需的增量备份）。尝试恢复前，`gprestore` 会确保整个备份集可用。

重要：增量备份集中的所有备份必须位于同一个设备上。例如，整个备份集必须都位于一个 Data Domain 系统上。

从备份集恢复时，`gprestore` 将恢复到与创建备份集时指定的名称相同的数据库。如果目标数据库已存在，且某个待恢复的表也已存在其中，恢复操作会失败。如果集群中不存在目标数据库，请添加 `--create-db` 选项。也可以使用 `--redirect-db` 选项将备份集恢复到另一个数据库。

如果备份集包含分区表中部分叶分区的数据，恢复时会恢复该分区表及这些叶分区的数据。例如，使用 `gpbackup` 的 `--include-table-file` 选项创建备份，文本文件中列出某个分区表的部分叶分区。恢复此备份时，会创建分区表，并且只恢复文件中所列叶分区的数据。

默认仅恢复备份集中的数据库对象。Apache Cloudberry 系统对象自动包含在 `gpbackup` 备份集中，但只有为 `gprestore` 指定 `--with-globals` 选项时才会恢复这些对象。

恢复操作期间，会禁用待恢复表的统计信息自动更新。如果备份时使用 `--with-stats` 选项备份了查询计划统计信息，可以为 `gprestore` 指定 `--with-stats` 来恢复这些信息。如果备份时未使用 `--with-stats`，或希望在恢复期间收集当前统计信息，可以使用 `--run-analyze` 选项对恢复的表运行 `ANALYZE`。

恢复物化视图时，不会恢复其数据。要填充物化视图的数据，请使用 `REFRESH MATERIALIZED VIEW`。物化视图定义引用的表必须可用。`gprestore` 日志文件会列出已恢复的物化视图，以及用于填充这些物化视图数据的 `REFRESH MATERIALIZED VIEW` 命令。

创建多个并行连接来恢复表数据和元数据，可以提高恢复操作性能。默认情况下，`gprestore` 使用 1 个连接；对于大规模恢复操作，可以通过 `--jobs` 选项增加连接数。

恢复操作完成后，`gprestore` 返回状态码。

`gprestore` 可以在备份操作完成后发送状态邮件通知。发送时机和收件人在配置文件中指定。

注意：此工具通过系统之间的安全 shell（SSH）连接执行任务。在大型 Apache Cloudberry 部署、云部署，或每台主机包含大量 Segment 的部署中，此工具可能超过主机对未认证连接设置的最大阈值。可以考虑更新 SSH 的 `MaxStartups` 和 `MaxSessions` 配置参数以提高此阈值。有关 SSH 配置选项的更多信息，请参阅 Linux 发行版的 SSH 文档。

## 选项 {#options}

**--timestamp YYYYMMDDHHMMSS**

必需。指定待恢复的 `gpbackup` 备份集的时间戳。默认情况下，`gprestore` 尝试在 Apache Cloudberry Coordinator 主机的 $MASTER_DATA_DIRECTORY/backups/YYYYMMDD/YYYYMMDDhhmmss/ 目录中查找该时间戳对应的元数据文件，并在各 Segment 主机的 `<seg_dir>/backups/YYYYMMDD/YYYYMMDDhhmmss/` 目录中查找 CSV 数据文件。

**--backup-dir directory**

可选。从指定目录读取所有备份文件（元数据文件和数据文件）。directory 必须为绝对路径，不能是相对路径。如果未提供此选项，`gprestore` 尝试在 Apache Cloudberry Coordinator 主机的 $MASTER_DATA_DIRECTORY/backups/YYYYMMDD/YYYYMMDDhhmmss/ 目录中查找该时间戳对应的元数据文件。各 Segment 的 `<seg_dir>/backups/YYYYMMDD/YYYYMMDDhhmmss/` 目录中必须有可用的 CSV 数据文件。如果在运行 `gpbackup` 时指定了自定义备份目录，此处也应包含此选项。

此选项不能与 `--plugin-config` 选项组合使用。

**--create-db**

可选。恢复数据库对象元数据前先创建数据库。

通过克隆空的标准系统数据库 `template0` 来创建数据库。

**--copy-queue-size int**

可选。指定恢复备份集时，`gprestore` 应加入队列的 `COPY` 命令数量。此选项通过减少初始化 `COPY` 命令所耗费的时间来优化恢复性能。如果未将此选项设为 2 或更大，`gprestore` 每次只将 1 条 `COPY` 命令加入队列。

**--data-only**

可选。从 `gpbackup` 工具创建的备份中恢复表数据，不创建数据库表。此选项假定目标数据库中已存在这些表。要从备份集中恢复特定一组表的数据，可以指定包含或排除表或模式的选项。指定 `--with-stats` 选项，可从备份中恢复表统计信息。

备份集必须包含待恢复的表数据。例如，使用 `gpbackup` 的 `--metadata-only` 选项创建的备份不包含表数据。

`SEQUENCE` 值会更新为备份时的值。

若要仅恢复数据库表而不恢复表数据，请参阅 `--metadata-only` 选项。

**--debug**

可选。在恢复操作期间显示详细日志和调试日志消息。

**--exclude-schema schema_name**

可选。指定要从恢复操作中排除的数据库模式。可以多次指定此选项。此选项不能与 `--include-schema`、`--include-schema-file` 或 `--include-table` 等表筛选选项组合使用。**--exclude-schema-file file_name**：可选。指定一个文本文件，其中列出要从备份中排除的模式。文件每行必须定义一个模式，文件末尾不能有多余行。如果模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。此选项不能与 `--include-schema`、`--include-schema-file` 或 `--include-table` 等表筛选选项组合使用。

**--exclude-table schema.table**

可选。指定要从恢复操作中排除的表。可以多次指定此选项。表必须采用 `<schema-name>.<table-name>` 格式。如果表名或模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。可以多次指定此选项。如果备份集中不存在该表，恢复操作会失败。不能指定分区表的叶分区。

此选项不能与 `--exclude-schema`、`--exclude-schema-file` 或 `--include-table` 等其他表筛选选项组合使用。

**--exclude-table-file file_name**

可选。指定一个文本文件，其中列出要从恢复操作中排除的表。文件每行必须以 `<schema-name>.<table-name>` 格式定义一个表，文件末尾不能有多余行。如果表名或模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。如果备份集中不存在某个表，恢复操作会失败。不能指定分区表的叶分区。

此选项不能与 `--exclude-schema`、`--exclude-schema-file` 或 `--include-table` 等其他表筛选选项组合使用。

**--include-schema schema_name**

可选。指定要恢复的数据库模式。可以多次指定此选项。指定的所有模式都必须存在于备份集中。后续 `--include-schema` 选项未包含的模式都将从恢复操作中省略。

如果指定要包含的模式已经存在于数据库中，此工具会报告错误并继续操作。如果待恢复的表已存在于数据库中，工具会失败。

如果备份集中的对象依赖多个模式，则不能使用此选项。

**--include-schema-file file_name**

可选。指定一个文本文件，其中列出要恢复的模式。文件每行必须定义一个模式，文件末尾不能有多余行。如果模式名包含小写字母、数字或下划线以外的字符，必须用双引号括起该名称。

这些模式必须存在于备份集中。未在此文件中列出的模式都会从恢复操作中省略。

如果备份集中的对象依赖多个模式，则不能使用此选项。

**--include-table schema.table**

可选。指定要恢复的表，必须采用 `<schema-name>.<table-name>` 格式。可以多次指定此选项。不能指定分区表的叶分区。

也可以指定序列、视图或物化视图的限定名称。

指定此选项后，工具不会自动恢复依赖对象，必须显式指定所需的依赖对象。例如，恢复视图或物化视图时，还必须恢复其使用的表。恢复使用序列的表时，还必须恢复该序列。依赖对象必须存在于备份集中。

此选项不能与 `--include-schema` 等模式筛选选项，或 `--exclude-table-file` 等其他表筛选选项组合使用。

**--include-table-file file_name**

可选。指定一个文本文件，其中列出要恢复的表。文件每行必须以 `<schema-name>.<table-name>` 格式定义一个表，文件末尾不能有多余行。未在此文件中列出的表都会从恢复操作中省略。不能指定分区表的叶分区。

也可以指定序列、视图或物化视图的限定名称。

指定此选项后，工具不会自动恢复依赖对象，必须显式指定所需的依赖对象。例如，恢复视图或物化视图时，还必须指定其使用的表。指定使用序列的表时，还必须指定该序列。依赖对象必须存在于备份集中。

对于物化视图，不会恢复数据。要填充物化视图的数据，必须使用 `REFRESH MATERIALIZED VIEW`，且其定义引用的表必须可用。

使用 `--include-table-file` 选项时，`gprestore` 不创建角色，也不设置表所有者。工具会恢复表索引和规则，也会恢复触发器，但 Apache Cloudberry 不支持触发器。

**--incremental（测试版）**

可选。要求使用 `--data-only option`。仅恢复 `--timestamp` 选项指定的增量备份中的表数据，不恢复备份集中之前增量备份的表数据。**警告：** 此功能为测试版，不支持用于生产环境。

增量备份包含以下可恢复的表数据。

-   所有堆表的数据。
-   自上次备份以来发生更改的 AO 表数据。
-   自上次备份以来发生更改的叶分区数据。

指定此选项时，`gprestore` 会先截断表，再向表中重新加载数据。随后将 `SEQUENCE` 值更新为备份时的值。

执行恢复操作前，`gprestore` 会确保待恢复的表存在。如果某个表不存在，`gprestore` 会返回错误并退出。如果指定了 `--on-error-continue` 选项，`gprestore` 会记录缺失的表，并尝试完成恢复操作。

**警告：** 指定此选项时，`gpbackup` 假定待恢复表的表定义未发生更改，例如未添加或删除列。**--truncate-table**

可选。从备份恢复表数据前，先截断一组表中的数据。此选项用于用备份数据替换表数据，否则表数据可能重复。

必须通过 `--include-table` 或 `--include-table-file` 选项指定这组表，还必须指定 `--data-only`，以恢复表数据而不创建表。

可以与 `--redirect-db` 选项一起使用，不能与 `--redirect-schema` 一起使用。

**--redirect-schema schema_name**

可选。将数据恢复到指定模式，而非原有模式。指定模式必须已存在。如果待恢复的数据位于多个模式中，所有数据都会重定向到指定模式。

必须与包含表或模式的选项一起使用：`--include-table`、`--include-table-file`、`--include-schema` 或 `--include-schema-file`。

不能与 `--exclude-schema` 或 `--exclude-table` 等排除模式或表的选项一起使用。

可以与 `--metadata-only` 或 `--data-only` 选项一起使用。

**--resize-cluster（测试版）**

可选。使用此选项，可将数据恢复到 Segment 数量与原备份集群不同的集群。

警告：此功能为测试版，不支持用于生产环境。

注意：要启用 `gprestore` 的 `--resize-cluster` 功能，必须使用 `gpbackup` 1.26 或更高版本创建备份。

**--jobs int**

可选。指定恢复表数据和元数据时使用的并行连接数。默认情况下，`gprestore` 使用 1 个连接。增大此值可以提高数据恢复速度。**注意：** 如果使用了 `gpbackup --single-data-file` 选项，将表备份合并为每个 Segment 一个文件，则不能将 `--jobs` 设为大于 1 的值来执行并行恢复。

**--metadata-only**

可选。从 `gpbackup` 工具创建的备份中创建数据库表，但不恢复表数据。此选项假定目标数据库中不存在这些表。要从备份集中创建特定一组表，可以指定包含或排除表或模式的选项。指定 `--with-globals` 选项，可恢复 Apache Cloudberry 系统对象。

备份集必须包含待恢复表的 DDL。例如，使用 `gpbackup` 的 `--data-only` 选项创建的备份不包含表的 DDL。

**--on-error-continue**

可选。指定此选项后，如果创建数据库元数据（如表、角色或函数）或恢复数据时发生 SQL 错误，会继续恢复操作。如果发生其他类型的错误，工具会退出。默认在第一个错误发生时退出。

包含此选项时，工具会显示错误汇总，将错误信息写入 `gprestore` 日志文件，并继续恢复操作。它还会在备份目录中创建文本文件，列出发生 SQL 错误的表。

-   发生元数据错误的表 - `gprestore_<backup-timestamp>_<restore-time>_error_tables_metadata`
-   发生数据错误的表 - `gprestore_<backup-timestamp>_<restore-time>_error_tables_data`

**--plugin-config config-file_location**

指定 `gpbackup` 插件配置文件的位置。该文件是 YAML 格式的文本文件，包含 `gprestore` 在恢复操作中使用的插件应用程序的配置信息。

备份数据库时如果指定了 `--plugin-config` 选项，从该备份恢复数据库时也必须指定此选项，并提供对应插件应用程序的配置信息。

此选项不能与 `--backup-dir` 选项组合使用。

**--quiet**

可选。不输出除警告和错误外的所有日志消息。

**--redirect-db database_name**

可选。恢复到指定的 database_name，而非原来备份的数据库。

**--verbose**

可选。在恢复操作期间显示详细日志消息。**--version**：可选。打印版本号并退出。

**--with-globals**

可选。除数据库对象外，还恢复备份集中的 Apache Cloudberry 系统对象。

**--with-stats**

可选。从备份集中恢复查询计划统计信息。如果创建备份集时未使用 `--with-stats` 选项，将返回错误。恢复的表仅具有备份中的统计信息。此选项不能与 `--run-analyze` 一起使用。

要在恢复操作期间为恢复的表收集当前统计信息，请使用 `--run-analyze` 选项。也可以在恢复表之后对其运行 `ANALYZE` 命令。

**--run-analyze**

可选。对恢复的表运行 `ANALYZE`。对于分区表，在根分区表上运行 `ANALYZE`。如果备份时指定了 `--with-stats`，这些统计信息会被忽略。此选项不能与 `--with-stats` 一起使用。

如果待恢复的备份使用了 `gpbackup` 的 `--leaf-partition-data` 选项，`gprestore` 仅对恢复的各个叶分区运行 `ANALYZE`，而非根分区表。

根据待恢复表的情况，对恢复的表运行 `ANALYZE` 可能延长恢复操作耗时。

**--help**

显示在线帮助。

## 返回码 {#return-codes}

`gprestore` 完成后会返回以下代码之一。

-   0 -- 恢复顺利完成。
-   1 -- 恢复完成，但有非致命错误。更多信息请查看日志文件。
-   2 -- 恢复因致命错误而失败。更多信息请查看日志文件。

## 示例 {#examples}

创建 demo 数据库，并恢复指定时间戳备份集中的所有模式和表：

```
$ dropdb demo
$ gprestore --timestamp 20171103152558 --create-db
```

将备份集恢复到“demo2”数据库，而非原来备份的“demo”数据库：

```
$ createdb demo2
$ gprestore --timestamp 20171103152558 --redirect-db demo2
```

除数据库对象外，还恢复 Apache Cloudberry 全局元数据和查询计划统计信息：

```
$ gprestore --timestamp 20171103152558 --create-db --with-globals --with-stats
```

使用 /home/gpadmin/backup 目录中的备份文件进行恢复，并创建 8 个并行连接：

```
$ gprestore --backup-dir /home/gpadmin/backups/ --timestamp 20171103153156 --create-db --jobs 8
```

仅恢复备份集中的“wikipedia”模式：

```
$ dropdb demo
$ gprestore --include-schema wikipedia --backup-dir /home/gpadmin/backups/ --timestamp 20171103153156 --create-db
```

从增量备份集恢复时，`gprestore` 必须能够访问备份集中所有必需的文件。例如，以下时间戳键指定一个增量备份集。20170514054532 是完整备份，其他均为增量备份。

```
20170514054532 (full backup)
20170714095512
20170914081205
20171114064330
20180114051246
```

以下 `gprestore` 命令指定时间戳 20121114064330。要执行恢复，时间戳为 20120714095512 和 20120914081205 的增量备份以及完整备份都必须可用。

```
gprestore --timestamp 20121114064330 --redirect-db mystest --create-db
```
