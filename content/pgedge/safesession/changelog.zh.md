---
title: pgEdge SafeSession 变更日志
description: 记录 pgEdge SafeSession 1.0 与 1.0-beta1 的新增、变更和修复。
weight: 200
upstream_source: pgedge-safesession
upstream_link: https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/changelog.md
upstream_modified: true
upstream_ref: b406cd1e82cf
source_kind: pinned-main-snapshot
translation_status: machine-draft
translation_notice: en
translator: PGSTY 社区
type: docs
---



pgEdge SafeSession 的所有重要变更都会记录在这个文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，
本项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [1.0] - 2026-08-25 {#10---2026-08-25}

### 新增 {#added}

- `SECURITY.md`，说明如何报告漏洞

## [1.0-beta1] - 2026-08-21 {#10-beta1---2026-08-21}

### 新增 {#added-1}

- pgEdge SafeSession 初始版本
- GUC `pgedge_safesession.roles`（SUSET），用于指定受限角色
- ExecutorStart 钩子，用于阻断 DML（INSERT、UPDATE、DELETE、
  MERGE）和 C 语言函数执行
- ProcessUtility 钩子，用于阻断 DDL、COPY FROM、GRANT/REVOKE、
  VACUUM/ANALYZE、排他锁和 GUC 篡改
- 以 session user 为锚点的角色检查：SET ROLE 无法摆脱限制
- 超级用户豁免：超级用户永不受限
- 通过 `is_member_of_role()` 实现角色成员继承
- 双重保险：为受限会话自动设置
  `default_transaction_read_only = on`
- 防止绕过 SECURITY DEFINER：无论 effective user 是谁，始终检查
  session user
- 全面回归测试套件，覆盖：

    - 基础 DML 阻断
    - 防止 SET ROLE 绕过
    - PL/pgSQL 和 SQL 函数强制执行
    - DDL 阻断
    - COPY FROM/TO 处理
    - 阻断 CREATE TABLE AS / SELECT INTO
    - SECURITY DEFINER 函数强制执行
    - 角色成员继承和超级用户豁免
- 通过新的 SUSET GUC 配置保护层：

    - `block_dml`：切换 DML 阻断（默认：on）
    - `block_ddl`：切换 DDL 阻断（默认：on）
    - `block_c_functions`：切换 C 语言函数
      阻断（默认：on）
    - `block_all_c_functions`：无论 volatility 如何，
      阻断所有 C 函数（默认：off）

- 为受限会话阻断 COPY TO PROGRAM
- 为受限会话阻断 SET TRANSACTION READ WRITE
- 针对高级攻击路径的新回归测试
  （PREPARE/EXECUTE、DO block、聚合、WHERE 子句、
  SET TRANSACTION）
- 针对 GUC 切换行为的新回归测试

### 变更 {#changed}

- C 语言函数阻断现在默认只阻断 VOLATILE
  C 函数。IMMUTABLE 和 STABLE C 函数
  （例如 PostGIS 几何运算、pgvector 距离
  运算符）允许执行。使用 `block_all_c_functions = on`
  可恢复之前阻断所有 C 函数的行为。
- 内建函数阻断现在默认拒绝任何 VOLATILE
  内建函数，只允许经审核确认无可观察副作用的内建函数列表
  （例如 `random()`、`clock_timestamp()`）。此前，
  内建函数默认允许，只在名称匹配固定拒绝列表时阻断，
  与 volatility 无关。PostgreSQL 自带数百个 volatile
  内建函数，旧拒绝列表只覆盖其中一小部分。

### 修复 {#fixed}

- 此前未检测到从 SQL 语言函数体调用被阻断函数的情况。
  `sql` 是受信语言，因此函数体被认为会在下游被捕获；这对写操作成立，
  但对不在安全 VOLATILE 内建函数允许列表中的内建函数不成立，而且 planner
  会内联简单 SQL 函数，而不是在调用时重新分析函数体。旧式文本函数体和标准
  `BEGIN ATOMIC` 函数体现在都会被检查。只读 SQL
  函数不受影响。
- 此前受限会话可以使用 `pg_current_xact_id()` 和 `txid_current()`。
  两者都会强制事务取得真实事务 ID；只读事务允许这样做，
  因此受限会话可能消耗事务 ID 并增加回绕压力。`_if_assigned()`
  变体只报告已经分配的 ID，仍然允许。
- 此前受限会话可以使用 `brin_summarize_new_values()`、`brin_summarize_range()`、
  `brin_desummarize_range()` 和 `gin_clean_pending_list()`。
  它们修改索引页并发出 WAL，却不经过 executor 或核心的任何只读检查，
  而且表 owner 可以调用它们，因此受限角色能够写自己拥有的表上的索引。
  四者现在都被阻断。
- `lo_import`/`lo_export` 之外的大对象读写函数族
  （`lo_get`、`loread`、`lo_open`、
  `lo_close`、`lo_lseek`、`lo_tell` 等）、
  `pg_export_snapshot()`、`pg_stat_clear_snapshot()`、
  `pg_sleep()`/`pg_sleep_for()`/`pg_sleep_until()`，
  以及 `pg_blocking_pids()`/`pg_lock_status()` 此前都允许受限会话使用，
  因为它们都不在旧拒绝列表中。它们会读取或持有服务器端状态，
  或者直接阻塞 backend；只读会话不应能够做这些事。由于都不在新的
  VOLATILE 内建函数允许列表中，它们现在都被阻断。
- 角色被授予受限角色成员身份时，此前不会丢弃缓存计划。
  `GRANT <role> TO <role>` 写入 `pg_auth_members` 而不是
  `pg_authid`，因此错过了重置计划缓存的回调；授权前构建的计划
  可能再运行一次，而没有执行被阻断函数检查。
- 受限会话此前会静默接受 SET TRANSACTION READ WRITE
  （策略缺口；由于双重保险保护，不能利用）
- 此前未显式阻断 COPY TO PROGRAM
  （PostgreSQL 权限要求可缓解，但为纵深防御而加入）
- 受限会话此前拒绝把 `transaction_read_only`
  或 `default_transaction_read_only` 设置为 on，而这只是请求
  SafeSession 已经强制执行的状态。在每个新建连接上都声明只读的客户端，
  例如以禁用写入运行的连接池，会被完全锁住。现在只会阻断放宽任一设置。
- 受限会话此前可以把任何被阻断函数作为参数传给 `EXECUTE` 来运行它，因为
  预编译语句的参数既不属于预编译查询，也不会经 executor 求值，
  所以两个本应捕获它们的检查都看不到参数。`EXPLAIN EXECUTE`
  无论是否带 `ANALYZE`，以及 `CREATE TABLE AS ... EXECUTE`，
  都会发生同样的求值；三者现在都会检查。
- 角色成员此前用 `is_member_of_role()` 测试，
  该函数会在没有实际授权的情况下把超级用户报告为数据库中每个角色的成员。
  因此，任何在 session user 不是超级用户时短暂充当超级用户的角色，
  例如位于超级用户拥有的 SECURITY DEFINER 函数中，或被 supautils
  这样的扩展为单条命令提升权限的角色，都会被视为每个受限角色的成员并被阻断，
  即使它没有被列出，也没有获得任何授权。成员检查现在使用
  `is_member_of_role_nosuper()`，只遵循实际授权。
- 有副作用的函数调用在语句解析时检测，因此会话受限前缓存的计划
  会重放而不再次执行检查。因为角色列表重载，或角色被授予受限角色成员身份，
  会话在生命周期中途变为受限后，可能继续通过之前执行过的预编译语句或
  PL/pgSQL 表达式调用被阻断函数。变为受限现在会丢弃该会话的缓存计划，
  使它们在新状态下重新分析。
- PostgreSQL 19 此前无法编译，因为它通过不同于早期版本的
  header 访问 `GETSTRUCT`，并把
  `jstate` 参数改为 `post_parse_analyze_hook_type`
  const。PostgreSQL 14 到 18 上的构建不变。
- 受限会话此前可以通过定义中调用被阻断函数的视图查询，
  或通过行级安全策略的 `USING`/`WITH CHECK` 子句运行该函数。
  视图体和 RLS qual 都在查询重写期间替换；该阶段发生在函数阻断检查
  使用的解析分析阶段之后，因此两者对检查不可见。受限会话还可以通过
  domain 的 `CHECK` 约束运行被阻断函数；该约束由 executor
  独立于查询树获取并求值，因此同样没有被检查。出现在查询解析树中的
  强制转换所触发的 domain `CHECK` 约束，包括作为 `EXECUTE`
  语句声明参数类型的约束，现在也会检查。
- 检查视图体中的被阻断函数是真实行为变化，而不只是 bug 修复：
  如果受限角色读取的视图定义中调用了非受信语言中的副作用函数，
  例如恰好包装这类调用的基于 `pg_stat_statements` 的监控视图，
  现在会被拒绝，而此前不会。这一收紧是有意的；但如果既有只读监控查询
  通过视图构建，值得关注。
- 当触发 domain `CHECK` 约束的强制转换没有出现在任何查询树中时，
  该约束仍可能运行被阻断函数。通过 extended query protocol 绑定的参数
  会在取得计划前在 `exec_bind_message()` 中强制转换；这是 JDBC、
  psycopg、node-postgres 和 npgsql 的正常路径。PL/pgSQL 变量声明的类型
  和函数的 `RETURNS` 类型则完全不会生成 `CoerceToDomain` 节点。
  现在，对象访问钩子会在 executor 编译被阻断函数时拒绝它，而这发生在
  约束求值之前，因此以上路径都会被捕获。参数甚至不需要被查询引用：
  声明它就足够，因为约束作为强制转换的副作用运行。
- 快速路径函数协议（libpq 的 `PQfn`，大对象客户端 API 建立在其上）
  此前不经过任何钩子，因此受限会话可以通过它调用任何函数。
  同一对象访问钩子现在覆盖该协议。

---

[上游原文](https://github.com/pgEdge/pgedge-safesession/blob/b406cd1e82cf21f30959351691c56de046562678/docs/changelog.md) · `b406cd1e82cf` · Copyright (c) 2025–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文整理：PGSTY 社区。本文为翻译初稿，尚待逐句审校。
