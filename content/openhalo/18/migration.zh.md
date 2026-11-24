---
type: docs
upstream_link: ""
search_keywords: ["ALTER EXTENSION", "1.5", "1.9", "PG14", "mysqldump", "pg_dump", "review_fix_migration", "generated_manifest", "FOREIGN_KEY_CHECKS", "pending_foreign_keys", "bind_pending_foreign_keys", "check_pg14_config", "upgrade", "升级", "外键"]
title: 迁移与升级
description: MySQL 5.7 迁移、OpenHalo PG14 逻辑迁移、已发布 v18.6（aux_mysql 1.5）到 1.9 的就地升级、不会自动修复的历史对象审计，以及备份与恢复。
weight: 50
---

OpenHalo 18 涉及三条截然不同的迁移与升级路径，操作前必须严格区分：

1. **MySQL 5.7 → OpenHalo 18** — 依据[兼容边界](/openhalo/18/compatibility/)完成模式适配与逻辑数据导入。
2. **OpenHalo PG14（`1.0.14.x`）→ OpenHalo 18** — **仅支持逻辑迁移**（严禁共用数据目录或物理 `pg_upgrade`，工具链已显式拦截）。
3. **OpenHalo `v18.6`（`aux_mysql 1.5`）→ `v18.6.1` / `aux_mysql 1.9`（`2627e6f` / `6a93e8f`）** — **同一 PG18 数据目录上的配套二进制替换 + `ALTER EXTENSION` 升级**，随后必须对**不会自动修复**的历史 `1.5` 对象和旧错值执行显式审计与修复。

## 变更与迁移前预检 {#preflight}

梳理当前运行的二进制版本、`aux_mysql` 版本（`SELECT extversion FROM pg_extension WHERE extname = 'aux_mysql'`）、`postgresql.conf`、权威原始 MySQL DDL 以及业务 SQL 和驱动版本。在正式切换完成验收前，保留经过恢复演练的备份与旧版二进制。

先在独立演练环境中完整走通流程：核对行数、主键/唯一键、文本值与 `HEX()` 原始字节、列默认值、生成列值、外键约束与级联动作、`SHOW WARNINGS`，以及真实业务驱动下的事务隔离与影响行数行为。部署 `1.9` 时请核实二进制来自源码标签 `v18.6.1`（`2627e6f3e94ffdaba9ca6a835c4a1ae2fba34183`）或已验收提交 `6a93e8fb914a4cc4b6a0c4e3f35af43b5f8dc41a`（严禁使用验收前的 `a000baa`），也切勿用 `SELECT VERSION()` 返回的 `5.7.32-log` 判断扩展版本。

## 从 MySQL 5.7 迁移 {#mysql}

当表结构与 SQL 处于[约定兼容边界](/openhalo/18/compatibility/)内时，可使用 Oracle `mysqldump` 5.7 逻辑导出并导入 OpenHalo 18：

1. **导出前先行排查不兼容类型与语法**：
   - 检查 `BIGINT UNSIGNED` 列是否存在大于 `9223372036854775807`（`INT64_MAX`）的值——任何模式下都会报 `1264` 错误。
   - 检查 `CHAR`/`VARCHAR`/`TEXT` 列是否含有内嵌 `0x00` 字节（报 `1366`）——确需保存原始字节的列应迁移为 `BINARY`/`VARBINARY`/`BLOB`，切勿在导入时静默删掉 `0x00`。
   - 检查 `utf8mb4_unicode_ci` 或特定语言排序规则列在映射为 `utf8mb4_general_ci` / `utf8mb4_bin` 后是否产生新的唯一键重复。
   - 确认外键引用的父表列具备 `PRIMARY KEY` 或 `UNIQUE` 约束（即使 `FOREIGN_KEY_CHECKS=0` 也会拒绝非唯一父索引）。转储文件中子表先于父表出现的情况由 `FOREIGN_KEY_CHECKS=0` 下的待绑定外键机制自动处理。
   - 显式转换不支持的 `ENUM`、`SET` 以及负数或 `>= 24:00:00` 的 `TIME` 时长列，并改写 MySQL 存储过程、MySQL 触发器体、`EVENT` 及 `DELETE target FROM ... JOIN ...` 语句。
2. **`ENUM`、`SET` 与时长 `TIME` 的显式 PostgreSQL 表示示例**：
   以下在 `mysql.database` 中经 PostgreSQL 连接执行的示例可约束合法枚举/集合成员并无损保存正负时长，但**不会**自动复现 MySQL `ENUM` 的序数排序、`SET` 的位掩码数值运算或驱动协议返回类型，需同步核查应用侧代码：

