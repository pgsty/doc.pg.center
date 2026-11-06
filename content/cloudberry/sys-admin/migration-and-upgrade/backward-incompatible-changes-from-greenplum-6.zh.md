---
title: "来自 Greenplum 6.x 的向后不兼容变更"
description: "本页列出了将工作负载从 Greenplum Database 6.x 迁移到 Apache Cloudberry 时可能遇到的向后不兼容（破坏性）变更。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-admin/migration-and-upgrade/backward-incompatible-changes-from-greenplum-6.md"
---

这些差异有两个来源：Cloudberry 底层使用了更新得多的 PostgreSQL 内核，以及对 Greenplum 特有语法、分区和系统目录进行的一系列有意清理。

将本页作为迁移前检查清单，与[迁移与升级](/cloudberry/sys-admin/migration-and-upgrade/migration-and-upgrade/)配合使用；后者介绍使用 `cbcopy` 执行迁移的具体过程。对于下面的每项变更，你都会看到：

- 简要说明变更内容、变更原因以及它可能如何破坏现有工作负载；
- **如何检测**部分，其中包含可在源 Greenplum 6.x 集群上执行的 SQL 或 shell 代码片段，用于查找受影响的对象；
- **如何修复**部分，其中给出建议的修复措施，可在迁移前应用于源集群，也可在迁移后应用于目标 Cloudberry 集群。

变更按以下类别分组：

- **升级阻断项** — 忽略这些变更会阻止迁移或导致数据损坏；应首先处理。
- **函数和运算符行为变更** — 现有内置函数和运算符的语义发生了变化，但语法没有变化，因此查询可能仍能运行，却返回不同结果。
- **语法变更与移除的构造** — 不再接受或需要重写的 SQL 语法。
- **分区机制变更** — 分区表的声明、约束和表示方式发生的差异。
- **系统目录和元数据变更** — 监控工具、脚本和扩展可能依赖的目录表、视图、列和函数被重命名或移除。
- **配置与资源管理变更** — GUC 参数被移除或重命名、默认值不同，以及随附扩展发生变化。

我们建议在迁移窗口前，在源集群的每个数据库上运行每条**如何检测**查询，建立受影响对象清单，并根据上述类别确定修复工作的优先级。

## 升级阻断项 {#upgrade-blockers}

### `jsonb` 类型内部格式的不兼容变更 {#incompatible-change-in-the-internal-format-of-the-jsonb-type}

在高于 9.4 的 PostgreSQL 内核版本中，`jsonb` 类型的内部表示发生了不向后兼容的变化。

**如何检测**

查找所有使用 `jsonb` 的表：

```sql
SELECT n.nspname, c.relname, a.attname
FROM pg_attribute a
    JOIN pg_class c ON c.oid = a.attrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE a.atttypid = 'jsonb'::regtype
    AND a.attnum > 0;
```

**如何修复**

重新创建有问题的列，将 `jsonb` 替换为 `json` 或 `text`。如有必要，请在删除包含 `jsonb` 的列之前迁移数据。

### 移除 `abstime`、`reltime`、`tinterval` 和 `unknown` 类型 {#removal-of-the-abstime-reltime-tinterval-and-unknown-types}

从 PostgreSQL 内核版本 10 开始，`unknown` 类型变成了伪类型。
从 PostgreSQL 内核版本 12 开始，`abstime`、`reltime` 和 `tinterval` 类型被移除。

在 Greenplum 6 中，以下查询可以无错误地执行：

```sql
CREATE TABLE example_abstime (x abstime);

CREATE TABLE example_reltime (x reltime);

CREATE TABLE example_tinterval (x tinterval);

CREATE TABLE example_unknown (x unknown);
WARNING:  column "x" has type "unknown"
```

在 Cloudberry 中，相同查询会因错误而失败：

```sql
CREATE TABLE example_abstime (x abstime);
ERROR:  type "abstime" does not exist

CREATE TABLE example_reltime (x reltime);
ERROR:  type "reltime" does not exist

CREATE TABLE example_tinterval (x tinterval);
ERROR:  type "tinterval" does not exist

CREATE TABLE example_unknown (x unknown);
ERROR:  column "x" has pseudo-type unknown
```

**如何检测**

这些数据类型都已被完全移除，不能再用于：

* SQL 查询；
* 表定义；
* PL/pgSQL 函数。

可以使用以下查询查找使用已移除类型的表：

```sql
SELECT n.nspname, c.relname, a.attname, t.typname
FROM pg_attribute a
    JOIN pg_class c ON c.oid = a.attrelid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_type t ON t.oid = a.atttypid
WHERE t.typname IN ('abstime', 'reltime', 'tinterval', '_abstime', '_reltime', '_tinterval', 'unknown')
    AND a.attnum > 0
    AND NOT a.attisdropped;
```

另外还应单独检查用户定义类型的定义、视图和 PL/pgSQL 函数。

**如何修复**

将每个已弃用类型的用法替换为当前等价类型：

* `abstime` → `timestamp` / `timestamptz`
* `reltime` → `interval`
* `tinterval` → 一对 `timestamp`/`timestamptz` 值，或 `text`
* `unknown` → 根据数据选择最合适的类型，或使用 `text`

### 禁止在角色名中使用 `pg_` 前缀 {#prohibition-on-using-the-pg_-prefix-in-role-names}

从 PostgreSQL 内核版本 9.6 开始，`pg_` 前缀为系统角色和用户名称保留，不再可供使用。

在 Greenplum 6 中，以下查询可以无错误地执行：

```sql
CREATE ROLE pg_example;
```

