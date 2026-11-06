---
title: "CREATE LANGUAGE"
description: "定义新的过程语言。"
weight: 660
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-language.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [ OR REPLACE ] [ PROCEDURAL ] LANGUAGE <name>

CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE <name>
    HANDLER <call_handler>
   [ INLINE <inline_handler> ] 
   [ VALIDATOR <valfunction> ]
            
```

## 说明 {#description}

`CREATE LANGUAGE` 在 Apache Cloudberry 中注册新的过程语言。之后可以使用这种新语言定义函数和过程。

> **注意** Apache Cloudberry 的过程语言已成为“扩展”，因此应使用 [CREATE EXTENSION](/cloudberry/reference/sql-stmts/create-extension/) 安装，而不是使用 `CREATE LANGUAGE`。直接使用 `CREATE LANGUAGE` 应限于扩展安装脚本。如果数据库中存在“裸”语言（例如升级产生的语言），可以使用 `CREATE EXTENSION <langname> FROM unpackaged` 将其转换为扩展。

`CREATE LANGUAGE` 实际上将语言名称与处理函数关联起来，这些函数负责执行以该语言编写的函数。

`CREATE LANGUAGE` 命令有两种形式。第一种形式只提供所需语言的名称，Apache Cloudberry 服务器会查询 `pg_pltemplate` 系统目录以确定正确的参数。第二种形式在语言名称之外提供语言参数。第二种形式可用于创建 `pg_pltemplate` 中未定义的语言，但现在已视为过时方式。

当服务器在 `pg_pltemplate` 目录中找到给定语言名称的条目时，即使命令包含语言参数，也会使用目录中的数据。这种行为简化了旧转储文件的加载，因为其中可能包含过时的语言支持函数信息。

通常，用户必须拥有 Apache Cloudberry 超级用户权限才能注册新语言。不过，如果语言列在 `pg_pltemplate` 目录中，并标记为允许数据库所有者创建（`tmpldbacreate` 为 `true`），数据库所有者就可以在该数据库中注册新语言。默认情况下，数据库所有者可以创建受信任语言；超级用户可以通过修改 `pg_pltemplate` 的内容调整此设置。语言的创建者会成为其所有者，之后可以删除、重命名语言，或将其分配给新的所有者。

`CREATE OR REPLACE LANGUAGE` 可以创建新语言，也可以替换现有定义。如果语言已存在，则根据指定的值或从 `pg_pltemplate` 获取的值更新其参数，但语言的所有权和权限设置不会改变，并且假定该语言中已有的函数仍然有效。除创建语言所需的通常权限外，用户还必须是超级用户或现有语言的所有者。`REPLACE` 形式主要用于确保语言存在。如果语言在 `pg_pltemplate` 中有条目，则 `REPLACE` 不会实际改变现有定义；只有在语言创建后 `pg_pltemplate` 条目被修改这一不常见情况下才会改变。

## 参数 {#parameters}

**`TRUSTED`**

`TRUSTED` 指定该语言不会访问用户本来无权访问的数据。注册语言时如果省略此关键字，则只有拥有 Apache Cloudberry 超级用户权限的用户才能使用该语言创建新函数。

**`PROCEDURAL`**

这是一个无实际意义的噪声词。

**`name`**

新过程语言的名称。该名称必须在数据库中的语言之间唯一。
为保持向后兼容，名称可以用单引号括起来。

**`HANDLER call_handler`**

先前注册的函数名称；该函数将被调用以运行过程语言的函数。过程语言的调用处理函数必须使用带有版本 1 调用约定的编译语言（例如 C）编写，并在 Apache Cloudberry 中注册为无参数且返回 `language_handler` 类型的函数。这是一个占位类型，仅用于标识调用处理函数。

**`INLINE inline_handler`**

先前注册的函数名称；执行 [DO](/cloudberry/reference/sql-stmts/do/) 命令创建的、该语言中的匿名代码块时会调用此函数。如果未指定 inline_handler 函数，则该语言不支持匿名代码块。处理函数必须接受一个 `internal` 类型的参数，即 [DO](/cloudberry/reference/sql-stmts/do/) 命令的内部表示。该函数通常返回 `void`，其返回值会被忽略。

**`VALIDATOR valfunction`**

先前注册的函数名称；创建语言中的新函数时会调用该函数，以验证新函数。如果未指定验证函数，Apache Cloudberry 在创建新函数时不会检查它。验证函数必须接受一个 `oid` 类型的参数，该参数是待创建函数的 OID，通常返回 `void`。

验证函数通常会检查函数体的语法正确性，也可以检查函数的其他属性，例如该语言是否无法处理某些参数类型。要报告错误，验证函数应使用 `ereport()` 函数。函数的返回值会被忽略。

> **注意** 如果服务器在 `pg_pltemplate` 中有指定语言名称的条目，则会忽略 `TRUSTED` 选项和支持函数名称。

## 注意事项 {#notes}

使用 [DROP LANGUAGE](/cloudberry/reference/sql-stmts/drop-language/) 删除过程语言。

系统目录 pg_language 记录当前已安装语言的信息。此外，psql 命令 `\dL` 会列出已安装的语言。

要在过程语言中创建函数，用户必须拥有该语言的 `USAGE` 权限。默认情况下，受信任语言会向 `PUBLIC`（所有人）授予 `USAGE`。如有需要，可以撤销该权限。

过程语言属于各个数据库。不过，可以将语言安装到 `template1` 数据库中，这样它会自动出现在之后创建的所有数据库中。

如果服务器没有该语言在 `pg_pltemplate` 中的条目，则调用处理函数、内联处理函数（如果有）和验证函数（如果有）必须已经存在。但如果存在目录条目，这些函数无需预先存在；如果数据库中没有它们，系统会自动定义。（如果实现该语言的共享库在安装中不可用，`CREATE LANGUAGE` 可能因此失败。）

## 示例 {#examples}

创建任何标准过程语言的首选方式是使用 `CREATE EXTENSION` 而不是 `CREATE LANGUAGE`。例如：

```sql
CREATE EXTENSION plperl;
```

对于 `pg_pltemplate` 目录中未知的语言，需要执行类似下面的步骤：

```sql
CREATE FUNCTION plsample_call_handler() RETURNS 
language_handler
    AS '$libdir/plsample'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

## 兼容性 {#compatibility}

`CREATE LANGUAGE` 是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[ALTER LANGUAGE](/cloudberry/reference/sql-stmts/alter-language/), [CREATE EXTENSION](/cloudberry/reference/sql-stmts/create-extension/), [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [DROP LANGUAGE](/cloudberry/reference/sql-stmts/drop-language/), [GRANT](/cloudberry/reference/sql-stmts/grant/), [DO](/cloudberry/reference/sql-stmts/do/)
