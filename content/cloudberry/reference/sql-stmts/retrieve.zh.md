---
title: "RETRIEVE"
description: "使用并行检索游标从查询中检索行。"
weight: 1620
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/retrieve.md"
---

## 语法概要 {#synopsis}

```sql
RETRIEVE { <count> | ALL } FROM ENDPOINT <endpoint_name>
```

## 说明 {#description}

`RETRIEVE` 使用预先创建的并行检索游标检索行。你需要在各个检索会话中检索行；这些会话分别直接连接到各个 Segment 的端点，由各端点提供相应 Segment 的结果。启动检索会话时，必须在连接请求中指定 `gp_retrieve_conn=true`。由于检索会话独立于并行检索游标及其对应的端点，因此可以在同一检索会话中从多个端点执行 `RETRIEVE`。

并行检索游标有一个关联的位置，供 `RETRIEVE` 使用。游标可以位于查询结果的第一行之前、结果中的任意一行上，或结果的最后一行之后。

> **注意：**
>
> 由于 Apache Cloudberry 不支持可滚动游标，`RETRIEVE` 命令只能向前移动并行检索游标的位置。

并行检索游标创建时位于第一行之前。检索若干行后，游标位于最近检索的那一行上。

如果 `RETRIEVE` 越过可用行的末尾，游标将停在最后一行之后。

`RETRIEVE ALL` 总是使并行检索游标停在最后一行之后。

## 参数 {#parameters}

**`count`**

检索接下来的 count 行。count 必须为正数。

**`ALL`**

检索所有剩余行。

**`endpoint_name`**

要从中检索行的端点名称。

## 输出 {#outputs}

成功完成时，`RETRIEVE` 命令返回获取的行（可能为空）以及获取的行数（可能为零）。

## 注意事项 {#notes}

使用 `DECLARE ... PARALLEL RETRIEVE CURSOR` 定义并行检索游标。

并行检索游标不支持 `FETCH` 或 `MOVE` 操作。

## 示例 {#examples}

开始事务：

```sql
BEGIN;
```

创建并行检索游标：

```sql
DECLARE mycursor PARALLEL RETRIEVE CURSOR FOR SELECT * FROM films;
```

列出游标端点：

```sql
SELECT * FROM gp_endpoints WHERE cursorname='mycursor';
```

记下各端点对应的 hostname、port、auth_token 和 name。

在另一个终端窗口中，使用上一查询返回的 hostname、port 和 auth_token 启动检索会话。例如：

```sql
PGPASSWORD=d3825fc07e56bee5fcd2b1d0b600c85e PGOPTIONS='-c gp_retrieve_conn=true' psql -d testdb -h sdw3 -p 6001;
```

获取某个端点的所有行（例如名为 `prc10000001100000005` 的端点）：

```sql
RETRIEVE ALL FROM ENDPOINT prc10000001100000005;
```

退出检索会话。

```sql
\q
```

回到原来的会话，关闭游标并结束事务：

```sql
CLOSE mycursor;
COMMIT;
```

## 兼容性 {#compatibility}

`RETRIEVE` 是 Apache Cloudberry 的扩展。SQL 标准未规定并行检索游标。

## 另请参阅 {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/), [CLOSE](/cloudberry/reference/sql-stmts/close/)