在 Cloudberry 中，该查询会因错误而失败：

```sql
CREATE ROLE pg_example;
ERROR:  role name "pg_example" is reserved
DETAIL:  Role names starting with "pg_" are reserved.
```

**如何检测**

```sql
SELECT rolname FROM pg_catalog.pg_roles WHERE rolname ~ '^pg_';
```

**如何修复**

```sql
ALTER ROLE pg_example RENAME TO another_example;
```

可以在升级前应用此修复。

### 移除 `tsearch2` 和 `timetravel` 扩展 {#removal-of-the-tsearch2-and-timetravel-extensions}

以下扩展已在 Cloudberry 中完全移除：

* `tsearch2`;
* `timetravel`.

**如何检测**

检查这些扩展是否已安装，以及代码库中是否使用了它们：

```sql
SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('tsearch2', 'timetravel');
```

**如何修复**

停止使用已移除的扩展。

### 已移除对使用 `WITH OIDS` 选项创建的表的支持 {#support-for-tables-created-with-the-with-oids-option-has-been-removed}

在高于 12 的 PostgreSQL 内核版本中，已移除对使用 `WITH OIDS` 选项创建表的支持。

在 Greenplum 6 中，以下查询可以无错误地执行：

```sql
CREATE TABLE example (value text) with oids;
```

在 Cloudberry 中，相同查询会因错误而失败：

```sql
CREATE TABLE example (value text) with oids;
ERROR:  syntax error at or near "oids"
```

**如何检测**

可以使用以下查询查找所有使用 `WITH OIDS` 选项定义的表：

```sql
SELECT n.nspname, c.relname
FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relhasoids
    AND n.nspname NOT IN ('pg_catalog', 'information_schema');
```

**如何修复**

对于找到的每张表，运行 `ALTER TABLE ... SET WITHOUT OIDS;`。如果 OID 被用作业务键，还应添加一个 `bigserial` 列，或添加其他合适的列。

## 函数和运算符行为变更 {#changes-in-function-and-operator-behavior}

### 集合返回函数的行为变更 {#change-in-the-behavior-of-set-returning-functions}

从 PostgreSQL 内核版本 10 开始，`SELECT` 列表中集合返回函数（例如 `generate_series`、`unnest`、`regexp_split_to_table`、`json_each` 和 `json_array_elements`）的行为发生了变化。

下面的示例展示了这种差异。

Greenplum 6：

```sql
SELECT 'example' AS value, generate_series(1, 3), generate_series(1, 2);
  value  | generate_series | generate_series
---------+-----------------+-----------------
 example |               1 |               1
 example |               2 |               2
 example |               3 |               1
 example |               1 |               2
 example |               2 |               1
 example |               3 |               2
(6 rows)
```

Cloudberry：

```sql
SELECT 'example' AS value, generate_series(1, 3), generate_series(1, 2);
  value  | generate_series | generate_series
---------+-----------------+-----------------
 example |               1 |               1
 example |               2 |               2
 example |               3 |
(3 rows)
```

**如何检测**

检查代码库，在 `SELECT` 列表中查找集合返回函数的用法。

**如何修复**

将 `SELECT` 列表中的集合返回函数调用替换为相应的 `CROSS JOIN LATERAL`。

### `extract()` 函数的返回类型已变更为 `numeric` {#the-return-type-of-the-extract-function-has-been-changed-to-numeric}

从 PostgreSQL 内核版本 14 开始，`extract()` 函数返回 `numeric` 类型的值，而不是 `double precision`。

Greenplum 6 示例：

```sql
SELECT pg_typeof(extract(epoch FROM now()));
     pg_typeof
------------------
 double precision
```

Cloudberry 示例：

```sql
SELECT pg_typeof(extract(epoch FROM now()));
 pg_typeof
-----------
  numeric
```

如果应用程序预期得到 `double precision`，其行为可能变得不可预测。

**如何检测**

检查代码库中 `extract()` 函数的用法。

**如何修复**

在应用程序或有问题的查询中添加显式类型转换 `::double precision`。

### `to_number()` 函数的行为已修复，可正确处理格式 {#the-behavior-of-the-to_number-function-has-been-fixed-for-correct-format-handling}

在 Greenplum 6 中，`to_number()` 函数会“吞掉”多余字符：

```sql
SELECT to_number('1234', '9,999');
 to_number
-----------
       134
(1 row)
```

在 Cloudberry 中，此行为已得到修复：

```sql
SELECT to_number('1234', '9,999');
 to_number
-----------
      1234
(1 row)
```

**如何检测**

检查代码库中 `to_number()` 函数的用法，以及“吞掉”多余字符可能造成的问题。

**如何修复**

让应用程序适应 `to_number()` 已改变且正确的行为。

### 部分运算符的求值顺序已变更 {#the-evaluation-order-of-some-operators-has-changed}

与 Greenplum 6 相比，Cloudberry 中 `<=`、`>=`、`<>`、`IS`、`NOT BETWEEN` 及其他复合运算符的求值顺序发生了变化。

例如，在 Greenplum 6 中，以下查询无效：

```sql
SELECT 1 <> 2 IS TRUE;
ERROR:  argument of IS TRUE must be type boolean, not type integer
```

但在 Cloudberry 中，该查询可以运行：

```sql
SELECT 1 <> 2 IS TRUE;
?column?
----------
t
(1 row)
```

**如何检测**

检查代码库中求值顺序不明确的表达式。

**如何修复**

使用括号明确指定运算符的求值顺序。

