---
title: "ALTER TYPE"
description: "更改数据类型的定义。"
weight: 390
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-type.md"
---

## 概要 {#synopsis}

```sql
ALTER TYPE <name> <action> [, ... ]
ALTER TYPE <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
ALTER TYPE <name> RENAME ATTRIBUTE <attribute_name> TO <new_attribute_name> [ CASCADE | RESTRICT ]
ALTER TYPE <name> RENAME TO <new_name>
ALTER TYPE <name> SET SCHEMA <new_schema>
ALTER TYPE <name> ADD VALUE [ IF NOT EXISTS ] <new_enum_value> [ { BEFORE | AFTER } <neighbor_enum_value> ]
ALTER TYPE <name> RENAME VALUE <existing_enum_value> to <new_enum_value>
ALTER TYPE <name> SET DEFAULT ENCODING ( <storage_directive> )

-- where <action> is one of:
  
  ADD ATTRIBUTE <attribute_name> <data_type> [ COLLATE <collation> ] [ CASCADE | RESTRICT ]
  DROP ATTRIBUTE [ IF EXISTS ] <attribute_name> [ CASCADE | RESTRICT ]
  ALTER ATTRIBUTE <attribute_name> [ SET DATA ] TYPE <data_type> [ COLLATE <collation> ] [ CASCADE | RESTRICT ]

-- where <storage_directive> is:

   COMPRESSTYPE={ZLIB | ZSTD | RLE_TYPE | NONE}
   COMPRESSLEVEL={0-19}
   BLOCKSIZE={8192-2097152}
```

## 描述 {#description}

`ALTER TYPE` 用于更改现有类型的定义。它有若干子形式：

**`ADD ATTRIBUTE`**

使用与 [CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/) 相同的语法，为复合类型添加一个新属性。

**`DROP ATTRIBUTE [ IF EXISTS ]`**

从复合类型中删除一个属性。如果指定了 `IF EXISTS` 且该属性不存在，则不会抛出错误。在这种情况下，Apache Cloudberry 会发出一条通知。

**`SET DATA TYPE`**

更改复合类型某个属性的类型。

**`OWNER`**

更改类型的所有者。

**`RENAME`**

更改类型的名称，或更改复合类型某个单独属性的名称。

**`SET SCHEMA`**

将类型移动到另一个模式。

**`ADD VALUE [ IF NOT EXISTS ] [ BEFORE | AFTER ]`**

向枚举类型添加一个新值。可以指定新值在枚举顺序中位于某个现有值的 `BEFORE`（之前）或 `AFTER`（之后）。否则，新项将添加到值列表的末尾。

如果指定了 `IF NOT EXISTS`，则当类型已包含该新值时不算错误；Apache Cloudberry 会发出一条通知，但不执行其他操作。否则，如果新值已经存在，就会发生错误。

**`RENAME VALUE`**

重命名枚举类型的一个值。该值在枚举顺序中的位置不受影响。如果指定的值不存在，或新名称已经存在，就会发生错误。

`ADD ATTRIBUTE`、`DROP ATTRIBUTE` 和 `ALTER ATTRIBUTE` 动作可以合并为一个包含多项更改的列表并行应用。例如，可以在单个命令中添加多个属性和/或更改多个属性的类型。

可以更改类型的名称、所有者和模式。也可以为标量类型添加或更新存储选项。

> **注意** Apache Cloudberry 不支持为行类型或复合类型添加存储选项。

必须拥有该类型才能使用 `ALTER TYPE`。要更改类型的模式，还必须对新模式具有 `CREATE` 权限。要更改所有者，还必须是新所有者角色的直接或间接成员，并且该角色必须对该类型所在的模式具有 `CREATE` 权限。（这些限制确保了更改所有者不会做出通过删除并重新创建类型无法做到的事情。不过，超级用户可以更改任何类型的所有权。）要添加属性或更改属性类型，还必须对该数据类型具有 `USAGE` 权限。

## 参数 {#parameters}

**`name`**

要更改的现有类型的名称（可以带模式限定）。

