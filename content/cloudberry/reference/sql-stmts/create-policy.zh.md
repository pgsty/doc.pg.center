---
title: "CREATE POLICY"
description: "为表定义新的行级安全策略。"
weight: 710
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-policy.md"
---

## 语法概要 {#synopsis}

```sql
CREATE POLICY <name> ON <table_name>
    [ AS { PERMISSIVE | RESTRICTIVE } ]
    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
    [ TO { <role_name> | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( <using_expression> ) ]
    [ WITH CHECK ( <check_expression> ) ]
```

## 说明 {#description}

`CREATE POLICY` 命令为表定义新的行级安全策略。必须先在表上启用行级安全（使用 `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`），Apache Cloudberry 才会应用所创建的策略。

策略授予选择、插入、更新或删除符合相关策略表达式的行的权限。现有表行根据 `USING` 中指定的表达式检查；通过 `INSERT` 或 `UPDATE` 创建的新行根据 `WITH CHECK` 中指定的表达式检查。当 `USING` 表达式对某行返回 true 时，用户可以看到该行；返回 false 或 null 时，用户看不到该行。当 `WITH CHECK` 表达式对某行返回 true 时，该行可以插入或更新；返回 false 或 null 时会发生错误。

对于 `INSERT` 和 `UPDATE` 语句，`WITH CHECK` 表达式会在实际数据修改前、其他约束前强制执行。

策略名称按表确定。因此，同一个策略名可以用于多个不同的表，并为每个表设置适合该表的定义。