### `SIMILAR TO` 与 `ESCAPE NULL` 的行为已变更 {#behavior-of-similar-to-with-escape-null-has-changed}

从 PostgreSQL 内核版本 13 开始，`SIMILAR TO ... ESCAPE NULL` 构造的行为发生了变化。

Greenplum 6 示例：

```sql
SELECT 'abc' SIMILAR TO 'abc' ESCAPE NULL;
?column?
----------
t
(1 row)
```

Cloudberry 示例：

```sql
SELECT 'abc' SIMILAR TO 'abc' ESCAPE NULL;
?column?
----------

(1 row)
```

**如何检测**

检查代码库中 `ESCAPE NULL` 构造的用法。

**如何修复**

将 `ESCAPE NULL` 替换为 `ESCAPE <some value>`。

## 语法变更与移除的构造 {#syntax-changes-and-removed-constructs}

### 带行构造器的 `UPDATE` 语句必须显式写出 `ROW()` {#explicit-row-is-required-in-update-statements-with-row-constructors}

从 PostgreSQL 内核版本 10 开始，通过 `ROW` 构造器更新单列时，必须显式指定 `ROW` 关键字。

在 Greenplum 6 中，以下查询可以无错误地执行：

```sql
CREATE TABLE example (value text);

INSERT INTO example (value) VALUES ('a');

-- this query
UPDATE example SET (value) = (value || '_updated');
```

在 Cloudberry 中，相同查询会因错误而失败：

```sql
CREATE TABLE example (value text);

INSERT INTO example (value) VALUES ('a');

-- this query
UPDATE example SET (value) = (value || '_updated');
ERROR:  source for a multiple-column UPDATE item must be a sub-SELECT or ROW() expression
```

**如何检测**

检查代码库中对单列使用 `ROW` 构造器的情况。

**如何修复**

修改有问题的查询，使其不使用 `ROW` 构造器（例如 `UPDATE ... SET col = expr`），或显式指定 `ROW` 关键字：`UPDATE ... SET (col) = ROW(expr)`。

### 不支持语句级触发器 {#statement-level-triggers-are-not-supported}

与 Greenplum 6 不同，Cloudberry 不支持语句级触发器。

以下查询在 Greenplum 6 中可以正常执行：

```sql
CREATE TABLE example (
    id bigserial,
    value text
) DISTRIBUTED BY (id);

CREATE OR REPLACE FUNCTION example_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER example_trigger
    AFTER INSERT OR UPDATE ON example
    FOR EACH STATEMENT
    EXECUTE PROCEDURE example_trigger_func();
```

但这些查询在 Cloudberry 中无法执行：

```sql
CREATE TABLE example (
    id bigserial,
    value text
) DISTRIBUTED BY (id);

CREATE OR REPLACE FUNCTION example_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER example_trigger
    AFTER INSERT OR UPDATE ON example
    FOR EACH STATEMENT
    EXECUTE PROCEDURE example_trigger_func();

ERROR:  Triggers for statements are not yet supported
```

**如何检测**

可以使用以下查询查找所有语句级触发器：

```sql
SELECT n.nspname, c.relname, tgname
FROM pg_trigger t
    JOIN pg_class c ON t.tgrelid = c.oid
    JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE tgtype & 1 = 0 AND NOT tgisinternal;
```

**如何修复**

停止使用语句级触发器：将相关逻辑移到应用程序侧，或使用行级触发器。

### 带 `EXECUTE ON` 的函数必须返回集合（`SETOF`） {#functions-with-execute-on-must-return-sets-setof}

在 Cloudberry 中，带有 `EXECUTE ON ALL SEGMENTS` / `COORDINATOR` / `INITPLAN` 属性的函数现在必须返回 `SETOF`。

Greenplum 6 中的有效示例：

```sql
CREATE OR REPLACE FUNCTION example_func()
RETURNS integer
AS $$
BEGIN
    RETURN 42;
END;
$$ LANGUAGE plpgsql
EXECUTE ON ALL SEGMENTS;
```

以下用法在 Cloudberry 中不再有效：

```sql
CREATE OR REPLACE FUNCTION example_func()
RETURNS integer
AS $$
BEGIN
    RETURN 42;
END;
$$ LANGUAGE plpgsql
EXECUTE ON ALL SEGMENTS;

ERROR:  EXECUTE ON ALL SEGMENTS is only supported for set-returning functions
```

**如何检测**

可以使用以下查询查找带有 `EXECUTE ON ALL SEGMENTS` / `COORDINATOR` / `INITPLAN` 属性但不返回 `SETOF` 的函数：

```sql
SELECT n.nspname, p.proname
FROM pg_proc p
    JOIN pg_language l ON l.oid = p.prolang
    JOIN pg_type t ON t.oid = p.prorettype
    JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE NOT proretset
    AND proexeclocation IN ('s', 'm', 'i')
    AND l.lanname NOT IN ('internal')
    AND t.typname NOT IN ('record');
```

**如何修复**

使用 `RETURNS SETOF ...` 和 `RETURN NEXT` 重新创建有问题的函数。

### 已移除对后缀运算符的支持 {#support-for-postfix-operators-has-been-removed}

从 PostgreSQL 内核版本 14 开始，系统定义和用户定义的后缀运算符均不再受支持。

在 Greenplum 6 中，以下查询可以无错误地执行：

```sql
SELECT 5! AS factorial;
 factorial
-----------
       120
```

在 Cloudberry 中，相同查询会因错误而失败：

```sql
SELECT 5! AS factorial;
ERROR:  syntax error at or near "AS"
LINE 1: SELECT 5! AS factorial;
```

**如何检测**

