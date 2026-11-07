---
title: 为 Citus 准备应用
description: 介绍如何调整应用，使其能够使用 Citus。
weight: 30
type: docs
upstream_source: citus
upstream_link: https://learn.microsoft.com/en-us/postgresql/citus/migrate/migration-query?view=citus-14
upstream_ref: citus-14; 4f3b88427ab7
translation_status: translated
---

[将现有应用迁移到 Citus](/citus/migration/migration/) 时，首先需要优化现有数据库模式。本文介绍接下来的一步：更新应用代码和查询，以适应这些模式变更。

## 搭建开发用 Citus 集群 {#set-up-development-citus-cluster}

修改应用以适配 Citus 时，需要一个数据库进行测试。请按照说明搭建所选的 `development` 环境。

接下来，从应用原有数据库导出一份模式，并在新的开发数据库中恢复。

```bash
# get schema from source db

pg_dump \
   --format=plain \
   --no-owner \
   --schema-only \
   --file=schema.sql \
   --schema=target_schema \
   postgres://user:pass@host:5432/db

# load schema into test db

psql postgres://user:pass@testhost:5432/db -f schema.sql
```

模式中所有需要分布的表都应包含分布键，即*租户 ID*。使用 pg_dump 导出模式前，务必完成[准备用于迁移的源表](/citus/migration/migration-schema/#prepare-source-tables-for-migration)这一步。

### 将分布列加入键中 {#include-distribution-column-in-keys}

只有唯一索引或主键包含分布列，Citus 才能强制执行唯一约束。因此，必须修改示例中的主键和外键，将 `store_id` 加入其中。

下一节列出的部分库可以协助迁移数据库模式，将分布列加入键中。下面展示底层 SQL 命令的示例，将开发数据库中的单列键改为复合键：

```sql
BEGIN;

-- drop simple primary keys (cascades to foreign keys)

ALTER TABLE products   DROP CONSTRAINT products_pkey CASCADE;
ALTER TABLE orders     DROP CONSTRAINT orders_pkey CASCADE;
ALTER TABLE line_items DROP CONSTRAINT line_items_pkey CASCADE;

-- recreate primary keys to include would-be distribution column

ALTER TABLE products   ADD PRIMARY KEY (store_id, product_id);
ALTER TABLE orders     ADD PRIMARY KEY (store_id, order_id);
ALTER TABLE line_items ADD PRIMARY KEY (store_id, line_item_id);

-- recreate foreign keys to include would-be distribution column

ALTER TABLE line_items ADD CONSTRAINT line_items_store_fkey
  FOREIGN KEY (store_id) REFERENCES stores (store_id);
ALTER TABLE line_items ADD CONSTRAINT line_items_product_fkey
  FOREIGN KEY (store_id, product_id) REFERENCES products (store_id, product_id);
ALTER TABLE line_items ADD CONSTRAINT line_items_order_fkey
  FOREIGN KEY (store_id, order_id) REFERENCES orders (store_id, order_id);

COMMIT;
```

完成后，上一节的模式如下图所示：

![示例多租户应用的部分模式，展示各表键之间的关系。](mt-after.png)

（带下划线的项目是主键，斜体项目是外键。）

务必同时修改数据流，为传入数据添加这些键。

## 将分布键加入查询 {#add-distribution-key-to-queries}

所有相关表都包含分布键后，应用还需要在查询中包含它。以下步骤应使用在开发环境中运行的应用副本，并以 Citus 为后端进行测试。应用可以正常使用 Citus 后，我们再介绍如何将源数据库中的生产数据迁移到实际的 Citus 集群。

- 更新向这些表写入数据的应用代码和其他摄入流程，使其包含新增的列。
- 针对 Citus 上修改后的模式运行应用测试套件，有助于确定哪些代码需要修改。
- 建议启用数据库日志。日志有助于找出多租户应用中遗漏的跨分片查询，这些查询应改为针对单个租户的查询。

Citus 支持跨分片查询，但多租户应用中的大多数查询应只访问一个节点。对于简单的 select、update 和 delete 查询，这意味着 *where* 子句应按租户 ID 过滤，Citus 就能在单个节点上高效执行这些查询。

许多常用应用框架都有辅助库，可以方便地将租户 ID 加入查询：

| 框架 | 资源 |
| --- | --- |
| Ruby on Rails | [Ruby on Rails 迁移指南](/citus/migration/migration-ruby-rails/) |
| Django | [Django Multitenant](https://django-multitenant.readthedocs.io/en/latest/migration_mt_django.html) |
| ASP.NET | [ASP.NET 迁移指南](/citus/migration/migration-asp/) |
| Java Hibernate | [使用 Hibernate 和 Spring 构建多租户 Java 应用](https://www.citusdata.com/blog/2018/02/13/using-hibernate-and-spring-to-build-multitenant-java-apps/) |

可以先将这些库用于数据库写入，包括数据摄入，之后再用于读取查询。例如，[activerecord-multi-tenant](https://github.com/citusdata/activerecord-multi-tenant) Gemfile 提供[只写模式](https://github.com/citusdata/activerecord-multi-tenant#rolling-out-activerecord-multi-tenant-for-your-application-write-only-mode)，只修改写入查询。

### 其他情况：SQL 原则 {#other-sql-principles}

如果使用上一节未列出的对象关系映射（ORM），或直接用 SQL 编写多租户查询，请遵循以下通用原则。

仍以前面的电商应用为例，假设需要获取某个订单的详细信息。在多租户应用中，按租户 ID 过滤的分布式查询执行效率最高。因此，下面的修改会加快查询，而两种写法返回的结果相同：

```sql
-- before
SELECT *
  FROM orders
 WHERE order_id = 123;

-- after
SELECT *
  FROM orders
 WHERE order_id = 123
   AND store_id = 42; -- <== added
```

对于插入语句，tenant_id 列不只是有帮助，更是必不可少。插入时必须提供 tenant_id 列的值，否则 Citus 无法将数据路由到正确的分片，并会报错。

最后，连接表时也务必按 tenant_id 过滤。例如，下面查询某家商店售出了多少件“Awesome Wool Pants”：

```sql
-- One way is to include store_id in the join and also
-- filter by it in one of the queries

SELECT sum(l.quantity)
  FROM line_items l
 INNER JOIN products p
    ON l.product_id = p.product_id
   AND l.store_id = p.store_id
 WHERE p.name='Awesome Wool Pants'
   AND l.store_id='8c69aa0d-3f13-4440-86ca-443566c1fc75'

-- Equivalently you omit store_id from the join condition
-- but filter both tables by it. This may be useful if
-- building the query in an ORM

SELECT sum(l.quantity)
  FROM line_items l
 INNER JOIN products p ON l.product_id = p.product_id
 WHERE p.name='Awesome Wool Pants'
   AND l.store_id='8c69aa0d-3f13-4440-86ca-443566c1fc75'
   AND p.store_id='8c69aa0d-3f13-4440-86ca-443566c1fc75'
```

## 启用安全连接 {#enable-secure-connections}

客户端应通过 TLS/SSL 连接 Citus，以保护信息并防范中间人攻击。

## 检查跨节点流量 {#check-for-cross-node-traffic}

对于庞大而复杂的应用代码库，应用生成的某些查询容易被遗漏，没有添加 tenant_id 过滤条件。Citus 的并行执行器仍能成功执行这些查询，因此应用在测试期间运行正常，问题也就没有暴露。然而，没有 tenant_id 过滤条件时，Citus 执行器会并行访问每个分片，却只有一个分片返回数据。这会无谓地消耗资源，可能直到进入吞吐量更高的生产环境才显现出问题。

为避免上线后才发现这类问题，可以配置 Citus，记录访问多个分片的查询。在配置和迁移正确的多租户应用中，每次查询应只访问一个分片。

测试期间，可以使用以下配置检测这类查询：

```sql
-- adjust for your own database's name of course

ALTER DATABASE citus SET citus.multi_task_query_log_level = 'error';
```

启用这一设置后，Citus 遇到将访问多个分片的查询就会报错。在测试中报错，有助于开发人员发现并迁移这些查询。

生产上线时，可以将同一参数配置为只记录日志，而不报错：

```sql
ALTER DATABASE citus SET citus.multi_task_query_log_level = 'log';
```

配置参数一节详细介绍了此设置支持的值。

## 相关内容 {#related-content}

- [迁移模式](/citus/migration/migration-schema/)
- [将现有应用迁移到 Citus](/citus/migration/migration/)
- [什么是 Citus？](/citus/overview/what-is-citus/)
