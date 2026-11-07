---
title: SafeSession
description: pgEdge SafeSession 使用 executor 和 utility 钩子，为指定数据库角色强制执行只读会话。
weight: 40
upstream_source: pgedge-safesession
upstream_link: https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/index.md
upstream_modified: true
upstream_ref: b406cd1e82cf
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
linkTitle: SafeSession
icon: fa-solid fa-book-open
sidebar_root_for: self
no_list: true
type: docs
sidebar_root_menu: false
---


> [!NOTE] 版本说明
> 本文档来自上游 `main` 的固定源码快照；与原站的版本化文档可能存在差异。部署前请核对[版本与来源](/zh/pgedge/about/attribution/)。


pgEdge SafeSession 是一个 PostgreSQL 扩展，可为指定数据库角色强制执行只读会话。它通过 executor 和 utility 钩子提供纵深防御，阻断所有写操作、DDL 以及其他潜在危险命令。

## 功能 {#features}

- 为受限角色阻断 DML（INSERT、UPDATE、DELETE、MERGE）
- 阻断 DDL（CREATE、ALTER、DROP、TRUNCATE 等）
- 阻断 COPY FROM 和 COPY TO PROGRAM
- 阻断 GRANT/REVOKE、VACUUM/ANALYZE
- 阻断 volatile C 语言函数执行（这类函数可能绕过 executor）
- 防止篡改只读 GUC 设置
- 角色成员继承：受限角色的成员同样受限
- 超级用户豁免：超级用户即使属于受限角色也永不受限
- 以 session user 为锚点：SET ROLE 无法摆脱限制
- 通过 GUC 配置保护层

## 要求 {#requirements}

- PostgreSQL 14 或更新版本
- 必须通过 `shared_preload_libraries` 加载

## 安装 {#installation}

### 从源码构建 {#build-from-source}

```bash
make
make install
```

### 配置 PostgreSQL {#configure-postgresql}

将扩展加入 `shared_preload_libraries`，该设置位于 `postgresql.conf`：

```
shared_preload_libraries = 'pgedge_safesession'
```

重启 PostgreSQL 使更改生效。

### 创建扩展（可选） {#create-the-extension-optional}

扩展通过 `shared_preload_libraries` 加载后即已完全可用。运行 `CREATE EXTENSION` 是可选的，但它会在 `pg_extension` catalog 中注册扩展，使其出现在 `\dx` 输出中：

```sql
CREATE EXTENSION pgedge_safesession;
```

## 配置 {#configuration}

所有 GUC 都是 SUSET 参数（只有超级用户可以修改）。

### `pgedge_safesession.roles` {#pgedge_safesessionroles}

以逗号分隔的 PostgreSQL 角色名列表，这些角色的会话将被限制为只读操作。

```sql
ALTER SYSTEM SET pgedge_safesession.roles =
    'readonly_user, reporting_role';
SELECT pg_reload_conf();
```

任何以这些角色之一认证的会话，或以属于其中某个角色的身份认证的会话，都会被限制为只读操作。

### `pgedge_safesession.block_dml` {#pgedge_safesessionblock_dml}

默认值：`on`

为受限角色阻断 INSERT、UPDATE、DELETE 和 MERGE。

### `pgedge_safesession.block_ddl` {#pgedge_safesessionblock_ddl}

默认值：`on`

为受限角色阻断 DDL 和其他 utility 命令。它采用白名单方式：只有显式允许的语句（SELECT、EXPLAIN、事务控制、SET、SHOW、LISTEN/NOTIFY、游标、DO block）可以执行。

### `pgedge_safesession.block_c_functions` {#pgedge_safesessionblock_c_functions}

默认值：`on`

为受限角色阻断 C 语言函数执行。默认情况下，只有 **volatile** C 函数会被阻断。IMMUTABLE 和 STABLE C 函数（例如 PostGIS 几何运算或 pgvector 距离运算符）允许执行，因为它们承诺没有副作用。

### `pgedge_safesession.block_all_c_functions` {#pgedge_safesessionblock_all_c_functions}

默认值：`off`

启用后，无论 volatility 如何，都阻断**所有** C 语言函数。这会提供更严格的保护，但代价是阻断只读扩展函数。仅在 `block_c_functions` 开启时适用。

## 被阻断的内容 {#what-is-blocked}

对于受限会话（且所有保护均启用），以下操作会被阻断：

