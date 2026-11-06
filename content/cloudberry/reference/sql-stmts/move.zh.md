---
title: "MOVE"
description: "定位游标。"
weight: 1540
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/move.md"
---

## 概要 {#synopsis}

```sql
MOVE [ <forward_direction> [ FROM | IN ] ] <cursor_name>
```

其中 `<forward_direction>` 可以为空，也可以是以下形式之一：

```sql
    NEXT
    FIRST
    LAST
    ABSOLUTE <count>
    RELATIVE <count>
    <count>
    ALL
    FORWARD
    FORWARD <count>
    FORWARD ALL
```

## 描述 {#description}

`MOVE` 重新定位游标，但不检索任何数据。`MOVE` 的行为与 [`FETCH`](/cloudberry/reference/sql-stmts/fetch/) 命令完全相同，只是仅定位游标而不返回行。

> **注意** 不能对 `PARALLEL RETRIEVE CURSOR` 执行 `MOVE`。

> **注意** Apache Cloudberry 不支持可滚动游标，因此无法向后移动游标位置。使用 `MOVE` 只能向前移动游标。

`MOVE` 命令的参数与 `FETCH` 命令相同；语法和用法详情见 [`FETCH`](/cloudberry/reference/sql-stmts/fetch/)。

## 输出 {#outputs}

成功完成时，`MOVE` 命令返回以下形式的命令标签：

```sql
MOVE <count>
```

count 表示使用相同参数的 `FETCH` 命令本应返回的行数（可能为零）。

## 示例 {#examples}

启动事务：

```sql
BEGIN;
```

创建游标：

```sql
DECLARE mycursor CURSOR FOR SELECT * FROM films;
```

跳过游标 `mycursor` 中的前 5 行：

```sql
MOVE FORWARD 5 IN mycursor;
MOVE 5
```

随后获取下一行（第 6 行）：

```sql
FETCH 1 FROM mycursor;
 code  | title  | did | date_prod  |  kind  |  len
-------+--------+-----+------------+--------+-------
 P_303 | 48 Hrs | 103 | 1982-10-22 | Action | 01:37
(1 row)
```

关闭游标并结束事务：

```sql
CLOSE mycursor;
COMMIT;
```

## 兼容性 {#compatibility}

SQL 标准中没有 `MOVE` 语句。

## 另见 {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/), [FETCH](/cloudberry/reference/sql-stmts/fetch/), [CLOSE](/cloudberry/reference/sql-stmts/close/)
