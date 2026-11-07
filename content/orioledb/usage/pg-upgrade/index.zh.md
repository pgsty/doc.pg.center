---
title: 使用 pg_upgrade 升级大版本
linkTitle: 大版本升级
description: 了解大版本升级时如何迁移 OrioleDB 文件并刷新索引表达式。
weight: 50
type: docs
search_keywords: ["OrioleDB", "pg upgrade", "pg_upgrade", "大版本升级"]
upstream_link: https://www.orioledb.com/docs/usage/pg-upgrade
upstream_source: orioledb
upstream_modified: true
translation_notice: en
upstream_notice: /zh/orioledb/attribution/
author: '[OrioleDB contributors](https://github.com/orioledb/orioledb/graphs/contributors) · 中文整理：[PGSTY](https://pgsty.com/)'
icon: fa-solid fa-arrow-up
---


`pg_upgrade` 通过复制系统目录和它能够识别的堆关系文件，将 PostgreSQL 集群就地迁移到新的大版本。但 OrioleDB 把表和索引数据存放在自己的 `orioledb_data/` 目录中，撤销日志存放在 `orioledb_undo/` 中；`pg_upgrade` 不会处理这些文件。OrioleDB 还在系统树中持久化了一些与版本相关的元数据。因此，升级 OrioleDB 集群需要额外执行两个标准 `pg_upgrade` 流程不会执行的手动步骤。

> [!NOTE]
>
> 升级前务必备份，并先在副本上执行以下步骤。复制文件时，两个集群都必须处于**停止**状态，旧集群必须已正常关闭。正常关闭时会执行最后一次检查点，因此复制的文件无需再重放 WAL。

## 操作步骤 {#procedure}

1. **正常停止旧集群**，照常运行 `pg_upgrade`，包括 `pg_upgrade --check`。此时 OrioleDB 表被恢复为空壳，数据仍在旧集群的 `orioledb_data/` 目录中。

2. **复制 OrioleDB 存储文件**，从旧数据目录复制到新数据目录。`pg_upgrade` 保留数据库 OID、关系 OID 和 relfilenode，而 OrioleDB 按 `(datoid, relnode)` 为文件命名，因此旧集群的文件无需修改即可用于新集群：

    ``` bash
    rm -rf "$NEW_DATA/orioledb_data" "$NEW_DATA/orioledb_undo"
    cp -R "$OLD_DATA/orioledb_data" "$NEW_DATA/orioledb_data"
    [ -d "$OLD_DATA/orioledb_undo" ] && \
        cp -R "$OLD_DATA/orioledb_undo" "$NEW_DATA/orioledb_undo"
    ```

3. **启动新集群。** 无需其他操作：升级后首次使用每个数据库时，OrioleDB 会**自动**把迁移过来的索引表达式重写为新服务器的格式。

    如果希望提前完成，例如在迁移脚本开放数据库流量前执行，可以**在每个使用 OrioleDB 的数据库中**显式触发同样的工作：

    ``` sql
    SELECT orioledb_upgrade_refresh();
    ```

## 表达式重写的工作方式 {#how-the-expression-rewrite-works}

OrioleDB 将索引**表达式**和**部分索引谓词**，以及它们调用的 SQL 函数的解析树，存储为序列化的 PostgreSQL 节点树。它还在自己的系统树中缓存与版本相关的目录数据，如元组描述符和数据库区域设置，使恢复进程和后台工作进程无需访问系统目录也能工作。这些格式**在不同大版本之间并不稳定**。跨大版本升级后，迁移过来的节点树由旧版本写入，新服务器无法解析；受影响的缓存也会被丢弃并重建。

重写过程从系统目录重新推导索引表达式和谓词，以当前服务器的格式保存，并重新填充所依赖的缓存。每个数据库首次使用时会自动运行，`orioledb_upgrade_refresh()` 则可以按需执行完全相同的工作。无论哪种方式，都只处理实际包含节点树的索引，即表达式索引和部分索引；普通索引无需重写。该操作可以安全地多次运行，没有需要重写的内容时不会执行任何操作。

> [!NOTE]
>
> 自动重写由数据库中第一条经过 utility 处理流程的语句触发。升级后连接数据库的工具，包括 `pg_dump`，会在会话启动时执行这样的语句。如果此前某个会话只对尚未重写的**表达式索引**或**部分索引**执行普通 `SELECT`，则会收到明确的错误信息，而不会崩溃；运行 `orioledb_upgrade_refresh()` 后即可继续：
>
> ```
> ERROR:  OrioleDB index "..." has expressions stored by another PostgreSQL major version
> HINT:   Run "SELECT orioledb_upgrade_refresh();" in this database before using the index.
> ```
>
> 没有此类索引的表不受影响，升级后可以立即使用。
