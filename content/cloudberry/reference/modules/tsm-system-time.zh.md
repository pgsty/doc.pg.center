---
title: tsm_system_time
description: tsm_system_time 实现 SELECT 的 TABLESAMPLE 子句可用的 SYSTEM_TIME 表采样方法。
weight: 270
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/tsm-system-time.md
---

`tsm_system_time` 模块实现 `SYSTEM_TIME` 表采样方法，可用于 `SELECT` 命令的 `TABLESAMPLE` 子句。

## 安装并注册模块 {#install-and-register-the-module}

`tsm_system_time` 不属于 Apache Cloudberry 的默认构建目标（`make` 和 `make install`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/tsm_system_time install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION tsm_system_time;
```

## 使用模块 {#use-the-module}

`SYSTEM_TIME` 采样方法接受一个浮点数参数，表示读取表最多使用的毫秒数。这样可以控制查询耗时，但样本大小难以预测。除非提前读完整张表，否则样本包含在指定时间内能读取的所有行。参数为负数时会报错。

与内置的 `SYSTEM` 采样方法一样，`SYSTEM_TIME` 按块采样，因此样本并非完全随机，可能受到聚集效应影响，尤其是在只选取少量行时。

`SYSTEM_TIME` 不支持 `REPEATABLE` 子句。

> [!NOTE]
> 在 Apache Cloudberry 中，每个 Segment 对分布式表中属于自己的部分进行采样，时间限制分别作用于每个 Segment。

## 示例 {#example}

以下命令从每个 Segment 返回其在 500 毫秒内能读取的尽可能多的 `tablea` 样本行。如果可以在更短时间内读完整张表，则返回所有行。

```sql
SELECT * FROM tablea TABLESAMPLE SYSTEM_TIME(500);
```

## 模块文档 {#module-documentation}

参见 PostgreSQL 文档中的 [tsm_system_time](https://www.postgresql.org/docs/14/tsm-system-time.html)。
