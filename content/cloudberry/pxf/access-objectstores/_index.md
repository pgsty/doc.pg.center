---
title: "Accessing Azure, Google Cloud Storage, and S3-Compatible Object Stores"
linkTitle: "Accessing Object Stores with PXF"
description: "Accessing Azure, Google Cloud Storage, MinIO, and S3 object stores with PXF."
weight: 60
upstream_link: "https://github.com/apache/cloudberry-pxf/blob/dff2632d2a364f466b83682439c3ae97e655c1b7/docs/access-objectstores/access_objstore.md"
---

<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

PXF is installed with connectors to Azure Blob Storage, Azure Data Lake Storage Gen2, Google Cloud Storage, AWS, MinIO, and Dell ECS S3-compatible object stores.

## Prerequisites {#prerequisites}

Before working with object store data using PXF, ensure that:

- You have configured PXF, and PXF is running on each Apache Cloudberry host. See [Configuring PXF](/cloudberry/pxf/administering/configuring/) for additional information.
- You have configured the PXF Object Store Connectors that you plan to use. Refer to [Configuring Connectors to Azure and Google Cloud Storage Object Stores](/cloudberry/pxf/administering/configuring/objstore_cfg/) and [Configuring Connectors to MinIO, AWS S3, and Dell ECS Object Stores](/cloudberry/pxf/administering/configuring/s3_objstore_cfg/) for instructions.
- Time is synchronized between the Apache Cloudberry hosts and the external object store systems.


## Connectors, Data Formats, and Profiles {#connectors-data-formats-and-profiles}

The PXF object store connectors provide built-in profiles to support the following data formats:

- Text
- CSV
- Avro
- JSON
- ORC
- Parquet
- AvroSequenceFile
- SequenceFile

The PXF connectors to Azure expose the following profiles to read, and in many cases write, these supported data formats.

>**Note**:
>ADL support has been deprecated. Use the ABFSS profile instead.