- **DML**：INSERT、UPDATE、DELETE、MERGE（PostgreSQL 15+），包括修改数据的 CTE（`WITH c AS (INSERT ... RETURNING ...) ...`）
- **DDL**：CREATE、ALTER、DROP、TRUNCATE 以及所有其他 schema 修改命令
- **COPY FROM**：数据导入（COPY TO 允许）
- **COPY TO PROGRAM**：通过 COPY 执行程序
- **CREATE TABLE AS / SELECT INTO**：从查询创建表，包括它们的 `EXPLAIN ANALYZE` 形式
- **写语句的 EXPLAIN ANALYZE**：它会执行语句，因此被视为写
- **GRANT / REVOKE**：权限修改
- **VACUUM / ANALYZE**：维护命令
- **CHECKPOINT**：强制产生大量 I/O 并发出 WAL
- **两阶段提交**：PREPARE TRANSACTION、COMMIT PREPARED、ROLLBACK PREPARED
- **有副作用函数**：非受信语言（C、internal，或 `plpython3u` 等非受信 PL）中的 volatile 函数，以及任何不在一个小型“确认无可观察副作用内建函数”允许列表中的 volatile 内建（`pg_catalog`）函数（`random()`、`clock_timestamp()` 等）。volatile 内建函数默认阻断；只有确认无害的函数才豁免，因此新增副作用内建函数的新 PostgreSQL 版本会自动阻断。非受信语言中的 `DO` block 或 `CALL` 出于同样原因被阻断。参数也计入语句的一部分，因此无论被阻断函数是直接调用、作为 `CALL` 参数传入，还是作为 `EXECUTE` 参数传入（包括通过 `EXPLAIN EXECUTE` 和 `CREATE TABLE AS ... EXECUTE`），都会被拒绝。仅通过视图体、行级安全策略的 `USING`/`WITH CHECK` qual，或 domain `CHECK` 约束间接触达的函数，也会像直接调用一样被拒绝。对 domain 而言，无论通过何种方式触达运行该约束的类型转换，该规则都成立：cast、预编译语句声明的参数类型、通过 extended query protocol 绑定的参数、PL/pgSQL 变量声明的类型，或函数的 `RETURNS` 类型。
- **Fast-path 函数调用**：libpq `PQfn` 背后的协议，大对象客户端 API 建立在其上。它完全绕过解析器和 planner，因此同一函数策略会直接应用于它。
- **排他锁**：模式高于 ROW SHARE 的 LOCK TABLE
- **GUC 篡改**：任何放宽 `transaction_read_only` 或 `default_transaction_read_only` 的尝试，无论是将它们设为假值、通过 RESET 或 SET TO DEFAULT，还是通过 SET TRANSACTION READ WRITE 与 SET SESSION CHARACTERISTICS AS TRANSACTION READ WRITE

## 允许的内容 {#what-is-allowed}

- **SELECT**：所有只读查询，包括使用 WHERE 子句、聚合函数和内建函数的查询
- **EXPLAIN**：查询计划。普通 EXPLAIN 只生成计划，始终允许；只有当被执行语句不写时，才允许 EXPLAIN ANALYZE。
- **事务控制**：BEGIN、COMMIT、ROLLBACK、SAVEPOINT
- **SET / RESET**：修改非受保护 GUC（例如 work_mem）
- **SET TRANSACTION**：ISOLATION LEVEL 和 READ ONLY（收紧事务限制允许）
- **声明只读**：将 `transaction_read_only` 或 `default_transaction_read_only` 设为 on，即请求已经强制执行的状态。因此，在每个新建连接上都声明只读的客户端（例如禁用写入的连接池）可以与受限角色配合工作。
- **SHOW**：显示设置
- **LISTEN / NOTIFY**：通知通道
- **游标**：DECLARE、FETCH、CLOSE
- **连接池 reset**：DISCARD ALL、DISCARD PLANS、RESET ALL（它们无法放宽限制，因为限制会按语句重新断言）
- **DO block 和 CALL**：受信语言（PL/pgSQL、SQL 等）中允许；内部任何写入都会被 executor 钩子捕获
- **PL/pgSQL 和 SQL 函数**：只读函数正常执行；函数内部的任何写尝试都会被 executor 钩子捕获，SQL 函数体中调用被阻断函数时，会在调用运行前被拒绝
- **IMMUTABLE/STABLE 函数**，以及 `random()` 和 `clock_timestamp()` 等无害 volatile 内建函数

## 安全模型 {#security-model}

### Session user 是锚点 {#session-user-is-the-anchor}

连接时设置的 session user 身份是主要检查对象。即使受限用户执行 `SET ROLE` 切换到另一个角色，session user 仍保持受限。这可防止通过角色切换绕过限制。

### 超级用户豁免 {#superuser-exemption}

超级用户即使属于受限角色也永不受限。超级用户检查基于 session user，因此在受限会话中调用超级用户拥有的 SECURITY DEFINER 函数也无法绕过限制。

### SECURITY DEFINER 函数 {#security-definer-functions}

SECURITY DEFINER 函数会临时将 effective user 更改为函数 owner。但 SafeSession 检查的是 session user，而不是 effective user。这意味着受限会话不能利用特权用户拥有的 SECURITY DEFINER 函数执行写操作。

