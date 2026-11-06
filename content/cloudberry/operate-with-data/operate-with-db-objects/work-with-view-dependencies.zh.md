---
title: "使用视图依赖"
description: "如果表上存在视图依赖，则必须使用 `CASCADE` 关键字删除该表。"
weight: 70
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/operate-with-db-objects/work-with-view-dependencies.md"
---

此外，如果表上存在视图依赖，也不能修改该表。以下示例展示了表上的视图依赖。

```sql
CREATE TABLE t (id integer PRIMARY KEY);
CREATE VIEW v AS SELECT * FROM t;
 
DROP TABLE t;
ERROR:  cannot drop table t because other objects depend on it
DETAIL:  view v depends on table t
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
 
ALTER TABLE t DROP id;
ERROR:  cannot drop column id of table t because other objects depend on it
DETAIL:  view v depends on column id of table t
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
```

如前面的示例所示，如果视图存在很深的层次结构，修改表可能会相当棘手，因为必须按正确顺序创建视图。除非视图所需的所有对象都已存在，否则不能创建视图。

需要修改被视图引用的表时，可以使用视图依赖信息。例如，可能需要将表列的数据类型从 `integer` 改为 `bigint`，因为发现需要存储更大的数字。但是，如果有视图使用该列，就不能这样做。必须先删除这些视图，然后修改列，最后重新运行所有 `CREATE VIEW` 语句来重新创建视图。

## 查找视图依赖 {#find-view-dependencies}

以下示例查询列出表和列上的视图依赖信息。

