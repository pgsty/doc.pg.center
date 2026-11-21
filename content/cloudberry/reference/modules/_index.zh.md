---
title: 扩展模块概览
description: Apache Cloudberry 可选模块的版本、2.x 变更和构建方式，涵盖数据类型、函数、操作符、外部数据包装器、存储格式和诊断工具。
weight: 40
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/index.md
---

Apache Cloudberry 提供一组可选模块，为数据库增加数据类型、函数、操作符、外部数据包装器、存储格式和诊断工具。这些模块位于源码树中的两个目录：

- `contrib/` 包含来自 PostgreSQL 的模块，以及 Apache Cloudberry 增加的若干模块。
- `gpcontrib/` 包含 Apache Cloudberry 专有的模块。

本页列出 Apache Cloudberry 2.2 中这两个目录下的所有模块，以及各模块的版本、在 2.x 各版本中的变更和构建方式。

## 使用模块 {#use-a-module}

大多数模块封装为扩展。要使用扩展，需要在每个目标数据库中注册一次：

```sql
CREATE EXTENSION <extension_name>;
```

列出集群上安装的扩展和当前数据库中注册的扩展：

```sql
SELECT name, default_version, installed_version FROM pg_available_extensions ORDER BY name;
```

某些模块是没有 SQL 对象的普通共享库。可以使用 `LOAD` 加载这类模块，或将其添加到 `shared_preload_libraries` 或 `session_preload_libraries`。各模块的页面会说明适用的方法。

## 表格说明 {#how-to-read-the-tables}

**版本**是 Apache Cloudberry 2.2 中的扩展版本（模块控制文件中的 `default_version`）。短横线表示该模块是没有扩展版本的库或程序。

**2.x 变更**比较 2.0、2.1 和 2.2 各版本的差异，也比较 2.0 与 1.6 的差异：

- **2.0 新增**、**2.1 新增**、**2.2 新增**：首次包含该模块的版本。
- **……更新**：该发行版本更改了扩展版本。
- 短横线表示模块在 2.0、2.1 和 2.2 中均存在，且版本相同。

**构建**说明从源码构建 Apache Cloudberry 时如何构建该模块：

- **默认**：在源码树根目录执行 `make` 和 `make install` 即可构建并安装模块。
- **按需**：模块包含在源码树中，但需要显式构建，例如执行 `make -C contrib/<module> install`，或构建 `world` 目标。源码树 `devops/build/automation/cloudberry/scripts` 中的构建脚本也会构建并安装 `contrib/`，因此只要设置了所需的 `configure` 选项，使用这些脚本构建的集群就会包含这些模块。
- **某个 `configure` 选项**：只有向 `configure` 传入该选项才会构建模块。如果选项默认开启，表格会予以说明。
- **不构建**：源码包含在树中，但 Apache Cloudberry 的 makefile 没有构建它的目标。

模块文件必须安装在 Coordinator 和每台 Segment 主机上。

> [!NOTE]
> 链接到本节页面的模块已对照 Apache Cloudberry 2.x 源码审查。其他 PostgreSQL 模块的链接指向 PostgreSQL 文档。这些模块遵循 PostgreSQL 的行为，其中一些可能在分布式集群中存在限制。

## contrib/ 中的模块 {#modules-in-contrib}

### PostgreSQL 模块 {#postgresql-modules}