在 Greenplum 6 中，只有一个系统后缀运算符：`!`。不过，也可能存在用户定义运算符。可以使用以下查询获取后缀运算符的完整列表：

```sql
SELECT o.oid, n.nspname, o.oprname, o.oid < 16384 AS is_system
FROM pg_operator o
    JOIN pg_namespace n ON o.oprnamespace = n.oid
WHERE o.oprright = 0;
```

**如何修复**

* 将 `!` 运算符的用法替换为显式调用 `factorial(...)` 函数。
* 将用户定义的后缀运算符替换为前缀运算符，或显式调用相应函数。

## 分区机制变更 {#changes-in-partitioning-mechanisms}

### 唯一索引必须包含所有分区键 {#requirement-to-include-all-partition-keys-in-unique-indexes}

与 Greenplum 6 不同，Cloudberry 中的唯一索引必须包含**所有**分区键。

在 Greenplum 6 中可以运行的查询示例：

```sql
CREATE TABLE sales (
    id int NOT NULL,
    region text,
    amount decimal(10, 2)
)
    DISTRIBUTED BY (id)
    PARTITION BY LIST (region)
    (
        VALUES ('Asia'),
        VALUES ('Europe')
    );

INSERT INTO sales (id, region, amount)
VALUES
    (1, 'Asia', 100.00),
    (1, 'Europe', 150.00),
    (2, 'Asia', 200.00);

CREATE UNIQUE INDEX sales_id_idx ON sales (id);
```

相同查询在 Cloudberry 中无法运行：

```sql
CREATE TABLE sales (
    id int NOT NULL,
    region text,
    amount decimal(10, 2)
)
    DISTRIBUTED BY (id)
    PARTITION BY LIST (region)
    (
        VALUES ('Asia'),
        VALUES ('Europe')
    );

INSERT INTO sales (id, region, amount)
VALUES
    (1, 'Asia', 100.00),
    (1, 'Europe', 150.00),
    (2, 'Asia', 200.00);

CREATE UNIQUE INDEX sales_id_idx ON sales (id);
ERROR:  unique constraint on partitioned table must include all partitioning columns
DETAIL:  UNIQUE constraint on table "sales" lacks column "region" which is part of the partition key.
```

**如何检测**

可以使用以下查询查找未包含**所有**分区键的唯一索引：

```sql
WITH partitions AS (
SELECT DISTINCT n.nspname, c.relname, c.oid, p.paratts
FROM pg_partition p
    JOIN pg_class c ON p.parrelid = c.oid
    JOIN pg_namespace n ON n.oid = c.relnamespace
)
SELECT p.nspname, p.relname, ir.relname AS indexname
FROM pg_index i
    JOIN partitions p ON p.oid = i.indrelid
    JOIN pg_class ir ON ir.oid = i.indexrelid
WHERE (i.indisunique OR i.indisprimary)
    AND NOT (p.paratts <@ i.indkey);
```

**如何修复**

重新创建找到的索引，并添加分区键。

### 按多列进行列表分区的限制 {#limitation-on-list-partitioning-by-multiple-columns}

在 Cloudberry 中，按多列进行列表分区是通过子分区实现的：标准 Cloudberry 语法假设每个层级只有一列或一个表达式。

此限制与以下事实有关：按多列进行列表分区（例如 `PARTITION BY LIST (col1, col2)`）通常会使 GPORCA 优化器无法使用。

以下示例在 Greenplum 6 中可以运行：

```sql
CREATE TABLE example (a int, b int, c int)
    PARTITION BY LIST (b, c)
    (
        DEFAULT PARTITION other
    );
```

但在 Cloudberry 中无法运行：

```sql
CREATE TABLE example (a int, b int, c int)
    PARTITION BY LIST (b, c)
    (
        DEFAULT PARTITION other
    );
ERROR:  cannot use "list" partition strategy with more than one column
```

**如何检测**

可以使用以下查询查找按多列进行列表分区的表：

```sql
SELECT n.nspname, c.relname
FROM pg_partition p
    JOIN pg_class c ON p.parrelid = c.oid
    JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE parkind = 'l'
    AND parnatts > 1;
```

**如何修复**

在 Cloudberry 中，应使用子分区来实现这一点：

```sql
CREATE TABLE example (a int, b int, c int)
PARTITION BY LIST (b)
    SUBPARTITION BY LIST (c)
    SUBPARTITION TEMPLATE (
        DEFAULT SUBPARTITION other_c
    )
    (
        DEFAULT PARTITION other
    );
```

### 已移除对分区 DDL 中 `FOR (RANK(...))` 的支持 {#support-for-for-rank-in-partition-ddl-has-been-removed}

Cloudberry 不支持在处理分区时使用 `FOR (RANK(...))` 构造。

Greenplum 6 中的可运行示例：

```sql
CREATE TABLE sales (
    id int,
    date date,
    amount decimal(10, 2)
)
WITH (appendoptimized = true, compresstype = zstd, compresslevel = 1)
DISTRIBUTED BY (id)
PARTITION BY RANGE (date) (
    START ('2026-01-01') END ('2027-01-01') EVERY (INTERVAL '1 month')
);

ALTER TABLE sales
    ALTER PARTITION FOR (RANK(2))
    TRUNCATE PARTITION FOR (RANK(2));
```

在 Cloudberry 中无法运行：

