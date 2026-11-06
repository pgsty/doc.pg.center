---
title: "编写外部数据包装器"
description: "本指南介绍如何为 Apache Cloudberry 编写新的外部数据包装器（FDW）。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/write-a-foreign-data-wrapper.md"
---

外部数据包装器是一个由一组函数组成的库，Apache Cloudberry 服务器通过调用这些函数访问外部数据源。FDW 负责从远程数据存储获取数据，并将其返回给 Apache Cloudberry 执行器。

FDW 使 Apache Cloudberry 能够将外部数据源视为普通数据库表，从而可以使用标准 SQL 查询外部数据。

## 开始之前 {#before-you-begin}

### 要求 {#requirements}

使用 Apache Cloudberry 外部数据包装器 API 开发时：

- 开发系统必须具有与 Apache Cloudberry 主机相同的硬件和软件架构。
- 代码必须使用 C 等编译型语言，并使用版本 1 接口。
- 对象文件中的符号名称不能与彼此或 Apache Cloudberry 服务器中定义的符号冲突。
- 应熟悉 [使用外表访问外部数据](/cloudberry/reference/sql-stmts/create-foreign-table/)中介绍的外表概念。

### 头文件 {#header-files}

用于 FDW 开发的 Apache Cloudberry 头文件位于 `$GPHOME/include/postgresql/server/`：

- `foreign/fdwapi.h`：FDW API 结构和回调函数签名
- `foreign/foreign.h`：外部数据包装器辅助结构和函数
- `catalog/pg_foreign_table.h`：外表定义
- `catalog/pg_foreign_server.h`：外部服务器定义

## FDW 架构 {#fdw-architecture}

FDW 包含两个主要组件：

1. 处理器函数，返回一个包含函数指针的结构体，其中包含 Apache Cloudberry 与外部数据源交互所需的全部回调函数。
2. 可选的验证器函数，用于验证在外部数据包装器、服务器、用户映射和外表的 `CREATE` 与 `ALTER` 命令中提供的配置选项。

### 处理器函数 {#handler-function}

处理器函数可由 SQL 调用，并返回一个包含回调函数指针的结构体：

```c
CREATE FUNCTION my_fdw_handler()
  RETURNS fdw_handler
  AS 'MODULE_PATHNAME'
LANGUAGE C STRICT;
```

### 验证器函数 {#validator-function}

验证器函数验证 FDW 对象的选项：

```c
CREATE FUNCTION my_fdw_validator(text[], oid)
  RETURNS void
  AS 'MODULE_PATHNAME'
LANGUAGE C STRICT;
```

## 回调函数 {#callback-functions}

FDW API 定义了 Apache Cloudberry 在扫描和更新外表时调用的回调函数。处理器函数返回一个 `FdwRoutine` 结构体，其中包含指向这些函数的指针。

### 必需的扫描相关回调函数 {#required-scan-related-callbacks}

所有 FDW 都必须实现以下函数：

#### GetForeignRelSize {#getforeignrelsize}

```c
void GetForeignRelSize(PlannerInfo *root,
                       RelOptInfo *baserel,
                       Oid foreigntableid)
```

获取外表的关系大小估计值。在规划开始时调用。

#### GetForeignPaths {#getforeignpaths}

```c
void GetForeignPaths(PlannerInfo *root,
                     RelOptInfo *baserel,
                     Oid foreigntableid)
```

为外表扫描创建可能的访问路径。必须调用 `create_foreignscan_path()` 以确保与 Apache Cloudberry 兼容。

#### GetForeignPlan {#getforeignplan}

```c
ForeignScan *GetForeignPlan(PlannerInfo *root,
                            RelOptInfo *baserel,
                            Oid foreigntableid,
                            ForeignPath *best_path,
                            List *tlist,
                            List *scan_clauses)
```

从选定的外部访问路径创建 ForeignScan 计划节点。

#### BeginForeignScan {#beginforeignscan}

```c
void BeginForeignScan(ForeignScanState *node,
                      int eflags)
```

开始执行外部扫描。在执行器启动期间调用。

#### IterateForeignScan {#iterateforeignscan}

```c
TupleTableSlot *IterateForeignScan(ForeignScanState *node)
```

从外部数据源获取一行数据。没有更多行可用时返回 NULL。

#### ReScanForeignScan {#rescanforeignscan}

```c
void ReScanForeignScan(ForeignScanState *node)
```

从头开始重新扫描。

#### EndForeignScan {#endforeignscan}

```c
void EndForeignScan(ForeignScanState *node)
```

结束扫描并释放资源。

### 可选的更新相关回调函数 {#optional-update-related-callbacks}

