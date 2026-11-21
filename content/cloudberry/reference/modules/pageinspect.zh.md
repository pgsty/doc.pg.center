---
title: pageinspect
description: pageinspect 提供底层检查数据库页面内容的函数。
weight: 180
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/pageinspect.md
---

`pageinspect` 模块提供底层检查数据库页面内容的函数。只有超级用户可以使用这些函数。

Apache Cloudberry 的 `pageinspect` 模块基于 PostgreSQL 的 `pageinspect` 模块。两者的区别见 [MPP 注意事项](#mpp-considerations)和 [Apache Cloudberry 新增的函数](#functions-added-by-apache-cloudberry)。

## 安装并注册模块 {#install-and-register-the-module}

Apache Cloudberry 的默认构建会构建并安装 `pageinspect`。在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION pageinspect;
```

如果数据库中已注册旧版本的扩展，请更新以获得当前版本的函数：

```sql
ALTER EXTENSION pageinspect UPDATE;
```

## MPP 注意事项 {#mpp-considerations}

- `get_raw_page()` 不读取 AO 表的页面。它还会拒绝自身没有页面存储的关系，例如视图、外表和分区表。
- 从关系读取数据的函数只读取函数所在实例上的数据。例如，在普通会话中对用户表调用 `get_raw_page()` 时，函数在 Coordinator 上运行，而 Coordinator 不存储该表的数据，因此调用会报错 `block number 0 is out of range for relation "..."`。系统目录表可以在 Coordinator 上读取。

    要检查某个 Segment 上的页面，请在该 Segment 上运行函数，例如通过连接该 Segment 的 utility 模式连接执行。

## 函数 {#functions}

此模块提供 PostgreSQL 14 的 `pageinspect` 函数：

| 类别 | 函数 |
|-------|-----------|
| 通用 | `get_raw_page`, `page_header`, `page_checksum`, `fsm_page_contents` |
| 堆 | `heap_page_items`, `tuple_data_split`, `heap_page_item_attrs`, `heap_tuple_infomask_flags` |
| B-树 | `bt_metap`, `bt_page_stats`, `bt_page_items` |
| BRIN | `brin_page_type`, `brin_metapage_info`, `brin_revmap_data`, `brin_page_items` |
| GIN | `gin_metapage_info`, `gin_page_opaque_info`, `gin_leafpage_items` |
| GiST | `gist_page_opaque_info`, `gist_page_items`, `gist_page_items_bytea` |
| 哈希 | `hash_page_type`, `hash_page_stats`, `hash_page_items`, `hash_bitmap_info`, `hash_metapage_info` |

这些函数的详细信息，参见 PostgreSQL 文档中的 [pageinspect](https://www.postgresql.org/docs/14/pageinspect.html)。

## Apache Cloudberry 新增的函数 {#functions-added-by-apache-cloudberry}

### 位图索引函数 {#bitmap-index-functions}

| 函数 | 说明 |
|----------|-------------|
| `bm_metap(relname text) returns record` | 返回位图索引的元页面信息：`magic`、`version`、`auxrelid`、`auxindexrelid` 和 `lovlastblknum`。 |
| `bm_bitmap_page_header(relname text, blkno int) returns record` | 返回位图页面的头部信息：`num_words`、`next_blkno` 和 `last_tid`。 |
| `bm_lov_page_items(relname text, blkno int) returns setof record` | 返回位图 LOV 页面的值列表（LOV）条目。 |
| `bm_bitmap_page_items(relname text, blkno int) returns setof record` | 返回位图页面的内容字及每个字是否经过压缩：`word_num`、`compressed` 和 `content_word`。 |
| `bm_bitmap_page_items(page bytea) returns setof record` | 与上一个函数相同，但输入为通过 `get_raw_page()` 获取的页面镜像。 |

`bm_lov_page_items()` 返回以下列：`itemoffset`、`lov_head_blkno`、`lov_tail_blkno`、`last_complete_word`、`last_word`、`last_tid`、`last_setbit_tid`、`is_last_complete_word_fill` 和 `is_last_word_fill`。

### BRIN 函数 {#brin-functions}

Apache Cloudberry 支持在 AO 表上创建 BRIN 索引，`pageinspect` 也相应提供支持：

- `brin_metapage_info(page bytea)` 除 PostgreSQL 原有列之外，还返回四列：`isAO`（`boolean`）、`firstrevmappages`（`bigint[]`）、`lastrevmappages`（`bigint[]`）和 `lastrevmappagenums`（`bigint[]`）。这些数组描述 AO 表索引的范围映射链。
- `brin_revmap_chain(indexrelid regclass, segno int) returns bigint[]` 返回 AO 表某个段文件编号（块序列）的范围映射块号链。`segno` 必须在 0 到 127 之间。

## 示例 {#examples}

获取名为 `i1` 的位图索引的元页面信息：

```sql
SELECT * FROM bm_metap('i1');
```

显示位图索引 `i1` 的第二个块的头部信息：

```sql
SELECT * FROM bm_bitmap_page_header('i1', 2);
```

显示位图索引 `i1` 的第一个块中的 LOV 条目：

```sql
SELECT * FROM bm_lov_page_items('i1', 1) ORDER BY itemoffset;
```

返回位图索引 `i1` 第二个块中的内容字，可以按索引名和块号查询，也可以从页面镜像查询：

```sql
SELECT * FROM bm_bitmap_page_items('i1', 2) ORDER BY word_num;
SELECT * FROM bm_bitmap_page_items(get_raw_page('i1', 2)) ORDER BY word_num;
```
