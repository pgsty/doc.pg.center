---
title: "加载数据"
description: "介绍向 Apache Cloudberry 添加数据的不同方式。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/best-practices/load-data-best-practices.md"
---

## 使用列值的 INSERT 语句 {#insert-statement-with-column-values}

带值的单行 `INSERT` 语句会向表中添加一行。该行经过 Coordinator 后分布到一个 Segment。这是最慢的方法，不适合加载大量数据。

## COPY 语句 {#copy-statement}

PostgreSQL `COPY` 语句将外部文件中的数据复制到数据库表中。与 `INSERT` 语句相比，它可以更高效地插入多行，但这些行仍然会经过 Coordinator。所有数据通过一条命令复制；该过程不是并行的。

`COPY` 命令的输入数据来自文件或标准输入。例如：

```sql
COPY table FROM '/data/mydata.csv' WITH CSV HEADER;
```

使用 `COPY` 添加相对较小的数据集，例如最多包含一万行的维度表，或执行一次性数据加载。

编写加载少量数据（少于 10,000 行）的脚本时，可以使用 `COPY`。

COPY 是单条命令，因此使用这种方式填充表时不需要停用自动提交。

可以并发运行多个 `COPY` 命令以提升性能。

## 外部表 {#external-tables}

外部表可以访问 Apache Cloudberry 之外的数据源。可以使用 `SELECT` 语句访问外部表；外部表通常与提取、加载、转换（ELT）模式结合使用。ELT 是提取、转换、加载（ETL）模式的变体，利用了 Apache Cloudberry 快速并行加载数据的能力。

在 ETL 模式中，从源提取数据，使用 Datastage 等外部转换工具在数据库外部进行转换，然后将数据加载到数据库中。

在 ELT 模式中，Cloudberry 外部表可以访问外部数据源，包括只读文件（例如文本、CSV 或 XML 文件）、Web 服务器、Hadoop 文件系统、可执行操作系统程序，或下一节介绍的 Cloudberry `gpfdist` 文件服务器。外部表支持选择、排序和连接等 SQL 操作，因此可以同时加载和转换数据，也可以先将数据加载到*加载表*，再在数据库中将其转换到目标表。

使用 `CREATE EXTERNAL TABLE` 语句定义外部表，其中 `LOCATION` 子句定义数据位置，`FORMAT` 子句定义源数据的格式，以便系统解析输入数据。文件使用 `file://` 协议，并且必须位于某个 Segment 主机上、Cloudberry 超级用户可以访问的位置。数据可以分散到多个 Segment 主机上，但每台主机上的每个主 Segment 最多对应一个文件。`LOCATION` 子句中列出的文件数量，就是并行读取外部表的 Segment 数量。

## 使用 gpfdist 的外部表 {#external-tables-with-gpfdist}

加载大型事实表最快的方法，是使用带 `gpfdist` 的外部表。`gpfdist` 是使用 HTTP 协议的文件服务器程序，可以并行向 Apache Cloudberry Segment 提供外部数据文件。一个 `gpfdist` 实例每秒可提供 200 MB，多个 `gpfdist` 进程可以同时运行，每个进程为待加载数据提供一部分数据。使用类似 `INSERT INTO <table> SELECT * FROM <external_table>` 的语句开始加载时，Coordinator 解析 `INSERT` 语句并将其分发到各个主 Segment。Segment 连接到 `gpfdist` 服务器，并行获取数据，解析和验证数据，计算分布键数据的哈希值，然后根据哈希键将行发送到目标 Segment。默认情况下，每个 `gpfdist` 实例最多接受来自 Segment 的 64 个连接。参与加载的 Segment 和 `gpfdist` 服务器较多时，数据可以以很高的速率加载。

使用 `gpfdist` 时，主 Segment 会并行访问外部文件，最大并行数由 `gp_external_max_segs` 的值决定。优化 `gpfdist` 性能时，应随着 Segment 数量增加而最大化并行度。将数据均匀分散到尽可能多的 ETL 节点上。将超大数据文件拆分成大小相等的部分，并尽可能分散到多个文件系统中。

每个文件系统运行两个 `gpfdist` 实例。加载时，`gpfdist` 往往受 Segment 节点的 CPU 限制。但是，例如在有八个机架的 Segment 节点的情况下，Segment 上有大量可用 CPU，可以驱动更多 `gpfdist` 进程。尽可能在多个接口上运行 `gpfdist`。注意绑定的 NIC，并确保启动足够多的 `gpfdist` 实例来使用这些接口。

必须在所有这些资源之间保持均衡。加载速度取决于最慢的节点。加载文件布局中的数据倾斜会使整个加载过程受该资源限制。

