---
title: "第 3 课：创建表"
description: "学习如何在 Apache Cloudberry 中创建表。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/tutorials/quick-trial-lessons/create-tables.md"
---

在[第 2 课：创建和准备数据库](/cloudberry/tutorials/quick-trial-lessons/create-and-prepare-database/)中创建并准备好数据库后，就可以开始在数据库中创建表。

> [!NOTE]
> 为了介绍 Apache Cloudberry，我们使用由美国交通部发布的公开数据集——航空公司航班准点统计和延误原因数据集，网址为 http://www.transtats.bts.gov/。航班准点率数据集按日期、航空公司、始发机场、目的机场和许多其他航班详细信息记录航班。该数据集包含自 1987 年以来的航班数据。本指南中的练习使用 2009 年和 2010 年约一百万个航班的数据。学习本简介时，建议查看 GitHub [`000-cbdb-sandbox/configs/faa.tar.gz`](https://github.com/apache/cloudberry-bootcamp/tree/main/000-cbdb-sandbox/configs) 目录中的 SQL 脚本。大多数练习既可以手动输入命令，也可以执行 `faa` 目录中的脚本。

## 使用 psql 中的 SQL 文件创建表 {#create-tables-using-a-sql-file-in-psql}

在 Apache Cloudberry 中，可以使用 `CREATE TABLE` SQL 语句创建表。

下面的步骤将引导你运行 SQL 文件 `create_dim_tables.sql`，其中包含创建 `faa` 数据库所需的 `CREATE TABLE` 语句。

1. 以 `gpadmin` 用户在 Docker 中登录 Apache Cloudberry。然后进入 `faa` 目录，SQL 文件 `create_dim_tables.sql` 位于该目录中。

    ```shell
    [gpadmin@cdw tmp]$ cd /tmp
    [gpadmin@cdw tmp]$ tar xzf faa.tar.gz
    [gpadmin@cdw tmp]$ cd faa
    ```

2. 查看 `create_dim_tables.sql` 文件。

    ```shell
    [gpadmin@cdw faa]$ more create_dim_tables.sql
    ```

    `create_dim_tables.sql` 文件包含以下 `CREATE TABLE` 语句：

    ```sql
    DROP TABLE IF EXISTS faa.d_airports;  -- Drops the table if it exists to avoid name conflict.
    CREATE TABLE faa.d_airports (  -- Creates the table.
        AirportID      INTEGER,
        Name           TEXT,
        City           TEXT,
        Country        TEXT,
        airport_code   TEXT,
        ICOA_code      TEXT,
        Latitude       FLOAT8,
        Longitude      FLOAT8,
        Altitude       FLOAT8,
        TimeZoneOffset FLOAT,
        DST_Flag       TEXT,
        TZ             TEXT
    )
    DISTRIBUTED BY (airport_code);  -- Specifies the distribution column airport_code.

    DROP TABLE IF EXISTS faa.d_wac;
    CREATE TABLE faa.d_wac (wac SMALLINT, area_desc TEXT)
    DISTRIBUTED BY (wac);

    DROP TABLE IF EXISTS faa.d_airlines;
    CREATE TABLE faa.d_airlines (airlineid INTEGER, airline_desc TEXT)
    DISTRIBUTED BY (airlineid);

    DROP TABLE IF EXISTS faa.d_cancellation_codes;
    CREATE TABLE faa.d_cancellation_codes (cancel_code TEXT, cancel_desc TEXT)
    DISTRIBUTED BY (cancel_code);

    DROP TABLE IF EXISTS faa.d_delay_groups;
    CREATE TABLE faa.d_delay_groups (delay_group_code TEXT, delay_group_desc TEXT)
    DISTRIBUTED BY (delay_group_code);

    DROP TABLE IF EXISTS faa.d_distance_groups;
    CREATE TABLE faa.d_distance_groups (distance_group_code TEXT, distance_group_desc TEXT)
    DISTRIBUTED BY (distance_group_code);
    ```

3. 以 `lily` 用户连接 `tutorial` 数据库，并使用 `psql`。你将以 `lily` 用户运行 SQL 文件。

    ```shell
    [gpadmin@cdw faa]$ psql -U lily tutorial

    Password for user lily:  # changeme
    ```

    ```shell
    psql (14.4, server 14.4)
    Type "help" for help.
    tutorial=>
    ```

4. 使用 `psql` 的 `\i` 命令运行 `create_dim_tables.sql` 文件。

    ```sql
    tutorial=> \i create_dim_tables.sql
    ```

    此时会显示以下消息：

    ```sql
    psql:create_dim_tables.sql:1: NOTICE:  table "d_airports" does not exist, skipping
    DROP TABLE
    CREATE TABLE
    psql:create_dim_tables.sql:18: NOTICE:  table "d_wac" does not exist, skipping
    DROP TABLE
    CREATE TABLE
    psql:create_dim_tables.sql:22: NOTICE:  table "d_airlines" does not exist, skipping
    DROP TABLE
    CREATE TABLE
    psql:create_dim_tables.sql:26: NOTICE:  table "d_cancellation_codes" does not exist, skipping
    DROP TABLE
    CREATE TABLE
    psql:create_dim_tables.sql:30: NOTICE:  table "d_delay_groups" does not exist, skipping
    DROP TABLE
    CREATE TABLE
    psql:create_dim_tables.sql:34: NOTICE:  table "d_distance_groups" does not exist, skipping
    DROP TABLE
    CREATE TABLE
    ```

5. 使用 `\dt` 命令显示 `faa` 模式中的所有表。可以看到已创建 6 个表。

    ```sql
    tutorial=> \dt
                        List of relations
    Schema |         Name         | Type  | Owner | Storage
   --------+----------------------+-------+-------+---------
    faa    | d_airlines           | table | lily  | heap
    faa    | d_airports           | table | lily  | heap
    faa    | d_cancellation_codes | table | lily  | heap
    faa    | d_delay_groups       | table | lily  | heap
    faa    | d_distance_groups    | table | lily  | heap
    faa    | d_wac                | table | lily  | heap
    (6 rows)
    ```

## 关于分布策略 {#about-the-distribution-policy}

表定义包含数据的分布策略，这对查询性能至关重要。分布策略的目标是：

- 在 Segment 之间均匀分布数据量和查询执行工作。
- 使 Segment 能够在本地完成复杂的查询处理步骤。

分布策略决定数据如何在 Segment 之间分布。要制定有效的分布策略，需要了解数据的特征、数据上将执行的查询类型，以及哪种分布策略能够最好地利用 Segment 之间的并行执行能力。

在 `CREATE TABLE` 语句中使用 `DISTRIBUTED` 子句为表定义分布策略。理想情况下，每个 Segment 都拥有相同的数据量，并在查询运行时承担相同份额的工作。Apache Cloudberry 中有两种分布策略语法：

- `DISTRIBUTED BY (column, ...)` 根据一个或多个列定义分布键。对分布键应用哈希函数，确定相应行存储在哪个 Segment 上。分布键相同的行存储在同一个 Segment 上。如果分布键是唯一的，哈希函数会确保数据均匀分布。默认分布策略是按表的主键进行哈希；如果未指定主键，则按表的第一列进行哈希。
- `DISTRIBUTED RANDOMLY` 以轮询方式在 Segment 之间分布行。

如果要连接的不同表具有相同或相似的分布键列，连接操作可能可以在 Segment 上完成，这比先在 Segment 之间重分布行再进行连接快得多。随机分布策略无法实现这一点，因此为表设置分布键显然更好。
