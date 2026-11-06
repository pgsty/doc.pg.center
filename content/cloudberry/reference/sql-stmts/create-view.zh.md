---
title: "CREATE VIEW"
description: "定义新的视图。"
weight: 940
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-view.md"
---

## 语法概要 {#synopsis}

```sql
CREATE [OR REPLACE] [TEMP | TEMPORARY] [RECURSIVE] VIEW <name> [ ( <column_name> [, ...] ) ]
    [ WITH ( view_option_name [= view_option_value] [, ... ] ) ]
    AS <query>
    [ WITH [ CASCADED | LOCAL ] CHECK OPTION ]
```

## 说明 {#description}

`CREATE VIEW` 定义查询的视图。视图不会被物理实例化；相反，每次在查询中引用视图时，Apache Cloudberry 都会运行该查询。

`CREATE OR REPLACE VIEW` 类似，但如果同名视图已存在，则会替换该视图。新查询必须生成与现有视图查询相同的列（即列名相同、顺序相同、数据类型相同），但可以在列表末尾追加列。生成输出列的计算方式可以完全不同。

如果给出模式名（例如 `CREATE VIEW myschema.myview ...`），则在指定模式中创建视图；否则在当前模式中创建。临时视图位于特殊模式中，因此创建临时视图时不能提供模式名。视图名称必须与同一模式中其他视图、表、序列、索引或外表的名称不同。

## 参数 {#parameters}

**`TEMPORARY | TEMP`**

如果指定，视图会创建为临时视图。当前会话结束时会自动删除临时视图。临时视图存在期间，同名永久关系对当前会话不可见，除非使用模式限定名称引用。

如果视图引用的任何表是临时表，则该视图会创建为临时视图（无论是否指定 `TEMPORARY`）。

**`RECURSIVE`**

创建递归视图。语法

```sql
    CREATE RECURSIVE VIEW [ <schema> . ] <view_name> (<column_names>) AS SELECT <...>;
```

等价于

```sql
CREATE VIEW [ <schema> . ] <view_name> AS WITH RECURSIVE <view_name> (<column_names>) AS (SELECT <...>) SELECT <column_names> FROM <view_name>;
```

递归视图必须指定视图列名称列表。

**`name`**

要创建的视图名称（可以用模式名限定）。

**`column_name`**

可选的视图列名称列表。如果未提供，则从查询中推导列名。

**`WITH ( view_option_name [= view_option_value] [, ... ] )`**

此子句指定视图的可选参数；支持以下参数：

**`check_option (string)`**

此参数可以是 `local` 或 `cascaded`，等价于指定 `WITH [ CASCADED | LOCAL ] CHECK OPTION`（见下文）。可以使用 [ALTER VIEW](/cloudberry/reference/sql-stmts/alter-view/) 更改现有视图的此选项。

**`security_barrier (boolean)`**

