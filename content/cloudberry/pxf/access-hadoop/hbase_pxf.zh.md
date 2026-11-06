---
title: "读取 HBase 表数据"
description: "使用 PXF 读取 HBase 表数据。"
weight: 100
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-hadoop/hbase_pxf.md"
---

Apache HBase 是建立在 Hadoop 之上的分布式、带版本的非关系型数据库。

PXF HBase 连接器读取存储在 HBase 表中的数据。HBase 连接器支持过滤条件下推。

本节介绍如何使用 PXF HBase 连接器。

## 前提条件 {#prerequisites}

在处理 HBase 表数据之前，请确保您已经：

- 将 `<PXF_INSTALL_DIR>/share/pxf-hbase-*.jar` 复制到 HBase 集群中的每个节点，并且该 PXF JAR 文件的位置位于 `$HBASE_CLASSPATH` 中。PXF HBase 连接器需要此配置才能支持过滤条件下推。
- 满足 PXF Hadoop [前提条件](/cloudberry/pxf/access-hadoop/#prerequisites)。

## HBase 入门 {#hbase-primer}

本主题假定您已基本了解以下 HBase 概念：
 
- HBase 列包含两个部分：列族和列限定符。这两个部分以冒号 `:` 字符分隔，即 \<column-family\>:\<column-qualifier\>。
- HBase 行由一个行键和一个或多个列值组成。行键是表中某一行的唯一标识符。
- HBase 表是由一列或多列以及若干行数据构成的多维映射。创建 HBase 表时，需要指定完整的列族集合。
- HBase 单元格由一行（列族、列限定符、列值）和一个时间戳组成。给定单元格中的列值和时间戳表示该值的一个版本。

有关 HBase 的详细信息，请参阅 [Apache HBase Reference Guide](http://hbase.apache.org/book.html)。

## HBase Shell {#hbase-shell}

HBase shell 是一个类似于 `psql` 的子系统。启动 HBase shell 的方法如下：

```shell
$ hbase shell
<hbase output>
hbase(main):001:0>
```

默认的 HBase 命名空间名为 `default`。 

### 示例：创建 HBase 表 {#example-creating-an-hbase-table}

创建一个示例 HBase 表。

1. 在 `default` 命名空间中创建名为 `order_info` 的 HBase 表。`order_info` 有两个列族：`product` 和 `shipping_info`：

    ```text
    hbase(main):> create 'order_info', 'product', 'shipping_info'
    ```

2. `order_info` 的 `product` 列族包含名为 `name` 和 `location` 的限定符。`shipping_info` 列族包含名为 `state` 和 `zipcode` 的限定符。向 `order_info` 表中添加一些数据：

    ```text
    put 'order_info', '1', 'product:name', 'tennis racquet'
    put 'order_info', '1', 'product:location', 'out of stock'
    put 'order_info', '1', 'shipping_info:state', 'CA'
    put 'order_info', '1', 'shipping_info:zipcode', '12345'
    put 'order_info', '2', 'product:name', 'soccer ball'
    put 'order_info', '2', 'product:location', 'on floor'
    put 'order_info', '2', 'shipping_info:state', 'CO'
    put 'order_info', '2', 'shipping_info:zipcode', '56789'
    put 'order_info', '3', 'product:name', 'snorkel set'
    put 'order_info', '3', 'product:location', 'warehouse'
    put 'order_info', '3', 'shipping_info:state', 'OH'
    put 'order_info', '3', 'shipping_info:zipcode', '34567'
    ```
    
    在本主题后面的示例中，您将通过 PXF 直接访问 `orders_info` HBase 表。

3. 显示 `order_info` 表的内容：

    ```text
    hbase(main):> scan 'order_info'
    ROW     COLUMN+CELL                                               
     1      column=product:location, timestamp=1499074825516, value=out of stock                                                
     1      column=product:name, timestamp=1499074825491, value=tennis racquet                                                  
     1      column=shipping_info:state, timestamp=1499074825531, value=CA                                                       
     1      column=shipping_info:zipcode, timestamp=1499074825548, value=12345                                                  
     2      column=product:location, timestamp=1499074825573, value=on floor    
     ... 
    3 row(s) in 0.0400 seconds                                         
    ```

## 查询外部 HBase 数据 {#querying-external-hbase-data}

PXF HBase 连接器支持名为 `hbase` 的单个 Profile。

使用以下语法创建引用 HBase 表的 Apache Cloudberry 外部表：

```sql
CREATE EXTERNAL TABLE <table_name>
    ( <column_name> <data_type> [, ...] | LIKE <other_table> )
LOCATION ('pxf://<hbase-table-name>?PROFILE=hbase[&SERVER=<server_name>]')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

Apache Cloudberry [CREATE EXTERNAL TABLE](/cloudberry/reference/sql-stmts/create-external-table/) 调用中使用的 HBase 连接器专用关键字及取值说明如下。

| 关键字  | 取值 |
|-------|-------------------------------------|
| \<hbase&#8209;table&#8209;name\>    | HBase 表的名称。 |
| PROFILE    | `PROFILE` 关键字必须指定为 `hbase`。 |
| SERVER=\<server_name\>    | PXF 用于访问数据的命名服务器配置。如果未指定，PXF 使用 `default` 服务器。 |
| FORMAT  | `FORMAT` 子句必须指定为 `'CUSTOM' (FORMATTER='pxfwritable_import')`。   |



## 数据类型映射 {#data-type-mapping}

HBase 是基于字节的；它将所有数据类型存储为字节数组。要在 Apache Cloudberry 中表示 HBase 数据，请为 Apache Cloudberry 列选择与 HBase 列限定符取值的底层内容相匹配的数据类型。

**注意**：PXF 不支持复杂的 HBase 对象。


## 列映射 {#column-mapping}

您可以创建引用 HBase 表中定义的全部或部分列限定符的 Apache Cloudberry 外部表。PXF 支持在 Apache Cloudberry 表列与 HBase 表列限定符之间进行直接映射或间接映射。

### 直接映射 {#direct-mapping}

使用直接映射将 Apache Cloudberry 外部表的列名映射到 HBase 限定符时，需要将带列族限定的 HBase 限定符名称指定为带引号的值。PXF HBase 连接器在读取表数据时，会将这些列名原样传递给 HBase。

例如，要创建一个 Apache Cloudberry 外部表，访问您在[示例：创建 HBase 表](#example-creating-an-hbase-table)中创建的 `order_info` HBase 表中的以下数据：

-   名为 `product` 的列族中的限定符 `name`
-   名为 `shipping_info` 的列族中的限定符 `zipcode` 

请使用如下 `CREATE EXTERNAL TABLE` 语法：

```sql
CREATE EXTERNAL TABLE orderinfo_hbase ("product:name" varchar, "shipping_info:zipcode" int)
    LOCATION ('pxf://order_info?PROFILE=hbase')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

### 通过查找表间接映射 {#indirect-mapping-via-lookup-table}

使用间接映射将 Apache Cloudberry 外部表的列名映射到 HBase 限定符时，需要在您于 HBase 中创建的查找表里指定映射。查找表将 \<column-family\>:\<column-qualifier\> 映射为您在创建 Apache Cloudberry 外部表时指定的列名别名。 

必须将 HBase PXF 查找表命名为 `pxflookup`，并且必须使用名为 `mapping` 的单个列族来定义该表。例如：

```text
hbase(main):> create 'pxflookup', 'mapping'
```

直接映射方法快速且直观，而使用间接映射则允许您为 HBase 的 \<column-family\>:\<column-qualifier\> 名称创建更短的、基于字符的别名。出于以下原因，这样可以更好地协调 HBase 列限定符名称与 Apache Cloudberry：

-   HBase 限定符名称可能非常长。Apache Cloudberry 对列名的长度限制为 63 个字符。
-   HBase 限定符名称可能包含二进制或不可打印字符。Apache Cloudberry 的列名是基于字符的。

向 `pxflookup` HBase 表填充数据时，请添加行，使得：

- 行键指定 HBase 表名
- `mapping` 列族限定符标识 Apache Cloudberry 的列名，其值标识您要为其创建别名的 HBase `<column-family>:<column-qualifier>`。

例如，要对 `order_info` 表使用间接映射，请向 `pxflookup` 表添加以下条目：

```text
hbase(main):> put 'pxflookup', 'order_info', 'mapping:pname', 'product:name'
hbase(main):> put 'pxflookup', 'order_info', 'mapping:zip', 'shipping_info:zipcode'
```

然后使用以下 `CREATE EXTERNAL TABLE` 语法创建 Apache Cloudberry 外部表：

```sql
CREATE EXTERNAL TABLE orderinfo_map (pname varchar, zip int)
    LOCATION ('pxf://order_info?PROFILE=hbase')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

## 行键 {#row-key}

HBase 表的行键是表中某一行的唯一标识符。PXF 对行键进行特殊处理。 

要在 Apache Cloudberry 外部表查询中使用行键，请使用 PXF 保留列名 `recordkey.` 来定义外部表。`recordkey` 列名指示 PXF 为每一行返回 HBase 表的记录键。

请使用 Apache Cloudberry 数据类型 `bytea` 来定义 `recordkey`。

例如：

```sql
CREATE EXTERNAL TABLE <table_name> (recordkey bytea, ... ) 
    LOCATION ('pxf://<hbase_table_name>?PROFILE=hbase')
    FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
```

创建外部表之后，可以在 `WHERE` 子句中使用 `recordkey`，按行键值范围过滤 HBase 表。

**注意**：要对 `recordkey` 启用过滤条件下推，请将该字段定义为 `text`。
