---
title: "使用 gpload 向 Apache Cloudberry 加载数据"
linkTitle: "使用 gpload 加载数据"
description: "Apache Cloudberry 的 `gpload` 工具使用可读外部表和 Apache Cloudberry 并行文件服务器（gpfdist）加载数据。"
weight: 50
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/load-data-using-gpload.md"
---

gpload 负责设置基于文件的并行外部表，并允许用户在单个配置文件中配置数据格式、外部表定义和 gpfdist 设置。

> [!TIP]
> 在 `gpload` 中，如果目标表列名是保留关键字、包含大写字母，或包含任何需要使用引号 `" "` 才能标识列的字符，则不支持 `MERGE` 和 `UPDATE` 操作。

## 使用 gpload {#to-use-gpload}

1. 确保环境已设置为可以运行 `gpload`。需要使用 Apache Cloudberry 安装中的一些依赖文件，例如 gpfdist 和 Python 3，还需要能够访问 Apache Cloudberry Segment 主机。`gpload` 还要求安装以下软件包：

    ```shell
    pip install psycopg2 pyyaml
    ```

2. 创建加载控制文件。这是一个 YAML 格式的文件，用于指定 Apache Cloudberry 连接信息、gpfdist 配置信息、外部表选项和数据格式。

    例如：

    ```yaml
    ---
    VERSION: 1.0.0.1
    DATABASE: ops
    USER: gpadmin
    HOST: cdw-1
    PORT: 5432
    GPLOAD:
       INPUT:
        - SOURCE:
             LOCAL_HOSTNAME:
               - etl1-1
               - etl1-2
               - etl1-3
               - etl1-4
             PORT: 8081
             FILE: 
               - /var/load/data/*
        - COLUMNS:
               - name: text
               - amount: float4
               - category: text
               - descr: text
               - date: date
        - FORMAT: text
        - DELIMITER: '|'
        - ERROR_LIMIT: 25
        - LOG_ERRORS: true
       OUTPUT:
        - TABLE: payables.expenses
        - MODE: INSERT
       PRELOAD:
        - REUSE_TABLES: true 
    # SQL:
    #   - BEFORE: "INSERT INTO audit VALUES('start', current_timestamp)"
    #   - AFTER: "INSERT INTO audit VALUES('end', current_timestamp)"
    ```

3. 运行 `gpload`，并传入加载控制文件。例如：

    ```sql
    gpload -f my_load.yml
    ```
