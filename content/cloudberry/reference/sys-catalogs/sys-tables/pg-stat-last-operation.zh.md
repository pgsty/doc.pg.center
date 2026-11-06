---
title: "pg_stat_last_operation"
description: "pg_stat_last_operation 表包含用于跟踪表、视图等数据库对象的元数据信息。"
weight: 360
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-stat-last-operation.md"
---

|列|类型|引用|说明|
|------|----|----------|-----------|
|`classid`|oid|pg_class.oid|包含此对象的系统目录的 OID。|
|`objid`|oid|任意 OID 列|此对象在其系统目录中的 OID。|
|`staactionname`|name| |对此对象执行的动作。|
|`stasysid`|oid|pg_authid.oid|引用 pg_authid.oid 的外键。|
|`stausename`|name| |对此对象执行操作的角色名称。|
|`stasubtype`|text| |操作的对象类型或所执行操作的子类型。|
|`statime`|timestamp with timezone| |操作的时间戳。此时间戳与写入 Apache Cloudberry 服务器日志文件的时间戳相同，可据此在日志中查找操作的更多详细信息。|

`pg_stat_last_operation` 表包含用于跟踪数据库对象操作的元数据信息。这些信息包括对象 ID、DDL 动作、用户、对象类型和操作时间戳。创建、修改、截断、清理、分析数据库对象或对其进行分区，以及授予对象权限时，Apache Cloudberry 都会更新此表。

要跟踪对特定对象执行的操作，请使用 `objid` 值。由于 `stasubtype` 值既可能标识操作的对象类型，也可能标识所执行操作的子类型，因此不适合作为查询 `pg_stat_last_operation` 表的参数。

以下示例创建并替换一个视图，然后演示如何使用 `objid` 作为参数查询 `pg_stat_last_operation` 表。

```sql
testdb=# CREATE VIEW trial AS SELECT * FROM gp_segment_configuration;

REATE VIEW

testdb=# CREATE OR REPLACE VIEW trial AS SELECT * FROM gp_segment_configuration;

CREATE VIEW

testdb=# SELECT * FROM pg_stat_last_operation WHERE objid='trial'::regclass::oid;

 classid | objid | staactionname | stasysid | stausename | stasubtype |            statime            
---------+-------+---------------+----------+------------+------------+-------------------------------
  1259  | 24735 | CREATE         |       10 | gpadmin    | VIEW       | 2020-04-07 16:44:28.808811+00
  1259  | 24735 | ALTER          |       10 | gpadmin    | SET        | 2020-04-07 16:44:38.110615+00
(2 rows)
```

请注意，视图的 `REPLACE` 操作在 `pg_stat_last_operation` 表中对应的条目指定了 `ALTER` 动作（`staactionname`）和 `SET` 子类型（`stasubtype`）。
