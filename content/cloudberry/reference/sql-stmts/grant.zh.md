---
title: "GRANT"
description: "定义访问权限。"
weight: 1480
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/grant.md"
---

## 语法概要 {#synopsis}

```sql
GRANT { {SELECT | INSERT | UPDATE | DELETE | REFERENCES | 
TRIGGER | TRUNCATE } [, ...] | ALL [PRIVILEGES] }
    ON { [TABLE] [[[ONLY] <table_name> [, ...]] [, ...]]
         | ALL TABLES IN SCHEMA <schema_name> [, ...] }
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { { SELECT | INSERT | UPDATE | REFERENCES } ( <column_name> [, ...] )
    [, ...] | ALL [ PRIVILEGES ] ( <column_name> [, ...] ) }
    ON [TABLE] [[[ONLY] <table_name> [, ...]] [, ...]]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { {USAGE | SELECT | UPDATE} [, ...] | ALL [PRIVILEGES] }
    ON { SEQUENCE <sequence_name> [, ...]
         | ALL SEQUENCES IN SCHEMA <schema_name> [, ...] }
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { {CREATE | CONNECT | TEMPORARY | TEMP} [, ...] | ALL 
[PRIVILEGES] }
    ON DATABASE <database_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON DOMAIN <domain_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN DATA WRAPPER <fdw_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON FOREIGN SERVER <server_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { EXECUTE | ALL [PRIVILEGES] }
    ON { { FUNCTION | PROCEDURE | ROUTINE } <routine_name> [ ( [ [ <argmode> ] [ <argname> ] <argtype> [, ...] ] ) ] [, ...]
        | ALL { FUNCTIONS | PROCEDURES | ROUTINES }  IN SCHEMA <schema_name> [, ...] }
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [PRIVILEGES] }
    ON LANGUAGE <lang_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { { CREATE | USAGE } [, ...] | ALL [PRIVILEGES] }
    ON SCHEMA <schema_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT { CREATE | ALL [PRIVILEGES] }
    ON TABLESPACE <tablespace_name> [, ...]
    TO <role_specification> [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPE <type_name> [, ...]
    TO <role_specification> [, ...] [ WITH GRANT OPTION ]

GRANT <role_name> [, ...] TO <role_specification> [, ...]
    [ WITH ADMIN OPTION ]
    [ GRANTED BY <role_specification> ]

GRANT { SELECT | INSERT | ALL [PRIVILEGES] } 
    ON PROTOCOL <protocolname>
    TO <username>

-- where <role_specification> can be:

    [ GROUP ] <role_name>
  | PUBLIC
  | CURRENT_USER
  | SESSION_USER
```

## 说明 {#description}

`GRANT` 命令有两种基本形式：一种授予数据库对象（表、列、视图、外表、序列、数据库、外部数据包装器、外部服务器、函数、过程语言、模式或表空间）的权限，另一种授予角色成员资格。这两种形式在很多方面相似，但差异足够大，因此分别说明。

**数据库对象的 GRANT**

此形式的 `GRANT` 命令将数据库对象的特定权限授予一个或多个角色。这些权限会追加到已有的授权之上。

关键字 `PUBLIC` 表示将权限授予所有角色，包括今后可能创建的角色。可以将 `PUBLIC` 视为一个隐式定义的组级角色，它始终包含所有角色。任何特定角色拥有的权限，都是直接授予它的权限、授予它当前所属角色的权限，以及授予 `PUBLIC` 的权限之和。

如果指定 `WITH GRANT OPTION`，权限接收者可以继续将该权限授予其他角色；没有授权选项则不能这样做。不能将授权选项授予 `PUBLIC`。

无须向对象所有者（通常是创建对象的角色）授予权限，因为所有者默认拥有全部权限。（但出于安全考虑，所有者可以选择撤销自己的一些权限。）

删除对象或以任何方式修改其定义的权利，不被视为可以授予的权限；它是所有者固有的权利，不能授予或撤销。（不过，通过授予或撤销拥有该对象的角色的成员资格，可以达到类似效果；见下文。）所有者还隐含拥有该对象的所有授权选项。

可用权限包括：

- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `TRUNCATE`
- `REFERENCES`
- `TRIGGER`
- `CREATE`
- `CONNECT`
- `TEMPORARY`, `TEMP`
- `EXECUTE`
- `USAGE`
- `ALL PRIVILEGES`

`FUNCTION` 语法适用于普通函数、聚合函数和窗口函数，但不适用于过程；过程应使用 `PROCEDURE`。也可以使用 `ROUTINE` 来指代函数、聚合函数、窗口函数或过程，而不区分具体类型。

还可以对一个或多个模式中同一类型的所有对象授予权限。目前仅表、序列、函数和过程支持此功能。与针对具体对象的 `GRANT` 命令一样，`ALL TABLES` 也影响视图和外表。与针对具体对象的 `GRANT` 命令一样，`ALL FUNCTIONS` 也影响聚合函数和窗口函数，但不影响过程。使用 `ALL ROUTINES` 可以包含过程。

**角色的 GRANT**

此形式的 `GRANT` 命令将某角色的成员资格授予一个或多个其他角色。角色成员资格的重要作用在于，将授予该角色的权限传递给它的每个成员。

如果指定 `WITH ADMIN OPTION`，成员可以继续将该角色的成员资格授予其他角色，也可以撤销成员资格。没有管理选项时，普通用户不能这样做。角色不被视为对自身持有 `WITH ADMIN OPTION`，但在会话用户就是该角色的数据库会话中，它可以授予或撤销自身的成员资格。数据库超级用户可以向任何角色授予或撤销任何角色的成员资格。具有 `CREATEROLE` 权限的角色可以授予或撤销任何非超级用户角色的成员资格。

如果指定 `GRANTED BY`，授权会被记录为由指定角色执行。除非指定的角色就是执行命令的角色，否则只有数据库超级用户可以使用此选项。

与对象权限不同，不能将角色成员资格授予 `PUBLIC`。还应注意，此命令形式不允许在 role_specification 中使用无实际作用的关键字 `GROUP`。

**分区表的 GRANT**

默认情况下，为分区表授予权限时，Apache Cloudberry 会将操作递归应用到其子表。要让 Apache Cloudberry 只对分区表执行 `GRANT`，请指定 `ONLY <table_name>` 子句。

**协议的 GRANT**

也可以使用 `GRANT` 命令指定哪些用户可以访问受信任协议。（如果协议不受信任，就不能授权其他用户使用它读写数据。）

- 允许用户使用受信任协议创建可读外部表：

    ```sql
    GRANT SELECT ON PROTOCOL <protocolname> TO <username>
    ```

- 允许用户使用受信任协议创建可写外部表：

    ```sql
    GRANT INSERT ON PROTOCOL <protocolname> TO <username>
    ```

- 允许用户使用受信任协议创建可读和可写外部表：

    ```sql
    GRANT ALL ON PROTOCOL <protocolname> TO <username>
    ```

也可以用此命令授予用户创建和使用 `s3`、`pxf` 外部表的权限。不过，`http`、`https`、`gpfdist` 和 `gpfdists` 类型的外部表由 Apache Cloudberry 内部实现，并非自定义协议。对于这些类型，应使用 `CREATE ROLE` 或 `ALTER ROLE` 命令为每个用户设置 `CREATEEXTTABLE` 或 `NOCREATEEXTTABLE` 属性。语法和示例请参阅 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/)。

## 参数 {#parameters}

**`SELECT`**

允许对指定表、视图或序列中的任何列或列出的特定列执行 `SELECT`，也允许使用 `COPY TO`。在 `UPDATE` 或 `DELETE` 中引用已有列值时也需要此权限。

**`INSERT`**

允许通过 `INSERT` 向指定表插入新行。如果列出了特定列，`INSERT` 命令只能对这些列赋值（其他列使用默认值）。也允许使用 `COPY FROM`。

**`UPDATE`**

允许对指定表中的任何列或列出的特定列执行 `UPDATE`。`SELECT ... FOR UPDATE` 和 `SELECT ... FOR SHARE` 也要求至少对一列具有此权限（以及 `SELECT` 权限）。对于序列，此权限允许使用 `nextval()` 和 `setval()` 函数。

**`DELETE`**