配置参数 `gp_external_max_segs` 控制每个 `gpfdist` 进程服务的 Segment 数量，默认值为 64。可以在 Coordinator 上的 `postgresql.conf` 配置文件中设置其他值。始终使 `gp_external_max_segs` 与 `gpfdist` 进程数构成整数倍关系；也就是说，`gp_external_max_segs` 的值应当是 `gpfdist` 进程数的倍数。例如，如果有 12 个 Segment 和 4 个 `gpfdist` 进程，规划器会按如下方式轮询 Segment 连接：

```
Segment 1  - gpfdist 1 
Segment 2  - gpfdist 2 
Segment 3  - gpfdist 3 
Segment 4  - gpfdist 4 
Segment 5  - gpfdist 1 
Segment 6  - gpfdist 2 
Segment 7  - gpfdist 3 
Segment 8  - gpfdist 4 
Segment 9  - gpfdist 1 
Segment 10 - gpfdist 2 
Segment 11 - gpfdist 3 
Segment 12 - gpfdist 4
```

向已有表加载数据前删除索引，加载后重新创建索引。对已有数据创建索引，比每加载一行就增量更新索引更快。

加载后对表运行 `ANALYZE`。将 `gp_autostats_mode` 设为 `NONE`，在加载期间停用自动统计信息收集。加载出错后运行 `VACUUM`，回收空间。

向高度分区的列存储表执行小批量、高频率数据加载，可能会因为每个时间段访问的物理文件数量较多而对系统产生很大影响。

## gpload {#gpload}

`gpload` 是数据加载工具，为 Cloudberry 外部表并行加载功能提供接口。

使用 `gpload` 时应谨慎，因为它会通过创建和删除外部表导致目录膨胀。应改用 `gpfdist`，因为它能提供最佳性能。

`gpload` 使用 YAML 格式控制文件中定义的规范执行加载。它会执行以下操作：

- 调用 `gpfdist` 进程
- 根据源数据定义创建临时外部表
- 执行 `INSERT`、`UPDATE` 或 `MERGE` 操作，将源数据加载到数据库的目标表
- 删除临时外部表
- 清理 `gpfdist` 进程

加载过程在单个事务中完成。

## 最佳实践 {#best-practices}

- 向已有表加载数据前删除所有索引，并在加载后重新创建索引。新建索引比每加载一行就增量更新索引更快。
- 将 `gp_autostats_mode` 配置参数设为 `NONE`，在加载期间停用自动统计信息收集。
- 外部表不适合频繁或临时访问。
- 使用 `gpfdist` 时，在 ETL 服务器上为每个 NIC 运行一个 `gpfdist` 实例，以最大化网络带宽。将源数据均匀分配到各个 `gpfdist` 实例。
- 使用 `gpload` 时，在资源允许的情况下运行尽可能多的并发 `gpload` 实例。利用可用的 CPU、内存和网络资源，增加从 ETL 服务器向 Apache Cloudberry 传输的数据量。
- 使用 `COPY` 语句的 `SEGMENT REJECT LIMIT` 子句，设置在取消 `COPY FROM` 命令前允许出错的行数或比例上限。拒绝上限按 Segment 计算；任意一个 Segment 超过该上限时，命令会被取消，并且不会添加任何行。使用 `LOG ERRORS` 子句保存错误行。如果行存在格式错误（例如缺少或多出值，或数据类型不正确），Apache Cloudberry 会在内部保存错误信息和该行。使用内置 SQL 函数 `gp_read_error_log()` 访问这些保存的信息。
- 如果加载出错，对表运行 `VACUUM`，回收空间。
- 向表加载数据后，对堆表（包括系统目录）运行 `VACUUM`，并对所有表运行 `ANALYZE`。对 AO 表不需要运行 `VACUUM`。如果表已分区，可以只清理和分析受数据加载影响的分区。这些步骤会清理提前结束的加载、删除或更新留下的行，并更新表统计信息。
- 大量加载数据后，重新检查表的 Segment 数据倾斜。可以使用类似以下查询检查倾斜：

    ```sql
    SELECT gp_segment_id, count(*) 
    FROM schema.table 
    GROUP BY gp_segment_id ORDER BY 2;
    ```

- 默认情况下，`gpfdist` 假定最大记录大小为 32K。要加载大于 32K 的数据记录，必须在 `gpfdist` 命令行中指定 `-m <*bytes*>` 选项来增大最大行大小参数。如果使用 `gpload`，则在 `gpload` 控制文件中设置 `MAX_LINE_LENGTH` 参数。
