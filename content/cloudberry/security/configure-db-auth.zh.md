---
title: "配置数据库授权"
description: "本文介绍如何使用角色和权限，在用户级别限制对数据库数据的授权访问。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/configure-db-auth.md"
---

## 访问权限与角色 {#access-permissions-and-roles}

Apache Cloudberry 使用*角色*管理数据库访问权限。角色的概念涵盖用户和组。角色可以是数据库用户、组，也可以同时兼具两者身份。角色可以拥有数据库对象（例如表），并将这些对象的权限授予其他角色，以控制对象访问。角色也可以是其他角色的成员，因此成员角色可以继承其父角色的对象权限。

每个 Apache Cloudberry 系统都包含一组数据库角色（用户和组）。这些角色独立于服务器所在操作系统管理的用户和组。不过，为方便使用，可以让操作系统用户名与 Apache Cloudberry 角色名保持对应关系，因为许多客户端应用程序默认使用当前操作系统的用户名。

在 Apache Cloudberry 中，用户通过 Coordinator 实例登录并连接，Coordinator 会验证其角色和访问权限。然后，Coordinator 在后台以当前登录角色的身份向 Segment 实例发出命令。

角色在系统级别定义，因此对系统中的所有数据库都有效。

为引导 Apache Cloudberry 系统，刚完成初始化的系统始终包含一个预定义的超级用户角色（也称为系统用户）。该角色与初始化 Apache Cloudberry 系统的操作系统用户同名。按照惯例，此角色名为 `gpadmin`。要创建更多角色，必须先以这个初始角色连接。

## 管理对象权限 {#manage-object-privileges}

创建对象（表、视图、序列、数据库、函数、语言、模式或表空间）时，会为其指定一个所有者。所有者通常是执行创建语句的角色。对于大多数类型的对象，初始状态下只有所有者（或超级用户）能够对其执行操作。要允许其他角色使用对象，必须授予相应权限。Apache Cloudberry 为各类对象支持以下权限：

|对象类型|权限|
|:----------|:---------|
|表、视图、序列|`SELECT`<br/>`INSERT`<br/>`UPDATE`<br/>`DELETE`<br/>`RULE`<br/>`ALL`|
|外部表|`SELECT`<br/>`RULE`<br/>`ALL`|
|数据库|`CONNECT`<br/>`CREATE`<br/>`TEMPORARY` 或 `TEMP`<br/>`ALL`|
|函数|`EXECUTE`|
|过程语言|`USAGE`|
|模式|`CREATE`<br/>`USAGE`<br/>`ALL`|

必须为每个对象单独授予权限。例如，在数据库上授予 `ALL` 并不意味着可以完全访问该数据库中的对象。它只是在数据库本身上授予所有数据库级权限（`CONNECT`、`CREATE`、`TEMPORARY`）。

使用 `GRANT` SQL 命令将对象的权限授予指定角色。例如：

```sql
GRANT INSERT ON mytable TO jsmith; 
```

要撤销权限，请使用 `REVOKE` 命令。例如：

```sql
REVOKE ALL PRIVILEGES ON mytable FROM jsmith; 
```

还可以使用 `DROP OWNED` 和 `REASSIGN OWNED` 命令，管理已停用角色拥有的对象。（注意：只有对象的所有者或超级用户才能删除对象或重新指定其所有者。）例如：

```sql
REASSIGN OWNED BY sally TO bob;
DROP OWNED BY visitor; 
```

## 按时间限制访问 {#restrict-access-by-time}

Apache Cloudberry 允许管理员按角色限制访问时间。使用 `CREATE ROLE` 或 `ALTER ROLE` 命令指定基于时间的限制。

可以按星期几，或按星期几和时间限制访问。无需删除并重新创建角色即可移除这些限制。

基于时间的限制只适用于分配了这些限制的角色。如果某个角色是另一个包含时间限制的角色的成员，则不会继承该时间限制。

基于时间的限制仅在登录时强制执行。`SET ROLE` 和 `SET SESSION AUTHORIZATION` 命令不受任何基于时间的限制影响。

需要超级用户或 `CREATEROLE` 权限才能为角色设置基于时间的限制。任何人都不能为超级用户添加基于时间的限制。

添加基于时间的限制有两种方式。在 `CREATE ROLE` 或 `ALTER ROLE` 命令中使用关键字 `DENY`，后跟以下内容之一。

- 访问受限的某一天，也可以选择指定时间。例如，星期三全天不允许访问。
- 一个时间段，即访问受限的起始日和结束日，以及可选的时间。例如，从星期三晚上 10 点到星期四早上 8 点不允许访问。

可以指定多个限制；例如，星期三全天不允许访问，以及星期五 15:00 到 17:00 之间不允许访问。

指定某一天有两种方式。如下面的表格所示，使用 `DAY`，后跟用单引号括起的英文星期名称，或 0 到 6 之间的数字。

