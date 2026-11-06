---
title: "CREATE PROCEDURE"
description: "定义新的过程。"
weight: 720
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-procedure.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [OR REPLACE] PROCEDURE <name>    
    ( [ [<argmode>] [<argname>] <argtype> [ { DEFAULT | = } <default_expr> ] [, ...] ] )
  { LANGUAGE <lang_name>
    | TRANSFORM { FOR TYPE <type_name> } [, ... ]
    | { [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER }
    | SET <configuration_parameter> { TO <value> | = <value> | FROM CURRENT }
    | AS '<definition>'
    | AS '<obj_file>', '<link_symbol>' 
  } ...
```

## 说明 {#description}

`CREATE PROCEDURE` 定义新的过程。`CREATE OR REPLACE PROCEDURE` 可以创建新过程，也可以替换现有定义。要定义过程，用户必须对该语言拥有 `USAGE` 权限。

如果包含模式名，则过程会在指定模式中创建；否则在当前模式中创建。新过程的名称不能与同一模式中具有相同输入参数类型的现有过程相同。不过，不同参数类型的过程和函数可以共享名称（即重载）。

要更新现有过程的当前定义，请使用 `CREATE OR REPLACE PROCEDURE`。这种方式不能更改过程名称或参数类型（那实际上会创建一个新的、不同的过程）。

使用 `CREATE OR REPLACE PROCEDURE` 替换现有过程时，过程的所有权和权限不会改变。其他过程属性会采用命令中指定或隐含的值。必须拥有该过程才能替换它（包括属于其所有者角色的成员）。

创建过程的用户会成为该过程的所有者。

要创建过程，必须对参数类型拥有 `USAGE` 权限。

有关创建过程的更多信息，请参阅 PostgreSQL 文档中的 [用户定义过程](https://www.postgresql.org/docs/12/xproc.html) 一节。

## 参数 {#parameters}

**`name`**

要创建的过程名称（可以用模式名限定）。

**`argmode`**

参数模式：`IN`、`INOUT` 或 `VARIADIC` 之一。省略时默认为 `IN`。（当前不支持过程的 `OUT` 参数，请改用 `INOUT`。）

**`argname`**

参数名称。

**`argtype`**

过程参数的数据类型（可用模式名限定，如果有）。参数类型可以是基本类型、复合类型或域类型，也可以引用表列的类型。

根据实现语言，还可能允许使用 `cstring` 等伪类型。伪类型表示实际参数类型未完整指定，或不属于普通 SQL 数据类型集合。

通过写成 `table_name.column_name%TYPE` 来引用列类型。使用此功能有时可以使过程不受表定义变化的影响。

**`default_expr`**

参数未指定时使用的默认值表达式。该表达式必须可转换为参数类型。参数列表中位于带默认值参数之后的每个输入参数也必须有默认值。

**`lang_name`**

过程实现所用语言的名称。可以是 `SQL`、`C`、`internal` 或用户定义过程语言的名称，例如 `plpgsql`。用单引号括起名称已弃用，并且要求大小写匹配。

**`TRANSFORM { FOR TYPE type_name } [, ... ] }`**

列出调用过程时应应用的转换。转换在 SQL 类型与语言特定数据类型之间转换。过程语言实现通常已硬编码了解内置类型，因此无需在此列出。如果过程语言实现不知道如何处理某种类型且未提供转换，它会回退到默认的数据类型转换行为，但具体行为取决于实现。

**`[EXTERNAL] SECURITY INVOKER`**<br />
**`[EXTERNAL] SECURITY DEFINER`**

`SECURITY INVOKER`（默认值）表示过程以调用用户的权限运行。

`SECURITY DEFINER` 指定过程以创建该过程的用户权限运行。

允许使用关键字 `EXTERNAL` 以符合 SQL，但它是可选的，因为与 SQL 不同，此功能适用于所有过程，而不只是外部过程。

`SECURITY DEFINER` 过程不能执行事务控制语句（例如 `COMMIT` 和 `ROLLBACK`，具体取决于语言）。

**`configuration_parameter`**

**`value`**

`SET` 子句在进入过程时为会话配置参数设置值。过程退出时恢复配置参数之前的值。`SET FROM CURRENT` 会保存运行 `CREATE PROCEDURE` 时参数的当前值，并将其作为进入过程时要应用的值。

如果过程附带 `SET` 子句，则在过程中针对同一变量执行的 `SET LOCAL` 命令的效果仅限于该过程：过程退出时仍会恢复配置参数的之前值。不过，普通的 `SET` 命令（不带 `LOCAL`）会覆盖 `SET` 子句，就像它覆盖之前的 `SET LOCAL` 命令一样；除非当前事务回滚，否则该命令的效果会在过程退出后继续存在。

如果过程附带 `SET` 子句，则该过程不能执行事务控制语句（例如 `COMMIT` 和 `ROLLBACK`，具体取决于语言）。

有关允许的参数名称和值的更多信息，请参见 [SET](/cloudberry/reference/sql-stmts/set/)。

**`definition`**

定义过程的字符串常量；其含义取决于语言。它可以是内部过程名称、对象文件路径、SQL 命令，或过程语言中的文本。

使用美元引用（参见 PostgreSQL 文档中的 [美元引用字符串常量
](https://www.postgresql.org/docs/12/sql-syntax-lexical.html#SQL-SYNTAX-DOLLAR-QUOTING)）编写过程定义字符串通常很有帮助，而不是使用普通的单引号语法。不使用美元引用时，过程定义中的单引号或反斜杠必须通过重复进行转义。

**`obj_file, link_symbol`**

这种 `AS` 子句形式用于动态加载的 C 语言过程：C 语言源代码中的过程名与 SQL 过程名不同时使用。字符串 obj_file 是包含动态加载对象的文件名，其解释方式与 [LOAD](/cloudberry/reference/sql-stmts/load/) 命令相同。字符串 link_symbol 是 C 语言源代码中的过程名称。如果省略链接符号，则假定它与正在定义的 SQL 过程名称相同。

重复的 `CREATE PROCEDURE` 调用引用同一对象文件时，每个会话只加载该文件一次。要卸载并重新加载文件（例如开发期间），请启动新会话。

## 注意事项 {#notes}

有关同样适用于过程的函数创建详情，请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

使用 [CALL](/cloudberry/reference/sql-stmts/call/) 执行过程。

## 示例 {#examples}

```sql
CREATE PROCEDURE insert_data(a integer, b integer)
LANGUAGE SQL
AS $$
INSERT INTO tbl VALUES (a);
INSERT INTO tbl VALUES (b);
$$;

CALL insert_data(1, 2);
```

## 兼容性 {#compatibility}

SQL 标准定义了 `CREATE PROCEDURE` 命令。Apache Cloudberry 的版本与标准相似，但并不完全兼容。详情也请参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)。

## 另请参阅 {#see-also}

[ALTER PROCEDURE](/cloudberry/reference/sql-stmts/alter-procedure/), [DROP PROCEDURE](/cloudberry/reference/sql-stmts/drop-procedure/), [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [CALL](/cloudberry/reference/sql-stmts/call/)
