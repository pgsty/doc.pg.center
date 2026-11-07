---
title: 源码结构
linkTitle: 源码结构
description: 了解 OrioleDB 的源码布局、构建目标、测试、CI 和停止事件。
weight: 10
type: docs
search_keywords: ["OrioleDB", "code structure"]
upstream_link: https://www.orioledb.com/docs/contributing/code-structure
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-folder-tree
---


OrioleDB 源码包含 CI/CD 工作流、文档、测试和 C 源文件，便于扩展的开发、测试（包括 Valgrind 测试）与部署。停止事件和 CI 工作流尤其重视并发测试与性能分析。

## 文件结构 {#file-structure}

``` sql
orioledb
|- .github
|  |- workflows -- GitHub workflows
|
|- ci  -- scripts for building, testing, and CI automation
|- doc -- documentation
|- docker
|  |- tests -- Docker images tests
|  |- Dockerfile -- Alpine based Dockerfile used within docker.yml and dockertest.yml workflows
|  |- Dockerfile.ubuntu -- Ubuntu based Dockerfile used within docker.yml and dockertest.yml workflows
|  |- README.md -- Docker images tests documentation
|  |- docker-entrypoint.sh -- entrypoint file for Docker images
|  |- orioledb-config.sh -- Docker images tests configuration
|  |- postgresql.docker.conf -- configuration file used by Docker images
|- include -- C-headers of extension
|- perf -- performance benchmarks
|- sql -- installation scripts with definitions of the extension's SQL-level objects
|- src -- C-sources of extension
|- test
|  |- expected -- expected output for regression and isolation tests
|  |- integration -- integration tests
|  |- specs -- isolation tests
|  |- sql -- regression tests
|  |- t -- python tests
|  |- orioledb_isolation.conf -- configuration file used during isolation tests
|  |- orioledb_regression.conf -- configuration file used during regression tests
|- Makefile -- defines make targets
|- README.md -- main documentation entrypoint
|- orioledb.control -- extension control file
|- stopevents.txt -- list of "stop event"
|- stopevents_gen.py -- generates include/utils/stopevents_(defs|data).h from stopevents.txt
|- typedefs_gen.py -- generates list of C-symbols in orioledb.so to orioledb.typedefs
|- valgrind.supp -- suppression rules for valgrind checks
```

## Makefile 目标 {#makefile-targets}

