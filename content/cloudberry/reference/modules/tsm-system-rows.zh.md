---
title: tsm_system_rows
description: tsm_system_rows 实现 SELECT 的 TABLESAMPLE 子句可用的 SYSTEM_ROWS 表采样方法。
weight: 260
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/tsm-system-rows.md
---

`tsm_system_rows` 模块实现 `SYSTEM_ROWS` 表采样方法，可用于 `SELECT` 命令的 `TABLESAMPLE` 子句。

## 安装并注册模块 {#install-and-register-the-module}

`tsm_system_rows` 不属于 Apache Cloudberry 的默认构建目标（`make` 和 `make install`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/tsm_system_rows install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION tsm_system_rows;
```

## 使用模块 {#use-the-module}

`SYSTEM_ROWS` 采样方法接受一个整数（`bigint`）参数，表示最多读取的行数。如果表中的行数不足，则选取整张表。参数为负数时会报错。

与内置的 `SYSTEM` 采样方法一样，`SYSTEM_ROWS` 按块采样，因此样本并非完全随机，可能受到聚集效应影响，尤其是在只请求少量行时。

`SYSTEM_ROWS` 不支持 `REPEATABLE` 子句。

> [!NOTE]
> 在 Apache Cloudberry 中，每个 Segment 对分布式表中属于自己的部分进行采样，行数限制分别作用于每个 Segment。因此，对分布式表的查询最多可以从每个 Segment 返回指定数量的行。例如，在具有三个主 Segment 的集群上，`SYSTEM_ROWS(75)` 最多返回 225 行。

## 示例 {#example}

以下命令从每个 Segment 上的 `tablea` 表中返回最多 75 行的样本：

```sql
SELECT * FROM tablea TABLESAMPLE SYSTEM_ROWS(75);
```

## 模块文档 {#module-documentation}

参见 PostgreSQL 文档中的 [tsm_system_rows](https://www.postgresql.org/docs/14/tsm-system-rows.html)。
