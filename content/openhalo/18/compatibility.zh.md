---
type: docs
upstream_link: ""
search_keywords: ["BIGINT UNSIGNED", "INT64_MAX", "NUL", "ENUM", "SET", "REPEATABLE READ", "FIND_IN_SET", "unicode_ci", "collation_connection", "COALESCE", "PAD_CHAR_TO_FULL_LENGTH", "ANSI_QUOTES", "wait_timeout", "TIMESTAMP", "3819", "sql_mode", "排序规则", "隔离级别"]
title: 兼容边界
description: aux_mysql 1.9 在精确兼容范围、有意映射、仅回显设置、不支持特性、同库原生 PostgreSQL 影响及错误码上的权威参考。
weight: 30
---

本页构成 **`aux_mysql 1.9` 兼容约定**（于 `6a93e8f` 通过源码验收并发布于源码标签 `v18.6.1`）的核心部分。[源码验收取得有条件 GO](/openhalo/18/acceptance/) 以准确披露以下边界为前提。回归套件通过不代表完整等价于 MySQL 5.7，也不能免除具体业务在模式、SQL、事务与驱动层面的迁移验证。

## 数据表示与存储上限 {#representation}

| 类型 / 范围 | OpenHalo 18 实际边界 | 对应用与迁移的影响 |
| --- | --- | --- |
| `BIGINT UNSIGNED` | 基于有符号 `int8` 的域 `mysql."bigint unsigned"`，仅可存储 **`0..9223372036854775807`（`INT64_MAX`）**。一切大于 `INT64_MAX` 的正数写入——无论落在 `INT64_MAX + 1 .. UINT64_MAX` 还是超过 `UINT64_MAX`，涵盖字面量、字符串、表达式、`INSERT SELECT`、`ODKU`、`REPLACE` 与二进制 `COM_STMT_EXECUTE` 无符号参数——**在任何 `sql_mode` 及 `IGNORE` 下均直接报 `1264` 错误**，并在进入唯一键冲突判定前回滚整条语句副作用。非严格模式（及 `IGNORE`）下负数夹为 `0` 并告警 `1264`；严格模式不带 `IGNORE` 的负数写入触发域检查错误 **`3819`**（而非 MySQL 的 `1264`）。 | 审查 64 位无符号主键、哈希 ID 与 `UUID_SHORT()` 消费方。高半区 `uint64` 值无法落库，既不会饱和为 `UINT64_MAX`，也不会静默夹到已有 `INT64_MAX` 唯一键。`CAST(expr AS UNSIGNED)` 底层落到有符号 `int8`（`CAST(-1 AS UNSIGNED)` 返回 `-1` 而非 `18446744073709551615`），超过 `INT64_MAX` 的十六进制算术同样报错。 |
| `CHAR` / `VARCHAR` / `TEXT` 中的 `NUL` | 使用原生 PostgreSQL 字符类型（`bpchar`、`varchar`、`text`）。凡含 `NUL` 字节（`0x00`）的写入**在所有 `sql_mode`（含 `INSERT IGNORE`）下均报 `1366` 错误**。`TINYTEXT`、`TEXT`、`MEDIUMTEXT`、`LONGTEXT` 在 `SHOW CREATE TABLE` 和 `information_schema.COLUMNS` 中统一显示为 `text`。 | 绝不会为使写入成功而静默剥离或替换字节。业务数据确实包含 `0x00` 或任意字节时，应显式改为 `BINARY`、`VARBINARY` 或 `BLOB`，并一并评估长度、比较规则和索引。 |
| 二进制转字符 | 将 `BINARY`、`VARBINARY`、`BLOB` 赋值或 `CAST` 为字符类型时，会对整个载荷校验 UTF-8。任何 `0x00`（**含 `BINARY(n)` 尾部自动补零**）或非法 UTF-8 即使带 `IGNORE` 也报 `1366`。 | 不要对补零的 `BINARY(n)` 或非 UTF-8 原始字节使用 `CAST(binary_col AS CHAR)`；应在二进制侧先行裁剪 `0x00` 或保持二进制类型。 |
| 旧版 `1.5` `BINARY` / `VARBINARY` | `1.8` 之前的 `mysql.binary` 与 `mysql.varbinary` 是丢弃了声明长度的 `bytea` 域；`1.5 → 1.9` 升级保留原列类型与落库字节。 | 需对照原始 MySQL DDL 找回 `(n)` 长度，审查后执行 `ALTER TABLE ... MODIFY` 切换至带补零和长度约束的 `mysql.binary_n` / `mysql.varbinary_n`。 |
| `DECIMAL` 元数据 | 裸 `DECIMAL` 默认为 `DECIMAL(10,0)`。表达式、视图或原生 PG 创建的无 typmod `numeric` 列导出为 `decimal(65,30)` 并伴随 `1105` 告警。 | 回放 `decimal(65,30)` 最多保留 `35` 位整数和 `30` 位小数；转储回放前需核查是否存在更宽的无界 `numeric` 值。 |
| `FLOAT` / `DOUBLE` / `REAL` | 新建不带精度的 `FLOAT` / `FLOAT(0..24)` 使用 `float4`（协议类型 `FLOAT`）；`DOUBLE`、`REAL` 与 `FLOAT(25..53)` 使用 `float8`（`REAL_AS_FLOAT` 不会把 `REAL` 切换为 `float4`）。废弃语法 `FLOAT(M,D)` / `DOUBLE(M,D)` 不执行小数位四舍五入约束。科学计数字面量如 `1.5e0` 解析为 `numeric` 而非 `DOUBLE`。 | 升级不会收窄既有 `float8` 列；需要保留 64 位双精度时应显式声明 `DOUBLE`。 |
| `DATETIME` 与 `TIMESTAMP` | `DATETIME[(0..6)]` 与不带时区子句的 MySQL `TIMESTAMP[(0..6)]` **均映射为 PostgreSQL `timestamp without time zone`**（默认精度 `0`；`SHOW CREATE TABLE` 可能规范化显示为 `timestamp(n)`）。不支持零日期（`0000-00-00`）。 | 裸 `TIMESTAMP` 列读写时**不会按会话 `time_zone` 与 UTC 做跨时区换算**（不同于 MySQL `TIMESTAMP`），首个 `TIMESTAMP NOT NULL` 列也不会隐式附加 `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`，需要时须显式声明。 |
| `ENUM` 与 `SET` | 明确不支持（报 `1091`：`type "enum"` / `"set" does not exist`）。 | 显式转换为带 `CHECK` 的 `text`、原生 PG `ENUM` 或整数位掩码，并改造依赖序数排序或位运算的查询；参见[迁移转换示例](/openhalo/18/migration/#mysql)。 |
| `TIME` 时长 | 映射为日内时刻 `time without time zone`，负数（如 `'-01:00:00'`）及 `>= 24:00:00` 的时长会报错。 | 耗时/时长字段请改用 PostgreSQL `interval` 或整数秒/微秒，并适配客户端解码逻辑。 |
| `BIT`、用户变量与时间/JSON 写入 | 已测路径中 `BIT(n)` 结果列按文本 `'1'` 返回而非单字节 `0x01`；`@user_var` 数值类型推断与 MySQL 有差异；向 `DATE`/`TIME`/`DATETIME`/`TIMESTAMP`、`YEAR`、`JSON` 写入布尔或整数表达式会报错；向 `BINARY`/`VARBINARY`/`BLOB` 直接赋整数表达式也会报错。 | 请实测驱动对 `BIT` 列的解码结果，并对时间、JSON 与二进制列提供显式格式化的值，不要依赖隐式整数或布尔转换。 |
{.wide .expand}

```sql
CREATE TABLE u64_demo (id INT PRIMARY KEY, u BIGINT UNSIGNED UNIQUE);
INSERT INTO u64_demo VALUES (1, 9223372036854775807);

-- Fails with error 1264 even under IGNORE; row (1, 9223372036854775807) is untouched:
-- INSERT IGNORE INTO u64_demo VALUES (2, 18446744073709551615);
-- REPLACE INTO u64_demo VALUES (2, 18446744073709551616);

SET sql_mode = '';
INSERT INTO u64_demo VALUES (2, -1);   -- Clips to 0 with warning 1264
SET sql_mode = 'STRICT_TRANS_TABLES';
-- INSERT INTO u64_demo VALUES (3, -1); -- Fails with domain check error 3819
```

## 排序规则、字符集与字面量传播 {#collations}

| 请求的设置或写法 | OpenHalo 18 实际行为 |
| --- | --- |
| `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_bin`、`utf8mb4_bin` | **`mysql` 模式下的四个专用精确实现**：`general_ci` 实现 MySQL 5.7 BMP 大小写/重音权重（`> U+FFFF` 补充平面字符映射为权重 `0xFFFD`，与 MySQL 5.7 `utf8mb4_general_ci` 一致），`bin` 实现 UTF-8 码点顺序，两者均遵守 `PAD SPACE`。 |
| 其他以 `_ci` 结尾的排序规则（如 `utf8mb4_unicode_ci`、`utf8mb4_0900_ai_ci`、`latin1_swedish_ci`） | 在 DDL、表达式 `COLLATE`、视图、`CREATE TABLE AS` 与 `SET NAMES ... COLLATE` 中映射为 `utf8mb4_general_ci`（`SET NAMES utf8` 下为 `utf8_general_ci`），并发出 **`1105` 告警**。 |
| 其他非 `_ci` 排序规则（如 `latin2_czech_cs`、`ascii_bin`） | 映射为 `utf8mb4_bin`（或 `utf8_bin`），并发出 **`1105` 告警**。 |
| 近似映射后的 `SHOW CREATE TABLE` | 直接展示实际生效的排序规则（`utf8mb4_general_ci` / `utf8mb4_bin`）或 OpenHalo 别名（`case_insensitive` / `case_sensitive`），不伪装成未实现的区域规则。 |
| 非 UTF-8 字符集（`latin1`、`gbk`、`ucs2`、`utf16`、`utf32`） | 底层存储与协议传输始终为 UTF-8；`SET NAMES` / `CONVERT(... USING ...)` 映射为 `utf8mb4` 并告警 `1105`，不做单字节或 UTF-16/32 转码。DDL 中显式写 `CHARACTER SET ascii` 仍存在解析器关键字缺口（报 `1064`）。 |
| `SET NAMES ... COLLATE ...` 对比 `SET collation_connection = ...` | `SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'` 会发出 `1105` 告警并将 `@@collation_connection` 设为实际生效的 `'utf8mb4_general_ci'`。而直接执行 `SET collation_connection = 'utf8mb4_unicode_ci'` **不发告警**，在 `SELECT @@collation_connection` 中原样回显 `'utf8mb4_unicode_ci'`，但并不会启用 `unicode_ci`。 |
| 裸字符串字面量与 `@vars` | **排序规则传播尚不完整。** 即使已执行 `SET NAMES utf8mb4 COLLATE utf8mb4_general_ci`，两个裸字面量仍使用 PostgreSQL 数据库默认排序规则（`C` / UTF-8 字节序）比较；表列引用或显式带 `COLLATE` 的表达式则按 MySQL 排序规则比较。 |
| 历史 ICU 排序规则（`case_insensitive`、`case_sensitive`、`ignore_accents`） | 为兼容旧表与旧索引原样保留，`ALTER EXTENSION` 升级不会就地改写既有对象。 |
{.wide .expand}

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;

-- Bare literals compare case-sensitively (returns 0, -1, 0; MySQL 5.7 returns 1, 0, 1):
SELECT 'A' = 'a', STRCMP('A', 'a'), FIND_IN_SET('A', 'a,b');

-- Column expressions and explicit COLLATE clauses use utf8mb4_general_ci (returns 1, 1):
SELECT ('A' COLLATE utf8mb4_general_ci) = 'a',
       FIND_IN_SET('A' COLLATE utf8mb4_general_ci, 'a,b');
```

在覆盖 MySQL 5.7 全部 `221` 个非二进制排序规则 × `3` 种字符列类型的 `collation_all` 扫描（共 **9,945 项断言**）中，所有查询均无报错地符合上述 `general_ci`/`bin` 映射约定，同时明确记录了 **246 组与所请求 MySQL 区域规则的预期差异**：其中 `latin2_czech_cs` 占 `3` 组（`_cs` 映射到区分大小写的 `bin` 而非捷克语权重），`ucs2_*`/`utf16_*`/`utf16le_*` 占 `165` 组、`utf32_*` 占 `78` 组（均源于 `LOCATE('', s, 2)` 在 UTF-8 存储下返回 `2`，而在 MySQL 双字节/四字节编码下返回字节偏移 `3`/`5`）。迁移原先依赖 `unicode_ci` 或特定语言排序规则的表之前，务必先在 `utf8mb4_general_ci` / `utf8mb4_bin` 下排查是否产生新的唯一键重复。

## 事务、隔离级别映射与影响行数 {#transactions}

| MySQL 事务 / DML 结构 | OpenHalo 18 实际生效行为 | 对应用的影响 |
| --- | --- | --- |
| `READ UNCOMMITTED` / `READ COMMITTED` | PostgreSQL `READ COMMITTED`。 | 标准语句级已提交读快照，不存在脏读。 |
| **读写 `REPEATABLE READ`**（默认） | **PostgreSQL `READ COMMITTED`**（明确的产品设计选择）。 | 避免常见遗留并发更新/删除负载触发 PostgreSQL 可重复读的 `40001` 序列化中止，**但同一读写事务内的多次普通 `SELECT` 会看见其他会话新提交的行**。 |
| **只读 `REPEATABLE READ`**（`START TRANSACTION READ ONLY` / `SET TRANSACTION READ ONLY`） | **PostgreSQL `REPEATABLE READ`**（真正稳定的事务快照）+ 只读拦截（写操作报 `1792`）。 | 多查询对账或一致性报表需要稳定快照时，应显式改用只读事务或 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。 |
| `START TRANSACTION WITH CONSISTENT SNAPSHOT` | **当有效 MySQL 隔离级别为默认的 `REPEATABLE READ` 时**立即获取 **PostgreSQL `REPEATABLE READ`** 快照；在 `READ COMMITTED`、`READ UNCOMMITTED` 或 `SERIALIZABLE` 下发出 **`138` 告警**并忽略该子句（与 InnoDB 一致）。 | 需要跨多次 `SELECT` 的一致时间点快照时，请将会话/下一事务隔离级别保持在 `REPEATABLE READ`。 |
| `SERIALIZABLE` | PostgreSQL SSI `SERIALIZABLE`（流复制热备库上回退为 `REPEATABLE READ`），序列化冲突映射为 MySQL 死锁错误码 **`1213`（`SQLSTATE 40001`）**。 | 已按 `1213` / `40001` 实现重试循环的应用可正常工作；加锁时机不同于 InnoDB 共享读锁。 |
| 并发删除重插竞争 | 采用 PostgreSQL MVCC 元组可见性加 btree 唯一检查，而非 InnoDB 间隙锁 / next-key 锁。 | 两个会话并发对同一键执行 `DELETE` + `INSERT` 时，后等待的 `DELETE` 在前序会话提交新行后可能匹配 `0` 行，随后 `INSERT` 触发 `1062` 唯一冲突。 |
| 语句级回滚（`mysql.statement_rollback = on`） | 在显式事务内为每条语句建立隐藏保存点（占用 `subxid`）。 | 单个事务超过 **64 条写语句**会溢出后端 `PGPROC` 的 `subxid` 缓存并放大快照开销。大批量写入请改用自动提交、分批提交，或在确认失败回滚语义后评估 `mysql.statement_rollback = off`。 |
| `INSERT ... ON DUPLICATE KEY UPDATE` 行数 | 插入一行计 `1`；冲突更新且落库值实际改变计 `2`；冲突但值未变计 `0`（客户端开启 `CLIENT_FOUND_ROWS` 时计 `1`）。 | 与 MySQL 5.7 影响行数规则一致。 |
| `REPLACE INTO` 行数 | 无冲突插入——或在仅含单个唯一索引、无行级 `DELETE` 触发器（含入站外键 `ON DELETE` 触发器）且全列值完全相同时——计 `1`；实际执行物理删旧插新时计 `1 + deleted_rows`（跨多个唯一键删多行时按实际删除行数累加）。 | 与 MySQL 5.7 InnoDB 计数规则一致。 |
| **普通 `UPDATE` 行数** | 始终返回**匹配行数**，即使未开启 `CLIENT_FOUND_ROWS` 且列值并未改变。 | 依赖“值未变时 `UPDATE` 返回 `0` 行”的乐观锁或 ORM 更新断言会拿到 `1`，迁移时必须核查。 |
{.wide .expand}

```sql
CREATE TABLE counters (id INT PRIMARY KEY, v INT NOT NULL);
INSERT INTO counters VALUES (1, 10);

-- Plain UPDATE returns 1 (matched) even though v is already 10 (MySQL without CLIENT_FOUND_ROWS returns 0):
UPDATE counters SET v = 10 WHERE id = 1;

-- ODKU distinguishes unchanged (0 without CLIENT_FOUND_ROWS) vs changed (2):
INSERT INTO counters VALUES (1, 10) ON DUPLICATE KEY UPDATE v = VALUES(v); -- 0 affected
INSERT INTO counters VALUES (1, 11) ON DUPLICATE KEY UPDATE v = VALUES(v); -- 2 affected
```

## 接受的语法设置与实际生效行为 {#accepted-vs-implemented}

切勿仅因 `SET` 执行成功、`SELECT @@var` 能回显新值，或某段 DDL/DML 解析不报错，就假定对应 MySQL 行为已经生效：

| 设置或语法 | 是否接受 / 回显 | 实际运行期行为 |
| --- | --- | --- |
| `USE` / `IGNORE` / `FORCE` `INDEX` 或 `KEY` | 在 `SELECT`、`UPDATE`、`DELETE` 中接受解析 | **忽略不执行**，由 PostgreSQL 优化器按统计信息选择路径。 |
| `auto_increment_increment`、`auto_increment_offset` | 在 `@@variables` / `SHOW VARIABLES` 中可修改并回显 | **未接入序列分配**，非默认值不改变步长与偏移，自增始终按步长 `1` 递增（`1, 2, 3, ...`）。 |
| `wait_timeout`、`interactive_timeout`、`innodb_lock_wait_timeout` | 可修改并回显 | **未联动** PostgreSQL 的 `idle_session_timeout` 或 `lock_timeout`；设置 `wait_timeout` 不会主动断开空闲 MySQL 连接，请在 `postgresql.conf` 或 `ALTER ROLE` 中配置 PG 超时参数。 |
| `sql_mode`：`STRICT_TRANS_TABLES`、`STRICT_ALL_TABLES`、`ERROR_FOR_DIVISION_BY_ZERO`、`NO_AUTO_VALUE_ON_ZERO`、`NO_BACKSLASH_ESCAPES`、`PAD_CHAR_TO_FULL_LENGTH`、`NO_ZERO_DATE`、`NO_ZERO_IN_DATE`、`ALLOW_INVALID_DATES` | 可修改并回显 | **实际生效**于已覆盖的赋值转换、词法转义、`AUTO_INCREMENT`、`CHAR` 提取及日期运算符路径（有限例外见下节）。 |
| `sql_mode`：`ANSI_QUOTES`、`PIPES_AS_CONCAT`、`REAL_AS_FLOAT`、`IGNORE_SPACE`、`NO_UNSIGNED_SUBTRACTION`、`HIGH_NOT_PRECEDENCE` | 可修改并回显 | **未实现对应切换**：开启 `ANSI_QUOTES` 后 `"..."` 仍是字符串字面量而非标识符，开启 `REAL_AS_FLOAT` 后 `REAL` 仍映射为 `float8`。 |
| `sql_mode`：`ONLY_FULL_GROUP_BY` | 设置后可回显（初始默认 `@@sql_mode` 串中未列出该项） | **PostgreSQL 分组规则始终生效**：清空 `SET sql_mode=''` **不会**放开非聚合且无主键函数依赖的 `SELECT` 列。 |
| `SET collation_connection = '...'` | 原样接受并回显 | **不做校验、近似映射或字面量传播**；查看实际映射规则与 `1105` 告警应使用 `SET NAMES ... COLLATE ...`。 |
| `ENGINE=InnoDB` / `MyISAM` 对比 `ENGINE=<pg_am>` | 接受语法 | `InnoDB`/`MyISAM` 使用默认 `heap`；已安装的 PG 表访问方法（如 `orioledb`）按名启用；`ENCRYPTION='Y'` 要求已安装 `pg_tde`（`tde_heap`），否则直接报错。 |
| `CREATE TABLE` 中的 `CHECK (...)` | 接受并**强制检查** | PostgreSQL 真正执行 `CHECK` 约束（MySQL 5.7 仅解析并忽略 `CHECK`）。 |
{.wide .expand}

## 表达式、函数与不支持的 SQL 形式 {#expressions}

| 范围 | 当前边界 |
| --- | --- |
| 布尔表达式与聚合 | 布尔写入（`1`/`0`、`'1'`/`'0'`）、`CONCAT`/`GROUP_CONCAT`、`IF(cond, TRUE, FALSE)` 以及 **`SUM(bool)`**（返回 `bigint`）均可用。**布尔算术**（`(1>0)+0`、`(status='paid')*amount`）、**其余布尔聚合**（`AVG`、`MIN`、`MAX`、`STD`、`BIT_OR`、`BIT_AND`、`BIT_XOR`，报 `1305`）、布尔上的数值函数（`ROUND`、`ABS`）以及跨类型 `COALESCE` / `GREATEST` 尚不支持；算术与均值/最值查询请显式包裹为 `IF(cond, 1, 0)` 或 `CASE WHEN cond THEN 1 ELSE 0 END`。 |
| 混合类型条件表达式 | `IF()` 与 `IFNULL()` 支持 `CHAR` / `VARCHAR` / `TEXT` 混用；但跨类型族组合如 `COALESCE(int_col, varchar_col)`（`1105`）、`IF(cond, int_col, varchar_col)`（`1305`）、`COALESCE(1, 'a')`（`1366`）、`IFNULL(varbinary_col, char_col)`（`1305`）需显式 `CAST(... AS CHAR)`。 |
| `GROUP_CONCAT` | 单参数 `GROUP_CONCAT([DISTINCT] expr [ORDER BY ...] [SEPARATOR ...])` 支持字符、布尔与原始二进制列；多参数 `GROUP_CONCAT(a, b)` 尚未支持，请改写为 `GROUP_CONCAT(CONCAT(a, b))`。 |
| `FIND_IN_SET` | `text` 与 `bigint` 重载已修正排序规则与尾空格匹配，但 `DECIMAL` 参数重载（如 `FIND_IN_SET(2.0, '1,2,3')`）报 `1305`。当前为 SQL 函数实现，30 万行扫描耗时约为 MySQL 5.7 的 9 倍。 |
| 未实现的 MySQL 函数与命令 | MySQL `JSON_*`（`JSON_EXTRACT`、`JSON_SET` 等）、空间函数（`POINT`、`ST_Distance`）、全文检索 `MATCH ... AGAINST`、`SHA1`、`CRC32`、`TO_BASE64`、`QUOTE`、`SOUNDEX`、`ORD`、`CHAR()`、`LOAD DATA INFILE`、`SELECT ... INTO OUTFILE` 及 `SHOW DATABASES LIKE ...` 尚未实现。 |
| 多表 `DELETE` 与多目标 DML | 支持单目标表 `DELETE FROM target USING ...` 与 `UPDATE ... JOIN ...`。**`DELETE target FROM target JOIN ...`**、逗号连接 `DELETE target FROM a, b ...`、`LEFT JOIN` 清理孤儿行写法，以及**多目标表同时 `UPDATE` / `DELETE`** 均报语法错误 `1064`。 |
| 多语句包的原始语法错误 | 在已开启的显式事务块内且启用 `mysql.statement_rollback = on` 时，语法错误会延后到隐藏保存点保护的标记语句上报错，保留事务内此前已完成的语句；在未开启显式事务块时（如 `autocommit=1` 下的 `INSERT ...; BAD SQL;`），解析器会先解析整个 `COM_QUERY` 报文并在第一条语句执行前整包报错。 |
| 存储程序、触发器体与事件 | 不支持原生 MySQL `CREATE PROCEDURE` / `FUNCTION`（`BEGIN ... END` 复合体）、MySQL 触发器语法体及 `CREATE EVENT`。升级测试夹具中使用的 PostgreSQL `BEGIN ATOMIC` / `DO ... LANGUAGE` 属于 PG 语法，不代表支持 MySQL 存储例程。 |
| 协议与会话控制 | 不支持 MySQL Unix 域套接字、`COM_CHANGE_USER`、MySQL `KILL [QUERY]`、`COM_STMT_FETCH` 服务端游标（`1421`）及 `mysql_native_password` 挑战-响应；`3306` 端口仅支持 `scram-sha-256`、`md5`、`password`、`trust`、`reject` 五种 `pg_hba.conf` 方法（其余报 `1045`），单会话预备语句上限为 `16,382`（超限报 `1461`）。 |
{.wide .expand}

以下三项范围明确的行为差异在 `1.9` 中作为已知边界保留：

- **未单独重载的字符串函数在 `PAD_CHAR_TO_FULL_LENGTH` 下的行为**：落库字节及 WP3 覆盖函数（`CONCAT`、`CAST`、`HEX`、`GROUP_CONCAT` 等）保留 `CHAR(n)` 完整补空格长度，但未提供 `bpchar` 专用重载的函数（如 `LENGTH(char_col)`）仍会收到隐式去尾空格后的 `text` 值。
- **二进制数字 `CAST` 的极端输入**：`CAST(binary_val AS SIGNED)` / `DECIMAL` 可能直接拒绝 `1e1000000` / `1e-1000000` 等极端指数及负数 `SIGNED` 溢出；含非法尾部的二进制 `DECIMAL` 统一发 `1292` 告警（MySQL 5.7 则视来源类型在无告警、`1292`、`1366` 间变化）。
- **多字节 UTF-8 字符串上的空串 `LOCATE`**：`LOCATE('', multibyte_string, pos)` 在边界位置返回字符位置，而非 MySQL 的字节/代码单元偏移。

## 索引、生成列与外键 {#objects}

- **`mysql_prefix` 索引扫描限制**：带显式 `(col(n))` 前缀或包含 `TEXT`、`BLOB`、超宽 `VARCHAR` 的键使用 `mysql_prefix` 访问方法，查询和唯一性检查始终需要回堆复核，不支持仅索引扫描（Index Only Scan）或直接为 `ORDER BY` 提供有序输出。当大量行共享相同候选前缀时，扫描与冲突复核开销会显著增加；普通有界无前缀键则保留原生 `btree` 优化。
- **键名长度与大小写折叠**：PostgreSQL 物理索引名在 `63` 字节上限中预留 `9` 字节（`$<8位十六进制>`），因此逻辑 MySQL 键名有效上限为 **`54` 字节**（约 18 个 UTF-8 汉字），且仅对 ASCII 字母做不区分大小写匹配。
- **物化的 `VIRTUAL` 生成列**：`VIRTUAL` 生成列在磁盘上实际物化存储，并按**写入会话**当时的 `sql_mode` / `IGNORE` 规则求值，后续读取会话修改 `sql_mode` 不会重算已存行。非确定性函数、会话变量、任意自定义函数以及生成列 `DATE_FORMAT` 中的隐式文本转日期（或 `CAST(CONCAT(...) AS DATE)`）均以 `3102` 拒绝。`VIRTUAL` 主键与引用 `AUTO_INCREMENT` 的生成列属于 OpenHalo 扩展，导出的 DDL 在原生 MySQL 5.7 上无法直接回放。
- **外键父键唯一性与 PostgreSQL 权限模型**：外键必须引用父表上的 `PRIMARY KEY` 或 `UNIQUE` 键且类型兼容；引用普通非唯一父索引即使在 `FOREIGN_KEY_CHECKS=0` 下也会被直接拒绝。父表 `TRUNCATE` 不会级联删除子表。待绑定外键在绑定时（含超级用户执行 `pg_restore`）始终检查子表 owner 当前对父模式的 `USAGE` 与对父表/列的 `REFERENCES` 权限；缺权限时发 `1142` 告警并保持待绑定——这是有意遵循 PostgreSQL 权限边界的设计，而 MySQL 5.7 并不检查对应 `REFERENCES` 授权。

## 同库原生 PostgreSQL 共存、ABI 与历史对象 {#coexistence}

- **`mysql.database` 内的数据库级布尔转换影响**：`aux_mysql 1.9` 注册了六个数据库级 `ASSIGNMENT` 转换（`pg_catalog.bool` 到 `numeric`、`float4`、`float8`、`bytea`、`mysql.binary_n`、`mysql.varbinary_n`）。在安装了 `aux_mysql` 的同一个 PostgreSQL 数据库（默认 `postgres`）中，**原生 PostgreSQL 会话（连接 `5432` 的 `psql`）执行 `SELECT true::numeric` 也会得到 `1`，执行 `SELECT true::bytea` 会得到 `\x31`**；而 `SELECT true::text` 保持 `'true'`，原生 PG 字符列 `DEFAULT true` 也保持 `'true'`。无关的原生 PostgreSQL 业务应部署在未安装 `aux_mysql` 的独立 PostgreSQL 数据库中。
- **内核与第三方扩展 ABI**：尽管 `PG_VERSION` 仍为 `18.6`（`PG_VERSION_NUM = 180006`），OpenHalo 18 修改了协议、解析与计划节点结构（`ClientSocket`、`OnConflictClause`、`ModifyTable`、`pg_locale` 回调），因此 `v18.6` 时期关于“未修改的原生 PGDG C 扩展二进制可直接加载”的旧说明在 `v18.6.1`（`aux_mysql 1.9`）中已不再成立。内核与 `aux_mysql` 必须配套编译；任何第三方 PostgreSQL C 扩展（`pg_tde`、`orioledb`、`PostGIS`、`pgvector` 等）必须基于同一套 OpenHalo 18 头文件重新编译并独立验证，跨协议混用扩展尚未验证。
- **不支持 PG14 物理升级，且升级不自动修复历史数据**：禁止从 OpenHalo PG14（`1.0.14.x`）执行物理 `pg_upgrade`。从 `v18.6`（`aux_mysql 1.5`）升级到 `1.9` 只更新扩展自身目录，**不会自动猜测或修复** `1.5` 丢失的 `BINARY`/`VARBINARY` 长度、丢失的前缀长度、旧 ICU 索引、已丢弃的生成表达式、不安全 `IMMUTABLE` 生成包装函数、`NOT ENFORCED` 外键、孤儿行，以及旧版本写错的 `'true'`/`'false'`/`0` 数据。请按[迁移与升级](/openhalo/18/migration/#audit)逐项审计。

## 运维与诊断限制 {#operations}

- `SHOW STATUS` 与 `performance_schema` 大多为空表或兼容桩；生产监控请使用 PostgreSQL 原生视图（`pg_stat_activity`、`pg_stat_statements`、`pg_locks`、`pg_stat_ssl`）。
- `SHOW WARNINGS` 与 `SHOW ERRORS` 在会话内存中最多保留当前语句的 **64** 条诊断消息，且不逐字复现 MySQL 5.7 的 `sql_mode` 废弃告警（`3090` / `3135`）或英文错误原文。
- 用户级命名锁（`GET_LOCK`）共享 PostgreSQL 锁表容量（`max_locks_per_transaction`）。
- 不提供 MySQL binlog / GTID 复制（`@@gtid_mode = 'OFF'`，`@@gtid_executed = ''`，`@@gtid_purged = ''`），PostgreSQL WAL LSN 也不是 MySQL GTID。原生 `pg_dump` 必须保留扩展管理的触发器，且在需要保留表默认排序规则时不能传入 `--no-security-labels`。

## 错误与告警代码速查 {#diagnostics}

| 代码 | 在 OpenHalo 18（`aux_mysql 1.9`）中的含义 |
| --- | --- |
| `138` | 非 `REPEATABLE READ` 隔离级别下忽略 `WITH CONSISTENT SNAPSHOT` 子句时发出的告警。 |
| `1045`（`28000`） | MySQL 认证失败、`pg_hba.conf` `reject` 规则、`scram-sha-256` 规则下角色仍存 `md5` 密钥，或 `3306` 端口不支持的 `pg_hba.conf` 方法（`peer`、`ident`、`cert`、`gss`、`ldap`、`pam` 等）。 |
| `1047`（`08S01`） | 未支持的 MySQL 线协议命令（如 `COM_CHANGE_USER`）。 |
| `1061` / `1062` | 同表内键名重复 / `PRIMARY` 或 `UNIQUE` 唯一键冲突。 |
| `1064` | SQL 语法错误（含未支持的 `DELETE target FROM ... JOIN ...` 或 `CHARACTER SET ascii`）。 |
| `1091` | 未支持的数据类型查找失败（如 `ENUM` 或 `SET`）。 |
| `1105` | 约定的字符集/排序规则或 `decimal(65,30)` 近似告警——也用于无专用 MySQL 映射码的一般 PG 错误（如 `COALESCE` 类型不兼容），须阅读消息文本。 |
| `1142` | 绑定待处理外键时子表 owner 缺少 `USAGE` / `REFERENCES` 权限（父表 DDL 或恢复期间作为 warning 发出）。 |
| `1180`（`40000`） | 对此前已因报错中止的事务执行 `COMMIT`。 |
| `1213`（`40001`） | `SERIALIZABLE` 序列化冲突或死锁，暴露给客户端供重试。 |
| `1264` | 数值越界：非严格可表示范围内截断为 warning；**`BIGINT UNSIGNED > INT64_MAX` 在任何模式及 `IGNORE` 下始终为 error**。 |
| `1265` / `1292` | 数据截断告警 / 数字前缀格式异常告警（含二进制 `DECIMAL` 转换与 `TEXT + 0`）。 |
| `1290` / `1792` | `GLOBAL read_only` 或 `super_read_only` 拒绝写入 / 只读事务拒绝写入。 |
| `1305` | 函数或运算符重载不存在（如 `AVG(bool)`、`(1>0)+0`、`FIND_IN_SET(decimal, text)`）。 |
| `1365` | 除零（默认返回 `NULL` 并告警；严格写入且开启 `ERROR_FOR_DIVISION_BY_ZERO` 时报错）。 |
| `1366` | 非法字符值或字符转换——**字符列写入 `NUL`（`0x00`）以及非法 UTF-8 / `BINARY(n)` 补零转文本时在任何模式（含 `IGNORE`）下始终报错**。 |
| `1406` / `1411` | 字符串或 `BIT(n)` 超出列定义长度 / `UNHEX()` 含非十六进制字符（返回 `NULL` 并告警）。 |
| `1421` / `1461` | 未开启服务端预备游标导致 `COM_STMT_FETCH` 报错 / 单会话预备语句数量超出上限（`16,382`）。 |
| `1451` / `1452` | 外键阻止父表更新或删除 / 子表写入缺少匹配的父键。 |
| `3057` / `3058` | `GET_LOCK` 锁名超过 64 个字符 / 用户级命名锁等待死锁环。 |
| `3102` / `3105` | 生成列包含不允许的函数或结构 / 显式向生成列写入非 `DEFAULT` 值。 |
| `3819` | PostgreSQL 域 `CHECK` 约束违例（如严格模式不带 `IGNORE` 向 `UNSIGNED` 列写入负数）。 |
{.wide .expand}

请把 `SHOW WARNINGS` 视为兼容性验证的一部分：最终验收同时比对了落库字节、error 代码与 warning 代码，从未仅凭收到 `OK` 包就判定行为一致。
