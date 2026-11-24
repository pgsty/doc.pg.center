---
type: docs
upstream_link: ""
search_keywords: ["AUTO_INCREMENT", "COM_STMT_PREPARE", "COM_STMT_FETCH", "WITH CONSISTENT SNAPSHOT", "FOREIGN_KEY_CHECKS", "GET_LOCK", "ODKU", "ON DUPLICATE KEY UPDATE", "REPLACE", "HEX", "UNHEX", "GROUP_CONCAT", "SHOW CREATE TABLE", "mysql.sum", "前缀索引", "排序规则", "生成列", "VIRTUAL", "STORED", "utf8mb4_general_ci"]
title: 功能集合
description: aux_mysql 1.9 在协议、SQL、DML、事务、数据类型、索引、生成列与运维元数据上的支持程度、核心行为、示例与迁移影响。
weight: 10
---

本参考页说明 OpenHalo 18 在 **`aux_mysql 1.9`**（源码标签 [`v18.6.1` / 已验收提交 `6a93e8f`](/openhalo/18/#versions)）中实际提供的功能。每一类能力均明确列出**支持程度**、**已实现行为**、**已验证 SQL 示例**及**兼容边界与迁移影响**；完整的边界条件与错误码说明见[兼容边界](/openhalo/18/compatibility/)。

## 协议、认证与预备语句 {#protocol}

| 能力 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| 双协议监听 | 已实现 | 同一 PostgreSQL 18.6 postmaster 同时提供 `5432`（PostgreSQL）与 `mysql.port`（`3306`，MySQL TCP）监听。MySQL 数据库映射为 `mysql.database`（默认 `postgres`）中的模式；`USE db` 与 `COM_INIT_DB` 切换 `search_path`。 |
| 认证与 TLS | 已实现 | 支持 MySQL 8 默认的 `caching_sha2_password`（共享内存 stage2 快速认证缓存 + TLS 或自动生成密钥的 RSA-OAEP 完整认证）以及可选的 `mysql_clear_password`（初始握手后通过 `AuthSwitchRequest` `0xfe` 切换），直接校验 PostgreSQL 的 SCRAM/MD5 角色密码并遵守 `pg_hba.conf`（`3306` 端口支持 `scram-sha-256`、`md5`、`password`、`trust`、`reject`；因 PG 校验串不存储 `SHA1(SHA1(password))`，不支持 `mysql_native_password` 挑战-响应）。`ALTER ROLE ... PASSWORD` 会自动使旧缓存失效；超级用户也可执行 `SELECT mysql.flush_auth_cache()` 手动清空缓存。TLS 复用 PostgreSQL `ssl_*`、`hostssl` 与 `pg_stat_ssl`。 |
| 连接字符集初始化 | 已实现（映射） | 支持带引号或不带引号的 `SET NAMES charset [COLLATE collation]`、`SET NAMES DEFAULT`、`SET CHARACTER SET`、`SET CHARSET`（含 `DEFAULT`）。同步更新 `character_set_client`、`character_set_results`、`character_set_connection` 与 `collation_connection`（`CHARACTER SET` 从当前数据库变量读取连接默认值）。非 UTF-8 字符集与非精确排序规则映射到 UTF-8 及 `utf8mb4_general_ci` / `utf8mb4_bin`（或 `utf8_*`），并发出 `1105` 告警。 |
| 报文上限与结果元数据 | 已实现 | 对入站命令包与累计 `COM_STMT_SEND_LONG_DATA` 数据强制检查可热重载的 `mysql.max_allowed_packet`（默认 `64 MiB`）。文本与二进制预备协议中，字符结果列统一返回 MySQL 5.7 字符集编号 `45`（`utf8mb4_general_ci`），二进制列返回 `63`（`binary`）。`mysql.halo_mysql_version` 低于 `8.0` 时握手通告 `45`。 |
| 二进制预备协议 | 已实现 | 支持 `COM_STMT_PREPARE`、`COM_STMT_EXECUTE`、`COM_STMT_CLOSE`、`COM_STMT_RESET`、`COM_STMT_SEND_LONG_DATA`，按二进制协议编码结果行，同时让绑定参数经过完整的 MySQL 改写与类型转换规则。不支持服务端预备游标，`COM_STMT_FETCH` 报 `1421`（`ER_STMT_HAS_NO_OPEN_CURSOR`）。 |
| SQL 预备语句 | 已实现 | 支持 `PREPARE name FROM 'sql'`（或 `@var`）、`EXECUTE name [USING @a, ...]` 以及 `DEALLOCATE` / `DROP PREPARE name`。语句名不区分大小写，同名重新 `PREPARE` 会替换旧定义；`USING` 除 `@var` 外还支持普通表达式（OpenHalo 扩展能力）。二进制预备协议与 SQL `PREPARE` 共用单会话 `max_prepared_stmt_count = 16,382` 上限（超限报 `1461`）。 |
| 连接重置与辅助命令 | 部分实现 / 桩响应 | `COM_RESET_CONNECTION` 回滚未提交事务、释放 `GET_LOCK` 会话锁、清理预备语句/用户变量/临时表、重置会话变量并保留当前 `USE` 模式。`COM_PING` 返回 OK；`COM_FIELD_LIST`、`COM_SET_OPTION`、`COM_STATISTICS` 返回最小兼容响应。 |
| 已实测客户端与驱动 | 约定范围已测 | Oracle `mysql` / `mysqldump` 5.7.32、MariaDB CLI、PyMySQL、`go-sql-driver/mysql` 1.9、Connector/J 8.4.0 与旧版 5.1.49、`mysqlslap`、`sysbench` 以及原始 `COM_STMT_*` 报文探针。 |
{.wide .expand}

```sql
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci';
SET @stmt_sql = 'SELECT id, HEX(payload) FROM items WHERE code = ?';
PREPARE lookup_item FROM @stmt_sql;
SET @target = 'alice';
EXECUTE lookup_item USING @target;
DEALLOCATE PREPARE lookup_item;
```

**兼容边界与迁移影响：** 不支持 MySQL Unix 域套接字、`COM_CHANGE_USER` 与 `KILL [QUERY]`（未实现的协议命令返回 `1047`；终止查询请通过 PostgreSQL 侧管理函数操作）。存储与网络传输始终为 UTF-8——执行 `SET NAMES latin1` 会发出 `1105` 告警而非按单字节透传，且 `@@collation_connection` 尚未传播到裸字符串字面量比较（`'A' = 'a'` 返回 `0`）。详见[排序规则与编码边界](/openhalo/18/compatibility/#collations)。

## SQL 方言与 DML {#sql}

| 能力 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| 词法与方言语法 | 已实现 | 反引号标识符、双引号字符串字面量、`LIMIT offset, count`、`INSERT ... VALUES ()` 空列默认插入、`INSERT ... SET col=val`、内联 `KEY` / `UNIQUE KEY`、表和列 `COMMENT`、`CREATE USER ... IDENTIFIED BY`、`@user_var`（`:=` 与 `SELECT ... INTO @var`）以及 `DO expr, ...`（PostgreSQL 匿名代码块需显式带 `LANGUAGE`）。 |
| 注释与 `LIKE` 转义 | 已实现 | `#` 行注释；`--` 仅在后接空白、控制字符或输入末尾时开启注释（`1--1` 解析为 `1 - -1`）；`NNNNN <= mysql.halo_mysql_version` 时执行 `/*! ... */` 与 `/*!NNNNN ... */` 可执行注释；多语句末尾分号后的注释单独回包 OK。字符串字面量保留 `\%` 与 `\_` 的反斜杠，使 `LIKE 'a\_b'` 只匹配字面下划线。遵守 `NO_BACKSLASH_ESCAPES`。 |
| 严格/非严格写入与 `IGNORE` | 已实现（有边界） | 关闭 `STRICT_TRANS_TABLES` / `STRICT_ALL_TABLES`（或使用 `INSERT IGNORE` / `UPDATE IGNORE`）时，越界有符号整数、`DECIMAL` 以及超长 `VARCHAR`/`CHAR`/`BINARY`/`VARBINARY` 会截断或夹逼并产生告警（`1264` / `1265`），`INSERT IGNORE` 按行跳过唯一键或外键冲突并告警。但 `BIGINT UNSIGNED > INT64_MAX`（`1264`）与字符 `NUL`（`1366`）在任何模式下均直接报错。 |
| `ON DUPLICATE KEY UPDATE` | 已实现 | 跨表上**所有**非部分 `PRIMARY KEY` 与 `UNIQUE` 索引（含前缀键与复合键）判定冲突；`VALUES(col)` 引用待插入新值，裸列名引用已有行旧值；同语句内重复键按顺序执行，并支持 `INSERT IGNORE ... ON DUPLICATE KEY UPDATE`。影响行数：插入计 `1`，值实际改变计 `2`，未改变计 `0`（启用 `CLIENT_FOUND_ROWS` 时计 `1`）。 |
| `REPLACE INTO` | 已实现 | 先删除在任意唯一键上冲突的**全部**旧行（触发 `ON DELETE` 外键动作与触发器），未显式指定的列填入列默认值而非旧行残留值，再插入新行。无冲突插入——或在仅含单个唯一索引、无行级 `DELETE` 触发器（含入站外键 `ON DELETE` 触发器）且全列值完全相同时——计 `1`；实际执行物理删旧插新时计 `1 + deleted_rows`。若目标表没有任何唯一键，`ODKU` 与 `REPLACE` 均退化为普通插入。 |
| 连接 `UPDATE` 与 `DELETE` | 部分实现 | 支持单目标表 `UPDATE t1 JOIN t2 ... SET ...`（含逗号连接）与单目标表 `DELETE FROM target USING table_references WHERE ...`（含自连接与索引提示），以及单表 `UPDATE`/`DELETE` 的 `ORDER BY ... LIMIT n`。 |
| `AUTO_INCREMENT` | 已实现（有边界） | 基于 `GENERATED BY DEFAULT AS IDENTITY`（`INCREMENT 1 CACHE 1 NO CYCLE`）加前置触发器实现。未设 `NO_AUTO_VALUE_ON_ZERO` 时写入 `NULL` 或 `0` 自动取号；显式写入正数原子推进序列高水位；`ALTER TABLE ... AUTO_INCREMENT = n` 推进计数器（空表时重置为 `n`）；`MODIFY` / `CHANGE` 支持保留、新增（从当前最大值之后继续）或移除自增；`CREATE TABLE ... LIKE` 复制默认值并建立独立自增序列。 |
| `ENGINE=` 与 `ENCRYPTION=` | 映射实现 | `ENGINE=<name>` 映射为已安装的同名小写 PostgreSQL 表访问方法（如 `orioledb`），`ENGINE=InnoDB` / `MyISAM` 保持默认 `heap`。`ENCRYPTION='Y'` 映射到 `tde_heap`；未安装 `pg_tde` 时直接报错，防止静默建成明文表。 |
| 索引提示 | 语法接受并忽略 | 在 `SELECT`、`UPDATE`、`DELETE` 中完整解析 `USE`、`IGNORE`、`FORCE` `INDEX` / `KEY`、可选作用域（`FOR JOIN` / `ORDER BY` / `GROUP BY`）、表别名、空列表 `USE INDEX ()`、`PRIMARY` 及连续多条提示，随后丢弃，不干预优化器。 |
{.wide .expand}

```sql
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(64) UNIQUE,
    code VARCHAR(32) UNIQUE,
    visits INT NOT NULL DEFAULT 0
);

INSERT INTO accounts (email, code, visits)
VALUES ('a@example.com', 'c1', 1), ('b@example.com', 'c2', 1);

-- Updates existing id=1 -> affected rows: 2 (0 if visits were already unchanged)
INSERT INTO accounts (email, code, visits) VALUES ('a@example.com', 'c9', 2)
ON DUPLICATE KEY UPDATE visits = visits + VALUES(visits);

-- Conflicts on BOTH email (id=1) and code (id=2): deletes both, inserts 1 new row -> affected rows: 3
REPLACE INTO accounts (email, code) VALUES ('a@example.com', 'c2');
```

*(上例先更新 `id=1` 返回影响行数 `2`；随后的 `REPLACE` 同时命中 `id=1` 与 `id=2` 两个唯一键，删除两行再插入一行，返回影响行数 `3`。)*

**兼容边界与迁移影响：** 普通 `UPDATE` 仍返回**匹配行数**而非值改变行数；`DELETE target FROM ... JOIN ...`（含逗号连接及 `LEFT JOIN` 孤儿清理写法）和真正的多目标表 `UPDATE`/`DELETE` 会报语法错误 `1064`——连接删除请改写为 `DELETE FROM target USING ... WHERE ...`。非默认的 `auto_increment_increment` / `auto_increment_offset` 仅回显不改变步长，分区父表不支持修改 `AUTO_INCREMENT` 计数器。详见[表达式与 SQL 形式边界](/openhalo/18/compatibility/#expressions)。

## 事务、隔离级别与外键 {#transactions}

| 能力 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| 事务生命周期与隐式提交 | 已实现 | 支持 `autocommit=0`、`BEGIN` / `START TRANSACTION`、`COMMIT`、`ROLLBACK`、`SAVEPOINT`，并在 `BEGIN`、DDL（`CREATE TEMPORARY TABLE` 除外）及 `SET autocommit=1` 前执行 MySQL 隐式提交。`autocommit=1` 下多语句 `COM_QUERY` 逐条独立提交。对已因错误中止的事务执行 `COMMIT` 会明确报 `1180`（`SQLSTATE 40000`），避免客户端把回滚误判为提交成功。 |
| 语句级回滚 | 已实现 | `mysql.statement_rollback = on`（默认）时，显式事务内的每条语句（含语法错误）运行在隐藏保存点（`__aux_mysql_stmt`）下，单条语句报错只回滚自身，保留同一事务内此前已完成的操作。 |
| 隔离级别与访问模式设置 | 已实现（映射） | 支持 `SET GLOBAL` / `SESSION TRANSACTION ...`（及不带作用域的 `SET TRANSACTION ...`）与 `transaction_isolation` / `tx_isolation`、`transaction_read_only` / `tx_read_only`（新旧别名保持同步）。不带作用域的 `SET TRANSACTION` 仅作用于下一事务，并在首次打开业务表或执行 `COMMIT`/`ROLLBACK`/DDL 时消耗。**读写 `REPEATABLE READ`、`READ COMMITTED` 与 `READ UNCOMMITTED` 统一运行在 PostgreSQL `READ COMMITTED` 下**；**只读 `REPEATABLE READ`** 与 **`START TRANSACTION WITH CONSISTENT SNAPSHOT`**（当有效 MySQL 隔离级别为默认的 `REPEATABLE READ` 时；在其他隔离级别下与 InnoDB 一致发出 `138` 告警并忽略该子句）获取真正的 `REPEATABLE READ` 一致快照；`SERIALIZABLE` 使用 PostgreSQL 可串行化检查并将 `40001` 冲突映射为 MySQL 死锁码 `1213`（在流复制热备库上回退为 `REPEATABLE READ`）。 |
| 只读约束执行 | 已实现 | 只读事务以 `1792` 拒绝写入。`SET GLOBAL read_only = 1`（限制普通角色）与 `super_read_only = 1`（限制含超级用户在内的所有角色）逐语句强制检查，以 `1290` 拒绝 DML、DDL、`SELECT ... FOR UPDATE` 与持久序列写入，同时允许读写 `TEMPORARY` 临时表。开启 `super_read_only=1` 会联动开启 `read_only`，关闭 `read_only=0` 会联动清除 `super_read_only`。 |
| 外键约束与级联 | 已实现 | 通过 PostgreSQL RI 触发器真正执行外键检查及 `ON DELETE` / `ON UPDATE`（`RESTRICT`、`NO ACTION`、`CASCADE`、`SET NULL`、`SET DEFAULT`）。子表非法键值报 `1452`，父表被阻止的修改/删除报 `1451`；`INSERT IGNORE` 可按行跳过违反外键的行并产生告警。 |
| `FOREIGN_KEY_CHECKS` 与待绑定外键 | 已实现 | 会话变量 `FOREIGN_KEY_CHECKS=0`（任意 MySQL 用户可设置）仅暂停外键检查与级联动作，不影响用户触发器、`AUTO_INCREMENT` 和 `ON UPDATE CURRENT_TIMESTAMP`。父表尚未创建（或在关闭检查时被删除）时，子表外键定义持久保存在扩展管理的触发器（`aux_mysql_pending_fk_*`）中，在 `SHOW CREATE TABLE` 与 `information_schema` 中可见；父表创建后若子表 owner 具备相应 `USAGE` + `REFERENCES` 权限则自动绑定为 `NOT VALID` 外键（缺权限时发 `1142` 告警并保持待绑定状态）。 |
{.wide .expand}

```sql
-- Stable repeatable snapshot for reporting queries:
START TRANSACTION WITH CONSISTENT SNAPSHOT;
SELECT COUNT(*), SUM(total) FROM orders;
COMMIT;

-- Load child tables before parents during logical dump import:
SET FOREIGN_KEY_CHECKS = 0;
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT NOT NULL,
    CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);
CREATE TABLE orders (id INT PRIMARY KEY);
SET FOREIGN_KEY_CHECKS = 1;
-- New orphan writes now fail with 1452; historical rows loaded while checks were off stay unvalidated.
```

**兼容边界与迁移影响：** 若业务在读写 `REPEATABLE READ` 事务内依赖多次普通 `SELECT` 看不见其他会话新提交的数据，必须将只读报表查询改为 `START TRANSACTION READ ONLY` 或 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。启用 `mysql.statement_rollback = on` 时，单个显式事务内超过 64 条写语句会溢出后端 `PGPROC` 的 `subxid` 缓存——批量导入请分批提交或评估 `mysql.statement_rollback = off`。外键父列必须具备 `PRIMARY KEY` 或 `UNIQUE` 约束（父表 `TRUNCATE` 不级联），且重新开启 `FOREIGN_KEY_CHECKS=1` 不会校验既有孤儿行。详见[事务与影响行数边界](/openhalo/18/compatibility/#transactions)。

## 数据类型与表达式 {#types}

| 范围 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| `CHAR` / `VARCHAR` / `TEXT` | 已实现（有边界） | 采用原生 PostgreSQL `bpchar`、`varchar`、`text` 存储（`TINYTEXT`、`TEXT`、`MEDIUMTEXT`、`LONGTEXT` 统一使用 `text`）。`CHAR(n)` 默认提取去除尾空格的逻辑值，并在 `CONCAT`、`CONCAT_WS`、`CAST`、`CONVERT`、`HEX`、`ELT`、`GROUP_CONCAT`、用户变量、锁名与 `EXECUTE` 中遵守 `PAD_CHAR_TO_FULL_LENGTH`。**所有字符类型在任何模式下遇到 `NUL`（`0x00`）均报 `1366` 错误。** |
| `BINARY` / `VARBINARY` / `BLOB` | 已实现 | 新建 `BINARY(n)`（`mysql.binary_n`）按 `n` 字节补 `0x00`；`VARBINARY(n)`（`mysql.varbinary_n`）强制校验字节上限 `n`；`TINYBLOB`/`BLOB`/`MEDIUMBLOB`/`LONGBLOB` 完整保留含 `0x00` 与任意非 UTF-8 字节的二进制载荷。严格模式越界报 `1406`，非严格/`IGNORE` 截断并发出 `1265` 告警。原生 PG 文本输入输出采用 `bytea` 十六进制转义，保证 `pg_dump` 无损往返。 |
| 二进制与字符互转 | 已实现 | 将二进制列赋值或 `CAST` 为 `CHAR`/`VARCHAR`/`TEXT` 时校验完整 UTF-8 编码；含 `0x00`（**包括 `BINARY(n)` 的补零字节**）或非法 UTF-8 时即使带 `IGNORE` 也报 `1366`。`CAST(bin AS SIGNED)` / `UNSIGNED` / `DECIMAL` 按带长度的十进制前缀解析，遇到 `NUL` 或非数字字符即停止（格式异常的二进制 `DECIMAL` 统一发 `1292` 告警）。 |
| 有符号与无符号整数 | 已实现（有边界） | 支持 `TINYINT`、`SMALLINT`、`MEDIUMINT`、`INT`、`BIGINT` 及其 `UNSIGNED` 域类型。**`BIGINT UNSIGNED` 基于 `int8` 域实现，可存储范围为 `0..9223372036854775807`（`INT64_MAX`）**：超过 `INT64_MAX` 的正数写入在所有模式（含 `IGNORE` 与二进制预备参数）下均报 `1264`；非严格负数夹为 `0` 并告警 `1264`。 |
| `DECIMAL` 与浮点数 | 已实现 | 未带精度的 `DECIMAL` 默认为 `DECIMAL(10,0)`，并通过 `SHOW` 与 `information_schema` 保留 `(p,s)`（无 typmod 的 PG `numeric` 显示为 `decimal(65,30)` 并告警 `1105`）。不带精度的 `FLOAT` / `FLOAT(0..24)` 使用 `float4`；`DOUBLE`、`REAL` 与 `FLOAT(25..53)` 使用 `float8`。 |
| 日期与时间类型 | 部分实现 | 支持 `DATE`、`TIME[(0..6)]`（日内时刻）、`DATETIME[(0..6)]`、`TIMESTAMP[(0..6)]`、`YEAR` 及 `ON UPDATE CURRENT_TIMESTAMP[(0..6)]`。`DATETIME` 与不带时区子句的 `TIMESTAMP` 均映射为 `timestamp without time zone`（默认精度 `0`，文本与预备结果均保留 `0..6` 声明精度）。 |
| 布尔值与默认值 | 已实现（有边界） | `TRUE`/`FALSE`、比较谓词及 `IF`/`CASE` 布尔结果写入数值列（`INT`、`BIGINT`、`TINYINT(1)`、`DECIMAL`、`FLOAT`、`DOUBLE`）存为 `1`/`0`，写入字符列（`CHAR`、`VARCHAR`、`TEXT`）存为 `'1'`/`'0'`，写入二进制列（`BINARY` 补零、`VARBINARY`、`BLOB`）存为字节 `'1'`/`'0'`，覆盖严格/非严格模式、`DEFAULT`、`CAST`/`CONVERT`、`ODKU`/`REPLACE` 唯一键判定、生成列与预备语句。带引号的 `'true'` 仍作为普通字符串保留。支持 `SUM(bool)` 与布尔 `CONCAT`/`GROUP_CONCAT`。 |
| 十六进制与位字面量（`mysql.hexlit`） | 已实现（有边界） | `X'41'`、`0x41`、`b'101'`、`0b101` 默认返回 `VARBINARY` 字节（`SELECT 0x41` 返回 `A`），在算术/数值/`BIT` 上下文中作为整数参与运算（`0x41 + 0` 为 `65`），写入数值列存整数、写入字符/二进制列存字节、写入 `BIT(n)` 存位值（超宽报 `1406`），并支持走索引的 `binary_col = X'...'` 查询。`HEX()` 与 `UNHEX()` 支持字符串、二进制、64 位补码整数（`HEX(-1)` 为 16 个 `F`）及 `BIT`（`UNHEX` 含非法字符返回 `NULL` 并告警 `1411`）。 |
| 字符串、条件与算术函数 | 部分实现 | `/` 返回 `DECIMAL`（`DIV` 为整除；除零返回 `NULL` 加 `1365` 告警，严格写入配合 `ERROR_FOR_DIVISION_BY_ZERO` 时报 `1365` 错误）。提供按排序规则比较的 `LOCATE`、`INSTR`、`POSITION`、`LIKE`、`STRCMP`、`FIELD` 与同时校验尾空格数量的 `FIND_IN_SET`；区分大小写的 `REPLACE()` 与按字节匹配的 `SUBSTRING_INDEX()`；`CHAR`/`VARCHAR`/`TEXT` 组合的 `IF()` / `IFNULL()`；保留原始字节的二进制 `GROUP_CONCAT()`。`SHOW WARNINGS` / `SHOW ERRORS` 最多保留 64 条诊断记录。 |
{.wide .expand}

```sql
CREATE TABLE payloads (
    id INT PRIMARY KEY,
    flag VARCHAR(8) NOT NULL DEFAULT TRUE,
    fixed_bin BINARY(4) NOT NULL,
    raw_blob BLOB,
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
);

INSERT INTO payloads (id, fixed_bin, raw_blob)
VALUES (1, 'A', 0x4100ff);

SELECT flag, HEX(flag), HEX(fixed_bin), HEX(raw_blob), CAST(0x3432 AS UNSIGNED)
FROM payloads;
-- flag='1', HEX(flag)='31', HEX(fixed_bin)='41000000', HEX(raw_blob)='4100FF', CAST=42
```

**兼容边界与迁移影响：** 不支持原生 `ENUM` 与 `SET`（报 `1091`）、负数或 `>= 24:00:00` 的 `TIME` 时长、零日期（`0000-00-00`）、MySQL `TIMESTAMP` 跨时区自动换算、`CAST(-1 AS UNSIGNED)` 的无符号 64 位回绕、布尔 `AVG`/`MIN`/`MAX`/`STD`/`BIT_*` 或 `(1>0)+0`、多参数 `GROUP_CONCAT(a, b)` 以及跨类型 `COALESCE(1, 'a')` / `IF(c, 1, 'a')`。安装 `aux_mysql` 还会在该库注册对原生 PostgreSQL 会话同样可见的 `bool -> numeric/float/binary` 赋值转换。详见[数据表示边界](/openhalo/18/compatibility/#representation)与[PostgreSQL 共存边界](/openhalo/18/compatibility/#coexistence)。

## 排序规则与索引 {#indexes}

| 能力 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| 四个精确 MySQL 排序规则 | 已实现 | `mysql` 模式下的 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_bin`、`utf8mb4_bin`。`general_ci` 实现 MySQL 5.7 BMP 大小写/重音权重表（`> U+FFFF` 补充平面字符权重统一为 `0xFFFD`）加 `PAD SPACE`、流式比较器与缩略排序键；`bin` 实现 UTF-8 码点顺序加 `PAD SPACE`。 |
| 其他 MySQL 排序规则名称 | 近似映射（`1105`） | 在列/表 DDL、表达式 `COLLATE`、视图、`CREATE TABLE AS` 与 `SET NAMES ... COLLATE` 中均可接受：以 `_ci` 结尾的名称映射为 `utf8mb4_general_ci`（或 `utf8_general_ci`），其余名称映射为 `utf8mb4_bin`（或 `utf8_bin`），统一发出 `1105` 告警。`SHOW CREATE TABLE` 展示实际生效的排序规则名称。 |
| 表级默认排序规则 | 已实现 | 未显式写 `COLLATE` 的字符列继承表级 `COLLATE=`（通过 `SECURITY LABEL FOR aux_mysql` 持久保存）或 `mysql.default_collation`（默认 `case_insensitive` 映射为 `utf8mb4_general_ci`）。 |
| 前缀索引与超长键（`mysql_prefix`） | 已实现（回堆复核） | `KEY (col(n))`、`UNIQUE KEY (col(n))`、`PRIMARY KEY (col(n))` 对字符列按字符数计 `n`，对二进制列按字节数计 `n`，支持单列与复合键。带显式前缀或含无界/超宽列的索引使用 `mysql_prefix` 访问方法：以有界 btree 候选键缩小扫描范围，再通过 dirty-snapshot 回堆读取原始前缀判定唯一性、`ODKU` 与 `REPLACE`。哈希碰撞绝不单独决定相等，`1.9` 也不再创建辅助 hash 索引。 |
| 短全列普通索引 | 已实现（原生 `btree`） | 未声明前缀且最大元组宽度在安全阈值内的索引保持原生 PostgreSQL `btree`，完整保留 `ORDER BY ... LIMIT` 有序扫描与仅索引扫描（Index Only Scan）。 |
| 表级作用域键名 | 已实现（有边界） | 键名像 MySQL 一样按表独立命名（不同表可共用 `KEY idx_created`）；未命名键默认取首列名 `col`、`col_2` 等。底层 PostgreSQL 物理索引名附加 `$<8位十六进制>` 后缀，而 `SHOW INDEX`、`SHOW CREATE TABLE`、`information_schema.STATISTICS`、`DROP INDEX k ON t`、`ALTER TABLE ... DROP/RENAME INDEX`、`CREATE TABLE ... LIKE` 与 `1062` 唯一冲突错误均展示逻辑键名。 |
{.wide .expand}

```sql
CREATE TABLE articles (
    id INT PRIMARY KEY,
    slug VARCHAR(500) COLLATE utf8mb4_general_ci NOT NULL,
    body LONGTEXT NOT NULL,
    UNIQUE KEY uk_slug_prefix (slug(12)),
    KEY idx_created (id),
    KEY idx_body (body(32))
);

-- Enforces uniqueness on the first 12 characters under utf8mb4_general_ci:
INSERT INTO articles VALUES (1, 'hello-world-alpha', 'first');
-- Fails with 1062 on key 'uk_slug_prefix' because first 12 chars match case-insensitively:
-- INSERT INTO articles VALUES (2, 'HELLO-WORLD-beta', 'second');
```

**兼容边界与迁移影响：** 不复现 Unicode UCA 或特定语言排序权重（如 `utf8mb4_unicode_ci`、`utf8mb4_0900_ai_ci`、`latin2_czech_cs`），重音、连字或补充平面字符的排序与唯一冲突关系可能与所请求规则不同。`mysql_prefix` 索引必须回堆复核，不支持仅索引扫描或消除 `ORDER BY` 排序。逻辑键名超过 `54` 字节（`63` 字节减去 9 字节后缀）会被截断，且仅对 ASCII 字母做大小写折叠。从 `1.5` 升级不会就地改写旧 ICU 排序规则或丢失长度的前缀索引，详见[历史对象迁移审计](/openhalo/18/migration/#audit)。

## 生成列 {#generated}

| 方面 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| `VIRTUAL` 与 `STORED` 声明 | 已实现（物化存储） | 支持 `col type [GENERATED ALWAYS] AS (expr)` 搭配 `VIRTUAL`（默认）或 `STORED`。由于 PostgreSQL 原生虚拟生成列既不能建索引也不能调用 `aux_mysql` 函数，**`VIRTUAL` 与 `STORED` 列在磁盘上均实际物化存储**，同时在 `SHOW COLUMNS`、`SHOW CREATE TABLE`、`information_schema.COLUMNS` 与 `CREATE TABLE ... LIKE` 中保留 `VIRTUAL GENERATED` / `STORED GENERATED` 标记，使 Oracle `mysqldump` 自动在 `INSERT` 中省略生成列值。 |
| 依赖链与 `ALTER` 重算 | 已实现 | 生成列可引用同表中更早定义的生成列；`ALTER TABLE ... MODIFY / CHANGE`（含基础列类型变更）会自动重算下游依赖的生成列。通过 `INSERT`、`UPDATE`、`ODKU` 或 `REPLACE` 写入非 `DEFAULT` 值统一报 `3105`。 |
| 确定性表达式白名单校验 | 已实现（白名单） | `CREATE TABLE`、`ALTER TABLE` 与 `CREATE TABLE ... LIKE` 在规划前审查解析后的表达式树（`src/mys_generated_policy.h`）。非确定性或外部依赖结构（`RAND()`、`NOW()`、`CURRENT_TIMESTAMP`、`@vars`、`@@vars`、子查询、序列、`'now'`/`'today'` 等相对时间字面量、用户自定义域及任意自定义 SQL/PLpgSQL 函数）一律报 `3102`。经过审计的兼容函数（`CONCAT`、`CONCAT_WS`、`IF`、`IFNULL`、`/`、`DIV`、`HEX`、`UNHEX`、`SUBSTR`、`LOCATE`、`REPLACE`、基于时间类型列的 `DATE_FORMAT` 等）封装为表所在模式下的 `aux_mysql_gen_<hash>` 函数，并在 `DROP` / `ALTER` 不再引用时自动清理。 |
| 写入者 `sql_mode` 转换 | 已实现 | 有界 `VARCHAR(n)` / `CHAR(n)` 与 `DECIMAL(p,s)` 生成列在写入时按**当前写入会话**的 `sql_mode` 和 `IGNORE` 规则执行截断/越界检查（覆盖常量生成表达式与重复预备语句执行），非严格模式告警、严格模式报错。 |
{.wide .expand}

```sql
CREATE TABLE line_items (
    id INT PRIMARY KEY,
    qty INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    gross DECIMAL(12,2) GENERATED ALWAYS AS (qty * unit_price) VIRTUAL,
    label VARCHAR(32) GENERATED ALWAYS AS (CONCAT('item-', id)) STORED,
    KEY idx_gross (gross)
);

INSERT INTO line_items (id, qty, unit_price) VALUES (1, 3, 19.50);
SELECT id, gross, label FROM line_items;
-- 1 | 58.50 | item-1
```

**兼容边界与迁移影响：** `VIRTUAL` 列在写入时物化落盘，占用与 `STORED` 相同的磁盘和写入开销，且后续读取会话更改 `sql_mode` 不会改变已落库的值。生成列中的 `DATE_FORMAT(col, fmt)` 要求输入列本身为 `DATE`/`DATETIME`/`TIMESTAMP` 类型（隐式文本转日期及 `CAST(CONCAT(...) AS DATE)` 会以 `3102` 拒绝）。`VIRTUAL` 主键与引用 `AUTO_INCREMENT` 列的生成表达式属于 OpenHalo 18 依赖 PostgreSQL 能力的扩展，直接回放到 MySQL 5.7 会被拒绝。`1.8` 之前被丢弃的生成表达式及历史遗留的不安全 `IMMUTABLE` 包装函数不会因扩展升级自动修复，详见[生成列迁移审计](/openhalo/18/migration/#audit)。

## 用户级锁、元数据与运维 {#operations}

| 能力 | 支持程度 | 已实现行为 |
| --- | --- | --- |
| MySQL 5.7 用户级命名锁 | 已实现 | 提供 `GET_LOCK(str, timeout)`、`RELEASE_LOCK(str)`、`IS_FREE_LOCK(str)`、`IS_USED_LOCK(str)` 与 `RELEASE_ALL_LOCKS()`。支持单会话同时持有多个锁及同一锁的递归重入；锁名不区分大小写，最长 64 个字符（超长报 `3057`）；超时以秒为单位（负数无限等待，兼容 `0x..` 十六进制参数）；自动检测等待死锁环并向成环方报 `3058`。事务 `COMMIT`/`ROLLBACK` 不释放锁，`COM_RESET_CONNECTION` 与连接断开时自动释放。底层映射为 `mysql.database` 下的会话级咨询锁（`pg_locks` 中 `objsubid = 19801`）。 |
| `SHOW` 与 `information_schema` | 部分实现 | 支持 `SHOW DATABASES`、`SHOW [FULL] TABLES`、`SHOW [FULL] COLUMNS`、`SHOW INDEX`、`SHOW CREATE TABLE`、`SHOW CREATE VIEW`、`SHOW CHARACTER SET [WHERE ...]`、`SHOW COLLATION`、`SHOW GLOBAL` / `SESSION VARIABLES`（经 `mysql.show_system_variable` 读取实时值）、`SHOW ENGINE INNODB STATUS`（语法桩）及 `SHOW WARNINGS` / `SHOW ERRORS [LIMIT ...]`。`information_schema`（`mys_informa_schema`）提供 `COLUMNS`、`STATISTICS`、`TABLES`、`VIEWS`、`ROUTINES`、`TABLE_CONSTRAINTS`、`KEY_COLUMN_USAGE` 与 `REFERENTIAL_CONSTRAINTS`（含缺父表的待绑定外键）。 |
| 备份、恢复与高可用复制 | PG 原生 + 逻辑转储 | 物理高可用、流复制、PITR 与归档直接使用标准 PostgreSQL WAL 工具链（Patroni、pgBackRest）。逻辑备份支持同版本 PG18 `pg_dump` / `pg_restore`（保留触发器与安全标签）及约定 SQL 子集内的 Oracle MySQL `mysqldump` 往返恢复。 |
{.wide .expand}

```sql
SELECT GET_LOCK('nightly_settlement', 5) AS acquired,
       IS_USED_LOCK('NIGHTLY_SETTLEMENT') = CONNECTION_ID() AS owned_by_me;
-- Perform multi-transaction work; COMMIT does not release GET_LOCK
SELECT RELEASE_LOCK('nightly_settlement');
```

**兼容边界与迁移影响：** `GET_LOCK` 占用 PostgreSQL 共享锁表空间（受 `max_locks_per_transaction` 影响）。`SHOW STATUS`、`performance_schema` 动态指标及未移植的 `information_schema` 视图仍为空表或部分字段桩。不提供 MySQL binlog / GTID 复制（`@@gtid_mode = 'OFF'`，`@@gtid_executed = ''`）。详见[运维与诊断限制](/openhalo/18/compatibility/#operations)与[备份与恢复](/openhalo/18/migration/#restore)。
