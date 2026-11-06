---
title: "创建和管理表空间"
description: "表空间允许数据库管理员在每台机器上使用多个文件系统，并决定如何最佳地利用物理存储来保存数据库对象。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-tablespaces.md"
---

表空间允许为使用频繁和不频繁的数据库对象分配不同的存储，也可以控制某些数据库对象的 I/O 性能。例如，将频繁使用的表放在使用高性能固态硬盘（SSD）的文件系统上，将其他表放在标准硬盘上。

表空间需要一个主机文件系统位置来存储数据库文件。在 Apache Cloudberry 中，该文件系统位置必须存在于所有主机上，包括运行 Coordinator、Standby Coordinator、每个主 Segment 和每个镜像 Segment 的主机。

表空间是 Apache Cloudberry 的系统对象（全局对象）；只要拥有适当的权限，就可以从任何数据库使用表空间。

> **注意** Apache Cloudberry 不支持为具有相同内容 ID 的主 Segment—镜像 Segment 对设置不同的表空间位置。只能为不同的内容 ID 配置不同的位置。不要修改 `pg_tblspc` 目录下的符号链接，使主 Segment—镜像 Segment 对指向不同的文件位置；这会导致错误行为。

## 创建表空间 {#creating-a-tablespace}

`CREATE TABLESPACE` 命令定义表空间。例如：

```sql
CREATE TABLESPACE fastspace LOCATION '/fastdisk/gpdb';
```

数据库超级用户定义表空间，并使用 `GRANT``CREATE` 命令向数据库用户授予访问权限。例如：

```sql
GRANT CREATE ON TABLESPACE fastspace TO admin;
```

## 使用表空间存储数据库对象 {#using-a-tablespace-to-store-database-objects}

拥有表空间 `CREATE` 权限的用户可以在该表空间中创建数据库对象，例如表、索引和数据库。命令如下：

```sql
CREATE TABLE tablename(options) TABLESPACE spacename
```

例如，以下命令在名为 *space1* 的表空间中创建表：

```sql
CREATE TABLE foo(i int) TABLESPACE space1;
```

还可以使用 `default_tablespace` 参数，为未指定表空间的 `CREATE TABLE` 和 `CREATE INDEX` 命令指定默认表空间：

```sql
SET default_tablespace = space1;
CREATE TABLE foo(i int);
```

此外还有 `temp_tablespaces` 配置参数，它决定临时表和索引的位置，以及用于大数据集排序等目的的临时文件的位置。该参数可以是以逗号分隔的表空间名称列表，而不只是一个名称，这样与临时对象相关的负载就可以分散到多个表空间中。每次要创建临时对象时，都会从列表中随机选择一个成员。

与数据库关联的表空间存储该数据库的系统目录、使用该数据库的服务器进程创建的临时文件；如果创建对象时没有指定 `TABLESPACE`，它还是在该数据库中创建的表和索引所选用的默认表空间。如果创建数据库时没有指定表空间，则数据库使用其模板数据库所使用的同一个表空间。

只要拥有适当的权限，就可以在 Apache Cloudberry 系统中的任何数据库使用表空间。

## 查看现有表空间 {#viewing-existing-tablespaces}

每个 Apache Cloudberry 系统都有以下默认表空间。

- `pg_global`：用于共享系统目录。
- `pg_default`：默认表空间，由 *template1* 和 *template0* 数据库使用。

这些表空间使用默认系统位置，即系统初始化时创建的数据目录位置。

要查看表空间信息，请使用 `pg_tablespace` 目录表获取表空间的对象 ID（OID），然后使用 `gp_tablespace_location()` 函数显示表空间目录。以下示例列出一个用户定义的表空间 `myspace`：

```sql
SELECT oid, * FROM pg_tablespace ;

  oid  |  spcname   | spcowner | spcacl | spcoptions
-------+------------+----------+--------+------------
  1663 | pg_default |       10 |        |
  1664 | pg_global  |       10 |        |
 16391 | myspace    |       10 |        |
(3 rows)
```

表空间 `myspace` 的 OID 为 `16391`。运行 `gp_tablespace_location()`，显示由两个 Segment 实例和 Coordinator 组成的系统中的表空间位置。

```sql
# SELECT * FROM gp_tablespace_location(16391);
 gp_segment_id |    tblspc_loc
---------------+------------------
             0 | /data/mytblspace
             1 | /data/mytblspace
            -1 | /data/mytblspace
(3 rows)
```

该查询使用 `gp_tablespace_location()` 函数和 `gp_segment_configuration` 目录表，显示 Segment 实例信息以及 `myspace` 表空间的文件系统位置。

```
WITH spc AS (SELECT * FROM  gp_tablespace_location(16391))
  SELECT seg.role, spc.gp_segment_id as seg_id, seg.hostname, seg.datadir, tblspc_loc 
    FROM spc, gp_segment_configuration AS seg 
    WHERE spc.gp_segment_id = seg.content ORDER BY seg_id;
```

以下是一个测试系统的信息，该系统由单台主机上的两个 Segment 实例和 Coordinator 组成。

```sql
 role | seg_id | hostname |       datadir        |    tblspc_loc
------+--------+----------+----------------------+------------------
 p    |     -1 | testhost | /data/coordinator/gpseg-1 | /data/mytblspace
 p    |      0 | testhost | /data/data1/gpseg0   | /data/mytblspace
 p    |      1 | testhost | /data/data2/gpseg1   | /data/mytblspace
(3 rows)
```

## 删除表空间 {#dropping-tablespaces}

要删除表空间，必须是表空间所有者或超级用户。在使用该表空间的所有数据库中删除全部对象之前，不能删除表空间。

`DROP TABLESPACE` 命令删除空表空间。

> [!NOTE]
> 如果表空间不为空，或者其中存储着临时文件或事务文件，则不能删除该表空间。

## 移动临时文件或事务文件的位置 {#moving-the-location-of-temporary-or-transaction-files}

可以将临时文件或事务文件移动到特定表空间，以提高运行查询和创建备份时的数据库性能，并使数据存储得更连续。

Apache Cloudberry 服务器配置参数 `temp_tablespaces` 控制临时表和哈希聚合、哈希连接查询的临时溢出文件的位置。用于大数据集排序等目的的临时文件也会在这些表空间中创建。

`temp_tablespaces` 指定在 `CREATE` 命令未明确指定表空间时创建临时对象（临时表和临时表上的索引）的表空间。

关于临时文件或事务文件，还需注意以下信息：

- 临时文件或事务文件只能专用一个表空间，但可以使用同一个表空间存储其他类型的文件。
- 如果表空间被临时文件使用，则不能删除该表空间。
