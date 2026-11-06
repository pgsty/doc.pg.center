---
title: "FETCH"
description: "使用游标从查询中检索行。"
weight: 1470
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/fetch.md"
---

## 语法概要 {#synopsis}

```sql
FETCH [ <forward_direction> { FROM | IN } ] <cursor_name>
```

其中 `<forward_direction>` 可以为空，或为以下选项之一：

```sql
    NEXT
    FIRST
    ABSOLUTE <count>
    RELATIVE <count>
    <count>
    ALL
    FORWARD
    FORWARD <count>
    FORWARD ALL
```

## 说明 {#description}

`FETCH` 使用预先创建的游标检索行。

> **注意** 不能对 `PARALLEL RETRIEVE CURSOR` 执行 `FETCH`，必须使用 [`RETRIEVE`](/cloudberry/reference/sql-stmts/retrieve/) 从中检索行。

游标有一个关联位置，供 `FETCH` 使用。游标可以位于查询结果的第一行之前、结果中的任意一行上，或最后一行之后。创建时，游标位于第一行之前。获取若干行后，游标位于最近检索的行上。如果 `FETCH` 超过可用行的末尾，则游标停在最后一行之后。`FETCH ALL` 总是使游标停在最后一行之后。

> **注意**
> Apache Cloudberry 不支持可滚动游标，因此不能向后移动游标位置。只能通过 `FETCH` 向前移动游标。

`NEXT`、`FIRST`、`ABSOLUTE`、`RELATIVE` 形式在适当移动游标后获取一行。如果不存在这样的行，则返回空结果，并将游标停在第一行之前或最后一行之后的相应位置。

使用 `FORWARD` 的形式沿向前方向检索指定数量的行，将游标停在最后返回的行上（如果请求行数超过可用行数，则停在所有行之后）。

`RELATIVE 0` 和 `FORWARD 0` 请求在不移动游标的情况下获取当前行，即再次获取最近获取的行。除非游标位于第一行之前或最后一行之后，否则会成功；在这两种情况下不返回任何行。

> **注意**
> 本页说明 SQL 命令层面游标的用法。如果要在 PL/pgSQL 函数中使用游标，规则有所不同。

## 参数 {#parameters}

**`forward_direction`**

定义获取方向和要获取的行数。Apache Cloudberry 只允许向前获取。可以是以下选项之一：

**`NEXT`**

获取下一行。省略方向时采用此默认行为。

**`FIRST`**

获取查询的第一行（等同于 `ABSOLUTE 1`）。只有这是使用该游标的第一次 `FETCH` 操作时才允许。

**`ABSOLUTE count`**

获取查询的指定行。如果 count 超出范围，则定位到最后一行之后。仅当 count 指定的行使游标向前移动时才允许。

**`RELATIVE count`**

获取查询中位于当前游标位置前方 count 行的指定行。`RELATIVE 0` 会重新获取当前行（如果有）。仅当 count 使游标向前移动时才允许。

**`count`**

获取接下来的 count 行（等同于 `FORWARD count`）。

**`ALL`**

获取所有剩余行（等同于 `FORWARD ALL`）。

**`FORWARD`**

获取下一行（等同于 `NEXT`）。

**`FORWARD count`**

获取接下来的 count 行。`FORWARD 0` 重新获取当前行。

**`FORWARD ALL`**

获取所有剩余行。

**`cursor_name`**

已打开游标的名称。

## 输出 {#outputs}

成功完成时，`FETCH` 命令返回以下形式的命令标签：

```sql
FETCH <count>
```

count 是获取的行数（可能为零）。请注意，`psql` 实际上不会显示该命令标签，因为 `psql` 会显示获取到的行。

## 注意事项 {#notes}

Apache Cloudberry 不支持可滚动游标，因此只能用 `FETCH` 向前移动游标位置。

使用 `ABSOLUTE` 获取并不会比通过相对移动到达所需行更快：底层实现无论如何都必须遍历所有中间行。

使用 `DECLARE` 定义游标。使用 `MOVE` 在不检索数据的情况下更改游标位置。

## 示例 {#examples}

开始事务：

```sql
BEGIN;
```

设置游标：

```sql
DECLARE mycursor CURSOR FOR SELECT * FROM films;
```

获取游标 `mycursor` 中的前 5 行：

```sql
FETCH FORWARD 5 FROM mycursor;
 code  |          title          | did | date_prod  |   kind   |  len
-------+-------------------------+-----+------------+----------+-------
 BL101 | The Third Man           | 101 | 1949-12-23 | Drama    | 01:44
 BL102 | The African Queen       | 101 | 1951-08-11 | Romantic | 01:43
 JL201 | Une Femme est une Femme | 102 | 1961-03-12 | Romantic | 01:25
 P_301 | Vertigo                 | 103 | 1958-11-14 | Action   | 02:08
 P_302 | Becket                  | 103 | 1964-02-03 | Drama    | 02:28
```

关闭游标并结束事务：

```sql
CLOSE mycursor;
COMMIT;
```

更改表 `films` 中游标 `c_films` 当前所在行的 `kind` 列：

```sql
UPDATE films SET kind = 'Dramatic' WHERE CURRENT OF c_films;
```

## 兼容性 {#compatibility}

SQL 标准只允许在嵌入式 SQL 和模块中使用游标。Apache Cloudberry 允许交互式使用游标。

这里描述的 `FETCH` 变体像 `SELECT` 结果一样返回数据，而不是将数据放入宿主变量。除这一点外，`FETCH` 完全向上兼容 SQL 标准。

包含 `FORWARD` 的 `FETCH` 形式，以及隐含 `FORWARD` 的 `FETCH` count 和 `FETCH ALL` 形式，都是 Apache Cloudberry 的扩展。不支持 `BACKWARD`。

SQL 标准只允许在游标名称之前使用 `FROM`；可使用 `IN` 或将其完全省略的选项属于扩展。

## 另请参阅 {#see-also}

[DECLARE](/cloudberry/reference/sql-stmts/declare/), [CLOSE](/cloudberry/reference/sql-stmts/close/), [MOVE](/cloudberry/reference/sql-stmts/move/)
