---
title: "使用列级压缩"
description: "Apache Cloudberry 支持列级压缩，通过压缩指定列来减少存储空间占用。"
weight: 60
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/performance/use-columnar-compression.md"
---

在某些情况下，列级压缩还可以提高查询性能，特别是在处理大规模数据时。

## 使用场景 {#user-scenarios}

- **存储优化**：减少存储密集型应用的磁盘空间占用。
- **性能提升**：在列式查询场景中，更小的压缩数据块可以降低 I/O 代价。
- **高频数据分析**：降低大规模数据分析中的数据访问代价。

## 使用示例 {#example-usage}

以下简单示例展示了列级压缩在 Apache Cloudberry 中的效果。

1. 创建不使用列级压缩的表。

    ```sql
    CREATE TABLE no_column_compression (
        id serial PRIMARY KEY,
        data1 text,
        data2 text
    );
    ```

2. 创建使用列级压缩的表。

    ```sql
    CREATE TABLE column_compression (
        id serial PRIMARY KEY,
        data1 text ENCODING (compresstype=zlib, compresslevel=5),
        data2 text
    )
    WITH (
        appendoptimized=true,
        orientation=column
    );
    ```

3. 向不使用列级压缩的表插入数据。

    ```sql
    INSERT INTO no_column_compression (data1, data2)
    SELECT repeat(md5(random()::text), 10), repeat(md5(random()::text), 10)
    FROM generate_series(1, 100000);
    ```

4. 向使用列级压缩的表插入数据。

    ```sql
    INSERT INTO column_compression (data1, data2)
    SELECT repeat(md5(random()::text), 10), repeat(md5(random()::text), 10)
    FROM generate_series(1, 100000);
    ```

5. 检查不使用列级压缩的表的存储大小。

    ```sql
    SELECT pg_size_pretty(pg_total_relation_size('no_column_compression')) AS no_column_compression_size;
    ```

    示例结果：

    ```sql
    no_column_compression_size
    ---------------------------
    69 MB
    ```

6. 检查使用列级压缩的表的存储大小。

    ```sql
    SELECT pg_size_pretty(pg_total_relation_size('column_compression')) AS column_compression_size;
    ```

    示例结果：

    ```sql
    column_compression_size
    ------------------------
    36 MB
    ```

压缩表占用的存储空间明显少于未压缩表。在本例中，使用列级压缩的表将存储占用减少了近 50%。
