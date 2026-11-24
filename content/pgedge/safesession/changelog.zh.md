---
title: pgEdge SafeSession 变更日志
description: 记录 pgEdge SafeSession 1.1、1.0 与 1.0-beta1 的新增、变更和修复。
weight: 200
upstream_source: pgedge-safesession-20261121
upstream_link: https://github.com/pgEdge/pgedge-safesession/blob/d66225fcceefa2b2cb2cdd7a0b8b84ccae8a4295/docs/changelog.md
upstream_modified: true
upstream_ref: d66225fcceef
source_kind: pinned-release-tag
translation_status: translated
translation_notice: en
translator: PGSTY 社区
type: docs
---



本页记录 pgEdge SafeSession 各版本的重要变更。安全修复按受影响的功能、修复后的行为及运维影响整理。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，
本项目遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [1.1] - 2026-11-06 {#11---2026-11-06}

### 变更 {#changed}

- 发布工作流在配置 pgEdge 软件包仓库之前安装仓库客户端证书，并验证密钥与证书匹配、证书及其颁发者均处于有效期内，以及证书链的颁发者符合预期。
- 仓库重写失败时，发布工作流也会失败。
- 发布工作流通过提交 SHA 固定构建器 Action。
- 打包不再为 Debian bullseye 构建软件包。
- 默认打包目标改为 v1.1。
- 从 README 和文档首页移除 pgEdge Labs 品牌标识。

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
- 以会话用户为锚点的角色检查：SET ROLE 无法摆脱限制
- 超级用户豁免：超级用户永不受限
- 通过 `is_member_of_role()` 实现角色成员继承
- 双重保险：为受限会话自动设置
  `default_transaction_read_only = on`
- 防止绕过 SECURITY DEFINER：无论当前有效用户是谁，始终检查
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
    - `block_all_c_functions`：无论易变性如何，
      阻断所有 C 函数（默认：off）

- 为受限会话阻断 COPY TO PROGRAM
- 为受限会话阻断 SET TRANSACTION READ WRITE
- 针对高级攻击路径的新回归测试
  （PREPARE/EXECUTE、DO 代码块、聚合、WHERE 子句、
  SET TRANSACTION）
- 针对 GUC 切换行为的新回归测试

### 变更 {#changed-1}

- C 语言函数阻断现在默认只阻断 VOLATILE
  C 函数。IMMUTABLE 和 STABLE C 函数
  （例如 PostGIS 几何运算、pgvector 距离
  运算符）允许执行。使用 `block_all_c_functions = on`
  可恢复之前阻断所有 C 函数的行为。
- 内建函数阻断现在默认拒绝任何 VOLATILE
  内建函数，只允许经审核确认无可观察副作用的内建函数列表
  （例如 `random()`、`clock_timestamp()`）。此前，
  内建函数默认允许，只在名称匹配固定拒绝列表时阻断，
  与易变性无关。PostgreSQL 自带数百个易变
  内建函数，旧拒绝列表只覆盖其中一小部分。

### 修复 {#fixed}

- SQL 函数体中的调用也受函数策略约束，包括传统文本函数体和 `BEGIN ATOMIC` 函数体。只读 SQL 函数可继续使用。
- 受限会话不再能强制分配事务 ID，以免增加事务 ID 回绕压力。只查询已分配 ID 的 `_if_assigned()` 变体仍可使用。
- 受限会话不能执行会修改索引的 BRIN 汇总、取消汇总和 GIN 清理操作。表所有者同样受此限制。
- 函数允许清单排除了会访问服务器状态的大对象、快照、统计和锁信息函数，以及会阻塞后端的休眠函数。
- 向角色授予受限成员身份后，扩展会使相关缓存计划失效。重载受限角色清单时也会重新检查既有连接，预备语句和 PL/pgSQL 表达式在新限制下重新分析。
- 现在明确拒绝把受限事务切换为可写，也明确禁止使用 `COPY TO PROGRAM`。原有只读事务保护和 PostgreSQL 自身的权限检查继续生效。
- 允许客户端显式声明只读，仍会阻止放宽 `transaction_read_only` 或 `default_transaction_read_only`。在每次建立连接时声明只读的连接池可正常使用。
- 扩大了对预备语句参数的函数检查范围，使直接执行、查看执行计划及使用查询结果建表时采用相同的只读策略。
- 角色成员检查改用 `is_member_of_role_nosuper()`，只考虑实际授予的成员身份。临时以超级用户权限执行语句的普通会话不会再被误判，已受限的会话仍然受限。
- 修复 PostgreSQL 19 构建时的头文件和解析钩子参数兼容问题。PostgreSQL 14 至 18 沿用原有构建方式。
- 函数检查现已覆盖视图、行级安全策略及域约束。读取依赖有副作用函数的监控视图可能被拒绝，升级时应复核这些视图。
- 域约束也在表达式编译时检查，覆盖扩展查询协议，以及 PL/pgSQL 变量和函数返回值的类型转换。
- libpq 快速路径函数协议也执行相同的函数检查，大对象客户端 API 同样受保护。

---

[上游原文](https://github.com/pgEdge/pgedge-safesession/blob/d66225fcceefa2b2cb2cdd7a0b8b84ccae8a4295/docs/changelog.md) · `d66225fcceef` · Copyright (c) 2025–2026, pgEdge, Inc. [PostgreSQL 许可证](/zh/pgedge/about/license/)。

中文译校：PGSTY 社区。