```sql
CREATE TABLE sales (
    id int,
    date date,
    amount decimal(10, 2)
)
WITH (appendoptimized = true, compresstype = zstd, compresslevel = 1)
DISTRIBUTED BY (id)
PARTITION BY RANGE (date) (
    START ('2026-01-01') END ('2027-01-01') EVERY (INTERVAL '1 month')
);

ALTER TABLE sales
    ALTER PARTITION FOR (RANK(2))
    TRUNCATE PARTITION FOR (RANK(2));
ERROR:  addressing partition by RANK is no longer supported
HINT:  Use partition name or FOR (<partition key value>) instead.
```

**如何检测**

检查代码库和脚本中 `FOR (RANK(...))` 构造的用法。

**如何修复**

将 `FOR (RANK(...))` 替换为 `FOR (VALUE ...)` 或 `FOR VALUES`。

### AO 表存储参数的继承方式已变更 {#inheritance-of-storage-parameters-for-ao-tables-has-changed}

如果没有为某个分区显式指定 AO 参数，则行为会有所不同：

* 在 Greenplum 6 中，应用默认值；
* 在 Cloudberry 中，从父表继承该参数。

以下查询在 Greenplum 6 中可以运行：

```sql
CREATE TABLE sales
(
    id int,
    date date,
    region text,
    amount decimal(10, 2)
)
    WITH (appendoptimized = true, compresstype = zstd, compresslevel = 1)
    DISTRIBUTED BY (id)
    PARTITION BY LIST (region)
        (
        PARTITION asia VALUES ('Asia')
            WITH (appendoptimized = true, compresslevel = 0),
        PARTITION europe VALUES ('Europe')
        );
```

但在 Cloudberry 中无法运行：

```sql
CREATE TABLE sales
(
    id int,
    date date,
    region text,
    amount decimal(10, 2)
)
    WITH (appendoptimized = true, compresstype = zstd, compresslevel = 1)
    DISTRIBUTED BY (id)
    PARTITION BY LIST (region)
        (
        PARTITION asia VALUES ('Asia')
            WITH (appendoptimized = true, compresslevel = 0),
        PARTITION europe VALUES ('Europe')
        );
ERROR:  compresstype "zstd" can't be used with compresslevel 0
```

**如何检测**

可以使用以下查询查找未显式指定选项创建的分区：

```sql
SELECT
    schemaname,
    tablename,
    partitionschemaname,
    partitiontablename,
    par.reloptions AS parent_options,
    c.reloptions AS child_options,
    po AS parent_option
FROM pg_partitions p
    JOIN pg_class par ON par.oid = format('%s.%s', schemaname, tablename)::regclass
    JOIN pg_class c ON c.oid = format('%s.%s', partitionschemaname, partitiontablename)::regclass
    JOIN unnest(par.reloptions) po ON TRUE
    LEFT JOIN unnest(c.reloptions) co ON split_part(po, '=', 1) = split_part(co, '=', 1)
WHERE co IS NULL;
```

**如何修复**

为有问题的分区创建一个明确指定选项的副本，将数据移入其中，然后用更新后的分区替换原分区。

### `float` / `numeric` / `text` 类型对 `EXCLUSIVE` / `INCLUSIVE` 边界的限制 {#limitations-on-exclusive--inclusive-boundaries-for-float--numeric--text-types}

与 Greenplum 6 不同，在 Cloudberry 中，`START EXCLUSIVE` / `END INCLUSIVE` 构造仅适用于带有 `+` 运算符的类型（例如 `integer` 和 `timestamp`），不适用于 `float`、`numeric` 或 `text`。

Greenplum 6 中的正确示例：

```sql
CREATE TABLE sales
(
    id int,
    date date,
    amount decimal(10, 2)
)
    WITH (appendoptimized = true)
    DISTRIBUTED BY (id)
    PARTITION BY RANGE (amount)
        (
        START (0) EXCLUSIVE
            END (1000)
            EVERY (250)
        );
```

在 Cloudberry 中无法运行：

```sql
CREATE TABLE sales
(
    id int,
    date date,
    amount decimal(10, 2)
)
    WITH (appendoptimized = true)
    DISTRIBUTED BY (id)
    PARTITION BY RANGE (amount)
        (
        START (0) EXCLUSIVE
            END (1000)
            EVERY (250)
        );
ERROR:  START EXCLUSIVE not supported for partition key data type: numeric
HINT:  Specify an inclusive START value and remove the EXCLUSIVE keyword
```

**如何检测**

可以使用以下查询查找在不支持的类型上使用 `START EXCLUSIVE` / `END INCLUSIVE` 的表：

```sql
SELECT n.nspname, c.relname, t.typname, pr.parchildrelid::regclass
FROM pg_partition p
    JOIN pg_partition_rule pr ON p.oid = pr.paroid
    JOIN pg_class c ON p.parrelid = c.oid
    JOIN pg_namespace n ON n.oid = c.relnamespace
    JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(p.paratts)
    JOIN pg_type t ON t.oid = a.atttypid
WHERE t.typname IN ('text', 'float8', 'float4', 'numeric')
    AND (NOT pr.parrangestartincl OR pr.parrangeendincl);
```

**如何修复**

重新创建这些有问题的表，并在这些类型上移除 `EXCLUSIVE` / `INCLUSIVE`。

### 分区表的层级系统已变更 {#the-level-system-for-partitioned-tables-has-changed}

在 Greenplum 6 中，直接子分区的 `pg_partition.parlevel = 0`。在 Cloudberry 中，直接子分区的 `pg_partition_tree().level = 1`。Cloudberry 已移除 `pg_partition` 视图，因此应改用 `pg_partition_tree()` 函数。

此变更可能会破坏依赖分区层级的查询。

**如何检测**

检查代码库和脚本中对分区层级的使用。