```sql
CREATE SCHEMA migrated;
CREATE TABLE migrated.example (
    id integer PRIMARY KEY,
    state text CHECK (state IN ('new', 'done')),
    flags text CHECK (string_to_array(flags, ',') <@ ARRAY['red', 'blue']),
    elapsed interval CHECK (extract(year FROM elapsed) = 0
                            AND extract(month FROM elapsed) = 0)
);
INSERT INTO migrated.example VALUES (1, 'done', 'red,blue', interval '-01:02:03');
SELECT state, flags, extract(epoch FROM elapsed) FROM migrated.example;
```

3. **切勿用 `--force` 掩盖导入错误**：Oracle `mysqldump` 生成的 `/*!50700 ... */` 可执行注释（包含 `SET NAMES`、`FOREIGN_KEY_CHECKS=0`、`TIME_ZONE`、`SQL_MODE` 与视图定义）在 `NNNNN <= mysql.halo_mysql_version` 时会被正常执行。不要把 `mysql --force` 的零退出码当作导入成功依据，导入后须逐表核对行数、索引和约束。

## 从 OpenHalo PG14（`1.0.14.x`）迁移 {#pg14}

OpenHalo 18 采用 PostgreSQL 18 系统目录与扩展化钩子，与 OpenHalo 14 分叉**二进制不兼容**。严禁用 OpenHalo 18 二进制直接启动 PG14 数据目录或运行 `pg_upgrade`（`pg_upgrade` 会显式拒绝 `1.0.14.x` 品牌二进制，伪造版本串也无法消除系统目录差异）。

1. 使用 OpenHalo 18 源码树中的只读预检脚本扫描旧配置及每一个 PG14 数据库：

```sh
python3 contrib/aux_mysql/tools/check_pg14_config.py /path/to/old/postgresql.conf
psql -X -d old_database -f contrib/aux_mysql/tools/check_pg14_schema.sql
```

当发现已移除或已改名参数（`database_compat_mode`、`standard_parserengine_auxiliary`、`mysql.ci_collation`、`halo_mysql.*`，或 `shared_preload_libraries` 未包含 `aux_mysql`）时，`check_pg14_config.py` 返回退出码 `2`。`check_pg14_schema.sql` 会标出需显式转换的 `ENUM`/`SET` 列、需核查时长范围的 `TIME` 列，以及精度规则变化的 `FLOAT` 列（PG14 为 `float8`，OpenHalo 18 新建裸 `FLOAT` 为 `float4`；需保留双精度时请改为 `DOUBLE`）。