如果 FDW 支持写操作，请实现以下函数：

#### ExecForeignInsert {#execforeigninsert}

```c
TupleTableSlot *ExecForeignInsert(EState *estate,
                                  ResultRelInfo *rinfo,
                                  TupleTableSlot *slot,
                                  TupleTableSlot *planSlot)
```

向外表插入单个元组。

#### ExecForeignUpdate {#execforeignupdate}

```c
TupleTableSlot *ExecForeignUpdate(EState *estate,
                                  ResultRelInfo *rinfo,
                                  TupleTableSlot *slot,
                                  TupleTableSlot *planSlot)
```

更新外表中的单个元组。

#### ExecForeignDelete {#execforeigndelete}

```c
TupleTableSlot *ExecForeignDelete(EState *estate,
                                  ResultRelInfo *rinfo,
                                  TupleTableSlot *slot,
                                  TupleTableSlot *planSlot)
```

从外表删除单个元组。

## Apache Cloudberry 注意事项 {#apache-cloudberry-considerations}

### mpp_execute 选项 {#the-mpp_execute-option}

Apache Cloudberry 通过 `mpp_execute` 选项支持并行执行。FDW 应处理此选项，以确定在哪里请求或发送数据：

```c
ForeignTable *table = GetForeignTable(foreigntableid);
if (table->exec_location == FTEXECLOCATION_ALL_SEGMENTS)
{
    // Execute on all segments in parallel
}
else if (table->exec_location == FTEXECLOCATION_ANY)
{
    // Execute on coordinator or any one segment
}
else if (table->exec_location == FTEXECLOCATION_COORDINATOR)
{
    // Execute on coordinator only (default)
}
```

### Segment 标识 {#segment-identification}

对于并行执行（`mpp_execute 'all segments'`），每个 Segment 都必须确定由自己负责的数据部分：

```c
int segmentNumber = GpIdentity.segindex;
int totalNumberOfSegments = getgpsegmentCount();
```

### 并行写操作 {#parallel-write-operations}

只有将 `mpp_execute` 设置为 `'all segments'` 时，Apache Cloudberry 才支持并行写操作。对于其他设置，写操作会通过 Coordinator 发起。

## FDW 实现示例 {#example-fdw-implementation}

以下是 FDW 的基本框架：

```c
#include "postgres.h"
#include "foreign/fdwapi.h"
#include "foreign/foreign.h"

PG_MODULE_MAGIC;

// Function declarations
extern Datum my_fdw_handler(PG_FUNCTION_ARGS);
extern Datum my_fdw_validator(PG_FUNCTION_ARGS);

// FDW callback functions
static void myGetForeignRelSize(PlannerInfo *root,
                                RelOptInfo *baserel,
                                Oid foreigntableid);
static void myGetForeignPaths(PlannerInfo *root,
                              RelOptInfo *baserel,
                              Oid foreigntableid);
// ... other callback functions

PG_FUNCTION_INFO_V1(my_fdw_handler);
Datum
my_fdw_handler(PG_FUNCTION_ARGS)
{
    FdwRoutine *fdwroutine = makeNode(FdwRoutine);

    // Required scan functions
    fdwroutine->GetForeignRelSize = myGetForeignRelSize;
    fdwroutine->GetForeignPaths = myGetForeignPaths;
    fdwroutine->GetForeignPlan = myGetForeignPlan;
    fdwroutine->BeginForeignScan = myBeginForeignScan;
    fdwroutine->IterateForeignScan = myIterateForeignScan;
    fdwroutine->ReScanForeignScan = myReScanForeignScan;
    fdwroutine->EndForeignScan = myEndForeignScan;

    // Optional write functions
    fdwroutine->ExecForeignInsert = myExecForeignInsert;
    fdwroutine->ExecForeignUpdate = myExecForeignUpdate;
    fdwroutine->ExecForeignDelete = myExecForeignDelete;

    PG_RETURN_POINTER(fdwroutine);
}

PG_FUNCTION_INFO_V1(my_fdw_validator);
Datum
my_fdw_validator(PG_FUNCTION_ARGS)
{
    List *options_list = untransformRelOptions(PG_GETARG_DATUM(0));
    Oid catalog = PG_GETARG_OID(1);
    
    // Validate options based on catalog type
    // Implementation depends on your FDW's specific options
    
    PG_RETURN_VOID();
}
```

## 构建和打包 {#building-and-packaging}

### 使用 PGXS {#using-pgxs}

使用 PostgreSQL 扩展构建基础设施创建 Makefile：