**如何修复**

调整应用程序代码库和脚本，使其适应分区层级的变化以及 `pg_partition` 视图的移除。使用 `pg_partition_tree()` 函数或 `pg_partitioned_table` 视图替代 `pg_partition`。

### 分区约束已从 `pg_constraint` 移出 {#partition-constraints-have-been-moved-out-of-pg_constraint}

在 Greenplum 6 中，分区边界在 `pg_constraint` 系统视图中显示为 `CHECK CONSTRAINT` 条目。

在 Cloudberry 中，分区边界不再是 `CHECK CONSTRAINT` 条目，也不会显示在 `pg_constraint` 中。现在可以从 `gp_toolkit.gp_partitions` 获取类似信息。

**如何检测**

检查代码库和脚本中使用 `pg_constraint` 处理分区约束的情况。

**如何修复**

使用 `gp_toolkit.gp_partitions` 视图替代 `pg_constraint` 来处理分区约束。

## 系统目录和元数据变更 {#changes-in-the-system-catalog-and-metadata}

### 系统目录视图和表中已移除及重命名的列 {#removed-and-renamed-columns-in-system-catalog-views-and-tables}

迁移到 Cloudberry 时，随着 PostgreSQL 内核和 Greenplum 6 的升级，系统目录视图和表中的以下列被移除或重命名：

| 旧列                                                                  | 新列                                                           |
|-----------------------------------------------------------------------------|----------------------------------------------------------------------|
| `pg_class.relhasoids`                                                       | 已移除                                                              |
| `pg_class.relhaspkey`                                                       | `EXISTS (SELECT FROM pg_index WHERE indrelid=... AND indisprimary)`  |
| `pg_class.relstorage`                                                       | `pg_class.relam`                                                     |
| `pg_proc.proisagg`                                                          | `pg_proc.prokind = 'a'`                                              |
| `pg_proc.proiswindow`                                                        | `pg_proc.prokind = 'w'`                                              |
| `pg_proc.protransform`                                                      | `pg_proc.prosupport`                                                 |
| `pg_attrdef.adsrc`                                                          | `pg_get_expr(adbin, adrelid)`                                        |
| `pg_constraint.consrc`                                                       | `pg_get_constraintdef(oid)`                                          |
| `pg_stat_activity.waiting`                                                  | `wait_event_type`、`wait_event`                                      |
| `pg_am.*` — 数十个列                                               | 访问方法 API 已经过重大重构。没有简单的替代方案。 |
| `gp_distributed_log.distributed_id`、`gp_distributed_xacts.distributed_id`  | 已移除                                                              |
| `gp_stat_replication.*_location`                                            | 重命名为 `*_lsn`                                                   |
| `information_schema.routines.result_cast_character_set_name`                | 重命名为 `result_cast_char_set_name`                               |

**如何检测**

检查代码库中使用已移除或重命名列的情况。

**如何修复**

在代码库中进行相应修改。

### 移除系统表和视图 {#removal-of-system-tables-and-views}

与 Greenplum 6 相比，Cloudberry 已完全移除以下系统表和视图：

* `pg_catalog.pg_partition`;
* `pg_catalog.pg_partition_columns`;
* `pg_catalog.pg_partition_encoding`;
* `pg_catalog.pg_partition_rule`;
* `pg_catalog.pg_partitions`;
* `pg_catalog.pg_partition_templates`;
* `pg_catalog.pg_stat_partition_operations`.

**如何检测**

检查代码库中使用已移除系统表和视图的情况。

**如何修复**

在代码库中进行相应修改。

要在 Cloudberry 中处理分区表，请使用 `pg_partitioned_table` 视图和 `pg_partition_tree()`、`pg_partition_ancestors()` 以及 `pg_partition_root()` 函数。

### 移除和重命名系统函数 {#removal-and-renaming-of-system-functions}

与 Greenplum 6 相比，Cloudberry 已完全移除以下系统函数：

* `pg_get_partition_def`, `pg_get_partition_rule_def`, `pg_get_partition_template_def`;
* `gp_elog`, `gp_fault_inject`, `gp_update_ao_master_stats`.

`pg_*_xlog*` 系列中的函数已按照 `pg_*_wal*` 模式重命名，例如 `pg_switch_xlog()` → `pg_switch_wal()`。
有些函数已被移除。

**如何检测**

检查代码库中使用已移除和重命名系统函数的情况。

**如何修复**

在代码库中进行相应修改。

### 序列元数据的显示方式已变更 {#changes-in-how-sequence-metadata-is-displayed}

从 PostgreSQL 内核版本 10 开始，序列元数据的显示方式发生了变化。
现在，`SELECT * FROM <seq_name>` 形式的查询只返回 `last_value`、`log_cnt` 和 `is_called`。其他属性可通过 `pg_sequence` 或 `pg_sequences` 获取。

Greenplum 6 示例：

```sql
CREATE SEQUENCE example_seq
    START WITH 100
    INCREMENT BY 1;

SELECT * FROM example_seq;
 sequence_name    | last_value | start_value | increment_by |      max_value      | min_value | cache_value | log_cnt | is_cycled | is_called
------------------+------------+-------------+--------------+---------------------+-----------+-------------+---------+-----------+-----------
 example_seq      |        100 |         100 |            1 | 9223372036854775807 |         1 |           1 |       0 | f         | f
```

Cloudberry 示例：