所有测试目标都接受 `VALGRIND=1`，用于在 [Valgrind](https://valgrind.org/) 下运行。Valgrind 会让测试慢约 100 倍，但能检测未初始化内存访问。这种极慢执行还有一个好处：改变时序，从而暴露各类并发错误。

- `regresscheck`：运行 SQL 测试，见下文。
- `isolationcheck`：运行隔离测试。
- `testgrescheck`：运行 testgres 测试。
- `testgrescheck_part_1`：运行前半部分 testgres 测试。测试分为两组规模近似的部分，以免单次 CI 运行过长。
- `testgrescheck_part_2`：运行后半部分 testgres 测试。
- `installcheck`：通过 PostgreSQL 扩展系统安装时（`USE_PGXS=1`），运行全部测试。
- `check`：从 PostgreSQL 源码的 `contrib` 目录安装时，运行全部测试。
- `pgindent`：自动整理 OrioleDB 源码缩进。[pgindent](https://github.com/postgres/postgres/blob/master/src/tools/pgindent/pgindent) 必须位于 `$PATH` 中，并需先安装 [pg_bsd_indent](https://github.com/postgres/postgres/blob/master/src/tools/pg_bsd_indent/README#L17)。此外，GNU Objdump 应以 `objdump` 或 `gobjdump` 的名称位于 `$PATH` 中，或通过 `OBJDUMP` 环境变量指定。

## 扩展 SQL 脚本 {#extension-sql-scripts}

OrioleDB 扩展使用一个基础版本安装脚本，再配合各小版本升级脚本。例如，安装 `1.7` 时，PostgreSQL 先应用 `1.0` 脚本，再依次运行从 `1.0` 到 `1.7` 的所有升级脚本。

提升扩展版本，例如从 `1.6` 到 `1.7`，需执行以下步骤：

1. 将 `orioledb.control` 的 `default_version` 改为新版本。
2. 在 `sql` 目录手动创建开发与生产升级脚本：
   - `./sql/orioledb--1.6--1.7_prod.sql`
   - `./sql/orioledb--1.6--1.7_dev.sql`
3. 添加对应脚本头并填写变更：
   - **仅限**开发环境的变更，例如不应向生产系统暴露的测试函数，放入 `_dev.sql`。
   - 所有常规变更放入 `_prod.sql`。

> [!NOTE]
>
> 构建系统 `make` 使用两个文件自动生成最终的 `./sql/orioledb--1.6--1.7.sql`，无需手动创建。仅在构建时指定 `IS_DEV` 才会纳入 `_dev.sql` 的内容，不必在两个文件中重复变更。

4. 将生成的 `./sql/orioledb--1.6--1.7.sql` 加入 `.gitignore` 和 `.dockerignore`。

## 测试 {#tests}

OrioleDB 有三组测试。

- SQL 测试位于 `test/sql`，是最简单的测试。将 SQL 文件交给 `psql`，把结果与 `test/expected` 中的参考输出比较。一个输入文件可能有多个参考输出。例如，`collate.sql` 包含排序规则相关测试，根据数据库编码和是否有 libicu，结果可能匹配 `collate.out`、`collate_1.out` 或 `collate_2.out`。

- 隔离测试位于 `specs`，模拟多个连接同时运行。详见 PostgreSQL 源码中的 [README](https://github.com/postgres/postgres/blob/master/src/test/isolation/README)。与停止事件配合时，这类测试尤其有效。

- Python [testgres](https://pypi.org/project/testgres/) 测试位于 `t`，功能最强、也最复杂。除了模拟多个并发连接，还能对整个 PostgreSQL 实例执行启动、停止、备份、复制等操作，详见 [testgres 文档](https://postgrespro.github.io/testgres/)。

> [!NOTE]
>
> 测试文件名应以 `_test.py` 结尾，才能正确纳入测试套件。

## CI {#ci}

OrioleDB 使用 GitHub CI，工作流如下。

### `check.yml` {#checkyml}

针对 gcc 和 clang 两种编译器，以及支持的 PostgreSQL 大版本 16 和 17，运行以下测试。

- `normal`：不启用断言和调试符号。
- `debug`：启用断言和调试符号。
- `sanitize`：启用断言、调试符号、对齐及其他 sanitizer 检查。这替代了在严格对齐架构上测试，甚至更严格。例如，访问未正确对齐的结构体中一个自身已正确对齐的成员也会触发错误，而真实硬件未必如此。
- `check_page`：启用断言、调试符号和 `CHECK_PAGE_STRUCT` 宏，每次解锁页面时检查页面结构。
- `valgrind_1`：启用断言和调试符号，在 Valgrind 下运行 `regresscheck`、`isolationcheck`、`testgrescheck_part_1`。
- `valgrind_2`：启用断言和调试符号，在 Valgrind 下运行 `testgrescheck_part_2`。
- `static`：对源码运行 `clang-analyzer` 或 `cppcheck`。

### `docker.yml` {#dockeryml}

在 Alpine 和 Ubuntu Linux 下，为 amd64 和 arm64v8 构建 Docker 镜像。其 Dockerfile 由 [PostgreSQL Dockerfile](https://github.com/docker-library/postgres) 略作调整而来，详见[我们的 Docker Hub](https://hub.docker.com/r/orioledb/orioledb)。

### `dockertest.yml` {#dockertestyml}

测试 Docker 镜像，每次推送和拉取请求都会运行。

### `pgindent.yml` {#pgindentyml}

使用 `pgindent` 检查代码格式，每次推送和拉取请求都会运行。

### `rpm.yml` {#rpmyml}

使用 [orioledb/pgrpms](https://github.com/orioledb/pgrpms) 仓库的 spec 为 CentOS 7 构建 RPM 包。该仓库 fork 自 [pgrpms](https://git.postgresql.org/gitweb/?p=pgrpms.git;a=summary)。

### `static.yml` {#staticyml}

执行代码静态分析，每次推送和拉取请求都会运行。

## 停止事件 {#stop-events}

停止事件是代码中可根据特定条件暂停执行的位置，用于可靠复现并发问题。OrioleDB 的隔离测试和 testgres 测试都使用它。

每个停止事件暴露一组封装为 jsonb 值的参数，使用 SQL/JSON path 语言定义参数条件。

SQL 层提供以下函数和变量：

- `orioledb.enable_stopevents`：为进程启用停止事件检查。检查开销较大，会明显影响性能，因此默认禁用。

- `orioledb.trace_stopevents`：记录所有停止事件，默认禁用。

- `pg_stopevent_set(eventname text, condition jsonpath) RETURNS void`：设置停止事件条件。执行后，所有触发该事件且参数满足 jsonpath 条件的进程都会暂停。

- `pg_stopevent_reset(eventname text) RETURNS bool`：重置停止事件。此前因该事件暂停的所有进程恢复执行。

- `pg_stopevents(OUT stopevent text, OUT condition jsonpath, OUT waiter_pids int[]) RETURNS SETOF record`：返回当前设置的所有停止事件、条件和等待进程 PID。

C 层提供以下宏：

- `STOPEVENTS_ENABLED()`：检查是否启用停止事件。
- `STOPEVENT(event_id, params)`：使用给定 jsonb 参数触发指定停止事件。
- `STOPEVENT_CONDITION(event_id, params)`：只检查条件，不暂停执行，用于模拟错误。

事件列表定义在 `stopevents.txt`。`stopevents_gen.py` 生成包含 C 定义的 `include/utils/stopevents_defs.h`（宏）和 `include/utils/stopevents_data.h`（名称字符串）。
