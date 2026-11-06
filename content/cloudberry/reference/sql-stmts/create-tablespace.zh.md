---
title: "CREATE TABLESPACE"
description: "定义新的表空间。"
weight: 840
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-tablespace.md"
---

## 概要 {#synopsis}

```sql
CREATE TABLESPACE <tablespace_name>
   [ OWNER { <owner_name> | CURRENT_USER | SESSION_USER } ]
   LOCATION '<directory>' 
   [ WITH (content<ID_1>='<directory>'[, content<ID_2>='<directory>' ... ] [, <tablespace_option = value [, ... ] ] ) ]
```

## 描述 {#description}

`CREATE TABLESPACE` 为 Apache Cloudberry 系统注册并配置新的表空间。表空间名称必须不同于系统中任何现有表空间的名称。表空间是 Apache Cloudberry 系统对象（全局对象），只要具备适当权限，就可以从任何数据库使用它。

表空间允许超级用户为包含数据库对象（例如表和索引）的数据文件指定其他主机文件系统位置。

具有适当权限的用户可以向 [`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/)、[`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/) 或 [`CREATE INDEX`](/cloudberry/reference/sql-stmts/create-index/) 传递 tablespace_name，让 Apache Cloudberry 将这些对象的数据文件存储在指定表空间中。

在 Apache Cloudberry 中，该文件系统位置必须存在于所有主机上，包括运行 Coordinator、备用镜像、每个主 Segment 和每个镜像 Segment 的主机。

## 参数 {#parameters}

**`tablespace_name`**

要创建的表空间名称。名称不能以 `pg_` 或 `gp_` 开头，因为这类名称保留给系统表空间。

**`owner_name`**

表空间所有者的用户名。如果省略，默认为运行命令的用户。只有超级用户才能创建表空间，但可以将表空间所有权分配给非超级用户。

**`LOCATION 'directory'`**

用于表空间的目录。目录应为空，并且必须归 Apache Cloudberry 系统用户所有。必须指定目录的绝对路径，路径名长度不得超过 100 个字符。（此位置用于在 pg_tblspc 目录中创建符号链接目标；`pg_basebackup` 等工具向 `tar` 传递符号链接目标时，会将其截断为 100 个字符。）

可以在 `WITH` 子句中为任意 Apache Cloudberry Segment 实例指定不同的表空间目录。

**`contentID_i='directory_i'`**

ID_i 是 Segment 实例的 content ID。directory_i 是该实例用作表空间根目录的主机文件系统位置的绝对路径。不能指定 Coordinator 实例的 content ID（`-1`）。可以为多个 Segment 指定相同目录。

如果 `WITH` 子句未列出某个 Segment 实例，Apache Cloudberry 将使用 `LOCATION` 子句指定的表空间目录。

`LOCATION` 目录的限制也适用于 directory_i。

**`tablespace_option`**

要设置或重置的表空间参数。目前只有 `seq_page_cost` 和 `random_page_cost` 两个参数。为特定表空间设置其中任一值，都会覆盖规划器通常依据同名配置参数确定的、从该表空间的表中读取页面的代价估算（见 `seq_page_cost`、`random_page_cost`）。当某个表空间位于比 I/O 子系统其他部分更快或更慢的磁盘上时，这可能有用。

## 注意事项 {#notes}

由于 `CREATE TABLESPACE` 会从 Coordinator 和 Segment 实例数据目录中的 `pg_tblspc` 目录创建指向命令所指定目录的符号链接，Apache Cloudberry 只在支持符号链接的系统上支持表空间。

不能在事务块中运行 `CREATE TABLESPACE`。

创建表空间时，应确保文件系统位置具有足够的 I/O 速度和可用磁盘空间。

> [!NOTE]
> Apache Cloudberry 不支持为具有相同 content ID 的主镜像对配置不同表空间位置，只能为不同 content ID 配置不同位置。不要修改 `pg_tblspc` 目录下的符号链接，让主镜像对指向不同文件位置；这会导致错误行为。

## 示例 {#examples}

创建新的表空间，并指定 Coordinator 和所有 Segment 实例的文件系统位置：

```sql
CREATE TABLESPACE mytblspace LOCATION '/mydbtspc/mytestspace';
```

在 `/data/indexes` 创建归用户 `genevieve` 所有的表空间 `indexspace`：

```sql
CREATE TABLESPACE indexspace OWNER genevieve LOCATION '/data/indexes';
```

创建新的表空间，并为 content ID 为 0 和 1 的 Segment 实例指定位置。对于 Coordinator 及 `WITH` 子句未列出的 Segment 实例，表空间的文件系统位置使用 `LOCATION` 子句指定的目录。

```sql
CREATE TABLESPACE mytblspace LOCATION '/mydbtspc/mytestspace' WITH (content0='/temp/mytest', content1='/temp/mytest');
```

此示例为两个 Segment 实例指定了相同位置。也可以为每个 Segment 指定不同位置。

## 兼容性 {#compatibility}

`CREATE TABLESPACE` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[`CREATE DATABASE`](/cloudberry/reference/sql-stmts/create-database/), [`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/), [`CREATE INDEX`](/cloudberry/reference/sql-stmts/create-index/), [`DROP TABLESPACE`](/cloudberry/reference/sql-stmts/drop-tablespace/), [`ALTER TABLESPACE`](/cloudberry/reference/sql-stmts/alter-tablespace/)
