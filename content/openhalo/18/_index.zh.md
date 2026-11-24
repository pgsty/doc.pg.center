---
type: docs
upstream_source: openhalo-pgsty
upstream_link: ""
search_keywords: ["OpenHalo 18", "aux_mysql 1.9", "PGSTY", "v18.6.1", "2627e6f", "6a93e8f", "v18.6", "MySQL 5.7"]
title: OpenHalo 18 与 aux_mysql 1.9
linkTitle: OpenHalo 18
description: PGSTY OpenHalo 18 的架构定位、产品谱系、版本标识、五级兼容约定与阅读指南。
weight: 1
cascade:
  type: docs
  upstream_source: openhalo-pgsty
no_list: true
---

OpenHalo 18 由**带协议、执行器、序列、外键与排序规则钩子的 PostgreSQL 18.6 内核**与同树维护的 **`aux_mysql` 扩展**组成，由扩展实现 MySQL 线协议、解析器、解析树改写、事务语义与兼容函数库。MySQL 客户端默认连接 TCP `3306` 端口，PostgreSQL 客户端连接 `5432` 端口。两种协议读写同一份表数据：MySQL 的数据库（database）对应指定 PostgreSQL 数据库（`mysql.database`，默认 `postgres`）中的模式（schema）。

本手册对应 [PGSTY 维护的分支](https://github.com/pgsty/openhalo)，兼容目标为遗留 MySQL 5.7 应用。切勿将其配置参数或支持结论与本栏目中的历史 PG14 openHalo 或商业 Halo Database 1.0.16 页面混用。

> [!IMPORTANT]
> **源码与安装包状态（2026-11-10）。** `main` 分支已发布源码标签 **`v18.6.1`**（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`），正式搭载 **`aux_mysql 1.9`**，取代早期标签 `v18.6`（`60e7a225f2182b0a056501dba1aa79e358f9cbb1`，`aux_mysql 1.5`）。2026-11-10 独立最终验收审计与性能基线严格固定在提交 **`6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`**（在本文档披露边界内取得源码级**有条件 GO**）；`6a93e8f` 到 `v18.6.1`（`2627e6f`）之间的 4 个提交仅补充版权注释头、`.gitignore` 规则与文档修订，**可执行 C、SQL 与语法规则零变更**。`v18.6.1` 的多平台生产 RPM/DEB 二进制安装包仍需完成目标平台构建与安装/升级/恢复包级验收；详见[最终验收与发布条件](/openhalo/18/acceptance/)。

## 阅读本手册 {#manual}

- [功能集合](/openhalo/18/features/) — 协议、DML、事务、类型、索引、生成列与元数据的支持程度、核心行为、可执行 SQL 示例及迁移影响。
- [v18.6 以来的修改](/openhalo/18/changes/) — 从最初七项阻断到 WP1–WP10、最终正确性修复及排序性能恢复的完整演进脉络。
- [兼容边界](/openhalo/18/compatibility/) — 精确行为与有意映射、仅回显设置、不支持的 SQL、同库原生 PostgreSQL 会话影响及诊断错误码。
- [构建与配置](/openhalo/18/configuration/) — 内核与扩展配套编译、实例初始化、`caching_sha2_password` 认证、`mysql.*` 参数上下文及废弃参数对照。
- [迁移与升级](/openhalo/18/migration/) — MySQL 5.7 迁移、PG14 逻辑迁移、真实 `1.5 → 1.9` 升级、不会自动修复的历史对象及备份恢复。
- [最终验收](/openhalo/18/acceptance/) — 已核验构建、SHA-256 校验值、测试与性能证据、未验证范围及剩余发布交付条件。
{.cards}

## 产品关系与架构 {#lineage}

| 维度 | OpenHalo 18（`pgsty/openhalo`） | 上游 openHalo 1.0（`pg14`） | 商业 Halo Database（`1.0.16`） | 原生 PostgreSQL 18.6 |
| --- | --- | --- | --- | --- |
| 内核基线 | PostgreSQL 18.6 + 协议、冲突、外键、序列与排序规则钩子 | PostgreSQL 14.18 分叉（修改约 320 个内核文件） | 商业闭源多模内核 | 未修改的 PostgreSQL 18.6 |
| MySQL 逻辑位置 | `contrib/aux_mysql`（通过 `shared_preload_libraries` 默认加载）+ 内核钩子 | 直接编译进分叉的内核解析分析/执行器 + `aux_mysql` SQL 层 | 专有引擎模块 + `aux_mysql` / `plmyssql` | 无 |
| 扩展与二进制 ABI | 保持 PG18 系统目录布局；协议、解析与计划节点结构体有改动，内核与扩展须配套编译 | 与原生 PG14 不一致（修改 `DestReceiver`、`pg_proc`、ACL 位） | 商业专有二进制分发 | 标准 PG18 ABI |
| 3306 协议认证 | `caching_sha2_password`（TLS / RSA-OAEP + 快速认证缓存）或 `mysql_clear_password`，复用 PG SCRAM/MD5 密码校验 | 依赖自定义 `password_encryption` 的 `mysql_native_password` | 通过 `hsql` / Halo 参数配置 `mysql_native_password` | 仅支持 PG 协议（`5432`） |
| 库 / 模式模型 | MySQL 数据库对应 `mysql.database`（`postgres`）中的模式；开启自动安装时首次超级用户 MySQL 登录自动安装扩展 | `database_compat_mode = 'mysql'` + 手动 `CREATE EXTENSION aux_mysql` | `cluster_net_services` + `mysql.default_tenant` | 原生数据库与模式 |
| 从 PG14 物理升级 | **不支持**（`pg_upgrade` 明确拒绝 `1.0.14.x` 二进制），必须逻辑迁移 | 不适用 | 厂商专有方案 | 支持从原生 PG 执行标准 `pg_upgrade` |
| 软件许可证 | 内核与协议钩子采用 PostgreSQL License；`aux_mysql` 及包含它的构建按 GNU GPL v3 分发 | GNU GPL v3 | 商业闭源许可 | PostgreSQL License |
{.wide .expand}

MySQL 语法文件（`src/parser/mys_gram.y`）与基础 SQL 目录（`sql/aux_mysql.sql`）由 `tools/port_grammar.py` 和 `tools/port_aux_sql.py` 从本仓库 `pg14` 分支（已同步 `HaloTech-Co-Ltd/openHalo` 至 `90fc8d7`）确定性生成，再叠加 OpenHalo 18 的 C 语言钩子与 SQL 升级脚本。

## 版本标识 {#versions}

| 标识 | 确切含义与当前状态（2026-11-10） |
| --- | --- |
| PostgreSQL `18.6`（`180006`） | `pgsty/openhalo` 的底层内核基线（`PG_VERSION = 18.6`，`PG_VERSION_NUM = 180006`），附加协议、ModifyTable 冲突、RI 外键、原子序列推进与排序规则钩子。 |
| 标签 `v18.6.1`（`2627e6f`） | `main` 分支当前源码标签（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`，附注标签 `55aab1f7ef3ce5d4f2893dcf76e6a6c270c4cf89`）；搭载 **`aux_mysql 1.9`**，在已验收 `6a93e8f` 之上仅增加 4 个版权注释头与文档提交，可执行 C/SQL/语法零变更（`e1f2424` 已完成干净归档复验）。 |
| 已验收提交 `6a93e8f` | `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`；2026-11-10 独立最终源码验收、二进制 SHA-256 指纹与性能采样固定的 **`aux_mysql 1.9`** 快照。`1.6`–`1.8` 为内部 SQL 升级步骤，从未单独发布。 |
| 验收前分支顶点 `a000baa` | `a000baaf68602eda91ccf0b83aca02a7bf694cb1`；2026-11-10 独立验收启动时的远端分支顶点，缺少最后的字符布尔 `DEFAULT` 唯一键冲突修复，已被 `6a93e8f` 与 `v18.6.1` 取代，禁止直接打包。 |
| 标签 `v18.6`（`60e7a22`） | 初始 PG18 标签（`60e7a225f2182b0a056501dba1aa79e358f9cbb1`），安装 **`aux_mysql 1.5`**。早期 `openhalodb-18.6` 源码归档与 RPM 配方指向该 `1.5` 基线；`v18.6.1` 的多平台二进制包仍待完成包级验收。 |
| `5.7.32-log` | `mysql.halo_mysql_version`、`VERSION()` 与 `@@version` 的默认返回串，控制握手字符集通告与 `/*!NNNNN ... */` 版本判断；**不代表**实际安装的 `aux_mysql` 版本，也不承诺完整等价于 MySQL 5.7。 |
| 标签 `v1.0-pg14` | 分支 `pg14` 上的 `f9aedb893233f1f95afcd72206df8707ce8f8d64`（上游 `90fc8d7` 加两个 PGSTY 默认套接字/启用提交），属历史 PG14 线。 |
{.wide .expand}

内核与扩展二进制必须来自同一次构建。尽管 `PG_VERSION` 仍为 `18.6`（`PG_VERSION_NUM = 180006`），系统目录兼容 PG18 **并不意味着** `aux_mysql.so` 可加载进原生 PostgreSQL 18；同时，`v18.6` 时期关于“未修改的原生 PGDG 第三方 C 扩展二进制可直接加载”的旧说明在 `v18.6.1`（`aux_mysql 1.9`）中已不再成立——因 `ClientSocket`、`OnConflictClause`、`ModifyTable` 与 `pg_locale` 结构体及回调已发生变化，第三方 C 扩展必须基于 OpenHalo 18 头文件重新编译并验证。

## 五级兼容约定 {#contract}

评估业务应用能否迁移至 OpenHalo 18 时，必须严格区分以下五个不能混为一谈的层次：

1. **语法被接受** — 解析器接受某种子句，但不会按其改变执行计划或行为。例如 `USE INDEX`、`IGNORE INDEX`、`FORCE INDEX` 在 `SELECT`、`UPDATE`、`DELETE` 中可解析，随后在规划前丢弃。
2. **设置可以回显** — 变量或 `sql_mode` 标志可以赋值并经 `SELECT @@...` 读回，但并未接入底层执行行为。典型例子包括 `wait_timeout`、非默认的 `auto_increment_increment` / `auto_increment_offset`、`ANSI_QUOTES`、`REAL_AS_FLOAT`，以及直接执行 `SET collation_connection = 'utf8mb4_unicode_ci'`。
3. **行为真正实现** — 服务端在执行期落实该规则：既包括与 MySQL 5.7 精确一致的路径（如 `utf8mb4_general_ci` 列比较、全唯一键 `ON DUPLICATE KEY UPDATE` / `REPLACE`、`FOREIGN_KEY_CHECKS=0`、`GLOBAL read_only`、布尔 `1`/`0` 写入），也包括明确的近似或 PostgreSQL 映射（如读写 `REPEATABLE READ` 映射为 PostgreSQL `READ COMMITTED`，非精确排序规则映射并发出 `1105` 告警）。
4. **已有独立实测** — 在固定提交 `6a93e8f` 的具名 `aarch64` 构建上，与真实运行的 Oracle MySQL `5.7.32` 逐项比对了落库值、`HEX` 字节、影响行数、warning 代码、error 代码、事务回滚以及真实 `1.5 → 1.9` 升级结果。
5. **全面兼容保证** — **不作承诺**。未穷举的类型组合、特定业务 SQL 写法、多平台正式安装包以及第三方扩展混用场景，仍须在目标应用自身的模式和查询上实测验证。

在已实现功能中，核心底线是**绝不静默写坏数据**：非严格 `sql_mode` 与 `INSERT IGNORE` 仅在可表示范围内保留约定的截断和告警，绝不静默剥离文本中的 `NUL` 字节，绝不暗中削弱已生效约束，也绝不把无法表示的 `BIGINT UNSIGNED` 正数夹到已有的唯一键上。迁移测试前请完整核对[兼容边界参考](/openhalo/18/compatibility/)。

## 文档依据与许可声明 {#sources}

本手册直接依据 `v18.6.1`（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`）中的 `README.md`、`CHANGELOG.md`、`contrib/aux_mysql/{README,MIGRATION,TESTING,ROUTE_A_RECHECK,UPSTREAM}.md`、C/SQL/生成器源码与回归测试，以及固定在 `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` 的 2026-11-10 独立最终验收证据整理。遇到说明文字、实现代码与实测输出表述侧重不同之处，一律以实际 C/SQL 代码与 `6a93e8f` 原始执行记录为准。

PostgreSQL 18.6 内核与新增协议钩子保留 PostgreSQL License（部分版权归 PostgreSQL Global Development Group，1996–2025）；`contrib/aux_mysql` 派生自 GPLv3 的 openHalo（版权归易景科技 Halo Tech Co., Ltd.，2025；部分修改版权归 PGSTY PTE. LTD.，2026），因此包含 `aux_mysql` 的构建按 GNU GPL v3 分发。源文件、验收制品与双语页面的校验指纹记录于 `data/imports/openhalo-pgsty.json`，详见[来源声明](/attribution/#openhalo)。
