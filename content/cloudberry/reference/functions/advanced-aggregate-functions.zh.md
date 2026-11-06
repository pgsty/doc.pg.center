---
title: "Apache Cloudberry 高级聚合函数"
linkTitle: "高级聚合函数"
description: "以下内置高级分析函数是 Cloudberry 对 PostgreSQL 数据库的扩展。"
weight: 30
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/functions/advanced-aggregate-functions.md"
---

分析函数均为*不可变*函数。

> **注意** Cloudberry MADlib 分析扩展提供了更多高级函数，可用于对 Apache Cloudberry 数据进行统计分析和机器学习。

| 函数 | 返回类型 | 完整语法 | 描述 |
|----------|-------------|-------------|-------------|
| `MEDIAN (expr)` | `timestamp, timestamptz, interval, float` | `MEDIAN (expression)` [^1] | 可以接收二维数组作为输入，并将其视为矩阵。 |
| `PERCENTILE_CONT (expr) WITHIN GROUP (ORDER BY expr [DESC/ASC])` | `timestamp, timestamptz, interval, float` | `PERCENTILE_CONT(percentage) WITHIN GROUP (ORDER BY expression)` [^2] | 计算逆分布函数，假定使用连续分布模型。接收一个百分位比例和排序规范，返回的数据类型与参数的数值数据类型相同。返回值通过线性插值计算得出。计算时忽略空值。 |
| `PERCENTILE_DISC (expr) WITHIN GROUP (ORDER BY expr [DESC/ASC])` | `timestamp, timestamptz, interval, float` | `PERCENTILE_DISC(percentage) WITHIN GROUP (ORDER BY expression)` [^3] | 计算逆分布函数，假定使用离散分布模型。接收一个百分位比例和排序规范。返回值是集合中的一个元素。计算时忽略空值。 |
| `sum(array[])` | `smallint[]int[], bigint[], float[]` | `sum(array[[1,2],[3,4]])` [^4] | 执行矩阵求和。可以接收二维数组作为输入，并将其视为矩阵。 |
| `pivot_sum (label[], label, expr)` | `int[], bigint[], float[]` | `pivot_sum( array['A1','A2'], attr, value)` | 执行透视聚合，使用求和处理重复条目。 |
| `unnest (array[])` | `anyelement` 的集合 | `unnest( array['one', 'row', 'per', 'item'])` | 将一维数组转换为多行。返回多态的 [PostgreSQL 伪类型](https://www.postgresql.org/docs/12/datatype-pseudo.html) `anyelement` 的集合。 |

[^1]:

    ```sql
    SELECT department_id, MEDIAN(salary) 
    FROM employees 
    GROUP BY department_id;
    ```

[^2]:

    ```sql
    SELECT department_id,
    PERCENTILE_CONT (0.5) WITHIN GROUP (ORDER BY salary DESC)
    "Median_cont"; 
    FROM employees GROUP BY department_id;
    ```

[^3]:

    ```sql
    SELECT department_id, 
    PERCENTILE_DISC (0.5) WITHIN GROUP (ORDER BY salary DESC)
    "Median_desc"; 
    FROM employees GROUP BY department_id;
    ```

[^4]:

    ```sql
    CREATE TABLE mymatrix (myvalue int[]);
    INSERT INTO mymatrix VALUES (array[[1,2],[3,4]]);
    INSERT INTO mymatrix VALUES (array[[0,1],[1,0]]);
    SELECT sum(myvalue) FROM mymatrix;
    sum 
    ---------------
    {{1,3},{4,4}}
    ```
