---
title: "ALTER DOMAIN"
description: "更改一个域的定义。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/alter-domain.md"
---

## 概要 {#synopsis}

```sql
ALTER DOMAIN <name> { SET DEFAULT <expression> | DROP DEFAULT }

ALTER DOMAIN <name> { SET | DROP } NOT NULL

ALTER DOMAIN <name> ADD <domain_constraint> [ NOT VALID ]

ALTER DOMAIN <name> DROP CONSTRAINT [ IF EXISTS ] <constraint_name> [RESTRICT | CASCADE]

ALTER DOMAIN <name> RENAME CONSTRAINT <constraint_name> TO <new_constraint_name>

ALTER DOMAIN <name> VALIDATE CONSTRAINT <constraint_name>
  
ALTER DOMAIN <name> OWNER TO { <new_owner> | CURRENT_USER | SESSION_USER }
  
ALTER DOMAIN <name> RENAME TO <new_name>

ALTER DOMAIN <name> SET SCHEMA <new_schema>
```

## 描述 {#description}

`ALTER DOMAIN` 更改一个现有域的定义。它有若干子形式：

- **SET/DROP DEFAULT** — 这些形式设置或移除域的默认值。请注意，默认值只应用于此后的 `INSERT` 命令，不会影响表中已经使用该域的行。
- **SET/DROP NOT NULL** — 这些形式更改域被标记为允许 NULL 值还是拒绝 NULL 值。只有当使用该域的列不包含空值时，才可以执行 `SET NOT NULL`。
- **ADD domain_constraint [ NOT VALID ]** — 此形式使用与 [CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/) 相同的语法为域添加一个新约束。向域添加新约束时，会针对新添加的约束检查所有使用该域的列。可以通过 `NOT VALID` 选项添加新约束来跳过这些检查；之后可以使用 `ALTER DOMAIN ... VALIDATE CONSTRAINT` 使该约束生效。新插入或更新的行始终会针对所有约束进行检查，即使是标记为 `NOT VALID` 的约束。`NOT VALID` 只被 `CHECK` 约束接受。
- **DROP CONSTRAINT [ IF EXISTS ]** — 此形式删除域上的约束。如果指定了 `IF EXISTS` 且该约束不存在，则不会抛出错误，而是发出一个提示。
- **RENAME CONSTRAINT** — 此形式更改域上某个约束的名称。
- **VALIDATE CONSTRAINT** — 此形式验证先前以 `NOT VALID` 添加的约束，即验证该域在表列中的所有值都满足指定的约束。
- **OWNER** — 此形式把域的所有者更改为指定的用户。
- **RENAME** — 此形式更改域的名称。
- **SET SCHEMA** — 此形式更改域所在的模式。与该域相关联的任何约束也会一并移入新模式。

要使用 `ALTER DOMAIN`，你必须拥有该域。要更改域的模式，你还必须在新模式上具有 `CREATE` 权限。要更改所有者，你还必须是新所有者角色的直接或间接成员，并且该角色必须在该域所在的模式上具有 `CREATE` 权限。（这些限制确保更改所有者不会做到任何通过删除并重新创建该域无法做到的事情。不过，超级用户无论如何都可以更改任何域的所有权。）

## 参数 {#parameters}

**`name`**

要更改的现有域的名称（可以是模式限定的）。

**`domain_constraint`**

域的新域约束。

**`constraint_name`**

要删除或重命名的现有约束的名称。

**`NOT VALID`**

不验证现有列数据是否满足约束。

**`CASCADE`**

自动删除依赖于该约束的对象，进而删除依赖于这些对象的所有对象。

**`RESTRICT`**

如果存在任何依赖对象，则拒绝删除该约束。这是默认行为。

**`new_name`**

域的新名称。

**`new_constraint_name`**

约束的新名称。

**`new_owner`**

域的新所有者的用户名。

**`new_schema`**

域的新模式。

## 注解 {#notes}

虽然 `ALTER DOMAIN ADD CONSTRAINT` 会尝试验证现有存储的数据是否满足新约束，但这种检查并非万无一失，因为该命令无法“看到”新插入或更新但尚未提交的表行。如果存在并发操作可能插入不良数据的风险，正确的做法是使用 `NOT VALID` 选项添加该约束，提交该命令，等待在该次提交之前启动的所有事务结束，然后发出 `ALTER DOMAIN VALIDATE CONSTRAINT` 来查找违反该约束的数据。这种方法是可靠的，因为约束一旦提交，就保证所有新事务都会针对域类型的新值强制执行它。

目前，如果数据库中任何表的某个容器类型列（复合类型、数组或范围类型列）内使用了所指定的域或任何派生域，则 `ALTER DOMAIN ADD CONSTRAINT`、`ALTER DOMAIN VALIDATE CONSTRAINT` 和 `ALTER DOMAIN SET NOT NULL` 都会失败。它们最终应当得到改进，以便能够对这类嵌套值验证新约束。

## 示例 {#examples}

为域添加一个 `NOT NULL` 约束：

```sql
ALTER DOMAIN zipcode SET NOT NULL;
```

从域中移除一个 `NOT NULL` 约束：

```sql
ALTER DOMAIN zipcode DROP NOT NULL;
```

为域添加一个检查约束：

```sql
ALTER DOMAIN zipcode ADD CONSTRAINT zipchk CHECK (char_length(VALUE) = 5);
```

从域中移除一个检查约束：

```sql
ALTER DOMAIN zipcode DROP CONSTRAINT zipchk;
```

重命名域上的一个检查约束：

```sql
ALTER DOMAIN zipcode RENAME CONSTRAINT zipchk TO zip_check;
```

将域移入另一个模式：

```sql
ALTER DOMAIN zipcode SET SCHEMA customers;
```

## 兼容性 {#compatibility}

`ALTER DOMAIN` 符合 SQL 标准，但 `OWNER`、`RENAME`、`SET SCHEMA` 和 `VALIDATE CONSTRAINT` 这几种变体除外，它们是 Apache Cloudberry 的扩展。`ADD CONSTRAINT` 变体的 `NOT VALID` 子句同样是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[CREATE DOMAIN](/cloudberry/reference/sql-stmts/create-domain/)、[DROP DOMAIN](/cloudberry/reference/sql-stmts/drop-domain/)
