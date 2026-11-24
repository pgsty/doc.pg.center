---
type: docs
upstream_link: ""
search_keywords: ["FIND_IN_SET", "boolean defaults", "布尔默认值", "UINT64_MAX", "ODKU", "REPLACE", "v18.6.1", "2627e6f", "6a93e8f", "a000baa", "sorting performance", "排序性能"]
title: v18.6 以来的修改
description: 从已发布 v18.6（aux_mysql 1.5）到通过验收的 6a93e8f 与源码标签 v18.6.1（aux_mysql 1.9）的完整工程记录，串联最初七项阻断、WP1–WP10、最终正确性修复与排序性能恢复。
weight: 20
---

本页完整梳理从初始 **`v18.6` 标签（`60e7a225f2182b0a056501dba1aa79e358f9cbb1`，`aux_mysql 1.5`）** 到 **`aux_mysql 1.9`**——于 `2026-11-10` 在 **`6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`** 通过源码验收并发布为 `main` 分支**源码标签 `v18.6.1`（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`）**——之间的全部实质修改。它记录已完成的源码工程与独立验证；`18.6.1` 多平台二进制安装包仍待完成包级验收。中间扩展版本 `1.6`、`1.7`、`1.8` 为内部 SQL 升级步骤（`1.5 → 1.6 → 1.7 → 1.8 → 1.9`），从未单独对外发布。

整个演进过程串联为五个阶段（随后完成源码标签发布）：

1. **初次独立 NO-GO 复核（`9dc937f`，2026-11-07）** — 定位七项 P1 阻断问题（`B01`–`B07`）与十三项附加行为差异（`B08`–`B20`）。
2. **内核与扩展基础改造（`cffcee6`..`517cd0b`，`1.6`–`1.9` 基础层）** — 引入 PostgreSQL 18 冲突判定、外键、序列、排序规则钩子，完成 DML、事务、二进制类型、前缀索引、命名锁与生成列主体实现。
3. **十个 Route A 工作包（`8cf384d`..`2a7f1e7`，WP1–WP10 + `f0dc476`）** — 逐项收口类型回退、字符/二进制转换、排序规则搜索、无符号越界、前缀 `NUL` 防御、真实 `1.5` 升级、索引提示及待绑定外键权限检查。
4. **最后正确性与排序性能修复（`aa25342`、`6f9c4f3`、`a000baa`、`6a93e8f`）** — 彻底关闭超 `UINT64_MAX` 正数和布尔值/默认值导致的唯一键错行更新删除缺陷，修正 `FIND_IN_SET` 尾空格与旧驱动字符集元数据，并消除 `general_ci` 数倍排序退化。
5. **独立最终验收与 `v18.6.1` 源码标签发布（2026-11-10）** — 在 EL9 debug/release（`GCC 11.5.0`）与 EL10（`GCC 14.3.1`）上对照真实 MySQL `5.7.32` 完成 `6a93e8f` 全量验证，随后补充 4 个版权注释头与文档提交（`e1f2424`..`2627e6f`，可执行 C/SQL/语法零变更；`e1f2424` 已完成干净归档复验）并打标 `v18.6.1`。

## 内核与扩展基础能力改造 {#foundation}

相比 `v18.6`（`aux_mysql 1.5`），`1.6`–`1.9` 基础层通过配套内核钩子（`9dc937f`、`c247eca`）与扩展子系统（`cffcee6`..`517cd0b`）补齐了以下核心语义：

- **内核钩子（`src/backend/` 与 `src/include/`）**：`nodeModifyTable.c` 中的全唯一索引冲突仲裁与先删后插 `REPLACE`；`ri_triggers.c` 与 `trigger.c` 中的 `FOREIGN_KEY_CHECKS=0` 外键门控及待绑定外键回调；`pg_locale.c` 中的自定义排序规则比较与缩略键接口；`sequence.c` 中的原子单调序列推进（`SetSequenceValueAtLeast`）与只读序列拦截；以及构建早期拒绝 Meson 和 `pg_upgrade` 明确拒绝 `1.0.14.x` 二进制。
- **协议、注释与预备执行**：SQL `PREPARE` / `EXECUTE` / `DEALLOCATE`、`DO expr`、`/*! ... */` 与 `/*!NNNNN ... */` 可执行注释、`#` 行注释、带空白判断的 `--` 注释、末尾注释独立 OK 包，以及 `LIKE` 字面量 `\%` / `\_` 反斜杠保留。
- **事务与访问控制**：`START TRANSACTION WITH CONSISTENT SNAPSHOT`、真正生效的事务 `READ ONLY`（`1792`）与 `GLOBAL read_only` / `super_read_only`（`1290`，含序列写入拦截）、`tx_*` / `transaction_*` 双名同步，以及对已中止事务执行 `COMMIT` 时报 `1180` 错误。
- **DML、锁、键名与类型体系**：修复单目标表 `UPDATE ... JOIN` 崩溃与逗号连接目标匹配；全唯一键 `ODKU` / `REPLACE`、`VALUES(col)`、`REPLACE` 省略列填默认值、无唯一键表退化为普通插入及 MySQL 影响行数统计；带长度的 `mysql.binary_n` / `mysql.varbinary_n`、`mysql.hexlit`（`0x..`、`X'..'`、`b'..'`、`0b..`）及 `HEX()` / `UNHEX()`；带回堆复核的 `mysql_prefix` 索引访问方法；表级键名作用域（物理名附加 `$<8位十六进制>`）；MySQL 5.7 用户级命名锁（`GET_LOCK` 系列）；`VIRTUAL` / `STORED` 生成列的物化计算、表达式白名单校验、写入者 `sql_mode` 转换与 MySQL 元数据导出；以及保留 `DECIMAL(p,s)` 和 `DATETIME(0..6)` 精度元数据。