**`new_name`**

类型的新名称。

**`new_owner`**

类型的新所有者的用户名。

**`new_schema`**

类型的新模式。

**`attribute_name`**

要添加、更改或删除的属性的名称。

**`new_attribute_name`**

要重命名的属性的新名称。

**`data_type`**

要添加的属性的数据类型，或要更改的属性的新类型。

**`new_enum_value`**

要添加到枚举类型值列表中的新值。与所有枚举字面量一样，它必须加引号。

**`neighbor_enum_value`**

现有的枚举值，新值应紧邻其之前或之后添加到枚举类型的排序顺序中。与所有枚举字面量一样，它必须加引号。

**`existing_enum_value`**

要重命名的现有枚举值。与所有枚举字面量一样，它必须加引号。

**`CASCADE`**

自动将该操作传播到被更改类型的类型化表及其后代表。

**`RESTRICT`**

如果被更改的类型是某个类型化表的类型，则拒绝该操作。这是默认行为。

**`storage_directive`**

标识当该类型用于表的列定义时的默认存储选项。选项包括 `COMPRESSTYPE`、`COMPRESSLEVEL` 和 `BLOCKSIZE`。

**COMPRESSTYPE** — 设置为 `ZLIB`（默认值）、`ZSTD` 或 `RLE_TYPE`，以指定所使用的压缩类型。

**COMPRESSLEVEL** — 对于 Zstd 压缩，设置为 1（压缩最快）到 19（压缩率最高）之间的整数值。对于 zlib 压缩，有效范围是 1 到 9。对于 `RLE_TYPE`，压缩级别可以设置为 1（压缩最快）到 4（压缩率最高）之间的整数值。默认压缩级别为 1。

**BLOCKSIZE** — 设置列中每个块的大小，单位为字节。`BLOCKSIZE` 必须介于 8192 和 2097152 字节之间，并且是 8192 的倍数。默认块大小为 32768。

> **注意** 在表级或列级定义的 storage_directives 会覆盖为类型定义的默认存储选项。

## 注意事项 {#notes}

如果在事务块内执行 `ALTER TYPE ... ADD VALUE`（即向枚举类型添加新值的形式），则在事务提交之后才能使用该新值。

涉及新添加枚举值的比较有时会比仅涉及枚举类型原始成员的比较更慢。这通常只会在使用 `BEFORE` 或 `AFTER` 将新值的排序位置设置在列表末尾以外的位置时发生。不过，有时即使新值添加在末尾也会发生这种情况（当自枚举类型最初创建以来 OID 计数器“回绕”时就会如此）。这种减速通常无关紧要；但如果确有影响，可以通过删除并重新创建该枚举类型，或者通过转储并重新加载数据库来恢复最佳性能。

## 示例 {#examples}

重命名名为 `electronic_mail` 的数据类型：

```sql
ALTER TYPE electronic_mail RENAME TO email;
```

将用户定义类型 `email` 的所有者更改为 `joe`：

```sql
ALTER TYPE email OWNER TO joe;
```

将用户定义类型 `email` 的模式更改为 `customers`：

```sql
ALTER TYPE email SET SCHEMA customers;
```

设置或更改名为 `int33` 的用户定义类型的压缩类型和压缩级别：

```sql
ALTER TYPE int33 SET DEFAULT ENCODING (compresstype=zlib, compresslevel=7);
```

为类型添加一个新属性：

```sql
ALTER TYPE compfoo ADD ATTRIBUTE f3 int;
```

在特定排序位置向枚举类型添加一个新值：

```sql
ALTER TYPE colors ADD VALUE 'orange' AFTER 'red';
```

重命名枚举值：

```sql
ALTER TYPE colors RENAME VALUE 'purple' TO 'mauve';
```

## 兼容性 {#compatibility}

添加和删除属性的变体属于 SQL 标准；其他变体是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[CREATE TYPE](/cloudberry/reference/sql-stmts/create-type/)、[DROP TYPE](/cloudberry/reference/sql-stmts/drop-type/)
