---
title: "使用 file:// 协议向 Apache Cloudberry 加载数据"
linkTitle: "使用 file 协议加载数据"
description: "`file://` 协议是 Apache Cloudberry 特有的协议，允许你从本地 Segment 主机上的文件向 Apache Cloudberry 加载数据。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-using-file-protocol.md"
---

`file://` 协议用于指定操作系统文件位置的 URI。使用 `file://` 协议创建的外部表是只读表。

URI 包含主机名、端口和文件路径。每个文件都必须位于 Segment 主机上，并且位于 Apache Cloudberry 超级用户（`gpadmin`）可以访问的位置。URI 中使用的主机名必须与 `gp_segment_configuration` 系统目录表中注册的 Segment 主机名匹配。

如[使用示例](#usage-examples)所示，`LOCATION` 子句可以包含多个 URI。

你在 `LOCATION` 子句中指定的 URI 数量，就是将并行访问外部表的 Segment 实例数量。对于每个 URI，Apache Cloudberry 会将指定主机上的一个主 Segment 分配给该文件。要在加载数据时实现最大并行度，请将数据拆分为大小相等的文件，文件数量与主 Segment 数量相同。这样可以确保所有 Segment 都参与加载。每个 Segment 主机上的外部文件数量不能超过该主机上的主 Segment 实例数量。例如，如果你的阵列中每个 Segment 主机有 4 个主 Segment 实例，则可以在每个 Segment 主机上放置 4 个外部文件。基于 `file://` 协议的表只能是可读表。

系统视图 `pg_max_external_files` 显示每个外部表允许使用的外部表文件数量。使用 `file://` 协议时，该视图列出每个 Segment 主机上的可用文件槽位。该视图仅适用于 `file://` 协议。例如：

```sql
SELECT * FROM pg_max_external_files;
```

## 使用示例 {#usage-examples}

以 CSV 格式加载多个带标题行的文件：

使用 `file` 协议创建可读外部表 `ext_expenses`。文件为 CSV 格式，并包含标题行。

```sql
=# CREATE EXTERNAL TABLE ext_expenses ( name text, 
   date date,  amount float4, category text, desc1 text ) 
   LOCATION ('file://filehost/data/international/*', 
             'file://filehost/data/regional/*',
             'file://filehost/data/supplement/*.csv')
   FORMAT 'CSV' (HEADER);
```

```sql
CREATE EXTERNAL TABLE ext_expenses (
   name text, date date, amount float4, category text, desc1 text ) 
LOCATION ('file://host1:5432/data/expense/*.csv', 
          'file://host2:5432/data/expense/*.csv', 
          'file://host3:5432/data/expense/*.csv') 
FORMAT 'CSV' (HEADER);
```