### 角色成员继承 {#role-membership-inheritance}

如果角色 `app_reader` 列在 `pgedge_safesession.roles` 中，那么任何属于 `app_reader` 的角色也受限。成员关系使用 PostgreSQL 的 `is_member_of_role_nosuper()` 测试，因此只遵循实际授权。

这个区别很重要，因为 PostgreSQL 在权限测试之外会把超级用户报告为数据库中每个角色的成员，背后并没有授权；这对权限测试是正确答案，在这里不是。任何在 session user 不是超级用户时短暂把当前用户变成超级用户的机制，例如超级用户拥有的 SECURITY DEFINER 函数，或像 supautils 这样为单条命令提升特权角色的扩展，否则都会表现为充当每个受限角色的成员并被阻断。强制执行仍以 session user 为锚点，因此这种提升也不能摆脱限制：受限会话在超级用户拥有的 SECURITY DEFINER 函数内部仍受限。

### 限制变更与缓存计划 {#restriction-changes-and-cached-plans}

有副作用的函数调用会在语句或表达式被解析时检测，并在它被规划时再次检测（用于捕获仅通过视图体或 RLS qual 触达的函数；它们在查询重写阶段、解析分析之后替换），而不是在执行时检测。因此，会话受限前缓存的计划如果不重新检查，就可能被重放。这很重要，因为会话可能在生命周期中途变为受限：角色列表可以编辑并重载配置，或角色在会话仍打开时被授予受限角色成员身份。

因此，变为受限会作为失效事件处理，会话的缓存计划会像执行 `DISCARD PLANS` 一样被丢弃，使所有内容在新状态下重新分析。这同时覆盖预编译语句和 PL/pgSQL 为表达式缓存的计划。会话受限期间构建的计划在限制解除后保持不变，因为它们已经被检查过。

### 双重保险 {#belt-and-suspenders}

对每个受限会话，SafeSession 还会强制当前事务只读（`XactReadOnly`），并在每条语句上重新断言。这提供了一层无法关闭的额外保护：即使某些内容绕过钩子并尝试直接写 heap，PostgreSQL 自身的内部只读检查也会捕获它。该设置的应用不会写入任何会话级 GUC，因此不会留下状态，也不会干扰连接池。

## 已知限制 {#known-limitations}

- 无害 volatile 内建函数允许列表刻意保守而非完备：实际无害但不在列表中的 volatile 内建函数仍会被阻断，这可能表现为受限会话被拒绝调用一个只读内建函数，而未来版本应把它加入列表。这是偏向失败关闭的可用性取舍：新增副作用内建函数默认被阻断，而不是被静默允许。受信语言中的 volatile 函数允许运行，其任何写操作会在执行时被捕获。
- 强制执行以 session user 为锚点。超级用户仍可使用 `SET SESSION AUTHORIZATION` 变成受限角色（这正是进入限制的方式）；这是设计行为，不是绕过。
- 角色列表必须从服务器配置设置（需要 `shared_preload_libraries`，角色通常在 `postgresql.conf` 中设置，或使用 `ALTER SYSTEM`）。如果只在单个会话中用 `SET` 设置，会话的 `DISCARD
  ALL` 或 `RESET ALL` 会撤销它。
- SafeSession 和 Spock 都会安装 executor、utility 和 planner 钩子。它们可以正确链接，但同时部署时，二者交互尚未经过穷尽测试。
- 被阻断函数会在出现在语句解析树中时，或 executor 将其编译为表达式的一部分时被捕获。PostgreSQL 直接通过 `fmgr` 调用、且没有围绕它编译表达式的函数两者都看不到：实际中出现的情形是类型自身的输入/输出函数，以及索引访问方法的 support 函数。触达它们需要别人定义的类型或 operator class，因为受限角色不能创建这两者。

## 示例 {#example}

```sql
-- As superuser: configure restrictions
ALTER SYSTEM SET pgedge_safesession.roles =
    'reporting_user';
SELECT pg_reload_conf();

-- Connect as reporting_user
-- Reads work normally:
SELECT * FROM sales;          -- OK
SELECT count(*) FROM sales;   -- OK
EXPLAIN SELECT * FROM sales;  -- OK
COPY sales TO '/tmp/out.csv'; -- OK

-- Writes are blocked:
INSERT INTO sales VALUES (1); -- ERROR
CREATE TABLE tmp (id int);    -- ERROR
COPY sales FROM '/tmp/in.csv'; -- ERROR
```

## 许可证 {#licence}

详情见[许可证](/pgedge/safesession/licence/)页面。

## 继续阅读 {#continue-reading}

- [LICENCE（英文）](/pgedge/safesession/licence/)
- [pgEdge SafeSession 变更日志](/zh/pgedge/safesession/changelog/)

---

[上游原文](https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/index.md) · `b406cd1e82cf` · Copyright (c) 2025–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
