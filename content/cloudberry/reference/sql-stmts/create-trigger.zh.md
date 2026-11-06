---
title: "CREATE TRIGGER"
description: "定义新的触发器。Apache Cloudberry 不支持用户定义的触发器。"
weight: 900
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-trigger.md"
---

## 语法概要 {#synopsis}

```sql
CREATE TRIGGER <name> {BEFORE | AFTER} {<event> [OR ...]}
       ON <table> [ FOR [EACH] {ROW | STATEMENT} ]
       EXECUTE PROCEDURE <funcname> ( <arguments> )
```

## 说明 {#description}

`CREATE TRIGGER` 创建新的触发器。触发器会与指定的表关联，并在特定事件发生时运行指定的函数。如果为同一事件定义了多个相同类型的触发器，它们会按名称的字母顺序触发。

>*重要* 由于 Apache Cloudberry 系统具有分布式特性，Apache Cloudberry 对数据触发器的使用受到很大限制。触发器使用的函数必须是 `IMMUTABLE`，也就是说不能使用其参数列表中未直接提供的信息。触发器中指定的函数也不能运行任何 SQL，或以任何方式修改分布式数据库对象。由于触发器通常用于修改表（例如在一行更新时更新其他行），这些限制使触发器几乎没有实际用途。因此，Apache Cloudberry 不支持使用用户定义的触发器。触发器不能用于 AO 表。
> 事件触发器 只捕获 DDL 事件，Apache Cloudberry 支持此功能。更多信息请参见 PostgreSQL 文档中的 [事件触发器](https://www.postgresql.org/docs/12/event-triggers.html)。

[SELECT](/cloudberry/reference/sql-stmts/select/) 不会修改任何行，因此不能创建 `SELECT` 触发器。在这种情况下，规则和视图更合适。

## 参数 {#parameters}

**`name`**

新触发器的名称。该名称必须与同一表的其他触发器名称不同。

**`BEFORE AFTER`**

决定函数是在事件之前还是之后调用。如果触发器在事件之前触发，可以跳过当前行的操作，或更改正在插入的行（仅适用于 `INSERT` 和 `UPDATE` 操作）。如果触发器在事件之后触发，则所有更改（包括最后一次插入、更新或删除）对触发器都可见。

**`event`**

指定会触发触发器的事件（`INSERT`、`UPDATE` 或 `DELETE`）。可以使用 OR 指定多个事件。

**`table`**

触发器所属表的名称（可以用模式名限定）。

**`FOR EACH ROW`**<br />
**`FOR EACH STATEMENT`**

指定触发器过程是为触发事件影响的每一行调用一次，还是每条 SQL 语句只调用一次。如果两者都未指定，默认采用 `FOR EACH STATEMENT`。标记为 `FOR EACH ROW` 的触发器会在操作修改每一行时调用一次。相反，标记为 `FOR EACH STATEMENT` 的触发器对任意一次操作只运行一次，与操作修改的行数无关。

**`funcname`**

由用户提供的函数，声明为 `IMMUTABLE`、不接受参数并返回 `trigger` 类型；触发器触发时会运行该函数。此函数不得运行 SQL 或以任何方式修改数据库。

**`arguments`**

触发器运行时传给函数的可选参数逗号分隔列表。参数是字符串字面量。这里也可以写简单名称和数字常量，但它们都会转换为字符串。请查看触发器函数实现语言关于如何在函数内访问触发器参数的说明；其方式可能不同于普通函数参数。

## 注意事项 {#notes}

要在表上创建触发器，用户必须拥有该表的 `TRIGGER` 权限。

## 示例 {#examples}

声明触发器函数，然后声明触发器：

```sql
CREATE FUNCTION sendmail() RETURNS trigger AS 
'$GPHOME/lib/emailtrig.so' LANGUAGE C IMMUTABLE;

CREATE TRIGGER t_sendmail AFTER INSERT OR UPDATE OR DELETE 
ON mytable FOR EACH STATEMENT EXECUTE PROCEDURE sendmail();
```

## 兼容性 {#compatibility}

Apache Cloudberry 中的 `CREATE TRIGGER` 语句实现了 SQL 标准的一个子集。目前缺少以下功能：

- Apache Cloudberry 对触发器调用函数有严格限制，因此触发器的用途非常有限。出于这个原因，Apache Cloudberry 不正式支持触发器。
- SQL 允许触发器只在特定列更新时触发（例如 `AFTER UPDATE OF col1, col2`）。
- SQL 允许在触发器动作定义中为“旧”和“新”行或表定义别名（例如 `CREATE TRIGGER ... ON tablename REFERENCING OLD ROW AS somename NEW ROW AS othername ...`）。由于 Apache Cloudberry 允许使用任意数量的用户定义语言编写触发器过程，数据访问方式由具体语言决定。
- Apache Cloudberry 只允许触发器动作执行用户定义函数。标准还允许执行其他 SQL 命令，例如将 `CREATE TABLE` 作为触发器动作。通过创建运行所需命令的用户定义函数，可以较容易地绕过此限制。
- SQL 规定多个触发器应按创建时间顺序触发。Apache Cloudberry 使用名称顺序，因为这种方式被认为更方便。
- SQL 规定级联删除中的 `BEFORE DELETE` 触发器应在级联 `DELETE` 完成后触发。Apache Cloudberry 的行为是 `BEFORE DELETE` 始终在删除动作前触发，即使是级联删除。这样做被认为更加一致。
- 使用 `OR` 为单个触发器指定多个动作是 Apache Cloudberry 对 SQL 标准的扩展。

## 另请参阅 {#see-also}

[CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/), [ALTER TRIGGER](/cloudberry/reference/sql-stmts/alter-trigger/), [DROP TRIGGER](/cloudberry/reference/sql-stmts/drop-trigger/), [CREATE RULE](/cloudberry/reference/sql-stmts/create-rule/)
