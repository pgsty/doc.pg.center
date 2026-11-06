---
title: "创建和管理分区表"
description: "本文介绍如何使用推荐语法在 Apache Cloudberry 中创建和维护分区表。"
weight: 110
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/create-and-manage-partitioned-tables.md"
---

有关分区表的更多信息，请参见[表分区概述](/cloudberry/operate-with-data/operate-with-db-objects/about-table-partitioning/)。

## 创建分区表 {#create-partitioned-tables}

创建分区表之前，应当：

- 选择分区方法：范围、列表或哈希。
- 选择分区键列。
- 确定合适的分区数量和层级数（如果使用多级分区）。
- 创建分区表。
- 创建各个分区。

Apache Cloudberry 会自动创建描述分区边界条件的约束。插入根分区表的任何数据，只要匹配某个分区的约束，就会被定向到该分区。

对于子分区，必要时可以使用相同的分区键列（例如，先按月分区，再按日划分子分区）。可以考虑直接按最细粒度分区（例如，创建 365 个按日分区，而不是先按年、再按月、最后按日分区），因为扁平的分区设计通常执行得更快，不过多级设计可以缩短查询规划时间。

### 定义日期范围分区表 {#define-a-date-range-partitioned-table}

日期范围分区表使用 `date` 或 `timestamp` 列作为分区键。范围分区表可以指定多个分区键列。

示例：为一家冰淇淋公司创建 `measurement` 表，按 `logdate` 列逐月分区，以保留 2 年的数据，并每月删除最早一个月的数据。

1. 创建根分区表：

    ```sql
    CREATE TABLE measurement (
        city_id         int not null,
        logdate         date not null,
        peaktemp        int,
        unitsales       int
    )
    DISTRIBUTED BY (city_id)
    PARTITION BY RANGE (logdate);
    ```

2. 创建分区（例如，为每个月创建一个分区）：

    ```sql
    CREATE TABLE measurement_y2021m01 PARTITION OF measurement
    FOR VALUES FROM ('2021-01-01') TO ('2021-02-01');

    CREATE TABLE measurement_y2021m02 PARTITION OF measurement
    FOR VALUES FROM ('2021-02-01') TO ('2021-03-01');
    -- ... and so on for other months ...

    CREATE TABLE measurement_y2022m12 PARTITION OF measurement
    FOR VALUES FROM ('2022-12-01') TO ('2023-01-01') -- Note: Source had '2022-01-01' likely a typo for '2023-01-01'
    TABLESPACE fasttablespace;

    CREATE TABLE measurement_y2023m01 PARTITION OF measurement
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01')
    WITH (parallel_workers = 4)
    TABLESPACE fasttablespace;
    ```

    范围不包含上界。如果插入父表的数据无法映射到现有分区，Apache Cloudberry 会返回错误（除非存在默认分区）。

### 定义数值范围分区表 {#define-a-numeric-range-partitioned-table}

此类表使用数值类型的列作为分区键，支持多个分区键列。

示例：创建按 `year` 分区的 `numpart` 表。

1. 创建根分区表：

    ```sql
    CREATE TABLE numpart (id int, rank int, year int, color char(1), count int)
    DISTRIBUTED BY (id)
    PARTITION BY RANGE (year);
    ```

2. 创建分区：

    ```sql
    CREATE TABLE numpart_y2019 PARTITION OF numpart FOR VALUES FROM (2019) TO (2020);
    CREATE TABLE numpart_y2020 PARTITION OF numpart FOR VALUES FROM (2020) TO (2021);
    CREATE TABLE numpart_y2021 PARTITION OF numpart FOR VALUES FROM (2021) TO (2022);
    CREATE TABLE numpart_y2022 PARTITION OF numpart FOR VALUES FROM (2022) TO (2023);
    ```

### 定义列表分区表 {#define-a-list-partitioned-table}

列表分区表可以使用任何支持相等比较的数据类型的列作为分区键。列表分区只允许使用单列作为分区键。必须为每个列表值声明分区规范。

示例：创建按 `color` 分区的 `listpart` 表。

1. 创建根分区表：

    ```sql
    CREATE TABLE listpart (id int, rank int, year int, color char(1), count int)
    DISTRIBUTED BY (id)
    PARTITION BY LIST (color);
    ```

2. 创建分区：

    ```sql
    CREATE TABLE listpart_red PARTITION OF listpart FOR VALUES IN ('r');
    CREATE TABLE listpart_green PARTITION OF listpart FOR VALUES IN ('g');
    CREATE TABLE listpart_blue PARTITION OF listpart FOR VALUES IN ('b');
    CREATE TABLE listpart_other PARTITION OF listpart DEFAULT;
    ```

    `DEFAULT` 关键字创建默认分区，用于接收不匹配其他分区的数据。