策略可以应用于特定命令或特定角色。新创建策略的默认行为是应用于所有命令和角色，除非另有指定。一个命令可以适用多个策略；更多详情见下文。[按命令应用的策略](#per-command-policies)表总结了不同类型的策略如何应用于特定命令。

对于同时具有 `USING` 和 `WITH CHECK` 表达式的策略（`ALL` 和 `UPDATE`），如果未定义 `WITH CHECK` 表达式，则同时使用 `USING` 表达式确定哪些行可见（普通的 `USING` 情况）以及哪些新行可以添加（`WITH CHECK` 情况）。

如果表启用了行级安全，但不存在适用策略，则假定采用“默认拒绝”策略，因此没有任何行可见或可更新。

## 参数 {#parameters}

**`name`**

要创建的策略名称。该名称必须与为该表定义的其他策略名称不同。

**`table_name`**

策略适用的表名称（可以用模式名限定）。

**`PERMISSIVE`**

指定将策略创建为宽松策略。适用于给定查询的所有宽松策略会使用布尔 `OR` 操作符组合。创建宽松策略可以让管理员扩大可访问记录的集合。默认策略是宽松策略。

**`RESTRICTIVE`**

指定将策略创建为限制性策略。适用于给定查询的所有限制性策略会使用布尔 `AND` 操作符组合。创建限制性策略可以让管理员缩小可访问记录的集合，因为每条记录都必须通过所有限制性策略。

必须至少定义一个宽松策略来授予记录访问权限，之后限制性策略才有意义地用于缩小访问范围。如果只有限制性策略，则没有任何记录可访问。当宽松策略和限制性策略混合存在时，记录必须至少通过一个宽松策略以及所有限制性策略，才可访问。

**`command`**

策略适用的命令。有效选项为 `ALL`、`SELECT`、`INSERT`、`UPDATE` 和 `DELETE`。默认值为 `ALL`。这些选项的具体应用方式见下文。

**`role_name`**

策略适用的角色。默认值为 `PUBLIC`，表示策略应用于所有角色。

**`using_expression`**

任意 SQL 条件表达式（返回 `boolean`）。条件表达式不能包含聚合函数或窗口函数。启用行级安全后，该表达式会添加到引用该表的查询中。表达式返回 true 的行可见；返回 false 或 null 的行在 `SELECT` 中对用户不可见，在 `UPDATE` 或 `DELETE` 中也不可修改。这些行会被静默过滤，不会报告错误。

**`check_expression`**

任意 SQL 条件表达式（返回 `boolean`）。条件表达式不能包含聚合函数或窗口函数。启用行级安全后，在针对该表的 `INSERT` 和 `UPDATE` 查询中使用此表达式。只有表达式计算为 true 的行才允许写入。如果插入的任何记录或更新产生的任何记录的表达式计算为 false 或 null，就会抛出错误。请注意，check_expression 针对行的拟议新内容计算，而不是针对原有内容计算。

## 按命令应用的策略 {#per-command-policies}

**`ALL`**

策略使用 `ALL` 表示它适用于所有命令，与命令类型无关。如果同时存在 `ALL` 策略和更具体的策略，则会同时应用 `ALL` 策略和更具体的策略（或多个策略）。此外，`ALL` 策略同时应用于查询的选择侧和修改侧；如果只定义了 `USING` 表达式，则两侧都使用 `USING` 表达式。

例如，如果发出 `UPDATE`，则 `ALL` 策略既适用于 `UPDATE` 能够选择哪些行进行更新（应用 `USING` 表达式），也适用于更新后的行，检查它们是否允许重新添加到表中（如果已定义则应用 `WITH CHECK` 表达式，否则应用 `USING` 表达式）。如果 `INSERT` 或 `UPDATE` 命令尝试向表中添加未通过 `ALL` 策略 `WITH CHECK` 表达式的行，整个命令都会中止。

**`SELECT`**

策略使用 `SELECT` 表示它适用于 `SELECT` 查询，以及对策略所在关系要求 `SELECT` 权限的任何场景。结果是，`SELECT` 查询只返回通过 `SELECT` 策略的关系记录；需要 `SELECT` 权限的查询（例如 `UPDATE`）也只能看到 `SELECT` 策略允许的记录。`SELECT` 策略不能有 `WITH CHECK` 表达式，因为它只适用于从关系中检索记录的场景。

**`INSERT`**

策略使用 `INSERT` 表示它适用于 `INSERT` 命令。插入但未通过该策略的行会导致策略违反错误，整个 `INSERT` 命令都会中止。`INSERT` 策略不能有 `USING` 表达式，因为它只适用于向关系中添加记录的场景。

请注意，带有 `ON CONFLICT DO UPDATE` 的 `INSERT` 只会对通过 `INSERT` 路径追加到关系中的行检查 `INSERT` 策略的 `WITH CHECK` 表达式。

**`UPDATE`**

策略使用 `UPDATE` 表示它适用于 `UPDATE`、`SELECT FOR UPDATE` 和 `SELECT FOR SHARE` 命令，也适用于 `INSERT` 命令的辅助 `ON CONFLICT DO UPDATE` 子句。由于 `UPDATE` 会取出一条现有记录并用修改后的新记录替换它，`UPDATE` 策略同时接受 `USING` 和 `WITH CHECK` 表达式。`USING` 表达式决定 `UPDATE` 命令可以看到并操作哪些记录，`WITH CHECK` 表达式决定哪些修改后的行允许存回关系。

更新后的值未通过 `WITH CHECK` 表达式的任何行都会导致错误，整个命令都会中止。如果只指定 `USING` 子句，则该子句同时用于 `USING` 和 `WITH CHECK` 情况。

通常，`UPDATE` 命令还需要读取被更新关系中的列数据（例如在 `WHERE` 子句、`RETURNING` 子句或 `SET` 子句右侧表达式中）。此时还需要对被更新关系具有 `SELECT` 权限，并且除 `UPDATE` 策略外，还会应用相应的 `SELECT` 或 `ALL` 策略。因此，用户除通过 `UPDATE` 或 `ALL` 策略获得更新行的权限外，还必须通过 `SELECT` 或 `ALL` 策略获得访问被更新行的权限。

当 `INSERT` 命令有辅助的 `ON CONFLICT DO UPDATE` 子句时，如果采用 `UPDATE` 路径，首先会根据任何 `UPDATE` 策略的 `USING` 表达式检查要更新的行，然后根据 `WITH CHECK` 表达式检查更新后的新行。不过，与独立的 `UPDATE` 命令不同，如果现有行未通过 `USING` 表达式，会抛出错误（不会静默跳过 `UPDATE` 路径）。

**`DELETE`**

策略使用 `DELETE` 表示它适用于 `DELETE` 命令。`DELETE` 命令只能看到通过该策略的行。如果某行未通过 `DELETE` 策略的 `USING` 表达式，则它可能通过 `SELECT` 可见，但不能删除。

多数情况下，`DELETE` 命令还需要读取所删除关系中的列数据（例如在 `WHERE` 或 `RETURNING` 子句中）。此时还需要对该关系具有 `SELECT` 权限，并且除 `DELETE` 策略外，还会应用相应的 `SELECT` 或 `ALL` 策略。因此，用户除通过 `DELETE` 或 `ALL` 策略获得删除行的权限外，还必须通过 `SELECT` 或 `ALL` 策略获得访问待删除行的权限。

`DELETE` 策略不能有 `WITH CHECK` 表达式，因为它只适用于从关系中删除记录的场景，不存在需要检查的新行。

| 命令 | `SELECT/ALL policy, USING expression` | `INSERT/ALL policy, WITH CHECK expression` | `UPDATE/ALL policy, USING expression` | `UPDATE/ALL policy, WITH CHECK expression` | `DELETE/ALL policy, USING expression`|
|--------------|-----------|-----|-----------|-----|-----------|
| SELECT | 现有行 | -- | -- | -- | -- |
| SELECT FOR UPDATE/SHARE | 现有行 | -- | 现有行 | -- | -- |
| INSERT | -- | 新行 | -- | -- | -- |
| INSERT ... RETURNING | 新行<sup>[a]</sup> | 新行 | -- | -- | -- |
| UPDATE  | 现有行和新行<sup>[a]</sup> | -- | 现有行 | 新行 | -- |
| DELETE  | 现有行<sup>[a]</sup> | -- | -- | -- | 现有行 |
| ON CONFLICT DO UPDATE  | 现有行和新行 | -- | 现有行 | 新行 | -- |

<sup>[a]</sup>如果需要读取现有行或新行（例如引用关系列的 `WHERE` 或 `RETURNING` 子句）。

## 多个策略的应用 {#application-of-multiple-policies}

当多个不同命令类型的策略适用于同一命令时（例如 `SELECT` 和 `UPDATE` 策略应用于 `UPDATE` 命令），用户必须同时拥有两类权限（例如从关系选择行的权限以及更新行的权限）。因此，一类策略的表达式与另一类策略的表达式使用 `AND` 操作符组合。

当同一命令类型的多个策略适用于同一命令时，必须至少有一个授予关系访问权限的 `PERMISSIVE` 策略，并且所有 `RESTRICTIVE` 策略都必须通过。因此，所有 `PERMISSIVE` 策略表达式使用 `OR` 组合，所有 `RESTRICTIVE` 策略表达式使用 `AND` 组合，随后两个结果再使用 `AND` 组合。如果不存在 `PERMISSIVE` 策略，则拒绝访问。

请注意，在组合多个策略时，`ALL` 策略被视为与正在应用的其他策略类型相同。

例如，在同时需要 `SELECT` 和 `UPDATE` 权限的 `UPDATE` 命令中，如果每种类型都有多个适用策略，它们会按以下方式组合：

```sql
expression from RESTRICTIVE SELECT/ALL policy 1
AND
expression from RESTRICTIVE SELECT/ALL policy 2
AND
...
AND
(
  expression from PERMISSIVE SELECT/ALL policy 1
  OR
  expression from PERMISSIVE SELECT/ALL policy 2
  OR
  ...
)
AND
expression from RESTRICTIVE UPDATE/ALL policy 1
AND
expression from RESTRICTIVE UPDATE/ALL policy 2
AND
...
AND
(
  expression from PERMISSIVE UPDATE/ALL policy 1
  OR
  expression from PERMISSIVE UPDATE/ALL policy 2
  OR
  ...
)
```

## 注意事项 {#notes}

必须是表的所有者才能为其创建或更改策略。

虽然策略会应用于数据库中针对表的显式查询，但系统执行内部引用完整性检查或验证约束时不会应用策略。这意味着存在间接判断给定值是否存在的方法。例如，尝试向主键列或具有唯一约束的列插入重复值。如果插入失败，用户就可以推断该值已经存在。（此例假定用户有权插入自己无权查看的记录。）另一个例子是，用户可以向引用另一个隐藏表的表中插入数据。用户可以向引用表插入值来判断值是否存在；如果成功，就表明被引用表中存在该值。可以通过精心设计策略，阻止用户插入、删除或更新任何可能泄露其无权查看值的记录，或使用生成值（例如代理键）替代具有外部含义的键，来处理这些问题。

通常，系统会在用户查询中出现的条件之前强制执行安全策略施加的过滤条件，以防止不可信的用户定义函数意外暴露受保护数据。不过，系统（或系统管理员）标记为 `LEAKPROOF` 的函数和操作符可能在策略表达式之前计算，因为系统认为它们可信。

由于策略表达式会直接添加到用户查询中，因此会以执行整个查询的用户权限运行。因此，使用某策略的用户必须能够访问表达式引用的任何表或函数；否则，在查询启用了行级安全的表时会收到权限拒绝错误。不过，这不会改变视图的工作方式。与普通查询和视图一样，视图所引用表的权限检查和策略会使用视图所有者的权限以及适用于视图所有者的策略。

更多信息和实际示例请参见“关于配置行级安全策略”。

## 兼容性 {#compatibility}

`CREATE POLICY` 是 Apache Cloudberry 对 SQL 标准的扩展。

## 另请参阅 {#see-also}

[ALTER POLICY](/cloudberry/reference/sql-stmts/alter-policy/), [DROP POLICY](/cloudberry/reference/sql-stmts/drop-policy/), [ALTER TABLE](/cloudberry/reference/sql-stmts/alter-table/)
