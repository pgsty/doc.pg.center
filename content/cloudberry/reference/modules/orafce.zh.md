---
title: orafce
description: orafce 在 Apache Cloudberry 中提供兼容 Oracle 的 SQL 函数、数据类型和包。
weight: 170
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/orafce.md
---

`orafce` 模块在 Apache Cloudberry 中提供兼容 Oracle 的 SQL 函数、数据类型和包。它实现了 Oracle RDBMS 中部分函数和包，帮助迁移 Oracle 应用。

Apache Cloudberry 中的此模块是开源 [Orafce](https://github.com/orafce/orafce) 扩展的修改版。源码文件位于 Apache Cloudberry 源码的 `gpcontrib/orafce` 目录，基于 Orafce 4.9（4.9.2）。

## 安装 {#installation}

`orafce` 默认不构建。要随 Apache Cloudberry 构建并安装此模块，在运行 `configure` 时指定 `--enable-orafce` 选项：

```shell
./configure --enable-orafce [other options...]
make
make install
```

此模块是一个扩展（版本为 `4.9`，不可迁移到其他模式）。使用前，在每个需要使用它的数据库中创建扩展：

```sql
CREATE EXTENSION orafce;
```

## 模式 {#schemas}

扩展在以下模式中创建对象：

| 模式 | 内容 |
|---|---|
| `oracle` | 兼容 Oracle 的函数（例如 `oracle.substr()`、`oracle.add_months()`、`oracle.nvl2()` 和 `oracle.sysdate()`）、`oracle.date` 域、`oracle.varchar2` 和 `oracle.nvarchar2` 数据类型，以及 `oracle.dual` 视图。 |
| `dbms_output` | `DBMS_OUTPUT` 包。 |
| `dbms_pipe` | `DBMS_PIPE` 包。 |
| `dbms_utility` | `DBMS_UTILITY` 包。 |
| `dbms_assert` | `DBMS_ASSERT` 包。 |
| `dbms_random` | `DBMS_RANDOM` 包。 |
| `dbms_sql` | `DBMS_SQL` 包。 |
| `utl_file` | `UTL_FILE` 包。 |
| `plvstr`, `plvchr`, `plvdate`, `plvsubst`, `plvlex` | PLVision 的字符串、字符、日期、替换和词法分析器包。 |
| `plunit` | PLUnit 断言函数。 |

## 用法 {#usage}

要在调用 `oracle` 模式中的函数时省略模式限定，将该模式加入搜索路径。例如，以下命令设置数据库的默认搜索路径：

```sql
ALTER DATABASE db_name SET search_path = "$user", public, oracle;
```

`oracle` 模式中的部分函数与内置函数同名，例如 `oracle.substr()`。默认先搜索内置的 `pg_catalog` 模式。要优先使用兼容 Oracle 的版本，可以在函数名前加模式限定，或在搜索路径中将 `oracle` 放在 `pg_catalog` 之前：

```sql
SET search_path TO oracle, "$user", public, pg_catalog;
```

例如：

```sql
SET search_path TO public, oracle;
SELECT add_months(date '2003-08-01', 3);
```

```
 add_months
------------
 2003-11-01
(1 row)
```

可以将 `oracle.varchar2` 和 `oracle.nvarchar2` 数据类型用作表的分布键或分区键：

```sql
CREATE TABLE t1 (str oracle.varchar2(30)) DISTRIBUTED BY (str);
```

### 配置参数 {#configuration-parameters}

此模块定义以下配置参数，可以在会话中通过 `SET` 设置。

| 参数 | 默认值 | 说明 |
|---|---|---|
| `orafce.nls_date_format` | 未设置 | 模拟 Oracle 的日期输出行为。 |
| `orafce.timezone` | `GMT` | `oracle.sysdate()` 函数使用、`oracle.dbtimezone()` 返回的时区。 |
| `orafce.varchar2_null_safe_concat` | `false` | `varchar2` 值的连接是否能安全处理空值。 |
| `orafce.sys_guid_source` | `uuid_generate_v1` | `oracle.sys_guid()` 用于生成结果的函数：`uuid-ossp` 扩展中的 `uuid_generate_v1`、`uuid_generate_v1mc` 或 `uuid_generate_v4`，或内置的 `gen_random_uuid`。在此版本中，值 `uuid_generate_v4` 会存储为 `uuid_generate_v1`。 |
| `orafce.using_substring_zero_width_in_substr` | `warning_oracle` | 子串长度参数为零时，`substr()` 函数的行为。有效值为 `warning_oracle`、`warning_orafce`、`oracle` 和 `orafce`。 |

## 与原始 Orafce 扩展的区别 {#differences-from-the-original-orafce-extension}

Apache Cloudberry 中的此模块与原始 Orafce 4.9 扩展有以下区别：

- 不创建 `oracle.decode()` 函数。Apache Cloudberry 内置支持 `decode()`：解析器将 `decode()` 调用转换为 `CASE` 表达式，因此无需 `orafce` 扩展即可使用 `decode()`。例如：

    ```sql
    SELECT decode(2, 1, 'ABC', 2, 'DEF');
    ```

    ```
     case
    ------
     DEF
    (1 row)
    ```

- 不提供 `dbms_alert` 包。由于其实现无法在 MPP 环境中运行，因此不创建 `dbms_alert` 模式及其函数。

> [!NOTE]
> Apache Cloudberry 所基于的 PostgreSQL 14 已内置 `sinh()`、`cosh()` 和 `tanh()` 函数。参见 PostgreSQL 文档中的[数学函数和操作符](https://www.postgresql.org/docs/14/functions-math.html)。使用这些函数无需安装 `orafce`。

## 更多文档 {#additional-documentation}

此模块各个函数及相关对象的详细信息，参见 Apache Cloudberry 源码 [`gpcontrib/orafce`](https://github.com/apache/cloudberry/tree/REL_2_STABLE/gpcontrib/orafce) 目录下的以下文件：

- `README.asciidoc`
- `doc/orafce_documentation` 目录中的文档
- `doc/sql_migration` 目录中的 Oracle 到 PostgreSQL 迁移说明