| Data Format | Azure Blob Storage | Azure Data Lake Storage Gen2 | Supported Operations |
|-----|------|---------| ---------|
| delimited single line [plain text](/cloudberry/pxf/access-objectstores/objstore_text/) | wasbs:text | abfss:text | Read, Write |
| delimited single line comma-separated values of [plain text](/cloudberry/pxf/access-objectstores/objstore_text/) | wasbs:csv | abfss:csv | Read, Write |
| multi-byte or multi-character delimited single line [csv](/cloudberry/pxf/access-objectstores/objstore_text/#about-reading-data-containing-multi-byte-or-multi-character-delimiters) | wasbs:csv | abfss:csv | Read |
| delimited [text with quoted linefeeds](/cloudberry/pxf/access-objectstores/objstore_text/) | wasbs:text:multi | abfss:text:multi | Read |
| fixed width single line [text](/cloudberry/pxf/access-objectstores/objstore_fixedwidth/) | wasbs:fixedwidth | abfss:fixedwidth | Read, Write |
| [Avro](/cloudberry/pxf/access-objectstores/objstore_avro/) | wasbs:avro | abfss:avro | Read, Write |
| [JSON](/cloudberry/pxf/access-objectstores/objstore_json/) | wasbs:json | abfss:json | Read, Write |
| [ORC](/cloudberry/pxf/access-objectstores/objstore_orc/) | wasbs:orc | abfss:orc | Read, Write |
| [Parquet](/cloudberry/pxf/access-objectstores/objstore_parquet/) | wasbs:parquet | abfss:parquet | Read, Write |
| AvroSequenceFile | wasbs:AvroSequenceFile | abfss:AvroSequenceFile | Read, Write |
| [SequenceFile](/cloudberry/pxf/access-objectstores/objstore_seqfile/) | wasbs:SequenceFile | abfss:SequenceFile | Read, Write |

Similarly, the PXF connectors to Google Cloud Storage, and S3-compatible object stores expose these profiles:

| Data Format | Google Cloud Storage | AWS S3, MinIO, or Dell ECS | Supported Operations |
|-----|------|---------| ---------|
| delimited single line [plain text](/cloudberry/pxf/access-objectstores/objstore_text/) | gs:text | s3:text | Read, Write |
| delimited single line comma-separated values of [plain text](/cloudberry/pxf/access-objectstores/objstore_text/) | gs:csv | s3:csv | Read, Write |
| multi-byte or multi-character delimited single line comma-separated values [csv](/cloudberry/pxf/access-objectstores/objstore_text/#about-reading-data-containing-multi-byte-or-multi-character-delimiters) | gs:csv | s3:csv | Read |
| delimited [text with quoted linefeeds](/cloudberry/pxf/access-objectstores/objstore_text/) | gs:text:multi | s3:text:multi | Read |
| fixed width single line [text](/cloudberry/pxf/access-objectstores/objstore_fixedwidth/) | gs:fixedwidth | s3:fixedwidth | Read, Write |
| [Avro](/cloudberry/pxf/access-objectstores/objstore_avro/) | gs:avro | s3:avro | Read, Write |
| [JSON](/cloudberry/pxf/access-objectstores/objstore_json/) | gs:json | s3:json | Read|
| [ORC](/cloudberry/pxf/access-objectstores/objstore_orc/) | gs:orc | s3:orc | Read, Write |
| [Parquet](/cloudberry/pxf/access-objectstores/objstore_parquet/) | gs:parquet | s3:parquet | Read, Write |
| AvroSequenceFile | gs:AvroSequenceFile | s3:AvroSequenceFile | Read, Write |
| [SequenceFile](/cloudberry/pxf/access-objectstores/objstore_seqfile/) | gs:SequenceFile | s3:SequenceFile | Read, Write |

You provide the profile name when you specify the `pxf` protocol on a `CREATE EXTERNAL TABLE` command to create an Apache Cloudberry external table that references a file or directory in the specific object store.

## Sample CREATE EXTERNAL TABLE Commands {#sample-create-external-table-commands}

> <b>Note:</b> When you create an external table that references a file or directory in an object store, you must specify a `SERVER` in the `LOCATION` URI.

The following command creates an external table that references a text file on S3. It specifies the profile named `s3:text` and the server configuration named `s3srvcfg`:

<pre>
CREATE EXTERNAL TABLE pxf_s3_text(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://S3_BUCKET/pxf_examples/pxf_s3_simple.txt?<b>PROFILE=s3:text&SERVER=s3srvcfg</b>')
FORMAT 'TEXT' (delimiter=E',');
</pre>

The following command creates an external table that references a text file on Azure Blob Storage. It specifies the profile named `wasbs:text` and the server configuration named `wasbssrvcfg`. You would provide the Azure Blob Storage container identifier and your Azure Blob Storage account name.

<pre>
CREATE EXTERNAL TABLE pxf_wasbs_text(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://<b>AZURE_CONTAINER@YOUR_AZURE_BLOB_STORAGE_ACCOUNT_NAME</b>.blob.core.windows.net/path/to/blob/file?<b>PROFILE=wasbs:text&SERVER=wasbssrvcfg</b>')
FORMAT 'TEXT';
</pre>

The following command creates an external table that references a text file on Azure Data Lake Storage Gen2. It specifies the profile named `abfss:text` and the server configuration named `abfsssrvcfg`. You would provide your Azure Data Lake Storage Gen2 account name.

<pre>
CREATE EXTERNAL TABLE pxf_abfss_text(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://<b>YOUR_ABFSS_ACCOUNT_NAME</b>.dfs.core.windows.net/path/to/file?<b>PROFILE=abfss:text&SERVER=abfsssrvcfg</b>')
FORMAT 'TEXT';
</pre>

The following command creates an external table that references a JSON file on Google Cloud Storage. It specifies the profile named `gs:json` and the server configuration named `gcssrvcfg`:

<pre>
CREATE EXTERNAL TABLE pxf_gsc_json(location text, month text, num_orders int, total_sales float8)
  LOCATION ('pxf://dir/subdir/file.json?<b>PROFILE=gs:json&SERVER=gcssrvcfg</b>')
FORMAT 'CUSTOM' (FORMATTER='pxfwritable_import');
</pre>
