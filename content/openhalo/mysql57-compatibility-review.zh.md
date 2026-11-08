---
type: docs
upstream_link: ""
title: OpenHalo 18 与 MySQL 5.7 兼容性研究报告
linkTitle: MySQL 5.7 实测报告
description: 固定 OpenHalo 提交 9dc937f，独立构建并与真实 MySQL 5.7.32 差分测试，记录可用范围、迁移结果和七项阻断问题。
weight: 65
---

**OpenHalo 18 可以运行经过明确适配的有限 MySQL 应用；现有结果不足以支持将它作为 MySQL 5.7 的直接替代，也不能批准无改造的生产迁移。** 所测基础查询和客户端连接路径可用，但崩溃、约束未执行、事务设置无效和 DDL 往返改变数据规则等问题仍然构成阻断。

这是 PGSTY 对 [`pgsty/openhalo@9dc937f`](https://github.com/pgsty/openhalo/tree/9dc937ff4e81667882c42c3618eafcf4b28ac059) 的独立验收，测试日期为 2026 年 11 月 7 日（Asia/Shanghai），问题分流与专项研究于 11 月 8 日整理。它与 [Halo Database 1.0.16 参考手册](/openhalo/mysql-compatibility/)、[历史 OpenHalo 测试报告](/openhalo/mysql-compatibility-gaps/) 分属不同版本和证据范围。本轮新发现不代表问题由这个提交引入。

## 固定版本与独立构建 {#environment}

固定提交为 `9dc937ff4e81667882c42c3618eafcf4b28ac059`，tree 为 `e45c40bb6c0202f6fe0de59c92ae81e15c938983`。使用 `git archive` 导出源码，7,396 个文件与固定提交逐文件一致。归档 SHA-256 为 `08a38f4c4cbc73987178a7ac1acc3fb3c4c8f40acad238b72cdd3d1361357ca2`。构建、安装与数据库初始化均独立完成，没有复用旧测试二进制或旧数据库。

| 对象 | 已核实身份与配置 | 用途 |
| --- | --- | --- |
| OpenHalo 主实例 | PostgreSQL 18.6 / aux_mysql 1.5，aarch64；GNU make，`--with-openssl --enable-debug --enable-cassert` | 功能与差分测试 |
| OpenHalo 崩溃实例 | 分离的 debug/cassert 与 release/no-cassert 安装和数据目录；release 保留调试符号 | 隔离复现崩溃 |
| 主基线 | Oracle MySQL Community Server **5.7.32**，InnoDB，linux/amd64 | 真实对照服务器 |
| 补充基线 | Oracle MySQL Community Server **5.7.44**，InnoDB，linux/amd64 | 仅复核四项差异 |

MySQL 镜像使用不可变引用：

```text
mysql@sha256:e08834258fcc0efd01df358222333919df53d4a0d9b2a54da05b204b822e3b7b
mysql@sha256:4bc6bc963e6d8443453676cae56536f4b8156d78bae03c0145cbe47c2aad73bb
```

第一项为 5.7.32，第二项为 5.7.44。记录了 `mysqld --version`、SQL 版本与版本说明、平台、启动参数和二进制哈希。MySQL 在 amd64 仿真下运行，OpenHalo 为原生 aarch64，因此本报告**不比较吞吐和延迟**。5.7.44 仅复核无符号值域、TIMESTAMP 时区、尾空格唯一性和可重复读可见性，均与 5.7.32 一致，不能称为完整的 5.7.44 验收。

两侧使用相同客户端：Oracle MySQL 5.7.32 CLI、PyMySQL 1.1.1、go-sql-driver/mysql v1.9.3、Connector/J 8.4.0。Go 测试与 JDBC 驱动从源码重编；Go 源码与固定上游模块一致，JDBC 完成了上游要求的插桩。另使用 MariaDB 10.5.29 作为导入客户端，未将其当作基线服务器。

首次构建包装命令在 build/install 成功后，因为检查了错误的共享库目录而返回 1。原始错误保留，实际 `lib/postgresql` 安装路径核实后完成了全新初始化。这属于测试脚本失败，不是产品编译失败。

## 测试方法与配置轨道 {#method}

共同框架记录 SQL 是否接受、带类型的值、二进制长度与十六进制、decimal 精度、时间小数秒、有定义的行顺序、字段元数据、影响行数、生成 ID、警告、错误码与 SQLSTATE、服务端状态，以及后续连接和数据状态。无序结果按多重集比较；没有唯一顺序的等权行不因换序记为排序缺陷。

保留两条轨道：新实例默认配置，以及明确请求共同设置（`SET NAMES utf8mb4`、开启 autocommit、会话 REPEATABLE READ）。后者只是**请求对齐**，不表示两个引擎已实现相同语义。OpenHalo 接受隔离级别设置，却未改变实测快照行为。没有通过放宽严格 SQL 模式掩盖失败。

| 设置 | OpenHalo | MySQL 5.7.32 | 如何解释 |
| --- | --- | --- | --- |
| `sql_mode` | 严格模式，缺少 `ONLY_FULL_GROUP_BY` | 严格模式，包含 `ONLY_FULL_GROUP_BY` | 所测非分组列查询仍被底层 PostgreSQL 拒绝 |
| 隔离级别 | 回显 RR；原生设置为 read committed | RR | 显式设置后行为仍然不同 |
| 服务端字符集 | utf8mb4 | latin1 | 驱动请求与数据库默认值分别记录 |
| 系统时区 | CST / Asia/Shanghai | UTC | TIMESTAMP 专项显式设置 +00:00 后切到 +08:00 |
| `lower_case_table_names` | 1 | 0 | 本轮配置下表名大小写行为不同 |
| `explicit_defaults_for_timestamp` | 1 | 0 | 首个 TIMESTAMP 的隐式默认不同 |
| `max_allowed_packet` | 64 MiB | 4 MiB | 默认上限不同，不能据此判断 OpenHalo 限包无效 |
| 握手认证 | caching_sha2_password | mysql_native_password | OpenHalo 回显的默认认证变量不能描述实际握手 |

为 OpenHalo 配置测试证书后执行 TLS 验证：PyMySQL 在 OpenHalo 协商为 TLS 1.3，在 MySQL 为 TLS 1.2。未覆盖证书链与主机名验证。TLS 连接成功与 `SHOW STATUS LIKE 'Ssl_cipher'` 元数据路径失败是两项不同结论。

## 可用范围与限制 {#usable-scope}

“已测范围等价”只适用于列出的断言。“条件支持”表示存在可用路径，但附带明确限制。接受但语义不同、错误成功、明确拒绝、崩溃、未测或环境阻塞分别记账。预期拒绝可以让测试断言通过，却不能算作功能已支持。

| 范围 | 本轮可用路径 | 条件与剩余限制 |
| --- | --- | --- |
| 客户端与协议 | CLI、Python、Go、JDBC 的共同连接与查询路径；prepared 执行、流式读取、ping | 外部套件仍有失败；认证能力与字段元数据有差异 |
| 二进制传输与连接 reset | 0x00–0xff 全字节、空 bytes、393,216 字节 long-data 往返；reset 清除未提交事务、变量、临时对象和预备句柄 | 尚未建立 BINARY 定长填充、全部压缩能力及所有包边界的兼容结论 |
| 普通数据类型 | 有符号整数边界、常用 varchar/text、显式声明的 DECIMAL、VARBINARY/BLOB、日内 TIME、DATETIME(0/3/6) | 完整 BIGINT UNSIGNED 值域、TIMESTAMP 时区、负/长 TIME、ENUM/SET 存在差异或失败 |
| DDL 与查询 | 基础表与索引操作、改名与清空、SELECT JOIN、子查询、UNION、LIMIT、基础 CRUD | JOIN UPDATE 崩溃；前缀键与外键约束未保持；未穷尽 ALTER 和 JOIN 形态 |
| AUTO_INCREMENT | 显式低值不降低设定起点；所测 LIKE 复制在显式导入后正确推进计数器 | 显式 NULL 组合、步长与偏移、生成键和影响行数仍有差异 |
| 事务与锁 | 提交/回滚、保存点、所测语句错误恢复、单行 FOR UPDATE 与共享锁 | RR、只读设置、删除重插竞争，以及更广泛的 InnoDB 锁语义仍有差异或未测 |
| 普通账号 | 补齐业务 schema 的 USAGE/CREATE 授权后，可建表、改表、自增、查询和诊断 | 初始漏授权属于夹具错误；未覆盖完整权限语义 |
| 重启恢复 | 两侧正常重启后四项断言、立即/强制恢复后四项断言均通过，覆盖持久性、回滚、可写性和排序规则 | 不涵盖所有崩溃窗口、存储故障、复制和故障切换 |

## 七项主要阻断问题 {#blocking-issues}

以下是实例可用性、数据完整性或依赖相应能力的应用上线阻断项，定为 P1。两项唯一性问题分别建 Issue，因为其实现与验收路径不同。

| 问题 | 真实 MySQL 5.7.32 | OpenHalo 实际行为与影响 | 证据用例 |
| --- | --- | --- | --- |
| [B01 · UPDATE JOIN](https://github.com/pgsty/openHalo/issues/1) | 更新一条匹配行 | debug 断言失败，release SIGSEGV；postmaster 终止其他 backend 并恢复 | `QUERY-UPDATE-JOIN`，独立 debug/release 日志 |
| [B02 · 外键](https://github.com/pgsty/openHalo/issues/2) | 非法子键报 1452；RESTRICT、CASCADE 保持关系 | 非法子键与受限父行删除成功，级联不执行；目录显示 `NOT ENFORCED` | `DDL-FK`、迁移业务链 |
| [B03 · REPEATABLE READ](https://github.com/pgsty/openHalo/issues/3) | B 提交 11 后，A 在同一事务两次仍读到 10 | A 读到 10→11，变量却回显 RR | `TXN-VISIBILITY-*` |
| [B04 · 只读设置](https://github.com/pgsty/openHalo/issues/4) | 全局只读拒绝普通用户写入，报 1290；事务只读报 1792 | 两类设置均返回成功，但所测写入仍成功 | `SETTING-READONLY-GLOBAL`、`TXN-READONLY` |
| [B05 · DECIMAL 导出](https://github.com/pgsty/openHalo/issues/5) | SHOW CREATE/重建保持精度和小数位数 | `DECIMAL(8,2)` 变为 `decimal`，重建丢失舍入和值域约束 | `DDL-DECIMAL-REPLAY` |
| [B06 · 排序规则唯一性](https://github.com/pgsty/openHalo/issues/6) | utf8mb4_bin 唯一键不允许 `a` 与 `a ` 共存 | 两行均接受；其他规则的比较权重也存在差异 | `COLL-BIN-SPACE`、`COLL-*` |
| [B07 · 前缀唯一性](https://github.com/pgsty/openHalo/issues/7) | `UNIQUE(v(3))` 拒绝 `abcdef` 与 `abcxyz` 共存，Sub_part 为 3 | 两行均接受，Sub_part 为 NULL | `DDL-PREFIX` |

各 Issue 包含固定环境、最小复现、实际结果、证据编号与验收条件。下面两个例子说明，仅有连接成功或 DDL 成功不足以建立兼容结论。

JOIN UPDATE 只需两张普通表和一条匹配行即可触发崩溃，只能在专用实例复现：

```sql
CREATE TABLE t(id INT PRIMARY KEY, v INT);
CREATE TABLE u(id INT PRIMARY KEY, v INT);
INSERT INTO t VALUES(1,1),(2,2);
INSERT INTO u VALUES(1,9);
UPDATE t JOIN u ON t.id=u.id SET t.v=u.v;
```

DECIMAL 的问题需要比较原表与根据 SHOW CREATE 输出重建的表：

```sql
CREATE TABLE t(n DECIMAL(8,2));
SHOW CREATE TABLE t;
```

OpenHalo 原表将 `1.2345` 舍入为 `1.23`，并以 1264 拒绝 `1234567.89`。将导出定义只改表名后重放，新表保留 `1.2345`，也接受 `1234567.89`。底层类型分别为 `numeric(8,2)` 与无精度限制的 `numeric`。这里改变的是数据规则，而不只是 DDL 的显示格式。

## 其他已确认差异 {#other-differences}

原始归档共记录二十个缺陷条目。上述七项阻断是首批专项 Issue；其余条目保留在研究待办中，不能视为已解决，也不能由单例失败推定整个功能族都不支持。

| 归档编号 / 功能 | 实际差异 | 应用影响 |
| --- | --- | --- |
| B08 · TIMESTAMP | +00:00 切换到 +08:00 后，OpenHalo 仍为 03:04:05.123456，MySQL 为 11:04:05.123456 | 跨时区时间解释不同 |
| B09 · 自增显式 NULL/0 | `(0,1),(NULL,2)` 在 OpenHalo 报 1048，MySQL 生成 ID；NO_AUTO_VALUE_ON_ZERO 下也不同 | 导入与插入习惯需要适配 |
| B10 · 自增步长/偏移 | 两侧回显 3/2，OpenHalo 生成 1、2、3，MySQL 生成 2、5、8 | 不能依赖这些设置分配 ID |
| B11 · REPLACE | OpenHalo 保留旧 ID、影响行数为 1；MySQL 生成新 ID、影响行数为 2 | 行身份与计数不同；未测触发器副作用 |
| B12 · UPDATE / ODKU 结果 | CLIENT_FOUND_ROWS 关闭时 OpenHalo 返回匹配行数，MySQL 返回改变行数；ODKU 的 ID/计数也不同 | 乐观更新与驱动结果判断可能出错 |
| B13 · BINARY(n) | BINARY(5) 的 `a ` 在 OpenHalo 为 2 字节，MySQL 为补 NUL 后的 5 字节 | 定长二进制值不等价 |
| B14 · ANSI_QUOTES | 设置成功，但双引号字符串/标识符没有按 MySQL 切换 | SQL 生成器可能改变含义或失败 |
| B15 · wait_timeout | 设置为 1、空闲 2 秒后，OpenHalo 仍接受查询，MySQL 断连 | 连接池超时假设失效 |
| B16 · 多语句中间语法错误 | OpenHalo 连错误前的语句也不执行；MySQL 保留前面已经提交的语句 | 部分执行与恢复逻辑不同 |
| B17 · 诊断与元数据 | 缺少 Note/1051、SHOW STATUS 失败、变量类型、别名大小写、flags/charset/scale、SQLSTATE 不同 | ORM 与驱动须逐路径验证 |
| B18 · CHAR 填充模式 | PAD_CHAR_TO_FULL_LENGTH 下两侧输出五字符，OpenHalo LENGTH 为 1，MySQL 为 5 | 输出与表达式语义不一致 |
| B19 · INSERT IGNORE | 截断使 OpenHalo 整条语句失败；MySQL 产生警告并插入其他有效行 | 导入进度与告警处理不同 |
| B20 · 无符号 64 位值域 | OpenHalo 拒绝 18446744073709551615，CAST(-1 AS UNSIGNED) 返回 -1 | 所测路径不能表示 MySQL 完整无符号值域 |

明确拒绝的样例包括 ENUM/SET、负或长 TIME、MySQL 存储过程/触发器/事件、DO、LOAD DATA、分区 DDL、常用 JSON/空间函数，以及所测生成列组合。JSON 能存储有效输入，不代表 JSON 函数可用。所测 CHECK 样例中，两侧均接受约束声明却允许违规值，与该 MySQL 5.7 样例一致；这不证明 CHECK 得到了执行。

受控的删除重插竞争复现了 3/3 次：A 删除并重插一行后，等待中的 B 在 OpenHalo 上 DELETE 影响 0 行，接着 INSERT 报 1062；MySQL 删除 1 行并成功重插。这解释了一类 sysbench 重复键错误。符合预期的 1213 死锁本身不自动列为缺陷。

## 测试统计与记账 {#test-accounting}

以下计数单位不同，不能相加，也不能换算为产品兼容率。

| 套件 / 范围 | OpenHalo | MySQL 5.7.32 |
| --- | --- | --- |
| 自带套件 | 22/22 组通过，无跳过；23 个 AB 断言包含在其中一组内 | 17 个共同可运行组中 15 通过，2 个夹具失败 |
| Go 全部顶层测试 | 142 通过 / 19 失败 / 2 跳过 | 161 通过 / 1 失败 / 1 跳过 |
| Go 服务端 driver_test.go 子集 | 51 通过 / 19 失败 / 2 跳过 | 70 通过 / 1 失败 / 1 跳过 |
| PyMySQL 全部用例 | 132 通过 / 30 失败 / 12 跳过 / 1 预期失败 | 默认库 161/1/12/1；utf8mb4 库 162/0/12/1 |
| PyMySQL 扣除 8 个纯客户端单元项 | 124 通过 / 30 失败 / 12 跳过 / 1 预期失败 | 默认库 153/1/12/1；utf8mb4 库 154/0/12/1 |
| SQL 目录 | 146 项：145 项双轨，加独立 debug/release 崩溃记录 | 相同输入逐项对照 |
| 补充用例 | 11 项协议、14 项并发/权限、9 项补测 | 按 case ID 配对 |
| 生命周期 | 每种重启模式各四项断言通过 | 每种重启模式各四项断言通过 |

MySQL 的自带 raw-statement 失败来自随产品提供的解码器假设；java-auth 查询了 PostgreSQL 专用的 `pg_stat_ssl`。两者都不是 MySQL 服务端缺陷。独立原始协议检查和共同 Java 语句/事务测试在两侧均执行。MySQL 唯一的 Go 失败是 TestLongData 压缩子场景触及默认 4 MiB 包限制；PyMySQL 的失败在明确使用 utf8mb4 测试库后消失，没有修改上游断言。

归档包含 701 条综合结果记录，混合重复运行、驱动单元项和配对摘要。SQL 原始标签为 206 条接受但不同、74 条拒绝/条件支持、6 条非 5.7、4 条观察项，其中包括字段元数据和诊断差异。这不代表 206 个独立缺陷，也不能构成兼容率分母。CTE、窗口函数、表达式默认值属于额外能力或负对照，排除在 MySQL 5.7 分母之外。

四种 sysbench 负载在两侧均完成。OpenHalo point-select/read-only 完成 109,227/11,206 个事件，无 ignored errors；read/write 完成 2,742 个事件、50 个 ignored errors，write-only 完成 1,289 个事件、53 个 ignored errors。MySQL 对应事件数为 377,680 / 21,855 / 12,279 / 28,015，ignored errors 为 0 / 0 / 43 / 115。写负载未逐事件记录重试，不能用“完成事件减 ignored errors”计算全程无错误事件数。verbose 错误样本也不是完整分布；这些数字只用于正确性与错误记账，不构成性能比较。

## 迁移试验 {#migration}

使用 Oracle mysqldump 5.7.32 导出三张关联表：customers 24 行、orders 72 行、items 216 行。模式包含主外键、唯一/复合索引、自增、ON UPDATE、中文/emoji、二进制字节、DECIMAL 和小数秒时间。数据生成 seed 为 573218；样本无符号 ID 没有超出有符号 BIGINT 范围。

原始 dump 的顺序为 customers → items → orders。虽然设置了 `FOREIGN_KEY_CHECKS=0`，OpenHalo 仍在 items 引用尚未创建的 orders 时以 1146 停止。另一次 `--force` 导入返回 0，却仍缺少 items；退出码为零不代表导入成功。

唯一适配是将完整表结构/数据块移动为 customers → orders → items，没有修改列定义、值、外键、SQL 模式或会话头尾。随后在 +00:00 查询时区下核对，行数、主键集合与带类型值一致。但继续运行的业务链未通过完整性检查：

| 操作 | OpenHalo | MySQL 5.7.32 |
| --- | --- | --- |
| 新 customer/order/item 的 ID | 25 / 73 / 217 | 25 / 73 / 217 |
| 重复 email | 拒绝，1062 | 拒绝，1062 |
| 删除仍被订单引用的 customer | 成功 | 拒绝，1451 |
| 插入引用不存在的 order999999 的 item | 成功 | 拒绝，1452 |
| 回滚金额修改 | 恢复 7.123456 | 恢复 7.123456 |
| 删除 order73 后剩余 item 数 | 1 | CASCADE 后为 0 |
| 链末 customers / orders / items | 24 / 72 / 218 | 25 / 72 / 216 |

两条迁移外键在 PostgreSQL 目录中均为 `conenforced=false`、`convalidated=false`。**适配后的数据搬运成功，应用语义未通过。** 重排 dump 不能解决外键、唯一性、时区、无符号值域或 DECIMAL 再次导出问题。本轮没有测试完整 ORM/应用启动或生产规模迁移。

## 专项研究与最小修复范围 {#research}

七个 Issue 各有一项独立调研，目标是找到恢复必要数据或事务规则的最小修改，并配套有意义的回归用例。本次研究不修改产品代码；源码诊断与修改建议也不等于已验证的修复。

| Issue | 源码结论 | 最小安全修改与验收边界 |
| --- | --- | --- |
| [B01 · UPDATE JOIN](https://github.com/pgsty/openHalo/issues/1) | `mys_rewrite.c:1180-1191` 直接信任嵌套 `RangeFunction` 列表；JOIN 语法还把表名 `A_Const` 节点混入 `UpdateStmt.targetList`，重写器却按 `ResTarget` 读取。 | 增加节点/列表形状检查，在遍历前返回 1235。随后只支持单目标、单右表、`INNER JOIN`、归一化 `ResTarget` 赋值和可证明唯一匹配；debug/release 都必须存活且结果一致。 |
| [B02 · 外键](https://github.com/pgsty/openHalo/issues/2) | `mys_gram.y:7103-7123` 的表级外键构造器没有设置 PG18 的 `Constraint.is_enforced`，因此 PostgreSQL 不创建执行约束和引用动作所需的触发器。 | 在共用表级构造器设置 `is_enforced=true`，保留正常验证，核对非法写入及 RESTRICT/CASCADE/SET NULL。`ALTER CONSTRAINT`、未适配的带外键 CTAS、`foreign_key_checks=0` 在实现前明确拒绝；盘点已有 `NOT ENFORCED` 数据。 |
| [B03 · REPEATABLE READ](https://github.com/pgsty/openHalo/issues/3) | `applySystemVarValue()` 没有把 `transaction_isolation` 或 `tx_isolation` 应用到 PostgreSQL MVCC；解析路径还把 SESSION 与 NEXT 作用域压成一类。 | 两个别名共享 GLOBAL/SESSION/NEXT 状态，在首次快照前应用隔离级别；验收 RR `10→10`、RC `10→11`、新连接、别名、reset 和 prepared。状态机未完成时应拒绝 RR，不能继续只回显 RR。 |
| [B04 · 只读设置](https://github.com/pgsty/openHalo/issues/4) | `read_only` 只写入兼容层 hash，没有跨 backend 写入闸门；`SET TRANSACTION READ ONLY` 变成会话变量赋值，而 `START TRANSACTION READ ONLY` 仍进入 PostgreSQL 原生保护。 | 在保存值前拒绝未实现的全局/SESSION/NEXT 设置；保留 `START TRANSACTION READ ONLY`，把真实只读事务错误映射为 1792/25006，并补只读状态位。完整全局实现还需要真正的跨 backend 闸门及权限/临时表规则。 |
| [B05 · DECIMAL 导出](https://github.com/pgsty/openHalo/issues/5) | SHOW 转换丢失 PostgreSQL numeric typmod，把 `numeric(8,2)` 输出为无界 `decimal`，回放后舍入和值域规则改变。 | 统一 COLUMN_TYPE、SHOW COLUMNS/FULL COLUMNS、SHOW CREATE 和精度/小数位元数据的 typmod 格式化；同步 SQL 生成器和升级路径。历史无界列无法可靠猜回原 typmod，不能臆造。 |
| [B06 · 排序规则唯一性](https://github.com/pgsty/openHalo/issues/6) | MySQL 名称被压缩成大小写敏感或 ICU 近似规则；C 排序规则没有 MySQL 5.7 的 PAD SPACE 与权重语义，原规则名也没有保留。 | 停止静默映射未实现名称，或明确标注近似规则。真正实现必须统一等值、排序、哈希、B-tree 和元数据；改变权重前先检查冲突并显式重建旧索引。 |
| [B07 · 前缀唯一性](https://github.com/pgsty/openHalo/issues/7) | 共用语法动作 `mys_gram.y:11063` 忽略前缀长度 `$3`，所以已接受的索引实际变成整列索引。 | 在 CREATE/ALTER/CREATE INDEX 的前缀语法完成元数据、字符/字节语义、SHOW 输出和冲突处理前统一返回 1235。不能只替换成表达式索引；应依据可信 DDL 盘点历史误建索引。 |

七项专项研究均已完成。这些是拟议的保护措施或修复设计，不是已经实施的产品修改；未来补丁完成后，每项验收边界都必须重新做 OpenHalo/MySQL 5.7 差分测试。

验收必须检查真实数据、约束、快照、连接存活和 DDL 重放。只改变量回显、错误标签或 SHOW 输出不能形成闭环。若完整语义需要较大工程，第一步可以明确拒绝不支持的语法；这属于防止错误成功，必须与真正实现 MySQL 功能区分。

## 证据与未测范围 {#evidence}

保留的证据集名称为 `mysql57-round2`，包含 REPORT、MYSQL57_SUPPORT、DIFFERENCES、BUGS、TEST_MATRIX、MIGRATION_TRIAL、带类型的 `results.jsonl`、脚本、用例、环境快照、原始日志，以及覆盖 635 个轻量文件的 SHA256SUMS。站点保存这份整理后的报告，完整本地归档未作为附件发布。对应 GitHub Issue 提供可独立阅读的最小复现和归档用例编号。

| 归档内证据路径 | 用途 |
| --- | --- |
| `artifacts/source-provenance.json`、`environment.json`、`artifacts/source-end.json` | 固定源码、二进制/环境、源码未变化证明 |
| `logs/sql-final.jsonl`、`logs/protocol.jsonl` | 逐语句与协议观察 |
| `logs/concurrency.jsonl`、`logs/supplement.jsonl` | 受控双连接顺序、普通账号、设置是否生效 |
| `logs/join-debug.jsonl`、`logs/join-release.jsonl`、`logs/crash-symbols.log` | 隔离崩溃与符号化调用栈 |
| `logs/precision-fk.jsonl`、`artifacts/native-constraint-types.json` | DDL 往返和原生目录证据 |
| `logs/migration-chain.json`、`artifacts/final-summary.json` | 业务不变量与统计单位 |

归档中的 `scripts/replay.sh` 可启动保留的测试实例，将重放日志写入新目录而不覆盖原结果。大型源码树、二进制、下载包、数据库和完整 dump 留在测试容器或专用卷内。测试轮结束时，三个 OpenHalo 测试实例与两个 MySQL 容器均已停止，共享开发容器保留运行。

未测范围包括全部客户端版本与认证模式、证书验证、完整字符集/排序规则/函数目录、所有 ALTER 与多表 DML 形态、SERIALIZABLE、READ UNCOMMITTED、XA、完整 gap/next-key 锁、存储故障窗口、MySQL 复制/binlog/GTID/PITR、故障切换、完整权限与安全、本提交的全部 PostgreSQL world 测试与六平台打包，以及真实应用/ORM 验收。本轮没有进行 OpenHalo 14 安全审计。

**“能用 MySQL 客户端连接”“握手显示 5.7.32”“SQL 被接受”都不等于 MySQL 5.7 语义兼容。** 可上线范围仍需由应用自己的模式、驱动、事务、迁移路径和运维假设共同验证。