- [查找表上的直接视图依赖](#find-direct-view-dependencies-on-a-table)
- [查找表列上的直接依赖](#find-direct-dependencies-on-a-table-column)
- [列出视图模式](#list-view-schemas)
- [列出视图定义](#list-view-definitions)
- [列出嵌套视图](#list-nested-views)

示例输出基于本主题末尾的[示例数据](#example-data)。

还可以使用第一个示例查询[查找表上的直接视图依赖](#find-direct-view-dependencies-on-a-table)来查找对用户定义函数（或过程）的依赖。该查询使用包含表和视图信息的 `pg_class` 目录表。对于函数，可以使用 `pg_proc` 目录表获取函数信息。

有关存储视图信息的系统目录表的详细信息，请参见[Apache Cloudberry 中的视图存储概述](/cloudberry/operate-with-data/operate-with-db-objects/view-storage/)。

### 查找表上的直接视图依赖 {#find-direct-view-dependencies-on-a-table}

要查找直接依赖表 `t1` 的视图，请创建一个查询，在包含依赖信息的目录表之间执行连接，并限定查询只返回视图依赖。

```sql
SELECT v.oid::regclass AS view,
  d.refobjid::regclass AS ref_object    -- name of table
  -- d.refobjid::regproc AS ref_object  -- name of function
FROM pg_depend AS d      -- objects that depend on a table
  JOIN pg_rewrite AS r  -- rules depending on a table
     ON r.oid = d.objid
  JOIN pg_class AS v    -- views for the rules
     ON v.oid = r.ev_class
WHERE v.relkind = 'v'         -- filter views only
  -- dependency must be a rule depending on a relation
  AND d.classid = 'pg_rewrite'::regclass 
  AND d.deptype = 'n'         -- normal dependency
  -- qualify object
  AND d.refclassid = 'pg_class'::regclass   -- dependent table
  AND d.refobjid = 't1'::regclass
  -- AND d.refclassid = 'pg_proc'::regclass -- dependent function
  -- AND d.refobjid = 'f'::regproc
;
    view    | ref_object
------------+------------
 v1         | t1
 v2         | t1
 v2         | t1
 v3         | t1
 mytest.vt1 | t1
 mytest.v2a | t1
 mytest.v2a | t1
(7 rows)
```

该查询将值转换为 `regclass` 对象标识符类型。有关对象标识符类型的信息，请参见 PostgreSQL 文档中的[对象标识符类型](https://www.postgresql.org/docs/14/datatype-oid.html)。

在某些情况下，由于视图引用了多个表列，视图会被列出多次。可以使用 `DISTINCT` 删除这些重复项。

可以修改该查询，以查找直接依赖函数 `f` 的视图。

-   在 `SELECT` 子句中，将表名 `d.refobjid::regclass as ref_object` 替换为函数名 `d.refobjid::regproc as ref_object`。
-   在 `WHERE` 子句中，将所引用对象的目录从表所用的 `d.refclassid = 'pg_class'::regclass` 改为过程（函数）所用的 `d.refclassid = 'pg_proc'::regclass`。同时将对象名从 `d.refobjid = 't1'::regclass` 改为 `d.refobjid = 'f'::regproc`。
-   在 `WHERE` 子句中，将表名 `refobjid = 't1'::regclass` 替换为函数名 `refobjid = 'f'::regproc`。

示例查询中已将这些更改注释掉（前缀为 `--`）。可以将表相关的行注释掉，并启用函数相关的行。

### 查找表列上的直接依赖 {#find-direct-dependencies-on-a-table-column}

可以修改前面的查询，以查找依赖某个表列的视图；如果计划删除某列，这会很有用（向基表添加列从来不会有问题）。该查询使用 `pg_attribute` 目录表中的表列信息。

该查询查找依赖表 `t1` 的 `id` 列的视图：

```sql
SELECT v.oid::regclass AS view,
  d.refobjid::regclass AS ref_object, -- name of table
  a.attname AS col_name               -- column name
FROM pg_attribute AS a   -- columns for a table
  JOIN pg_depend AS d    -- objects that depend on a column
    ON d.refobjsubid = a.attnum AND d.refobjid = a.attrelid
  JOIN pg_rewrite AS r   -- rules depending on the column
    ON r.oid = d.objid
  JOIN pg_class AS v     -- views for the rules
    ON v.oid = r.ev_class
WHERE v.relkind = 'v'    -- filter views only
  -- dependency must be a rule depending on a relation
  AND d.classid = 'pg_rewrite'::regclass
  AND d.refclassid = 'pg_class'::regclass 
  AND d.deptype = 'n'    -- normal dependency
  AND a.attrelid = 't1'::regclass
  AND a.attname = 'id'
;
    view    | ref_object | col_name
------------+------------+----------
 v1         | t1         | id
 v2         | t1         | id
 mytest.vt1 | t1         | id
 mytest.v2a | t1         | id
(4 rows)
```

### 列出视图模式 {#list-view-schemas}

如果在多个模式中创建了视图，还可以列出视图、每个视图的模式以及视图引用的表。查询从 `pg_namespace` 目录表中获取模式，并排除系统模式 `pg_catalog`、`information_schema` 和 `gp_toolkit`。此外，如果某个视图引用自身，查询也不会列出该视图。

```sql
SELECT v.oid::regclass AS view,
  ns.nspname AS schema,       -- view schema,
  d.refobjid::regclass AS ref_object -- name of table
FROM pg_depend AS d            -- objects that depend on a table
  JOIN pg_rewrite AS r        -- rules depending on a table
    ON r.oid = d.objid
  JOIN pg_class AS v          -- views for the rules
    ON v.oid = r.ev_class
  JOIN pg_namespace AS ns     -- schema information
    ON ns.oid = v.relnamespace
WHERE v.relkind = 'v'          -- filter views only
  -- dependency must be a rule depending on a relation
  AND d.classid = 'pg_rewrite'::regclass 
  AND d.refclassid = 'pg_class'::regclass  -- referenced objects in pg_class -- tables and views
  AND d.deptype = 'n'         -- normal dependency
  -- qualify object
  AND ns.nspname NOT IN ('pg_catalog', 'information_schema', 'gp_toolkit') -- system schemas
  AND NOT (v.oid = d.refobjid) -- not self-referencing dependency
;
    view    | schema | ref_object
------------+--------+------------
 v1         | public | t1
 v2         | public | t1
 v2         | public | t1
 v2         | public | v1
 v3         | public | t1
 vm1        | public | mytest.tm1
 mytest.vm1 | mytest | t1
 vm2        | public | mytest.tm1
 mytest.v2a | mytest | t1
 mytest.v2a | mytest | t1
 mytest.v2a | mytest | v1
(11 rows)
```

### 列出视图定义 {#list-view-definitions}

此查询列出依赖 `t1` 的视图、被引用的列以及视图定义。通过向视图定义添加适当的文本来生成 `CREATE VIEW` 命令。

```sql
SELECT v.relname AS view,  
  d.refobjid::regclass as ref_object,
  d.refobjsubid as ref_col, 
  'CREATE VIEW ' || v.relname || ' AS ' || pg_get_viewdef(v.oid) AS view_def
FROM pg_depend AS d
  JOIN pg_rewrite AS r
    ON r.oid = d.objid
  JOIN pg_class AS v
    ON v.oid = r.ev_class
WHERE NOT (v.oid = d.refobjid) 
  AND d.refobjid = 't1'::regclass
  ORDER BY d.refobjsubid
;
 view | ref_object | ref_col |                  view_def
------+------------+---------+--------------------------------------------
 v1   | t1         |       1 | CREATE VIEW v1 AS  SELECT max(t1.id) AS id+
      |            |         |    FROM t1;
 v2a  | t1         |       1 | CREATE VIEW v2a AS  SELECT t1.val         +
      |            |         |    FROM (t1                               +
      |            |         |      JOIN v1 USING (id));
 vt1  | t1         |       1 | CREATE VIEW vt1 AS  SELECT t1.id          +
      |            |         |    FROM t1                                +
      |            |         |   WHERE (t1.id < 3);
 v2   | t1         |       1 | CREATE VIEW v2 AS  SELECT t1.val          +
      |            |         |    FROM (t1                               +
      |            |         |      JOIN v1 USING (id));
 v2a  | t1         |       2 | CREATE VIEW v2a AS  SELECT t1.val         +
      |            |         |    FROM (t1                               +
      |            |         |      JOIN v1 USING (id));
 v3   | t1         |       2 | CREATE VIEW v3 AS  SELECT (t1.val || f()) +
      |            |         |    FROM t1;
 v2   | t1         |       2 | CREATE VIEW v2 AS  SELECT t1.val          +
      |            |         |    FROM (t1                               +
      |            |         |      JOIN v1 USING (id));
(7 rows)
```

### 列出嵌套视图 {#list-nested-views}

此 CTE 查询列出引用另一个视图的视图信息。

此 CTE 查询中的 `WITH` 子句选择用户模式中的所有视图。主 `SELECT` 语句查找引用另一个视图的所有视图。

```sql
WITH views AS ( SELECT v.relname AS view,
  d.refobjid AS ref_object,
  v.oid AS view_oid,
  ns.nspname AS namespace
FROM pg_depend AS d
  JOIN pg_rewrite AS r
    ON r.oid = d.objid
  JOIN pg_class AS v
    ON v.oid = r.ev_class
  JOIN pg_namespace AS ns
    ON ns.oid = v.relnamespace
WHERE v.relkind = 'v'
  AND ns.nspname NOT IN ('pg_catalog', 'information_schema', 'gp_toolkit') -- exclude system schemas
  AND d.deptype = 'n'    -- normal dependency
  AND NOT (v.oid = d.refobjid) -- not a self-referencing dependency
 )
SELECT views.view, views.namespace AS schema,
  views.ref_object::regclass AS ref_view,
  ref_nspace.nspname AS ref_schema
FROM views 
  JOIN pg_depend as dep
    ON dep.refobjid = views.view_oid 
  JOIN pg_class AS class
    ON views.ref_object = class.oid
  JOIN  pg_namespace AS ref_nspace
      ON class.relnamespace = ref_nspace.oid
  WHERE class.relkind = 'v'
    AND dep.deptype = 'n'    
; 
 view | schema | ref_view | ref_schema
------+--------+----------+------------
 v2   | public | v1       | public
 v2a  | mytest | v1       | public
```

### 示例数据 {#example-data}

示例查询的输出基于以下数据库对象和数据。

```sql
CREATE TABLE t1 (
   id integer PRIMARY KEY,
   val text NOT NULL
);

INSERT INTO t1 VALUES
   (1, 'one'), (2, 'two'), (3, 'three');

CREATE FUNCTION f() RETURNS text
   LANGUAGE sql AS 'SELECT ''suffix''::text';

CREATE VIEW v1 AS
  SELECT max(id) AS id
  FROM t1;
 
CREATE VIEW v2 AS
  SELECT t1.val
  FROM t1 JOIN v1 USING (id);
 
CREATE VIEW v3 AS
  SELECT val || f()
  FROM t1;

CREATE VIEW v5 AS
  SELECT f() ;

CREATE SCHEMA mytest ;

CREATE TABLE mytest.tm1 (
   id integer PRIMARY KEY,
   val text NOT NULL
);

INSERT INTO mytest.tm1 VALUES
   (1, 'one'), (2, 'two'), (3, 'three');

CREATE VIEW vm1 AS
  SELECT id FROM mytest.tm1 WHERE id < 3 ;

CREATE VIEW mytest.vm1 AS
  SELECT id FROM public.t1 WHERE id < 3 ;

CREATE VIEW vm2 AS
  SELECT max(id) AS id
  FROM mytest.tm1;

CREATE VIEW mytest.v2a AS
  SELECT t1.val
  FROM public.t1 JOIN public.v1 USING (id);
```