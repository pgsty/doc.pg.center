---
title: "配置行级安全策略"
description: "行级安全（RLS）策略允许表所有者定义访问策略，控制用户对表中特定行的访问。"
weight: 80
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/security/configure-row-level-security-policy.md"
---

当用户尝试查询或更新表时，系统会先应用 RLS 策略，然后才执行用户发出的任何用于截断表中行的命令。

行级安全策略可以针对特定命令创建，例如 `SELECT`/`INSERT`/`UPDATE`/`DELETE`，也可以针对所有命令（`ALL`）创建。行级安全策略还可以根据特定用户、用户组或特定条件，控制对表中特定行的访问。

## 行级安全策略概述 {#row-level-security-policy-overview}

- 默认情况下，表没有设置行级安全策略。如果按照 SQL 权限系统，用户有权访问该表，就可以查询或更新表中的所有行。

- 用户可以通过 `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` 命令为表启用行级安全策略。启用后，除表所有者外，其他用户都无法访问和修改该表。必须设置适当的安全策略，其他用户才能访问和操作表中的行。

    > [!NOTE] 注意
    > 作用于整张表的操作（如 `TRUNCATE` 和 `REFERENCES`）不受行级安全限制。

- 行级安全策略可以针对命令、用户角色或两者。策略可以应用于所有命令，也可以仅针对 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE` 中的某一种命令。同一策略可以授予多个角色，通常的角色层次结构和继承规则也适用于行级安全策略。

- 超级用户和具有 `BYPASSRLS` 属性的角色不受行级安全策略约束。表所有者通常也不受策略约束，但可以使用 `ALTER TABLE ... FORCE ROW LEVEL SECURITY` 对表所有者强制实施行级安全。

- 只有表所有者才能启用、禁用或添加行级安全策略。

## 启用和创建行级安全策略 {#enable-and-create-row-level-security-policy}

表所有者必须先为表启用行级安全策略，然后才能创建具体策略。

**步骤 1.** 启用行级安全策略

表所有者必须先使用以下命令启用行级安全策略：

```
ALTER TABLE <table_name> ENABLE ROW LEVEL SECURITY;
```

**步骤 2.** 创建策略

启用行级安全策略后，可以使用 `CREATE POLICY` 创建策略。

RLS 策略必须在 `USING` 或 `WITH CHECK` 子句中提供一个返回布尔值的表达式，以决定哪些行可以返回。在执行用户查询中的任何条件和函数之前，系统会逐行计算此表达式。表达式未返回 `true` 的行不会被处理。

可以指定不同的表达式，分别控制哪些行可见、哪些行可以修改。策略表达式作为查询的一部分运行，具有执行查询的用户的权限。用户也可以使用以定义者权限执行的函数，访问用户本身无权访问的数据。

创建行级安全策略的语法如下：

```
CREATE POLICY <name> ON <table_name>
    [ AS { PERMISSIVE | RESTRICTIVE } ]
    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
    [ TO { <role_name> | PUBLIC | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( <using_expression> ) ]
    [ WITH CHECK ( <check_expression> ) ]
```

有关详细用法，请参阅以下参数说明：

- `name`：策略的名称。

- `table_name`：策略所应用的表名。

- `PERMISSIVE`：指定将策略创建为宽松策略。适用于给定查询的所有宽松策略都会使用 `OR` 运算符组合。通过创建宽松策略，管理员可以增加可访问的记录集。默认情况下，策略为宽松策略。

- `RESTRICTIVE`：指定将策略创建为限制性策略。适用于给定查询的所有限制性策略都会使用 `AND` 运算符组合。通过创建限制性策略，管理员可以缩小可访问的记录集，因为每条记录都必须通过所有限制性策略。

- 命令（`ALL`、`SELECT`、`INSERT`、`UPDATE`、`DELETE`）：策略所应用的命令。

- `role_name`：策略所应用的角色；默认为 `PUBLIC`，表示策略将应用于所有角色。

- `using_expression`：任意 SQL 条件表达式（返回布尔值）。条件表达式不能包含任何聚合函数或窗口函数。如果启用了行级安全，此表达式会被添加到引用该表的查询中。表达式返回 `true` 的行可见。表达式返回 `false` 或 `null` 的行对用户不可见（在 `SELECT` 命令中），也无法被修改（`UPDATE` 或 `DELETE`）。不可见或不可修改的行不会返回，也不会引发错误。

- `check_expression`：任意 SQL 条件表达式（返回布尔值）。条件表达式不能包含任何聚合函数或窗口函数。如果启用了行级安全，此表达式会用于该表的 `INSERT` 和 `UPDATE` 操作。只有表达式求值为 `true` 的行才被允许。对于任何待插入或更新后的记录，如果表达式求值为 `false` 或 `null`，就会引发错误。

    > [!NOTE] 注意
    > `check_expression` 根据命令拟写入的新内容进行求值，而不是根据原有内容。

## 行级安全策略使用示例 {#example-of-using-row-level-security-policy}

以下示例在表上设置行级访问安全策略，只允许返回 `(department = current_setting('myapp.current_department'))` 为 `true` 的行。

1. 以管理员身份访问数据库：

    ```
    psql -h <host_ip> -p <port> -U <user_name> -d <db_name>
    ```
2. 创建表并插入数据：

    ```
    CREATE TABLE projects (
        project_id SERIAL PRIMARY KEY,
        project_name TEXT,
        project_manager TEXT,
        department TEXT
    );

    INSERT INTO projects (project_name, project_manager, department) VALUES
    ('Project Alpha', 'zhangsan', 'Engineering'),
    ('Project Beta', 'lisi', 'HR'),
    ('Project Gamma', 'wangwu', 'Sales');
    ```
3. 启用行级安全策略：

    ```
    ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
    ```
4.  创建行级安全策略：

    ```
    CREATE POLICY department_policy
    ON projects
    FOR SELECTUSING (department = current_setting('myapp.current_department'));
    ```
    此策略只返回 `(department = current_setting('myapp.current_department'))` 为 `true` 的行。
5. 创建测试用户：

    ```
    CREATE USER zhangsan WITH PASSWORD '<password>';
    CREATE USER lisi WITH PASSWORD '<password>';
    CREATE USER wangwu WITH PASSWORD '<password>';
    ```
6. 授予测试用户查询 `projects` 表的权限：

    ```
    GRANT SELECT ON projects TO zhangsan;
    ```
7. 切换到测试用户，并为当前会话定义变量 `myapp.current_department` 的值：

    ```
    SET ROLE zhangsan;
    SET myapp.current_department = 'Engineering';
    ```
8. 以当前用户身份查询 `projects` 表：

    ```
    SELECT * FROM projects;
    ```

由于 `myapp.current_department` 的值设为 `Engineering`，预期会返回以下数据：

```
project_id | project_name | project_manager | department
------------+--------------+-----------------+------------
        1 | Project Alpha | zhangsan        | Engineering
```

由于行级安全策略生效，用户 `zhangsan` 只能看到与 "Engineering" 部门相关的行。