如果视图用于提供行级安全，应使用此参数。更多信息参见 PostgreSQL 文档中的[规则和权限](https://www.postgresql.org/docs/12/rules-privileges.html)。

**`query`**

用于提供视图列和行的 [SELECT](/cloudberry/reference/sql-stmts/select/) 或 [VALUES](/cloudberry/reference/sql-stmts/values/) 命令。

**`WITH [ CASCADED | LOCAL ] CHECK OPTION`**

此选项控制自动可更新视图的行为。指定后，会检查视图上的 `INSERT` 和 `UPDATE` 命令，确保新行满足视图定义条件（即确保新行通过该视图可见）。如果不满足，Apache Cloudberry 会拒绝更新。如果未指定 `CHECK OPTION`，视图上的 `INSERT` 和 `UPDATE` 命令可以创建通过视图不可见的行。支持以下检查选项：

**`LOCAL`**

新行只根据视图自身直接定义的条件检查。底层基视图中定义的条件不检查（除非底层基视图也指定了 `CHECK OPTION`）。

**`CASCADED`**

新行根据视图及所有底层基视图的条件检查。如果指定 `CHECK OPTION`，而没有指定 `LOCAL` 或 `CASCADED`，则默认使用 `CASCADED`。

`CHECK OPTION` 不能与 `RECURSIVE` 视图一起使用。

## 注意事项 {#notes}

使用 [DROP VIEW](/cloudberry/reference/sql-stmts/drop-view/) 语句删除视图。

请确保按需要为视图列分配名称和数据类型。例如：

```sql
CREATE VIEW vista AS SELECT 'Hello World';
```

这在两个方面都不理想：列名默认为 `?column?`，列数据类型默认为 `text`，可能不是你想要的。如果希望视图结果中包含字符串字面量，应使用类似下面的写法：

```sql
CREATE VIEW vista AS SELECT text 'Hello World' AS hello;
```

访问视图所引用的表由视图所有者的权限决定，而不是由当前用户决定（即使当前用户是超级用户）。对于超级用户来说，这可能令人困惑，因为超级用户通常可以访问所有对象。但对于视图，即使是超级用户，如果不是视图所有者，也必须明确授予其访问视图引用表的权限。在某些情况下，视图可以用于提供对底层表的安全但受限的访问。不过，并非所有视图都能防止篡改；详情参见 PostgreSQL 文档中的[规则和权限](https://www.postgresql.org/docs/12/rules-privileges.html)。

视图中调用的函数与直接从使用该视图的查询中调用时的处理方式相同。因此，视图用户必须拥有调用视图所用任何函数的权限。

当 `CREATE VIEW <view> ...` 和 `SELECT ... FROM <view>` 都指定 `ORDER BY` 子句时，Apache Cloudberry 会忽略 `CREATE VIEW` 语句中的 `ORDER BY` 子句。

对现有视图使用 `CREATE OR REPLACE VIEW` 时，只会更改视图定义的 `SELECT` 规则。其他视图属性（包括所有权、权限和非 `SELECT` 规则）保持不变。必须拥有该视图才能替换它（包括属于其所有者角色的成员）。

## 可更新视图 {#updatable-views}

简单视图会自动可更新：Apache Cloudberry 允许像对普通表一样在视图上执行 `INSERT`、`UPDATE` 和 `DELETE` 语句。视图满足以下全部条件时会自动可更新：

- `FROM` 列表中必须恰好有一个条目，且该条目必须是表或另一个可更新视图。

- 视图定义的顶层不能包含 `WITH`、`DISTINCT`、`GROUP BY`、`HAVING`、`LIMIT` 或 `OFFSET` 子句。

- 视图定义的顶层不能包含集合操作（`UNION`、`INTERSECT` 或 `EXCEPT`）。

- 视图的选择列表不能包含聚合函数、窗口函数或返回集合的函数。

自动可更新视图可以混合包含可更新和不可更新列。如果某列只是对底层基关系可更新列的简单引用，则该列可更新；否则列为只读，若 `INSERT` 或 `UPDATE` 语句尝试为其赋值，Apache Cloudberry 会报错。

如果视图自动可更新，系统会将视图上的任何 `INSERT`、`UPDATE` 或 `DELETE` 语句转换为对底层基关系的相应语句。带 `ON CONFLICT UPDATE` 子句的 `INSERT` 语句完全支持。

如果自动可更新视图包含 `WHERE` 条件，该条件会限制 `UPDATE` 和 `DELETE` 语句可以修改底层关系中的哪些行。不过，`UPDATE` 允许将某行修改到不再满足 `WHERE` 条件的状态，从而使其不再通过视图可见。同样，`INSERT` 命令可能插入不满足 `WHERE` 条件的基关系行，因此这些行不会通过视图可见（`ON CONFLICT UPDATE` 也可能影响视图中不可见的现有行）。可以使用 `CHECK OPTION`，防止 `INSERT` 和 `UPDATE` 创建这种通过视图不可见的行。

如果自动可更新视图标记了 `security_barrier` 属性，则视图的所有 `WHERE` 条件（以及使用标记为 `LEAKPROOF` 的操作符的条件）始终会在视图用户添加的任何条件之前计算。完整详情参见 PostgreSQL 文档中的[规则和权限](https://www.postgresql.org/docs/12/rules-privileges.html)。请注意，因此最终不会返回（因为不满足用户 `WHERE` 条件）的行仍可能被锁定。可以使用 `EXPLAIN` 查看哪些条件在关系级别应用（因此不会锁行），哪些条件不在关系级别应用。

不满足这些条件的更复杂视图默认是只读的：系统不允许在视图上插入、更新或删除。可以通过创建规则（参见 [CREATE RULE](/cloudberry/reference/sql-stmts/create-rule/)）获得可更新视图的效果。

请注意，在视图上执行插入、更新或删除的用户必须对视图拥有相应的插入、更新或删除权限。此外，视图所有者必须对底层基关系拥有相关权限，但执行更新的用户不需要对底层基关系拥有任何权限（同样参见 PostgreSQL 文档中的[规则和权限](https://www.postgresql.org/docs/12/rules-privileges.html)）。

## 示例 {#examples}

创建由所有喜剧电影组成的视图：

```sql
CREATE VIEW comedies AS
    SELECT * FROM films 
    WHERE kind = 'comedy';
```

此视图包含视图创建时 `film` 表中的列。虽然使用了 `*` 创建视图，但之后添加到表中的列不会成为视图的一部分。

创建带有 `LOCAL CHECK OPTION` 的视图：

```sql
CREATE VIEW universal_comedies AS
    SELECT *
    FROM comedies
    WHERE classification = 'U'
    WITH LOCAL CHECK OPTION;
```

此视图基于 comedies `view`，只显示 `kind = 'Comedy'` 且 `classification = 'U'` 的电影。尝试在视图中 `INSERT` 或 `UPDATE` 行时，如果新行没有 `classification = 'U'`，操作会被拒绝，但不会检查电影 `kind`。

创建带有 `CASCADED CHECK OPTION` 的视图：

```sql
CREATE VIEW pg_comedies AS
    SELECT *
    FROM comedies
    WHERE classification = 'PG'
    WITH CASCADED CHECK OPTION;
```

此视图会同时检查新行的 `kind` 和 `classification`。

创建包含可更新和不可更新列混合内容的视图：

```sql
CREATE VIEW comedies AS
    SELECT f.*,
           country_code_to_name(f.country_code) AS country,
           (SELECT avg(r.rating)
            FROM user_ratings r
            WHERE r.film_id = f.id) AS avg_rating
    FROM films f
    WHERE f.kind = 'Comedy';
```

此视图支持 `INSERT`、`UPDATE` 和 `DELETE`。`films` 表中的所有列都可更新，而计算列 `country` 和 `avg_rating` 为只读。

创建获取排名前十的婴儿姓名的视图：

```sql
CREATE VIEW topten AS 
    SELECT name, rank, gender, year
    FROM names, rank
    WHERE rank < '11' AND names.id=rank.id;
```

创建由 1 到 100 的数字组成的递归视图：

```sql
CREATE RECURSIVE VIEW public.nums_1_100 (n) AS
    VALUES (1)
UNION ALL
    SELECT n+1 FROM nums_1_100 WHERE n < 100;
```

请注意，虽然此 `CREATE VIEW` 命令中的递归视图名称带有模式限定，但其内部自引用没有模式限定。这是因为隐式创建的 CTE 名称不能带模式限定。

## 兼容性 {#compatibility}

`CREATE OR REPLACE VIEW` 是 Apache Cloudberry 的扩展。临时视图的概念也是扩展。`WITH ( ... )` 子句同样是扩展。

## 另请参阅 {#see-also}

[ALTER VIEW](/cloudberry/reference/sql-stmts/alter-view/), [DROP VIEW](/cloudberry/reference/sql-stmts/drop-view/), [CREATE MATERIALIZED VIEW](/cloudberry/reference/sql-stmts/create-materialized-view/)
