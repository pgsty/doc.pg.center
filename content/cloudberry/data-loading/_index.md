---
title: "Data Loading Overview"
linkTitle: "Load Data"
description: "Apache Cloudberry loads data mainly by transforming external data into external tables (or foreign tables) via loading tools."
weight: 50
icon: "fa-solid fa-file-import"
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/data-loading/index.md"
---

Then it reads data from these external tables or writes data into them to achieve external data loading.

## Loading process {#loading-process}

The general process of loading external data into Apache Cloudberry is as follows:

1. Assess the data loading scenario (such as data source location, data type, and data volume) and select an appropriate loading tool.
2. Set up and enable the loading tool.
3. Create an external table, specifying information such as the protocol of the loading tool, data source address, data format in the `CREATE EXTERNAL TABLE` statement.
4. Once the external table is created, data from the external table can be queried directly using the `SELECT` statement, or data can be imported from the external table using `INSERT INTO SELECT`.

## Loading methods and scenarios {#loading-methods-and-scenarios}

Apache Cloudberry offers multiple data loading solutions, and you can select different data loading methods according to different data sources.

| Loading method              | Data source                                                 | Data format                                                  | Parallel or not |
| -------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------ | -------- |
| [`copy`](/cloudberry/data-loading/files/load-data-using-copy/)                     | Local file system<br /><br />• Coordinator node host (for a single file)<br />• Segment node host (for multiple files) | • TXT<br />• CSV<br />• Binary                                             | No       |
| [`file://` protocol](/cloudberry/data-loading/files/load-data-using-file-protocol/)         | Local file system (local segment host, accessible only by superuser) | • TXT<br />• CSV                                             | Yes      |
| [`gpfdist`](/cloudberry/data-loading/files/load-data-using-gpfdist/)    | Local host files or files accessible via internal network   | • TXT<br />• CSV<br />• Any delimited text format supported by the `FORMAT` clause<br />• XML and JSON (requires conversion to text format via YAML configuration file) | Yes      |
| [`gpfdists`](/cloudberry/data-loading/files/load-data-using-gpfdists/) (secure `gpfdist`) | Local host files or files accessible via internal network (with SSL encryption)   | • TXT<br />• CSV<br />• Any delimited text format supported by the `FORMAT` clause<br />• XML and JSON (requires conversion to text format via YAML configuration file) | Yes      |
| [Batch loading using `gpload`](/cloudberry/data-loading/files/load-data-using-gpload/) (with `gpfdist` as the underlying worker) | Local host files or files accessible via internal network   | • TXT<br />• CSV<br />• Any delimited text format supported by the `FORMAT` clause<br />• XML and JSON (require conversion to text format via YAML configuration file) | Yes      |
| [`s3://` protocol](/cloudberry/data-loading/cloud/load-data-from-s3/)         | Amazon S3 and S3-compatible object stores | • TXT<br />• CSV<br />• Any delimited text format supported by the `FORMAT` clause                                             | Yes      |
| [`pxf://` protocol](/cloudberry/data-loading/cloud/load-data-using-pxf/)         | Object stores (S3, Azure, GCS), Hadoop systems (HDFS, Hive, HBase), SQL databases | • Text<br />• Avro<br />• JSON<br />• Parquet<br />• ORC<br />• CSV                                             | Yes      |
| [Create external web tables](/cloudberry/data-loading/load-data-from-web-services/)         | Data pulled from network services or from any source accessible by command lines | • TXT<br />• CSV                                             | Yes      |
| [Kafka FDW](/cloudberry/data-loading/load-data-from-kafka-using-fdw/)         | Streaming data from Apache Kafka | • JSON<br />• CSV                                             | No      |

## Learn more {#learn-more}