```sql
CREATE SEQUENCE example_seq
    START WITH 100
    INCREMENT BY 1;

SELECT * FROM example_seq;
 last_value | log_cnt | is_called
------------+---------+-----------
        100 |       0 | f

SELECT * FROM pg_sequence WHERE seqrelid = 'example_seq'::regclass;
 seqrelid | seqtypid | seqstart | seqincrement |       seqmax        | seqmin | seqcache | seqcycle
----------+----------+----------+--------------+---------------------+--------+----------+----------
    17186 |       20 |      100 |            1 | 9223372036854775807 |      1 |       20 | f

SELECT * FROM pg_sequences WHERE sequencename = 'example_seq';
 schemaname | sequencename    | sequenceowner | data_type | start_value | min_value |      max_value      | increment_by | cycle | cache_size | last_value
------------+-----------------+---------------+-----------+-------------+-----------+---------------------+--------------+-------+------------+------------
 public     | example_seq     | user1         | bigint    |         100 |         1 | 9223372036854775807 |            1 | f     |         20 |
```

**如何检测**

检查代码库中形如 `SELECT * FROM <seq_name>` 的查询，确认是否使用了 `last_value`、`log_cnt` 和 `is_called` 以外的字段。

**如何修复**

通过查询 `pg_sequence` 或 `pg_sequences` 在代码库中进行相应修改。

### 外部表内部表示的变更 {#change-in-the-internal-representation-of-external-tables}

在 Cloudberry 内部，外部表以外表（FDW）表示。与 Greenplum 6 相比，这会产生以下差异：

* `pg_tables` 系统视图不再显示外部表。
* 外部表的 `pg_class.relkind` 现在为 `'f'`，而不是 `'r'`。
* `pg_exttable` 系统表已变为视图。
* `EXPLAIN` 输出已发生变化：显示 `Foreign Scan`，而不是 `External Scan`。

**如何检测**

检查代码库和脚本中对外部表元数据的引用。

可以使用以下查询获取外部表列表：

```sql
SELECT n.nspname, c.relname, c.relkind, e.urilocation, e.execlocation, e.fmttype, e.fmtopts
FROM pg_exttable e
    JOIN pg_class c ON c.oid = e.reloid
    JOIN pg_namespace n ON n.oid = c.relnamespace;
```

**如何修复**

根据这些变化修改代码库和脚本。

### `gp_toolkit` 模式现在作为扩展提供 {#the-gp_toolkit-schema-is-now-provided-as-an-extension}

与 Greenplum 6 不同，Cloudberry 将 `gp_toolkit` 作为扩展提供。
从安装角度看，没有任何变化：创建数据库时会自动连接 `gp_toolkit`。

以下视图已被移除：

* `gp_toolkit.gp_size_of_partition_and_indexes_disk`;
* `gp_toolkit.__gp_user_data_tables`.

以下现有函数的签名发生了变化：

* `gp_toolkit.__gp_aoseg*`;
* `gp_toolkit.__gp_aocsseg*`;
* `gp_dist_wait_status`;
* `gp_execution_segment`;
* `gp_request_fts_probe_scan`;
* `gp_tablespace_segment_location`.

以下列已从现有视图中移除：

* `gp_toolkit.gp_locks_on_resqueue.lorwaiting`;
* `gp_toolkit.gp_resgroup_config.cpu_rate_limit`;
* `gp_toolkit.gp_resgroup_config.memory_auditor`;
* `gp_toolkit.gp_resgroup_config.memory_shared_quota`;
* `gp_toolkit.gp_resgroup_config.memory_spill_ratio`;
* `gp_toolkit.gp_resgroup_status.cpu_usage`;
* `gp_toolkit.gp_resgroup_status.memory_usage`;
* `gp_toolkit.gp_resgroup_status_per_host.cpu`;
* `gp_toolkit.gp_resgroup_status_per_host.memory_available`;
* `gp_toolkit.gp_resgroup_status_per_host.memory_quota_available`;
* `gp_toolkit.gp_resgroup_status_per_host.memory_quota_used`;
* `gp_toolkit.gp_resgroup_status_per_host.memory_shared_available`;
* `gp_toolkit.gp_resgroup_status_per_host.memory_shared_used`;
* `gp_toolkit.gp_resgroup_status_per_host.memory_used`;
* `gp_toolkit.gp_resgroup_status_per_host.rsgname`;
* `gp_toolkit.gp_resgroup_status_per_segment.cpu`;
* `gp_toolkit.gp_resgroup_status_per_segment.hostname`;
* `gp_toolkit.gp_resgroup_status_per_segment.memory_available`;
* `gp_toolkit.gp_resgroup_status_per_segment.memory_quota_available`;
* `gp_toolkit.gp_resgroup_status_per_segment.memory_quota_used`;
* `gp_toolkit.gp_resgroup_status_per_segment.memory_shared_available`;
* `gp_toolkit.gp_resgroup_status_per_segment.memory_shared_used`;
* `gp_toolkit.gp_resgroup_status_per_segment.memory_used`;
* `gp_toolkit.gp_resgroup_status_per_segment.rsgname`;
* `gp_toolkit.gp_resgroup_status.rsgname`;
* `gp_toolkit.__gp_user_tables.autrelstorage`.

**如何检测**

检查代码库和脚本中使用已变更或已移除对象的情况。

**如何修复**

调整代码库和脚本：停止使用已移除的对象，并适应现有对象的变化。

## 配置与资源管理变更 {#changes-in-configuration-and-resource-management}

### 移除配置参数 {#removal-of-configuration-parameters}

与 Greenplum 6 相比，Cloudberry 已完全移除以下配置参数：

