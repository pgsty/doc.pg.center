---
title: "gpreload"
description: "按指定列排序并重新加载 Apache Cloudberry 表数据。"
weight: 230
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-utilities/gpreload.md"
---

## 概要 {#synopsis}

```shell
gpreload -d <database> [-p <port>] {-t | --table-file} <path_to_file> [-a]

gpreload -h 

gpreload --version
```

## 说明 {#description}

`gpreload` 工具将列数据排序后重新加载表数据。对于使用表存储选项 `appendoptimized=TRUE` 创建并启用压缩的表，按排序后的数据重新加载可以提高表的压缩率。在文本文件中指定要重新加载的表列表，以及要排序的表列。

如果某列的不同值数量相对于总行数较少，通过排序数据可以提高压缩率。

对于正在重新加载的表，待排序列的顺序可能影响压缩率。应优先列出不同值最少的列。例如，先列出 state，再列出 city，通常比先列出 city 再列出 state 能获得更好的压缩效果。

```shell
public.cust_table: state, city
public.cust_table: city, state
```

有关 `gpreload` 所用文件的格式，请参阅 `--table-file` 选项。

## 注意事项 {#notes}

为提高重新加载的性能，应在重新加载数据前删除相关表上的索引。

重新加载表数据后运行 `ANALYZE` 命令，可能会因重新加载的数据分布发生变化而影响查询性能。

对于每个表，此工具将表数据复制到临时表，截断现有表数据，再按指定排序顺序将临时表中的数据插回原表。每个表的重新加载都在单个事务中执行。

对于分区表，可以重新加载某个叶分区的数据。但是，数据通过根分区表插入，因此会对整个表获取 `ROW EXCLUSIVE` 锁。

## 选项 {#options}

**`-a (do not prompt)`**

可选。如果指定此选项，`gpreload` 工具不提示用户确认。

**`-d database`**

包含待重新加载表的数据库。`gpreload` 工具以运行该工具的用户身份连接数据库。

**`-p port`**

Apache Cloudberry Coordinator 端口。如果未指定，将使用 `PGPORT` 环境变量的值。如果无法获取该值，则返回错误。

**`{-t | --table-file } path_to_file`**

文件的位置和名称，其中列出 Apache Cloudberry 中要重新加载的表名（以模式限定）及要重新排序的列名。仅支持用户定义的表，不支持视图或系统目录表。

如果文件中列出的表定义了索引，`gpreload` 会提示是否继续。

每行指定一个表名及待排序列的列表。文件中每行的格式如下：

`schema.table_name: column [desc] [, column2 [desc] ... ]`

表名后跟冒号（:），然后是至少一个列名。如果指定多个列，列名之间用逗号分隔。各列按升序排序。在列名后指定关键字 `desc`，可按降序排序该列。

不支持通配符。

如果文件有错误，`gpreload` 会报告第一个错误并退出，不会重新加载任何数据。

以下示例重新加载三个表：

```shell
public.clients: region, state, rep_id desc
public.merchants: region, state
test.lineitem: group, assy, whse 
```

在第一个表 `public.clients` 中，`rep_id` 列的数据按降序排序，其他列的数据按升序排序。

**`--version (show utility version)`**

显示此工具的版本。

**`-? (help)`**

显示在线帮助。

## 示例 {#example}

以下示例命令重新加载数据库 `mytest` 中在文件 `data-tables.txt` 中列出的表。

```shell
gpreload -d mytest --table-file data-tables.txt
```

## 另请参阅 {#see-also}

[`CREATE TABLE`](/cloudberry/reference/sql-stmts/create-table/)