2. 初始化全新的 OpenHalo 18 实例，仅迁移经过审查的配置项（参见[不可沿用的旧配置](/openhalo/18/configuration/#old-settings)），安装 `aux_mysql`，创建审查后的业务表结构，再通过逻辑方式导入业务数据。**切勿将 OpenHalo 14 转储中的旧扩展内部函数、转换或系统目录修改回放到 OpenHalo 18。**

## 从已发布 v18.6（`aux_mysql 1.5`）升级到 `1.9` {#upgrade}

已发布标签 `v18.6` 安装的是 `aux_mysql 1.5`。将既有 OpenHalo 18 实例升级至 `v18.6.1` / `aux_mysql 1.9`（`2627e6f` / `6a93e8f`）可直接复用原 PG18 数据目录：

1. 正常停止运行中的 `v18.6` 实例。
2. 安装由同一提交配套编译的新版 OpenHalo 18 内核与 `aux_mysql 1.9` 二进制（切勿只单独替换 `aux_mysql.so`）。若在旧测试集群上排演，注意避免 `1.5` 旧后台自动安装器与手动建扩展并发冲突。
3. 使用新二进制启动同一数据目录，通过 PostgreSQL 连接（`psql`）进入 `mysql.database` 并执行：

```sql
ALTER EXTENSION aux_mysql UPDATE TO '1.9';
SELECT extname, extversion FROM pg_extension WHERE extname = 'aux_mysql';
```

PostgreSQL 会自动顺序执行 `1.5 → 1.6 → 1.7 → 1.8 → 1.9` 升级脚本，不重写用户表，并保留 `information_schema.columns.EXTRA` 列描述符，使依赖它的用户视图保持完好。**切勿在有业务数据的数据库上执行 `DROP EXTENSION aux_mysql CASCADE`。**

在新二进制启动后、执行 `ALTER EXTENSION` 之前的短暂窗口内，旧 SQL 层对象仍可继续工作；`ALTER EXTENSION` 提交后，系统目录失效机制会让既有连接和新建 MySQL 连接立即可用 `1.9` 新类型、转换和前缀索引，无需再次重启服务。

*（注：最终验收在真实 `v18.6` / `1.5` 实例升级后与全新 `1.9` 实例比对，全部 3,476 个扩展成员**原始定义零差异**；仅单独测试的未发布 `1.6 → 1.7 → 1.8 → 1.9` 历史开发链在固定 ASCII 元数据列 `mys_informa_schema.columns.extra` 上保留一处无害的 `pg_catalog.default` 与 `pg_catalog.C` 排序规则差异。）*

## 不会随升级自动修复的历史对象与错误数据 {#audit}

扩展系统目录与全新 `1.9` 一致，**绝不代表历史业务表结构或既往写错的数据已被自动修复**。`1.5 → 1.9` 升级不会猜测早期丢弃的长度/表达式，也不会静默篡改用户已有数据。切换前必须在 `mysql.database` 中对每个业务模式运行只读迁移审计：

```sh
psql -X -v review_schema=app -v check_fk=1 \
  -f contrib/aux_mysql/tools/review_fix_migration.sql
```

（`check_fk=1` 会执行只读孤儿行统计查询，在大表上会产生表扫描。）以下八类历史状态均需管理员显式审查与处置：

| `1.5 → 1.9` 后保留的历史状态 | 升级无法自动修复的原因 | 受支持的审计与修复方法 |
| --- | --- | --- |
| **`BINARY(n)` / `VARBINARY(n)` 长度丢失**（旧 `mysql.binary` / `mysql.varbinary` 域） | `1.5` 丢弃了声明长度 `(n)`（`atttypmod = -1`）；原声明 `BINARY(4)` 写入 `'A'` 时磁盘物理值可能只有单字节 `0x41`。 | 对照原始 MySQL DDL 核查 `octet_length` / `HEX()`，确认所有行不超过 `n` 后，通过 MySQL 连接执行审查后的 `ALTER TABLE ... MODIFY col BINARY(n)` 迁移至 `mysql.binary_n` / `mysql.varbinary_n`。 |
| **前缀索引长度丢失 / 旧全列或 MD5 索引** | `1.5` 建立的全列或表达式索引未记录原始 `col(n)` 前缀长度。 | 对照 `pg_get_indexdef()` 与权威 MySQL DDL；先在目标前缀与排序规则下排查重复键（如 `GROUP BY LEFT(col, n) COLLATE utf8mb4_general_ci HAVING COUNT(*) > 1`），处理冲突后再通过 MySQL DDL 重建新键并替换旧索引。 |
| **旧版 ICU 排序规则与索引**（`case_insensitive` 等） | 既有列与索引保留原排序规则 OID，其比较权重和 `PAD SPACE` 行为不同于 `1.9` 的 `utf8mb4_general_ci` / `utf8mb4_bin`。 | 先排查在新排序规则下是否出现唯一键冲突，再按原始 MySQL DDL 重建表和索引。对缺表级排序规则标签的旧表，审查后显式打标（`SECURITY LABEL FOR aux_mysql ON TABLE app.t IS 'case_sensitive'`）。 |
| **被丢弃的生成列表达式（退化为 `NULL` 普通列或普通 `DEFAULT`）** | `1.8` 之前的解析器可能丢弃 `GENERATED ALWAYS AS (expr)`，使列变成值为 `NULL` 的普通列；从 `NULL` 数据无法反推原 `v + 1` 表达式。 | 通过可信 `generated_manifest`（见下文）提供原始 MySQL 生成定义，审查脚本输出的 `ALTER TABLE ... MODIFY` 语句，按列依赖顺序在目标 `sql_mode` 下经 MySQL 执行。`1.9` 之前的既有生成列若需启用新的写入者 `sql_mode` 转换，同样需审查后重新 `MODIFY`。 |
| **不安全的历史 `IMMUTABLE` 生成包装函数（`aux_mysql_gen_*`）** | `1.9` 之前可能把 `RAND()`、`NOW()`、`@vars` 或外部查询包进 `IMMUTABLE` 函数。`1.9` 会在 `ALTER` / `CREATE TABLE LIKE` 时以 `3102` 拦截此类旧表，且不会改写已折叠落库的值。 | 审查 `review_fix_migration.sql` 打印的生成函数体，删除该列或 `MODIFY` 替换为合规的确定性表达式，并核验重算后的值。 |
| **`NOT ENFORCED` 外键与历史孤儿行** | `1.5` 创建的外键处于 `NOT ENFORCED`，且 `FOREIGN_KEY_CHECKS=0` 期间可能写入孤儿行；升级脚本若自动删行或强行校验会损毁数据或阻断升级。 | 检查 `conenforced`、`convalidated` 及 `check_fk=1` 统计的孤儿行数，按业务规则清理或补齐父键后，执行下方的 `enforce_fk=1` 与 `validate_fk=1`。 |
| **旧版本布尔写入留下的 `'true'`、`'false'`、`'fals'` 或 `0` 错值** | `6a93e8f` 之前的版本在写入布尔值时可能把字符列存成 `'true'`/`'false'` 或在非严格数值列存成 `0`，磁盘上无法与业务有意写入的字符串 `'true'` 或 `0` 区分。 | 切换前对照权威上游数据源或业务日志核对受影响表，按业务语义定向修正。 |
| **既有 `FLOAT`（`float8`）与无精度约束 `DATETIME` 域** | 升级绝不会自动把已有 `float8` 列收窄为 `float4`，也不会截断已有微秒时间戳。 | 修改列定义前先核查数据范围与小数精度；需保留 `float8` 精度时显式使用 `DOUBLE`。 |
{.wide .expand}

按业务规则处理完所有孤儿行后，可就地事务性启用并验证历史 `NOT ENFORCED` / `NOT VALID` 外键（保留原约束 OID、注释与依赖；若仍存留任何孤儿行则整笔事务安全回滚）：

```sh
psql -X -v review_schema=app -v enforce_fk=1 -v validate_fk=1 \
  -f contrib/aux_mysql/tools/review_fix_migration.sql
```

对于在 `1.5` 中丢失了表达式的生成列，可将源自权威 MySQL 模式历史的清单文件通过 `-v generated_manifest=/path/to/manifest.sql` 传给审计脚本，以生成供审阅的 `ALTER TABLE ... MODIFY` 语句：

```sql
INSERT INTO pg_temp.review_fix_generated_source
 (table_schema, table_name, column_name, type_sql, expression_sql, kind, attributes_sql, provenance)
VALUES ('app', 't', 'g', 'varchar(2)', 'v', 'STORED', '', 'original MySQL schema dump');
```

## 待绑定外键与 PostgreSQL 权限检查 {#pending-fk}

当子表在父表尚不存在时声明外键（例如 `FOREIGN_KEY_CHECKS=0` 导入转储或先删父表），OpenHalo 18 会将外键声明保存在子表的 `POST_DATA` 触发器（`aux_mysql_pending_fk_*`）中，并在父表出现前拦截新的非 `NULL` 子键写入。

后续创建、修改或恢复父表时——**即便由 PostgreSQL 超级用户执行 `pg_restore`**——OpenHalo 18 都会严格核查**子表当前 owner** 的权限：

- 对父表所在模式的 `USAGE` 权限，**以及**
- 对父表（或每一个被引用父列，含隐式主键列）的 `REFERENCES` 权限。

若缺少上述权限，系统发出 **`1142` 告警**，允许父表 DDL 或恢复继续完成，不改动任何既有行，并将外键继续保留在受保护的待绑定状态。注意删除并重建父表不会继承旧表的授权。确认无误后向子表 owner 授予所需的 `USAGE` 与 `REFERENCES` 权限，再对子表或父表执行一次 `ALTER TABLE` 即可完成绑定（绑定生成 `NOT VALID` 外键以免历史孤儿行中断 DDL；核查完历史数据后再执行 `VALIDATE CONSTRAINT`）。

## 备份、恢复、切换与回退 {#restore}

生产切换前应同时保留 PostgreSQL 原生备份与 MySQL 逻辑转储，并完整演练恢复：

- **原生 `pg_dump` / `pg_restore`**：使用与当前 OpenHalo 18 PG18 版本匹配的备份恢复工具。**必须保留触发器与安全标签**——切勿使用 `--no-security-labels`（会丢弃表级默认排序规则标签），也切勿剔除 `aux_mysql_pending_fk_*` 触发器（承载缺失父表的待绑定外键元数据）。`1.8` 之前不含 `$<8位十六进制>` 后缀的旧索引名会被自动识别，无需仅为改名而重建索引。
- **MySQL 逻辑转储（`mysqldump`）**：涉及生成列时，请使用 **Oracle MySQL `5.7+` 的 `mysqldump` 与 `mysql` 客户端**。MariaDB `10.5` 的 `mysqldump` 即使面对真实 MySQL 5.7 也会把生成列值写进 `INSERT` 语句，导致导出的 SQL 在 MySQL 5.7 与 OpenHalo 18（报 `3105`）上均无法直接恢复。包含 PostgreSQL 专有语法的视图/生成列、`VIRTUAL` 主键以及引用 `AUTO_INCREMENT` 的生成列，在回放到原生 MySQL 5.7 前需先做语法转换。
- **高可用与复制**：使用标准 PostgreSQL 物理流复制与 WAL 归档（Patroni、pgBackRest）；不支持 MySQL binlog / GTID 复制。
- **升级回退**：**不支持将已升级到 `aux_mysql 1.9` 的数据库就地降级回 `1.5`**——仅换回旧二进制无法撤销已执行的系统目录、新类型与运算符类变更。如需回退，请使用匹配的旧版二进制恢复升级前已验证的备份。