* `wal_keep_segments` — 重命名为 `wal_keep_size`；
* `memory_spill_ratio`;
* `gp_resource_group_memory_limit`;
* `gp_resource_group_enable_recalculate_query_mem`;
* `gp_resource_group_cpu_ceiling_enforcement`;
* `gp_enable_gpperfmon`;
* `gp_gpperfmon_send_interval`;
* `gpperfmon_log_alert_level`;
* `gpperfmon_port`;
* `gp_log_resqueue_priority_sleep_time`;
* `dev_opt_unsafe_truncate_in_subtransaction`;
* `gp_add_column_inherits_table_setting`;
* `gp_allow_rename_relation_without_lock`;
* `gp_count_host_segments_using_address`;
* `gp_eager_agg_distinct_pruning`;
* `gp_eager_one_phase_agg`;
* `gp_eager_preunique`;
* `gp_enable_exchange_default_partition`;
* `gp_enable_mk_sort`;
* `gp_enable_motion_mk_sort`;
* `gp_enable_sort_distinct`;
* `gp_ignore_window_exclude`;
* `gp_indexcheck_vacuum`;
* `gp_partitioning_dynamic_selection_log`;
* `gp_safefswritesize`;
* `gp_use_synchronize_seqscans_catalog_vacuum_full`;
* `optimizer_analyze_enable_merge_of_leaf_stats`;
* `optimizer_enable_dml_triggers`;
* `optimizer_enable_partial_index`;
* `optimizer_prune_unused_columns`.

**如何检测**

检查代码库中是否使用了所列配置参数。

**如何修复**

在代码库中移除对已删除配置参数的使用，进行相应修改。

### `password_encryption` 参数的可能值已变更 {#change-in-possible-values-of-the-password_encryption-parameter}

从 PostgreSQL 内核版本 10 开始，`password_encryption` 参数的类型和可能值发生了变化。

在 Greenplum 6 中，该参数具有以下类型和可能值：

```sql
SELECT vartype, enumvals FROM pg_settings WHERE name = 'password_encryption';
 vartype | enumvals
---------+----------
 bool    |
(1 row)
```

在 Cloudberry 中，该参数具有以下类型和可能值：

```sql
SELECT vartype, enumvals FROM pg_settings WHERE name = 'password_encryption';
 vartype |      enumvals
---------+---------------------
 enum    | {md5,scram-sha-256}
(1 row)
```

**如何检测**

检查代码库中 `password_encryption` 参数的用法，并考虑这些变化。

**如何修复**

在使用 `password_encryption` 参数的所有位置，将值替换为 `md5`。也允许使用 `scram-sha-256`，但在当前服务版本中存在支持限制。

只能在升级后应用此修复。

### 默认参数值已变更 {#changes-in-default-parameter-values}

与 Greenplum 6 相比，Cloudberry 中以下参数的默认值发生了变化：

| 参数                         | Greenplum 6 | Cloudberry |
|--------------------------------|------------:|-----------:|
| `wal_level`                    | `archive`  | `replica`  |
| `autovacuum_vacuum_cost_delay` | `20ms`     | `2ms`      |
| `checkpoint_completion_target` | 0.5        | 0.9        |
| `extra_float_digits`           | 0          | 1          |
| `gp_interconnect_address_type` | `wildcard` | `unicast`  |
| `autovacuum`                   | `off`      | `template0` 为 `on` |
| `optimizer_enable_orderedagg`  | `off`      | `on`       |
| `vacuum_cost_page_miss`        | 10         | 2          |

**如何检测**

其中大多数参数是系统级参数，只会间接影响运行。`extra_float_digits` 比较特殊，因为它可能影响查询结果。

**如何修复**

在观察到新 `extra_float_digits` 值影响的地方，显式地在会话级或事务级设置 `extra_float_digits = 0`。

### 查询执行计划可能发生变化 {#possible-changes-in-query-execution-plans}

Cloudberry 在 GPORCA 优化器中包含许多变更和改进，可能会改变查询执行计划。查询的逻辑不会因此“出错”，但其执行方式可能发生变化。

需要考虑以下事项：

* 出现了影响查询计划构建的新参数：

    * `enable_partitionwise_aggregate`;
    * `enable_partitionwise_join`;
    * `enable_parallel`;
    * `enable_parallel_dedup_semi_join`;
    * `enable_parallel_hash`;
    * `enable_parallel_append`;
    * `enable_parallel_dedup_semi_reverse_join`;
    * `enable_parallel_semi_join`;
    * `jit`;
    * `jit_above_cost`;
    * `jit_dump_bitcode`;
    * `jit_expressions`;
    * `jit_inline_above_cost`;
    * `jit_optimize_above_cost`;
    * `jit_tuple_deforming`.

* GPORCA 不支持多级分区表。

**如何检测**

在迁移到 Cloudberry 前，捕获关键查询的基准计划：

```sql
EXPLAIN (ANALYZE, VERBOSE, COSTS, BUFFERS) <query>;
```

**如何修复**

根据计划变更的性质及其重要性，重写有问题的查询或调整参数。

### 已合并到内核的扩展 {#extensions-merged-into-the-core}

在 Cloudberry 中，以下扩展已被移除，其功能已移入内核：

* `gp_parallel_retrieve_cursor`;
* `gp_array_agg`;
* `gp_percentile_agg`.

**如何检测**

检查这些扩展是否已安装，以及代码库中是否使用了它们：

```sql
SELECT extname, extversion
FROM pg_extension
WHERE extname IN ('gp_parallel_retrieve_cursor', 'gp_array_agg', 'gp_percentile_agg');
```

**如何修复**

如有必要，调整代码库和脚本，使用内置功能。