允许通过 `DELETE` 删除指定表中的行。

**`REFERENCES`**

虽然 Apache Cloudberry 目前不支持外键约束，但仍接受此关键字。创建外键约束需要同时对引用列和被引用列具有此权限。可以为表的所有列授予此权限，也可以只为特定列授予。

**`TRIGGER`**

允许在指定表上创建触发器。

> **注意** Apache Cloudberry 不支持触发器。

**`TRUNCATE`**

允许通过 `TRUNCATE` 清空指定表的所有行。

**`CREATE`**

对于数据库，允许在数据库中创建新模式。

对于模式，允许在模式中创建新对象。要重命名已有对象，必须拥有该对象，并对其所在模式具有此权限。

对于表空间，允许在其中创建表和索引，以及创建以此表空间为默认表空间的数据库。（注意，撤销此权限不会改变已有对象的存放位置。）

**`CONNECT`**

允许用户连接指定数据库。在建立连接时检查此权限（同时还会检查 `pg_hba.conf` 规定的各项限制）。

**`TEMPORARY`**<br />
**`TEMP`**

允许在使用该数据库时创建临时表。

**`EXECUTE`**

允许使用指定函数，以及基于该函数实现的任何操作符。这是唯一适用于函数的权限类型。（此语法也适用于聚合函数。）

**`USAGE`**

对于过程语言，允许使用指定语言创建以该语言编写的函数。这是唯一适用于过程语言的权限类型。

对于模式，允许访问指定模式中的对象（前提是也满足这些对象自身的权限要求）。这实际上允许被授权者在模式中查找对象。

对于序列，此权限允许使用 `currval()` 和 `nextval()` 函数。

对于类型和域，此权限允许在创建表、函数及其他模式对象时使用该类型或域。（注意，它不控制类型的一般“使用”，例如在查询中出现该类型的值。它只阻止创建依赖此类型的对象。该权限的主要用途是控制哪些用户可以创建对某类型的依赖，因为这些依赖可能使所有者日后无法更改该类型。）

对于外部数据包装器，此权限允许被授权者使用该外部数据包装器创建新服务器。

对于服务器，此权限允许被授权者使用该服务器创建外表，以及创建、修改或删除与该服务器关联的自身用户映射。

**`ALL PRIVILEGES`**

一次授予所有可用权限。在 Apache Cloudberry 中，`PRIVILEGES` 关键字是可选的，不过严格遵循 SQL 时必须提供。

**`PUBLIC`**

一个特殊的组级角色，表示将权限授予所有角色，包括今后可能创建的角色。

**`WITH GRANT OPTION`**

权限接收者可以继续将该权限授予其他角色。

**`WITH ADMIN OPTION`**

角色成员可以继续将该角色的成员资格授予其他角色。

## 注意事项 {#notes}

使用 [REVOKE](/cloudberry/reference/sql-stmts/revoke/) 命令撤销访问权限。

Apache Cloudberry 将用户和组统一为一种称为角色的实体。因此，无须使用 `GROUP` 关键字来区分被授权者是用户还是组。命令中仍允许使用 `GROUP`，但它没有实际作用。

只要用户对特定列或整张表具有相应权限，就可以对该列执行 `SELECT`、`INSERT` 等操作。先在表级授予权限，再对某一列撤销权限，并不能达到预想的效果：表级授权不受列级操作影响。

非所有者尝试对对象执行 `GRANT` 授权时，如果用户对该对象没有任何权限，命令会直接失败。只要具有某些权限，命令就会继续，但只授予该用户具有授权选项的那些权限。对于 `GRANT ALL PRIVILEGES` 形式，如果用户没有任何授权选项，会发出警告；对于其他形式，如果缺少命令明确列出的任何权限的授权选项，就会发出警告。（原则上这些规则也适用于对象所有者，但由于所有者始终被视为持有全部授权选项，这些情况不会发生。）

数据库超级用户可以访问所有对象，不受对象权限设置的限制。这类似于 Unix 系统中的 `root` 权限。与 `root` 一样，除非确有必要，否则不应以超级用户身份操作。视图对象是一个例外：访问视图引用的表时，使用视图所有者的权限，而非当前用户的权限（即使当前用户是超级用户）。