### 定义哈希分区表 {#define-a-hash-partitioned-table}

哈希分区表使用单个可哈希的列作为分区键。必须为每种模数／余数组合声明分区规范。

示例：创建按列 `c` 的哈希值分区的 `hpt` 表。

1. 创建根分区表：

    ```sql
    CREATE TABLE hpt (a int, b int, c text) PARTITION BY HASH(c);
    ```

2. 创建分区：

    ```sql
    CREATE TABLE hpt_p1 PARTITION OF hpt FOR VALUES WITH (MODULUS 3, REMAINDER 0);
    CREATE TABLE hpt_p2 PARTITION OF hpt FOR VALUES WITH (MODULUS 3, REMAINDER 1);
    CREATE TABLE hpt_p3 PARTITION OF hpt FOR VALUES WITH (MODULUS 3, REMAINDER 2);
    ```

### 定义多级分区表 {#define-a-multi-level-partitioned-table}

可以对现有分区进一步划分子分区，以创建多级分区层次结构。

示例：为 `msales` 创建两级分区，先按 `year` 进行范围分区，再按 `region` 进行列表子分区。

1. 创建根（第 1 级）分区表：

    ```sql
    CREATE TABLE msales (trans_id int, year int, amount decimal(9,2), region text)
    DISTRIBUTED BY (trans_id)
    PARTITION BY RANGE (year);
    ```

2. 创建按年的分区（第 2 级），这些分区本身再按区域分区：

    ```sql
    CREATE TABLE msales_2021 PARTITION OF msales FOR VALUES FROM (2021) TO (2022)
    PARTITION BY LIST (region);
    CREATE TABLE msales_2022 PARTITION OF msales FOR VALUES FROM (2022) TO (2023)
    PARTITION BY LIST (region);
    CREATE TABLE msales_2023 PARTITION OF msales FOR VALUES FROM (2023) TO (2024)
    PARTITION BY LIST (region);
    ```

3. 创建区域子分区（叶子分区）：

    ```sql
    CREATE TABLE msales_2021_usa PARTITION OF msales_2021 FOR VALUES IN ('usa');
    CREATE TABLE msales_2021_asia PARTITION OF msales_2021 FOR VALUES IN ('asia');
    CREATE TABLE msales_2021_europe PARTITION OF msales_2021 FOR VALUES IN ('europe');
    -- ... and similarly for msales_2022 and msales_2023 ...
    ```

## 对现有表进行分区 {#partition-an-existing-table}

表只能在创建时进行分区。要对现有表进行分区：

1. 创建具有所需结构的新分区表。
2. 将原表的数据加载到新分区表中。
3. 删除原表。
4. 将新分区表重命名为原表的名称。
5. 重新授予所需权限。

```sql
-- Assume 'msales' is an existing non-partitioned table
-- 1. Create new partitioned table (msales2)
CREATE TABLE msales2 (LIKE msales) PARTITION BY RANGE (year); -- Define partitions for msales2 here
-- (Example: CREATE TABLE msales2_y2021 PARTITION OF msales2 FOR VALUES FROM (2021) TO (2022); etc.)

-- 2. Load data
INSERT INTO msales2 SELECT * FROM msales;

-- 3. Drop old table
DROP TABLE msales;

-- 4. Rename new table
ALTER TABLE msales2 RENAME TO msales;

-- 5. Re-grant permissions
GRANT ALL PRIVILEGES ON msales TO admin;
GRANT SELECT ON msales TO guest;
```

注意：根据分区表创建新表时，`LIKE` 子句不会复制分区结构。

## 向分区表加载数据 {#load-data-into-a-partitioned-table}

最初，顶层根分区表为空。向根表插入数据时，Apache Cloudberry 会将数据路由到最底层的相应叶子分区。在多级设计中，只有最底层的叶子分区包含数据。

Apache Cloudberry 会拒绝无法映射到叶子分区的行，并使加载失败，除非定义了 `DEFAULT` 分区来接收此类行。

请谨慎使用 ` DEFAULT` 分区：只要其中包含数据，查询优化器就总会扫描它们，可能增加整体扫描时间。

使用 `COPY` 或 `INSERT` 向父表加载数据时，数据会自动路由到正确的叶子分区。最佳实践是：加载大量数据时，先创建中间暂存表，将数据加载到该表中，再将其挂接到分区层次结构中。

## 验证分区策略 {#verify-the-partition-strategy}

使用 `EXPLAIN` 命令检查查询计划，验证优化器是否只扫描相关分区。

