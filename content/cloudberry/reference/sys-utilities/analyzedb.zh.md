---
title: "analyzedb"
description: "对表执行增量并发 `ANALYZE` 操作的工具。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/analyzedb.md"
---

对于 AO 表，analyzedb 仅在统计信息不是最新时更新统计信息。

## 概要 {#synopsis}

```shell
analyzedb -d <dbname>
   { -s <schema>  | 
   { -t <schema>.<table> 
     [ -i <col1>[,<col2>, ...] | 
       -x <col1>[,<col2>, ...] ] } |
     { -f | --file} <config-file> }
   [ -l | --list ]
   [ --gen_profile_only ]   
   [ -p <parallel-level> ]
   [ --full ]
   [ --skip_root_stats ]
   [ --skip_orca_root_stats ]
   [ -v | --verbose ]
   [ -a ]
   [ --skip-locked ]

analyzedb { --clean_last | --clean_all }
analyzedb --version
analyzedb { -? | -h | --help }
```

## 说明 {#description}

analyzedb 工具以增量并发方式更新 Apache Cloudberry 中指定表的数据统计信息。

执行 [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/) 操作时，analyzedb 会创建表元数据快照，并将其存储在 Coordinator 主机的磁盘上。仅当表发生过修改时才会执行 `ANALYZE` 操作。如果表或分区自上次分析以来未发生修改，analyzedb 会自动跳过该表或分区，因为其中已经包含最新统计信息。

- 对于 AO 表，如果统计信息不是最新，analyzedb 会增量更新统计信息。例如，表的统计信息收集后表数据发生了变化时。如果表没有统计信息，则会收集统计信息。
- 对于堆表，始终更新统计信息。

指定 `--full` 选项，即使 AO 表的统计信息是最新的，也会更新这些统计信息。

默认情况下，analyzedb 最多创建 5 个并发会话，以并行分析表。对于每个会话，analyzedb 都会向数据库发出一条 ANALYZE 命令，并指定不同的表名。`-p` 选项控制并发会话的最大数量。

**分区 AO 表**