| 模块 | 说明 | 版本 | 2.x 变更 | 构建 |
|---|---|---|---|---|
| [adminpack](https://www.postgresql.org/docs/14/adminpack.html) | 为 pgAdmin 等管理工具提供支持函数。 | 2.1 | — | 不构建 |
| [amcheck](https://www.postgresql.org/docs/14/amcheck.html) | 验证关系和索引的逻辑一致性。 | 1.3 | — | 按需 |
| [auth_delay](https://www.postgresql.org/docs/14/auth-delay.html) | 在报告认证失败之前暂停一段时间。 | — | — | 按需 |
| [auto_explain](/cloudberry/reference/modules/auto-explain/) | 自动记录慢语句的执行计划。 | — | — | 默认 |
| [bloom](https://www.postgresql.org/docs/14/bloom.html) | 基于布隆过滤器的索引访问方法。 | 1.0 | — | 按需 |
| bool_plperl | 在 `bool` 与 PL/Perl 之间转换。 | 1.0 | — | 按需，需使用 `--with-perl` |
| [btree_gin](/cloudberry/reference/modules/btree-gin/) | 提供 B-树行为的 GIN 操作符类。 | 1.3 | — | 默认 |
| [btree_gist](https://www.postgresql.org/docs/14/btree-gist.html) | 提供 B-树行为的 GiST 操作符类。 | 1.6 | — | 按需 |
| [citext](/cloudberry/reference/modules/citext/) | 不区分大小写的字符串类型。 | 1.6 | — | 默认 |
| [cube](https://www.postgresql.org/docs/14/cube.html) | 多维立方体数据类型。 | 1.5 | — | 不构建 |
| [dblink](/cloudberry/reference/modules/dblink/) | 在会话内连接其他数据库。 | 1.2 | — | 默认 |
| [dict_int](https://www.postgresql.org/docs/14/dict-int.html) | 用于整数的文本搜索词典模板。 | 1.0 | — | 按需 |
| [dict_xsyn](https://www.postgresql.org/docs/14/dict-xsyn.html) | 用于扩展同义词处理的文本搜索词典模板。 | 1.0 | — | 按需 |
| [earthdistance](https://www.postgresql.org/docs/14/earthdistance.html) | 计算地球表面的大圆距离。 | 1.1 | — | 不构建 |
| [file_fdw](https://www.postgresql.org/docs/14/file-fdw.html) | 用于服务器文件系统中文件的外部数据包装器。 | 1.0 | — | 默认 |
| [fuzzystrmatch](/cloudberry/reference/modules/fuzzystrmatch/) | 确定字符串之间的相似度和距离。 | 1.1 | — | 默认 |
| [hstore](/cloudberry/reference/modules/hstore/) | 在单个值中存储一组键值对。 | 1.8 | — | 默认 |
| hstore_plperl | 在 `hstore` 与 PL/Perl 之间转换。 | 1.0 | — | 按需，需使用 `--with-perl` |
| hstore_plpython | 在 `hstore` 与 PL/Python 之间转换。 | 1.0 | — | 按需，需使用 `--with-python`（默认开启） |
| [intagg](https://www.postgresql.org/docs/14/intagg.html) | 整数聚合器和枚举器（已过时）。 | 1.1 | — | 按需 |
| [intarray](https://www.postgresql.org/docs/14/intarray.html) | 用于整数数组的函数、操作符和索引支持。 | 1.5 | — | 按需 |
| [isn](/cloudberry/reference/modules/isn/) | 用于国际产品编号标准的数据类型。 | 1.2 | — | 按需 |
| jsonb_plperl | 在 `jsonb` 与 PL/Perl 之间转换。 | 1.0 | — | 按需，需使用 `--with-perl` |
| jsonb_plpython | 在 `jsonb` 与 PL/Python 之间转换。 | 1.0 | — | 按需，需使用 `--with-python`（默认开启） |
| [lo](https://www.postgresql.org/docs/14/lo.html) | 大对象维护。 | 1.1 | — | 不构建 |
| [ltree](/cloudberry/reference/modules/ltree/) | 用于层级树状标签的数据类型。 | 1.2 | — | 按需 |
| ltree_plpython | 在 `ltree` 与 PL/Python 之间转换。 | 1.0 | — | 按需，需使用 `--with-python`（默认开启） |
| [oid2name](https://www.postgresql.org/docs/14/oid2name.html) | 将 OID 和文件节点解析为名称的工具。 | — | — | 按需 |
| [old_snapshot](https://www.postgresql.org/docs/14/oldsnapshot.html) | 显示 `old_snapshot_threshold` 使用的 XID/时间映射。 | 1.0 | — | 按需 |
| [pageinspect](/cloudberry/reference/modules/pageinspect/) | 从底层检查数据库页面的内容。 | 1.9 | — | 默认 |
| [passwordcheck](https://www.postgresql.org/docs/14/passwordcheck.html) | 检查密码强度。 | — | — | 默认 |
| [pg_buffercache](/cloudberry/reference/modules/pg-buffercache/) | 检查共享缓冲区缓存。 | 1.4.1 | **2.0 更新**（1.3 → 1.4.1） | 默认 |
| [pg_freespacemap](https://www.postgresql.org/docs/14/pgfreespacemap.html) | 检查空闲空间映射。 | 1.2 | — | 按需 |
| [pg_prewarm](https://www.postgresql.org/docs/14/pgprewarm.html) | 将关系数据加载到缓冲区缓存。 | 1.2 | — | 按需 |
| [pg_standby](https://www.postgresql.org/docs/14/pgstandby.html) | 用于温备服务器的工具。 | — | — | 不构建 |
| [pg_stat_statements](https://www.postgresql.org/docs/14/pgstatstatements.html) | 跟踪 SQL 语句的规划和执行统计信息。 | 1.9 | — | 按需 |
| [pg_surgery](https://www.postgresql.org/docs/14/pgsurgery.html) | 修复损坏的关系。 | 1.0 | — | 按需 |
| [pg_trgm](/cloudberry/reference/modules/pg-trgm/) | 基于三元组的文本相似度度量和索引搜索。 | 1.6 | — | 默认 |
| [pg_visibility](https://www.postgresql.org/docs/14/pgvisibility.html) | 检查可见性映射和页级可见性信息。 | 1.2 | — | 按需 |
| [pgcrypto](/cloudberry/reference/modules/pgcrypto/) | 密码学函数。 | 1.3 | — | 默认 |
| [pgrowlocks](https://www.postgresql.org/docs/14/pgrowlocks.html) | 显示行级锁定信息。 | 1.2 | — | 按需 |
| [pgstattuple](https://www.postgresql.org/docs/14/pgstattuple.html) | 显示元组级统计信息。 | 1.5 | — | 按需 |
| [postgres_fdw](/cloudberry/reference/modules/postgres-fdw/) | 用于访问外部 PostgreSQL 服务器上所存数据的外部数据包装器。 | 1.1 | — | 按需 |
| [seg](https://www.postgresql.org/docs/14/seg.html) | 表示线段或浮点数区间的数据类型。 | 1.4 | — | 按需 |
| [sepgsql](https://www.postgresql.org/docs/14/sepgsql.html) | 基于 SELinux 标签的强制访问控制。 | — | — | 按需，需使用 `--with-selinux` |
| [spi](https://www.postgresql.org/docs/14/contrib-spi.html) | 示例触发器函数：`autoinc`、`insert_username`、`moddatetime` 和 `refint`。 | 1.0 | — | 按需 |
| [sslinfo](/cloudberry/reference/modules/sslinfo/) | 当前客户端的 SSL 证书信息。 | 1.2 | — | 按需，需要 OpenSSL |
| start-scripts | 在系统启动时启动服务器的示例脚本。 | — | — | 不构建 |
| [tablefunc](/cloudberry/reference/modules/tablefunc/) | 返回表的函数，包括 `crosstab`。 | 1.0 | — | 默认 |
| [tcn](https://www.postgresql.org/docs/14/tcn.html) | 向监听者通知表变更的触发器函数。 | 1.0 | — | 按需 |
| [test_decoding](https://www.postgresql.org/docs/14/test-decoding.html) | 逻辑解码的示例输出插件。 | — | — | 按需 |
| [tsm_system_rows](/cloudberry/reference/modules/tsm-system-rows/) | `SYSTEM_ROWS` 表采样方法。 | 1.0 | — | 按需 |
| [tsm_system_time](/cloudberry/reference/modules/tsm-system-time/) | `SYSTEM_TIME` 表采样方法。 | 1.0 | — | 按需 |
| [unaccent](https://www.postgresql.org/docs/14/unaccent.html) | 去除重音符号的文本搜索词典。 | 1.1 | — | 按需 |
| [uuid-ossp](/cloudberry/reference/modules/uuid-ossp/) | 生成通用唯一标识符（UUID）的函数。 | 1.1 | — | 按需，需使用 `--with-uuid=LIB` |
| [vacuumlo](https://www.postgresql.org/docs/14/vacuumlo.html) | 删除孤立大对象的工具。 | — | — | 按需 |
| [xml2](https://www.postgresql.org/docs/14/xml2.html) | XPath 查询和 XSLT 函数（已过时）。 | 1.1 | — | 按需，需使用 `--with-libxml` |

### Apache Cloudberry 模块 {#apache-cloudberry-modules}

| 模块 | 说明 | 版本 | 2.x 变更 | 构建 |
|---|---|---|---|---|
| extprotocol | 外部表自定义协议示例。 | — | — | 默认 |
| formatter | 外部表自定义数据格式化器示例。 | — | — | 默认 |
| formatter_fixedwidth | 读写定宽数据文件的自定义格式化器。 | — | — | 默认 |
| indexscan | 用于测试和诊断的 `readindex()` 函数，读取索引条目。 | — | — | 默认 |
| interconnect | 以可加载模块形式提供的 Interconnect 实现（UDP、TCP 和代理）。`interconnect` 扩展添加包含 Interconnect 统计信息的视图。 | 1.0 | **2.2 更新**（封装为扩展） | 默认 |
| pax_storage | PAX 表格式。参阅 [PAX 存储格式](/cloudberry/operate-with-data/pax-table-format/)。 | — | **2.0 新增** | `--enable-pax` |
| sasdemo | 与 SAS 交换数据的示例程序和格式化器函数。 | — | — | 不构建 |
| try_convert | 类型转换失败时返回默认值而不是报错的 `try_convert()` 函数。 | 1.0 | **2.2 新增** | 默认 |
| udp2 | 重新实现的 UDP Interconnect，与数据库内核分离。 | — | **2.1 新增** | `--enable-ic-udp2` |

## gpcontrib/ 中的模块 {#modules-in-gpcontrib}

| 模块 | 说明 | 版本 | 2.x 变更 | 构建 |
|---|---|---|---|---|
| [diskquota](/cloudberry/reference/modules/diskquota/) | 限制模式、角色和表空间可使用的磁盘空间。 | 2.3 | **2.2 新增** | `--with-diskquota` |
| gp_debug_numsegments | 获取并设置创建新表时默认使用的 Segment 数量。用于开发和测试。 | 1.0 | — | 默认（调试扩展） |
| [gp_distribution_policy](/cloudberry/reference/modules/gp-distribution-policy/) | 检查表中的行是否存储在分布策略预期的 Segment 上。 | 1.0 | — | 默认 |
| [gp_exttable_fdw](/cloudberry/reference/modules/gp-exttable-fdw/) | 实现外部表的外部数据包装器。 | 1.0 | — | 默认 |
| gp_inject_fault | 故障注入框架。用于开发和测试。 | 1.0 | — | 默认（调试扩展） |
| [gp_internal_tools](/cloudberry/reference/modules/gp-internal-tools/) | 用于故障排查的诊断视图和函数。 | 1.0.0 | — | 默认 |
| [gp_legacy_string_agg](/cloudberry/reference/modules/gp-legacy-string-agg/) | 单参数 `string_agg()` 聚合函数。 | 1.0.0 | — | 默认 |
| [gp_relsizes_stats](/cloudberry/reference/modules/gp-relsizes-stats/) | 跟踪表在磁盘上的大小。 | 1.0 | **2.2 新增** | 默认 |
| gp_replica_check | 比较主 Segment 和镜像 Segment。用于开发和测试。 | 0.0.1 | — | 默认（调试扩展） |
| [gp_sparse_vector](/cloudberry/reference/modules/gp-sparse-vector/) | 稀疏向量数据类型及其操作符。 | 1.0.1 | — | 默认 |
| [gp_stats_collector](/cloudberry/reference/modules/gp-stats-collector/) | 收集查询及计划执行指标，并报告给监控代理。 | 1.2 | **2.2 新增** | `--with-gp-stats-collector` |
| [gp_toolkit](/cloudberry/reference/sys-catalogs/gp_toolkit/) | 管理视图和函数。 | 1.7 | **2.0 更新**（1.4 → 1.6），**2.2 更新**（1.6 → 1.7） | 默认 |
| gpcloud | 外部表的 `s3` 协议和 `gpcheckcloud` 工具。参阅[从 Amazon S3 加载数据](/cloudberry/data-loading/cloud/load-data-from-s3/)。 | — | — | `--enable-gpcloud` |
| gpmapreduce | `gpmapreduce` 工具。 | — | — | `--enable-mapreduce` |
| [orafce](/cloudberry/reference/modules/orafce/) | Oracle 兼容函数和包。 | 4.9 | — | `--enable-orafce` |
| pg_hint_plan | 通过 SQL 注释中的提示控制执行计划。参阅[查询计划提示](/cloudberry/performance/optimize-queries/query-hints/)。 | 1.3.9 | **2.0 新增** | 默认 |
| pxf_fdw | 平台扩展框架（PXF）的外部数据包装器。参阅[使用 PXF 加载数据](/cloudberry/data-loading/cloud/load-data-using-pxf/)。 | 1.0 | — | `--enable-pxf`（默认开启） |
| [reject_partition_fullscan](/cloudberry/reference/modules/reject-partition-fullscan/) | 拒绝未做分区剪枝、扫描表所有分区的查询。 | 1.0 | **2.2 新增** | 默认（调试扩展） |
| [yezzey](/cloudberry/reference/modules/yezzey/) | 将 AO 表的数据转存到兼容 S3 的对象存储。源码为 Git 子模块。 | 2.0 | **2.2 新增** | `--with-yezzey` |
| zstd | AO 表的 Zstandard 压缩。 | — | — | `--with-zstd`（默认开启） |

除非向 `configure` 传入 `--disable-debug-extensions`，否则都会构建标记为调试扩展的模块。不要在生产集群中使用 `gp_debug_numsegments`、`gp_inject_fault` 或 `gp_replica_check`。

### 已移除的模块 {#removed-modules}

| 模块 | 说明 | 移除版本 |
|---|---|---|
| quicklz | AO 表的 QuickLZ 压缩。 | 2.1 |
