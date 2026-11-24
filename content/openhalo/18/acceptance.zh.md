---
type: docs
upstream_link: ""
search_keywords: ["6a93e8f", "6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a", "2627e6f", "2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183", "v18.6.1", "a000baa", "GCC 14", "231", "922", "FIND_IN_SET", "GO", "NO-GO", "final acceptance", "最终验收"]
title: 最终验收与发布条件
description: 提交 6a93e8f 在 2026-11-10 的固定验收结论、验收后源码标签 v18.6.1（2627e6f）增量说明、二进制 SHA-256 校验值、测试与性能证据、未验证范围及剩余安装包交付条件。
weight: 60
---

**验收日期：** `2026-11-10`（`Asia/Shanghai`） · **固定受测提交：** `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`（`aux_mysql 1.9`）。

- **受测源码 `6a93e8f` 验收结论：在约定 `aux_mysql 1.9` 兼容范围内有条件 GO。** 规定范围内的全部干净构建、核心回归、差分对照套件、真实升级/恢复测试及收尾阻断验证均已完成，未发现尚未关闭的候选代码阻断。此前复现的超 `UINT64_MAX` 无符号唯一键错行操作、布尔字面量/转换/默认值唯一键错行操作、`FIND_IN_SET` 尾空格误判及 `general_ci` 数倍排序性能退化均已在 `6a93e8f` 验证关闭。放行前提是随版本准确公布[兼容边界](/openhalo/18/compatibility/)，不得将其宣传为完整无差别的 MySQL 5.7 替代实现。
- **审计时点分支（`a000baa`）对比验收后源码标签 `v18.6.1`（`2627e6f`）与二进制安装包状态**：在 `2026-11-10` 执行 `6a93e8f` 独立验收时，`origin/master` 仍停留在 `a000baaf68602eda91ccf0b83aca02a7bf694cb1`（**NO-GO**，尚缺字符布尔 `DEFAULT` 错行覆盖/误删修复），早期 `openhalodb-18.6` 源码归档与 RPM 配方仍打包 `aux_mysql 1.5`（对 `1.9` 发布为 **NO-GO**）。`2026-11-10` 晚些时候，仓库已将 `6a93e8f` 合入 `main` 并发布**源码标签 `v18.6.1`**（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`，附注标签 `55aab1f7ef3ce5d4f2893dcf76e6a6c270c4cf89`）：`6a93e8f..2627e6f` 之间的 4 个提交（`e1f2424`、`1d7e45e`、`2ae3a15`、`2627e6f`）仅增加版权注释头、`.gitignore` 规则与文档修订，**可执行 C、SQL 与语法规则零变更**，且 `e1f2424` 已完成干净归档 debug/release 复验（见 `ROUTE_A_RECHECK.md`）。**多平台生产 RPM/DEB 二进制安装包仍待完成**目标平台构建与包级验收。

本页严格将 `2026-11-10` 独立验收的二进制校验指纹、差分断言统计与基准测试样本固定在 `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`，不会将其暗中改标到后续提交或尚未验证的二进制安装包上。

## 验收对象与仓库身份 {#identity}

| 对象 | 已核验状态 |
| --- | --- |
| 固定验收提交 | `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`（审计时位于分支 `codex/aux19-boolean-defaults`，工作区干净） |
| 候选版本构成 | 带 OpenHalo 钩子的 PostgreSQL `18.6`（`PG_VERSION_NUM = 180006`）内核 + `aux_mysql 1.9` |
| 审计时点 `origin/master` | `a000baaf68602eda91ccf0b83aca02a7bf694cb1` —— 缺少 `6a93e8f` 的布尔默认值唯一键冲突修复（直接发版为 **NO-GO**） |
| 验收后 `main` 与 `v18.6.1` | `2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`（附注标签 `v18.6.1` `55aab1f7ef3ce5d4f2893dcf76e6a6c270c4cf89`，`2026-11-10 18:16:14 +0800`）；在 `6a93e8f` 之上仅含 4 个版权注释头/`.gitignore`/文档提交（可执行 C/SQL/语法零变更；`e1f2424` 干净归档复验通过：`231/231` 核心回归、`26/26` smoke、`23/23` 集成与升级、`922` 项 `release_fixes.py`） |
| 历史 Git 标签 | `v18.6`（`60e7a225f2182b0a056501dba1aa79e358f9cbb1`，附注标签 `5086d18f03af2794b69c87c784768a7aeb5d43e9`，含 `aux_mysql 1.5`）与 `v1.0-pg14`（`f9aedb893233f1f95afcd72206df8707ce8f8d64`） |
| 源码树逐字节一致性 | 从 `6a93e8f` 导出的 `git archive`（`7,464` 个跟踪文件）与本地工作区、EL9 构建树、EL10 构建树逐字节一致（对照 `v18.6` 为 `7,391` 个文件，`a000baa` 为 `7,464` 个文件） |
| 参照数据库 | 真实运行的 Oracle MySQL Community Server `5.7.32`（`VERSION() = '5.7.32'`） |
| 候选独立构建 | 三套从提交归档重新编译的安装（均启用 `--with-openssl --enable-depend`、`-O2`，并将隐式函数声明与整数/指针隐式转换作为编译错误）：**EL9 Debug**（额外启用 `--enable-debug --enable-cassert`，Rocky Linux 9.8 `aarch64`，GCC `11.5.0`）、**EL9 Release**（同环境）、**EL10 GCC 14**（独立容器内 Rocky Linux 10.2 `aarch64`，GCC `14.3.1`） |
| 运行进程身份核验 | 逐一核验测试后端进程的 `/proc/<pid>/exe` 与实际内存映射的 `aux_mysql.so` SHA-256，不以端口号或目录名代替二进制身份 |
{.wide .expand}

验收全程未修改任何产品源码、测试脚本或 `expected/` 期望文件。针对容器宿主共享 `/dev/shm` 仅 64 MiB 的环境限制，测试实例显式设置 `dynamic_shared_memory_type = mmap` 以避免共享内存干扰，未改动产品默认配置。

## 验证矩阵 {#tests}

| 验证项目 | EL9 Debug（`GCC 11.5.0`） | EL9 Release（`GCC 11.5.0`） | EL10（`GCC 14.3.1`） |
| --- | --- | --- | --- |
| 提交归档干净构建与安装 | 通过 | 通过 | 通过 |
| PostgreSQL 核心回归 `installcheck` | `231 / 231` | `231 / 231` | `231 / 231` |
| `tests/run.sh` 协议与驱动 smoke | `26 / 26`（`0` 跳过） | `26 / 26`（`0` 跳过） | 未重复整套 smoke |
| `tests/release_fixes.py` 专项断言 | `922` 项断言 | `922` 项断言 | `922` 项断言 |
| `TESTING.md` 集成、Route A、历史升级与恢复 | `23 / 23` 次调用 | `23 / 23` 次调用 | 未重复该完整矩阵 |
| 真实 `v18.6`（`1.5`）→ `1.9` 二进制与 SQL 升级 | 通过 | 通过 | 未重复 |
| 旧版 Connector/J `5.1.49`（TLS、文本与预备语句） | 通过 | 通过 | 未重复 |
| 独立布尔写入与默认值对照矩阵 | `547` 组（`0` 差异） | `547` 组（`0` 差异） | 已由 `release_fixes.py` 覆盖专项路径 |
| 随机对抗字符串排序规则对照 | `4,000` 条字符串（随机种子 `191106`，`0` 差异） | 同左 | 未重复 |
{.wide .expand}

各套件统计粒度存在嵌套与重叠，**严禁直接相加包装成“总测试用例数”或产品兼容率百分比**：

- **生成器与源码洁净度检查**：基于 `pg14` 重新生成的全部 `5` 个语法/SQL 输出文件（`mys_gram.y`、`aux_mysql.sql`、`aux_mysql_fix_show.sql`、`aux_mysql--1.6--1.7.sql`、`aux_mysql_update18.sql`）逐字节一致；全树无 `text_string` 残留。
- **Smoke 与多语言驱动覆盖（`26/26`，`0` 跳过）**：覆盖 SQL 回归脚本（`p3`–`p9`、`m1`–`m4`）、`46` 项 AB 对照、PyMySQL、原始 `COM_STMT_*` 二进制报文、TLS/RSA 与错误密码拒绝、`mysql` CLI、`mysqlslap`、现场重编的 `go-sql-driver/mysql` `1.9` 及 Connector/J `8.4.0`。缺少测试依赖时退出码为 `2`（验证不完整），绝不计为 `PASS`。
- **Route A 分包断言数（每套 EL9 构建）**：`text`（`375`）、`binary`（`122`）、`char`（`42`）、`collation`（`468`）、`collation_all`（覆盖 MySQL 5.7 全部 `221` 个字符排序规则 × `3` 种列类型共 `9,945` 项断言，并显式保留 **`1105` 近似约定下的 246 组区域/编码差异日志**）、`numeric_cast`（`372`）、`uint64`（`167`，测试超 `UINT64_MAX` 写入与回滚前预先埋入 `INT64_MAX` 旧键）、`prefix_nul`（`19`）、`hints`（`315`）及 `route_a_fk_privileges`（`46`）。
- **独立 547 组布尔与默认值对照探针**：由 `480` 组布尔写入（`10` 种列类型 × `6` 种布尔表达式 × `4` 种写入形式 × `2` 种 `sql_mode`）、`16` 组预埋唯一键冲突写入（`INSERT`、`ODKU`、`REPLACE`、`UPDATE IGNORE`）、`32` 组 `DEFAULT` 与默认冲突用例、`19` 组 `ALTER`/事务/重连检查组成，对照真实 MySQL `5.7.32` 逐一核对落库值、`HEX`、warning 级别与代码、error 代码，并对前 `480 + 16` 组在**执行 `SHOW WARNINGS` 之前**捕获比对影响行数——差异均为零。
- **原生 PostgreSQL 18 独立模块验证**：`indexes_standalone.py` 与 `binary_fix/run.sh` 在原生 PG18 上全部通过，覆盖 libpq 文本/二进制协议 I/O、内嵌 `NUL` 前缀裁剪防御、并发写入、缓存失效及 `pg_dump`/`pg_restore`。

## 真实升级与备份恢复证据 {#upgrade}

- **真实 `v18.6`（`1.5`）→ `1.9` 停机升级**：先以真实 `v18.6` 二进制与 `aux_mysql 1.5`（预先关闭 `1.5` 存在启动竞态的旧后台自动安装功能）初始化实例，经 MySQL 协议创建数值、字符/二进制、前缀索引、已强制/未强制外键、孤儿行、被丢弃的旧生成列、字符布尔默认值、视图、`BEGIN ATOMIC` 过程与基于原生 `DO` 的触发器；停止旧服务后用 `6a93e8f` 新二进制启动同一数据目录并执行 `ALTER EXTENSION aux_mysql UPDATE`。升级前后同一长连接、新建连接、重复预备语句、继承的布尔默认值及依赖视图均正常工作。*（注：`BEGIN ATOMIC` 过程与 `DO` 触发器仅验证既有目录对象跨升级保留，不代表支持 MySQL 5.7 存储过程或触发器体语法。）*
- **扩展系统目录零原始差异（`1.5 → 1.9` 对比全新 `1.9`）**：`3,476` 个扩展成员、`1,859` 个函数/过程、`20` 个视图、`272` 个视图列、`88` 个转换、`665` 个运算符、`27` 个运算符类**原始定义差异为空**；另有独立目录审计比对 `596` 个类型、`13` 个域约束、`5` 个排序规则、`1,866` 条函数属性记录（含 `7` 个聚合）、`7` 个聚合定义与 `201` 条关系属性，同样**原始差异为空**。仅单独验证的**未发布 `1.6 → 1.7 → 1.8 → 1.9` 链**在 `mys_informa_schema.columns.extra` 上保留已约定的 `pg_catalog.default` 与 `pg_catalog.C` 排序规则差异。
- **逻辑备份恢复往返**：完成同版本原生 `pg_dump`/`pg_restore` 往返及 Oracle MySQL `5.7.32` 客户端 `mysqldump`/`mysql` 往返——包括将 OpenHalo 导出的同一份未修改 `mysqldump` 文件直接恢复进真实 MySQL `5.7.32`——完整保留二进制 `NUL`/任意字节、十六进制默认值、生成值、前缀主键、缺父表的待绑定外键触发器及历史孤儿行，并在恢复后验证新非法写入拦截与外键级联生效。

## 性能裁决与适用范围 {#performance}

性能采样在 EL9 `aarch64` 主机（`GCC 11.5.0 -O2` release 构建）上针对 **300,000 行**测试集执行，待全部编译与回归任务结束后预热 1 次、交错采样 10 轮：

- **`ORDER BY` 负载**：对 32 字符 `MD5(id)` 字符串按 `utf8mb4_general_ci` 排序，在 `work_mem = '64MB'`、关闭 JIT 与并行工作进程条件下通过服务端 `EXPLAIN (ANALYZE, TIMING OFF)` 计时。
- **`FIND_IN_SET` 负载**：对 8 项逗号分隔列表做 30 万行全表聚合求和（结果恒为 `1350000`），按客户端完整往返查询耗时计时。

| 被测构建 / 基线 | `ORDER BY` 中位数（10 轮样本区间） | `FIND_IN_SET` 客户端中位数 |
| --- | ---: | ---: |
| 候选 `6a93e8f`（`aux_mysql 1.9`） | **`63.82 ms`**（`57.98–76.12 ms`） | **`0.677 s`** |
| 前一提交 `a000baa`（`aux_mysql 1.9`） | `59.97 ms`（`56.05–124.12 ms`） | `0.688 s` |
| 已发布 `v18.6`（`aux_mysql 1.5`，ICU） | `102.24 ms` | `3.049 s` |
| 参照 MySQL `5.7.32`（3 次采样对照） | *（计时层级不同，不并表对比）* | **`~0.073 s`** |
{.wide .expand}

**解读边界：**

- 相比已发布 `v18.6`，候选 `6a93e8f` 的排序耗时缩短约 **38%**，`FIND_IN_SET` 耗时缩短约 **78%**，证实此前 `1.9` 中出现的数倍排序退化已消除。
- 候选 `6a93e8f` 与 `a000baa` 的排序代码完全相同；两者的 10 轮样本区间重叠（空闲阶段 10 轮中位数 `63.82 ms` 对比 `59.97 ms`，而更早一轮 3 次采样中位数为 `58.14 ms` 对比 `62.80 ms`），反映共享宿主的负载波动，不能据此宣称性能绝对等同或存在真实退化。
- **`FIND_IN_SET` 仍比 MySQL `5.7.32` 慢约 9 倍（`0.677 s` 对比 `0.073 s`）**，原因在于它仍是 SQL 函数（`unnest(string_to_array(...))`）而非 C 实现。由于服务端 `EXPLAIN (ANALYZE, TIMING OFF)` 与客户端协议总耗时统计口径不同，未将跨引擎 `ORDER BY` 数字并列比较。以上受控样本不替代独占物理机与真实客户业务负载基准。

## 验收制品 SHA-256 指纹 {#evidence}

验收目录完整保留 `FINAL_REPORT.md`、`verification.json`、`SHA256SUMS`、进程映射、编译日志、各套件返回码、原始 SQL/HEX/warning 记录、目录差异与全部性能样本。以下校验值用于核对取得的审计副本，**不代表存在公开安装包下载链接**：

| 已核验审计制品 | SHA-256 |
| --- | --- |
| 候选源码归档快照（`source.tar.gz`） | `e0a7fc4a2e278985847e575121e60a2f92e7cea5b3b5a1f551721c6fa4b2c6f5` |
| 完整验收证据归档（`evidence.tar.gz`，`33,580,392` 字节） | `df0c062078ab9cfdf612fea4c905aa7eb203ccfef614d3b6d55558799d78803c` |
| EL9 Debug `postgres`（`Rocky 9.8 aarch64`，`GCC 11.5.0`） | `631926e75e09c7fe630c33aedb1434fe3ef3497749d907d3838ce8eff88ae1ea` |
| EL9 Debug `aux_mysql.so` | `f895c7421412ef46135b971878e51c598edf95f0bb5df7589eba34d68e9ea3d9` |
| EL9 Release `postgres`（`Rocky 9.8 aarch64`，`GCC 11.5.0`） | `2d054ec9405cd4cfdffb8190f4efe358e4752e9857b337562cc4888dfd9ee326` |
| EL9 Release `aux_mysql.so` | `6eac22a68a39d47296a688464ea0a950c5156be0f1e495a7cbb1ce1534b96557` |
| EL10 Release `postgres`（`Rocky 10.2 aarch64`，`GCC 14.3.1`） | `cb443a169f60cc21074fa3a7fdf1746c6e3ccb249f9ef244fe2f2e4f51cadcb5` |
| EL10 Release `aux_mysql.so` | `80bcdc4fe4afc93f67ac64b6597d4becd0083799d6eef0def47c283b19069b37` |
{.wide .expand}

如需从源码复现，请从确切提交 `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a` 导出干净目录，按照 `contrib/aux_mysql/TESTING.md` 在隔离的一次性实例上运行各套件。切勿将测试指向共享或生产实例（部分套件会重建模式并切换 `GLOBAL read_only` / `super_read_only`），且运行 `release_real_upgrade.py` 必须构建真实的 `v18.6` 旧二进制，不能用新二进制加载旧 SQL 代替。

## 发布交付条件状态 {#release-gates}

1. **D1 —— 将 `6a93e8f` 合入主分支并发布源码标签（`源码层面已完成：v18.6.1`）**：仓库已将 `6a93e8f` 合入 `main` 并打标 **`v18.6.1`**（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`），取代验收前的 `a000baa`，增量仅包含版权注释头、`.gitignore` 与文档提交（`e1f2424`..`2627e6f`）。
2. **D2 —— 生成新的不可变打包源码归档并更新 RPM/DEB 配方（`待完成`）**：现有 `openhalodb-18.6` 打包输入（`source tarball sha256: 6fdd17769c1f25bc4bf9e3677afeb940b73eb9a401dcea13616391fa38d064b4`）仍指向 `default_version = '1.5'`。须从 `v18.6.1`（`2627e6f`）导出独立的 `18.6.1` 不可变源码包并更新 RPM/DEB 配方，不得覆盖历史 `18.6` 归档。
3. **D3 —— 在全部目标平台构建并验收最终安装包（`待完成`）**：在实际发布的操作系统与架构矩阵上验证主包与 debuginfo 载荷、运行时依赖、双协议全新安装、真实 `1.5 → 1.9` 包升级及 `pg_dump` / `mysqldump` 恢复，通过后再执行签名与软件源入库分发。
4. **D4 —— 随版本同步公开兼容边界与迁移审计说明（`源码仓库与本手册已完成；发包时须附于发行说明`）**：`v18.6.1` 仓库文档与本手册均已完整披露[兼容边界](/openhalo/18/compatibility/)与[不会自动修复的历史对象审计规则](/openhalo/18/migration/#audit)，正式分发安装包时须在发行说明中直接关联。

鉴于 `v18.6.1`（`2627e6f`）相对 `6a93e8f` 没有引入任何可执行 C、SQL 或语法规则改动（且 `e1f2424` 的注释头重生成已通过干净归档复验），无需盲目重跑全部源码级差分回归——**在对外宣布二进制包发布前，真正必须补齐的是多平台打包与包级安装/升级/恢复验收（`D2` 与 `D3`）**。后续一旦改动源码、编译参数或安装布局，则必须补测受影响范围。

## 未验证范围与证据不足事项 {#limits}

以下范围在本轮验收中**未执行验证**，不作任何 `PASS` 声明（在补齐专项实测前均属证据不足）：

- **多平台生产安装包及其他架构/编译器**：未在 `6a93e8f` 上执行六平台生产 RPM/DEB 构建安装、`x86_64` 架构、Debian/Ubuntu 工具链及 Clang 构建验证（本轮仅验证 EL9 `aarch64` GCC `11.5.0` 与 EL10 `aarch64` GCC `14.3.1` 源码构建）。
- **第三方 PostgreSQL 扩展的二进制与运行期共存**：未基于 `6a93e8f` 修改后的节点/回调头文件重新编译并集成测试 `pg_tde`、`orioledb`、`PostGIS`、`pgvector`、`Citus`、`TimescaleDB` 等第三方扩展（早期 `c380da3` 上的预编译扩展冒烟早于 `c247eca` 的结构体变更，不能证明当前 ABI 兼容）。
- **更早期客户端版本**：探索性测试 Connector/J `5.1.40` 时在查询执行前即因环境 JDK 的 TLS 握手协商失败终止——既不能证明支持 `5.1.40`，也不构成协议字段元数据缺陷证据（`5.1.49` 与 `8.4.0` 已通过）。仅支持 `mysql_native_password` 且无法使用 `caching_sha2_password` 或 `mysql_clear_password` 的客户端不在验证范围内。
- **非布尔时间/JSON 表达式全空间穷举与长稳压测**：本轮未对 `DATE`/`TIME`/`DATETIME`/`TIMESTAMP`/`YEAR`/`JSON` 上的非布尔表达式组合做全语法空间重新穷举，也未开展真实客户生产负载、高倾斜长前缀极限压测、数天级长稳/容量测试或全面安全渗透审计。
- **非零编译警告**：隐式函数声明与整数/指针转换已按错误处理并通过，但 GCC `11.5.0` 下仍保留 `3` 条未使用函数/变量遮蔽警告，GCC `14.3.1` 下保留 `9` 条警告（含继承全局变量的 `-Wmissing-variable-declarations`），不宣称“零编译警告”。

关于修复前的基线问题背景，可对照保留的 [2026-11-07 `9dc937f` 初次复核报告](/openhalo/mysql57-compatibility-review/)。