示例：对于按 `year` 分区、再按 `region` 划分子分区的 `msales` 表：

```sql
EXPLAIN SELECT * FROM msales WHERE year='2021' AND region='usa';
```

查询计划应当显示只扫描 `msales_2021_usa`（相关叶子分区）。对父表或默认分区（如果有）的扫描应返回 0–1 行。请确保没有扫描不必要的分区。

### 排查选择性分区扫描问题 {#troubleshoot-selective-partition-scans}

以下限制可能使选择性扫描无法进行：

- 只有查询使用 `=`、`<`、`<=`、`>`、`>=` 和 `<>` 等不可变操作符，对表施加直接且简单的限制时，查询优化器才能进行选择性扫描。
- 选择性扫描能识别查询中的 `STABLE` 和 `IMMUTABLE` 函数，但不能识别 `VOLATILE` 函数。例如，`WHERE date > CURRENT_DATE` 允许选择性扫描，而 `WHERE time > TIMEOFDAY()` 不允许。

## 查看分区设计 {#view-your-partition-design}

分区信息存储在 `pg_partitioned_table` 等系统目录中，以及 `pg_class` 的附加字段（`relispartition`、`relpartbound`）中。

使用以下函数获取分区表信息：

- `pg_partition_tree(regclass)`：列出给定分区表／索引的分区层次结构中的表／索引信息。
- `pg_partition_ancestors(regclass)`：列出给定分区的祖先关系，包括其自身。
- `pg_partition_root(regclass)`：返回给定关系在层次结构中最顶层的父表。

示例：显示 `msales` 的分区结构：

```sql
SELECT * FROM pg_partition_tree('msales');
```

## 分区剪枝概述 {#about-partition-pruning}

分区剪枝是一种提高分区表性能的查询优化技术。它由服务器配置参数 `enable_partition_pruning` 控制，默认值为 `on `。

规划器／优化器检查分区定义，以证明某个分区不可能包含满足查询 `WHERE` 子句的行，因此无需扫描。如果能够证明，就会从查询计划中排除（剪除）该分区。

剪枝由分区键隐式定义的约束驱动，而不取决于键列上是否存在索引。

分区剪枝可以发生在：

- 查询规划期间：适用于已知值。
- 查询执行期间：当子句包含在规划时尚不知其值的表达式（例如 `PREPARE` 中的参数、子查询结果、参数化嵌套循环连接中的值）时很有用。

    - 计划初始化期间：适用于执行初始化阶段已知的参数值。被剪除的分区不会出现在 `EXPLAIN`/`EXPLAIN ANALYZE` 中。`EXPLAIN` 输出中的“Subplans Removed”属性显示在此阶段删除的子计划数。
    - 实际执行期间：适用于仅在运行过程中才知道的值。需要仔细检查 `EXPLAIN ANALYZE` 输出中的 loops 属性。不同分区的子计划可能具有不同的循环次数；如果每次都被剪除，则可能显示为（`never executed`）。

## 维护分区 {#maintain-partitions}

分区集合通常是动态的，需要删除旧分区并添加新分区。通过操作分区结构，几乎可以瞬间完成这些任务。对顶层根分区表或分区本身使用 `ALTER TABLE`。

### 添加分区 {#add-a-partition}

- 直接添加到层次结构中：

    ```sql
    CREATE TABLE msales_mfeb20 PARTITION OF msales
        FOR VALUES FROM ('2020-02-01') TO ('2020-03-01');
    ```

- 先创建为普通表，再挂接（可以预先加载和检查数据）：

    ```sql
    -- Create table with same structure as parent
    CREATE TABLE msales_mfeb20 (LIKE msales INCLUDING DEFAULTS INCLUDING CONSTRAINTS);

    -- Add constraints matching intended partition bounds
    ALTER TABLE msales_mfeb20 ADD CONSTRAINT y2020m02
    CHECK ( logdate >= DATE '2020-02-01' AND logdate < DATE '2020-03-01' );

    -- Load data or perform other prep work into msales_mfeb20
    -- ...

    -- Attach to the partition hierarchy
    ALTER TABLE msales ATTACH PARTITION msales_mfeb20
    FOR VALUES FROM ('2020-02-01') TO ('2020-03-01');
    ```

    - `ATTACH PARTITION` 需要获取分区表上的 `SHARE UPDATE EXCLUSIVE` 锁。
    - 在待挂接的表上创建与分区边界匹配的 `CHECK` 约束（如上所示），可以让系统跳过验证扫描。`ATTACH PARTITION` 完成后，删除这个多余的 `CHECK` 约束。
    - 如果分区表有 `DEFAULT` 分区，可以考虑在 `DEFAULT` 分区上创建 `CHECK` 约束，以排除待挂接分区的数据。这样可以避免扫描 `DEFAULT` 分区来验证是否有记录属于新分区。

