---
title: "使用 Kafka FDW 从 Kafka 加载数据"
description: "Kafka 外部数据包装器（FDW）允许 Apache Cloudberry 直接连接 Apache Kafka，从而将 Kafka 数据作为外表读取和处理。"
weight: 40
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-from-kafka-using-fdw.md"
---

此集成提升实时 Kafka 数据处理的效率、灵活性和可靠性，从而改善数据操作和业务性能。

Apache Cloudberry 支持使用 Kafka FDW 创建外表并导入数据。

如需更多信息，请参阅 Kafka FDW 仓库：[https://github.com/cloudberry-contrib/kafka_fdw](https://github.com/cloudberry-contrib/kafka_fdw)。请注意，该仓库由社区成员贡献，但 PPMC 并未将其作为官方社区项目维护。

## 基本用法 {#basic-usage}

- 创建 `kafka_fdw` 扩展：

    ``` sql
    CREATE EXTENSION kafka_fdw;
    ```

- 创建外部服务器并指定 Kafka 集群地址。你需要将 `localhost:9092` 替换为 Kafka 集群地址。

    ``` sql
    CREATE SERVER kafka_server
    FOREIGN DATA WRAPPER kafka_fdw
    OPTIONS (mpp_execute 'all segments', brokers 'localhost:9092');
    ```

- 创建用户映射：

    ``` sql
    CREATE USER MAPPING FOR PUBLIC SERVER kafka_server;
    ```

- 创建外表：

    创建外表时，需要指定两个元数据列：`partition` 和 `offset`，用于标识 Kafka 主题中消息的分区和偏移量。示例：

    ``` sql
    CREATE FOREIGN TABLE kafka_test (
        part int OPTIONS (partition 'true'),
        offs bigint OPTIONS (offset 'true'),
        some_int int,
        some_text text,
        some_date date,
        some_time timestamp
    )
    SERVER kafka_server OPTIONS
        (format 'csv', topic 'contrib_regress_csv', batch_size '1000', buffer_delay '1000');
    ```

    参数说明：

    - `batch_size`：一次从 Kafka 读取的数据量。
    - `buffer_delay`：从 Kafka 获取数据的超时时间。

## 支持的数据格式 {#supported-data-formats}

目前支持 `CSV` 和 `JSON` 数据格式。

## 查询 {#query}

你可以在查询中使用 `partition` 或 `offset` 列条件指定消息的分区和偏移量：

``` sql
SELECT * FROM kafka_test WHERE part = 0 AND offs > 1000 LIMIT 60;
```

你也可以指定多个条件：

``` sql
SELECT * FROM kafka_test WHERE (part = 0 AND offs > 100) OR (part = 1 AND offs > 300) OR (part = 3 AND offs > 700);
```

## 消息生产者 {#message-producer}

目前，Kafka FDW 支持将数据插入外表，充当 Kafka 的消息生产者。你只需使用 `INSERT` 语句。

``` sql
INSERT INTO kafka_test(part, some_int, some_text)
VALUES
    (0, 5464565, 'some text goes into partition 0'),
    (1, 5464565, 'some text goes into partition 1'),
    (0, 5464565, 'some text goes into partition 0'),
    (3, 5464565, 'some text goes into partition 3'),
    (NULL, 5464565, 'some text goes into partition selected by kafka');
```

插入数据时，可以使用 `partition` 指定要插入数据的分区。

## 数据导入 {#data-import}

要使用 Kafka FDW 导入数据，可以创建使用 `INSERT INTO SELECT` 等语句的自定义函数。基本原理是从外表中获取所有数据，然后依次将其插入目标表。

以下是一个简单示例，你可以根据需要修改：

``` sql
CREATE OR REPLACE FUNCTION import_kafka_data(
  src_table_name text,
  dest_table_name text,
  dest_table_columns text[]
) RETURNS void AS $$

DECLARE
    current_row RECORD;
    current_part integer;
    current_offs bigint;
    max_off bigint;
    import_progress_table_name text;
    max_off_result bigint;
BEGIN

    import_progress_table_name := src_table_name || '_import_progress';

    -- Creates progress record table.
    EXECUTE FORMAT('CREATE TABLE IF NOT EXISTS %I (part integer PRIMARY KEY, offs bigint NOT NULL)', import_progress_table_name);

    -- The number of partitions in the topic table might change, so reinitialize before each import.
    EXECUTE FORMAT('INSERT INTO %I SELECT DISTINCT part, 0 FROM %I ON CONFLICT (part) DO NOTHING', import_progress_table_name, src_table_name);

    -- Imports data partition by partition.
    FOR current_row IN
        EXECUTE FORMAT('SELECT part, offs FROM %I', import_progress_table_name)
    LOOP
        current_part := current_row.part;
        current_offs := current_row.offs;

        -- Gets the maximum offset for the current partition.
        EXECUTE FORMAT('SELECT MAX(offs) FROM %I WHERE part = %s', src_table_name, current_part) INTO max_off_result;
        max_off := max_off_result;

        -- Skips if there is no new data.
        IF max_off+1 = current_offs THEN
            CONTINUE;
        END IF;

        -- Imports data.
        EXECUTE FORMAT('
            INSERT INTO %I (%s)
            SELECT %s
            FROM %I
            WHERE part = %s AND offs >= %s AND offs <= %s',
            dest_table_name,
            array_to_string(dest_table_columns, ', '),
            array_to_string(dest_table_columns, ', '),
            src_table_name,
            current_part,
            current_offs,
            max_off
        );        

        -- Updates import progress.
        EXECUTE FORMAT('UPDATE %I SET offs = %s WHERE part = %s', import_progress_table_name, max_off + 1, current_part);
    END LOOP;

    RETURN;
END;
$$ LANGUAGE plpgsql;
```

执行查询时，调用此函数，并传入外表名、目标表名和要导入的字段。示例：

``` sql
SELECT import_kafka_data('kafka_test', 'dest_table_fdw', ARRAY['some_int', 'some_text', 'some_date', 'some_time']);
```