|英文名称|数字|
|:-----------|:-----|
|DAY 'Sunday'|DAY 0|
|DAY 'Monday'|DAY 1|
|DAY 'Tuesday'|DAY 2|
|DAY 'Wednesday'|DAY 3|
|DAY 'Thursday'|DAY 4|
|DAY 'Friday'|DAY 5|
|DAY 'Saturday'|DAY 6|

一天中的时间可以使用 12 小时制或 24 小时制指定。`TIME` 后跟用单引号括起的时间规格。只指定小时和分钟，两者之间用冒号（:）分隔。使用 12 小时制时，在末尾添加 `AM` 或 `PM`。以下示例展示了各种时间规格。

```sql
TIME '14:00'     # 24-hour time implied
TIME '02:00 PM'  # 12-hour time specified by PM 
TIME '02:00'     # 24-hour time implied. This is equivalent to TIME '02:00 AM'. 
```

> [!NOTE] 注意
> 基于时间的认证使用服务器时间强制执行。系统会忽略时区。

要指定拒绝访问的时间段，请使用两个日期/时间规格，并按示例使用 `BETWEEN` 和 `AND`。`DAY` 始终是必需的。

```sql
BETWEEN DAY 'Monday' AND DAY 'Tuesday' 

BETWEEN DAY 'Monday' TIME '00:00' AND
        DAY 'Monday' TIME '01:00'

BETWEEN DAY 'Monday' TIME '12:00 AM' AND
        DAY 'Tuesday' TIME '02:00 AM'

BETWEEN DAY 'Monday' TIME '00:00' AND
        DAY 'Tuesday' TIME '02:00'
        DAY 2 TIME '02:00'
```

最后三个语句是等价的。

> [!NOTE] 注意
> 天数区间不能跨越星期六。

以下语法不正确：

```sql
DENY BETWEEN DAY 'Saturday' AND DAY 'Sunday'
```

正确的写法使用两个 DENY 子句，如下所示：

```sql
DENY DAY 'Saturday'
DENY DAY 'Sunday'
```

以下示例演示如何创建带有基于时间限制的角色，以及修改角色以添加基于时间限制。示例只显示基于时间限制所需的语句。详情请参阅 [`CREATE ROLE`](/cloudberry/reference/sql-stmts/create-role/) 和 [`ALTER ROLE`](/cloudberry/reference/sql-stmts/alter-table/)。

### 示例 1 — 创建带有基于时间限制的新角色 {#example-1--create-a-new-role-with-time-based-constraints}

周末不允许访问。

```sql
CREATE ROLE generaluser
DENY DAY 'Saturday'
DENY DAY 'Sunday'
... 
```

### 示例 2 — 修改角色以添加基于时间限制 {#example-2--alter-a-role-to-add-time-based-constraints}

每天凌晨 2:00 到 4:00 之间不允许访问。

```sql
ALTER ROLE generaluser
 DENY BETWEEN DAY 'Monday' TIME '02:00' AND DAY 'Monday' TIME '04:00'
 DENY BETWEEN DAY 'Tuesday' TIME '02:00' AND DAY 'Tuesday' TIME '04:00'
 DENY BETWEEN DAY 'Wednesday' TIME '02:00' AND DAY 'Wednesday' TIME '04:00'
 DENY BETWEEN DAY 'Thursday' TIME '02:00' AND DAY 'Thursday' TIME '04:00'
 DENY BETWEEN DAY 'Friday' TIME '02:00' AND DAY 'Friday' TIME '04:00'
 DENY BETWEEN DAY 'Saturday' TIME '02:00' AND DAY 'Saturday' TIME '04:00'
 DENY BETWEEN DAY 'Sunday' TIME '02:00' AND DAY 'Sunday' TIME '04:00'
  ... 
```

### 示例 3 — 修改角色以添加基于时间限制 {#example-3--alter-a-role-to-add-time-based-constraints}

星期三全天不允许访问，星期五 15:00 到 17:00 之间也不允许访问。

```sql
ALTER ROLE generaluser
 DENY DAY 'Wednesday'
 DENY BETWEEN DAY 'Friday' TIME '15:00' AND DAY 'Friday' TIME '17:00'
 
```

## 删除基于时间的限制 {#drop-a-time-based-restriction}

要移除基于时间的限制，请使用 `ALTER ROLE` 命令。输入关键字 `DROP DENY FOR`，后跟要删除的日期/时间规格。

```sql
DROP DENY FOR DAY 'Sunday' 
```

包含 `DROP` 子句中全部或部分条件的任何限制都会被移除。例如，如果现有的限制禁止星期一和星期二访问，而 `DROP` 子句删除星期一的限制，则现有的限制将被完全删除。`DROP` 子句会完全删除与其中限制重叠的所有限制。即使重叠的限制还包含 `DROP` 子句中未提及的其他限制，也会被完全删除。

示例 1：从角色中移除基于时间的限制

```sql
ALTER ROLE generaluser
DROP DENY FOR DAY 'Monday'
    ... 
```

对于示例 2 中角色 `generaluser` 的星期一限制，此语句会删除与其重叠的所有限制，即使其中还包含其他限制。
