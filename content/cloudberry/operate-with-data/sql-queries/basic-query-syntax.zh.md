---
title: "Apache Cloudberry 基本查询"
linkTitle: "基本查询语法"
description: "本文介绍 Apache Cloudberry 的基本查询。"
weight: 10
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/operate-with-data/sql-queries/basic-query-syntax.md"
---

Apache Cloudberry 是基于 PostgreSQL 和 Greenplum 开发的高性能、高度并行的数据仓库。下面是基本查询语法的一些示例。

- `SELECT`：用于从数据库和表中检索数据。

    ```sql
    SELECT * FROM employees;  -- Queries all data in the employees table.
    ```

- 条件查询（`WHERE`）：用于根据特定条件筛选结果集。

    ```sql
    SELECT * FROM employees WHERE salary > 50000;  -- Queries employee information with salary exceeding 50,000.
    ```

- `ORDER BY`：用于按一个或多个列对查询结果排序。

    ```sql
    SELECT * FROM employees ORDER BY salary DESC;  -- Sorts employee information in descending order by salary.
    ```

- 聚合函数：例如 `COUNT`、`SUM`、`AVG`、`MAX`、`MIN`，用于计算数据集的统计信息。

    ```sql
    SELECT AVG(salary) FROM employees;  -- Calculates the average salary of employees.
    ```

- `GROUP BY`：与聚合函数结合使用，对结果集分组。

    ```sql
    SELECT department, COUNT(*) FROM employees GROUP BY department;  -- Counts the number of employees by department.
    ```

- 限制结果数量（`LIMIT`）：用于限制查询结果返回的行数。

    ```sql
    SELECT * FROM employees LIMIT 10;  -- Only queries the information of the first 10 employees.
    ```

- 连接查询（`JOIN`）：用于根据相关列组合两个或多个表中的数据。

    ```sql
    SELECT employees.name, departments.name 
    FROM employees 
    JOIN departments ON employees.department_id = departments.id;  -- Queries employees and their corresponding department names.
    ```

- 子查询：嵌套在另一个 SQL 查询中的查询。

    ```sql
    SELECT name FROM employees 
    WHERE department_id IN (SELECT id FROM departments WHERE location = 'New York');  -- Queries all employees working in New York.
    ```

以上只是 Apache Cloudberry 基本查询语法的简要概览。Apache Cloudberry 还提供更高级的查询和函数，帮助开发者执行复杂的数据操作和分析。

## 另请参见 {#see-also}

- [插入、更新和删除行](/cloudberry/operate-with-data/operate-with-db-objects/insert-update-delete-rows/)