上述改动形成的用户可见能力以[功能集合](/openhalo/18/features/)为准。

### 初次复核问题的处理结果 {#initial-review}

[2026-11-07 在 `9dc937f` 上的初次复核报告](/openhalo/mysql57-compatibility-review/#blocking-issues)作为历史记录原样保留。其中七项 P1 阻断问题（`B01`–`B07`）与其余记录项（`B08`–`B20`）在候选 `6a93e8f` 中的最终去向如下：

| 初次复核发现（`9dc937f`） | 在 `6a93e8f`（`aux_mysql 1.9`）中的处理结果 |
| --- | --- |
| `B01` · `UPDATE ... JOIN` 后端崩溃 | **已修复（`cffcee6`）。** 安全改写连接更新而不再触发断言失败或 `SIGSEGV`，由 debug/release 连接 DML 测试覆盖。 |
| `B02` · 外键未生效（`NOT ENFORCED`） | **新 DDL 已修复（`da426c5`、`c247eca`、`2a7f1e7`）。** 执行 RI 外键检查与级联动作，支持会话 `FOREIGN_KEY_CHECKS=0`、缺失父表待绑定声明及子表 owner 权限复核。历史遗留的 `NOT ENFORCED` 外键与孤儿行仍需执行[迁移审计](/openhalo/18/migration/#audit)。 |
| `B03` · `REPEATABLE READ` 可见性差异 | **明确保留为产品级映射（`510d65f`）。** 读写 `REPEATABLE READ` 有意运行于 PostgreSQL `READ COMMITTED`；只读 `REPEATABLE READ` 与 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 现提供真正稳定的一致快照。 |
| `B04` · 只读设置不生效 | **已修复（`510d65f`、`c247eca`）。** 事务只读（`1792`）与 `GLOBAL read_only` / `super_read_only`（`1290`，含序列推进）逐语句强制执行，`TEMPORARY` 临时表仍可写。 |
| `B05` · `DECIMAL` 导出丢失 `(p,s)` | **已修复（`381c6b7`）。** `DECIMAL(p,s)` 经 `SHOW` 与 `information_schema` 完整保留并可回放；裸 `DECIMAL` 默认 `(10,0)`；无 typmod 的 PG `numeric` 显示为 `decimal(65,30)` 并告警 `1105`。 |
| `B06` · 排序规则唯一性（`PAD SPACE`） | **四个精确名称已修复（`0bf5d13`、`c247eca`、`4419811`、`6f9c4f3`）。** `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_bin`、`utf8mb4_bin` 按 MySQL 5.7 权重与 `PAD SPACE` 判定唯一性；其他名称以 `1105` 告警近似映射；旧 ICU 索引不会就地改写。 |
| `B07` · 前缀索引唯一性（`UNIQUE(col(n))`） | **新索引已修复（`92a181a`、`9ef2a83`）。** 字符/字节前缀经 `mysql_prefix` 回堆复核执行唯一约束与 `ODKU`/`REPLACE`，并正确暴露 `Sub_part`；历史 `1.5` 丢失长度的旧索引需按原始 DDL 重建。 |
| 次要项 `B09`、`B11`、`B13`、`B19` | **约定范围内已修复。** `AUTO_INCREMENT` 对 `NULL` 与 `0` 自动生成 ID（遵守 `NO_AUTO_VALUE_ON_ZERO`）；`REPLACE` 执行删除加新 ID 插入并返回正确默认值与行数；新建 `BINARY(n)` 补零字节；`INSERT IGNORE` 对可表示越界截断告警并按行跳过键冲突。 |
| 次要项 `B08`、`B10`、`B12`、`B14`–`B18`、`B20` | **保留为明确文档边界或部分修复。** 裸 `TIMESTAMP` 仍为无时区 `timestamp`、不做跨时区换算（`B08`）；`auto_increment_increment`/`offset`（`B10`）、`ANSI_QUOTES`（`B14`）、`wait_timeout`（`B15`）仍仅回显；`ODKU` 行数已修复而普通 `UPDATE` 仍统计匹配行数（`B12`）；保存点事务外的多语句包遇到语法错误仍在执行前整包报错（`B16`）；字符集编号（`45`/`63`）、`SHOW VARIABLES`、`SHOW WARNINGS` 已完善而 `SHOW STATUS` 仍不完整（`B17`）；`PAD_CHAR_TO_FULL_LENGTH` 覆盖核心转换但 `LENGTH()` 等函数仍去尾空格（`B18`）；`BIGINT UNSIGNED > INT64_MAX` 统一报 `1264` 而非提供完整 `uint64`（`B20`）。 |
{.wide .expand}

## 十个 Route A 兼容工作包 {#work-packages}

在合入 `1.9` 主体改动（`6821954`）后，十个专项工作包（`WP1`–`WP10`）与补充转换提交（`f0dc476`）逐项处理了兼容性回归与真实升级安全性：

| 工作包与提交 | 修改范围与验证结论 |
| --- | --- |
| `WP1` · 回退原生 `TEXT`（`8cf384d`） | 移除未公开的自定义 `text_string` 类型，将 `TINYTEXT`/`TEXT`/`MEDIUMTEXT`/`LONGTEXT` 恢复为原生 PostgreSQL `text`；保留 `CAST` 中显式 `CHAR(n)` 长度，支持 `CONVERT(... USING ...)`，并以 375 项断言锁定字符 `NUL` 报 `1366` 的边界。 |
| `WP2` · 二进制转字符（`894b949`） | 为 `mysql.binary_n` / `mysql.varbinary_n` 到 `text`/`varchar`/`bpchar` 增加 UTF-8 全量校验赋值转换（遇到含 `BINARY(n)` 补零在内的 `NUL` 或非法 UTF-8 即使带 `IGNORE` 也报 `1366`），并提供保留原始字节的二进制 `GROUP_CONCAT`（122 项断言）。 |
| `WP3` · `CHAR` 逻辑值（`29a3d6d`） | 统一提取 `CHAR(n)` 字节：默认去尾空格，开启 `PAD_CHAR_TO_FULL_LENGTH` 时保留完整补空格宽度，覆盖 `CONCAT`、`CONCAT_WS`、`CAST`、`CONVERT`、`HEX`、`ELT`、`GROUP_CONCAT`、用户变量、锁名与 `EXECUTE`（42 项断言）。 |
| `WP4` · 排序规则字符串搜索（`4419811`） | 让 MySQL 会话下的 `LOCATE`、`INSTR`、`POSITION` 按排序规则（`general_ci` 权重、`bin` 码点及旧 ICU 别名）搜索，并为字符类型补充区分大小写的 `REPLACE()` 重载（468 + 9,945 项断言）。 |
| `WP5` · 二进制数字 `CAST`（`3f26bed`） | 将 `BLOB`/`VARBINARY`/`BINARY`/`UNHEX` 向 `SIGNED`/`UNSIGNED`/`DECIMAL` 的 `CAST`/`CONVERT` 分发到按长度解析的十进制解析器（`NUL` 与非法 UTF-8 仅终止数字前缀而不报 `1366`），同时保持原生 PG `bytea::int8` 不变（372 项断言）。 |
| `WP6` · `uint64` 高半区防护（`bc1d29c`） | 对 `INT64_MAX + 1 .. UINT64_MAX` 写入（含 `IGNORE` 与二进制 `MYSQL_TYPE_LONGLONG` 无符号参数）统一报 `1264`，防止不同主键折叠到 `INT64_MAX`，并放通 `INSERT IGNORE ... ON DUPLICATE KEY UPDATE` 语法。*（超 `UINT64_MAX` 输入在下方 `F1` 中进一步收紧。）* |
| `WP7` · 前缀索引 `NUL` 防御（`9ef2a83`） | 让 `bin` 与历史排序规则的前缀裁剪按显式字符计数，防止内嵌 `NUL` 提前截断索引键，通过独立原生 PG18 桥接模块验证，同时保持生产路径字符 `NUL` 报 `1366`（19 项断言 + 独立套件）。 |
| `WP8` · 真实 `1.5 → 1.9` 升级（`0dc12fe`） | 补齐升级缺失的列元数据与诊断辅助函数，保留 `information_schema.columns.EXTRA` 视图列描述符，实测真实 `v18.6`（`1.5`）数据目录就地升级至 `1.9` 后扩展目录零原始差异。 |
| `WP9` · 忽略索引提示与 `USING` 删除（`311ef83`） | 在 `SELECT`、`UPDATE`、`DELETE` 中解析并忽略 `USE`/`IGNORE`/`FORCE` `INDEX`/`KEY`，并通过 `(tableoid, ctid)` 关联目标表自引用以支持带提示的 `DELETE FROM target USING ...`（315 项断言）。 |
| `WP10` · 待绑定外键 owner 权限（`2a7f1e7`） | 绑定待处理外键前（含超级用户执行 `pg_restore` 时）校验子表 owner 当前的父模式 `USAGE` 与父表/列 `REFERENCES` 权限；缺权限时发 `1142` 告警并保持待绑定，不中断父表 DDL（46 项断言）。 |
{.wide .expand}

## 最终正确性修复 {#final-fixes}

针对 `f0dc476`、`aa25342`、`6f9c4f3` 与 `a000baa` 的多轮独立审查先后发现了残余的错行更新/删除路径、旧驱动元数据问题及排序性能退化。四个提交在不新增扩展版本号（仍为 `1.9`）的前提下全部收口：

| 修复项与提交 | 修复前缺陷 | `6a93e8f` / `v18.6.1` 最终行为 |
| --- | --- | --- |
| `F1` · 超 `UINT64_MAX` 正数越界（`aa25342`） | `sql_mode=''` 或 `IGNORE` 下，超过 `18446744073709551615` 的输入在 `mys_lenient_int` 中被夹到 `INT64_MAX`，导致 `ODKU` 误更新或 `REPLACE` 误删除已有的 `INT64_MAX` 行。 | 任何大于 `9223372036854775807` 的 `BIGINT UNSIGNED` 正数写入在所有模式及 `IGNORE` 下均直接报 `1264`（`src/mys_semantics.c` 中的 `mys_lenient_int`），完整回滚语句与触发器副作用。 |
| `F2` · `FIND_IN_SET` 尾空格（`aa25342`） | `PAD SPACE` 相等比较导致 `FIND_IN_SET` 把带尾空格与不带尾空格的列表项误判为相等。 | `sql/aux_mysql_fix_compat.sql` 中的 `mysql.find_in_set` 在 `text` 与 `bigint` 重载上同时要求排序规则相等且尾部空格字节数相等，不改变 `FIELD`、`STRCMP`、`LIKE`、`IN`。 |
| `F3` / `F6` · 布尔拼接与 `CHAR`/`VARCHAR` 条件重载（`aa25342`） | 布尔 `CONCAT` / `GROUP_CONCAT` 输出 `'t'`/`'f'`；混合 `CHAR`/`VARCHAR` 的 `IF()` 与 `IFNULL()` 因重载歧义报错。 | 布尔拼接输出 `'1'`/`'0'`；`bpchar`/`varchar`/`text` 与 `bool` 的 `IF`/`IFNULL` 重载无歧义解析，并纳入生成列白名单。 |
| `F9` · 结果集字符集编号（`aa25342`） | 字符结果列报告 MySQL 8 字符集编号 `255`（`utf8mb4_0900_ai_ci`），导致旧版 MySQL 5.7 驱动解析失败。 | 文本与预备协议中字符列统一报告 `45`（`utf8mb4_general_ci`），二进制列保持 `63`，通过 Connector/J `5.1.49` 实测。 |
| `F10` · 连接字符集初始化语法（`aa25342`） | 带引号字符集名、`SET NAMES ... COLLATE ...`、`SET NAMES DEFAULT`、`SET CHARACTER SET`、`SET CHARSET` 解析失败。 | 上述写法全部可执行并同步更新会话变量，遇到字符集/排序规则近似时发 `1105` 告警（`src/mysm/systemVar.c` 中的 `set_connection_charset`）。 |
| 新编译器类型安全（`aa25342`） | 隐式函数声明与整数/指针隐式转换在新版编译器上报错。 | 在 Rocky Linux 10.2 `GCC 14.3.1` 将隐式函数声明与 int-conversion 视为错误的前提下顺利编译并通过核心回归与 `release_fixes.py`。 |
| 布尔数值与字符写入（`6f9c4f3`） | `sql_mode=''` 下字面量 `TRUE` 经 `'true'` 转为数值 `0`（`1265`），且隐式 `text(bool)` 向字符列写入 `'true'`/`'false'`（或截断为 `'fals'` / 报 `1406`），导致 `ODKU`/`REPLACE` 改错行。 | `bool_literal_value` 将 `TRUE`/`FALSE` 字面量转为 `1`/`0`，隐式 MySQL 布尔到字符赋值改经 `int4(bool)` 写入 `'1'`/`'0'`，同时保留原生 PG 会话 `true::text = 'true'`。 |
| 布尔向 `DECIMAL`、浮点与二进制转换（`a000baa`） | 将谓词、`IF()` 或 `TRUE`/`FALSE` 写入 `DECIMAL`、`FLOAT`/`DOUBLE`、`BINARY`/`VARBINARY`/`BLOB` 在 1,640 组探测用例中报 `1105`。 | 新增六个从 `pg_catalog.bool` 到 `numeric`、`float4`、`float8`、`bytea`、`mysql.binary_n`、`mysql.varbinary_n` 的 `ASSIGNMENT` 转换及 C 实现函数（`sql/aux_mysql_fix_compat.sql`）。 |
| 字符布尔 `DEFAULT` 与 `LIKE`（`6a93e8f`） | `VARCHAR`/`CHAR DEFAULT TRUE/FALSE` 在 `a000baa` 上仍展开为 `'true'`/`'false'`，导致省略该列的 `ODKU`/`REPLACE` 误命中键值为 `'true'` 的无关旧行；`CREATE TABLE ... LIKE` 也会丢弃列默认值。 | 在 `CREATE`/`ALTER` 保存默认值时规范化布尔常量，并将 `mys_assign_bool_as_int` 移至 `DEFAULT` 展开之后的 `mys_planner` 钩子（`src/mys_utility.c`，无需迁移目录即可兼容 `1.5` 继承的旧默认值），同时开启 `CREATE_TABLE_LIKE_DEFAULTS` 且保持独立自增序列。 |
{.wide .expand}

### 为什么必须在唯一键判定前处理默认值展开 {#default-example}

在验收前分支顶点 `a000baa`（`6a93e8f` 与 `v18.6.1` 合入前）上，插入时若省略声明了 `VARCHAR UNIQUE DEFAULT TRUE` 的列，默认值会展开为 `'true'` 而非 `'1'`，进而使 `ON DUPLICATE KEY UPDATE` 误改——或 `REPLACE` 误删——原本键值为字符串 `'true'` 的无关旧行：

```sql
SET sql_mode='';
CREATE TABLE d (
    id INT PRIMARY KEY,
    k VARCHAR(20) UNIQUE DEFAULT TRUE,
    note VARCHAR(20)
);
INSERT INTO d VALUES (10, 'true', 'old');
INSERT INTO d(id, note) VALUES (20, 'new')
    ON DUPLICATE KEY UPDATE note='changed';
SELECT id, k, HEX(k), note FROM d ORDER BY id;
DROP TABLE d;
```

候选 `6a93e8f` 与 MySQL 5.7.32 均保留 `(10, 'true', '74727565', 'old')`、新增 `(20, '1', '31', 'new')`，并返回影响行数 `1`（执行 `REPLACE INTO d(id, note) VALUES (20, 'new')` 同样保留两行）。而在 `a000baa` 上，`ODKU` 只留下被篡改的 `(10, 'true', 'changed')`，`REPLACE` 则删掉 `id = 10` 只剩 `(20, 'true', 'new')`，返回影响行数 `2` 且没有任何 warning。真正带引号的字符串默认值（`DEFAULT 'true'`）与原生 PostgreSQL 会话保持 `'true'` 不变；历史版本已经落库的错误 `'true'` 数据不会自动改写。

## 排序与 FIND_IN_SET 性能修正 {#performance}

早期 `1.9` 提交（`aa25342`）在每次调用 `general_strncoll` 时都会动态构造并释放完整双字节权重数组，且禁用了 `utf8mb4_general_ci` 与 `utf8mb4_bin` 的缩略排序键，导致 `ORDER BY` / `GROUP BY` / `CREATE INDEX` 相比 `v18.6` 出现数十倍性能退化（开发探针 30 万行排序从 `92 ms` 退化至 `3,845 ms`）。

提交 `6f9c4f3`（`src/mys_prefix.c` 中的 `general_strncoll` 与 `general_strnxfrm_prefix`）改为直接流式比较字符权重（对 ASCII 字符使用基于同一份 MySQL 5.7 权重表的 128 项查表，遇到首个不同权重立即返回），并提供以空格权重（`0x20`）填充的 `strnxfrm_prefix` 缩略排序键，使其 `memcmp` 顺序与 `PAD SPACE` 完全一致，同时保留独立的去尾空格 `strnxfrm` 用于哈希相等键。

由于 `FIND_IN_SET` 内部按调用者排序规则执行 `item = $1` 比较，更快的排序规则比较也一并降低了其开销。**`FIND_IN_SET` 当前仍是 SQL 函数实现**（`sql/aux_mysql_fix_compat.sql` 中的 `mysql.find_in_set`），并未改写为 C 函数。在 2026-11-10 的最终十轮交错验收采样中（Rocky Linux 9.8 `aarch64`，`GCC 11.5.0 -O2` release 构建，300,000 行，`work_mem = 64MB`，关闭 JIT 与并行工作进程，预热 1 次 + 交错采样 10 轮）：

- **`ORDER BY`（32 字符 MD5 字符串，`utf8mb4_general_ci`，`EXPLAIN (ANALYZE, TIMING OFF)`）**：候选 `6a93e8f` 中位数 **`63.82 ms`**，对比已发布 `v18.6` 的 **`102.24 ms`**（缩短约 38%；`a000baa` 中位数 `59.97 ms`，共享宿主上样本区间重叠）。
- **`FIND_IN_SET`（8 项列表全表聚合，客户端完整耗时）**：候选 `6a93e8f` 中位数 **`0.677 s`**，对比已发布 `v18.6` 的 **`3.049 s`**（缩短约 78%），但因逐行调用 SQL 函数与数组展开开销，**仍比 MySQL 5.7.32（三次采样中位数约 `0.073 s`）慢约 9 倍**。

以上数据仅证明此前 `1.9` 的数倍排序退化已在验收夹具上消除，不构成通用硬件或业务查询的性能承诺。完整样本区间与方法见[最终验收性能裁决](/openhalo/18/acceptance/#performance)。

## 明确延期范围与有限差异 {#deferred}

按既定版本范围裁决，`aux_mysql 1.9` 明确延期原生 `ENUM`/`SET`、负数或 `>= 24 小时` 的 `TIME` 时长、MySQL `TIMESTAMP` 跨时区存储换算、完整无符号 64 位（`> INT64_MAX`）存储与表达式、布尔算术及 `AVG`/`MIN`/`MAX`/`STD`/`BIT_*` 布尔聚合、跨类型 `IF`/`IFNULL`/`COALESCE`/`GREATEST`、多参数 `GROUP_CONCAT`、`DELETE target FROM ... JOIN ...` 与多目标 DML、裸字面量/变量排序规则传播、MySQL 存储过程/触发器体/事件、`JSON_*` / 空间函数，以及 MySQL binlog/GTID 复制。

同时保留三项范围明确的 `1.9` 有限差异：`PAD_CHAR_TO_FULL_LENGTH` 下 `LENGTH()` 等未重载函数仍接收去尾空格文本；二进制数字 `CAST` 可能拒绝 `1e1000000` / `1e-1000000` 等极端指数及负数 `SIGNED` 溢出；多字节 UTF-8 字符串上的空串搜索 `LOCATE('', multibyte_str, pos)` 在边界位置返回字符位置而非字节偏移。各项限制的详细行为与迁移规避方式见[兼容边界](/openhalo/18/compatibility/)。
