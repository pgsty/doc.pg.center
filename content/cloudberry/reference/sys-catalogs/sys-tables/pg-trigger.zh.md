---
title: "pg_trigger"
description: "`pg_trigger` 系统目录表存储表上的触发器。"
weight: 420
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-trigger.md"
---

> [!NOTE]
> Apache Cloudberry 不支持触发器。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID|
|`tgrelid`|oid|*pg_class.oid*<br/><br/>请注意，Apache Cloudberry 不强制实施参照完整性。|此触发器所在的表。|
| `tgparentid` | oid | *pg_trigger.oid* |此触发器所克隆的父触发器的 OID（例如，分区上的触发器）；如果不是克隆，则为零。|
|`tgname`|name| |触发器名称（在同一表的触发器中必须唯一）。|
|`tgfoid`|oid|*pg_proc.oid*<br/><br/>请注意，Apache Cloudberry 不强制实施参照完整性。|要调用的函数。|
|`tgtype`|smallint| |标识触发条件的位掩码。|
|`tgenabled`|char| |如果触发器已启用，则为 true。|
|`tgisinternal`|boolean| |如果触发器由内部生成，则为 true（通常用于实施 tgconstraint 标识的约束）。|
|`tgconstrrelid`|oid|*pg_class.oid*<br/><br/>请注意，Apache Cloudberry 不强制实施参照完整性。|参照完整性约束所引用的表。|
|`tgconstrindid`|oid|*pg_class.oid*|支持唯一约束、主键约束或参照完整性约束的索引。|
|`tgconstraint`|oid|*pg_constraint.oid*|与触发器关联的 `pg_constraint` 条目（如果有）。|
|`tgdeferrable`|boolean| |如果可延迟，则为 true。|
|`tginitdeferred`|boolean| |如果初始状态为延迟，则为 true。|
|`tgnargs`|smallint| |传递给触发器函数的参数字符串数量。|
|`tgattr`|ARRAY| |目前未使用。|
|`tgargs`|bytea| |传递给触发器的参数字符串，每个字符串以 NULL 结尾。|
|`tgqual`|pg_node_tree| |触发器 `WHEN` 条件的表达式树（以 `nodeToString()` 形式表示）；如果没有，则为 null。|
|`tgoldtable`|name| |旧过渡表的名称；如果没有，则为 NULL。|
|`tgnewtable`|name| |新过渡表的名称；如果没有，则为 NULL。|