### 为分区表创建索引 {#index-partitioned-tables}

在分区表的键列上创建索引时，会自动在每个现有分区上创建匹配的索引；以后创建或挂接的分区也会获得这样的索引。分区表上的索引是“虚拟”的，实际数据位于各个分区的子索引中。

为大型分区层次结构创建索引时，为避免长时间持锁：

- 仅在父表上创建无效索引：

    ```sql
    CREATE INDEX measurement_usls_idx ON ONLY measurement (unitsales);
    ```

- 在各个分区上创建索引：

    ```sql
    CREATE INDEX measurement_usls_202102_idx ON measurement_y2021m02 (unitsales);
    -- ... repeat for other partitions ...
    ```

- 将每个分区的索引挂接到父索引：

    ```sql
    ALTER INDEX measurement_usls_idx ATTACH PARTITION measurement_usls_202102_idx;
    -- ... repeat for other partition indexes ...
    ```

所有分区的索引都挂接完成后，父索引会自动标记为有效。

此方法同样适用于 `UNIQUE` 和 `PRIMARY KEY` 约束（索引会隐式创建）。

```sql
ALTER TABLE ONLY measurement ADD UNIQUE (city_id, logdate);

ALTER TABLE measurement_y2021m02 ADD UNIQUE (city_id, logdate);
ALTER INDEX measurement_city_id_logdate_key
    ATTACH PARTITION measurement_y2021m02_city_id_logdate_key;
-- ...
```

此方法同样适用于 `UNIQUE` 和 `PRIMARY KEY` 约束（索引会隐式创建）。

```sql
ALTER TABLE ONLY measurement ADD UNIQUE (city_id, logdate);

ALTER TABLE measurement_y2021m02 ADD UNIQUE (city_id, logdate);
ALTER INDEX measurement_city_id_logdate_key
    ATTACH PARTITION measurement_y2021m02_city_id_logdate_key;
-- ...
```

### 重命名分区 {#rename-a-partition}

使用 `ALTER TABLE ... RENAME TO` 重命名分区（它也是表）：

```sql
ALTER TABLE msales_mfeb17 RENAME TO msales_month_feb17;
```

## 添加默认分区 {#add-a-default-partition}

`DEFAULT` 分区接收不符合其他任何已定义分区的数据。没有默认分区时，此类数据会导致错误。一个分区表只能有一个默认分区。

1. 创建表时：

    ```sql
    CREATE TABLE msales_other PARTITION OF msales DEFAULT;
    ```

2. 创建表后（将现有表挂接为默认分区）：

    ```sql
    -- Create a table with the same schema as the root
    CREATE TABLE msales_other (LIKE msales);

    -- Attach it as the default partition
    ALTER TABLE msales ATTACH PARTITION msales_other DEFAULT;
    ```

### 删除分区 {#drop-a-partition}

要移除旧数据，可以删除分区。这会快速删除该分区中的所有记录。

```sql
DROP TABLE measurement_y2020m02;
```

此命令需要获取父表上的 `ACCESS EXCLUSIVE` 锁。

### 分离分区 {#detach-a-partition}

将分区从层次结构中移除，但保留为独立的表。

```sql
ALTER TABLE msales DETACH PARTITION msales_2021;
```

分离本身包含子分区的分区时，其子分区也会自动分离。这常用于滚动移出旧数据，可以在删除数据之前进一步执行备份、聚合等操作。

### 截断分区 {#truncate-a-partition}

删除特定分区中的所有数据。

```sql
TRUNCATE ONLY msales_other; -- Truncates only the specified partition
```

如果截断的分区本身也是分区表，其子分区也会被截断。
要截断整个分区表（所有分区）：

```sql
TRUNCATE msales;
```

### 交换分区 {#exchange-a-partition}

用一个表替换现有分区。这需要先分离原分区，再将新表挂接为分区。

- 只能在层次结构的最低层交换分区（包含数据的叶子分区）。
- 不能将分区与复制表、另一个分区表或非叶子子分区进行交换。
- 待挂接表中的数据必须满足目标分区的分区约束。

示例：

```sql
-- Assume msales_2021_new is a table with the correct structure and data for the 2021 partition
ALTER TABLE msales DETACH PARTITION msales_2021;
ALTER TABLE msales ATTACH PARTITION msales_2021_new FOR VALUES FROM (2021) TO (2022);
```
