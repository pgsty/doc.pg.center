---
title: gp_exttable_fdw
description: gp_exttable_fdw 是 Apache Cloudberry 用于实现外部表的外部数据包装器。
weight: 80
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/gp-exttable-fdw.md
---

`gp_exttable_fdw` 模块是 Apache Cloudberry 用于实现外部表的外部数据包装器。外部表在系统目录中存储为属于 `gp_exttable_server` 外部服务器的外表，由 `gp_exttable_fdw` 扫描或写入。

> [!NOTE]
> `gp_exttable_fdw` 和 `gp_exttable_server` 是为向后兼容外部表而保留的特殊内置对象。日常操作中不要直接使用此包装器，应通过 [`CREATE EXTERNAL TABLE`](/cloudberry/reference/sql-stmts/create-external-table/) 定义外部表。

## 安装 {#installation}

`gp_exttable_fdw` 始终随 Apache Cloudberry 构建和安装。它属于默认的 `gpcontrib` 构建目标，不依赖任何 `configure` 选项。

此模块以扩展形式打包（版本为 `1.0`，不可迁移到其他模式），对象创建在 `pg_catalog` 模式中。`initdb` 在集群初始化时注册此扩展，因此无需运行 `CREATE EXTENSION`。它不需要 `shared_preload_libraries`，也不需要重启。

## 模块提供的对象 {#objects-provided-by-the-module}

| 对象 | 类型 | 说明 |
|---|---|---|
| `gp_exttable_fdw` | 外部数据包装器 | 外部表的包装器。以 `gp_exttable_fdw_handler()` 为处理器，以 `gp_exttable_permission_check()` 为验证器。 |
| `gp_exttable_server` | 外部服务器 | 所有外部表所属的服务器。 |
| `gp_exttable_fdw_handler()` | 函数 | FDW 处理器，支持外表扫描和外表插入。 |
| `gp_exttable_permission_check(text[], oid)` | 函数 | FDW 验证器，检查表选项和当前角色的权限。 |
| `pg_exttable()` | 函数 | 每个外部表返回一行，在 Coordinator 上运行。 |
| `pg_exttable` | 视图 | 定义为 `SELECT * FROM pg_exttable()`。 |

### pg_exttable 视图 {#the-pg_exttable-view}

`pg_exttable` 视图显示存储在 `gp_exttable_server` 各个外表选项中的外部表定义。

| 列 | 类型 | 说明 |
|---|---|---|
| `reloid` | `oid` | 外部表的 OID。 |
| `urilocation` | `text[]` | 外部表的位置 URI。 |
| `execlocation` | `text[]` | 外部表运行的 Segment 位置。 |
| `fmttype` | `"char"` | 外部数据的格式类型。 |
| `fmtopts` | `text` | 格式选项。 |
| `options` | `text[]` | 使用 `LOG ERRORS PERSISTENTLY` 创建表时为 `{error_log_persistent=true}`，否则为 `NULL`。 |
| `command` | `text` | `EXECUTE` 外部表要运行的操作系统命令。 |
| `rejectlimit` | `int4` | 单行错误处理的拒绝上限。不使用单行错误处理时为 `NULL`。 |
| `rejectlimittype` | `"char"` | 拒绝上限的类型：`r` 表示行数，`p` 表示百分比。不使用单行错误处理时为 `NULL`。 |
| `logerrors` | `bool` | 是否记录错误。 |
| `encoding` | `int4` | 外部数据的编码 ID。使用 `pg_encoding_to_char(encoding)` 获取名称。 |
| `writable` | `bool` | 此表是否为可写外部表。 |

例如：

```sql
SELECT reloid::regclass, urilocation, pg_encoding_to_char(encoding)
FROM pg_exttable;
```

## 外表选项 {#foreign-table-options}

`gp_exttable_fdw` 的验证器检查属于 `gp_exttable_server` 的外表的以下选项：

| 选项 | 说明 |
|---|---|
| `format_type` | 必需。取值为 `t`（文本）、`c`（CSV）或 `b`（自定义）。 |
| `location_uris` | 位置 URI，以 `\|` 字符分隔。必须指定 `location_uris` 或 `command` 之一，不能同时指定。 |
| `command` | `EXECUTE` 外部 Web 表的命令。只有超级用户可以设置此选项。 |
| `is_writable` | 布尔值，标记表是否可写。 |
| `reject_limit_type` | `r`（行数，默认值）或 `p`（百分比）。 |
| `reject_limit` | 单行错误处理的拒绝上限，不能用于可写外部表。 |
| `encoding` | 编码名称（例如 `UTF8` 或 `GBK`），或数字编码 ID。 |

非超级用户角色创建表时，验证器还会检查该角色是否有权针对位置 URI 的协议创建外部表。

位置 URI 中的字面字符 `|` 或 `\` 必须在 `location_uris` 选项值中转义为 `\|` 或 `\\`。
