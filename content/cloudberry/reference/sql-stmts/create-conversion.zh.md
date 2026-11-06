---
title: "CREATE CONVERSION"
description: "定义一个新的编码转换。"
weight: 560
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-conversion.md"
---

## 概要 {#synopsis}

```sql
CREATE [DEFAULT] CONVERSION <name>
     FOR <source_encoding> TO <dest_encoding> FROM <function_name>
```

## 描述 {#description}

`CREATE CONVERSION` 定义一个新的字符集编码之间的转换。此外，标记为 `DEFAULT` 的转换可用于客户端与服务器之间的自动编码转换。为此，必须定义两个转换：从编码 A 到 B *以及*从编码 B 到 A。

要创建转换，必须对函数具有 `EXECUTE` 权限，并对目标模式具有 `CREATE` 权限。

## 参数 {#parameters}

**`DEFAULT`**

表示该转换是此特定源编码到目标编码的默认转换。一个模式中，每个编码对应只应有一个默认编码转换。

**`name`**

转换的名称。转换名称可以带模式限定。如果不带模式限定，则在当前模式中定义该转换。转换名称在模式内必须唯一。

**`source_encoding`**

源编码名称。

**`dest_encoding`**

目标编码名称。

**`function_name`**

用于执行转换的函数。函数名可以带模式限定。如果不带模式限定，则会在路径中查找该函数。该函数必须具有以下签名：

```sql
conv_proc(
    integer,  -- source encoding ID
    integer,  -- destination encoding ID
    cstring,  -- source string (null terminated C string)
    internal, -- destination (fill with a null terminated C string)
    integer   -- source string length
) RETURNS void;
```

## 注解 {#notes}

使用 [DROP CONVERSION](/cloudberry/reference/sql-stmts/drop-conversion/) 删除用户定义的转换。

创建转换所需的权限可能会在未来版本中改变。

注意，在本版本的 Apache Cloudberry 中，用户定义转换所使用的用户定义函数必须定义为 `IMMUTABLE`。自定义函数的任何已编译代码（共享库文件）必须放在 Apache Cloudberry 阵列（Coordinator 和所有 Segment）中每台主机上的同一位置。该位置还必须在 `LD_LIBRARY_PATH` 中，以便服务器能够找到这些文件。

## 示例 {#examples}

使用 `myfunc` 创建从编码 `UTF8` 到 `LATIN1` 的转换：

```sql
CREATE CONVERSION myconv FOR 'UTF8' TO 'LATIN1' FROM myfunc;
```

## 兼容性 {#compatibility}

`CREATE CONVERSION` 是 Apache Cloudberry 的扩展。SQL 标准中没有 `CREATE CONVERSION` 语句，但有一个在目的和语法上非常相似的 `CREATE TRANSLATION` 语句。

## 另见 {#see-also}

[ALTER CONVERSION](/cloudberry/reference/sql-stmts/alter-conversion/)、[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)、[DROP CONVERSION](/cloudberry/reference/sql-stmts/drop-conversion/)