如果超级用户执行 `GRANT` 或 `REVOKE` 命令，效果与受影响对象的所有者执行该命令相同。具体而言，通过此类命令授予的权限会显示为由对象所有者授予。（对于角色成员资格，则显示为由被加入的角色自身授予。）

`GRANT` 和 `REVOKE` 也可以由不是受影响对象所有者的角色执行，只要它是拥有该对象的角色的成员，或是对该对象持有 `WITH GRANT OPTION` 权限的角色的成员。此时，授权会被记录为由实际拥有对象或持有 `WITH GRANT OPTION` 权限的角色执行。例如，表 `t1` 由角色 `g1` 拥有，而角色 `u1` 是其成员，则 `u1` 可以将 `t1` 的权限授予 `u2`，但这些权限会显示为由 `g1` 直接授予。角色 `g1` 的其他成员之后也可以撤销这些权限。

如果执行 `GRANT` 的角色通过多条角色成员关系路径间接持有所需权限，系统不保证将哪个所属角色记录为授权者。此时，最佳做法是先用 `SET ROLE` 切换到希望用来执行 `GRANT` 的具体角色。

授予表的权限不会自动扩展到该表使用的序列，包括与 `SERIAL` 列关联的序列。必须单独设置序列权限。

不能使用 `GRANT` 命令设置 `file`、`gpfdist` 或 `gpfdists` 协议的权限。这些协议由 Apache Cloudberry 内部实现。应使用 [CREATE ROLE](/cloudberry/reference/sql-stmts/create-role/) 或 [ALTER ROLE](/cloudberry/reference/sql-stmts/alter-role/) 命令为角色设置 `CREATEEXTTABLE` 属性。

使用 `psql` 的 `\dp` 元命令可以查看表和列的现有权限。其他 `\d` 元命令可用于显示非表对象的权限。

## 示例 {#examples}

向所有角色授予表 `mytable` 的插入权限：

```sql
GRANT INSERT ON mytable TO PUBLIC;
```

将视图 `kinds` 的所有可用权限授予用户 `manuel`：

```sql
GRANT ALL PRIVILEGES ON kinds TO manuel;
```

注意，上述命令由超级用户或 `kinds` 的所有者运行时，确实会授予所有权限；由其他角色运行时，只会授予授权角色具有授权选项的权限。

将角色 `admins` 的成员资格授予用户 `joe`：

```sql
GRANT admins TO joe;
```

## 兼容性 {#compatibility}

根据 SQL 标准，`ALL PRIVILEGES` 中的 `PRIVILEGES` 关键字是必需的，但在 Apache Cloudberry 中是可选的。SQL 标准不支持在一条命令中设置多个对象的权限。

Apache Cloudberry 允许对象所有者撤销自身的普通权限。例如，表所有者可以撤销自己的 `INSERT`、`UPDATE`、`DELETE` 和 `TRUNCATE` 权限，使该表对自己只读。SQL 标准不允许这样做。Apache Cloudberry 将所有者的权限视为由所有者授予自己，因此也允许其撤销。在 SQL 标准中，所有者的权限由一个假定的*系统*实体授予；所有者并非*系统*，因此无法撤销这些权利。

SQL 标准允许在所有形式的 `GRANT` 中使用 `GRANTED BY` 选项。Apache Cloudberry 只在授予角色成员资格时支持该选项，而且只有超级用户才能将它用于指定自身以外的角色。

SQL 标准还为其他类型的对象规定了 `USAGE` 权限：字符集、排序规则和转换。

在 SQL 标准中，序列只有 `USAGE` 权限，用于控制 `NEXT VALUE FOR` 表达式的使用，该表达式等价于 Apache Cloudberry 中的 `nextval()` 函数。序列权限 `SELECT` 和 `UPDATE` 是 Apache Cloudberry 的扩展。将序列的 `USAGE` 权限应用于 `currval()` 函数也是 Apache Cloudberry 的扩展（函数本身同样是扩展）。

数据库、表空间、模式和语言上的权限是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[ALTER DEFAULT PRIVILEGES](/cloudberry/reference/sql-stmts/alter-default-privileges/), [REVOKE](/cloudberry/reference/sql-stmts/revoke/)
