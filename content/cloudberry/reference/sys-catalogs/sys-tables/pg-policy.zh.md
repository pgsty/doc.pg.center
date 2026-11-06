---
title: "pg_policy"
description: "`pg_policy` 目录存储表的行级安全策略。"
weight: 250
upstream_link: "https://github.com/apache/cloudberry-site/blob/d4e372af8170f7e23d501b70deb3938efa1c978b/versioned_docs/version-2.x/sys-catalogs/sys-tables/pg-policy.md"
---

策略包含其适用的命令类型（可能是所有命令）、适用的角色、向涉及该表的查询添加的安全屏障限定表达式，以及向尝试在该表中添加新记录的查询添加的 `WITH CHECK` 选项表达式。

|列|类型|引用|说明|
|------|----|----------|-----------|
|`oid`|oid| |对象 ID。|
|`polname`|name| |策略名称。|
|`polerelid`|oid|pg_class.oid|策略适用的表。|
|`polcmd`|char| |策略适用的命令类型：`r` 表示 `SELECT`，`a` 表示 `INSERT`，`w` 表示 `UPDATE`，`d` 表示 `DELETE`，`*` 表示所有命令。|
|`polpermissive`|boolean| |策略是宽松型还是限制型。|
|`polroles`|ARRAY|pg_authid.oid |策略适用的角色。|
|`polqual`|pg_node_tree| |向使用此表的查询的安全屏障限定条件中添加的表达式树。|
|`polwithcheck`|pg_node_tree| |向尝试在此表中添加行的查询的 `WITH CHECK` 限定条件中添加的表达式树。|

> [!NOTE]
> 只有为表设置了 `pg_class.relrowsecurity` 时，Apache Cloudberry 才会应用 `pg_policy` 中存储的策略。
