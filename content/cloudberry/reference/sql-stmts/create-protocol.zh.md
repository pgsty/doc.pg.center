---
title: "CREATE PROTOCOL"
description: "注册自定义数据访问协议，供定义 Apache Cloudberry 外部表时使用。"
weight: 730
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sql-stmts/create-protocol.md"
---

## 概要 {#synopsis}

```sql
CREATE [TRUSTED] PROTOCOL <name> (
   [readfunc='<read_call_handler>'] [, writefunc='<write_call_handler>']
   [, validatorfunc='<validate_handler>' ])
```

## 描述 {#description}

`CREATE PROTOCOL` 将数据访问协议名称与负责从外部数据源读取数据和向其写入数据的调用处理函数关联。必须是超级用户才能创建协议。

`CREATE PROTOCOL` 命令必须指定读取调用处理函数或写入调用处理函数。`CREATE PROTOCOL` 命令中指定的处理函数必须已经在数据库中定义。

可以在 `CREATE EXTERNAL TABLE` 命令中指定该协议名称。

关于创建和启用自定义数据访问协议，见“自定义数据访问协议示例”文档。

## 参数 {#parameters}

**`TRUSTED`**

如果未指定，只有超级用户和协议所有者可以使用该协议创建外部表。如果指定，超级用户和协议所有者可以向其他数据库角色 `GRANT` 该协议的权限。

**`name`**

数据访问协议的名称。协议名区分大小写，并且在数据库的协议中必须唯一。

**`readfunc= 'read_call_handler'`**

先前注册的函数名称，Apache Cloudberry 调用它从外部数据源读取数据。命令必须指定读取调用处理函数或写入调用处理函数。

**`writefunc= 'write_call_handler'`**

先前注册的函数名称，Apache Cloudberry 调用它向外部数据源写入数据。命令必须指定读取调用处理函数或写入调用处理函数。

**`validatorfunc='validate_handler'`**

可选的验证函数，用于验证 `CREATE EXTERNAL TABLE` 命令中指定的 URL。

## 注意事项 {#notes}

Apache Cloudberry 在内部处理 `file`、`gpfdist` 和 `gpfdists` 类型的外部表。

实现数据访问协议的任何共享库，都必须位于所有 Apache Cloudberry Segment 主机上的相同位置。例如，共享库可以放在所有主机的操作系统环境变量 `LD_LIBRARY_PATH` 所指定的位置。也可以在定义处理函数时指定位置。例如，在 `CREATE PROTOCOL` 命令中定义 `s3` 协议时，将共享对象的位置指定为 `$libdir/gps3ext.so`，其中 `$libdir` 位于 `$GPHOME/lib`。

## 兼容性 {#compatibility}

`CREATE PROTOCOL` 是 Apache Cloudberry 的扩展。

## 另见 {#see-also}

[ALTER PROTOCOL](/cloudberry/reference/sql-stmts/alter-protocol/), [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/), [DROP PROTOCOL](/cloudberry/reference/sql-stmts/drop-protocol/), [GRANT](/cloudberry/reference/sql-stmts/grant/)