```makefile
MODULE_big = my_fdw
OBJS = my_fdw.o

PG_CONFIG = pg_config
PGXS := $(shell $(PG_CONFIG) --pgxs)

PG_CPPFLAGS = -I$(shell $(PG_CONFIG) --includedir)
SHLIB_LINK = -L$(shell $(PG_CONFIG) --libdir)
include $(PGXS)
```

### 创建扩展 {#creating-an-extension}

创建 SQL 脚本文件（`my_fdw--1.0.sql`）：

```sql
CREATE FUNCTION my_fdw_handler()
  RETURNS fdw_handler
  AS 'MODULE_PATHNAME'
LANGUAGE C STRICT;

CREATE FUNCTION my_fdw_validator(text[], oid)
  RETURNS void
  AS 'MODULE_PATHNAME'
LANGUAGE C STRICT;

CREATE FOREIGN DATA WRAPPER my_fdw
  HANDLER my_fdw_handler
  VALIDATOR my_fdw_validator;
```

创建控制文件（`my_fdw.control`）：

```ini
# my_fdw extension
comment = 'My custom foreign data wrapper'
default_version = '1.0'
module_pathname = '$libdir/my_fdw'
relocatable = true
```

更新扩展的 Makefile：

```makefile
EXTENSION = my_fdw
DATA = my_fdw--1.0.sql
```

## 部署 {#deployment}

对于 Apache Cloudberry 集群：

1. 将共享库安装到所有主机上的 `$GPHOME/lib/postgresql/`。
2. 将扩展文件安装到所有主机上的 `$GPHOME/share/postgresql/extension/`。
3. 设置权限，使 `gpadmin` 用户能够访问所有文件。
4. 在所有主机上安装，包括 Coordinator 和所有 Segment 主机。

## 测试 FDW {#testing-your-fdw}

### 基本功能测试 {#basic-functionality-test}

```sql
-- Create extension
CREATE EXTENSION my_fdw;

-- Create foreign server
CREATE SERVER my_server
    FOREIGN DATA WRAPPER my_fdw
    OPTIONS (host 'remote-host', port '5432');

-- Create user mapping
CREATE USER MAPPING FOR current_user
    SERVER my_server
    OPTIONS (user 'remote_user', password 'remote_password');

-- Create foreign table
CREATE FOREIGN TABLE my_foreign_table (
    id integer,
    name text
) SERVER my_server
OPTIONS (table_name 'remote_table');

-- Test query
SELECT * FROM my_foreign_table LIMIT 5;
```

### 并行执行测试 {#parallel-execution-test}

```sql
-- Test parallel execution
CREATE FOREIGN TABLE parallel_test (
    id integer,
    data text
) SERVER my_server
OPTIONS (
    table_name 'large_table',
    mpp_execute 'all segments'
);

SELECT count(*) FROM parallel_test;
```

## 最佳实践 {#best-practices}

- 在 FDW 代码中实现全面的错误处理，确保正确报告所有失败情况，并向用户提供清晰、可操作的错误消息。
- 正确使用 PostgreSQL 内存上下文，防止内存泄漏，并确保查询被取消或遇到错误时能正确清理。
- 设计 FDW 以高效处理批量数据操作，并在适当情况下利用 Apache Cloudberry 的并行处理能力。
- 验证所有用户输入和配置参数，实现安全的身份验证机制，并遵循外部数据访问的安全最佳实践。
- 创建完整的文档，说明所有配置选项、连接参数，以及管理员和开发者的使用示例。
- 创建全面的测试套件，覆盖不同外部数据源中的各种数据类型、边界情况、错误条件和性能场景。

## 调试 {#debugging}

### 启用详细日志 {#enable-verbose-logging}

在 postgresql.conf 中设置：
```ini
log_min_messages = DEBUG1
```

### 使用 elog 调试 {#use-elog-for-debugging}

```c
elog(DEBUG1, "FDW: Processing %d rows", row_count);
elog(WARNING, "FDW: Connection failed, retrying...");
```

### 常见问题 {#common-issues}

1. 段错误经常由不正确的内存管理导致，例如访问已释放的内存或 C 代码中的缓冲区溢出。
2. 多个扩展定义同名函数时可能出现符号名称冲突；请确保所有函数名称唯一，并使用适当的命名空间。
3. 并行执行问题通常很难调试；启用多 Segment 并行处理之前，先使用单 Segment 配置进行测试。
4. 数据转换或网络操作中可能出现性能瓶颈；使用性能分析工具识别并优化关键代码路径。

## 了解更多 {#learn-more}

- [外部数据包装器辅助函数](https://www.postgresql.org/docs/12/fdw-helpers.html)
- [外部数据包装器回调例程](https://www.postgresql.org/docs/12/fdw-callbacks.html)
