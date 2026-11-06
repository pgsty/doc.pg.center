---
title: "CREATE SCHEMA"
description: "定义新的模式。"
weight: 780
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-schema.md"
---

## 概要 {#synopsis}

```sql
CREATE SCHEMA <schema_name> [AUTHORIZATION <role_specification>] 
   [<schema_element> [ ... ]]

CREATE SCHEMA AUTHORIZATION <role_specification> [<schema_element> [ ... ]]

CREATE SCHEMA IF NOT EXISTS <schema_name> [ AUTHORIZATION <role_specification> ]

CREATE SCHEMA IF NOT EXISTS AUTHORIZATION <role_specification>

-- where <role_specification> can be:

    <user_name>
  | CURRENT_USER
  | SESSION_USER
```

## 描述 {#description}

`CREATE SCHEMA` 在当前数据库中创建新模式。模式名必须不同于当前数据库中任何现有模式的名称。

模式本质上是命名空间：它包含命名对象（表、数据类型、函数和操作符），这些对象的名称可以与其他模式中的对象重复。访问命名对象时，可以使用模式名作为前缀来限定对象名称，或者设置包含所需模式的搜索路径。`CREATE` 命令指定未限定的对象名称时，会在当前模式中创建对象（即搜索路径中的第一个模式，可以通过 `current_schema()` 函数确定）。

`CREATE SCHEMA` 还可以包含在新模式中创建对象的子命令。这些子命令基本上等同于创建模式后单独发出的命令，但如果使用了 `AUTHORIZATION` 子句，则创建的所有对象都归该角色所有。

## 参数 {#parameters}

**`schema_name`**

要创建的模式名称。如果省略，使用 user_name 作为模式名称。名称不能以 `pg_` 开头，因为这类名称保留给系统目录模式。

**`user_name`**

新模式所有者的角色名称。如果省略，默认为运行命令的用户。要创建归其他角色所有的模式，必须是该角色的直接或间接成员，或者是超级用户。

**`schema_element`**

定义要在模式中创建的对象的 SQL 语句。目前，`CREATE SCHEMA` 中只接受 `CREATE TABLE`、`CREATE VIEW`、`CREATE INDEX`、`CREATE SEQUENCE`、`CREATE TRIGGER` 和 `GRANT` 作为子句。其他类型的对象可在创建模式后通过单独命令创建。

> **注意** Apache Cloudberry 不支持触发器。

**`IF NOT EXISTS`**

如果同名模式已经存在，则不执行任何操作（只发出一条提示）。使用此选项时不能包含 schema_element 子命令。

## 注意事项 {#notes}

创建模式时，调用用户必须拥有当前数据库的 `CREATE` 权限，或者是超级用户。

## 示例 {#examples}

创建模式：

```sql
CREATE SCHEMA myschema;
```

为角色 `joe` 创建模式，模式也命名为 `joe`：

```sql
CREATE SCHEMA AUTHORIZATION joe;
```

创建名为 `test`、归用户 `joe` 所有的模式，除非名为 `test` 的模式已经存在。（现有模式是否归 `joe` 所有无关紧要。）

```sql
CREATE SCHEMA IF NOT EXISTS test AUTHORIZATION joe;
```

创建模式，并在其中创建表和视图：

```sql
CREATE SCHEMA hollywood
    CREATE TABLE films (title text, release date, awards text[])
    CREATE VIEW winners AS
        SELECT title, release FROM films WHERE awards IS NOT NULL;
```

注意，各个子命令不以分号结尾。

下面的等效写法可以获得相同结果：

```sql
CREATE SCHEMA hollywood;
CREATE TABLE hollywood.films (title text, release date, awards text[]);
CREATE VIEW hollywood.winners AS
    SELECT title, release FROM hollywood.films WHERE awards IS NOT NULL;
```

## 兼容性 {#compatibility}

SQL 标准允许在 `CREATE SCHEMA` 中使用 `DEFAULT CHARACTER SET` 子句，并且允许的子命令类型比 Apache Cloudberry 当前接受的更多。

SQL 标准规定，`CREATE SCHEMA` 中的子命令可以按任意顺序出现。当前 Apache Cloudberry 实现不能处理子命令中所有的前向引用情况；有时可能需要调整子命令顺序，以避免前向引用。

按照 SQL 标准，模式所有者始终拥有模式中的所有对象。Apache Cloudberry 允许模式包含其他用户拥有的对象。只有模式所有者将该模式上的 `CREATE` 权限授予其他人，或超级用户选择在其中创建对象时，才会出现这种情况。

`IF NOT EXISTS` 选项是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER SCHEMA](/cloudberry/reference/sql-stmts/alter-schema/), [DROP SCHEMA](/cloudberry/reference/sql-stmts/drop-schema/)
