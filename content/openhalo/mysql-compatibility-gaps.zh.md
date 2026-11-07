---
type: docs
upstream_source: openhalo-tests
upstream_link: "" # Original summary; cite the reference below without claiming an upstream licence.
upstream_ref: "OpenHalo 1.0.14.18 测试报告；提交 80a8d07"
upstream_notice: /zh/attribution/#openhalo-tests
title: 已知 MySQL 兼容边界
linkTitle: 兼容边界
description: 公开 OpenHalo 测试中需要改写或额外验证的 MySQL 功能。
weight: 60
---

独立的 [OpenHalo MySQL 兼容性测试报告](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md) 在 2025 年 11 月 27 日至 12 月 3 日使用 MySQL 5.7.32 客户端测试了 OpenHalo `1.0.14.18 (251127)`。报告共测试 57 项，通过 42 项、失败 15 项。73.7% 只是该测试集的通过比例，不是产品整体的兼容率。

这些结果是单个 OpenHalo 版本的历史迁移证据，不是 Halo Database 的官方支持矩阵。有些失败取决于具体语句和测试 schema。请在计划部署的版本和 schema 上重新执行实际语句。

## 报告中需要关注的功能 {#reported-boundaries}

| MySQL 功能或测试 | 测试版本中的结果 | 迁移方向 |
| --- | --- | --- |
| `JSON_EXTRACT`、`JSON_SET` 等 JSON 辅助函数 | 测试在函数解析阶段失败。 | 对照 PostgreSQL `json`/`jsonb` 操作符和函数，比较结果类型与 NULL 行为。 |
| 一种 `FORCE INDEX` 写法 | 报告中的确切索引提示测试在索引名处失败。 | 重新测试应用实际使用的提示，并先检查 PostgreSQL 执行计划再决定改写。 |
| MySQL 分区 DDL | `PARTITION BY RANGE (...)` 及 MySQL 分区子句失败。 | 转换为 PostgreSQL 分区语法，并重新检查分区剪枝和唯一键规则。 |
| 带 `BEGIN ... END` 的存储过程 | 创建 MySQL 过程时在过程体处失败。 | 改写为 PostgreSQL 函数、应用逻辑或目标版本支持的过程语言形式。 |
| `MATCH(...) AGAINST(...)` | MySQL 搜索表达式在 `AGAINST` 处失败。报告中索引 DDL 被接受并不能证明 MySQL 全文检索已实现，测试建索引的 schema 还有限制。 | 使用 PostgreSQL 全文检索，或单独验证完整的搜索工作负载。 |
| `POINT()`、`ST_Distance()` 等空间函数 | 测试运行中找不到这些函数。 | 使用经过验证的 PostgreSQL 空间实现并改写调用。 |
| `HANDLER` 语句 | MySQL 底层表访问语法在 `HANDLER` 处失败。 | 改用普通查询和索引。 |
| `USE` 后执行 `SHOW TABLE STATUS` | 测试报告 PostgreSQL `search_path` 无效且没有选中的 schema。 | 检查数据库、租户和 schema 的准备方式；这不能证明所有 `SHOW` 命令都不支持。 |
| MySQL `GET DIAGNOSTICS` | 语句在 `GET` 处失败。 | 使用客户端驱动返回的受影响行数，或在服务端函数中使用 PostgreSQL 诊断机制。 |
| `SELECT ... INTO OUTFILE` | 服务端导出子句在 `INTO` 处失败。 | 使用客户端输出重定向，或通过 PostgreSQL 连接使用 `COPY`。 |
| 报告中的 `UNION` 语句 | 确切测试在 `UNION` 前使用未加括号的 `LIMIT`，并在 `UNION` 处失败。 | 使用带括号的分支重新验证；不能据此推断所有 `UNION` 形式都不支持。 |

报告还指出，语法错误可能使当前 PostgreSQL 事务进入 aborted 状态。出现错误后，应执行 `ROLLBACK` 或建立新会话，再判断后续结果。

当前 Halo 1.0.16 参考资料单独记录了 `mysql.multi_table_delete_methond` 参数及其两种兼容模式。多表 `DELETE` 应在确切版本上重新测试，不能直接沿用旧 OpenHalo 结果。

## 报告中通过的功能 {#passed-features}

报告记录了以下成功案例：

- 基础 `SELECT`、`WHERE`、`LIKE`、`IS NULL`、`ORDER BY` 和 `LIMIT`；
- `GROUP BY`、`COUNT`、`AVG`、`MIN`、`MAX` 和 `FLOOR`；
- 普通 `INSERT`、`UPDATE` 和 `DELETE`；
- 普通索引和 `SHOW INDEX`；
- 内连接、左连接、多表连接和自连接；
- 视图、`START TRANSACTION`、`COMMIT` 和 `ROLLBACK`；
- `CONCAT`、`SUBSTRING`、`UPPER`、`LOWER`、`LENGTH`、`REPLACE` 和 `TRIM`；
- 唯一键、外键和检查约束；
- 派生表、相关子查询和 `EXISTS`。

Halo 官方手册另外在[兼容的 MySQL 语句](/openhalo/mysql-statements/)和[兼容的 MySQL 数据类型](/openhalo/mysql-data-types/)中整理了 MySQL 风格语法与类型。

## 迁移测试计划 {#test-plan}

切换应用前：

1. 使用生产环境相同的 MySQL 驱动、认证方式和监听端口连接。
2. 导入具有代表性的 schema，包括索引、约束、生成值、`ENUM`/`SET` 以及 dump 特有的语句。
3. 在隔离数据库中执行 DDL 和 DML，比较行数、结果类型、受影响行数、警告和错误码。
4. 测试事务、预处理语句、连接池、重试和会话变量。
5. 单独测试导出、存储程序、分区维护和优化器提示等管理任务。

不能因为客户端可以连接，或基础 CRUD 语句能够执行，就认定 MySQL 工作负载已经完成迁移。

## 资料来源 {#sources}

本页为 [OpenHalo MySQL 兼容性测试报告](https://github.com/fxcollot/openHaloDocumentation/blob/80a8d077b1d329e397b251fa8c64dbded303bba2/TestingReport/OpenHaloMySQLCompatibilityTestingReport.md)的原创摘要。上游未明确公开文档许可证；版本、版权与引用方式见[来源说明](/attribution/#openhalo-tests)。
