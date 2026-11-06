---
title: "Apache Cloudberry 窗口函数"
linkTitle: "窗口函数"
description: "以下是 Apache Cloudberry 的内置窗口函数。"
weight: 20
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/functions/window-functions.md"
---

所有窗口函数均为*不可变*函数。<!-- For more information about window functions, see "Window Expressions" in the *Apache Cloudberry Administrator Guide*. -->

|函数|返回类型|完整语法|描述|
|--------|-----------|-----------|-----------|
|`cume_dist()`|`double precision`|`CUME_DIST() OVER ( [PARTITION BY` expr `] ORDER BY` expr `)`|计算一个值在一组值中的累积分布。值相等的行始终得到相同的累积分布值。|
|`dense_rank()`|`bigint`|`DENSE_RANK () OVER ( [PARTITION BY` expr `] ORDER BY` expr `)`|计算一行在有序行组中的排名，不跳过排名值。值相等的行获得相同的排名值。|
|`first_value(*expr*)`|与输入 expr 的类型相同|`FIRST_VALUE(` expr `) OVER ( [PARTITION BY` expr `] ORDER BY` expr `[ROWS\|RANGE` frame_expr `] )`|返回有序值集合中的第一个值。|
|`lag(*expr* [,*offset*] [,*default*])`|与输入 *expr* 的类型相同|`LAG(` *expr* `[,` *offset* `] [,` *default* `]) OVER ( [PARTITION BY` *expr* `] ORDER BY` *expr* `)`|无需自连接即可访问同一表中的多行。给定查询返回的一系列行和游标位置，`LAG` 可以访问该位置之前指定物理偏移量处的行。`offset` 默认为 1。*default* 指定偏移量超出窗口范围时返回的值。如果未指定 *default*，默认值为空值。|
|`last_value(*expr*)`|与输入 *expr* 的类型相同|`LAST_VALUE(*expr*) OVER ( [PARTITION BY *expr*] ORDER BY *expr* [ROWS\|RANGE *frame_expr*] )`|返回有序值集合中的最后一个值。|
|``lead(*expr* [,*offset*] [,*default*])``|与输入 *expr* 的类型相同|`LEAD(*expr*[,*offset*] [,*expr**default*]) OVER ( [PARTITION BY *expr*] ORDER BY *expr* )`|无需自连接即可访问同一表中的多行。给定查询返回的一系列行和游标位置，`lead` 可以访问该位置之后指定物理偏移量处的行。如果未指定 *offset*，默认偏移量为 1。*default* 指定偏移量超出窗口范围时返回的值。如果未指定 *default*，默认值为空值。|
|`ntile(*expr*)`|`bigint`|`NTILE(*expr*) OVER ( [PARTITION BY *expr*] ORDER BY *expr* )`|将有序数据集划分为若干个桶（数量由 *expr* 定义），并为每行分配桶编号。|
|`percent_rank()`|`double precision`|`PERCENT_RANK () OVER ( [PARTITION BY *expr*] ORDER BY *expr*)`|计算（假想行 `R` 的排名 − 1）除以（窗口分区内所评估的行数 − 1）所得的值。|
|`rank()`|`bigint`|`RANK () OVER ( [PARTITION BY *expr*] ORDER BY *expr*)`|计算一行在有序值组中的排名。按排名条件取值相等的行获得相同的排名。将并列行数加到当前排名值上，即得下一排名值。因此，排名可能不是连续的数字。|
|`row_number()`|`bigint`|`ROW_NUMBER () OVER ( [PARTITION BY *expr*] ORDER BY *expr*)`|为作用范围内的每一行分配唯一编号（可以是窗口分区中的每一行，也可以是查询结果中的每一行）。|
