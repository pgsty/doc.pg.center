---
title: 小型数据库迁移
description: 介绍将小型 PostgreSQL 数据库迁移到 Microsoft Azure 上的 Citus 集群所需的步骤。
weight: 50
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-data-small?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

对于规模较小、能够容忍短暂停机的环境，可以采用简单直接的 pg_dump/pg_restore 流程。步骤如下。

1. 从开发数据库中导出数据库结构：

   ```bash
   pg_dump \
      --format=plain \
      --no-owner \
      --schema-only \
      --file=schema.sql \
      --schema=target_schema \
      postgres://user:pass@host:5432/db
   ```
2. 使用 psql 连接到 Citus 集群并创建模式：

   ```psql
   \i schema.sql
   ```
3. 执行 `create_distributed_table` 和 `create_reference_table` 语句。如果遇到外键错误，通常是操作顺序所致。应先删除外键，再分布表，最后重新添加外键。
4. 将应用切换到维护模式，并禁止对旧数据库的任何其他写入。
5. 使用 `pg_dump` 将原生产数据库的数据导出到磁盘：

   ```bash
   pg_dump \
      --format=custom \
      --no-owner \
      --data-only \
      --file=data.dump \
      --schema=target_schema \
      postgres://user:pass@host:5432/db
   ```
6. 使用 `pg_restore` 将数据导入 Citus：

   ```bash
   # remember to use connection details for Citus,
   # not the source database
   pg_restore  \
      --host=host \
      --dbname=dbname \
      --username=username \
      data.dump
   
   # it'll prompt you for the connection password
   ```
7. 测试应用。
8. 上线！

## 相关内容 {#related-content}

- [数据迁移](/citus/migration/migration-data/)
- [使用复制迁移大型数据库](/citus/migration/migration-data-big/)
- [迁移概述](/citus/migration/migration/)
