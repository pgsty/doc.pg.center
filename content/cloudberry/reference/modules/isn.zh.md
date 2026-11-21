---
title: isn
description: isn 提供 EAN13、UPC、ISBN（图书）、ISMN（音乐）和 ISSN（连续出版物）国际产品编号标准的数据类型。
weight: 150
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/isn.md
---

`isn` 模块为 EAN13、UPC、ISBN（图书）、ISMN（音乐）和 ISSN（连续出版物）等国际产品编号标准提供数据类型。

Apache Cloudberry 的 `isn` 模块与 PostgreSQL 的 `isn` 模块等价，没有 MPP 特有的注意事项。

## 安装并注册模块 {#install-and-register-the-module}

`isn` 不属于 Apache Cloudberry 的默认构建目标（`make` 和 `make install`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/isn install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION isn;
```

## 模块文档 {#module-documentation}

此模块定义的数据类型、类型转换和函数的详细信息，参见 PostgreSQL 文档中的 [isn](https://www.postgresql.org/docs/14/isn.html)。