对于分区 AO 表，analyzedb 会检查根分区表和叶分区。如果需要，此工具会更新统计信息过期的分区及根分区的统计信息。有关分区表统计信息收集方式的信息，请参阅 [`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/)。

`analyzedb` 遇到统计信息过期的分区时，即使已经收集了统计信息，也必须在分区表中采样其他分区。建议每次向分区表添加新分区时，都在根分区上运行 `analyzedb`。此操作会并行分析叶分区，并将更新后的统计信息合并到根分区中。

## 注意事项 {#notes}

如果表经过 DML 或 DDL 命令修改，analyzedb 工具会更新 AO 表的统计信息，这些命令包括 INSERT、DELETE、UPDATE、CREATE TABLE、ALTER TABLE 和 TRUNCATE。此工具会将表的目录元数据与上一次 analyzedb 操作中获取的元数据快照进行比较，以确定表是否发生修改。表元数据快照以状态文件形式存储在 Apache Cloudberry Coordinator 数据目录的 `db_analyze/<db_name>/<timestamp>` 目录中。

此工具会保留过去 8 天的旧快照信息，以及不论存在时间长短都保留最近 3 个状态目录，同时自动删除其他所有目录。也可以指定 `--clean_last` 或 `--clean_all` 选项，删除 analyzedb 生成的状态文件。

如果未指定表、表集合或模式，analyzedb 工具会根据需要，收集数据库中所有系统目录表和用户定义表的统计信息。

外部表不受 analyzedb 影响。

不支持包含空格的表名。

直接对表运行 `ANALYZE` 命令（不使用 `analyzedb` 工具）不会更新 `analyzedb` 用于确定表统计信息是否最新的表元数据。

## 选项 {#options}

**`--clean_last`**

删除上一次 analyzedb 操作生成的状态文件。除 -d 外，其他所有选项均被忽略。

**`--clean_all`**

删除 analyzedb 生成的所有状态文件。除 -d 外，其他所有选项均被忽略。

**`-d dbname`**

指定包含待分析表的数据库名称。如果未指定此选项，将从环境变量 `PGDATABASE` 读取数据库名称。如果未设置 `PGDATABASE`，则使用为连接指定的用户名。

**`-f config-file | --file config-file`**

包含待分析表列表的文本文件。可以指定相对于当前目录的文件路径。

该文件每行列出一个表。表名必须使用模式名限定。也可以使用 -i 或 -x 指定列列表。文件中不允许使用其他选项。`--full` 等其他选项必须在命令行中指定。

用于指定待分析文件的选项只能使用其中一个：`-f` 或 `--file`、`-t` 或 `-s`。

对多个表执行 ANALYZE 操作时，analyzedb 会创建并发会话来并行分析表。`-p` 选项控制并发会话的最大数量。

以下示例中，第一行对表 `public.nation` 执行 ANALYZE 操作；第二行仅对表 `public.lineitem` 中的 `l_shipdate` 和 `l_receiptdate` 列执行 ANALYZE 操作。

```shell
public.nation
public.lineitem -i l_shipdate,l_receiptdate 
```

**`--full`**

对所有指定表执行 ANALYZE 操作。即使统计信息已经是最新的，也会执行此操作。

**`--gen_profile_only`**

更新 `analyzedb` 的表统计信息快照，但不执行任何 `ANALYZE` 操作。如果其他选项指定了表或模式，则仅更新指定表的快照信息。

如果已经对数据库表运行了 `ANALYZE` 命令，并且希望更新这些表的 `analyzedb` 快照，请指定此选项。

**`-i col1,col2, ...`**

可选。必须与 -t 选项一起指定。对于由 -t 选项指定的表，仅收集指定列的统计信息。

只能指定 -i 或 -x，不能同时指定这两个选项。

**`-l | --list`**

列出使用指定选项时将要分析的表。不执行 ANALYZE 操作。

**`-p parallel-level`**

并行分析的表数量。parallel level 可以是介于 1 和 10（含）之间的整数。默认值为 5。

**`--skip_root_stats`**

此选项已不再使用，可以从脚本中删除。

**`--skip_orca_root_stats`**

> **注意** 如果启用了 GPORCA，请勿使用此选项。

如果发现 `ANALYZE ROOTPARTITION` 命令执行时间很长，请使用此选项。

> **小心** 使用此选项运行 `analyzedb` 后，后续执行 `analyzedb` 时，除非表发生变化，否则不会更新根分区统计信息。

**`-s schema`**

指定要分析的模式。模式中的所有表都会被分析。命令行中只能指定一个模式名。

用于指定待分析文件的选项只能使用其中一个：`-f` 或 `--file`、`-t` 或 `-s`。

**`-t schema.table`**

仅收集 schema.table 的统计信息。表名必须使用模式名限定。命令行中只能指定一个表名。可以使用 `-f` 选项指定文件中的多个表，也可以使用 `-s` 选项指定某个模式中的所有表。

用于指定待分析文件的这些选项只能使用其中一个：`-f` 或 `--file`、`-t` 或 `-s`。

**`-x col1,col2, ...`**

可选。必须与 -t 选项一起指定。对于由 -t 选项指定的表，排除指定列的统计信息收集。仅收集未列出的列的统计信息。

只能指定 -i 或 -x，不能同时指定这两个选项。

**`-a`**

静默模式。不提示用户确认。

**`--skip-locked`**

跳过无法立即锁定的关系。

**`-h | -? | --help`**

显示在线帮助。

**`-v | --verbose`**

如果指定此选项，将日志级别设为 verbose，在命令执行期间向日志文件和命令行写入额外信息。这些信息包括所有待分析表的列表（包括分区表的叶分区）。输出还包括每个 `ANALYZE` 操作的持续时间。

**`--version`**

显示此工具的版本。

## 示例 {#examples}

示例：仅收集一组表列的统计信息。在数据库 `mytest` 中，收集表 `public.orders` 的 `shipdate` 和 `receiptdate` 列的统计信息：

```shell
analyzedb -d mytest -t public.orders -i shipdate,receiptdate
```

示例：对表执行统计信息收集并排除一组列。在数据库 `mytest` 中，收集表 `public.foo` 的统计信息，但不收集 `bar` 和 `test2` 列的统计信息。

```shell
analyzedb -d mytest -t public.foo -x bar,test2
```

示例：指定包含表列表的文件。此命令在名为 `mytest` 的数据库中，对文件 `analyze-tables` 所列的表收集统计信息。

```shell
analyzedb -d mytest -f analyze-tables
```

如果未指定表、表集合或模式，analyzedb 工具会根据需要，收集指定数据库中所有目录表和用户定义表的统计信息。此命令会刷新数据库 `mytest` 中系统目录表和用户定义表的表统计信息。

```shell
analyzedb -d mytest
```

可以创建 PL/Python 函数，将 `analyzedb` 工具作为 Apache Cloudberry 函数运行。此示例 `CREATE FUNCTION` 命令创建一个用户定义的 PL/Python 函数，该函数运行 `analyzedb` 工具并在命令行显示输出。将 `analyzedb` 选项指定为函数参数。

```sql
CREATE OR REPLACE FUNCTION analyzedb(params TEXT)
  RETURNS VOID AS
$BODY$
    import subprocess
    cmd = ['analyzedb', '-a' ] + params.split()
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        # verbose output of process
        for line in proc.stdout:
            plpy.info(line.decode(errors='replace'))
$BODY$
LANGUAGE plpython3u VOLATILE;
```

gpadmin 用户运行此 `SELECT` 命令时，`analyzedb` 工具会对数据库 `mytest` 中的表 `public.mytable` 执行分析操作。

```sql
SELECT analyzedb('-d mytest -t public.mytable');
```

> **注意** 要创建 PL/Python 函数，必须在数据库中将 PL/Python 过程语言注册为一种语言。例如，以下以 gpadmin 身份运行的 `CREATE LANGUAGE` 命令会将 PL/Python 注册为不受信任语言：

```sql
CREATE LANGUAGE plpython3u;
```

## 另请参阅 {#see-also}

[`ANALYZE`](/cloudberry/reference/sql-stmts/analyze/)
