---
title: "SET"
description: "更改 Apache Cloudberry 运行时配置参数的值。"
weight: 1730
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/set.md"
---

## 语法概要 {#synopsis}

```sql
SET [ SESSION | LOCAL ] <configuration_parameter> { TO | = } { <value> | '<value>' | DEFAULT }

SET [SESSION | LOCAL] TIME ZONE { <value> | '<value>' |  LOCAL | DEFAULT }
```

## 说明 {#description}

`SET` 命令更改服务器配置参数。任何归类为会话参数的配置参数都可以使用 `SET` 动态更改。（某些参数需要超级用户权限才能更改，另一些参数则在服务器或会话启动后无法更改。）`SET` 仅影响当前会话使用的值。

如果在事务内执行 `SET` 或 `SET SESSION`，而该事务随后被取消，则事务回滚时 `SET` 命令的效果会消失。一旦所在事务提交，其效果将持续到会话结束，除非被另一个 `SET` 覆盖。

`SET LOCAL` 的效果仅持续到当前事务结束，无论事务是否提交。一个特殊情况是在同一事务中先执行 `SET`，再执行 `SET LOCAL`：事务结束之前使用 `SET LOCAL` 设置的值，而在此之后（如果事务提交）则使用 `SET` 设置的值。

回滚到早于该命令的保存点也会取消 `SET` 或 `SET LOCAL` 的效果。

如果在函数中使用 `SET LOCAL`，而该函数包含针对同一配置参数的 `SET` 选项（参见 [CREATE FUNCTION](/cloudberry/reference/sql-stmts/create-function/)），则函数退出时 `SET LOCAL` 命令的效果会消失；无论如何都会恢复函数调用时生效的值。这样既可以通过 `SET LOCAL` 在函数内动态或反复更改参数，又能保留使用 `SET` 选项保存和恢复调用者参数值的便利。请注意，普通的 `SET` 命令会覆盖外围函数的任何 `SET` 选项；除非回滚，否则其效果将一直保持。

有关服务器参数的信息，请参见服务器配置参数。

## 参数 {#parameters}

**`SESSION`**

指定命令对当前会话生效。如果既未出现 `SESSION` 也未出现 `LOCAL`，则采用此默认行为。

**`LOCAL`**

指定命令仅对当前事务生效。在 `COMMIT` 或 `ROLLBACK` 后，会话级设置重新生效。在事务块之外执行此命令会发出警告，除此之外没有任何效果。

**`configuration_parameter`**

可设置的 Apache Cloudberry 运行时配置参数名称。只有归类为*会话*的参数才能用 `SET` 更改。详情请参见服务器配置参数。

**`value`**

参数的新值。根据具体参数的要求，可以将值指定为字符串常量、标识符、数字，或由这些值组成的逗号分隔列表。可以用 `DEFAULT` 将参数重置为默认值（即假如当前会话中未执行过 `SET` 时该参数应有的值）。指定内存大小或时间单位时，请用单引号括起该值。

有些配置参数只能使用 `SET` 命令调整，或具有特殊语法：

**`SCHEMA`**

`SET SCHEMA '<value>'` 是 `SET <search_path> TO <value>` 的别名。使用此语法只能指定一个模式。

**`NAMES`**

`SET NAMES <value>` 是 `SET client_encoding TO <value>` 的别名。

**`SEED`**

设置随机数生成器（函数 `random()`）的内部种子。允许的值为 -1 到 1 之间的浮点数，包括两端。

也可以调用 `setseed()` 函数设置种子：

```sql
SELECT setseed(value);
```

**`TIME ZONE`**

`SET TIME ZONE <value>` 是 `SET timezone TO <value>` 的别名。`SET TIME ZONE` 语法允许使用特殊语法指定时区。以下是合法值的示例：

- `'PST8PDT'`
- `'Europe/Rome'`
- `-7`（比 UTC 晚 7 小时的时区）
- `INTERVAL '-08:00' HOUR TO MINUTE`（比 UTC 晚 8 小时的时区）。

**`LOCAL`**<br />
**`DEFAULT`**

将时区设为本地时区（即服务器的 timezone 默认值）。

有关 Apache Cloudberry 时区的更多信息，请参见 PostgreSQL 文档的[时区](https://www.postgresql.org/docs/12/datatype-datetime.html#DATATYPE-TIMEZONES)一节。

## 示例 {#examples}

设置模式搜索路径：

```sql
SET search_path TO my_schema, public;
```

将 Segment 主机上每个查询的内存增加到 200 MB：

```sql
SET statement_mem TO '200MB';
```

将日期样式设置为传统的 POSTGRES 样式，并采用“日先于月”的输入约定：

```sql
SET datestyle TO postgres, dmy;
```

设置加利福尼亚州圣马特奥的时区（太平洋时间）：

```sql
SET TIME ZONE 'PST8PDT';
```

设置意大利的时区：

```sql
SET TIME ZONE 'Europe/Rome'; 
```

## 兼容性 {#compatibility}

`SET TIME ZONE` 扩展了 SQL 标准定义的语法。标准仅允许数值时区偏移，而 Apache Cloudberry 允许更灵活的时区指定方式。所有其他 `SET` 功能都是 Apache Cloudberry 的扩展。

## 另请参阅 {#see-also}

[RESET](/cloudberry/reference/sql-stmts/reset/), [SHOW](/cloudberry/reference/sql-stmts/show/)
