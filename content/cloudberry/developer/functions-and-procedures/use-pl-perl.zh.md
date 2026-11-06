---
title: "使用 PL/Perl"
description: "PL/Perl 是一种嵌入式过程语言，允许使用 Perl 编程语言编写 PostgreSQL 函数。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/developer/functions-and-procedures/use-pl-perl.md"
---

使用 PL/Perl 可以：

- 用 Perl 编写函数，并从 SQL 调用这些函数。
- 使用 Perl 强大的字符串处理功能。
- 使用可用的 Perl 模块。

## 启用 PL/Perl {#enable-plperl}

要使用 PL/Perl，必须在数据库中启用它。

1. 使用 `psql` 连接数据库。

    ```bash
    psql -d <database_name>
    ```

2. 创建 `plperl` 扩展。

    ```sql
    CREATE EXTENSION plperl;
    ```

    这会注册受信任的 `plperl` 语言。如果需要不受信任的语言，请使用 `CREATE EXTENSION plperlu`。

## 编写 PL/Perl 函数 {#write-plperl-functions}

使用标准 SQL `CREATE FUNCTION` 语法定义 PL/Perl 函数。函数体是普通的 Perl 代码。

```sql
CREATE FUNCTION perl_max (integer, integer)
RETURNS integer
AS $$
    if ($_[0] > $_[1]) { return $_[0]; }
    return $_[1];
$$ LANGUAGE plperl;
```

### 参数和结果 {#arguments-and-results}

- 通过 `@_` 数组访问参数。
- 使用 `return` 语句或将最后一个求值的表达式作为结果返回。
- 要返回 SQL `NULL`，请返回 Perl 的 `undef`。

### 严格函数 {#strict-functions}

默认情况下，调用 PL/Perl 函数时传入的参数不为空。如果传入 SQL `NULL`，除非指定 `STRICT`，否则结果为 `NULL`。

```sql
CREATE FUNCTION perl_max_strict (integer, integer)
RETURNS integer
AS $$
    if ($_[0] > $_[1]) { return $_[0]; }
    return $_[1];
$$ LANGUAGE plperl STRICT;
```

## 内置函数 {#built-in-functions}

PL/Perl 提供了通过内置函数访问数据库的能力。

- `spi_exec_query(query [, limit])`：执行查询并返回结果。
- `elog(level, msg)`：输出日志消息。

使用 `spi_exec_query` 的示例：

```sql
CREATE OR REPLACE FUNCTION return_match(varchar) RETURNS SETOF test AS $$
    my $rv = spi_exec_query('select * from test;');
    my $nrows = $rv->{processed};
    foreach my $rn (0 .. $nrows - 1) {
        my $row = $rv->{rows}[$rn];
        if (index($row->{v}, $_[0]) != -1) {
            return_next($row);
        }
    }
    return undef;
$$ LANGUAGE plperl;
```

## 安全性和限制 {#security-and-limitations}

- **受信任语言（`plperl`）**：限制文件系统操作和其他可能不安全的操作。任何用户都可以使用 `plperl` 创建函数。
- **不受信任语言（`plperlu`）**：允许不受限制地访问系统。只有超级用户可以使用 `plperlu` 创建函数。
- **限制**：
    - Apache Cloudberry 不支持 PL/Perl 触发器。
    - PL/Perl 函数不能直接相互调用。
