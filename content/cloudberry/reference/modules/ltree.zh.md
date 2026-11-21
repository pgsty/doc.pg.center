---
title: ltree
description: ltree 用于表示分层树状结构中的数据标签，并支持标签树搜索。
weight: 160
upstream_link: https://github.com/apache/cloudberry-site/blob/e3a102d15d0e85928a0cb5aaec24e67e6b40be7c/versioned_docs/version-2.x/modules/ltree.md
---

`ltree` 模块实现名为 `ltree` 的数据类型，用于表示以分层树状结构存储的数据的标签。此模块还提供了丰富的标签树搜索功能。

Apache Cloudberry 的 `ltree` 模块基于 PostgreSQL 的 `ltree` 模块。两者的区别见 [MPP 注意事项](#mpp-considerations)。

## 安装并注册模块 {#install-and-register-the-module}

`ltree` 不属于 Apache Cloudberry 的默认构建目标（`make` 和 `make install`）。如果 `CREATE EXTENSION` 报告该扩展不可用，请使用配置当前安装版本时所用的 Apache Cloudberry 源码树，构建并安装此模块：

```shell
make -C contrib/ltree install
```

集群的每台主机（Coordinator、Standby Coordinator 及所有 Segment 主机）上都必须有模块文件。`make install-world` 也会安装此模块。

然后在每个需要使用它的数据库中注册扩展：

```sql
CREATE EXTENSION ltree;
```

## MPP 注意事项 {#mpp-considerations}

此扩展不为 `ltree` 数据类型提供哈希操作符类，因此不能将 `ltree` 列用作表的分布键。如果表只有一个 `ltree` 类型的列，则创建时采用随机分布。

## 模块文档 {#module-documentation}

此模块定义的数据类型、操作符和函数的详细信息，参见 PostgreSQL 文档中的 [ltree](https://www.postgresql.org/docs/14/ltree.html)。
